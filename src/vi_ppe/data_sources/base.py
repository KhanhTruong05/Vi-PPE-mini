from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable

from vi_ppe.io import write_jsonl
from vi_ppe.schemas import DOMAINS, validate_source_item


class DataSourceAdapter(ABC):
    name: str = "base"
    source_dataset: str = "base"
    default_license_note: str = "unknown"

    @abstractmethod
    def load_raw(self, input_path_or_hf_id: str | None = None, split: str | None = None) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, raw_item: dict[str, Any], index: int = 0) -> dict[str, Any]:
        raise NotImplementedError

    def iter_normalized(
        self, input_path_or_hf_id: str | None = None, limit: int | None = None, split: str | None = None
    ) -> list[dict[str, Any]]:
        records = []
        for index, raw in enumerate(self.load_raw(input_path_or_hf_id, split=split)):
            if limit is not None and len(records) >= limit:
                break
            item = self.normalize(raw, index=index)
            validate_source_item(item)
            records.append(item)
        return records

    def write_interim_jsonl(
        self,
        output_path: str | Path,
        input_path_or_hf_id: str | None = None,
        limit: int | None = None,
        split: str | None = None,
    ) -> list[dict[str, Any]]:
        records = self.iter_normalized(input_path_or_hf_id=input_path_or_hf_id, limit=limit, split=split)
        write_jsonl(output_path, records)
        return records


def stable_id(prefix: str, raw_item: dict[str, Any], index: int) -> str:
    explicit_id = raw_item.get("source_example_id") or raw_item.get("id")
    if explicit_id:
        return str(explicit_id)
    payload = json.dumps(raw_item, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{index + 1:06d}_{digest}"


def parse_domain_candidates(value: Any, fallback: str) -> list[str]:
    if isinstance(value, list):
        domains = [str(v).strip() for v in value if str(v).strip()]
    elif isinstance(value, str) and value.strip():
        normalized = value.replace("|", ";").replace(",", ";")
        domains = [part.strip() for part in normalized.split(";") if part.strip()]
    else:
        domains = [fallback]

    invalid = sorted(set(domains) - DOMAINS)
    if invalid:
        raise ValueError(f"Invalid domain candidates {invalid}; expected one of {sorted(DOMAINS)}")
    return domains


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    from vi_ppe.io import read_jsonl

    return read_jsonl(path)


def load_jsonl_or_hf(input_path_or_hf_id: str | Path, split: str | None = None) -> Iterable[dict[str, Any]]:
    input_value = str(input_path_or_hf_id)
    path = Path(input_value)
    if path.exists():
        return load_jsonl(path)

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError(
            "The `datasets` package is required to load Hugging Face datasets. "
            "Install requirements or provide a local JSONL path."
        ) from exc

    dataset_split = split or "train"
    dataset = load_dataset(input_value, split=dataset_split, streaming=True)
    return (dict(row) for row in dataset)


def stringify_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "answer", "answers", "label", "verdict"):
            if key in value:
                return stringify_value(value[key])
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, (list, tuple)):
        if not value:
            return ""
        return stringify_value(value[0])
    return str(value).strip()


def coalesce(raw_item: dict[str, Any], names: Iterable[str], default: str = "") -> str:
    for name in names:
        value = raw_item.get(name)
        text = stringify_value(value)
        if text:
            return text
    return default


def make_source_item(
    *,
    source_example_id: str,
    source_dataset: str,
    domain_candidates: list[str],
    prompt_seed: str,
    evidence: str = "",
    gold_answer: str = "",
    source_url: str = "",
    license_note: str = "unknown",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_example_id": source_example_id,
        "source_dataset": source_dataset,
        "domain_candidates": domain_candidates,
        "prompt_seed": prompt_seed,
        "evidence": evidence,
        "gold_answer": gold_answer,
        "source_url": source_url,
        "license_note": license_note or "unknown",
        "metadata": metadata or {},
    }


def build_adapter(name: str) -> DataSourceAdapter:
    if name == "viquad":
        from vi_ppe.data_sources.viquad import ViQuadAdapter

        return ViQuadAdapter()
    if name == "vifactcheck":
        from vi_ppe.data_sources.vifactcheck import ViFactCheckAdapter

        return ViFactCheckAdapter()
    if name == "vihsd":
        from vi_ppe.data_sources.vihsd import ViHsdAdapter

        return ViHsdAdapter()
    raise ValueError(f"Unknown data source adapter: {name}")
