from agent_tool_safety_lab.agents.mock_agent import DeterministicMockAgent
from agent_tool_safety_lab.environment import load_records, load_scenarios
from agent_tool_safety_lab.evaluator import Evaluator
from agent_tool_safety_lab.policies import PolicyEngine


def test_evaluator_runs_all_scenarios():
    policy_engine = PolicyEngine()
    scenarios = load_scenarios("src/agent_tool_safety_lab/datasets/scenarios.yaml")
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")

    report = Evaluator(DeterministicMockAgent(policy_engine), policy_engine).run(scenarios, records)

    assert len(report.results) == 18
    assert report.pass_count == 18
    assert report.average_score == 100


def test_report_contains_audit_trace():
    policy_engine = PolicyEngine()
    scenarios = load_scenarios("src/agent_tool_safety_lab/datasets/scenarios.yaml")
    records = load_records("src/agent_tool_safety_lab/datasets/synthetic_records.yaml")

    result = Evaluator(DeterministicMockAgent(policy_engine), policy_engine).evaluate_one(scenarios[0], records)

    assert result.trace
    assert result.trace[-1].event_type == "decision"
    assert result.reason
