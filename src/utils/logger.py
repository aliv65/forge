"""
Forge Logger.

Централизованное логирование событий системы.
"""

from __future__ import annotations

import json
import logging

from datetime import UTC, datetime

from pathlib import Path

from typing import Any

from utils.config import config


class ForgeLogger:
    """
    Логгер Forge.

    Ответственность:
    - запись событий выполнения;
    - запись ошибок;
    - структурированный вывод.

    Не отвечает за:
    - принятие решений;
    - обработку ошибок;
    - управление pipeline.
    """

    def __init__(
        self,
        log_directory: str | Path | None = None
    ) -> None:
        project_root = Path(__file__).resolve().parents[2]

        configured_directory = Path(
            log_directory or config.logs_directory
        )

        self.log_directory = (
            configured_directory
            if configured_directory.is_absolute()
            else project_root / configured_directory
        )

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.execution_logger = (
            self._create_logger(
                "forge_execution",
                "execution.log"
            )
        )

        self.error_logger = (
            self._create_logger(
                "forge_errors",
                "errors.log"
            )
        )


    def _create_logger(
        self,
        name: str,
        filename: str
    ) -> logging.Logger:
        """
        Создает внутренний logger.
        """

        logger = logging.getLogger(
            f"{name}.{self.log_directory}"
        )

        logger.setLevel(
            logging.INFO
        )

        if not logger.handlers:

            handler = logging.FileHandler(
                self.log_directory / filename,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(message)s"
            )

            handler.setFormatter(
                formatter
            )

            logger.addHandler(
                handler
            )

        return logger


    def log(
        self,
        event: str,
        message: str,
        data: dict[str, Any] | None = None
    ) -> None:
        """
        Записывает событие выполнения.
        """

        payload = {
            "timestamp": (
                datetime.now(UTC)
                .isoformat()
            ),
            "event": event,
            "message": message,
            "data": data or {}
        }

        self.execution_logger.info(
            json.dumps(
                payload,
                ensure_ascii=False
            )
        )


    def error(
        self,
        event: str,
        message: str,
        data: dict[str, Any] | None = None
    ) -> None:
        """
        Записывает ошибку.
        """

        payload = {
            "timestamp": (
                datetime.now(UTC)
                .isoformat()
            ),
            "event": event,
            "message": message,
            "data": data or {}
        }

        self.error_logger.error(
            json.dumps(
                payload,
                ensure_ascii=False
            )
        )


    def pipeline_failed(
        self,
        stage: str,
        error: str
    ) -> None:
        """
        Специализированная запись ошибки pipeline.
        """

        self.error(
            "pipeline_failed",
            (
                f"Pipeline failed at {stage}"
            ),
            {
                "stage": stage,
                "error": error
            }
        )
