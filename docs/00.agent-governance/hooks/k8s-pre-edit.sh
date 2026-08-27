#!/usr/bin/env bash
# k8s-pre-edit.sh — warn before editing Kubernetes, secrets, or authored docs.
# Runs at PreToolUse for Write|Edit|MultiEdit. Invalid path transport fails closed.
# Accept boundary: any path inside this repository, including any of its linked
# worktrees. Everything outside this repository is rejected. A worktree path is
# resolved against its own worktree root, never against PROJECT_DIR.
# Trust boundary: every program this hook runs comes from PROJECT_DIR. A root
# derived from tool input selects data only; it never selects an executable.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
INPUT_FILE="$(mktemp)"
PATHS_FILE="$(mktemp --suffix=.nul)"
SELECT_LOG="$(mktemp)"
ROOT_FILE="$(mktemp)"
trap 'rm -f "$INPUT_FILE" "$PATHS_FILE" "$SELECT_LOG" "$ROOT_FILE"' EXIT
cat >"$INPUT_FILE"
export PROJECT_DIR INPUT_FILE PATHS_FILE ROOT_FILE CLAUDE_TOOL_INPUT_FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-}" CLAUDE_TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

python3 - <<'PY'
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

project_dir = os.environ.get("PROJECT_DIR", "").rstrip("/")
raw = Path(os.environ["INPUT_FILE"]).read_text(encoding="utf-8")
if not raw:
    raw = os.environ.get("CLAUDE_TOOL_INPUT", "")

paths: list[str] = []
absolute_roots: set[str] = set()
_git_cache: dict[tuple[str, ...], str] = {}

GIT_TIMEOUT_SECONDS = 5


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
    """Accept an absolute path only inside PROJECT_DIR or a linked worktree of
    the same repository, and return it relative to its own worktree root.

    Worktree resolution is tried first, because a linked worktree may live
    under PROJECT_DIR and a plain prefix strip would then yield a path that is
    relative to the wrong tree."""
    if not project_dir:
        reject("HOOK-PATH-ROOT")
    directory = nearest_existing_directory(path)
    worktree_root = ""
    if directory and repository_identity(directory) == repository_identity(project_dir) != "":
        worktree_root = git_value(directory, "--show-toplevel").rstrip("/")
    if worktree_root and path.startswith(worktree_root + "/"):
        absolute_roots.add(worktree_root)
        return path[len(worktree_root) + 1 :]
    if path.startswith(project_dir + "/"):
        absolute_roots.add(project_dir)
        return path[len(project_dir) + 1 :]
    reject("HOOK-PATH-ROOT")
    raise SystemExit(2)


def add_path(value):
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


try:
    data = json.loads(raw) if raw else {}
except (TypeError, json.JSONDecodeError):
    reject("HOOK-PAYLOAD-JSON")
if not isinstance(data, dict):
    reject("HOOK-PAYLOAD-SHAPE")


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


if "tool_input" in data and not isinstance(data["tool_input"], dict):
    reject("HOOK-PAYLOAD-SHAPE")
tool_input = data.get("tool_input", {})
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
    value = tool_input[key]
    for item in value:
        add_path(item)

if "edits" in tool_input:
    edits = tool_input["edits"]
    if not isinstance(edits, list):
        reject("HOOK-PATH-LIST")
    for edit in edits:
        if not isinstance(edit, dict):
            reject("HOOK-PATH-TYPE")
        consume_scalar_alias(edit)

environment_path = os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH", "")
if environment_path:
    add_path(environment_path)
if len(absolute_roots) > 1:
    reject("HOOK-PATH-ROOT")
resolved_root = next(iter(absolute_roots), project_dir)

for candidate in paths:
    cursor = Path(resolved_root)
    for part in PurePosixPath(candidate).parts:
        cursor /= part
        if cursor.is_symlink():
            reject("HOOK-PATH-SYMLINK")

Path(os.environ["ROOT_FILE"]).write_text(resolved_root, encoding="utf-8")
Path(os.environ["PATHS_FILE"]).write_bytes(
    b"".join(path.encode("utf-8") + b"\0" for path in paths)
)

manifest_re = re.compile(
    r"(gitops/.*\.ya?ml|infrastructure/.*\.ya?ml|examples/sample-app/.*\.ya?ml|"
    r"examples/.*/gitops/.*\.ya?ml|examples/.*/kubernetes/.*\.ya?ml|traefik/.*\.ya?ml)$"
)
secret_re = re.compile(r"(secret|credential|password|token)", re.IGNORECASE)


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
        reject_with_detail(code, f"{relative.as_posix()}: escapes repository root: {exc}")
    return cursor


