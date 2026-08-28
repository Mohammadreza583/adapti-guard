import json
from pathlib import Path
from collections import Counter

TRAIN = Path("dataset/processed/NotInject/train_final.json")
VALID = Path("dataset/raw/NotInject/datasets/valid.json")

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def stats(name, data):
    labels = Counter(x.get("label") for x in data)

    print()
    print("=" * 80)
    print(name)
    print("=" * 80)
    print(f"Records: {len(data):,}")

    for label, count in sorted(labels.items()):
        print(f"Label {label}: {count:,} ({count/len(data)*100:.2f}%)")

    print()
    print("Sources:")
    sources = Counter(x.get("source", "UNKNOWN") for x in data)
    for source, count in sources.most_common():
        print(f"  {source}: {count:,}")

def examples(data, label, n=10):
    rows = [x for x in data if x.get("label") == label]

    print()
    print("-" * 80)
    print(f"LABEL {label} EXAMPLES")
    print("-" * 80)

    for i, row in enumerate(rows[:n], 1):
        prompt = str(row.get("prompt", "")).replace("\n", " ")
        print(f"{i}. {prompt[:500]}")
        print(f"   source={row.get('source', 'UNKNOWN')}")

train = load(TRAIN)
valid = load(VALID)

stats("TRAIN", train)
stats("VALIDATION", valid)

examples(train, 0, 10)
examples(train, 1, 10)

print()
print("=" * 80)
print("NOTINJECT LABEL AUDIT COMPLETE")
print("=" * 80)
print("No data was modified.")
