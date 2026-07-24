"""
Product Agent.

Первый этап Forge pipeline.
Преобразует входную задачу в структурированный продуктовый контекст.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ProductAgent(BaseAgent):
    """
    Агент анализа требований.

    Ответственность:
    - понять цель задачи;
    - выделить требования;
    - проверить полноту входных данных.

    Не отвечает за:
    - архитектуру;
    - код;
    - тестирование.
    """

    name = "product-agent"

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Выполняет продуктовый анализ задачи.
        """

        if not self.validate_context(context):
            return self.create_error_result(
                "Invalid execution context"
            )

        task = context.task

        if not task.is_ready_for_processing():
            return self.create_error_result(
                "Task does not contain enough information"
            )

        result = {
            "task_id": task.id,
            "title": task.title,
            "goal": task.description,
            "requirements": task.requirements,
            "constraints": task.constraints,
            "acceptance_criteria": task.acceptance_criteria,
            "open_questions": task.open_questions
        }

        context.add_result(
            self.name,
            result
        )

        return self.create_success_result(
            result
        )
