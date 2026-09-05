"""Regression boundaries for the terminal agent control plane."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def module(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / (name + ".py")
    )
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


class CoreCutoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = module("validate-agent-governance")

    def test_symlink_projection_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outside" / "agents").mkdir(parents=True)
            (root / ".claude").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(self.registry.HarnessError):
                self.registry._projection_files(
                    root, PurePosixPath(".claude/agents"), ".md"
                )

    def test_diagnostics_redact_duplicate_key_and_invalid_value(self):
        sentinel = "synthetic-sensitive-sentinel"
        with self.assertRaises(self.registry.HarnessError) as raised:
            self.registry.decode_json_text(
                '{"' + sentinel + '":1,"' + sentinel + '":2}', sentinel
            )
        self.assertNotIn(sentinel, str(raised.exception))
        data = self.registry.load_json(ROOT, self.registry.REGISTRY_PATH)
        data["roles"][0]["permission_class"] = sentinel
        with self.assertRaises(self.registry.HarnessError) as raised:
            self.registry.validate_registry(ROOT, data, check_files=False)
        self.assertNotIn(sentinel, str(raised.exception))

    def test_schema_and_cli_diagnostics_never_disclose_input(self):
        sentinel = "synthetic-sensitive-sentinel"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema = root / self.registry.REGISTRY_SCHEMA_PATH
            schema.parent.mkdir(parents=True)
            schema.write_text(json.dumps({"type": sentinel}))
            with self.assertRaises(self.registry.HarnessError) as raised:
                self.registry.validate_registry(root, {}, check_files=False)
            self.assertNotIn(sentinel, str(raised.exception))
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/validate-agent-governance.py"),
                    "--root",
                    str(root / sentinel),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_nonexistent_tier_fragment_is_rejected(self):
        data = self.registry.load_json(ROOT, self.registry.REGISTRY_PATH)
        data["roles"][0]["capability_tier_ref"] = (
            "docs/00.agent-governance/policies/model-selection.md#missing"
        )
        with self.assertRaises(self.registry.HarnessError):
            self.registry.validate_registry(ROOT, data)

    def test_schema_references_fail_closed_without_network(self):
        sentinel = "synthetic-sensitive-sentinel"
        for reference in ("#/$defs/" + sentinel, "https://invalid.example/" + sentinel):
            with (
                self.subTest(reference=reference),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                schema = root / self.registry.REGISTRY_SCHEMA_PATH
                schema.parent.mkdir(parents=True)
                schema.write_text(json.dumps({"$ref": reference}))
                (root / self.registry.REGISTRY_PATH).write_text("{}")
                with (
                    mock.patch(
                        "urllib.request.urlopen",
                        side_effect=RuntimeError("fetch forbidden"),
                    ) as urlopen,
                    mock.patch(
                        "socket.socket", side_effect=RuntimeError("socket forbidden")
                    ),
                    mock.patch(
                        "socket.getaddrinfo", side_effect=RuntimeError("DNS forbidden")
                    ),
                ):
                    with self.assertRaises(self.registry.HarnessError) as raised:
                        self.registry._validate_registry_schema(root, {})
                    self.assertEqual(raised.exception.code, "AGENT-REGISTRY-SCHEMA")
                    self.assertNotIn(sentinel, str(raised.exception))
                    urlopen.assert_not_called()
                if reference.startswith("#"):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(ROOT / "scripts/validate-agent-governance.py"),
                            "--root",
                            str(root),
                        ],
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn(sentinel, result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_valid_local_schema_reference_is_supported(self):
        schema = {"$ref": "#/$defs/object", "$defs": {"object": {"type": "object"}}}
        with mock.patch.object(self.registry, "load_json", return_value=schema):
            self.assertEqual(self.registry._validate_registry_schema(ROOT, {}), {})
