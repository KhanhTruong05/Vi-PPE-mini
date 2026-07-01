from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vi_ppe.config import load_project_config
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import DOMAINS, validate_pairs


def main() -> int:
    cfg = load_project_config(ROOT / "configs" / "project.yaml")
    smoke_path = ROOT / cfg["dataset"]["smoke_pairs"]
    pairs = read_jsonl(smoke_path)
    validate_pairs(pairs)

    observed_domains = {pair["domain"] for pair in pairs}
    if observed_domains != DOMAINS:
        raise AssertionError(f"Smoke dataset domains mismatch: {observed_domains} != {DOMAINS}")

    counts = {domain: sum(1 for pair in pairs if pair["domain"] == domain) for domain in DOMAINS}
    if any(count != 2 for count in counts.values()):
        raise AssertionError(f"Expected exactly 2 smoke pairs per domain, got {counts}")

    print("OK: scaffold and smoke data are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
