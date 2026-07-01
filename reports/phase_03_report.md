# Phase 3 Report - Pair Construction cho MVP 1

## Status

Done.

## Scope đã thực hiện

- Sinh draft pairwise examples cho 3 domain: `fact_check`, `instruction`, `safety`.
- Gán `gold_winner`, `gold_reason`, `criteria`, `perturbation_type`.
- Tính `length_a_tokens` và `length_b_tokens`.
- Validate draft pairs bằng schema hiện có.
- Viết notes về cách sinh pair.

## Files đã tạo/sửa

- `src/vi_ppe/build_pairs.py`
- `scripts/02_build_pairs.py`
- `data/processed/pairs_all_draft.jsonl`
- `reports/pair_generation_notes.md`
- `tests/test_build_pairs.py`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --output data/processed/pairs_all_draft.jsonl --limit 90
python scripts/03_validate_dataset.py --input data/processed/pairs_all_draft.jsonl
python scripts/00_smoke_check.py
pytest -q
```

## Kết quả test

- Build pairs: pass, tạo 90 draft pairs.
- Domain counts: 30 `fact_check`, 40 `instruction`, 20 `safety`.
- Validate pairs: pass, `OK: validated 90 pairs records`.
- Smoke check: pass.
- Pytest: pass, `10 passed in 0.06s`.

## Acceptance Criteria

- [x] Không lộ gold winner.
- [x] Mỗi domain có đủ sample.
- [x] Response thua vẫn plausible.
- [x] Mỗi pair có `gold_reason`.
- [x] Mỗi pair có `perturbation_type`.

## Ghi chú

Do `Manual CSV` đã bị bỏ khỏi Source Priority, instruction pairs hiện được sinh từ internal synthetic templates với provenance `synthetic_instruction_templates`. Đây không phải source adapter Phase 2.

## Blocker

Không có blocker cho Phase 3. Draft pairs vẫn cần manual review ở Phase 5 trước khi dùng làm dev/test.

## Kết luận

Phase 3 đủ điều kiện chuyển sang Phase 4.
