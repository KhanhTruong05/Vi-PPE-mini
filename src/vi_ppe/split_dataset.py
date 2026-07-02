from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vi_ppe.io import read_jsonl, write_jsonl
from vi_ppe.schemas import validate_bias_pairs, validate_pairs


def reviewed_only(pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [pair for pair in pairs if pair.get("review_status") == "reviewed"]


def group_pairs(pairs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        key = pair.get("source_example_id") or pair["pair_id"]
        groups[key].append(pair)
    return dict(groups)


def group_signature(group: list[dict[str, Any]]) -> tuple[str, str]:
    domains = Counter(pair["domain"] for pair in group)
    perturbations = Counter(pair["perturbation_type"] for pair in group)
    return domains.most_common(1)[0][0], perturbations.most_common(1)[0][0]


def split_reviewed_pairs(
    pairs: list[dict[str, Any]], dev_ratio: float = 0.2, seed: int = 42
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    clean = reviewed_only(pairs)
    validate_pairs(clean)

    strata: dict[tuple[str, str], list[list[dict[str, Any]]]] = defaultdict(list)
    for group in group_pairs(clean).values():
        strata[group_signature(group)].append(group)

    rng = random.Random(seed)
    dev: list[dict[str, Any]] = []
    test: list[dict[str, Any]] = []
    for groups in strata.values():
        rng.shuffle(groups)
        dev_group_count = max(1, round(len(groups) * dev_ratio)) if len(groups) > 1 else 0
        for index, group in enumerate(groups):
            target = dev if index < dev_group_count else test
            for pair in group:
                frozen = {**pair, "split": "dev" if target is dev else "test"}
                target.append(frozen)

    if not dev and test:
        moved = test.pop(0)
        moved["split"] = "dev"
        dev.append(moved)
    if not test and dev:
        moved = dev.pop()
        moved["split"] = "test"
        test.append(moved)

    validate_no_source_leakage(dev, test)
    validate_pairs(dev)
    validate_pairs(test)
    return dev, test


def freeze_bias_subset(pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clean = reviewed_only(pairs)
    frozen = [{**pair, "split": "bias"} for pair in clean]
    validate_bias_pairs(frozen)
    return frozen


def validate_no_source_leakage(dev: list[dict[str, Any]], test: list[dict[str, Any]]) -> None:
    dev_sources = {pair.get("source_example_id") for pair in dev}
    test_sources = {pair.get("source_example_id") for pair in test}
    overlap = sorted(source for source in dev_sources & test_sources if source)
    if overlap:
        raise ValueError(f"source_example_id leakage between dev/test: {overlap[:10]}")


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_jsonl(path: str | Path) -> int:
    return len(read_jsonl(path))


def write_manifest(paths: list[str | Path], output_path: str | Path) -> dict[str, Any]:
    manifest = {
        "schema_version": "v1",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "files": [],
    }
    root = Path.cwd().resolve()
    for path in paths:
        resolved = Path(path).resolve()
        try:
            manifest_path = resolved.relative_to(root)
        except ValueError:
            manifest_path = Path(path)
        manifest["files"].append(
            {
                "path": str(manifest_path).replace("\\", "/"),
                "sha256": sha256_file(path),
                "num_records": count_jsonl(path),
            }
        )
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def write_dataset_card(
    *,
    output_path: str | Path,
    dev: list[dict[str, Any]],
    test: list[dict[str, Any]],
    bias: list[dict[str, Any]],
    manifest_path: str | Path,
) -> None:
    all_core = dev + test
    source_counts = Counter(pair["source_dataset"] for pair in all_core + bias)
    domain_counts = Counter(pair["domain"] for pair in all_core)
    split_counts = {"dev": len(dev), "test": len(test), "bias": len(bias)}
    perturbation_counts = Counter(pair["perturbation_type"] for pair in all_core + bias)
    try:
        manifest_display_path = Path(manifest_path).resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        manifest_display_path = Path(manifest_path).as_posix()

    lines = [
        "# Dataset Card: Vi-PPE-mini",
        "",
        "## Status",
        "",
        "Frozen local sample built from reviewed/bootstrap-reviewed records. This is suitable for pipeline validation; final thesis runs still require larger human-reviewed data.",
        "",
        "## Sources",
        "",
        "- `taidng/UIT-ViQuAD2.0` via `viquad` adapter.",
        "- `tranthaihoa/vifactcheck` via `vifactcheck` adapter.",
        "- `ura-hcmut/UIT-ViHSD` via `vihsd` adapter.",
        "- `synthetic_instruction_templates` for instruction-following pairs.",
        "- `manual_safety_templates` for controlled safety/refusal pairs.",
        "",
        "## Counts",
        "",
        f"- Split counts: {split_counts}",
        f"- Core domain counts: {dict(domain_counts)}",
        f"- Source counts: {dict(source_counts)}",
        f"- Perturbation counts: {dict(perturbation_counts)}",
        "",
        "## License And Provenance Notes",
        "",
        "- Keep upstream license notes from each record before redistribution.",
        "- `tranthaihoa/vifactcheck` dataset card lists MIT.",
        "- `ura-hcmut/UIT-ViHSD` requires careful review of use restrictions before redistribution.",
        "- `taidng/UIT-ViQuAD2.0` license should be verified before redistribution.",
        "",
        "## Manifest",
        "",
        f"See `{manifest_display_path}` for SHA256 hashes and record counts.",
    ]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
