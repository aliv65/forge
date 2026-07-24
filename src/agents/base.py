"""
Base Agent.

Определяет базовый контракт для всех агентов Forge.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from orchestrator.context import ExecutionContext
from providers.base import BaseProvider
from utils.logger import ForgeLogger


@dataclass(slots=True)
class AgentResult:
    """
    Результат выполнения агента.
    """

    success: bool
    payload: dict[str, Any] | None = None
    error: str | None = None

    @classmethod
    def ok(cls, payload: dict[str, Any]) -> "AgentResult":
        return cls(
            success=True,
            payload=payload,
            error=None
        )

    @classmethod
    def fail(cls, message: str) -> "AgentResult":
        return cls(
            success=False,
            payload=None,
            error=message
        )


class BaseAgent(ABC):
    """
    Базовый класс всех агентов Forge.

    Жизненный цикл:

        run()
            ↓
        validate()
            ↓
        execute()
            ↓
        logging
            ↓
        AgentResult
    """

    name = "base-agent"

    def __init__(
        self,
        provider: BaseProvider,
        logger: ForgeLogger
    ):
        self.provider = provider
        self.logger = logger

    def run(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Единая точка входа.
        """

        self.logger.agent_started(
            self.name,
            context.task.id
        )

        if not self.validate(context):
            result = AgentResult.fail(
                "Context validation failed."
            )

            self.logger.error(
                result.error,
                {
                    "agent": self.name,
                    "task_id": context.task.id
                }
            )

            return result

        result = self.execute(context)

        if result.success:

            if result.payload is not None:
                context.add_result(
                    self.name,
                    result.payload
                )

            self.logger.agent_completed(
                self.name,
                context.task.id
            )

        else:

            self.logger.error(
                result.error or "Unknown error",
                {
                    "agent": self.name,
                    "task_id": context.task.id
                }
            )

        return result

    def validate(
        self,
        context: ExecutionContext
    ) -> bool:
        """
        Базовая проверка контекста.
        """

        return context is not None and context.task is not None

    def ask_llm(
        self,
        prompt: str,
        context: dict[str, Any] | None = None
    ) -> str:
        """
        Унифицированный вызов AI Provider.
        """

        response = self.provider.generate(
            prompt=prompt,
            context=context
        )

        return response.content

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Реализуется конкретным агентом.
        """
        raise NotImplementedError
