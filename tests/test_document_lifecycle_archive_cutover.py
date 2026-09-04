"""Finite ARWB-003 lifecycle admission regressions."""

from __future__ import annotations

import importlib.util
import inspect
import hashlib
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
import archive_cutover as ARCHIVE_CUTOVER  # noqa: E402
import archive_cutover_manifest as CUTOVER_MANIFEST  # noqa: E402
import document_contracts  # noqa: E402
import document_lifecycle as lifecycle  # noqa: E402
from archive_recovery import (  # noqa: E402
    WP004C_SEALED_TARGET_COMMIT,
)
from document_contracts import DocumentContractError, load_registry  # noqa: E402
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    LifecycleRename,
    compare_lifecycle,
)


LEGACY_PROFILE = "content/archive-tombstone"
LEGACY_TEMPLATE_PROFILE = "template/content/archive-tombstone"
NEW_TEMPLATE_PROFILE = "common/template-archive-tombstone"
LEGACY_TEMPLATE = PurePosixPath(
    "docs/99.templates/templates/common/archive-tombstone.template.md"
)
NEW_TEMPLATE = PurePosixPath(ARCHIVE_TEMPLATE)
REGISTRY_PATH = "docs/99.templates/registry.json"
HISTORICAL_ARWB_REGISTRY_PATH = "docs/99.templates/support/document-profiles.json"
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
        base = committed_blob_oid(CUTOVER_BASE_COMMIT, HISTORICAL_ARWB_REGISTRY_PATH)
        proposed = committed_blob_oid(
            CUTOVER_PROPOSED_COMMIT, HISTORICAL_ARWB_REGISTRY_PATH
        )
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
                    committed_blob_oid(malformed_commit, HISTORICAL_ARWB_REGISTRY_PATH)

        with self.assertRaises(GitFixtureResolutionError):
            committed_blob_oid("0" * 40, HISTORICAL_ARWB_REGISTRY_PATH)
        with self.assertRaises(GitFixtureResolutionError):
            committed_blob_oid(
                PROPOSED_REGISTRY_BLOB_OID,
                HISTORICAL_ARWB_REGISTRY_PATH,
            )

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
        unrelated = PurePosixPath("docs/03.specs/0999-unrelated/spec.md")
        base[unrelated] = LifecycleDocument(unrelated, "sdlc/spec", "active")
        proposed[unrelated] = LifecycleDocument(unrelated, "operation/guide", "active")
        self.assertFalse(self._admit(base_documents=base, proposed_documents=proposed))

    def test_snapshot_or_explicit_ref_mode_is_not_admitted(self):
        self.assertFalse(self._admit(mode="snapshot"))
        self.assertFalse(self._admit(mode="explicit-ref"))


class _RetiredWork054Wp002TransitionAdmission:
    """The WP-002 exception is one evidence-bound transition, not a bypass."""

    def _admit(self, *, mode: str = "staged", mutation: str = "exact"):
        fixture = getattr(VALIDATOR, "_work054_wp002_transition_fixture_inputs", None)
        admission = getattr(VALIDATOR, "finite_work054_wp002_transition_paths", None)
        self.assertTrue(callable(fixture), "WP-002 transition fixture is missing")
        self.assertTrue(callable(admission), "WP-002 transition admission is missing")
        return admission(**fixture(ROOT, mode, mutation))

    def test_wp004b_corpus_closes_the_old_wp002_transition_admission(self):
        staged = self._admit(mode="staged")
        ci = self._admit(mode="ci")
        self.assertEqual(staged, frozenset())
        self.assertEqual(ci, staged)

    def test_unknown_retired_profile_alias_still_fails_closed(self):
        current = VALIDATOR.load_registry(ROOT)
        raw = json.loads(
            (ROOT / "docs/99.templates/support/document-profiles.json").read_text(
                encoding="utf-8"
            )
        )
        raw["profiles"][0]["id"] = "sdlc/prd-typo"
        with self.assertRaisesRegex(
            VALIDATOR.InvocationError,
            "comparison registry profile has no current lifecycle projection",
        ):
            VALIDATOR._classification_registry(current, raw)

    def test_authority_manifest_and_target_drift_fail_closed(self):
        for mutation in (
            "wrong-base",
            "missing-migration",
            "missing-ledger-row",
            "extra-ledger-row",
            "source-blob-drift",
            "source-digest-drift",
            "replacement-drift",
            "target-artifact-drift",
            "standalone-lineage-drift",
            "missing-spec-transition",
            "missing-decision",
            "decision-blob-drift",
        ):
            with self.subTest(mutation=mutation):
                self.assertFalse(self._admit(mutation=mutation))

    def test_transition_is_not_a_generic_create_delete_or_ref_exception(self):
        self.assertFalse(self._admit(mode="snapshot"))
        self.assertFalse(self._admit(mode="explicit-ref"))

    def test_mig0002_full_document_pin_rejects_trailing_and_oversize_bytes(self):
        raw = (ROOT / VALIDATOR.WORK054_WP002_MIGRATION_PATH).read_bytes()
        self.assertEqual(len(VALIDATOR._work054_wp002_migration_rows(raw)), 154)
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            VALIDATOR.WORK054_WP002_MIGRATION_SHA256,
        )
        for name, candidate in (
            ("trailing", raw + b"\nUnreviewed trailing prose.\n"),
            (
                "oversize",
                raw + b"x" * (VALIDATOR.MIGRATION_DOCUMENT_MAX_BYTES + 1 - len(raw)),
            ),
        ):
            with self.subTest(name=name), self.assertRaises(VALIDATOR.InvocationError):
                VALIDATOR._work054_wp002_migration_rows(candidate)


class FiniteWork054Wp003AgentGovernanceAdmissionTest(unittest.TestCase):
    """MIG-0003 admits only its three exact legacy owner deletions."""

    migration_path = VALIDATOR.WORK054_WP003_MIGRATION_PATH

    def _snapshot(self):
        raw = (ROOT / self.migration_path).read_bytes()
        base = {
            PurePosixPath(str(row["legacy_path"])): str(row["source_blob"])
            for row in VALIDATOR.WORK054_WP003_OWNER_RETIREMENTS
        }
        proposed = {self.migration_path: VALIDATOR._git_blob_oid(raw)}
        proposed.update(
            {
                PurePosixPath(str(row["replacement"])): "f" * 40
                for row in VALIDATOR.WORK054_WP003_OWNER_RETIREMENTS
            }
        )
        return raw, base, proposed

    def _admit(
        self,
        *,
        base_commit: str = VALIDATOR.WORK054_WP003_BASE_COMMIT,
        base_blobs=None,
        proposed_blobs=None,
    ):
        _raw, exact_base, exact_proposed = self._snapshot()
        return VALIDATOR.finite_work054_wp003_agent_governance_paths(
            root=ROOT,
            mode="staged",
            base_commit=base_commit,
            base_blobs=base_blobs if base_blobs is not None else exact_base,
            proposed_blobs=(
                proposed_blobs if proposed_blobs is not None else exact_proposed
            ),
        )

    def test_exact_projection_admits_only_four_paths(self):
        _raw, base, _proposed = self._snapshot()
        expected = frozenset({self.migration_path, *base})
        self.assertEqual(self._admit(), expected)
        self.assertEqual(len(expected), 4)

    def test_authority_digest_and_endpoint_drift_fail_closed(self):
        raw, base, proposed = self._snapshot()
        legacy = next(iter(base))
        replacement = PurePosixPath(
            str(VALIDATOR.WORK054_WP003_OWNER_RETIREMENTS[0]["replacement"])
        )
        mutations = {
            "wrong-base": {
                "base_commit": "0" * 40,
                "base_blobs": base,
                "proposed_blobs": proposed,
            },
            "partial-legacy-retention": {
                "base_blobs": base,
                "proposed_blobs": {**proposed, legacy: base[legacy]},
            },
            "missing-replacement": {
                "base_blobs": base,
                "proposed_blobs": {
                    path: oid for path, oid in proposed.items() if path != replacement
                },
            },
        }
        for name, kwargs in mutations.items():
            with self.subTest(name=name):
                self.assertFalse(self._admit(**kwargs))
        with (
            self.subTest(name="migration-digest-drift"),
            mock.patch.object(
                VALIDATOR,
                "_blob_bytes",
                return_value=raw + b"\n",
            ),
        ):
            self.assertFalse(self._admit(base_blobs=base, proposed_blobs=proposed))


