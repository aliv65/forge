"""
Forge MVP entry point.

Запускает процесс обработки инженерной задачи через Orchestrator.
"""

from orchestrator.engine import Orchestrator
from orchestrator.context import ExecutionContext

from models.task import Task


def create_demo_task() -> Task:
    """
    Создает демонстрационную задачу для проверки pipeline.
    """

    return Task(
        id="TASK-001",
        title="Добавить поддержку нового отчета",
        description=(
            "Создать новый тип отчета в системе "
            "с возможностью формирования итоговых данных."
        ),
        requirements=[
            "Пользователь может создать отчет",
            "Отчет содержит необходимые данные",
            "Результат доступен после выполнения операции"
        ],
        constraints=[
            "Не изменять существующую архитектуру",
            "Соблюдать правила Constitution"
        ],
        acceptance_criteria=[
            "Отчет успешно создается",
            "Данные отчета корректно отображаются"
        ],
        open_questions=[]
    )


def main() -> None:
    """
    Основной сценарий запуска Forge.
    """

    task = create_demo_task()

    context = ExecutionContext(
        task=task
    )

    orchestrator = Orchestrator()

    result = orchestrator.run(context)

    print("Forge execution completed")
    print("------------------------")
    print(result)


if __name__ == "__main__":
    main()
