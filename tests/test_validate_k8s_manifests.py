"""Presence boundary for the Kubernetes manifest validator."""

from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidateK8sManifestsTests(unittest.TestCase):
    def test_scoped_yaml_does_not_check_unrelated_invalid_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "gitops").mkdir()
            (root / "infrastructure").mkdir()
            (root / "gitops/changed.yaml").write_text("kind: ConfigMap\n")
            (root / "gitops/unrelated.yaml").write_text("invalid: [\n")
            command = [
                "bash",
                str(ROOT / "scripts/validate-k8s-manifests.sh"),
                str(root),
            ]
            result = subprocess.run(
                [*command, "--changed-path=gitops/changed.yaml"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("unrelated.yaml", result.stdout)
            deleted = subprocess.run(
                [*command, "--changed-path=gitops/deleted.yaml"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(deleted.returncode, 0, deleted.stdout + deleted.stderr)
            self.assertIn("NOT_APPLICABLE", deleted.stdout)
            unsafe = subprocess.run(
                [*command, "--changed-path=../outside.yaml"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(unsafe.returncode, 0)

    def test_scoped_policy_keeps_verify_and_only_selected_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in (
                "gitops",
                "infrastructure",
                "examples",
                "policy/conftest",
                "bin",
            ):
                (root / folder).mkdir(parents=True)
            (root / "gitops/changed.yaml").write_text("kind: ConfigMap\n")
            (root / "gitops/unrelated.yaml").write_text("kind: ConfigMap\n")
            tool = root / "bin/conftest"
            tool.write_text(
                '#!/bin/sh\ncase "$*" in *unrelated.yaml*) exit 9;; esac\nprintf "%s\\n" "$1"\n'
            )
            tool.chmod(0o755)
            result = subprocess.run(
                [
                    "bash",
                    str(ROOT / "scripts/validate-policy-gates.sh"),
                    str(root),
                    "--changed-path=gitops/changed.yaml",
                ],
                env={**os.environ, "HY_HOME_K8S_CONFTEST_EXECUTABLE": str(tool)},
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("verify", result.stdout)
            self.assertIn("test", result.stdout)

    def test_manifest_validator_rejects_missing_and_empty_roots(self):
        script = ROOT / "scripts/validate-k8s-manifests.sh"
        with tempfile.TemporaryDirectory(prefix="manifest-presence-") as directory:
            root = Path(directory)
            (root / "gitops").mkdir()
            missing = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("missing infrastructure/", missing.stderr)
            (root / "infrastructure").mkdir()
            empty = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(empty.returncode, 0)
            self.assertIn("no YAML manifests matched", empty.stderr)


if __name__ == "__main__":
    unittest.main()
