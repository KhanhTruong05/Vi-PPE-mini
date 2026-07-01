# Phase 1 Report - Rubric, Schema và Annotation Guideline

## Status

Done.

## Scope đã thực hiện

- Mở rộng rubric cho `fact_check`, `instruction`, và `safety`.
- Mỗi domain có 5 criteria theo implementation plan.
- Cập nhật schema để validate criteria đúng domain.
- Thêm helper cho tie policy: `gold_winner = "tie"` hợp lệ nhưng không tính core accuracy.
- Viết annotation guideline bằng tiếng Việt.
- Thêm test rubric coverage và tie handling.

## Files đã tạo/sửa

- `configs/project.yaml`
- `src/vi_ppe/schemas.py`
- `tests/test_schemas.py`
- `reports/annotation_guideline.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/00_smoke_check.py
pytest -q tests/test_schemas.py
```

## Kết quả test

- `python scripts/00_smoke_check.py`: pass, in `OK: scaffold and smoke data are valid`.
- `pytest -q tests/test_schemas.py`: pass, `6 passed in 0.05s`.

## Acceptance Criteria

- [x] Rubric đủ rõ.
- [x] Criteria đúng domain.
- [x] Có quy tắc tie.

## Blocker

Không có blocker.

## Kết luận

Phase 1 đủ điều kiện chuyển sang Phase 2.

