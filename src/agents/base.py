"""
Base Agent.

Базовый контракт всех AI-агентов Forge.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from analytics.token_usage import TokenUsage

from orchestrator.context import ExecutionContext

from providers.base import BaseProvider
from providers.mock import MockProvider

from utils.logger import ForgeLogger

from validators.constitution_validator import ConstitutionValidator
from validators.schema_validator import (
    SchemaValidationError,
    SchemaValidator,
)


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

    constitution_role: str = ""

    schema_name: str | None = None

    def __init__(
        self,
        provider: BaseProvider,
        logger: ForgeLogger,
        schema_validator: SchemaValidator | None = None,
        constitution_validator: ConstitutionValidator | None = None
    ) -> None:

        if not isinstance(provider, MockProvider):
            raise TypeError(
                "Forge supports MockProvider only."
            )

        self.provider = provider

        self.logger = logger

        self.schema_validator = (
            schema_validator
            or SchemaValidator()
        )

        self.constitution_validator = (
            constitution_validator
            or ConstitutionValidator()
        )

        self.last_token_usage = TokenUsage()

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

            agent_contract = (
                self.constitution_validator
                .check_agent_contract(
                    self.constitution_role
                )
            )

            if not agent_contract["registered"]:
                return AgentResult.fail(
                    f"Agent role is not registered: "
                    f"{self.constitution_role}"
                )

            result = self.execute(
                context
            )

            if result.success:

                if result.artifact is None:
                    return AgentResult.fail(
                        "Successful agent result has no artifact."
                    )

                self._validate_artifact(
                    result.artifact
                )

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

        self.last_token_usage = TokenUsage(
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens
        )

        return response.content

    def commit(
        self,
        context: ExecutionContext
    ) -> None:
        """
        Фиксирует отложенные изменения после успешного pipeline.
        """

    def _validate_artifact(
        self,
        artifact: dict[str, Any]
    ) -> None:
        """
        Проверяет контракт и заявленный результат Constitution.
        """

        if self.schema_name:
            self.schema_validator.validate(
                artifact,
                self.schema_name
            )

        constitution_result = (
            self.constitution_validator.validate(
                artifact
            )
        )

        if not constitution_result["passed"]:
            raise SchemaValidationError(
                "Artifact failed Constitution validation."
            )


    @abstractmethod
    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Реализация конкретного агента.
        """

        raise NotImplementedError
