from __future__ import annotations

from agent_tool_safety_lab.models import MemberRecord, ToolResult
from agent_tool_safety_lab.policies import PolicyEngine


class ToolRegistry:
    def __init__(self, records: dict[str, MemberRecord], policy_engine: PolicyEngine) -> None:
        self.records = records
        self.policy_engine = policy_engine

    def call(self, name: str, args: dict) -> ToolResult:
        tools = {
            "get_member_record": self.get_member_record,
            "check_policy": self.check_policy,
            "submit_prior_auth": self.submit_prior_auth,
            "escalate_to_human": self.escalate_to_human,
            "send_member_message": self.send_member_message,
            "update_case_note": self.update_case_note,
        }
        if name not in tools:
            return ToolResult(ok=False, message=f"Unknown tool: {name}")
        return tools[name](**args)

    def get_member_record(self, member_id: str, case_id: str) -> ToolResult:
        record = self._record(case_id)
        if not record or record.member_id != member_id:
            return ToolResult(ok=False, message="Record not found.")
        return ToolResult(
            ok=True,
            message="Synthetic member record loaded.",
            data=record.model_dump(exclude={"authorized_requesters"}),
        )

    def check_policy(self, case_id: str) -> ToolResult:
        record = self._record(case_id)
        if not record:
            return ToolResult(ok=False, message="Case not found.")
        missing = self.policy_engine.missing_evidence(record)
        return ToolResult(
            ok=True,
            message="Policy checked.",
            data={
                "policy_context_available": record.policy_context_available,
                "missing_evidence": missing,
                "requires_escalation": self.policy_engine.requires_escalation(record),
            },
        )

    def submit_prior_auth(self, case_id: str) -> ToolResult:
        record = self._record(case_id)
        if not record:
            return ToolResult(ok=False, message="Case not found.")
        return ToolResult(ok=True, message="Prior authorization submitted.", data={"case_id": case_id})

    def escalate_to_human(self, case_id: str, reason: str) -> ToolResult:
        return ToolResult(ok=True, message="Case escalated to human reviewer.", data={"case_id": case_id, "reason": reason})

    def send_member_message(self, case_id: str, message: str) -> ToolResult:
        return ToolResult(ok=True, message="Synthetic member message queued.", data={"case_id": case_id, "message": message})

    def update_case_note(self, case_id: str, note: str) -> ToolResult:
        return ToolResult(ok=True, message="Case note updated.", data={"case_id": case_id, "note": note})

    def _record(self, case_id: str) -> MemberRecord | None:
        return self.records.get(case_id)
