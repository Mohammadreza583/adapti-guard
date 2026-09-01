#!/usr/bin/env python3
"""Build datasets/benchmark_v3 from available sources. Does NOT fabricate real benchmark rows."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "datasets" / "benchmark_v3"
CATEGORIES = [
    "direct_prompt_injection",
    "indirect_prompt_injection",
    "jailbreak",
    "rag_injection",
    "agent_attacks",
    "tool_attacks",
    "benign_tasks",
]

SOURCE_PATHS = {
    "NotInject_train": ROOT / "dataset/processed/NotInject/train_final.json",
    "NotInject_valid": ROOT / "dataset/raw/NotInject/datasets/valid.json",
    "BIPIA": ROOT / "BIPIA",
    "InjecAgent": ROOT / "dataset/raw/InjecAgent",
    "TensorTrust": ROOT / "dataset/raw/TensorTrust",
    "PIArena": ROOT / "dataset/raw/PIArena",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_notinject(path: Path, split: str, category_map: dict) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for i, row in enumerate(data):
        label = int(row.get("label", 0))
        prompt = row.get("prompt") or row.get("text") or ""
        cat = category_map.get(row.get("source", ""), "direct_prompt_injection" if label else "benign_tasks")
        rows.append({
            "id": f"notinject_{split}_{i:06d}",
            "category": cat,
            "subcategory": str(row.get("source", "notinject")),
            "prompt": prompt,
            "source": "NotInject",
            "severity": "high" if label else "none",
            "attack_type": cat,
            "label": label,
            "split": split,
        })
    return rows


def dedup(rows: list[dict]) -> tuple[list[dict], dict]:
    seen = set()
    kept = []
    removed = 0
    for r in rows:
        key = normalize(r["prompt"])
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        kept.append(r)
    before = len(rows)
    return kept, {
        "method": "exact_normalized_prompt",
        "before": before,
        "after": len(kept),
        "removed": removed,
        "duplicate_rate": removed / before if before else 0.0,
    }


def stratified_split(rows: list[dict], train_ratio=0.7, val_ratio=0.15) -> dict[str, list[dict]]:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)

    splits = {"train": [], "validation": [], "test": []}
    for cat, items in by_cat.items():
        n = len(items)
        n_train = max(1, int(n * train_ratio)) if n >= 3 else 0
        n_val = max(1, int(n * val_ratio)) if n >= 3 else 0
        if n < 3:
            for item in items:
                item["split"] = "test"
                splits["test"].append(item)
            continue
        for i, item in enumerate(items):
            if i < n_train:
                item["split"] = "train"
                splits["train"].append(item)
            elif i < n_train + n_val:
                item["split"] = "validation"
                splits["validation"].append(item)
            else:
                item["split"] = "test"
                splits["test"].append(item)
    return splits


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    availability = {}
    all_rows: list[dict] = []

    category_map = {"injection": "direct_prompt_injection"}

    for name, path in SOURCE_PATHS.items():
        if path.exists() and path.is_file():
            split = "train" if "train" in name else "validation"
            rows = load_notinject(path, split, category_map)
            availability[name] = f"LOADED ({len(rows)})"
            all_rows.extend(rows)
        elif path.exists():
            availability[name] = "PRESENT_UNPARSED"
        else:
            availability[name] = "DATASET_UNAVAILABLE"

    publication_ready = any(v.startswith("LOADED") for v in availability.values())

    if not publication_ready:
        # Document smoke-only internal templates — NOT publication evidence
        from scripts.generate_attack_stream import generate_stream

        stream = generate_stream(100)
        benign = [
            "What is the capital of Germany?",
            "Summarize the benefits of regular exercise.",
            "Explain what a database is.",
        ]
        mapping = {
            "direct_injection": "direct_prompt_injection",
            "indirect_injection": "indirect_prompt_injection",
            "context_manipulation": "rag_injection",
            "tool_output_injection": "tool_attacks",
        }
        for i, row in enumerate(stream[:40]):
            all_rows.append({
                "id": f"smoke_{i:04d}",
                "category": mapping.get(row["attack_family"], "direct_prompt_injection"),
                "subcategory": "template",
                "prompt": row["payload"],
                "source": "internal_smoke",
                "severity": "medium",
                "attack_type": row["attack_family"],
                "label": 1,
                "split": "test",
                "metadata": {"warning": "SMOKE_ONLY_NOT_PUBLICATION_EVIDENCE"},
            })
        for i, text in enumerate(benign):
            all_rows.append({
                "id": f"smoke_benign_{i:04d}",
                "category": "benign_tasks",
                "subcategory": "qa",
                "prompt": text,
                "source": "internal_smoke",
                "severity": "none",
                "attack_type": "benign",
                "label": 0,
                "split": "test",
                "metadata": {"warning": "SMOKE_ONLY_NOT_PUBLICATION_EVIDENCE"},
            })
        availability["internal_smoke"] = "GENERATED_SMOKE_ONLY"

    deduped, dedup_report = dedup(all_rows)
    splits = stratified_split(deduped) if publication_ready else {
        "train": [], "validation": [], "test": deduped,
    }

    for split_name, rows in splits.items():
        write_jsonl(OUT / f"{split_name}.jsonl", rows)

    labels = Counter(r["label"] for r in deduped)
    cats = Counter(r["category"] for r in deduped)
    sources = Counter(r["source"] for r in deduped)

    statistics = {
        "total": len(deduped),
        "train": len(splits["train"]),
        "validation": len(splits["validation"]),
        "test": len(splits["test"]),
        "label_distribution": dict(labels),
        "category_distribution": dict(cats),
        "source_distribution": dict(sources),
        "dedup_report": dedup_report,
        "availability": availability,
        "publication_ready": publication_ready,
        "required_categories": {c: cats.get(c, 0) for c in CATEGORIES},
        "sha256": {
            s: sha256_file(OUT / f"{s}.jsonl") if (OUT / f"{s}.jsonl").exists() else None
            for s in ("train", "validation", "test")
        },
    }

    with (OUT / "statistics.json").open("w", encoding="utf-8") as f:
        json.dump(statistics, f, indent=2)
        f.write("\n")

    card = f"""# benchmark_v3 Dataset Card

## Status
- publication_ready: **{publication_ready}**
- total samples: {len(deduped)}

## Sources
{json.dumps(availability, indent=2)}

## Category coverage
{json.dumps(statistics['required_categories'], indent=2)}

## Dedup
{json.dumps(dedup_report, indent=2)}

## Warning
If publication_ready is false, this bundle is smoke/infrastructure only.
"""
    (OUT / "dataset_card.md").write_text(card, encoding="utf-8")
    print(json.dumps(statistics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
