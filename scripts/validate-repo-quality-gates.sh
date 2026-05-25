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

python3 - "$ROOT_DIR" <<'PY'
import collections
import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse

import yaml

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


def workflow_on(data):
    return data.get("on") if "on" in data else data.get(True, {})


def load_json(path: pathlib.Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_toml(path: pathlib.Path):
    if tomllib is None:
        raise RuntimeError("python3 tomllib module is required to parse TOML agent mirrors")
    with path.open("rb") as handle:
        return tomllib.load(handle)


def extract_scope_imports(text: str) -> list[str]:
    return sorted(re.findall(r"@import\s+(docs/00\.agent-governance/scopes/[A-Za-z0-9_.-]+\.md)", text))


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(root))


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


def extract_ci_branch_policy_prefixes(branch_policy_text: str) -> list[str]:
    match = re.search(r"allowed_branch_regex=['\"]\^\(([^)]+)\)/['\"]", branch_policy_text)
    if not match:
        return []
    return match.group(1).split("|")


def extract_pr_template_prefixes(text: str) -> list[str]:
    return [prefix.rstrip("/") for prefix in re.findall(r"`([a-z0-9-]+/)`", text)]


def markdown_table_after_heading(text: str, heading: str) -> list[list[str]]:
    lines = text.splitlines()
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        fail(f"missing markdown heading: {heading}")
        return []

    table_lines: list[str] = []
    for line in lines[start + 1 :]:
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
    return rows


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
    if tracked_path == ".agents" or tracked_path.startswith(".agents/"):
        fail(f"ignored local agent runtime path must not be tracked: {tracked_path}")
    if re.fullmatch(r"\.claude/[^/]+\.local\.md", tracked_path):
        fail(f"ignored local Claude/Hookify runtime rule must not be tracked: {tracked_path}")

ignore_check = subprocess.run(["git", "check-ignore", "-q", ".agents/"], cwd=root)
if ignore_check.returncode == 1:
    fail(".agents/ must remain ignored by Git")
elif ignore_check.returncode not in {0, 1}:
    fail("git check-ignore failed while validating .agents/ ignore contract")

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
    fail(".agents must be an ignored local directory when present")
if local_agents_skills_dir.exists() and not local_agents_skills_dir.is_dir():
    fail(".agents/skills must be an ignored local directory when present")
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
                "local ignored skill mirror drift: "
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
for provider in ["aws", "azure"]:
    example_docs = root / "examples" / provider / "docs"
    if not example_docs.exists():
        fail(f"example docs root is missing: {rel(example_docs)}")
        continue
    actual_example_top_level = {path.name for path in example_docs.iterdir() if path.is_dir()}
    for name in sorted(actual_example_top_level & old_top_level_docs):
        fail(f"old example docs stage folder must not exist after hard migration: {rel(example_docs / name)}")
    for name in sorted(actual_example_top_level - example_docs_allowed_top_level):
        fail(f"example docs top-level folder is not allowed: {rel(example_docs / name)}")
    for name in sorted(example_docs_required):
        if not (example_docs / name).is_dir():
            fail(f"required example docs taxonomy folder is missing: {rel(example_docs / name)}")

readme_base_sections = {
    "Overview": re.compile(r"^##\s+Overview\b", re.MULTILINE),
    "Audience": re.compile(r"^##\s+Audience\b", re.MULTILINE),
    "Scope": re.compile(r"^##\s+Scope\b", re.MULTILINE),
    "Structure": re.compile(r"^##\s+Structure\b", re.MULTILINE),
    "How to Work in This Area": re.compile(r"^##\s+How to Work in This Area\b", re.MULTILINE),
    "Link Basis": re.compile(r"^##\s+Link Basis\b", re.MULTILINE),
    "Related Documents": re.compile(r"^##\s+Related Documents\b", re.MULTILINE),
}
for name in sorted(required_doc_dirs):
    readme = docs_dir / name / "README.md"
    if not readme.exists():
        fail(f"required README.md is missing: {rel(readme)}")
for readme in sorted(root.rglob("README.md")):
    if ".git" in readme.parts or ".agents" in readme.parts or ".agent-work" in readme.parts:
        continue
    text = read_text(readme)
    for section, pattern in readme_base_sections.items():
        if not pattern.search(text):
            fail(f"{rel(readme)} missing README base section: {section}")
    if not re.search(r"^##\s+Related Documents\b", text, re.MULTILINE):
        fail(f"{rel(readme)} missing canonical README section: Related Documents")
    if re.search(r"^##\s+Related References\b", text, re.MULTILINE):
        fail(f"{rel(readme)} still uses legacy README section: Related References")

