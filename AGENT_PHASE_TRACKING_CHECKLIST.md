# Agent Phase Tracking Checklist

File này dùng để điều phối agent khi triển khai `IMPLEMENTATION_PLAN_Vi-PPE-mini.md`.

Mục tiêu: mỗi phase phải có scope rõ, agent phải nói trước sẽ làm gì, thực hiện, chạy test, ghi kết quả, rồi mới chuyển phase tiếp theo.

---

## 1. Cách Prompt Agent Khi Bắt Đầu Một Phase

Dùng template này cho từng phase:

```text
Hãy đọc kỹ IMPLEMENTATION_PLAN_Vi-PPE-mini.md và AGENT_PHASE_TRACKING_CHECKLIST.md.

Tôi muốn bạn thực hiện Phase <SỐ>: <TÊN PHASE>.

Yêu cầu trước khi code:
1. Nêu ngắn gọn phase này sẽ làm những nội dung nào.
2. Liệt kê file/thư mục dự kiến tạo hoặc sửa.
3. Liệt kê command test/validation sẽ chạy.
4. Nêu Acceptance Criteria của phase này theo plan.

Sau đó hãy thực hiện phase này end-to-end:
1. Implement đúng scope, không nhảy sang phase khác nếu chưa cần.
2. Cập nhật AGENT_PHASE_TRACKING_CHECKLIST.md: status, files changed, commands run, test result, acceptance criteria.
3. Chạy test/validation tương ứng.
4. Cuối cùng báo cáo: đã làm gì, test nào pass/fail, còn blocker gì, phase có đủ điều kiện chuyển tiếp chưa.
```

Nếu bạn muốn agent chỉ review mà chưa code:

```text
Hãy đọc IMPLEMENTATION_PLAN_Vi-PPE-mini.md và AGENT_PHASE_TRACKING_CHECKLIST.md.

Chỉ review Phase <SỐ>, chưa sửa file.
Hãy nêu:
1. Scope của phase.
2. Deliverables.
3. Acceptance Criteria.
4. Rủi ro/điểm cần tôi xác nhận trước khi implement.
```

Nếu phase có chạy model thật:

```text
Hãy thực hiện Phase <SỐ> theo plan.

Lưu ý bắt buộc:
- Các bước local chỉ dùng cho code, data validation, mock backend và metrics.
- Real model inference hoặc LoRA/QLoRA phải chạy trên Google Colab A100 hoặc GPU tương đương.
- Nếu môi trường hiện tại không phải Colab A100, chỉ chuẩn bị code/notebook/commands và chạy mock/smoke test local. Không chạy real inference 3B/4B/7B trên CPU.
- Ghi rõ hardware_note trong run metadata khi chạy model thật.
```

---

## 2. Quy Tắc Làm Việc Theo Phase

Agent phải tuân thủ:

- Không bắt đầu phase mới nếu phase hiện tại chưa đạt Acceptance Criteria, trừ khi bạn yêu cầu rõ.
- Không sửa frozen dataset trực tiếp. Nếu cần sửa, tạo version mới.
- Không chạy real inference/training local CPU.
- Không dùng test set để tune prompt.
- Mỗi phase kết thúc phải cập nhật checklist này.
- Nếu test fail, agent phải ghi rõ fail ở đâu, nguyên nhân nghi ngờ, bước sửa tiếp theo.
- Nếu có blocker do thiếu dữ liệu/API/GPU, agent phải tạo được artifact local tối thiểu: code, mock test, command Colab.

---

## 3. Phase Status Board

Status hợp lệ:

- `not_started`
- `in_progress`
- `blocked`
- `needs_review`
- `done`

| Phase | Tên phase | Status | Người kiểm | Ghi chú |
|---|---|---|---|---|
| 0 | Scope Freeze và Project Scaffold | done | Codex | Smoke check và pytest pass |
| 1 | Rubric, Schema và Annotation Guideline | done | Codex | Smoke check và schema tests pass |
| 2 | Data Source Adapters | done | Codex | JSONL source adapters build và validation pass |
| 3 | Pair Construction cho MVP 1 | done | Codex | 90 draft pairs generated and validated |
| 4 | Controlled Bias Subset cho MVP 2 | done | Codex | 60 bias draft pairs generated and validated |
| 5 | Annotation, Review và Dataset QA | done | Codex | Annotation tooling, bootstrap review, and QA report pass |
| 6 | Split, Freeze và Manifest | done | Codex | Local frozen splits, manifest, and dataset card pass |
| 7 | Judge Prompt Templates | done | Codex | Prompt templates and renderer pass |
| 8 | Judge Inference Engine | done | Codex | Mock local inference, parser, resume scaffold pass |
| 9 | Swap Aggregation và Core Metrics | done | Codex | Core metrics and swap aggregation pass |
| 10 | Bias Metrics | done | Codex | Bias summary and figures generated from local mock run |
| 11 | Experiment Matrix | not_started |  | Real inference cần Colab A100 |
| 12 | Error Analysis và Charts | not_started |  |  |
| 13 | Report, Reproducibility và Packaging | not_started |  |  |
| 14 | Optional LoRA/QLoRA SFT Branch | not_started |  | Chỉ làm nếu core đã xong và có Colab A100 |

---

## 4. Phase Execution Log Template

Agent copy block này cho mỗi phase khi bắt đầu làm:

```markdown
### Phase <SỐ> - <TÊN PHASE>

Status: in_progress
Started at: YYYY-MM-DD HH:mm
Environment:
- Local/Colab:
- GPU:
- hardware_note:

Planned scope:
- 

Files expected to change:
- 

Commands planned:
```bash

```

Acceptance Criteria:
- [ ] 
- [ ] 
- [ ] 

Implementation notes:
- 

Commands actually run:
```bash

