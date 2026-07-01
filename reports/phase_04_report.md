# Phase 4 Report - Controlled Bias Subset cho MVP 2

## Status

Done.

## Scope đã thực hiện

- Tạo controlled bias subset draft.
- Gắn `diagnostic_subset = true` cho toàn bộ bias pairs.
- Gắn `bias_hypothesis` cho từng pair.
- Thêm validator cho bias fields.
- Tạo guideline cho bias subset.

## Files đã tạo/sửa

- `src/vi_ppe/bias_pair_builders.py`
- `src/vi_ppe/schemas.py`
- `scripts/02_build_pairs.py`
- `scripts/03_validate_dataset.py`
- `data/processed/bias_subset_draft.jsonl`
- `reports/bias_subset_guideline.md`
- `tests/test_bias_pair_builders.py`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/02_build_pairs.py --bias-only --output data/processed/bias_subset_draft.jsonl --limit 60
python scripts/03_validate_dataset.py --input data/processed/bias_subset_draft.jsonl --require-bias-fields
python scripts/00_smoke_check.py
pytest -q
```

## Kết quả test

- Build bias subset: pass, tạo 60 draft pairs.
- Domain counts: 45 `fact_check`, 10 `instruction`, 5 `safety`.
- Perturbation counts:
  - 15 `concise_correct_vs_verbose_wrong`
  - 15 `same_content_different_length`
  - 15 `plain_style_vs_polished_style`
  - 10 `instruction_following_vs_over_elaboration`
  - 5 `appropriate_refusal_vs_verbose_moralizing`
- Validate bias fields: pass.
- Delta length distribution: 23 `A_longer`, 37 `B_longer`.
- Pytest: pass, `12 passed in 0.06s`.

## Acceptance Criteria

- [x] Có field length/style.
- [x] Có perturbation type.
- [x] Pair tie không tính vào core accuracy.
- [x] Mỗi bias pair có `bias_hypothesis`.

## Blocker

Không có blocker cho draft local. Theo plan, target cuối cần 150-200 high-control pairs được manual review trước final; hiện Phase 4 user test yêu cầu `--limit 60`, nên artifact này là draft smoke/subset.

## Kết luận

Phase 4 đủ điều kiện chuyển sang Phase 5.
