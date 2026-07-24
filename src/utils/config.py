"""
Forge Configuration.

Централизованные настройки приложения.
"""

from __future__ import annotations

from dataclasses import dataclass

import os


@dataclass(slots=True)
class ForgeConfig:
    """
    Основная конфигурация Forge.
    """

    environment: str

    logs_directory: str

    memory_directory: str

    application_name: str

    version: str


def load_config() -> ForgeConfig:
    """
    Загружает конфигурацию приложения.

    Значения могут быть переопределены
    через переменные окружения.
    """

    return ForgeConfig(

        application_name=(
            "Forge"
        ),

        version=(
            "0.1.0"
        ),

        environment=os.getenv(
            "FORGE_ENV",
            "development"
        ),

        logs_directory=os.getenv(
            "FORGE_LOGS_PATH",
            "logs"
        ),

        memory_directory=os.getenv(
            "FORGE_MEMORY_PATH",
            "memory/decisions"
        )
    )


config = load_config()
