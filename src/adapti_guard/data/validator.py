from dataclasses import fields
from .schema import StandardRecord


REQUIRED_FIELDS = {
    "id",
    "dataset",
    "split",
}


def validate_record(record: StandardRecord):
    data = record.to_dict()

    errors = []

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            errors.append(f"missing required field: {field}")

    if record.split not in {
        "train",
        "validation",
        "test",
        "unseen",
        "adaptive",
    }:
        errors.append(
            f"invalid split: {record.split}"
        )

    if record.tool_use and not record.agent_task:
        errors.append(
            "tool_use=True but agent_task is missing"
        )

    return errors


def validate_records(records):
    results = []

    for record in records:
        errors = validate_record(record)

        if errors:
            results.append({
                "id": record.id,
                "errors": errors,
            })

    return results
