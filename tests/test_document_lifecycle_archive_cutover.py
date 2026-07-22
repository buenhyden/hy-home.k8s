"""Finite ARWB-003 lifecycle admission regressions."""

from __future__ import annotations

import importlib.util
import inspect
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "validate-document-lifecycle.py"
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_cutover_tested", MODULE_PATH
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError(f"cannot load lifecycle validator from {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from archive_cutover import (  # noqa: E402
    ARCHIVE_PROFILE,
    ARCHIVE_TEMPLATE,
    CUTOVER_BASE_COMMIT,
    EXPECTED_ARCHIVE_PATHS,
)
import archive_cutover_manifest as CUTOVER_MANIFEST  # noqa: E402
from document_contracts import load_registry  # noqa: E402
from document_lifecycle import LifecycleDocument  # noqa: E402


LEGACY_PROFILE = "content/archive-tombstone"
LEGACY_TEMPLATE_PROFILE = "template/content/archive-tombstone"
NEW_TEMPLATE_PROFILE = "template/content/archive"
LEGACY_TEMPLATE = PurePosixPath(
    "docs/99.templates/templates/common/archive-tombstone.template.md"
)
NEW_TEMPLATE = PurePosixPath(ARCHIVE_TEMPLATE)
REGISTRY_PATH = "docs/99.templates/support/document-profiles.json"
BASE_REGISTRY_BLOB_OID = getattr(CUTOVER_MANIFEST, "BASE_REGISTRY_BLOB_OID", "")
PROPOSED_REGISTRY_BLOB_OID = getattr(CUTOVER_MANIFEST, "PROPOSED_REGISTRY_BLOB_OID", "")
CUTOVER_PROPOSED_COMMIT = getattr(CUTOVER_MANIFEST, "CUTOVER_PROPOSED_COMMIT", "")
GIT_EXECUTABLE = Path("/usr/bin/git")
GIT_TIMEOUT_SECONDS = 10
GIT_OBJECT_ID = re.compile(r"[0-9a-f]{40}")
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "PATH": "/usr/bin:/bin",
}


class GitFixtureResolutionError(RuntimeError):
    """Raised when an immutable Git fixture cannot be resolved exactly."""


