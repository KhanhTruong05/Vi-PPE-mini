# Prompt Design Notes

Phase 7 defines judge prompt templates for baseline, criteria-aware, and
bias-mitigated evaluations.

## Principles

- All prompts require valid JSON output.
- Prompts never include `gold_winner` or `gold_reason`.
- Criteria-aware prompts explicitly warn against rewarding length or polished
  style when correctness, evidence, safety, or instruction-following is worse.
- `BA` order swaps responses at render time. Aggregation will map the winner
  back to original A/B space in a later phase.

## Templates

- `baseline_generic_vi.md`
- `criteria_fact_check_vi.md`
- `criteria_instruction_vi.md`
- `criteria_safety_vi.md`
- `criteria_bias_mitigated_vi.md`