reference_readme_path = root / "docs/90.references/README.md"
reference_readme_text = read_text(reference_readme_path)
for obsolete_heading in [
    "## 목적",
    "## 포함할 내용",
    "## 포함하지 말아야 할 내용",
    "## 관련 폴더",
    "## 예시",
    "## Agent 참고 문서 배치 규칙",
    "## 문서 인덱스",
    "## Templates",
]:
    if re.search(rf"^{re.escape(obsolete_heading)}\s*$", reference_readme_text, re.MULTILINE):
        fail(f"{rel(reference_readme_path)} contains obsolete duplicate README heading: {obsolete_heading}")


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


markdown_link_roots = [
    root / "README.md",
    root / "docs",
    root / ".claude",
    root / ".codex",
    root / ".github",
    root / "scripts",
    root / "infrastructure",
    root / "gitops",
    root / "traefik",
    root / "tests",
    root / "examples",
]
seen_markdown_link_paths: set[pathlib.Path] = set()
for scan_root in markdown_link_roots:
    candidates = [scan_root] if scan_root.is_file() else scan_root.rglob("*.md")
    for markdown in sorted(candidates):
        if not markdown.is_file() or markdown in seen_markdown_link_paths:
            continue
        if ".git" in markdown.parts or ".agents" in markdown.parts:
            continue
        seen_markdown_link_paths.add(markdown)
        for raw_target in iter_markdown_link_targets(read_text(markdown)):
            target = normalize_markdown_target(raw_target)
            if not target or target.startswith("#"):
                continue
            if target.startswith("file://"):
                fail(f"{rel(markdown)} uses file:// Markdown link target: {target}")
                continue
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target_without_fragment = target.split("#", 1)[0]
            if not target_without_fragment:
                continue
            target_path = pathlib.Path(urllib.parse.unquote(target_without_fragment))
            if target_path.is_absolute():
                fail(f"{rel(markdown)} uses absolute Markdown link target: {target}")
                continue
            if not (markdown.parent / target_path).exists():
                fail(f"{rel(markdown)} has broken Markdown link target: {target}")

template_readme = read_text(root / "docs/99.templates/README.md")
for template in sorted((root / "docs/99.templates").iterdir()):
    if template.is_file() and template.name != "README.md" and template.name not in template_readme:
        fail(f"template is not listed in docs/99.templates/README.md: {template.name}")
for phrase in [
    "## Structural Template Coverage",
    "structural template mapping",
    "exactly one mapping",
]:
    if phrase not in template_readme:
        fail(f"{rel(root / 'docs/99.templates/README.md')} missing structural template coverage phrase: {phrase}")

reference_template_path = root / "docs/99.templates/reference.template.md"
reference_template_text = read_text(reference_template_path)
reference_template_target_parent = root / "docs/90.references/example-category"
reference_template_target_relative_links = {
    "../../05.operations/runbooks/0011-reference-maintenance-runbook.md": root
    / "docs/05.operations/runbooks/0011-reference-maintenance-runbook.md",
    "../../05.operations/guides/0009-llm-wiki-curation-guide.md": root
    / "docs/05.operations/guides/0009-llm-wiki-curation-guide.md",
}
for target, expected_path in reference_template_target_relative_links.items():
    if f"`{target}`" not in reference_template_text:
        fail(f"{rel(reference_template_path)} missing target-relative reference link: {target}")
    resolved_path = (reference_template_target_parent / target).resolve()
    if resolved_path != expected_path.resolve():
        fail(
            f"{rel(reference_template_path)} target-relative link does not resolve from "
            f"docs/90.references/<category>/<item>.md: {target}"
        )
    if not expected_path.exists():
        fail(f"{rel(reference_template_path)} target-relative link points to missing file: {target}")

for path in docs_dir.rglob("*"):
    if not path.is_file():
        continue
    if path.is_relative_to(root / "docs/99.templates"):
        continue
    if re.search(r"(^template\.md$|\.template\.|template\.)", path.name):
        fail(f"template-like docs file must live in docs/99.templates: {rel(path)}")

