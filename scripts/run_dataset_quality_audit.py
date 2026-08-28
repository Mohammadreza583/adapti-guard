import json
import hashlib
from pathlib import Path
from collections import Counter

ROOTS = [
    ("BIPIA", Path("BIPIA")),
    ("AgentHarm", Path("dataset/raw/AgentHarm")),
    ("InjecAgent", Path("dataset/raw/InjecAgent")),
    ("PIArena", Path("dataset/raw/PIArena")),
    ("TensorTrust", Path("dataset/raw/TensorTrust")),
    ("NotInject", Path("dataset/raw/NotInject")),
    ("ASB", Path("dataset/raw/ASB")),
]


def fingerprint(obj):
    text = json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=False
    )
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def analyze_records(records):
    fingerprints = []
    keys = Counter()
    empty = 0
    malformed = 0

    for record in records:

        if record in ({}, [], "", None):
            empty += 1

        if not isinstance(record, (dict, list, str)):
            malformed += 1

        if isinstance(record, dict):
            keys.update(record.keys())

        try:
            fingerprints.append(
                fingerprint(record)
            )
        except Exception:
            pass

    counts = Counter(fingerprints)

    duplicates = sum(
        n - 1
        for n in counts.values()
        if n > 1
    )

    return {
        "total_records": len(records),
        "unique_records": len(counts),
        "duplicate_records": duplicates,
        "empty_records": empty,
        "malformed_records": malformed,
        "top_keys": dict(keys.most_common(20)),
    }


def process_json(path):

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"error": str(e)}

    if isinstance(data, list):
        result = analyze_records(data)
        result["container_type"] = "list"
        return result

    if isinstance(data, dict):

        if isinstance(data.get("behaviors"), list):
            result = analyze_records(
                data["behaviors"]
            )
            result["container_type"] = "dict.behaviors"
            return result

        return {
            "container_type": "dict",
            "dictionary_keys": list(data.keys())[:20],
        }

    return {
        "container_type": type(data).__name__
    }


def process_jsonl(path):

    records = []
    malformed_lines = 0

    with open(path, encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            try:
                records.append(
                    json.loads(line)
                )
            except json.JSONDecodeError:
                malformed_lines += 1

    result = analyze_records(records)

    result["container_type"] = "jsonl"
    result["malformed_jsonl_lines"] = malformed_lines

    return result


def main():

    report = []

    grand = {
        "total_records": 0,
        "duplicate_records": 0,
        "empty_records": 0,
        "malformed_records": 0,
    }

    for dataset_name, root in ROOTS:

        print()
        print("=" * 80)
        print(dataset_name)
        print("=" * 80)

        if not root.exists():
            print("WARNING: directory not found")
            continue

        files = sorted(
            list(root.rglob("*.json")) +
            list(root.rglob("*.jsonl"))
        )

        dataset_total = 0
        dataset_duplicates = 0
        dataset_empty = 0
        dataset_malformed = 0

        for path in files:

            relative = str(
                path.relative_to(root)
            )

            if path.suffix == ".jsonl":
                result = process_jsonl(path)
            else:
                result = process_json(path)

            report.append({
                "dataset": dataset_name,
                "file": relative,
                **result,
            })

            total = result.get(
                "total_records", 0
            )

            duplicates = result.get(
                "duplicate_records", 0
            )

            empty = result.get(
                "empty_records", 0
            )

            malformed = result.get(
                "malformed_records", 0
            )

            dataset_total += total
            dataset_duplicates += duplicates
            dataset_empty += empty
            dataset_malformed += malformed

            print(
                f"{relative}: "
                f"records={total:,}, "
                f"duplicates={duplicates:,}, "
                f"empty={empty:,}, "
                f"malformed={malformed:,}"
            )

        print()
        print("SUMMARY")
        print(f"Records:     {dataset_total:,}")
        print(f"Duplicates:  {dataset_duplicates:,}")
        print(f"Empty:       {dataset_empty:,}")
        print(f"Malformed:   {dataset_malformed:,}")

        grand["total_records"] += dataset_total
        grand["duplicate_records"] += dataset_duplicates
        grand["empty_records"] += dataset_empty
        grand["malformed_records"] += dataset_malformed

    output = Path(
        "dataset/manifests/dataset_quality_report.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final = {
        "summary": grand,
        "files": report,
    }

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 80)
    print(
        f"Quality report written to: {output}"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
