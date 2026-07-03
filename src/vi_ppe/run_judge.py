from __future__ import annotations

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from vi_ppe.config import load_project_config
from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.judge_backends.hf_local import HfLocalBackend
from vi_ppe.judge_backends.mock import MockJudgeBackend
from vi_ppe.parse_judgment import parse_judgment
from vi_ppe.prompt_render import load_prompt_template, render_prompt


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_models_config(path: str | Path = "configs/models.yaml") -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_backend(backend_name: str | None, model_name: str | None):
    if backend_name == "mock" or (backend_name is None and model_name in {None, "mock"}):
        return MockJudgeBackend(), {"model_id": "mock", "backend": "mock"}
    cfg = load_models_config()
    if not model_name or model_name not in cfg["models"]:
        raise ValueError(f"Unknown model: {model_name}")
    model_cfg = cfg["models"][model_name]
    if model_cfg.get("backend") != "hf_local":
        raise ValueError(f"Unsupported backend for model {model_name}: {model_cfg.get('backend')}")
    return HfLocalBackend(model_cfg), model_cfg


def existing_judgment_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["judgment_id"] for row in read_jsonl(path)}


def run_judge(
    *,
    dataset_path: str | Path,
    template_name: str,
    run_id: str,
    backend_name: str | None = None,
    model_name: str | None = None,
    orders: list[str] | None = None,
    resume: bool = False,
    limit: int | None = None,
    output_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    orders = orders or ["AB", "BA"]
    dataset_path = Path(dataset_path)
    output = Path(output_path or f"results/judgments/{run_id}.jsonl")
    output.parent.mkdir(parents=True, exist_ok=True)
    pairs = read_jsonl(dataset_path)
    if limit is not None:
        pairs = pairs[:limit]
    backend, model_cfg = build_backend(backend_name, model_name)
    skip_ids = existing_judgment_ids(output) if resume else set()
    new_rows: list[dict[str, Any]] = []
    all_rows = read_jsonl(output) if resume and output.exists() else []
    dataset_hash = sha256_file(dataset_path)
    config_hash = sha256_text(str(model_cfg))
    batch_size = max(1, int(model_cfg.get("batch_size", 1)))
    jobs: list[dict[str, Any]] = []

    for pair in pairs:
        for order in orders:
            judgment_id = f"{run_id}_{pair['pair_id']}_{order.lower()}"
            if judgment_id in skip_ids:
                continue
            prompt = render_prompt(pair, template_name, order)
            jobs.append(
                {
                    "pair": pair,
                    "order": order,
                    "judgment_id": judgment_id,
                    "prompt": prompt,
                }
            )

    def append_row(job: dict[str, Any], raw_output: str, latency: float) -> None:
        pair = job["pair"]
        parsed = parse_judgment(raw_output)
        row = {
            "judgment_id": job["judgment_id"],
            "run_id": run_id,
            "pair_id": pair["pair_id"],
            "order": job["order"],
            "judge_model": model_cfg["model_id"],
            "backend": model_cfg.get("backend", backend_name or "mock"),
            "prompt_template": template_name,
            "prompt_hash": sha256_text(load_prompt_template(template_name if template_name != "auto_criteria_by_domain" else "criteria_fact_check_vi")),
            "dataset_hash": dataset_hash,
            "config_hash": config_hash,
            "raw_output": raw_output,
            "parsed": parsed,
            "parse_status": parsed["parse_status"],
            "latency_sec": round(latency, 4),
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "hardware_note": "local mock" if model_cfg["model_id"] == "mock" else "Colab A100 or equivalent required",
        }
        all_rows.append(row)
        new_rows.append(row)

    for start_index in range(0, len(jobs), batch_size):
        batch = jobs[start_index : start_index + batch_size]
        prompts = [job["prompt"] for job in batch]
        started = time.perf_counter()
        if batch_size > 1 and hasattr(backend, "generate_batch"):
            try:
                raw_outputs = backend.generate_batch(
                    prompts,
                    pairs=[job["pair"] for job in batch],
                    orders=[job["order"] for job in batch],
                )
                if len(raw_outputs) != len(batch):
                    raise ValueError(f"batch returned {len(raw_outputs)} outputs for {len(batch)} prompts")
                latency = (time.perf_counter() - started) / max(1, len(batch))
                for job, raw_output in zip(batch, raw_outputs):
                    append_row(job, raw_output, latency)
                continue
            except Exception:
                if len(batch) == 1:
                    raise

        for job in batch:
            started = time.perf_counter()
            raw_output = backend.generate(job["prompt"], pair=job["pair"], order=job["order"])
            latency = time.perf_counter() - started
            append_row(job, raw_output, latency)

    write_jsonl(output, all_rows)
    return new_rows
