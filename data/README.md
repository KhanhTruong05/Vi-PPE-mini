# Vi-PPE-mini Data

The released benchmark contains 900 reviewed Vietnamese pairwise preference examples across fact checking, instruction following, and safety.

## Frozen Benchmark

| Split | Fact check | Instruction | Safety | Total |
|---|---:|---:|---:|---:|
| Development | 34 | 33 | 30 | 97 |
| Main test | 166 | 167 | 170 | 503 |
| Controlled bias | 100 | 100 | 100 | 300 |
| **Total** | **300** | **300** | **300** | **900** |

Primary files:

| File | Role |
|---|---|
| `processed/pairs_dev_llm_v4.jsonl` | Development pairs |
| `processed/pairs_test_llm_v4.jsonl` | Main held-out test pairs |
| `processed/bias_subset_llm_v4.jsonl` | Controlled verbosity/style pairs |
| `processed/dataset_manifest_llm_v4.json` | Frozen counts and SHA256 hashes |

## Sources and Construction

- Fact checking uses ViFactCheck claims and evidence.
- Instruction following uses Vietnamese task templates and UIT-ViQuAD2.0-style content.
- Safety uses UIT-ViHSD examples and manually designed safety tasks.
- GPT-assisted generation converts normalized items into controlled better/worse response pairs.
- Two project reviewers verify the gold winner and rationale using domain-specific rubrics.

Each pair stores the Vietnamese prompt, optional evidence, Response A, Response B, gold winner, gold rationale, domain criteria, perturbation type, and provenance metadata. The gold label is hidden during judge inference.

See `reports/dataset_card_llm_v4_frozen.md`, `reports/annotation_guideline.md`, and `reports/real_data_sources.md` for details and upstream-license notes.

## Agreement Audit

The local `processed/iaa/` sheets support an optional two-annotator agreement audit. These working sheets are not tracked in the public repository and do not alter the frozen benchmark or the reported results unless a new dataset version is explicitly released.
