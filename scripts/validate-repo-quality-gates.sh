#!/usr/bin/env bash
# validate-repo-quality-gates.sh — repository docs, workflow, script, and version contract checks
# Usage: bash scripts/validate-repo-quality-gates.sh [repo-root]
set -euo pipefail

ROOT_INPUT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
ROOT_DIR="$(cd "$ROOT_INPUT" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERR python3 is required for repository quality validation" >&2
  exit 1
fi

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
  echo "ERR python3 PyYAML package is required for repository quality validation" >&2
  exit 1
fi

if ! python3 -c 'import jsonschema' >/dev/null 2>&1; then
  echo "ERR python3 jsonschema package is required for repository quality validation" >&2
  exit 1
fi

python3 "$ROOT_DIR/scripts/validate-document-contract-registry.py" --self-test
python3 "$ROOT_DIR/scripts/validate-document-contract-registry.py" --root "$ROOT_DIR" --mode strict
python3 "$ROOT_DIR/scripts/validate-markdown-profiles.py" --root "$ROOT_DIR" --mode strict
python3 "$ROOT_DIR/scripts/validate-links-and-owners.py" --root "$ROOT_DIR" --self-test
python3 "$ROOT_DIR/scripts/validate-links-and-owners.py" --root "$ROOT_DIR" --mode strict
python3 "$ROOT_DIR/scripts/validate-gitops-change-set.py" --self-test
python3 "$ROOT_DIR/scripts/validate-gitops-change-set.py" --root "$ROOT_DIR" --base-ref HEAD
python3 "$ROOT_DIR/scripts/validate-vault-eso-contracts.py" --self-test
python3 "$ROOT_DIR/scripts/validate-vault-eso-contracts.py" --root "$ROOT_DIR"
python3 "$ROOT_DIR/scripts/validate-affected-surfaces.py" --self-test
python3 "$ROOT_DIR/scripts/validate-affected-surfaces.py" --root "$ROOT_DIR"
python3 "$ROOT_DIR/scripts/validate-agent-role-semantics.py" --self-test
python3 "$ROOT_DIR/scripts/validate-agent-role-semantics.py" --root "$ROOT_DIR"

python3 "$ROOT_DIR/scripts/validate-agent-roster-currentness.py" \
  "$ROOT_DIR" --self-test
python3 "$ROOT_DIR/scripts/validate-agent-roster-currentness.py" "$ROOT_DIR"

python3 - "$ROOT_DIR" <<'PY'
import collections
import copy
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / "scripts"))
from document_contracts import (  # noqa: E402 - repository-local contract module
    DocumentContractError,
    TARGET_ROOTS,
    classify_path,
    load_registry,
)

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback path
    tomllib = None

root = pathlib.Path(sys.argv[1])
failures = []


class DuplicateKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping_without_duplicates(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise ValueError(f"duplicate YAML key: {key}")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping_without_duplicates,
)


