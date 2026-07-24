"""
Architecture Memory.

Долговременное хранилище архитектурных решений (ADR).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ArchitectureMemory:
    """
    Хранилище архитектурных решений.

    Ответственность:
    - сохранять ADR;
    - загружать ADR;
    - искать решения;
    - предоставлять историю решений.

    Не отвечает за:
    - принятие архитектурных решений;
    - выполнение pipeline;
    - работу с AI.
    """

    def __init__(
        self,
        root: str = "memory/decisions"
    ) -> None:
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        decision: dict[str, Any]
    ) -> Path:
        """
        Сохраняет архитектурное решение.
        """

        task_id = decision.get(
            "task_id",
            "unknown"
        )

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_path = (
            self.root
            / f"{timestamp}_{task_id}.json"
        )

        with file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                decision,
                file,
                ensure_ascii=False,
                indent=2
            )

        return file_path

    def load_all(
        self
    ) -> list[dict[str, Any]]:
        """
        Загружает все архитектурные решения.
        """

        decisions: list[dict[str, Any]] = []

        for file in sorted(
            self.root.glob("*.json")
        ):
            with file.open(
                "r",
                encoding="utf-8"
            ) as f:
                decisions.append(
                    json.load(f)
                )

        return decisions

    def find_by_task(
        self,
        task_id: str
    ) -> dict[str, Any] | None:
        """
        Возвращает последнее решение
        для указанной задачи.
        """

        decisions = [
            decision
            for decision in self.load_all()
            if decision.get("task_id") == task_id
        ]

        if not decisions:
            return None

        return decisions[-1]

    def latest(
        self
    ) -> dict[str, Any] | None:
        """
        Возвращает последнее сохраненное решение.
        """

        decisions = self.load_all()

        if not decisions:
            return None

        return decisions[-1]

    def count(
        self
    ) -> int:
        """
        Возвращает количество сохраненных решений.
        """

        return len(
            list(
                self.root.glob("*.json")
            )
        )

    def clear(
        self
    ) -> None:
        """
        Удаляет все сохраненные решения.

        Используется только
        в тестах и демонстрациях.
        """

        for file in self.root.glob("*.json"):
            file.unlink()
