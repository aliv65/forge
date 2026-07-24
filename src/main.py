"""
Forge.

Точка входа в приложение.
"""

from models.task import Task
from orchestrator.context import ExecutionContext
from orchestrator.engine import Orchestrator


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
            "Скачать файл пользователю"
        ],
        constraints=[
            "Использовать существующую архитектуру",
            "Не нарушать API"
        ],
        acceptance_criteria=[
            "PDF успешно создается",
            "Файл скачивается",
            "Ошибки отображаются пользователю"
        ],
        open_questions=[]
    )


def print_header() -> None:
    """
    Печатает заголовок приложения.
    """

    print("=" * 60)
    print("Forge")
    print("AI-First Engineering Orchestrator")
    print("=" * 60)
    print()


def print_summary(result: dict) -> None:
    """
    Печатает итог выполнения.
    """

    print()
    print("=" * 60)

    if result["status"] == "completed":

        print("Pipeline completed successfully")

        release = result["release"]

        print(f"Release ID : {release['id']}")
        print(f"Status     : {release['status']}")
        print(f"Task       : {release['task_id']}")

    else:

        print("Pipeline failed")

        print(f"Stage : {result['stage']}")
        print(f"Error : {result['error']}")

    print("=" * 60)


def main() -> None:
    """
    Запускает демонстрационный pipeline.
    """

    print_header()

    task = create_demo_task()

    print(f"Task: {task.title}")
    print()

    context = ExecutionContext(task)

    orchestrator = Orchestrator()

    result = orchestrator.run(context)

    print()

    print("Pipeline:")

    for stage in context.results.keys():
        print(f"  ✓ {stage}")

    print_summary(result)


if __name__ == "__main__":
    main()
