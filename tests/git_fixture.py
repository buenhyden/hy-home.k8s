#!/usr/bin/env python3
"""Shared Git object fixture for archive and lifecycle regressions.

Two suites carried their own copy of this helper and three more imported one
of them from a test module, so importing a fixture re-ran that module's own
tests. The helper lives beside the other shared case data instead.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


def lifecycle_registry_fixture(raw: dict[str, Any]) -> dict[str, Any]:
    """Keep the document profiles and form predicates used by lifecycle fixtures."""

    selected = {
        "governance/rule",
        "sdlc/architecture-description",
        "sdlc/spec",
        "sdlc/plan",
        "common/program-non-target",
        *(domain["profile_ids"][0] for domain in raw["lifecycle_domains"]),
    }
    profiles = [{**profile} for profile in raw["profiles"] if profile["id"] in selected]
    roles = {profile.get("document_role") for profile in profiles}

    def sections(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = []
        for item in items:
            scoped = {**item, "children": sections(item["children"])}
            if applicability := item.get("applicability"):
                sources = [
                    source
                    for source in applicability["source_profile_ids"]
                    if source in selected
                ]
                if not sources:
                    continue
                scoped["applicability"] = {
                    **applicability,
                    "source_profile_ids": sources,
                }
            result.append(scoped)
        return result

    # Navigation and language include global profile references unrelated to replay.
    registry = {
        key: value
        for key, value in raw.items()
        if key not in {"readme_navigation", "document_language"}
    }
    common_document = raw["common_document_contract"]
    profile_kinds = {
        profile_id: kind
        for profile_id, kind in common_document["profile_kinds"].items()
        if profile_id in selected
    }
    declared_kinds = set(common_document["profile_kinds"].values()) | set(
        common_document["unused_kinds"]
    )
    return {
        **registry,
        "profiles": profiles,
        "common_document_contract": {
            **common_document,
            "profile_kinds": profile_kinds,
            "unused_kinds": sorted(declared_kinds - set(profile_kinds.values())),
        },
        "lifecycle_domains": [
            {
                **domain,
                "profile_ids": [
                    item for item in domain["profile_ids"] if item in selected
                ],
            }
            for domain in raw["lifecycle_domains"]
        ],
        "common_forms": {
            **raw["common_forms"],
            "forms": [
                {**form, "sections": sections(form["sections"])}
                for form in raw["common_forms"]["forms"]
                if form["form_id"] in roles
            ],
        },
    }


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
