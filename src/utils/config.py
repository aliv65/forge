"""
Forge configuration.

Централизованная конфигурация приложения.
"""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class PathsConfig:
    """
    Пути файловой структуры Forge.
    """

    memory_dir: Path = Path("memory")
    decisions_dir: Path = Path("memory/decisions")
    logs_dir: Path = Path("logs")
    schemas_dir: Path = Path("schemas")
    constitution_file: Path = Path(
        "constitution/constitution.yaml"
    )


@dataclass(frozen=True)
class ProviderConfig:
    """
    Настройки AI Provider.
    """

    provider: str = os.getenv(
        "FORGE_PROVIDER",
        "mock"
    )

    model: str = os.getenv(
        "FORGE_MODEL",
        "mock-model"
    )

    api_key: str = os.getenv(
        "FORGE_API_KEY",
        ""
    )

    temperature: float = float(
        os.getenv(
            "FORGE_TEMPERATURE",
            "0.2"
        )
    )


@dataclass(frozen=True)
class PipelineConfig:
    """
    Настройки pipeline.
    """

    stop_on_error: bool = (
        os.getenv(
            "FORGE_STOP_ON_ERROR",
            "true"
        ).lower() == "true"
    )

    enable_logging: bool = (
        os.getenv(
            "FORGE_ENABLE_LOGGING",
            "true"
        ).lower() == "true"
    )

    validate_schema: bool = (
        os.getenv(
            "FORGE_VALIDATE_SCHEMA",
            "true"
        ).lower() == "true"
    )

    validate_constitution: bool = (
        os.getenv(
            "FORGE_VALIDATE_CONSTITUTION",
            "true"
        ).lower() == "true"
    )


@dataclass(frozen=True)
class AppConfig:
    """
    Корневая конфигурация Forge.
    """

    app_name: str = "Forge"
    version: str = "0.1.0"

    paths: PathsConfig = PathsConfig()
    provider: ProviderConfig = ProviderConfig()
    pipeline: PipelineConfig = PipelineConfig()


config = AppConfig()