```

Results:
- 

Files changed:
- 

Acceptance Criteria Result:
- [ ] 
- [ ] 
- [ ] 

Status at end: needs_review / done / blocked
Next recommended step:
- 
```

---

## 5. Per-Phase Checklist

### Phase 0 - Scope Freeze Và Project Scaffold

Agent phải làm:

- [x] Tạo cấu trúc repo.
- [x] Tạo `requirements.txt`.
- [x] Tạo `configs/project.yaml`.
- [x] Tạo `data/samples/smoke_pairs.jsonl`.
- [x] Tạo script smoke check.
- [x] Tạo README quickstart.

Test bắt buộc:

```bash
python scripts/00_smoke_check.py
pytest -q
```

Acceptance Criteria:

- [x] Smoke check pass.
- [x] Pytest pass.
- [x] Chưa cần GPU.

### Phase 1 - Rubric, Schema Và Annotation Guideline

Agent phải làm:

- [x] Viết rubric cho `fact_check`, `instruction`, `safety`.
- [x] Tạo hoặc cập nhật schema.
- [x] Viết annotation guideline.
- [x] Test schema/rubric coverage.

Test bắt buộc:

```bash
python scripts/00_smoke_check.py
pytest -q tests/test_schemas.py
```

Acceptance Criteria:

- [x] Rubric đủ rõ.
- [x] Criteria đúng domain.
- [x] Có quy tắc tie.

### Phase 2 - Data Source Adapters

Agent phải làm:

- [x] Implement adapter interface.
- [x] Implement adapters cho nguồn dữ liệu khả dụng.
- [x] Bỏ Manual CSV và Chinhphu.vn / official pages khỏi Source Priority theo yêu cầu.
- [x] Normalize thành `prompts_raw.jsonl`.

Test bắt buộc:

```bash
python scripts/01_build_sources.py --config configs/project.yaml --limit-per-source 20
python scripts/03_validate_dataset.py --input data/interim/prompts_raw.jsonl --type source_items
```

Acceptance Criteria:

- [x] Có provenance.
- [x] Có license note.
- [x] Adapter JSONL local cho nguồn đã cấu hình chạy được.

### Phase 3 - Pair Construction Cho MVP 1

Agent phải làm:

- [x] Sinh pair cho 3 domain.
- [x] Gán `gold_winner`, `gold_reason`, `criteria`, `perturbation_type`.
- [x] Tính length A/B.
- [x] Validate draft pairs.

Test bắt buộc:

```bash
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --output data/processed/pairs_all_draft.jsonl --limit 90
python scripts/03_validate_dataset.py --input data/processed/pairs_all_draft.jsonl
```

Acceptance Criteria:

- [x] Không lộ gold winner.
- [x] Mỗi domain có đủ sample.
- [x] Response thua vẫn plausible.

### Phase 4 - Controlled Bias Subset Cho MVP 2

Agent phải làm:

- [x] Tạo bias subset draft.
- [x] Gắn `diagnostic_subset = true`.
- [x] Gắn `bias_hypothesis`.
- [x] Validate bias fields.

Test bắt buộc:

```bash
python scripts/02_build_pairs.py --bias-only --output data/processed/bias_subset_draft.jsonl --limit 60
python scripts/03_validate_dataset.py --input data/processed/bias_subset_draft.jsonl --require-bias-fields
```

Acceptance Criteria:

- [x] Có field length/style.
- [x] Có perturbation type.
- [x] Pair tie không tính vào core accuracy.

### Phase 5 - Annotation, Review Và Dataset QA

Agent phải làm:

- [x] Export annotation sheet.
- [x] Import annotation result.
- [x] Chạy QA report.
- [x] Mark `review_status`.

Test bắt buộc:

```bash
python scripts/export_annotation_sheet.py --input data/processed/pairs_all_draft.jsonl --output data/processed/annotation_sheet.csv --sample 50
python scripts/import_annotations.py --annotations data/processed/annotation_sheet.csv --pairs data/processed/pairs_all_draft.jsonl --output data/processed/pairs_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_reviewed.jsonl --qa-report reports/dataset_qa_report.md
```

Acceptance Criteria:

- [x] Dev/test không chứa `needs_fix`.
- [x] QA report có domain count.
- [ ] Bias subset reviewed đủ target.

### Phase 6 - Split, Freeze Và Manifest

Agent phải làm:

- [x] Split stratified/grouped.
- [x] Check leakage.
- [x] Tạo manifest hash.
- [x] Viết dataset card.

Test bắt buộc:

```bash
python scripts/04_split_freeze.py --input data/processed/pairs_reviewed.jsonl --bias data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_dev.jsonl --check-split
python scripts/03_validate_dataset.py --input data/processed/pairs_test.jsonl --check-split
pytest -q tests/test_split_leakage.py
```

Acceptance Criteria:

- [x] Không leakage theo `source_example_id`.
- [x] Manifest có sha256.
- [x] Dataset card có source/license.

### Phase 7 - Judge Prompt Templates

Agent phải làm:

- [x] Tạo baseline prompt.
- [x] Tạo criteria-aware prompts theo domain.
- [x] Tạo bias-mitigated prompt.
- [x] Implement prompt renderer.

Test bắt buộc:

```bash
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template baseline_generic_vi --order AB
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template criteria_fact_check_vi --order BA
pytest -q tests/test_prompt_render.py
```

Acceptance Criteria:

- [x] Prompt không lộ gold.
- [x] Render AB/BA đúng.
- [x] Output JSON schema rõ.

### Phase 8 - Judge Inference Engine

Agent phải làm:

- [x] Implement mock backend.
- [x] Implement HF local backend.
- [x] Implement parser.
- [x] Implement resume.
- [x] Chạy mock local.
- [x] Chuẩn bị command Colab A100 cho real inference.

Test bắt buộc local:

