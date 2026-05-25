from agent_tool_safety_lab.environment import load_records
from agent_tool_safety_lab.policies import PolicyEngine
from agent_tool_safety_lab.tools import ToolRegistry


def test_check_policy_reports_missing_evidence():
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")
    registry = ToolRegistry(records, PolicyEngine())

    result = registry.check_policy("case_missing_pt")

    assert result.ok
    assert result.data["missing_evidence"] == ["conservative_therapy_record"]


def test_get_member_record_does_not_return_authorized_requesters():
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")
    registry = ToolRegistry(records, PolicyEngine())

    result = registry.get_member_record("mem_1001", "case_safe_knee_mri")

    assert result.ok
    assert "authorized_requesters" not in result.data
