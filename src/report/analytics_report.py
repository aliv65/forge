"""Detailed analytics report for Forge pipelines."""

from analytics.pipeline_metrics import (
    PipelineAnalytics,
    PipelineMetrics,
)


class AnalyticsReport:
    """Renders the final human-readable Forge analytics report."""

    def __init__(
        self,
        metrics: PipelineMetrics,
        analytics: PipelineAnalytics,
        provider_name: str,
        status: str
    ) -> None:
        self.metrics = metrics
        self.analytics = analytics
        self.provider_name = provider_name
        self.status = status

    def render(self) -> str:
        """Returns the complete analytics report."""

        lines = [
            "=" * 40,
            "Forge Analytics",
            "=" * 40,
            "",
            "Pipeline Summary",
            (
                "Pipeline duration: "
                f"{self.metrics.total_duration_ms / 1000:.3f} sec"
            ),
            f"Stages: {self.metrics.agents_count}",
            "",
            "Performance",
            (
                "Average agent duration: "
                f"{self.metrics.average_agent_duration_ms:.2f} ms"
            ),
            (
                "Fastest agent: "
                f"{self.analytics.fastest_agent or 'n/a'}"
            ),
            (
                "Slowest agent: "
                f"{self.analytics.slowest_agent or 'n/a'}"
            ),
            "",
            "Agent Statistics",
        ]

        for metric in self.metrics.agent_metrics:
            lines.append(
                f"{metric.agent_name}: "
                f"{metric.duration_ms / 1000:.3f} sec"
            )

        lines.extend([
            "",
            "LLM Usage",
            (
                "Prompt tokens: "
                f"{self.analytics.total_prompt_tokens}"
            ),
            (
                "Completion tokens: "
                f"{self.analytics.total_completion_tokens}"
            ),
            f"Total tokens: {self.analytics.total_tokens}",
            "",
            "Cost",
            f"Model: {self.provider_name}",
            (
                "Estimated cost: "
                f"${self.analytics.total_estimated_cost:.6f}"
            ),
            "",
            "Artifacts",
            f"Created artifacts: {self.analytics.artifacts_count}",
            "",
            "Errors",
            f"Errors: {self.analytics.errors_count}",
            "",
            "Final Status",
            self.status,
            "=" * 40,
        ])

        return "\n".join(lines)
