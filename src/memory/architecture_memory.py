"""
Architecture Memory.

Хранилище архитектурного контекста Forge.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json


class ArchitectureMemory:
    """
    Локальное хранилище архитектурных решений.

    Ответственность:
    - сохранять решения;
    - читать историю решений;
    - предоставлять контекст агентам.

    Не отвечает за:
    - принятие решений;
    - запуск pipeline;
    - анализ кода.
    """

    def __init__(
        self,
        storage_path: str = "memory/decisions"
    ):
        self.storage_path = Path(
            storage_path
        )

        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_decision(
        self,
        decision: Dict[str, Any]
    ) -> str:
        """
        Сохраняет архитектурное решение.

        Возвращает путь к файлу.
        """

        decision_id = decision.get(
            "id",
            f"ADR-{datetime.now().timestamp()}"
        )

        file_path = (
            self.storage_path
            / f"{decision_id}.json"
        )

        payload = {
            "id": decision_id,
            "created_at": (
                datetime.now()
                .isoformat()
            ),
            "decision": decision
        }

        file_path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return str(file_path)

    def get_decisions(
        self
    ) -> List[Dict[str, Any]]:
        """
        Возвращает все сохраненные решения.
        """

        decisions = []

        for file in self.storage_path.glob(
            "*.json"
        ):
            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            decisions.append(
                data
            )

        return decisions

    def get_context(
        self
    ) -> str:
        """
        Формирует текстовый контекст
        для AI-агентов.
        """

        decisions = self.get_decisions()

        if not decisions:
            return (
                "No architecture decisions "
                "available."
            )

        context = []

        for item in decisions:
            decision = item["decision"]

            context.append(
                (
                    f"{decision.get('id')}: "
                    f"{decision.get('summary')}"
                )
            )

        return "\n".join(context)

    def clear(
        self
    ) -> None:
        """
        Очищает память.

        Используется для тестов.
        """

        for file in self.storage_path.glob(
            "*.json"
        ):
            file.unlink()