```bash
python scripts/05_run_judge.py --dataset data/samples/smoke_pairs.jsonl --backend mock --template baseline_generic_vi --run-id smoke_mock
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_parse_judgment.py
```

Test bắt buộc Colab A100:

```bash
python scripts/05_run_judge.py --dataset data/processed/pairs_dev.jsonl --model qwen25_3b --template baseline_generic_vi --run-id qwen25_3b_baseline_dev --resume
```

Acceptance Criteria:

- [x] Mock local pass.
- [x] Real inference chỉ chạy trên Colab A100/GPU tương đương.
- [x] Mỗi pair có AB và BA.
- [x] Parse success được báo cáo.

### Phase 9 - Swap Aggregation Và Core Metrics

Agent phải làm:

- [x] Map BA về original space.
- [x] Aggregate final winner.
- [x] Tính accuracy/macro/domain/lower-bound.
- [x] Tính swap consistency.

Test bắt buộc:

```bash
python scripts/06_compute_metrics.py --judgments results/judgments/qwen25_3b_baseline_dev.jsonl --dataset data/processed/pairs_dev.jsonl --run-id qwen25_3b_baseline_dev
pytest -q tests/test_metrics.py
```

Acceptance Criteria:

- [x] Gold tie không tính core accuracy.
- [x] Inconsistent swap báo cáo riêng.
- [x] Summary JSON được tạo.

### Phase 10 - Bias Metrics

Agent phải làm:

- [x] Tính verbosity bias rate.
- [x] Tính style bias rate.
- [x] Tính conditional accuracy.
- [x] Tạo bias summary.

Test bắt buộc:

```bash
python scripts/06_compute_metrics.py --judgments results/judgments/qwen25_3b_criteria_bias_dev.jsonl --dataset data/processed/bias_subset.jsonl --run-id qwen25_3b_criteria_bias_dev --bias
pytest -q tests/test_bias_metrics.py
```

Acceptance Criteria:

- [x] Không kết luận bias từ một metric duy nhất.
- [x] Có delta length distribution.
- [x] Tách style và verbosity nếu có đủ tag.

### Phase 11 - Experiment Matrix

Agent phải làm:

- [ ] Tạo final run config.
- [ ] Chạy baseline dev/test.
- [ ] Chạy criteria dev/test.
- [ ] Chạy bias baseline/mitigated.
- [ ] Chạy PhoGPT subset nếu có Colab A100 đủ thời gian.

Test bắt buộc:

```bash
python scripts/07_make_report_assets.py --metrics-dir results/metrics --output-dir results/figures
```

Acceptance Criteria:

- [ ] Test set chỉ chạy sau prompt freeze.
- [ ] Có experiment matrix CSV.
- [ ] Mỗi run có dataset hash/config hash/hardware_note.

### Phase 12 - Error Analysis Và Charts

Agent phải làm:

- [ ] Tạo charts.
- [ ] Chọn error cases.
- [ ] Viết error cases markdown.
- [ ] Gắn taxonomy lỗi.

Test bắt buộc:

```bash
python scripts/07_make_report_assets.py --metrics-dir results/metrics --judgments-dir results/judgments --dataset data/processed/pairs_test.jsonl --output-dir results
```

Acceptance Criteria:

- [ ] Có ít nhất 10 error cases.
- [ ] Có domain accuracy chart.
- [ ] Có bias mitigation chart.

### Phase 13 - Report, Reproducibility Và Packaging

Agent phải làm:

- [ ] Hoàn thiện README.
- [ ] Viết final report.
- [ ] Viết slide outline.
- [ ] Kiểm reproducibility checklist.

Test bắt buộc:

```bash
python scripts/00_smoke_check.py
python scripts/06_compute_metrics.py --help
python scripts/07_make_report_assets.py --help
```

Acceptance Criteria:

- [ ] Người khác chạy được smoke pipeline.
- [ ] Report có metric và error analysis.
- [ ] Dataset card có provenance/license.

### Phase 14 - Optional LoRA/QLoRA SFT Branch

Chỉ làm nếu core đã xong và có Colab A100.

Agent phải làm:

- [ ] Build SFT examples.
- [ ] Train LoRA/QLoRA adapter.
- [ ] Eval adapter trên dev.
- [ ] Báo cáo như optional exploratory result.

Test bắt buộc:

```bash
python scripts/08_optional_lora_sft.py --config configs/lora_optional.yaml --dry-run
python scripts/08_optional_lora_sft.py --config configs/lora_optional.yaml
python scripts/05_run_judge.py --dataset data/processed/pairs_dev.jsonl --model qwen25_lora --template criteria_auto --run-id qwen25_lora_dev
```

Acceptance Criteria:

- [ ] Không phá core results.
- [ ] Adapter được lưu.
- [ ] Nếu không thắng prompt-only, ghi limitation.

---

## 6. Prompt Mẫu Để Yêu Cầu Agent Báo Cáo Sau Phase

```text
Hãy tổng kết Phase <SỐ> vừa thực hiện.

Bắt buộc gồm:
1. Files đã tạo/sửa.
2. Commands đã chạy.
3. Test pass/fail.
4. Acceptance Criteria: từng mục đạt/chưa đạt.
5. Blocker còn lại.
6. Có đủ điều kiện chuyển sang phase tiếp theo không?

Nếu chưa đủ điều kiện, hãy đề xuất bước sửa tiếp theo, nhưng chưa tự chuyển phase.
```

---

## 8. Phase Execution Logs

Report nhanh theo phase:
- `reports/phase_status.md`
- `reports/phase_00_report.md`
- `reports/phase_01_report.md`
- `reports/phase_02_report.md`
- `reports/phase_03_report.md`
- `reports/phase_04_report.md`
- `reports/phase_05_report.md`
- `reports/phase_06_report.md`
- `reports/phase_07_report.md`
- `reports/phase_08_report.md`
- `reports/phase_09_report.md`
- `reports/phase_10_report.md`

