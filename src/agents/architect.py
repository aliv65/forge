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
            specification=(
                specification["summary"]
            )
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
            "summary": response,
            "components": [
                "API",
                "Application Layer",
                "Persistence Layer"
            ],
            "constraints": (
                specification["constraints"]
            ),
            "status": "accepted"
        }

        self.memory.save(
            architecture_decision
        )

        context.set_metadata(
            "architecture_memory_saved",
            True
        )

        return AgentResult.ok(
            architecture_decision
        )
