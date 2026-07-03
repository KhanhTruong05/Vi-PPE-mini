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

- Split counts: {'dev': 100, 'test': 500, 'bias': 150}
- Core domain counts: {'fact_check': 200, 'instruction': 200, 'safety': 200}
- Source counts: {'ViFactCheck': 250, 'synthetic_instruction_templates': 250, 'manual_safety_templates': 190, 'ViHSD': 60}
- Perturbation counts: {'correct_vs_hallucinated': 100, 'evidence_grounded_vs_unsupported': 100, 'format_following_vs_format_violation': 100, 'helpful_safe_vs_over_refusal': 118, 'constraint_following_vs_over_elaboration': 100, 'safe_refusal_vs_unsafe_compliance': 110, 'concise_correct_vs_verbose_wrong': 17, 'instruction_following_vs_over_elaboration': 50, 'same_content_different_length': 17, 'appropriate_refusal_vs_verbose_moralizing': 22, 'plain_style_vs_polished_style': 16}

## License And Provenance Notes

- Keep upstream license notes from each record before redistribution.
- `tranthaihoa/vifactcheck` dataset card lists MIT.
- `ura-hcmut/UIT-ViHSD` requires careful review of use restrictions before redistribution.
- `taidng/UIT-ViQuAD2.0` license should be verified before redistribution.

## Manifest

See `data/processed/dataset_manifest_v3.json` for SHA256 hashes and record counts.
