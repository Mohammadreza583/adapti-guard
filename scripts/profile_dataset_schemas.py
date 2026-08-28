import json
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


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def inspect_structure(obj):
    if isinstance(obj, list):
        return {
            "type": "list",
            "length": len(obj),
            "sample_keys": (
                list(obj[0].keys())
                if obj and isinstance(obj[0], dict)
                else []
            ),
        }

    if isinstance(obj, dict):
        return {
            "type": "dict",
            "keys": list(obj.keys())[:20],
        }

    return {
        "type": type(obj).__name__
    }


def inspect_jsonl(path):
    records = 0
    key_counter = Counter()

    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            records += 1

            try:
                obj = json.loads(line)

                if isinstance(obj, dict):
                    for key in obj.keys():
                        key_counter[key] += 1

            except Exception:
                pass

    return {
        "type": "jsonl",
        "records": records,
        "keys": dict(key_counter),
    }


def main():

    output = []

    for dataset_name, root in ROOTS:

        print("\n" + "=" * 90)
        print(dataset_name)
        print("=" * 90)

        if not root.exists():
            print("WARNING: dataset directory not found")
            continue

        files = sorted(
            list(root.rglob("*.json")) +
            list(root.rglob("*.jsonl"))
        )

        for path in files:

            rel = str(path.relative_to(root))

            if path.suffix == ".jsonl":

                info = inspect_jsonl(path)

            else:

                data = load_json(path)

                if data is None:
                    continue

                info = inspect_structure(data)

            item = {
                "dataset": dataset_name,
                "file": rel,
                **info,
            }

            output.append(item)

            print(f"\nFILE: {rel}")
            print(json.dumps(info, indent=2, ensure_ascii=False))

    output_path = Path(
        "dataset/manifests/dataset_schema_profile.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 90)
    print(f"Schema profile written to: {output_path}")
    print("=" * 90)


if __name__ == "__main__":
    main()