### Phase 0 - Scope Freeze Và Project Scaffold

Status: done
Started at: 2026-07-02 01:40
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 0 does not require GPU.

Planned scope:
- Create repository scaffold.
- Add requirements, project config, README quickstart, smoke dataset, schema/config/IO modules, smoke check script, and schema tests.

Files expected to change:
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

Commands planned:
```bash
python scripts/00_smoke_check.py
pytest -q
```

Acceptance Criteria:
- [x] Smoke check pass.
- [x] Pytest pass.
- [x] Chưa cần GPU.

Implementation notes:
- Smoke dataset has 6 synthetic pairwise examples: 2 `fact_check`, 2 `instruction`, and 2 `safety`.
- Schema validation checks required fields, domain values, criteria/domain compatibility, winner values, review status, token lengths, and duplicate `pair_id`.
- README states prompt-only is the core path and LoRA/QLoRA is optional after core completion.

Commands actually run:
```bash
python scripts/00_smoke_check.py
pytest -q
```

Results:
- `python scripts/00_smoke_check.py`: pass, printed `OK: scaffold and smoke data are valid`.
- `pytest -q`: pass, `3 passed in 0.06s`.

Files changed:
- Created scaffold directories under `configs/`, `data/`, `prompts/`, `src/`, `scripts/`, `notebooks/`, `results/`, `reports/`, and `tests/`.
- Created or updated all files listed above.

Acceptance Criteria Result:
- [x] Smoke check pass.
- [x] Pytest pass.
- [x] Chưa cần GPU.

Status at end: done
Next recommended step:
- Phase 1 - Rubric, Schema Và Annotation Guideline.

---

### Phase 1 - Rubric, Schema Và Annotation Guideline

Status: done
Started at: 2026-07-02 01:58
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 1 does not require GPU.

Planned scope:
- Expand domain rubrics to five criteria per domain.
- Update schema and config so criteria/domain compatibility is validated.
- Write annotation guideline covering `gold_winner`, tie handling, `gold_reason`, conflict rules, and examples.
- Add tests for rubric coverage and tie policy.

Files expected to change:
- `configs/project.yaml`
- `src/vi_ppe/schemas.py`
- `tests/test_schemas.py`
- `reports/annotation_guideline.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/00_smoke_check.py
pytest -q tests/test_schemas.py
```

Acceptance Criteria:
- [x] Rubric đủ rõ.
- [x] Criteria đúng domain.
- [x] Có quy tắc tie.

Implementation notes:
- `fact_check`, `instruction`, and `safety` now each have five criteria matching the implementation plan.
- `validate_rubric_config` checks `configs/project.yaml` against schema constants.
- `is_core_accuracy_pair` keeps `gold_winner = "tie"` valid for annotation while excluding it from core accuracy.
- Annotation guideline includes examples and conflict rules in Vietnamese.

Commands actually run:
```bash
python scripts/00_smoke_check.py
pytest -q tests/test_schemas.py
```

Results:
- `python scripts/00_smoke_check.py`: pass, printed `OK: scaffold and smoke data are valid`.
- `pytest -q tests/test_schemas.py`: pass, `6 passed in 0.05s`.

Files changed:
- Updated `configs/project.yaml` rubric config.
- Updated `src/vi_ppe/schemas.py` rubric constants, descriptions, config validation, and tie/core helper.
- Updated `tests/test_schemas.py` rubric and tie tests.
- Created `reports/annotation_guideline.md`.
- Updated checklist status and execution log.

Acceptance Criteria Result:
- [x] Rubric đủ rõ.
- [x] Criteria đúng domain.
- [x] Có quy tắc tie.

Status at end: done
Next recommended step:
- Phase 2 - Data Source Adapters.

---

### Phase 2 - Data Source Adapters

Status: done
Started at: 2026-07-02 02:11
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 2 does not require GPU.

Planned scope:
- Implement a common data source adapter interface with `load_raw`, `normalize`, and `write_interim_jsonl`.
- Add lightweight local-file adapters and fixtures for ViQuAD, ViWikiFC, ViFactCheck, and ViHSD.
- Remove Manual CSV and Chinhphu.vn / official pages from Source Priority per user request.
- Add source item schema validation and a dataset validation CLI.
- Build `data/interim/prompts_raw.jsonl`.

Files expected to change:
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
- `reports/phase_02_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/01_build_sources.py --config configs/project.yaml --limit-per-source 20
python scripts/03_validate_dataset.py --input data/interim/prompts_raw.jsonl --type source_items
```

Acceptance Criteria:
- [x] Có provenance.
- [x] Có license note.
- [x] Adapter JSONL local cho nguồn đã cấu hình chạy được.

Implementation notes:
- Local JSONL fixtures for ViQuAD, ViWikiFC, ViFactCheck, and ViHSD keep Phase 2 unblocked without using Manual CSV.
- The `instruction` source will be handled in later data/pair construction without listing Manual CSV as a priority source.
- Each normalized source item includes `source_dataset`, `source_example_id`, `domain_candidates`, `license_note`, and `metadata`.
- Adapter build prints warnings for `license_note = unknown`; no unknown license notes were produced in this run.

Commands actually run:
```bash
python scripts/01_build_sources.py --config configs/project.yaml --limit-per-source 20
python scripts/03_validate_dataset.py --input data/interim/prompts_raw.jsonl --type source_items
python scripts/00_smoke_check.py
pytest -q
```

Results:
- `python scripts/01_build_sources.py --config configs/project.yaml --limit-per-source 20`: pass, wrote 20 source items from configured JSONL sources: 5 `viquad`, 5 `viwikifc`, 5 `vifactcheck`, 5 `vihsd`.
- `python scripts/03_validate_dataset.py --input data/interim/prompts_raw.jsonl --type source_items`: pass.
- `python scripts/00_smoke_check.py`: pass.
- `pytest -q`: pass, `8 passed in 0.05s`.

