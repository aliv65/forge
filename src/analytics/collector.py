"""Collection of execution metrics for Forge pipelines."""

from __future__ import annotations

from datetime import UTC, datetime
from time import perf_counter

from analytics.agent_metrics import AgentMetrics
from analytics.pipeline_metrics import PipelineMetrics
from analytics.token_usage import TokenUsage


class MetricsCollector:
    """Collects pipeline and agent execution metrics."""

    def __init__(self) -> None:
        self._pipeline_started_at: datetime | None = None
        self._pipeline_started_timer: float | None = None
        self._pipeline_finished_at: datetime | None = None
        self._active_agents: dict[str, tuple[datetime, float]] = {}
        self._agent_metrics: list[AgentMetrics] = []

    def start_pipeline(self) -> None:
        """Starts a new metrics collection session."""

        self._pipeline_started_at = datetime.now(UTC)
        self._pipeline_started_timer = perf_counter()
        self._pipeline_finished_at = None
        self._active_agents.clear()
        self._agent_metrics.clear()

    def finish_pipeline(self) -> None:
        """Records pipeline completion time."""

        self._require_pipeline_started()
        self._pipeline_finished_at = datetime.now(UTC)

    def start_agent(
        self,
        agent_name: str
    ) -> None:
        """Starts execution timing for one agent."""

        self._require_pipeline_started()

        if agent_name in self._active_agents:
            raise ValueError(
                f"Agent is already running: {agent_name}"
            )

        self._active_agents[agent_name] = (
            datetime.now(UTC),
            perf_counter()
        )

    def finish_agent(
        self,
        agent_name: str,
        success: bool,
        usage: TokenUsage | None = None,
        estimated_cost: float = 0.0
    ) -> AgentMetrics:
        """Completes and stores metrics for one agent."""

        started_at, started_timer = self._active_agents.pop(
            agent_name
        )
        finished_at = datetime.now(UTC)
        duration_ms = (
            perf_counter() - started_timer
        ) * 1000
        token_usage = usage or TokenUsage()

        metric = AgentMetrics(
            agent_name=agent_name,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
            execution_time_ms=duration_ms,
            success=success,
            prompt_tokens=token_usage.prompt_tokens,
            completion_tokens=token_usage.completion_tokens,
            total_tokens=token_usage.total_tokens,
            estimated_cost=estimated_cost,
        )
        self._agent_metrics.append(metric)

        return metric

    def is_agent_active(
        self,
        agent_name: str
    ) -> bool:
        """Returns whether an agent currently has active timing."""

        return agent_name in self._active_agents

    def build_pipeline_metrics(self) -> PipelineMetrics:
        """Builds aggregate metrics for the collected pipeline run."""

        self._require_pipeline_started()

        if self._pipeline_finished_at is None:
            self.finish_pipeline()

        total_duration_ms = (
            perf_counter() - self._pipeline_started_timer
        ) * 1000
        agents_count = len(self._agent_metrics)
        succeeded_agents = sum(
            metric.success
            for metric in self._agent_metrics
        )
        failed_agents = agents_count - succeeded_agents
        average_duration_ms = 0.0

        if agents_count:
            average_duration_ms = sum(
                metric.duration_ms
                for metric in self._agent_metrics
            ) / agents_count

        return PipelineMetrics(
            pipeline_started=self._pipeline_started_at,
            pipeline_finished=self._pipeline_finished_at,
            total_duration_ms=total_duration_ms,
            agents_count=agents_count,
            succeeded_agents=succeeded_agents,
            failed_agents=failed_agents,
            average_agent_duration_ms=average_duration_ms,
            agent_metrics=list(self._agent_metrics),
        )

    def _require_pipeline_started(self) -> None:
        """Ensures collection is initialized before recording metrics."""

        if (
            self._pipeline_started_at is None
            or self._pipeline_started_timer is None
        ):
            raise RuntimeError("Pipeline metrics were not started.")
