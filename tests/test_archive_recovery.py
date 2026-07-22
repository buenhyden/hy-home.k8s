#!/usr/bin/env python3
"""Focused fixture tests for the private ARWB-001 recovery capability."""

from __future__ import annotations

import hashlib
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
            "replacement": "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
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
            "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md",
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
        real_run = subprocess.run

        def capture(
            *args: object, **kwargs: object
        ) -> subprocess.CompletedProcess[bytes]:
            observed.append((list(args[0]), dict(kwargs)))
            return real_run(*args, **kwargs)

        with mock.patch.dict(os.environ, hostile, clear=False):
            with mock.patch.object(
                archive_recovery.subprocess, "run", side_effect=capture
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
            self.assertEqual(kwargs["timeout"], archive_recovery.GIT_TIMEOUT_SECONDS)

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
            "run",
            side_effect=FileNotFoundError("STARTUP-SENTINEL"),
        ):
            with self.assertRaisesRegex(
                ArchiveContractError,
                r"^RECOVERY-GIT-STARTUP:",
            ) as startup:
                recover_git_blob(self.root, self.original_path, self.commit)
        self.assertNotIn("STARTUP-SENTINEL", str(startup.exception))

        with mock.patch.object(
            archive_recovery.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(
                cmd=["git", "TIMEOUT-SENTINEL"],
                timeout=0.001,
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
                    archive_recovery.subprocess,
                    "run",
                    side_effect=responses,
                ):
                    with self.assertRaisesRegex(
                        ArchiveContractError,
                        r"^RECOVERY-OBJECT-FORMAT:",
                    ):
                        recover_git_blob(self.root, self.original_path, self.commit)

    def test_rejects_worktree_byte_substitution(self) -> None:
        recovered = recover_git_blob(self.root, self.original_path, self.commit)
        substitute = self.payload.replace(b"\n", b"\r\n")

        with self.assertRaisesRegex(
            ArchiveContractError,
            r"^ARCHIVE-PAYLOAD-NOT-SOURCE-BLOB:",
        ):
            render_fixture_archive_envelope(self.metadata(), recovered, substitute)


if __name__ == "__main__":
    unittest.main()
