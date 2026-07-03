import csv
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
    assert stats["missing_annotation"] == 5
    assert sum(1 for pair in pairs if pair["review_status"] == "reviewed") == 0


def test_import_annotations_requires_explicit_human_fields(tmp_path: Path):
    sheet = tmp_path / "annotation_sheet.csv"
    reviewed = tmp_path / "pairs_reviewed.jsonl"
    export_annotation_sheet("data/processed/pairs_all_draft.jsonl", sheet, sample=1, include_draft_labels=True)
    with sheet.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())
    rows[0]["annotator_winner"] = "A"
    rows[0]["annotator_reason"] = "A được annotator xác nhận là tốt hơn theo rubric."
    with sheet.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    stats = import_annotations(sheet, "data/processed/pairs_all_draft.jsonl", reviewed)
    pairs = read_jsonl(reviewed)
    assert stats["reviewed"] == 1
    assert sum(1 for pair in pairs if pair["review_status"] == "reviewed") == 1


def test_dataset_qa_report_has_counts():
    pairs = read_jsonl("data/processed/pairs_all_draft.jsonl")
    report = dataset_qa_report(pairs)
    assert report["total_pairs"] == len(pairs)
    assert "domain_counts" in report
    assert "perturbation_counts" in report
