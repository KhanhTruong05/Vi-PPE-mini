# Phase 11 Report - Experiment Matrix V5

## Trạng thái

Hoàn thành. V5 là phiên bản kết quả chính thức được dùng trong báo cáo.

## Môi trường

- Runtime: Google Colab A100 40GB.
- Backend: Hugging Face local inference.
- Precision: BF16, không quantize cho các run chính.
- Decoding: deterministic, `do_sample=False`, `temperature=0`.
- Batch size chính: 16, tùy model profile.
- Real inference không chạy trong Codex/local CPU.

## Dataset

- Dev: `data/processed/pairs_dev_llm_v4.jsonl` - 97 pairs.
- Main test: `data/processed/pairs_test_llm_v4.jsonl` - 503 pairs.
- Bias subset: `data/processed/bias_subset_llm_v4.jsonl` - 300 pairs.
- Manifest: `data/processed/dataset_manifest_llm_v4.json`.

Mỗi core run có 1006 judgments AB/BA; mỗi bias run có 600 judgments AB/BA.

## Model và prompt

- Qwen2.5-3B-Instruct.
- Qwen2.5-7B-Instruct.
- Gemma-3-4B-IT.
- Llama-3.1-8B-Instruct.
- Core prompts: generic baseline và criteria-aware.
- Bias prompts: generic baseline và bias-mitigated.

## Kết quả main test

| Model | Prompt | Accuracy | Macro | Swap | Parse |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | Baseline | 83.70% | 83.63% | 84.89% | 100.00% |
| Qwen2.5-3B | Criteria | 75.15% | 75.11% | 73.56% | 100.00% |
| **Qwen2.5-7B** | **Baseline** | **94.04%** | **94.00%** | **94.43%** | **100.00%** |
| Qwen2.5-7B | Criteria | 90.06% | 90.00% | 91.45% | 99.90% |
| Gemma-3-4B | Baseline | 86.48% | 86.42% | 87.67% | 99.11% |
| Gemma-3-4B | Criteria | 76.34% | 76.32% | 77.14% | 100.00% |
| Llama-3.1-8B | Baseline | 86.88% | 86.79% | 88.27% | 100.00% |
| Llama-3.1-8B | Criteria | 89.86% | 89.80% | 91.45% | 100.00% |

Qwen2.5-7B baseline là cấu hình core tốt nhất. Criteria prompt giúp một số fact-check setting nhưng thường làm giảm instruction accuracy.

## Kết quả theo domain của cấu hình core tốt nhất

| Fact-check | Instruction | Safety |
|---:|---:|---:|
| 93.37% | 89.22% | 99.41% |

## Kết quả controlled bias subset

| Model | Prompt | Conditional accuracy | Macro | Swap | Verbosity |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | Baseline | 62.88% | 62.79% | 66.67% | 65.00% |
| Qwen2.5-3B | Mitigated | 62.88% | 62.81% | 62.00% | 53.27% |
| Qwen2.5-7B | Baseline | 76.59% | 76.49% | 79.33% | 55.20% |
| **Qwen2.5-7B** | **Mitigated** | **79.26%** | **79.20%** | **83.00%** | **47.83%** |
| Gemma-3-4B | Baseline | 73.91% | 73.87% | 77.33% | 55.91% |
| Gemma-3-4B | Mitigated | 67.89% | 67.82% | 69.33% | 56.07% |
| Llama-3.1-8B | Baseline | 77.26% | 77.19% | 86.67% | 70.34% |
| Llama-3.1-8B | Mitigated | 76.25% | 76.19% | 79.67% | 64.29% |

Qwen2.5-7B mitigated là cấu hình bias tốt nhất về tổng thể. Llama baseline có swap consistency cao nhưng verbosity bias cũng cao nhất.

## Kết luận

- Official V5 core: Qwen2.5-7B baseline, accuracy `94.04%`, swap `94.43%`.
- Official V5 bias: Qwen2.5-7B mitigated, conditional accuracy `79.26%`, swap `83.00%`.
- Parse success gần như hoàn toàn; lỗi chính còn lại là swap inconsistency và prompt sensitivity.
- V5 đạt Acceptance Criteria và đủ điều kiện chuyển Phase 12.
