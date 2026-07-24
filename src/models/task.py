"""
Task model.

Внутренняя модель инженерной задачи Forge.
Соответствует контракту schemas/task.json.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Task:
    """
    Инженерная задача, проходящая через pipeline Forge.
    """

    id: str
    title: str
    description: str

    requirements: List[str] = field(default_factory=list)

    constraints: List[str] = field(default_factory=list)

    acceptance_criteria: List[str] = field(
        default_factory=list
    )

    open_questions: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def is_ready_for_processing(self) -> bool:
        """
        Проверяет готовность задачи к обработке.
        """

        return (
            bool(self.id)
            and bool(self.title)
            and bool(self.description)
            and len(self.acceptance_criteria) > 0
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует модель в словарь
        для сериализации.
        """

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "requirements": self.requirements,
            "constraints": self.constraints,
            "acceptance_criteria": self.acceptance_criteria,
            "open_questions": self.open_questions,
            "metadata": self.metadata
        }
