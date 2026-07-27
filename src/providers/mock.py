"""
Mock Provider.

Локальная реализация AI Provider
для демонстрации и тестирования Forge.
"""

from __future__ import annotations

from typing import Any

from providers.base import (
    BaseProvider,
    ProviderResponse
)


class MockProvider(BaseProvider):
    """
    Детерминированный AI Provider.

    Используется для:
    - локального запуска;
    - тестирования pipeline;
    - демонстрации архитектуры.

    Не использует внешние API.
    """

    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None
    ) -> ProviderResponse:
        """
        Генерирует ответ модели.
        """

        self.calls.append(
            prompt
        )

        response = self._generate_response(
            prompt
        )
        prompt_tokens, completion_tokens = (
            self._get_token_usage(prompt)
        )

        return ProviderResponse(
            content=response,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=(
                prompt_tokens
                + completion_tokens
            ),
            metadata={
                "provider": self.name,
                "mode": "mock",
                "context": context or {}
            }
        )

    def _generate_response(
        self,
        prompt: str
    ) -> str:
        """
        Создает детерминированный ответ.

        В реальном Provider здесь был бы
        вызов LLM API.
        """

        prompt_lower = prompt.lower()

        if "product manager" in prompt_lower:

            return (
                "Product specification generated. "
                "Business requirements analyzed."
            )

        if "системный архитектор" in prompt_lower:

            return (
                "Architecture decision generated. "
                "System boundaries defined."
            )

        if "qa engineer" in prompt_lower:

            return (
                "Test suite generated. "
                "Release readiness confirmed."
            )

        if "release manager" in prompt_lower:

            return (
                "Release package prepared. "
                "All pipeline stages completed."
            )

        if "code review" in prompt_lower:

            return (
                "Code review completed. "
                "Implementation quality accepted."
            )

        if "senior software engineer" in prompt_lower:

            return (
                "Implementation plan generated. "
                "Required code changes identified."
            )

        return (
            "Mock AI response generated."
        )

    def _get_token_usage(
        self,
        prompt: str
    ) -> tuple[int, int]:
        """Returns deterministic token usage for each agent role."""

        prompt_lower = prompt.lower()

        if "product manager" in prompt_lower:
            return 1200, 800

        if "системный архитектор" in prompt_lower:
            return 1000, 700

        if "qa engineer" in prompt_lower:
            return 600, 400

        if "release manager" in prompt_lower:
            return 400, 300

        if "code review" in prompt_lower:
            return 700, 500

        if "senior software engineer" in prompt_lower:
            return 1800, 1200

        return 0, 0

    def reset(
        self
    ) -> None:
        """
        Очищает историю запросов.
        """

        self.calls.clear()

    def get_call_count(
        self
    ) -> int:
        """
        Возвращает количество запросов.
        """

        return len(
            self.calls
        )
