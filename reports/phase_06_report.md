# Phase 6 Report - Split, Freeze và Manifest

## Status

Done for local frozen sample.

## Scope đã thực hiện

- Split reviewed core pairs thành dev/test theo group `source_example_id`.
- Freeze reviewed bias subset.
- Kiểm tra leakage theo `source_example_id`.
- Tạo manifest SHA256.
- Viết dataset card.

## Files đã tạo/sửa

- `src/vi_ppe/split_dataset.py`
- `scripts/04_split_freeze.py`
- `scripts/03_validate_dataset.py`
- `tests/test_split_leakage.py`
- `data/processed/pairs_dev.jsonl`
- `data/processed/pairs_test.jsonl`
- `data/processed/bias_subset.jsonl`
- `data/processed/dataset_manifest.json`
- `reports/dataset_card.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/04_split_freeze.py --input data/processed/pairs_reviewed.jsonl --bias data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_dev.jsonl --check-split
python scripts/03_validate_dataset.py --input data/processed/pairs_test.jsonl --check-split
pytest -q tests/test_split_leakage.py
pytest -q
```

## Kết quả test

- Dev split: 11 records.
- Test split: 39 records.
- Bias subset: 60 records.
- Dev validation: pass.
- Test validation: pass.
- Leakage tests: pass.
- Full pytest: pass, `16 passed in 0.11s`.

## Acceptance Criteria

- [x] Không leakage theo `source_example_id`.
- [x] Manifest có sha256.
- [x] Dataset card có source/license.

## Blocker / Residual Risk

Không có blocker cho pipeline local. Dataset hiện vẫn là frozen sample nhỏ vì Phase 5 mới bootstrap-reviewed 50 core rows và 60 bias rows. Trước final experiment cần tăng số lượng và human review.

## Kết luận

Phase 6 đủ điều kiện chuyển sang Phase 7.
