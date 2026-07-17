# Trạng thái các phase

| Phase | Nội dung | Trạng thái | Báo cáo |
|---:|---|---|---|
| 0 | Scope Freeze và Project Scaffold | Hoàn thành | `reports/phase_00_report.md` |
| 1 | Rubric, Schema và Annotation Guideline | Hoàn thành | `reports/phase_01_report.md` |
| 2 | Data Source Adapters | Hoàn thành | `reports/phase_02_report.md` |
| 3 | Core Pair Construction | Hoàn thành | `reports/phase_03_report.md` |
| 4 | Controlled Bias Subset | Hoàn thành | `reports/phase_04_report.md` |
| 5 | Annotation, Review và Dataset QA | Hoàn thành | `reports/phase_05_report.md` |
| 6 | Split, Freeze và Manifest | Hoàn thành | `reports/phase_06_report.md` |
| 7 | Judge Prompt Templates | Hoàn thành | `reports/phase_07_report.md` |
| 8 | Judge Inference Engine | Hoàn thành | `reports/phase_08_report.md` |
| 9 | Swap Aggregation và Core Metrics | Hoàn thành | `reports/phase_09_report.md` |
| 10 | Bias Metrics | Hoàn thành | `reports/phase_10_report.md` |
| 11 | Official V5 Experiment Matrix | Hoàn thành | `reports/phase_11_report.md` |
| 12 | V5 Error Analysis và Charts | Hoàn thành | `reports/phase_12_report.md` |
| 13 | Report, Reproducibility và Packaging | Hoàn thành | `reports/Vi-PPE-mini-paper.pdf` |
| 14 | Optional LoRA/QLoRA | Chưa thực hiện | Không thuộc kết quả báo cáo chính |

## Phiên bản chính thức

- Dataset frozen: LLM V4 (`97 dev / 503 test / 300 bias`).
- Experiment chính thức: **V5**.
- Core tốt nhất: Qwen2.5-7B baseline, accuracy `94.04%`, swap `94.43%`.
- Bias tốt nhất: Qwen2.5-7B mitigated, accuracy `79.26%`, swap `83.00%`.
- V6 chỉ là prompt-hardening ablation, không thay thế V5.
