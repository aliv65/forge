"""
Mock Provider.

Локальная реализация AI Provider
для демонстрации и тестирования Forge.
"""

from __future__ import annotations

from providers.base import BaseProvider


class MockResponse:
    """
    Ответ Mock Provider.
    """

    def __init__(
        self,
        content: str
    ) -> None:
        self.content = content


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
        context: dict | None = None
    ) -> MockResponse:
        """
        Генерирует предсказуемый ответ.
        """

        self.calls.append(
            prompt
        )

        response = self._generate_response(
            prompt
        )

        return MockResponse(
            response
        )

    def _generate_response(
        self,
        prompt: str
    ) -> str:
        """
        Формирует демонстрационный ответ.
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
                "Components and boundaries defined."
            )

        if "senior software engineer" in prompt_lower:

            return (
                "Implementation plan generated. "
                "Required changes identified."
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
                "All stages completed."
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
        Возвращает количество обращений.
        """

        return len(self.calls)
