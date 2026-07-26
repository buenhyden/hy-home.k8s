"""Focused regressions for portable GitOps non-regular self-test fixtures."""

from __future__ import annotations

import errno
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/validate-gitops-change-set.py"
SPEC = importlib.util.spec_from_file_location("validate_gitops_change_set", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CreateNonRegularFixtureTests(unittest.TestCase):
    def test_supported_fifo_creator_returns_fifo(self) -> None:
        created: list[Path] = []

        def supported(path: Path) -> None:
            created.append(path)

        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = MODULE._create_non_regular_fixture(target, supported)
            self.assertEqual(result, "fifo")
            self.assertEqual(created, [target])

    def test_unsupported_fifo_uses_directory_fallback(self) -> None:
        def unsupported(_path: Path) -> None:
            raise OSError(errno.EOPNOTSUPP, "unsupported")

        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = MODULE._create_non_regular_fixture(target, unsupported)
            self.assertEqual(result, "directory-fallback")
            self.assertTrue(target.is_dir())

    def test_unexpected_fifo_error_is_not_downgraded(self) -> None:
        def denied(_path: Path) -> None:
            raise OSError(errno.EACCES, "denied")

        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(OSError) as raised:
                MODULE._create_non_regular_fixture(Path(raw) / "resource.yaml", denied)
            self.assertEqual(raised.exception.errno, errno.EACCES)

    def test_none_creator_uses_directory_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "resource.yaml"
            result = MODULE._create_non_regular_fixture(target, None)
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
            root = MODULE._write_self_test_case(
                Path(raw), "non-regular", supported + "resources: [pipe.yaml]\n"
            )
            fixture_kind = MODULE._create_non_regular_fixture(root / "pipe.yaml", unsupported)
            self.assertEqual(fixture_kind, "directory-fallback")
            with self.assertRaises(MODULE.GitOpsValidationError) as raised:
                MODULE._render_self_test_case(root)
            self.assertEqual(raised.exception.code, "RESOURCE_NOT_REGULAR")

    def test_self_test_boundaries_complete(self) -> None:
        MODULE._self_test_boundaries()


if __name__ == "__main__":
    unittest.main()