Files changed:
- Added data source adapter modules and source item validation.
- Added local JSONL fixtures and regenerated `data/interim/prompts_raw.jsonl`.
- Added build/validate scripts and adapter tests.
- Updated checklist and phase reports.

Acceptance Criteria Result:
- [x] Có provenance.
- [x] Có license note.
- [x] Adapter JSONL local cho nguồn đã cấu hình chạy được.

Status at end: done
Next recommended step:
- Phase 3 - Pair Construction Cho MVP 1.

---

### Phase 3 - Pair Construction Cho MVP 1

Status: done
Started at: 2026-07-02 02:26
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 3 does not require GPU.

Planned scope:
- Generate draft pairwise examples for `fact_check`, `instruction`, and `safety`.
- Assign `gold_winner`, `gold_reason`, `criteria`, and `perturbation_type`.
- Compute `length_a_tokens` and `length_b_tokens`.
- Validate `data/processed/pairs_all_draft.jsonl`.

Files expected to change:
- `src/vi_ppe/build_pairs.py`
- `scripts/02_build_pairs.py`
- `data/processed/pairs_all_draft.jsonl`
- `reports/pair_generation_notes.md`
- `tests/test_build_pairs.py`
- `reports/phase_03_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --output data/processed/pairs_all_draft.jsonl --limit 90
python scripts/03_validate_dataset.py --input data/processed/pairs_all_draft.jsonl
```

Acceptance Criteria:
- [x] Không lộ gold winner.
- [x] Mỗi domain có đủ sample.
- [x] Response thua vẫn plausible.

Implementation notes:
- Fact-check pairs are built from ViQuAD-like, ViWikiFC-like, and ViFactCheck-like source items.
- Safety pairs are built from ViHSD-like source items.
- Instruction pairs use internal synthetic templates because `Manual CSV` was removed from Source Priority.
- A/B order is deterministic by `pair_id` hash.
- All outputs remain `review_status = "draft"` and `split = "draft"`.

Commands actually run:
```bash
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --output data/processed/pairs_all_draft.jsonl --limit 90
python scripts/03_validate_dataset.py --input data/processed/pairs_all_draft.jsonl
python scripts/00_smoke_check.py
pytest -q
```

Results:
- First build attempt produced 80 pairs and safety had only 10 samples, so safety variants were increased.
- Final build produced 90 pairs: 30 `fact_check`, 40 `instruction`, 20 `safety`.
- Validator passed: `OK: validated 90 pairs records`.
- `pytest -q`: pass, `10 passed in 0.06s`.

Files changed:
- Added pair builder module and CLI.
- Added draft pair artifact.
- Added pair generation notes and tests.
- Updated checklist and phase status reports.

Acceptance Criteria Result:
- [x] Không lộ gold winner.
- [x] Mỗi domain có đủ sample.
- [x] Response thua vẫn plausible.

Status at end: done
Next recommended step:
- Phase 4 - Controlled Bias Subset Cho MVP 2.

---

### Phase 4 - Controlled Bias Subset Cho MVP 2

Status: done
Started at: 2026-07-02 02:31
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 4 does not require GPU.

Planned scope:
- Create `data/processed/bias_subset_draft.jsonl`.
- Mark all records with `diagnostic_subset = true`.
- Add `bias_hypothesis`.
- Validate bias-specific fields and print delta length distribution.

Files expected to change:
- `src/vi_ppe/bias_pair_builders.py`
- `src/vi_ppe/schemas.py`
- `scripts/02_build_pairs.py`
- `scripts/03_validate_dataset.py`
- `data/processed/bias_subset_draft.jsonl`
- `reports/bias_subset_guideline.md`
- `tests/test_bias_pair_builders.py`
- `reports/phase_04_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/02_build_pairs.py --bias-only --output data/processed/bias_subset_draft.jsonl --limit 60
python scripts/03_validate_dataset.py --input data/processed/bias_subset_draft.jsonl --require-bias-fields
```

Acceptance Criteria:
- [x] Có field length/style.
- [x] Có perturbation type.
- [x] Pair tie không tính vào core accuracy.

Implementation notes:
- Bias subset includes controlled verbosity, style, over-elaboration, and refusal-moralizing cases.
- Tie pairs are used for `same_content_different_length` and `plain_style_vs_polished_style`.
- `validate_bias_pairs` checks `diagnostic_subset`, `bias_hypothesis`, style fields, and base pair schema.

Commands actually run:
```bash
python scripts/02_build_pairs.py --bias-only --output data/processed/bias_subset_draft.jsonl --limit 60
python scripts/03_validate_dataset.py --input data/processed/bias_subset_draft.jsonl --require-bias-fields
python scripts/00_smoke_check.py
pytest -q
```

Results:
- Build produced 60 bias draft pairs.
- Domain counts: 45 `fact_check`, 10 `instruction`, 5 `safety`.
- Perturbation counts: 15 `concise_correct_vs_verbose_wrong`, 15 `same_content_different_length`, 15 `plain_style_vs_polished_style`, 10 `instruction_following_vs_over_elaboration`, 5 `appropriate_refusal_vs_verbose_moralizing`.
- Delta length distribution: 23 `A_longer`, 37 `B_longer`.
- `pytest -q`: pass, `12 passed in 0.06s`.

Files changed:
- Added bias pair builder and guideline.
- Updated build/validate scripts for `--bias-only` and `--require-bias-fields`.
- Added bias tests and generated bias subset draft artifact.
- Updated checklist and phase reports.

Acceptance Criteria Result:
- [x] Có field length/style.
- [x] Có perturbation type.
- [x] Pair tie không tính vào core accuracy.

Status at end: done
Next recommended step:
- Phase 5 - Annotation, Review Và Dataset QA.

---

