"""
Forge Pipeline.

Определяет последовательность выполнения агентов.
"""

from typing import List

from agents.base import BaseAgent


class Pipeline:
    """
    Последовательность выполнения Forge agents.

    Pipeline отвечает только за порядок этапов.
    """

    def __init__(
        self,
        agents: List[BaseAgent]
    ):
        self.agents = agents

    def get_agents(self) -> List[BaseAgent]:
        """
        Возвращает список агентов pipeline.
        """

        return self.agents

    def add_agent(
        self,
        agent: BaseAgent
    ) -> None:
        """
        Добавляет новый этап в pipeline.

        Используется для расширения процесса
        без изменения Orchestrator.
        """

        self.agents.append(agent)

    def remove_agent(
        self,
        agent_name: str
    ) -> None:
        """
        Удаляет агент из pipeline по имени.
        """

        self.agents = [
            agent
            for agent in self.agents
            if agent.name != agent_name
        ]

    def describe(self) -> list[str]:
        """
        Возвращает описание pipeline.
        """

        return [
            agent.name
            for agent in self.agents
        ]
