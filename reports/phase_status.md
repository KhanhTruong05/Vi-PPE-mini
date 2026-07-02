# Phase Status

File này là bảng theo dõi nhanh. Chi tiết từng phase nằm ở các file
`reports/phase_XX_report.md`.

| Phase | Tên phase | Status | Report | Ghi chú |
|---|---|---|---|---|
| 0 | Scope Freeze và Project Scaffold | done | `reports/phase_00_report.md` | Smoke check và pytest pass |
| 1 | Rubric, Schema và Annotation Guideline | done | `reports/phase_01_report.md` | Smoke check và schema tests pass |
| 2 | Data Source Adapters | done | `reports/phase_02_report.md` | Real HF sample imported from 3 sources |
| 3 | Pair Construction cho MVP 1 | done | `reports/phase_03_report.md` | 90 draft pairs regenerated from real HF sample |
| 4 | Controlled Bias Subset cho MVP 2 | done | `reports/phase_04_report.md` | 60 bias draft pairs regenerated from real HF sample |
| 5 | Annotation, Review và Dataset QA | done | `reports/phase_05_report.md` | Bootstrap review and QA regenerated |
| 6 | Split, Freeze và Manifest | done | `reports/phase_06_report.md` | Local frozen splits, manifest, and dataset card pass |
| 7 | Judge Prompt Templates | done | `reports/phase_07_report.md` | Prompt templates and renderer pass |
| 8 | Judge Inference Engine | done | `reports/phase_08_report.md` | Mock local inference, parser, resume scaffold pass |
| 9 | Swap Aggregation và Core Metrics | done | `reports/phase_09_report.md` | Core metrics and swap aggregation pass |
| 10 | Bias Metrics | done | `reports/phase_10_report.md` | Bias summary and figures generated from local mock run |
| 11 | Experiment Matrix | not_started | `reports/final_colab_commands.md` | Final dataset v2 prepared; real inference cần Colab A100 |
| 12 | Error Analysis và Charts | not_started |  |  |
| 13 | Report, Reproducibility và Packaging | not_started |  |  |
| 14 | Optional LoRA/QLoRA SFT Branch | not_started |  | Chỉ làm nếu core đã xong và có Colab A100 |
