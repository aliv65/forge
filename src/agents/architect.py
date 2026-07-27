"""
Architect Agent.

Формирует архитектурное решение (ADR) и сохраняет его в Architecture Memory.
"""

from __future__ import annotations

from agents.base import BaseAgent, AgentResult

from memory.architecture_memory import ArchitectureMemory

from orchestrator.context import ExecutionContext


class ArchitectAgent(BaseAgent):
    """
    Architect Agent.

    Ответственность:
    - анализировать спецификацию;
    - формировать архитектурное решение;
    - сохранять ADR в память.

    Не отвечает за:
    - реализацию;
    - тестирование;
    - релиз.
    """

    name = "architect-agent"

    constitution_role = "architecture"

    schema_name = "architecture_decision.json"

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

    def __init__(
        self,
        provider,
        logger,
        memory: ArchitectureMemory | None = None
    ) -> None:

        super().__init__(
            provider,
            logger
        )

        self.memory = (
            memory
            or ArchitectureMemory()
        )

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Создает ADR.
        """

        specification = context.get_result(
            "product-agent"
        )

        if specification is None:

            return AgentResult.fail(
                "Product specification not found."
            )

        prompt = self.PROMPT_TEMPLATE.format(
            specification=specification["description"]
        )

        response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": context.task.id
            }
        )

        architecture_decision = {
            "id": (
                f"ADR-{context.task.id}"
            ),
            "task_id": context.task.id,
            "title": (
                f"Architecture for {context.task.title}"
            ),
            "summary": response,
            "affected_components": [
                "API",
                "Application Layer",
                "Persistence Layer"
            ],
            "changes": [
                "Implement the approved task within existing boundaries."
            ],
            "rationale": (
                "The mock pipeline preserves the current architecture."
            ),
            "risks": specification["open_questions"],
            "constitution_check": {
                "passed": True,
                "violations": []
            },
            "status": "accepted",
        }

        return AgentResult.ok(
            architecture_decision
        )

    def commit(
        self,
        context: ExecutionContext
    ) -> None:
        """
        Сохраняет утвержденный ADR после полного успеха pipeline.
        """

        decision = context.get_result(
            self.name
        )

        if decision is None:
            return

        file_path = self.memory.save(
            decision
        )

        context.set_metadata(
            "architecture_memory_saved",
            True
        )

        context.set_metadata(
            "architecture_memory_path",
            str(file_path)
        )
