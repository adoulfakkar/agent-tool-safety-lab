from pathlib import Path

from agent_tool_safety_lab.cli import run


ROOT = Path(__file__).resolve().parents[1]

run(
    str(ROOT / "src/agent_tool_safety_lab/datasets/scenarios.yaml"),
    str(ROOT / "src/agent_tool_safety_lab/datasets/synthetic_records.yaml"),
    str(ROOT / "outputs/eval_report.json"),
)
