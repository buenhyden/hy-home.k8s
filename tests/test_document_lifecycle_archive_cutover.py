"""Finite ARWB-003 lifecycle admission regressions."""

from __future__ import annotations

import importlib.util
import inspect
import json
import subprocess
import sys
import unittest
from pathlib import Path, PurePosixPath


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
        base = subprocess.run(
            ["git", "rev-parse", f"{CUTOVER_BASE_COMMIT}:{REGISTRY_PATH}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        proposed = (
            subprocess.run(
                ["git", "hash-object", "--stdin"],
                cwd=ROOT,
                check=True,
                input=(ROOT / REGISTRY_PATH).read_bytes(),
                stdout=subprocess.PIPE,
            )
            .stdout.decode("ascii")
            .strip()
        )
        self.assertEqual(BASE_REGISTRY_BLOB_OID, base)
        self.assertEqual(PROPOSED_REGISTRY_BLOB_OID, proposed)

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


if __name__ == "__main__":
    unittest.main()
