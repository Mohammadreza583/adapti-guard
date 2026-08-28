import json
from pathlib import Path
from collections import Counter


ROOTS = {
    "BIPIA": Path("BIPIA"),
    "AgentHarm": Path("dataset/raw/AgentHarm"),
    "InjecAgent": Path("dataset/raw/InjecAgent"),
    "PIArena": Path("dataset/raw/PIArena"),
    "TensorTrust": Path("dataset/raw/TensorTrust"),
    "NotInject": Path("dataset/raw/NotInject"),
    "ASB": Path("dataset/raw/ASB"),
}


EXTENSIONS = {
    ".json",
    ".jsonl",
    ".csv",
    ".parquet",
    ".yaml",
    ".yml",
}


def count_jsonl(path):
    count = 0

    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1

    return count


def inspect_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return {
                "type": "list",
                "records": len(data),
            }

        if isinstance(data, dict):
            return {
                "type": "dict",
                "keys": list(data.keys())[:20],
            }

        return {
            "type": type(data).__name__
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def main():

    output = []

    for dataset, root in ROOTS.items():

        if not root.exists():
            continue

        files = [
            p for p in root.rglob("*")
            if p.is_file()
            and p.suffix.lower() in EXTENSIONS
        ]

        extension_counts = Counter(
            p.suffix.lower()
            for p in files
        )

        dataset_info = {
            "dataset": dataset,
            "root": str(root),
            "file_count": len(files),
            "extensions": dict(extension_counts),
            "files": [],
        }

        for path in sorted(files):

            info = {
                "path": str(path),
                "relative_path": str(path.relative_to(root)),
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
            }

            if path.suffix.lower() == ".jsonl":
                try:
                    info["records"] = count_jsonl(path)
                except Exception as e:
                    info["error"] = str(e)

            elif path.suffix.lower() == ".json":
                info.update(inspect_json(path))

            dataset_info["files"].append(info)

        output.append(dataset_info)

    output_path = Path(
        "dataset/manifests/dataset_inventory.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Inventory written to: {output_path}"
    )


if __name__ == "__main__":
    main()
