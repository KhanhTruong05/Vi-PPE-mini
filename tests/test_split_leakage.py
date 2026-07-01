from pathlib import Path

from vi_ppe.io import read_jsonl
from vi_ppe.split_dataset import split_reviewed_pairs, validate_no_source_leakage, write_manifest


def test_split_reviewed_pairs_has_no_source_leakage():
    pairs = read_jsonl("data/processed/pairs_reviewed.jsonl")
    dev, test = split_reviewed_pairs(pairs, dev_ratio=0.2, seed=42)
    validate_no_source_leakage(dev, test)
    assert dev
    assert test
    assert all(pair["review_status"] == "reviewed" for pair in dev + test)


def test_manifest_records_hashes(tmp_path: Path):
    paths = [
        Path("data/processed/pairs_dev.jsonl"),
        Path("data/processed/pairs_test.jsonl"),
        Path("data/processed/bias_subset.jsonl"),
    ]
    if not all(path.exists() for path in paths):
        return
    manifest = write_manifest(paths, tmp_path / "manifest.json")
    assert len(manifest["files"]) == 3
    assert all(entry["sha256"] for entry in manifest["files"])
