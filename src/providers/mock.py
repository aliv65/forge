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

        return ProviderResponse(
            content=response,
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

        if "senior software engineer" in prompt_lower:

            return (
                "Implementation plan generated. "
                "Required code changes identified."
            )

        if "code review" in prompt_lower:

            return (
                "Code review completed. "
                "Implementation quality accepted."
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

        return (
            "Mock AI response generated."
        )

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
