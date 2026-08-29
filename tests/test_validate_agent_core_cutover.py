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
        cls.registry = module("validate-agent-harness-contract")
        cls.semantics = module("validate-agent-harness-semantics")
        cls.provider = module("validate-agent-provider-config")

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

    def test_registry_handoff_changes_reject_unchanged_projections(self):
        for addition in (False, True):
            data = self.registry.load_json(ROOT, self.registry.REGISTRY_PATH)
            if addition:
                data["roles"][0]["handoff_to"].append("incident-responder")
            else:
                data["roles"][0]["handoff_to"].pop()
            with (
                self.subTest(addition=addition),
                self.assertRaises(self.semantics.ContractError) as raised,
            ):
                self.semantics.validate_contract(ROOT, data)
            self.assertEqual(raised.exception.code, "ROLE-REGISTRY-HANDOFF")

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
                    str(ROOT / "scripts/validate-agent-harness-contract.py"),
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

    def test_native_empty_model_and_invalid_effort_are_rejected(self):
        for metadata in (
            {"model": ""},
            {"model": "configured-model", "model_reasoning_effort": "invalid"},
            {"model": "configured-model", "model_reasoning_effort": []},
            {"model": "configured-model", "model_reasoning_effort": {}},
        ):
            with (
                self.subTest(metadata=metadata),
                self.assertRaises(self.provider.ProviderConfigError),
            ):
                self.provider.validate_native_metadata("codex", metadata)

    def test_reserved_assertions_are_unique_across_all_projections(self):
        source = self.semantics.adapter_source
        for prefix, code in (
            ("Registry handoff targets:", "ROLE-REGISTRY-HANDOFF"),
            ("Capability tier reference:", "ROLE-REGISTRY-TIER"),
        ):
            for same_value in (True, False):
                for misplaced in (True, False):

                    def mutated(root, selection, surface, role_id):
                        path, text = source(root, selection, surface, role_id)
                        declaration = next(
                            line for line in text.splitlines() if prefix in line
                        )
                        duplicate = (
                            declaration
                            if same_value
                            else "- " + prefix + " `conflict`."
                        )
                        if misplaced:
                            text = text.replace(
                                "## Runtime Bootstrap",
                                duplicate + "\n\n## Runtime Bootstrap",
                                1,
                            )
                        else:
                            text = text.replace(
                                declaration, declaration + "\n\n" + duplicate, 1
                            )
                        return path, text

                    with self.subTest(
                        prefix=prefix, same=same_value, misplaced=misplaced
                    ):
                        with mock.patch.object(
                            self.semantics, "adapter_source", side_effect=mutated
                        ):
                            with self.assertRaises(
                                self.semantics.ContractError
                            ) as raised:
                                self.semantics.validate_repository(ROOT)
                        self.assertEqual(raised.exception.code, code)

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
                        "requests.get", side_effect=RuntimeError("fetch forbidden")
                    ) as get,
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
                    get.assert_not_called()
                    urlopen.assert_not_called()
                if reference.startswith("#"):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(ROOT / "scripts/validate-agent-harness-contract.py"),
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

    def test_unsupported_graph_reintroduction_is_rejected_without_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (".agents/hooks.json", ".codex/hooks.json"):
                path = root / relative
                path.parent.mkdir(exist_ok=True)
                for graph in (
                    {
                        "hooks": {
                            "SessionStart": [
                                {
                                    "matcher": "never",
                                    "hooks": [{"type": "command", "command": ":"}],
                                }
                            ]
                        }
                    },
                    {"customInstructions": "synthetic attack", "hooks": {}},
                ):
                    path.write_text(json.dumps(graph))
                    with self.assertRaises(self.provider.ProviderConfigError) as raised:
                        self.provider.validate_unsupported_hook_surfaces(root)
                    self.assertEqual(raised.exception.code, "PNME-HOOK-UNSUPPORTED")
                path.unlink()
