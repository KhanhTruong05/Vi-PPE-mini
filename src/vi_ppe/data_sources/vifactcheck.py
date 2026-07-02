from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from vi_ppe.data_sources.base import DataSourceAdapter, coalesce, load_jsonl_or_hf, make_source_item, stable_id

LABELS = {
    "0": "SUPPORTED",
    "1": "REFUTED",
    "2": "NEI",
}


class ViFactCheckAdapter(DataSourceAdapter):
    name = "vifactcheck"
    source_dataset = "ViFactCheck"
    default_license_note = "Hugging Face dataset tranthaihoa/vifactcheck; license MIT per dataset card."

    def load_raw(self, input_path_or_hf_id: str | None = None, split: str | None = None) -> Iterable[dict[str, Any]]:
        if input_path_or_hf_id is None:
            raise ValueError("vifactcheck adapter expects a local JSONL path or Hugging Face dataset id")
        path = Path(str(input_path_or_hf_id))
        if path.exists() and path.suffix == ".parquet":
            return self._load_parquet_file(path, split=split)
        if path.exists() and path.is_dir():
            return self._load_parquet_dir(path)
        return load_jsonl_or_hf(input_path_or_hf_id, split=split)

    def _load_parquet_file(self, path: Path, split: str | None = None) -> Iterable[dict[str, Any]]:
        import pandas as pd

        frame = pd.read_parquet(path)
        inferred_split = split or path.name.split("-", 1)[0]
        for row in frame.to_dict(orient="records"):
            row["_vifactcheck_split"] = inferred_split
            yield row

    def _load_parquet_dir(self, path: Path) -> Iterable[dict[str, Any]]:
        for parquet_path in sorted(path.glob("*.parquet")):
            yield from self._load_parquet_file(parquet_path)

    def normalize(self, raw_item: dict[str, Any], index: int = 0) -> dict[str, Any]:
        label_id = coalesce(raw_item, ["labels", "label", "verdict", "gold_answer", "answer"])
        label_text = LABELS.get(label_id, label_id)
        split = coalesce(raw_item, ["_vifactcheck_split"], "unknown")
        explicit_id = coalesce(raw_item, ["annotation_id", "source_example_id", "id", "index"])
        source_example_id = f"vifactcheck_{split}_{explicit_id}_{index:06d}" if explicit_id else f"vifactcheck_{split}_{index:06d}"
        evidence = coalesce(raw_item, ["Evidence", "evidence"])
        context = coalesce(raw_item, ["Context", "context", "article", "explanation"])
        return make_source_item(
            source_example_id=source_example_id or stable_id("vifactcheck", raw_item, index),
            source_dataset=self.source_dataset,
            domain_candidates=["fact_check"],
            prompt_seed=coalesce(raw_item, ["Statement", "claim", "statement", "prompt", "prompt_seed", "text"]),
            evidence=evidence or context,
            gold_answer=label_text,
            source_url=coalesce(raw_item, ["source_url", "Url", "url"]),
            license_note=coalesce(raw_item, ["license_note"], self.default_license_note),
            metadata={
                "adapter": self.name,
                "row_index": index,
                "raw_keys": sorted(k for k in raw_item.keys() if not k.startswith("_")),
                "Topic": coalesce(raw_item, ["Topic"]),
                "Author": coalesce(raw_item, ["Author"]),
                "split": split,
                "label_id": label_id,
            },
        )
