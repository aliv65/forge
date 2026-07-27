"""
Product Agent.

Преобразует исходную задачу в структурированную
спецификацию для последующих агентов.
"""

from agents.base import BaseAgent, AgentResult
from orchestrator.context import ExecutionContext


class ProductAgent(BaseAgent):
    """
    Product Agent.

    Ответственность:
    - анализировать бизнес-задачу;
    - формировать спецификацию;
    - выделять функциональные требования.
    """

    name = "product-agent"

    constitution_role = "product"

    schema_name = "task.json"

    PROMPT_TEMPLATE = """
Ты Product Manager.

Проанализируй задачу и сформируй структурированную спецификацию.

Название:
{title}

Описание:
{description}

Требования:
{requirements}

Ограничения:
{constraints}

Критерии приемки:
{acceptance_criteria}

Верни краткую спецификацию.
"""

    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        """
        Выполняет анализ задачи.
        """

        task = context.task

        prompt = self.PROMPT_TEMPLATE.format(
            title=task.title,
            description=task.description,
            requirements="\n".join(task.requirements),
            constraints="\n".join(task.constraints),
            acceptance_criteria="\n".join(
                task.acceptance_criteria
            )
        )

        llm_response = self.ask_llm(
            prompt=prompt,
            context={
                "task_id": task.id
            }
        )

        specification = task.to_dict()

        specification["metadata"] = {
            "source": "mock-pipeline"
        }

        specification["description"] = (
            f"{task.description} {llm_response}"
        )

        return AgentResult.ok(
            specification
        )
