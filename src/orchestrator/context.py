"""
Execution context.

Содержит состояние текущего запуска Forge pipeline.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from models.task import Task


@dataclass
class ExecutionContext:
    """
    Контекст выполнения инженерной задачи.

    Используется Orchestrator для передачи
    данных между этапами pipeline.
    """

    task: Task

    architecture_memory: str = ""

    previous_decisions: list[str] = field(
        default_factory=list
    )

    project_metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    results: Dict[str, Any] = field(
        default_factory=dict
    )

    current_stage: Optional[str] = None

    errors: list[str] = field(
        default_factory=list
    )

    def add_result(
        self,
        stage: str,
        result: Any
    ) -> None:
        """
        Сохраняет результат выполнения этапа.
        """

        self.results[stage] = result

    def get_result(
        self,
        stage: str
    ) -> Any:
        """
        Получает результат предыдущего этапа.
        """

        return self.results.get(stage)

    def add_error(
        self,
        error: str
    ) -> None:
        """
        Добавляет ошибку выполнения.
        """

        self.errors.append(error)

    def has_errors(self) -> bool:
        """
        Проверяет наличие ошибок.
        """

        return len(self.errors) > 0

    def update_stage(
        self,
        stage: str
    ) -> None:
        """
        Обновляет текущий этап pipeline.
        """

        self.current_stage = stage
