#!/usr/bin/env python3
"""Legacy instruction cutover and retained bounded-reader/Git regressions."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-agent-legacy-cutover.py"


def load_validator():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        spec = importlib.util.spec_from_file_location(
            "validate_agent_legacy_cutover", VALIDATOR_PATH
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


class ValidatorArtifactOwnerTests(unittest.TestCase):
    def setUp(self) -> None:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        self.addCleanup(sys.path.remove, str(REPO_ROOT / "scripts"))
        spec = importlib.util.spec_from_file_location(
            "legacy_affected_owner", REPO_ROOT / "scripts/validate-affected-surfaces.py"
        )
        self.owner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.owner)
        self.contract = json.loads((REPO_ROOT / self.owner.CONTRACT_PATH).read_text())
        self.schema = json.loads((REPO_ROOT / self.owner.SCHEMA_PATH).read_text())

    def test_supplied_owner_facts_never_reopen_paths(self) -> None:
        expected = self.owner.validator_script_paths(REPO_ROOT)
        with mock.patch.object(
            self.owner, "load_json", side_effect=AssertionError("reopen")
        ):
            actual = self.owner.validator_script_paths(
                REPO_ROOT, self.contract, raw_schema=self.schema
            )
        self.assertEqual(actual, expected)
        self.assertIn("scripts/validate-agent-legacy-cutover.py", actual)

    def test_local_schema_references_preserve_default_validation(self) -> None:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://example.invalid/owner-schema",
            "$defs": {"owner": self.schema},
            "$ref": "#/$defs/owner",
        }
        self.assertEqual(
            self.owner.validator_script_paths(
                REPO_ROOT, self.contract, raw_schema=schema
            ),
            self.owner.validator_script_paths(REPO_ROOT),
        )

    def test_external_schema_references_fail_offline_and_redacted(self) -> None:
        sentinel = "private-schema-sentinel"
        for reference in ("https://example.invalid/" + sentinel, "file:///" + sentinel):
            with (
                self.subTest(reference=reference),
                mock.patch(
                    "urllib.request.urlopen", side_effect=AssertionError("network")
                ),
                mock.patch.object(
                    self.owner, "load_json", side_effect=AssertionError("reopen")
                ),
            ):
                with self.assertRaises(self.owner.ContractError) as raised:
                    self.owner.validator_script_paths(
                        REPO_ROOT, self.contract, raw_schema={"$ref": reference}
                    )
                self.assertNotIn(sentinel, str(raised.exception))
                self.assertEqual(raised.exception.code, "SURFACE-SCHEMA-DEFINITION")


class AgentLegacyCutoverValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.documents = cls.validator.documents.load_registry(REPO_ROOT)

    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-cutover-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        self.targets = {
            "docs/00.agent-governance/contracts/agent-role-semantics.json": ".agents/registry.json",
            "docs/00.agent-governance/contracts/agent-role-semantics.schema.json": ".agents/contracts/agent-registry.schema.json",
            "scripts/validate-agent-role-semantics.py": "scripts/validate-agent-harness-semantics.py",
            "tests/fixtures/agent-role-semantics.json": ".agents/registry.json",
            ".github/ABOUT.md": ".github/README.md",
            "docs/00.agent-governance/common-governance.md": ".agents/registry.json",
            "docs/00.agent-governance/harness-implementation-map.md": ".agents/registry.json",
            "docs/00.agent-governance/providers/agents-md.md": "docs/00.agent-governance/providers/codex.md",
        }
        for relative in set(self.targets.values()):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "{}\n" if relative.endswith(".json") else "Current artifact\n"
            )
        self.owners = types.SimpleNamespace(
            document_registry=self.documents,
            native_paths=frozenset({"AGENTS.md", ".codex/agents/reviewer.toml"}),
            enforcement_paths=frozenset({"scripts/validate-agent-legacy-cutover.py"}),
            proof=types.SimpleNamespace(
                terminal_targets=self.targets,
                consumers={},
                rendered_dispositions={},
                declarations={},
            ),
        )
        # Explicit owner facts isolate legacy scanning/IO from the full archive
        # corpus; public historical proof has separate real-Git tests.
        patcher = mock.patch.object(
            self.validator, "_load_owners", return_value=self.owners
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        subprocess.run(
            ["/usr/bin/git", "init", "--quiet"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.stage(root)
        return root

    def stage(self, root: Path, *paths: str | Path) -> None:
        subprocess.run(
            [
                "/usr/bin/git",
                "add",
                "--",
                *(os.fspath(path) for path in paths or (".",)),
            ],
            cwd=root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "HOME": "/dev/null",
                "LC_ALL": "C",
            },
        )

    def add_text(self, root: Path, path: str, text: str) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        self.stage(root, path)

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_valid_cutover_passes(self) -> None:
        root = self.make_valid_root()
        self.assertEqual(self.validator.validate_repository(root)["activeConsumers"], 0)

    def test_plain_instructions_fail_for_every_published_or_unknown_artifact(
        self,
    ) -> None:
        for path in (
            "AGENTS.md",
            "README.md",
            "docs/90.references/research/2099-01-01-test/report.md",
            "docs/99.templates/templates/common/readme-implementation.template.md",
            "docs/00.agent-governance/memory/progress.md",
            ".codex/agents/reviewer.toml",
            "scripts/tool",
            "scripts/unknown.py",
        ):
            for status in ("active", "accepted", "done"):
                with self.subTest(path=path, status=status):
                    root = self.make_valid_root()
                    self.add_text(
                        root,
                        path,
                        "---\nstatus: "
                        + status
                        + "\n---\nuse scripts/validate-agent-role-semantics.py\n",
                    )
                    self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_rendered_relative_retired_link_is_a_consumer(self) -> None:
        root = self.make_valid_root()
        self.add_text(
            root, "README.md", "[old](scripts/validate-agent-role-semantics.py)\n"
        )
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_declared_enforcement_artifacts_are_not_instructions(self) -> None:
        root = self.make_valid_root()
        for path in self.owners.enforcement_paths:
            self.add_text(root, path, '"scripts/validate-agent-role-semantics.py"\n')
        self.assertEqual(self.validator.validate_repository(root)["activeConsumers"], 0)

    def test_test_artifacts_are_never_opened_by_the_production_consumer_scan(
        self,
    ) -> None:
        root = self.make_valid_root()
        self.add_text(
            root,
            "tests/dynamic-regression.py",
            'RETIRED = "scripts/validate-agent-role-semantics.py"\n',
        )
        with self.validator._RepositoryReader(root) as reader:
            candidates = self.validator._repository_candidates(reader)
            original = reader.candidate_payload

            def guarded_payload(path: str, *, read: bool):
                if read and path.startswith("tests/"):
                    raise AssertionError(f"production opened {path}")
                return original(path, read=read)

            with mock.patch.object(
                reader, "candidate_payload", side_effect=guarded_payload
            ):
                _scanned, _evidence, consumers = (
                    self.validator._scan_consumers_with_reader(
                        reader,
                        candidates,
                        self.owners,
                    )
                )
        self.assertEqual(consumers, [])

    def test_published_document_precedes_a_control_identity(self) -> None:
        root = self.make_valid_root()
        self.owners.enforcement_paths |= {"README.md"}
        self.add_text(root, "README.md", "use .github/ABOUT.md\n")
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_exact_history_requires_applicable_disposition_and_rejects_append(
        self,
    ) -> None:
        root = self.make_valid_root()
        path = "docs/00.agent-governance/memory/progress.md"
        raw = b"[old](../harness-implementation-map.md)\n"
        self.add_text(root, path, raw.decode())
        retired_path = "docs/00.agent-governance/harness-implementation-map.md"
        self.owners.proof.consumers[path] = raw
        self.owners.proof.rendered_dispositions[(path, retired_path)] = (
            ".agents/registry.json"
        )
        self.assertEqual(self.validator.validate_repository(root)["activeConsumers"], 0)
        self.add_text(root, path, raw.decode() + "new instruction\n")
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_archive_payload_proof_requires_whole_input_and_scans_header(self) -> None:
        root = self.make_valid_root()
        path = "docs/90.references/research/2099-01-01-test/archive.md"
        payload = b"scripts/validate-agent-role-semantics.py\n"
        raw = b"Archive envelope header\n" + payload
        self.add_text(root, path, raw.decode())
        self.owners.proof.archive_payloads = {
            path: types.SimpleNamespace(
                input_bytes=raw,
                remaining_text="Archive envelope header\n",
            )
        }
        self.assertEqual(self.validator.validate_repository(root)["activeConsumers"], 0)
        self.add_text(root, path, (raw + b"drift\n").decode())
        self.assert_rule(root, "AGQC-LEGACY-OWNER")

        root = self.make_valid_root()
        header = "use .github/ABOUT.md\n"
        self.add_text(root, path, header + payload.decode())
        self.owners.proof.archive_payloads = {
            path: types.SimpleNamespace(
                input_bytes=(header.encode() + payload),
                remaining_text=header,
            )
        }
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_literal_only_history_requires_each_mention_to_be_consumer_scoped(
        self,
    ) -> None:
        root = self.make_valid_root()
        path = "docs/00.agent-governance/memory/progress.md"
        retired_path = "docs/00.agent-governance/harness-implementation-map.md"
        raw = (retired_path + "\n").encode()
        self.add_text(root, path, raw.decode())
        self.owners.proof.consumers[path] = raw
        self.owners.proof.literal_dispositions = {
            (path, retired_path): ".agents/registry.json"
        }
        self.assertEqual(self.validator.validate_repository(root)["activeConsumers"], 0)
        self.add_text(root, path, raw.decode() + "use .github/ABOUT.md\n")
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_literal_only_history_rejects_matching_raw_with_an_unproved_token(self):
        path = "docs/00.agent-governance/memory/progress.md"
        literal = "docs/00.agent-governance/harness-implementation-map.md"
        extra = ".github/ABOUT.md"
        raw = (literal + "\n" + extra + "\n").encode()
        proof = types.SimpleNamespace(
            consumers={path: raw},
            literal_dispositions={(path, literal): ".agents/registry.json"},
            rendered_dispositions={},
            terminal_targets={
                literal: ".agents/registry.json",
                extra: ".github/README.md",
            },
        )
        self.assertFalse(
            self.validator._historical_dispositions_cover(
                path, raw, frozenset({literal, extra}), proof
            )
        )

    def test_rendered_history_keeps_terminal_coverage_when_it_also_has_literal_evidence(
        self,
    ) -> None:
        path = "docs/00.agent-governance/memory/progress.md"
        literal = "docs/00.agent-governance/harness-implementation-map.md"
        rendered = "scripts/validate-agent-role-semantics.py"
        raw = (literal + "\n" + rendered + "\n").encode()
        proof = types.SimpleNamespace(
            consumers={path: raw},
            literal_dispositions={(path, literal): ".agents/registry.json"},
            rendered_dispositions={
                (path, rendered): "scripts/validate-agent-harness-semantics.py"
            },
            terminal_targets={
                literal: ".agents/registry.json",
                rendered: "scripts/validate-agent-harness-semantics.py",
            },
        )
        self.assertTrue(
            self.validator._historical_dispositions_cover(
                path, raw, frozenset({literal, rendered}), proof
            )
        )

    def test_exact_membership_without_disposition_does_not_waive_retired_token(
        self,
    ) -> None:
        root = self.make_valid_root()
        path = "docs/90.references/research/2099-01-01-test/report.md"
        raw = b"use scripts/validate-agent-role-semantics.py\n"
        self.add_text(root, path, raw.decode())
        self.owners.proof.consumers[path] = raw
        self.owners.proof.terminal_targets.pop(
            "scripts/validate-agent-role-semantics.py"
        )
        self.assert_rule(root, "AGQC-LEGACY-REPLACEMENT")

    def test_retained_surfaces_and_missing_successors_fail_closed(self) -> None:
        for path in (
            self.validator.RETIRED_SURFACES + self.validator.RETIRED_OWNER_PATHS
        ):
            with self.subTest(path=path):
                root = self.make_valid_root()
                self.add_text(root, path, "{}\n")
                self.assert_rule(root, "AGQC-LEGACY-RETIRED")
        root = self.make_valid_root()
        (root / ".github/README.md").unlink()
        self.assert_rule(root, "AGQC-LEGACY-REPLACEMENT")

    def test_successor_symlink_is_rejected(self) -> None:
        root = self.make_valid_root()
        target = root / ".github/README.md"
        target.unlink()
        target.symlink_to("../.agents/registry.json")
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

    def test_invalid_utf8_retired_consumer_fails_closed(self) -> None:
        root = self.make_valid_root()
        (root / "tool").write_bytes(b"scripts/validate-agent-role-semantics.py\xff")
        self.stage(root, "tool")
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

    def test_untracked_files_are_never_read_or_counted(self) -> None:
        root = self.make_valid_root()
        baseline = self.validator.validate_repository(root)
        self.add_text(root, ".gitignore", "ignored*\n")
        for path in ("ignored-tool", "untracked-tool"):
            target = root / path
            target.write_text("use .github/ABOUT.md\n")
            target.chmod(0)
        counts = self.validator.validate_repository(root)
        self.assertEqual(counts["activeConsumers"], 0)
        self.assertEqual(counts["scannedFiles"], baseline["scannedFiles"] + 1)
        (root / "untracked-tool").chmod(0o600)
        self.stage(root, "untracked-tool")
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_owner_inputs_reject_nonobjects_and_duplicate_json(self) -> None:
        root = self.make_valid_root()
        for raw in ('{"duplicate": 1, "duplicate": 2}', "[]", "null", "{"):
            with self.subTest(raw=raw):
                (root / ".agents/registry.json").write_text(raw)
                with self.validator._RepositoryReader(root) as reader:
                    with self.assertRaises(self.validator.ContractError):
                        self.validator._owner_object(reader, ".agents/registry.json")

    def test_held_reader_owner_limit_cannot_enlarge_legacy_limit(self) -> None:
        root = self.make_valid_root()
        path = "bounded-owner.json"
        (root / path).write_bytes(b"12345")
        with self.validator._RepositoryReader(root) as reader:
            self.assertEqual(reader.read_bytes(path, max_bytes=5), b"12345")
            for limit in (4, 0, -1, True, None):
                with (
                    self.subTest(limit=limit),
                    self.assertRaises(self.validator.ContractError),
                ):
                    reader.read_bytes(path, max_bytes=limit)
            with mock.patch.object(self.validator, "MAX_REGULAR_FILE_BYTES", 4):
                with self.assertRaises(self.validator.ContractError):
                    reader.read_bytes(path, max_bytes=100)

    def test_nonregular_roots_and_candidates_fail_closed(self) -> None:
        root = self.make_valid_root()
        alias = root / "root-alias"
        alias.symlink_to(root, target_is_directory=True)
        with self.assertRaises(self.validator.ContractError):
            self.validator.validate_repository(alias)
        (root / "directory").mkdir()
        os.mkfifo(root / "fifo")
        (root / "link").symlink_to(".agents/registry.json")
        for path in ("directory", "fifo", "link"):
            with (
                self.subTest(path=path),
                self.validator._RepositoryReader(root) as reader,
            ):
                with self.assertRaises(self.validator.ContractError):
                    reader.candidate_payload(path, read=True)

    def test_candidate_encoding_and_paths_fail_closed(self) -> None:
        for raw in (b"unterminated", b"/absolute\0", b"../escape\0", b"bad\xff\0"):
            with self.subTest(raw=raw), self.assertRaises(self.validator.ContractError):
                self.validator._parse_git_candidates(raw)

    def owner_candidates(self) -> tuple[str, ...]:
        registry = json.loads(
            (REPO_ROOT / self.validator.documents.REGISTRY_PATH).read_bytes()
        )
        return (
            ".agents/registry.json",
            ".agents/contracts/agent-registry.schema.json",
            "scripts/validation/registry.json",
            "scripts/validation/registry.schema.json",
            self.validator.documents.REGISTRY_PATH.as_posix(),
            self.validator.documents.SCHEMA_PATH.as_posix(),
            *(
                profile["template_source"]
                for profile in registry["profiles"]
                if profile["template_source"] is not None
            ),
        )

    def test_missing_typed_document_registry_never_falls_back_to_reopen(self) -> None:
        with (
            self.validator._RepositoryReader(REPO_ROOT) as reader,
            mock.patch.object(
                self.validator.links,
                "repository_historical_migration_proof",
                return_value=types.SimpleNamespace(document_registry=None),
            ),
            mock.patch.object(
                self.validator.documents,
                "load_json_file",
                side_effect=AssertionError("reopen"),
            ),
        ):
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator._load_owners(reader, self.owner_candidates())
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-OWNER")

    def test_owner_handoff_keeps_complete_held_inputs_and_checked_adapters(
        self,
    ) -> None:
        observed = []
        expected = (REPO_ROOT / "README.md").read_bytes()

        def historical(root, *, registry, raw_schema, read_current_bytes, read_symlink):
            self.assertEqual(root, REPO_ROOT)
            self.assertIsInstance(registry, self.validator.documents.Registry)
            self.assertIsInstance(raw_schema, dict)
            self.assertEqual(read_current_bytes("README.md", len(expected)), expected)
            with self.assertRaises(self.validator.ContractError):
                read_current_bytes("README.md", len(expected) - 1)
            self.assertEqual(read_symlink(".codex/skills"), "../.agents/skills")
            with self.assertRaises(self.validator.ContractError):
                read_symlink("README.md")
            observed.append(registry)
            return types.SimpleNamespace(document_registry=registry)

        with (
            self.validator._RepositoryReader(REPO_ROOT) as reader,
            mock.patch.object(
                self.validator.links,
                "repository_historical_migration_proof",
                side_effect=historical,
            ),
            mock.patch.object(
                self.validator.documents,
                "load_json_file",
                side_effect=AssertionError("JSON reopen"),
            ),
            mock.patch.object(
                self.validator.documents,
                "_lstat_named_path",
                side_effect=AssertionError("template reopen"),
            ),
        ):
            owners = self.validator._load_owners(reader, self.owner_candidates())
        self.assertIs(owners.document_registry, observed[0])

    def test_git_runner_is_absolute_closed_and_ambient_state_free(self) -> None:
        root = self.make_valid_root()
        hostile_bin = root / "hostile-bin"
        hostile_bin.mkdir()
        marker = root / "hostile-git-ran"
        hostile_git = hostile_bin / "git"
        hostile_git.write_text(
            '#!/bin/sh\nprintf invoked > "$HOSTILE_GIT_MARKER"\nexit 127\n',
            encoding="utf-8",
        )
        hostile_git.chmod(0o700)
        hostile_home = root / "hostile-home"
        hostile_home.mkdir()
        (hostile_home / ".gitconfig").write_text("[invalid\n", encoding="utf-8")

        with mock.patch.dict(
            os.environ,
            {
                "PATH": os.fspath(hostile_bin),
                "HOME": os.fspath(hostile_home),
                "XDG_CONFIG_HOME": os.fspath(hostile_home),
                "HOSTILE_GIT_MARKER": os.fspath(marker),
                "GIT_CONFIG_COUNT": "not-an-integer",
                "GIT_CONFIG_KEY_0": "core.fsmonitor",
                "GIT_CONFIG_VALUE_0": "/hostile/fsmonitor",
                "GIT_NAMESPACE": "hostile",
                "GIT_INDEX_FILE": os.fspath(root / "hostile-index"),
            },
            clear=False,
        ):
            self.validator.validate_repository(root)
        self.assertFalse(marker.exists())

        self.assertEqual(self.validator.GIT_EXECUTABLE, "/usr/bin/git")
        with mock.patch.object(
            self.validator,
            "GIT_EXECUTABLE",
            "/definitely/unavailable/git",
        ):
            self.assert_rule(root, "AGQC-LEGACY-INPUT")

    def test_git_runner_closes_argv_environment_and_process_options(self) -> None:
        root = self.make_valid_root()
        observed: list[tuple[list[str], dict[str, object]]] = []
        original = subprocess.Popen

        def recording_popen(arguments, **kwargs):
            observed.append((list(arguments), dict(kwargs)))
            return original(arguments, **kwargs)

        with mock.patch.object(
            self.validator.subprocess,
            "Popen",
            side_effect=recording_popen,
        ):
            self.validator.validate_repository(root)

        self.assertEqual(len(observed), 2)
        expected_commands = (
            ("rev-parse", "--show-toplevel"),
            ("ls-files", "-z", "--cached"),
        )
        for (arguments, options), expected in zip(observed, expected_commands):
            self.assertEqual(arguments[0], "/usr/bin/git")
            self.assertEqual(tuple(arguments[-len(expected) :]), expected)
            self.assertNotIn("--others", arguments)
            self.assertIs(options["stdin"], subprocess.DEVNULL)
            self.assertIs(options["shell"], False)
            self.assertEqual(options["env"], self.validator.GIT_ENVIRONMENT)
            self.assertNotIn("PATH", options["env"])
            self.assertNotIn("GIT_NAMESPACE", options["env"])
            self.assertEqual(len(options["pass_fds"]), 1)

    def test_git_pipe_timeout_and_overflow_reap_process_groups(self) -> None:
        cases = (
            (
                "timeout",
                "import subprocess,sys,time; "
                "child=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                "print(child.pid, flush=True); time.sleep(30)",
                1024,
                1024,
                0.05,
            ),
            (
                "stdout",
                "import subprocess,sys,time; "
                "child=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                "print(child.pid, flush=True); "
                "sys.stdout.buffer.write(b'x'*4096); sys.stdout.flush(); "
                "time.sleep(30)",
                64,
                1024,
                2.0,
            ),
            (
                "stderr",
                "import subprocess,sys,time; "
                "child=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                "print(child.pid, flush=True); "
                "sys.stderr.buffer.write(b'x'*4096); sys.stderr.flush(); "
                "time.sleep(30)",
                1024,
                64,
                2.0,
            ),
        )
        for name, program, stdout_limit, stderr_limit, timeout in cases:
            with self.subTest(name=name):
                pid_fd, pid_path = tempfile.mkstemp(prefix="agent-legacy-child-")
                os.close(pid_fd)
                pid_file = Path(pid_path)
                self.addCleanup(pid_file.unlink, missing_ok=True)
                program = program.replace(
                    "child=subprocess.Popen([sys.executable, '-c', ",
                    "child=subprocess.Popen([sys.executable, '-c', ",
                ).replace(
                    "print(child.pid, flush=True)",
                    f"open({os.fspath(pid_file)!r}, 'w').write(str(child.pid)); "
                    "print(child.pid, flush=True)",
                )
                process = subprocess.Popen(
                    [sys.executable, "-c", program],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False,
                    start_new_session=True,
                )
                child_pid = self.wait_for_published_pid(pid_file)
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator._drain_process(
                        process,
                        timeout_seconds=timeout,
                        stdout_limit=stdout_limit,
                        stderr_limit=stderr_limit,
                        detail="synthetic Git boundary",
                    )
                self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
                self.assertIsNotNone(process.poll())
                self.assert_process_gone(child_pid)

    def test_git_cleanup_kills_descendant_after_leader_exits(self) -> None:
        pid_fd, pid_path = tempfile.mkstemp(prefix="agent-legacy-child-")
        os.close(pid_fd)
        pid_file = Path(pid_path)
        self.addCleanup(pid_file.unlink, missing_ok=True)
        process = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import subprocess,sys; "
                "child=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                f"open({os.fspath(pid_file)!r}, 'w').write(str(child.pid)); "
                "print(child.pid, flush=True)",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=True,
        )
        child_pid = self.wait_for_published_pid(pid_file)
        self.assertEqual(
            process.wait(timeout=self.validator.GIT_CLEANUP_TIMEOUT_SECONDS),
            0,
        )
        self.assertIsNotNone(process.poll())
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._drain_process(
                process,
                timeout_seconds=0.05,
                stdout_limit=1024,
                stderr_limit=1024,
                detail="synthetic Git boundary",
            )
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        self.assertIsNotNone(process.poll())
        self.assert_process_gone(child_pid)

    def test_git_cleanup_wait_allowance_uses_one_deadline(self) -> None:
        class TimedOutProcess:
            pid = 123

            def __init__(self) -> None:
                self.wait_timeouts: list[float] = []

            def poll(self) -> None:
                return None

            def kill(self) -> None:
                pass

            def wait(self, *, timeout: float) -> None:
                self.wait_timeouts.append(timeout)
                clock[0] += timeout
                raise subprocess.TimeoutExpired("synthetic Git", timeout)

        clock = [0.0]
        process = TimedOutProcess()
        with (
            mock.patch.object(self.validator.os, "killpg"),
            mock.patch.object(
                self.validator.time, "monotonic", side_effect=lambda: clock[0]
            ),
            self.assertRaises(self.validator.ContractError) as raised,
        ):
            self.validator._terminate_process(process)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        self.assertLessEqual(
            sum(process.wait_timeouts),
            self.validator.GIT_CLEANUP_TIMEOUT_SECONDS,
        )

    def assert_process_gone(self, process_id: int) -> None:
        deadline = time.monotonic() + self.validator.GIT_CLEANUP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            try:
                os.kill(process_id, 0)
            except ProcessLookupError:
                return
            time.sleep(0.01)
        self.fail(f"synthetic descendant remains alive: {process_id}")

    def wait_for_published_pid(self, pid_file: Path) -> int:
        deadline = time.monotonic() + self.validator.GIT_CLEANUP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            published = pid_file.read_text(encoding="utf-8").strip()
            if published:
                return int(published)
            time.sleep(0.01)
        self.fail(f"synthetic child PID was not published: {pid_file}")

    def test_equal_size_same_inode_content_restore_fails_closed(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-stable-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        payload = root / "payload.txt"
        original = b"safe content\n"
        payload.write_bytes(original)
        original_read = os.read
        restored = False

        def hide_read_restore(descriptor: int, size: int) -> bytes:
            nonlocal restored
            chunk = original_read(descriptor, size)
            if chunk and not restored:
                restored = True
                payload.write_bytes(b"stale-token\n")
                payload.write_bytes(original)
            return chunk

        with (
            self.validator._RepositoryReader(root) as reader,
            mock.patch.object(self.validator.os, "read", side_effect=hide_read_restore),
        ):
            with self.assertRaises(self.validator.ContractError) as raised:
                reader.read_bytes(payload.name)
        self.assertTrue(restored)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

    def test_reader_closes_opened_descriptors_once_when_validation_raises(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-fd-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        safe = root / "safe"
        safe.mkdir()
        (safe / "payload.txt").write_text("inside\n", encoding="utf-8")

        with (
            mock.patch.object(self.validator.os, "open", return_value=731),
            mock.patch.object(
                self.validator.os,
                "fstat",
                side_effect=OSError("synthetic root fstat failure"),
            ),
            mock.patch.object(self.validator.os, "close") as close,
        ):
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator._RepositoryReader(root)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        self.assertEqual(close.call_args_list, [mock.call(731)])

        original_open = os.open
        original_fstat = os.fstat
        original_close = os.close
        closed: list[int] = []

        def record_close(descriptor: int) -> None:
            closed.append(descriptor)
            original_close(descriptor)

        with self.validator._RepositoryReader(root) as reader:

            def fail_child_fstat(descriptor: int):
                if descriptor != reader.root_fd:
                    raise OSError("synthetic child fstat failure")
                return original_fstat(descriptor)

            with (
                mock.patch.object(self.validator.os, "open", side_effect=original_open),
                mock.patch.object(
                    self.validator.os, "fstat", side_effect=fail_child_fstat
                ),
                mock.patch.object(self.validator.os, "close", side_effect=record_close),
            ):
                with self.assertRaises(self.validator.ContractError) as raised:
                    reader.read_bytes("safe/payload.txt")
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        self.assertEqual(len(closed), 1)

        original_stat = os.stat
        closed = []

        with self.validator._RepositoryReader(root) as reader:

            def fail_parent_entry(path, *args, **kwargs):
                if path == "safe" and kwargs.get("dir_fd") == reader.root_fd:
                    raise OSError("synthetic parent entry stat failure")
                return original_stat(path, *args, **kwargs)

            with (
                mock.patch.object(
                    self.validator.os, "stat", side_effect=fail_parent_entry
                ),
                mock.patch.object(self.validator.os, "close", side_effect=record_close),
            ):
                with self.assertRaises(self.validator.ContractError) as raised:
                    reader.read_bytes("safe/payload.txt")
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        self.assertEqual(len(closed), 1)

    def test_git_dual_pipe_drain_is_deadlock_safe(self) -> None:
        process = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import sys; "
                "sys.stdout.buffer.write(b'o'*32768); sys.stdout.flush(); "
                "sys.stderr.buffer.write(b'e'*32768); sys.stderr.flush()",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        stdout, stderr, returncode = self.validator._drain_process(
            process,
            timeout_seconds=2.0,
            stdout_limit=65536,
            stderr_limit=65536,
            detail="synthetic Git boundary",
        )
        self.assertEqual((len(stdout), len(stderr), returncode), (32768, 32768, 0))

    def test_candidate_count_and_path_byte_limits_fail_closed(self) -> None:
        with mock.patch.object(self.validator, "MAX_CANDIDATES", 2):
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator._parse_git_candidates(b"a\0b\0c\0")
            self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
        with mock.patch.object(self.validator, "MAX_CANDIDATE_PATH_BYTES", 3):
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator._parse_git_candidates(b"four\0")
            self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

    def test_every_production_content_read_uses_the_root_dirfd(self) -> None:
        root = self.make_valid_root()
        with (
            mock.patch.object(
                Path,
                "read_text",
                side_effect=AssertionError("Path.read_text is forbidden"),
            ),
            mock.patch.object(
                Path,
                "read_bytes",
                side_effect=AssertionError("Path.read_bytes is forbidden"),
            ),
        ):
            counts = self.validator.validate_repository(root)
        self.assertEqual(counts["activeConsumers"], 0)

    def test_parent_and_final_component_swaps_fail_closed(self) -> None:
        for component in ("parent", "final"):
            with self.subTest(component=component):
                directory = tempfile.TemporaryDirectory(
                    prefix=f"agent-legacy-{component}-swap-"
                )
                outside_directory = tempfile.TemporaryDirectory(
                    prefix="agent-legacy-outside-"
                )
                self.addCleanup(directory.cleanup)
                self.addCleanup(outside_directory.cleanup)
                root = Path(directory.name)
                safe = root / "safe"
                safe.mkdir()
                payload = safe / "payload.txt"
                payload.write_text("inside\n", encoding="utf-8")
                outside = Path(outside_directory.name) / "payload.txt"
                outside.write_text("outside sentinel\n", encoding="utf-8")
                original_open = os.open
                swapped = False

                with self.validator._RepositoryReader(root) as reader:

                    def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
                        nonlocal swapped
                        if path == "payload.txt" and not swapped:
                            swapped = True
                            if component == "parent":
                                safe.rename(root / "safe-original")
                                safe.symlink_to(
                                    Path(outside_directory.name),
                                    target_is_directory=True,
                                )
                            else:
                                payload.unlink()
                                payload.symlink_to(outside)
                        return original_open(path, flags, mode, dir_fd=dir_fd)

                    with mock.patch.object(
                        self.validator.os,
                        "open",
                        side_effect=swapping_open,
                    ):
                        with self.assertRaises(self.validator.ContractError) as raised:
                            reader.read_bytes("safe/payload.txt")
                self.assertTrue(swapped)
                self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
                self.assertEqual(
                    outside.read_text(encoding="utf-8"), "outside sentinel\n"
                )

    def test_oversized_and_growing_files_fail_closed(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-size-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        oversized = root / "oversized.bin"
        oversized.write_bytes(b"x" * 65)
        with (
            mock.patch.object(self.validator, "MAX_REGULAR_FILE_BYTES", 64),
            self.validator._RepositoryReader(root) as reader,
        ):
            with self.assertRaises(self.validator.ContractError) as raised:
                reader.read_bytes(oversized.name)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

        growing = root / "growing.bin"
        growing.write_bytes(b"x" * 32)
        original_read = os.read
        grew = False

        def growing_read(descriptor: int, size: int) -> bytes:
            nonlocal grew
            chunk = original_read(descriptor, size)
            if chunk and not grew:
                grew = True
                with growing.open("ab") as stream:
                    stream.write(b"y" * 64)
            return chunk

        with (
            mock.patch.object(self.validator, "MAX_REGULAR_FILE_BYTES", 64),
            self.validator._RepositoryReader(root) as reader,
            mock.patch.object(self.validator.os, "read", side_effect=growing_read),
        ):
            with self.assertRaises(self.validator.ContractError) as raised:
                reader.read_bytes(growing.name)
        self.assertTrue(grew)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

    def test_diagnostics_are_escaped_bounded_and_single_line(self) -> None:
        hostile = "../evil\n\r\x1b[31m" + ("x" * 900)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._parse_git_candidates(hostile.encode("utf-8") + b"\0")
        detail = raised.exception.detail
        self.assertLessEqual(
            len(detail.encode("utf-8")),
            self.validator.MAX_DIAGNOSTIC_DETAIL_BYTES,
        )
        self.assertNotIn("\n", detail)
        self.assertNotIn("\r", detail)
        self.assertNotIn("\x1b", detail)
        self.assertIn("\\n", detail)
        self.assertIn("\\r", detail)
        self.assertIn("\\x1b", detail)

        with self.assertRaises(self.validator.ContractError) as long_raised:
            self.validator._parse_git_candidates((b"x" * 5000) + b"\0")
        self.assertLessEqual(
            len(long_raised.exception.detail.encode("utf-8")),
            self.validator.MAX_DIAGNOSTIC_DETAIL_BYTES,
        )


if __name__ == "__main__":
    unittest.main()
