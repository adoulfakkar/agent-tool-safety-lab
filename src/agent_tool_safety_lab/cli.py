from __future__ import annotations

import argparse
import os

from rich.console import Console
from rich.table import Table

from agent_tool_safety_lab.agents.base import Agent
from agent_tool_safety_lab.agents.llm_agent import ProviderToolAgent
from agent_tool_safety_lab.agents.mock_agent import DeterministicMockAgent
from agent_tool_safety_lab.config import load_settings
from agent_tool_safety_lab.environment import load_records, load_scenarios
from agent_tool_safety_lab.evaluator import Evaluator
from agent_tool_safety_lab.policies import PolicyEngine
from agent_tool_safety_lab.reports.report_writer import write_json_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate tool-using agents under safety policies.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run an agent safety evaluation.")
    run_parser.add_argument("--scenarios", required=True, help="Path to scenarios YAML.")
    run_parser.add_argument("--records", required=True, help="Path to synthetic records YAML.")
    run_parser.add_argument("--out", required=True, help="Path for JSON evaluation report.")
    run_parser.add_argument("--agent", choices=["mock", "llm"], help="Agent implementation to evaluate.")
    run_parser.add_argument(
        "--llm-provider",
        choices=["ollama", "huggingface"],
        help="Optional provider override for --agent llm.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "run":
        run(
            args.scenarios,
            args.records,
            args.out,
            args.agent,
            args.llm_provider,
        )


def run(
    scenarios_path: str,
    records_path: str,
    out_path: str,
    agent_name: str | None = None,
    llm_provider: str | None = None,
) -> None:
    if llm_provider:
        os.environ["ATSL_LLM_PROVIDER"] = llm_provider
    settings = load_settings()
    policy_engine = PolicyEngine()
    scenarios = load_scenarios(scenarios_path)
    records = load_records(records_path)
    selected_agent = agent_name or ("llm" if settings.runtime_mode == "llm" else "mock")
    agent = _build_agent(selected_agent, settings, policy_engine)
    report = Evaluator(agent, policy_engine).run(scenarios, records)
    output_path = write_json_report(report, out_path)
    _print_summary(report, str(output_path))


def _build_agent(agent_name: str, settings: Settings, policy_engine: PolicyEngine) -> Agent:
    if agent_name == "llm":
        return ProviderToolAgent(settings)
    return DeterministicMockAgent(policy_engine)


def _print_summary(report, output_path: str) -> None:
    console = Console()
    table = Table(title="Agent Tool Safety Evaluation")
    table.add_column("Scenario")
    table.add_column("Decision")
    table.add_column("Score", justify="right")
    table.add_column("Pass")
    table.add_column("Violations")

    for result in report.results:
        violations = ", ".join(v.policy_id for v in result.violated_policies) or "-"
        table.add_row(
            result.scenario_id,
            result.final_decision.value,
            str(result.score),
            "yes" if result.passed else "no",
            violations,
        )

    console.print(table)
    console.print(f"Passed {report.pass_count}/{len(report.results)} scenarios. Average score: {report.average_score:.1f}")
    console.print(f"JSON report written to {output_path}")


if __name__ == "__main__":
    main()