def load_document_routes(root: str) -> tuple[dict[str, object], ...]:
    registry_relative = PurePosixPath("docs/99.templates/registry.json")
    try:
        registry_path = safe_registry_file(root, registry_relative, "HOOK-DOC-REGISTRY")
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        reject_with_detail("HOOK-DOC-REGISTRY", str(exc))
    profiles = registry.get("profiles") if isinstance(registry, dict) else None
    if not isinstance(profiles, list) or not profiles:
        reject_with_detail("HOOK-DOC-REGISTRY", "profiles must be a non-empty list")
    routes: list[dict[str, object]] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            reject_with_detail("HOOK-DOC-REGISTRY", "profile must be an object")
        profile_id = profile.get("id")
        pattern = profile.get("pathPattern")
        template = profile.get("template")
        if not isinstance(profile_id, str) or not isinstance(pattern, str):
            reject_with_detail(
                "HOOK-DOC-REGISTRY", "profile id and pathPattern must be strings"
            )
        if template is not None and not isinstance(template, str):
            reject_with_detail("HOOK-DOC-REGISTRY", "template must be a string")
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            reject_with_detail("HOOK-DOC-REGISTRY", f"{profile_id}: {exc}")
        routes.append({"id": profile_id, "pattern": compiled, "template": template})
    return tuple(routes)


document_routes = load_document_routes(resolved_root)


def retired_document_owner(path: str) -> str:
    basename = path.rsplit("/", 1)[-1]
    if path.startswith("docs/01.requirements/") and basename.startswith(
        ("prd-", "srs-", "ifc-", "interface-")
    ):
        return "sdlc/requirement-package"
    if path.startswith("docs/03.specs/"):
        return {
            "design.md": "sdlc/spec",
            "tests.md": "sdlc/spec",
            "agent-design.md": "sdlc/spec",
            "tasks.md": "sdlc/task",
        }.get(basename, "")
    return ""


def authored_doc_route(path: str) -> tuple[str, str] | None:
    if not path.endswith(".md"):
        return None
    if path.startswith("docs/00.agent-governance/") or path.startswith("docs/99.templates/"):
        return None
    if path == "docs/90.references/llm-wiki/wiki-index.md":
        return (
            "exception/generated-record",
            "generated by scripts/generate-llm-wiki-index.sh; do not edit by hand",
        )
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


messages: list[str] = []
for path in paths:
    if manifest_re.search(path):
        messages.append(
            "\n".join(
                [
                    f"Editing Kubernetes manifest `{path}`.",
                    "- Keep the change GitOps-first: repository review -> ArgoCD reconciliation.",
                    "- Do not introduce plaintext Kubernetes secrets.",
                    "- The PostToolUse hook will run manifest and secret-handling validation.",
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
    route = authored_doc_route(path)
    if route:
        profile_id, template = route
        if template.startswith("generated by "):
            messages.append(
                "\n".join(
                    [
                        f"Editing generated documentation `{path}`.",
                        f"- This path is {template}.",
                        "- Route policy or procedure changes to the canonical owner document instead.",
                        "- The PostToolUse hook will run documentation template enforcement.",
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
                        "- The PostToolUse hook will run documentation template enforcement.",
                    ]
                )
            )

if messages:
    print(json.dumps({"systemMessage": "\n\n".join(messages)}))
PY

RESOLVED_ROOT="$PROJECT_DIR"
if [ -s "$ROOT_FILE" ]; then
  RESOLVED_ROOT="$(cat "$ROOT_FILE")"
fi

# The program always comes from PROJECT_DIR. RESOLVED_ROOT is derived from tool
# input, so it may select data only; letting it select the executable would make
# this guard run code from the tree it is guarding.
if ! python3 "$PROJECT_DIR/scripts/select-affected-surfaces.py" \
  --root "$RESOLVED_ROOT" --lane affected --paths-file "$PATHS_FILE" \
  --delimiter nul --format json >"$SELECT_LOG" 2>&1; then
  python3 - <<'PY'
import json

print(json.dumps({"systemMessage": "Affected-surface selection rejected an edit path. Normalize it to one repository-relative POSIX path and update the canonical surface contract before editing."}))
PY
  exit 2
fi

exit 0
