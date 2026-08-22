#!/usr/bin/env python3
"""Focused fixture tests for the private ARWB-001 recovery capability."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import archive_recovery  # noqa: E402
from scripts.archive_recovery import (  # noqa: E402
    ARCHIVE_ENVELOPE_MARKER,
    ARCHIVE_METADATA_KEYS,
    ArchiveContractError,
    parse_archive_envelope,
    recover_git_blob,
    render_fixture_archive_envelope,
    validate_archive_metadata,
)


class GitFixture:
    """Create exact Git objects without consulting the repository worktree."""

    def __init__(self, root: Path, *, initialize: bool = True) -> None:
        self.root = root
        if initialize:
            self.run("init", "--quiet")
        self.run("config", "user.email", "archive-fixture@example.invalid")
        self.run("config", "user.name", "Archive Fixture")

    def run(self, *args: str, input_bytes: bytes | None = None) -> bytes:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.root,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"fixture git command failed: git {' '.join(args)}: "
                f"{completed.stderr.decode('utf-8', errors='replace')}"
            )
        return completed.stdout

    def commit(self, relative_path: str, payload: bytes) -> tuple[str, str]:
        commit, blobs = self.commit_many({relative_path: payload})
        return commit, blobs[relative_path]

    def commit_many(self, files: dict[str, bytes]) -> tuple[str, dict[str, str]]:
        for relative_path, payload in files.items():
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        self.run("--literal-pathspecs", "add", "--", *files)
        self.run("commit", "--quiet", "-m", "fixture")
        commit = self.run("rev-parse", "HEAD").decode("ascii").strip()
        blobs = {
            relative_path: self.run("rev-parse", f"HEAD:{relative_path}")
            .decode("ascii")
            .strip()
            for relative_path in files
        }
        return commit, blobs


class ArchiveRecoveryTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="archive-recovery-")
        self.root = Path(self.temporary.name)
        self.git = GitFixture(self.root)
        self.original_path = "docs/03.specs/900-fixture/spec.md"
        self.payload = (
            b"---\n"
            b"title: 'Historical fixture'\n"
            b"type: sdlc/spec\n"
            b"status: done\n"
            b"owner: platform\n"
            b"updated: 2026-07-01\n"
            b"---\n\n"
            b"# Historical fixture\n\n"
            b"[one](../one.md) and [two](../two.md)\n"
        )
        self.commit, self.blob = self.git.commit(self.original_path, self.payload)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def metadata(self, **overrides: object) -> dict[str, object]:
        result: dict[str, object] = {
            "title": "Archive: Historical fixture",
            "type": "content/archive",
            "status": "archived",
            "owner": "platform",
            "updated": "2026-07-18",
            "original_type": "sdlc/spec",
            "original_path": self.original_path,
            "archived_on": "2026-07-18",
            "archive_reason": "superseded",
            "replacement": "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
            "source_commit": self.commit,
            "source_blob": self.blob,
            "content_sha256": hashlib.sha256(self.payload).hexdigest(),
        }
        result.update(overrides)
        return result

    def test_recovers_exact_full_git_object_and_ignores_worktree_bytes(self) -> None:
        worktree_path = self.root / self.original_path
        worktree_path.write_bytes(b"converted worktree bytes\r\n")

        recovered = recover_git_blob(self.root, self.original_path, self.commit)

        self.assertEqual(recovered.original_path, self.original_path)
        self.assertEqual(recovered.source_commit, self.commit)
        self.assertEqual(recovered.source_blob, self.blob)
        self.assertRegex(recovered.source_commit, re.compile(r"^[0-9a-f]{40,64}$"))
        self.assertRegex(recovered.source_blob, re.compile(r"^[0-9a-f]{40,64}$"))
        self.assertEqual(recovered.source_bytes, self.payload)
        self.assertEqual(recovered.byte_count, len(self.payload))
        self.assertEqual(
            recovered.content_sha256, hashlib.sha256(self.payload).hexdigest()
        )
        self.assertEqual(recovered.inline_link_candidate_count, 2)
        self.assertEqual(
            recovered.proposed_archive_path,
            "docs/98.archive/03.specs/900-fixture/spec.md",
        )

    def test_rejects_missing_and_ambiguous_commit_objects_and_wrong_path(self) -> None:
        object_length = len(self.commit)
        cases = (
            (
                "missing-full-object",
                "0" * object_length,
                self.original_path,
                "RECOVERY-OBJECT-MISSING",
            ),
            (
                "abbreviated-object-is-ambiguous",
                self.commit[:8],
                self.original_path,
                "RECOVERY-OBJECT-AMBIGUOUS",
            ),
            (
                "wrong-original-path",
                self.commit,
                "docs/03.specs/900-fixture/missing.md",
                "RECOVERY-PATH-MISSING",
            ),
        )
        for name, commit, original_path, expected_code in cases:
            with self.subTest(name=name):
                with self.assertRaisesRegex(ArchiveContractError, f"^{expected_code}:"):
                    recover_git_blob(self.root, original_path, commit)

    def test_rejects_non_utf8_git_blob(self) -> None:
        original_path = "docs/03.specs/901-binary/spec.md"
        commit, _ = self.git.commit(original_path, b"# binary\n\xff\xfe")

        with self.assertRaisesRegex(ArchiveContractError, r"^RECOVERY-NON-UTF8:"):
            recover_git_blob(self.root, original_path, commit)

    def test_metadata_schema_and_reason_replacement_dependency_fail_closed(
        self,
    ) -> None:
        self.assertEqual(tuple(self.metadata()), ARCHIVE_METADATA_KEYS)
        replacement = validate_archive_metadata(self.metadata())
        self.assertIsInstance(
            replacement,
            archive_recovery.ArchiveReplacementReference,
        )
        self.assertEqual(
            replacement.path,
            "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md",
        )

        invalid_cases = (
            ("unsupported reason", {"archive_reason": "other"}),
            ("required replacement absent", {"replacement": None}),
            (
                "archive replacement forbidden",
                {
                    "replacement": (
                        "docs/98.archive/03.specs/900-fixture/replacement.md"
                    )
                },
            ),
            (
                "replacement forbidden",
                {"archive_reason": "retired", "replacement": self.original_path},
            ),
            ("wrong type", {"type": "content/archive-tombstone"}),
            ("wrong metadata order", {"owner": None}),
        )
        for name, override in invalid_cases:
            with self.subTest(name=name):
                metadata = self.metadata(**override)
                if name == "wrong metadata order":
                    owner = metadata.pop("owner")
                    metadata["owner"] = owner
                with self.assertRaisesRegex(
                    ArchiveContractError, r"^ARCHIVE-METADATA-"
                ):
                    validate_archive_metadata(metadata)

    def test_round_trips_payload_to_eof_with_collisions_and_final_newline_states(
        self,
    ) -> None:
        payloads = (
            b"# no final newline",
            b"# one final newline\n",
            b"---\nfrontmatter: collision\n---\n\n"
            + ARCHIVE_ENVELOPE_MARKER
            + b"\n\n```markdown\n<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->\n```\n\n",
        )
        for payload in payloads:
            with self.subTest(payload=payload[-24:]):
                source_path = "docs/03.specs/902-roundtrip/spec.md"
                commit, _ = self.git.commit(source_path, payload)
                source = recover_git_blob(self.root, source_path, commit)
                metadata = self.metadata(
                    original_path=source_path,
                    source_commit=source.source_commit,
                    source_blob=source.source_blob,
                    content_sha256=source.content_sha256,
                )
                envelope_bytes = render_fixture_archive_envelope(
                    metadata, source, payload
                )
                parsed = parse_archive_envelope(envelope_bytes, expected=source)
                self.assertEqual(parsed.payload, payload)
                self.assertEqual(
                    parsed.payload.endswith(b"\n"), payload.endswith(b"\n")
                )
                self.assertEqual(parsed.metadata, metadata)

    def test_rejects_malformed_or_misplaced_marker(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        metadata = self.metadata()
        valid = render_fixture_archive_envelope(metadata, recovered, self.payload)
        malformed = valid.replace(
            ARCHIVE_ENVELOPE_MARKER, b"<!-- archive-envelope:v2 -->", 1
        )
        misplaced = valid.replace(
            ARCHIVE_ENVELOPE_MARKER + b"\n",
            b"prose before marker\n" + ARCHIVE_ENVELOPE_MARKER + b"\n",
            1,
        )
        for name, fixture in (("malformed", malformed), ("misplaced", misplaced)):
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ArchiveContractError, r"^ARCHIVE-MARKER-INVALID:"
                ):
                    parse_archive_envelope(fixture, expected=recovered)

    def test_rejects_duplicate_frontmatter_key(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        valid = render_fixture_archive_envelope(
            self.metadata(),
            recovered,
            self.payload,
        )
        duplicate = valid.replace(
            b'title: "Archive: Historical fixture"\n',
            b'title: "Archive: Historical fixture"\ntitle: "Duplicate title"\n',
            1,
        )

        with self.assertRaisesRegex(
            ArchiveContractError,
            r"^ARCHIVE-FRONTMATTER-DUPLICATE:",
        ):
            parse_archive_envelope(duplicate, expected=recovered)

    def test_rejects_noncanonical_frontmatter_serialization(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        valid = render_fixture_archive_envelope(
            self.metadata(),
            recovered,
            self.payload,
        )
        frontmatter, payload = valid.split(ARCHIVE_ENVELOPE_MARKER + b"\n", 1)
        cases = (
            (
                "crlf",
                frontmatter.replace(b"\n", b"\r\n")
                + ARCHIVE_ENVELOPE_MARKER
                + b"\n"
                + payload,
            ),
            (
                "extra-spacing",
                valid.replace(
                    b'title: "Archive: Historical fixture"\n',
                    b'title:  "Archive: Historical fixture"\n',
                    1,
                ),
            ),
        )

        for name, fixture in cases:
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ArchiveContractError,
                    r"^ARCHIVE-FRONTMATTER-NONCANONICAL:",
                ):
                    parse_archive_envelope(fixture, expected=recovered)

    def test_rejects_noncanonical_raw_original_path(self) -> None:
        cases = (
            "docs/03.specs/./900-fixture/spec.md",
            "docs/03.specs//900-fixture/spec.md",
            "docs/03.specs/900-fixture/spec\x7f.md",
        )

        for original_path in cases:
            with self.subTest(original_path=original_path):
                with self.assertRaisesRegex(
                    ArchiveContractError,
                    r"^ARCHIVE-METADATA-PATH:",
                ):
                    recover_git_blob(self.root, original_path, self.commit)

    def test_repr_does_not_disclose_recovered_or_parsed_payload(self) -> None:
        source_path = "docs/03.specs/904-repr/spec.md"
        sentinel = b"ARWB-SECRET-PAYLOAD-SENTINEL"
        commit, _ = self.git.commit(source_path, sentinel)
        recovered = recover_git_blob(self.root, source_path, commit)
        metadata = self.metadata(
            original_path=source_path,
            source_commit=recovered.source_commit,
            source_blob=recovered.source_blob,
            content_sha256=recovered.content_sha256,
        )
        parsed = parse_archive_envelope(
            render_fixture_archive_envelope(metadata, recovered, sentinel),
            expected=recovered,
        )

        self.assertNotIn(sentinel.decode("ascii"), repr(recovered))
        self.assertNotIn(sentinel.decode("ascii"), repr(parsed))

    def test_literal_pathspec_recovers_metacharacter_filenames_exactly(self) -> None:
        fixtures = {
            "docs/03.specs/905-pathspec/literal*.md": b"literal-star",
            "docs/03.specs/905-pathspec/literal-other.md": b"glob-star",
            "docs/03.specs/905-pathspec/question?.md": b"literal-question",
            "docs/03.specs/905-pathspec/question1.md": b"glob-question",
            "docs/03.specs/905-pathspec/bracket[1].md": b"literal-bracket",
            "docs/03.specs/905-pathspec/bracket1.md": b"glob-bracket",
        }
        commit, blobs = self.git.commit_many(fixtures)

        for source_path in (
            "docs/03.specs/905-pathspec/literal*.md",
            "docs/03.specs/905-pathspec/question?.md",
            "docs/03.specs/905-pathspec/bracket[1].md",
        ):
            with self.subTest(source_path=source_path):
                recovered = recover_git_blob(self.root, source_path, commit)
                self.assertEqual(recovered.source_blob, blobs[source_path])
                self.assertEqual(recovered.source_bytes, fixtures[source_path])

    def test_sha256_repository_recovery_and_round_trip(self) -> None:
        root = self.root / "sha256-repository"
        root.mkdir()
        initialized = subprocess.run(
            ["git", "init", "--quiet", "--object-format=sha256"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if initialized.returncode != 0:
            detail = initialized.stderr.decode("utf-8", errors="replace").lower()
            unsupported = (
                "unknown option" in detail
                or "unsupported object format" in detail
                or "sha256 is not supported" in detail
            )
            if unsupported:
                self.skipTest(
                    "Git explicitly reports SHA-256 object format unsupported"
                )
            self.fail(
                "Git SHA-256 fixture initialization failed without unsupported report"
            )
        git = GitFixture(root, initialize=False)
        source_path = "docs/03.specs/906-sha256/spec.md"
        payload = b"# SHA-256 repository\n"
        commit, blob = git.commit(source_path, payload)

        recovered = recover_git_blob(root, source_path, commit)
        self.assertEqual(len(recovered.source_commit), 64)
        self.assertEqual(len(recovered.source_blob), 64)
        self.assertEqual(recovered.source_blob, blob)
        metadata = self.metadata(
            original_path=source_path,
            source_commit=recovered.source_commit,
            source_blob=recovered.source_blob,
            content_sha256=recovered.content_sha256,
        )
        parsed = parse_archive_envelope(
            render_fixture_archive_envelope(metadata, recovered, payload),
            expected=recovered,
        )
        self.assertEqual(parsed.payload, payload)

    def test_hostile_git_environment_isolated_and_replacements_disabled(self) -> None:
        original_payload = self.payload
        (self.root / self.original_path).write_bytes(b"replacement payload\n")
        self.git.run("add", "--", self.original_path)
        self.git.run("commit", "--quiet", "-m", "replacement fixture")
        replacement_commit = self.git.run("rev-parse", "HEAD").decode("ascii").strip()
        self.git.run("replace", self.commit, replacement_commit)
        hostile = {
            "GIT_CONFIG_GLOBAL": "/hostile/config",
            "GIT_OBJECT_DIRECTORY": "/hostile/objects",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/hostile/alternates",
            "GIT_TERMINAL_PROMPT": "1",
            "GIT_NO_LAZY_FETCH": "0",
        }
        observed: list[tuple[list[str], dict[str, object]]] = []
        real_popen = subprocess.Popen

        def capture(*args: object, **kwargs: object):
            observed.append((list(args[0]), dict(kwargs)))
            return real_popen(*args, **kwargs)

        with mock.patch.dict(os.environ, hostile, clear=False):
            with mock.patch.object(
                archive_recovery.subprocess, "Popen", side_effect=capture
            ):
                recovered = recover_git_blob(self.root, self.original_path, self.commit)

        self.assertEqual(recovered.source_bytes, original_payload)
        self.assertTrue(observed)
        for argv, kwargs in observed:
            environment = kwargs["env"]
            self.assertIsInstance(environment, dict)
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
            self.assertEqual(environment["GIT_CONFIG_SYSTEM"], os.devnull)
            self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
            self.assertEqual(environment["GIT_GRAFT_FILE"], os.devnull)
            self.assertEqual(environment["GIT_TERMINAL_PROMPT"], "0")
            self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
            self.assertEqual(environment["GIT_NO_REPLACE_OBJECTS"], "1")
            self.assertNotIn("GIT_OBJECT_DIRECTORY", environment)
            self.assertNotIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", environment)
            self.assertIn("--no-replace-objects", argv)
            self.assertIn("--literal-pathspecs", argv)
            self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)

    def test_stable_recovery_errors_for_root_startup_timeout_and_object_format(
        self,
    ) -> None:
        missing_root = self.root / "missing"
        with self.assertRaisesRegex(
            ArchiveContractError,
            r"^RECOVERY-ROOT-INVALID:",
        ):
            recover_git_blob(missing_root, self.original_path, self.commit)

        with mock.patch.object(
            archive_recovery.subprocess,
            "Popen",
            side_effect=FileNotFoundError("STARTUP-SENTINEL"),
        ):
            with self.assertRaisesRegex(
                ArchiveContractError,
                r"^RECOVERY-GIT-STARTUP:",
            ) as startup:
                recover_git_blob(self.root, self.original_path, self.commit)
        self.assertNotIn("STARTUP-SENTINEL", str(startup.exception))

        with mock.patch.object(
            archive_recovery._DeadlineReader,  # noqa: SLF001
            "read",
            side_effect=ArchiveContractError(
                "RECOVERY-GIT-TIMEOUT", "bounded timeout"
            ),
        ):
            with self.assertRaisesRegex(
                ArchiveContractError,
                r"^RECOVERY-GIT-TIMEOUT:",
            ) as timeout:
                recover_git_blob(self.root, self.original_path, self.commit)
        self.assertNotIn("TIMEOUT-SENTINEL", str(timeout.exception))

        root_output = f"{self.root.resolve()}\n".encode("utf-8")
        for name, format_output in (
            ("non-ASCII", b"\xff\n"),
            ("unsupported", b"sha512\n"),
            ("multiple-lines", b"sha1\nsha256\n"),
        ):
            responses = (
                subprocess.CompletedProcess([], 0, root_output, b""),
                subprocess.CompletedProcess([], 0, format_output, b""),
            )
            with self.subTest(name=name):
                with mock.patch.object(
                    archive_recovery,
                    "_git",
                    side_effect=responses,
                ):
                    with self.assertRaisesRegex(
                        ArchiveContractError,
                        r"^RECOVERY-OBJECT-FORMAT:",
                    ):
                        recover_git_blob(self.root, self.original_path, self.commit)

    def test_git_batch_rejects_oversized_header_before_body_read(self) -> None:
        object_id = self.blob
        header = (
            f"{object_id} blob {archive_recovery.MAX_GIT_BLOB_BYTES + 1}\n"
        ).encode("ascii")

        class HeaderOnly:
            def __init__(self) -> None:
                self.offset = 0
                self.body_read = False

            def read(self, size: int = -1) -> bytes:
                if self.offset >= len(header):
                    self.body_read = True
                    raise AssertionError("oversized body must not be read")
                end = len(header) if size < 0 else min(len(header), self.offset + size)
                result = header[self.offset:end]
                self.offset = end
                return result

        stream = HeaderOnly()
        with self.assertRaisesRegex(
            ArchiveContractError, r"^RECOVERY-RESOURCE-LIMIT:"
        ) as failure:
            archive_recovery._read_git_blob_batch_protocol(  # noqa: SLF001
                stream,
                (object_id,),
                object_id_length=len(object_id),
            )

        self.assertFalse(stream.body_read)
        self.assertNotIn(object_id, str(failure.exception))

    def test_git_batch_enforces_aggregate_budget_and_redacts_payload(self) -> None:
        first = self.blob
        second = "0" * len(first)
        sentinel = b"SECRET-PAYLOAD-SENTINEL"
        response = (
            f"{first} blob {len(sentinel)}\n".encode("ascii")
            + sentinel
            + b"\n"
            + f"{second} blob {len(sentinel)}\n".encode("ascii")
            + sentinel
            + b"\n"
        )

        with self.assertRaisesRegex(
            ArchiveContractError, r"^RECOVERY-RESOURCE-LIMIT:"
        ) as failure:
            archive_recovery._read_git_blob_batch_protocol(  # noqa: SLF001
                io.BytesIO(response),
                (first, second),
                object_id_length=len(first),
                aggregate_limit=len(sentinel),
            )

        self.assertNotIn(sentinel.decode("ascii"), str(failure.exception))
        self.assertNotIn(second, str(failure.exception))

        with self.assertRaisesRegex(
            ArchiveContractError, r"^RECOVERY-RESOURCE-LIMIT:"
        ):
            archive_recovery._read_git_blob_batch_protocol(  # noqa: SLF001
                io.BytesIO(b""),
                (first, second),
                object_id_length=len(first),
                object_limit=1,
            )

    def test_git_batch_rejects_truncated_and_extra_protocol_without_payload(self) -> None:
        object_id = self.blob
        cases = {
            "truncated": f"{object_id} blob 5\nabc".encode("ascii"),
            "extra": f"{object_id} blob 3\nabc\nEXTRA-SENTINEL".encode("ascii"),
        }
        for name, response in cases.items():
            with self.subTest(name=name), self.assertRaisesRegex(
                ArchiveContractError, r"^RECOVERY-OBJECT-MISSING:"
            ) as failure:
                archive_recovery._read_git_blob_batch_protocol(  # noqa: SLF001
                    io.BytesIO(response),
                    (object_id,),
                    object_id_length=len(object_id),
                )
            self.assertNotIn("EXTRA-SENTINEL", str(failure.exception))

    def test_recover_git_blob_uses_size_aware_batch_reader(self) -> None:
        with mock.patch.object(
            archive_recovery,
            "_read_git_blob_batch",
            wraps=archive_recovery._read_git_blob_batch,  # noqa: SLF001
        ) as batch:
            recovered = recover_git_blob(self.root, self.original_path, self.commit)

        self.assertEqual(recovered.source_bytes, self.payload)
        batch.assert_called_once()

    def test_rejects_worktree_byte_substitution(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        substitute = self.payload.replace(b"\n", b"\r\n")

        with self.assertRaisesRegex(
            ArchiveContractError,
            r"^ARCHIVE-PAYLOAD-NOT-SOURCE-BLOB:",
        ):
            render_fixture_archive_envelope(self.metadata(), recovered, substitute)

    def test_cli_verify_is_read_only_and_output_is_exact_non_overwriting(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        record = self.root / "docs/98.archive/03.specs/900-fixture/spec.md"
        record.parent.mkdir(parents=True)
        record.write_bytes(
            render_fixture_archive_envelope(self.metadata(), recovered, self.payload)
        )
        before = tuple(sorted(path.as_posix() for path in self.root.rglob("*")))

        self.assertEqual(
            archive_recovery.main(
                ["--root", str(self.root), "--record", record.relative_to(self.root).as_posix(), "--verify"]
            ),
            0,
        )
        self.assertEqual(
            tuple(sorted(path.as_posix() for path in self.root.rglob("*"))), before
        )

        output = Path(self.temporary.name).parent / f"recovered-{self.root.name}.md"
        self.addCleanup(lambda: output.unlink(missing_ok=True))
        self.assertEqual(
            archive_recovery.main(
                ["--root", str(self.root), "--record", record.relative_to(self.root).as_posix(), "--output", str(output)]
            ),
            0,
        )
        self.assertEqual(output.read_bytes(), self.payload)
        with self.assertRaisesRegex(ArchiveContractError, r"^RECOVERY-OUTPUT-EXISTS:"):
            archive_recovery.recover_archive_record(self.root, record.relative_to(self.root).as_posix(), output=output)

    def test_recovery_output_rejects_repository_and_unconfined_paths(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        record = self.root / "docs/98.archive/03.specs/900-fixture/spec.md"
        record.parent.mkdir(parents=True)
        record.write_bytes(
            render_fixture_archive_envelope(self.metadata(), recovered, self.payload)
        )
        for output in (
            self.root / "docs/recovered.md",
            Path("relative-output.md"),
        ):
            with self.subTest(output=output), self.assertRaisesRegex(
                ArchiveContractError, r"^RECOVERY-OUTPUT-CONFINEMENT:"
            ):
                archive_recovery.recover_archive_record(
                    self.root,
                    record.relative_to(self.root).as_posix(),
                    output=output,
                )

    def test_recovery_rejects_archive_intermediate_parent_symlink(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        real_parent = self.root / "archive-record-parent"
        real_parent.mkdir()
        (real_parent / "spec.md").write_bytes(
            render_fixture_archive_envelope(self.metadata(), recovered, self.payload)
        )
        linked_parent = self.root / "docs/98.archive/03.specs/900-fixture"
        linked_parent.parent.mkdir(parents=True)
        linked_parent.symlink_to(real_parent, target_is_directory=True)

        with self.assertRaisesRegex(
            ArchiveContractError, r"^RECOVERY-RECORD-READ:"
        ):
            archive_recovery.recover_archive_record(
                self.root,
                "docs/98.archive/03.specs/900-fixture/spec.md",
                verify=True,
            )

    def test_recovery_rejects_output_intermediate_parent_symlink(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        record = self.root / "docs/98.archive/03.specs/900-fixture/spec.md"
        record.parent.mkdir(parents=True)
        record.write_bytes(
            render_fixture_archive_envelope(self.metadata(), recovered, self.payload)
        )
        temporary_root = Path(tempfile.gettempdir()).resolve()
        real_parent = Path(tempfile.mkdtemp(prefix="recovery-output-real-"))
        linked_parent = temporary_root / f"recovery-output-link-{self.root.name}"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        self.addCleanup(lambda: real_parent.rmdir())
        self.addCleanup(
            lambda: [child.unlink(missing_ok=True) for child in real_parent.iterdir()]
        )
        self.addCleanup(lambda: linked_parent.unlink(missing_ok=True))

        with self.assertRaisesRegex(
            ArchiveContractError, r"^RECOVERY-OUTPUT-CONFINEMENT:"
        ):
            archive_recovery.recover_archive_record(
                self.root,
                record.relative_to(self.root).as_posix(),
                output=linked_parent / "recovered.md",
            )

    def test_recovery_cleanup_keeps_substituted_output_identity(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        record = self.root / "docs/98.archive/03.specs/900-fixture/spec.md"
        record.parent.mkdir(parents=True)
        record.write_bytes(
            render_fixture_archive_envelope(self.metadata(), recovered, self.payload)
        )
        parent = Path(tempfile.mkdtemp(prefix="recovery-output-parent-"))
        parked = parent.with_name(f"{parent.name}-parked")
        output = parent / "recovered.md"
        replacement = b"replacement identity must survive\n"

        def substitute_parent_then_fail(_descriptor: int, _payload: object) -> int:
            parent.rename(parked)
            parent.mkdir()
            output.write_bytes(replacement)
            raise OSError("injected write failure")

        try:
            with mock.patch.object(
                archive_recovery.os, "write", side_effect=substitute_parent_then_fail
            ), self.assertRaisesRegex(
                ArchiveContractError, r"^RECOVERY-OUTPUT-WRITE:"
            ):
                archive_recovery.recover_archive_record(
                    self.root,
                    record.relative_to(self.root).as_posix(),
                    output=output,
                )
            self.assertTrue(output.exists())
            self.assertEqual(output.read_bytes(), replacement)
        finally:
            output.unlink(missing_ok=True)
            parent.rmdir()
            parked_output = parked / output.name
            parked_output.unlink(missing_ok=True)
            parked.rmdir()


class PinnedMigrationRecoveryCliTest(unittest.TestCase):
    """Keep CLI migration recovery limited to the sealed MIG-0004 control."""

    migration_path = (
        "docs/98.archive/migrations/0004-document-authority-convergence.md"
    )

    @staticmethod
    def run_cli(root: Path, record: str, *, verify: bool = True) -> tuple[int, str]:
        arguments = ["--root", str(root), "--record", record]
        arguments.extend(["--verify"] if verify else ["--output", "/tmp/recovery.md"])
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            result = archive_recovery.main(arguments)
        return result, output.getvalue()

    def test_cli_verifies_exact_sealed_mig0004_through_pinned_recovery(self) -> None:
        result, output = self.run_cli(ROOT, self.migration_path)

        self.assertEqual(result, 0, output)
        self.assertEqual(
            output,
            "PASS archive recovery operation=verify migration=MIG-0004\n",
        )

    def test_cli_rejects_wrong_digest_and_status_before_git_recovery(self) -> None:
        migration = (ROOT / self.migration_path).read_bytes()
        cases = (
            ("wrong-digest", migration + b"\n"),
            (
                "wrong-status",
                migration.replace(b'status: "sealed"', b'status: "accepted"', 1),
            ),
        )
        for name, content in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="migration-recovery-cli-"
            ) as temporary:
                root = Path(temporary)
                fixture = GitFixture(root)
                target = root / self.migration_path
                target.parent.mkdir(parents=True)
                target.write_bytes(content)
                fixture.run("add", "--", self.migration_path)

                result, output = self.run_cli(root, self.migration_path)

                self.assertEqual(result, 1)
                self.assertEqual(
                    output,
                    "FAIL archive recovery code=ARCHIVE-MIGRATION-PROFILE\n",
                )

    def test_cli_does_not_promote_wrong_or_unknown_migration_paths(self) -> None:
        migration = (ROOT / self.migration_path).read_bytes()
        cases = (
            (
                "wrong-declared-path",
                "docs/98.archive/migrations/"
                "mig-0003-agent-governance-control-plane-consolidation.md",
            ),
            (
                "unknown-migration",
                "docs/98.archive/migrations/9999-unreviewed.md",
            ),
        )
        for name, record in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="migration-recovery-cli-"
            ) as temporary:
                root = Path(temporary)
                _fixture = GitFixture(root)
                target = root / record
                target.parent.mkdir(parents=True)
                target.write_bytes(migration)

                result, output = self.run_cli(root, record)

                self.assertEqual(result, 1)
                self.assertEqual(
                    output,
                    "FAIL archive recovery code=ARCHIVE-MARKER-INVALID\n",
                )

    def test_cli_does_not_recover_mig0004_to_an_output_file(self) -> None:
        result, output = self.run_cli(ROOT, self.migration_path, verify=False)

        self.assertEqual(result, 1)
        self.assertEqual(
            output,
            "FAIL archive recovery code=ARCHIVE-MARKER-INVALID\n",
        )


class Work107StableArchiveContractTest(unittest.TestCase):
    """Focused WORK-107 contract for the reviewed 93-to-93 stable rehome."""

    maxDiff = None

    def test_work107_reviewed_mapping_is_exact_and_bijective(self) -> None:
        rows = archive_recovery.build_work107_migration_rows(ROOT)

        self.assertEqual(
            archive_recovery.WORK107_LEGACY_ARCHIVE_COMMIT,
            "eaf4f21ca84b68d98e20cd0b41db8b8d08ba6d0c",  # pragma: allowlist secret
        )
        self.assertEqual(len(rows), 93)
        self.assertEqual({row["action"] for row in rows}, {"moved"})
        self.assertEqual({row["replacement"] for row in rows}, {None})
        self.assertEqual(len({row["legacy_path"] for row in rows}), 93)
        self.assertEqual(len({row["stable_path"] for row in rows}), 93)
        self.assertEqual(len({row["artifact_id"] for row in rows}), 93)

        changes: dict[str, set[str]] = {}
        tombstones: dict[str, int] = {}
        for row in rows:
            stable = Path(row["stable_path"])
            if row["record_kind"].startswith("change-"):
                changes.setdefault(stable.parent.as_posix(), set()).add(stable.name)
            else:
                stage = stable.parts[3]
                tombstones[stage] = tombstones.get(stage, 0) + 1
            self.assertEqual(row["legacy_archive_commit"], archive_recovery.WORK107_LEGACY_ARCHIVE_COMMIT)
            actual_blob = subprocess.run(
                ["git", "rev-parse", f'{row["legacy_archive_commit"]}:{row["legacy_path"]}'],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertEqual(row["legacy_envelope_blob"], actual_blob)

        shapes = [frozenset(leaves) for leaves in changes.values()]
        self.assertEqual(len(changes), 41)
        self.assertEqual(shapes.count(frozenset({"plan.md", "task.md"})), 35)
        self.assertEqual(shapes.count(frozenset({"plan.md"})), 2)
        self.assertEqual(shapes.count(frozenset({"task.md"})), 4)
        self.assertEqual(
            tombstones,
            {
                "01.requirements": 3,
                "02.architecture": 8,
                "03.specs": 4,
                "05.operations": 2,
            },
        )

    def test_work107_ledger_round_trip_and_closed_mutations(self) -> None:
        rows = archive_recovery.build_work107_migration_rows(ROOT)
        rendered = archive_recovery.render_work107_migration_document(rows)
        parsed = archive_recovery.parse_work107_migration_document(rendered)
        self.assertEqual(parsed, rows)
        self.assertEqual(tuple(parsed[0]), archive_recovery.WORK107_LEDGER_FIELDS)

        mutations = []
        duplicate = [dict(row) for row in rows]
        duplicate[-1]["stable_path"] = duplicate[-2]["stable_path"]
        mutations.append(duplicate)
        wrong_action = [dict(row) for row in rows]
        wrong_action[0]["action"] = "merged"
        mutations.append(wrong_action)
        wrong_object = [dict(row) for row in rows]
        wrong_object[0]["legacy_envelope_blob"] = "0" * 40
        mutations.append(wrong_object)
        missing = [dict(row) for row in rows]
        missing.pop()
        mutations.append(missing)

        for mutation in mutations:
            with self.subTest(mutation=json.dumps(mutation[0], sort_keys=True)[:80]):
                with self.assertRaises(ArchiveContractError):
                    archive_recovery.validate_work107_migration_rows(ROOT, mutation)

    def test_work107_stable_wrapper_preserves_payload_and_dual_recovery(self) -> None:
        rows = archive_recovery.build_work107_migration_rows(ROOT)
        change = next(row for row in rows if row["record_kind"] == "change-plan")
        tombstone = next(row for row in rows if row["record_kind"] == "tombstone")

        for row in (change, tombstone):
            legacy = subprocess.run(
                ["git", "show", f'{row["legacy_archive_commit"]}:{row["legacy_path"]}'],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            legacy_parsed = parse_archive_envelope(legacy)
            terminal = archive_recovery.render_work107_stable_envelope(legacy, row)
            terminal_parsed = parse_archive_envelope(terminal)

            self.assertEqual(terminal_parsed.payload, legacy_parsed.payload)
            for key in ("source_commit", "source_blob", "content_sha256"):
                self.assertEqual(terminal_parsed.metadata[key], legacy_parsed.metadata[key])
            if row["record_kind"].startswith("change-"):
                self.assertEqual(
                    terminal_parsed.metadata["change_id"],
                    row["artifact_id"].removeprefix("PLAN-").removeprefix("TASK-"),
                )

            recovered = archive_recovery.recover_work107_legacy_envelope(ROOT, row)
            self.assertEqual(recovered.payload, legacy_parsed.payload)
            self.assertEqual(recovered.metadata, legacy_parsed.metadata)


if __name__ == "__main__":
    unittest.main()
