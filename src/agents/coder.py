"""
Coding Agent.

Формирует реализацию на основе архитектурного решения.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class CodingAgent(BaseAgent):
    """
    Coding Agent.

    Ответственность:
    - реализовать архитектурное решение;
    - сформировать описание изменений;
    - подготовить артефакт реализации.

    Не отвечает за:
    - архитектуру;
    - ревью;
    - тестирование.
    """

    name = "coding-agent"

    constitution_role = "coding"

    schema_name = "implementation.json"

    PROMPT_TEMPLATE = """
Ты Senior Software Engineer.

На основе архитектурного решения подготовь реализацию.

Архитектурное решение:

{architecture}

Верни:

1. Краткое описание реализации.
2. Какие компоненты необходимо изменить.
3. Какие файлы будут созданы или изменены.
4. Возможные технические риски.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Формирует реализацию.
        """

        architecture = context.get_result(
            "architect-agent"
        )

        if architecture is None:
            return AgentResult.fail(
                "Architecture decision not found."
            )

        prompt = self.PROMPT_TEMPLATE.format(
            architecture=architecture["summary"]
        )

        llm_response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        implementation = {
            "id": f"IMPL-{context.task.id}",
            "task_id": context.task.id,
            "architecture_decision_id": architecture["id"],
            "status": "completed",
            "summary": llm_response,
            "used_components": architecture[
                "affected_components"
            ],
            "changed_files": [],
            "implementation_details": [
                "Mock provider generated an implementation plan.",
                "No project files were changed."
            ],
            "limitations": [
                "The demo pipeline does not write application code."
            ]
        }

        return AgentResult.ok(
            implementation
        )
