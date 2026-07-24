"""
AI Provider Base.

Абстракция взаимодействия Forge с AI-моделями.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ProviderResponse:
    """
    Унифицированный результат ответа AI Provider.
    """

    def __init__(
        self,
        content: str,
        metadata: Dict[str, Any] | None = None
    ):
        self.content = content

        self.metadata = (
            metadata
            if metadata is not None
            else {}
        )


class BaseProvider(ABC):
    """
    Абстрактный AI Provider.

    Любой источник AI-моделей должен
    реализовывать этот контракт.
    """

    name: str = "base-provider"

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: Dict[str, Any] | None = None
    ) -> ProviderResponse:
        """
        Генерирует ответ на основе запроса.

        Args:
            prompt:
                Инструкция для модели.

            context:
                Дополнительные данные задачи.

        Returns:
            ProviderResponse
        """

        pass

    def validate_prompt(
        self,
        prompt: str
    ) -> bool:
        """
        Базовая проверка запроса.
        """

        return (
            prompt is not None
            and len(prompt.strip()) > 0
        )
