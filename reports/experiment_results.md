# Vi-PPE-mini Experiment Results

This summary mirrors the official **V5** results reported in `Vi-PPE-mini-paper.pdf`. The experiments use the frozen 503-pair held-out test set and the separate 300-pair controlled bias subset. Every pair is judged in AB and BA order.

## Main Held-Out Test

All values are percentages.

| Model | Prompt | Accuracy | Macro | Swap | Parse |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | Baseline | 83.70 | 83.63 | 84.89 | 100.00 |
| Qwen2.5-3B | Criteria | 75.15 | 75.11 | 73.56 | 100.00 |
| **Qwen2.5-7B** | **Baseline** | **94.04** | **94.00** | **94.43** | **100.00** |
| Qwen2.5-7B | Criteria | 90.06 | 90.00 | 91.45 | 99.90 |
| Gemma-3-4B | Baseline | 86.48 | 86.42 | 87.67 | 99.11 |
| Gemma-3-4B | Criteria | 76.34 | 76.32 | 77.14 | 100.00 |
| Llama-3.1-8B | Baseline | 86.88 | 86.79 | 88.27 | 100.00 |
| Llama-3.1-8B | Criteria | 89.86 | 89.80 | 91.45 | 100.00 |

## Accuracy by Domain

| Model | Prompt | Fact check | Instruction | Safety |
|---|---|---:|---:|---:|
| Qwen2.5-3B | Baseline | 83.13 | 73.05 | 94.71 |
| Qwen2.5-3B | Criteria | 87.95 | 51.50 | 85.88 |
| **Qwen2.5-7B** | **Baseline** | **93.37** | **89.22** | **99.41** |
| Qwen2.5-7B | Criteria | 86.14 | 85.63 | 98.24 |
| Gemma-3-4B | Baseline | 81.93 | 81.44 | 95.88 |
| Gemma-3-4B | Criteria | 84.34 | 62.28 | 82.35 |
| Llama-3.1-8B | Baseline | 80.12 | 80.84 | 99.41 |
| Llama-3.1-8B | Criteria | 89.16 | 80.84 | 99.41 |

## Controlled Bias Subset

| Model | Prompt | Conditional accuracy | Macro | Swap | Verbosity |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | Baseline | 62.88 | 62.79 | 66.67 | 65.00 |
| Qwen2.5-3B | Bias-mitigated | 62.88 | 62.81 | 62.00 | 53.27 |
| Qwen2.5-7B | Baseline | 76.59 | 76.49 | 79.33 | 55.20 |
| **Qwen2.5-7B** | **Bias-mitigated** | **79.26** | **79.20** | **83.00** | **47.83** |
| Gemma-3-4B | Baseline | 73.91 | 73.87 | 77.33 | 55.91 |
| Gemma-3-4B | Bias-mitigated | 67.89 | 67.82 | 69.33 | 56.07 |
| Llama-3.1-8B | Baseline | 77.26 | 77.19 | 86.67 | 70.34 |
| Llama-3.1-8B | Bias-mitigated | 76.25 | 76.19 | 79.67 | 64.29 |

Normalized polished-style selection rates for bias-mitigated prompts were 40.74% for Qwen2.5-3B, 48.81% for Qwen2.5-7B, 49.32% for Gemma-3-4B, and 47.37% for Llama-3.1-8B. These values are diagnostic and do not prove that style bias is absent.

## Main Findings

- Qwen2.5-7B with the concise generic prompt is the strongest core judge.
- Criteria prompts can help fact checking but often reduce instruction-following accuracy.
- Bias mitigation helps Qwen2.5-7B on the controlled subset, but the effect does not transfer consistently to every model.
- Swap consistency reveals order sensitivity that single-order accuracy would hide.
- Stricter checklist-like prompting can induce evaluation hallucinations and over-focus on secondary constraints.
