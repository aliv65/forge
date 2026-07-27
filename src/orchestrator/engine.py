"""
Forge Orchestrator Engine.

Управляет жизненным циклом выполнения pipeline.
"""

from __future__ import annotations

from datetime import UTC, datetime

from analytics.collector import MetricsCollector
from analytics.cost_calculator import CostCalculator
from analytics.pipeline_metrics import PipelineAnalytics

from orchestrator.context import ExecutionContext
from orchestrator.pipeline import Pipeline

from report.analytics_report import AnalyticsReport
from report.execution_report import ExecutionReport

from utils.logger import ForgeLogger


class Orchestrator:
    """
    Главный исполнитель Forge.

    Ответственность:
    - запускать pipeline;
    - контролировать порядок выполнения;
    - обрабатывать ошибки верхнего уровня;
    - фиксировать состояние выполнения.

    Не отвечает за:
    - логику агентов;
    - создание артефактов;
    - работу AI Provider.
    """

    def __init__(
        self,
        pipeline: Pipeline,
        logger: ForgeLogger | None = None,
        metrics_collector: MetricsCollector | None = None,
        cost_calculator: CostCalculator | None = None
    ) -> None:

        self.pipeline = pipeline

        self.logger = (
            logger
            or ForgeLogger()
        )

        self.metrics_collector = (
            metrics_collector
            or MetricsCollector()
        )

        self.cost_calculator = (
            cost_calculator
            or CostCalculator()
        )

    def run(
        self,
        context: ExecutionContext
    ) -> dict:
        """
        Выполняет полный pipeline.
        """

        self.metrics_collector.start_pipeline()
        active_agent = None

        self.logger.log(
            "pipeline_started",
            "Forge pipeline started",
            {
                "task_id": context.task.id,
                "started_at": (
                    datetime.now(UTC)
                    .isoformat()
                )
            }
        )

        try:

            for agent in self.pipeline:

                active_agent = agent

                self.metrics_collector.start_agent(
                    agent.name
                )

                context.update_stage(
                    agent.name
                )

                self.logger.log(
                    "stage_started",
                    (
                        f"Stage {agent.name} started"
                    ),
                    {
                        "task_id": context.task.id
                    }
                )

                result = agent.run(
                    context
                )

                usage = agent.last_token_usage

                self.metrics_collector.finish_agent(
                    agent.name,
                    success=result.success,
                    usage=usage,
                    estimated_cost=(
                        self.cost_calculator.calculate(
                            usage
                        )
                    )
                )

                active_agent = None

                if not result.success:

                    context.add_error(
                        result.error
                    )

                    self.logger.pipeline_failed(
                        agent.name,
                        result.error or "Unknown error"
                    )

                    return self._build_result(
                        context=context,
                        status="failed",
                        stage=agent.name,
                        error=result.error
                    )

                self.logger.log(
                    "stage_completed",
                    (
                        f"Stage {agent.name} completed"
                    ),
                    {
                        "task_id": context.task.id
                    }
                )

            context.mark_completed()

            for agent in self.pipeline:
                agent.commit(context)

            self.logger.log(
                "pipeline_completed",
                "Forge pipeline completed",
                {
                    "task_id": context.task.id
                }
            )

            return self._build_result(
                context=context,
                status="completed"
            )

        except Exception as error:

            if (
                active_agent is not None
                and self.metrics_collector.is_agent_active(
                    active_agent.name
                )
            ):
                usage = active_agent.last_token_usage

                self.metrics_collector.finish_agent(
                    active_agent.name,
                    success=False,
                    usage=usage,
                    estimated_cost=(
                        self.cost_calculator.calculate(
                            usage
                        )
                    )
                )

            context.add_error(
                str(error)
            )

            self.logger.pipeline_failed(
                context.stage,
                str(error)
            )

            return self._build_result(
                context=context,
                status="failed",
                stage=context.stage,
                error=str(error)
            )

    def _build_result(
        self,
        context: ExecutionContext,
        status: str,
        stage: str | None = None,
        error: str | None = None
    ) -> dict:
        """Builds the pipeline result and its analytics reports."""

        self.metrics_collector.finish_pipeline()

        metrics = self.metrics_collector.build_pipeline_metrics()
        analytics = PipelineAnalytics.from_metrics(
            metrics,
            artifacts_count=len(context.artifacts),
            errors_count=len(context.errors)
        )
        execution_report = ExecutionReport(metrics).render()
        analytics_report = AnalyticsReport(
            metrics=metrics,
            analytics=analytics,
            provider_name=self._provider_name(),
            status=status
        ).render()

        result = {
            "status": status,
            "context": context.to_dict(),
            "metrics": metrics.to_dict(),
            "analytics": analytics.to_dict(),
            "execution_report": execution_report,
            "analytics_report": analytics_report,
        }

        if status == "completed":
            result["release"] = context.get_result(
                "release-agent"
            )
        else:
            result["stage"] = stage
            result["error"] = error

        return result

    def _provider_name(self) -> str:
        """Returns the provider name used by the first pipeline agent."""

        agents = self.pipeline.get_agents()

        if not agents:
            return "Unknown"

        return agents[0].provider.name
