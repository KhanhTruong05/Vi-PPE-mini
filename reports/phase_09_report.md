# Phase 9 Report - Swap Aggregation và Core Metrics

## Status

Done.

## Scope đã thực hiện

- Map BA judgments về original A/B space.
- Aggregate AB/BA thành final winner.
- Tính pairwise accuracy, domain accuracy, macro accuracy, lower-bound domain score.
- Tính swap consistency, parse success, missing judgments, inconsistent count, invalid count.
- Thêm position-bias raw winner counts.
- Thêm tests cho gold tie exclusion và inconsistent swap.

## Files đã tạo/sửa

- `src/vi_ppe/aggregate_swaps.py`
- `src/vi_ppe/metrics.py`
- `scripts/06_compute_metrics.py`
- `tests/test_metrics.py`
- `results/metrics/smoke_mock_summary.json`
- `results/metrics/smoke_mock_pair_results.jsonl`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_metrics.py
pytest -q
```

## Kết quả test

- Smoke metrics generated.
- Parse success rate: 1.0.
- Pairwise accuracy: 1.0 on mock smoke.
- Macro accuracy: 1.0 on mock smoke.
- Swap consistency: 1.0 on mock smoke.
- Metrics tests: pass.
- Full pytest: pass, `27 passed in 0.16s`.

## Acceptance Criteria

- [x] Gold tie không tính core accuracy.
- [x] Inconsistent swap báo cáo riêng.
- [x] Summary JSON được tạo.

## Ghi chú

Metric outputs hiện dùng `smoke_mock` để validate local. Khi có real model judgments, chạy cùng command với file judgments tương ứng.

## Kết luận

Phase 9 đủ điều kiện chuyển sang Phase 10.