class ArchiveCutoverMigrationGraphTests(unittest.TestCase):
    """Archive replacements resolve through the sealed migration graph."""

    def test_exact_multi_hop_graph_resolves_to_current_profiles(self):
        edges = {
            "docs/legacy.md": "docs/intermediate.md",
            "docs/intermediate.md": "docs/current.md",
            "docs/current-self.md": "docs/current-self.md",
        }
        profiles = {
            "docs/current.md": "sdlc/plan",
            "docs/current-self.md": "sdlc/requirement",
        }
        self.assertEqual(
            ARCHIVE_CUTOVER._resolve_migration_graph(edges, profiles),
            {
                "docs/current-self.md": "docs/current-self.md",
                "docs/intermediate.md": "docs/current.md",
                "docs/legacy.md": "docs/current.md",
            },
        )

    def test_graph_rejects_cycle_unknown_missing_and_wrong_profile(self):
        cases = (
            (
                "cycle",
                {"docs/a.md": "docs/b.md", "docs/b.md": "docs/a.md"},
                {},
            ),
            ("unknown", {"docs/a.md": "docs/unknown.md"}, {}),
            (
                "missing-target",
                {"docs/a.md": "docs/missing.md"},
                {"docs/current.md": "sdlc/plan"},
            ),
            (
                "wrong-profile",
                {"docs/a.md": "docs/archive.md"},
                {"docs/archive.md": ARCHIVE_PROFILE},
            ),
        )
        for name, edges, profiles in cases:
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                ARCHIVE_CUTOVER._resolve_migration_graph(edges, profiles)


