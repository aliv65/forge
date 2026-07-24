"""
Forge.

Точка входа в приложение.
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


def create_demo_task() -> Task:
    """
    Создает демонстрационную задачу.
    """

    return Task(
        id="TASK-001",
        title="Добавить экспорт отчета в PDF",
        description=(
            "Пользователь должен иметь возможность "
            "экспортировать сформированный отчет в PDF."
        ),
        requirements=[
            "Добавить кнопку экспорта",
            "Сгенерировать PDF",
            "Вернуть пользователю готовый файл"
        ],
        constraints=[
            "Не изменять публичный API",
            "Использовать существующую архитектуру"
        ],
        acceptance_criteria=[
            "PDF успешно создается",
            "Файл доступен пользователю",
            "Ошибки корректно обрабатываются"
        ],
        open_questions=[]
    )


def create_pipeline() -> Pipeline:
    """
    Создает стандартный pipeline Forge.
    """

    provider = MockProvider()
    logger = ForgeLogger()

    agents = [
        ProductAgent(provider, logger),
        ArchitectAgent(provider, logger),
        CodingAgent(provider, logger),
        ReviewAgent(provider, logger),
        TestingAgent(provider, logger),
        ReleaseAgent(provider, logger),
    ]

    return Pipeline(agents)


def print_header() -> None:
    """
    Выводит заголовок приложения.
    """

    print("=" * 60)
    print("Forge")
    print("AI-First Engineering Orchestrator")
    print("=" * 60)
    print()


def print_pipeline(pipeline: Pipeline) -> None:
    """
    Показывает последовательность агентов.
    """

    print("Pipeline:")

    for index, agent in enumerate(
        pipeline.get_agents(),
        start=1
    ):
        print(f"{index}. {agent.name}")

    print()


def print_summary(result: dict) -> None:
    """
    Выводит итог выполнения.
    """

    print("=" * 60)

    if result["status"] == "completed":

        release = result["release"]

        print("Pipeline completed successfully")
        print()

        print(f"Release ID : {release['id']}")
        print(f"Status     : {release['status']}")
        print(f"Task ID    : {release['task_id']}")

    else:

        print("Pipeline failed")
        print()

        print(f"Stage : {result['stage']}")
        print(f"Error : {result['error']}")

    print("=" * 60)


def main() -> None:

    print_header()

    task = create_demo_task()

    context = ExecutionContext(task)

    pipeline = create_pipeline()

    print_pipeline(pipeline)

    orchestrator = Orchestrator(
        pipeline=pipeline
    )

    result = orchestrator.run(
        context
    )

    print_summary(result)


if __name__ == "__main__":
    main()
