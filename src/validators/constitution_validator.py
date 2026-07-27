"""
Constitution Validator.

Проверка соответствия результатов Forge
инженерным правилам из Constitution.
"""

from pathlib import Path
from typing import Any
import yaml


class ConstitutionViolation:
    """
    Представляет нарушение правила Constitution.
    """

    def __init__(
        self,
        rule: str,
        description: str
    ):
        self.rule = rule
        self.description = description

    def to_dict(
        self
    ) -> dict[str, str]:
        return {
            "rule": self.rule,
            "description": self.description
        }


class ConstitutionValidator:
    """
    Проверяет соблюдение инженерных правил Forge.

    Ответственность:
    - загрузка Constitution;
    - проверка обязательных правил;
    - формирование отчета.

    Не отвечает за:
    - исправление нарушений;
    - изменение Constitution;
    - принятие архитектурных решений.
    """

    def __init__(
        self,
        constitution_path: str | Path | None = None
    ) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.path = Path(
            constitution_path
            or project_root / "constitution/constitution.yaml"
        )

        self.constitution = (
            self.load()
        )

    def load(
        self
    ) -> dict[str, Any]:
        """
        Загружает Constitution.
        """

        if not self.path.exists():
            return {}

        return yaml.safe_load(
            self.path.read_text(
                encoding="utf-8"
            )
        ) or {}

    def validate(
        self,
        artifact: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Проверяет артефакт.
        """

        violations: list[ConstitutionViolation] = []

        constitution_check = artifact.get(
            "constitution_check"
        )

        if constitution_check and not constitution_check.get(
            "passed",
            False
        ):
            for violation in constitution_check.get(
                "violations",
                []
            ):
                violations.append(
                    ConstitutionViolation(
                        rule=violation,
                        description="Artifact failed Constitution validation."
                    )
                )

        return {
            "passed": (
                len(violations) == 0
            ),
            "violations": [
                violation.to_dict()
                for violation in violations
            ]
        }

    def check_agent_contract(
        self,
        agent_role: str
    ) -> dict[str, Any]:
        """
        Проверяет наличие агента в Constitution.
        """

        agent_rules = self.constitution.get(
            "agent_rules",
            {}
        )

        return {
            "registered": (
                agent_role
                in agent_rules
            )
        }
