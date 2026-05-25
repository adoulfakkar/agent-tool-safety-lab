from __future__ import annotations

from pathlib import Path

import yaml

from agent_tool_safety_lab.models import MemberRecord, Scenario


def load_scenarios(path: str | Path) -> list[Scenario]:
    raw = yaml.safe_load(Path(path).read_text()) or []
    return [Scenario.model_validate(item) for item in raw]


def load_records(path: str | Path) -> dict[str, MemberRecord]:
    raw = yaml.safe_load(Path(path).read_text()) or []
    records = [MemberRecord.model_validate(item) for item in raw]
    return {record.case_id: record for record in records}
