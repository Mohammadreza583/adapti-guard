from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class StandardRecord:
    id: str
    dataset: str
    split: str

    text: Optional[str] = None
    instruction: Optional[str] = None
    context: Optional[str] = None
    response: Optional[str] = None

    attack_family: Optional[str] = None
    attack_type: Optional[str] = None

    agent_task: Optional[str] = None
    tool_use: bool = False
    tool_name: Optional[str] = None

    injection_location: Optional[str] = None

    label: Optional[str] = None
    severity: Optional[str] = None

    source_file: Optional[str] = None
    source_index: Optional[int] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False
        )
