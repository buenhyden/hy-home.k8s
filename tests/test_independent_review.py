"""Tests for the local independent review check publisher."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest import mock
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

    def test_render_marks_truncation(self):
        data = review.load_verdict(
            verdict(findings=[finding("low") | {"message": "x" * 3999}] * 100)
        )
        summary = review.render(data)[1]
        self.assertLessEqual(len(summary), review.MAX_SUMMARY)
        self.assertTrue(summary.endswith("full verdict._"))


class KeyFileTests(unittest.TestCase):
    def test_key_file_must_be_owner_only_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / "app.pem"
            key.write_text("key", encoding="utf-8")
            for mode in (0o644, 0o640, 0o604, 0o660):
                os.chmod(key, mode)
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
            claims = review.json.loads(
                review.base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
            )
            self.assertEqual(claims["iss"], "123")
            self.assertLessEqual(claims["exp"] - claims["iat"], 600)
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


class PublishTests(unittest.TestCase):
    def run_publish(self, pull, data=None):
        calls = []

        def fake(method, path, auth, body=None):
            calls.append((method, path, auth, body))
            if path.endswith("/installation"):
                return {"id": 7}
            if path.endswith("/access_tokens"):
                return {"token": "secret-token"}
            if "/pulls/" in path:
                return pull
            if path.endswith("/check-runs"):
                return {"id": 1}
            return {}

        with (
            mock.patch.object(review, "app_jwt", return_value="jwt"),
            mock.patch.object(review, "github", side_effect=fake),
        ):
            try:
                result = review.publish(
                    "o/r", 5, review.load_verdict(data or verdict()), "1", Path("k")
                )
            except review.ReviewError as exc:
                result = exc
        return result, calls

    def pull(self, **overrides):
        data = {"state": "open", "base": {"ref": "main"}, "head": {"sha": "a" * 40}}
        data.update(overrides)
        return data

    def test_publishes_scoped_check_on_reviewed_head(self):
        result, calls = self.run_publish(self.pull())
        self.assertEqual(result, {"id": 1})
        token_body = calls[1][3]
        self.assertEqual(token_body["repositories"], ["r"])
        self.assertEqual(
            token_body["permissions"], {"checks": "write", "pull_requests": "read"}
        )
        method, path, auth, body = calls[3]
        self.assertEqual(
            (method, path, auth),
            ("POST", "/repos/o/r/check-runs", "token secret-token"),
        )
        self.assertEqual(body["name"], "independent-review")
        self.assertEqual(body["head_sha"], "a" * 40)
        self.assertEqual(body["conclusion"], "success")
        self.assertEqual(calls[-1][:2], ("DELETE", "/installation/token"))

    def test_refuses_moved_closed_or_non_main_pull(self):
        for pull in (
            self.pull(head={"sha": "b" * 40}),
            self.pull(state="closed"),
            self.pull(base={"ref": "dev"}),
        ):
            result, calls = self.run_publish(pull)
            self.assertIsInstance(result, review.ReviewError)
            self.assertNotIn("/check-runs", [c[1] for c in calls])
            self.assertEqual(calls[-1][:2], ("DELETE", "/installation/token"))


class GithubTests(unittest.TestCase):
    def test_http_errors_map_without_credentials(self):
        errors = [
            review.urllib.error.HTTPError("u", 403, "no", {}, None),
            review.urllib.error.URLError("down"),
            TimeoutError(),
        ]
        for error in errors:
            with mock.patch.object(review.urllib.request, "urlopen", side_effect=error):
                with self.assertRaises(review.ReviewError) as caught:
                    review.github("GET", "/x", "token secret-token")
            self.assertNotIn("secret-token", str(caught.exception))
            self.assertIn("GET /x", str(caught.exception))


class MainTests(unittest.TestCase):
    def run_main(self, argv, env):
        err, out = StringIO(), StringIO()
        with (
            mock.patch.object(sys, "argv", ["independent_review.py", *argv]),
            mock.patch.dict(os.environ, env, clear=True),
            redirect_stderr(err),
            redirect_stdout(out),
        ):
            return review.main(), err.getvalue() + out.getvalue()

    def test_errors_exit_one_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "v.json"
            good.write_text(review.json.dumps(verdict()), encoding="utf-8")
            bad = Path(tmp) / "bad.json"
            bad.write_text("{", encoding="utf-8")
            base = ["--repo", "o/r", "--pr", "1", "--verdict"]
            cases = [
                (base + [str(bad)], {}),
                (["--repo", "bad", "--pr", "1", "--verdict", str(good)], {}),
                (base + [str(good)], {"REVIEW_APP_ID": "x"}),
                (base + [str(good)], {"REVIEW_APP_ID": "1"}),
            ]
            for argv, env in cases:
                code, err = self.run_main(argv, env)
                self.assertEqual(code, 1)
                self.assertTrue(err.startswith("FAIL: "), err)

    def test_unexpected_response_shape_fails_without_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "v.json"
            good.write_text(review.json.dumps(verdict()), encoding="utf-8")
            key = Path(tmp) / "k.pem"
            key.write_text("k", encoding="utf-8")
            os.chmod(key, 0o600)
            with mock.patch.object(review, "publish", return_value={"id": 1}):
                code, output = self.run_main(
                    ["--repo", "o/r", "--pr", "1", "--verdict", str(good)],
                    {"REVIEW_APP_ID": "1", "REVIEW_APP_KEY_FILE": str(key)},
                )
            self.assertEqual(code, 1)
            self.assertIn("unexpected GitHub response shape", output)

    def test_check_only_makes_no_network_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "v.json"
            good.write_text(review.json.dumps(verdict()), encoding="utf-8")
            with mock.patch.object(review, "github") as github:
                code, _ = self.run_main(
                    [
                        "--repo",
                        "o/r",
                        "--pr",
                        "1",
                        "--verdict",
                        str(good),
                        "--check-only",
                    ],
                    {},
                )
            self.assertEqual(code, 0)
            github.assert_not_called()


if __name__ == "__main__":
    unittest.main()
