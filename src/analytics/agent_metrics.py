"""Metrics for one Forge agent execution."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AgentMetrics:
    """Stores performance and LLM usage for an agent."""

    agent_name: str

    started_at: datetime

    finished_at: datetime

    duration_ms: float

    execution_time_ms: float

    success: bool

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    estimated_cost: float = 0.0

    def to_dict(self) -> dict:
        """Returns serializable agent metrics."""

        return {
            "agent_name": self.agent_name,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat(),
            "duration_ms": self.duration_ms,
            "execution_time_ms": self.execution_time_ms,
            "success": self.success,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost": self.estimated_cost,
        }
