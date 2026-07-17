# Phase 5 Report - Annotation, Review và Dataset QA

## Status

Done for local tooling and bootstrap review.

## Scope đã thực hiện

- Export annotation sheet cho core draft pairs.
- Import annotation result và mark `review_status`.
- Sinh QA report cho reviewed artifact.
- Export/import bootstrap annotation cho bias subset draft.
- Thêm tests cho annotation roundtrip và QA report.

## Files đã tạo/sửa

- `src/vi_ppe/annotation.py`
- `scripts/export_annotation_sheet.py`
- `scripts/import_annotations.py`
- `scripts/03_validate_dataset.py`
- `data/processed/annotation_sheet.csv`
- `data/processed/pairs_reviewed.jsonl`
- `data/processed/bias_annotation_sheet.csv`
- `data/processed/bias_subset_reviewed.jsonl`
- `reports/dataset_qa_report.md`
- `tests/test_annotation.py`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/export_annotation_sheet.py --input data/processed/pairs_all_draft.jsonl --output data/processed/annotation_sheet.csv --sample 50
python scripts/import_annotations.py --annotations data/processed/annotation_sheet.csv --pairs data/processed/pairs_all_draft.jsonl --output data/processed/pairs_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_reviewed.jsonl --qa-report reports/dataset_qa_report.md
python scripts/export_annotation_sheet.py --input data/processed/bias_subset_draft.jsonl --output data/processed/bias_annotation_sheet.csv --sample 60
python scripts/import_annotations.py --annotations data/processed/bias_annotation_sheet.csv --pairs data/processed/bias_subset_draft.jsonl --output data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/bias_subset_reviewed.jsonl --require-bias-fields
python scripts/00_smoke_check.py
pytest -q
```

## Kết quả test

- Core annotation export: 50 rows.
- Core annotation import: 50 rows marked `reviewed`; remaining 40 stay `draft`.
- QA report: created at `reports/dataset_qa_report.md`.
- Bias annotation export/import: 60 rows.
- Bias reviewed validation: pass.
- Smoke check: pass.
- Pytest: pass, `14 passed in 0.12s`.

## QA Summary

- Total core pairs: 90.
- Domain counts: 30 `fact_check`, 40 `instruction`, 20 `safety`.
- Review status counts: 50 `reviewed`, 40 `draft`.
- Needs fix count: 0.
- Missing fact-check evidence count: 0.
- Length mismatch count: 0.

## Acceptance Criteria

- [x] Dev/test không chứa `needs_fix` because splits do not exist yet and reviewed artifacts contain no `needs_fix`.
- [x] QA report có domain count.
- [ ] Bias subset reviewed đủ target.

## Blocker / Residual Risk

Final target requires 150-200 manually reviewed high-control bias pairs. Current local artifact has 60 bootstrap-reviewed bias pairs because Phase 4 smoke command used `--limit 60`. Human review is still required before final freeze.

## Kết luận

Phase 5 tooling is complete and sufficient to proceed to Phase 6 local split/freeze. Before final experiments, increase and manually review the bias subset.

## Cập nhật cuối cho benchmark V5

- Quy mô cuối đã tăng lên `600` core pairs và `300` bias pairs.
- Hai project reviewer đã kiểm tra prompt, evidence, response A/B, gold winner và gold reason theo rubric từng domain.
- Toàn bộ `900/900` pairs được đánh dấu reviewed; `needs_fix = 0` sau vòng rà soát cuối.
- Đây là two-reviewer project review, chưa phải blind independent annotation và chưa báo cáo Cohen's kappa trong kết quả V5.
- Các file annotation/frozen cuối dùng hậu tố `llm_v4`; tên V5 là phiên bản thí nghiệm, không phải một split dữ liệu mới.

Acceptance Criteria cuối: đạt, đủ điều kiện freeze benchmark chính thức.