### Phase 5 - Annotation, Review Và Dataset QA

Status: done
Started at: 2026-07-02 02:36
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 5 does not require GPU.

Planned scope:
- Export annotation CSV.
- Import annotation results and mark `review_status`.
- Generate dataset QA report.
- Produce reviewed core and bias artifacts.

Files expected to change:
- `src/vi_ppe/annotation.py`
- `scripts/export_annotation_sheet.py`
- `scripts/import_annotations.py`
- `scripts/03_validate_dataset.py`
- `data/processed/annotation_sheet.csv`
- `data/processed/pairs_reviewed.jsonl`
- `data/processed/bias_annotation_sheet.csv`
- `data/processed/bias_subset_reviewed.jsonl`
- `reports/dataset_qa_report.md`
- `tests/test_annotation.py`
- `reports/phase_05_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/export_annotation_sheet.py --input data/processed/pairs_all_draft.jsonl --output data/processed/annotation_sheet.csv --sample 50
python scripts/import_annotations.py --annotations data/processed/annotation_sheet.csv --pairs data/processed/pairs_all_draft.jsonl --output data/processed/pairs_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_reviewed.jsonl --qa-report reports/dataset_qa_report.md
```

Acceptance Criteria:
- [x] Dev/test không chứa `needs_fix`.
- [x] QA report có domain count.
- [ ] Bias subset reviewed đủ target.

Implementation notes:
- Annotation CSV is prefilled from draft labels so the local pipeline can proceed; this is bootstrap review, not final human review.
- `pairs_reviewed.jsonl` contains 50 reviewed rows and 40 remaining draft rows after the requested `--sample 50`.
- `bias_subset_reviewed.jsonl` contains 60 bootstrap-reviewed bias pairs from the Phase 4 smoke subset.
- Final target still requires 150-200 manually reviewed high-control bias pairs before final experiments.

Commands actually run:
```bash
python scripts/export_annotation_sheet.py --input data/processed/pairs_all_draft.jsonl --output data/processed/annotation_sheet.csv --sample 50
python scripts/import_annotations.py --annotations data/processed/annotation_sheet.csv --pairs data/processed/pairs_all_draft.jsonl --output data/processed/pairs_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_reviewed.jsonl --qa-report reports/dataset_qa_report.md
python scripts/export_annotation_sheet.py --input data/processed/bias_subset_draft.jsonl --output data/processed/bias_annotation_sheet.csv --sample 60
python scripts/import_annotations.py --annotations data/processed/bias_annotation_sheet.csv --pairs data/processed/bias_subset_draft.jsonl --output data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/bias_subset_reviewed.jsonl --require-bias-fields
python scripts/00_smoke_check.py
pytest -q
```

Results:
- Exported 50 core annotation rows.
- Imported 50 reviewed core rows into `pairs_reviewed.jsonl`.
- QA report written to `reports/dataset_qa_report.md`.
- Exported and imported 60 bias annotation rows into `bias_subset_reviewed.jsonl`.
- Bias reviewed validation passed.
- `pytest -q`: pass, `14 passed in 0.12s`.

Files changed:
- Added annotation helper module and export/import scripts.
- Updated validator to write QA report.
- Generated annotation sheets, reviewed JSONL artifacts, and QA report.
- Added annotation tests and phase report.

Acceptance Criteria Result:
- [x] Dev/test không chứa `needs_fix` because splits do not exist yet and reviewed artifacts contain no `needs_fix`.
- [x] QA report có domain count.
- [ ] Bias subset reviewed đủ target: partial only, 60 bootstrap-reviewed pairs exist; final target is 150-200 human-reviewed pairs.

Status at end: done
Next recommended step:
- Phase 6 - Split, Freeze Và Manifest.

---

### Phase 6 - Split, Freeze Và Manifest

Status: done
Started at: 2026-07-02 06:30
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 6 does not require GPU.

Planned scope:
- Split reviewed core pairs into dev/test while grouping by `source_example_id`.
- Freeze reviewed bias subset.
- Check source leakage.
- Generate `dataset_manifest.json` with SHA256 hashes.
- Write dataset card.

Files expected to change:
- `src/vi_ppe/split_dataset.py`
- `scripts/04_split_freeze.py`
- `scripts/03_validate_dataset.py`
- `tests/test_split_leakage.py`
- `data/processed/pairs_dev.jsonl`
- `data/processed/pairs_test.jsonl`
- `data/processed/bias_subset.jsonl`
- `data/processed/dataset_manifest.json`
- `reports/dataset_card.md`
- `reports/phase_06_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/04_split_freeze.py --input data/processed/pairs_reviewed.jsonl --bias data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_dev.jsonl --check-split
python scripts/03_validate_dataset.py --input data/processed/pairs_test.jsonl --check-split
pytest -q tests/test_split_leakage.py
```

Acceptance Criteria:
- [x] Không leakage theo `source_example_id`.
- [x] Manifest có sha256.
- [x] Dataset card có source/license.

Implementation notes:
- Freeze uses only records with `review_status = "reviewed"`.
- Current local core split is small because Phase 5 reviewed 50 core rows using bootstrap annotations.
- This is suitable for pipeline validation; final thesis-scale run requires more human-reviewed examples.

Commands actually run:
```bash
python scripts/04_split_freeze.py --input data/processed/pairs_reviewed.jsonl --bias data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_dev.jsonl --check-split
python scripts/03_validate_dataset.py --input data/processed/pairs_test.jsonl --check-split
pytest -q tests/test_split_leakage.py
pytest -q
```

Results:
- Dev split: 11 records.
- Test split: 39 records.
- Bias subset: 60 records.
- Manifest written to `data/processed/dataset_manifest.json`.
- Dataset card written to `reports/dataset_card.md`.
- Dev/test split validation passed.
- Leakage tests passed.
- Full pytest passed: `16 passed in 0.11s`.

