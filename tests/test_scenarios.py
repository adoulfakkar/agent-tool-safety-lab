from agent_tool_safety_lab.environment import load_records, load_scenarios


def test_scenarios_have_matching_records():
    scenarios = load_scenarios("src/agent_tool_safety_lab/datasets/scenarios.yaml")
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")

    assert len(scenarios) >= 18
    for scenario in scenarios:
        assert scenario.case_id in records
        assert scenario.member_id == records[scenario.case_id].member_id
        assert scenario.expected_behavior


def test_compound_scenarios_are_present():
    scenarios = load_scenarios("src/agent_tool_safety_lab/datasets/scenarios.yaml")

    compound = [scenario for scenario in scenarios if "compound_risk" in scenario.tags]

    assert len(compound) >= 8


def test_dataset_is_synthetic_by_identifier_shape():
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")

    assert all(record.member_id.startswith("mem_") for record in records.values())
    assert all(record.case_id.startswith("case_") for record in records.values())
