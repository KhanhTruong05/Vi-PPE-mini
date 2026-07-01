# Phase 0 Report - Scope Freeze và Project Scaffold

## Status

Done.

## Scope đã thực hiện

- Tạo cấu trúc repo cho Vi-PPE-mini.
- Tạo `requirements.txt`.
- Tạo `configs/project.yaml`.
- Tạo smoke dataset 6 cặp toy examples, mỗi domain 2 cặp.
- Tạo script smoke check.
- Tạo README quickstart.
- Tạo module tối thiểu cho config, JSONL IO và schema validation.
- Tạo test schema cơ bản.

## Files đã tạo/sửa

- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `configs/project.yaml`
- `data/raw/README.md`
- `data/samples/smoke_pairs.jsonl`
- `src/vi_ppe/__init__.py`
- `src/vi_ppe/config.py`
- `src/vi_ppe/io.py`
- `src/vi_ppe/schemas.py`
- `scripts/00_smoke_check.py`
- `tests/test_schemas.py`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/00_smoke_check.py
pytest -q
```

## Kết quả test

- `python scripts/00_smoke_check.py`: pass, in `OK: scaffold and smoke data are valid`.
- `pytest -q`: pass, `3 passed in 0.06s`.

## Acceptance Criteria

- [x] Smoke check pass.
- [x] Pytest pass.
- [x] Chưa cần GPU.

## Blocker

Không có blocker.

## Kết luận

Phase 0 đủ điều kiện chuyển sang Phase 1.