def run_closed_git(*arguments: str) -> str:
    try:
        completed = subprocess.run(
            [
                str(GIT_EXECUTABLE),
                "--no-replace-objects",
                "-c",
                "core.attributesFile=/dev/null",
                "-c",
                "core.excludesFile=/dev/null",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.hooksPath=/dev/null",
                *arguments,
            ],
            cwd=ROOT,
            check=True,
            env=CLOSED_GIT_ENVIRONMENT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise GitFixtureResolutionError(
            "immutable Git fixture resolution failed"
        ) from error
    output = completed.stdout.strip()
    if not output or len(output.splitlines()) != 1:
        raise GitFixtureResolutionError("immutable Git fixture output is invalid")
    return output


def committed_blob_oid(commit_oid: str, path: str) -> str:
    if GIT_OBJECT_ID.fullmatch(commit_oid) is None:
        raise GitFixtureResolutionError("fixture commit identity is invalid")
    posix_path = PurePosixPath(path)
    if (
        not path
        or posix_path.is_absolute()
        or posix_path.as_posix() != path
        or any(part in {".", ".."} for part in posix_path.parts)
        or ":" in path
    ):
        raise GitFixtureResolutionError("fixture path is invalid")

    if run_closed_git("cat-file", "-t", commit_oid) != "commit":
        raise GitFixtureResolutionError("fixture identity is not a commit")

    blob_oid = run_closed_git("rev-parse", "--verify", f"{commit_oid}:{path}")
    if GIT_OBJECT_ID.fullmatch(blob_oid) is None:
        raise GitFixtureResolutionError("fixture blob identity is invalid")
    if run_closed_git("cat-file", "-t", blob_oid) != "blob":
        raise GitFixtureResolutionError("fixture path does not resolve to a blob")
    return blob_oid


def registry(version: int) -> dict[str, object]:
    if version == 7:
        profile_ids = (LEGACY_PROFILE, LEGACY_TEMPLATE_PROFILE)
    else:
        profile_ids = (ARCHIVE_PROFILE, NEW_TEMPLATE_PROFILE)
    return {
        "$id": f"https://hy-home.k8s/schemas/document-profiles-{version}.schema.json",
        "schemaVersion": version,
        "profiles": [{"id": profile_id} for profile_id in profile_ids],
    }


def exact_documents() -> tuple[
    dict[PurePosixPath, LifecycleDocument],
    dict[PurePosixPath, LifecycleDocument],
]:
    base = {
        PurePosixPath(path): LifecycleDocument(
            PurePosixPath(path), LEGACY_PROFILE, "archived"
        )
        for path in EXPECTED_ARCHIVE_PATHS
    }
    proposed = {
        PurePosixPath(path): LifecycleDocument(
            PurePosixPath(path), ARCHIVE_PROFILE, "archived"
        )
        for path in EXPECTED_ARCHIVE_PATHS
    }
    base[LEGACY_TEMPLATE] = LifecycleDocument(
        LEGACY_TEMPLATE, LEGACY_TEMPLATE_PROFILE, None
    )
    proposed[NEW_TEMPLATE] = LifecycleDocument(NEW_TEMPLATE, NEW_TEMPLATE_PROFILE, None)
    return base, proposed


class FiniteArchiveCutoverAdmissionTest(unittest.TestCase):
    def _admit(
        self,
        *,
        mode: str = "staged",
        base_commit: str = CUTOVER_BASE_COMMIT,
        base_registry_oid: str = BASE_REGISTRY_BLOB_OID,
        proposed_registry_oid: str = PROPOSED_REGISTRY_BLOB_OID,
        base_registry: dict[str, object] | None = None,
        proposed_registry: dict[str, object] | None = None,
        base_documents: dict[PurePosixPath, LifecycleDocument] | None = None,
        proposed_documents: dict[PurePosixPath, LifecycleDocument] | None = None,
    ) -> frozenset[PurePosixPath]:
        admission = getattr(VALIDATOR, "finite_archive_cutover_paths", None)
        self.assertTrue(callable(admission), "finite cutover admission is missing")
        exact_base, exact_proposed = exact_documents()
        kwargs = {
            "mode": mode,
            "base_commit": base_commit,
            "base_registry": base_registry or registry(7),
            "proposed_registry": proposed_registry or registry(8),
            "base_documents": base_documents or exact_base,
            "proposed_documents": proposed_documents or exact_proposed,
        }
        parameters = inspect.signature(admission).parameters
        if {"base_registry_oid", "proposed_registry_oid"} <= set(parameters):
            kwargs["base_registry_oid"] = base_registry_oid
            kwargs["proposed_registry_oid"] = proposed_registry_oid
        return admission(
            **kwargs,
        )

    def test_manifest_registry_blob_oids_match_exact_git_objects(self):
        base = committed_blob_oid(CUTOVER_BASE_COMMIT, REGISTRY_PATH)
        proposed = committed_blob_oid(CUTOVER_PROPOSED_COMMIT, REGISTRY_PATH)
        self.assertEqual(BASE_REGISTRY_BLOB_OID, base)
        self.assertEqual(PROPOSED_REGISTRY_BLOB_OID, proposed)

    def test_manifest_oid_resolution_ignores_hostile_git_environment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            hostile_root = Path(temporary_directory)
            hostile_environment = {
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(hostile_root / "alternates"),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.repositoryformatversion",
                "GIT_CONFIG_VALUE_0": "999",
                "GIT_CONFIG_GLOBAL": str(hostile_root / "global.gitconfig"),
                "GIT_CONFIG_SYSTEM": str(hostile_root / "system.gitconfig"),
                "GIT_DIR": str(hostile_root / "missing.git"),
                "GIT_OBJECT_DIRECTORY": str(hostile_root / "objects"),
                "GIT_REPLACE_REF_BASE": "refs/hostile-replacements/",
                "GIT_WORK_TREE": str(hostile_root / "worktree"),
            }
            with mock.patch.dict(os.environ, hostile_environment, clear=False):
                self.test_manifest_registry_blob_oids_match_exact_git_objects()

    def test_manifest_oid_resolution_enforces_closed_git_invocation(self):
        completed = subprocess.CompletedProcess(
            args=(), returncode=0, stdout="commit\n", stderr=""
        )
        with mock.patch.object(subprocess, "run", return_value=completed) as git_run:
            self.assertEqual(
                run_closed_git("cat-file", "-t", CUTOVER_BASE_COMMIT), "commit"
            )

        command = git_run.call_args.args[0]
        options = git_run.call_args.kwargs
        self.assertEqual(command[0], "/usr/bin/git")
        self.assertIn("--no-replace-objects", command)
        self.assertEqual(options["env"], CLOSED_GIT_ENVIRONMENT)
        self.assertEqual(options["env"]["GIT_NO_REPLACE_OBJECTS"], "1")
        self.assertNotIn("GIT_DIR", options["env"])
        self.assertEqual(options["env"]["GIT_CONFIG_GLOBAL"], "/dev/null")
        self.assertEqual(options["env"]["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertTrue(options["check"])
        self.assertEqual(options["timeout"], GIT_TIMEOUT_SECONDS)

    def test_manifest_oid_resolution_rejects_invalid_git_objects(self):
        for malformed_commit in ("", "HEAD", "0" * 39, "G" * 40):
            with self.subTest(malformed_commit=malformed_commit):
                with self.assertRaises(GitFixtureResolutionError):
                    committed_blob_oid(malformed_commit, REGISTRY_PATH)

        with self.assertRaises(GitFixtureResolutionError):
            committed_blob_oid("0" * 40, REGISTRY_PATH)
        with self.assertRaises(GitFixtureResolutionError):
            committed_blob_oid(PROPOSED_REGISTRY_BLOB_OID, REGISTRY_PATH)

    def test_exact_staged_and_ci_cutover_consume_only_finite_manifest(self):
        expected = frozenset(PurePosixPath(path) for path in EXPECTED_ARCHIVE_PATHS) | {
            LEGACY_TEMPLATE,
            NEW_TEMPLATE,
        }
        self.assertEqual(self._admit(mode="staged"), expected)
        self.assertEqual(self._admit(mode="ci"), expected)

    def test_partial_manifest_is_not_admitted(self):
        base, proposed = exact_documents()
        proposed.pop(PurePosixPath(EXPECTED_ARCHIVE_PATHS[0]))
        self.assertFalse(self._admit(base_documents=base, proposed_documents=proposed))

    def test_extra_archive_path_is_not_admitted(self):
        base, proposed = exact_documents()
        extra = PurePosixPath("docs/98.archive/03.specs/999-extra/spec.md")
        base[extra] = LifecycleDocument(extra, LEGACY_PROFILE, "archived")
        proposed[extra] = LifecycleDocument(extra, ARCHIVE_PROFILE, "archived")
        self.assertFalse(self._admit(base_documents=base, proposed_documents=proposed))

    def test_wrong_base_is_not_admitted(self):
        self.assertFalse(self._admit(base_commit="0" * 40))

    def test_wrong_base_or_proposed_registry_blob_oid_is_not_admitted(self):
        self.assertFalse(self._admit(base_registry_oid="0" * 40))
        self.assertFalse(self._admit(proposed_registry_oid="f" * 40))

    def test_same_ids_policy_drift_blob_oid_is_not_admitted(self):
        proposed_registry = registry(8)
        proposed_registry["unrelatedPolicy"] = {"mode": "changed"}
        drift_bytes = json.dumps(
            proposed_registry, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        drift_oid = (
            subprocess.run(
                ["git", "hash-object", "--stdin"],
                cwd=ROOT,
                check=True,
                input=drift_bytes,
                stdout=subprocess.PIPE,
            )
            .stdout.decode("ascii")
            .strip()
        )
        self.assertNotEqual(drift_oid, PROPOSED_REGISTRY_BLOB_OID)
        self.assertFalse(
            self._admit(
                proposed_registry=proposed_registry,
                proposed_registry_oid=drift_oid,
            )
        )

    def test_missing_template_pair_is_not_admitted(self):
        base, proposed = exact_documents()
        proposed.pop(NEW_TEMPLATE)
        self.assertFalse(self._admit(base_documents=base, proposed_documents=proposed))

    def test_registry_version_or_profile_pair_drift_is_not_admitted(self):
        wrong_version = registry(8)
        wrong_version["schemaVersion"] = 9
        self.assertFalse(self._admit(proposed_registry=wrong_version))

        wrong_profiles = registry(8)
        wrong_profiles["profiles"] = [{"id": ARCHIVE_PROFILE}]
        self.assertFalse(self._admit(proposed_registry=wrong_profiles))

    def test_unrelated_profile_change_is_not_admitted(self):
        base, proposed = exact_documents()
        unrelated = PurePosixPath("docs/03.specs/999-unrelated/spec.md")
        base[unrelated] = LifecycleDocument(unrelated, "sdlc/spec", "active")
        proposed[unrelated] = LifecycleDocument(unrelated, "sdlc/guide", "active")
        self.assertFalse(self._admit(base_documents=base, proposed_documents=proposed))

    def test_snapshot_or_explicit_ref_mode_is_not_admitted(self):
        self.assertFalse(self._admit(mode="snapshot"))
        self.assertFalse(self._admit(mode="explicit-ref"))


class LifecycleArchiveImmutabilityOperatingTest(unittest.TestCase):
    original_path = "docs/03.specs/900-fixture/spec.md"
    archive_path = "docs/98.archive/03.specs/900-fixture/spec.md"

    @staticmethod
    def _git(root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 0:
            raise AssertionError(completed.stderr)
        return completed.stdout.strip()

    @classmethod
    def _archive_bytes(cls) -> bytes:
        return (
            b"---\n"
            b'title: "Archive fixture"\n'
            b'type: "content/archive"\n'
            b'status: "archived"\n'
            b'owner: "platform"\n'
            b'updated: "2026-07-19"\n'
            b'original_type: "sdlc/spec"\n'
            + f'original_path: "{cls.original_path}"\n'.encode()
            + b'archived_on: "2026-07-19"\n'
            + b'archive_reason: "superseded"\n'
            + b'replacement: "docs/03.specs/036-archive-record-and-workspace-boundary/spec.md"\n'
            + b'source_commit: "0000000000000000000000000000000000000000"\n'
            + b'source_blob: "1111111111111111111111111111111111111111"\n'
            + b'content_sha256: "2222222222222222222222222222222222222222222222222222222222222222"\n'
            + b"---\n"
            + b"<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->\n"
            + b"# Historical payload\n"
        )

    @staticmethod
    def _source_bytes() -> bytes:
        return (
            b"---\n"
            b'title: "Source fixture"\n'
            b'type: "sdlc/spec"\n'
            b'status: "done"\n'
            b'owner: "platform"\n'
            b'updated: "2026-07-19"\n'
            b"---\n\n"
            b"# Source fixture\n"
        )

    def _repository(
        self, *, archived: bool
    ) -> tuple[tempfile.TemporaryDirectory, Path, str]:
        temporary = tempfile.TemporaryDirectory(prefix="lifecycle-archive-bytes-")
        root = Path(temporary.name)
        self._git(root, "init", "--quiet")
        self._git(root, "config", "user.email", "fixture@example.invalid")
        self._git(root, "config", "user.name", "Lifecycle Archive Fixture")
        registry_path = root / REGISTRY_PATH
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_bytes((ROOT / REGISTRY_PATH).read_bytes())
        document_path = root / (self.archive_path if archived else self.original_path)
        document_path.parent.mkdir(parents=True, exist_ok=True)
        document_path.write_bytes(
            self._archive_bytes() if archived else self._source_bytes()
        )
        self._git(
            root, "add", "--", REGISTRY_PATH, document_path.relative_to(root).as_posix()
        )
        self._git(root, "commit", "--quiet", "-m", "base")
        return temporary, root, self._git(root, "rev-parse", "HEAD")

    def _mutate_archive(self, root: Path, mutation: str) -> None:
        path = root / self.archive_path
        content = path.read_bytes()
        if mutation == "metadata":
            content = content.replace(b'owner: "platform"', b'owner: "security"', 1)
        elif mutation == "payload":
            content = content.replace(
                b"# Historical payload\n", b"# Historical payload!\n", 1
            )
        else:  # pragma: no cover - test helper boundary
            raise AssertionError(mutation)
        path.write_bytes(content)
        self._git(root, "add", "--", self.archive_path)

    def _create_archive(self, root: Path) -> None:
        (root / self.original_path).unlink()
        archive = root / self.archive_path
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(self._archive_bytes())
        self._git(root, "add", "-A", "--", "docs")

    def test_staged_rejects_metadata_and_payload_byte_mutation(self) -> None:
        registry = load_registry(ROOT)
        for mutation in ("metadata", "payload"):
            with self.subTest(mutation=mutation):
                temporary, root, _base = self._repository(archived=True)
                with temporary:
                    self._mutate_archive(root, mutation)
                    diagnostics = VALIDATOR._evaluate_comparison(
                        root,
                        registry,
                        mode="staged",
                    )
                self.assertEqual(
                    [(item.rule_id, item.path.as_posix()) for item in diagnostics],
                    [("LIFECYCLE-EVIDENCE", self.archive_path)],
                )

    def test_explicit_ref_rejects_metadata_and_payload_byte_mutation(self) -> None:
        registry = load_registry(ROOT)
        for mutation in ("metadata", "payload"):
            with self.subTest(mutation=mutation):
                temporary, root, base = self._repository(archived=True)
                with temporary:
                    self._mutate_archive(root, mutation)
                    self._git(root, "commit", "--quiet", "-m", "mutation")
                    proposed = self._git(root, "rev-parse", "HEAD")
                    diagnostics = VALIDATOR._evaluate_comparison(
                        root,
                        registry,
                        mode="explicit-ref",
                        from_ref=base,
                        to_ref=proposed,
                    )
                self.assertEqual(
                    [(item.rule_id, item.path.as_posix()) for item in diagnostics],
                    [("LIFECYCLE-EVIDENCE", self.archive_path)],
                )

    def test_staged_and_explicit_ref_allow_new_archive_creation_contract(self) -> None:
        registry = load_registry(ROOT)
        for mode in ("staged", "explicit-ref"):
            with self.subTest(mode=mode):
                temporary, root, base = self._repository(archived=False)
                with temporary:
                    self._create_archive(root)
                    kwargs: dict[str, object] = {"mode": mode}
                    if mode == "explicit-ref":
                        self._git(root, "commit", "--quiet", "-m", "archive")
                        kwargs.update(
                            from_ref=base,
                            to_ref=self._git(root, "rev-parse", "HEAD"),
                        )
                    diagnostics = VALIDATOR._evaluate_comparison(
                        root,
                        registry,
                        **kwargs,
                    )
                self.assertEqual(diagnostics, ())


if __name__ == "__main__":
    unittest.main()
