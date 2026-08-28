import json
import hashlib
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = Path(".")
RAW = ROOT / "dataset/raw/NotInject/datasets"
PROC = ROOT / "dataset/processed/NotInject"
MAN = ROOT / "dataset/manifests"

TRAIN = RAW / "train.json"
VALID = RAW / "valid.json"
CLEAN = PROC / "train_clean.json"
BACKUP = PROC / "train_clean_backup.json"

MAN.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def prompt_hash(text):
    return hashlib.sha256(
        normalize(text).encode("utf-8")
    ).hexdigest()


print("=" * 80)
print("NOTINJECT FINAL QUALITY AUDIT")
print("=" * 80)

# ------------------------------------------------------------------
# 1. Backup
# ------------------------------------------------------------------

if not BACKUP.exists():
    BACKUP.write_bytes(CLEAN.read_bytes())
    print("\n[OK] Backup created")
else:
    print("\n[OK] Backup already exists")

# ------------------------------------------------------------------
# 2. Load
# ------------------------------------------------------------------

train_raw = load(TRAIN)
train_clean = load(CLEAN)
valid = load(VALID)

# ------------------------------------------------------------------
# 3. Exact duplicates in cleaned dataset
# ------------------------------------------------------------------

exact_seen = set()
exact_duplicates = 0

for r in train_clean:
    p = r.get("prompt", "")
    h = hashlib.sha256(p.strip().encode("utf-8")).hexdigest()

    if h in exact_seen:
        exact_duplicates += 1
    else:
        exact_seen.add(h)

# ------------------------------------------------------------------
# 4. Normalized duplicates
# ------------------------------------------------------------------

norm_groups = defaultdict(list)

for i, r in enumerate(train_clean):
    p = r.get("prompt", "")
    norm_groups[prompt_hash(p)].append(i)

normalized_duplicate_groups = {
    h: ids
    for h, ids in norm_groups.items()
    if len(ids) > 1
}

normalized_duplicate_rows = sum(
    len(ids) - 1
    for ids in normalized_duplicate_groups.values()
)

# ------------------------------------------------------------------
# 5. Conflicting labels
# ------------------------------------------------------------------

conflicting_groups = []

for h, ids in normalized_duplicate_groups.items():
    labels = {
        train_clean[i].get("label")
        for i in ids
    }

    if len(labels) > 1:
        conflicting_groups.append({
            "hash": h,
            "indices": ids,
            "labels": sorted(str(x) for x in labels)
        })

# ------------------------------------------------------------------
# 6. Train / validation leakage
# ------------------------------------------------------------------

train_exact = {
    r.get("prompt", "").strip()
    for r in train_clean
}

valid_exact = {
    r.get("prompt", "").strip()
    for r in valid
}

exact_leakage = train_exact & valid_exact

train_norm = {
    normalize(r.get("prompt", ""))
    for r in train_clean
}

valid_norm = {
    normalize(r.get("prompt", ""))
    for r in valid
}

normalized_leakage = train_norm & valid_norm

# ------------------------------------------------------------------
# 7. Label distributions
# ------------------------------------------------------------------

train_labels = Counter(
    r.get("label")
    for r in train_clean
    if isinstance(r, dict)
)

valid_labels = Counter(
    r.get("label")
    for r in valid
    if isinstance(r, dict)
)

# ------------------------------------------------------------------
# 8. Structural checks
# ------------------------------------------------------------------

empty = 0
malformed = 0

for r in train_clean:
    if not isinstance(r, dict):
        malformed += 1
        continue

    if not r.get("prompt", "").strip():
        empty += 1

    if r.get("label") not in (0, 1):
        malformed += 1

# ------------------------------------------------------------------
# 9. Suspicious label heuristic
# ------------------------------------------------------------------

suspicious_label_0 = []
suspicious_label_1 = []

injection_terms = [
    "ignore previous",
    "ignore all previous",
    "system prompt",
    "jailbreak",
    "do anything now",
    "dan ",
    "bypass",
    "override instructions",
    "forget previous",
]

for i, r in enumerate(train_clean):
    prompt = normalize(r.get("prompt", ""))
    label = r.get("label")

    hits = sum(term in prompt for term in injection_terms)

    if label == 0 and hits >= 2:
        suspicious_label_0.append(i)

    if label == 1 and hits == 0:
        suspicious_label_1.append(i)

# ------------------------------------------------------------------
# 10. Reports
# ------------------------------------------------------------------

near_report = {
    "dataset": "NotInject",
    "records": len(train_clean),
    "exact_duplicate_rows": exact_duplicates,
    "normalized_duplicate_groups": len(normalized_duplicate_groups),
    "normalized_duplicate_rows": normalized_duplicate_rows,
    "conflicting_label_groups": len(conflicting_groups),
    "conflicting_groups": conflicting_groups,
}

