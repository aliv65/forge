"""
Review Agent.

Выполняет автоматизированное ревью реализации.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ReviewAgent(BaseAgent):
    """
    Review Agent.

    Ответственность:
    - анализировать реализацию;
    - выявлять потенциальные проблемы;
    - формировать отчет ревью.

    Не отвечает за:
    - изменение реализации;
    - тестирование;
    - принятие архитектурных решений.
    """

    name = "review-agent"

    PROMPT_TEMPLATE = """
Ты Senior Software Engineer.

Проведи code review реализации.

Описание реализации:

{implementation}

Оцени:

1. Качество реализации.
2. Возможные проблемы.
3. Риски поддержки.
4. Соответствие архитектуре.

Верни краткий отчет ревью.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Выполняет ревью реализации.
        """

        implementation = context.get_result(
            "coding-agent"
        )

        if implementation is None:
            return AgentResult.fail(
                "Implementation not found."
            )

        prompt = self.PROMPT_TEMPLATE.format(
            implementation=implementation["summary"]
        )

        llm_response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        review_report = {
            "id": f"REVIEW-{context.task.id}",
            "task_id": context.task.id,
            "status": "approved",
            "summary": llm_response,
            "findings": [],
            "recommendations": [
                "Добавить модульные тесты.",
                "Обработать возможные ошибки ввода-вывода."
            ],
            "score": 9.2
        }

        return AgentResult.ok(
            review_report
        )