class DocumentAuthorityLifecycleTests(unittest.TestCase):
    @staticmethod
    def _wp004b_committed_transition():
        migration_path = VALIDATOR.WORK054_WP004B_MIGRATION_PATH.as_posix()
        target_commit = run_closed_git(
            "log",
            "--format=%H",
            "--diff-filter=A",
            "--",
            migration_path,
        )
        proposed = VALIDATOR._tree_blob_map(ROOT, target_commit)
        rows = VALIDATOR.parse_pinned_migration_control(
            migration_path,
            VALIDATOR._blob_bytes(
                ROOT,
                proposed[VALIDATOR.WORK054_WP004B_MIGRATION_PATH],
            ),
        )
        source_commits = {row.get("source_commit") for row in rows}
        if len(source_commits) != 1:
            raise AssertionError("MIG-0004 must name one transition source commit")
        base_commit = source_commits.pop()
        if not isinstance(base_commit, str):
            raise AssertionError("MIG-0004 source commit is malformed")
        return (
            base_commit,
            target_commit,
            VALIDATOR._tree_blob_map(ROOT, base_commit),
            proposed,
        )

    @staticmethod
    def _wp004b_admitted(base_commit, base, proposed):
        return VALIDATOR.finite_work054_wp004b_document_authority_paths(
            root=ROOT,
            mode="ci",
            base_commit=base_commit,
            base_blobs=base,
            proposed_blobs=proposed,
        )

    @staticmethod
    def _mutation_result(base_commit, base, proposed, path, mutation):
        original_blob_reader = VALIDATOR._blob_bytes
        sentinel = "f" * 40
        changed = dict(proposed)
        changed[path] = sentinel

        def read_blob(root, oid, **kwargs):
            if oid == sentinel:
                return mutation
            return original_blob_reader(root, oid, **kwargs)

        with mock.patch.object(VALIDATOR, "_blob_bytes", side_effect=read_blob):
            return DocumentAuthorityLifecycleTests._wp004b_admitted(
                base_commit,
                base,
                changed,
            )

    @staticmethod
    def _authority():
        path = ROOT / "scripts/document_authority.py"
        specification = importlib.util.spec_from_file_location(
            "document_lifecycle_authority", path
        )
        if specification is None or specification.loader is None:
            raise AssertionError("document authority module could not be loaded")
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        return module

    def test_real_registry_edge_list_accepts_legal_and_rejects_illegal(self):
        authority = self._authority()
        registry = json.loads(
            (ROOT / authority.REGISTRY_PATH).read_text(encoding="utf-8")
        )
        lifecycle = next(
            domain
            for domain in registry["lifecycle_domains"]
            if domain["family"] == "requirement-architecture"
        )
        self.assertTrue(
            authority.is_lifecycle_transition_allowed(lifecycle, "draft", "active")
        )
        self.assertFalse(
            authority.is_lifecycle_transition_allowed(lifecycle, "draft", "accepted")
        )
        self.assertFalse(
            authority.is_lifecycle_transition_allowed(lifecycle, "draft", "retired")
        )

    def test_loaded_registry_types_terminal_domains_and_owns_transition_projection(
        self,
    ):
        registry = load_registry(ROOT)
        # 12 before the content/audit, content/research and content/data
        # families retired with their unroutable profiles, 9 while the three
        # reference roles carried a domain no graph governed, and 12 again now
        # that each role declares the lifecycle Spec 0054 names for it.
        self.assertEqual(len(registry.lifecycle_domains), 12)
        requirement = next(
            domain
            for domain in registry.lifecycle_domains
            if domain.family == "requirement-architecture"
        )
        self.assertEqual(requirement.validation_class("active"), "current")
        self.assertTrue(requirement.allows("draft", "active"))
        self.assertFalse(requirement.allows("draft", "retired"))
        raw = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        self.assertIn("lifecycle_domains", raw)
        self.assertNotIn("transition_lifecycle_contracts", raw)

    def _retired_wp004b_committed_document_authority_cutover_is_finitely_admitted(self):
        base_commit, target_commit, base, proposed = self._wp004b_committed_transition()
        accepted = self._wp004b_admitted(base_commit, base, proposed)
        self.assertTrue(accepted)

        diagnostics = VALIDATOR._evaluate_comparison(
            ROOT,
            load_registry(ROOT),
            mode="ci",
            base_ref=base_commit,
            to_ref=target_commit,
        )
        self.assertEqual(diagnostics, ())

        with mock.patch.object(
            VALIDATOR,
            "_work054_wp004b_admission",
            return_value=VALIDATOR._EMPTY_WORK054_WP004B_ADMISSION,
        ):
            diagnostics_without_admission = VALIDATOR._evaluate_comparison(
                ROOT,
                load_registry(ROOT),
                mode="ci",
                base_ref=base_commit,
                to_ref=target_commit,
            )
        self.assertTrue(diagnostics_without_admission)

    def _retired_wp004b_finite_admission_consumes_only_named_diagnostics(self):
        base_commit, target_commit, _base, proposed = (
            self._wp004b_committed_transition()
        )
        task = next(
            path
            for path in proposed
            if VALIDATOR.WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
        )
        unexpected = VALIDATOR.LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-STATE",
            path=task,
            profile="sdlc/task",
            expected_transition="reviewed finite transition only",
            observed_transition="unexpected admitted-path diagnostic",
            base_mode="ci",
            evidence_gap="synthetic unexpected transition",
        )
        with mock.patch.object(
            VALIDATOR,
            "compare_lifecycle",
            return_value=(unexpected,),
        ):
            diagnostics = VALIDATOR._evaluate_comparison(
                ROOT,
                load_registry(ROOT),
                mode="ci",
                base_ref=base_commit,
                to_ref=target_commit,
            )
        self.assertEqual(diagnostics, (unexpected,))

    def _retired_wp004b_post_cutover_active_requirement_body_edit_is_valid(self):
        _base_commit, target_commit, _base, proposed = (
            self._wp004b_committed_transition()
        )
        current_registry = load_registry(ROOT)
        target_registry = VALIDATOR._classification_registry(
            current_registry,
            VALIDATOR._registry_blob(
                ROOT,
                VALIDATOR._tree_blob_oid(
                    ROOT,
                    target_commit,
                    VALIDATOR.RETIRED_REGISTRY_PATH,
                ),
            ),
        )
        converged_registry = VALIDATOR._wp004b_classification_registry(
            current_registry,
            target_registry,
            authority_converged=True,
        )
        requirement = PurePosixPath(
            "docs/01.requirements/0008-workspace-document-taxonomy-consolidation.md"
        )
        original = VALIDATOR._blob_bytes(ROOT, proposed[requirement]).decode("utf-8")
        changed = original + "\nCurrent traceability prose update.\n"
        base_document = VALIDATOR.document_from_text(
            converged_registry, requirement, original
        )
        proposed_document = VALIDATOR.document_from_text(
            converged_registry, requirement, changed
        )
        self.assertEqual(base_document.profile_id, "sdlc/requirement")
        self.assertEqual(base_document.status, "active")
        self.assertIsNone(base_document.state_issue)
        self.assertEqual(
            VALIDATOR.compare_lifecycle(
                converged_registry,
                {requirement: base_document},
                {requirement: proposed_document},
                base_mode="staged",
            ),
            (),
        )

    def _retired_wp004b_finite_admission_rejects_missing_extra_and_source_drift(self):
        base_commit, _target_commit, base, proposed = (
            self._wp004b_committed_transition()
        )
        accepted = self._wp004b_admitted(base_commit, base, proposed)
        tasks = sorted(
            (
                path
                for path in accepted
                if VALIDATOR.WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
            ),
            key=PurePosixPath.as_posix,
        )
        self.assertTrue(tasks)

        missing = dict(proposed)
        missing.pop(tasks[0])
        extra = dict(proposed)
        extra[PurePosixPath("docs/03.specs/9999-rogue/tasks/tsk-0001-rogue.md")] = (
            "0" * 40
        )
        drifted_base = dict(base)
        legacy_task = next(
            path
            for path in base
            if path.as_posix().endswith(
                "0055-workspace-governance-audit-and-remediation/tasks.md"
            )
        )
        drifted_base[legacy_task] = "0" * 40

        for case_base, case_proposed in (
            (base, missing),
            (base, extra),
            (drifted_base, proposed),
        ):
            self.assertEqual(
                self._wp004b_admitted(
                    base_commit,
                    case_base,
                    case_proposed,
                ),
                frozenset(),
            )

    def _retired_wp004b_finite_admission_binds_task_oid_bytes_and_frontmatter(self):
        base_commit, _target_commit, base, proposed = (
            self._wp004b_committed_transition()
        )
        accepted = self._wp004b_admitted(base_commit, base, proposed)
        tasks = sorted(
            (
                path
                for path in accepted
                if VALIDATOR.WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
            ),
            key=PurePosixPath.as_posix,
        )
        self.assertTrue(tasks)
        task = next(
            path
            for path in tasks
            if b"status: done\n" in VALIDATOR._blob_bytes(ROOT, proposed[path])
        )
        other = next(path for path in tasks if path.parent != task.parent)
        swapped = dict(proposed)
        swapped[task] = proposed[other]
        self.assertEqual(
            self._wp004b_admitted(base_commit, base, swapped),
            frozenset(),
        )

        original = VALIDATOR._blob_bytes(ROOT, proposed[task])
        mutations = (
            original + b"\nunauthorized body drift\n",
            original.replace(b"status: done\n", b"status: queued\n", 1),
            original.replace(b"type: sdlc/task\n", b"type: sdlc/spec\n", 1),
            original.replace(b'artifact_id: "SPEC-', b'artifact_id: "SPEC-9999-', 1),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[-48:]):
                self.assertEqual(
                    self._mutation_result(
                        base_commit,
                        base,
                        proposed,
                        task,
                        mutation,
                    ),
                    frozenset(),
                )

    def _retired_wp004b_finite_admission_binds_requirement_and_ad_metadata(self):
        base_commit, _target_commit, base, proposed = (
            self._wp004b_committed_transition()
        )
        accepted = self._wp004b_admitted(base_commit, base, proposed)
        requirement = next(
            path
            for path in accepted
            if path.as_posix().startswith("docs/01.requirements/")
            and b"status: active\n" in VALIDATOR._blob_bytes(ROOT, proposed[path])
        )
        architecture = next(
            path
            for path in accepted
            if path.as_posix().startswith("docs/02.architecture/descriptions/")
            and "/ad-" not in path.as_posix()
            and b"status: active\n" in VALIDATOR._blob_bytes(ROOT, proposed[path])
        )
        requirement_bytes = VALIDATOR._blob_bytes(ROOT, proposed[requirement])
        architecture_bytes = VALIDATOR._blob_bytes(ROOT, proposed[architecture])
        mutations = (
            (
                requirement,
                requirement_bytes.replace(b"status: active\n", b"status: draft\n", 1),
            ),
            (
                requirement,
                requirement_bytes.replace(
                    b"type: sdlc/requirement\n",
                    b"type: sdlc/prd\n",
                    1,
                ),
            ),
            (
                requirement,
                requirement_bytes.replace(
                    b'artifact_id: "REQ-', b'artifact_id: "REQ-9999-', 1
                ),
            ),
            (
                architecture,
                architecture_bytes.replace(b"status: active\n", b"status: draft\n", 1),
            ),
            (
                architecture,
                architecture_bytes.replace(
                    b'artifact_id: "AD-', b'artifact_id: "AD-9999-', 1
                ),
            ),
        )
        for path, mutation in mutations:
            with self.subTest(path=path, mutation=mutation[:80]):
                self.assertEqual(
                    self._mutation_result(
                        base_commit,
                        base,
                        proposed,
                        path,
                        mutation,
                    ),
                    frozenset(),
                )

    def _retired_wp004b_finite_admission_rejects_duplicate_router_and_foreign_task(
        self,
    ):
        base_commit, _target_commit, base, proposed = (
            self._wp004b_committed_transition()
        )
        accepted = self._wp004b_admitted(base_commit, base, proposed)
        router = next(
            path
            for path in accepted
            if VALIDATOR.WORK054_WP004B_ROUTER_PATTERN.fullmatch(path.as_posix())
            and b"tasks/tsk-" in VALIDATOR._blob_bytes(ROOT, proposed[path])
        )
        router_bytes = VALIDATOR._blob_bytes(ROOT, proposed[router])
        task_line = next(
            line
            for line in router_bytes.splitlines(keepends=True)
            if b"](tasks/tsk-" in line
        )
        self.assertEqual(
            self._mutation_result(
                base_commit,
                base,
                proposed,
                router,
                router_bytes + task_line,
            ),
            frozenset(),
        )

        foreign = dict(proposed)
        foreign[PurePosixPath("docs/03.specs/9999-rogue/tasks/tsk-0001-rogue.md")] = (
            proposed[
                next(
                    path
                    for path in accepted
                    if VALIDATOR.WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
                )
            ]
        )
        self.assertEqual(
            self._wp004b_admitted(base_commit, base, foreign),
            frozenset(),
        )

    def test_production_compare_allows_body_maintenance_without_state_change(
        self,
    ):
        registry = load_registry(ROOT)
        path = PurePosixPath("docs/03.specs/9999-terminal/spec.md")

        def compare_body_change(status: str):
            document = LifecycleDocument(path, "sdlc/spec", status)
            return compare_lifecycle(
                registry,
                {path: document},
                {path: document},
                base_mode="staged",
                evidence_context=LifecycleEvidenceContext(
                    base_documents={path: document},
                    proposed_documents={
                        path: LifecycleEvidenceDocument(
                            document,
                            (),
                            (),
                            (),
                            (),
                            True,
                            True,
                            status == "done",
                        )
                    },
                    changed_paths=frozenset({path}),
                    status_changed_paths=frozenset(),
                    body_changed_paths=frozenset({path}),
                    created_paths=frozenset(),
                ),
            )

        for status in ("draft", "active", "done"):
            with self.subTest(status=status):
                self.assertEqual(compare_body_change(status), ())

    def test_lifecycle_free_navigation_creation_needs_no_migration_event(self):
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/90.references/research/9999-navigation-fixture/README.md"
        )
        created = lifecycle.document_from_text(registry, path, "# Fixture\n")

        self.assertEqual(created.profile_id, "common/readme-research-pack")

        actual = compare_lifecycle(
            registry,
            {},
            {path: created},
            base_mode="staged",
        )

        self.assertEqual(actual, ())

    def test_reference_creation_answers_to_its_own_role_vocabulary(self):
        # This fixture used to create an audit at `active` and assert silence,
        # which is what the old five-value domain and absent graph allowed.
        # Audit findings are completed or invalidated; `active` was borrowed
        # vocabulary that meant nothing for the role.
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/90.references/audits/0001-example-audit/m0001-findings.md"
        )

        def created(status: str):
            return lifecycle.document_from_text(
                registry,
                path,
                f"""---
title: 'Reference: Example Audit Findings'
version: "1.0.0"
type: reference/audit
layer: "references"
status: {status}
owner: platform
updated: 2026-09-01
artifact_id: "AUD-0001-m0001"
---

# Reference: Example Audit Findings
""",
            )

        self.assertEqual(created("draft").profile_id, "reference/audit")
        self.assertEqual(
            compare_lifecycle(
                registry, {}, {path: created("draft")}, base_mode="staged"
            ),
            (),
        )
        for status, rule in (
            ("active", "LIFECYCLE-STATE"),
            ("completed", "LIFECYCLE-CREATE"),
        ):
            with self.subTest(status=status):
                self.assertEqual(
                    [
                        item.rule_id
                        for item in compare_lifecycle(
                            registry, {}, {path: created(status)}, base_mode="staged"
                        )
                    ],
                    [rule],
                )

    def test_deletion_is_owned_by_consumer_and_git_recovery_gates(self):
        registry = load_registry(ROOT)
        path = PurePosixPath("docs/05.operations/guides/9999-obsolete.md")
        document = LifecycleDocument(path, "operation/guide", "active")

        self.assertEqual(
            compare_lifecycle(registry, {path: document}, {}, base_mode="staged"),
            (),
        )

    def test_a_proved_form_move_admits_its_rename(self):
        # A form carries no lifecycle state, so it can rehome through neither
        # the current-document rule (governance paths only) nor the archive
        # rule. Without a third admission a reviewed, byte-identical form move
        # is reported as a bare rename and cannot be made at all.
        registry = load_registry(ROOT)
        old = PurePosixPath("docs/99.templates/templates/references/x-old.template.md")
        new = PurePosixPath("docs/99.templates/templates/references/audit.template.md")
        base = {
            old: lifecycle.LifecycleDocument(
                old, "common/template-reference-audit", None
            )
        }
        proposed = {
            new: lifecycle.LifecycleDocument(
                new, "common/template-reference-audit", None
            )
        }
        rename = (lifecycle.LifecycleRename(old_path=old, new_path=new),)

        bare = compare_lifecycle(
            registry, base, proposed, renames=rename, base_mode="staged"
        )
        self.assertEqual([item.rule_id for item in bare], ["LIFECYCLE-RENAME"])

        admitted = compare_lifecycle(
            registry,
            base,
            proposed,
            renames=rename,
            base_mode="staged",
            migration_events=lifecycle.MigrationLifecycleEvents(
                form_rehomes=frozenset({(old, new)})
            ),
        )
        self.assertEqual(admitted, ())

    def test_stage_index_creation_is_bounded_by_the_registry_route(self):
        # The lifecycle validator once reported creating a stage index as a
        # failure for having no lifecycle, and each README that had to be
        # created was exempted by id until the exemption list held four. The
        # route already bounds these profiles: every domainless README pattern
        # is a closed enumeration, so an unlisted path is refused outright and
        # a listed one needs no lifecycle admission.
        registry = load_registry(ROOT)
        path = PurePosixPath("docs/03.specs/README.md")
        created = lifecycle.document_from_text(registry, path, "# Fixture\n")

        self.assertEqual(created.profile_id, "common/readme-stage-index")
        self.assertEqual(
            compare_lifecycle(registry, {}, {path: created}, base_mode="staged"),
            (),
        )

        with self.assertRaises(DocumentContractError):
            lifecycle.document_from_text(
                registry, PurePosixPath("docs/04.invented/README.md"), "# Fixture\n"
            )

    def test_terminal_supersession_uses_reciprocal_production_evidence(self):
        registry = load_registry(ROOT)
        source = PurePosixPath("docs/03.specs/9998-source/spec.md")
        successor = PurePosixPath("docs/03.specs/9999-successor/spec.md")
        base = {
            source: LifecycleDocument(source, "sdlc/spec", "active"),
            successor: LifecycleDocument(successor, "sdlc/spec", "active"),
        }
        proposed = {
            source: LifecycleDocument(source, "sdlc/spec", "superseded"),
            successor: base[successor],
        }

        def context(*, reciprocal: bool) -> LifecycleEvidenceContext:
            source_view = LifecycleEvidenceDocument(
                proposed[source],
                (successor,),
                (successor,),
                (),
                (),
                True,
                True,
                False,
            )
            successor_links = (source,) if reciprocal else ()
            successor_view = LifecycleEvidenceDocument(
                proposed[successor],
                successor_links,
                successor_links,
                (),
                (),
                True,
                True,
                False,
            )
            return LifecycleEvidenceContext(
                base_documents=base,
                proposed_documents={source: source_view, successor: successor_view},
                changed_paths=frozenset({source}),
                status_changed_paths=frozenset({source}),
                body_changed_paths=frozenset({source}),
                created_paths=frozenset(),
            )

        missing = compare_lifecycle(
            registry,
            base,
            proposed,
            base_mode="staged",
            evidence_context=context(reciprocal=False),
        )
        self.assertIn("LIFECYCLE-EVIDENCE", [item.rule_id for item in missing])
        exact = compare_lifecycle(
            registry,
            base,
            proposed,
            base_mode="staged",
            evidence_context=context(reciprocal=True),
        )
        self.assertEqual(exact, ())

    def test_mutable_supersession_requires_reciprocal_links(self):
        authority = self._authority()
        with self.assertRaisesRegex(
            authority.AuthorityError, "SUPERSESSION_RECIPROCAL"
        ):
            authority.require_reciprocal_supersession(
                source="docs/01.requirements/0001-old.md",
                successor="docs/01.requirements/0002-new.md",
                source_links={"superseded_by": "docs/01.requirements/0002-new.md"},
                successor_links={},
            )

    def test_material_staged_registry_drift_is_rejected(self):
        authority = self._authority()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Fixture"], cwd=root, check=True
            )
            path = root / "registry.json"
            path.write_text('{"state":"staged"}\n', encoding="utf-8")
            subprocess.run(["git", "add", "registry.json"], cwd=root, check=True)
            path.write_text('{"state":"worktree"}\n', encoding="utf-8")
            with self.assertRaisesRegex(authority.AuthorityError, "AUTHORITY_DRIFT"):
                authority.assert_staged_authority_matches_worktree(
                    root,
                    PurePosixPath("registry.json"),
                    timeout_seconds=2,
                )

    def test_git_backed_readers_are_stream_capped_and_timed(self):
        authority = self._authority()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            path = root / "registry.json"
            path.write_bytes(b"x" * 128)
            subprocess.run(["git", "add", "registry.json"], cwd=root, check=True)
            with self.assertRaisesRegex(authority.AuthorityError, "AUTHORITY_SIZE"):
                authority.staged_authority_bytes(
                    root, PurePosixPath("registry.json"), max_bytes=16
                )
            with self.assertRaisesRegex(authority.AuthorityError, "AUTHORITY_TIMEOUT"):
                authority.staged_authority_bytes(
                    root,
                    PurePosixPath("registry.json"),
                    timeout_seconds=1e-9,
                )
            with self.assertRaisesRegex(
                document_contracts.AuthorityError, "AUTHORITY_SIZE"
            ):
                document_contracts._run_git(
                    root, ["show", ":registry.json"], max_stdout_bytes=16
                )
            with self.assertRaisesRegex(
                document_contracts.AuthorityError, "AUTHORITY_TIMEOUT"
            ):
                document_contracts._run_git(
                    root,
                    ["show", ":registry.json"],
                    timeout_seconds=1e-9,
                )
            with self.assertRaisesRegex(
                document_contracts.AuthorityError, "AUTHORITY_TIMEOUT"
            ):
                document_contracts._is_ignored(
                    root,
                    PurePosixPath("registry.json"),
                    timeout_seconds=1e-9,
                )

    def test_wp004a_current_owner_activation_is_finite_and_atomic(self):
        admission = getattr(VALIDATOR, "finite_work054_wp004a_authority_paths", None)
        self.assertTrue(callable(admission), "WP-004A authority admission is missing")
        owner_paths = (
            PurePosixPath("docs/00.agent-governance/policies/document-lifecycle.md"),
            PurePosixPath("docs/00.agent-governance/sdlc.md"),
        )
        required_paths = tuple(VALIDATOR.WORK054_WP004A_REQUIRED_CHANGED_PATHS)
        proposed_documents = {
            path: LifecycleDocument(path, "governance/rule", "active")
            for path in owner_paths
        }
        base_blobs = {path: "1" * 40 for path in required_paths}
        proposed_blobs = {path: "2" * 40 for path in required_paths}
        for path in owner_paths:
            base_blobs.pop(path, None)
            proposed_blobs[path] = "2" * 40

        exact = admission(
            mode="staged",
            base_commit=VALIDATOR.WORK054_WP004A_BASE_COMMIT,
            base_documents={},
            proposed_documents=proposed_documents,
            base_blobs=base_blobs,
            proposed_blobs=proposed_blobs,
        )
        self.assertEqual(exact, frozenset(owner_paths))

        partial_blobs = dict(proposed_blobs)
        partial_blobs[required_paths[0]] = base_blobs[required_paths[0]]
        self.assertEqual(
            admission(
                mode="staged",
                base_commit=VALIDATOR.WORK054_WP004A_BASE_COMMIT,
                base_documents={},
                proposed_documents=proposed_documents,
                base_blobs=base_blobs,
                proposed_blobs=partial_blobs,
            ),
            frozenset(),
        )


