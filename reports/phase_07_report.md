# Phase 7 Report - Judge Prompt Templates

## Status

Done.

## Scope đã thực hiện

- Tạo baseline judge prompt.
- Tạo criteria-aware prompts theo 3 domain.
- Tạo bias-mitigated prompt.
- Implement prompt renderer có AB/BA swap.
- Thêm tests để kiểm prompt không leak gold và render đúng.

## Files đã tạo/sửa

- `prompts/baseline_generic_vi.md`
- `prompts/criteria_fact_check_vi.md`
- `prompts/criteria_instruction_vi.md`
- `prompts/criteria_safety_vi.md`
- `prompts/criteria_bias_mitigated_vi.md`
- `prompts/fewshot_examples.jsonl`
- `src/vi_ppe/prompt_render.py`
- `tests/test_prompt_render.py`
- `reports/prompt_design_notes.md`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands đã chạy

```bash
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template baseline_generic_vi --order AB
python -m src.vi_ppe.prompt_render --pair-id factcheck_000001 --dataset data/samples/smoke_pairs.jsonl --template criteria_fact_check_vi --order BA
pytest -q tests/test_prompt_render.py
pytest -q
```

## Kết quả test

- Baseline render: pass.
- Criteria render với BA swap: pass.
- Prompt tests: pass.
- Full pytest: pass, `20 passed in 0.14s`.

## Acceptance Criteria

- [x] Prompt không lộ gold.
- [x] Render AB/BA đúng.
- [x] Output JSON schema rõ.

## Ghi chú

Renderer hỗ trợ `auto_criteria_by_domain` để map domain sang template criteria tương ứng. CLI đã ép stdout UTF-8 để in tiếng Việt ổn trên Windows.

## Kết luận

Phase 7 đủ điều kiện chuyển sang Phase 8.

## Cập nhật prompt freeze cho V5

V5 sử dụng các prompt tiếng Việt ngắn, output JSON thuần và quy tắc `tie` chặt hơn:

- `baseline_generic_vi`: generic baseline cho core test.
- `auto_criteria_by_domain`: chọn criteria prompt theo fact-check, instruction hoặc safety.
- `criteria_bias_mitigated_vi`: cảnh báo không thưởng response chỉ vì dài hoặc polished hơn.

Kết quả V5 xác nhận baseline ngắn là cấu hình core tốt nhất; criteria prompt không được xem là mặc định tốt hơn cho mọi domain.
