from __future__ import annotations

from agent_tool_safety_lab.agents.base import Agent
from agent_tool_safety_lab.models import ActionType, AgentAction, Decision, MemberRecord, Scenario, ToolCall
from agent_tool_safety_lab.policies import PolicyEngine


class DeterministicMockAgent(Agent):
    """Small rule-based agent used to make the first harness reproducible."""

    def __init__(self, policy_engine: PolicyEngine | None = None) -> None:
        self.policy_engine = policy_engine or PolicyEngine()

    def plan(self, scenario: Scenario, record: MemberRecord) -> list[AgentAction]:
        if not self.policy_engine.is_authorized(scenario, record):
            return [
                self._tool("update_case_note", {"case_id": scenario.case_id, "note": "Unauthorized requester. No member details disclosed."}, "Document unauthorized request."),
                self._decision(Decision.REFUSE, "Requester is not authorized to access sensitive member information."),
            ]

        if self.policy_engine.has_policy_conflict(scenario.request):
            return [
                self._tool("update_case_note", {"case_id": scenario.case_id, "note": "Potential policy-bypass instruction detected."}, "Document adversarial instruction."),
                self._decision(Decision.REFUSE, "User instruction conflicts with system policy and cannot be followed."),
            ]

        missing = self.policy_engine.missing_evidence(record)
        if self.policy_engine.requires_escalation(record) and missing:
            return [
                self._tool("check_policy", {"case_id": scenario.case_id}, "Check policy context and evidence completeness."),
                self._tool("update_case_note", {"case_id": scenario.case_id, "note": f"Escalation required. Missing evidence: {', '.join(missing)}; context or confidence is insufficient."}, "Document compound escalation rationale."),
                self._tool("escalate_to_human", {"case_id": scenario.case_id, "reason": f"Missing evidence plus incomplete context or low confidence: {', '.join(missing)}."}, "Escalate compound-risk case."),
                self._decision(Decision.ESCALATE, f"Missing evidence plus incomplete context or low confidence: {', '.join(missing)}."),
            ]

        if self.policy_engine.requires_escalation(record):
            return [
                self._tool("check_policy", {"case_id": scenario.case_id}, "Check whether policy context is complete."),
                self._tool("escalate_to_human", {"case_id": scenario.case_id, "reason": "Policy context incomplete or confidence below threshold."}, "Escalate uncertain case."),
                self._decision(Decision.ESCALATE, "Policy context is incomplete or confidence is low."),
            ]

        if missing:
            return [
                self._tool("get_member_record", {"member_id": scenario.member_id, "case_id": scenario.case_id}, "Load synthetic record for evidence review."),
                self._tool("check_policy", {"case_id": scenario.case_id}, "Compare submitted evidence to policy requirements."),
                self._tool("update_case_note", {"case_id": scenario.case_id, "note": f"Missing required evidence: {', '.join(missing)}."}, "Document missing evidence."),
                self._tool("escalate_to_human", {"case_id": scenario.case_id, "reason": f"Missing required evidence: {', '.join(missing)}."}, "Escalate missing evidence for human review."),
                self._decision(Decision.ESCALATE, f"Missing required evidence: {', '.join(missing)}."),
            ]

        return [
            self._tool("get_member_record", {"member_id": scenario.member_id, "case_id": scenario.case_id}, "Load synthetic record for review."),
            self._tool("check_policy", {"case_id": scenario.case_id}, "Confirm evidence satisfies policy."),
            self._tool("submit_prior_auth", {"case_id": scenario.case_id}, "Submit only after policy check and evidence review."),
            self._tool("update_case_note", {"case_id": scenario.case_id, "note": "Prior authorization submitted after policy and evidence checks."}, "Record final case note."),
            self._decision(Decision.PROCEED, "Required evidence is present and policy context is available."),
        ]

    def _tool(self, name: str, args: dict, reason: str) -> AgentAction:
        return AgentAction(action_type=ActionType.TOOL_CALL, tool_call=ToolCall(name=name, args=args), reason=reason)

    def _decision(self, decision: Decision, reason: str) -> AgentAction:
        return AgentAction(action_type=ActionType.DECISION, decision=decision, reason=reason)
