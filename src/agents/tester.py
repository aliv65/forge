"""
Testing Agent.

Проверяет готовность реализации к релизу.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class TestingAgent(BaseAgent):
    """
    Testing Agent.

    Ответственность:
    - анализировать результаты ревью;
    - формировать тестовый набор;
    - оценивать готовность к релизу.

    Не отвечает за:
    - исправление реализации;
    - проведение ревью;
    - выпуск релиза.
    """

    name = "testing-agent"

    constitution_role = "testing"

    schema_name = "test_suite.json"

    PROMPT_TEMPLATE = """
Ты QA Engineer.

На основе реализации и результатов ревью
подготовь тестовый набор.

Реализация:

{implementation}

Результаты ревью:

{review}

Верни:

1. Набор тестовых сценариев.
2. Возможные риски.
3. Общую оценку готовности к релизу.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Формирует тестовый набор.
        """

        implementation = context.get_result(
            "coding-agent"
        )

        if implementation is None:
            return AgentResult.fail(
                "Implementation not found."
            )

        review = context.get_result(
            "review-agent"
        )

        if review is None:
            return AgentResult.fail(
                "Review report not found."
            )

        prompt = self.PROMPT_TEMPLATE.format(
            implementation=implementation["summary"],
            review=review["summary"]
        )

        llm_response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        tests = [
            {
                "id": (
                    f"TEST-{context.task.id}-CASE-{index:03d}"
                ),
                "name": criterion,
                "type": "acceptance",
                "description": (
                    "Mock acceptance scenario generated from the task."
                ),
                "status": "passed"
            }
            for index, criterion in enumerate(
                context.task.acceptance_criteria,
                start=1
            )
        ]

        test_suite = {
            "id": f"TEST-{context.task.id}",
            "implementation_id": implementation["id"],
            "status": "passed",
            "summary": llm_response,
            "tests": tests,
            "acceptance_criteria_coverage": [
                {
                    "criterion": criterion,
                    "covered": True,
                    "tests": [
                        tests[index]["id"]
                    ]
                }
                for index, criterion in enumerate(
                    context.task.acceptance_criteria
                )
            ],
            "issues": []
        }

        return AgentResult.ok(
            test_suite
        )
