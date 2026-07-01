# Dataset Card: Vi-PPE-mini

## Status

Frozen local sample built from reviewed/bootstrap-reviewed records. This is suitable for pipeline validation; final thesis runs still require larger human-reviewed data.

## Sources

- `taidng/UIT-ViQuAD2.0` via `viquad` adapter.
- `tranthaihoa/vifactcheck` via `vifactcheck` adapter.
- `ura-hcmut/UIT-ViHSD` via `vihsd` adapter.
- `synthetic_instruction_templates` for instruction-following pairs.

## Counts

- Split counts: {'dev': 11, 'test': 39, 'bias': 60}
- Core domain counts: {'fact_check': 17, 'instruction': 17, 'safety': 16}
- Source counts: {'UIT-ViQuAD2.0': 37, 'synthetic_instruction_templates': 37, 'ViHSD': 36}
- Perturbation counts: {'correct_vs_hallucinated': 9, 'evidence_grounded_vs_unsupported': 8, 'format_following_vs_format_violation': 11, 'helpful_safe_vs_over_refusal': 16, 'constraint_following_vs_over_elaboration': 6, 'concise_correct_vs_verbose_wrong': 7, 'instruction_following_vs_over_elaboration': 20, 'appropriate_refusal_vs_verbose_moralizing': 20, 'same_content_different_length': 7, 'plain_style_vs_polished_style': 6}

## License And Provenance Notes

- Keep upstream license notes from each record before redistribution.
- `tranthaihoa/vifactcheck` dataset card lists MIT.
- `ura-hcmut/UIT-ViHSD` requires careful review of use restrictions before redistribution.
- `taidng/UIT-ViQuAD2.0` license should be verified before redistribution.

## Manifest

See `C:\Users\Lenovo\Desktop\KYf\LLM\Vi-PPE-mini\data\processed\dataset_manifest.json` for SHA256 hashes and record counts.
