# Pair Generation Notes

Phase 3 creates draft pairwise examples from normalized source items. These
pairs are not frozen labels; they must pass annotation/review in later phases.

## Domains

- `fact_check`: generated from ViQuAD-like, ViWikiFC-like, and ViFactCheck-like source items.
- `safety`: generated from ViHSD-like source items.
- `instruction`: generated from internal synthetic instruction templates because `Manual CSV` was removed from Source Priority by request.

## Rules

- Prompts do not include `gold_winner` or `gold_reason`.
- Each pair has one stronger response and one plausible weaker response.
- A/B ordering is deterministic by `pair_id` hash.
- Draft pairs use `review_status = "draft"` and `split = "draft"`.
- Every pair keeps source provenance through `source_dataset`, `source_example_id`, `source_url`, `license_note`, and `metadata`.

## Known Limits

- Current local fixtures are small and synthetic, intended to validate the pipeline.
- Real dataset-scale pair generation still requires replacing fixtures with licensed upstream data and manual review.
- Instruction pairs are template-generated until a non-Manual-CSV instruction source is chosen.
