"""Bounded repository I/O regressions for validation owners."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validation.repository.bounded_io import (
    BoundedInputError,
    BoundedOutputError,
    read_bytes,
    read_text,
    run,
)


class ValidationBoundedIoTests(unittest.TestCase):
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
