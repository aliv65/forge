"""
Architect Agent.

Формирует архитектурное решение (ADR) на основе
спецификации Product Agent.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ArchitectAgent(BaseAgent):
    """
    Architect Agent.

    Ответственность:
    - анализировать спецификацию;
    - выбирать архитектурный подход;
    - фиксировать архитектурное решение.
    """

    name = "architect-agent"

    PROMPT_TEMPLATE = """
Ты системный архитектор.

На основе спецификации подготовь архитектурное решение.

Спецификация:

{specification}

Верни:

1. Краткое описание архитектуры.
2. Основные компоненты.
3. Архитектурные ограничения.
4. Причины выбора решения.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Создает архитектурное решение.
        """

        specification = context.get_result(
            "product-agent"
        )

        if specification is None:
            return AgentResult.fail(
                "Product specification not found."
            )

        prompt = self.PROMPT_TEMPLATE.format(
            specification=specification["summary"]
        )

        llm_response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        architecture_decision = {
            "id": f"ADR-{context.task.id}",
            "task_id": context.task.id,
            "summary": llm_response,
            "components": [
                "API",
                "Application Layer",
                "Persistence Layer"
            ],
            "constraints": specification["constraints"],
            "status": "accepted"
        }

        return AgentResult.ok(
            architecture_decision
        )
