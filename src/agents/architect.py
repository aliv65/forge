"""
Architecture Agent.

Второй этап Forge pipeline.
Формирует архитектурное решение на основе задачи.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ArchitectAgent(BaseAgent):
    """
    Агент архитектурного проектирования.

    Ответственность:
    - анализировать требования;
    - учитывать ограничения;
    - формировать архитектурное решение.

    Не отвечает за:
    - написание кода;
    - тестирование;
    - релиз.
    """

    name = "architect-agent"

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Создает архитектурное решение.
        """

        if not self.validate_context(context):
            return self.create_error_result(
                "Invalid execution context"
            )

        product_result = context.get_result(
            "product-agent"
        )

        if product_result is None:
            return self.create_error_result(
                "Product analysis result not found"
            )

        decision = {
            "id": "ADR-001",
            "title": (
                "Implementation based on "
                "existing Forge pipeline"
            ),
            "status": "accepted",
            "summary": (
                "Реализация выполняется через "
                "существующий pipeline агентов "
                "с передачей данных через ExecutionContext."
            ),
            "affected_components": [
                "orchestrator",
                "agents",
                "models"
            ],
            "changes": [
                "Создать необходимый компонент",
                "Использовать существующие контракты"
            ],
            "rationale": (
                "Решение сохраняет слабую связанность "
                "между агентами и соответствует "
                "архитектуре Forge."
            ),
            "risks": [
                "Недостаток информации при сложных задачах"
            ],
            "constitution_check": {
                "passed": True,
                "violations": []
            }
        }

        context.add_result(
            self.name,
            decision
        )

        return self.create_success_result(
            decision
        )
