"""Offline JSON Schema evaluation keeps its boundary across jsonschema versions."""

from __future__ import annotations

import importlib
import sys
import unittest
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import json_schema_validation  # noqa: E402


class SchemaEvaluationBoundaryTest(unittest.TestCase):
    def test_internal_definitions_resolve(self) -> None:
        schema = {
            "$defs": {"count": {"type": "integer"}},
            "properties": {"a": {"$ref": "#/$defs/count"}},
        }

        messages = [
            error.message
            for error in json_schema_validation.schema_errors(schema, {"a": "x"})
        ]

        self.assertEqual(messages, ["'x' is not of type 'integer'"])

    def test_clean_instance_reports_nothing(self) -> None:
        schema = {
            "$defs": {"count": {"type": "integer"}},
            "properties": {"a": {"$ref": "#/$defs/count"}},
        }

        self.assertEqual(json_schema_validation.schema_errors(schema, {"a": 1}), [])

    def test_external_schema_resources_stay_forbidden(self) -> None:
        """The resolver must never reach the network, on any jsonschema version."""

        schema = {"properties": {"a": {"$ref": "https://example.invalid/s.json"}}}

        with self.assertRaises(json_schema_validation.SchemaEvaluationError):
            json_schema_validation.schema_errors(schema, {"a": 1})

    def test_invalid_schema_fails_closed_without_leaking_values(self) -> None:
        with self.assertRaises(json_schema_validation.SchemaEvaluationError) as raised:
            json_schema_validation.schema_errors({"type": 5}, {})

        self.assertEqual(str(raised.exception), "invalid local JSON Schema")

    def test_import_emits_no_deprecation_warning(self) -> None:
        """A validator writes evidence; a warning on stderr is not evidence.

        The pinned CI interpreter carries a newer jsonschema than a developer
        machine may have, so this only fails where the deprecation exists. That
        is the environment whose stderr the archive cutover contract reads.
        """

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(json_schema_validation)

        deprecations = [
            str(item.message)
            for item in caught
            if issubclass(item.category, DeprecationWarning)
        ]
        self.assertEqual(deprecations, [])


if __name__ == "__main__":
    unittest.main()
