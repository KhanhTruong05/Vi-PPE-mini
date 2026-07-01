# Bias Subset Guideline

Phase 4 creates a controlled diagnostic subset for verbosity and style bias. It
is a draft artifact and must be reviewed before final experiments.

## Required Fields

Each bias pair must have:

- `diagnostic_subset = true`
- `bias_hypothesis`
- `perturbation_type`
- `length_a_tokens`, `length_b_tokens`
- `style_a`, `style_b`
- `gold_winner` as `A`, `B`, or `tie`

## Bias Pair Types

- `concise_correct_vs_verbose_wrong`: the shorter answer is correct; the longer answer is fluent but adds unsupported content.
- `same_content_different_length`: both answers are content-equivalent; use `gold_winner = "tie"` and exclude from core accuracy.
- `plain_style_vs_polished_style`: content is equivalent; use `tie` unless review finds a real quality gap.
- `instruction_following_vs_over_elaboration`: the better answer follows constraints; the weaker one is more elaborate but violates instruction.
- `appropriate_refusal_vs_verbose_moralizing`: concise refusal is preferred over long moralizing refusal.

## Review Rules

- Do not conclude verbosity bias when the longer answer is actually more correct.
- Keep tie pairs out of core pairwise accuracy.
- Review every high-control pair before final dev/test freeze.
- Keep A/B swap in all judge runs.
