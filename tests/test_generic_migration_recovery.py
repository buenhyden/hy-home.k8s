"""Public migration recovery proof over disposable, synchronized Git trees."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import archive_recovery as recovery, archive_validation as archive  # noqa: E402
from tests.test_archive_recovery import GitFixture  # noqa: E402


class GenericMigrationRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="generic-migration-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git = GitFixture(self.root)
        registry_path = Path("docs/99.templates/registry.json")
        registry = json.loads((ROOT / registry_path).read_text())
        selected = {
            "sdlc/architecture-description",
            "sdlc/data-model",
            "sdlc/plan",
            "archive/tombstone",
        }
        for domain in registry["lifecycle_domains"]:
            profile_id = (
                "archive/migration"
                if "archive/migration" in domain["profile_ids"]
                else domain["profile_ids"][0]
            )
            selected.add(profile_id)
        for domain in registry["lifecycle_domains"]:
            domain["profile_ids"] = [
                profile_id
                for profile_id in domain["profile_ids"]
                if profile_id in selected
            ]
        registry["profiles"] = [
            profile for profile in registry["profiles"] if profile["id"] in selected
        ]
        (self.root / registry_path).parent.mkdir(parents=True)
        (self.root / registry_path).write_text(json.dumps(registry))
        templates = {
            profile["template_source"]
            for profile in registry["profiles"]
            if profile["template_source"] is not None
        }
        for relative in {
            "docs/99.templates/contracts/document-profile.schema.json",
            *templates,
        }:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        self.git.run("add", "--", "docs/99.templates")
        self.source = "docs/00.agent-governance/old.md"
        self.target = "docs/00.agent-governance/new.md"
        self.consumer = "docs/03.specs/0099-fixture/spec.md"
        self.payload = b"# Original policy\n"
        self.consumer_bytes = (
            b"# Completed\n\n[policy](../../00.agent-governance/old.md)\n"
        )
        self.commit, blobs = self.git.commit_many(
            {
                self.source: self.payload,
                self.consumer: self.consumer_bytes,
            }
        )
        self.row = dict(
            legacy_path=self.source,
            stable_path=None,
            artifact_id=None,
            action="merged",
            replacement=self.target,
            source_commit=self.commit,
            source_blob=blobs[self.source],
            content_sha256=hashlib.sha256(self.payload).hexdigest(),
            reason="Consolidate policy responsibility",
        )
        self.path = "docs/98.archive/migrations/0005-policy-convergence.md"
        self.git.run("rm", "--quiet", "--", self.source)
        (self.root / self.target).parent.mkdir(parents=True, exist_ok=True)
        (self.root / self.target).write_bytes(b"# Current policy\n")
        self.git.run("add", "--", self.target)
        self.write()

    def write(self, rows=None, consumers=None, references=None, *, path=None):
        rows = [self.row] if rows is None else rows
        consumers = (
            [{"source_commit": self.commit, "paths": [self.consumer]}]
            if consumers is None
            else consumers
        )
        data = (
            "---\n"
            'title: "MIG-0005: Policy convergence"\n'
            'version: "1.0.0"\n'
            'type: "archive/migration"\nstatus: "sealed"\n'
            'owner: "platform"\nupdated: "2026-08-28"\nlayer: "archive"\n'
            'artifact_id: "MIG-0005"\n---\n\n'
            "# MIG-0005: Policy convergence\n\n## Overview\n\nReviewed policy cutover.\n\n"
            "## Migration Ledger\n\n<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
            + json.dumps(rows, indent=2)
            + "\n```\n\n## Recovery\n\n"
            "<!-- archive-historical-consumers:v1 format=json -->\n\n```json\n"
            + json.dumps(consumers, indent=2)
            + "\n```\n"
        ).encode()
        if references is not None:
            data += (
                b"\n<!-- archive-historical-reference-evidence:v1 format=json -->\n\n```json\n"
                + json.dumps(references, indent=2).encode()
                + b"\n```\n"
            )
        path = self.path if path is None else path
        data = data.replace(b"MIG-0005", archive.generic_migration_id(path).encode())
        record = self.root / path
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_bytes(data)
        self.git.run("add", "--", path)
        return data

    def verify(self):
        return recovery.verify_declared_migration_record(self.root, self.path)

    def held_document_inputs(self):
        owner = archive._load_canonical_markdown_module()
        documents = sys.modules[owner.load_registry.__module__]
        registry = documents.load_registry(self.root)
        raw_registry = json.loads((self.root / documents.REGISTRY_PATH).read_bytes())
        schema = json.loads((self.root / documents.SCHEMA_PATH).read_bytes())
        templates = frozenset(
            PurePosixPath(profile["template_source"])
            for profile in raw_registry["profiles"]
            if profile["template_source"] is not None
        )
        return documents, registry, raw_registry, schema, templates

    def test_held_registry_preserves_identity_schema_semantics_without_reopens(self):
        documents, expected, raw, schema, templates = self.held_document_inputs()
        with (
            mock.patch.object(
                documents, "load_json_file", side_effect=AssertionError("JSON reopen")
            ),
            mock.patch.object(
                documents,
                "_lstat_named_path",
                side_effect=AssertionError("template reopen"),
            ),
        ):
            actual = documents.load_registry(
                self.root,
                raw_registry=raw,
                raw_schema=schema,
                template_regular_paths=templates,
            )
            self.assertEqual(actual, expected)
            changed = json.loads(json.dumps(raw))
            changed["profiles"][0]["path_pattern"] = "^(?:a+)+$"
            with (
                mock.patch.object(
                    documents,
                    "_compile_route",
                    side_effect=AssertionError("untrusted pattern compiled"),
                ),
                self.assertRaises(documents.DocumentContractError) as raised,
            ):
                documents.validate_registry(
                    self.root,
                    changed,
                    raw_schema=schema,
                    template_regular_paths=templates,
                    trusted_registry=expected,
                )
            self.assertEqual(
                {item.rule_id for item in raised.exception.diagnostics},
                {"REGISTRY_EXECUTABLE_POLICY"},
            )
            for change in ({"schema_version": 7}, {"$id": "https://invalid/registry"}):
                with (
                    self.subTest(change=change),
                    self.assertRaises(documents.DocumentContractError),
                ):
                    documents.load_registry(
                        self.root,
                        raw_registry=dict(raw, **change),
                        raw_schema=schema,
                        template_regular_paths=templates,
                    )
            for inputs in (
                {"raw_registry": raw},
                {"raw_schema": schema},
                {
                    "raw_registry": None,
                    "raw_schema": schema,
                    "template_regular_paths": templates,
                },
                {
                    "raw_registry": raw,
                    "raw_schema": None,
                    "template_regular_paths": templates,
                },
                {"raw_registry": raw, "raw_schema": schema},
                {
                    "raw_registry": raw,
                    "raw_schema": schema,
                    "template_regular_paths": frozenset(),
                },
                {
                    "raw_registry": raw,
                    "raw_schema": {"$ref": "https://invalid/schema"},
                    "template_regular_paths": templates,
                },
            ):
                with (
                    self.subTest(keys=tuple(inputs)),
                    self.assertRaises(documents.DocumentContractError),
                ):
                    documents.load_registry(self.root, **inputs)

    def test_held_generic_proof_preserves_inputs_without_default_reopens(self):
        documents, registry, _raw, schema, _templates = self.held_document_inputs()
        default_reader = archive.read_worktree_regular_bounded
        reads = []

        def read_current_bytes(path, max_bytes):
            reads.append((path, max_bytes))
            return default_reader(self.root, path, max_bytes=max_bytes)

        with (
            mock.patch.object(
                documents,
                "load_registry",
                side_effect=AssertionError("registry reopen"),
            ),
            mock.patch.object(
                documents, "load_json_file", side_effect=AssertionError("schema reopen")
            ),
            mock.patch.object(
                archive,
                "read_worktree_regular_bounded",
                side_effect=AssertionError("current reopen"),
            ),
        ):
            proof = archive.repository_migration_proof(
                self.root,
                registry=registry,
                raw_schema=schema,
                read_current_bytes=read_current_bytes,
            )
        self.assertEqual(proof.targets[self.source], self.target)
        self.assertEqual(proof.consumers[self.consumer], self.consumer_bytes)
        paths = [path for path, _limit in reads]
        self.assertGreaterEqual(paths.count(self.path), 3)
        self.assertIn(str(documents.REGISTRY_PATH), paths)
        self.assertIn(self.target, paths)
        self.assertNotIn(self.consumer, paths)
        self.assertTrue(
            all(limit <= archive.CURRENT_MARKDOWN_MAX_BYTES for _, limit in reads)
        )

    def test_held_generic_proof_rejects_partial_invalid_and_oversized_inputs(self):
        _documents, registry, _raw, schema, _templates = self.held_document_inputs()
        for inputs in (
            {"registry": registry},
            {"raw_schema": schema},
            {"registry": registry, "read_current_bytes": lambda *_args: b""},
            {
                "registry": registry,
                "raw_schema": None,
                "read_current_bytes": lambda *_args: b"",
            },
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda *_args: None,
            },
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda _path, limit: b" " * (limit + 1),
            },
        ):
            with (
                self.subTest(keys=tuple(inputs)),
                self.assertRaises(archive.ArchiveContractError),
            ):
                archive.repository_migration_proof(self.root, **inputs)

    def test_held_generic_proof_keeps_current_parity_and_final_record_recheck(self):
        documents, registry, _raw, schema, _templates = self.held_document_inputs()

        def prove(reader):
            return archive.repository_migration_proof(
                self.root,
                registry=registry,
                raw_schema=schema,
                read_current_bytes=reader,
            )

        for changed_path, changed_read in (
            (self.path, 2),
            (self.path, 3),
            (documents.REGISTRY_PATH.as_posix(), 1),
            (self.target, 1),
        ):
            counts = {}

            def read_current_bytes(path, max_bytes):
                content = archive.read_worktree_regular_bounded(
                    self.root, path, max_bytes=max_bytes
                )
                counts[path] = counts.get(path, 0) + 1
                return (
                    content + b"\n"
                    if path == changed_path and counts[path] == changed_read
                    else content
                )

            with (
                self.subTest(path=changed_path, read=changed_read),
                self.assertRaises(archive.ArchiveContractError) as raised,
            ):
                prove(read_current_bytes)
            self.assertEqual(raised.exception.code, "ARCHIVE-MIGRATION-STAGED-DRIFT")

    def test_public_main_rejects_nonstring_actions_without_traceback(self):
        for action in ([], {}):
            self.write([dict(self.row, action=action)])
            output = io.StringIO()
            with (
                self.subTest(action=action),
                redirect_stdout(output),
                redirect_stderr(output),
            ):
                result = recovery.main(
                    ["--root", str(self.root), "--record", self.path, "--verify"]
                )
                self.assertEqual(result, 1)
                self.assertEqual(
                    output.getvalue(),
                    "FAIL archive recovery code=RECOVERY-MIGRATION-ROW\n",
                )

    def test_stage99_schema_failures_are_offline_typed_and_redacted(self):
        owner = archive._load_canonical_markdown_module()
        contracts = sys.modules[owner.load_registry.__module__]
        load_json = contracts.load_json_file
        registry = load_json(self.root / contracts.REGISTRY_PATH)
        sentinel = "synthetic-schema-resource-sentinel"
        cases = (
            {"$ref": "#/$defs/" + sentinel},
            {"$ref": "https://schema.invalid/" + sentinel},
            {"$ref": "file:///" + sentinel + ".json"},
            {"type": sentinel},
        )
        transports = (
            "requests.get",
            "urllib.request.urlopen",
            "jsonschema.validators.urlopen",
            "urllib.request.OpenerDirector.open",
            "socket.socket",
            "socket.getaddrinfo",
        )
        for schema in cases:

            def loaded(path, **kwargs):
                if path == self.root / contracts.PROFILE_SCHEMA_PATH:
                    return schema
                return load_json(path, **kwargs)

            with self.subTest(schema=schema), ExitStack() as stack:
                blockers = [
                    stack.enter_context(
                        mock.patch(
                            name, side_effect=RuntimeError("resource fetch forbidden")
                        )
                    )
                    for name in transports
                ]
                stack.enter_context(
                    mock.patch.object(contracts, "load_json_file", side_effect=loaded)
                )
                output = io.StringIO()
                with (
                    self.subTest(caller="recovery.main"),
                    redirect_stdout(output),
                    redirect_stderr(output),
                ):
                    result = recovery.main(
                        ["--root", str(self.root), "--record", self.path, "--verify"]
                    )
                    self.assertEqual(result, 1)
                    self.assertEqual(
                        output.getvalue(),
                        "FAIL archive recovery code=ARCHIVE-MIGRATION-PROFILE\n",
                    )
                for call in (
                    lambda: contracts.load_registry(self.root),
                    lambda: contracts.validate_registry(self.root, registry),
                ):
                    with self.subTest(caller=call):
                        with self.assertRaises(
                            contracts.DocumentContractError
                        ) as raised:
                            call()
                        self.assertEqual(
                            {item.rule_id for item in raised.exception.diagnostics},
                            {"REGISTRY_SCHEMA"},
                        )
                        self.assertNotIn(sentinel, repr(raised.exception.diagnostics))
                for blocker in blockers:
                    blocker.assert_not_called()

    def test_stage99_embedded_schema_refs_remain_supported(self):
        owner = archive._load_canonical_markdown_module()
        contracts = sys.modules[owner.load_registry.__module__]
        load_json = contracts.load_json_file
        schema = {"$ref": "#/$defs/object", "$defs": {"object": {"type": "object"}}}

        def loaded(path, **kwargs):
            if path == self.root / contracts.PROFILE_SCHEMA_PATH:
                return schema
            return load_json(path, **kwargs)

        with mock.patch.object(contracts, "load_json_file", side_effect=loaded):
            self.assertTrue(contracts.load_registry(self.root).profiles)
            self.assertEqual(self.verify(), "MIG-0005")

    def chain(self, middle_bytes, *, action="moved"):
        middle = "docs/00.agent-governance/middle.md"
        commit, blobs = self.git.commit_many({middle: middle_bytes})
        self.git.run("rm", "--quiet", "--", middle)
        (self.root / self.target).write_bytes(
            middle_bytes if action == "moved" else b"# Consolidated policy\n"
        )
        self.git.run("add", "--", self.target)
        first = dict(self.row, action="moved", stable_path=middle, replacement=None)
        second = dict(
            self.row,
            legacy_path=middle,
            source_commit=commit,
            source_blob=blobs[middle],
            content_sha256=hashlib.sha256(middle_bytes).hexdigest(),
            action=action,
            stable_path=self.target if action == "moved" else None,
            replacement=None if action == "moved" else self.target,
        )
        return first, second

    def test_every_moved_edge_is_proven_before_composition(self):
        for action in ("moved", "merged"):
            with self.subTest(action=action):
                rows = self.chain(b"# Different intermediate bytes\n", action=action)
                self.write(list(rows))
                with self.assertRaisesRegex(recovery.ArchiveContractError, "TARGET"):
                    self.verify()
        rows = self.chain(self.payload)
        self.write(list(rows))
        self.assertEqual(self.verify(), "MIG-0005")

    def test_sealed_move_target_can_evolve_after_historical_proof(self):
        moved = dict(
            self.row,
            action="moved",
            stable_path=self.target,
            replacement=None,
        )
        (self.root / self.target).write_bytes(self.payload)
        self.git.run("add", "--", self.target)
        self.write([moved])
        self.git.run("commit", "--quiet", "-m", "seal byte-identical move")

        (self.root / self.target).write_bytes(self.payload + b"Later metadata.\n")
        self.git.run("add", "--", self.target)

        proof = archive.repository_migration_proof(self.root)
        self.assertEqual(proof.targets[self.source], self.target)

    def test_sealed_move_cannot_be_repaired_only_in_the_current_target(self):
        moved = dict(
            self.row,
            action="moved",
            stable_path=self.target,
            replacement=None,
        )
        self.write([moved])
        self.git.run("commit", "--quiet", "-m", "seal non-identical move")

        (self.root / self.target).write_bytes(self.payload)
        self.git.run("add", "--", self.target)

        with self.assertRaisesRegex(recovery.ArchiveContractError, "TARGET"):
            archive.repository_migration_proof(self.root)

    def test_draft_migration_is_inert_until_it_is_sealed(self):
        # document_lifecycle admits a migration only in draft, so every
        # migration exists as a draft before it is sealed.  A draft is not yet
        # evidence: it must contribute no target rather than break the proof
        # for the whole repository, or no migration can ever be opened in a
        # green commit.
        self.write()
        draft_path = "docs/98.archive/migrations/0006-next-policy-convergence.md"
        draft_source = "docs/00.agent-governance/policies/draft-only.md"
        row = dict(self.row, legacy_path=draft_source)
        data = self.write([row], consumers=[], path=draft_path)
        record = self.root / draft_path
        record.write_bytes(data.replace(b'status: "sealed"', b'status: "draft"'))
        self.git.run("add", "--", draft_path)

        proof = archive.repository_migration_proof(self.root)

        self.assertEqual(proof.targets[self.source], self.target)
        self.assertNotIn(draft_source, proof.targets)

    def test_a_sealed_row_releases_a_registered_consumer_from_the_tree(self):
        # A historical consumer proves that a retired path's disposition was
        # reviewed in a real document at a real commit.  The proof reads that
        # document's bytes from Git, so it still holds once the consumer is
        # itself retired by a later sealed row.  Requiring the current tree to
        # keep those bytes freezes the present without proving more about the
        # past, and a sealed row carrying source commit, blob and digest is the
        # stronger record of the two.
        self.write()
        retirement = "docs/98.archive/migrations/0006-consumer-retirement.md"
        blob = (
            self.git.run("rev-parse", f"{self.commit}:{self.consumer}")
            .decode("ascii")
            .strip()
        )
        row = dict(
            self.row,
            legacy_path=self.consumer,
            replacement=None,
            action="deleted",
            source_blob=blob,
            content_sha256=hashlib.sha256(self.consumer_bytes).hexdigest(),
            reason="Retire the reviewed consumer; Git retains its exact source.",
        )
        # A deleted row points its edge at the Archive index, which this
        # fixture otherwise never needs.
        index = self.root / "docs/98.archive/README.md"
        index.write_bytes(b"# Archive\n")
        self.git.run("add", "--", "docs/98.archive/README.md")
        self.write([row], consumers=[], path=retirement)
        self.git.run("rm", "--quiet", "--", self.consumer)

        proof = archive.repository_migration_proof(self.root)

        self.assertEqual(proof.consumers[self.consumer], self.consumer_bytes)
        self.assertEqual(proof.targets[self.source], self.target)

    def test_current_consumer_can_evolve_after_historical_proof(self):
        # Archive proves the reviewed consumer bytes from Git. Current document
        # evolution is governed by active validators, not by a historical record.
        self.write()
        (self.root / self.consumer).write_bytes(self.consumer_bytes + b"\n# later\n")
        self.git.run("add", "--", self.consumer)

        proof = archive.repository_migration_proof(self.root)

        self.assertEqual(proof.consumers[self.consumer], self.consumer_bytes)

    def test_cli_uses_validated_successor_records(self):
        first, second = self.chain(self.payload, action="merged")
        first_bytes = self.write([first])
        next_path = "docs/98.archive/migrations/0006-next-policy-convergence.md"
        self.write([second], consumers=[], path=next_path)
        proof = archive.repository_migration_proof(self.root)
        self.assertEqual(proof.targets[self.source], self.target)
        self.assertEqual(self.verify(), "MIG-0005")
        self.assertEqual(
            recovery.verify_declared_migration_record(self.root, next_path), "MIG-0006"
        )
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/archive_recovery.py"),
                "--root",
                str(self.root),
                "--record",
                self.path,
                "--verify",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with self.assertRaisesRegex(recovery.ArchiveContractError, "STAGED-DRIFT"):
            archive.repository_migration_proof(
                self.root, requested_record=(self.path, first_bytes + b"changed\n")
            )
        self.write(
            [dict(second, content_sha256="0" * 64)], consumers=[], path=next_path
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "CONTENT"):
            self.verify()
        self.write([second], consumers=[], path=next_path)
        (self.root / self.path).write_bytes(first_bytes + b"changed\n")
        with self.assertRaises(recovery.ArchiveContractError):
            self.verify()

    def test_public_discovery_has_entry_record_and_byte_bounds(self):
        for limit in (
            "_GIT_TREE_ENTRY_LIMIT",
            "MAX_GIT_BATCH_OBJECTS",
            "MAX_GIT_BATCH_BYTES",
        ):
            with self.subTest(limit=limit), mock.patch.object(archive, limit, 0):
                with self.assertRaisesRegex(
                    recovery.ArchiveContractError, "RESOURCE-LIMIT"
                ):
                    self.verify()

    def test_public_recovery_delegates_document_form_to_stage99(self):
        valid = self.write()
        for extra in (
            b"\n## Unsupported policy\n",
            b"\n## Recovery\n",
            b"\n```unclosed\n",
        ):
            (self.root / self.path).write_bytes(valid + extra)
            self.git.run("add", "--", self.path)
            with (
                self.subTest(extra=extra),
                self.assertRaisesRegex(recovery.ArchiveContractError, "PROFILE"),
            ):
                self.verify()
        changed = valid.replace(
            b'title: "MIG-0005: Policy convergence"', b"title: 'Policy recovery'"
        )
        (self.root / self.path).write_bytes(changed)
        self.git.run("add", "--", self.path)
        self.assertEqual(self.verify(), "MIG-0005")

    def test_public_cli_rejects_record_and_target_fifos_promptly(self):
        for relative in (self.path, self.target):
            path = self.root / relative
            content = path.read_bytes()
            path.unlink()
            os.mkfifo(path)
            try:
                with self.subTest(path=relative):
                    try:
                        result = subprocess.run(
                            [
                                sys.executable,
                                str(ROOT / "scripts/archive_recovery.py"),
                                "--root",
                                str(self.root),
                                "--record",
                                self.path,
                                "--verify",
                            ],
                            capture_output=True,
                            text=True,
                            timeout=3,
                        )
                    except subprocess.TimeoutExpired:
                        self.fail("public recovery blocked on a nonregular FIFO")
                    self.assertEqual(
                        result.returncode, 1, result.stdout + result.stderr
                    )
                    code = (
                        "RECOVERY-RECORD-READ"
                        if relative == self.path
                        else "RECOVERY-MIGRATION-TARGET"
                    )
                    self.assertEqual(
                        result.stdout, f"FAIL archive recovery code={code}\n"
                    )
            finally:
                path.unlink()
                path.write_bytes(content)

    def test_public_cli_does_not_reopen_a_historical_consumer_fifo(self):
        path = self.root / self.consumer
        content = path.read_bytes()
        path.unlink()
        os.mkfifo(path)
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/archive_recovery.py"),
                    "--root",
                    str(self.root),
                    "--record",
                    self.path,
                    "--verify",
                ],
                capture_output=True,
                text=True,
                timeout=3,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(
                result.stdout,
                "PASS archive recovery operation=verify migration=MIG-0005\n",
            )
        finally:
            path.unlink()
            path.write_bytes(content)

    def test_future_migration_public_cli_and_exact_consumers(self):
        self.assertEqual(self.verify(), "MIG-0005")
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/archive_recovery.py"),
                "--root",
                str(self.root),
                "--record",
                self.path,
                "--verify",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        proof = archive.validate_migration_records(
            self.root, {self.path: (self.root / self.path).read_bytes()}
        )
        self.assertEqual(proof.targets, {self.source: self.target})
        self.assertEqual(proof.consumers, {self.consumer: self.consumer_bytes})

    def test_accepts_a_target_retired_after_reachable_history_proved_it(self):
        self.git.run("commit", "--quiet", "-m", "seal migration target")
        self.git.run("rm", "--quiet", "--", self.target)

        self.assertEqual(self.verify(), "MIG-0005")
        proof = archive.validate_migration_records(
            self.root, {self.path: (self.root / self.path).read_bytes()}
        )
        self.assertEqual(proof.targets, {self.source: self.target})

    def test_later_numbered_profile_is_not_a_per_migration_allowlist(self):
        from scripts.document_contracts import classify_path, load_registry

        future = "docs/98.archive/migrations/0123-future-convergence.md"
        self.assertEqual(
            classify_path(load_registry(ROOT), PurePosixPath(future)).profile_id,
            "archive/migration",
        )
        content = self.write().replace(b"MIG-0005", b"MIG-0123")
        archive.parse_migration_control(future, content)
        with self.assertRaises(recovery.ArchiveContractError):
            archive.parse_migration_control(future, self.write())

    def test_public_link_diagnostics_do_not_admit_an_unregistered_done_consumer(self):
        links = archive._load_canonical_link_module()
        consumer = PurePosixPath(self.consumer)
        unregistered = consumer.with_name("plan.md")
        (self.root / unregistered).write_bytes(self.consumer_bytes)
        self.git.run("add", "--", str(unregistered))
        context = types.SimpleNamespace(
            root=self.root,
            paths=(consumer, unregistered),
            texts={
                consumer: self.consumer_bytes.decode(),
                unregistered: self.consumer_bytes.decode(),
            },
            profiles={
                path: types.SimpleNamespace(profile_id="sdlc/spec", mode="authored")
                for path in (consumer, unregistered)
            },
            metadata={path: {"status": "done"} for path in (consumer, unregistered)},
            tracked_regular_paths=frozenset(
                {consumer, unregistered, PurePosixPath(self.target)}
            ),
            adapter_targets={},
            route_state="terminal",
        )
        # Unrelated sealed migration corpora do not exist in this disposable repo.
        # The generic migration/source/index proof and actual renderer remain real.
        with (
            mock.patch.object(
                links,
                "_document_taxonomy_transition_manifest",
                return_value=({}, {}, {}),
            ),
            mock.patch.object(
                links,
                "_work109_migration_projection",
                return_value=({}, {}, {}, frozenset()),
            ),
            mock.patch.object(links, "_work054_wp003_owner_merges", return_value={}),
            mock.patch.object(links, "_work054_wp004b_targets", return_value={}),
        ):
            diagnostics = links._link_diagnostics(context)
        self.assertEqual(
            [(item.rule_id, str(item.path)) for item in diagnostics],
            [("LINK-BROKEN", str(unregistered))],
        )

    def test_consumer_without_rendered_disposition_is_rejected(self):
        commit, _ = self.git.commit_many(
            {self.consumer: b"# Done\n\n`[policy](../../00.agent-governance/old.md)`\n"}
        )
        self.write(consumers=[{"source_commit": commit, "paths": [self.consumer]}])
        with self.assertRaisesRegex(recovery.ArchiveContractError, "CONSUMER"):
            self.verify()
        self.write()
        with mock.patch.object(archive, "_ARCHIVE_RECORD_LIMIT", 5):
            with self.assertRaisesRegex(
                recovery.ArchiveContractError, "RESOURCE-LIMIT"
            ):
                self.verify()

    def test_literal_reference_admits_only_exact_registered_consumer_occurrence(self):
        literal = "docs/00.agent-governance/old.md"
        raw = b"# Completed\n\n`docs/00.agent-governance/old.md`\n"
        commit, _ = self.git.commit_many({self.consumer: raw})
        evidence = [
            {
                "kind": "literal-path",
                "consumer_path": self.consumer,
                "legacy_path": literal,
            }
        ]
        self.write(
            consumers=[{"source_commit": commit, "paths": [self.consumer]}],
            references=evidence,
        )
        proof = archive.repository_migration_proof(self.root)
        self.assertEqual(proof.consumers[self.consumer], raw)
        self.assertEqual(
            proof.references[self.consumer, literal].terminal_path, self.target
        )
        self.write(
            consumers=[{"source_commit": commit, "paths": [self.consumer]}],
            references=[dict(evidence[0], legacy_path=literal + ".bak")],
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "REFERENCE"):
            self.verify()

    def test_literal_reference_requires_supported_whole_token_forms(self):
        literal = self.source
        evidence = {
            "kind": "literal-path",
            "consumer_path": self.consumer,
            "legacy_path": literal,
        }
        rejected = (
            literal.encode() + b",\n",
            b"`" + literal.encode() + b",`\n",
            b"`" + literal.encode() + b"`,suffix\n",
            b"`" + literal.encode() + b"`,,\n",
            b"prefix`" + literal.encode() + b"`,\n",
            b"`" + literal.encode() + b"+backup`\n",
            b"`" + literal.encode() + b":backup`\n",
            b"`" + literal.encode() + b";backup`\n",
            b"prefix=" + literal.encode() + b"\n",
            b"`" + literal.encode() + "\ud55c\uae00".encode() + b"`\n",
            b'prefix"' + literal.encode() + b'"suffix\n',
            b'"' + literal.encode() + b'":backup\n',
            b'"' + literal.encode() + b'";backup\n',
            b"`" + literal.encode() + b"'\n",
            b'prefix="' + literal.encode() + b'"\n',
        )
        for raw in rejected:
            with self.subTest(raw=raw):
                commit, _ = self.git.commit_many({self.consumer: raw})
                self.write(
                    consumers=[{"source_commit": commit, "paths": [self.consumer]}],
                    references=[evidence],
                )
                with self.assertRaisesRegex(
                    recovery.ArchiveContractError, "occurrence"
                ):
                    archive.repository_migration_proof(self.root)
        supported = (
            b"sed -n '1,2p' " + literal.encode() + b"\n",
            b"`" + literal.encode() + b"`\n",
            b'"' + literal.encode() + b'"\n',
            b"'" + literal.encode() + b"'\n",
            b"`" + literal.encode() + b"`,\n",
            b'"' + literal.encode() + b'", \n',
            b"'" + literal.encode() + b"',\t\n",
        )
        for raw in supported:
            with self.subTest(raw=raw):
                commit, _ = self.git.commit_many({self.consumer: raw})
                self.write(
                    consumers=[{"source_commit": commit, "paths": [self.consumer]}],
                    references=[evidence],
                )
                self.assertEqual(
                    archive.repository_migration_proof(self.root).consumers[
                        self.consumer
                    ],
                    raw,
                )

    def test_reference_rows_share_the_existing_aggregate_budget(self):
        evidence = {
            "kind": "literal-path",
            "consumer_path": self.consumer,
            "legacy_path": self.source,
        }
        self.write(references=[evidence] * (archive.MAX_GIT_BATCH_OBJECTS + 1))
        with self.assertRaisesRegex(recovery.ArchiveContractError, "RESOURCE-LIMIT"):
            archive.repository_migration_proof(self.root)

    def test_reference_rows_share_one_budget_across_two_valid_sized_records(self):
        evidence = {
            "kind": "literal-path",
            "consumer_path": self.consumer,
            "legacy_path": self.source,
        }
        self.write(references=[evidence] * archive.MAX_GIT_BATCH_OBJECTS)
        self.write(
            references=[evidence] * archive.MAX_GIT_BATCH_OBJECTS,
            consumers=[],
            path="docs/98.archive/migrations/0006-policy-convergence.md",
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "RESOURCE-LIMIT"):
            archive.repository_migration_proof(self.root)

    def test_real_mig0003_bridge_composes_to_the_generic_terminal(self):
        bridge = archive._pinned_mig0003_targets(
            ROOT, proposed_commit=None, read_current_bytes=None
        )
        self.assertEqual(
            archive.compose_migration_targets(
                (
                    bridge,
                    {
                        "docs/00.agent-governance/harness-catalog.md": ".agents/registry.json"
                    },
                )
            )["docs/00.agent-governance/harness-implementation-map.md"],
            ".agents/registry.json",
        )

    def test_held_mig0003_bridge_uses_the_supplied_current_reader(self):
        path = archive._WORK054_WP003_MIGRATION_PATH
        expected = archive.read_worktree_regular_bounded(
            ROOT, path, max_bytes=archive.MIGRATION_DOCUMENT_MAX_BYTES
        )
        reads = []

        def reader(actual_path, max_bytes):
            reads.append((actual_path, max_bytes))
            self.assertEqual(actual_path, path)
            self.assertEqual(max_bytes, archive.MIGRATION_DOCUMENT_MAX_BYTES)
            return expected

        with mock.patch.object(
            archive,
            "read_worktree_regular_bounded",
            side_effect=AssertionError("default reader reopened MIG-0003"),
        ):
            bridge = archive._pinned_mig0003_targets(
                ROOT, proposed_commit=None, read_current_bytes=reader
            )
        self.assertIn("docs/00.agent-governance/harness-implementation-map.md", bridge)
        self.assertEqual(reads, [(path, archive.MIGRATION_DOCUMENT_MAX_BYTES)])

    def test_unknown_reference_marker_is_not_an_absent_evidence_block(self):
        evidence = {
            "kind": "literal-path",
            "consumer_path": self.consumer,
            "legacy_path": self.source,
        }
        for references in (None, [evidence]):
            with self.subTest(references=references):
                raw = self.write(references=references)
                changed = raw + archive._HISTORICAL_REFERENCE_PREFIX.replace(
                    b"v1", b"v2"
                )
                changed += b"[]\n```\n"
                (self.root / self.path).write_bytes(changed)
                self.git.run("add", "--", self.path)
                with self.assertRaisesRegex(recovery.ArchiveContractError, "REFERENCE"):
                    archive.repository_migration_proof(self.root)

    def test_literal_pinned_terminal_is_a_current_regular_target(self):
        legacy = "docs/00.agent-governance/old-mig3.md"
        raw = ("# Done\n\n`" + legacy + "`\n").encode()
        commit, _ = self.git.commit_many({self.consumer: raw})
        self.write(
            consumers=[{"source_commit": commit, "paths": [self.consumer]}],
            references=[
                {
                    "kind": "literal-path",
                    "consumer_path": self.consumer,
                    "legacy_path": legacy,
                }
            ],
        )
        with (
            mock.patch.object(
                archive,
                "_pinned_mig0003_targets",
                return_value={legacy: "docs/00.agent-governance/missing.md"},
            ),
            self.assertRaisesRegex(recovery.ArchiveContractError, "TARGET"),
        ):
            archive.repository_migration_proof(self.root)

    def test_symlink_view_is_consumer_scoped_and_kept_out_of_recovery_targets(self):
        view = ".claude/workflows"
        extra_view = ".codex/workflows"
        target = "../.agents/workflows"
        raw = b"# Completed\n\n[workflows](../../../.claude/workflows)\n"
        second_consumer = "docs/03.specs/0100-fixture/spec.md"
        consumer = self.root / self.consumer
        consumer.write_bytes(raw)
        second = self.root / second_consumer
        second.parent.mkdir(parents=True, exist_ok=True)
        second.write_bytes(raw)
        link = self.root / view
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(target)
        extra_link = self.root / extra_view
        extra_link.parent.mkdir(parents=True, exist_ok=True)
        extra_link.symlink_to(target)
        self.git.run("add", "--", self.consumer, second_consumer, view, extra_view)
        self.git.run("commit", "--quiet", "-m", "historical view")
        other_commit = self.git.run("rev-parse", "HEAD").decode().strip()
        self.git.run("commit", "--allow-empty", "--quiet", "-m", "view identity")
        commit = self.git.run("rev-parse", "HEAD").decode().strip()
        blob = self.git.run("rev-parse", f"HEAD:{view}").decode().strip()
        extra_blob = self.git.run("rev-parse", f"HEAD:{extra_view}").decode().strip()
        link.unlink()
        extra_link.unlink()
        lookup = self.root / archive.ARCHIVE_INDEX
        lookup.parent.mkdir(parents=True, exist_ok=True)
        lookup.write_text("# Archive\n")
        self.git.run("add", "--", archive.ARCHIVE_INDEX.as_posix())
        references = [
            {
                "kind": "symlink-view",
                "consumer_path": self.consumer,
                "legacy_path": view,
                "source_commit": commit,
                "source_mode": "120000",
                "source_blob": blob,
                "link_target": target,
                "lookup_path": archive.ARCHIVE_INDEX.as_posix(),
            }
        ]
        references.append(dict(references[0], consumer_path=second_consumer))
        self.write(
            consumers=[
                {"source_commit": commit, "paths": [self.consumer, second_consumer]}
            ],
            references=references,
        )
        with self.assertRaisesRegex(
            recovery.ArchiveContractError,
            "view remains|stage-zero inventory is malformed",
        ):
            archive.repository_migration_proof(self.root)
        self.git.run("rm", "--cached", "--quiet", "--", view)
        proof = archive.repository_migration_proof(self.root)
        self.assertEqual(
            proof.references[self.consumer, view].terminal_path,
            archive.ARCHIVE_INDEX.as_posix(),
        )
        self.assertNotIn(view, proof.targets)
        self.assertEqual(
            proof.references[second_consumer, view].terminal_path,
            archive.ARCHIVE_INDEX.as_posix(),
        )
        self.git.run("rm", "--cached", "--quiet", "--", extra_view)
        conflicting = dict(references[1], source_commit=other_commit)
        self.write(
            consumers=[
                {"source_commit": commit, "paths": [self.consumer, second_consumer]}
            ],
            references=[references[0], conflicting],
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "REFERENCE"):
            archive.repository_migration_proof(self.root)
        self.write(
            consumers=[
                {"source_commit": commit, "paths": [self.consumer, second_consumer]}
            ],
            references=[references[0], references[0]],
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "REFERENCE"):
            archive.repository_migration_proof(self.root)
        for mutation in (
            {"source_mode": "100644"},
            {"source_blob": "0" * 40},
            {"link_target": "../../escape"},
            {"legacy_path": self.source},
        ):
            with self.subTest(mutation=mutation):
                self.write(
                    consumers=[
                        {
                            "source_commit": commit,
                            "paths": [self.consumer, second_consumer],
                        }
                    ],
                    references=[dict(references[0], **mutation)],
                )
                with self.assertRaisesRegex(recovery.ArchiveContractError, "REFERENCE"):
                    archive.repository_migration_proof(self.root)
        self.write(
            consumers=[
                {"source_commit": commit, "paths": [self.consumer, second_consumer]}
            ],
            references=[
                *references,
                dict(
                    references[0],
                    legacy_path=extra_view,
                    source_blob=extra_blob,
                ),
            ],
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "occurrence"):
            archive.repository_migration_proof(self.root)

    def test_rejects_invalid_duplicate_rows_and_missing_targets(self):
        cases = [
            [self.row, self.row],
            [dict(self.row, action="unknown")],
            [dict(self.row, replacement="../escape.md")],
            [dict(self.row, replacement="missing.md")],
            [dict(self.row, content_sha256="0" * 64)],
            [dict(self.row, source_blob="0" * 40)],
            [dict(self.row, legacy_path="absent.md")],
            [dict(self.row, source_commit=self.row["source_blob"])],
        ]
        for rows in cases:
            with (
                self.subTest(rows=rows),
                self.assertRaises(recovery.ArchiveContractError),
            ):
                self.write(rows)
                self.verify()

    def test_rejects_source_symlink_and_tree(self):
        (self.root / "link.md").symlink_to(self.target)
        self.git.run("add", "--", "link.md")
        self.git.run("commit", "--quiet", "-m", "fixture link")
        commit = self.git.run("rev-parse", "HEAD").decode().strip()
        blob = self.git.run("rev-parse", "HEAD:link.md").decode().strip()
        for path, oid in [
            ("link.md", blob),
            ("docs", self.git.run("rev-parse", "HEAD:docs").decode().strip()),
        ]:
            self.write(
                [
                    dict(
                        self.row,
                        legacy_path=path,
                        source_commit=commit,
                        source_blob=oid,
                    )
                ]
            )
            with (
                self.subTest(path=path),
                self.assertRaises(recovery.ArchiveContractError),
            ):
                self.verify()

    def test_rejects_unreachable_source(self):
        tree = self.git.run("rev-parse", "HEAD^{tree}").decode().strip()
        orphan = (
            self.git.run("commit-tree", tree, input_bytes=b"unreachable\n")
            .decode()
            .strip()
        )
        self.write([dict(self.row, source_commit=orphan)])
        with self.assertRaisesRegex(recovery.ArchiveContractError, "UNREACHABLE"):
            self.verify()

    def test_rejects_record_and_target_drift_but_not_current_consumer_change(self):
        for path in [self.path, self.target]:
            saved = (self.root / path).read_bytes()
            (self.root / path).write_bytes(saved + b"changed\n")
            with (
                self.subTest(path=path),
                self.assertRaises(recovery.ArchiveContractError),
            ):
                self.verify()
            (self.root / path).write_bytes(saved)
        (self.root / self.consumer).write_bytes(self.consumer_bytes + b"changed\n")
        self.git.run("add", "--", self.consumer)
        proof = archive.repository_migration_proof(self.root)
        self.assertEqual(proof.consumers[self.consumer], self.consumer_bytes)

    def test_rejects_duplicate_consumers_utf8_and_read_bounds(self):
        self.write(
            consumers=[
                {"source_commit": self.commit, "paths": [self.consumer, self.consumer]}
            ]
        )
        with self.assertRaises(recovery.ArchiveContractError):
            self.verify()
        self.write()
        with mock.patch.object(archive, "MIGRATION_DOCUMENT_MAX_BYTES", 20):
            with self.assertRaises(recovery.ArchiveContractError):
                self.verify()
        commit, blobs = self.git.commit_many({"binary.md": b"\xff"})
        self.write(
            [
                dict(
                    self.row,
                    legacy_path="binary.md",
                    source_commit=commit,
                    source_blob=blobs["binary.md"],
                    content_sha256=hashlib.sha256(b"\xff").hexdigest(),
                )
            ]
        )
        with self.assertRaisesRegex(recovery.ArchiveContractError, "UTF8"):
            self.verify()

    def test_composition_rejects_cycles_and_conflicts(self):
        self.assertEqual(
            archive.compose_migration_targets(({"a": "b"}, {"b": "c"})),
            {"a": "c", "b": "c"},
        )
        for maps in [({"a": "b"}, {"b": "a"}), ({"a": "b"}, {"a": "c"})]:
            with self.assertRaises(recovery.ArchiveContractError):
                archive.compose_migration_targets(maps)

    def test_composition_stops_where_a_later_ledger_reoccupied_the_path(self):
        # A row retires the document that held a path, not the path. When a
        # later ledger moves a different document onto that path, the earlier
        # occupant's departure belongs to the previous generation and is not
        # part of the new arrival's chain. Following it closes a false cycle:
        # a -> b, b -> c, and c -> a where c was reoccupied by the b -> c move.
        loop = ({"a": "b"}, {"b": "c"}, {"c": "a"})
        with self.assertRaises(recovery.ArchiveContractError):
            archive.compose_migration_targets(loop)
        self.assertEqual(
            archive.compose_migration_targets(loop, reoccupied={"c"}),
            {"a": "c", "b": "c", "c": "c"},
        )

    def test_composition_reoccupation_names_no_path_by_default(self):
        # The admission is opt-in: a caller that cannot say which paths were
        # reoccupied still gets the strict walk.
        self.assertEqual(
            archive.compose_migration_targets(({"a": "b"}, {"b": "c"}), reoccupied=()),
            {"a": "c", "b": "c"},
        )

    def test_mig4_sealed_target_is_independent_of_current_template_bytes(self):
        rows = archive.parse_pinned_migration_control(
            recovery.WP004B_PINNED_MIGRATION_PATH,
            (ROOT / recovery.WP004B_PINNED_MIGRATION_PATH).read_bytes(),
        )
        archive.validate_mig0004_historical_targets(ROOT, rows)
        changed = [dict(row) for row in rows]
        next(
            row
            for row in changed
            if row["action"] == "moved"
            and str(row["legacy_path"]).startswith("docs/99.templates/")
        )["content_sha256"] = "0" * 64
        with self.assertRaisesRegex(recovery.ArchiveContractError, "TARGET"):
            archive.validate_mig0004_historical_targets(ROOT, tuple(changed))
        with mock.patch.object(archive, "WP004C_SEALED_TARGET_COMMIT", self.commit):
            with self.assertRaises(recovery.ArchiveContractError):
                archive.validate_mig0004_historical_targets(ROOT, rows)


if __name__ == "__main__":
    unittest.main()
