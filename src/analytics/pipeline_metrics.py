"""Aggregated metrics and analytics for Forge pipelines."""

from dataclasses import dataclass, field
from datetime import datetime

from analytics.agent_metrics import AgentMetrics


@dataclass(slots=True)
class PipelineMetrics:
    """Stores aggregate execution metrics for one pipeline run."""

    pipeline_started: datetime

    pipeline_finished: datetime

    total_duration_ms: float

    agents_count: int

    succeeded_agents: int

    failed_agents: int

    average_agent_duration_ms: float

    agent_metrics: list[AgentMetrics] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        """Returns serializable pipeline metrics."""

        return {
            "pipeline_started": self.pipeline_started.isoformat(),
            "pipeline_finished": self.pipeline_finished.isoformat(),
            "total_duration_ms": self.total_duration_ms,
            "agents_count": self.agents_count,
            "succeeded_agents": self.succeeded_agents,
            "failed_agents": self.failed_agents,
            "average_agent_duration_ms": (
                self.average_agent_duration_ms
            ),
            "agent_metrics": [
                metric.to_dict()
                for metric in self.agent_metrics
            ],
        }


@dataclass(slots=True)
class PipelineAnalytics:
    """Provides higher-level technical analytics for a pipeline run."""

    total_tokens: int

    total_prompt_tokens: int

    total_completion_tokens: int

    total_estimated_cost: float

    errors_count: int

    completed_stages: int

    artifacts_count: int

    fastest_agent: str | None

    slowest_agent: str | None

    success_rate_percent: float

    @classmethod
    def from_metrics(
        cls,
        metrics: PipelineMetrics,
        artifacts_count: int,
        errors_count: int
    ) -> "PipelineAnalytics":
        """Builds technical analytics from pipeline metrics."""

        agent_metrics = metrics.agent_metrics

        fastest_agent = None
        slowest_agent = None

        if agent_metrics:
            fastest_agent = min(
                agent_metrics,
                key=lambda metric: metric.duration_ms
            ).agent_name
            slowest_agent = max(
                agent_metrics,
                key=lambda metric: metric.duration_ms
            ).agent_name

        total_prompt_tokens = sum(
            metric.prompt_tokens
            for metric in agent_metrics
        )
        total_completion_tokens = sum(
            metric.completion_tokens
            for metric in agent_metrics
        )

        success_rate = 0.0

        if metrics.agents_count:
            success_rate = (
                metrics.succeeded_agents
                / metrics.agents_count
                * 100
            )

        return cls(
            total_tokens=sum(
                metric.total_tokens
                for metric in agent_metrics
            ),
            total_prompt_tokens=total_prompt_tokens,
            total_completion_tokens=total_completion_tokens,
            total_estimated_cost=round(
                sum(
                    metric.estimated_cost
                    for metric in agent_metrics
                ),
                6
            ),
            errors_count=errors_count,
            completed_stages=metrics.succeeded_agents,
            artifacts_count=artifacts_count,
            fastest_agent=fastest_agent,
            slowest_agent=slowest_agent,
            success_rate_percent=round(success_rate, 2),
        )

    def to_dict(self) -> dict:
        """Returns serializable technical analytics."""

        return {
            "total_tokens": self.total_tokens,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": (
                self.total_completion_tokens
            ),
            "total_estimated_cost": self.total_estimated_cost,
            "errors_count": self.errors_count,
            "completed_stages": self.completed_stages,
            "artifacts_count": self.artifacts_count,
            "fastest_agent": self.fastest_agent,
            "slowest_agent": self.slowest_agent,
            "success_rate_percent": self.success_rate_percent,
        }