label_report = {
    "dataset": "NotInject",
    "records": len(train_clean),
    "label_distribution": dict(train_labels),
    "suspicious_label_0_count": len(suspicious_label_0),
    "suspicious_label_1_count": len(suspicious_label_1),
    "note": (
        "Suspicious examples are heuristic candidates only; "
        "no automatic relabeling was performed."
    ),
}

validation_report = {
    "train_records": len(train_clean),
    "validation_records": len(valid),
    "validation_labels": dict(valid_labels),
    "exact_overlap": len(exact_leakage),
    "normalized_overlap": len(normalized_leakage),
    "assessment": (
        "Small validation set; retained unchanged for reproducibility."
        if len(valid) < 500
        else "Validation size acceptable for the current evaluation."
    ),
}

final_hash = sha256(CLEAN)

warnings = []

if len(valid) < 500:
    warnings.append("Validation set is relatively small.")

if len(normalized_duplicate_groups) > 0:
    warnings.append("Normalized duplicate candidates exist.")

if len(conflicting_groups) > 0:
    warnings.append("Conflicting-label groups exist.")

if len(normalized_leakage) > 0:
    warnings.append("Normalized train/validation leakage detected.")

if abs(train_labels.get(0, 0) - train_labels.get(1, 0)) > len(train_clean) * 0.5:
    warnings.append("Class imbalance is substantial; use balanced metrics.")

final_report = {
    "dataset": "NotInject",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "source": str(TRAIN),
    "processed": str(CLEAN),
    "original_records": len(train_raw),
    "final_records": len(train_clean),
    "removed_records": len(train_raw) - len(train_clean),
    "label_distribution": dict(train_labels),
    "empty_records": empty,
    "malformed_records": malformed,
    "exact_duplicate_rows": exact_duplicates,
    "normalized_duplicate_groups": len(normalized_duplicate_groups),
    "normalized_duplicate_rows": normalized_duplicate_rows,
    "conflicting_label_groups": len(conflicting_groups),
    "train_validation_exact_overlap": len(exact_leakage),
    "train_validation_normalized_overlap": len(normalized_leakage),
    "validation_records": len(valid),
    "validation_label_distribution": dict(valid_labels),
    "suspicious_label_0": len(suspicious_label_0),
    "suspicious_label_1": len(suspicious_label_1),
    "sha256": final_hash,
    "warnings": warnings,
    "status": (
        "READY"
        if (
            empty == 0
            and malformed == 0
            and len(exact_leakage) == 0
            and len(normalized_leakage) == 0
            and len(conflicting_groups) == 0
        )
        else "NEEDS_REVIEW"
    ),
}

manifest = {
    "dataset": "NotInject",
    "source_path": str(TRAIN),
    "processed_path": str(CLEAN),
    "backup_path": str(BACKUP),
    "processed_at_utc": datetime.now(timezone.utc).isoformat(),
    "processing": [
        "Removed exact duplicate prompts",
        "Removed conflicting-label duplicate groups",
        "Preserved raw dataset",
        "Preserved validation dataset",
        "No automatic relabeling",
        "Deterministic SHA-256 fingerprinting",
    ],
    "original_records": len(train_raw),
    "final_records": len(train_clean),
    "label_distribution": dict(train_labels),
    "sha256": final_hash,
}

save(MAN / "notinject_near_duplicate_report.json", near_report)
save(MAN / "notinject_label_audit.json", label_report)
save(MAN / "notinject_validation_audit.json", validation_report)
save(MAN / "notinject_final_quality_report.json", final_report)
save(MAN / "notinject_dataset_manifest.json", manifest)

# ------------------------------------------------------------------
# Final console
# ------------------------------------------------------------------

print("\n" + "=" * 80)
print("NOTINJECT FINAL STATUS")
print("=" * 80)
print(f"Records:                  {len(train_clean):,}")
print(f"Label 0:                  {train_labels.get(0, 0):,}")
print(f"Label 1:                  {train_labels.get(1, 0):,}")
print(f"Exact duplicates:         {exact_duplicates}")
print(f"Normalized duplicate rows:{normalized_duplicate_rows}")
print(f"Conflicting groups:       {len(conflicting_groups)}")
print(f"Train/valid exact leak:   {len(exact_leakage)}")
print(f"Train/valid norm. leak:   {len(normalized_leakage)}")
print(f"Validation records:       {len(valid):,}")
print(f"Warnings:                 {len(warnings)}")
print(f"SHA256:                   {final_hash}")
print(f"Status:                   {final_report['status']}")
print("=" * 80)
