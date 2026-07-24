"""
Schema Validator.

Проверка соответствия артефактов Forge
JSON Schema контрактам.
"""

from pathlib import Path
from typing import Dict, Any, List
import json


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
        schema_path: str = "schemas"
    ):
        self.schema_path = Path(
            schema_path
        )

    def load_schema(
        self,
        schema_name: str
    ) -> Dict[str, Any]:
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
        data: Dict[str, Any],
        schema_name: str
    ) -> bool:
        """
        Проверяет объект по схеме.
        """

        schema = self.load_schema(
            schema_name
        )

        required_fields = schema.get(
            "required",
            []
        )

        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing_fields:
            raise SchemaValidationError(
                (
                    "Missing required fields: "
                    f"{missing_fields}"
                )
            )

        return True

    def validate_with_report(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> Dict[str, Any]:
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
