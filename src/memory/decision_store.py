"""
Decision Store.

Предоставляет API для поиска и анализа архитектурных решений, сохраненных в ArchitectureMemory.
"""

from __future__ import annotations

from typing import Any

from memory.architecture_memory import ArchitectureMemory


class DecisionStore:
    """
    Каталог архитектурных решений.

    Ответственность:
    - поиск решений;
    - фильтрация;
    - получение статистики.

    Не отвечает за:
    - сохранение решений;
    - изменение решений;
    - выполнение pipeline.
    """

    def __init__(
        self,
        memory: ArchitectureMemory | None = None
    ) -> None:
        self.memory = memory or ArchitectureMemory()

    def all(
        self
    ) -> list[dict[str, Any]]:
        """
        Возвращает все решения.
        """

        return self.memory.load_all()

    def latest(
        self
    ) -> dict[str, Any] | None:
        """
        Возвращает последнее решение.
        """

        return self.memory.latest()

    def by_task(
        self,
        task_id: str
    ) -> dict[str, Any] | None:
        """
        Возвращает решение по идентификатору задачи.
        """

        return self.memory.find_by_task(task_id)

    def by_status(
        self,
        status: str
    ) -> list[dict[str, Any]]:
        """
        Возвращает решения с указанным статусом.
        """

        return [
            decision
            for decision in self.memory.load_all()
            if decision.get("status") == status
        ]

    def containing_component(
        self,
        component: str
    ) -> list[dict[str, Any]]:
        """
        Ищет решения, содержащие компонент.
        """

        return [
            decision
            for decision in self.memory.load_all()
            if component in decision.get(
                "components",
                []
            )
        ]

    def search(
        self,
        text: str
    ) -> list[dict[str, Any]]:
        """
        Выполняет простой полнотекстовый поиск
        по краткому описанию решения.
        """

        query = text.lower()

        return [
            decision
            for decision in self.memory.load_all()
            if query in decision.get(
                "summary",
                ""
            ).lower()
        ]

    def statistics(
        self
    ) -> dict[str, Any]:
        """
        Возвращает сводную статистику.
        """

        decisions = self.memory.load_all()

        statuses: dict[str, int] = {}

        for decision in decisions:
            status = decision.get(
                "status",
                "unknown"
            )

            statuses[status] = (
                statuses.get(status, 0) + 1
            )

        return {
            "total": len(decisions),
            "statuses": statuses
        }
