"""
Constitution Validator.

Проверка соответствия результатов Forge
инженерным правилам из Constitution.
"""

from pathlib import Path
from typing import Dict, Any, List
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
    ) -> Dict[str, str]:
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
        constitution_path: str = (
            "constitution/constitution.yaml"
        )
    ):
        self.path = Path(
            constitution_path
        )

        self.constitution = (
            self.load()
        )

    def load(
        self
    ) -> Dict[str, Any]:
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
        artifact: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Проверяет артефакт.
        """

        violations: List[
            ConstitutionViolation
        ] = []

        rules = self.constitution.get(
            "rules",
            []
        )

        for rule in rules:

            rule_name = rule.get(
                "name"
            )

            required_field = rule.get(
                "required_field"
            )

            if (
                required_field
                and required_field not in artifact
            ):
                violations.append(
                    ConstitutionViolation(
                        rule=rule_name,
                        description=(
                            f"Missing required field: "
                            f"{required_field}"
                        )
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
        agent_name: str
    ) -> Dict[str, Any]:
        """
        Проверяет наличие агента в Constitution.
        """

        agents = self.constitution.get(
            "agents",
            []
        )

        registered_agents = [
            agent.get("name")
            for agent in agents
        ]

        return {
            "registered": (
                agent_name
                in registered_agents
            )
        }
