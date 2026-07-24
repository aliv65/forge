"""
Base Provider.

Абстракция для взаимодействия Forge с различными AI-моделями.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ProviderResponse:
    """
    Унифицированный ответ AI Provider.
    """

    content: str

    metadata: dict[str, Any] | None = None


class BaseProvider(ABC):
    """
    Базовый контракт AI Provider.

    Ответственность:
    - предоставить единый интерфейс
      генерации ответа.

    Не отвечает за:
    - формирование prompt;
    - бизнес-логику;
    - обработку артефактов.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: dict[str, Any] | None = None
    ) -> ProviderResponse:
        """
        Выполняет запрос к AI-модели.

        Args:
            prompt:
                Текст запроса.

            context:
                Дополнительные данные выполнения.

        Returns:
            ProviderResponse.
        """

        raise NotImplementedError

    def health_check(
        self
    ) -> bool:
        """
        Проверяет доступность провайдера.

        По умолчанию считаем,
        что провайдер доступен.
        """

        return True

    @property
    def name(
        self
    ) -> str:
        """
        Название провайдера.
        """

        return self.__class__.__name__
