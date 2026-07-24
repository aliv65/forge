"""
Base Agent.

Общий контракт всех инженерных агентов Forge.
"""

from abc import ABC, abstractmethod
from typing import Any

from orchestrator.context import ExecutionContext


class AgentResult:
    """
    Базовый контейнер результата работы агента.
    """

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str | None = None
    ):
        self.success = success
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        """
        Проверяет успешность выполнения.
        """

        return self.success


class BaseAgent(ABC):
    """
    Абстрактный инженерный агент Forge.

    Все агенты системы должны наследоваться
    от этого класса.
    """

    name: str = "base-agent"

    def __init__(self):
        pass

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Выполняет этап pipeline.

        Каждый агент реализует собственную логику.
        """

        pass

    def validate_context(
        self,
        context: ExecutionContext
    ) -> bool:
        """
        Базовая проверка входного контекста.
        """

        return (
            context is not None
            and context.task is not None
        )

    def create_success_result(
        self,
        data: Any
    ) -> AgentResult:
        """
        Создает успешный результат.
        """

        return AgentResult(
            success=True,
            data=data
        )

    def create_error_result(
        self,
        error: str
    ) -> AgentResult:
        """
        Создает результат с ошибкой.
        """

        return AgentResult(
            success=False,
            error=error
        )
