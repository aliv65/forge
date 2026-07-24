"""
Coding Agent.

Третий этап Forge pipeline.
Создает результат реализации на основе архитектурного решения.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class CodingAgent(BaseAgent):
    """
    Агент реализации.

    Ответственность:
    - реализовать утвержденное решение;
    - описать изменения;
    - подготовить результат для проверки.

    Не отвечает за:
    - архитектурные решения;
    - ревью;
    - тестирование.
    """

    name = "coding-agent"

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Создает результат реализации.
        """

        if not self.validate_context(context):
            return self.create_error_result(
                "Invalid execution context"
            )

        architecture_decision = context.get_result(
            "architect-agent"
        )

        if architecture_decision is None:
            return self.create_error_result(
                "Architecture decision not found"
            )

        implementation = {
            "id": "IMPL-001",
            "task_id": context.task.id,
            "architecture_decision_id": (
                architecture_decision["id"]
            ),
            "status": "completed",
            "summary": (
                "Реализация выполнена "
                "в соответствии с архитектурным решением."
            ),
            "changed_files": [
                {
                    "path": "src/example.py",
                    "change_type": "created",
                    "description": (
                        "Создан демонстрационный "
                        "компонент реализации."
                    )
                }
            ],
            "implementation_details": [
                "Использован существующий pipeline Forge",
                "Данные передаются через ExecutionContext"
            ],
            "used_components": [
                "orchestrator",
                "agents",
                "models"
            ],
            "limitations": [
                "Генерация реального кода "
                "будет добавлена через Provider"
            ]
        }

        context.add_result(
            self.name,
            implementation
        )

        return self.create_success_result(
            implementation
        )
