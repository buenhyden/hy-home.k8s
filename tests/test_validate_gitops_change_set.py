"""Focused regressions for GitOps change-set validation."""

from __future__ import annotations

import errno
import importlib.util
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.gitops_change_set_cases import (
    create_non_regular_fixture,
    render_case,
    run_boundaries,
    write_case,
)


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate-gitops-change-set.py"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures/gitops-change-set"
SPEC = importlib.util.spec_from_file_location("validate_gitops_change_set", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CreateNonRegularFixtureTests(unittest.TestCase):
    def test_fixture_change_set_matches_expected_object_identities(self) -> None:
        cases = json.loads((FIXTURE_PATH / "cases.json").read_text(encoding="utf-8"))
        rows = MODULE._render_path_diff(FIXTURE_PATH / "base", FIXTURE_PATH / "head")
        self.assertEqual(rows, cases["expected"])
        output = "\n".join(rows)
        self.assertFalse(any(value in output for value in cases["forbidden_output"]))

    def test_supported_fifo_creator_returns_fifo(self) -> None:
        created: list[Path] = []

        def supported(path: Path) -> None:
            created.append(path)

        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = create_non_regular_fixture(target, supported)
            self.assertEqual(result, "fifo")
            self.assertEqual(created, [target])

    def test_unsupported_fifo_uses_directory_fallback(self) -> None:
        def unsupported(_path: Path) -> None:
            raise OSError(errno.EOPNOTSUPP, "unsupported")

        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = create_non_regular_fixture(target, unsupported)
            self.assertEqual(result, "directory-fallback")
            self.assertTrue(target.is_dir())

    def test_unexpected_fifo_error_is_not_downgraded(self) -> None:
        def denied(_path: Path) -> None:
            raise OSError(errno.EACCES, "denied")

        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(OSError) as raised:
                create_non_regular_fixture(Path(raw) / "resource.yaml", denied)
            self.assertEqual(raised.exception.errno, errno.EACCES)

    def test_none_creator_uses_directory_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = create_non_regular_fixture(target, None)
            self.assertEqual(result, "directory-fallback")
            self.assertTrue(target.is_dir())

    def test_directory_fallback_is_rejected_as_non_regular_resource(self) -> None:
        def unsupported(_path: Path) -> None:
            raise OSError(errno.EOPNOTSUPP, "unsupported")

        supported = (
            f"apiVersion: {MODULE.KUSTOMIZATION_API_VERSION}\n"
            f"kind: {MODULE.KUSTOMIZATION_KIND}\n"
        )
        with tempfile.TemporaryDirectory() as raw:
            root = write_case(
                MODULE,
                Path(raw),
                "non-regular",
                supported + "resources: [pipe.yaml]\n",
            )
            fixture_kind = create_non_regular_fixture(root / "pipe.yaml", unsupported)
            self.assertEqual(fixture_kind, "directory-fallback")
            with self.assertRaises(MODULE.GitOpsValidationError) as raised:
                render_case(MODULE, root)
            self.assertEqual(raised.exception.code, "RESOURCE_NOT_REGULAR")

    def test_self_test_boundaries_complete(self) -> None:
        run_boundaries(MODULE)

    def test_git_runner_maps_output_limit_and_timeout_to_domain_diagnostics(self) -> None:
        for failure, expected in (
            (MODULE.BoundedOutputError("stdout exceeds its byte budget"), "GIT_OUTPUT_LIMIT"),
            (subprocess.TimeoutExpired(["git"], 1), "GIT_TIMEOUT"),
        ):
            with self.subTest(expected=expected), mock.patch.object(
                MODULE, "run_bounded_process", side_effect=failure
            ):
                with self.assertRaises(MODULE.GitOpsValidationError) as raised:
                    MODULE._run_git(Path.cwd(), ["status"])
                self.assertEqual(raised.exception.code, expected)


if __name__ == "__main__":
    unittest.main()
