"""Tests for the local independent review check publisher."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/independent_review.py"


def load_module():
    spec = importlib.util.spec_from_file_location("independent_review", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


review = load_module()


def verdict(**overrides):
    data = {
        "head_sha": "a" * 40,
        "reviewer": "security-auditor",
        "decision": "approve",
        "summary": "No blocking finding.",
        "findings": [],
    }
    data.update(overrides)
    return data


def finding(severity):
    return {"severity": severity, "path": "a.py", "message": "issue"}


class VerdictTests(unittest.TestCase):
    def test_clean_approval_passes(self):
        self.assertEqual(review.conclusion(review.load_verdict(verdict())), "success")

    def test_approval_with_blocking_finding_fails(self):
        for severity in ("critical", "high"):
            data = review.load_verdict(verdict(findings=[finding(severity)]))
            self.assertEqual(review.conclusion(data), "failure")
            self.assertIn("blocked", review.render(data)[0])

    def test_approval_with_minor_finding_passes(self):
        data = review.load_verdict(verdict(findings=[finding("medium")]))
        self.assertEqual(review.conclusion(data), "success")

    def test_request_changes_fails(self):
        data = review.load_verdict(verdict(decision="request_changes"))
        self.assertEqual(review.conclusion(data), "failure")

    def test_malformed_verdicts_are_rejected(self):
        bad = [
            [],
            verdict(extra=True),
            verdict(head_sha="abc"),
            verdict(head_sha="A" * 40),
            verdict(decision="lgtm"),
            verdict(reviewer=" "),
            verdict(findings={}),
            verdict(findings=[{"severity": "high", "path": "a"}]),
            verdict(findings=[finding("blocker")]),
            verdict(findings=[finding("low")] * 101),
        ]
        for data in bad:
            with self.assertRaises(review.ReviewError):
                review.load_verdict(data)

    def test_render_escapes_table_cells(self):
        data = review.load_verdict(
            verdict(findings=[{"severity": "low", "path": "", "message": "a|b\nc"}])
        )
        summary = review.render(data)[1]
        self.assertIn("| low | - | a\\|b c |", summary)
        self.assertIn("a" * 40, summary)


class KeyFileTests(unittest.TestCase):
    def test_key_file_must_be_owner_only_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / "app.pem"
            key.write_text("key", encoding="utf-8")
            os.chmod(key, 0o644)
            with self.assertRaises(review.ReviewError):
                review.check_key_file(key)
            os.chmod(key, 0o600)
            self.assertEqual(review.check_key_file(key), key)
            link = Path(tmp) / "link.pem"
            link.symlink_to(key)
            with self.assertRaises(review.ReviewError):
                review.check_key_file(link)
            with self.assertRaises(review.ReviewError):
                review.check_key_file(Path(tmp) / "missing.pem")


class JwtTests(unittest.TestCase):
    def test_jwt_signature_verifies_with_public_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / "app.pem"
            pub = Path(tmp) / "app.pub"
            run = {"check": True, "capture_output": True, "timeout": 30}
            subprocess.run(["openssl", "genrsa", "-out", str(key), "2048"], **run)
            subprocess.run(
                ["openssl", "rsa", "-in", str(key), "-pubout", "-out", str(pub)], **run
            )
            token = review.app_jwt("123", key)
            header, payload, signature = token.split(".")
            sig = Path(tmp) / "sig"
            pad = "=" * (-len(signature) % 4)
            sig.write_bytes(review.base64.urlsafe_b64decode(signature + pad))
            signed = Path(tmp) / "in"
            signed.write_bytes(f"{header}.{payload}".encode())
            verify = subprocess.run(
                ["openssl", "dgst", "-sha256", "-verify", str(pub)]
                + ["-signature", str(sig), str(signed)],
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(verify.returncode, 0)


if __name__ == "__main__":
    unittest.main()
