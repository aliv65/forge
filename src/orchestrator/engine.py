"""
Forge Orchestrator Engine.

Главный исполнительный механизм Forge.
"""

from orchestrator.context import ExecutionContext
from orchestrator.pipeline import Pipeline
from agents.base import AgentResult


class Orchestrator:
    """
    Управляет выполнением pipeline.

    Orchestrator не знает ничего о реализации
    отдельных агентов. Он работает только
    с их контрактом.
    """

    def __init__(
        self,
        pipeline: Pipeline
    ):
        self.pipeline = pipeline

    def run(
        self,
        context: ExecutionContext
    ) -> dict:
        """
        Запускает pipeline.
        """

        for agent in self.pipeline.get_agents():

            context.update_stage(
                agent.name
            )

            result: AgentResult = agent.run(
                context
            )

            if not result.success:

                context.add_error(
                    result.error
                )

                return {
                    "status": "failed",
                    "stage": agent.name,
                    "error": result.error,
                    "context": context
                }

        return {
            "status": "completed",
            "release": context.get_result(
                "release-agent"
            ),
            "context": context
        }
