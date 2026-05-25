from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Decision(str, Enum):
    PROCEED = "proceed"
    ESCALATE = "escalate"
    REFUSE = "refuse"


class ActionType(str, Enum):
    TOOL_CALL = "tool_call"
    DECISION = "decision"


class ToolCall(BaseModel):
    name: str
    args: dict[str, Any] = Field(default_factory=dict)


class AgentAction(BaseModel):
    action_type: ActionType
    tool_call: ToolCall | None = None
    decision: Decision | None = None
    reason: str


class MemberRecord(BaseModel):
    member_id: str
    case_id: str
    authorized_requesters: list[str]
    diagnosis_category: str
    requested_service: str
    required_evidence: list[str]
    submitted_evidence: list[str]
    policy_context_available: bool = True
    confidence: float = 0.9


class Scenario(BaseModel):
    id: str
    name: str
    requester_id: str
    member_id: str
    case_id: str
    request: str
    allowed_tools: list[str]
    expected_decision: Decision
    expected_behavior: str
    tags: list[str] = Field(default_factory=list)


class AuditEvent(BaseModel):
    step: int
    actor: str
    event_type: str
    detail: str
    tool_name: str | None = None
    allowed: bool = True
    policy_ids: list[str] = Field(default_factory=list)


class ToolResult(BaseModel):
    ok: bool
    message: str
    data: dict[str, Any] = Field(default_factory=dict)


class PolicyViolation(BaseModel):
    policy_id: str
    message: str


class EvaluationResult(BaseModel):
    scenario_id: str
    name: str
    passed: bool
    score: int
    dimensions: dict[str, int]
    violated_policies: list[PolicyViolation]
    expected_behavior: str
    actual_behavior: str
    final_decision: Decision
    trace: list[AuditEvent]
    reason: str


class EvaluationReport(BaseModel):
    results: list[EvaluationResult]

    @property
    def pass_count(self) -> int:
        return sum(1 for result in self.results if result.passed)

    @property
    def average_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(result.score for result in self.results) / len(self.results)
