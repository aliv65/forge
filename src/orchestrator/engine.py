"""
Forge Orchestrator Engine.

Главный исполнительный механизм pipeline.
"""

from orchestrator.context import ExecutionContext
from orchestrator.pipeline import Pipeline

from agents.product import ProductAgent
from agents.architect import ArchitectAgent
from agents.coder import CodingAgent
from agents.reviewer import ReviewAgent
from agents.tester import TestingAgent
from agents.release import ReleaseAgent


class Orchestrator:
    """
    Управляет жизненным циклом выполнения задачи.

    Ответственность:
    - создать pipeline;
    - запускать агентов;
    - контролировать ошибки;
    - возвращать итоговый результат.

    Не отвечает за:
    - бизнес-логику агентов;
    - генерацию решений;
    - хранение данных.
    """

    def __init__(
        self,
        pipeline: Pipeline | None = None
    ):
        self.pipeline = (
            pipeline
            if pipeline is not None
            else self.create_default_pipeline()
        )

    def create_default_pipeline(self) -> Pipeline:
        """
        Создает стандартный Forge pipeline.
        """

        return Pipeline(
            agents=[
                ProductAgent(),
                ArchitectAgent(),
                CodingAgent(),
                ReviewAgent(),
                TestingAgent(),
                ReleaseAgent()
            ]
        )

    def run(
        self,
        context: ExecutionContext
    ):
        """
        Запускает выполнение pipeline.
        """

        for agent in self.pipeline.get_agents():

            context.update_stage(
                agent.name
            )

            result = agent.execute(
                context
            )

            if not result.is_successful():

                context.add_error(
                    f"{agent.name}: {result.error}"
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
