from __future__ import annotations

from abc import ABC, abstractmethod

from agent_tool_safety_lab.models import AgentAction, MemberRecord, Scenario


class Agent(ABC):
    @abstractmethod
    def plan(self, scenario: Scenario, record: MemberRecord) -> list[AgentAction]:
        """Return the actions the agent wants to take for a scenario."""
