"""
Base Agent.

Базовый контракт всех AI-агентов Forge.
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

    artifact: dict[str, Any] | None = None

    error: str | None = None

    @classmethod
    def ok(
        cls,
        artifact: dict[str, Any]
    ) -> "AgentResult":
        """
        Успешный результат.
        """

        return cls(
            success=True,
            artifact=artifact
        )

    @classmethod
    def fail(
        cls,
        error: str
    ) -> "AgentResult":
        """
        Ошибка выполнения.
        """

        return cls(
            success=False,
            error=error
        )


class BaseAgent(ABC):
    """
    Базовый класс AI-агента Forge.

    Ответственность:
    - общий жизненный цикл агента;
    - вызов AI Provider;
    - сохранение результата;
    - обработка ошибок.

    Не отвечает за:
    - бизнес-логику конкретного этапа.
    """

    name: str = "base-agent"

    def __init__(
        self,
        provider: BaseProvider,
        logger: ForgeLogger
    ) -> None:

        self.provider = provider

        self.logger = logger


    def run(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Полный жизненный цикл агента.
        """

        self.logger.log(
            "agent_started",
            f"{self.name} started",
            {
                "task_id": context.task.id
            }
        )

        try:

            result = self.execute(
                context
            )

            if result.success:

                context.add_result(
                    self.name,
                    result.artifact
                )

                self.logger.log(
                    "agent_completed",
                    f"{self.name} completed",
                    {
                        "task_id": (
                            context.task.id
                        )
                    }
                )

            else:

                self.logger.log(
                    "agent_failed",
                    f"{self.name} failed",
                    {
                        "error": result.error
                    }
                )

            return result


        except Exception as error:

            self.logger.log(
                "agent_exception",
                f"{self.name} exception",
                {
                    "error": str(error)
                }
            )

            return AgentResult.fail(
                str(error)
            )


    def ask_llm(
        self,
        prompt: str,
        context: dict | None = None
    ) -> str:
        """
        Унифицированный вызов AI Provider.
        """

        response = self.provider.generate(
            prompt,
            context
        )

        return response.content


    @abstractmethod
    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Реализация конкретного агента.
        """

        raise NotImplementedError