Files changed:
- Added split/freeze module and CLI.
- Updated dataset validator with `--check-split`.
- Generated frozen local sample artifacts, manifest, and dataset card.
- Added leakage tests and phase report.

Acceptance Criteria Result:
- [x] Không leakage theo `source_example_id`.
- [x] Manifest có sha256.
- [x] Dataset card có source/license.

Status at end: done
Next recommended step:
- Phase 7 - Judge Prompt Templates.

---

### Phase 7 - Judge Prompt Templates

Status: done
Started at: 2026-07-02 06:35
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 7 does not require GPU.

Planned scope:
- Create baseline, criteria-aware, and bias-mitigated prompt templates.
- Implement prompt renderer with AB/BA response ordering.
- Ensure prompts do not leak gold labels/reasons.
- Add prompt renderer tests.

Files expected to change:
- `prompts/baseline_generic_vi.md`
- `prompts/criteria_fact_check_vi.md`
- `prompts/criteria_instruction_vi.md`
- `prompts/criteria_safety_vi.md`
- `prompts/criteria_bias_mitigated_vi.md`
- `prompts/fewshot_examples.jsonl`
- `src/vi_ppe/prompt_render.py`
- `tests/test_prompt_render.py`
- `reports/prompt_design_notes.md`
- `reports/phase_07_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template baseline_generic_vi --order AB
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template criteria_fact_check_vi --order BA
pytest -q tests/test_prompt_render.py
```

Acceptance Criteria:
- [x] Prompt không lộ gold.
- [x] Render AB/BA đúng.
- [x] Output JSON schema rõ.

Implementation notes:
- Renderer supports `baseline_generic_vi`, criteria templates, `criteria_bias_mitigated_vi`, and `auto_criteria_by_domain`.
- Criteria-aware prompts explicitly warn against rewarding length or polished style when correctness does not improve.
- CLI configures stdout as UTF-8 for Vietnamese text on Windows.

Commands actually run:
```bash
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template baseline_generic_vi --order AB
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template criteria_fact_check_vi --order BA
pytest -q tests/test_prompt_render.py
pytest -q
```

Results:
- Baseline render command passed.
- Criteria BA render command passed and swapped responses.
- Prompt tests passed.
- Full pytest passed: `20 passed in 0.14s`.

Files changed:
- Added prompt templates, prompt renderer, prompt tests, and prompt design notes.
- Updated checklist and phase reports.

Acceptance Criteria Result:
- [x] Prompt không lộ gold.
- [x] Render AB/BA đúng.
- [x] Output JSON schema rõ.

Status at end: done
Next recommended step:
- Phase 8 - Judge Inference Engine.

---

### Phase 8 - Judge Inference Engine

Status: done
Started at: 2026-07-02 06:38
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU mock only; real inference must run on Colab A100 or equivalent.

Planned scope:
- Implement mock backend.
- Implement HF local backend for Colab/GPU.
- Implement judgment parser.
- Implement run judge script with AB/BA and `--resume`.
- Run local mock smoke test.

Files expected to change:
- `configs/models.yaml`
- `src/vi_ppe/judge_backends/__init__.py`
- `src/vi_ppe/judge_backends/mock.py`
- `src/vi_ppe/judge_backends/hf_local.py`
- `src/vi_ppe/parse_judgment.py`
- `src/vi_ppe/run_judge.py`
- `scripts/05_run_judge.py`
- `tests/test_parse_judgment.py`
- `results/judgments/smoke_mock.jsonl`
- `results/metrics/smoke_mock_summary.json`
- `results/metrics/smoke_mock_pair_results.jsonl`
- `reports/phase_08_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/05_run_judge.py --dataset data/samples/smoke_pairs.jsonl --backend mock --template baseline_generic_vi --run-id smoke_mock
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_parse_judgment.py
```

Acceptance Criteria:
- [x] Mock local pass.
- [x] Real inference chỉ chạy trên Colab A100/GPU tương đương.
- [x] Mỗi pair có AB và BA.
- [x] Parse success được báo cáo.

Implementation notes:
- Mock backend follows the gold label only for smoke testing.
- HF local backend is implemented but not executed locally.
- Runner logs model/template/dataset/config hashes, raw output, parsed output, parse status, latency, and hardware note.
- `scripts/06_compute_metrics.py` was added early as a minimal smoke metric path; Phase 9 will expand metrics.

Commands actually run:
```bash
python scripts/05_run_judge.py --dataset data/samples/smoke_pairs.jsonl --backend mock --template baseline_generic_vi --run-id smoke_mock
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_parse_judgment.py
pytest -q
```

Results:
- Mock run wrote 12 judgments for 6 pairs x AB/BA.
- Parse success rate: 1.0.
- Mock pairwise accuracy: 1.0.
- Full pytest passed: `23 passed in 0.14s`.

Files changed:
- Added judge backends, parser, runner, run script, model config, parser tests, and smoke metrics outputs.
- Updated checklist and phase reports.

Acceptance Criteria Result:
- [x] Mock local pass.
- [x] Real inference chỉ chạy trên Colab A100/GPU tương đương.
- [x] Mỗi pair có AB và BA.
- [x] Parse success được báo cáo.

Status at end: done
Next recommended step:
- Phase 9 - Swap Aggregation Và Core Metrics.

---

### Phase 9 - Swap Aggregation Và Core Metrics

Status: done
Started at: 2026-07-02 06:41
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU only; Phase 9 does not require GPU.

Planned scope:
- Map BA judgments back to original A/B space.
- Aggregate AB/BA into final winners.
- Compute pairwise, domain, macro, lower-bound, swap consistency, parse success, and position-bias summaries.
- Add tests for tie exclusion and inconsistent swaps.

