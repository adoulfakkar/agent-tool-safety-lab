from __future__ import annotations

import json
from pathlib import Path

from agent_tool_safety_lab.models import EvaluationReport


def write_json_report(report: EvaluationReport, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.model_dump(mode="json"), indent=2))
    return path
