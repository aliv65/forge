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

    constitution_role = "release"

    schema_name = "release_package.json"

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

        if review["status"] != "approved":
            return AgentResult.fail(
                "Release is not approved by review."
            )

        if tests["status"] != "passed":
            return AgentResult.fail(
                "Release tests did not pass."
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
            "changes": {
                "description": implementation["summary"],
                "affected_components": architecture[
                    "affected_components"
                ],
                "changed_files": [
                    file["path"]
                    for file in implementation["changed_files"]
                ]
            },
            "validation": {
                "review_status": review["status"],
                "test_status": tests["status"],
                "checks_passed": True,
                "issues": []
            },
            "architecture_decisions": [
                architecture["id"]
            ],
            "memory_updates": [
                "Architecture decision will be saved after release."
            ],
            "release_notes": (
                "Mock pipeline completed without changing application code."
            )
        }

        return AgentResult.ok(
            release_package
        )
