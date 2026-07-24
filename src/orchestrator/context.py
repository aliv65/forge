"""
Execution Context.

Хранит состояние выполнения задачи в рамках
одного запуска Forge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from models.task import Task


@dataclass(slots=True)
class ExecutionContext:
    """
    Контекст выполнения pipeline.

    Ответственность:
    - хранить исходную задачу;
    - хранить артефакты агентов;
    - хранить состояние выполнения;
    - предоставлять доступ к результатам.

    Не отвечает за:
    - выполнение агентов;
    - логирование;
    - сохранение памяти.
    """

    task: Task

    stage: str = "created"

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    artifacts: dict[str, dict[str, Any]] = field(
        default_factory=dict
    )

    errors: list[str] = field(
        default_factory=list
    )

    completed: bool = False

    def update_stage(
        self,
        stage: str
    ) -> None:
        """
        Обновляет текущий этап выполнения.
        """

        self.stage = stage

    def add_result(
        self,
        agent_name: str,
        artifact: dict[str, Any]
    ) -> None:
        """
        Сохраняет артефакт агента.
        """

        self.artifacts[agent_name] = artifact

    def get_result(
        self,
        agent_name: str
    ) -> dict[str, Any] | None:
        """
        Возвращает артефакт агента.
        """

        return self.artifacts.get(agent_name)

    def has_result(
        self,
        agent_name: str
    ) -> bool:
        """
        Проверяет наличие артефакта.
        """

        return agent_name in self.artifacts

    def add_error(
        self,
        message: str
    ) -> None:
        """
        Регистрирует ошибку выполнения.
        """

        self.errors.append(message)

    def has_errors(
        self
    ) -> bool:
        """
        Проверяет наличие ошибок.
        """

        return len(self.errors) > 0

    def mark_completed(
        self
    ) -> None:
        """
        Помечает выполнение завершенным.
        """

        self.completed = True

    def set_metadata(
        self,
        key: str,
        value: Any
    ) -> None:
        """
        Сохраняет служебные данные.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Возвращает служебные данные.
        """

        return self.metadata.get(
            key,
            default
        )

    def to_dict(
        self
    ) -> dict[str, Any]:
        """
        Представляет контекст в виде словаря.
        """

        return {
            "task_id": self.task.id,
            "stage": self.stage,
            "completed": self.completed,
            "started_at": self.started_at.isoformat(),
            "artifacts": self.artifacts,
            "errors": self.errors,
            "metadata": self.metadata,
        }