class _RetiredIndependentLifecycleFixtureTests:
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            (ROOT / VALIDATOR.FIXTURE_PATH).read_text(encoding="utf-8")
        )
        cls.registry = load_registry(ROOT)

    def test_forward_comparison_and_admission_cases_are_independent(self):
        for contract in self.fixture["forwardContracts"]:
            for profile_id in contract["profiles"]:
                for from_state, to_state in contract["edges"]:
                    with self.subTest(
                        group="forward",
                        contract=contract["name"],
                        profile=profile_id,
                        edge=(from_state, to_state),
                    ):
                        path = PurePosixPath("docs/__lifecycle__/fixture.md")
                        diagnostics = compare_lifecycle(
                            self.registry,
                            {path: LifecycleDocument(path, profile_id, from_state)},
                            {path: LifecycleDocument(path, profile_id, to_state)},
                            base_mode="explicit-ref",
                        )
                        self.assertEqual(diagnostics, ())

        for case in self.fixture["comparisonCases"]:
            with self.subTest(group="comparison", case=case["name"]):
                base = LifecycleDocument(
                    PurePosixPath(case["base"][0]), case["base"][1], case["base"][2]
                )
                proposed = LifecycleDocument(
                    PurePosixPath(case["proposed"][0]),
                    case["proposed"][1],
                    case["proposed"][2],
                )
                actual = compare_lifecycle(
                    self.registry,
                    {base.path: base},
                    {proposed.path: proposed},
                    base_mode="explicit-ref",
                )
                self.assertEqual(
                    [item.rule_id for item in actual], case["expectedRuleIds"]
                )

        for case in self.fixture["admissionCases"]:
            with self.subTest(group="admission", case=case["name"]):
                documents = [
                    LifecycleDocument(PurePosixPath(item[0]), item[1], item[2])
                    for item in case["documents"]
                ]
                operation = case.get("operation", "create")
                if operation == "create":
                    actual = compare_lifecycle(
                        self.registry,
                        {},
                        {item.path: item for item in documents},
                        base_mode="staged",
                    )
                elif operation == "delete":
                    actual = compare_lifecycle(
                        self.registry,
                        {item.path: item for item in documents},
                        {},
                        base_mode="staged",
                    )
                else:
                    base, proposed = documents
                    actual = compare_lifecycle(
                        self.registry,
                        {base.path: base},
                        {proposed.path: proposed},
                        renames=(LifecycleRename(base.path, proposed.path),),
                        base_mode="staged",
                    )
                self.assertEqual(
                    [item.rule_id for item in actual], case["expectedRuleIds"]
                )


