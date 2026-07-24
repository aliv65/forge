"""
Pipeline.

Определяет последовательность выполнения агентов Forge.
"""

from __future__ import annotations

from typing import Iterable

from agents.base import BaseAgent


class Pipeline:
    """
    Последовательность агентов Forge.

    Pipeline является неизменяемым описанием
    процесса выполнения. Он не управляет
    исполнением и не содержит бизнес-логики.

    Ответственность:
    - хранить порядок выполнения агентов;
    - предоставлять доступ к агентам;
    - поддерживать расширение pipeline.

    Не отвечает за:
    - выполнение агентов;
    - обработку ошибок;
    - логирование;
    - управление состоянием.
    """

    def __init__(
        self,
        agents: Iterable[BaseAgent]
    ) -> None:
        self._agents = list(agents)

        if not self._agents:
            raise ValueError(
                "Pipeline must contain at least one agent."
            )

    def get_agents(self) -> list[BaseAgent]:
        """
        Возвращает агентов в порядке выполнения.
        """
        return list(self._agents)

    def add_agent(
        self,
        agent: BaseAgent
    ) -> None:
        """
        Добавляет нового агента
        в конец pipeline.
        """

        self._agents.append(agent)

    def insert_agent(
        self,
        index: int,
        agent: BaseAgent
    ) -> None:
        """
        Вставляет агента
        в указанную позицию.
        """

        self._agents.insert(
            index,
            agent
        )

    def remove_agent(
        self,
        name: str
    ) -> bool:
        """
        Удаляет агента по имени.

        Возвращает True,
        если агент найден.
        """

        for index, agent in enumerate(
            self._agents
        ):

            if agent.name == name:

                del self._agents[index]

                return True

        return False

    def has_agent(
        self,
        name: str
    ) -> bool:
        """
        Проверяет наличие агента.
        """

        return any(
            agent.name == name
            for agent in self._agents
        )

    def __iter__(self):
        """
        Позволяет итерироваться
        по pipeline.
        """

        return iter(self._agents)

    def __len__(self) -> int:
        """
        Возвращает количество агентов.
        """

        return len(self._agents)

    def __repr__(self) -> str:
        """
        Строковое представление pipeline.
        """

        names = [
            agent.name
            for agent in self._agents
        ]

        return (
            f"Pipeline({names})"
        )
