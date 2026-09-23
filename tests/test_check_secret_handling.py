"""Behavior check for scripts/check-secret-handling.sh placeholder rules."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-secret-handling.sh"

MANIFEST = """apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sample
spec:
  source:
    helm:
      values: |
        auth:
          password: {value}
"""


def scan(value: str) -> int:
    with tempfile.TemporaryDirectory() as directory:
        for required in ("gitops", "infrastructure", "examples"):
            (Path(directory) / required).mkdir()
        target = Path(directory) / "gitops"
        (target / "app.yaml").write_text(MANIFEST.format(value=value), encoding="utf-8")
        return subprocess.run(
            ["bash", str(SCRIPT), directory], capture_output=True, check=False
        ).returncode


class SecretHandlingPlaceholderTests(unittest.TestCase):
    def test_kiali_secret_reference_is_not_a_plaintext_secret(self) -> None:
        self.assertEqual(scan('"secret:kiali-prometheus-auth:password"'), 0)

    def test_plaintext_value_is_still_reported(self) -> None:
        self.assertEqual(scan('"not-a-reference-value"'), 1)


if __name__ == "__main__":
    unittest.main()
