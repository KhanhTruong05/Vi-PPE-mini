# Real Data Sources

The real-data pass uses three Hugging Face datasets:

| Adapter | Hugging Face dataset | Domain | License/provenance note |
|---|---|---|---|
| `viquad` | `taidng/UIT-ViQuAD2.0` | `fact_check` / evidence-grounded QA | Verify upstream license before redistribution. |
| `vifactcheck` | `tranthaihoa/vifactcheck` | `fact_check` | Dataset card lists MIT. |
| `vihsd` | `ura-hcmut/UIT-ViHSD` | `safety` | Dataset card/use restrictions should be checked before redistribution. |

`ViWikiFC` was removed because no reliable source was provided. The old local
JSONL fixtures for the three retained sources remain useful for offline tests,
but `configs/project.yaml` now points to the real Hugging Face dataset ids.

## Latest Import Smoke

- Imported 20 rows/source from each real Hugging Face dataset.
- Wrote 60 normalized source items to `data/interim/prompts_raw.jsonl`.
- Regenerated 90 core draft pairs with balanced domain counts.
- Regenerated 60 bias draft pairs with balanced domain counts.
