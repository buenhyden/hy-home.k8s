"""List the tracked Markdown documents that link to one target path.

Each traceability relation is written once, by the citing document. This tool
derives the reverse view from those forward links on demand, using the link
validator's own resolution, so no document has to hand-write a back-link.
"""

from __future__ import annotations

import argparse
import importlib.util
import posixpath
import sys
from collections.abc import Sequence
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation.repository.bounded_io import (  # noqa: E402
    BoundedInputError,
    read_bytes,
    run as run_bounded_process,
)

MAX_DOCUMENT_BYTES = 1024 * 1024
MAX_LISTING_BYTES = 8 * 1024 * 1024


class BacklinkError(Exception):
    """The target or the tree could not be read."""


def _link_validator():
    path = Path(__file__).with_name("validate-links-and-owners.py")
    name = "_document_backlinks_link_validator"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BacklinkError("the link validator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _tracked_markdown(root: Path) -> list[str]:
    completed = run_bounded_process(
        ["git", "-C", str(root), "ls-files", "-z", "--", "*.md"],
        timeout=30,
        stdout_limit=MAX_LISTING_BYTES,
        stderr_limit=64 * 1024,
    )
    if completed.returncode != 0:
        raise BacklinkError("the tracked file list is unavailable")
    return sorted(item for item in completed.stdout.decode("utf-8").split("\0") if item)


def _target(root: Path, raw: str) -> PurePosixPath:
    normalized = posixpath.normpath(PurePosixPath(raw).as_posix())
    if normalized.startswith("../") or normalized == ".." or raw.startswith("/"):
        raise BacklinkError(f"{raw} is outside the repository root")
    if not (root / normalized).exists():
        raise BacklinkError(f"{raw} does not exist")
    return PurePosixPath(normalized)


def backlinks(root: Path, target: str) -> list[str]:
    """Return every tracked Markdown path whose local link resolves to target."""

    wanted = _target(root, target)
    validator = _link_validator()
    sources: list[str] = []
    for document in _tracked_markdown(root):
        source = PurePosixPath(document)
        if source == wanted:
            continue
        try:
            text = read_bytes(root / document, max_bytes=MAX_DOCUMENT_BYTES).decode(
                "utf-8"
            )
        except (BoundedInputError, UnicodeError):
            continue
        for link in validator.rendered_local_links(text, source):
            if link.kind in {"local", "anchor"} and link.target == wanted:
                sources.append(document)
                break
    return sources


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("target")
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        for document in backlinks(Path(arguments.root).resolve(), arguments.target):
            print(document)
    except BacklinkError as exc:
        print(f"FAIL BACKLINKS {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
