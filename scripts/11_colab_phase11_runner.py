from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run_command(args: list[str]) -> None:
    print("\n$ " + " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def load_runs(config_path: Path, include_optional: bool) -> list[dict[str, Any]]:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    runs = list(cfg.get("runs", []))
    if include_optional:
        runs.extend(cfg.get("optional_runs", []))
    return runs


def preflight(required_datasets: list[str]) -> None:
    print("Phase 11 Colab preflight")
    print(f"repo_root={ROOT}")
    run_command(["nvidia-smi"])
    for dataset in sorted(set(required_datasets)):
        path = ROOT / dataset
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset: {path}")
        print(f"OK dataset: {dataset}")
    run_command([sys.executable, "scripts/00_smoke_check.py"])
    run_command([sys.executable, "-m", "pytest", "-q"])


def run_inference(run: dict[str, Any], limit: int | None) -> None:
    cmd = [
        sys.executable,
        "scripts/05_run_judge.py",
        "--dataset",
        run["dataset"],
        "--model",
        run["model"],
        "--template",
        run["template"],
        "--run-id",
        run["run_id"],
        "--resume",
    ]
    effective_limit = limit if limit is not None else run.get("limit")
    if effective_limit is not None:
        cmd.extend(["--limit", str(effective_limit)])
    run_command(cmd)


def run_metrics(run: dict[str, Any]) -> None:
    cmd = [
        sys.executable,
        "scripts/06_compute_metrics.py",
        "--judgments",
        f"results/judgments/{run['run_id']}.jsonl",
        "--dataset",
        run["dataset"],
        "--run-id",
        run["run_id"],
    ]
    if run.get("bias", False):
        cmd.append("--bias")
    run_command(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 11 experiment matrix on Colab A100.")
    parser.add_argument("--config", default="configs/final_runs.yaml")
    parser.add_argument("--include-optional", action="store_true")
    parser.add_argument("--only-run", default=None, help="Run only one run_id from the matrix.")
    parser.add_argument("--limit", type=int, default=None, help="Limit pairs per run for smoke testing.")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--skip-inference", action="store_true")
    parser.add_argument("--skip-metrics", action="store_true")
    args = parser.parse_args()

    runs = load_runs(ROOT / args.config, args.include_optional)
    if args.only_run:
        runs = [run for run in runs if run["run_id"] == args.only_run]
        if not runs:
            raise ValueError(f"Run id not found in matrix: {args.only_run}")

    if not args.skip_preflight:
        preflight([run["dataset"] for run in runs])

    for run in runs:
        print(f"\n=== {run['run_id']} ===", flush=True)
        if not args.skip_inference:
            run_inference(run, args.limit)
        if not args.skip_metrics:
            run_metrics(run)

    print("\nPhase 11 runner finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
