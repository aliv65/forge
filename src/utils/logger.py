"""
Forge Logger.

Единый журнал событий выполнения pipeline.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import json


class ForgeLogger:
    """
    Логирование событий Forge.

    Ответственность:
    - фиксировать этапы выполнения;
    - сохранять ошибки;
    - создавать audit trail.

    Не отвечает за:
    - обработку ошибок;
    - изменение состояния pipeline;
    - принятие решений.
    """

    def __init__(
        self,
        log_path: str = "logs"
    ):
        self.log_path = Path(
            log_path
        )

        self.log_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.execution_file = (
            self.log_path
            / "execution.log"
        )

        self.error_file = (
            self.log_path
            / "errors.log"
        )

    def _write(
        self,
        file_path: Path,
        event: Dict[str, Any]
    ) -> None:
        """
        Записывает событие в файл.
        """

        with file_path.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    event,
                    ensure_ascii=False
                )
            )

            file.write("\n")

    def log(
        self,
        event_type: str,
        message: str,
        metadata: Dict[str, Any] | None = None
    ) -> None:
        """
        Создает информационное событие.
        """

        event = {
            "timestamp": (
                datetime.now()
                .isoformat()
            ),
            "type": event_type,
            "message": message,
            "metadata": (
                metadata
                if metadata
                else {}
            )
        }

        self._write(
            self.execution_file,
            event
        )

    def error(
        self,
        message: str,
        metadata: Dict[str, Any] | None = None
    ) -> None:
        """
        Создает событие ошибки.
        """

        event = {
            "timestamp": (
                datetime.now()
                .isoformat()
            ),
            "level": "error",
            "message": message,
            "metadata": (
                metadata
                if metadata
                else {}
            )
        }

        self._write(
            self.error_file,
            event
        )

    def agent_started(
        self,
        agent_name: str,
        task_id: str
    ) -> None:
        """
        Лог начала работы агента.
        """

        self.log(
            "agent_started",
            (
                f"Agent {agent_name} started"
            ),
            {
                "agent": agent_name,
                "task_id": task_id
            }
        )

    def agent_completed(
        self,
        agent_name: str,
        task_id: str
    ) -> None:
        """
        Лог успешного завершения агента.
        """

        self.log(
            "agent_completed",
            (
                f"Agent {agent_name} completed"
            ),
            {
                "agent": agent_name,
                "task_id": task_id
            }
        )

    def pipeline_failed(
        self,
        stage: str,
        error: str
    ) -> None:
        """
        Лог ошибки pipeline.
        """

        self.error(
            (
                f"Pipeline failed "
                f"at stage {stage}"
            ),
            {
                "stage": stage,
                "error": error
            }
        )
