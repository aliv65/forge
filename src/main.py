"""
Forge.

Точка входа приложения.
"""

from agents.architect import ArchitectAgent
from agents.coder import CodingAgent
from agents.product import ProductAgent
from agents.release import ReleaseAgent
from agents.reviewer import ReviewAgent
from agents.tester import TestingAgent

from models.task import Task

from orchestrator.context import ExecutionContext
from orchestrator.engine import Orchestrator
from orchestrator.pipeline import Pipeline

from providers.mock import MockProvider

from utils.logger import ForgeLogger

from utils.config import config


def create_demo_task() -> Task:

    return Task(
        id="TASK-001",
        title="Добавить экспорт отчета в PDF",
        description=(
            "Пользователь должен иметь возможность "
            "экспортировать отчет в PDF."
        ),
        requirements=[
            "Создать экспорт PDF",
            "Обработать ошибки генерации"
        ],
        constraints=[
            "Не менять существующую архитектуру"
        ],
        acceptance_criteria=[
            "PDF успешно создается",
            "Ошибки корректно обрабатываются"
        ],
        open_questions=[]
    )


def create_pipeline(
    provider: MockProvider,
    logger: ForgeLogger
) -> Pipeline:

    if not isinstance(provider, MockProvider):
        raise ValueError(
            "Forge demo supports MockProvider only."
        )

    agents = [
        ProductAgent(
            provider,
            logger
        ),

        ArchitectAgent(
            provider,
            logger
        ),

        CodingAgent(
            provider,
            logger
        ),

        ReviewAgent(
            provider,
            logger
        ),

        TestingAgent(
            provider,
            logger
        ),

        ReleaseAgent(
            provider,
            logger
        )
    ]

    return Pipeline(
        agents
    )


def main():

    print("=" * 60)
    print("Forge")
    print("AI Engineering Orchestrator")
    print("=" * 60)

    provider = MockProvider()

    logger = ForgeLogger(
        config.logs_directory
    )

    task = create_demo_task()

    context = ExecutionContext(
        task
    )

    pipeline = create_pipeline(
        provider,
        logger
    )

    orchestrator = Orchestrator(
        pipeline=pipeline,
        logger=logger
    )

    result = orchestrator.run(
        context
    )

    print()

    if result["status"] == "completed":

        print(
            "Pipeline completed"
        )

        print(
            result["release"]
        )

    else:

        print(
            "Pipeline failed"
        )

        print(
            result["error"]
        )


if __name__ == "__main__":
    main()
