import json
import hashlib
from pathlib import Path

SRC = Path("dataset/raw/NotInject/datasets/train.json")
OUT = Path("dataset/processed/NotInject/train_clean.json")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

groups = {}

for record in data:
    prompt = record.get("prompt", "").strip()
    if not prompt:
        continue

    h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    if h not in groups:
        groups[h] = []
    
    groups[h].append(record)

clean = []
conflicts = []

for h, records in groups.items():
    labels = {r.get("label") for r in records}

    if len(labels) > 1:
        conflicts.append(records)
        continue

    clean.append(records[0])

OUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)

print("=" * 70)
print("NOTINJECT CLEANING")
print("=" * 70)
print(f"Original records:       {len(data):,}")
print(f"Unique records:         {len(clean):,}")
print(f"Removed duplicates:     {len(data) - len(clean) - sum(len(x) for x in conflicts):,}")
print(f"Conflicting groups:     {len(conflicts):,}")
print(f"Conflicting rows:       {sum(len(x) for x in conflicts):,}")
print(f"Final records:          {len(clean):,}")
print(f"Output:                 {OUT}")