class LifecycleArchiveImmutabilityOperatingTest(unittest.TestCase):
    original_path = "docs/03.specs/0900-fixture/spec.md"
    archive_path = "docs/98.archive/03.specs/0900-fixture/spec.md"

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
            b'type: "archive/tombstone"\n'
            b'status: "archived"\n'
            b'owner: "platform"\n'
            b'updated: "2026-07-19"\n'
            b'original_type: "sdlc/spec"\n'
            + f'original_path: "{cls.original_path}"\n'.encode()
            + b'archived_on: "2026-07-19"\n'
            + b'archive_reason: "superseded"\n'
            + b'replacement: "docs/03.specs/0036-archive-record-and-workspace-boundary/spec.md"\n'
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

    def _document_repository(
        self, documents: dict[str, bytes]
    ) -> tuple[tempfile.TemporaryDirectory, Path, str]:
        temporary = tempfile.TemporaryDirectory(prefix="lifecycle-production-adapter-")
        root = Path(temporary.name)
        self._git(root, "init", "--quiet")
        self._git(root, "config", "user.email", "fixture@example.invalid")
        self._git(root, "config", "user.name", "Lifecycle Adapter Fixture")
        registry_path = root / REGISTRY_PATH
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_bytes((ROOT / REGISTRY_PATH).read_bytes())
        for relative, content in documents.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        self._git(root, "add", "--", REGISTRY_PATH, *sorted(documents))
        self._git(root, "commit", "--quiet", "-m", "base")
        return temporary, root, self._git(root, "rev-parse", "HEAD")

    def test_staged_adapter_allows_terminal_body_maintenance(self) -> None:
        path = "docs/03.specs/9001-terminal-mutation/spec.md"
        base = (
            b"---\n"
            b'title: "Terminal mutation fixture"\n'
            b'type: "sdlc/spec"\n'
            b'status: "done"\n'
            b'owner: "platform"\n'
            b'updated: "2026-08-23"\n'
            b'artifact_id: "SPEC-9001"\n'
            b"---\n\n"
            b"# Terminal mutation fixture\n\nStable body.\n"
        )
        temporary, root, _base_commit = self._document_repository({path: base})
        with temporary:
            (root / path).write_bytes(base + b"Unauthorized terminal edit.\n")
            self._git(root, "add", "--", path)
            diagnostics = VALIDATOR._evaluate_comparison(
                root,
                load_registry(ROOT),
                mode="staged",
            )
        self.assertEqual(diagnostics, ())

    def test_ci_adapter_rejects_supersession_without_reciprocal_link(
        self,
    ) -> None:
        source = "docs/02.architecture/decisions/9001-source.md"
        successor = "docs/02.architecture/decisions/9002-successor.md"

        def adr(status: str, artifact_id: str, body: bytes) -> bytes:
            return (
                b"---\n"
                b'title: "ADR fixture"\n'
                b'type: "sdlc/architecture-decision"\n'
                + f'status: "{status}"\n'.encode()
                + b'owner: "platform"\n'
                + b'updated: "2026-08-23"\n'
                + f'artifact_id: "{artifact_id}"\n'.encode()
                + b"---\n\n# ADR fixture\n\n"
                + body
            )

        source_body = (
            b"## Traceability\n\n"
            b"### Lifecycle Traceability\n\n"
            b"| Decision lineage | Replacement relation | Affected Spec |\n"
            b"| --- | --- | --- |\n"
            b"| [ADR-9002](./9002-successor.md) | superseded by | N/A |\n"
        )
        successor_body = b"## Traceability\n\nNo reciprocal predecessor link.\n"
        base_source = adr("accepted", "ADR-9001", source_body)
        proposed_source = adr("superseded", "ADR-9001", source_body)
        temporary, root, base_commit = self._document_repository(
            {
                source: base_source,
                successor: adr("accepted", "ADR-9002", successor_body),
            }
        )
        with temporary:
            (root / source).write_bytes(proposed_source)
            self._git(root, "add", "--", source)
            self._git(root, "commit", "--quiet", "-m", "supersede")
            proposed_commit = self._git(root, "rev-parse", "HEAD")
            diagnostics = VALIDATOR._evaluate_comparison(
                root,
                load_registry(ROOT),
                mode="ci",
                base_ref=base_commit,
                to_ref=proposed_commit,
            )
        self.assertEqual(
            [(item.rule_id, item.path.as_posix()) for item in diagnostics],
            [("LIFECYCLE-EVIDENCE", source)],
        )

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

    def test_staged_and_explicit_ref_reject_archive_creation_without_migration(
        self,
    ) -> None:
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
                self.assertEqual(
                    [(item.rule_id, item.path.as_posix()) for item in diagnostics],
                    [("LIFECYCLE-EVIDENCE", self.archive_path)],
                )


