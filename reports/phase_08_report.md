# Phase 8 Report - Judge Inference Engine

## Status

Done for local mock inference. Real model inference is prepared but not run locally.

## Scope đã thực hiện

- Implement mock backend.
- Implement HF local backend for Colab/GPU.
- Implement robust JSON judgment parser.
- Implement judge runner with AB/BA orders and `--resume`.
- Run local mock smoke inference.
- Add minimal metric command for Phase 8 smoke validation.

## Files đã tạo/sửa

- `configs/models.yaml`
- `src/vi_ppe/judge_backends/__init__.py`
- `src/vi_ppe/judge_backends/mock.py`
- `src/vi_ppe/judge_backends/hf_local.py`
- `src/vi_ppe/parse_judgment.py`
- `src/vi_ppe/run_judge.py`
- `scripts/05_run_judge.py`
- `src/vi_ppe/aggregate_swaps.py`
- `src/vi_ppe/metrics.py`
- `scripts/06_compute_metrics.py`
- `tests/test_parse_judgment.py`
- `results/judgments/smoke_mock.jsonl`
- `results/metrics/smoke_mock_summary.json`
- `results/metrics/smoke_mock_pair_results.jsonl`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/05_run_judge.py --dataset data/samples/smoke_pairs.jsonl --backend mock --template baseline_generic_vi --run-id smoke_mock
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_parse_judgment.py
pytest -q
```

## Kết quả test

- Mock judge wrote 12 judgments for 6 pairs x AB/BA.
- Parse success rate: 1.0.
- Smoke pairwise accuracy: 1.0.
- Full pytest: pass, `23 passed in 0.14s`.

## Acceptance Criteria

- [x] Mock local pass.
- [x] Real inference chỉ chạy trên Colab A100/GPU tương đương.
- [x] Mỗi pair có AB và BA.
- [x] Parse success được báo cáo.

## Colab Command Prepared

```bash
python scripts/05_run_judge.py --dataset data/processed/pairs_dev.jsonl --model qwen25_3b --template baseline_generic_vi --run-id qwen25_3b_baseline_dev --resume
```

## Ghi chú

`scripts/06_compute_metrics.py` được thêm sớm để Phase 8 smoke test chạy được. Phase 9 sẽ mở rộng và chuẩn hóa metrics.

## Kết luận

Phase 8 đủ điều kiện chuyển sang Phase 9.

## Cập nhật inference engine dùng trong V5

- HF backend hỗ trợ batched inference, padding và decode riêng từng prompt.
- Runner giữ AB/BA, JSONL append và `--resume` để tiếp tục sau khi Colab mất kết nối.
- V5 chạy BF16, không quantize, deterministic decoding trên Colab A100.
- Các model: Qwen2.5-3B, Qwen2.5-7B, Gemma-3-4B-IT và Llama-3.1-8B-Instruct.
- Mỗi core run có `503 x 2 = 1006` judgments; mỗi bias run có `300 x 2 = 600` judgments.

Không có real-model inference nào được chạy trong Codex/local CPU.
