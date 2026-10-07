"""Local release preparation and operator-only publication boundaries."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
import io
import hashlib
import json
import os
from types import SimpleNamespace
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import release
from tests.git_fixture import GitFixture


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/release.py"


class ReleaseVersionTest(unittest.TestCase):
    def test_strict_semver_rejects_leading_zero_numeric_parts(self) -> None:
        for value in ("v01.2.3", "v1.02.3", "v1.2.03", "v1.2.3-01", "v1.2.3-alpha.01"):
            with self.subTest(value=value), self.assertRaises(release.ReleaseError):
                release.parse_version(value)
        self.assertEqual(
            release.parse_version("v1.2.3-rc.1+build.4").tag, "v1.2.3-rc.1+build.4"
        )


class ReleaseCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="release-contract-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git = GitFixture(self.root)
        shutil.copyfile(ROOT / "cliff.toml", self.root / "cliff.toml")
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n")
        self.git.run("add", "cliff.toml", "CHANGELOG.md")
        self.git.run("commit", "--quiet", "-m", "feat: create fixture platform")
        self.git.run("branch", "-M", "main")

    def invoke(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), "--root", str(self.root), *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )

    def prepare_main_release(self) -> str:
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [0.1.0] - 2026-10-07\n\n### Added\n- Fixture.\n"
        )
        self.git.run("add", "CHANGELOG.md")
        self.git.run("commit", "--quiet", "-m", "docs: prepare fixture release")
        return self.git.run("rev-parse", "HEAD").decode().strip()

    def prepare_with_fixture_cliff(self, *, write: bool) -> str:
        command = release._command

        def fixture_command(root: Path, argv, *, timeout=20):
            if argv[0] == "git-cliff":
                return (
                    "# Changelog\n\n## [0.1.0] - 2026-10-07\n\n### Added\n- Fixture.\n"
                )
            return command(root, argv, timeout=timeout)

        with (
            mock.patch.object(release, "_command", side_effect=fixture_command),
            redirect_stdout(io.StringIO()) as output,
        ):
            release.prepare(
                self.root, release.parse_version("v0.1.0"), initial=True, write=write
            )
        return output.getvalue()

    def test_prepare_preview_is_read_only_and_requires_release_branch(self) -> None:
        before = (self.root / "CHANGELOG.md").read_bytes()
        on_main = self.invoke("prepare", "--version", "v0.1.0", "--initial-version")
        self.assertEqual(on_main.returncode, 2)
        self.git.run("checkout", "--quiet", "-b", "release/v0.1.0")
        preview = self.prepare_with_fixture_cliff(write=False)
        self.assertIn("PREVIEW", preview)
        self.assertEqual((self.root / "CHANGELOG.md").read_bytes(), before)

    def test_initial_version_intent_and_invalid_asset_fail_closed(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "release/v0.1.0")
        no_intent = self.invoke("prepare", "--version", "v0.1.0")
        self.assertEqual(no_intent.returncode, 2)
        self.git.run("checkout", "--quiet", "main")
        self.prepare_main_release()
        outside = self.invoke(
            "publish",
            "--version",
            "v0.1.0",
            "--initial-version",
            "--asset",
            "../outside.tgz",
        )
        self.assertEqual(outside.returncode, 2)
        preview = self.invoke("publish", "--version", "v0.1.0", "--initial-version")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("PREVIEW", preview.stdout)

    def test_prepare_write_updates_only_tracked_changelog(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "release/v0.1.0")
        prior_config = (self.root / "cliff.toml").read_bytes()
        result = self.prepare_with_fixture_cliff(write=True)
        self.assertIn("WRITTEN release prepare", result)
        self.assertIn("## [0.1.0]", (self.root / "CHANGELOG.md").read_text())
        self.assertEqual((self.root / "cliff.toml").read_bytes(), prior_config)

    def test_publish_draft_includes_assets_before_release_becomes_visible(self) -> None:
        sha = self.prepare_main_release()
        asset = self.root / "dist" / "fixture.tgz"
        asset.parent.mkdir()
        asset.write_bytes(b"synthetic release asset")
        self.git.run("add", "dist/fixture.tgz")
        self.git.run("commit", "--quiet", "-m", "build: fixture asset")
        sha = self.git.run("rev-parse", "HEAD").decode().strip()
        observed: list[tuple[str, ...]] = []
        original = release._command

        def command(root, argv, *, timeout=20):
            if argv[0] == "gh":
                observed.append(tuple(argv))
                if argv[2] == "create":
                    self.assertTrue(
                        Path(argv[argv.index("--notes-file") + 1]).is_file()
                    )
                if argv[2] == "view":
                    return json.dumps(
                        {
                            "isDraft": len(observed) == 2,
                            "tagName": "v0.1.0",
                            "targetCommitish": sha,
                            "assets": [{"name": "fixture.tgz"}],
                        }
                    )
                if argv[1] == "api":
                    return json.dumps(
                        {
                            "assets": [
                                {
                                    "name": "fixture.tgz",
                                    "size": len(b"synthetic release asset"),
                                    "digest": "sha256:"
                                    + hashlib.sha256(
                                        b"synthetic release asset"
                                    ).hexdigest(),
                                }
                            ]
                        }
                    )
                return ""
            return original(root, argv, timeout=timeout)

        with (
            mock.patch.object(release, "_remote_main") as remote,
            mock.patch.object(release, "_command", side_effect=command),
            redirect_stdout(io.StringIO()) as output,
        ):
            release.publish(
                self.root,
                release.parse_version("v0.1.0"),
                initial=True,
                requested_assets=("dist/fixture.tgz",),
                execute=True,
            )
        self.assertEqual(len(observed), 6)
        self.assertIn("PUBLISHED release", output.getvalue())
        self.assertEqual(observed[0][:3], ("gh", "release", "create"))
        self.assertIn("--draft", observed[0])
        self.assertIn("fixture.tgz", Path(observed[0][-1]).name)
        self.assertIn("--repo", observed[0])
        self.assertEqual(
            observed[0][observed[0].index("--repo") + 1],
            "github.com/buenhyden/hy-home.k8s",
        )
        self.assertEqual(observed[0][observed[0].index("--target") + 1], sha)
        self.assertEqual(observed[3][:3], ("gh", "release", "edit"))
        self.assertIn("--draft=false", observed[3])
        self.assertEqual(remote.call_count, 3)
        self.assertEqual(remote.call_args.kwargs["require_tag"], True)

    def test_publish_preview_keeps_git_index_bytes_unchanged(self) -> None:
        self.prepare_main_release()
        changelog = self.root / "CHANGELOG.md"
        observed = changelog.stat()
        os.utime(
            changelog,
            ns=(observed.st_atime_ns, observed.st_mtime_ns + 2_000_000_000),
        )
        index = self.root / ".git" / "index"
        before = index.read_bytes()
        preview = self.invoke("publish", "--version", "v0.1.0", "--initial-version")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(index.read_bytes(), before)

    def test_asset_symlink_and_existing_remote_tag_are_refused(self) -> None:
        self.prepare_main_release()
        directory = self.root / "dist"
        directory.mkdir()
        (directory / "fixture.tgz").write_bytes(b"fixture")
        (directory / "link.tgz").symlink_to("fixture.tgz")
        with self.assertRaises(release.ReleaseError) as raised:
            release._assets(self.root, ("dist/link.tgz",))
        self.assertEqual(raised.exception.code, "RELEASE-ASSET-PATH")

        sha = "a" * 40

        def remote_command(_root, argv, *, timeout=20):
            if argv[:4] == ("git", "remote", "get-url", "origin"):
                return "git@github.com:buenhyden/hy-home.k8s.git\n"
            if argv[:2] == ("git", "ls-remote"):
                return f"{sha}\trefs/heads/main\n{sha}\trefs/tags/v0.1.0\n"
            self.fail(f"unexpected remote read: {argv}")

        with mock.patch.object(release, "_command", side_effect=remote_command):
            with self.assertRaises(release.ReleaseError) as collision:
                release._remote_main(
                    self.root,
                    release.parse_version("v0.1.0"),
                    sha,
                    initial=True,
                )
        self.assertEqual(collision.exception.code, "RELEASE-TAG-COLLISION")

    def test_draft_may_have_pending_tag_but_wrong_tag_is_rejected(self) -> None:
        sha = "a" * 40
        version = release.parse_version("v0.1.0")

        def remote_command(_root, argv, *, timeout=20):
            if argv[:4] == ("git", "remote", "get-url", "origin"):
                return "git@github.com:buenhyden/hy-home.k8s.git\n"
            if argv[:2] == ("git", "ls-remote"):
                return f"{sha}\trefs/heads/main\n"
            self.fail(f"unexpected remote read: {argv}")

        with mock.patch.object(release, "_command", side_effect=remote_command):
            release._remote_main(
                self.root, version, sha, initial=True, draft_created=True
            )

    def test_asset_replacement_before_upload_does_not_escape_approved_bytes(
        self,
    ) -> None:
        self.prepare_main_release()
        directory = self.root / "dist"
        directory.mkdir()
        asset = directory / "fixture.tgz"
        asset.write_bytes(b"approved asset bytes")
        self.git.run("add", "dist/fixture.tgz")
        self.git.run("commit", "--quiet", "-m", "build: fixture asset")
        sha = self.git.run("rev-parse", "HEAD").decode().strip()
        outside = self.root.parent / f"{self.root.name}-outside.tgz"
        outside.write_bytes(b"unapproved replacement")
        self.addCleanup(outside.unlink)
        original = release._command
        calls: list[tuple[str, ...]] = []

        def remote(
            _root, _version, _sha, *, initial, draft_created=False, require_tag=False
        ):
            if not draft_created:
                asset.unlink()
                asset.symlink_to(outside)

        def command(root, argv, *, timeout=20):
            if argv[0] == "gh":
                calls.append(tuple(argv))
                if argv[2] == "create":
                    uploaded = Path(argv[-1])
                    self.assertEqual(uploaded.read_bytes(), b"approved asset bytes")
                    self.assertNotEqual(uploaded, asset)
                if argv[2] == "view":
                    return json.dumps(
                        {
                            "isDraft": len(calls) == 2,
                            "tagName": "v0.1.0",
                            "targetCommitish": sha,
                            "assets": [{"name": "fixture.tgz"}],
                        }
                    )
                if argv[1] == "api":
                    return json.dumps(
                        {
                            "assets": [
                                {
                                    "name": "fixture.tgz",
                                    "size": len(b"approved asset bytes"),
                                    "digest": "sha256:"
                                    + hashlib.sha256(
                                        b"approved asset bytes"
                                    ).hexdigest(),
                                }
                            ]
                        }
                    )
                return ""
            return original(root, argv, timeout=timeout)

        with (
            mock.patch.object(release, "_remote_main", side_effect=remote),
            mock.patch.object(release, "_command", side_effect=command),
            redirect_stdout(io.StringIO()),
        ):
            release.publish(
                self.root,
                release.parse_version("v0.1.0"),
                initial=True,
                requested_assets=("dist/fixture.tgz",),
                execute=True,
            )
        self.assertTrue(calls)

    def test_command_ignores_untrusted_path_and_pins_github_host(self) -> None:
        fake = self.root / "gh"
        fake.write_text("#!/bin/sh\nexit 0\n")
        fake.chmod(0o755)
        runner = release._trusted_runner()
        output = runner.StreamObservation(2, hashlib.sha256(b"ok").hexdigest(), b"ok")
        empty = runner.StreamObservation(0, hashlib.sha256(b"").hexdigest(), b"")
        result = runner.BoundedCommandResult("completed", 0, output, empty, True)
        with (
            mock.patch.dict(
                os.environ,
                {
                    "PATH": str(self.root),
                    "GH_HOST": "evil.example",
                    "GIT_SSH_COMMAND": str(fake),
                },
            ),
            mock.patch.object(
                runner, "run_bounded_command", return_value=result
            ) as run,
        ):
            self.assertEqual(release._command(self.root, ("gh", "--version")), "ok")
        argv = run.call_args.args[0]
        self.assertNotEqual(argv[0], str(fake))
        self.assertEqual(argv[0], release._trusted_executable(self.root, "gh"))
        environment = run.call_args.kwargs["env"]
        self.assertEqual(environment["GH_HOST"], "github.com")
        self.assertEqual(environment["GH_REPO"], release.REPOSITORY)
        self.assertNotIn("GIT_SSH_COMMAND", environment)

    def test_draft_asset_digest_mismatch_blocks_publication(self) -> None:
        directory = self.root / "dist"
        directory.mkdir()
        asset = directory / "fixture.tgz"
        asset.write_bytes(b"approved bytes")
        sha = "a" * 40

        def command(_root, argv, *, timeout=20):
            if argv[1:3] == ("release", "view"):
                return json.dumps(
                    {
                        "isDraft": True,
                        "tagName": "v0.1.0",
                        "targetCommitish": sha,
                        "assets": [{"name": "fixture.tgz"}],
                    }
                )
            if argv[1] == "api":
                return json.dumps(
                    {
                        "assets": [
                            {
                                "name": "fixture.tgz",
                                "size": len(b"approved bytes"),
                                "digest": "sha256:" + "0" * 64,
                            }
                        ]
                    }
                )
            self.fail(f"unexpected release command: {argv}")

        with mock.patch.object(release, "_command", side_effect=command):
            with self.assertRaises(release.ReleaseError) as error:
                release._verify_release(
                    self.root,
                    release.parse_version("v0.1.0"),
                    sha,
                    (asset,),
                    draft=True,
                )
        self.assertEqual(error.exception.code, "RELEASE-ASSET-VERIFY")

    def test_prepare_preserves_reviewed_prior_release_section_verbatim(self) -> None:
        reviewed = (
            "## [0.1.0] - 2026-09-01\n\n### Fixed\n"
            "- Reviewed historical wording and  two spaces.\n"
        )
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n" + reviewed
        )
        self.git.run("add", "CHANGELOG.md")
        self.git.run("commit", "--quiet", "-m", "docs: reviewed first release")
        self.git.run("tag", "v0.1.0")
        self.git.run("checkout", "--quiet", "-b", "release/v0.2.0")
        generated = (
            "# Changelog\n\n## [Unreleased]\n\n"
            "## [0.2.0] - 2026-10-07\n\n### Added\n- New feature.\n\n"
            "## [0.1.0] - 2026-09-01\n\n### Fixed\n- Rewritten history.\n"
        )
        command = release._command

        def fixture_command(root, argv, *, timeout=20):
            return (
                generated
                if argv[0] == "git-cliff"
                else command(root, argv, timeout=timeout)
            )

        with (
            mock.patch.object(release, "_command", side_effect=fixture_command),
            redirect_stdout(io.StringIO()),
        ):
            release.prepare(
                self.root, release.parse_version("v0.2.0"), initial=False, write=True
            )
        content = (self.root / "CHANGELOG.md").read_text()
        self.assertIn(reviewed, content)
        self.assertNotIn("Rewritten history", content)
        self.assertIn("## [0.2.0] - 2026-10-07", content)
        self.assertLess(content.index("## [Unreleased]"), content.index("## [0.2.0]"))
        self.assertLess(content.index("## [0.2.0]"), content.index(reviewed))

    def test_publish_preview_rejects_drift_from_prior_tagged_changelog(self) -> None:
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n"
            "## [0.1.0] - 2026-09-01\n\n### Added\n- Reviewed text.\n"
        )
        self.git.run("add", "CHANGELOG.md")
        self.git.run("commit", "--quiet", "-m", "docs: reviewed first release")
        self.git.run("tag", "v0.1.0")
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n"
            "## [0.2.0] - 2026-10-07\n\n### Added\n- Next release.\n\n"
            "## [0.1.0] - 2026-09-01\n\n### Added\n- Mutated text.\n"
        )
        self.git.run("add", "CHANGELOG.md")
        self.git.run("commit", "--quiet", "-m", "docs: prepare next release")
        with self.assertRaises(release.ReleaseError) as error:
            release.publish(
                self.root,
                release.parse_version("v0.2.0"),
                initial=False,
                requested_assets=(),
                execute=False,
            )
        self.assertEqual(error.exception.code, "RELEASE-CHANGELOG-HISTORY-DRIFT")

    def test_draft_recheck_rejects_newer_remote_tag_before_publication(self) -> None:
        sha = "a" * 40

        def remote_command(_root, argv, *, timeout=20):
            if argv[:4] == ("git", "remote", "get-url", "origin"):
                return "git@github.com:buenhyden/hy-home.k8s.git\n"
            if argv[:2] == ("git", "ls-remote"):
                return f"{sha}\trefs/heads/main\n{sha}\trefs/tags/v0.2.0\n"
            self.fail(f"unexpected remote read: {argv}")

        with mock.patch.object(release, "_command", side_effect=remote_command):
            with self.assertRaises(release.ReleaseError) as error:
                release._remote_main(
                    self.root,
                    release.parse_version("v0.1.0"),
                    sha,
                    initial=True,
                    draft_created=True,
                )
        self.assertEqual(error.exception.code, "RELEASE-INITIAL-ALREADY-USED")

    def test_command_rejects_oversized_output_without_echoing_it(self) -> None:
        runner = release._trusted_runner()
        output = runner.StreamObservation(
            release._STDOUT_LIMIT + 1, "synthetic", b"synthetic-secret", True
        )
        empty = runner.StreamObservation(0, hashlib.sha256(b"").hexdigest(), b"")
        result = runner.BoundedCommandResult("completed", 0, output, empty, True)
        with mock.patch.object(runner, "run_bounded_command", return_value=result):
            with self.assertRaises(release.ReleaseError) as error:
                release._command(self.root, ("git", "--version"))
        self.assertEqual(error.exception.code, "RELEASE-OUTPUT-LIMIT")
        self.assertNotIn("synthetic-secret", str(error.exception))

    def test_command_refuses_timeout_with_incomplete_descendant_cleanup(self) -> None:
        output = SimpleNamespace(observed_bytes=0, retained=b"", complete=False)
        result = SimpleNamespace(
            status="timeout",
            returncode=0,
            stdout=output,
            stderr=output,
            cleanup_complete=False,
            escaped_descendants=((123, 456, "child", "S"),),
        )
        runner = release._trusted_runner()
        with mock.patch.object(runner, "run_bounded_command", return_value=result):
            with self.assertRaises(release.ReleaseError) as error:
                release._command(self.root, ("git", "--version"))
        self.assertEqual(error.exception.code, "RELEASE-COMMAND-BOUNDARY")

    def test_command_classifies_normal_nonzero_without_echoing_stderr(self) -> None:
        runner = release._trusted_runner()
        empty = runner.StreamObservation(0, hashlib.sha256(b"").hexdigest(), b"")
        secret = runner.StreamObservation(16, "synthetic", b"synthetic-secret", True)
        result = runner.BoundedCommandResult("completed", 17, empty, secret, True)
        with mock.patch.object(runner, "run_bounded_command", return_value=result):
            with self.assertRaises(release.ReleaseError) as error:
                release._command(self.root, ("git", "--version"))
        self.assertEqual(error.exception.code, "RELEASE-COMMAND-FAILED")
        self.assertNotIn("synthetic-secret", str(error.exception))


if __name__ == "__main__":
    unittest.main()
