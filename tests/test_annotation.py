from pathlib import Path

from vi_ppe.annotation import dataset_qa_report, export_annotation_sheet, import_annotations
from vi_ppe.io import read_jsonl


def test_export_import_annotations_roundtrip(tmp_path: Path):
    sheet = tmp_path / "annotation_sheet.csv"
    reviewed = tmp_path / "pairs_reviewed.jsonl"
    count = export_annotation_sheet("data/processed/pairs_all_draft.jsonl", sheet, sample=5)
    assert count == 5
    stats = import_annotations(sheet, "data/processed/pairs_all_draft.jsonl", reviewed)
    pairs = read_jsonl(reviewed)
    assert stats["reviewed"] == 5
    assert sum(1 for pair in pairs if pair["review_status"] == "reviewed") == 5


def test_dataset_qa_report_has_counts():
    pairs = read_jsonl("data/processed/pairs_all_draft.jsonl")
    report = dataset_qa_report(pairs)
    assert report["total_pairs"] == len(pairs)
    assert "domain_counts" in report
    assert "perturbation_counts" in report
