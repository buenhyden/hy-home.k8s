"""Public historical-consumer proof over minimal, real temporary Git history."""

from __future__ import annotations

import types
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

from tests.test_validate_agent_legacy_cutover import load_validator

_original_sys_path = sys.path
try:
    sys.path = list(_original_sys_path)
    from tests import test_generic_migration_recovery as fixtures
finally:
    sys.path = _original_sys_path


class HistoricalProofImportTest(unittest.TestCase):
    def test_fresh_import_preserves_sys_path_identity_values_and_discovery(self):
        script = """
import builtins
import importlib
import sys
import unittest
sys.path.insert(0, sys.argv[1])
original = sys.path
before = list(original)
normal_import = builtins.__import__
def fail_fixture_import(name, *args, **kwargs):
    fromlist = args[2] if len(args) > 2 else kwargs.get("fromlist", ())
    if name == "tests" and "test_generic_migration_recovery" in (fromlist or ()):
        sys.path.append("fixture-import-marker")
        raise ImportError("expected fixture import failure")
    return normal_import(name, *args, **kwargs)
if sys.argv[2] == "failure":
    builtins.__import__ = fail_fixture_import
try:
    module = importlib.import_module("tests.test_archive_historical_proof")
except ImportError as error:
    assert sys.argv[2] == "failure" and str(error) == "expected fixture import failure"
else:
    assert sys.argv[2] == "success"
    exported_tests = [value for value in vars(module).values()
                      if isinstance(value, type) and issubclass(value, unittest.TestCase)]
    assert exported_tests and all(value.__module__ == module.__name__ for value in exported_tests)
finally:
    builtins.__import__ = normal_import
assert sys.path is original, "sys.path object replaced"
assert sys.path == before, "sys.path values leaked"
print("PASS")
"""
        for mode in ("success", "failure"):
            with self.subTest(mode=mode):
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        "-I",
                        "-c",
                        script,
                        str(fixtures.ROOT),
                        mode,
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stdout, "PASS\n")


