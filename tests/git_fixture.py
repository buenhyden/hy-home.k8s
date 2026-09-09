#!/usr/bin/env python3
"""Shared Git object fixture for archive and lifecycle regressions.

Two suites carried their own copy of this helper and three more imported one
of them from a test module, so importing a fixture re-ran that module's own
tests. The helper lives beside the other shared case data instead.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitFixture:
    """Create exact Git objects without consulting the repository worktree."""

    def __init__(self, root: Path, *, initialize: bool = True) -> None:
        self.root = root
        if initialize:
            self.run("init", "--quiet")
        self.run("config", "user.email", "archive-fixture@example.invalid")
        self.run("config", "user.name", "Archive Fixture")

    def run(self, *args: str, input_bytes: bytes | None = None) -> bytes:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.root,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"fixture git command failed: git {' '.join(args)}: "
                f"{completed.stderr.decode('utf-8', errors='replace')}"
            )
        return completed.stdout

    def commit(self, relative_path: str, payload: bytes) -> tuple[str, str]:
        commit, blobs = self.commit_many({relative_path: payload})
        return commit, blobs[relative_path]

    def commit_many(self, files: dict[str, bytes]) -> tuple[str, dict[str, str]]:
        for relative_path, payload in files.items():
            path = self.root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        self.run("--literal-pathspecs", "add", "--", *files)
        self.run("commit", "--quiet", "-m", "fixture")
        commit = self.run("rev-parse", "HEAD").decode("ascii").strip()
        blobs = {
            relative_path: self.run("rev-parse", f"HEAD:{relative_path}")
            .decode("ascii")
            .strip()
            for relative_path in files
        }
        return commit, blobs
