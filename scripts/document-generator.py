"""Create one new governed document from the Stage 99 registry and its template.

The caller names the profile and writes the number in the target path. The
generator fills the five shared value markers, restates no registry, identity
or lifecycle rule, and refuses every request that those owners do not admit.
It is the documented default for starting a document; a hand copy stays valid.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import os
import re
import stat
import sys
import unicodedata
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from types import ModuleType
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from document_contracts import (  # noqa: E402
    MARKDOWN_TEMPLATE_PLACEHOLDER,
    DocumentContractError,
    DocumentProfile,
    Registry,
    classify_path,
    direct_parent,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    artifact_identity_reuse_diagnostics,
    creation_states,
    lineage_retired_identities,
)
from frontmatter_yaml import FrontmatterError, load_frontmatter  # noqa: E402

SHARED = ("TITLE", "OWNER", "UPDATED", "ARTIFACT_ID", "PARENT_ID")
SHARED_MARKER = re.compile(r"\{\{(" + "|".join(SHARED) + r")\}\}")
PLACEHOLDER = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
NATIVE_PLACEHOLDER = re.compile(r"__[A-Z][A-Z0-9_]*__")
_profile_module: ModuleType | None = None


class Refusal(Exception):
    """A refused request: a reason ID and one line of cause."""

    def __init__(self, rule_id: str, reason: str):
        self.rule_id = rule_id
        self.reason = " ".join(reason.split())
        super().__init__(f"{rule_id} {self.reason}")


def _profile_check() -> ModuleType:
    """Load the hyphenated profile check once, as `document-backlinks.py` does."""

    global _profile_module
    if _profile_module is None:
        path = Path(__file__).with_name("validate-markdown-profiles.py")
        name = "_document_generator_profile_check"
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise Refusal("GENERATOR-OUTPUT", "the profile check could not be loaded")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        _profile_module = module
    return _profile_module


def _block(text: str) -> str | None:
    """Return the frontmatter block of a text, or None when it has none."""

    if not text.startswith("---\n"):
        return None
    closing = text.find("\n---\n", 4)
    return None if closing < 0 else text[4:closing]


def _frontmatter(text: str) -> dict:
    block = _block(text)
    try:
        data = {} if block is None else load_frontmatter(block) or {}
    except FrontmatterError as error:
        raise Refusal("GENERATOR-OUTPUT", f"frontmatter is invalid: {error}") from error
    if not isinstance(data, dict):
        raise Refusal("GENERATOR-OUTPUT", "frontmatter is not a mapping")
    return data


def _template(root: Path, profile: DocumentProfile) -> str:
    """Return the template of a generable profile or refuse the profile."""

    if profile.mode == "template" or profile.template is None:
        raise Refusal(
            "GENERATOR-PROFILE", f"{profile.profile_id} has no authored Markdown form"
        )
    if profile.template.suffix != ".md":
        raise Refusal(
            "GENERATOR-PROFILE", f"{profile.profile_id} does not use a Markdown form"
        )
    try:
        text = read_repository_text(root, profile.template)
    except ValueError as error:
        raise Refusal(
            "GENERATOR-PROFILE", f"the form is unreadable: {error}"
        ) from error
    block = _block(text) or ""
    foreign = set(PLACEHOLDER.findall(block)) - set(SHARED)
    foreign |= set(NATIVE_PLACEHOLDER.findall(block))
    if foreign:
        raise Refusal(
            "GENERATOR-PROFILE",
            f"{profile.profile_id} has placeholders beyond the shared markers: "
            + ", ".join(sorted(foreign)),
        )
    return text


def _check_input(label: str, value: str) -> None:
    unsafe = any(
        character in '"\\' or unicodedata.category(character) in {"Cc", "Zl", "Zp"}
        for character in value
    )
    if not value.strip() or unsafe or MARKDOWN_TEMPLATE_PLACEHOLDER.search(value):
        raise Refusal(
            "GENERATOR-INPUT",
            f"{label} is empty or holds a quote, backslash, line break, control "
            "character or marker",
        )


def _target(root: Path, raw: str) -> PurePosixPath:
    """Normalize the target and refuse a path that leaves the root or is a link."""

    path = PurePosixPath(raw)
    if (
        not raw
        or path.is_absolute()
        or path.as_posix() != raw
        or {"..", "."} & set(path.parts)
        or "\\" in raw
        or "\0" in raw
    ):
        raise Refusal("GENERATOR-ROUTE", f"{raw!r} is not a normalized relative path")
    current = root
    for part in path.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise Refusal("GENERATOR-ROUTE", f"{current.name} is a symbolic link")
    return path


def _current_documents(root: Path, registry: Registry) -> list:
    """Read the routed Markdown under docs/, the only home of an identity.

    ponytail: a full read of docs/ on each call; index it if the tree outgrows that.
    """

    documents = []
    for directory, names, files in os.walk(root / "docs"):
        names[:] = sorted(n for n in names if not (Path(directory) / n).is_symlink())
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = PurePosixPath((Path(directory) / name).relative_to(root).as_posix())
            try:
                documents.append(
                    (
                        path,
                        classify_path(registry, path),
                        read_repository_text(root, path),
                    )
                )
            except (DocumentContractError, ValueError):
                continue
    return documents


def _identity_refusal(
    root: Path,
    registry: Registry,
    profile: DocumentProfile,
    path: PurePosixPath,
    identity: str,
    status: object,
) -> None:
    documents = _current_documents(root, registry)
    base = {
        owner: LifecycleDocument(
            path=owner,
            profile_id=next(p.profile_id for q, p, _ in documents if q == owner),
            status=None,
            artifact_id=artifact_id,
        )
        for owner, artifact_id in _profile_check().current_artifact_identities(
            documents
        )
    }
    proposed = {
        path: LifecycleDocument(
            path=path,
            profile_id=profile.profile_id,
            status=status if isinstance(status, str) else None,
            artifact_id=identity,
        )
    }
    found = artifact_identity_reuse_diagnostics(
        base,
        proposed,
        base_mode="snapshot",
        retired=lineage_retired_identities({q: t for q, _, t in documents}),
    )
    if found:
        raise Refusal("GENERATOR-IDENTITY", found[0].observed_transition)


def generate(
    root: Path,
    profile_id: str,
    title: str,
    owner: str,
    target: str,
    *,
    today: dt.date | None = None,
    registry: Registry | None = None,
) -> str:
    """Return the text of the new document or raise a `Refusal` with its reason ID.

    `registry` lets a caller that generates many documents load the registry once.
    """

    root = root.absolute()
    check = _profile_check()
    try:
        registry = registry or load_registry(root)
    except DocumentContractError as error:
        raise Refusal("GENERATOR-PROFILE", f"the registry cannot be loaded: {error}")
    profile = next((p for p in registry.profiles if p.profile_id == profile_id), None)
    if profile is None:
        raise Refusal("GENERATOR-PROFILE", f"{profile_id} is not a registry profile")
    template = _template(root, profile)
    _check_input("title", title)
    _check_input("owner", owner)

    path = _target(root, target)
    try:
        routed = classify_path(registry, path)
    except DocumentContractError as error:
        raise Refusal("GENERATOR-ROUTE", f"the registry routes no profile: {error}")
    if routed.profile_id != profile_id:
        raise Refusal("GENERATOR-ROUTE", f"the registry routes {routed.profile_id}")
    if os.path.lexists(root / path):
        raise Refusal("GENERATOR-OCCUPIED", f"{target} already exists")

    identity = check.expected_artifact_id(path, profile)
    if identity is None and profile.artifact_id_pattern is not None:
        raise Refusal("GENERATOR-IDENTITY", "no identity derives from the path")
    parent = direct_parent(path, profile_id)
    if parent is not None:
        try:
            regular = stat.S_ISREG(os.lstat(root / parent[0]).st_mode)
        except OSError:
            regular = False
        if not regular:
            raise Refusal("GENERATOR-PARENT", f"the parent {parent[0]} is absent")
    status = _frontmatter(template).get("status")
    if profile.lifecycle_domain is not None and status not in creation_states(
        profile.lifecycle_domain
    ):
        raise Refusal(
            "GENERATOR-STATUS",
            f"template status {status!r} is not a creation state of {profile_id}",
        )
    if identity is not None:
        _identity_refusal(root, registry, profile, path, identity, status)

    today = today or dt.datetime.now(ZoneInfo("Asia/Seoul")).date()
    values = {
        "TITLE": title,
        "OWNER": owner,
        "UPDATED": today.isoformat(),
        "ARTIFACT_ID": identity,
        "PARENT_ID": None if parent is None else parent[1],
    }
    text = SHARED_MARKER.sub(
        lambda found: values[found.group(1)] or found.group(0), template
    )

    if SHARED_MARKER.search(text):
        raise Refusal("GENERATOR-OUTPUT", "a shared marker has no value")
    _frontmatter(text)
    try:
        findings = check.validate_document_text(
            text,
            path,
            profile,
            "strict",
            today=today,
            frontmatter_schema=check.load_frontmatter_schema(root),
            include_body=False,
        )
    except (OSError, ValueError) as error:
        raise Refusal(
            "GENERATOR-OUTPUT", f"the profile check failed: {error}"
        ) from error
    if findings:
        raise Refusal(
            "GENERATOR-OUTPUT",
            "; ".join(sorted({f"{item.rule_id}" for item in findings})),
        )
    return text


def create_exclusive(root: Path, path: PurePosixPath, text: str) -> None:
    """Create the file exactly once, with its missing folders; leave nothing on failure."""

    destination = root / path
    missing, folder = [], destination.parent
    while not os.path.lexists(folder):
        missing.append(folder)
        folder = folder.parent
    made: list[Path] = []
    try:
        for directory in reversed(missing):
            directory.mkdir()
            made.append(directory)
        descriptor = os.open(
            destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644
        )
    except OSError as error:
        for directory in reversed(made):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise Refusal(
            "GENERATOR-OCCUPIED", f"{path} cannot be created: {error}"
        ) from error
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("target")
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(arguments.root).resolve()
    try:
        text = generate(
            root, arguments.profile, arguments.title, arguments.owner, arguments.target
        )
        create_exclusive(root, PurePosixPath(arguments.target), text)
    except Refusal as refusal:
        print(f"FAIL {refusal.rule_id} {refusal.reason}", file=sys.stderr)
        return 2
    data = _frontmatter(text)
    print(
        f"created {arguments.target} profile={arguments.profile} "
        f"identity={data.get('artifact_id', 'none')} "
        f"parent={(data.get('parent_ids') or ['none'])[0]} "
        f"status={data.get('status', 'none')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
