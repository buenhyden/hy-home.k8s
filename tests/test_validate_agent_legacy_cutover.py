#!/usr/bin/env python3
"""Focused regressions for the closed AGQC-003 legacy cutover contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-agent-legacy-cutover.py"
CONTRACT_PATH = (
    REPO_ROOT
    / "docs/00.agent-governance/contracts/agent-legacy-cutover.json"
)
SCHEMA_PATH = CONTRACT_PATH.with_name("agent-legacy-cutover.schema.json")
FIXTURE_PATH = REPO_ROOT / "tests/fixtures/agent-legacy-cutover.json"

RETIRED_CONTRACT = Path(
    "docs/00.agent-governance/contracts/agent-role-semantics.json"
)
HARNESS_CONTRACT = Path(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
REPLACEMENTS = (
    HARNESS_CONTRACT,
    Path("docs/00.agent-governance/contracts/harness-contract.schema.json"),
    Path("scripts/validate-agent-harness-semantics.py"),
    Path("tests/fixtures/agent-harness-semantics.json"),
    Path(".github/README.md"),
)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_legacy_cutover",
        VALIDATOR_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentLegacyCutoverArtifactTests(unittest.TestCase):
    def test_core_artifacts_exist(self) -> None:
        missing = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in (CONTRACT_PATH, SCHEMA_PATH, VALIDATOR_PATH, FIXTURE_PATH)
            if not path.is_file()
        ]
        self.assertEqual(missing, [])


@unittest.skipUnless(
    VALIDATOR_PATH.is_file() and CONTRACT_PATH.is_file() and SCHEMA_PATH.is_file(),
    "validator is intentionally absent at the RED gate",
)
class AgentLegacyCutoverValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-cutover-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for relative_text in dict.fromkeys(
            self.validator.PACKAGE_REFERENCES
            + self.validator.MIGRATION_REFERENCES
        ):
            relative = Path(relative_text)
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for record in self.validator.PROTECTED_EVIDENCE_FILES:
            relative = Path(record["path"])
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for relative in REPLACEMENTS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if relative == HARNESS_CONTRACT:
                target.write_text(
                    json.dumps(
                        {
                            "consumers": [
                                {
                                    "id": "harness-semantics-validator",
                                    "path": (
                                        "scripts/"
                                        "validate-agent-harness-semantics.py"
                                    ),
                                }
                            ]
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            elif relative.suffix == ".json":
                target.write_text("{}\n", encoding="utf-8")
            else:
                target.write_text("canonical replacement\n", encoding="utf-8")
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
        arguments = ["/usr/bin/git", "add", "--"]
        arguments.extend(os.fspath(path) for path in paths or (".",))
        subprocess.run(
            arguments,
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

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_valid_cutover_root_passes(self) -> None:
        counts = self.validator.validate_repository(self.make_valid_root())
        self.assertEqual(counts["retiredSurfaces"], 5)
        self.assertEqual(counts["replacementSurfaces"], 5)
        self.assertEqual(counts["activeConsumers"], 0)

    def test_self_test_is_deterministic_and_repo_is_unchanged(self) -> None:
        before = CONTRACT_PATH.read_bytes()
        self.assertEqual(self.validator.run_self_test(REPO_ROOT), (3, 24))
        self.assertEqual(CONTRACT_PATH.read_bytes(), before)

    def test_self_test_requires_index_admission_before_source_reads(self) -> None:
        root = self.make_valid_root()
        sentinel = self.validator.FIXTURE_PATH.as_posix()
        subprocess.run(
            ["/usr/bin/git", "rm", "--cached", "--", sentinel],
            cwd=root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.validator.GIT_ENVIRONMENT,
        )
        self.assertTrue((root / sentinel).is_file())
        original_read_bytes = self.validator._RepositoryReader.read_bytes

        def reject_sentinel(reader, value, **kwargs):
            if reader.root_path == root and value == sentinel:
                raise AssertionError("unadmitted source sentinel was opened")
            return original_read_bytes(reader, value, **kwargs)

        with mock.patch.object(
            self.validator._RepositoryReader,
            "read_bytes",
            autospec=True,
            side_effect=reject_sentinel,
        ):
            self.assert_rule_for_self_test(root, "AGQC-LEGACY-INPUT")

    def assert_rule_for_self_test(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.run_self_test(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_closed_schema_rejects_unknown_contract_key(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        mutated["unexpected"] = True
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

        mutated = copy.deepcopy(contract)
        mutated["scanPolicy"]["scanAllRegularFiles"] = True
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_repository_root_and_candidate_paths_fail_closed(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-nongit-")
        self.addCleanup(directory.cleanup)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(Path(directory.name))
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

        root = self.make_valid_root()
        nested = root / "nested"
        nested.mkdir()
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_repository(nested)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

        for payload in (b"../outside\0", b"unterminated", b"invalid-\xff\0"):
            with self.subTest(payload=payload):
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator._parse_git_candidates(payload)
                self.assertEqual(
                    raised.exception.rule_id,
                    "AGQC-LEGACY-INPUT",
                )

    def test_nul_safe_candidate_and_candidate_types_fail_closed(self) -> None:
        root = self.make_valid_root()
        proposed = root / "proposed\nconsumer.txt"
        proposed.write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.stage(root, proposed.name)
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

        proposed.unlink()
        self.stage(root)
        link = root / "proposed-link"
        link.symlink_to("AGENTS.md")
        self.stage(root, link.name)
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

        link.unlink()
        fifo = root / "proposed-fifo"
        os.mkfifo(fifo)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._candidate_payload(
                root,
                fifo.name,
                read=True,
            )
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")

    def test_retained_surface_is_rejected(self) -> None:
        root = self.make_valid_root()
        path = root / RETIRED_CONTRACT
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        self.stage(root, path.relative_to(root))
        self.assert_rule(root, "AGQC-LEGACY-RETIRED")

    def test_missing_replacement_is_rejected(self) -> None:
        root = self.make_valid_root()
        (root / ".github/README.md").unlink()
        self.assert_rule(root, "AGQC-LEGACY-REPLACEMENT")

    def test_stale_current_consumer_is_rejected(self) -> None:
        root = self.make_valid_root()
        (root / "AGENTS.md").write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.stage(root, "AGENTS.md")
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_ignored_unreadable_file_is_not_opened_or_counted(self) -> None:
        root = self.make_valid_root()
        (root / ".gitignore").write_text(
            "ignored-private/\n",
            encoding="utf-8",
        )
        baseline = self.validator.validate_repository(root)
        sentinel = root / "ignored-private/retired-token.txt"
        sentinel.parent.mkdir()
        sentinel.write_text(
            f"private {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        sentinel.chmod(0)
        self.addCleanup(sentinel.chmod, 0o600)

        proposed = root / "proposed-consumer.txt"
        proposed.write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        proposed.chmod(0)
        self.addCleanup(proposed.chmod, 0o600)

        ignored = self.validator.validate_repository(root)
        self.assertEqual(ignored, baseline)

        proposed.chmod(0o600)
        self.stage(root, proposed.name)
        proposed.write_text(
            f"use {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_terminal_and_digest_pinned_evidence_are_not_active_consumers(
        self,
    ) -> None:
        root = self.make_valid_root()
        terminal = root / "docs/04.execution/plans/completed.md"
        terminal.parent.mkdir(parents=True, exist_ok=True)
        terminal.write_text(
            "---\nstatus: Done\n---\n"
            f"historical: {RETIRED_CONTRACT.as_posix()}\n",
            encoding="utf-8",
        )
        self.stage(root, terminal.relative_to(root))
        protected_relative = Path(
            "docs/90.references/data/active-corpus-retention-census.json"
        )
        protected = root / protected_relative
        protected.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / protected_relative, protected)
        self.validator.validate_repository(root)

    def test_digest_pinned_draft_reference_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        record = mutated["referencePolicy"]["protectedEvidenceFiles"][0]
        record["path"] = (
            "docs/90.references/audits/draft-stale-reference.md"
        )
        record["evidenceKind"] = "authored-document"
        record["lifecycleStatus"] = "draft"
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_missing_protected_evidence_is_rejected(self) -> None:
        root = self.make_valid_root()
        protected = root / self.validator.PROTECTED_EVIDENCE_FILES[0]["path"]
        protected.unlink()
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_protected_reference_removal_is_rejected(self) -> None:
        root = self.make_valid_root()
        record = self.validator.PROTECTED_EVIDENCE_FILES[0]
        protected = root / record["path"]
        raw = protected.read_bytes()
        retired = record["retiredReference"].encode("utf-8")
        replacement = record["supersededBy"].encode("utf-8")
        self.assertEqual(raw.count(retired), record["count"])
        protected.write_bytes(raw.replace(retired, replacement))
        self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_active_and_accepted_reference_documents_are_consumers(self) -> None:
        for status in ("active", "accepted"):
            with self.subTest(status=status):
                root = self.make_valid_root()
                reference = (
                    root
                    / "docs/90.references/research/2026-07-07-wer"
                    / f"unowned-{status}.md"
                )
                reference.parent.mkdir(parents=True, exist_ok=True)
                reference.write_text(
                    "---\n"
                    "title: 'Current reference'\n"
                    "type: content/reference\n"
                    f"status: {status}\n"
                    "owner: platform\n"
                    "updated: 2026-07-30\n"
                    "---\n\n"
                    f"use {RETIRED_CONTRACT.as_posix()}\n",
                    encoding="utf-8",
                )
                self.stage(root, reference.relative_to(root))
                self.assert_rule(root, "AGQC-LEGACY-CONSUMER")

    def test_old_harness_consumer_and_compatibility_are_rejected(self) -> None:
        for mutation in ("consumer", "compatibility"):
            with self.subTest(mutation=mutation):
                root = self.make_valid_root()
                harness = root / HARNESS_CONTRACT
                value = json.loads(harness.read_text(encoding="utf-8"))
                if mutation == "consumer":
                    value["consumers"] = [
                        {
                            "id": "role-semantics-validator",
                            "path": "scripts/validate-agent-role-semantics.py",
                        }
                    ]
                else:
                    value["compatibility"] = {
                        "removalOwnerSpec": (
                            "docs/03.specs/"
                            "045-agent-governance-ci-qa-cutover/spec.md"
                        )
                    }
                harness.write_text(
                    json.dumps(value, indent=2) + "\n",
                    encoding="utf-8",
                )
                self.assert_rule(root, "AGQC-LEGACY-HARNESS")

    def test_symlink_replacement_is_rejected(self) -> None:
        root = self.make_valid_root()
        hub = root / ".github/README.md"
        target = hub.with_name("hub-copy.md")
        shutil.copyfile(hub, target)
        hub.unlink()
        hub.symlink_to(target.name)
        self.assert_rule(root, "AGQC-LEGACY-INPUT")

    def test_malformed_and_duplicate_json_are_rejected(self) -> None:
        for text in ('{"consumers": [', '{"consumers": [], "consumers": []}\n'):
            with self.subTest(text=text):
                root = self.make_valid_root()
                (root / HARNESS_CONTRACT).write_text(text, encoding="utf-8")
                self.assert_rule(root, "AGQC-LEGACY-JSON")

    def test_undeclared_allowlist_growth_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        for key, value, expected_rule in (
            ("migrationReferences", "docs/unreviewed.md", "AGQC-LEGACY-SCHEMA"),
            (
                "protectedEvidenceFiles",
                {
                    "path": "docs/current.md",
                    "sha256": "0" * 64,
                },
                "AGQC-LEGACY-SCHEMA",
            ),
        ):
            with self.subTest(key=key):
                mutated = copy.deepcopy(contract)
                mutated["referencePolicy"][key].append(value)
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.validate_contract_data(mutated, schema)
                self.assertEqual(
                    raised.exception.rule_id,
                    expected_rule,
                )

    def test_path_escape_is_rejected(self) -> None:
        root = self.make_valid_root()
        contract, schema = self.validator.load_contract_documents(root)
        mutated = copy.deepcopy(contract)
        mutated["replacementSurfaces"][4] = "../outside.md"
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract_data(mutated, schema)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-SCHEMA")

    def test_fixture_payload_path_changes_are_rejected_before_execution(
        self,
    ) -> None:
        for value in ("/tmp/outside", "../../outside"):
            with self.subTest(value=value):
                directory = tempfile.TemporaryDirectory(
                    prefix="agent-legacy-fixture-"
                )
                self.addCleanup(directory.cleanup)
                root = Path(directory.name)
                fixture = copy.deepcopy(self.fixture)
                fixture["mutationCases"][0]["mutation"]["path"] = value
                path = root / "tests/fixtures/agent-legacy-cutover.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(fixture, indent=2) + "\n",
                    encoding="utf-8",
                )
                with self.assertRaises(
                    self.validator.ContractError
                ) as raised:
                    self.validator._load_fixture(root)
                self.assertEqual(
                    raised.exception.rule_id,
                    "AGQC-LEGACY-FIXTURE",
                )

    def test_fixture_write_rejects_symlink_parent(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-legacy-parent-")
        outside = tempfile.TemporaryDirectory(prefix="agent-legacy-outside-")
        self.addCleanup(directory.cleanup)
        self.addCleanup(outside.cleanup)
        root = Path(directory.name)
        (root / "safe").symlink_to(Path(outside.name), target_is_directory=True)
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator._write_text(root, "safe/escape.md", "blocked\n")
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-FIXTURE")
        self.assertFalse((Path(outside.name) / "escape.md").exists())

    def test_git_runner_is_absolute_closed_and_ambient_state_free(self) -> None:
        root = self.make_valid_root()
        hostile_bin = root / "hostile-bin"
        hostile_bin.mkdir()
        marker = root / "hostile-git-ran"
        hostile_git = hostile_bin / "git"
        hostile_git.write_text(
            "#!/bin/sh\nprintf invoked > \"$HOSTILE_GIT_MARKER\"\nexit 127\n",
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
                pid_file = Path(tempfile.mkstemp(prefix="agent-legacy-child-")[1])
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
                child_pid = int(pid_file.read_text(encoding="utf-8"))
                self.assert_process_gone(child_pid)

    def test_git_cleanup_kills_descendant_after_leader_exits(self) -> None:
        pid_file = Path(tempfile.mkstemp(prefix="agent-legacy-child-")[1])
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
        self.assert_process_gone(int(pid_file.read_text(encoding="utf-8")))

    def assert_process_gone(self, process_id: int) -> None:
        deadline = time.monotonic() + self.validator.GIT_CLEANUP_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            try:
                os.kill(process_id, 0)
            except ProcessLookupError:
                return
            time.sleep(0.01)
        self.fail(f"synthetic descendant remains alive: {process_id}")

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

        with mock.patch.object(self.validator.os, "open", return_value=731), mock.patch.object(
            self.validator.os,
            "fstat",
            side_effect=OSError("synthetic root fstat failure"),
        ), mock.patch.object(self.validator.os, "close") as close:
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
                mock.patch.object(self.validator.os, "fstat", side_effect=fail_child_fstat),
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
                mock.patch.object(self.validator.os, "stat", side_effect=fail_parent_entry),
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
                        with self.assertRaises(
                            self.validator.ContractError
                        ) as raised:
                            reader.read_bytes("safe/payload.txt")
                self.assertTrue(swapped)
                self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-INPUT")
                self.assertEqual(outside.read_text(encoding="utf-8"), "outside sentinel\n")

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

    def test_every_allowed_reference_rejects_occurrence_growth(self) -> None:
        for relative, _counts in self.validator.ALLOWED_REFERENCE_COUNTS:
            with self.subTest(relative=relative):
                root = self.make_valid_root()
                path = root / relative
                path.write_bytes(
                    path.read_bytes()
                    + b"\n"
                    + self.validator.RETIRED_SURFACES[0].encode("utf-8")
                    + b"\n"
                )
                _scanned, _evidence, consumers = (
                    self.validator._scan_consumers(root)
                )
                self.assertTrue(
                    any(
                        consumer.startswith(
                            f"{relative}:allowed-reference-count-drift"
                        )
                        for consumer in consumers
                    ),
                    consumers,
                )


if __name__ == "__main__":
    unittest.main()
