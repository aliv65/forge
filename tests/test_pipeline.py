from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agents.architect import ArchitectAgent
from agents.base import AgentResult
from agents.coder import CodingAgent
from agents.product import ProductAgent
from agents.release import ReleaseAgent
from agents.reviewer import ReviewAgent
from agents.tester import TestingAgent
from memory.architecture_memory import ArchitectureMemory
from models.task import Task
from orchestrator.context import ExecutionContext
from orchestrator.engine import Orchestrator
from orchestrator.pipeline import Pipeline
from providers.mock import MockProvider
from utils.logger import ForgeLogger
from validators.constitution_validator import ConstitutionValidator
from validators.schema_validator import (
    SchemaValidationError,
    SchemaValidator,
)


class InvalidProductAgent(ProductAgent):
    def execute(
        self,
        context: ExecutionContext
    ) -> AgentResult:
        return AgentResult.ok(
            {"id": context.task.id}
        )


class MockPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = TemporaryDirectory()
        self.runtime_directory = Path(
            self.temp_directory.name
        )
        self.provider = MockProvider()
        self.logger = ForgeLogger(
            self.runtime_directory / "logs"
        )
        self.memory = ArchitectureMemory(
            self.runtime_directory / "decisions"
        )
        self.task = Task(
            id="TASK-TEST-001",
            title="Validate the mock pipeline",
            description="Run the local demonstration pipeline.",
            requirements=["Complete every mock stage."],
            constraints=["Do not call external services."],
            acceptance_criteria=[
                "Every agent returns a valid artifact.",
                "No application files are modified."
            ],
            open_questions=[]
        )

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def create_orchestrator(self) -> Orchestrator:
        agents = [
            ProductAgent(self.provider, self.logger),
            ArchitectAgent(
                self.provider,
                self.logger,
                memory=self.memory
            ),
            CodingAgent(self.provider, self.logger),
            ReviewAgent(self.provider, self.logger),
            TestingAgent(self.provider, self.logger),
            ReleaseAgent(self.provider, self.logger)
        ]

        return Orchestrator(
            pipeline=Pipeline(agents),
            logger=self.logger
        )

    def test_complete_pipeline_returns_valid_mock_release(self) -> None:
        context = ExecutionContext(self.task)

        result = self.create_orchestrator().run(context)

        self.assertEqual(result["status"], "completed")
        self.assertTrue(context.completed)
        self.assertEqual(self.provider.get_call_count(), 6)
        self.assertEqual(self.memory.count(), 1)
        self.assertTrue(
            context.get_metadata(
                "architecture_memory_saved"
            )
        )

        implementation = context.get_result("coding-agent")
        self.assertEqual(implementation["changed_files"], [])

        release = result["release"]
        self.assertEqual(release["status"], "ready")
        self.assertTrue(
            release["validation"]["checks_passed"]
        )

        schemas = {
            "product-agent": "task.json",
            "architect-agent": "architecture_decision.json",
            "coding-agent": "implementation.json",
            "review-agent": "review_report.json",
            "testing-agent": "test_suite.json",
            "release-agent": "release_package.json"
        }
        validator = SchemaValidator()

        for agent_name, schema_name in schemas.items():
            self.assertTrue(
                validator.validate(
                    context.get_result(agent_name),
                    schema_name
                )
            )

    def test_invalid_artifact_stops_pipeline_without_saving_adr(self) -> None:
        pipeline = Pipeline([
            InvalidProductAgent(
                self.provider,
                self.logger
            )
        ])
        orchestrator = Orchestrator(
            pipeline=pipeline,
            logger=self.logger
        )

        result = orchestrator.run(
            ExecutionContext(self.task)
        )

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["stage"], "product-agent")
        self.assertEqual(self.memory.count(), 0)

    def test_schema_validator_rejects_unknown_properties(self) -> None:
        artifact = self.task.to_dict()
        artifact["unexpected"] = "value"

        with self.assertRaises(SchemaValidationError):
            SchemaValidator().validate(
                artifact,
                "task.json"
            )

    def test_agents_reject_non_mock_providers(self) -> None:
        with self.assertRaises(TypeError):
            ProductAgent(object(), self.logger)

    def test_constitution_registers_pipeline_roles(self) -> None:
        validator = ConstitutionValidator()

        for role in (
            "product",
            "architecture",
            "coding",
            "review",
            "testing",
            "release"
        ):
            self.assertTrue(
                validator.check_agent_contract(role)["registered"]
            )

        result = validator.validate({
            "constitution_check": {
                "passed": False,
                "violations": ["ARCH-001"]
            }
        })

        self.assertFalse(result["passed"])
        self.assertEqual(
            result["violations"][0]["rule"],
            "ARCH-001"
        )
