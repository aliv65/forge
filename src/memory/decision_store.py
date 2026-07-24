"""
Decision Store.

Управление архитектурными решениями Forge (ADR).
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class DecisionStore:
    """
    Хранилище архитектурных решений.

    Ответственность:
    - создавать ADR;
    - получать ADR по ID;
    - искать решения;
    - обновлять статус решений.

    Не отвечает за:
    - принятие архитектурных решений;
    - генерацию решений;
    - работу агентов.
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

    def create(
        self,
        decision: Dict[str, Any]
    ) -> str:
        """
        Создает новое архитектурное решение.
        """

        decision_id = decision.get(
            "id"
        )

        if decision_id is None:
            decision_id = (
                f"ADR-{int(datetime.now().timestamp())}"
            )

        decision_record = {
            "id": decision_id,
            "created_at": (
                datetime.now()
                .isoformat()
            ),
            "status": (
                decision.get(
                    "status",
                    "proposed"
                )
            ),
            "decision": decision
        }

        file_path = (
            self.storage_path
            / f"{decision_id}.json"
        )

        file_path.write_text(
            json.dumps(
                decision_record,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return decision_id

    def get(
        self,
        decision_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Получает решение по идентификатору.
        """

        file_path = (
            self.storage_path
            / f"{decision_id}.json"
        )

        if not file_path.exists():
            return None

        return json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

    def list_all(
        self
    ) -> List[Dict[str, Any]]:
        """
        Возвращает все архитектурные решения.
        """

        decisions = []

        for file_path in self.storage_path.glob(
            "*.json"
        ):
            decisions.append(
                json.loads(
                    file_path.read_text(
                        encoding="utf-8"
                    )
                )
            )

        return decisions

    def update_status(
        self,
        decision_id: str,
        status: str
    ) -> bool:
        """
        Обновляет статус ADR.
        """

        decision = self.get(
            decision_id
        )

        if decision is None:
            return False

        decision["status"] = status

        file_path = (
            self.storage_path
            / f"{decision_id}.json"
        )

        file_path.write_text(
            json.dumps(
                decision,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return True

    def search(
        self,
        keyword: str
    ) -> List[Dict[str, Any]]:
        """
        Поиск решений по ключевому слову.
        """

        results = []

        keyword = keyword.lower()

        for decision in self.list_all():

            content = json.dumps(
                decision,
                ensure_ascii=False
            ).lower()

            if keyword in content:
                results.append(
                    decision
                )

        return results
