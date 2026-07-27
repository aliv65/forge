"""
Schema Validator.

Проверка соответствия артефактов Forge
JSON Schema контрактам.
"""

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


class SchemaValidationError(Exception):
    """
    Ошибка нарушения JSON Schema.
    """

    pass


class SchemaValidator:
    """
    Валидатор контрактов Forge.

    Ответственность:
    - загрузка схем;
    - проверка данных;
    - возврат результата проверки.

    Не отвечает за:
    - исправление данных;
    - генерацию артефактов;
    - принятие решений.
    """

    def __init__(
        self,
        schema_path: str | Path | None = None
    ) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.schema_path = Path(schema_path or project_root / "schemas")

    def load_schema(
        self,
        schema_name: str
    ) -> dict[str, Any]:
        """
        Загружает JSON Schema из файла.
        """

        file_path = (
            self.schema_path
            / schema_name
        )

        if not file_path.exists():
            raise SchemaValidationError(
                f"Schema not found: {schema_name}"
            )

        return json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )

    def validate(
        self,
        data: dict[str, Any],
        schema_name: str
    ) -> bool:
        """
        Проверяет объект по схеме.
        """

        schema = self.load_schema(
            schema_name
        )

        try:
            Draft202012Validator(schema).validate(data)
        except ValidationError as error:
            raise SchemaValidationError(
                error.message
            ) from error

        return True

    def validate_with_report(
        self,
        data: dict[str, Any],
        schema_name: str
    ) -> dict[str, Any]:
        """
        Возвращает подробный отчет проверки.
        """

        try:
            self.validate(
                data,
                schema_name
            )

            return {
                "valid": True,
                "errors": []
            }

        except SchemaValidationError as error:

            return {
                "valid": False,
                "errors": [
                    str(error)
                ]
            }
