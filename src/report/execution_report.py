"""Technical execution report for Forge pipelines."""

from analytics.pipeline_metrics import PipelineMetrics


class ExecutionReport:
    """Renders concise technical execution metrics."""

    def __init__(
        self,
        metrics: PipelineMetrics
    ) -> None:
        self.metrics = metrics

    def render(self) -> str:
        """Returns a technical execution report."""

        return "\n".join([
            "Forge Execution Report",
            "=" * 40,
            (
                "Pipeline duration: "
                f"{self.metrics.total_duration_ms:.2f} ms"
            ),
            f"Agents: {self.metrics.agents_count}",
            (
                "Succeeded stages: "
                f"{self.metrics.succeeded_agents}"
            ),
            f"Errors: {self.metrics.failed_agents}",
            (
                "Average agent duration: "
                f"{self.metrics.average_agent_duration_ms:.2f} ms"
            ),
        ])