authored_template_residue = ("Target: docs/", "Use this template")
for path in docs_dir.rglob("*.md"):
    if path.is_relative_to(root / "docs/99.templates"):
        continue
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        if any(marker in line for marker in authored_template_residue):
            fail(f"authored docs template residue in {rel(path)}:{line_number}")

required_stage_templates = [
    ("docs/01.requirements/*.md", "prd.template.md"),
    ("docs/02.architecture/requirements/*.md", "ard.template.md"),
    ("docs/02.architecture/decisions/*.md", "adr.template.md"),
    ("docs/03.specs/*/spec.md", "spec.template.md"),
    ("docs/03.specs/*/api-spec.md", "api-spec.template.md"),
    ("docs/03.specs/*/agent-design.md", "agent-design.template.md"),
    ("docs/03.specs/*/data-model.md", "data-model.template.md"),
    ("docs/03.specs/*/tests.md", "tests.template.md"),
    ("docs/04.execution/plans/*.md", "plan.template.md"),
    ("docs/04.execution/tasks/*.md", "task.template.md"),
    ("docs/05.operations/guides/*.md", "guide.template.md"),
    ("docs/05.operations/policies/*.md", "operation.template.md"),
    ("docs/05.operations/runbooks/*.md", "runbook.template.md"),
    ("docs/05.operations/incidents/[0-9][0-9][0-9][0-9]/*.md", "incident.template.md"),
    ("docs/05.operations/incidents/postmortems/**/*.md", "postmortem.template.md"),
    ("docs/90.references/**/*.md", "reference.template.md"),
]

for glob_pattern, template_name in required_stage_templates:
    template_path = root / "docs/99.templates" / template_name
    if not template_path.exists():
        fail(f"structural template mapping points to missing template: {glob_pattern} -> {template_name}")

structural_template_roots = [
    root / "docs/01.requirements",
    root / "docs/02.architecture",
    root / "docs/03.specs",
    root / "docs/04.execution",
    root / "docs/05.operations",
    root / "docs/90.references",
]
for scan_root in structural_template_roots:
    for path in sorted(scan_root.rglob("*.md")):
        if path.name == "README.md":
            continue
        relative_path = rel(path)
        matching_templates = [
            template_name
            for glob_pattern, template_name in required_stage_templates
            if fnmatch.fnmatchcase(relative_path, glob_pattern)
        ]
        if not matching_templates:
            fail(f"{relative_path} is not covered by a structural template mapping")
        elif len(matching_templates) > 1:
            fail(
                f"{relative_path} matches multiple structural template mappings: "
                f"{', '.join(matching_templates)}"
            )


def required_headings_from_template(template_name: str) -> list[str]:
    headings: list[str] = []
    for line in read_text(root / "docs/99.templates" / template_name).splitlines():
        if not line.startswith("## "):
            continue
        heading = line.strip()
        if "[" in heading or "<" in heading:
            continue
        if "(If Applicable)" in heading or "(Optional)" in heading:
            continue
        headings.append(heading)
    return headings


for glob_pattern, template_name in required_stage_templates:
    required_headings = required_headings_from_template(template_name)
    for path in sorted(root.glob(glob_pattern)):
        if path.name == "README.md":
            continue
        document_headings = {
            line.strip()
            for line in read_text(path).splitlines()
            if line.startswith("## ")
        }
        for heading in required_headings:
            if heading not in document_headings:
                fail(f"{rel(path)} missing required template heading from {template_name}: {heading}")

