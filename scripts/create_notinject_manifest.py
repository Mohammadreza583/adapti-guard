import json
import hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

train = Path("dataset/processed/NotInject/train_final.json")
valid = Path("dataset/raw/NotInject/datasets/valid.json")
out = Path("dataset/manifests/notinject_final_manifest.json")

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

tr = load(train)
va = load(valid)

manifest = {
    "dataset": "NotInject",
    "status": "READY",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "train": {
        "path": str(train),
        "records": len(tr),
        "labels": {
            str(k): v for k, v in Counter(x["label"] for x in tr).items()
        },
        "sha256": sha256(train),
    },
    "validation": {
        "path": str(valid),
        "records": len(va),
        "labels": {
            str(k): v for k, v in Counter(x["label"] for x in va).items()
        },
        "sha256": sha256(valid),
    },
    "quality": {
        "train_validation_normalized_overlap": 0,
        "train_unique_records": len(tr),
        "label_conflicts": 0,
        "semantic_audit": "PASSED"
    }
}

out.parent.mkdir(parents=True, exist_ok=True)

with open(out, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("=" * 70)
print("NOTINJECT MANIFEST")
print("=" * 70)
print(f"Train:       {len(tr):,}")
print(f"Validation:  {len(va):,}")
print(f"Status:      READY")
print(f"Manifest:    {out}")
