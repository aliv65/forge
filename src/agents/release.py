"""
Release Agent.

Финальный этап Forge pipeline.
Формирует итоговый пакет результата выполнения задачи.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ReleaseAgent(BaseAgent):
    """
    Агент подготовки релиза.

    Ответственность:
    - собрать результаты pipeline;
    - определить готовность результата;
    - сформировать Release Package.

    Не отвечает за:
    - изменение кода;
    - исправление ошибок;
    - повторную проверку.
    """

    name = "release-agent"

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Формирует итоговый пакет релиза.
        """

        if not self.validate_context(context):
            return self.create_error_result(
                "Invalid execution context"
            )

        implementation = context.get_result(
            "coding-agent"
        )

        review_report = context.get_result(
            "review-agent"
        )

        test_suite = context.get_result(
            "testing-agent"
        )

        architecture_decision = context.get_result(
            "architect-agent"
        )

        required_results = [
            implementation,
            review_report,
            test_suite,
            architecture_decision
        ]

        if any(
            result is None
            for result in required_results
        ):
            return self.create_error_result(
                "Pipeline results are incomplete"
            )

        is_ready = (
            review_report["status"] == "approved"
            and test_suite["status"] == "passed"
        )

        release_package = {
            "id": "RELEASE-001",
            "task_id": context.task.id,
            "status": (
                "ready"
                if is_ready
                else "blocked"
            ),
            "summary": (
                "Результат задачи подготовлен "
                "к передаче."
            ),
            "changes": {
                "description": (
                    implementation["summary"]
                ),
                "affected_components": (
                    implementation["used_components"]
                ),
                "changed_files": [
                    file["path"]
                    for file in implementation[
                        "changed_files"
                    ]
                ]
            },
            "validation": {
                "review_status": (
                    review_report["status"]
                ),
                "test_status": (
                    test_suite["status"]
                ),
                "checks_passed": is_ready,
                "issues": (
                    test_suite["issues"]
                )
            },
            "architecture_decisions": [
                architecture_decision["id"]
            ],
            "memory_updates": [],
            "release_notes": (
                "Демонстрационный релиз "
                "Forge pipeline."
            )
        }

        context.add_result(
            self.name,
            release_package
        )

        return self.create_success_result(
            release_package
        )
