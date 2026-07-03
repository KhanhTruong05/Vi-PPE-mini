# Dataset Card: Vi-PPE-mini

## Status

Frozen local sample built from reviewed/bootstrap-reviewed records. This is suitable for pipeline validation; final thesis runs still require larger human-reviewed data.

## Sources

- `taidng/UIT-ViQuAD2.0` via `viquad` adapter.
- `tranthaihoa/vifactcheck` via `vifactcheck` adapter.
- `ura-hcmut/UIT-ViHSD` via `vihsd` adapter.
- `synthetic_instruction_templates` for instruction-following pairs.
- `manual_safety_templates` for controlled safety/refusal pairs.

## Counts

- Split counts: {'dev': 97, 'test': 503, 'bias': 300}
- Core domain counts: {'fact_check': 200, 'instruction': 200, 'safety': 200}
- Source counts: {'ViFactCheck': 280, 'llm_generated_instruction_seed': 300, 'ViHSD': 300, 'UIT-ViQuAD2.0': 20}
- Perturbation counts: {'faithful_vs_subtle_hallucination': 67, 'correct_concise_vs_fluent_unsupported': 66, 'constraint_following_vs_near_miss': 67, 'appropriate_refusal_vs_unsafe_compliance': 67, 'safe_alternative_vs_moralizing_refusal': 66, 'helpful_safe_vs_over_refusal': 67, 'grounded_calibrated_vs_overconfident': 67, 'format_correct_vs_extra_content': 67, 'complete_specific_vs_generic_filler': 66, 'concise_correct_vs_verbose_wrong': 34, 'instruction_following_vs_over_elaboration': 34, 'appropriate_refusal_vs_verbose_moralizing': 34, 'same_content_different_length': 66, 'helpful_safe_vs_verbose_over_refusal': 33, 'plain_style_vs_polished_style': 99}

## License And Provenance Notes

- Keep upstream license notes from each record before redistribution.
- `tranthaihoa/vifactcheck` dataset card lists MIT.
- `ura-hcmut/UIT-ViHSD` requires careful review of use restrictions before redistribution.
- `taidng/UIT-ViQuAD2.0` license should be verified before redistribution.

## Manifest

See `data/processed/dataset_manifest_llm_v4.json` for SHA256 hashes and record counts.