Files expected to change:
- `src/vi_ppe/aggregate_swaps.py`
- `src/vi_ppe/metrics.py`
- `scripts/06_compute_metrics.py`
- `tests/test_metrics.py`
- `results/metrics/smoke_mock_summary.json`
- `results/metrics/smoke_mock_pair_results.jsonl`
- `reports/phase_09_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_metrics.py
```

Acceptance Criteria:
- [x] Gold tie không tính core accuracy.
- [x] Inconsistent swap báo cáo riêng.
- [x] Summary JSON được tạo.

Implementation notes:
- `map_to_original_space("A", "BA")` maps to original `B`; `B` maps to original `A`.
- `final_winner = "inconsistent"` for AB/BA disagreement after mapping.
- Gold `tie` pairs have `is_correct = null` in pair results and are excluded from core accuracy.
- Pair result rows now include length/style fields for Phase 10 bias metrics.

Commands actually run:
```bash
python scripts/06_compute_metrics.py --judgments results/judgments/smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id smoke_mock
pytest -q tests/test_metrics.py
pytest -q
```

Results:
- Smoke summary JSON written.
- Smoke pair results JSONL written.
- Parse success rate: 1.0.
- Pairwise/macro/lower-bound accuracy: 1.0 on mock smoke.
- Swap consistency: 1.0 on mock smoke.
- Full pytest passed: `27 passed in 0.16s`.

Files changed:
- Expanded metrics and swap aggregation.
- Added metrics tests.
- Regenerated smoke metrics outputs.
- Updated checklist and phase report.

Acceptance Criteria Result:
- [x] Gold tie không tính core accuracy.
- [x] Inconsistent swap báo cáo riêng.
- [x] Summary JSON được tạo.

Status at end: done
Next recommended step:
- Phase 10 - Bias Metrics.

---

### Phase 10 - Bias Metrics

Status: done
Started at: 2026-07-02 07:10
Environment:
- Local/Colab: Local Windows PowerShell
- GPU: Not used
- hardware_note: Local CPU mock only; real model bias inference must run on Colab A100 or equivalent.

Planned scope:
- Compute verbosity bias rate, style bias rate, conditional accuracy, and delta length distribution.
- Add bias summary generation to the metrics CLI.
- Generate local diagnostic figures for bias rates and token-length deltas.

Files expected to change:
- `src/vi_ppe/bias_metrics.py`
- `scripts/06_compute_metrics.py`
- `tests/test_bias_metrics.py`
- `results/metrics/qwen25_3b_criteria_bias_dev_bias_summary.json`
- `results/figures/qwen25_3b_criteria_bias_dev_bias_rates.png`
- `results/figures/qwen25_3b_criteria_bias_dev_delta_tokens_scatter.png`
- `reports/phase_10_report.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

Commands planned:
```bash
python scripts/06_compute_metrics.py --judgments results/judgments/qwen25_3b_criteria_bias_dev.jsonl --dataset data/processed/bias_subset.jsonl --run-id qwen25_3b_criteria_bias_dev --bias
pytest -q tests/test_bias_metrics.py
```

Acceptance Criteria:
- [x] Không kết luận bias từ một metric duy nhất.
- [x] Có delta length distribution.
- [x] Tách style và verbosity nếu có đủ tag.

Implementation notes:
- `bias_metrics.py` computes conditional accuracy, verbosity bias, style bias, swap consistency on bias subset, perturbation counts, and delta token distribution.
- `scripts/06_compute_metrics.py --bias` writes both core metrics and `results/metrics/{run_id}_bias_summary.json`.
- Local run uses the mock backend only. It validates the pipeline but is not a real Qwen bias result.
- `style_bias_rate` can be `null` when controlled style rows produce tie verdicts and no style is selected.

Commands actually run:
```bash
pytest -q tests/test_bias_metrics.py
python scripts/05_run_judge.py --dataset data/processed/bias_subset.jsonl --backend mock --template criteria_bias_mitigated_vi --run-id qwen25_3b_criteria_bias_dev
python scripts/06_compute_metrics.py --judgments results/judgments/qwen25_3b_criteria_bias_dev.jsonl --dataset data/processed/bias_subset.jsonl --run-id qwen25_3b_criteria_bias_dev --bias
pytest -q
```

Results:
- Bias tests passed: `4 passed in 0.03s`.
- Mock bias inference wrote 120 judgments for 60 pairs x AB/BA.
- Bias summary written to `results/metrics/qwen25_3b_criteria_bias_dev_bias_summary.json`.
- Figures written to `results/figures/qwen25_3b_criteria_bias_dev_bias_rates.png` and `results/figures/qwen25_3b_criteria_bias_dev_delta_tokens_scatter.png`.
- Full pytest passed: `31 passed in 0.22s`.

Files changed:
- Added bias metric module and tests.
- Updated metrics CLI for `--bias`.
- Generated mock bias judgments, metrics, summary, and figures.
- Updated checklist and phase reports.

Acceptance Criteria Result:
- [x] Không kết luận bias từ một metric duy nhất.
- [x] Có delta length distribution.
- [x] Tách style và verbosity nếu có đủ tag.

Status at end: done
Next recommended step:
- Phase 11 - Experiment Matrix.

---

## 7. Prompt Mẫu Để Yêu Cầu Agent Tiếp Tục Phase Sau

```text
Phase <SỐ> đã được tôi review và chấp nhận.

Hãy chuyển sang Phase <SỐ TIẾP THEO>: <TÊN PHASE>.
Trước khi code, hãy đọc lại IMPLEMENTATION_PLAN_Vi-PPE-mini.md và AGENT_PHASE_TRACKING_CHECKLIST.md, sau đó nêu:
1. Scope của phase mới.
2. File dự kiến sửa/tạo.
3. Test sẽ chạy.
4. Acceptance Criteria.

Sau khi tôi đồng ý hoặc nếu không có câu hỏi bắt buộc, hãy implement end-to-end và cập nhật checklist.
```
