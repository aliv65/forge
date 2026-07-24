"""
Mock Provider.

Тестовая реализация AI Provider
для локальной демонстрации Forge.
"""

from typing import Dict, Any

from providers.base import (
    BaseProvider,
    ProviderResponse
)


class MockProvider(BaseProvider):
    """
    Имитация AI-модели.

    Используется для:
    - локального запуска;
    - тестирования pipeline;
    - демонстрации архитектуры.

    Не используется для:
    - реальной генерации решений.
    """

    name = "mock-provider"

    def generate(
        self,
        prompt: str,
        context: Dict[str, Any] | None = None
    ) -> ProviderResponse:
        """
        Возвращает демонстрационный ответ.
        """

        if not self.validate_prompt(prompt):
            return ProviderResponse(
                content=(
                    "Empty prompt received"
                ),
                metadata={
                    "status": "error"
                }
            )

        response = {
            "provider": self.name,
            "prompt": prompt,
            "message": (
                "Mock response generated. "
                "Replace with real LLM provider."
            ),
            "context_received": (
                context is not None
            )
        }

        return ProviderResponse(
            content=str(response),
            metadata={
                "provider": self.name,
                "mock": True
            }
        )
