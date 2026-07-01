# Phase 2 Report - Data Source Adapters

## Status

Done.

## Scope đã thực hiện

- Implement adapter interface chung với `load_raw`, `normalize`, và `write_interim_jsonl`.
- Thêm local-file adapters cho ViQuAD, ViWikiFC, ViFactCheck, và ViHSD.
- Bỏ `Manual CSV` và `Chinhphu.vn / official pages` khỏi Source Priority theo yêu cầu.
- Tạo JSONL fixture nhỏ cho các nguồn còn lại để không bị block khi chưa tải dataset thật.
- Normalize source items thành `data/interim/prompts_raw.jsonl`.
- Thêm validator CLI cho `source_items`.
- Thêm test cho JSONL source adapters và artifact đã build.

## Files đã tạo/sửa

- `configs/project.yaml`
- `data/raw/viquad_sample.jsonl`
- `data/raw/viwikifc_sample.jsonl`
- `data/raw/vifactcheck_sample.jsonl`
- `data/raw/vihsd_sample.jsonl`
- `data/interim/prompts_raw.jsonl`
- `src/vi_ppe/schemas.py`
- `src/vi_ppe/data_sources/__init__.py`
- `src/vi_ppe/data_sources/base.py`
- `src/vi_ppe/data_sources/viquad.py`
- `src/vi_ppe/data_sources/viwikifc.py`
- `src/vi_ppe/data_sources/vifactcheck.py`
- `src/vi_ppe/data_sources/vihsd.py`
- `scripts/01_build_sources.py`
- `scripts/03_validate_dataset.py`
- `tests/test_source_adapters.py`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/01_build_sources.py --config configs/project.yaml --limit-per-source 20
python scripts/03_validate_dataset.py --input data/interim/prompts_raw.jsonl --type source_items
python scripts/00_smoke_check.py
pytest -q
```

## Kết quả test

- Build sources: pass, tạo 20 source items từ các nguồn JSONL đã cấu hình: 5 `viquad`, 5 `viwikifc`, 5 `vifactcheck`, 5 `vihsd`.
- Validate source items: pass, `OK: validated 20 source_items records`.
- Smoke check: pass.
- Pytest: pass, `8 passed in 0.05s`.

## Acceptance Criteria

- [x] Có provenance.
- [x] Có license note.
- [x] Adapter JSONL local cho nguồn đã cấu hình chạy được.

## Blocker

Không có blocker. Các adapter ViQuAD/ViWikiFC/ViFactCheck/ViHSD hiện hỗ trợ local JSONL để giữ pipeline offline; khi có dataset thật chỉ cần trỏ path trong config.

## Revision sau yêu cầu người dùng

- Đã bỏ `Manual CSV` khỏi Source Priority, config, adapter registry, tests, raw data và generated interim data.
- Đã bỏ `Chinhphu.vn / official pages` khỏi Source Priority.
- `data/interim/prompts_raw.jsonl` đã được regenerate, không còn `manual_csv`, `manual_seed` hoặc `manual_sources`.

## Kết luận

Phase 2 đủ điều kiện chuyển sang Phase 3.
