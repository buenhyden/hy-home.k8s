"""Bounded repository I/O regressions for validation owners."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.validation.repository.bounded_io import (
    BoundedInputError,
    BoundedOutputError,
    read_bytes,
    read_text,
    run,
)


class ValidationBoundedIoTests(unittest.TestCase):
    def test_file_reader_rejects_symlink_parents(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bounded-parent-") as raw:
            root = Path(raw)
            outside = root / "outside"
            outside.mkdir()
            (outside / "input").write_bytes(b"harmless fixture")
            (root / "linked").symlink_to(outside)
            with self.assertRaises(BoundedInputError):
                read_bytes(root / "linked/input", max_bytes=64)

    def test_file_reader_rejects_changes_during_read(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bounded-race-") as raw:
            target = Path(raw) / "input"
            target.write_bytes(b"original")
            real_read = os.read
            changed = False

            def read(descriptor, count):
                nonlocal changed
                payload = real_read(descriptor, count)
                if not changed:
                    changed = True
                    target.write_bytes(b"modified")
                return payload

            with mock.patch.object(os, "read", side_effect=read):
                with self.assertRaises(BoundedInputError):
                    read_bytes(target, max_bytes=64)

    def test_growing_file_cannot_extend_the_byte_budget(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bounded-growth-") as raw:
            target = Path(raw) / "input"
            target.write_bytes(b"ab")
            real_read = os.read
            grown = False
            observed = 0

            def read(descriptor, count):
                nonlocal grown, observed
                payload = real_read(descriptor, count)
                observed += len(payload)
                if not grown:
                    grown = True
                    with target.open("ab") as output:
                        output.write(b"cdef")
                return payload

            with mock.patch.object(os, "read", side_effect=read):
                with self.assertRaisesRegex(BoundedInputError, "byte budget"):
                    read_bytes(target, max_bytes=4)
            self.assertEqual(observed, 5)

    def test_file_reader_rejects_oversize_invalid_utf8_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="validation-bounded-io-") as raw:
            root = Path(raw)
            oversized = root / "oversized.txt"
            oversized.write_bytes(b"12345")
            with self.assertRaises(BoundedInputError):
                read_bytes(oversized, max_bytes=4)

            invalid = root / "invalid.txt"
            invalid.write_bytes(b"\xff")
            with self.assertRaises(BoundedInputError):
                read_text(invalid, max_bytes=4)

            link = root / "link.txt"
            link.symlink_to(oversized)
            with self.assertRaises(BoundedInputError):
                read_bytes(link, max_bytes=8)

    def test_process_reader_rejects_oversize_output_and_timeout(self) -> None:
        with self.assertRaises(BoundedOutputError):
            run(
                [sys.executable, "-c", "print('x' * 32)"],
                timeout=2,
                stdout_limit=8,
                stderr_limit=8,
            )
        with self.assertRaises(subprocess.TimeoutExpired):
            run(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                timeout=0.05,
                stdout_limit=8,
                stderr_limit=8,
            )


if __name__ == "__main__":
    unittest.main()
