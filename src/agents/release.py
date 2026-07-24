"""
Release Agent.

Формирует итоговый пакет релиза на основе
всех предыдущих артефактов.
"""

from agents.base import AgentResult, BaseAgent
from orchestrator.context import ExecutionContext


class ReleaseAgent(BaseAgent):
    """
    Release Agent.

    Ответственность:
    - проверить готовность к релизу;
    - собрать все артефакты;
    - сформировать Release Package.

    Не отвечает за:
    - разработку;
    - тестирование;
    - архитектуру.
    """

    name = "release-agent"

    PROMPT_TEMPLATE = """
Ты Release Manager.

На основе результатов предыдущих этапов
подготовь краткое описание релиза.

Верни:

1. Краткое описание релиза.
2. Основные изменения.
3. Возможные ограничения.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Формирует пакет релиза.
        """

        specification = context.get_result(
            "product-agent"
        )

        architecture = context.get_result(
            "architect-agent"
        )

        implementation = context.get_result(
            "coding-agent"
        )

        review = context.get_result(
            "review-agent"
        )

        tests = context.get_result(
            "testing-agent"
        )

        if specification is None:
            return AgentResult.fail(
                "Specification not found."
            )

        if architecture is None:
            return AgentResult.fail(
                "Architecture decision not found."
            )

        if implementation is None:
            return AgentResult.fail(
                "Implementation not found."
            )

        if review is None:
            return AgentResult.fail(
                "Review report not found."
            )

        if tests is None:
            return AgentResult.fail(
                "Test suite not found."
            )

        if not tests.get("release_ready", False):
            return AgentResult.fail(
                "Release is not approved."
            )

        prompt = self.PROMPT_TEMPLATE.format()

        summary = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        release_package = {
            "id": f"RELEASE-{context.task.id}",
            "task_id": context.task.id,
            "status": "ready",
            "summary": summary,
            "specification": specification,
            "architecture": architecture,
            "implementation": implementation,
            "review": review,
            "tests": tests
        }

        return AgentResult.ok(
            release_package
        )
