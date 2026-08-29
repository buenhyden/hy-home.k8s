"""Migration events use exact proposed Git bytes, not checkout evidence."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import PurePosixPath
from unittest import mock

from tests import test_generic_migration_recovery as generic
from tests.test_document_lifecycle_agent_roster_cutover import VALIDATOR, ROOT


class MigrationLifecycleTest(unittest.TestCase):
    write = generic.GenericMigrationRecoveryTest.write

    def setUp(self):
        generic.GenericMigrationRecoveryTest.setUp(self)
        registry_path = "docs/99.templates/registry.json"
        registry = json.loads((self.root / registry_path).read_text())
        canonical = json.loads((ROOT / registry_path).read_text())
        profile = next(
            p for p in canonical["profiles"] if p["id"] == "governance/reference"
        )
        registry["profiles"].append(profile)
        navigation = next(
            p for p in canonical["profiles"] if p["id"] == "readme/collection-index"
        )
        registry["profiles"].append(navigation)
        domain = next(
            d
            for d in registry["programLineage"]["lifecycleDomains"]
            if d["family"] == "governance-guide-policy-runbook"
        )
        domain["profileIds"].append(profile["id"])
        self.stage(registry_path, json.dumps(registry).encode())
        self.stage(profile["template"], (ROOT / profile["template"]).read_bytes())
        self.stage(navigation["template"], (ROOT / navigation["template"]).read_bytes())
        self.git.run("rm", "--quiet", "-f", "--", self.target, self.path)
        self.payload = (
            "---\ntitle: 'Policy'\ntype: governance/reference\nstatus: active\n"
            "owner: platform\nupdated: 2026-08-28\n---\n\n# Policy\n\n"
            + "".join(
                f"## {heading}\n\nReviewed policy responsibility.\n\n"
                for heading in (
                    "Overview",
                    "Authority Boundary",
                    "Governance Context",
                    "Current Contract",
                    "Validation and Refresh",
                    "Related Documents",
                )
            )
        ).encode()
        self.git.run("add", "--", "docs/99.templates")
        self.commit, blobs = self.git.commit_many({self.source: self.payload})
        self.row.update(
            source_commit=self.commit,
            source_blob=blobs[self.source],
            content_sha256=hashlib.sha256(self.payload).hexdigest(),
        )
        self.git.run("rm", "--quiet", "--", self.source)
        self.stage(self.target, self.payload.replace(b"Policy", b"Owner"))
        self.write(consumers=[])

    def invoke(self, mode="staged", **refs):
        args = ["--root", str(self.root), "--mode", mode]
        for name, value in refs.items():
            args.extend(["--" + name.replace("_", "-"), value])
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            result = VALIDATOR.main(args)
        return result, output.getvalue()

    def assert_pass(self, *args, **kwargs):
        result, output = self.invoke(*args, **kwargs)
        self.assertEqual(result, 0, output)

    def assert_fail(self, rule, *args, **kwargs):
        result, output = self.invoke(*args, **kwargs)
        self.assertNotEqual(result, 0, output)
        self.assertIn(rule, output)

    def stage(self, path, content):
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).write_bytes(content)
        self.git.run("add", "--", path)

    def assert_bounded_proposal_failure(self, raw, original):
        path = "docs/99.templates/registry.json"
        self.stage(path, json.dumps(raw).encode())
        self.git.run("commit", "--quiet", "-m", "untrusted proposed policy")
        proposal = self.git.run("rev-parse", "HEAD").decode().strip()
        self.stage(path, original)
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "scripts/validate-document-lifecycle.py"),
                    "--root",
                    str(self.root),
                    "--mode",
                    "explicit-ref",
                    "--from-ref",
                    self.commit,
                    "--to-ref",
                    proposal,
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
        except subprocess.TimeoutExpired:
            # subprocess.run kills and waits for its child on timeout.
            self.fail("proposed executable policy exceeded the bounded probe")
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("ARCHIVE-MIGRATION-PROFILE", output)
        self.assertNotIn("UNREACHABLE", output)
        self.assertNotIn("Traceback", output)

    def test_proposed_executable_patterns_are_rejected_before_evaluation(self):
        original = (self.root / "docs/99.templates/registry.json").read_bytes()
        for profile_id, field in (
            ("governance/reference", "pathPattern"),
            ("sdlc/data-model", "pathPattern"),
            ("content/archive-migration", "artifactIdPattern"),
            ("sdlc/data-model", "artifactIdPattern"),
        ):
            with self.subTest(profile=profile_id, field=field):
                raw = json.loads(original)
                next(p for p in raw["profiles"] if p["id"] == profile_id)[field] = (
                    "^(.+)+UNREACHABLE$"
                )
                self.assert_bounded_proposal_failure(raw, original)

    def test_proposed_profile_identities_are_bound_to_trusted_policy(self):
        original = (self.root / "docs/99.templates/registry.json").read_bytes()
        for change in ("alias", "duplicate", "missing", "extra"):
            with self.subTest(change=change):
                raw = json.loads(original)
                profile = next(
                    p for p in raw["profiles"] if p["id"] == "sdlc/data-model"
                )
                if change == "alias":
                    profile["id"] = "common/proposal-only"
                elif change == "duplicate":
                    raw["profiles"].append(dict(profile))
                elif change == "missing":
                    raw["profiles"].remove(profile)
                else:
                    raw["profiles"].append(dict(profile, id="common/proposal-only"))
                self.assert_bounded_proposal_failure(raw, original)

    def test_canonical_policy_guard_precedes_pattern_compilation(self):
        contracts = sys.modules[VALIDATOR.load_registry.__module__]
        trusted = contracts.load_registry(self.root)
        original = (self.root / contracts.REGISTRY_PATH).read_bytes()
        for change in (
            "pathPattern",
            "artifactIdPattern",
            "alias",
            "duplicate",
            "missing",
            "extra",
        ):
            with self.subTest(change=change):
                raw = json.loads(original)
                profile = next(
                    p for p in raw["profiles"] if p["id"] == "sdlc/data-model"
                )
                if change in {"pathPattern", "artifactIdPattern"}:
                    profile[change] = "^(.+)+UNREACHABLE$"
                elif change == "alias":
                    profile["id"] = "common/proposal-only"
                elif change == "duplicate":
                    raw["profiles"].append(dict(profile))
                elif change == "missing":
                    raw["profiles"].remove(profile)
                else:
                    raw["profiles"].append(dict(profile, id="common/proposal-only"))
                with (
                    mock.patch.object(
                        contracts,
                        "_compile_route",
                        side_effect=AssertionError("proposed pattern compiled"),
                    ) as compile_route,
                    self.assertRaises(contracts.DocumentContractError) as caught,
                ):
                    contracts.validate_registry(
                        self.root, raw, trusted_registry=trusted
                    )
                compile_route.assert_not_called()
                self.assertEqual(str(caught.exception), "REGISTRY_EXECUTABLE_POLICY")
                self.assertNotIn("UNREACHABLE", repr(caught.exception.diagnostics))
                self.assertNotIn("proposal-only", repr(caught.exception.diagnostics))

    def test_canonical_default_api_and_schema_null_semantics_are_preserved(self):
        contracts = sys.modules[VALIDATOR.load_registry.__module__]
        trusted = contracts.load_registry(self.root)
        original = (self.root / contracts.REGISTRY_PATH).read_bytes()
        raw = json.loads(original)
        profile = next(p for p in raw["profiles"] if p["id"] == "sdlc/data-model")
        profile["pathPattern"] = "^docs/no-policy-owner\\.md$"
        changed = contracts.validate_registry(self.root, raw)
        self.assertEqual(
            next(
                p for p in changed.profiles if p.profile_id == profile["id"]
            ).path_pattern,
            profile["pathPattern"],
        )
        contracts.validate_registry(
            self.root, json.loads(original), trusted_registry=trusted
        )
        for profile_id, add_null in (
            ("readme/collection-index", True),
            ("governance/reference", False),
        ):
            with self.subTest(profile=profile_id):
                raw = json.loads(original)
                profile = next(p for p in raw["profiles"] if p["id"] == profile_id)
                if add_null:
                    profile["artifactIdPattern"] = None
                else:
                    del profile["artifactIdPattern"]
                with self.assertRaises(contracts.DocumentContractError) as caught:
                    contracts.validate_registry(
                        self.root, raw, trusted_registry=trusted
                    )
                self.assertTrue(
                    all(
                        d.rule_id == "REGISTRY_SCHEMA"
                        for d in caught.exception.diagnostics
                    )
                )

    def test_staged_proven_sealed_publication_and_current_owner_rehome(self):
        self.assert_pass()

    def test_exact_moved_owner_is_admitted_without_rename_waiver(self):
        self.stage(self.target, self.payload)
        self.write(
            [dict(self.row, action="moved", stable_path=self.target, replacement=None)],
            consumers=[],
        )
        self.assert_pass()

    def test_mapped_navigation_creation_is_not_an_active_owner_or_general_waiver(self):
        self.git.run("rm", "--quiet", "-f", "--", self.target)
        self.target = "docs/00.agent-governance/roles/README.md"
        content = (ROOT / self.target).read_bytes()
        self.stage(self.target, content)
        self.write([dict(self.row, replacement=self.target)], consumers=[])
        self.assert_pass()
        self.stage(self.target, b"---\nstatus: active\n---\n" + content)
        self.assert_fail("LIFECYCLE-EVIDENCE")
        self.stage(self.target, content)
        self.stage("docs/00.agent-governance/memory/README.md", content)
        self.assert_fail("LIFECYCLE-CREATE")

    def test_draft_creation_and_later_sealing_still_require_recovery_proof(self):
        sealed = (self.root / self.path).read_bytes()
        self.git.run("rm", "--quiet", "-f", "--", self.target)
        self.stage(self.source, self.payload)
        self.stage(self.path, sealed.replace(b'"sealed"', b'"draft"'))
        self.assert_pass()
        self.git.run("commit", "--quiet", "-m", "publish draft")
        self.stage(self.path, sealed)
        self.assert_fail("LIFECYCLE-EVIDENCE")
        self.git.run("rm", "--quiet", "--", self.source)
        self.stage(self.target, self.payload.replace(b"Policy", b"Owner"))
        self.assert_pass()

    def test_ci_and_explicit_proposal_do_not_consult_checkout_ancestry_or_bytes(self):
        self.write(consumers=[{"source_commit": self.commit, "paths": [self.consumer]}])
        self.git.run("commit", "--quiet", "-m", "publish migration")
        proposal = self.git.run("rev-parse", "HEAD").decode().strip()
        self.git.run("branch", "proposal", proposal)
        self.git.run(
            "checkout", "--quiet", "-b", "unrelated-checkout", self.commit + "^"
        )
        # Keep the trusted current authority available; neither payload nor
        # recovery ancestry in this checkout may substitute for the proposal.
        self.git.run("checkout", proposal, "--", "docs/99.templates")
        self.stage(self.target, b"invalid unrelated checkout")
        self.stage(self.consumer, b"invalid unrelated historical consumer")
        self.stage(self.path, b"invalid unrelated record")
        for mode, refs in (
            ("ci", {"base_ref": self.commit, "to_ref": proposal}),
            ("explicit-ref", {"from_ref": self.commit, "to_ref": proposal}),
        ):
            with self.subTest(mode=mode):
                self.assert_pass(mode, **refs)

    def test_checkout_reachable_source_outside_proposal_ancestry_is_rejected(self):
        tree = self.git.run("write-tree").decode().strip()
        proposal = (
            self.git.run(
                "commit-tree", tree, "-p", self.commit + "^", "-m", "unrelated proposal"
            )
            .decode()
            .strip()
        )
        self.git.run("branch", "unrelated-proposal", proposal)
        self.assert_fail(
            "RECOVERY-OBJECT-UNREACHABLE",
            "explicit-ref",
            from_ref=self.commit,
            to_ref=proposal,
        )

    def test_proposed_registry_routes_cannot_use_checkout_routes(self):
        path = "docs/99.templates/registry.json"
        original = (self.root / path).read_bytes()
        for profile_id, field, value in (
            ("content/archive-migration", "pathPattern", "^docs/never-matches\\.md$"),
            ("governance/reference", "pathPattern", "^docs/never-matches\\.md$"),
            ("governance/reference", "mode", "classification-only"),
        ):
            with self.subTest(profile=profile_id, field=field):
                raw = json.loads(original)
                profile = next(p for p in raw["profiles"] if p["id"] == profile_id)
                profile[field] = value
                self.stage(path, json.dumps(raw).encode())
                self.git.run("commit", "--quiet", "-m", "proposed route mismatch")
                proposal = self.git.run("rev-parse", "HEAD").decode().strip()
                self.stage(path, original)
                self.assert_fail(
                    "LIFECYCLE-EVIDENCE",
                    "explicit-ref",
                    from_ref=self.commit,
                    to_ref=proposal,
                )

    def test_proposed_template_mode_is_not_proven_by_current_file(self):
        path = "docs/99.templates/templates/governance/proposed-template.txt"
        registry_path = "docs/99.templates/registry.json"
        original = (self.root / registry_path).read_bytes()
        raw = json.loads(original)
        next(p for p in raw["profiles"] if p["id"] == "governance/reference")[
            "template"
        ] = path
        self.stage(registry_path, json.dumps(raw).encode())
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).symlink_to("missing.md")
        self.git.run("add", "--", path)
        self.git.run("commit", "--quiet", "-m", "invalid proposed template mode")
        proposal = self.git.run("rev-parse", "HEAD").decode().strip()
        (self.root / path).unlink()
        self.stage(path, b"Current regular file is not proposal evidence.\n")
        self.stage(registry_path, original)
        self.assert_fail(
            "LIFECYCLE-EVIDENCE", "explicit-ref", from_ref=self.commit, to_ref=proposal
        )
        self.stage(registry_path, json.dumps(raw).encode())
        self.git.run("commit", "--quiet", "-m", "regular proposed template")
        proposal = self.git.run("rev-parse", "HEAD").decode().strip()
        self.stage(registry_path, original)
        (self.root / path).unlink()
        self.assert_pass("explicit-ref", from_ref=self.commit, to_ref=proposal)

    def test_nonregular_proposal_record_and_nonmarkdown_target_are_rejected(self):
        record = (self.root / self.path).read_bytes()
        self.git.run("rm", "--quiet", "-f", "--", self.path)
        (self.root / self.path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / self.path).symlink_to("elsewhere.md")
        self.git.run("add", "--", self.path)
        self.git.run("commit", "--quiet", "-m", "invalid mode")
        self.assert_fail(
            "LIFECYCLE-", "explicit-ref", from_ref=self.commit, to_ref="HEAD"
        )
        (self.root / self.path).unlink()
        self.stage(self.path, record)
        target = ".agents/registry.json"
        (self.root / target).parent.mkdir(parents=True, exist_ok=True)
        (self.root / target).symlink_to("elsewhere.json")
        self.git.run("add", "--", target)
        self.write([dict(self.row, replacement=target)], consumers=[])
        self.git.run("commit", "--quiet", "-m", "invalid target mode")
        self.assert_fail(
            "RECOVERY-MIGRATION-TARGET",
            "explicit-ref",
            from_ref=self.commit,
            to_ref="HEAD",
        )

    def test_missing_record_does_not_admit_deletion_or_active_creation(self):
        self.git.run("rm", "--quiet", "-f", "--", self.path)
        self.assert_fail("LIFECYCLE-DELETE")
        self.assert_fail("LIFECYCLE-CREATE")

    def test_source_comparison_base_must_match_recovered_blob(self):
        self.git.run("rm", "--quiet", "-f", "--", self.target, self.path)
        self.git.commit_many({self.source: self.payload + b"Changed base.\n"})
        self.git.run("rm", "--quiet", "--", self.source)
        self.stage(self.target, self.payload)
        self.write(consumers=[])
        self.assert_fail("LIFECYCLE-DELETE")

    def test_target_form_state_and_profile_fail_without_path_waivers(self):
        for content, rule in (
            (
                self.payload.replace(b"status: active", b"status: retired"),
                "LIFECYCLE-CREATE",
            ),
            (
                self.payload.replace(b"governance/reference", b"sdlc/spec"),
                "LIFECYCLE-STATE",
            ),
            (
                self.payload.replace(b"## Overview", b"## Unsupported"),
                "LIFECYCLE-EVIDENCE",
            ),
        ):
            with self.subTest(rule=rule):
                self.stage(self.target, content)
                self.assert_fail(rule)

    def test_target_absence_and_nonregular_modes_fail(self):
        self.git.run("rm", "--quiet", "-f", "--", self.target)
        self.assert_fail("LIFECYCLE-EVIDENCE")
        (self.root / self.target).parent.mkdir(parents=True, exist_ok=True)
        (self.root / self.target).symlink_to("old.md")
        self.git.run("add", "--", self.target)
        self.assert_fail("LIFECYCLE-")

    def test_unmapped_active_and_terminal_creation_remain_denied(self):
        extra = "docs/00.agent-governance/unmapped.md"
        for state in (b"active", b"retired"):
            with self.subTest(state=state):
                self.stage(
                    extra,
                    self.payload.replace(b"status: active", b"status: " + state)
                    + b"Unmapped owner.\n",
                )
                self.assert_fail("LIFECYCLE-CREATE")

    def test_record_profile_status_and_unproved_seal_fail(self):
        original = (self.root / self.path).read_bytes()
        for content in (
            original.replace(b'"content/archive-migration"', b'"governance/reference"'),
            original.replace(b'"sealed"', b'"accepted"'),
            original.replace(self.row["source_blob"].encode(), b"0" * 40),
        ):
            with self.subTest(content=content[:80]):
                self.stage(self.path, content)
                self.assert_fail("LIFECYCLE-")

    def test_old_sealed_record_changes_and_deletions_fail_before_new_admission(self):
        self.git.run("commit", "--quiet", "-m", "publish")
        original = (self.root / self.path).read_bytes()
        for content in (
            original.replace(b"Reviewed policy cutover.", b"Mutated sealed body."),
            original.replace(b'"sealed"', b'"draft"'),
        ):
            self.stage(self.path, content)
            with mock.patch.object(
                VALIDATOR,
                "validate_migration_records",
                side_effect=AssertionError("must protect seal first"),
            ):
                self.assert_fail("LIFECYCLE-TERMINAL-MUTATION")
        self.git.run("rm", "--quiet", "-f", "--", self.path)
        self.assert_fail("LIFECYCLE-TERMINAL-MUTATION")

    def test_staged_record_target_and_deleted_source_worktree_drift_fail(self):
        for path, content in (
            (self.path, (self.root / self.path).read_bytes() + b"drift\n"),
            (self.target, self.payload + b"drift\n"),
            (self.source, self.payload),
        ):
            with self.subTest(path=path):
                original = (
                    (self.root / path).read_bytes()
                    if (self.root / path).exists()
                    else None
                )
                (self.root / path).write_bytes(content)
                self.assert_fail("LIFECYCLE-EVIDENCE")
                if original is None:
                    (self.root / path).unlink()
                else:
                    (self.root / path).write_bytes(original)

    def test_registry_domain_and_verified_old_accepted_controls(self):
        registry = VALIDATOR.load_registry(self.root)
        document = VALIDATOR.document_from_text(
            registry, PurePosixPath(self.path), (self.root / self.path).read_text()
        )
        self.assertEqual(document.status, "sealed")
        for path in sorted(
            (ROOT / "docs/98.archive/migrations").glob("mig-000[1-3]-*.md")
        ):
            relative = PurePosixPath(path.relative_to(ROOT).as_posix())
            text = path.read_text()
            document = VALIDATOR.document_from_text(registry, relative, text)
            failures = VALIDATOR.validate_snapshot_documents(registry, [document])
            self.assertFalse(
                [item for item in failures if item.severity == "FAIL"], failures
            )
            tampered = VALIDATOR.document_from_text(
                registry, relative, text + "tampered\n"
            )
            failures = VALIDATOR.validate_snapshot_documents(registry, [tampered])
            self.assertTrue([item for item in failures if item.severity == "FAIL"])


if __name__ == "__main__":
    unittest.main()
