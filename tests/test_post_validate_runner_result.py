"""Exact runner-result cardinality tests for the production post-validate hook."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "docs/00.agent-governance/hooks/post-validate-runner-result.py"
SPEC = importlib.util.spec_from_file_location(
    "post_validate_runner_result", MODULE_PATH
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError(f"cannot load runner-result helper from {MODULE_PATH}")
RESULT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RESULT
SPEC.loader.exec_module(RESULT)


class PostValidateRunnerResultTest(unittest.TestCase):
    def test_requires_one_exact_pass_and_no_competing_status(self):
        identifier = "repository-quality"
        valid = (
            '[PASS] repository-quality command=[] tool="/usr/bin/bash" '
            'scope="affected:paths=1"\n'
        )
        cases = {
            "single-pass": (valid, True),
            "missing": ("", False),
            "skip": ("[SKIP] repository-quality command=[]\n", False),
            "duplicate": (valid + valid, False),
            "pass-plus-skip": (
                valid + "[SKIP] repository-quality command=[]\n",
                False,
            ),
        }
        for label, (log_text, expected) in cases.items():
            with self.subTest(label=label):
                self.assertEqual(
                    RESULT.has_one_required_pass(log_text, identifier),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
