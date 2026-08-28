import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapti_guard.detector.prompt_injection_detector import (
    PromptInjectionDetector
)

DATA = ROOT / "dataset/processed/NotInject/train_final.json"

with open(DATA, encoding="utf-8") as f:
    data = json.load(f)

detector = PromptInjectionDetector()

tp = tn = fp = fn = 0
fn_examples = []
fp_examples = []

for r in data:
    label = int(r["label"])
    text = r["prompt"]

    result = detector.detect(text)
    pred = int(result.is_injection)

    if label == 1 and pred == 1:
        tp += 1

    elif label == 0 and pred == 0:
        tn += 1

    elif label == 0 and pred == 1:
        fp += 1
        if len(fp_examples) < 30:
            fp_examples.append((text, result))

    elif label == 1 and pred == 0:
        fn += 1
        if len(fn_examples) < 50:
            fn_examples.append((text, result))


print("=" * 80)
print("NOTINJECT FULL DETECTOR ERROR ANALYSIS")
print("=" * 80)

print(f"Total: {len(data):,}")
print(f"TP:    {tp:,}")
print(f"TN:    {tn:,}")
print(f"FP:    {fp:,}")
print(f"FN:    {fn:,}")

print()
print("=" * 80)
print("FALSE NEGATIVE EXAMPLES")
print("=" * 80)

for i, (text, result) in enumerate(fn_examples, 1):
    print()
    print(f"[FN {i}]")
    print(f"Score:      {result.injection_probability}")
    print(f"Indicators: {result.indicators}")
    print(f"Prompt:     {text[:1000]}")

print()
print("=" * 80)
print("FALSE POSITIVE EXAMPLES")
print("=" * 80)

for i, (text, result) in enumerate(fp_examples, 1):
    print()
    print(f"[FP {i}]")
    print(f"Score:      {result.injection_probability}")
    print(f"Indicators: {result.indicators}")
    print(f"Prompt:     {text[:1000]}")

print()
print("=" * 80)
print("DONE")
print("=" * 80)