class HistoricalMigrationProofTest(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.GenericMigrationRecoveryTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.fixture = fixture
        self.links = fixtures.archive._load_canonical_link_module()
        self.build_context = self.links._build_context
        self.root = fixture.root
        self.consumer = PurePosixPath(fixture.consumer)
        self.context = types.SimpleNamespace(
            root=self.root,
            paths=(self.consumer,),
            texts={self.consumer: fixture.consumer_bytes.decode()},
            metadata={self.consumer: {"status": "done"}},
            profiles={self.consumer: types.SimpleNamespace(profile_id="sdlc/spec")},
            tracked_regular_paths=frozenset(
                {self.consumer, PurePosixPath(fixture.target)}
            ),
            adapter_targets={},
            route_state="terminal",
            ria_contract_text=None,
        )
        # These old sealed corpora do not exist in this minimal repository.
        # Generic records, source objects, staged parity and renderer are real.
        for name, value in (
            ("_build_context", self.context),
            ("_document_taxonomy_transition_manifest", ({}, {}, set())),
            ("_work109_migration_projection", ({}, {}, {})),
            ("_work054_wp003_owner_merges", {}),
            ("_work054_wp004b_targets", {}),
            ("_work107_stable_archive_aliases", {}),
        ):
            self.enterContext(mock.patch.object(self.links, name, return_value=value))

    def proof(self):
        return self.links.repository_historical_migration_proof(self.root)

    def legacy_declaration_fixture(self):
        legacy = load_validator()
        sources = {path: b"Retired source\n" for path in legacy.RETIRED_TOKENS}
        commit, blobs = self.fixture.git.commit_many(sources)
        rows = [self.fixture.row]
        for path, raw in sources.items():
            self.fixture.git.run("rm", "--quiet", "--", path)
            rows.append(
                dict(
                    legacy_path=path,
                    stable_path=None,
                    artifact_id=None,
                    action="merged",
                    replacement=self.fixture.target,
                    source_commit=commit,
                    source_blob=blobs[path],
                    content_sha256=hashlib.sha256(raw).hexdigest(),
                    reason="Move responsibility to the current owner",
                )
            )
        self.fixture.write(rows)
        return legacy, rows

    def validate_legacy_with_public_proof(self, legacy):
        proof = self.proof()
        owners = types.SimpleNamespace(
            document_registry=proof.document_registry,
            proof=proof,
            native_paths=frozenset(),
            enforcement_paths=frozenset(),
            helper_roles={},
            retention=None,
        )
        # Only unrelated current native/helper owner fixtures are omitted.
        # Actual generic Git proof, public historical adapter and scanner run.
        with mock.patch.object(legacy, "_load_owners", return_value=owners):
            return legacy.validate_repository(self.root)

    def stable_archive_payload_fixture(self):
        """Create one real source-backed ArchiveEnvelope and its MIG1 row."""

        source = "docs/03.specs/0998-archive-payload/spec.md"
        alternate = "docs/03.specs/0997-archive-payload/spec.md"
        payload = (
            b"# Completed historical source\n\n"
            b"[completed source](../0099-fixture/spec.md)\n\n"
            b"Use `scripts/validate-agent-role-semantics.py`.\n"
        )
        source_commit, source_blobs = self.fixture.git.commit_many(
            {source: payload, alternate: payload}
        )
        recovered = fixtures.recovery.recover_git_blob(self.root, source, source_commit)
        metadata = {
            "title": "Archive: completed payload source",
            "type": "content/archive",
            "status": "archived",
            "owner": "platform",
            "updated": "2026-08-29",
            "original_type": "sdlc/spec",
            "original_path": source,
            "archived_on": "2026-08-29",
            "archive_reason": "superseded",
            "replacement": self.fixture.target,
            "source_commit": source_commit,
            "source_blob": source_blobs[source],
            "content_sha256": hashlib.sha256(payload).hexdigest(),
        }
        envelope = fixtures.recovery.render_archive_envelope(
            metadata, recovered, payload
        )
        legacy_path = "docs/98.archive/legacy/archive-payload-source.md"
        legacy_commit, legacy_blobs = self.fixture.git.commit_many(
            {legacy_path: envelope}
        )
        self.fixture.git.run("rm", "--quiet", "--", source, alternate, legacy_path)
        stable_path = "docs/98.archive/03.specs/0998-archive-payload/spec.md"
        stable = self.root / stable_path
        stable.parent.mkdir(parents=True, exist_ok=True)
        stable.write_bytes(envelope)
        self.fixture.git.run("add", "--", stable_path)
        stable_key = PurePosixPath(stable_path)
        self.context.paths = (*self.context.paths, stable_key)
        self.context.texts[stable_key] = envelope.decode("utf-8")
        self.context.metadata[stable_key] = {"type": "content/archive"}
        self.context.profiles[stable_key] = self.links.ProfileView(
            "content/archive", "common", "classification-only"
        )
        self.context.tracked_regular_paths = frozenset(
            {*self.context.tracked_regular_paths, stable_key}
        )
        row = {
            "schema_version": 1,
            "migration_id": "MIG-0001",
            "legacy_path": legacy_path,
            "stable_path": stable_path,
            "artifact_id": "ARCHIVE-TEST",
            "action": "moved",
            "replacement": None,
            "source_commit": source_commit,
            "legacy_archive_commit": legacy_commit,
            "legacy_envelope_blob": legacy_blobs[legacy_path],
            "source_blob": source_blobs[source],
            "content_sha256": hashlib.sha256(payload).hexdigest(),
            "record_kind": "tombstone",
            "reason": "Reviewed stable Stage 98 rehome",
        }
        return stable_key, envelope, row, alternate

    def canonical_archive_payload_fixture(self):
        """Create a real canonical Archive mirror without a MIG1 row."""

        source = "docs/03.specs/0996-canonical-archive/spec.md"
        payload = (
            b"# Completed canonical source\n\n"
            b"[completed source](../0099-fixture/spec.md)\n\n"
            b"Use `scripts/validate-agent-role-semantics.py`.\n"
        )
        source_commit, source_blobs = self.fixture.git.commit_many({source: payload})
        recovered = fixtures.recovery.recover_git_blob(self.root, source, source_commit)
        metadata = {
            "title": "Archive: completed canonical source",
            "type": "content/archive",
            "status": "archived",
            "owner": "platform",
            "updated": "2026-08-29",
            "original_type": "sdlc/spec",
            "original_path": source,
            "archived_on": "2026-08-29",
            "archive_reason": "superseded",
            "replacement": self.fixture.target,
            "source_commit": source_commit,
            "source_blob": source_blobs[source],
            "content_sha256": hashlib.sha256(payload).hexdigest(),
        }
        envelope = fixtures.recovery.render_archive_envelope(
            metadata, recovered, payload
        )
        self.fixture.git.run("rm", "--quiet", "--", source)
        archive_path = "docs/98.archive/03.specs/0996-canonical-archive/spec.md"
        current = self.root / archive_path
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_bytes(envelope)
        self.fixture.git.run("add", "--", archive_path)
        archive_key = PurePosixPath(archive_path)
        self.context.paths = (*self.context.paths, archive_key)
        self.context.texts[archive_key] = envelope.decode("utf-8")
        self.context.metadata[archive_key] = {"type": "content/archive"}
        self.context.profiles[archive_key] = self.links.ProfileView(
            "content/archive", "common", "classification-only"
        )
        self.context.tracked_regular_paths = frozenset(
            {*self.context.tracked_regular_paths, archive_key}
        )
        return archive_key, envelope

    def test_valid_migration_path_declarations_are_not_instructions(self):
        legacy, _rows = self.legacy_declaration_fixture()
        self.assertEqual(
            self.validate_legacy_with_public_proof(legacy)["activeConsumers"], 0
        )

    def test_archive_payload_is_public_historical_proof_not_current_instruction(self):
        legacy, _rows = self.legacy_declaration_fixture()
        stable_path, envelope, row, _alternate = self.stable_archive_payload_fixture()
        with mock.patch.object(
            self.links, "_work107_stable_archive_rows", return_value=(row,)
        ):
            proof = self.proof()
            self.assertIn(stable_path.as_posix(), proof.archive_payloads)
            archive_proof = proof.archive_payloads[stable_path.as_posix()]
            self.assertNotIn(
                "scripts/validate-agent-role-semantics.py",
                archive_proof.remaining_text,
            )
            owners = types.SimpleNamespace(
                document_registry=proof.document_registry,
                proof=proof,
                native_paths=frozenset(),
                enforcement_paths=frozenset(),
                helper_roles={},
                retention=None,
            )
            with mock.patch.object(legacy, "_load_owners", return_value=owners):
                self.assertEqual(
                    legacy.validate_repository(self.root)["activeConsumers"], 0
                )
        self.assertEqual(archive_proof.input_bytes, envelope)
        self.assertEqual(
            proof.terminal_targets[self.fixture.source], self.fixture.target
        )

    def test_canonical_non_mig1_archive_payload_is_public_historical_proof(self):
        legacy, _rows = self.legacy_declaration_fixture()
        archive_path, envelope = self.canonical_archive_payload_fixture()
        proof = self.proof()
        self.assertIn(archive_path.as_posix(), proof.archive_payloads)
        owners = types.SimpleNamespace(
            document_registry=proof.document_registry,
            proof=proof,
            native_paths=frozenset(),
            enforcement_paths=frozenset(),
            helper_roles={},
            retention=None,
        )
        with mock.patch.object(legacy, "_load_owners", return_value=owners):
            self.assertEqual(
                legacy.validate_repository(self.root)["activeConsumers"], 0
            )
        self.assertEqual(
            proof.archive_payloads[archive_path.as_posix()].input_bytes, envelope
        )

    def test_archive_candidate_admission_uses_profile_and_context_path(self):
        stable_path, envelope, row, _alternate = self.stable_archive_payload_fixture()
        malformed_type = envelope.replace(
            b'type: "content/archive"', b'type: "content/invalid"', 1
        )
        self.context.texts[stable_path] = malformed_type.decode("utf-8")
        self.context.metadata[stable_path] = {"type": "content/invalid"}
        with (
            mock.patch.object(
                self.links, "_work107_stable_archive_rows", return_value=(row,)
            ),
            self.assertRaises(self.links.ConfigurationError),
        ):
            self.proof()
        self.context.texts[stable_path] = envelope.decode("utf-8")
        self.context.metadata[stable_path] = {"type": "content/archive"}
        self.context.paths = tuple(
            path for path in self.context.paths if path != stable_path
        )
        proof = self.proof()
        self.assertNotIn(stable_path.as_posix(), proof.archive_payloads)

    def test_archive_owner_rejects_changed_payload_marker_and_source(self):
        stable_path, envelope, row, _alternate = self.stable_archive_payload_fixture()
        source_commit = row["source_commit"].encode("ascii")
        cases = {
            "payload": envelope[:-1] + b"!",
            "marker": envelope.replace(
                fixtures.recovery.ARCHIVE_ENVELOPE_MARKER,
                b"<!-- archive-envelope:v2 -->",
                1,
            ),
            "missing_source": envelope.replace(
                source_commit, b"0" * len(source_commit), 1
            ),
            "blob_not_commit": envelope.replace(
                source_commit,
                row["source_blob"].encode("ascii"),
                1,
            ),
        }
        for name, changed in cases.items():
            with self.subTest(name=name):
                self.context.texts[stable_path] = changed.decode("utf-8")
                with (
                    mock.patch.object(
                        self.links,
                        "_work107_stable_archive_rows",
                        return_value=(row,),
                    ),
                    self.assertRaises(self.links.ConfigurationError),
                ):
                    self.proof()
        self.context.texts[stable_path] = envelope.decode("utf-8")

    def test_archive_owner_rejects_false_historical_source_and_unadmitted_mirror(self):
        stable_path, envelope, row, alternate = self.stable_archive_payload_fixture()
        source_payload = fixtures.recovery.parse_archive_envelope(envelope).payload
        alternate_recovered = fixtures.recovery.recover_git_blob(
            self.root, alternate, row["source_commit"]
        )
        historical = fixtures.recovery.parse_archive_envelope(envelope)
        alternate_metadata = dict(historical.metadata)
        alternate_metadata.update(
            original_path=alternate,
            source_commit=row["source_commit"],
            source_blob=row["source_blob"],
            content_sha256=hashlib.sha256(source_payload).hexdigest(),
        )
        false_identity = fixtures.recovery.render_archive_envelope(
            alternate_metadata, alternate_recovered, source_payload
        )
        self.context.texts[stable_path] = false_identity.decode("utf-8")
        with (
            mock.patch.object(
                self.links, "_work107_stable_archive_rows", return_value=(row,)
            ),
            self.assertRaises(self.links.ConfigurationError),
        ):
            self.proof()
        made_up_path = stable_path.with_name("unproved-stable.md")
        self.context.paths = tuple(
            made_up_path if path == stable_path else path for path in self.context.paths
        )
        self.context.texts.pop(stable_path)
        self.context.texts[made_up_path] = envelope.decode("utf-8")
        self.context.metadata[made_up_path] = self.context.metadata.pop(stable_path)
        self.context.profiles[made_up_path] = self.context.profiles.pop(stable_path)
        self.context.tracked_regular_paths = frozenset(
            made_up_path if path == stable_path else path
            for path in self.context.tracked_regular_paths
        )
        with (
            mock.patch.object(
                self.links, "_work107_stable_archive_rows", return_value=()
            ),
            self.assertRaises(self.links.ConfigurationError),
        ):
            self.proof()

    def test_archive_owner_uses_held_context_bytes_not_a_live_reread(self):
        stable_path, envelope, row, _alternate = self.stable_archive_payload_fixture()
        (self.root / stable_path).write_bytes(envelope[:-1] + b"!")
        with mock.patch.object(
            self.links, "_work107_stable_archive_rows", return_value=(row,)
        ):
            proof = self.proof()
        self.assertEqual(
            proof.archive_payloads[stable_path.as_posix()].input_bytes, envelope
        )

    def test_exact_historical_inline_mention_uses_its_terminal_disposition(self):
        legacy, rows = self.legacy_declaration_fixture()
        raw = self.fixture.consumer_bytes + (
            b"\nAdded `docs/00.agent-governance/harness-implementation-map.md`.\n"
        )
        commit, _ = self.fixture.git.commit_many({self.fixture.consumer: raw})
        self.fixture.write(
            rows,
            consumers=[{"source_commit": commit, "paths": [self.fixture.consumer]}],
        )
        self.context.texts[self.consumer] = raw.decode()
        self.assertEqual(
            self.validate_legacy_with_public_proof(legacy)["activeConsumers"], 0
        )
        changed = raw + b"new instruction\n"
        (self.root / self.fixture.consumer).write_bytes(changed)
        self.fixture.git.run("add", "--", self.fixture.consumer)
        self.context.texts[self.consumer] = changed.decode()
        with self.assertRaises(self.links.ConfigurationError):
            self.validate_legacy_with_public_proof(legacy)

    def test_quoted_comma_literal_disposition_flows_to_legacy_scanner(self):
        legacy, rows = self.legacy_declaration_fixture()
        literal = next(iter(legacy.RETIRED_TOKENS))
        raw = b"# Completed\n\n`" + literal.encode() + b"`,\n"
        commit, _ = self.fixture.git.commit_many({self.fixture.consumer: raw})
        consumers = [{"source_commit": commit, "paths": [self.fixture.consumer]}]
        reference = {
            "kind": "literal-path",
            "consumer_path": self.fixture.consumer,
            "legacy_path": literal,
        }
        self.fixture.write(rows, consumers=consumers, references=[reference])
        self.context.texts[self.consumer] = raw.decode()

        proof = self.proof()
        key = (self.fixture.consumer, literal)
        self.assertEqual(proof.consumers[self.fixture.consumer], raw)
        self.assertEqual(proof.literal_dispositions[key], self.fixture.target)
        self.assertNotIn(key, proof.rendered_dispositions)
        self.assertEqual(
            self.validate_legacy_with_public_proof(legacy)["activeConsumers"], 0
        )

        self.fixture.write(rows, consumers=consumers)
        with self.assertRaises(self.links.ConfigurationError):
            self.validate_legacy_with_public_proof(legacy)

        self.fixture.write(rows, consumers=consumers, references=[reference])
        changed = raw + b"changed\n"
        (self.root / self.fixture.consumer).write_bytes(changed)
        self.fixture.git.run("add", "--", self.fixture.consumer)
        self.context.texts[self.consumer] = changed.decode()
        with self.assertRaises(self.links.ConfigurationError):
            self.validate_legacy_with_public_proof(legacy)

    def test_fresh_migration_reason_retired_instruction_fails(self):
        legacy, rows = self.legacy_declaration_fixture()
        rows[-1]["reason"] = "use " + rows[-1]["legacy_path"]
        self.fixture.write(rows)
        with self.assertRaises(legacy.ContractError) as raised:
            self.validate_legacy_with_public_proof(legacy)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-CONSUMER")

    def test_fresh_migration_outside_ledger_retired_instruction_fails(self):
        legacy, _rows = self.legacy_declaration_fixture()
        path = self.root / self.fixture.path
        path.write_bytes(path.read_bytes() + b"\nuse .github/ABOUT.md\n")
        self.fixture.git.run("add", "--", self.fixture.path)
        with self.assertRaises(legacy.ContractError) as raised:
            self.validate_legacy_with_public_proof(legacy)
        self.assertEqual(raised.exception.rule_id, "AGQC-LEGACY-CONSUMER")

    def test_old_mig3_source_proof_and_field_projection_preserve_nonpath_text(self):
        path = self.links.WORK054_MIGRATION_PATH
        raw = (fixtures.ROOT / path).read_bytes()
        rows = fixtures.archive.validate_pinned_migration_recovery(
            fixtures.ROOT, str(path), raw
        )
        targets = {row["legacy_path"]: row["replacement"] for row in rows}
        view = fixtures.archive.project_migration_declaration_fields(raw, targets)
        self.assertEqual(view.source_bytes, raw)
        self.assertTrue(set(targets).issubset(view.path_dispositions))
        self.assertIn("## Recovery", view.remaining_text)
        for row in rows:
            self.assertIn(row["reason"], view.remaining_text)

    def test_reference_projection_masks_only_verified_paths_and_scanner_keeps_prose(
        self,
    ):
        legacy = load_validator()
        view_path = ".claude/workflows"
        link_target = "../.agents/workflows"
        raw = self.fixture.write(
            references=[
                {
                    "kind": "symlink-view",
                    "consumer_path": self.fixture.consumer,
                    "legacy_path": view_path,
                    "source_commit": self.fixture.commit,
                    "source_mode": "120000",
                    "source_blob": "0" * 40,
                    "link_target": link_target,
                    "lookup_path": fixtures.archive.ARCHIVE_INDEX.as_posix(),
                }
            ]
        )
        view = fixtures.archive.project_migration_declaration_fields(
            raw, {self.fixture.source: self.fixture.target}
        )
        self.assertNotIn(view_path, view.remaining_text)
        self.assertIn(link_target, view.remaining_text)
        self.assertIn("symlink-view", view.remaining_text)
        self.assertIn(self.fixture.row["reason"], view.remaining_text)
        self.assertNotIn(
            view_path, legacy._retired_mentions(self.fixture.path, view.remaining_text)
        )

    def test_public_proof_returns_exact_bytes_and_terminal_dispositions(self):
        proof = self.proof()
        fixture = self.fixture
        self.assertEqual(proof.consumers[fixture.consumer], fixture.consumer_bytes)
        self.assertEqual(proof.terminal_targets[fixture.source], fixture.target)
        self.assertEqual(
            proof.rendered_dispositions[(fixture.consumer, fixture.source)],
            fixture.target,
        )
        for mapping in (
            proof.consumers,
            proof.terminal_targets,
            proof.rendered_dispositions,
        ):
            with self.assertRaises(TypeError):
                mapping["unreviewed"] = b"unreviewed"

    def test_view_cannot_overwrite_an_existing_rendered_disposition(self):
        reference = fixtures.archive.HistoricalReferenceDisposition(
            "symlink-view", fixtures.archive.ARCHIVE_INDEX.as_posix()
        )
        proof = fixtures.archive.MigrationProof(
            {self.fixture.source: self.fixture.target},
            {self.fixture.consumer: self.fixture.consumer_bytes},
            references={(self.fixture.consumer, self.fixture.source): reference},
        )
        with (
            mock.patch.object(
                self.links, "_context_migration_proof", return_value=proof
            ),
            self.assertRaisesRegex(self.links.ConfigurationError, "conflicts"),
        ):
            self.proof()

    def test_public_adapter_exports_consumer_scoped_literal_and_view_results(self):
        for kind, terminal in (
            ("literal-path", self.fixture.target),
            ("symlink-view", fixtures.archive.ARCHIVE_INDEX.as_posix()),
        ):
            with self.subTest(kind=kind):
                reference = fixtures.archive.HistoricalReferenceDisposition(
                    kind, terminal
                )
                proof = fixtures.archive.MigrationProof(
                    {},
                    {self.fixture.consumer: self.fixture.consumer_bytes},
                    references={
                        (self.fixture.consumer, self.fixture.source): reference
                    },
                )
                with mock.patch.object(
                    self.links, "_context_migration_proof", return_value=proof
                ):
                    historical = self.proof()
                key = (self.fixture.consumer, self.fixture.source)
                if kind == "literal-path":
                    self.assertEqual(historical.literal_dispositions[key], terminal)
                    self.assertNotIn(key, historical.rendered_dispositions)
                else:
                    self.assertEqual(historical.rendered_dispositions[key], terminal)
                    self.assertNotIn(key, historical.literal_dispositions)

    def test_held_context_reuses_markdown_ria_bytes_and_generic_inputs(self):
        documents, registry, _raw, schema, _templates = (
            self.fixture.held_document_inputs()
        )
        for relative in (self.links.RIA_CONTRACT_PATH, self.links.RIA_SCHEMA_PATH):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((fixtures.ROOT / relative).read_bytes())
        self.fixture.git.run("add", "--", str(self.links.RIA_SCHEMA_PATH))
        inventory = types.SimpleNamespace(
            current_paths=(self.consumer,),
            baseline_paths=(),
            current_symlink_paths=(PurePosixPath(".codex/skills"),),
        )
        legacy = load_validator()
        (self.root / ".codex").mkdir()
        (self.root / ".codex/skills").symlink_to("../.agents/skills")
        reads = []
        with legacy._RepositoryReader(self.root) as reader:

            def read_current_bytes(path, max_bytes):
                reads.append((path, max_bytes))
                return reader.read_bytes(path, max_bytes=max_bytes)

            def read_symlink(path):
                self.assertIsNone(reader.candidate_payload(path, read=False))
                return dict(legacy.ALLOWED_INTERNAL_SYMLINKS)[path]

            with (
                mock.patch.object(
                    self.links,
                    "load_registry",
                    side_effect=AssertionError("registry reopen"),
                ),
                mock.patch.object(
                    self.links,
                    "read_repository_text",
                    side_effect=AssertionError("text reopen"),
                ),
                mock.patch.object(
                    self.links, "enumerate_target_markdown", return_value=inventory
                ),
                mock.patch.object(
                    self.links,
                    "_terminal_governance_current_owners",
                    return_value=((), ()),
                ),
                mock.patch.object(
                    self.links,
                    "_terminal_reference_current_packs",
                    return_value=self.links.ReferenceCurrentPacks(
                        "content/reference", ()
                    ),
                ),
            ):
                context = self.build_context(
                    self.root,
                    registry=registry,
                    raw_schema=schema,
                    read_current_bytes=read_current_bytes,
                    read_symlink=read_symlink,
                )
            self.assertIs(context.document_registry, registry)
            self.assertIs(context.raw_schema, schema)
            self.assertEqual(
                context.texts[self.consumer].encode(), self.fixture.consumer_bytes
            )
            self.assertEqual(
                context.ria_contract_text.encode(),
                (self.root / self.links.RIA_CONTRACT_PATH).read_bytes(),
            )
            self.assertEqual(
                context.adapter_targets[PurePosixPath(".codex/skills")],
                PurePosixPath(".agents/skills"),
            )
            self.assertEqual(
                [path for path, _ in reads].count(str(self.links.RIA_CONTRACT_PATH)), 1
            )
            with mock.patch.object(
                self.links,
                "repository_migration_proof",
                wraps=self.links.repository_migration_proof,
            ) as proof:
                # Both the old MIG2/MIG3 helpers and the new public proof use
                # this same context seam; each call must retain held mode.
                self.assertEqual(
                    self.links._generic_migration_targets(context)[
                        PurePosixPath(self.fixture.source)
                    ],
                    PurePosixPath(self.fixture.target),
                )
                self.links._context_migration_proof(context)
            self.assertEqual(proof.call_count, 2)
            for call in proof.call_args_list:
                self.assertIs(call.kwargs["registry"], registry)
                self.assertIs(call.kwargs["raw_schema"], schema)
                self.assertIs(call.kwargs["read_current_bytes"], read_current_bytes)
        self.assertEqual(
            documents.REGISTRY_PATH.as_posix(), "docs/99.templates/registry.json"
        )

    def test_held_context_rejects_partial_invalid_and_oversized_inputs(self):
        _documents, registry, _raw, schema, _templates = (
            self.fixture.held_document_inputs()
        )
        inventory = types.SimpleNamespace(
            current_paths=(self.consumer,), baseline_paths=(), current_symlink_paths=()
        )
        for inputs in (
            {"registry": registry},
            {"raw_schema": None},
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda *_args: b"",
            },
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda *_args: None,
                "read_symlink": lambda _path: "",
            },
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda *_args: b"\xff",
                "read_symlink": lambda _path: "",
            },
            {
                "registry": registry,
                "raw_schema": schema,
                "read_current_bytes": lambda _path, limit: b" " * (limit + 1),
                "read_symlink": lambda _path: "",
            },
        ):
            with (
                self.subTest(keys=tuple(inputs)),
                mock.patch.object(
                    self.links, "enumerate_target_markdown", return_value=inventory
                ),
                mock.patch.object(
                    self.links,
                    "load_registry",
                    side_effect=AssertionError("registry reopen"),
                ),
                mock.patch.object(
                    self.links,
                    "read_repository_text",
                    side_effect=AssertionError("text reopen"),
                ),
                self.assertRaises(self.links.ConfigurationError),
            ):
                self.build_context(self.root, **inputs)

    def test_migration_declarations_mask_only_validated_path_fields(self):
        fixture = self.fixture
        row = dict(fixture.row, reason="use " + fixture.source)
        fixture.write([row])
        proof = fixtures.archive.repository_migration_proof(self.root)
        declaration = proof.declarations[fixture.path]
        self.assertEqual(
            declaration.source_bytes, (self.root / fixture.path).read_bytes()
        )
        self.assertEqual(declaration.path_dispositions[fixture.source], fixture.target)
        self.assertIn("use " + fixture.source, declaration.remaining_text)
        self.assertNotIn('"legacy_path"', declaration.remaining_text)
        with self.assertRaises(TypeError):
            declaration.path_dispositions["unproved"] = "unproved"

    def test_public_proof_rejects_changed_exact_historical_consumer(self):
        fixture = self.fixture
        (self.root / fixture.consumer).write_bytes(
            fixture.consumer_bytes + b"\nnew use\n"
        )
        fixture.git.run("add", "--", fixture.consumer)
        with self.assertRaises(self.links.ConfigurationError):
            self.proof()

    def test_membership_does_not_admit_a_token_only_consumer(self):
        fixture = self.fixture
        raw = f"`{fixture.source}`\n".encode()
        commit, _ = fixture.git.commit_many({fixture.consumer: raw})
        fixture.write(
            consumers=[{"source_commit": commit, "paths": [fixture.consumer]}]
        )
        self.context.texts[self.consumer] = raw.decode()
        with self.assertRaises(self.links.ConfigurationError):
            self.proof()

    def test_ria_eligibility_requires_actual_exact_source_bytes(self):
        fixture = self.fixture
        source = PurePosixPath("docs/90.references/audits/fixture/report.md")
        raw = b"[policy](../../../00.agent-governance/old.md)\n"
        commit, _ = fixture.git.commit_many({str(source): raw})
        self.context.paths += (source,)
        self.context.texts[source] = raw.decode()
        self.context.profiles[source] = types.SimpleNamespace(
            profile_id="content/reference"
        )
        self.context.metadata[source] = {"status": "done"}
        self.context.tracked_regular_paths |= {source}
        self.context.ria_contract_text = json.dumps(
            {
                "snapshotGuard": {
                    "sourceCommit": "git-sha1:" + commit,
                    "historicalPackIds": ["audits/fixture"],
                },
                "retiredCurrentPackBaselines": [],
            }
        )
        proof = self.proof()
        self.assertEqual(proof.consumers[str(source)], raw)
        self.context.texts[source] += "new instruction\n"
        with self.assertRaises(self.links.ConfigurationError):
            self.proof()

    def test_audit_settled_retired_readme_uses_real_protected_git_bytes(self):
        source = PurePosixPath("docs/90.references/audits/2026-07-11-weia/README.md")
        contract_text = (fixtures.ROOT / self.links.RIA_CONTRACT_PATH).read_text()
        contract = json.loads(contract_text)
        record = next(
            record
            for record in contract["retiredCurrentPackBaselines"]
            if record["id"] == "audits/2026-07-11-weia"
        )
        current = (fixtures.ROOT / source).read_bytes()
        old = self.links._read_ria_commit_path(
            fixtures.ROOT,
            record["sourceCommit"].removeprefix("git-sha1:"),
            Path(source),
        )
        self.assertNotEqual(old, current)
        self.context.root = fixtures.ROOT
        self.context.paths = (source,)
        self.context.texts = {source: current.decode()}
        self.context.metadata = {source: {}}
        self.context.profiles = {
            source: types.SimpleNamespace(profile_id="readme/snapshot-pack")
        }
        self.context.tracked_regular_paths = frozenset({source})
        self.context.ria_contract_text = contract_text
        # This case proves actual RIA Git bytes, not unrelated migration corpora.
        with mock.patch.object(
            self.links,
            "repository_migration_proof",
            return_value=fixtures.archive.MigrationProof({}, {}),
        ):
            proof = self.proof()
        self.assertEqual(proof.consumers[str(source)], current)

    def test_terminal_status_alone_never_proves_historical_links(self):
        source = PurePosixPath("docs/03.specs/unproved/spec.md")
        self.context.paths += (source,)
        self.context.metadata[source] = {"status": "archived"}
        self.context.profiles[source] = types.SimpleNamespace(profile_id="sdlc/spec")
        self.context.texts[source] = (
            "[old role](../../../scripts/validate-agent-role-semantics.py)\n"
        )
        self.context.tracked_regular_paths |= {source}
        proof = self.proof()
        self.assertNotIn(str(source), proof.consumers)
        self.assertFalse(
            any(owner == str(source) for owner, _ in proof.rendered_dispositions)
        )

    def test_ria_projection_uses_proven_removed_contract_and_schema_bytes(self):
        from scripts import reference_information_architecture as ria

        fixture = self.fixture
        paths = (ria.AGENT_LEGACY_CUTOVER_PATH, ria.AGENT_LEGACY_CUTOVER_SCHEMA_PATH)
        source_inputs = {}
        for path in paths:
            current = fixtures.ROOT / path
            if current.is_file():
                source_inputs[str(path)] = current.read_bytes()
                continue
            migration = "docs/98.archive/migrations/0005-codex-claude-agent-governance-convergence.md"
            rows, _ = fixtures.archive.parse_migration_control(
                migration, (fixtures.ROOT / migration).read_bytes()
            )
            row = next(row for row in rows if row["legacy_path"] == str(path))
            source_inputs[str(path)] = self.links._read_ria_commit_path(
                fixtures.ROOT, row["source_commit"], path
            )
        commit, blobs = fixture.git.commit_many(source_inputs)
        target = "scripts/current-legacy-validator.py"
        (self.root / target).parent.mkdir()
        (self.root / target).write_bytes(b"# Current validator\n")
        fixture.git.run("add", "--", target)
        rows = [fixture.row]
        for path, raw in source_inputs.items():
            fixture.git.run("rm", "--quiet", "--", path)
            rows.append(
                dict(
                    legacy_path=path,
                    stable_path=None,
                    artifact_id=None,
                    action="merged",
                    replacement=target,
                    source_commit=commit,
                    source_blob=blobs[path],
                    content_sha256=hashlib.sha256(raw).hexdigest(),
                    reason="Retire duplicate current authority; retain its historical interpretation",
                )
            )
        fixture.write(rows)
        projections = ria.load_agent_cutover_projections(self.root, None)
        self.assertEqual(
            tuple(map(str, projections)),
            tuple(path for path, _ in ria.AGENT_CUTOVER_CURRENT_PATH_COUNTS),
        )
        # No authority reappears in the current fixture tree.
        self.assertTrue(all(not (self.root / path).exists() for path in paths))
        fixture.write(rows[:-1])
        with self.assertRaises(ria._GitError):
            ria.load_agent_cutover_projections(self.root, None)


if __name__ == "__main__":
    unittest.main()
