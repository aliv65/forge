"""
Review Agent.

Четвертый этап Forge pipeline.
Проверяет реализацию на соответствие архитектуре и правилам проекта.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ReviewAgent(BaseAgent):
    """
    Агент проверки реализации.

    Ответственность:
    - проверить результат Coding Agent;
    - проверить соответствие архитектуре;
    - сформировать отчет проверки.

    Не отвечает за:
    - исправление кода;
    - изменение архитектуры;
    - тестирование.
    """

    name = "review-agent"

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Выполняет проверку реализации.
        """

        if not self.validate_context(context):
            return self.create_error_result(
                "Invalid execution context"
            )

        implementation = context.get_result(
            "coding-agent"
        )

        if implementation is None:
            return self.create_error_result(
                "Implementation result not found"
            )

        architecture_decision = context.get_result(
            "architect-agent"
        )

        if architecture_decision is None:
            return self.create_error_result(
                "Architecture decision not found"
            )

        report = {
            "id": "REVIEW-001",
            "implementation_id": (
                implementation["id"]
            ),
            "status": "approved",
            "summary": (
                "Реализация соответствует "
                "архитектурному решению."
            ),
            "violations": [],
            "warnings": [
                (
                    "Используется mock-реализация "
                    "без подключения AI Provider"
                )
            ],
            "recommendations": [
                (
                    "Добавить Provider Adapter "
                    "для реального LLM"
                )
            ],
            "constitution_check": {
                "passed": True,
                "checked_rules": [
                    "Agents isolation",
                    "Context-based communication",
                    "Schema contracts"
                ]
            },
            "architecture_check": {
                "passed": True,
                "deviations": []
            },
            "conclusion": (
                "Результат готов к тестированию."
            )
        }

        context.add_result(
            self.name,
            report
        )

        return self.create_success_result(
            report
        )