def fail(message: str) -> None:
    failures.append(f"ERR {message}")


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_bytes(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def load_yaml(path: pathlib.Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=DuplicateKeyLoader) or {}


def load_yaml_documents(path: pathlib.Path) -> list:
    with path.open(encoding="utf-8") as handle:
        return [document or {} for document in yaml.load_all(handle, Loader=DuplicateKeyLoader)]


def workflow_on(data):
    return data.get("on") if "on" in data else data.get(True, {})


def load_json(path: pathlib.Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_toml(path: pathlib.Path):
    if tomllib is None:
        raise RuntimeError("python3 tomllib module is required to parse TOML agent adapters")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_markdown_frontmatter(path: pathlib.Path) -> dict:
    text = read_text(path)
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        fail(f"{rel(path)} missing YAML frontmatter")
        return {}
    try:
        return yaml.load(frontmatter.group(1), Loader=DuplicateKeyLoader) or {}
    except Exception as exc:
        fail(f"{rel(path)} frontmatter parse failed: {exc}")
        return {}


def has_markdown_frontmatter(path: pathlib.Path, text: str | None = None) -> bool:
    content = read_text(path) if text is None else text
    return bool(re.match(r"^---\n.*?\n---\n", content, re.DOTALL))


def strip_multiline_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove HTML comments while retaining visible text around them."""
    visible = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                return "".join(visible), True
            cursor = end + 3
            in_comment = False
            continue
        start = line.find("<!--", cursor)
        if start < 0:
            visible.append(line[cursor:])
            break
        visible.append(line[cursor:start])
        cursor = start + 4
        in_comment = True
    return "".join(visible), in_comment


def visible_markdown_lines(markdown: str) -> list[tuple[int, str]]:
    """Return visible Markdown lines with their original zero-based offsets."""
    visible_lines: list[tuple[int, str]] = []
    fence_character = None
    fence_length = 0
    in_comment = False
    opening_fence = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

    for source_offset, raw_line in enumerate(markdown.splitlines()):
        if fence_character is not None:
            closing_fence = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing_fence.match(raw_line):
                fence_character = None
                fence_length = 0
            continue

        line, in_comment = strip_multiline_html_comments(raw_line, in_comment)
        fence_match = opening_fence.match(line)
        if fence_match:
            marker = fence_match.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            continue

        visible_lines.append((source_offset, line))

    return visible_lines


def normalize_tools(value) -> str:
    if isinstance(value, str):
        return ", ".join(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, list):
        return ", ".join(str(part).strip() for part in value if str(part).strip())
    return ""


def extract_scope_imports(text: str) -> list[str]:
    return sorted(re.findall(r"@import\s+(docs/00\.agent-governance/scopes/[A-Za-z0-9_.-]+\.md)", text))


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(root))


def is_historical_evidence_path(path: pathlib.Path) -> bool:
    return (
        path == root / "docs/00.agent-governance/memory/progress.md"
        or path.is_relative_to(root / "docs/90.references/audits")
        or path.is_relative_to(root / "docs/98.archive")
    )


def collect_strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(collect_strings(item))
        return values
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(collect_strings(item))
        return values
    return []


def branch_prefixes_from_git_workflow(path: pathlib.Path) -> list[str]:
    prefixes: list[str] = []
    for line in read_text(path).splitlines():
        match = re.match(r"^-\s+`([a-z0-9-]+)/<[^`]+>`$", line.strip())
        if match:
            prefixes.append(match.group(1))
    return prefixes


def format_branch_prefixes(prefixes: list[str]) -> str:
    return ", ".join(f"{prefix}/" for prefix in prefixes)


def parse_env_keys(path: pathlib.Path) -> list[str]:
    keys: list[str] = []
    for raw_line in read_text(path).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key = stripped.split("=", 1)[0].strip()
        if key:
            keys.append(key)
    return keys


def extract_ci_branch_policy_prefixes(branch_policy_text: str) -> list[str]:
    match = re.search(r"allowed_branch_regex=['\"]\^\(([^)]+)\)/['\"]", branch_policy_text)
    if not match:
        return []
    return match.group(1).split("|")


def extract_pr_template_prefixes(text: str) -> list[str]:
    return [prefix.rstrip("/") for prefix in re.findall(r"`([a-z0-9-]+/)`", text)]


def has_cloud_example_snapshot_preservation_prompt(text: str) -> bool:
    required_terms = [
        "examples/aws",
        "examples/azure",
        "cloud example snapshot",
        "approved",
        "provider",
        "refresh",
        "spec",
    ]
    for line in text.splitlines():
        normalized = line.casefold()
        if (
            all(term in normalized for term in required_terms)
            and "preserv" in normalized
            and "boundar" in normalized
        ):
            return True
    return False


def markdown_table_after_heading(
    text: str,
    heading: str | tuple[str, ...],
) -> list[list[str]]:
    rows, diagnostic = parse_markdown_table_after_heading(text, heading)
    if diagnostic:
        fail(diagnostic)
        return []
    return rows


def parse_markdown_table_after_heading(
    text: str,
    heading: str | tuple[str, ...],
) -> tuple[list[list[str]], str | None]:
    headings = (heading,) if isinstance(heading, str) else heading
    visible_lines = visible_markdown_lines(text)
    matches = [
        (source_offset, candidate)
        for source_offset, line in visible_lines
        for candidate in headings
        if line.strip() == candidate
    ]
    if not matches:
        return [], f"missing visible markdown heading: one of {headings!r}"
    if len(matches) != 1:
        return (
            [],
            "ambiguous visible markdown table headings: "
            f"{[candidate for _, candidate in matches]!r}",
        )
    start, _ = matches[0]

    table_lines: list[str] = []
    for source_offset, line in visible_lines:
        if source_offset <= start:
            continue
        stripped = line.strip()
        if not stripped:
            if table_lines:
                break
            continue
        if not stripped.startswith("|"):
            if table_lines:
                break
            continue
        table_lines.append(stripped)

    rows: list[list[str]] = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows, None


def profiled_readme_table_headings(title: str) -> tuple[str, str]:
    """Accept one visible legacy H2 or canonical implementation-profile H3."""
    return (f"## {title}", f"### {title}")


def assert_profiled_readme_table_heading_probe() -> None:
    expected = [["Name", "Value"], ["alpha", "one"]]
    consumer_titles = (
        "Example Role Matrix",
        "Script Inventory",
        "Script Classification Matrix",
        "Kube-linter Exclusion Matrix",
        "Service Coverage Matrix",
        "External Service Contract Matrix",
        "Secret Management Responsibility Matrix",
        "Workload Coverage Matrix",
        "AppProject Allow-list Rationale Matrix",
        "Workload Image and Kind Policy Matrix",
        "Namespace Ownership Matrix",
        "Infrastructure Coverage Matrix",
        "WSL2 Runtime Prerequisite Matrix",
        "Bootstrap Boundary Matrix",
        "Infrastructure Test Inventory",
        "Traefik Route Inventory",
    )
    candidates = profiled_readme_table_headings("Probe Index")
    documents = {
        "visible legacy H2": """# Probe

## Probe Index

| Name | Value |
| --- | --- |
| alpha | one |
""",
        "visible canonical H3": """# Probe

### Probe Index

| Name | Value |
| --- | --- |
| alpha | one |
""",
        "visible plus fenced fakes": """# Probe

```markdown
## Probe Index
| Name | Value |
| fake-backtick | ignored |
```

~~~markdown
### Probe Index
| Name | Value |
| fake-tilde | ignored |
~~~

### Probe Index

| Name | Value |
| --- | --- |
| alpha | one |
""",
        "visible plus multiline-comment fake": """# Probe

<!--
## Probe Index
| Name | Value |
| fake-comment | ignored |
-->

### Probe Index

| Name | Value |
| --- | --- |
| alpha | one |
""",
    }
    for label, document in documents.items():
        actual, diagnostic = parse_markdown_table_after_heading(
            document,
            candidates,
        )
        if diagnostic or actual != expected:
            fail(
                f"profiled README table heading probe failed for {label}: "
                f"rows={actual!r} diagnostic={diagnostic!r}"
            )

    duplicate = """# Probe

## Probe Index

### Probe Index

| Name | Value |
| --- | --- |
| alpha | one |
"""
    duplicate_rows, duplicate_diagnostic = parse_markdown_table_after_heading(
        duplicate,
        candidates,
    )
    if duplicate_rows or duplicate_diagnostic != (
        "ambiguous visible markdown table headings: "
        "['## Probe Index', '### Probe Index']"
    ):
        fail(
            "profiled README table heading duplicate probe failed: "
            f"rows={duplicate_rows!r} diagnostic={duplicate_diagnostic!r}"
        )

    for title in consumer_titles:
        for level in ("##", "###"):
            document = f"""# Probe

{level} {title}

| Name | Value |
| --- | --- |
| alpha | one |
"""
            actual, diagnostic = parse_markdown_table_after_heading(
                document,
                profiled_readme_table_headings(title),
            )
            if diagnostic or actual != expected:
                fail(
                    f"profiled README consumer probe failed for {level} {title}: "
                    f"rows={actual!r} diagnostic={diagnostic!r}"
                )

        hidden = f"""# Probe

```markdown
## {title}
| Name | Value |
| hidden-fence | ignored |
```

<!--
### {title}
| Name | Value |
| hidden-comment | ignored |
-->

### {title}

| Name | Value |
| --- | --- |
| alpha | one |
"""
        hidden_rows, hidden_diagnostic = parse_markdown_table_after_heading(
            hidden,
            profiled_readme_table_headings(title),
        )
        if hidden_diagnostic or hidden_rows != expected:
            fail(
                f"profiled README hidden consumer probe failed for {title}: "
                f"rows={hidden_rows!r} diagnostic={hidden_diagnostic!r}"
            )

        duplicate = f"""# Probe

## {title}

### {title}

| Name | Value |
| --- | --- |
| alpha | one |
"""
        duplicate_rows, duplicate_diagnostic = parse_markdown_table_after_heading(
            duplicate,
            profiled_readme_table_headings(title),
        )
        expected_duplicate = (
            "ambiguous visible markdown table headings: "
            f"['## {title}', '### {title}']"
        )
        if duplicate_rows or duplicate_diagnostic != expected_duplicate:
            fail(
                f"profiled README duplicate consumer probe failed for {title}: "
                f"rows={duplicate_rows!r} diagnostic={duplicate_diagnostic!r}"
            )


assert_profiled_readme_table_heading_probe()


def validate_component_matrix(text: str, heading: str) -> None:
    rows = markdown_table_after_heading(text, heading)
    if len(rows) < 2:
        fail(f"{heading} must contain a header and at least one component row")
        return
    expected_header = ["Required Component", "Current Surface", "Status", "Gap", "Remediation"]
    allowed_statuses = {"Ready", "Partial", "Missing"}
    if rows[0] != expected_header:
        fail(f"{heading} header must be: {' | '.join(expected_header)}")
    for row_number, row in enumerate(rows[1:], start=1):
        if len(row) != len(expected_header):
            fail(f"{heading} row {row_number} must have {len(expected_header)} columns")
            continue
        component, surface, status, gap, remediation = row
        for label, value in [
            ("Required Component", component),
            ("Current Surface", surface),
            ("Status", status),
            ("Gap", gap),
            ("Remediation", remediation),
        ]:
            if not value:
                fail(f"{heading} row {row_number} has empty {label}")
        if status not in allowed_statuses:
            fail(f"{heading} row {row_number} has unsupported Status value: {status}")
        if status == "Ready" and gap != "None":
            fail(f"{heading} row {row_number} with Status=Ready must use Gap=None")
        if status in {"Partial", "Missing"}:
            if gap in {"", "None"}:
                fail(f"{heading} row {row_number} with Status={status} must name a concrete Gap")
            if remediation in {"", "None"}:
                fail(f"{heading} row {row_number} with Status={status} must include concrete Remediation")
        if gap == "None" and not remediation:
            fail(f"{heading} row {row_number} with Gap=None still needs remediation guidance")


tracked = set()
try:
    proc = subprocess.run(["git", "ls-files"], cwd=root, check=True, text=True, capture_output=True)
    tracked = set(proc.stdout.splitlines())
except Exception as exc:
    fail(f"git ls-files failed: {exc}")

for tracked_path in sorted(tracked):
    if re.fullmatch(r"\.claude/[^/]+\.local\.md", tracked_path):
        fail(f"ignored local Claude/Hookify runtime rule must not be tracked: {tracked_path}")
    if tracked_path == ".env":
        fail(".env must remain untracked; commit .env.example only")
    tracked_name = pathlib.Path(tracked_path).name
    if tracked_name == "progress.md" and tracked_path != "docs/00.agent-governance/memory/progress.md":
        fail(f"tracked progress.md must live only at docs/00.agent-governance/memory/progress.md: {tracked_path}")
    if re.search(r"(^temp_|_(new|old|backup)(\.|$))", tracked_name):
        fail(f"tracked temporary or backup-style file name is not allowed: {tracked_path}")

workspace_readme_rel = "_workspace/README.md"
if workspace_readme_rel not in tracked:
    fail("_workspace/README.md is required as the tracked workspace staging contract")

workspace_scratch_ignore_check = subprocess.run(
    ["git", "check-ignore", "-q", "_workspace/probe.log"],
    cwd=root,
)
if workspace_scratch_ignore_check.returncode == 1:
    fail(".gitignore must ignore _workspace/* scratch artifacts")
elif workspace_scratch_ignore_check.returncode not in {0, 1}:
    fail("git check-ignore failed while validating _workspace scratch ignore contract")

workspace_readme_ignore_check = subprocess.run(
    ["git", "check-ignore", "-q", workspace_readme_rel],
    cwd=root,
)
if workspace_readme_ignore_check.returncode == 0:
    fail(".gitignore must unignore _workspace/README.md")
elif workspace_readme_ignore_check.returncode not in {0, 1}:
    fail("git check-ignore failed while validating _workspace README unignore contract")

workspace_tracked_paths = sorted(
    tracked_path
    for tracked_path in tracked
    if tracked_path == "_workspace" or tracked_path.startswith("_workspace/")
)
for tracked_path in workspace_tracked_paths:
    if tracked_path != workspace_readme_rel:
        fail(f"_workspace may track only README.md; remove or promote: {tracked_path}")

workspace_prohibited_path_pattern = re.compile(
    r"(token|secret|credential|auth|history|kubeconfig|ssh|password|diagnostic|profile|cache)",
    re.IGNORECASE,
)
for tracked_path in workspace_tracked_paths:
    if workspace_prohibited_path_pattern.search(tracked_path):
        fail(f"_workspace tracked path contains prohibited secret-risk wording: {tracked_path}")

requirements_stage = root / "docs/01.requirements"
if requirements_stage.exists():
    for requirement_doc in sorted(requirements_stage.glob("*.md")):
        if requirement_doc.name == "README.md":
            continue
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+\.md", requirement_doc.name):
            fail(
                "active PRDs must use numeric route "
                f"docs/01.requirements/<###-Numbering>-<feature-or-system>.md: {rel(requirement_doc)}"
            )
        if not re.fullmatch(r"\d{3}-.+\.md", requirement_doc.name):
            fail(
                "active PRD filename must start with a three-digit numeric prefix: "
                f"{rel(requirement_doc)}"
            )

specs_stage = root / "docs/03.specs"
if specs_stage.exists():
    for spec_entry in sorted(specs_stage.iterdir()):
        if spec_entry.name == "README.md":
            continue
        if spec_entry.is_dir():
            if not re.fullmatch(r"\d{3}-.+", spec_entry.name):
                fail(
                    "active Spec folder must start with a three-digit numeric prefix: "
                    f"{rel(spec_entry)}"
                )
            continue
        if spec_entry.is_file():
            fail(f"docs/03.specs may contain only README.md and numbered Spec folders: {rel(spec_entry)}")

env_ignore_check = subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=root)
if env_ignore_check.returncode == 1:
    fail(".env must remain ignored by Git")
elif env_ignore_check.returncode not in {0, 1}:
    fail("git check-ignore failed while validating .env ignore contract")

env_example_path = root / ".env.example"
env_path = root / ".env"
if not env_example_path.exists():
    fail(".env.example is required as the tracked environment key contract")
else:
    env_example_keys = parse_env_keys(env_example_path)
    duplicated_example_keys = sorted(key for key, count in collections.Counter(env_example_keys).items() if count > 1)
    if duplicated_example_keys:
        fail(".env.example contains duplicate keys: " + ", ".join(duplicated_example_keys))
    if env_path.exists():
        env_keys = parse_env_keys(env_path)
        duplicated_env_keys = sorted(key for key, count in collections.Counter(env_keys).items() if count > 1)
        if duplicated_env_keys:
            fail(".env contains duplicate keys: " + ", ".join(duplicated_env_keys))
        missing_env_keys = sorted(set(env_example_keys) - set(env_keys))
        extra_env_keys = sorted(set(env_keys) - set(env_example_keys))
        if missing_env_keys:
            fail(".env is missing keys from .env.example: " + ", ".join(missing_env_keys))
        if extra_env_keys:
            fail(".env has keys not present in .env.example: " + ", ".join(extra_env_keys))



claude_local_rule_paths = sorted((root / ".claude").glob("*.local.md"))
for local_rule_path in claude_local_rule_paths:
    local_rule_rel = rel(local_rule_path)
    local_rule_ignore_check = subprocess.run(["git", "check-ignore", "-q", local_rule_rel], cwd=root)
    if local_rule_ignore_check.returncode == 1:
        fail(f"{local_rule_rel} must remain ignored by Git")
    elif local_rule_ignore_check.returncode not in {0, 1}:
        fail(f"git check-ignore failed while validating local rule ignore contract: {local_rule_rel}")

    if local_rule_path.name.startswith("hookify."):
        text = read_text(local_rule_path)
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not frontmatter:
            fail(f"{local_rule_rel} missing Hookify YAML frontmatter")
            continue
        try:
            metadata = yaml.load(frontmatter.group(1), Loader=DuplicateKeyLoader) or {}
        except Exception as exc:
            fail(f"{local_rule_rel} Hookify frontmatter parse failed: {exc}")
            continue
        for field in ["name", "enabled", "event"]:
            if field not in metadata:
                fail(f"{local_rule_rel} missing Hookify frontmatter field: {field}")
        if metadata.get("event") not in {"bash", "file", "stop", "prompt", "all"}:
            fail(f"{local_rule_rel} has unsupported Hookify event: {metadata.get('event')}")
        if "action" in metadata and metadata.get("action") not in {"warn", "block"}:
            fail(f"{local_rule_rel} has unsupported Hookify action: {metadata.get('action')}")
        if "pattern" not in metadata and "conditions" not in metadata:
            fail(f"{local_rule_rel} must define Hookify pattern or conditions")

local_agents_dir = root / ".agents"
local_agents_skills_dir = root / ".agents" / "skills"
if local_agents_dir.exists() and not local_agents_dir.is_dir():
    fail(".agents must be a directory when present")
if local_agents_skills_dir.exists() and not local_agents_skills_dir.is_dir():
    fail(".agents/skills must be a directory when present")
if local_agents_skills_dir.is_dir():
    canonical_skill_paths = [
        root / tracked_path
        for tracked_path in sorted(tracked)
        if re.fullmatch(r"\.claude/skills/[^/]+/skill\.md", tracked_path)
    ]
    for canonical_skill_path in canonical_skill_paths:
        local_skill_path = local_agents_skills_dir / canonical_skill_path.parent.name / "skill.md"
        if not local_skill_path.exists():
            continue
        if read_bytes(local_skill_path) != read_bytes(canonical_skill_path):
            fail(
                "shared skill mirror drift: "
                f"{rel(local_skill_path)} differs from {rel(canonical_skill_path)}"
            )

allowed_top_level_docs = {
    "00.agent-governance",
    "01.requirements",
    "02.architecture",
    "03.specs",
    "04.execution",
    "05.operations",
    "90.references",
    "98.archive",
    "99.templates",
}
required_doc_dirs = {
    "00.agent-governance",
    "01.requirements",
    "02.architecture",
    "02.architecture/requirements",
    "02.architecture/decisions",
    "03.specs",
    "04.execution",
    "04.execution/plans",
    "04.execution/tasks",
    "05.operations",
    "05.operations/guides",
    "05.operations/policies",
    "05.operations/runbooks",
    "05.operations/incidents",
    "90.references",
    "98.archive",
    "99.templates",
}
old_top_level_docs = {
    "01.prd",
    "02.ard",
    "03.adr",
    "04.specs",
    "05.plans",
    "06.tasks",
    "07.guides",
    "08.operations",
    "09.runbooks",
    "10.incidents",
}

docs_dir = root / "docs"
actual_docs = {path.name for path in docs_dir.iterdir() if path.is_dir()}
for name in sorted(actual_docs & old_top_level_docs):
    fail(f"old docs stage folder must not exist after hard migration: docs/{name}")
for name in sorted(actual_docs - allowed_top_level_docs):
    fail(f"docs top-level folder is not allowed: docs/{name}")
for name in sorted(allowed_top_level_docs - actual_docs):
    fail(f"required docs top-level folder is missing: docs/{name}")

example_docs_required = {
    "01.requirements",
    "02.architecture",
    "02.architecture/requirements",
    "02.architecture/decisions",
    "03.specs",
    "04.execution",
    "04.execution/plans",
    "04.execution/tasks",
    "05.operations",
    "05.operations/guides",
    "05.operations/policies",
    "05.operations/runbooks",
}
example_docs_allowed_top_level = {
    "01.requirements",
    "02.architecture",
    "03.specs",
    "04.execution",
    "05.operations",
}
expected_provider_asset_counts = {"aws": 8, "azure": 14}
for provider in ["aws", "azure"]:
    example_docs = root / "examples" / provider / "docs"
    if example_docs.exists():
        fail(f"retired example docs root must be absent after ADM-006: {rel(example_docs)}")
    provider_root = root / "examples" / provider
    executable_assets = [
        path
        for path in provider_root.rglob("*")
        if path.is_file() and path.suffix.lower() != ".md"
    ]
    if len(executable_assets) != expected_provider_asset_counts[provider]:
        fail(
            f"{rel(provider_root)} executable asset count changed: "
            f"{len(executable_assets)} != {expected_provider_asset_counts[provider]}"
        )

examples_readme_path = root / "examples/README.md"
examples_readme_text = read_text(examples_readme_path)
example_role_rows = markdown_table_after_heading(
    examples_readme_text,
    profiled_readme_table_headings("Example Role Matrix"),
)
expected_example_role_header = [
    "Example path",
    "Role",
    "Active source of truth",
    "Validation",
]
expected_example_paths = ["sample-app/", "aws/", "azure/"]
if len(example_role_rows) < 2:
    fail("examples/README.md Example Role Matrix must contain a header and example rows")
elif example_role_rows[0] != expected_example_role_header:
    fail(
        "examples/README.md Example Role Matrix header must be: "
        + " | ".join(expected_example_role_header)
    )
else:
    indexed_example_paths: list[str] = []
    for row_number, row in enumerate(example_role_rows[1:], start=1):
        if len(row) != len(expected_example_role_header):
            fail(
                "examples/README.md Example Role Matrix "
                f"row {row_number} must have {len(expected_example_role_header)} columns"
            )
            continue
        path_cell, role, source_of_truth, validation = row
        match = re.fullmatch(r"`([^`]+/)`", path_cell)
        if not match:
            fail(
                "examples/README.md Example Role Matrix "
                f"row {row_number} must start with a backticked example directory"
            )
            continue
        example_path = match.group(1)
        indexed_example_paths.append(example_path)
        if not (root / "examples" / example_path.rstrip("/")).is_dir():
            fail(f"examples/README.md Example Role Matrix references missing directory: examples/{example_path}")
        for label, value in [
            ("Role", role),
            ("Active source of truth", source_of_truth),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"examples/README.md Example Role Matrix row {row_number} has empty {label}")
        for command in [
            "scripts/validate-repo-quality-gates.sh",
            "scripts/validate-k8s-manifests.sh",
            "scripts/check-secret-handling.sh",
        ]:
            if command not in validation:
                fail(f"examples/README.md Example Role Matrix row {row_number} must cite {command}")
        if example_path == "sample-app/":
            if "Minimal local k3d GitOps onboarding template" not in role:
                fail("examples/README.md sample-app role must identify the minimal local k3d onboarding template")
            if "../gitops/workloads/adminer/" not in source_of_truth:
                fail("examples/README.md sample-app source of truth must point to ../gitops/workloads/adminer/")
            for phrase in [
                "../gitops/workloads/<appname>/",
                "placeholder replacement",
                "validation",
                "active desired state",
            ]:
                if phrase not in source_of_truth:
                    fail(f"examples/README.md sample-app source of truth missing activation phrase: {phrase}")
        else:
            if "Cloud Example Snapshot" not in source_of_truth:
                fail(f"examples/README.md {example_path} source of truth must cite Cloud Example Snapshot")
            if "not live provider-latest guidance" not in source_of_truth:
                fail(f"examples/README.md {example_path} must not claim live provider-latest guidance")
    if indexed_example_paths != expected_example_paths:
        fail(
            "examples/README.md Example Role Matrix row order must be: "
            + ", ".join(expected_example_paths)
        )

sample_app_dir = root / "examples/sample-app"
expected_sample_app_files = [
    "README.md",
    "analysis-template.yaml",
    "external-secret.yaml",
    "ingress.yaml",
    "kustomization.yaml",
    "rollout.yaml",
    "service.yaml",
    "traefik-k3d.yaml.example",
]
actual_sample_app_files = sorted(path.name for path in sample_app_dir.iterdir() if path.is_file())
if actual_sample_app_files != expected_sample_app_files:
    fail(
        "examples/sample-app file set must stay minimal onboarding template: "
        + ", ".join(expected_sample_app_files)
    )

sample_app_readme = read_text(sample_app_dir / "README.md")
for phrase in [
    "최소 GitOps 템플릿",
    "fuller active reference",
    "gitops/workloads/adminer/",
    "feature branch + PR flow",
    "active GitOps desired state",
    "remoteRef.key",
    "secret values",
]:
    if phrase not in sample_app_readme:
        fail(f"examples/sample-app/README.md missing onboarding boundary phrase: {phrase}")
for active_reference_file in [
    "service-stable.yaml",
    "service-canary.yaml",
    "virtual-service.yaml",
    "destination-rule.yaml",
    "peer-authentication.yaml",
]:
    if not (root / "gitops/workloads/adminer" / active_reference_file).is_file():
        fail(f"gitops/workloads/adminer missing fuller active reference file: {active_reference_file}")

sample_app_external_secret = read_text(sample_app_dir / "external-secret.yaml")
for phrase in [
    "secret/apps/<appname>/config",
    "remoteRef.key",
    "apps/<appname>/config",
    "ClusterSecretStore path",
]:
    if phrase not in sample_app_external_secret:
        fail(f"examples/sample-app/external-secret.yaml missing app secret path contract phrase: {phrase}")
if "key: secret/apps/<appname>/config" in sample_app_external_secret:
    fail("examples/sample-app/external-secret.yaml remoteRef.key must exclude the Vault mount prefix")

active_app_secret_contracts = [
    (
        root / "docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md",
        [
            "secret/apps/<appname>/config",
            "remoteRef.key",
            "apps/<appname>/config",
            "mount prefix",
            "gitops/workloads/adminer/",
        ],
    ),
    (
        root / "docs/05.operations/policies/0007-app-gitops-onboarding-policy.md",
        [
            "Vault 경로 규칙",
            "secret/apps/<appname>/config",
            "ESO remoteRef",
            "apps/<appname>/config",
            "mount prefix 제외",
        ],
    ),
    (
        root / "docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md",
        [
            "secret/apps/${APP}/config",
            "ExternalSecret remoteRef.key",
            "apps/${APP}/config",
            "mount prefix secret/",
        ],
    ),
    (
        root / "gitops/README.md",
        [
            "Sample app ExternalSecret",
            "ESO remoteRef key",
            "apps/<appname>/config",
            "Vault CLI path remains",
            "secret/apps/<appname>/config",
        ],
    ),
]
for contract_path, phrases in active_app_secret_contracts:
    contract_text = read_text(contract_path)
    for phrase in phrases:
        if phrase not in contract_text:
            fail(f"{rel(contract_path)} missing app onboarding secret path contract phrase: {phrase}")

github_native_markdown = [
    root / ".github/ABOUT.md",
    root / ".github/PULL_REQUEST_TEMPLATE.md",
    root / ".github/SECURITY.md",
]
for github_doc in github_native_markdown:
    if github_doc.exists() and has_markdown_frontmatter(github_doc):
        fail(f"{rel(github_doc)} must remain frontmatter-free GitHub-native Markdown")

def iter_markdown_link_targets(text: str):
    in_fence = False
    inline_link = re.compile(r"!?\[[^\]\n]*\]\(([^\)\n]+)\)")
    reference_link = re.compile(r"^\[[^\]\n]+\]:\s+(\S+)")
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in inline_link.finditer(line):
            yield match.group(1).strip()
        match = reference_link.match(line.strip())
        if match:
            yield match.group(1).strip()


def normalize_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split()[0]
    return target.strip()


template_readme = read_text(root / "docs/99.templates/README.md")
template_locations = {
    "readme-collection-index.template.md": "templates/common/readme-collection-index.template.md",
    "readme-implementation.template.md": "templates/common/readme-implementation.template.md",
    "readme-repository.template.md": "templates/common/readme-repository.template.md",
    "readme-snapshot-pack.template.md": "templates/common/readme-snapshot-pack.template.md",
    "readme-stage-index.template.md": "templates/common/readme-stage-index.template.md",
    "readme-workspace-staging.template.md": "templates/common/readme-workspace-staging.template.md",
    "reference.template.md": "templates/common/reference.template.md",
    "archive-tombstone.template.md": "templates/common/archive-tombstone.template.md",
    "governance-reference.template.md": "templates/common/governance-reference.template.md",
    "memory.template.md": "templates/common/memory.template.md",
    "progress.template.md": "templates/common/progress.template.md",
    "prd.template.md": "templates/sdlc/requirements/prd.template.md",
    "ard.template.md": "templates/sdlc/architecture/ard.template.md",
    "template-support.template.md": "templates/common/template-support.template.md",
    "adr.template.md": "templates/sdlc/architecture/adr.template.md",
    "spec.template.md": "templates/sdlc/specs/spec.template.md",
    "api-spec.template.md": "templates/sdlc/specs/api-spec.template.md",
    "agent-design.template.md": "templates/sdlc/specs/agent-design.template.md",
    "data-model.template.md": "templates/sdlc/specs/data-model.template.md",
    "tests.template.md": "templates/sdlc/specs/tests.template.md",
    "openapi.template.yaml": "templates/sdlc/specs/openapi.template.yaml",
    "schema.template.graphql": "templates/sdlc/specs/schema.template.graphql",
    "service.template.proto": "templates/sdlc/specs/service.template.proto",
    "plan.template.md": "templates/sdlc/execution/plan.template.md",
    "task.template.md": "templates/sdlc/execution/task.template.md",
    "guide.template.md": "templates/sdlc/operations/guide.template.md",
    "policy.template.md": "templates/sdlc/operations/policy.template.md",
    "runbook.template.md": "templates/sdlc/operations/runbook.template.md",
    "incident.template.md": "templates/sdlc/operations/incident.template.md",
    "postmortem.template.md": "templates/sdlc/operations/postmortem.template.md",
}

archive_reason_allowed_values = {
    "superseded",
    "duplicate",
    "obsolete",
    "migrated",
    "historical-baseline",
}


def template_path(template_name: str) -> pathlib.Path:
    location = template_locations.get(template_name)
    if not location:
        fail(f"template mapping points to an unknown template: {template_name}")
    return root / "docs/99.templates" / location


template_root = root / "docs/99.templates/templates"
for template in sorted(template_root.rglob("*")):
    if template.is_file() and template.name not in template_readme:
        fail(f"template is not listed in docs/99.templates/README.md: {rel(template)}")
template_compatibility_path = (
    root / "tests/fixtures/document-contracts/template-compatibility.json"
)
template_compatibility = load_json(template_compatibility_path)

TEMPLATE_COMPATIBILITY_CONTRACT_V1 = {
    "name": "TemplateCompatibilityContract.v1",
    "semantic_sha256": (
        "e2a7b02ed9cf31b97480a9de31128d5d1486acf01c8e556d040f4071a6083cf6"  # pragma: allowlist secret
    ),
}
EXPECTED_TEMPLATE_COMPATIBILITY_KEYS = (
    "schemaVersion",
    "owner",
    "growthAllowed",
    "baselineDebtCounts",
    "canonicalFormCoverage",
    "templateModeCoverage",
)
RETIRED_TEMPLATE_DEBT_FIELDS = {"compatibilityDebt", "semanticDebtCaps"}


def template_compatibility_semantic_sha256(contract: dict) -> str:
    """Hash the complete semantic fixture projection with stable JSON encoding."""
    payload = json.dumps(
        contract,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def template_compatibility_contract_matches(contract: dict) -> bool:
    return (
        template_compatibility_semantic_sha256(contract)
        == TEMPLATE_COMPATIBILITY_CONTRACT_V1["semantic_sha256"]
    )


def assert_template_compatibility_mutation_proof(contract: dict) -> None:
    """Prove retained coverage and retired debt fields remain fail-closed."""

    def mutate_owner(candidate: dict) -> None:
        candidate["owner"] = "Spec 999"

    def mutate_growth_policy(candidate: dict) -> None:
        candidate["growthAllowed"] = True

    def mutate_baseline(candidate: dict) -> None:
        candidate["baselineDebtCounts"]["profileRows"] += 1

    def mutate_canonical_form(candidate: dict) -> None:
        candidate["canonicalFormCoverage"][0]["requiredHeadings"].append(
            "Synthetic Drift"
        )

    def mutate_template_mode(candidate: dict) -> None:
        candidate["templateModeCoverage"][0]["placeholderPolicy"] = "drift"

    def restore_compatibility_debt(candidate: dict) -> None:
        candidate["compatibilityDebt"] = []

    def restore_semantic_caps(candidate: dict) -> None:
        candidate["semanticDebtCaps"] = {}

    def restore_both_debt_fields(candidate: dict) -> None:
        restore_compatibility_debt(candidate)
        restore_semantic_caps(candidate)

    mutations = {
        "owner": mutate_owner,
        "growth policy": mutate_growth_policy,
        "baseline coverage": mutate_baseline,
        "canonical form coverage": mutate_canonical_form,
        "template mode coverage": mutate_template_mode,
        "compatibilityDebt reintroduction": restore_compatibility_debt,
        "semanticDebtCaps reintroduction": restore_semantic_caps,
        "both retired debt fields": restore_both_debt_fields,
    }
    for label, mutate in mutations.items():
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        if template_compatibility_contract_matches(candidate):
            fail(
                f"{TEMPLATE_COMPATIBILITY_CONTRACT_V1['name']} mutation proof "
                f"accepted changed {label}"
            )


if tuple(template_compatibility) != EXPECTED_TEMPLATE_COMPATIBILITY_KEYS:
    fail(
        f"{rel(template_compatibility_path)} top-level fields differ from the "
        "retired debt-free contract"
    )
restored_debt_fields = RETIRED_TEMPLATE_DEBT_FIELDS & set(template_compatibility)
if restored_debt_fields:
    fail(
        f"{rel(template_compatibility_path)} restored retired fields: "
        f"{sorted(restored_debt_fields)}"
    )
if not template_compatibility_contract_matches(template_compatibility):
    fail(
        f"{rel(template_compatibility_path)} does not match "
        f"{TEMPLATE_COMPATIBILITY_CONTRACT_V1['name']} semantic SHA-256"
    )
assert_template_compatibility_mutation_proof(template_compatibility)

if template_compatibility.get("owner") != "Spec 030":
    fail(f"{rel(template_compatibility_path)} owner must be Spec 030")
if template_compatibility.get("growthAllowed") is not False:
    fail(f"{rel(template_compatibility_path)} must set growthAllowed=false")
template_support_root = root / "docs/99.templates/support"
support_stale_patterns = [
    (re.compile(r"Phase [1-4]"), "migration phase wording"),
    (re.compile(r"during the migration"), "migration-only wording"),
    (re.compile(r"after Phase"), "migration phase ordering"),
    (re.compile(r"current and target frontmatter"), "current/target schema wording"),
]
for support_doc in sorted(template_support_root.glob("*.md")):
    support_text = read_text(support_doc)
    for pattern, label in support_stale_patterns:
        if pattern.search(support_text):
            fail(f"{rel(support_doc)} contains stale {label}")
    if support_doc.name == "README.md":
        continue


for provider in ["aws", "azure"]:
    docs_root = root / "examples" / provider / "docs"
    if not docs_root.exists():
        continue
    for example_doc in sorted(docs_root.rglob("*.md")):
        text = read_text(example_doc)
        if example_doc.name == "README.md":
            continue
        if "## Snapshot Boundary" not in text:
            fail(f"{rel(example_doc)} missing example-local snapshot heading: ## Snapshot Boundary")
        for required_phrase in [
            "Cloud Example Snapshot",
            "not live provider-latest guidance",
        ]:
            if required_phrase not in text:
                fail(f"{rel(example_doc)} missing snapshot boundary phrase: {required_phrase}")
        for stale_heading in [
            "## Azure Migration Product Requirements",
            "## Azure Migration Specification",
            "## Azure Kubernetes Service Architecture Reference Document",
        ]:
            if stale_heading in text:
                fail(f"{rel(example_doc)} contains duplicate stale heading: {stale_heading}")
        if re.search(r"^##\s+[0-9]+\.\s+.*관련 문서", text, re.MULTILINE):
            fail(f"{rel(example_doc)} must use canonical ## Related Documents heading")

template_routing_path = template_support_root / "template-routing.md"
document_registry = load_registry(root)
registry_profiles_by_id = {
    profile.profile_id: profile for profile in document_registry.profiles
}


def template_route_pairs(
    path: pathlib.Path,
    heading: str | tuple[str, ...],
) -> list[tuple[str, str]]:
    rows = markdown_table_after_heading(read_text(path), heading)
    if len(rows) < 2:
        fail(f"{rel(path)} {heading} must contain a header and route rows")
        return []
    route_pairs: list[tuple[str, str]] = []
    for row_number, row in enumerate(rows[1:], start=1):
        if len(row) < 2:
            fail(f"{rel(path)} {heading} row {row_number} must have target and template columns")
            continue
        route_pairs.append((row[0], row[1]))
    return route_pairs


template_readme_route_pairs = template_route_pairs(
    root / "docs/99.templates/README.md",
    ("## Template-Folder Mapping", "### Template-Folder Mapping"),
)
template_routing_route_pairs = template_route_pairs(
    template_routing_path,
    "### Current Route Map",
)


def registry_profile(profile_id: str):
    profile = registry_profiles_by_id.get(profile_id)
    if profile is None:
        fail(f"public template route references missing registry profile: {profile_id}")
    return profile


def public_template_cell(template_path: pathlib.PurePosixPath) -> str:
    prefix = "docs/99.templates/"
    value = template_path.as_posix()
    if not value.startswith(prefix):
        fail(f"public template route escapes canonical template root: {value}")
        return f"`{value}`"
    path = root / value
    if not path.is_file():
        fail(f"public template route points to missing canonical template: {value}")
    return f"`{value.removeprefix(prefix)}`"


def registry_backed_public_route(
    target_pattern: str,
    profile_id: str,
    witness_path: str,
) -> tuple[str, str]:
    profile = registry_profile(profile_id)
    if profile is None or profile.template is None:
        fail(f"public template route profile has no canonical template: {profile_id}")
        return f"`{target_pattern}`", "`<missing>`"
    try:
        selected = classify_path(document_registry, pathlib.PurePosixPath(witness_path))
    except DocumentContractError as exc:
        fail(f"public template route witness is unclassified: {witness_path}: {exc}")
    else:
        if selected.profile_id != profile_id:
            fail(
                "public template route witness selects the wrong registry profile: "
                f"{witness_path}: expected {profile_id}, actual {selected.profile_id}"
            )
    return f"`{target_pattern}`", public_template_cell(profile.template)


expected_readme_profile_ids = (
    "readme/repository",
    "readme/stage-index",
    "readme/collection-index",
    "readme/implementation",
    "readme/snapshot-pack",
    "readme/workspace-staging",
)
actual_readme_profile_ids = tuple(
    profile.profile_id
    for profile in document_registry.profiles
    if (
        profile.profile_class == "readme"
        and profile.profile_id.startswith("readme/")
        and profile.template is not None
    )
)
if actual_readme_profile_ids != expected_readme_profile_ids:
    fail(
        "public README route projection must track the canonical registry order: "
        f"expected {expected_readme_profile_ids}, actual {actual_readme_profile_ids}"
    )
expected_public_route_pairs = [
    (
        f"Registry `{profile_id}` routes",
        public_template_cell(registry_profile(profile_id).template),
    )
    for profile_id in actual_readme_profile_ids
    if registry_profile(profile_id) is not None
    and registry_profile(profile_id).template is not None
]

public_structural_route_bridge = (
    ("docs/01.requirements/<###-Numbering>-<feature-or-system>.md", "sdlc/prd", "docs/01.requirements/999-projection.md"),
    ("docs/02.architecture/requirements/####-<system-or-domain>.md", "sdlc/ard", "docs/02.architecture/requirements/9999-projection.md"),
    ("docs/02.architecture/decisions/####-<short-title>.md", "sdlc/adr", "docs/02.architecture/decisions/9999-projection.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/spec.md", "sdlc/spec", "docs/03.specs/999-projection/spec.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md", "sdlc/api-spec", "docs/03.specs/999-projection/api-spec.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md", "sdlc/agent-design", "docs/03.specs/999-projection/agent-design.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/data-model.md", "sdlc/data-model", "docs/03.specs/999-projection/data-model.md"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/tests.md", "sdlc/tests", "docs/03.specs/999-projection/tests.md"),
)
expected_public_route_pairs.extend(
    registry_backed_public_route(*route) for route in public_structural_route_bridge
)

native_contract_profile = registry_profile("exception/native-contract")
native_contract_route_bridge = (
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml", "docs/03.specs/999-projection/contracts/openapi.yaml", "docs/99.templates/templates/sdlc/specs/openapi.template.yaml"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql", "docs/03.specs/999-projection/contracts/schema.graphql", "docs/99.templates/templates/sdlc/specs/schema.template.graphql"),
    ("docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto", "docs/03.specs/999-projection/contracts/service.proto", "docs/99.templates/templates/sdlc/specs/service.template.proto"),
)
for target_pattern, witness_path, template_path_text in native_contract_route_bridge:
    try:
        selected = classify_path(document_registry, pathlib.PurePosixPath(witness_path))
    except DocumentContractError as exc:
        fail(f"native public route witness is unclassified: {witness_path}: {exc}")
    else:
        if native_contract_profile is None or selected.profile_id != native_contract_profile.profile_id:
            fail(
                "native public route witness must select exception/native-contract: "
                f"{witness_path}: actual {selected.profile_id}"
            )
    expected_public_route_pairs.append(
        (
            f"`{target_pattern}`",
            public_template_cell(pathlib.PurePosixPath(template_path_text)),
        )
    )

public_structural_route_bridge_tail = (
    ("docs/04.execution/plans/YYYY-MM-DD-<feature>.md", "sdlc/plan", "docs/04.execution/plans/2099-01-01-projection.md"),
    ("docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md", "sdlc/task", "docs/04.execution/tasks/2099-01-01-projection.md"),
    ("docs/05.operations/guides/####-<topic>.md", "sdlc/guide", "docs/05.operations/guides/9999-projection.md"),
    ("docs/05.operations/policies/####-<policy-or-standard>.md", "sdlc/policy", "docs/05.operations/policies/9999-projection.md"),
    ("docs/05.operations/runbooks/####-<topic>.md", "sdlc/runbook", "docs/05.operations/runbooks/9999-projection.md"),
    ("docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md", "sdlc/incident", "docs/05.operations/incidents/2099/INC-999-projection/INC-999-projection.md"),
    ("docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md", "sdlc/postmortem", "docs/05.operations/incidents/2099/INC-999-projection/postmortem.md"),
    ("docs/90.references/<category>/<topic>.md", "content/reference", "docs/90.references/research/projection.md"),
    ("docs/98.archive/**/*.md", "content/archive-tombstone", "docs/98.archive/projection.md"),
    ("docs/00.agent-governance/memory/<topic>.md", "governance/memory", "docs/00.agent-governance/memory/projection.md"),
)
expected_public_route_pairs.extend(
    registry_backed_public_route(*route) for route in public_structural_route_bridge_tail
)

progress_entry_profile = registry_profile("governance/progress-entry")
progress_ledger_profile = registry_profile("governance/progress-ledger")
if (
    progress_entry_profile is None
    or progress_ledger_profile is None
    or progress_entry_profile.source_profile_ids != ("governance/progress-ledger",)
    or progress_entry_profile.template is None
):
    fail("public progress route must link the canonical progress-entry and progress-ledger profiles")
else:
    selected_progress_profile = classify_path(
        document_registry,
        pathlib.PurePosixPath("docs/00.agent-governance/memory/progress.md"),
    )
    if selected_progress_profile.profile_id != progress_ledger_profile.profile_id:
        fail("canonical progress path must select governance/progress-ledger")
    expected_public_route_pairs.append(
        (
            "`docs/00.agent-governance/memory/progress.md`",
            public_template_cell(progress_entry_profile.template),
        )
    )


def assert_public_route_projection(
    route_pairs: list[tuple[str, str]],
    source_label: str,
) -> None:
    if not public_route_projection_matches(route_pairs):
        fail(f"{source_label} must equal the canonical registry-backed public route projection")


def public_route_projection_matches(route_pairs: list[tuple[str, str]]) -> bool:
    return route_pairs == expected_public_route_pairs


assert_public_route_projection(
    template_readme_route_pairs,
    "docs/99.templates/README.md Template-Folder Mapping",
)
assert_public_route_projection(
    template_routing_route_pairs,
    "docs/99.templates/support/template-routing.md Current Route Map",
)
public_route_mutation = list(expected_public_route_pairs)
public_route_mutation[0] = (public_route_mutation[0][0], "`templates/common/drift.template.md`")
if public_route_projection_matches(public_route_mutation):
    fail("public route projection mutation proof failed to reject same-table canonical drift")
for phrase in [
    "## Structural Template Coverage",
    "structural template mapping",
    "exactly one mapping",
]:
    if phrase not in template_readme:
        fail(f"{rel(root / 'docs/99.templates/README.md')} missing structural template coverage phrase: {phrase}")


def canonical_markdown_owns_generic_residue(path: pathlib.Path) -> bool:
    try:
        profile = classify_path(
            document_registry,
            pathlib.PurePosixPath(rel(path)),
        )
    except DocumentContractError:
        return False
    if profile.placeholder_policy != "forbidden" or profile.append_contract is not None:
        return False
    if (
        profile.frontmatter.mode == "not-applicable"
        and not profile.headings.required
        and not profile.headings.allowed
    ):
        return False
    return bool(profile.headings.required or profile.headings.allowed)


authored_template_residue = ("Target: " + "docs/", "Use this " + "template")


def generic_template_residue_lines(text: str) -> list[int]:
    return [
        line_number
        for line_number, line in enumerate(text.splitlines(), start=1)
        if any(marker in line for marker in authored_template_residue)
    ]


def assert_generic_residue_delegation_probe() -> None:
    if generic_template_residue_lines("route: Use this " + "template") != [1]:
        fail("generic residue mutation probe failed for active non-Markdown config")
    if generic_template_residue_lines("Target: " + "docs/example.md") != [1]:
        fail("generic residue mutation probe failed for non-structural Markdown")
    structural = root / "docs/01.requirements/999-projection.md"
    if not canonical_markdown_owns_generic_residue(structural):
        fail("generic residue delegation probe must delegate authored structural Markdown")
    provider_shim = root / "AGENTS.md"
    if canonical_markdown_owns_generic_residue(provider_shim):
        fail("generic residue delegation probe must retain headingless provider shims")


assert_generic_residue_delegation_probe()
active_residue_suffixes = {
    ".graphql",
    ".json",
    ".md",
    ".proto",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
}
tracked_active_paths = subprocess.run(
    ["git", "-C", str(root), "ls-files", "-z"],
    check=True,
    stdout=subprocess.PIPE,
).stdout.split(b"\0")
for raw_relative_path in tracked_active_paths:
    if not raw_relative_path:
        continue
    try:
        relative_path = pathlib.PurePosixPath(raw_relative_path.decode("utf-8"))
    except UnicodeDecodeError:
        fail("git returned a non-UTF-8 active path during generic residue validation")
        continue
    if not (
        relative_path.as_posix() in {"README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"}
        or relative_path.parts[0] in TARGET_ROOTS
    ):
        continue
    path = root / relative_path
    if path.suffix not in active_residue_suffixes or not path.is_file() or path.is_symlink():
        continue
    if path.is_relative_to(root / "docs/99.templates/templates"):
        continue
    if is_historical_evidence_path(path):
        continue
    if path.suffix == ".md" and canonical_markdown_owns_generic_residue(path):
        continue
    for line_number in generic_template_residue_lines(read_text(path)):
        fail(f"active non-structural template residue in {rel(path)}:{line_number}")

reference_template_path = template_path("reference.template.md")
reference_template_text = read_text(reference_template_path)
if re.search(r"archive", reference_template_text, re.IGNORECASE):
    fail(f"{rel(reference_template_path)} must not contain archive wording")

for path in docs_dir.rglob("*"):
    if not path.is_file():
        continue
    if path.is_relative_to(root / "docs/99.templates"):
        continue
    if re.search(r"(^template\.md$|\.template\.|template\.)", path.name):
        fail(f"template-like docs file must live in docs/99.templates: {rel(path)}")

english_first_stage_globs = [
    "docs/03.specs/*/spec.md",
    "docs/04.execution/plans/*.md",
    "docs/04.execution/tasks/*.md",
]
hangul_pattern = re.compile(r"[\uac00-\ud7a3]")
for glob_pattern in english_first_stage_globs:
    for path in sorted(root.glob(glob_pattern)):
        if path.name == "README.md":
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            if hangul_pattern.search(line):
                fail(f"{rel(path)}:{line_number} contains Korean text in an English-first Stage 03/04 artifact")

archive_root = root / "docs/98.archive"
archive_required_phrases = [
    "type: content/archive-tombstone",
    "status: archived",
    "Original path:",
    "Archived on:",
    "Currentness rule:",
    "Current owner document:",
    "Current Implementation Evidence",
    "Archive README",
]
for tombstone in sorted(archive_root.rglob("*.md")):
    if tombstone.name == "README.md":
        continue
    metadata = load_markdown_frontmatter(tombstone)
    archive_reason = str(metadata.get("archive_reason", "")).strip()
    if archive_reason not in archive_reason_allowed_values:
        fail(f"{rel(tombstone)} archive_reason is unsupported: {archive_reason or '<empty>'}")
    original_path = str(metadata.get("original_path", "")).strip()
    replacement = str(metadata.get("replacement", "")).strip()
    if not original_path.startswith("docs/") or original_path.startswith("docs/98.archive/"):
        fail(f"{rel(tombstone)} original_path must point to the original non-archive docs path")
    if replacement != "none" and not replacement.startswith("docs/"):
        fail(f"{rel(tombstone)} replacement must be docs/... or none")
    text = read_text(tombstone)
    for phrase in archive_required_phrases:
        if phrase not in text:
            fail(f"{rel(tombstone)} missing archive Tombstone phrase: {phrase}")
    if len(text.splitlines()) > 90:
        fail(f"{rel(tombstone)} must be metadata-only Tombstone, not a preserved old body")
    old_body_headings = [
        "## Requirements",
        "## Functional Requirements",
        "## Non-Functional Requirements",
        "## Work Breakdown",
        "## Tasks",
        "## Implementation Status",
        "## Verification",
    ]
    for heading in old_body_headings:
        if heading in text and heading not in {"## Verification"}:
            fail(f"{rel(tombstone)} appears to preserve old body heading: {heading}")

archive_readme_text = read_text(archive_root / "README.md")
for phrase in [
    "docs/01-05",
    "### 01.requirements",
    "### 02.architecture",
    "### 03.specs",
    "### 04.execution",
    "### 05.operations",
    "05.operations/guides",
    "05.operations/policies",
    "05.operations/runbooks",
    "05.operations/incidents",
]:
    if phrase not in archive_readme_text:
        fail(f"docs/98.archive/README.md missing archive index phrase: {phrase}")

operations_stage_path = root / "docs/05.operations"
allowed_operations_buckets = {"guides", "policies", "runbooks", "incidents"}
actual_operations_buckets = {
    path.name
    for path in operations_stage_path.iterdir()
    if path.is_dir()
}
for name in sorted(allowed_operations_buckets - actual_operations_buckets):
    fail(f"required operations bucket is missing: {rel(operations_stage_path / name)}")
for name in sorted(actual_operations_buckets - allowed_operations_buckets):
    fail(f"docs/05.operations contains unsupported bucket: {rel(operations_stage_path / name)}")

operations_readme_path = operations_stage_path / "README.md"
operations_readme_text = read_text(operations_readme_path)
operations_routing_rows = markdown_table_after_heading(
    operations_readme_text,
    ("## Operations Routing Matrix", "### Operations Routing Matrix"),
)
expected_operations_routing_header = ["필요 상황", "사용할 위치", "시작 템플릿"]
expected_operations_routing_targets = [
    ("./guides/README.md", "../99.templates/templates/sdlc/operations/guide.template.md"),
    ("./policies/README.md", "../99.templates/templates/sdlc/operations/policy.template.md"),
    ("./runbooks/README.md", "../99.templates/templates/sdlc/operations/runbook.template.md"),
    ("./incidents/README.md", "../99.templates/templates/sdlc/operations/incident.template.md"),
    ("./incidents/README.md", "../99.templates/templates/sdlc/operations/postmortem.template.md"),
]
if len(operations_routing_rows) < 2:
    fail("docs/05.operations/README.md Operations Routing Matrix must contain a header and routing rows")
elif operations_routing_rows[0] != expected_operations_routing_header:
    fail(
        "docs/05.operations/README.md Operations Routing Matrix header must be: "
        + " | ".join(expected_operations_routing_header)
    )
else:
    actual_operations_routing_targets: list[tuple[str, str]] = []
    for row_number, row in enumerate(operations_routing_rows[1:], start=1):
        if len(row) != len(expected_operations_routing_header):
            fail(
                "docs/05.operations/README.md Operations Routing Matrix "
                f"row {row_number} must have {len(expected_operations_routing_header)} columns"
            )
            continue
        situation, location_cell, template_cell = row
        if not situation:
            fail(f"docs/05.operations/README.md Operations Routing Matrix row {row_number} has empty 필요 상황")
        location_targets = list(iter_markdown_link_targets(location_cell))
        template_targets = list(iter_markdown_link_targets(template_cell))
        if len(location_targets) != 1:
            fail(
                "docs/05.operations/README.md Operations Routing Matrix "
                f"row {row_number} must have exactly one location link"
            )
            continue
        if len(template_targets) != 1:
            fail(
                "docs/05.operations/README.md Operations Routing Matrix "
                f"row {row_number} must have exactly one template link"
            )
            continue
        location_target = normalize_markdown_target(location_targets[0])
        template_target = normalize_markdown_target(template_targets[0])
        if not (operations_readme_path.parent / pathlib.Path(location_target)).exists():
            fail(
                "docs/05.operations/README.md Operations Routing Matrix "
                f"row {row_number} location target is missing: {location_target}"
            )
        if not (operations_readme_path.parent / pathlib.Path(template_target)).exists():
            fail(
                "docs/05.operations/README.md Operations Routing Matrix "
                f"row {row_number} template target is missing: {template_target}"
            )
        actual_operations_routing_targets.append((location_target, template_target))
    if actual_operations_routing_targets != expected_operations_routing_targets:
        fail(
            "docs/05.operations/README.md Operations Routing Matrix target order must be: "
            + ", ".join(
                f"{location} -> {template}"
                for location, template in expected_operations_routing_targets
            )
        )

incidents_readme_path = operations_stage_path / "incidents/README.md"
incidents_readme_text = read_text(incidents_readme_path)
incident_boundary_rows = markdown_table_after_heading(
    incidents_readme_text,
    ("## Incident Boundary Matrix", "### Incident Boundary Matrix"),
)
expected_incident_boundary_header = [
    "Artifact",
    "Path rule",
    "Template",
    "Creation rule",
    "Current state",
]
expected_incident_boundary = [
    {
        "artifact": "Incident Record",
        "path_rule": "./YYYY/INC-###-<title>/INC-###-<title>.md",
        "template": "../../99.templates/templates/sdlc/operations/incident.template.md",
        "creation_phrase": "real incident fact record",
        "current_state": "No tracked incident records.",
    },
    {
        "artifact": "Postmortem",
        "path_rule": "./YYYY/INC-###-<title>/postmortem.md",
        "template": "../../99.templates/templates/sdlc/operations/postmortem.template.md",
        "creation_phrase": "root cause/prevention analysis",
        "current_state": "No tracked postmortems.",
    },
]
if len(incident_boundary_rows) < 2:
    fail("docs/05.operations/incidents/README.md Incident Boundary Matrix must contain a header and boundary rows")
elif incident_boundary_rows[0] != expected_incident_boundary_header:
    fail(
        "docs/05.operations/incidents/README.md Incident Boundary Matrix header must be: "
        + " | ".join(expected_incident_boundary_header)
    )
else:
    actual_incident_artifacts: list[str] = []
    for row_number, (row, expected) in enumerate(
        zip(incident_boundary_rows[1:], expected_incident_boundary),
        start=1,
    ):
        if len(row) != len(expected_incident_boundary_header):
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} must have {len(expected_incident_boundary_header)} columns"
            )
            continue
        artifact_cell, path_rule_cell, template_cell, creation_rule, current_state = row
        artifact_match = re.fullmatch(r"`([^`]+)`", artifact_cell)
        path_rule_match = re.fullmatch(r"`([^`]+)`", path_rule_cell)
        template_targets = list(iter_markdown_link_targets(template_cell))
        if not artifact_match:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} must start with a backticked Artifact"
            )
            continue
        if not path_rule_match:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} must use a backticked Path rule"
            )
            continue
        artifact = artifact_match.group(1)
        path_rule = path_rule_match.group(1)
        actual_incident_artifacts.append(artifact)
        if artifact != expected["artifact"]:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} Artifact must be {expected['artifact']!r}"
            )
        if path_rule != expected["path_rule"]:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} Path rule must be {expected['path_rule']!r}"
            )
        if len(template_targets) != 1:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} must have exactly one Template link"
            )
        else:
            template_target = normalize_markdown_target(template_targets[0])
            if template_target != expected["template"]:
                fail(
                    "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                    f"row {row_number} Template must be {expected['template']!r}"
                )
            if not (incidents_readme_path.parent / pathlib.Path(template_target)).exists():
                fail(
                    "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                    f"row {row_number} Template target is missing: {template_target}"
                )
        if expected["creation_phrase"] not in creation_rule:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} Creation rule must mention {expected['creation_phrase']!r}"
            )
        if current_state != expected["current_state"]:
            fail(
                "docs/05.operations/incidents/README.md Incident Boundary Matrix "
                f"row {row_number} Current state must be {expected['current_state']!r}"
            )
    if actual_incident_artifacts != [item["artifact"] for item in expected_incident_boundary]:
        fail("docs/05.operations/incidents/README.md Incident Boundary Matrix row order is invalid")

tracked_incident_docs = [
    path
    for path in sorted((operations_stage_path / "incidents").rglob("*.md"))
    if path.name != "README.md"
]
for path in tracked_incident_docs:
    relative_incident_path = path.relative_to(operations_stage_path / "incidents")
    parts = relative_incident_path.parts
    if len(parts) != 3:
        fail(
            "docs/05.operations/incidents document must live at "
            "YYYY/INC-###-<title>/INC-###-<title>.md or "
            f"YYYY/INC-###-<title>/postmortem.md: {rel(path)}"
        )
        continue
    year, incident_folder, filename = parts
    if not re.fullmatch(r"[0-9]{4}", year):
        fail(f"docs/05.operations/incidents document year folder must be YYYY: {rel(path)}")
    if not re.fullmatch(r"INC-[0-9]{3}-[^/]+", incident_folder):
        fail(f"docs/05.operations/incidents document folder must be INC-###-<title>: {rel(path)}")
    if filename not in {f"{incident_folder}.md", "postmortem.md"}:
        fail(
            "docs/05.operations/incidents document filename must match the "
            f"incident folder or be postmortem.md: {rel(path)}"
        )
if not tracked_incident_docs:
    for phrase in [
        "현재 tracked incident record와 postmortem 문서는 없다.",
        "No tracked incident records.",
        "No tracked postmortems.",
    ]:
        if phrase not in incidents_readme_text:
            fail(f"docs/05.operations/incidents/README.md missing no-incident state phrase: {phrase}")
    unexpected_incident_dirs = [
        path
        for path in sorted((operations_stage_path / "incidents").iterdir())
        if path.is_dir()
    ]
    if unexpected_incident_dirs:
        fail(
            "docs/05.operations/incidents has placeholder directory without tracked incident docs: "
            + ", ".join(rel(path) for path in unexpected_incident_dirs)
        )

operations_index_roots = [
    root / "docs/05.operations/guides",
    root / "docs/05.operations/policies",
    root / "docs/05.operations/runbooks",
]
for operations_root in operations_index_roots:
    readme_path = operations_root / "README.md"
    if not readme_path.exists():
        fail(f"operations subfolder README is missing: {rel(readme_path)}")
        continue

    readme_text = read_text(readme_path)
    rows = markdown_table_after_heading(
        readme_text,
        ("## 문서 인덱스", "### 문서 인덱스"),
    )
    expected_header = ["문서", "설명", "상태", "최종 수정"]
    if len(rows) < 2:
        fail(f"{rel(readme_path)} 문서 인덱스 must contain a header and document rows")
        continue
    if rows[0] != expected_header:
        fail(f"{rel(readme_path)} 문서 인덱스 header must be: {' | '.join(expected_header)}")

    indexed_rows: dict[str, list[str]] = {}
    for row_number, row in enumerate(rows[1:], start=1):
        if len(row) != len(expected_header):
            fail(f"{rel(readme_path)} 문서 인덱스 row {row_number} must have {len(expected_header)} columns")
            continue
        match = re.search(r"\]\(\./([^)]+\.md)\)", row[0])
        if not match:
            fail(f"{rel(readme_path)} 문서 인덱스 row {row_number} must link to ./<document>.md")
            continue
        target_name = match.group(1)
        if target_name in indexed_rows:
            fail(f"{rel(readme_path)} 문서 인덱스 duplicates document: {target_name}")
        indexed_rows[target_name] = row

    operation_docs = sorted(path for path in operations_root.glob("*.md") if path.name != "README.md")
    operation_doc_names = {path.name for path in operation_docs}
    for doc_name in sorted(operation_doc_names - set(indexed_rows)):
        fail(f"{rel(readme_path)} 문서 인덱스 missing document: {doc_name}")
    for doc_name in sorted(set(indexed_rows) - operation_doc_names):
        fail(f"{rel(readme_path)} 문서 인덱스 links to missing document: {doc_name}")

    for doc_path in operation_docs:
        row = indexed_rows.get(doc_path.name)
        if not row:
            continue
        doc_text = read_text(doc_path)
        frontmatter = re.match(r"^---\n(.*?)\n---\n", doc_text, re.DOTALL)
        if not frontmatter:
            fail(f"{rel(doc_path)} missing YAML frontmatter for operations index validation")
            continue
        try:
            metadata = yaml.load(frontmatter.group(1), Loader=DuplicateKeyLoader) or {}
        except Exception as exc:
            fail(f"{rel(doc_path)} frontmatter parse failed for operations index validation: {exc}")
            continue
        status = str(metadata.get("status", "")).strip()
        updated = str(metadata.get("updated", "")).strip()
        row_status = row[2].strip()
        row_updated = row[3].strip()
        if not status:
            fail(f"{rel(doc_path)} missing status for operations index validation")
        elif row_status.lower() != status.lower():
            fail(f"{rel(readme_path)} status mismatch for {doc_path.name}: index={row_status}, frontmatter={status}")
        if not updated:
            fail(f"{rel(doc_path)} missing updated for operations index validation")
        elif row_updated != updated:
            fail(f"{rel(readme_path)} updated mismatch for {doc_path.name}: index={row_updated}, frontmatter={updated}")


template_enforcement_phrase_checks = {
    root / "docs/00.agent-governance/rules/documentation-protocol.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "structural template mapping",
        "required template headings",
        "template path used and the validation evidence",
    ],
    root / "docs/00.agent-governance/rules/document-stage-routing.md": [
        "docs/99.templates/support/document-profiles.json",
        "structural template mapping",
        "required template headings",
        "template path used and validation evidence",
    ],
    root / ".agents/skills/docs-stage-routing/skill.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "Required Template",
        "validation evidence",
    ],
    root / ".agents/agents/doc-writer.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "required template headings",
        "structural template mapping",
        "template path used",
        "Validation evidence",
    ],
}
for path, phrases in template_enforcement_phrase_checks.items():
    text = read_text(path)
    for phrase in phrases:
        if phrase not in text:
            fail(f"{rel(path)} missing template enforcement phrase: {phrase}")

active_policy_template_routes = [
    root / ".agents/skills/docs-stage-routing/skill.md",
    root / "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
    root / "docs/00.agent-governance/rules/document-stage-routing.md",
]
for path in active_policy_template_routes:
    text = read_text(path)
    legacy_operation_template = "operation" + ".template.md"
    if legacy_operation_template in text:
        fail(f"{rel(path)} must route operations policy docs to policy.template.md, not {legacy_operation_template}")
    if "policy.template.md" not in text:
        fail(f"{rel(path)} missing operations policy template route: policy.template.md")

active_template_routing_reference_files = [
    root / "README.md",
    root / "docs/README.md",
    root / ".agents/GEMINI.md",
    root / ".codex/CODEX.md",
    root / ".agents/hooks.json",
    root / ".claude/settings.json",
    root / ".codex/hooks.json",
    root / ".agents/agents/doc-writer.md",
    root / ".claude/agents/doc-writer.md",
    root / ".codex/agents/doc-writer.toml",
    root / ".agents/output-styles/hy-home-k8s.md",
    root / ".agents/rules/workspace-rules.md",
    root / ".agents/skills/docs-stage-conformance/skill.md",
    root / ".agents/skills/docs-stage-routing/skill.md",
    root / ".agents/workflows/qa-cicd-workflow.md",
    root / "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
]
for path in active_template_routing_reference_files:
    text = read_text(path)
    if "99.templates/support/template-routing.md" not in text:
        fail(f"{rel(path)} must route exact template selection through docs/99.templates/support/template-routing.md")

legacy_denylist_literals = {
    "operation" + ".template.md": "deprecated operations policy template route",
    "platform" + "-" + "team": "deprecated owner value",
    "Related " + "References": "deprecated README related-document heading",
}
legacy_scan_roots = [
    root / "docs",
    root / "scripts",
    root / ".codex",
    root / "AGENTS.md",
    root / "RTK.md",
]
legacy_scan_suffixes = {".md", ".sh", ".py", ".toml", ".yaml", ".yml", ".json"}
for scan_root in legacy_scan_roots:
    if not scan_root.exists():
        continue
    candidates = [scan_root] if scan_root.is_file() else sorted(scan_root.rglob("*"))
    for candidate in candidates:
        if not candidate.is_file():
            continue
        if candidate.suffix not in legacy_scan_suffixes and candidate.name not in {"AGENTS.md", "RTK.md"}:
            continue
        text = read_text(candidate)
        for literal, replacement in legacy_denylist_literals.items():
            if literal in text:
                fail(f"{rel(candidate)} contains {replacement} literal: {literal}")

llm_wiki_dir = root / "docs/90.references/llm-wiki"
llm_wiki_readme = llm_wiki_dir / "README.md"
llm_wiki_index = llm_wiki_dir / "wiki-index.md"
llm_wiki_generator = root / "scripts/generate-llm-wiki-index.sh"
if not llm_wiki_readme.exists():
    fail(f"LLM WIKI reference index is missing: {rel(llm_wiki_readme)}")
else:
    llm_wiki_text = read_text(llm_wiki_readme)
    for phrase in [
        "reference-only",
        "deterministic",
        "link map",
        "not a runtime surface",
        "not a static wiki site",
        "not a vector store",
        "not a retrieval service",
        "generated Markdown",
        "scripts/generate-llm-wiki-index.sh",
        "wiki-index.md",
        "does not define policy",
        "canonical owner",
    ]:
        if phrase not in llm_wiki_text:
            fail(f"{rel(llm_wiki_readme)} missing LLM WIKI reference-only boundary phrase: {phrase}")
if not llm_wiki_index.exists():
    fail(f"generated LLM WIKI index is missing: {rel(llm_wiki_index)}")
if not llm_wiki_generator.exists():
    fail(f"LLM WIKI generator is missing: {rel(llm_wiki_generator)}")
else:
    generator_check = subprocess.run(
        ["bash", str(llm_wiki_generator), "--check"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if generator_check.returncode != 0:
        detail = "\n".join(
            item
            for item in [generator_check.stdout.strip(), generator_check.stderr.strip()]
            if item
        )
        fail(f"generated LLM WIKI index is stale; run bash scripts/generate-llm-wiki-index.sh\n{detail}")
if llm_wiki_dir.exists():
    disallowed_llm_wiki_suffixes = {
        ".db",
        ".sqlite",
        ".sqlite3",
        ".faiss",
        ".npy",
        ".npz",
        ".parquet",
        ".lock",
    }
    disallowed_llm_wiki_names = {
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "poetry.lock",
        "uv.lock",
        "requirements.txt",
        "pyproject.toml",
        "Cargo.toml",
        "go.mod",
    }
    disallowed_llm_wiki_path_names = {
        ".cache",
        ".venv",
        "__pycache__",
        "cache",
        "dist",
        "embeddings",
        "node_modules",
        "runtime",
        "site",
        "vector",
        "vectors",
        "venv",
    }
    for path in sorted(llm_wiki_dir.rglob("*")):
        relative_parts = set(path.relative_to(llm_wiki_dir).parts)
        if relative_parts & disallowed_llm_wiki_path_names:
            fail(f"LLM WIKI must not contain generated runtime/cache/vector/static-site paths: {rel(path)}")
        if path.is_dir():
            continue
        if path.suffix in disallowed_llm_wiki_suffixes or path.name in disallowed_llm_wiki_names:
            fail(f"LLM WIKI must remain a reference-only index, not a generated/runtime store: {rel(path)}")
        if path.suffix != ".md":
            fail(f"LLM WIKI may only contain Markdown reference files: {rel(path)}")

legacy_postmortems = "11" + ".postmortems"
legacy_learning = "50" + ".Learning"
legacy_stage_range = "00" + "~" + "11"
legacy_docs_range = "01" + "~" + "99"
legacy_stage_label = "Stage " + "11"
legacy_harness = "H" + "100"
legacy_harness_examples = "examples/" + "harness-100"
old_docs_path_refs = [
    "docs/" + name for name in sorted(old_top_level_docs)
] + [
    "../" + name for name in sorted(old_top_level_docs)
]
legacy_dashboard_app = "platform" + "-dashboard"
legacy_dashboard_ns_file = "namespace" + "-kubernetes-dashboard"
legacy_dashboard_kubectl = "kubectl -n " + "kubernetes-dashboard"
legacy_dashboard_namespace_code = "`" + "kubernetes-dashboard" + "` namespace"
legacy_dashboard_namespace_text = "kubernetes-dashboard " + "namespace"
legacy_docs_traefik = "docs/" + "traefik"
stale_patterns = [
    *old_docs_path_refs,
    "file://",
    str(root),
    "docs/" + legacy_postmortems,
    "docs/" + legacy_learning,
    legacy_postmortems,
    legacy_learning,
    legacy_stage_range,
    legacy_docs_range,
    legacy_stage_label,
    legacy_harness,
    legacy_harness_examples,
]
legacy_contract_patterns = [
    legacy_dashboard_app,
    legacy_dashboard_ns_file,
    legacy_dashboard_kubectl,
    legacy_dashboard_namespace_code,
    legacy_dashboard_namespace_text,
    legacy_docs_traefik,
]
legacy_contract_markers = [
    "현재 실행계약 메모",
    "Superseded",
    "superseded",
    "역사적",
    "Headlamp Replaces Kubernetes Dashboard",
]
scan_roots = [
    root / "README.md",
    root / "docs",
    root / ".claude",
    root / ".codex",
    root / ".github",
    root / "scripts",
    root / "infrastructure",
    root / "gitops",
    root / "examples",
]
stale_scan_skip = {
    root / "docs/00.agent-governance/rules/document-stage-routing.md",
}
for scan_root in scan_roots:
    candidates = [scan_root] if scan_root.is_file() else scan_root.rglob("*")
    for path in candidates:
        if not path.is_file() or path.name == "validate-repo-quality-gates.sh":
            continue
        if path in stale_scan_skip:
            continue
        if path.suffix not in {".md", ".toml", ".json", ".yml", ".yaml", ".sh"}:
            continue
        text = read_text(path)
        for pattern in stale_patterns:
            if pattern in text:
                fail(f"stale docs path reference found in {rel(path)}: {pattern}")
        for pattern in legacy_contract_patterns:
            if pattern in text and not any(marker in text for marker in legacy_contract_markers):
                fail(f"legacy runtime contract reference lacks historical/superseded note in {rel(path)}: {pattern}")

active_stale_contract_roots = [
    root / "docs/01.requirements",
    root / "docs/02.architecture",
    root / "docs/03.specs",
    root / "docs/04.execution",
    root / "docs/05.operations",
]
active_stale_contract_patterns = [
    "172.19",
    "172.30",
    "kubernetes-dashboard",
    "Kubernetes Dashboard",
    "k8s-dashboard",
    "K8s Dashboard",
    "platform-dashboard",
    "dashboard-admin",
]
for scan_root in active_stale_contract_roots:
    for path in sorted(scan_root.rglob("*.md")):
        if path.name == "validate-repo-quality-gates.sh":
            continue
        if path.is_relative_to(root / "docs/98.archive"):
            continue
        text = read_text(path)
        for pattern in active_stale_contract_patterns:
            if pattern in text:
                fail(
                    f"active authored docs must not retain stale implementation "
                    f"contract in {rel(path)}: {pattern}"
                )

active_currentness_roots = [
    root / "docs/01.requirements",
    root / "docs/02.architecture",
    root / "docs/03.specs",
    root / "docs/04.execution",
    root / "docs/05.operations",
    root / "docs/90.references",
]
migration_evidence_ledger_path = (
    root
    / "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md"
)


def is_currentness_evidence_only(path: pathlib.Path) -> bool:
    return path == migration_evidence_ledger_path


if not is_currentness_evidence_only(migration_evidence_ledger_path):
    fail("migration evidence ledger currentness exception must match its exact path")
if is_currentness_evidence_only(root / "docs/90.references/README.md"):
    fail("migration evidence ledger currentness exception must not widen to Stage 90")

stale_provider_hook_path = "." + "claude/hooks"
stale_shell_job_name = "shell" + "-static"
stale_headlamp_oidc_patterns = [
    "0004-" + "headlamp-auth-oidc-guide.md",
    "0005-" + "headlamp-keycloak-runbook.md",
    "headlamp-" + "oidc-secret",
    "externalsecret-" + "oidc.yaml",
    "gitops/platform/headlamp/" + "values.yaml",
]
stale_rollouts_currentness_patterns = [
    (
        "analysis-run 없이",
        "stale Rollouts analysis-free promotion contract",
    ),
    (
        "Prometheus analysis provider 연동 (후속 Phase)",
        "stale Rollouts Prometheus analysis future-only contract",
    ),
]
stale_app_onboarding_currentness_patterns = [
    (
        "Deployment는 `appproject-apps` whitelist에 포함",
        "stale apps AppProject Deployment whitelist claim",
    ),
]
for scan_root in active_currentness_roots:
    for path in sorted(scan_root.rglob("*.md")):
        if path.is_relative_to(root / "docs/98.archive"):
            continue
        if is_currentness_evidence_only(path):
            continue
        text = read_text(path)
        if stale_provider_hook_path in text:
            fail(
                f"active authored docs must not retain stale provider-local hook path "
                f"in {rel(path)}"
            )
        if stale_shell_job_name in text:
            fail(
                f"active authored docs must not list stale CI job name "
                f"in {rel(path)}"
            )
        for pattern in stale_headlamp_oidc_patterns:
            if pattern in text:
                fail(
                    f"active authored docs must not retain archived Headlamp OIDC "
                    f"contract in {rel(path)}: {pattern}"
                )
        for pattern, description in [
            *stale_rollouts_currentness_patterns,
            *stale_app_onboarding_currentness_patterns,
        ]:
            if pattern in text:
                fail(
                    f"active authored docs must not retain {description} "
                    f"in {rel(path)}: {pattern}"
                )

authored_command_roots = [
    root / "docs/02.architecture/decisions",
    root / "docs/03.specs",
    root / "docs/05.operations/guides",
    root / "docs/05.operations/policies",
    root / "docs/05.operations/runbooks",
    root / "docs/05.operations/incidents",
]


def has_nearby_marker(lines: list[str], index: int, markers: list[str]) -> bool:
    start = max(0, index - 8)
    end = min(len(lines), index + 5)
    window = "\n".join(lines[start:end])
    return any(marker in window for marker in markers)


def is_pr_flow_push(lines: list[str], index: int) -> bool:
    return has_nearby_marker(
        lines,
        index,
        [
            "PR review",
            "PR flow",
            "PR-flow",
            "pull request",
            "review/merge",
            "review 후",
            "merge되면",
            "feature branch",
        ],
    )


allowed_push_branch = re.compile(
    r"\bgit\s+push\s+origin\s+(?:feat|fix|docs|refactor|chore|ci|release|hotfix|codex|dependabot)/\S+"
)


command_boundary_rules = [
    (
        "kubectl apply/patch",
        re.compile(r"\bkubectl\b.*\b(?:apply|patch)\b"),
        ["human-approved", "break-glass", "bootstrap-only", "bootstrap only", "operator-approved", "dry-run"],
    ),
    (
        "kubectl create clusterrolebinding",
        re.compile(r"\bkubectl\b.*\bcreate\s+clusterrolebinding\b"),
        ["human-approved", "break-glass", "bootstrap-only", "bootstrap only", "operator-approved", "dry-run"],
    ),
    (
        "kubectl get secret yaml/json",
        re.compile(r"\bkubectl\s+get\s+secret\b.*\b-o\s+(?:yaml|json)\b"),
        ["metadata-only", "status-only", "jsonpath", "no secret value", "redacted"],
    ),
    (
        "argocd app sync",
        re.compile(r"\bargocd\s+app\s+sync\b"),
        ["operator-triggered reconciliation", "operator-approved", "break-glass"],
    ),
    (
        "vault kv put",
        re.compile(r"\bvault\s+kv\s+put\b"),
        ["external secret operation", "human-approved"],
    ),
    (
        "vault policy write",
        re.compile(r"\bvault\s+policy\s+write\b"),
        ["external secret operation", "operator-approved", "human-approved", "break-glass"],
    ),
    (
        "terraform apply/destroy",
        re.compile(r"\bterraform\s+(?:apply|destroy)\b"),
        ["operator-approved", "break-glass", "human-approved", "approved DR change"],
    ),
    (
        "helm install/upgrade",
        re.compile(r"\bhelm\s+(?:install|upgrade)\b"),
        ["operator-approved", "break-glass", "human-approved"],
    ),
    (
        "az deployment group create",
        re.compile(r"\baz\s+deployment\s+group\s+create\b"),
        ["operator-approved", "break-glass", "human-approved"],
    ),
    (
        "docker network mutation",
        re.compile(r"\bdocker\s+network\s+(?:connect|disconnect|create|rm)\b"),
        ["human-approved", "break-glass", "bootstrap-only", "bootstrap only", "operator-approved"],
    ),
    (
        "kubeconfig mutation",
        re.compile(r"\b(?:aws\s+eks\s+update-kubeconfig|az\s+aks\s+get-credentials|kubectl\s+config)\b"),
        ["--kubeconfig", "--file", "temporary kubeconfig", "임시 kubeconfig"],
    ),
]

command_boundary_roots = authored_command_roots + [root / "examples"]
for command_root in command_boundary_roots:
    candidates = command_root.rglob("*") if command_root == root / "examples" else command_root.rglob("*.md")
    for path in sorted(candidates):
        if not path.is_file():
            continue
        if command_root == root / "examples" and path.suffix not in {".md", ".yaml", ".yml", ".sh", ".tf", ".bicep"}:
            continue
        lines = read_text(path).splitlines()
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped == "git push" or "git push origin main" in stripped:
                fail(f"{rel(path)} contains bare/main direct push example; use feature branch + PR flow: line {index + 1}")
            elif re.search(r"\bgit\s+push\b", line):
                if not allowed_push_branch.search(line) or not is_pr_flow_push(lines, index):
                    fail(f"{rel(path)} contains push example without nearby PR-flow context: line {index + 1}")
            for label, pattern, markers in command_boundary_rules:
                if pattern.search(line) and not has_nearby_marker(lines, index, markers):
                    fail(f"{rel(path)} has unmarked {label} example near line {index + 1}")

markdown_direct_push_roots = [
    root / "README.md",
    root / "docs/README.md",
    root / "gitops",
    root / "infrastructure",
    root / "traefik",
    root / "examples",
    root / "docs/05.operations",
    root / "docs/90.references",
]
seen_markdown_direct_push_paths: set[pathlib.Path] = set()
for scan_root in markdown_direct_push_roots:
    candidates = [scan_root] if scan_root.is_file() else scan_root.rglob("*.md")
    for path in sorted(candidates):
        if not path.is_file() or path in seen_markdown_direct_push_paths:
            continue
        seen_markdown_direct_push_paths.add(path)
        lines = read_text(path).splitlines()
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped == "git push" or "git push origin main" in stripped:
                fail(f"{rel(path)} contains bare/main direct push example; use feature branch + PR flow: line {index + 1}")

gateway_contracts = {
    "AGENTS.md": {
        "max_lines": 25,
        "required": [
            "@docs/00.agent-governance/rules/bootstrap.md",
            "@docs/00.agent-governance/providers/codex.md",
            "@.codex/CODEX.md",
            "@RTK.md",
            "docs/00.agent-governance/harness-catalog.md",
        ],
    },
    "CLAUDE.md": {
        "max_lines": 25,
        "required": [
            "@docs/00.agent-governance/rules/bootstrap.md",
            "@docs/00.agent-governance/providers/claude.md",
            "@.claude/CLAUDE.md",
            "@RTK.md",
            "docs/00.agent-governance/harness-catalog.md",
        ],
    },
    "GEMINI.md": {
        "max_lines": 25,
        "required": [
            "@docs/00.agent-governance/rules/bootstrap.md",
            "@docs/00.agent-governance/providers/gemini.md",
            "@.agents/GEMINI.md",
            "@RTK.md",
            "docs/00.agent-governance/harness-catalog.md",
        ],
    },
}
for rel_path, contract in gateway_contracts.items():
    path = root / rel_path
    if not path.exists():
        fail(f"gateway file missing: {rel_path}")
        continue
    text = read_text(path)
    line_count = len(text.splitlines())
    if line_count > contract["max_lines"]:
        fail(f"{rel_path} must remain a thin gateway: {line_count} lines > {contract['max_lines']}")
    for phrase in contract["required"]:
        if phrase not in text:
            fail(f"{rel_path} missing required gateway pointer: {phrase}")
    for stale_heading in ["Agent Catalog", "Role Separation", "Runtime Roster"]:
        if stale_heading in text:
            fail(f"{rel_path} must not embed runtime catalog policy: {stale_heading}")

tracked_language_roots = (
    "docs/00.agent-governance/",
    ".claude/",
    ".codex/",
)
for tracked_path in sorted(tracked):
    if tracked_path == ".claude/settings.local.json":
        continue
    if not tracked_path.startswith(tracked_language_roots):
        continue
    path = root / tracked_path
    if not path.is_file() or path.suffix not in {".md", ".toml", ".json", ".sh"}:
        continue
    if re.search(r"[가-힣]", read_text(path)):
        fail(f"tracked governance/runtime file must remain English-only: {tracked_path}")

agent_section_headings = [
    "AI Agent Requirements",
    "Agent Execution Notes",
    "Agent Harness Requirements",
]
for tracked_path in sorted(tracked):
    if not tracked_path.startswith("docs/") or not tracked_path.endswith(".md"):
        continue
    if tracked_path.startswith("docs/00.agent-governance/"):
        continue
    path = root / tracked_path
    if not path.is_file():
        continue
    text = read_text(path)
    for heading in agent_section_headings:
        match = re.search(rf"^## {re.escape(heading)}(?:\s|\(|$).*?$", text, re.MULTILINE)
        if not match:
            continue
        section_start = match.end()
        next_heading = re.search(r"^##\s+", text[section_start:], re.MULTILINE)
        section = text[section_start : section_start + next_heading.start()] if next_heading else text[section_start:]
        if re.search(r"[가-힣]", section):
            fail(f"{tracked_path} {heading} section must remain English for AI-agent execution requirements")

harness_catalog_path = root / "docs/00.agent-governance/harness-catalog.md"
harness_catalog_text = read_text(harness_catalog_path)
# Normalize pipe-table whitespace so markdown formatters that pad column widths
# do not break substring checks for table header phrases.
import re as _re
harness_catalog_normalized = _re.sub(r"\| +", "| ", _re.sub(r" +\|", " |", harness_catalog_text))
for phrase in [
    "## Harness Four-Element Control Model",
    "Instruction and settings documents -> Architecture constraints -> Feedback loops -> Knowledge stores",
    "Architecture constraints",
    "Feedback loops",
    "Knowledge stores",
    "Domain definition",
    "Data governance",
    "Observability",
    "Continuous evaluation",
    "Documentation language and template routing",
    "Drift garbage collection",
    "## ECC DAILY/LIBRARY Surface",
    "DAILY",
    "LIBRARY",
    "skill-library router is not created",
    "## Agent Eval Completion Contract",
    "Hookify local advisory",
    "AI Agent Requirements",
    "Repeated mistakes must update the harness surface",
    "Permissions and hooks",
    "Codex event hooks",
    "not a permission gate equivalent",
    ".claude/settings.json",
    ".codex/hooks.json",
    "Runtime surface added for LLM Wiki curation",
    "## Matrix Status Contract",
    "`Ready`, `Partial`, and `Missing`",
    "A `Ready` row is not semantic proof",
    "destructive Git deny list",
    "regression and structure guard",
    "Authored-doc command boundary",
    "command examples in authored docs require",
    "### Harness Engineering Matrix",
    "### Agent-first Engineering Matrix",
]:
    if phrase not in harness_catalog_text:
        fail(f"{rel(harness_catalog_path)} missing runtime readiness boundary phrase: {phrase}")
if "| Required Component | Current Surface | Status | Gap | Remediation |" not in harness_catalog_normalized:
    fail(f"{rel(harness_catalog_path)} missing runtime readiness boundary phrase: | Required Component | Current Surface | Status | Gap | Remediation |")
validate_component_matrix(harness_catalog_text, "### Harness Engineering Matrix")
validate_component_matrix(harness_catalog_text, "### Agent-first Engineering Matrix")
for phrase in [
    "Thin gateway",
    "Runtime baseline",
    "Four-element control model",
    "Domain definition",
    "Data governance",
    "Observability",
    "Continuous evaluation",
    "Documentation language and template routing",
    "Drift garbage collection",
    "Local Agents",
    "Agent Adapters",
    "Evidence-first intake",
    "Context hierarchy",
    "JIT loading",
    "Scope and persona routing",
    "Authored-doc command boundaries",
    "risky command examples",
    "Validation before completion",
    "Postflight and handoff",
    "LLM Wiki curation",
]:
    if phrase not in harness_catalog_text:
        fail(f"{rel(harness_catalog_path)} missing component audit matrix entry: {phrase}")

baseline_four_element_checks = {
    root / ".claude/CLAUDE.md": [
        "## Harness Four-Element Runtime Contract",
        "Instruction and settings documents",
        "Architecture constraints",
        "Feedback loops",
        "Knowledge stores",
        "native allow/deny policy",
        "canonical progress ledger",
        "Agent eval completion",
        "Hookify local advisory",
        "harness-catalog.md",
    ],
    root / ".codex/CODEX.md": [
        "## Harness Four-Element Runtime Contract",
        "Instruction and settings documents",
        "Architecture constraints",
        "Feedback loops",
        "Knowledge stores",
        "sandboxing",
        "not a Claude-style permission gate",
        "canonical progress ledger",
        "Agent eval completion",
        "context/validation wiring",
        "harness-catalog.md",
    ],
}
for path, phrases in baseline_four_element_checks.items():
    text = read_text(path)
    for phrase in phrases:
        if phrase not in text:
            fail(f"{rel(path)} missing four-element runtime contract phrase: {phrase}")

workspace_harness_skill_path = root / ".agents/skills/workspace-harness-audit/skill.md"
workspace_harness_skill_text = read_text(workspace_harness_skill_path)
for phrase in [
    "## Workflow Phases",
    "### Phase 1 - Intake and Evidence Boundary",
    "Entry Criteria",
    "Exit Criteria",
    "Verification Criteria",
    "agent-sort",
    "eval-harness",
    "enhance-prompt",
    "DAILY",
    "LIBRARY",
    "four harness elements",
    "instruction and settings documents",
    "architecture constraints",
    "feedback loops",
    "knowledge stores",
    "instructions -> constraints -> feedback ->",
]:
    if phrase not in workspace_harness_skill_text:
        fail(f"{rel(workspace_harness_skill_path)} missing four-element audit phrase: {phrase}")

agentic_path = root / "docs/00.agent-governance/rules/agentic.md"
agentic_text = read_text(agentic_path)
for phrase in [
    "When an agent output fails validation or repeats a mistake",
    "canonical progress ledger",
    "only tracked progress.md",
    "Agent eval completion",
    "## Drift Garbage Collection Defaults",
    "temp_",
    "_backup",
    "## Matrix-first Change Rule",
    "Harness Engineering Matrix",
    "Agent-first Engineering Matrix",
    "Gap",
    "## Context Hierarchy Defaults",
    "root gateway context minimal",
    "Load durable policy just in time",
    "Load task-specific stage docs",
    "not as instructions that override repository governance",
    "Treat authored-doc command examples",
    "command-boundary regression gates",
    "no currently tracked concrete gap",
    "human explicitly requests",
    "equivalent enforcement layers",
]:
    if phrase not in agentic_text:
        fail(f"{rel(agentic_path)} missing Agent-first matrix/context rule phrase: {phrase}")

documentation_protocol_path = root / "docs/00.agent-governance/rules/documentation-protocol.md"
documentation_protocol_text = read_text(documentation_protocol_path)
for phrase in [
    "Folder responsibilities are defined by `stage-authoring-matrix.md`",
    "The canonical template map is the Template Routing Contract",
    "AI Agent Requirements",
    "canonical progress ledger",
    "only tracked `progress.md`",
    "Agent eval completion",
    "## Drift Garbage Collection",
    "code drift, document drift, and structure drift",
]:
    if phrase not in documentation_protocol_text:
        fail(f"{rel(documentation_protocol_path)} missing documentation harness phrase: {phrase}")

docs_readme_path = root / "docs/README.md"
docs_readme_text = read_text(docs_readme_path)
for phrase in [
    "## 문서 역할과 언어 계약",
    "AI Agent Requirements",
    "사람이 읽는 안내와 요약은 한국어를 우선",
]:
    if phrase not in docs_readme_text:
        fail(f"{rel(docs_readme_path)} missing docs language/template contract phrase: {phrase}")

memory_progress_path = root / "docs/00.agent-governance/memory/progress.md"
memory_progress_text = read_text(memory_progress_path)
for phrase in [
    "docs/99.templates/templates/common/progress.template.md",
    "## Work Entries",
    "#### Progress",
    "#### Memory",
    "#### Evidence",
    "#### Handoff",
    "repo-changing agent progress",
    "historical initial implementation snapshot",
    "Current runtime truth",
    "Current script inventory",
    "docs/00.agent-governance/harness-catalog.md",
    "scripts/README.md",
]:
    if phrase not in memory_progress_text:
        fail(f"{rel(memory_progress_path)} missing historical/current-source phrase: {phrase}")

memory_dir = root / "docs/00.agent-governance/memory"
memory_template_path = root / "docs/99.templates/templates/common/memory.template.md"
progress_template_path = root / "docs/99.templates/templates/common/progress.template.md"
for path in [memory_dir / "README.md", memory_progress_path, memory_template_path, progress_template_path]:
    if not path.exists():
        fail(f"required memory contract file is missing: {rel(path)}")

memory_readme_text = read_text(memory_dir / "README.md")
for phrase in [
    "docs/99.templates/templates/common/memory.template.md",
    "docs/99.templates/templates/common/progress.template.md",
    "Standalone files under this folder must use",
    "Related Progress",
    "`progress.md` work entry",
]:
    if phrase not in memory_readme_text:
        fail(f"{rel(memory_dir / 'README.md')} missing memory contract phrase: {phrase}")

for phrase in ["memory.template.md", "progress.template.md", "00.agent-governance/memory/"]:
    if phrase not in template_readme:
        fail(f"{rel(root / 'docs/99.templates/README.md')} missing memory template inventory phrase: {phrase}")

workflow_paths = sorted((root / ".github").glob("**/*.yml")) + sorted((root / ".github").glob("**/*.yaml"))
for workflow in workflow_paths:
    try:
        load_yaml(workflow)
    except Exception as exc:
        fail(f"GitHub Actions YAML parse failed for {rel(workflow)}: {exc}")

for workflow in sorted((root / ".github/workflows").glob("*.yml")):
    try:
        data = load_yaml(workflow)
    except Exception:
        continue
    for job_id, job in (data.get("jobs") or {}).items():
        seen = collections.Counter()
        for step in job.get("steps") or []:
            label = step.get("name") or step.get("uses") or (step.get("run") or "").strip().splitlines()[0:1]
            if isinstance(label, list):
                label = label[0] if label else "<unnamed>"
            seen[str(label)] += 1
        for label, count in seen.items():
            if label and label != "<unnamed>" and count > 1:
                fail(f"duplicate workflow step in {rel(workflow)} job {job_id}: {label}")

codeowners_path = root / ".github/CODEOWNERS"
codeowners_text = read_text(codeowners_path)
if not re.search(r"^/\.github/\s+@buenhyden(?:\s|$)", codeowners_text, re.MULTILINE):
    fail(".github/CODEOWNERS must assign /.github/ ownership to @buenhyden")

action_security_self_test = subprocess.run(
    [sys.executable, str(root / "scripts/validate-github-actions-security.py"), "--self-test"],
    cwd=root,
    text=True,
    capture_output=True,
)
if action_security_self_test.returncode != 0:
    fail("GitHub Actions security self-test failed: " + action_security_self_test.stdout.strip())

action_security = subprocess.run(
    [sys.executable, str(root / "scripts/validate-github-actions-security.py"), "--root", str(root)],
    cwd=root,
    text=True,
    capture_output=True,
)
if action_security.returncode != 0:
    fail("GitHub Actions security validation failed: " + action_security.stdout.strip())

git_workflow_path = root / "docs/00.agent-governance/rules/git-workflow.md"
git_workflow_text = read_text(git_workflow_path)
branch_prefixes = branch_prefixes_from_git_workflow(git_workflow_path)
if not branch_prefixes:
    fail(f"{rel(git_workflow_path)} must define branch types as the branch prefix policy SSoT")
for phrase in [
    "Every pull request targeting `main` must run the required CI and branch-policy checks with no bypass exceptions.",
    "Do not run destructive or history-rewriting Git commands from the default",
    "Shared Claude permissions deny",
    "git reset --hard",
    "git checkout --",
    "git restore",
    "git clean",
    "git rebase",
    "git commit --amend",
    "git branch -D",
    "git push --force",
    "git push -f",
    "git push --delete",
    "git push --mirror",
    "record the approval scope, target branch, rollback or backup expectation",
    "Draft or WIP PRs",
    "90% coverage",
    "validation-matrix coverage",
]:
    if phrase not in git_workflow_text:
        fail(f"{rel(git_workflow_path)} missing PR/coverage governance phrase: {phrase}")

quality_standards_path = root / "docs/00.agent-governance/rules/quality-standards.md"
quality_standards_text = read_text(quality_standards_path)
for phrase in [
    "90% line and branch coverage",
    "validation-matrix coverage",
    "PR verification must state which coverage lane applies",
]:
    if phrase not in quality_standards_text:
        fail(f"{rel(quality_standards_path)} missing coverage applicability phrase: {phrase}")

qa_scope_path = root / "docs/00.agent-governance/scopes/qa.md"
qa_scope_text = read_text(qa_scope_path)
for phrase in [
    "90% coverage",
    "validation-matrix coverage",
]:
    if phrase not in qa_scope_text:
        fail(f"{rel(qa_scope_path)} missing coverage applicability phrase: {phrase}")

ci_cd_qa_guide_path = root / "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md"
ci_cd_qa_guide_text = read_text(ci_cd_qa_guide_path)
for phrase in [
    "90% coverage",
    "validation-matrix",
]:
    if phrase not in ci_cd_qa_guide_text:
        fail(f"{rel(ci_cd_qa_guide_path)} missing coverage applicability phrase: {phrase}")

ci_path = root / ".github/workflows/ci.yml"
ci_text = read_text(ci_path)
try:
    ci_data = load_yaml(ci_path)
except Exception as exc:
    fail(f"CI workflow parse failed for {rel(ci_path)}: {exc}")
    ci_data = {}

ci_on = workflow_on(ci_data)
if ci_data.get("name") != "CI":
    fail(f"{rel(ci_path)} workflow name must remain CI")
if not isinstance(ci_on, dict):
    fail(f"{rel(ci_path)} must declare structured push and pull_request triggers")
else:
    for event_name in ["push", "pull_request"]:
        event_config = ci_on.get(event_name)
        branches = []
        if isinstance(event_config, dict):
            branch_value = event_config.get("branches") or []
            branches = branch_value if isinstance(branch_value, list) else [branch_value]
        if branches != ["main"]:
            fail(f"{rel(ci_path)} {event_name} trigger must target only main: {branches}")
    if "workflow_dispatch" not in ci_on:
        fail(f"{rel(ci_path)} must include workflow_dispatch for manual QA reruns")
    if set(ci_on) != {"push", "pull_request", "workflow_dispatch"}:
        fail(f"{rel(ci_path)} workflow triggers must remain exact Spec 031 triggers")

ci_jobs = ci_data.get("jobs") or {}
required_ci_jobs = {
    "branch-policy",
    "changes",
    "pre-commit",
    "repo-quality-static",
    "manifest-static",
    "ci-summary",
}
for job_id in sorted(required_ci_jobs - set(ci_jobs)):
    fail(f"{rel(ci_path)} missing required CI job: {job_id}")
if set(ci_jobs) != required_ci_jobs:
    fail(f"{rel(ci_path)} job IDs must remain exact Spec 031 jobs: {sorted(required_ci_jobs)}")

expected_job_needs = {
    "branch-policy": [],
    "changes": [],
    "pre-commit": ["changes"],
    "repo-quality-static": ["changes"],
    "manifest-static": ["changes"],
    "ci-summary": [
        "branch-policy",
        "changes",
        "pre-commit",
        "repo-quality-static",
        "manifest-static",
    ],
}
expected_job_if = {
    "branch-policy": "github.event_name == 'pull_request'",
    "changes": "",
    "pre-commit": "needs.changes.outputs.precommit == 'true'",
    "repo-quality-static": "needs.changes.outputs.repo_quality == 'true'",
    "manifest-static": "needs.changes.outputs.manifests == 'true'",
    "ci-summary": "always()",
}
for job_id in sorted(required_ci_jobs):
    job = ci_jobs.get(job_id) or {}
    needs = job.get("needs") or []
    if isinstance(needs, str):
        needs = [needs]
    if needs != expected_job_needs[job_id]:
        fail(f"{rel(ci_path)} {job_id} needs must remain {expected_job_needs[job_id]}")
    if str(job.get("if") or "") != expected_job_if[job_id]:
        fail(f"{rel(ci_path)} {job_id} if must remain {expected_job_if[job_id]!r}")

branch_policy_job = ci_jobs.get("branch-policy") or {}
branch_policy_if = str(branch_policy_job.get("if") or "")
if "github.event_name == 'pull_request'" not in branch_policy_if:
    fail(f"{rel(ci_path)} branch-policy must run only for pull_request")
branch_policy_text = "\n".join(
    str(step.get("run") or "")
    for step in branch_policy_job.get("steps") or []
)
for phrase in [
    "BASE_REF",
    "HEAD_REF",
    "allowed_branch_regex",
    "PR base branch must be main",
    "branch-policy=ok",
]:
    if phrase not in branch_policy_text:
        fail(f"{rel(ci_path)} branch-policy missing validation phrase: {phrase}")

ci_branch_prefixes = extract_ci_branch_policy_prefixes(branch_policy_text)
if ci_branch_prefixes != branch_prefixes:
    fail(
        f"{rel(ci_path)} branch-policy prefixes must match {rel(git_workflow_path)} "
        f"SSoT: expected {format_branch_prefixes(branch_prefixes)} got {format_branch_prefixes(ci_branch_prefixes)}"
    )
for prefix in branch_prefixes:
    if prefix not in branch_policy_text:
        fail(
            f"{rel(ci_path)} branch-policy message missing branch prefix from "
            f"{rel(git_workflow_path)} SSoT: {prefix}/"
        )

ci_summary_job = ci_jobs.get("ci-summary") or {}
ci_summary_needs = ci_summary_job.get("needs") or []
if isinstance(ci_summary_needs, str):
    ci_summary_needs = [ci_summary_needs]
for job_id in sorted(required_ci_jobs - set(ci_summary_needs)):
    if job_id != "ci-summary":
        fail(f"{rel(ci_path)} ci-summary must aggregate required CI job: {job_id}")
ci_summary_text = "\n".join(
    str(step.get("run") or "")
    for step in ci_summary_job.get("steps") or []
)
ci_summary_env_text = "\n".join(
    "\n".join(f"{key}={value}" for key, value in (step.get("env") or {}).items())
    for step in ci_summary_job.get("steps") or []
)
for phrase in ["BRANCH_POLICY_RESULT", "branch-policy="]:
    if phrase not in (ci_summary_text + "\n" + ci_summary_env_text):
        fail(f"{rel(ci_path)} ci-summary missing branch-policy linkage: {phrase}")

changes_job = ci_jobs.get("changes") or {}
expected_changes_outputs = {
    "precommit": "${{ steps.filter.outputs.precommit }}",
    "repo_quality": "${{ steps.filter.outputs.repo_quality }}",
    "manifests": "${{ steps.filter.outputs.manifests }}",
}
if changes_job.get("outputs") != expected_changes_outputs:
    fail(
        f"{rel(ci_path)} changes outputs must be canonical selector outputs: "
        f"{expected_changes_outputs}"
    )

changes_steps = changes_job.get("steps") or []
changes_checkout_steps = [
    step
    for step in changes_steps
    if step.get("uses") == "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"
]
if len(changes_checkout_steps) != 1:
    fail(f"{rel(ci_path)} changes job must have exactly one pinned checkout step")
elif (changes_checkout_steps[0].get("with") or {}).get("fetch-depth") != 0:
    fail(f"{rel(ci_path)} changes checkout must use fetch-depth: 0")

selector_steps = [step for step in changes_steps if step.get("id") == "filter"]
if len(selector_steps) != 1:
    fail(f"{rel(ci_path)} changes job must have exactly one selector step with id=filter")
    selector_step = {}
else:
    selector_step = selector_steps[0]
if selector_step.get("uses"):
    fail(f"{rel(ci_path)} canonical selector step must not delegate to an Action")
selector_run = str(selector_step.get("run") or "")
for marker in [
    "git diff --name-only -z",
    "git ls-tree -r --name-only -z",
    '"$RUNNER_TEMP/changed-paths.nul"',
    "python3 scripts/select-affected-surfaces.py",
    "--lane ci",
    "--delimiter nul",
    "--format github-output",
    '>> "$GITHUB_OUTPUT"',
]:
    if marker not in selector_run:
        fail(f"{rel(ci_path)} canonical selector step missing marker: {marker}")
for forbidden_marker in ["$(", "`", "dorny/paths-filter", "filters: |"]:
    if forbidden_marker in selector_run or forbidden_marker in ci_text:
        fail(f"{rel(ci_path)} canonical selector contains forbidden marker: {forbidden_marker}")


manifest_static_steps = (ci_jobs.get("manifest-static") or {}).get("steps") or []
manifest_checkout_steps = [
    step
    for step in manifest_static_steps
    if step.get("uses") == "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"
]
if len(manifest_checkout_steps) != 1:
    fail(f"{rel(ci_path)} manifest-static must have exactly one pinned checkout step")
else:
    manifest_checkout_with = manifest_checkout_steps[0].get("with") or {}
    if manifest_checkout_with.get("persist-credentials") is not False:
        fail(f"{rel(ci_path)} manifest-static checkout must disable persisted credentials")
    if manifest_checkout_with.get("fetch-depth") != 0:
        fail(f"{rel(ci_path)} manifest-static checkout must use fetch-depth: 0")

gitops_change_set_steps = [
    step
    for step in manifest_static_steps
    if step.get("name") == "Review GitOps object identity and deletion set"
]
if len(gitops_change_set_steps) != 1:
    fail(f"{rel(ci_path)} manifest-static must contain exactly one GitOps change-set step")
else:
    gitops_change_set_step = gitops_change_set_steps[0]
    expected_gitops_change_set_env = {
        "BASE_REF": "${{ github.event.pull_request.base.sha || github.event.before || github.sha }}"
    }
    if gitops_change_set_step.get("env") != expected_gitops_change_set_env:
        fail(
            f"{rel(ci_path)} GitOps change-set env must equal: "
            f"{expected_gitops_change_set_env}"
        )
    expected_gitops_change_set_run = (
        'python3 scripts/validate-gitops-change-set.py --root . --base-ref "$BASE_REF"'
    )
    if str(gitops_change_set_step.get("run") or "").strip() != expected_gitops_change_set_run:
        fail(
            f"{rel(ci_path)} GitOps change-set command must equal: "
            f"{expected_gitops_change_set_run}"
        )

manifest_static_runs = "\n".join(
    str(step.get("run") or "")
    for step in manifest_static_steps
)
for command in [
    'python3 scripts/validate-gitops-change-set.py --root . --base-ref "$BASE_REF"',
    "bash infrastructure/tests/verify-contracts-static.sh",
    "bash scripts/validate-gitops-structure.sh",
    "bash scripts/validate-k8s-manifests.sh .",
    "bash scripts/check-secret-handling.sh .",
    "python3 scripts/validate-vault-eso-contracts.py --root .",
    "bash scripts/validate-policy-gates.sh .",
]:
    if command not in manifest_static_runs:
        fail(f"{rel(ci_path)} manifest-static missing command: {command}")

static_contract_steps = [
    step for step in manifest_static_steps if step.get("name") == "Run static contract checks"
]
expected_static_contract_commands = [
    "bash infrastructure/tests/verify-contracts-static.sh",
    "bash scripts/validate-gitops-structure.sh",
    "bash scripts/validate-k8s-manifests.sh .",
    "bash scripts/check-secret-handling.sh .",
    "python3 scripts/validate-vault-eso-contracts.py --root .",
    "bash scripts/validate-policy-gates.sh .",
]
if len(static_contract_steps) != 1:
    fail(f"{rel(ci_path)} manifest-static must contain exactly one static contract step")
else:
    actual_static_contract_commands = [
        line.strip()
        for line in str(static_contract_steps[0].get("run") or "").splitlines()
        if line.strip()
    ]
    if actual_static_contract_commands != expected_static_contract_commands:
        fail(
            f"{rel(ci_path)} manifest-static static commands must remain exact and ordered: "
            f"{expected_static_contract_commands}"
        )



pr_template_path = root / ".github/PULL_REQUEST_TEMPLATE.md"
pr_template_text = read_text(pr_template_path)

for phrase in [
    "Workflow path filters and job ownership reviewed",
    "No live cluster mutation",
    "approved prefix",
    "`main`",
]:
    if phrase not in pr_template_text:
        fail(f"{rel(pr_template_path)} missing GitHub/GitOps review phrase: {phrase}")
for phrase in [
    "any exception must update CI `branch-policy` and governance in the same change",
    "No PR targeting `main` bypasses CI or branch-policy checks",
    "Draft/WIP status is intentional",
    "90% target for future testable application code",
    "`test`: Tests or validation updates",
    "`chore`: Maintenance updates",
    "`infra` is a change type, not an approved branch prefix",
    "branch protection/rulesets enforce direct-push restrictions",
]:
    if phrase not in pr_template_text:
        fail(f"{rel(pr_template_path)} missing branch-policy clarification: {phrase}")
if not has_cloud_example_snapshot_preservation_prompt(pr_template_text):
    fail(
        f"{rel(pr_template_path)} missing Cloud Example Snapshot checklist line with "
        "examples/aws, examples/azure, boundary preservation, and approved provider refresh spec terms"
    )

# Harness implementation surfaces: existence and cross-reference contracts only.
# Wrapper script existence is already enforced by the scripts inventory, so it
# is not re-validated here.
harness_map_path = root / "docs/00.agent-governance/harness-implementation-map.md"
if not harness_map_path.exists():
    fail(f"required harness surface is missing: {rel(harness_map_path)}")
approval_boundaries_path = root / "docs/00.agent-governance/rules/approval-boundaries.md"
if not approval_boundaries_path.exists():
    fail(f"required harness surface is missing: {rel(approval_boundaries_path)}")
if "## 8. Harness Impact" not in pr_template_text:
    fail(f"{rel(pr_template_path)} missing Harness Impact section heading: ## 8. Harness Impact")
harness_catalog_map_text = read_text(root / "docs/00.agent-governance/harness-catalog.md")
if (
    "harness-implementation-map.md" not in harness_catalog_map_text
    and "approval-boundaries.md" not in harness_catalog_map_text
):
    fail(
        "docs/00.agent-governance/harness-catalog.md must reference the harness "
        "implementation map or approval boundaries"
    )
canonical_task_form_text = read_text(
    root / "docs/99.templates/templates/sdlc/execution/task.template.md"
)
for phrase in [
    "## Approval and Safety Boundaries",
    "**Allowed Paths**:",
    "**Forbidden Paths**:",
    "**Approval Required**:",
    "**Static Validation**:",
    "**Live Validation**:",
    "**Secret / Vault Handling**:",
    "**Rollback Plan**:",
    "**Evidence Location**:",
]:
    if phrase not in canonical_task_form_text:
        fail(f"canonical Task form missing approval/safety contract field: {phrase}")

pr_branch_prefixes = extract_pr_template_prefixes(pr_template_text)
if pr_branch_prefixes != branch_prefixes:
    fail(
        f"{rel(pr_template_path)} approved branch prefixes must match {rel(git_workflow_path)} "
        f"SSoT: expected {format_branch_prefixes(branch_prefixes)} got {format_branch_prefixes(pr_branch_prefixes)}"
    )
for prefix in branch_prefixes:
    prefix_label = f"{prefix}/"
    if prefix not in pr_template_text:
        fail(
            f"{rel(pr_template_path)} missing approved source branch prefix from "
            f"{rel(git_workflow_path)} SSoT: {prefix_label}"
        )

github_about_path = root / ".github/ABOUT.md"
github_about_text = read_text(github_about_path)
for phrase in [
    "docs/00.agent-governance/rules/git-workflow.md",
    "workflows/ci.yml",
    "scripts/validate-repo-quality-gates.sh",
    "PULL_REQUEST_TEMPLATE.md",
    "docs/90.references/data/tech-stack-version-inventory.md",
    "branch protection/rulesets enforce direct-push restrictions",
    "QA gates and release-evidence automation, not deploy CD",
    "Source Basis",
    "Parent Spec",
    "GitHub Actions documentation",
]:
    if phrase not in github_about_text:
        fail(f"{rel(github_about_path)} must route to the policy/enforcement SSoT instead of duplicating policy: {phrase}")
if "docs/90.references/tech-stack-version-inventory.md" in github_about_text:
    fail(f"{rel(github_about_path)} contains stale version inventory path without versions/ segment")
if "PR source branches must start" in github_about_text or "Default PR target is `main`" in github_about_text:
    fail(
        f"{rel(github_about_path)} must not duplicate branch-policy prose; "
        f"move branch rules to {rel(git_workflow_path)} and keep enforcement in {rel(ci_path)}"
    )
about_prefix_count = sum(1 for prefix in branch_prefixes if f"{prefix}/" in github_about_text)
if about_prefix_count >= len(branch_prefixes):
    fail(
        f"{rel(github_about_path)} must not mirror the full branch prefix list; "
        f"use {rel(git_workflow_path)} as the branch policy SSoT"
    )

workflow_responsibility_rows = markdown_table_after_heading(
    github_about_text,
    "## Workflow Responsibility Matrix",
)
expected_workflow_responsibility_header = [
    "Workflow",
    "Role",
    "Trigger / scope",
    "Required evidence",
    "Boundary",
]
expected_workflows = [path.name for path in sorted((root / ".github/workflows").glob("*.yml"))]
if len(workflow_responsibility_rows) < 2:
    fail(".github/ABOUT.md Workflow Responsibility Matrix must contain a header and workflow rows")
elif workflow_responsibility_rows[0] != expected_workflow_responsibility_header:
    fail(
        ".github/ABOUT.md Workflow Responsibility Matrix header must be: "
        + " | ".join(expected_workflow_responsibility_header)
    )
else:
    indexed_workflows: list[str] = []
    for row_number, row in enumerate(workflow_responsibility_rows[1:], start=1):
        if len(row) != len(expected_workflow_responsibility_header):
            fail(
                ".github/ABOUT.md Workflow Responsibility Matrix "
                f"row {row_number} must have {len(expected_workflow_responsibility_header)} columns"
            )
            continue
        workflow_cell, role, trigger_scope, required_evidence, boundary = row
        match = re.fullmatch(r"`([^`]+\.yml)`", workflow_cell)
        if not match:
            fail(
                ".github/ABOUT.md Workflow Responsibility Matrix "
                f"row {row_number} must start with a backticked workflow filename"
            )
            continue
        workflow_name = match.group(1)
        indexed_workflows.append(workflow_name)
        if not (root / ".github/workflows" / workflow_name).is_file():
            fail(f".github/ABOUT.md Workflow Responsibility Matrix references missing workflow: {workflow_name}")
        for label, value in [
            ("Role", role),
            ("Trigger / scope", trigger_scope),
            ("Required evidence", required_evidence),
            ("Boundary", boundary),
        ]:
            if not value:
                fail(f".github/ABOUT.md Workflow Responsibility Matrix row {row_number} has empty {label}")
        if workflow_name == "ci.yml":
            for phrase, value in [
                ("Required QA gate", role),
                ("repo-quality", role),
                ("manifest", role),
                ("secret", role),
                ("push", trigger_scope),
                ("pull_request", trigger_scope),
                ("workflow_dispatch", trigger_scope),
                ("ci-summary", required_evidence),
                ("repo-quality-static", required_evidence),
                ("manifest-static", required_evidence),
                ("No deploy CD", boundary),
                ("direct Kubernetes mutation", boundary),
                ("external Vault mutation", boundary),
            ]:
                if phrase not in value:
                    fail(f".github/ABOUT.md ci.yml responsibility row missing phrase: {phrase}")
        elif workflow_name == "generate-changelog.yml":
            for phrase, value in [
                ("Release-evidence", role),
                ("release tag", trigger_scope),
                ("CHANGELOG.md", required_evidence),
                ("Does not commit", boundary),
                ("push", boundary),
                ("publish", boundary),
            ]:
                if phrase not in value:
                    fail(f".github/ABOUT.md generate-changelog.yml responsibility row missing phrase: {phrase}")
        elif workflow_name == "greetings.yml":
            for phrase, value in [
                ("maintenance greeting", role),
                ("issue or PR", trigger_scope),
                ("onboarding guidance", required_evidence),
                ("Not a QA gate", boundary),
                ("deployment automation", boundary),
            ]:
                if phrase not in value:
                    fail(f".github/ABOUT.md greetings.yml responsibility row missing phrase: {phrase}")
        elif workflow_name == "labeler.yml":
            for phrase, value in [
                ("maintenance labeling", role),
                ("pull request", trigger_scope),
                (".github/labeler.yml", required_evidence),
                ("Not a QA gate", boundary),
                ("CODEOWNERS", boundary),
                ("human review", boundary),
            ]:
                if phrase not in value:
                    fail(f".github/ABOUT.md labeler.yml responsibility row missing phrase: {phrase}")
        elif workflow_name == "stale.yml":
            for phrase, value in [
                ("maintenance stale-item", role),
                ("scheduled", trigger_scope),
                ("stale", required_evidence),
                ("Not a QA gate", boundary),
                ("not release evidence", boundary),
                ("deployment automation", boundary),
            ]:
                if phrase not in value:
                    fail(f".github/ABOUT.md stale.yml responsibility row missing phrase: {phrase}")
    if indexed_workflows != expected_workflows:
        fail(
            ".github/ABOUT.md Workflow Responsibility Matrix row order must match actual workflows: "
            + ", ".join(expected_workflows)
        )

labeler_path = root / ".github/labeler.yml"
labeler_data = load_yaml(labeler_path)
test_label_globs = set(collect_strings(labeler_data.get("area/tests") or []))
for expected_glob in ["tests/**", "infrastructure/tests/**"]:
    if expected_glob not in test_label_globs:
        fail(f"{rel(labeler_path)} area/tests missing glob: {expected_glob}")

for workflow in sorted((root / ".github/workflows").glob("*.yml")):
    workflow_text = read_text(workflow)
    for command in [
        "kubectl apply",
        "kubectl patch",
        "argocd app sync",
        "argocd app set",
        "vault kv",
        "docker push",
        "git push",
    ]:
        if command in workflow_text:
            fail(f"{rel(workflow)} contains forbidden live mutation or publish command: {command}")

    try:
        workflow_data = load_yaml(workflow)
    except Exception:
        continue
    if workflow.name in {"generate-changelog.yml", "labeler.yml", "stale.yml"} and "concurrency" not in workflow_data:
        fail(f"{rel(workflow)} must declare workflow-level concurrency")
    for job_id, job in (workflow_data.get("jobs") or {}).items():
        if "timeout-minutes" not in job:
            fail(f"{rel(workflow)} job {job_id} must declare timeout-minutes")
        for step in job.get("steps") or []:
            run_block = str(step.get("run") or "")
            if re.search(r"\$\{\{\s*needs(?:\.|\[)[^}]*\.result\s*\}\}", run_block):
                fail(f"{rel(workflow)} job {job_id} run block expands needs.*.result directly")

for json_path in [root / ".claude/settings.json", root / ".agents/hooks.json", root / ".codex/hooks.json"]:
    try:
        load_json(json_path)
    except Exception as exc:
        fail(f"agent runtime JSON parse failed for {rel(json_path)}: {exc}")

claude_settings = load_json(root / ".claude/settings.json")
claude_permissions = claude_settings.get("permissions") or {}
claude_allow = set(claude_permissions.get("allow") or [])
claude_deny = set(claude_permissions.get("deny") or [])
if "Bash(git:*)" not in claude_allow:
    fail(".claude/settings.json must keep broad Git routing explicit before deny hardening")
for allow_rule in [
    "Bash(bash scripts/validate-repo-quality-gates.sh:*)",
    "Bash(bash scripts/validate-k8s-manifests.sh:*)",
    "Bash(bash scripts/validate-gitops-structure.sh:*)",
    "Bash(bash scripts/check-secret-handling.sh:*)",
    "Bash(bash scripts/validate-policy-gates.sh:*)",
]:
    if allow_rule not in claude_allow:
        fail(f".claude/settings.json missing local QA allow rule: {allow_rule}")
expected_destructive_git_denies = [
    "Bash(git reset --hard:*)",
    "Bash(git checkout --:*)",
    "Bash(git restore:*)",
    "Bash(git clean:*)",
    "Bash(git rebase:*)",
    "Bash(git commit --amend:*)",
    "Bash(git branch -D:*)",
    "Bash(git push --force:*)",
    "Bash(git push -f:*)",
    "Bash(git push --delete:*)",
    "Bash(git push --mirror:*)",
]
for deny_rule in expected_destructive_git_denies:
    if deny_rule not in claude_deny:
        fail(f".claude/settings.json missing destructive Git deny rule: {deny_rule}")
post_validate_command = json.dumps(claude_settings.get("hooks", {}))
for phrase in [
    "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
    "docs/00.agent-governance/hooks/post-validate.sh",
    "docs/00.agent-governance/hooks/session-start.sh",
    "docs/00.agent-governance/hooks/lifecycle-guard.sh",
    '"Stop"',
    '"SubagentStop"',
    '"PreCompact"',
    '"timeout": 60',
    '"timeout": 20',
]:
    if phrase not in post_validate_command and phrase not in read_text(root / ".claude/settings.json"):
        fail(f".claude/settings.json missing hook contract phrase: {phrase}")

codex_hooks_path = root / ".codex/hooks.json"
codex_hooks = load_json(codex_hooks_path).get("hooks", {})
for event_name in ["SessionStart", "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "PreCompact"]:
    if event_name not in codex_hooks:
        fail(f"{rel(codex_hooks_path)} missing event hook: {event_name}")
codex_hooks_text = read_text(codex_hooks_path)
for phrase in [
    "docs/00.agent-governance/hooks/session-start.sh",
    "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
    "docs/00.agent-governance/hooks/post-validate.sh",
    "docs/00.agent-governance/hooks/lifecycle-guard.sh",
    "CODEX_PROJECT_DIR",
    "Glob|Grep",
    '"timeout": 60',
    '"timeout": 20',
]:
    if phrase not in codex_hooks_text:
        fail(f"{rel(codex_hooks_path)} missing Codex event hook phrase: {phrase}")

gemini_hooks_path = root / ".agents/hooks.json"
gemini_hooks = load_json(gemini_hooks_path).get("hooks", {})
for event_name in ["SessionStart", "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "PreCompact"]:
    if event_name not in gemini_hooks:
        fail(f"{rel(gemini_hooks_path)} missing event hook: {event_name}")
gemini_hooks_text = read_text(gemini_hooks_path)
for phrase in [
    "docs/00.agent-governance/hooks/session-start.sh",
    "docs/00.agent-governance/hooks/k8s-pre-edit.sh",
    "docs/00.agent-governance/hooks/post-validate.sh",
    "docs/00.agent-governance/hooks/lifecycle-guard.sh",
    "GEMINI_PROJECT_DIR",
    "Glob|Grep",
    '"timeout": 60',
    '"timeout": 20',
]:
    if phrase not in gemini_hooks_text:
        fail(f"{rel(gemini_hooks_path)} missing Gemini event hook phrase: {phrase}")


def hook_command(data: dict, event_name: str, matcher: str, script_name: str) -> str:
    for entry in data.get(event_name, []) or []:
        if entry.get("matcher") != matcher:
            continue
        for hook in entry.get("hooks", []) or []:
            command = str(hook.get("command") or "")
            if script_name in command:
                return command
    return ""


if os.environ.get("HY_HOME_K8S_SKIP_HOOK_SIMULATION") != "1":
    hook_env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
    manifest_hook_payload = json.dumps(
        {"tool_input": {"file_path": "gitops/platform/headlamp/headlamp-ingress.yaml"}}
    )
    docs_hook_payload = json.dumps(
        {"tool_input": {"file_path": "docs/03.specs/example-feature/api-spec.md"}}
    )
    pre_hook_path = root / "docs/00.agent-governance/hooks/k8s-pre-edit.sh"
    pre_hook_result = subprocess.run(
        ["bash", str(pre_hook_path)],
        cwd=root,
        input=manifest_hook_payload,
        text=True,
        capture_output=True,
        env=hook_env,
    )
    if pre_hook_result.returncode != 0:
        fail(f"{rel(pre_hook_path)} payload simulation failed: {pre_hook_result.stderr.strip()}")
    for phrase in ["systemMessage", "GitOps-first", "PostToolUse hook"]:
        if phrase not in pre_hook_result.stdout:
            fail(f"{rel(pre_hook_path)} payload simulation missing output phrase: {phrase}")

    docs_pre_hook_result = subprocess.run(
        ["bash", str(pre_hook_path)],
        cwd=root,
        input=docs_hook_payload,
        text=True,
        capture_output=True,
        env=hook_env,
    )
    if docs_pre_hook_result.returncode != 0:
        fail(f"{rel(pre_hook_path)} docs payload simulation failed: {docs_pre_hook_result.stderr.strip()}")
    for phrase in [
        "Template-First",
        "docs/99.templates/README.md",
        "docs/99.templates/templates/sdlc/specs/api-spec.template.md",
        "documentation template enforcement",
    ]:
        if phrase not in docs_pre_hook_result.stdout:
            fail(f"{rel(pre_hook_path)} docs payload simulation missing output phrase: {phrase}")

    post_hook_path = root / "docs/00.agent-governance/hooks/post-validate.sh"
    post_hook_result = subprocess.run(
        ["bash", str(post_hook_path)],
        cwd=root,
        input=manifest_hook_payload,
        text=True,
        capture_output=True,
        env=hook_env,
    )
    if post_hook_result.returncode != 0:
        detail = "\n".join(
            item
            for item in [post_hook_result.stdout.strip(), post_hook_result.stderr.strip()]
            if item
        )
        fail(f"{rel(post_hook_path)} manifest payload simulation failed:\n{detail}")
    for phrase in [
        "[hook] PASS Kubernetes manifests",
        "[hook] PASS secret handling",
    ]:
        if phrase not in post_hook_result.stdout:
            fail(f"{rel(post_hook_path)} manifest payload simulation missing output phrase: {phrase}")

    docs_post_hook_result = subprocess.run(
        ["bash", str(post_hook_path)],
        cwd=root,
        input=docs_hook_payload,
        text=True,
        capture_output=True,
        env=hook_env,
    )
    if docs_post_hook_result.returncode != 0:
        detail = "\n".join(
            item
            for item in [docs_post_hook_result.stdout.strip(), docs_post_hook_result.stderr.strip()]
            if item
        )
        fail(f"{rel(post_hook_path)} docs payload simulation failed:\n{detail}")
    if "[hook] PASS documentation template enforcement" not in docs_post_hook_result.stdout:
        fail(f"{rel(post_hook_path)} docs payload simulation missing template enforcement output")

    lifecycle_hook_path = root / "docs/00.agent-governance/hooks/lifecycle-guard.sh"
    lifecycle_selftest_env = {
        **hook_env,
        "HY_HOME_K8S_LIFECYCLE_GUARD_SELFTEST": "1",
        "HY_HOME_K8S_CHANGED_PATHS": "docs/01.requirements/example.md",
    }
    clean_stop_result = subprocess.run(
        ["bash", str(lifecycle_hook_path)],
        cwd=root,
        input=json.dumps({"hook_event_name": "Stop"}),
        text=True,
        capture_output=True,
        env=lifecycle_selftest_env,
    )
    if clean_stop_result.returncode != 0:
        fail(f"{rel(lifecycle_hook_path)} clean Stop payload simulation failed: {clean_stop_result.stderr.strip()}")
    if "block" in clean_stop_result.stdout:
        fail(f"{rel(lifecycle_hook_path)} clean Stop payload simulation unexpectedly blocked")
    for phrase in [
        "systemMessage",
        "Task-unit commit discipline",
        "git diff --cached",
        "dirty state spans multiple SDD overlays",
        "forward-only exception",
    ]:
        if phrase not in clean_stop_result.stdout:
            fail(f"{rel(lifecycle_hook_path)} clean Stop payload simulation missing task-unit commit phrase: {phrase}")

    failing_stop_result = subprocess.run(
        ["bash", str(lifecycle_hook_path)],
        cwd=root,
        input=json.dumps({"hook_event_name": "Stop"}),
        text=True,
        capture_output=True,
        env={**lifecycle_selftest_env, "HY_HOME_K8S_FORCE_FAIL": "1"},
    )
    if failing_stop_result.returncode != 0:
        fail(f"{rel(lifecycle_hook_path)} failing Stop payload simulation exited non-zero")
    for phrase in ["decision", "block", "validation failed"]:
        if phrase not in failing_stop_result.stdout:
            fail(f"{rel(lifecycle_hook_path)} failing Stop payload simulation missing output phrase: {phrase}")

    failing_subagent_result = subprocess.run(
        ["bash", str(lifecycle_hook_path)],
        cwd=root,
        input=json.dumps({"hook_event_name": "SubagentStop"}),
        text=True,
        capture_output=True,
        env={**lifecycle_selftest_env, "HY_HOME_K8S_FORCE_FAIL": "1"},
    )
    if failing_subagent_result.returncode != 0:
        fail(f"{rel(lifecycle_hook_path)} failing SubagentStop payload simulation exited non-zero")
    for phrase in ["decision", "block", "SubagentStop"]:
        if phrase not in failing_subagent_result.stdout:
            fail(f"{rel(lifecycle_hook_path)} failing SubagentStop payload simulation missing output phrase: {phrase}")

    precompact_result = subprocess.run(
        ["bash", str(lifecycle_hook_path)],
        cwd=root,
        input=json.dumps({"hook_event_name": "PreCompact", "trigger": "manual"}),
        text=True,
        capture_output=True,
        env={
            **hook_env,
            "HY_HOME_K8S_LIFECYCLE_GUARD_SELFTEST": "1",
            "HY_HOME_K8S_CHANGED_PATHS": ".claude/settings.json\n.codex/hooks.json",
        },
    )
    if precompact_result.returncode != 0:
        fail(f"{rel(lifecycle_hook_path)} PreCompact payload simulation failed: {precompact_result.stderr.strip()}")
    for phrase in [
        "systemMessage",
        "Lifecycle guard",
        "Suggested validation",
        "Task-unit commit discipline",
        "dirty state spans multiple SDD overlays",
        "forward-only exception",
    ]:
        if phrase not in precompact_result.stdout:
            fail(f"{rel(lifecycle_hook_path)} PreCompact payload simulation missing output phrase: {phrase}")
    if '"decision": "block"' in precompact_result.stdout:
        fail(f"{rel(lifecycle_hook_path)} PreCompact payload simulation must not block")

    codex_hook_env = {
        **os.environ,
        "CODEX_PROJECT_DIR": str(root),
        "CLAUDE_PROJECT_DIR": str(root),
    }
    codex_pre_command = hook_command(codex_hooks, "PreToolUse", "Write|Edit|MultiEdit", "k8s-pre-edit.sh")
    if not codex_pre_command:
        fail(f"{rel(codex_hooks_path)} missing Codex PreToolUse edit hook command")
    else:
        codex_pre_result = subprocess.run(
            ["bash", "-lc", codex_pre_command],
            cwd=root,
            input=manifest_hook_payload,
            text=True,
            capture_output=True,
            env=codex_hook_env,
        )
        if codex_pre_result.returncode != 0:
            fail(f"{rel(codex_hooks_path)} Codex PreToolUse payload simulation failed: {codex_pre_result.stderr.strip()}")
        if "GitOps-first" not in codex_pre_result.stdout:
            fail(f"{rel(codex_hooks_path)} Codex PreToolUse simulation missing GitOps warning")

        codex_docs_pre_result = subprocess.run(
            ["bash", "-lc", codex_pre_command],
            cwd=root,
            input=docs_hook_payload,
            text=True,
            capture_output=True,
            env=codex_hook_env,
        )
        if codex_docs_pre_result.returncode != 0:
            fail(f"{rel(codex_hooks_path)} Codex docs PreToolUse payload simulation failed: {codex_docs_pre_result.stderr.strip()}")
        if "documentation template enforcement" not in codex_docs_pre_result.stdout:
            fail(f"{rel(codex_hooks_path)} Codex docs PreToolUse simulation missing template enforcement warning")

    codex_post_command = hook_command(codex_hooks, "PostToolUse", "Write|Edit|MultiEdit", "post-validate.sh")
    if not codex_post_command:
        fail(f"{rel(codex_hooks_path)} missing Codex PostToolUse edit hook command")
    else:
        codex_post_result = subprocess.run(
            ["bash", "-lc", codex_post_command],
            cwd=root,
            input=manifest_hook_payload,
            text=True,
            capture_output=True,
            env=codex_hook_env,
        )
        if codex_post_result.returncode != 0:
            detail = "\n".join(
                item
                for item in [codex_post_result.stdout.strip(), codex_post_result.stderr.strip()]
                if item
            )
            fail(f"{rel(codex_hooks_path)} Codex PostToolUse payload simulation failed:\n{detail}")
        for phrase in [
            "[hook] PASS Kubernetes manifests",
            "[hook] PASS secret handling",
        ]:
            if phrase not in codex_post_result.stdout:
                fail(f"{rel(codex_hooks_path)} Codex PostToolUse simulation missing output phrase: {phrase}")

        codex_docs_post_result = subprocess.run(
            ["bash", "-lc", codex_post_command],
            cwd=root,
            input=docs_hook_payload,
            text=True,
            capture_output=True,
            env=codex_hook_env,
        )
        if codex_docs_post_result.returncode != 0:
            detail = "\n".join(
                item
                for item in [codex_docs_post_result.stdout.strip(), codex_docs_post_result.stderr.strip()]
                if item
            )
            fail(f"{rel(codex_hooks_path)} Codex docs PostToolUse payload simulation failed:\n{detail}")
        if "[hook] PASS documentation template enforcement" not in codex_docs_post_result.stdout:
            fail(f"{rel(codex_hooks_path)} Codex docs PostToolUse simulation missing template enforcement output")

    for lifecycle_event, lifecycle_matcher in [
        ("Stop", "*"),
        ("SubagentStop", "*"),
        ("PreCompact", "manual|auto"),
    ]:
        lifecycle_command = hook_command(codex_hooks, lifecycle_event, lifecycle_matcher, "lifecycle-guard.sh")
        if not lifecycle_command:
            fail(f"{rel(codex_hooks_path)} missing Codex {lifecycle_event} lifecycle hook command")
            continue
        codex_lifecycle_result = subprocess.run(
            ["bash", "-lc", lifecycle_command],
            cwd=root,
            input=json.dumps({"hook_event_name": lifecycle_event}),
            text=True,
            capture_output=True,
            env={
                **codex_hook_env,
                "HY_HOME_K8S_LIFECYCLE_GUARD_SELFTEST": "1",
                "HY_HOME_K8S_CHANGED_PATHS": ".claude/settings.json",
            },
        )
        if codex_lifecycle_result.returncode != 0:
            fail(f"{rel(codex_hooks_path)} Codex {lifecycle_event} lifecycle simulation failed: {codex_lifecycle_result.stderr.strip()}")
        if lifecycle_event == "PreCompact" and "Lifecycle guard" not in codex_lifecycle_result.stdout:
            fail(f"{rel(codex_hooks_path)} Codex PreCompact lifecycle simulation missing advisory output")

claude_agents_dir = root / ".claude/agents"
codex_agents_dir = root / ".codex/agents"
gemini_agents_dir = root / ".agents/agents"
if claude_agents_dir.is_symlink():
    fail(".claude/agents must be a real Claude-specific directory, not a symlink")
elif not claude_agents_dir.is_dir():
    fail(".claude/agents must be a real Claude-specific directory")
claude_agents = {path.stem: path for path in sorted(claude_agents_dir.glob("*.md"))}
codex_agents = {path.stem: path for path in sorted(codex_agents_dir.glob("*.toml"))}
gemini_agents = {path.stem: path for path in sorted(gemini_agents_dir.glob("*.md"))}
for stem in sorted(set(claude_agents) - set(codex_agents)):
    fail(f"missing Codex agent adapter for .claude/agents/{stem}.md")
for stem in sorted(set(codex_agents) - set(claude_agents)):
    fail(f"Codex agent adapter has no Claude peer: .codex/agents/{stem}.toml")
for stem in sorted(set(claude_agents) - set(gemini_agents)):
    fail(f"missing Gemini agent adapter for .claude/agents/{stem}.md")
for stem in sorted(set(gemini_agents) - set(claude_agents)):
    fail(f"Gemini agent adapter has no Claude peer: .agents/agents/{stem}.md")

expected_codex_agent_models = {
    "supervisor": ("gpt-5.5", "xhigh"),
    "code-reviewer": ("gpt-5.3-codex", "high"),
    "doc-writer": ("gpt-5.3-codex", "medium"),
    "gitops-reviewer": ("gpt-5.3-codex", "high"),
    "incident-responder": ("gpt-5.3-codex", "high"),
    "k8s-implementer": ("gpt-5.3-codex", "high"),
    "network-reviewer": ("gpt-5.3-codex", "high"),
    "observability-reviewer": ("gpt-5.3-codex", "high"),
    "security-auditor": ("gpt-5.3-codex", "high"),
    "wiki-curator": ("gpt-5.3-codex", "medium"),
}
expected_claude_agent_models = {
    "supervisor": "opus 4.8",
    "code-reviewer": "sonnet 4.6",
    "doc-writer": "sonnet 4.6",
    "gitops-reviewer": "sonnet 4.6",
    "incident-responder": "sonnet 4.6",
    "k8s-implementer": "sonnet 4.6",
    "network-reviewer": "sonnet 4.6",
    "observability-reviewer": "sonnet 4.6",
    "security-auditor": "sonnet 4.6",
    "wiki-curator": "sonnet 4.6",
}
expected_claude_agent_tools = {
    "supervisor": "Read, Grep, Glob, Bash, Edit, Write, Task",
    "code-reviewer": "Read, Grep, Glob, Bash",
    "doc-writer": "Read, Write, Edit, Grep, Glob, Bash",
    "gitops-reviewer": "Read, Grep, Glob, Bash",
    "incident-responder": "Read, Grep, Glob, Bash",
    "k8s-implementer": "Read, Write, Edit, Grep, Glob, Bash",
    "network-reviewer": "Read, Grep, Glob, Bash",
    "observability-reviewer": "Read, Grep, Glob, Bash",
    "security-auditor": "Read, Grep, Glob, Bash",
    "wiki-curator": "Read, Write, Edit, Grep, Glob, Bash",
}
for stem, claude_path in sorted(claude_agents.items()):
    claude_text = read_text(claude_path)
    claude_metadata = load_markdown_frontmatter(claude_path)
    if claude_metadata.get("name") != stem:
        fail(f"{rel(claude_path)} name must match file stem: {stem}")
    expected_claude_model = expected_claude_agent_models.get(stem)
    if expected_claude_model and claude_metadata.get("model") != expected_claude_model:
        fail(f"{rel(claude_path)} model must be {expected_claude_model!r}")
    expected_claude_tools = expected_claude_agent_tools.get(stem)
    if expected_claude_tools and normalize_tools(claude_metadata.get("tools")) != expected_claude_tools:
        fail(f"{rel(claude_path)} tools must be {expected_claude_tools!r}")
    codex_path = codex_agents.get(stem)
    gemini_path = gemini_agents.get(stem)
    if not codex_path:
        continue
    codex_text = read_text(codex_path)
    try:
        codex_data = load_toml(codex_path)
    except Exception as exc:
        fail(f"Codex agent TOML parse failed for {rel(codex_path)}: {exc}")
        codex_data = {}
    if codex_data.get("name") != stem:
        fail(f"{rel(codex_path)} name must match file stem: {stem}")
    expected_model_effort = expected_codex_agent_models.get(stem)
    if expected_model_effort:
        expected_model, expected_effort = expected_model_effort
        if codex_data.get("model") != expected_model:
            fail(f"{rel(codex_path)} model must be {expected_model!r}")
        if codex_data.get("model_reasoning_effort") != expected_effort:
            fail(f"{rel(codex_path)} model_reasoning_effort must be {expected_effort!r}")
    if not gemini_path:
        continue
    gemini_text = read_text(gemini_path)
    gemini_metadata = load_markdown_frontmatter(gemini_path)
    if gemini_metadata.get("name") != stem:
        fail(f"{rel(gemini_path)} name must match file stem: {stem}")
    expected_gemini_model = "Gemini 3.1 Pro" if stem == "supervisor" else "Gemini 3.5 Flash"
    if gemini_metadata.get("model") != expected_gemini_model:
        fail(f"{rel(gemini_path)} model must be {expected_gemini_model!r}")
    provider_scope_imports = {
        "claude": extract_scope_imports(claude_text),
        "codex": extract_scope_imports(codex_text),
        "gemini": extract_scope_imports(gemini_text),
    }
    if len({tuple(imports) for imports in provider_scope_imports.values()}) != 1:
        fail(
            f"scope import mismatch for role {stem}: "
            + ", ".join(
                f"{provider}={imports!r}"
                for provider, imports in sorted(provider_scope_imports.items())
            )
        )

harness_catalog_path = root / "docs/00.agent-governance/harness-catalog.md"
harness_catalog_text = read_text(harness_catalog_path)
for agent_path in sorted(claude_agents.values()):
    if rel(agent_path) not in harness_catalog_text:
        fail(f"{rel(harness_catalog_path)} missing agent inventory entry: {rel(agent_path)}")
for skill_path in sorted((root / ".claude/skills").glob("*/skill.md")):
    if rel(skill_path) not in harness_catalog_text:
        fail(f"{rel(harness_catalog_path)} missing skill inventory entry: {rel(skill_path)}")

scripts_dir = root / "scripts"
scripts_readme = read_text(scripts_dir / "README.md")
script_paths = sorted(scripts_dir.glob("*.sh"))
script_names = {script.name for script in script_paths}
disallowed_script_absolute_path_patterns = [
    re.compile(r"(?<![A-Za-z0-9_.-])/(?:home|Users|var|opt)/[A-Za-z0-9_.-]"),
    re.compile(r"\b[A-Z]:\\\\"),
]
for script in script_paths:
    script_text = read_text(script)
    if not os.access(script, os.X_OK):
        fail(f"script must be executable: {rel(script)}")
    if not script_text.startswith("#!/usr/bin/env bash\n"):
        fail(f"script must start with bash shebang: {rel(script)}")
    if script.name not in scripts_readme:
        fail(f"script missing from scripts/README.md inventory: {script.name}")
    for pattern in disallowed_script_absolute_path_patterns:
        if pattern.search(script_text):
            fail(f"{rel(script)} contains a hardcoded absolute machine path")

script_inventory_rows = markdown_table_after_heading(
    scripts_readme,
    profiled_readme_table_headings("Script Inventory"),
)
expected_script_inventory_header = ["스크립트", "결정", "보존 근거", "명령·문서 표면", "목적"]
allowed_script_decisions = {"Keep", "Delete candidate", "Consolidation candidate", "Deferred"}
if len(script_inventory_rows) < 2:
    fail("scripts/README.md Script Inventory must contain a header and script rows")
elif script_inventory_rows[0] != expected_script_inventory_header:
    fail(
        "scripts/README.md Script Inventory header must be: "
        + " | ".join(expected_script_inventory_header)
    )
else:
    indexed_scripts: dict[str, list[str]] = {}
    for row_number, row in enumerate(script_inventory_rows[1:], start=1):
        if len(row) != len(expected_script_inventory_header):
            fail(f"scripts/README.md Script Inventory row {row_number} must have {len(expected_script_inventory_header)} columns")
            continue
        match = re.fullmatch(r"`([^`]+\.sh)`", row[0])
        if not match:
            fail(f"scripts/README.md Script Inventory row {row_number} must start with a backticked script name")
            continue
        script_name = match.group(1)
        if script_name in indexed_scripts:
            fail(f"scripts/README.md Script Inventory duplicates script: {script_name}")
        indexed_scripts[script_name] = row

        decision = row[1]
        retention_evidence = row[2]
        command_surface = row[3]
        purpose = row[4]
        if decision not in allowed_script_decisions:
            fail(f"scripts/README.md Script Inventory row {row_number} has unsupported decision: {decision}")
        for label, value in [
            ("보존 근거", retention_evidence),
            ("명령·문서 표면", command_surface),
            ("목적", purpose),
        ]:
            if not value:
                fail(f"scripts/README.md Script Inventory row {row_number} has empty {label}")
        if decision == "Keep" and not ("Tier A" in retention_evidence or "Tier B" in retention_evidence):
            fail(f"scripts/README.md Script Inventory row {row_number} with Keep must cite Tier A or Tier B retention evidence")

    for script_name in sorted(script_names - set(indexed_scripts)):
        fail(f"scripts/README.md Script Inventory missing script row: {script_name}")
    for script_name in sorted(set(indexed_scripts) - script_names):
        fail(f"scripts/README.md Script Inventory references missing script: {script_name}")

script_classification_rows = markdown_table_after_heading(
    scripts_readme,
    profiled_readme_table_headings("Script Classification Matrix"),
)
expected_script_classification_header = ["스크립트", "분류", "삭제 후보", "통합 후보", "근거"]
expected_script_classifications = {
    "validate-repo-quality-gates.sh": "operations-critical/reusable",
    "validate-gitops-structure.sh": "operations-critical/reusable",
    "validate-k8s-manifests.sh": "operations-critical/reusable",
    "check-secret-handling.sh": "operations-critical/reusable",
    "generate-llm-wiki-index.sh": "development-helper/reusable",
    "render-platform-chart-kinds.sh": "development-helper/reusable",
    "validate-policy-gates.sh": "operations-critical/reusable",
}
allowed_script_classification_terms = {
    "one-off",
    "reusable",
    "operations-critical",
    "development-helper",
    "unknown",
}
if len(script_classification_rows) < 2:
    fail("scripts/README.md Script Classification Matrix must contain a header and script rows")
elif script_classification_rows[0] != expected_script_classification_header:
    fail(
        "scripts/README.md Script Classification Matrix header must be: "
        + " | ".join(expected_script_classification_header)
    )
else:
    classified_scripts: dict[str, list[str]] = {}
    for row_number, row in enumerate(script_classification_rows[1:], start=1):
        if len(row) != len(expected_script_classification_header):
            fail(
                "scripts/README.md Script Classification Matrix "
                f"row {row_number} must have {len(expected_script_classification_header)} columns"
            )
            continue
        match = re.fullmatch(r"`([^`]+\.sh)`", row[0])
        if not match:
            fail(
                "scripts/README.md Script Classification Matrix "
                f"row {row_number} must start with a backticked script name"
            )
            continue
        script_name = match.group(1)
        if script_name in classified_scripts:
            fail(f"scripts/README.md Script Classification Matrix duplicates script: {script_name}")
        classified_scripts[script_name] = row

        classification = row[1]
        deletion_candidate = row[2]
        consolidation_candidate = row[3]
        evidence = row[4]
        classification_terms = {part.strip() for part in classification.split("/") if part.strip()}
        unsupported_terms = classification_terms - allowed_script_classification_terms
        if unsupported_terms:
            fail(
                "scripts/README.md Script Classification Matrix "
                f"row {row_number} has unsupported classification term(s): {', '.join(sorted(unsupported_terms))}"
            )
        expected_classification = expected_script_classifications.get(script_name)
        if expected_classification and classification != expected_classification:
            fail(
                "scripts/README.md Script Classification Matrix "
                f"{script_name} classification must be {expected_classification}"
            )
        for label, value in [
            ("삭제 후보", deletion_candidate),
            ("통합 후보", consolidation_candidate),
            ("근거", evidence),
        ]:
            if not value:
                fail(f"scripts/README.md Script Classification Matrix row {row_number} has empty {label}")
        if deletion_candidate != "No":
            fail(f"scripts/README.md Script Classification Matrix {script_name} deletion candidate must be No")
        if consolidation_candidate != "No":
            fail(f"scripts/README.md Script Classification Matrix {script_name} consolidation candidate must be No")

    for script_name in sorted(script_names - set(classified_scripts)):
        fail(f"scripts/README.md Script Classification Matrix missing script row: {script_name}")
    for script_name in sorted(set(classified_scripts) - script_names):
        fail(f"scripts/README.md Script Classification Matrix references missing script: {script_name}")

kube_linter_config_path = root / ".kube-linter.yaml"
kube_linter_config = load_yaml(kube_linter_config_path)
expected_kube_linter_exclusions = [
    "no-read-only-root-fs",
    "no-anti-affinity",
    "unset-cpu-requirements",
    "unset-memory-requirements",
    "run-as-non-root",
    "latest-tag",
    "dangling-service",
]
kube_linter_exclusions = (
    (kube_linter_config.get("checks") or {}).get("exclude") or []
)
if kube_linter_exclusions != expected_kube_linter_exclusions:
    fail(
        ".kube-linter.yaml checks.exclude must match the documented exclusion order: "
        + ", ".join(expected_kube_linter_exclusions)
    )

kube_linter_text = read_text(kube_linter_config_path)
for exclusion in expected_kube_linter_exclusions:
    match = re.search(rf'^\s*-\s+"{re.escape(exclusion)}"\s+#\s*(.+)$', kube_linter_text, re.MULTILINE)
    if not match:
        fail(f".kube-linter.yaml exclusion must have an inline rationale comment: {exclusion}")
        continue
    rationale = match.group(1).strip()
    if len(rationale) < 12 or "TODO" in rationale or "TBD" in rationale:
        fail(f".kube-linter.yaml exclusion rationale is too weak: {exclusion}")

kube_linter_rows = markdown_table_after_heading(
    scripts_readme,
    profiled_readme_table_headings("Kube-linter Exclusion Matrix"),
)
expected_kube_linter_header = ["Excluded check", "Current rationale", "Boundary", "Follow-up"]
if len(kube_linter_rows) < 2:
    fail("scripts/README.md Kube-linter Exclusion Matrix must contain a header and exclusion rows")
elif kube_linter_rows[0] != expected_kube_linter_header:
    fail(
        "scripts/README.md Kube-linter Exclusion Matrix header must be: "
        + " | ".join(expected_kube_linter_header)
    )
else:
    indexed_kube_linter_exclusions: list[str] = []
    for row_number, row in enumerate(kube_linter_rows[1:], start=1):
        if len(row) != len(expected_kube_linter_header):
            fail(
                "scripts/README.md Kube-linter Exclusion Matrix "
                f"row {row_number} must have {len(expected_kube_linter_header)} columns"
            )
            continue
        excluded_cell, rationale, boundary, follow_up = row
        match = re.fullmatch(r"`([^`]+)`", excluded_cell)
        if not match:
            fail(
                "scripts/README.md Kube-linter Exclusion Matrix "
                f"row {row_number} must start with a backticked excluded check"
            )
            continue
        exclusion = match.group(1)
        indexed_kube_linter_exclusions.append(exclusion)
        for label, value in [
            ("Current rationale", rationale),
            ("Boundary", boundary),
            ("Follow-up", follow_up),
        ]:
            if not value:
                fail(f"scripts/README.md Kube-linter Exclusion Matrix row {row_number} has empty {label}")
        if ".kube-linter.yaml" not in boundary:
            fail(
                "scripts/README.md Kube-linter Exclusion Matrix "
                f"row {row_number} must cite .kube-linter.yaml in Boundary"
            )
        if "Revisit" not in follow_up:
            fail(
                "scripts/README.md Kube-linter Exclusion Matrix "
                f"row {row_number} must include a Revisit follow-up"
            )
        if exclusion == "latest-tag":
            for phrase in ["active GitOps image tag policy", "validate-repo-quality-gates.sh"]:
                if phrase not in boundary:
                    fail(
                        "scripts/README.md latest-tag kube-linter row "
                        f"must cite the repo-quality image policy boundary: {phrase}"
                    )
        if exclusion == "dangling-service" and "Argo Rollouts" not in rationale:
            fail("scripts/README.md dangling-service kube-linter row must cite Argo Rollouts")
    if indexed_kube_linter_exclusions != expected_kube_linter_exclusions:
        fail(
            "scripts/README.md Kube-linter Exclusion Matrix row order must match .kube-linter.yaml: "
            + ", ".join(expected_kube_linter_exclusions)
        )

gitops_dir = root / "gitops"
gitops_readme_path = gitops_dir / "README.md"
gitops_readme = read_text(gitops_readme_path)
expected_gitops_service_header = [
    "Area",
    "Purpose and owner",
    "Lifecycle and config",
    "Dependencies, routes, secrets",
    "Validation and operations",
]
expected_gitops_service_areas = (
    ["clusters/local", "apps/root"]
    + [f"platform/{path.name}" for path in sorted((gitops_dir / "platform").iterdir()) if path.is_dir()]
    + [f"workloads/{path.name}" for path in sorted((gitops_dir / "workloads").iterdir()) if path.is_dir()]
)
gitops_service_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("Service Coverage Matrix"),
)
if len(gitops_service_rows) < 2:
    fail("gitops/README.md Service Coverage Matrix must contain a header and service rows")
elif gitops_service_rows[0] != expected_gitops_service_header:
    fail(
        "gitops/README.md Service Coverage Matrix header must be: "
        + " | ".join(expected_gitops_service_header)
    )
else:
    indexed_gitops_areas: list[str] = []
    seen_gitops_areas: set[str] = set()
    for row_number, row in enumerate(gitops_service_rows[1:], start=1):
        if len(row) != len(expected_gitops_service_header):
            fail(
                "gitops/README.md Service Coverage Matrix "
                f"row {row_number} must have {len(expected_gitops_service_header)} columns"
            )
            continue
        area_cell, purpose, lifecycle, dependencies, validation = row
        match = re.fullmatch(r"`([^`]+)`", area_cell)
        if not match:
            fail(
                "gitops/README.md Service Coverage Matrix "
                f"row {row_number} must start with a backticked area path"
            )
            continue
        area = match.group(1)
        if area in seen_gitops_areas:
            fail(f"gitops/README.md Service Coverage Matrix duplicates area: {area}")
        seen_gitops_areas.add(area)
        indexed_gitops_areas.append(area)
        area_path = gitops_dir / area
        if not area_path.is_dir():
            fail(f"gitops/README.md Service Coverage Matrix references missing directory: gitops/{area}")
        for label, value in [
            ("Purpose and owner", purpose),
            ("Lifecycle and config", lifecycle),
            ("Dependencies, routes, secrets", dependencies),
            ("Validation and operations", validation),
        ]:
            if not value:
                fail(f"gitops/README.md Service Coverage Matrix row {row_number} has empty {label}")
        if "owned by" not in purpose:
            fail(f"gitops/README.md Service Coverage Matrix row {row_number} must name ownership")
        if not any(marker in validation for marker in ["`bash ", "Validate", "validate-", "verify-"]):
            fail(f"gitops/README.md Service Coverage Matrix row {row_number} must cite a validation command")
    if indexed_gitops_areas != expected_gitops_service_areas:
        fail(
            "gitops/README.md Service Coverage Matrix area order must match actual GitOps directories: "
            + ", ".join(expected_gitops_service_areas)
        )

expected_external_contract_header = [
    "Contract",
    "Host / service",
    "Port",
    "Database or Vault path",
    "Secret keys",
    "TLS / CA",
    "Rotation responsibility",
    "Namespace convention",
    "Validation",
]
expected_external_contracts = [
    "Vault API",
    "PostgreSQL write",
    "PostgreSQL read",
    "Valkey auth",
]
external_contract_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("External Service Contract Matrix"),
)
if len(external_contract_rows) < 2:
    fail("gitops/README.md External Service Contract Matrix must contain a header and contract rows")
elif external_contract_rows[0] != expected_external_contract_header:
    fail(
        "gitops/README.md External Service Contract Matrix header must be: "
        + " | ".join(expected_external_contract_header)
    )
else:
    indexed_external_contracts: list[str] = []
    for row_number, row in enumerate(external_contract_rows[1:], start=1):
        if len(row) != len(expected_external_contract_header):
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must have {len(expected_external_contract_header)} columns"
            )
            continue
        contract_cell, host, port, database_or_path, secret_keys, tls_ca, rotation, namespace, validation = row
        match = re.fullmatch(r"`([^`]+)`", contract_cell)
        if not match:
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must start with a backticked contract name"
            )
            continue
        contract = match.group(1)
        indexed_external_contracts.append(contract)
        for label, value in [
            ("Host / service", host),
            ("Port", port),
            ("Database or Vault path", database_or_path),
            ("Secret keys", secret_keys),
            ("TLS / CA", tls_ca),
            ("Rotation responsibility", rotation),
            ("Namespace convention", namespace),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"gitops/README.md External Service Contract Matrix row {row_number} has empty {label}")
        if "verify-contracts-static.sh" not in validation:
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must cite infrastructure/tests/verify-contracts-static.sh"
            )
        if "platform" not in namespace:
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must cite the platform namespace convention"
            )
        if "operator" not in rotation and "owner" not in rotation:
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must name the rotation owner"
            )
        if "TLS" not in tls_ca or "CA" not in tls_ca:
            fail(
                "gitops/README.md External Service Contract Matrix "
                f"row {row_number} must explicitly cover TLS/CA responsibility"
            )
        if contract == "Vault API":
            for phrase, value in [
                ("vault-external.platform.svc.cluster.local", host),
                ("172.18.0.8", host),
                ("8200", port),
                ("ClusterSecretStore", database_or_path),
                ("platform/argocd", database_or_path),
                ("platform/postgres-app", database_or_path),
                ("platform/notifications", database_or_path),
                ("eso-read-platform", secret_keys),
                ("http://", tls_ca),
                ("external-secrets", namespace),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md Vault API contract row missing phrase: {phrase}")
        elif contract == "PostgreSQL write":
            for phrase, value in [
                ("postgres-write-external.platform.svc.cluster.local", host),
                ("172.18.0.15", host),
                ("15432", port),
                ("db_name", database_or_path),
                ("platform/postgres-app", database_or_path),
                ("postgres-app-secret", secret_keys),
                ("username", secret_keys),
                ("password", secret_keys),
                ("external PostgreSQL service workspace", tls_ca),
                ("ESO refreshes", rotation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md PostgreSQL write contract row missing phrase: {phrase}")
        elif contract == "PostgreSQL read":
            for phrase, value in [
                ("postgres-read-external.platform.svc.cluster.local", host),
                ("172.18.0.15", host),
                ("15433", port),
                ("db_name", database_or_path),
                ("postgres-app-secret", secret_keys),
                ("read/write split", namespace),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md PostgreSQL read contract row missing phrase: {phrase}")
        elif contract == "Valkey auth":
            for phrase, value in [
                ("valkey-external.platform.svc.cluster.local", host),
                ("172.18.0.9", host),
                ("6379", port),
                ("platform/argocd", database_or_path),
                ("valkey_password", database_or_path),
                ("argocd-external-valkey", secret_keys),
                ("redis-password", secret_keys),
                ("external Valkey service workspace", tls_ca),
                ("argocd", namespace),
                ("verify-secrets.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md Valkey contract row missing phrase: {phrase}")
    if indexed_external_contracts != expected_external_contracts:
        fail(
            "gitops/README.md External Service Contract Matrix row order must be: "
            + ", ".join(expected_external_contracts)
        )

expected_secret_responsibility_header = [
    "Responsibility",
    "Source / auth contract",
    "Destination / naming rule",
    "Owner boundary",
    "Value handling",
    "Validation",
]
expected_secret_responsibilities = [
    "ClusterSecretStore vault-backend",
    "Platform postgres-app-secret",
    "ArgoCD argocd-external-valkey",
    "ArgoCD argocd-notifications-secret",
    "Sample app ExternalSecret",
]
secret_responsibility_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("Secret Management Responsibility Matrix"),
)
if len(secret_responsibility_rows) < 2:
    fail("gitops/README.md Secret Management Responsibility Matrix must contain a header and responsibility rows")
elif secret_responsibility_rows[0] != expected_secret_responsibility_header:
    fail(
        "gitops/README.md Secret Management Responsibility Matrix header must be: "
        + " | ".join(expected_secret_responsibility_header)
    )
else:
    indexed_secret_responsibilities: list[str] = []
    for row_number, row in enumerate(secret_responsibility_rows[1:], start=1):
        if len(row) != len(expected_secret_responsibility_header):
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must have {len(expected_secret_responsibility_header)} columns"
            )
            continue
        responsibility_cell, source, destination, owner, value_handling, validation = row
        match = re.fullmatch(r"`([^`]+)`", responsibility_cell)
        if not match:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must start with a backticked responsibility name"
            )
            continue
        responsibility = match.group(1)
        indexed_secret_responsibilities.append(responsibility)
        for label, value in [
            ("Source / auth contract", source),
            ("Destination / naming rule", destination),
            ("Owner boundary", owner),
            ("Value handling", value_handling),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"gitops/README.md Secret Management Responsibility Matrix row {row_number} has empty {label}")
        if "Vault" not in source or "vault-backend" not in source:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must cite Vault and vault-backend"
            )
        if "Secret" not in destination and "secret" not in destination:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must cite a Kubernetes secret naming rule"
            )
        if "owner" not in owner and "owns" not in owner:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must name ownership"
            )
        if "outside Git" not in value_handling and "value-free" not in value_handling:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must keep secret values outside Git"
            )
        if "check-secret-handling.sh" not in validation:
            fail(
                "gitops/README.md Secret Management Responsibility Matrix "
                f"row {row_number} must cite scripts/check-secret-handling.sh"
            )
        if responsibility == "ClusterSecretStore vault-backend":
            for phrase, value in [
                ("External Secrets Operator", source),
                ("eso-read-platform", source),
                ("kubernetes", source),
                ("secret", source),
                ("external-secrets", destination),
                ("external Vault operator", owner),
                ("reviewer JWT", value_handling),
                ("verify-contracts-static.sh", validation),
                ("verify-secrets.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md ClusterSecretStore responsibility row missing phrase: {phrase}")
        elif responsibility == "Platform postgres-app-secret":
            for phrase, value in [
                ("ExternalSecret", source),
                ("platform/postgres-app", source),
                ("db_name", source),
                ("username", source),
                ("password", source),
                ("postgres-app-secret", destination),
                ("platform", destination),
                ("creationPolicy: Owner", destination),
                ("external PostgreSQL owner", owner),
                ("ESO refresh", value_handling),
                ("verify-contracts-static.sh", validation),
                ("verify-secrets.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md postgres secret responsibility row missing phrase: {phrase}")
        elif responsibility == "ArgoCD argocd-external-valkey":
            for phrase, value in [
                ("ExternalSecret", source),
                ("platform/argocd", source),
                ("valkey_password", source),
                ("argocd-external-valkey", destination),
                ("argocd", destination),
                ("redis-password", destination),
                ("external Valkey owner", owner),
                ("ESO refresh", value_handling),
                ("verify-secrets.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md Valkey secret responsibility row missing phrase: {phrase}")
        elif responsibility == "ArgoCD argocd-notifications-secret":
            for phrase, value in [
                ("ExternalSecret", source),
                ("platform/notifications", source),
                ("slack_token", source),
                ("argocd-notifications-secret", destination),
                ("argocd", destination),
                ("slack-token", destination),
                ("notification token owner", owner),
                ("must not appear", value_handling),
                ("verify-secrets.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md notifications secret responsibility row missing phrase: {phrase}")
        elif responsibility == "Sample app ExternalSecret":
            for phrase, value in [
                ("apps/<appname>/config", source),
                ("<appname>-secret", destination),
                ("apps", destination),
                ("db_password", destination),
                ("api_key", destination),
                ("App operator", owner),
                ("Vault policy", owner),
                ("value-free", value_handling),
                ("examples/sample-app/kustomization.yaml", value_handling),
                ("validate-k8s-manifests.sh", validation),
            ]:
                if phrase not in value:
                    fail(f"gitops/README.md sample app secret responsibility row missing phrase: {phrase}")
    if indexed_secret_responsibilities != expected_secret_responsibilities:
        fail(
            "gitops/README.md Secret Management Responsibility Matrix row order must be: "
            + ", ".join(expected_secret_responsibilities)
        )

workloads_readme_path = gitops_dir / "workloads/README.md"
workloads_readme = read_text(workloads_readme_path)
for phrase in [
    "examples/sample-app",
    "gitops/workloads/<appname>",
    "active GitOps desired state",
    "check-secret-handling.sh",
]:
    if phrase not in workloads_readme:
        fail(f"gitops/workloads/README.md missing onboarding activation phrase: {phrase}")
expected_workload_header = [
    "Workload",
    "Purpose and owner",
    "Lifecycle and config",
    "Dependencies, routes, secrets",
    "Validation and operations",
]
expected_workloads = [
    path.name for path in sorted((gitops_dir / "workloads").iterdir()) if path.is_dir()
]
workload_rows = markdown_table_after_heading(
    workloads_readme,
    profiled_readme_table_headings("Workload Coverage Matrix"),
)
if len(workload_rows) < 2:
    fail("gitops/workloads/README.md Workload Coverage Matrix must contain a header and workload rows")
elif workload_rows[0] != expected_workload_header:
    fail(
        "gitops/workloads/README.md Workload Coverage Matrix header must be: "
        + " | ".join(expected_workload_header)
    )
else:
    indexed_workloads: list[str] = []
    seen_workloads: set[str] = set()
    for row_number, row in enumerate(workload_rows[1:], start=1):
        if len(row) != len(expected_workload_header):
            fail(
                "gitops/workloads/README.md Workload Coverage Matrix "
                f"row {row_number} must have {len(expected_workload_header)} columns"
            )
            continue
        workload_cell, purpose, lifecycle, dependencies, validation = row
        match = re.fullmatch(r"`([^`]+)`", workload_cell)
        if not match:
            fail(
                "gitops/workloads/README.md Workload Coverage Matrix "
                f"row {row_number} must start with a backticked workload directory"
            )
            continue
        workload = match.group(1)
        if workload in seen_workloads:
            fail(f"gitops/workloads/README.md Workload Coverage Matrix duplicates workload: {workload}")
        seen_workloads.add(workload)
        indexed_workloads.append(workload)
        if not (gitops_dir / "workloads" / workload).is_dir():
            fail(f"gitops/workloads/README.md Workload Coverage Matrix references missing workload: {workload}")
        for label, value in [
            ("Purpose and owner", purpose),
            ("Lifecycle and config", lifecycle),
            ("Dependencies, routes, secrets", dependencies),
            ("Validation and operations", validation),
        ]:
            if not value:
                fail(f"gitops/workloads/README.md Workload Coverage Matrix row {row_number} has empty {label}")
        for command in [
            "scripts/validate-gitops-structure.sh",
            "scripts/validate-k8s-manifests.sh",
            "scripts/check-secret-handling.sh",
        ]:
            if command not in validation:
                fail(
                    "gitops/workloads/README.md Workload Coverage Matrix "
                    f"row {row_number} must cite {command}"
                )
    if indexed_workloads != expected_workloads:
        fail(
            "gitops/workloads/README.md Workload Coverage Matrix row order must match actual workloads: "
            + ", ".join(expected_workloads)
        )


def gitops_yaml_documents_under(scope: pathlib.Path) -> list[tuple[pathlib.Path, dict]]:
    documents: list[tuple[pathlib.Path, dict]] = []
    yaml_paths = sorted(scope.rglob("*.yaml")) + sorted(scope.rglob("*.yml"))
    for path in yaml_paths:
        for document in load_yaml_documents(path):
            if isinstance(document, dict):
                documents.append((path, document))
    return documents


def collect_container_images(value) -> list[str]:
    images: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"containers", "initContainers", "ephemeralContainers"} and isinstance(item, list):
                for container in item:
                    if isinstance(container, dict) and "image" in container:
                        image = container.get("image")
                        images.append(image if isinstance(image, str) else "")
            images.extend(collect_container_images(item))
    elif isinstance(value, list):
        for item in value:
            images.extend(collect_container_images(item))
    return images


def image_has_explicit_version(image: str) -> bool:
    if "@sha256:" in image:
        return True
    last_segment = image.rsplit("/", 1)[-1]
    return ":" in last_segment and not last_segment.endswith(":")


def image_uses_latest(image: str) -> bool:
    last_segment = image.rsplit("/", 1)[-1]
    tag_segment = last_segment.split("@", 1)[0]
    return tag_segment.endswith(":latest")


def collect_container_image_entries(scope: pathlib.Path) -> list[tuple[pathlib.Path, str]]:
    entries: list[tuple[pathlib.Path, str]] = []
    for path, document in gitops_yaml_documents_under(scope):
        if path.name == "kustomization.yaml":
            continue
        for image in collect_container_images(document):
            entries.append((path, image))
    return entries


workload_image_entries = collect_container_image_entries(gitops_dir / "workloads")
platform_image_entries = collect_container_image_entries(gitops_dir / "platform")
for scope_name, entries in [
    ("gitops/workloads", workload_image_entries),
    ("gitops/platform", platform_image_entries),
]:
    if scope_name == "gitops/workloads" and not entries:
        fail("active gitops/workloads container image scan found no images")
    for path, image in entries:
        if not image:
            fail(f"{rel(path)} contains a container image field that is not a nonempty string")
            continue
        if image_uses_latest(image):
            fail(f"{rel(path)} must not use latest container image tag: {image}")
        if not image_has_explicit_version(image):
            fail(f"{rel(path)} container image must use an explicit tag or sha256 digest: {image}")

workload_manifest_kinds: set[str] = set()
for path, document in gitops_yaml_documents_under(gitops_dir / "workloads"):
    if path.name == "kustomization.yaml":
        continue
    kind = document.get("kind")
    if isinstance(kind, str) and kind:
        workload_manifest_kinds.add(kind)

apps_project_path = gitops_dir / "clusters/local/appproject-apps.yaml"
apps_project = load_yaml(apps_project_path)
apps_cluster_kind_whitelist = {
    item.get("kind")
    for item in apps_project.get("spec", {}).get("clusterResourceWhitelist", [])
    if isinstance(item, dict) and isinstance(item.get("kind"), str)
}
apps_namespace_kind_whitelist = {
    item.get("kind")
    for item in apps_project.get("spec", {}).get("namespaceResourceWhitelist", [])
    if isinstance(item, dict) and isinstance(item.get("kind"), str)
}
if apps_cluster_kind_whitelist:
    fail("gitops/clusters/local/appproject-apps.yaml clusterResourceWhitelist must be empty")
if not apps_namespace_kind_whitelist:
    fail("gitops/clusters/local/appproject-apps.yaml namespaceResourceWhitelist must not be empty")
for kind in sorted(workload_manifest_kinds - apps_namespace_kind_whitelist):
    fail(f"gitops/workloads manifest kind is not allowed by apps AppProject namespaceResourceWhitelist: {kind}")

policy_apps_namespace_kinds = {"ExternalSecret"}
expected_apps_namespace_kind_whitelist = workload_manifest_kinds | policy_apps_namespace_kinds
if apps_namespace_kind_whitelist != expected_apps_namespace_kind_whitelist:
    fail(
        "gitops/clusters/local/appproject-apps.yaml namespaceResourceWhitelist must equal "
        "active workload kinds plus policy-optional ExternalSecret: "
        + ", ".join(sorted(expected_apps_namespace_kind_whitelist))
    )
expected_allowlist_header = [
    "Project",
    "Allow-list surface",
    "Current allowed kinds",
    "Evidence class",
    "Tightening boundary",
    "Validation",
]
expected_allowlist_surfaces = [
    "apps|clusterResourceWhitelist",
    "apps|active namespaceResourceWhitelist",
    "apps|policy namespaceResourceWhitelist",
    "platform|platform AppProject allow-lists",
]
allowlist_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("AppProject Allow-list Rationale Matrix"),
)
if len(allowlist_rows) < 2:
    fail("gitops/README.md AppProject Allow-list Rationale Matrix must contain a header and allow-list rows")
elif allowlist_rows[0] != expected_allowlist_header:
    fail(
        "gitops/README.md AppProject Allow-list Rationale Matrix header must be: "
        + " | ".join(expected_allowlist_header)
    )
else:
    indexed_allowlist_surfaces: list[str] = []
    for row_number, row in enumerate(allowlist_rows[1:], start=1):
        if len(row) != len(expected_allowlist_header):
            fail(
                "gitops/README.md AppProject Allow-list Rationale Matrix "
                f"row {row_number} must have {len(expected_allowlist_header)} columns"
            )
            continue
        project_cell, surface_cell, kinds_cell, evidence, boundary, validation = row
        project_match = re.fullmatch(r"`([^`]+)`", project_cell)
        surface_match = re.search(r"`([^`]+)`", surface_cell)
        if not project_match or not surface_match:
            fail(
                "gitops/README.md AppProject Allow-list Rationale Matrix "
                f"row {row_number} must start with backticked project and surface"
            )
            continue
        project = project_match.group(1)
        surface = surface_match.group(1)
        surface_key = f"{project}|{surface}"
        indexed_allowlist_surfaces.append(surface_key)
        for label, value in [
            ("Evidence class", evidence),
            ("Tightening boundary", boundary),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"gitops/README.md AppProject Allow-list Rationale Matrix row {row_number} has empty {label}")
        if "scripts/validate-repo-quality-gates.sh" not in validation:
            fail(
                "gitops/README.md AppProject Allow-list Rationale Matrix "
                f"row {row_number} must cite scripts/validate-repo-quality-gates.sh"
            )
        documented_kinds = set(re.findall(r"`([^`]+)`", kinds_cell))
        if surface_key == "apps|clusterResourceWhitelist":
            if documented_kinds:
                fail("gitops/README.md apps clusterResourceWhitelist rationale row must document no kinds")
            for phrase in [
                "Workloads own no cluster-scoped resources",
                "app-owned cluster resource design",
                "live reconciliation impact review",
            ]:
                if phrase not in evidence + " " + boundary:
                    fail(f"gitops/README.md apps cluster allow-list row missing phrase: {phrase}")
        elif surface_key == "apps|active namespaceResourceWhitelist":
            if documented_kinds != workload_manifest_kinds:
                fail(
                    "gitops/README.md active apps namespaceResourceWhitelist rationale row must match active workload kinds: "
                    + ", ".join(sorted(workload_manifest_kinds))
                )
            if "gitops/workloads/adminer" not in evidence:
                fail("gitops/README.md active apps allow-list row must cite gitops/workloads/adminer")
        elif surface_key == "apps|policy namespaceResourceWhitelist":
            if documented_kinds != policy_apps_namespace_kinds:
                fail(
                    "gitops/README.md policy apps namespaceResourceWhitelist rationale row must match policy kinds: "
                    + ", ".join(sorted(policy_apps_namespace_kinds))
                )
            for phrase in ["0007-app-gitops-onboarding-policy.md", "ESO", "app onboarding policy"]:
                if phrase not in evidence + " " + boundary:
                    fail(f"gitops/README.md policy apps allow-list row missing phrase: {phrase}")
        elif surface_key == "platform|platform AppProject allow-lists":
            for phrase in ["Helm charts", "raw manifest scan", "chart render review", "ArgoCD sync impact review"]:
                if phrase not in evidence + " " + boundary:
                    fail(f"gitops/README.md platform allow-list row missing phrase: {phrase}")
        else:
            fail(f"gitops/README.md AppProject Allow-list Rationale Matrix unexpected row: {surface_key}")
    if indexed_allowlist_surfaces != expected_allowlist_surfaces:
        fail(
            "gitops/README.md AppProject Allow-list Rationale Matrix row order must be: "
            + ", ".join(expected_allowlist_surfaces)
        )

expected_workload_policy_header = [
    "Surface",
    "Current image policy",
    "Resource-kind policy",
    "Current evidence",
    "Deferred boundary",
    "Validation",
]
expected_workload_policy_surfaces = [
    "gitops/workloads/*",
    "gitops/platform/*",
    "examples/sample-app/*",
]
workload_policy_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("Workload Image and Kind Policy Matrix"),
)
if len(workload_policy_rows) < 2:
    fail("gitops/README.md Workload Image and Kind Policy Matrix must contain a header and policy rows")
elif workload_policy_rows[0] != expected_workload_policy_header:
    fail(
        "gitops/README.md Workload Image and Kind Policy Matrix header must be: "
        + " | ".join(expected_workload_policy_header)
    )
else:
    indexed_policy_surfaces: list[str] = []
    for row_number, row in enumerate(workload_policy_rows[1:], start=1):
        if len(row) != len(expected_workload_policy_header):
            fail(
                "gitops/README.md Workload Image and Kind Policy Matrix "
                f"row {row_number} must have {len(expected_workload_policy_header)} columns"
            )
            continue
        surface_cell, image_policy, kind_policy, evidence, deferred_boundary, validation = row
        match = re.fullmatch(r"`([^`]+)`", surface_cell)
        if not match:
            fail(
                "gitops/README.md Workload Image and Kind Policy Matrix "
                f"row {row_number} must start with a backticked surface"
            )
            continue
        surface = match.group(1)
        indexed_policy_surfaces.append(surface)
        for label, value in [
            ("Current image policy", image_policy),
            ("Resource-kind policy", kind_policy),
            ("Current evidence", evidence),
            ("Deferred boundary", deferred_boundary),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"gitops/README.md Workload Image and Kind Policy Matrix row {row_number} has empty {label}")
        if "validate-repo-quality-gates.sh" not in validation:
            fail(
                "gitops/README.md Workload Image and Kind Policy Matrix "
                f"row {row_number} must cite scripts/validate-repo-quality-gates.sh"
            )
        if surface == "gitops/workloads/*":
            if "non-latest" not in image_policy or "tag or digest" not in image_policy:
                fail("gitops/README.md workload policy row must require explicit non-latest tag or digest")
            if "AppProject" not in kind_policy or "namespaceResourceWhitelist" not in kind_policy:
                fail("gitops/README.md workload policy row must cite apps AppProject namespaceResourceWhitelist")
            for image in sorted({image for _, image in workload_image_entries}):
                if image not in evidence:
                    fail(f"gitops/README.md workload policy row missing active image evidence: {image}")
            for kind in sorted(workload_manifest_kinds):
                if kind not in evidence:
                    fail(f"gitops/README.md workload policy row missing active kind evidence: {kind}")
            for phrase in ["app onboarding policy decision", "AppProject"]:
                if phrase not in deferred_boundary:
                    fail(f"gitops/README.md workload policy row deferred boundary missing phrase: {phrase}")
        elif surface == "gitops/platform/*":
            if "non-latest" not in image_policy or "tag or digest" not in image_policy:
                fail("gitops/README.md platform policy row must require explicit non-latest tag or digest")
            if "platform AppProject" not in kind_policy:
                fail("gitops/README.md platform policy row must cite platform AppProject")
            for image in sorted({image for _, image in platform_image_entries}):
                if image not in evidence:
                    fail(f"gitops/README.md platform policy row missing platform image evidence: {image}")
            if "AppProject permissions" not in deferred_boundary:
                fail("gitops/README.md platform policy row must defer AppProject permission changes")
        elif surface == "examples/sample-app/*":
            if "placeholder" not in image_policy or "ghcr.io/<owner>/<appname>:<tag>" not in evidence:
                fail("gitops/README.md sample policy row must document the placeholder image boundary")
            if "not active desired state" not in kind_policy:
                fail("gitops/README.md sample policy row must say examples are not active desired state")
            if "gitops/workloads/<appname>" not in deferred_boundary:
                fail("gitops/README.md sample policy row must require replacement before workload copy")
        else:
            fail(f"gitops/README.md Workload Image and Kind Policy Matrix unexpected surface: {surface}")
    if indexed_policy_surfaces != expected_workload_policy_surfaces:
        fail(
            "gitops/README.md Workload Image and Kind Policy Matrix row order must be: "
            + ", ".join(expected_workload_policy_surfaces)
        )


def has_sync_option(spec: dict, option: str) -> bool:
    sync_options = ((spec.get("syncPolicy") or {}).get("syncOptions")) or []
    return option in sync_options


create_namespace_applications: list[tuple[pathlib.Path, str, str]] = []
create_namespace_application_sets: list[tuple[pathlib.Path, str, str]] = []
for path, document in gitops_yaml_documents_under(gitops_dir):
    kind = document.get("kind")
    metadata = document.get("metadata") or {}
    name = metadata.get("name")
    if not isinstance(name, str) or not name:
        continue
    if kind == "Application":
        spec = document.get("spec") or {}
        destination = spec.get("destination") or {}
        namespace = destination.get("namespace")
        if has_sync_option(spec, "CreateNamespace=true"):
            create_namespace_applications.append((path, name, namespace if isinstance(namespace, str) else ""))
    elif kind == "ApplicationSet":
        template_spec = (((document.get("spec") or {}).get("template") or {}).get("spec")) or {}
        destination = template_spec.get("destination") or {}
        namespace = destination.get("namespace")
        if has_sync_option(template_spec, "CreateNamespace=true"):
            create_namespace_application_sets.append((path, name, namespace if isinstance(namespace, str) else ""))

namespace_manifest_files: dict[str, str] = {}
for path, document in gitops_yaml_documents_under(gitops_dir / "platform/namespaces"):
    if document.get("kind") == "Namespace":
        namespace_name = (document.get("metadata") or {}).get("name")
        if isinstance(namespace_name, str) and namespace_name:
            namespace_manifest_files[namespace_name] = rel(path)

if create_namespace_applications or create_namespace_application_sets:
    for _, name, namespace in create_namespace_applications + create_namespace_application_sets:
        fail(f"GitOps Application/ApplicationSet must not use CreateNamespace=true: {name} -> {namespace}")

root_namespace_entries: list[tuple[str, str]] = []
apps_namespace_entries: list[tuple[str, str]] = []
platform_namespace_entries: list[tuple[str, str]] = []
for path, document in gitops_yaml_documents_under(gitops_dir):
    kind = document.get("kind")
    metadata = document.get("metadata") or {}
    name = metadata.get("name")
    if not isinstance(name, str) or not name:
        continue
    if kind == "Application":
        spec = document.get("spec") or {}
        destination = spec.get("destination") or {}
        namespace = destination.get("namespace")
        if not isinstance(namespace, str) or not namespace:
            continue
        if rel(path) == "gitops/clusters/local/root-application.yaml":
            root_namespace_entries.append((name, namespace))
        elif rel(path).startswith("gitops/apps/root/") and namespace != "argocd":
            platform_namespace_entries.append((name, namespace))
    elif kind == "ApplicationSet":
        template_spec = (((document.get("spec") or {}).get("template") or {}).get("spec")) or {}
        destination = template_spec.get("destination") or {}
        namespace = destination.get("namespace")
        if rel(path) == "gitops/clusters/local/applicationset-apps.yaml" and isinstance(namespace, str) and namespace:
            apps_namespace_entries.append((name, namespace))

root_namespace_entries = sorted(root_namespace_entries)
apps_namespace_entries = sorted(apps_namespace_entries)
platform_namespace_entries = sorted(platform_namespace_entries)

if root_namespace_entries != [("root-platform", "argocd")]:
    fail("gitops root Application namespace surface must be root-platform -> argocd")
if apps_namespace_entries != [("apps-generator", "apps")]:
    fail("gitops apps ApplicationSet namespace surface must be apps-generator -> apps")
if not platform_namespace_entries:
    fail("gitops platform root Applications must have inventoried namespace surfaces")

for name, namespace in apps_namespace_entries + platform_namespace_entries:
    if namespace not in namespace_manifest_files:
        fail(
            f"GitOps destination {name} -> {namespace} must have a "
            "gitops/platform/namespaces Namespace manifest"
        )

expected_namespace_ownership_header = [
    "Surface",
    "Namespace surface",
    "Declared namespace owner",
    "Current behavior",
    "Remaining boundary",
    "Validation",
]
expected_namespace_ownership_surfaces = [
    "root Application",
    "apps ApplicationSet",
    "platform root Applications",
]
namespace_ownership_rows = markdown_table_after_heading(
    gitops_readme,
    profiled_readme_table_headings("Namespace Ownership Matrix"),
)
if len(namespace_ownership_rows) < 2:
    fail("gitops/README.md Namespace Ownership Matrix must contain a header and ownership rows")
elif namespace_ownership_rows[0] != expected_namespace_ownership_header:
    fail(
        "gitops/README.md Namespace Ownership Matrix header must be: "
        + " | ".join(expected_namespace_ownership_header)
    )
else:
    indexed_namespace_surfaces: list[str] = []
    expected_pairs = {
        "root Application": root_namespace_entries,
        "apps ApplicationSet": apps_namespace_entries,
        "platform root Applications": platform_namespace_entries,
    }
    for row_number, row in enumerate(namespace_ownership_rows[1:], start=1):
        if len(row) != len(expected_namespace_ownership_header):
            fail(
                "gitops/README.md Namespace Ownership Matrix "
                f"row {row_number} must have {len(expected_namespace_ownership_header)} columns"
            )
            continue
        surface_cell, namespace_surface, owner, behavior, deferred_boundary, validation = row
        match = re.fullmatch(r"`([^`]+)`", surface_cell)
        if not match:
            fail(
                "gitops/README.md Namespace Ownership Matrix "
                f"row {row_number} must start with a backticked surface"
            )
            continue
        surface = match.group(1)
        indexed_namespace_surfaces.append(surface)
        for label, value in [
            ("Namespace surface", namespace_surface),
            ("Declared namespace owner", owner),
            ("Current behavior", behavior),
            ("Remaining boundary", deferred_boundary),
            ("Validation", validation),
        ]:
            if not value:
                fail(f"gitops/README.md Namespace Ownership Matrix row {row_number} has empty {label}")
        for command in [
            "scripts/validate-repo-quality-gates.sh",
            "scripts/validate-gitops-structure.sh",
        ]:
            if command not in validation:
                fail(
                    "gitops/README.md Namespace Ownership Matrix "
                    f"row {row_number} must cite {command}"
                )
        for name, namespace in expected_pairs.get(surface, []):
            pair = f"{name} -> {namespace}"
            if pair not in namespace_surface:
                fail(f"gitops/README.md Namespace Ownership Matrix {surface} row missing pair: {pair}")
        if surface == "root Application":
            for phrase in ["bootstrap/ArgoCD installation boundary", "not by `gitops/platform/namespaces`"]:
                if phrase not in owner:
                    fail(f"gitops/README.md root namespace ownership row missing phrase: {phrase}")
            for phrase in ["no longer uses `CreateNamespace=true`", "bootstrap must create `argocd`"]:
                if phrase not in behavior:
                    fail(f"gitops/README.md root namespace ownership row missing behavior phrase: {phrase}")
            if "bootstrap/ArgoCD install ownership pass" not in deferred_boundary:
                fail("gitops/README.md root namespace ownership row must retain bootstrap/ArgoCD install ownership boundary")
        elif surface == "apps ApplicationSet":
            namespace_file = namespace_manifest_files.get("apps", "")
            if namespace_file not in owner:
                fail(f"gitops/README.md apps namespace ownership row missing owner file: {namespace_file}")
            for phrase in ["no longer uses `CreateNamespace=true`", "`platform/namespaces` is the Git SSoT"]:
                if phrase not in behavior:
                    fail(f"gitops/README.md apps namespace ownership row missing behavior phrase: {phrase}")
            if "namespace owner manifests before onboarding" not in deferred_boundary:
                fail("gitops/README.md apps namespace ownership row must require namespace owner manifests before onboarding")
        elif surface == "platform root Applications":
            for _, namespace in platform_namespace_entries:
                namespace_file = namespace_manifest_files.get(namespace, "")
                if namespace_file not in owner:
                    fail(f"gitops/README.md platform namespace ownership row missing owner file: {namespace_file}")
            for phrase in ["no longer use `CreateNamespace=true`", "namespace manifests remain the Git SSoT"]:
                if phrase not in behavior:
                    fail(f"gitops/README.md platform namespace ownership row missing behavior phrase: {phrase}")
            if "platform AppProject destinations first" not in deferred_boundary:
                fail("gitops/README.md platform namespace ownership row must require platform AppProject destinations first")
        else:
            fail(f"gitops/README.md Namespace Ownership Matrix unexpected surface: {surface}")
    if indexed_namespace_surfaces != expected_namespace_ownership_surfaces:
        fail(
            "gitops/README.md Namespace Ownership Matrix row order must be: "
            + ", ".join(expected_namespace_ownership_surfaces)
        )

infrastructure_dir = root / "infrastructure"
infrastructure_readme_path = infrastructure_dir / "README.md"
infrastructure_readme = read_text(infrastructure_readme_path)
expected_infrastructure_coverage_header = [
    "Area",
    "Purpose and owner",
    "Lifecycle and config",
    "Dependencies, routes, secrets",
    "Validation and operations",
]
expected_infrastructure_coverage_areas = [
    "argocd/",
    "k3d/",
    "tests/",
    "vault/",
    "bootstrap-local.sh",
    "ipaddresspool.yaml",
    "l2advertisement.yaml",
]
infrastructure_coverage_rows = markdown_table_after_heading(
    infrastructure_readme,
    profiled_readme_table_headings("Infrastructure Coverage Matrix"),
)
if len(infrastructure_coverage_rows) < 2:
    fail("infrastructure/README.md Infrastructure Coverage Matrix must contain a header and coverage rows")
elif infrastructure_coverage_rows[0] != expected_infrastructure_coverage_header:
    fail(
        "infrastructure/README.md Infrastructure Coverage Matrix header must be: "
        + " | ".join(expected_infrastructure_coverage_header)
    )
else:
    indexed_infrastructure_areas: list[str] = []
    seen_infrastructure_areas: set[str] = set()
    for row_number, row in enumerate(infrastructure_coverage_rows[1:], start=1):
        if len(row) != len(expected_infrastructure_coverage_header):
            fail(
                "infrastructure/README.md Infrastructure Coverage Matrix "
                f"row {row_number} must have {len(expected_infrastructure_coverage_header)} columns"
            )
            continue
        area_cell, purpose, lifecycle, dependencies, validation = row
        area_names = re.findall(r"`([^`]+)`", area_cell)
        if not area_names:
            fail(
                "infrastructure/README.md Infrastructure Coverage Matrix "
                f"row {row_number} must name at least one backticked area path"
            )
            continue
        for area in area_names:
            if area in seen_infrastructure_areas:
                fail(f"infrastructure/README.md Infrastructure Coverage Matrix duplicates area: {area}")
            seen_infrastructure_areas.add(area)
            indexed_infrastructure_areas.append(area)
            area_path = infrastructure_dir / area.rstrip("/")
            if area.endswith("/"):
                if not area_path.is_dir():
                    fail(
                        "infrastructure/README.md Infrastructure Coverage Matrix "
                        f"references missing directory: infrastructure/{area}"
                    )
            elif not area_path.is_file():
                fail(
                    "infrastructure/README.md Infrastructure Coverage Matrix "
                    f"references missing file: infrastructure/{area}"
                )
        for label, value in [
            ("Purpose and owner", purpose),
            ("Lifecycle and config", lifecycle),
            ("Dependencies, routes, secrets", dependencies),
            ("Validation and operations", validation),
        ]:
            if not value:
                fail(f"infrastructure/README.md Infrastructure Coverage Matrix row {row_number} has empty {label}")
        if "owned by" not in purpose:
            fail(f"infrastructure/README.md Infrastructure Coverage Matrix row {row_number} must name ownership")
        if not any(marker in validation for marker in ["`bash ", "Validate", "Run ", "verify-"]):
            fail(f"infrastructure/README.md Infrastructure Coverage Matrix row {row_number} must cite validation or operation evidence")
    if indexed_infrastructure_areas != expected_infrastructure_coverage_areas:
        fail(
            "infrastructure/README.md Infrastructure Coverage Matrix area order must match actual infrastructure entrypoints: "
            + ", ".join(expected_infrastructure_coverage_areas)
        )

wsl2_prerequisite_rows = markdown_table_after_heading(
    infrastructure_readme,
    profiled_readme_table_headings("WSL2 Runtime Prerequisite Matrix"),
)
expected_wsl2_prerequisite_header = [
    "Prerequisite",
    "Repository SSoT",
    "Owner / responsibility",
    "Validation / evidence",
    "Failure boundary",
]
expected_wsl2_prerequisites = [
    "WSL2 shell and Docker context",
    "kubectl and k3d context",
    "kubeconfig and TLS trust",
    "Port and network contracts",
    "WSL networking constraints",
]
if len(wsl2_prerequisite_rows) < 2:
    fail("infrastructure/README.md WSL2 Runtime Prerequisite Matrix must contain a header and prerequisite rows")
elif wsl2_prerequisite_rows[0] != expected_wsl2_prerequisite_header:
    fail(
        "infrastructure/README.md WSL2 Runtime Prerequisite Matrix header must be: "
        + " | ".join(expected_wsl2_prerequisite_header)
    )
else:
    indexed_wsl2_prerequisites: list[str] = []
    for row_number, row in enumerate(wsl2_prerequisite_rows[1:], start=1):
        if len(row) != len(expected_wsl2_prerequisite_header):
            fail(
                "infrastructure/README.md WSL2 Runtime Prerequisite Matrix "
                f"row {row_number} must have {len(expected_wsl2_prerequisite_header)} columns"
            )
            continue
        prerequisite_cell, ssot, owner, validation, failure_boundary = row
        match = re.fullmatch(r"`([^`]+)`", prerequisite_cell)
        if not match:
            fail(
                "infrastructure/README.md WSL2 Runtime Prerequisite Matrix "
                f"row {row_number} must start with a backticked prerequisite name"
            )
            continue
        prerequisite = match.group(1)
        indexed_wsl2_prerequisites.append(prerequisite)
        for label, value in [
            ("Repository SSoT", ssot),
            ("Owner / responsibility", owner),
            ("Validation / evidence", validation),
            ("Failure boundary", failure_boundary),
        ]:
            if not value:
                fail(f"infrastructure/README.md WSL2 Runtime Prerequisite Matrix row {row_number} has empty {label}")
        if prerequisite == "WSL2 shell and Docker context":
            if "WSL-native Docker" not in ssot or "docker context show" not in validation:
                fail("infrastructure/README.md Docker prerequisite row must cite WSL-native Docker and docker context show")
            if "does not switch contexts automatically" not in failure_boundary:
                fail("infrastructure/README.md Docker prerequisite row must keep context switching operator-owned")
        elif prerequisite == "kubectl and k3d context":
            for phrase in ["k3d-hyhome", "k3d/k3d-cluster.yaml"]:
                if phrase not in ssot:
                    fail(f"infrastructure/README.md kubectl/k3d prerequisite row missing SSoT phrase: {phrase}")
            for command in ["k3d cluster list", "kubectl config current-context"]:
                if command not in validation:
                    fail(f"infrastructure/README.md kubectl/k3d prerequisite row missing validation command: {command}")
        elif prerequisite == "kubeconfig and TLS trust":
            if "~/.kube/config" not in ssot or "KUBECONFIG" not in ssot:
                fail("infrastructure/README.md kubeconfig prerequisite row must cite ~/.kube/config and KUBECONFIG")
            if "x509: certificate signed by unknown authority" not in validation:
                fail("infrastructure/README.md kubeconfig prerequisite row must cite the x509 TLS blocker")
            if "not an automatic" not in failure_boundary:
                fail("infrastructure/README.md kubeconfig prerequisite row must keep TLS repair operator-owned")
        elif prerequisite == "Port and network contracts":
            for phrase in ["172.18.0.240:443", "172.18.0.9:6379", "172.18.0.15:15432/15433"]:
                if phrase not in ssot:
                    fail(f"infrastructure/README.md port/network prerequisite row missing contract: {phrase}")
            for command in ["verify-contracts-static.sh", "run-all.sh"]:
                if command not in validation:
                    fail(f"infrastructure/README.md port/network prerequisite row missing validation command: {command}")
        elif prerequisite == "WSL networking constraints":
            if "127.0.0.1.nip.io" not in ssot or "Traefik dynamic configs" not in ssot:
                fail("infrastructure/README.md WSL networking row must cite nip.io and Traefik dynamic configs")
            if "outside repo-static ownership" not in failure_boundary:
                fail("infrastructure/README.md WSL networking row must keep Windows/WSL gateway state outside repo-static ownership")
    if indexed_wsl2_prerequisites != expected_wsl2_prerequisites:
        fail(
            "infrastructure/README.md WSL2 Runtime Prerequisite Matrix row order must be: "
            + ", ".join(expected_wsl2_prerequisites)
        )

bootstrap_boundary_rows = markdown_table_after_heading(
    infrastructure_readme,
    profiled_readme_table_headings("Bootstrap Boundary Matrix"),
)
expected_bootstrap_boundary_header = [
    "Boundary",
    "Repository responsibility",
    "Operator / external responsibility",
    "Allowed command surface",
    "Verification / evidence",
    "Failure boundary",
]
expected_bootstrap_boundaries = [
    "k3d cluster creation",
    "ArgoCD installation",
    "root app application",
    "Vault connection contract",
    "PostgreSQL and Valkey connection contract",
]
if len(bootstrap_boundary_rows) < 2:
    fail("infrastructure/README.md Bootstrap Boundary Matrix must contain a header and boundary rows")
elif bootstrap_boundary_rows[0] != expected_bootstrap_boundary_header:
    fail(
        "infrastructure/README.md Bootstrap Boundary Matrix header must be: "
        + " | ".join(expected_bootstrap_boundary_header)
    )
else:
    indexed_bootstrap_boundaries: list[str] = []
    for row_number, row in enumerate(bootstrap_boundary_rows[1:], start=1):
        if len(row) != len(expected_bootstrap_boundary_header):
            fail(
                "infrastructure/README.md Bootstrap Boundary Matrix "
                f"row {row_number} must have {len(expected_bootstrap_boundary_header)} columns"
            )
            continue
        boundary_cell, repo_resp, operator_resp, command_surface, verification, failure_boundary = row
        match = re.fullmatch(r"`([^`]+)`", boundary_cell)
        if not match:
            fail(
                "infrastructure/README.md Bootstrap Boundary Matrix "
                f"row {row_number} must start with a backticked boundary name"
            )
            continue
        boundary = match.group(1)
        indexed_bootstrap_boundaries.append(boundary)
        for label, value in [
            ("Repository responsibility", repo_resp),
            ("Operator / external responsibility", operator_resp),
            ("Allowed command surface", command_surface),
            ("Verification / evidence", verification),
            ("Failure boundary", failure_boundary),
        ]:
            if not value:
                fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} has empty {label}")
        if "Owns" not in repo_resp:
            fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} must name repository ownership")
        if not any(marker in operator_resp for marker in ["Operator owns", "External", "external"]):
            fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} must name operator or external ownership")
        if "bootstrap" not in command_surface and "Bootstrap" not in command_surface:
            fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} must describe bootstrap command boundary")
        if not any(command in verification for command in ["verify-", "validate-", "check-secret-handling.sh", "k3d cluster list", "kubectl config current-context"]):
            fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} must cite verification evidence")
        if "Repo-static checks do not" not in failure_boundary and "Steady-state" not in failure_boundary and "Agents do not" not in failure_boundary:
            fail(f"infrastructure/README.md Bootstrap Boundary Matrix row {row_number} must state a fail-closed boundary")
        if boundary == "k3d cluster creation":
            for phrase, value in [
                ("k3d/k3d-cluster.yaml", repo_resp),
                ("k3d-hyhome", repo_resp),
                ("WSL-native Docker", operator_resp),
                ("human-approved", operator_resp),
                ("k3d cluster create", command_surface),
                ("infrastructure/tests/verify-cluster.sh", verification),
                ("do not create", failure_boundary),
            ]:
                if phrase not in value:
                    fail(f"infrastructure/README.md k3d bootstrap boundary row missing phrase: {phrase}")
        elif boundary == "ArgoCD installation":
            for phrase, value in [
                ("argocd/values-local.yaml", repo_resp),
                ("ingress/TLS", repo_resp),
                ("certificate inputs", operator_resp),
                ("helm upgrade --install", command_surface),
                ("verify-contracts-static.sh", verification),
                ("infrastructure/tests/verify-gitops.sh", verification),
                ("outside approved bootstrap/break-glass", failure_boundary),
            ]:
                if phrase not in value:
                    fail(f"infrastructure/README.md ArgoCD bootstrap boundary row missing phrase: {phrase}")
        elif boundary == "root app application":
            for phrase, value in [
                ("gitops/clusters/local/root-application.yaml", repo_resp),
                ("gitops/apps/root", repo_resp),
                ("first root app apply", operator_resp),
                ("kubectl apply", command_surface),
                ("bootstrap-only exception", command_surface),
                ("scripts/validate-gitops-structure.sh", verification),
                ("direct apply is not normal operation", failure_boundary),
            ]:
                if phrase not in value:
                    fail(f"infrastructure/README.md root app bootstrap boundary row missing phrase: {phrase}")
        elif boundary == "Vault connection contract":
            for phrase, value in [
                ("vault-external.yaml", repo_resp),
                ("vault-secret-store.yaml", repo_resp),
                ("no-secret static checks", repo_resp),
                ("External Vault operator", operator_resp),
                ("secret values are not printed or committed", command_surface),
                ("check-secret-handling.sh", verification),
                ("verify-secrets.sh", verification),
                ("do not read secret values", failure_boundary),
                ("refresh Vault auth", failure_boundary),
            ]:
                if phrase not in value:
                    fail(f"infrastructure/README.md Vault bootstrap boundary row missing phrase: {phrase}")
        elif boundary == "PostgreSQL and Valkey connection contract":
            for phrase, value in [
                ("Service/EndpointSlice", repo_resp),
                ("ExternalSecret target naming", repo_resp),
                ("PostgreSQL/Valkey runtime", operator_resp),
                ("TLS/CA material", operator_resp),
                ("TCP reachability prechecks", command_surface),
                ("ArgoCD Valkey Secret", command_surface),
                ("verify-external-services.sh", verification),
                ("verify-secrets.sh", verification),
                ("do not start external services", failure_boundary),
                ("change `.env` values", failure_boundary),
            ]:
                if phrase not in value:
                    fail(f"infrastructure/README.md PostgreSQL/Valkey bootstrap boundary row missing phrase: {phrase}")
    if indexed_bootstrap_boundaries != expected_bootstrap_boundaries:
        fail(
            "infrastructure/README.md Bootstrap Boundary Matrix row order must be: "
            + ", ".join(expected_bootstrap_boundaries)
        )

infrastructure_shell_paths = sorted(
    [infrastructure_dir / "bootstrap-local.sh"]
    + list((infrastructure_dir / "tests").glob("*.sh"))
)
for script in infrastructure_shell_paths:
    if not script.exists():
        fail(f"infrastructure shell entrypoint is missing: {rel(script)}")
        continue
    if not os.access(script, os.X_OK):
        fail(f"infrastructure shell entrypoint must be executable: {rel(script)}")
    if not read_text(script).startswith("#!/usr/bin/env bash\n"):
        fail(f"infrastructure shell entrypoint must start with bash shebang: {rel(script)}")

infrastructure_test_rows = markdown_table_after_heading(
    infrastructure_readme,
    profiled_readme_table_headings("Infrastructure Test Inventory"),
)
expected_infra_test_header = [
    "Test script",
    "Type",
    "Preconditions",
    "Result semantics",
    "Retention / command surface",
]
allowed_infra_test_types = {"Static", "Live", "Live aggregate"}
test_script_paths = sorted((infrastructure_dir / "tests").glob("*.sh"))
test_script_names = {path.name for path in test_script_paths}
if len(infrastructure_test_rows) < 2:
    fail("infrastructure/README.md Infrastructure Test Inventory must contain a header and test rows")
elif infrastructure_test_rows[0] != expected_infra_test_header:
    fail(
        "infrastructure/README.md Infrastructure Test Inventory header must be: "
        + " | ".join(expected_infra_test_header)
    )
else:
    indexed_test_scripts: dict[str, list[str]] = {}
    live_test_scripts: set[str] = set()
    for row_number, row in enumerate(infrastructure_test_rows[1:], start=1):
        if len(row) != len(expected_infra_test_header):
            fail(
                "infrastructure/README.md Infrastructure Test Inventory "
                f"row {row_number} must have {len(expected_infra_test_header)} columns"
            )
            continue
        match = re.fullmatch(r"`([^`]+\.sh)`", row[0])
        if not match:
            fail(
                "infrastructure/README.md Infrastructure Test Inventory "
                f"row {row_number} must start with a backticked test script name"
            )
            continue
        script_name = match.group(1)
        if script_name in indexed_test_scripts:
            fail(f"infrastructure/README.md Infrastructure Test Inventory duplicates test script: {script_name}")
        indexed_test_scripts[script_name] = row

        test_type = row[1]
        preconditions = row[2]
        result_semantics = row[3]
        retention_surface = row[4]
        if test_type not in allowed_infra_test_types:
            fail(
                "infrastructure/README.md Infrastructure Test Inventory "
                f"row {row_number} has unsupported Type: {test_type}"
            )
        for label, value in [
            ("Preconditions", preconditions),
            ("Result semantics", result_semantics),
            ("Retention / command surface", retention_surface),
        ]:
            if not value:
                fail(
                    "infrastructure/README.md Infrastructure Test Inventory "
                    f"row {row_number} has empty {label}"
                )
        if "Tier" not in retention_surface:
            fail(
                "infrastructure/README.md Infrastructure Test Inventory "
                f"row {row_number} must cite a retention or command-surface Tier"
            )
        if test_type == "Live":
            live_test_scripts.add(script_name)

    for script_name in sorted(test_script_names - set(indexed_test_scripts)):
        fail(f"infrastructure/README.md Infrastructure Test Inventory missing test script row: {script_name}")
    for script_name in sorted(set(indexed_test_scripts) - test_script_names):
        fail(f"infrastructure/README.md Infrastructure Test Inventory references missing test script: {script_name}")

    run_all_path = infrastructure_dir / "tests/run-all.sh"
    if run_all_path.exists():
        run_all_called = set(
            re.findall(r'bash "\$script_dir/([^"]+\.sh)"', read_text(run_all_path))
        )
        missing_run_all_calls = sorted(live_test_scripts - run_all_called)
        extra_run_all_calls = sorted(run_all_called - live_test_scripts)
        if missing_run_all_calls:
            fail(
                "infrastructure/tests/run-all.sh is missing live test call(s): "
                + ", ".join(missing_run_all_calls)
            )
        if extra_run_all_calls:
            fail(
                "infrastructure/tests/run-all.sh calls test(s) not marked Live in Infrastructure Test Inventory: "
                + ", ".join(extra_run_all_calls)
            )

traefik_dir = root / "traefik"
traefik_readme_path = traefik_dir / "README.md"
traefik_readme = read_text(traefik_readme_path)
normalized_traefik_readme = re.sub(r"\s+", " ", traefik_readme)
for phrase in [
    "`k3d-hyhome-serverlb` is not the external Traefik gateway",
    "hy-home.docker external gateway container",
    "external Traefik dynamic config",
    "not a k3d GitOps desired-state failure",
    "repo-static 검증은 route manifest 계약만 확인",
    "live port availability",
    "operator-owned runtime evidence",
]:
    if phrase not in normalized_traefik_readme:
        fail(f"traefik/README.md missing external gateway/serverlb boundary phrase: {phrase}")
traefik_rows = markdown_table_after_heading(
    traefik_readme,
    profiled_readme_table_headings("Traefik Route Inventory"),
)
expected_traefik_header = ["Config", "Router host", "Backend URL", "Boundary", "Validation"]
traefik_configs = sorted(traefik_dir.glob("*.yaml"))
traefik_config_names = {path.name for path in traefik_configs}
if len(traefik_rows) < 2:
    fail("traefik/README.md Traefik Route Inventory must contain a header and route rows")
elif traefik_rows[0] != expected_traefik_header:
    fail(
        "traefik/README.md Traefik Route Inventory header must be: "
        + " | ".join(expected_traefik_header)
    )
else:
    indexed_traefik_configs: dict[str, list[str]] = {}
    for row_number, row in enumerate(traefik_rows[1:], start=1):
        if len(row) != len(expected_traefik_header):
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must have {len(expected_traefik_header)} columns")
            continue
        config_match = re.fullmatch(r"`([^`]+\.yaml)`", row[0])
        host_match = re.fullmatch(r"`([^`]+)`", row[1])
        backend_match = re.fullmatch(r"`([^`]+)`", row[2])
        if not config_match:
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must start with a backticked config filename")
            continue
        if not host_match:
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must use a backticked Router host")
            continue
        if not backend_match:
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must use a backticked Backend URL")
            continue
        config_name = config_match.group(1)
        host = host_match.group(1)
        backend_url = backend_match.group(1)
        boundary = row[3]
        validation = row[4]
        if config_name in indexed_traefik_configs:
            fail(f"traefik/README.md Traefik Route Inventory duplicates config: {config_name}")
        indexed_traefik_configs[config_name] = row
        if not boundary or "Reference-only" not in boundary:
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must keep reference-only boundary")
        if not validation or "validate-repo-quality-gates.sh" not in validation:
            fail(f"traefik/README.md Traefik Route Inventory row {row_number} must cite repo quality validation")

        config_path = traefik_dir / config_name
        if not config_path.exists():
            fail(f"traefik/README.md Traefik Route Inventory references missing config: {config_name}")
            continue
        try:
            config = load_yaml(config_path)
        except Exception as exc:
            fail(f"Traefik config YAML parse failed for {rel(config_path)}: {exc}")
            continue
        http = config.get("http") if isinstance(config, dict) else {}
        services = http.get("services") if isinstance(http, dict) else {}
        routers = http.get("routers") if isinstance(http, dict) else {}
        transports = http.get("serversTransports") if isinstance(http, dict) else {}
        if not isinstance(services, dict) or len(services) != 1:
            fail(f"{rel(config_path)} must define exactly one Traefik service")
            continue
        if not isinstance(routers, dict) or len(routers) != 1:
            fail(f"{rel(config_path)} must define exactly one Traefik router")
            continue
        service_name, service = next(iter(services.items()))
        router_name, router = next(iter(routers.items()))
        load_balancer = service.get("loadBalancer") if isinstance(service, dict) else {}
        servers = load_balancer.get("servers") if isinstance(load_balancer, dict) else []
        urls = [
            server.get("url")
            for server in servers
            if isinstance(server, dict) and server.get("url")
        ]
        if urls != [backend_url]:
            fail(f"{rel(config_path)} backend URL must match README inventory: {backend_url}")
        if load_balancer.get("passHostHeader") is not True:
            fail(f"{rel(config_path)} loadBalancer.passHostHeader must be true")
        transport_name = load_balancer.get("serversTransport")
        if not transport_name or transport_name not in transports:
            fail(f"{rel(config_path)} service must reference a defined serversTransport")
        elif transports.get(transport_name, {}).get("insecureSkipVerify") is not True:
            fail(f"{rel(config_path)} serversTransport must set insecureSkipVerify: true")
        expected_rule = f"Host(`{host}`)"
        if not isinstance(router, dict) or router.get("rule") != expected_rule:
            fail(f"{rel(config_path)} router rule must match README inventory host: {expected_rule}")
        entrypoints = router.get("entryPoints") if isinstance(router, dict) else []
        if entrypoints != ["websecure"]:
            fail(f"{rel(config_path)} router entryPoints must be exactly ['websecure']")
        if router.get("service") != service_name:
            fail(f"{rel(config_path)} router service must reference the defined service")
        if "tls" not in router:
            fail(f"{rel(config_path)} router must define tls")

    for config_name in sorted(traefik_config_names - set(indexed_traefik_configs)):
        fail(f"traefik/README.md Traefik Route Inventory missing config row: {config_name}")
    for config_name in sorted(set(indexed_traefik_configs) - traefik_config_names):
        fail(f"traefik/README.md Traefik Route Inventory references missing config: {config_name}")

stale_traefik_backend_pattern = "k3d-hyhome-serverlb:443"
for path in sorted([*traefik_configs, root / "examples/sample-app/traefik-k3d.yaml.example"]):
    text = read_text(path)
    if stale_traefik_backend_pattern in text:
        fail(f"{rel(path)} contains stale Traefik backend: {stale_traefik_backend_pattern}")
    if "https://172.18.0.240:443" not in text:
        fail(f"{rel(path)} must reference ingress-nginx LoadBalancer backend https://172.18.0.240:443")

script_ref_pattern = re.compile(r"scripts/[A-Za-z0-9_.-]+\.sh")
script_command_contract_paths = [
    root / "README.md",
    scripts_dir / "README.md",
    root / ".github/workflows/ci.yml",
    root / ".github/PULL_REQUEST_TEMPLATE.md",
    root / ".github/ABOUT.md",
    root / ".claude/settings.json",
    root / ".claude/CLAUDE.md",
    root / "docs/00.agent-governance/hooks/post-validate.sh",
    root / "docs/00.agent-governance/hooks/lifecycle-guard.sh",
    root / ".codex/hooks.json",
    root / "docs/05.operations/guides/0009-llm-wiki-curation-guide.md",
    root / "docs/90.references/README.md",
    root / "docs/90.references/llm-wiki/README.md",
    root / "docs/90.references/llm-wiki/wiki-index.md",
    root / "gitops/README.md",
    root / "gitops/workloads/README.md",
    root / "docs/README.md",
    root / "docs/00.agent-governance/rules/document-stage-routing.md",
]
for path in script_command_contract_paths:
    if not path.exists():
        continue
    for match in sorted(set(script_ref_pattern.findall(read_text(path)))):
        if not (root / match).exists():
            fail(f"script reference points to missing file in {rel(path)}: {match}")

broad_script_reference_suffixes = {
    ".md",
    ".toml",
    ".json",
    ".yml",
    ".yaml",
    ".sh",
    ".tf",
    ".bicep",
    ".txt",
}
for tracked_path in sorted(tracked):
    path = root / tracked_path
    if not path.is_file() or path.suffix not in broad_script_reference_suffixes:
        continue
    for match in sorted(set(script_ref_pattern.findall(read_text(path)))):
        if not (root / match).is_file():
            fail(f"tracked script reference points to missing file in {rel(path)}: {match}")

secret_scanner_text = read_text(scripts_dir / "check-secret-handling.sh")
for phrase in [
    "examples/sample-app",
    '-name "gitops"',
    '-name "kubernetes"',
    "value=<redacted>",
]:
    if phrase not in secret_scanner_text:
        fail(f"{rel(scripts_dir / 'check-secret-handling.sh')} missing examples secret-scan contract phrase: {phrase}")

for obsolete in ["k3d_kubeconfig.yaml"]:
    if obsolete in tracked:
        fail(f"obsolete tracked file remains: {obsolete}")
for tracked_path in tracked:
    if tracked_path.startswith("docs/" + legacy_postmortems + "/") or tracked_path.startswith("docs/" + legacy_learning + "/"):
        fail(f"obsolete tracked docs path remains: {tracked_path}")

inventory_path = root / "docs/90.references/data/tech-stack-version-inventory.md"
inventory_text = read_text(inventory_path)
match = re.search(r"```yaml\n(.*?)\n```", inventory_text, re.DOTALL)
if not match:
    fail(f"missing YAML inventory block in {rel(inventory_path)}")
    inventory = {}
else:
    inventory = yaml.safe_load(match.group(1)) or {}

k3d_config = load_yaml(root / "infrastructure/k3d/k3d-cluster.yaml")
actual_k3s_image = k3d_config.get("image")
if inventory.get("k3s_image") != actual_k3s_image:
    fail(f"k3s image drift: inventory={inventory.get('k3s_image')} actual={actual_k3s_image}")

actual_charts = {}
for app_file in sorted((root / "gitops/apps/root").glob("*.yaml")):
    data = load_yaml(app_file)
    source = ((data.get("spec") or {}).get("source") or {})
    if source.get("chart"):
        actual_charts[(data.get("metadata") or {}).get("name")] = {
            "repoURL": source.get("repoURL"),
            "chart": source.get("chart"),
            "targetRevision": str(source.get("targetRevision")),
        }
expected_charts = inventory.get("helm_charts") or {}
for name, expected in sorted(expected_charts.items()):
    actual = actual_charts.get(name)
    if actual != expected:
        fail(f"Helm chart drift for {name}: inventory={expected} actual={actual}")
for name in sorted(set(actual_charts) - set(expected_charts)):
    fail(f"Helm chart missing from inventory: {name}")

actual_actions = {}
for workflow in sorted((root / ".github/workflows").glob("*.yml")):
    data = load_yaml(workflow)
    for job in (data.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            uses = step.get("uses")
            if not uses:
                continue
            if "@" not in uses:
                fail(f"GitHub Action is not pinned with @version in {rel(workflow)}: {uses}")
                continue
            action, version = uses.rsplit("@", 1)
            previous = actual_actions.get(action)
            if previous and previous != version:
                fail(f"GitHub Action version conflict for {action}: {previous} vs {version}")
            actual_actions[action] = version
expected_actions = inventory.get("github_actions") or {}
for action, expected in sorted(expected_actions.items()):
    actual = actual_actions.get(action)
    if actual != expected:
        fail(f"GitHub Action version drift for {action}: inventory={expected} actual={actual}")
for action in sorted(set(actual_actions) - set(expected_actions)):
    fail(f"GitHub Action missing from inventory: {action}")

pre_commit_data = load_yaml(root / ".pre-commit-config.yaml")
actual_pre_commit = {
    repo_entry.get("repo"): str(repo_entry.get("rev"))
    for repo_entry in pre_commit_data.get("repos") or []
    if repo_entry.get("repo") and repo_entry.get("rev")
}
expected_pre_commit = inventory.get("pre_commit") or {}
for repo_url, expected in sorted(expected_pre_commit.items()):
    actual = actual_pre_commit.get(repo_url)
    if actual != expected:
        fail(f"pre-commit version drift for {repo_url}: inventory={expected} actual={actual}")
for repo_url in sorted(set(actual_pre_commit) - set(expected_pre_commit)):
    fail(f"pre-commit repo missing from inventory: {repo_url}")

pre_commit_text = read_text(root / ".pre-commit-config.yaml")
stale_pre_commit_hook_regex = "\\." + "claude/hooks/.*\\.sh"
for hook_id in ["shellcheck", "shfmt"]:
    if "docs/00\\.agent-governance/hooks/.*\\.sh" not in pre_commit_text:
        fail(f".pre-commit-config.yaml {hook_id} must include docs/00.agent-governance/hooks/*.sh coverage")
    if stale_pre_commit_hook_regex in pre_commit_text:
        fail(f".pre-commit-config.yaml {hook_id} must not use stale provider-local hook coverage")

active_hook_reference_files = [
    root / ".claude/CLAUDE.md",
    root / "docs/00.agent-governance/providers/claude.md",
    root / "docs/00.agent-governance/scopes/meta.md",
    root / "scripts/README.md",
    root / "tests/README.md",
    root / "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md",
    root / "docs/00.agent-governance/hooks/post-validate.sh",
    root / "docs/00.agent-governance/hooks/lifecycle-guard.sh",
]
for path in active_hook_reference_files:
    text = read_text(path)
    if stale_provider_hook_path in text:
        fail(f"{rel(path)} contains stale active hook path; use docs/00.agent-governance/hooks")
    if "docs/00.agent-governance/hooks" not in text:
        fail(f"{rel(path)} missing shared hook path docs/00.agent-governance/hooks")

tests_readme_text = read_text(root / "tests/README.md")
for phrase in [
    "Repo-static",
    "Optional tool",
    "Live/operator-owned",
    "SKIP",
    "kube-linter",
    "conftest",
    "infrastructure/tests/run-all.sh",
]:
    if phrase not in tests_readme_text:
        fail(f"tests/README.md missing validation evidence boundary phrase: {phrase}")

for hook_path in [
    root / "docs/00.agent-governance/hooks/post-validate.sh",
    root / "docs/00.agent-governance/hooks/lifecycle-guard.sh",
]:
    hook_text = read_text(hook_path)
    if ".agents/*" not in hook_text:
        fail(f"{rel(hook_path)} must trigger repository quality gates for .agents/** shared asset changes")
    if ".agents/hooks.json" not in hook_text:
        fail(f"{rel(hook_path)} must parse .agents/hooks.json with other runtime hook JSON files")

ci_qa_guide_path = root / "docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md"
ci_qa_guide_text = read_text(ci_qa_guide_path)
for phrase in [
    "## Source Basis",
    "Parent Spec",
    "GitHub Actions documentation",
    "GitHub Actions CI gate definitions",
]:
    if phrase not in ci_qa_guide_text:
        fail(f"{rel(ci_qa_guide_path)} missing CI/QA source basis phrase: {phrase}")
stale_shell_job = "`" + "shell" + "-static" + "`"
if stale_shell_job in ci_qa_guide_text:
    fail(f"{rel(ci_qa_guide_path)} must not list stale shell static job as an active CI job")

if failures:
    print("=== validate-repo-quality-gates ===")
    for item in failures:
        print(item)
    sys.exit(1)

print("[PASS] repository quality gates passed")
PY