class TerminalLifecycleDomainTests(unittest.TestCase):
    """WP-004C lifecycle-domain-only model regressions."""

    def test_specification_relationship_group_tracks_terminal_registry_profiles(
        self,
    ) -> None:
        registry = load_registry(ROOT)
        self.assertEqual(
            lifecycle.specification_relationship_profiles(registry),
            frozenset(
                {
                    "sdlc/spec",
                    "sdlc/data-model",
                    "common/native-contract-openapi",
                    "common/native-contract-graphql",
                    "common/native-contract-protobuf",
                }
            ),
        )
        self.assertNotIn(
            "sdlc/agent-design",
            lifecycle.specification_relationship_profiles(registry),
        )
        self.assertNotIn(
            "sdlc/tests",
            lifecycle.specification_relationship_profiles(registry),
        )
        self.assertEqual(
            lifecycle.requirement_relationship_profiles(registry),
            frozenset({"sdlc/requirement"}),
        )

    def test_production_cli_has_no_embedded_self_test_surface(self) -> None:
        option_strings = {
            option
            for action in VALIDATOR._parser()._actions
            for option in action.option_strings
        }
        self.assertNotIn("--self-test", option_strings)
        self.assertFalse(hasattr(VALIDATOR, "_evidence_case_context"))
        self.assertFalse(hasattr(VALIDATOR, "_git_case"))

    def test_statefulness_uses_only_the_profile_lifecycle_domain(self) -> None:
        registry = load_registry(ROOT)
        requirement = next(
            profile
            for profile in registry.profiles
            if profile.profile_id == "sdlc/requirement"
        )
        readme = next(
            profile
            for profile in registry.profiles
            if profile.profile_id == "common/readme-repository"
        )
        self.assertTrue(lifecycle._stateful(requirement))
        self.assertFalse(lifecycle._stateful(readme))

    def _created(self, path: str, profile_id: str, status: str | None, **events):
        registry = load_registry(ROOT)
        document = lifecycle.LifecycleDocument(
            path=PurePosixPath(path), profile_id=profile_id, status=status
        )
        diagnostics = lifecycle._create_diagnostics(
            registry,
            [document],
            base_mode="staged",
            migration_events=lifecycle.MigrationLifecycleEvents(**events),
        )
        return [diagnostic.rule_id for diagnostic in diagnostics]

    def test_a_reference_role_is_governed_by_the_graph_it_declares(self):
        # The three reference profiles carry a declared lifecycle. While they
        # were skipped for being classification-only the graph decided nothing:
        # a report could appear already published, or move to a state no edge
        # reaches, and the validator stayed silent.
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/90.references/research/0001-workspace-engineering/m0099-probe.md"
        )
        published = lifecycle.LifecycleDocument(path, "reference/research", "published")
        draft = lifecycle.LifecycleDocument(path, "reference/research", "draft")
        superseded = lifecycle.LifecycleDocument(
            path, "reference/research", "superseded"
        )

        self.assertEqual(
            [
                item.rule_id
                for item in compare_lifecycle(
                    registry, {}, {path: published}, base_mode="staged"
                )
            ],
            ["LIFECYCLE-CREATE"],
        )
        self.assertEqual(
            compare_lifecycle(registry, {}, {path: draft}, base_mode="staged"), ()
        )
        self.assertEqual(
            [
                item.rule_id
                for item in compare_lifecycle(
                    registry,
                    {path: draft},
                    {path: superseded},
                    base_mode="staged",
                )
            ],
            ["LIFECYCLE-EDGE"],
        )

    def test_creation_evaluates_the_migration_profile_it_declares_stateful(self):
        # `_stateful` calls `archive/migration` stateful, and the transition and
        # snapshot paths honour that. Creation asked `mode` instead, so it saw a
        # classification-only profile and skipped every migration record: a new
        # ledger could appear in a state its own domain has no node for.
        record = "docs/98.archive/migrations/0099-undeclared.md"
        self.assertEqual(
            self._created(record, "archive/migration", "active"),
            ["LIFECYCLE-STATE"],
        )
        self.assertEqual(
            self._created(record, "archive/migration", "sealed"),
            ["LIFECYCLE-CREATE"],
        )
        self.assertEqual(self._created(record, "archive/migration", "draft"), [])
        self.assertEqual(
            self._created(
                record,
                "archive/migration",
                "sealed",
                publications=frozenset({PurePosixPath(record)}),
            ),
            [],
        )

    def test_creation_is_silent_for_every_profile_without_a_lifecycle_domain(self):
        # A profile carrying no domain declares no creation state, so creating
        # one is not a lifecycle event. Naming four such profiles by hand left
        # the rest reporting a lifecycle failure for having no lifecycle.
        registry = load_registry(ROOT)
        stateless = [
            profile.profile_id
            for profile in registry.profiles
            if profile.lifecycle_domain is None
        ]
        self.assertIn("common/readme-stage-index", stateless)
        for profile_id in stateless:
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    self._created("docs/01.requirements/README.md", profile_id, None),
                    [],
                )

    @staticmethod
    def _mig0004_baseline() -> tuple[
        str, dict[PurePosixPath, str], dict[PurePosixPath, str]
    ]:
        # The gate admits one cutover: the sealed target tree is its proposed
        # side. Reading the live index instead would pair a historical base with
        # a tree that has advanced past the cutover, which never occurs in a run.
        proposed = VALIDATOR._tree_blob_map(ROOT, VALIDATOR.WP004C_SEALED_TARGET_COMMIT)
        migration = VALIDATOR._blob_bytes(
            ROOT, proposed[VALIDATOR.WORK054_WP004B_MIGRATION_PATH]
        )
        rows = VALIDATOR.parse_pinned_migration_control(
            VALIDATOR.WORK054_WP004B_MIGRATION_PATH.as_posix(), migration
        )
        terminal = {
            str(row["source_commit"])
            for row in rows
            if str(row["legacy_path"]).startswith("docs/99.templates/")
            or row["legacy_path"]
            == "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
        }
        source_commit = (
            "7a770c3c0eabaeda554c4030fc08fb17de164fe5"  # pragma: allowlist secret
        )
        assert terminal == {source_commit}
        base_commit = terminal.pop()
        return base_commit, VALIDATOR._tree_blob_map(ROOT, base_commit), proposed

    def test_mig0004_projects_only_the_pinned_stage99_and_spec0054_cutover(
        self,
    ) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        admitted = VALIDATOR._wp004c_mig0004_paths(
            root=ROOT,
            mode="staged",
            base_commit=base_commit,
            base_blobs=base_blobs,
            proposed_blobs=proposed_blobs,
        )
        self.assertIn(
            PurePosixPath(
                "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
            ),
            admitted,
        )
        self.assertIn(
            PurePosixPath(
                "docs/99.templates/templates/sdlc/execution/task.template.md"
            ),
            admitted,
        )
        self.assertIn(
            PurePosixPath("docs/99.templates/templates/specs/task.template.md"),
            admitted,
        )

    def test_mig0004_rejects_missing_or_extra_task_records(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        task_root = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks"
        )
        task = next(path for path in proposed_blobs if path.parent == task_root)
        missing = dict(proposed_blobs)
        missing.pop(task)
        extra = dict(proposed_blobs)
        extra[task_root / "tsk-9999-rogue.md"] = proposed_blobs[task]
        for candidate in (missing, extra):
            with self.subTest(paths=len(candidate)):
                self.assertEqual(
                    VALIDATOR._wp004c_mig0004_paths(
                        root=ROOT,
                        mode="staged",
                        base_commit=base_commit,
                        base_blobs=base_blobs,
                        proposed_blobs=candidate,
                    ),
                    frozenset(),
                )

    def test_mig0004_reports_the_exact_tampered_task_field(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        task = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-"
            "consolidation/tasks/tsk-0001-approved-design-authority.md"
        )
        original_oid = proposed_blobs[task]
        sentinel = "f" * 40
        altered = VALIDATOR._blob_bytes(ROOT, original_oid).replace(
            b"WORK-054-001", b"WORK-054-999", 1
        )
        mutated = dict(proposed_blobs)
        mutated[task] = sentinel
        original_reader = VALIDATOR._blob_bytes

        def read_blob(root: Path, oid: str, **kwargs: object) -> bytes:
            if oid == sentinel:
                return altered
            return original_reader(root, oid, **kwargs)

        with mock.patch.object(VALIDATOR, "_blob_bytes", side_effect=read_blob):
            with self.assertRaisesRegex(
                VALIDATOR.InvocationError,
                rf"{re.escape(task.as_posix())}:work-row",
            ):
                VALIDATOR._wp004c_mig0004_paths(
                    root=ROOT,
                    mode="staged",
                    base_commit=base_commit,
                    base_blobs=base_blobs,
                    proposed_blobs=mutated,
                )

    def test_mig0004_rejects_an_unsealed_new_task_payload_after_structural_proof(
        self,
    ) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        task = PurePosixPath(
            "docs/03.specs/0054-sdlc-document-and-agent-governance-"
            "consolidation/tasks/tsk-0001-approved-design-authority.md"
        )
        original_oid = proposed_blobs[task]
        altered = VALIDATOR._blob_bytes(ROOT, original_oid) + b"\nUnsealed payload.\n"
        sentinel = "e" * 40
        mutated = dict(proposed_blobs)
        mutated[task] = sentinel
        original_reader = VALIDATOR._blob_bytes

        def read_blob(root: Path, oid: str, **kwargs: object) -> bytes:
            if oid == sentinel:
                return altered
            return original_reader(root, oid, **kwargs)

        with mock.patch.object(VALIDATOR, "_blob_bytes", side_effect=read_blob):
            self.assertEqual(
                VALIDATOR._wp004c_mig0004_paths(
                    root=ROOT,
                    mode="staged",
                    base_commit=base_commit,
                    base_blobs=base_blobs,
                    proposed_blobs=mutated,
                ),
                frozenset(),
            )

    def test_mig0004_rejects_an_unsealed_stage99_target_blob(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        migration = VALIDATOR._blob_bytes(
            ROOT, proposed_blobs[VALIDATOR.WORK054_WP004B_MIGRATION_PATH]
        )
        row = next(
            row
            for row in VALIDATOR.parse_pinned_migration_control(
                VALIDATOR.WORK054_WP004B_MIGRATION_PATH.as_posix(), migration
            )
            if row["source_commit"] == base_commit
            and row["action"] == "replaced"
            and row["legacy_path"].startswith("docs/99.templates/")
            and row["replacement"].endswith(".md")
            and PurePosixPath(row["replacement"]) in proposed_blobs
        )
        path = PurePosixPath(row["replacement"])
        original_oid = proposed_blobs[path]
        altered = VALIDATOR._blob_bytes(ROOT, original_oid) + b"\nUnsealed payload.\n"
        sentinel = "d" * 40
        mutated = dict(proposed_blobs)
        mutated[path] = sentinel
        original_reader = VALIDATOR._blob_bytes

        def read_blob(root: Path, oid: str, **kwargs: object) -> bytes:
            if oid == sentinel:
                return altered
            return original_reader(root, oid, **kwargs)

        with mock.patch.object(VALIDATOR, "_blob_bytes", side_effect=read_blob):
            self.assertEqual(
                VALIDATOR._wp004c_mig0004_paths(
                    root=ROOT,
                    mode="staged",
                    base_commit=base_commit,
                    base_blobs=base_blobs,
                    proposed_blobs=mutated,
                ),
                frozenset(),
            )

    def test_mig0004_admits_the_exact_reviewed_target_blob(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        target_blobs = VALIDATOR._tree_blob_map(ROOT, WP004C_SEALED_TARGET_COMMIT)
        path = next(
            candidate
            for candidate in sorted(set(base_blobs) & set(target_blobs))
            if candidate.suffix == ".md"
            and base_blobs[candidate] != target_blobs[candidate]
            and proposed_blobs.get(candidate) == target_blobs[candidate]
        )

        admitted = VALIDATOR._wp004c_mig0004_paths(
            root=ROOT,
            mode="staged",
            base_commit=base_commit,
            base_blobs=base_blobs,
            proposed_blobs=proposed_blobs,
        )

        self.assertIn(path, admitted)
        self.assertIn(
            PurePosixPath(
                "docs/03.specs/0054-sdlc-document-and-agent-governance-"
                "consolidation/README.md"
            ),
            admitted,
        )

    def test_mig0004_requires_the_current_named_durable_ref_for_target(
        self,
    ) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        durable_ref = VALIDATOR.current_named_durable_ref(ROOT)
        with mock.patch.object(
            VALIDATOR,
            "require_commits_reachable_from_durable_refs",
            wraps=VALIDATOR.require_commits_reachable_from_durable_refs,
        ) as require_reachable:
            admitted = VALIDATOR._wp004c_mig0004_paths(
                root=ROOT,
                mode="staged",
                base_commit=base_commit,
                base_blobs=base_blobs,
                proposed_blobs=proposed_blobs,
            )

        require_reachable.assert_called_once_with(
            ROOT,
            (WP004C_SEALED_TARGET_COMMIT,),
            (durable_ref,),
        )
        self.assertTrue(admitted)

    def test_mig0004_rejects_existing_target_without_durable_reachability(
        self,
    ) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        self.assertTrue(VALIDATOR._tree_blob_map(ROOT, WP004C_SEALED_TARGET_COMMIT))
        with mock.patch.object(
            VALIDATOR,
            "require_commits_reachable_from_durable_refs",
            side_effect=VALIDATOR.ArchiveContractError(
                "RECOVERY-OBJECT-UNREACHABLE",
                "sealed target is not reachable from a durable ref",
            ),
        ):
            self.assertEqual(
                VALIDATOR._wp004c_mig0004_paths(
                    root=ROOT,
                    mode="staged",
                    base_commit=base_commit,
                    base_blobs=base_blobs,
                    proposed_blobs=proposed_blobs,
                ),
                frozenset(),
            )

    def test_mig0004_rejects_unsealed_markdown_blobs_by_target_parity(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()
        target_blobs = VALIDATOR._tree_blob_map(ROOT, WP004C_SEALED_TARGET_COMMIT)
        path = next(
            candidate
            for candidate in sorted(set(base_blobs) & set(target_blobs))
            if candidate.suffix == ".md"
            and base_blobs[candidate] != target_blobs[candidate]
            and proposed_blobs.get(candidate) == target_blobs[candidate]
        )
        target = VALIDATOR._blob_bytes(ROOT, target_blobs[path])
        cases = {
            "valid-link": (
                target,
                target + b"\n[approved](README.md)\n",
            ),
            "frontmatter": (
                target,
                b"---\nsealed: false\n---\n" + target,
            ),
            "code": (
                target,
                target + b"\n```markdown\n[approved](README.md)\n```\n",
            ),
            "html": (
                target,
                target + b"\n<div>[approved](README.md)</div>\n",
            ),
            "header": (
                target,
                target
                + b"\n| Requirement ID | Spec criterion | Verification method |\n",
            ),
            "prose": (
                target,
                target + b"\nArbitrary prose mutation.\n",
            ),
            "one-byte": (
                target,
                target[:1] + bytes([target[0] ^ 1]) + target[1:],
            ),
        }
        original_reader = VALIDATOR._blob_bytes

        for kind, (source, proposed) in cases.items():
            with self.subTest(kind=kind):
                source_oid = hashlib.sha1(
                    b"blob " + str(len(source)).encode() + b"\0" + source
                ).hexdigest()
                proposed_oid = hashlib.sha1(
                    b"blob " + str(len(proposed)).encode() + b"\0" + proposed
                ).hexdigest()
                candidate_base = dict(base_blobs)
                candidate_proposed = dict(proposed_blobs)
                candidate_base[path] = source_oid
                candidate_proposed[path] = proposed_oid

                def read_blob(root: Path, oid: str, **kwargs: object) -> bytes:
                    if oid == source_oid:
                        return source
                    if oid == proposed_oid:
                        return proposed
                    return original_reader(root, oid, **kwargs)

                with mock.patch.object(VALIDATOR, "_blob_bytes", side_effect=read_blob):
                    self.assertEqual(
                        VALIDATOR._wp004c_mig0004_paths(
                            root=ROOT,
                            mode="staged",
                            base_commit=base_commit,
                            base_blobs=candidate_base,
                            proposed_blobs=candidate_proposed,
                        ),
                        frozenset(),
                    )

    def test_mig0004_rejects_a_source_base_other_than_the_sealed_migration(
        self,
    ) -> None:
        _, base_blobs, proposed_blobs = self._mig0004_baseline()

        self.assertEqual(
            VALIDATOR._wp004c_mig0004_paths(
                root=ROOT,
                mode="staged",
                base_commit="0" * 40,
                base_blobs=base_blobs,
                proposed_blobs=proposed_blobs,
            ),
            frozenset(),
        )

    def test_mig0004_fails_closed_when_the_sealed_target_tree_is_missing(self) -> None:
        base_commit, base_blobs, proposed_blobs = self._mig0004_baseline()

        with mock.patch.object(
            VALIDATOR,
            "_tree_blob_map",
            side_effect=VALIDATOR.InvocationError("target tree unavailable"),
        ):
            self.assertEqual(
                VALIDATOR._wp004c_mig0004_paths(
                    root=ROOT,
                    mode="staged",
                    base_commit=base_commit,
                    base_blobs=base_blobs,
                    proposed_blobs=proposed_blobs,
                ),
                frozenset(),
            )

    def test_ad_template_creates_in_zero_indegree_draft_state(self) -> None:
        registry = load_registry(ROOT)
        template = (
            ROOT / "docs/99.templates/templates/architecture/description.template.md"
        ).read_text(encoding="utf-8")
        path = PurePosixPath(
            "docs/02.architecture/descriptions/9999-template-admission.md"
        )
        created = VALIDATOR.document_from_text(registry, path, template)

        self.assertEqual(created.status, "draft")
        self.assertEqual(
            VALIDATOR.compare_lifecycle(
                registry, {}, {path: created}, base_mode="staged"
            ),
            (),
        )


if __name__ == "__main__":
    unittest.main()