template_enforcement_phrase_checks = {
    root / "docs/00.agent-governance/rules/documentation-protocol.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "structural template mapping",
        "required template headings",
        "template path used and the validation evidence",
    ],
    root / "docs/00.agent-governance/rules/document-stage-routing.md": [
        "docs/99.templates/readme.template.md",
        "structural template mapping",
        "required template headings",
        "template path used and validation evidence",
    ],
    root / ".claude/skills/docs-stage-routing/skill.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "Required Template",
        "validation evidence",
    ],
    root / ".claude/agents/doc-writer.md": [
        "docs/99.templates/README.md",
        "status: draft",
        "required template headings",
        "structural template mapping",
        "template path used",
        "Validation evidence",
    ],
    root / ".codex/agents/doc-writer.toml": [
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
        "max_lines": 40,
        "required": [
            "docs/00.agent-governance/rules/bootstrap.md",
            "docs/00.agent-governance/rules/preflight-checklist.md",
            "docs/00.agent-governance/rules/persona.md",
            ".claude/CLAUDE.md",
            "docs/00.agent-governance/harness-catalog.md",
            "docs/00.agent-governance/rules/agentic.md",
            "docs/00.agent-governance/rules/document-stage-routing.md",
            "docs/00.agent-governance/rules/git-workflow.md",
        ],
    },
    "CLAUDE.md": {
        "max_lines": 30,
        "required": [
            "@AGENTS.md",
            "@docs/00.agent-governance/providers/claude.md",
            "@.claude/CLAUDE.md",
            "@RTK.md",
            "docs/00.agent-governance/harness-catalog.md",
        ],
    },
    "GEMINI.md": {
        "max_lines": 25,
        "required": [
            "@AGENTS.md",
            "@docs/00.agent-governance/providers/gemini.md",
            "@.claude/CLAUDE.md",
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

harness_catalog_path = root / "docs/00.agent-governance/harness-catalog.md"
harness_catalog_text = read_text(harness_catalog_path)
for phrase in [
    "Claude permissions/hooks",
    "Codex event hooks",
    "not a permission gate equivalent",
    ".claude/settings.json",
    ".codex/hooks.json",
    "Runtime surface added for LLM Wiki curation",
    "## Matrix Status Contract",
    "`Ready`, `Partial`, and `Missing`",
    "A `Ready` row is not semantic proof",
    "regression and structure guard",
    "Authored-doc command boundary",
    "command examples in authored docs require",
    "## Harness Engineering Matrix",
    "## Agent-first Engineering Matrix",
    "| Required Component | Current Surface | Status | Gap | Remediation |",
]:
    if phrase not in harness_catalog_text:
        fail(f"{rel(harness_catalog_path)} missing runtime readiness boundary phrase: {phrase}")
validate_component_matrix(harness_catalog_text, "## Harness Engineering Matrix")
validate_component_matrix(harness_catalog_text, "## Agent-first Engineering Matrix")
for phrase in [
    "Thin gateway",
    "Runtime baseline",
    "Agent roster",
    "Codex mirrors",
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

agentic_path = root / "docs/00.agent-governance/rules/agentic.md"
agentic_text = read_text(agentic_path)
for phrase in [
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

memory_progress_path = root / "docs/00.agent-governance/memory/progress.md"
memory_progress_text = read_text(memory_progress_path)
for phrase in [
    "docs/99.templates/progress.template.md",
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
memory_template_path = root / "docs/99.templates/memory.template.md"
progress_template_path = root / "docs/99.templates/progress.template.md"
for path in [memory_dir / "README.md", memory_progress_path, memory_template_path, progress_template_path]:
    if not path.exists():
        fail(f"required memory contract file is missing: {rel(path)}")

memory_readme_text = read_text(memory_dir / "README.md")
for phrase in [
    "docs/99.templates/memory.template.md",
    "docs/99.templates/progress.template.md",
    "Standalone files under this folder must use",
    "Related Progress",
    "`progress.md` work entry",
]:
    if phrase not in memory_readme_text:
        fail(f"{rel(memory_dir / 'README.md')} missing memory contract phrase: {phrase}")

for phrase in [
    "docs/00.agent-governance/memory/progress.md",
    "docs/99.templates/progress.template.md",
    "## Related Progress",
]:
    if phrase not in read_text(memory_template_path):
        fail(f"{rel(memory_template_path)} missing standalone memory template phrase: {phrase}")

for phrase in [
    "docs/00.agent-governance/memory/progress.md",
    "## Work Entries",
]:
    if phrase not in read_text(progress_template_path):
        fail(f"{rel(progress_template_path)} missing progress template phrase: {phrase}")

for phrase in ["memory.template.md", "progress.template.md", "00.agent-governance/memory/"]:
    if phrase not in template_readme:
        fail(f"{rel(root / 'docs/99.templates/README.md')} missing memory template inventory phrase: {phrase}")

standalone_memory_required_headings = required_headings_from_template("memory.template.md")
for memory_file in sorted(memory_dir.glob("*.md")):
    if memory_file.name in {"README.md", "progress.md"}:
        continue
    document_headings = {
        line.strip()
        for line in read_text(memory_file).splitlines()
        if line.startswith("## ")
    }
    for heading in standalone_memory_required_headings:
        if heading not in document_headings:
            fail(f"{rel(memory_file)} missing required template heading from memory.template.md: {heading}")

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

zizmor_path = root / ".github/zizmor.yml"
zizmor_rules = (load_yaml(zizmor_path).get("rules") or {})
allowed_zizmor_disables = {"unpinned-uses"}
for rule_name, rule_config in sorted(zizmor_rules.items()):
    if isinstance(rule_config, dict) and rule_config.get("disable") is True and rule_name not in allowed_zizmor_disables:
        fail(f"{rel(zizmor_path)} disables unsupported zizmor rule: {rule_name}")
if not isinstance(zizmor_rules.get("unpinned-uses"), dict) or zizmor_rules["unpinned-uses"].get("disable") is not True:
    fail(f"{rel(zizmor_path)} must keep only unpinned-uses disabled for tag-plus-inventory action pinning")

git_workflow_path = root / "docs/00.agent-governance/rules/git-workflow.md"
git_workflow_text = read_text(git_workflow_path)
branch_prefixes = branch_prefixes_from_git_workflow(git_workflow_path)
if not branch_prefixes:
    fail(f"{rel(git_workflow_path)} must define branch types as the branch prefix policy SSoT")
for phrase in [
    "Every pull request targeting `main` must run the required CI and branch-policy checks with no bypass exceptions.",
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

ci_path = root / ".github/workflows/ci.yml"
try:
    ci_data = load_yaml(ci_path)
except Exception as exc:
    fail(f"CI workflow parse failed for {rel(ci_path)}: {exc}")
    ci_data = {}

ci_on = workflow_on(ci_data)
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

ci_jobs = ci_data.get("jobs") or {}
required_ci_jobs = {
    "branch-policy",
    "changes",
    "pre-commit",
    "repo-quality-static",
    "manifest-static",
    "shell-static",
    "ci-summary",
}
for job_id in sorted(required_ci_jobs - set(ci_jobs)):
    fail(f"{rel(ci_path)} missing required CI job: {job_id}")

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
filters = {}
for step in changes_job.get("steps") or []:
    if step.get("id") == "filter":
        try:
            filters = yaml.safe_load(((step.get("with") or {}).get("filters") or "")) or {}
        except Exception as exc:
            fail(f"{rel(ci_path)} changes filter YAML parse failed: {exc}")
        break
repo_quality_filter_paths = filters.get("repo_quality") or []
if "examples/**" not in repo_quality_filter_paths:
    fail(f"{rel(ci_path)} repo_quality path filter must include examples/**")
shell_filter_paths = filters.get("shell") or []
if ".claude/hooks/**/*.sh" not in shell_filter_paths:
    fail(f"{rel(ci_path)} shell path filter must include .claude/hooks/**/*.sh")

manifest_static_runs = "\n".join(
    str(step.get("run") or "")
    for step in (ci_jobs.get("manifest-static") or {}).get("steps") or []
)
for command in [
    "bash infrastructure/tests/verify-contracts-static.sh",
    "bash scripts/validate-gitops-structure.sh",
    "bash scripts/validate-k8s-manifests.sh .",
    "bash scripts/check-secret-handling.sh .",
]:
    if command not in manifest_static_runs:
        fail(f"{rel(ci_path)} manifest-static missing command: {command}")

shell_static_text = "\n".join(
    str(step.get("run") or "")
    for step in (ci_jobs.get("shell-static") or {}).get("steps") or []
)
if ".claude/hooks" not in shell_static_text:
    fail(f"{rel(ci_path)} shell-static scope must include .claude/hooks")

pr_template_path = root / ".github/PULL_REQUEST_TEMPLATE.md"
pr_template_text = read_text(pr_template_path)
for command in [
    "bash scripts/validate-repo-quality-gates.sh .",
    "bash infrastructure/tests/verify-contracts-static.sh",
    "bash scripts/validate-gitops-structure.sh",
    "bash scripts/validate-k8s-manifests.sh .",
    "bash scripts/check-secret-handling.sh .",
]:
    if command not in pr_template_text:
        fail(f"{rel(pr_template_path)} missing manual verification command: {command}")
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
    "docs/90.references/versions/tech-stack-version-inventory.md",
    "branch protection/rulesets enforce direct-push restrictions",
    "QA gates and release-evidence automation, not deploy CD",
    "Defensive overlap between CI jobs is intentional QA coverage",
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

for json_path in [root / ".claude/settings.json", root / ".codex/hooks.json"]:
    try:
        load_json(json_path)
    except Exception as exc:
        fail(f"agent runtime JSON parse failed for {rel(json_path)}: {exc}")

claude_settings = load_json(root / ".claude/settings.json")
post_validate_command = json.dumps(claude_settings.get("hooks", {}))
for phrase in [
    ".claude/hooks/k8s-pre-edit.sh",
    ".claude/hooks/post-validate.sh",
    ".claude/hooks/session-start.sh",
    ".claude/hooks/lifecycle-guard.sh",
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
    ".claude/hooks/session-start.sh",
    ".claude/hooks/k8s-pre-edit.sh",
    ".claude/hooks/post-validate.sh",
    ".claude/hooks/lifecycle-guard.sh",
    "CODEX_PROJECT_DIR",
    "Glob|Grep",
    '"timeout": 60',
    '"timeout": 20',
]:
    if phrase not in codex_hooks_text:
        fail(f"{rel(codex_hooks_path)} missing Codex event hook phrase: {phrase}")


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
    pre_hook_path = root / ".claude/hooks/k8s-pre-edit.sh"
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
        "docs/99.templates/api-spec.template.md",
        "documentation template enforcement",
    ]:
        if phrase not in docs_pre_hook_result.stdout:
            fail(f"{rel(pre_hook_path)} docs payload simulation missing output phrase: {phrase}")

    post_hook_path = root / ".claude/hooks/post-validate.sh"
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

    lifecycle_hook_path = root / ".claude/hooks/lifecycle-guard.sh"
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
claude_agents = {path.stem: path for path in sorted(claude_agents_dir.glob("*.md"))}
codex_agents = {path.stem: path for path in sorted(codex_agents_dir.glob("*.toml"))}
for stem in sorted(set(claude_agents) - set(codex_agents)):
    fail(f"missing Codex agent mirror for .claude/agents/{stem}.md")
for stem in sorted(set(codex_agents) - set(claude_agents)):
    fail(f"Codex agent mirror has no .claude source: .codex/agents/{stem}.toml")

runtime_contract_phrases = [
    "## Runtime Bootstrap",
    "bootstrap -> preflight -> persona -> scope -> provider -> postflight",
    "## Guardrails",
    "## Handoff / Escalation",
    "postflight-checklist.md",
]
for stem, claude_path in sorted(claude_agents.items()):
    claude_text = read_text(claude_path)
    for phrase in runtime_contract_phrases:
        if phrase not in claude_text:
            fail(f"{rel(claude_path)} missing runtime contract phrase: {phrase}")

    codex_path = codex_agents.get(stem)
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
    for phrase in runtime_contract_phrases:
        if phrase not in codex_text:
            fail(f"{rel(codex_path)} missing runtime contract phrase: {phrase}")
    if extract_scope_imports(claude_text) != extract_scope_imports(codex_text):
        fail(f"scope import mismatch between {rel(claude_path)} and {rel(codex_path)}")

    if stem == "wiki-curator":
        for phrase in [
            "canonical owners without duplicating policy",
            "Do not create vector stores",
            "Target LLM Wiki path or generator command",
            "Keep policy and procedure changes in their canonical owner files",
        ]:
            if phrase not in claude_text or phrase not in codex_text:
                fail(f"wiki-curator mirror missing core guardrail phrase: {phrase}")

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
for script in sorted(scripts_dir.glob("*.sh")):
    if script.name not in scripts_readme:
        fail(f"script missing from scripts/README.md inventory: {script.name}")

script_ref_pattern = re.compile(r"scripts/[A-Za-z0-9_.-]+\.sh")
script_command_contract_paths = [
    root / "README.md",
    scripts_dir / "README.md",
    root / ".github/workflows/ci.yml",
    root / ".github/PULL_REQUEST_TEMPLATE.md",
    root / ".github/ABOUT.md",
    root / ".claude/settings.json",
    root / ".claude/CLAUDE.md",
    root / ".claude/hooks/post-validate.sh",
    root / ".claude/hooks/lifecycle-guard.sh",
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

inventory_path = root / "docs/90.references/versions/tech-stack-version-inventory.md"
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

if failures:
    print("=== validate-repo-quality-gates ===")
    for item in failures:
        print(item)
    sys.exit(1)

print("[PASS] repository quality gates passed")
PY
