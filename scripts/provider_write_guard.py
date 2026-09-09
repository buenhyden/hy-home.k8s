#!/usr/bin/env python3
"""Shared pre-action write boundary for every supported provider.

One implementation serves both providers. Each provider directory holds only a
thin adapter that names its provider and forwards the payload, so no provider
directory owns a control both providers depend on.

Accept boundary: any path inside this repository, including any of its linked
worktrees. Everything outside this repository is rejected. A worktree path is
resolved against its own worktree root, never against the project directory.

Trust boundary: every program this guard runs comes from the project directory.
A root derived from tool input selects data only; it never selects an
executable.

Invalid path transport fails closed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

PROVIDERS = ("claude", "codex")
PATCH_BEGIN = "*** Begin Patch"
PATCH_END = "*** End Patch"
# A move carries its destination on its own header line, so both the source
# Update header and the Move header contribute a path.
PATCH_HEADERS = (
    "*** Add File:",
    "*** Update File:",
    "*** Delete File:",
    "*** Move to:",
)
GIT_TIMEOUT_SECONDS = 5
# The guard runs inside a pre-action hook whose own registration allows ten
# seconds, so the selector must not be able to outlive that window. A bound
# above that window is never reached: the runtime kills the hook first and the
# guard loses the controlled rejection this constant exists to produce. The
# selector reads the routing registry and classifies the edited paths, which
# stays far below this bound even when handed the whole tracked tree.
SELECTOR_TIMEOUT_SECONDS = 5
SELECTOR_RELATIVE_PATH = "scripts/select-affected-surfaces.py"

project_dir: str = ""
paths: list[str] = []
absolute_roots: set[str] = set()
_git_cache: dict[tuple[str, ...], str] = {}


def reject(code: str) -> None:
    print(f"[FAIL] {code}", file=sys.stderr)
    raise SystemExit(2)


def reject_with_detail(code: str, detail: str) -> None:
    print(f"[FAIL] {code}: {detail}", file=sys.stderr)
    raise SystemExit(2)


def git_value(directory: str, *arguments: str) -> str:
    """Return one trimmed `git rev-parse` value, or an empty string.

    Every query is bounded and memoized, so one directory costs at most one git
    process per query no matter how many edited paths share it."""
    key = (directory, *arguments)
    if key in _git_cache:
        return _git_cache[key]
    try:
        completed = subprocess.run(
            ("git", "-C", directory, "rev-parse", *arguments),
            capture_output=True,
            text=True,
            check=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        # subprocess.TimeoutExpired is a SubprocessError, so a hung or missing
        # git degrades to the same fail-closed path as any other failure.
        _git_cache[key] = ""
        return ""
    value = completed.stdout.strip()
    _git_cache[key] = value
    return value


def repository_identity(directory: str) -> str:
    """Return the shared common git directory identifying one repository."""
    value = git_value(directory, "--path-format=absolute", "--git-common-dir")
    return os.path.realpath(value) if value else ""


def nearest_existing_directory(path: str) -> str:
    """Return the closest existing ancestor directory of a possibly new file."""
    cursor = os.path.dirname(path)
    while cursor and not os.path.isdir(cursor):
        parent = os.path.dirname(cursor)
        if parent == cursor:
            return ""
        cursor = parent
    return cursor


def repository_relative(path: str) -> str:
    """Accept an absolute path only inside the project directory or a linked
    worktree of the same repository, and return it relative to its own worktree
    root.

    Worktree resolution is tried first, because a linked worktree may live under
    the project directory and a plain prefix strip would then yield a path that
    is relative to the wrong tree."""
    if not project_dir:
        reject("HOOK-PATH-ROOT")
    directory = nearest_existing_directory(path)
    worktree_root = ""
    if (
        directory
        and repository_identity(directory) == repository_identity(project_dir) != ""
    ):
        worktree_root = git_value(directory, "--show-toplevel").rstrip("/")
    if worktree_root and path.startswith(worktree_root + "/"):
        absolute_roots.add(worktree_root)
        return path[len(worktree_root) + 1 :]
    if path.startswith(project_dir + "/"):
        absolute_roots.add(project_dir)
        return path[len(project_dir) + 1 :]
    reject("HOOK-PATH-ROOT")
    raise SystemExit(2)


def add_path(value) -> None:
    if not isinstance(value, str) or not value:
        reject("HOOK-PATH-TYPE")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        reject("HOOK-PATH-CONTROL")
    if value[0].isspace() or value[-1].isspace():
        reject("HOOK-PATH-WHITESPACE")

    path = value
    if path.startswith("/"):
        path = repository_relative(path)
    posix = PurePosixPath(path)
    if (
        not path
        or path.startswith("./")
        or path.endswith("/")
        or "//" in path
        or "\\" in path
        or posix.is_absolute()
        or "." in posix.parts
        or ".." in posix.parts
        or posix.as_posix() != path
    ):
        reject("HOOK-PATH-NORMALIZATION")

    if path not in paths:
        paths.append(path)


def consume_scalar_alias(mapping) -> int:
    present = [key for key in ("file_path", "path") if key in mapping]
    for key in present:
        if not isinstance(mapping[key], str) or not mapping[key]:
            reject("HOOK-PATH-TYPE")
    if len(present) > 1:
        reject("HOOK-PATH-ALIAS")
    if present:
        add_path(mapping[present[0]])
    return len(present)


def collect_structured_paths(tool_input: dict) -> None:
    """Read every structured file-tool path shape into the path pipeline."""
    scalar_count = consume_scalar_alias(tool_input)
    collection_aliases = [key for key in ("files", "paths") if key in tool_input]
    for key in collection_aliases:
        value = tool_input[key]
        if not isinstance(value, list):
            reject("HOOK-PATH-LIST")
        if any(not isinstance(item, str) or not item for item in value):
            reject("HOOK-PATH-TYPE")
    if len(collection_aliases) > 1 or (scalar_count and collection_aliases):
        reject("HOOK-PATH-ALIAS")
    for key in collection_aliases:
        for item in tool_input[key]:
            add_path(item)

    if "edits" in tool_input:
        edits = tool_input["edits"]
        if not isinstance(edits, list):
            reject("HOOK-PATH-LIST")
        for edit in edits:
            if not isinstance(edit, dict):
                reject("HOOK-PATH-TYPE")
            consume_scalar_alias(edit)


def _patch_segments(command: object) -> list[str]:
    """Return the string parts of a command in either payload form."""
    if isinstance(command, str):
        return [command]
    if isinstance(command, list):
        return [item for item in command if isinstance(item, str)]
    return []


def is_patch_envelope(tool_name: object, command: object) -> bool:
    """Decide by tool name, or by a segment that opens with the envelope marker.

    Matching a marker anywhere inside a command would misread an ordinary shell
    command that merely mentions one, so only a leading marker counts."""
    if tool_name == "apply_patch":
        return True
    return any(
        segment.lstrip().startswith(PATCH_BEGIN) for segment in _patch_segments(command)
    )


def collect_patch_targets(command: object) -> bool:
    """Read a patch envelope's file headers into the path pipeline.

    The envelope is data. Its headers name the files the patch would write, and
    those paths receive the same manifest, secret-adjacency and document-route
    evaluation a structured write receives. The body is never interpreted: a
    line that resembles a shell command is inert text here.

    Returns True when an envelope was found, so a payload that names the patch
    tool but carries something else still reaches the shell observer."""
    segments = [
        segment
        for segment in _patch_segments(command)
        if PATCH_BEGIN in segment or any(header in segment for header in PATCH_HEADERS)
    ]
    if not segments:
        return False
    for segment in segments:
        if PATCH_BEGIN in segment and PATCH_END not in segment:
            reject("HOOK-PATCH-ENVELOPE")
        for line in segment.splitlines():
            stripped = line.strip()
            for header in PATCH_HEADERS:
                if stripped.startswith(header):
                    target = stripped[len(header) :].strip()
                    if not target:
                        reject("HOOK-PATCH-PATH")
                    add_path(target)
                    break
    return True


def note_shell_target(shell_targets: list[str], value: str) -> None:
    if not isinstance(value, str) or not value or value.startswith("-"):
        return
    if value.startswith("/"):
        if not project_dir or not value.startswith(project_dir + "/"):
            return
        value = value[len(project_dir) + 1 :]
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        return
    candidate = PurePosixPath(value)
    if (
        value.startswith("./")
        or value.endswith("/")
        or "//" in value
        or candidate.is_absolute()
        or "." in candidate.parts
        or ".." in candidate.parts
        or candidate.as_posix() != value
    ):
        return
    if value not in shell_targets:
        shell_targets.append(value)


def collect_shell_targets(command: object) -> list[str]:
    """Read a shell command's obvious write targets.

    A shell command can create or modify a tracked file without ever reaching a
    structured file tool. Read its obvious write targets so the guard can still
    report the surface, but keep them out of the path pipeline: an unparsed
    guess must never reach the affected-surface selector, whose failure is a
    hard block. This observation is advisory and detects no interpreter-mediated
    or otherwise indirect write."""
    shell_targets: list[str] = []
    if not isinstance(command, str) or not command:
        return shell_targets
    try:
        tokens = shlex.split(command, comments=True)
    except ValueError:
        tokens = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in (">", ">>") and index + 1 < len(tokens):
            note_shell_target(shell_targets, tokens[index + 1])
            index += 2
            continue
        if token.startswith(">") and len(token) > 1 and not token.startswith(">&"):
            note_shell_target(shell_targets, token.lstrip(">"))
        elif token in ("tee", "/usr/bin/tee"):
            for following in tokens[index + 1 :]:
                if following in ("|", "&&", ";", "||"):
                    break
                note_shell_target(shell_targets, following)
        elif token in ("sed", "/usr/bin/sed") and any(
            following == "-i" or following.startswith("-i")
            for following in tokens[index + 1 :]
        ):
            for following in tokens[index + 1 :]:
                if following in ("|", "&&", ";", "||"):
                    break
                note_shell_target(shell_targets, following)
        index += 1
    return shell_targets


def safe_registry_file(root: str, relative: PurePosixPath, code: str) -> Path:
    root_path = Path(root)
    try:
        root_mode = os.lstat(root_path).st_mode
    except OSError as exc:
        reject_with_detail(code, str(exc))
    if stat.S_ISLNK(root_mode) or not stat.S_ISDIR(root_mode):
        reject_with_detail(code, "resolved repository root must be a real directory")
    cursor = root_path
    for index, part in enumerate(relative.parts):
        cursor /= part
        try:
            mode = os.lstat(cursor).st_mode
        except OSError as exc:
            reject_with_detail(code, f"{relative.as_posix()}: {exc}")
        if stat.S_ISLNK(mode):
            reject_with_detail(
                code, f"{relative.as_posix()}: symlink component {part!r} is forbidden"
            )
        final = index == len(relative.parts) - 1
        if not final and not stat.S_ISDIR(mode):
            reject_with_detail(
                code, f"{relative.as_posix()}: parent {part!r} is not a directory"
            )
        if final and not stat.S_ISREG(mode):
            reject_with_detail(code, f"{relative.as_posix()}: not a regular file")
    try:
        cursor.resolve(strict=True).relative_to(root_path.resolve(strict=True))
    except (OSError, ValueError) as exc:
        reject_with_detail(
            code, f"{relative.as_posix()}: escapes repository root: {exc}"
        )
    return cursor


def load_document_routes(root: str) -> tuple[dict[str, object], ...]:
    registry_relative = PurePosixPath("docs/99.templates/registry.json")
    try:
        registry_path = safe_registry_file(root, registry_relative, "HOOK-DOC-REGISTRY")
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        reject_with_detail("HOOK-DOC-REGISTRY", str(exc))
    if not isinstance(registry, dict) or registry.get("schema_version") != 9:
        reject_with_detail("HOOK-DOC-REGISTRY", "schema_version must be 9")
    profiles = registry.get("profiles") if isinstance(registry, dict) else None
    if not isinstance(profiles, list) or not profiles:
        reject_with_detail("HOOK-DOC-REGISTRY", "profiles must be a non-empty list")
    routes: list[dict[str, object]] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            reject_with_detail("HOOK-DOC-REGISTRY", "profile must be an object")
        profile_id = profile.get("id")
        pattern = profile.get("path_pattern")
        template = profile.get("template_source")
        if not isinstance(profile_id, str) or not isinstance(pattern, str):
            reject_with_detail(
                "HOOK-DOC-REGISTRY", "profile id and path_pattern must be strings"
            )
        if template is not None and not isinstance(template, str):
            reject_with_detail("HOOK-DOC-REGISTRY", "template_source must be a string")
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            reject_with_detail("HOOK-DOC-REGISTRY", f"{profile_id}: {exc}")
        routes.append({"id": profile_id, "pattern": compiled, "template": template})
    return tuple(routes)


def retired_document_owner(path: str) -> str:
    basename = path.rsplit("/", 1)[-1]
    if path.startswith("docs/01.requirements/") and basename.startswith(
        ("prd-", "srs-", "ifc-", "interface-")
    ):
        return "sdlc/requirement"
    if path.startswith("docs/03.specs/"):
        return {
            "design.md": "sdlc/spec",
            "tests.md": "sdlc/spec",
            "agent-design.md": "sdlc/spec",
            "tasks.md": "sdlc/task",
        }.get(basename, "")
    return ""


def authored_doc_route(
    path: str, resolved_root: str, document_routes: tuple[dict[str, object], ...]
) -> tuple[str, str] | None:
    if not path.endswith(".md"):
        return None
    if path.startswith(".agents/") or path.startswith("docs/99.templates/"):
        return None
    if not re.match(
        r"^docs/(01\.requirements|02\.architecture|03\.specs|04\.execution|"
        r"05\.operations|90\.references|98\.archive)(/|$)",
        path,
    ):
        return None
    retired_owner = retired_document_owner(path)
    if retired_owner:
        reject_with_detail(
            "HOOK-DOC-RETIRED",
            f"{path} is a retired standalone form; use registry profile {retired_owner}",
        )
    matches = [route for route in document_routes if route["pattern"].fullmatch(path)]
    if len(matches) != 1:
        reject_with_detail(
            "HOOK-DOC-ROUTE",
            f"{path} must resolve to exactly one profile in docs/99.templates/registry.json",
        )
    route = matches[0]
    profile_id = str(route["id"])
    template = route["template"]
    if template is None:
        return (profile_id, "no copyable template; consult docs/99.templates/README.md")
    template_path = PurePosixPath(str(template))
    if (
        template_path.is_absolute()
        or template_path.parts[:3] != ("docs", "99.templates", "templates")
        or any(part in {"", ".", ".."} for part in template_path.parts)
    ):
        reject_with_detail(
            "HOOK-DOC-TEMPLATE", f"{profile_id} has an unsafe template path"
        )
    safe_registry_file(resolved_root, template_path, "HOOK-DOC-TEMPLATE")
    return (profile_id, template_path.as_posix())


def build_messages(resolved_root: str, shell_targets: list[str]) -> list[str]:
    manifest_re = re.compile(
        r"(gitops/.*\.ya?ml|infrastructure/.*\.ya?ml|examples/sample-app/.*\.ya?ml|"
        r"examples/.*/gitops/.*\.ya?ml|examples/.*/kubernetes/.*\.ya?ml|traefik/.*\.ya?ml)$"
    )
    secret_re = re.compile(r"(secret|credential|password|token)", re.IGNORECASE)
    document_routes = load_document_routes(resolved_root)

    messages: list[str] = []
    for path in paths:
        if manifest_re.search(path):
            messages.append(
                "\n".join(
                    [
                        f"Editing Kubernetes manifest `{path}`.",
                        "- Keep the change GitOps-first: repository review -> ArgoCD reconciliation.",
                        "- Do not introduce plaintext Kubernetes secrets.",
                        "- Run explicit repository QA for manifest and secret-handling validation.",
                    ]
                )
            )
        if secret_re.search(path):
            messages.append(
                "\n".join(
                    [
                        f"File name is secret-adjacent: `{path}`.",
                        "- Never write plaintext secret values.",
                        "- Use ExternalSecret or SealedSecret-style patterns only.",
                    ]
                )
            )
        route = authored_doc_route(path, resolved_root, document_routes)
        if route:
            profile_id, template = route
            if template.startswith("generated by "):
                messages.append(
                    "\n".join(
                        [
                            f"Editing generated documentation `{path}`.",
                            f"- This path is {template}.",
                            "- Route policy or procedure changes to the canonical owner document instead.",
                            "- Run explicit repository QA for documentation template enforcement.",
                        ]
                    )
                )
            else:
                route_line = (
                    f"- Required template: `{template}`."
                    if template.startswith("docs/99.templates/templates/")
                    else f"- Route note: `{template}`."
                )
                messages.append(
                    "\n".join(
                        [
                            f"Editing authored documentation `{path}`.",
                            "- Template-First is mandatory: resolve the route in `docs/99.templates/registry.json`; use `docs/99.templates/README.md` for author guidance.",
                            f"- Registry profile: `{profile_id}`.",
                            route_line,
                            "- New authored docs must keep `status: draft`, required template headings, and the registry-selected relationship section.",
                            "- Folder-level adds, moves, or removals require the owning `README.md` to be updated in the same change.",
                            "- Run explicit repository QA for documentation template enforcement.",
                        ]
                    )
                )

    for target in shell_targets:
        if (
            manifest_re.search(target)
            or secret_re.search(target)
            or target.endswith(".md")
        ):
            messages.append(
                "\n".join(
                    [
                        f"Shell command writes `{target}`.",
                        "- The structured-tool guard did not see this write; the same"
                        " manifest, secret, and template rules still apply.",
                        "- Prefer a file tool so the route and template check runs, or"
                        " run explicit repository QA after the change.",
                    ]
                )
            )
    return messages


def run_surface_selector(resolved_root: str) -> bool:
    """Run the affected-surface selector over the collected paths.

    The program always comes from the project directory. The resolved root is
    derived from tool input, so it may select data only; letting it select the
    executable would make this guard run code from the tree it is guarding."""
    handle, paths_file = tempfile.mkstemp(suffix=".nul")
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(b"".join(path.encode("utf-8") + b"\0" for path in paths))
        completed = subprocess.run(
            (
                "python3",
                os.path.join(project_dir, SELECTOR_RELATIVE_PATH),
                "--root",
                resolved_root,
                "--lane",
                "affected",
                "--paths-file",
                paths_file,
                "--delimiter",
                "nul",
                "--format",
                "json",
            ),
            capture_output=True,
            text=True,
            timeout=SELECTOR_TIMEOUT_SECONDS,
        )
    except subprocess.SubprocessError:
        # A hung or unlaunchable selector is a failure, never a silent pass.
        return False
    finally:
        try:
            os.unlink(paths_file)
        except OSError:
            pass
    return completed.returncode == 0


def read_payload(provider: str) -> str:
    raw = sys.stdin.read()
    if not raw and provider == "claude":
        # Only the Claude runtime sets this variable. Reading it under another
        # provider would let an unrelated exported value reach the evaluated
        # payload, so the fallback stays bound to the adapter that names it.
        raw = os.environ.get("CLAUDE_TOOL_INPUT", "")
    return raw


def main(argv: list[str] | None = None) -> int:
    global project_dir

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=PROVIDERS)
    parser.add_argument("--project-dir", default="")
    arguments = parser.parse_args(argv)

    claude = arguments.provider == "claude"
    project_dir = (
        arguments.project_dir
        or (os.environ.get("CLAUDE_PROJECT_DIR", "") if claude else "")
    ).rstrip("/")
    if not project_dir:
        project_dir = (
            git_value(os.getcwd(), "--show-toplevel").rstrip("/") or os.getcwd()
        )

    raw = read_payload(arguments.provider)
    try:
        data = json.loads(raw) if raw else {}
    except (TypeError, json.JSONDecodeError):
        reject("HOOK-PAYLOAD-JSON")
    if not isinstance(data, dict):
        reject("HOOK-PAYLOAD-SHAPE")

    if "tool_input" in data and not isinstance(data["tool_input"], dict):
        reject("HOOK-PAYLOAD-SHAPE")
    tool_input = data.get("tool_input", {})

    collect_structured_paths(tool_input)
    command = tool_input.get("command")
    patched = (
        collect_patch_targets(command)
        if is_patch_envelope(data.get("tool_name"), command)
        else False
    )
    shell_targets = [] if patched else collect_shell_targets(command)

    environment_path = (
        os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH", "") if claude else ""
    )
    if environment_path:
        add_path(environment_path)
    if len(absolute_roots) > 1:
        reject("HOOK-PATH-ROOT")
    resolved_root = next(iter(absolute_roots), project_dir)

    for candidate in paths:
        # QA may resolve a deleted historical source to its current owner. An
        # edit must not use that deletion proof to recreate the retired
        # authority root.
        if candidate == "docs/00.agent-governance" or candidate.startswith(
            "docs/00.agent-governance/"
        ):
            reject_with_detail(
                "HOOK-PATH-RETIRED", "common authority is owned by .agents/"
            )
        cursor = Path(resolved_root)
        for part in PurePosixPath(candidate).parts:
            cursor /= part
            if cursor.is_symlink():
                reject("HOOK-PATH-SYMLINK")

    messages = build_messages(resolved_root, shell_targets)
    if messages:
        print(json.dumps({"systemMessage": "\n\n".join(messages)}))

    if not run_surface_selector(resolved_root):
        print(
            json.dumps(
                {
                    "systemMessage": "Affected-surface selection rejected an edit path. Normalize it to one repository-relative POSIX path and update the canonical surface contract before editing."
                }
            )
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
