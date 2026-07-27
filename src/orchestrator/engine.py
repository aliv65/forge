"""
Forge Orchestrator Engine.

Управляет жизненным циклом выполнения pipeline.
"""

from __future__ import annotations

from datetime import UTC, datetime

from orchestrator.context import ExecutionContext
from orchestrator.pipeline import Pipeline

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
        logger: ForgeLogger | None = None
    ) -> None:

        self.pipeline = pipeline

        self.logger = (
            logger
            or ForgeLogger()
        )

    def run(
        self,
        context: ExecutionContext
    ) -> dict:
        """
        Выполняет полный pipeline.
        """

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

                if not result.success:

                    context.add_error(
                        result.error
                    )

                    self.logger.pipeline_failed(
                        agent.name,
                        result.error or "Unknown error"
                    )

                    return {
                        "status": "failed",
                        "stage": agent.name,
                        "error": result.error,
                        "context": (
                            context.to_dict()
                        )
                    }

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

            return {
                "status": "completed",
                "release": context.get_result(
                    "release-agent"
                ),
                "context": (
                    context.to_dict()
                )
            }

        except Exception as error:

            context.add_error(
                str(error)
            )

            self.logger.pipeline_failed(
                context.stage,
                str(error)
            )

            return {
                "status": "failed",
                "stage": context.stage,
                "error": str(error),
                "context": (
                    context.to_dict()
                )
            }
