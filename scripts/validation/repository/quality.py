#!/usr/bin/env python3
"""Validate repository-wide contracts not owned by a focused validator."""

import argparse
import ast
import collections
import json
import os
import pathlib
import re
import subprocess
import sys

import yaml

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path.cwd())
args = parser.parse_args()
root = args.root.resolve()

sys.path.insert(0, str(root / "scripts"))
from document_contracts import (  # noqa: E402 - repository-local contract module
    DocumentContractError,
    TARGET_ROOTS,
    classify_path,
    is_opaque_evaluation_output,
    verify_opaque_evaluation_output,
    load_registry,
)
from validation.current_executable_references import (  # noqa: E402
    executable_suffixes_from_registry,
    reachable_git_path_exists,
    validate_current_executable_references,
)
from validation.repository.form_contracts import (  # noqa: E402
    canonical_form_content_errors,
    canonical_form_contract_errors,
    collect_physical_form_paths,
)
from validation.repository.sample_app_contract import (  # noqa: E402
    sample_app_copyset_errors,
)
from validation.repository.bounded_io import (  # noqa: E402
    BoundedInputError,
    BoundedOutputError,
    read_bytes as read_bounded_bytes,
    read_text as read_bounded_text,
    run as run_bounded_process,
)

failures = []
MAX_REPOSITORY_INPUT_BYTES = 8 * 1024 * 1024
MAX_PROCESS_STDOUT_BYTES = 4 * 1024 * 1024
MAX_PROCESS_STDERR_BYTES = 512 * 1024


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


def display_path(path: pathlib.Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root).as_posix()
    except (OSError, ValueError):
        return path.name


def read_text(path: pathlib.Path) -> str:
    try:
        return read_bounded_text(path, max_bytes=MAX_REPOSITORY_INPUT_BYTES)
    except BoundedInputError:
        fail(f"{display_path(path)} is not a bounded strict UTF-8 regular file")
        return ""


def read_bytes(path: pathlib.Path) -> bytes:
    try:
        return read_bounded_bytes(path, max_bytes=MAX_REPOSITORY_INPUT_BYTES)
    except BoundedInputError:
        fail(f"{display_path(path)} is not a bounded regular file")
        return b""


def bounded_process(
    argv,
    *,
    cwd,
    timeout,
    input=None,
    text=False,
    capture_output=False,
    env=None,
    check=False,
    stdout=None,
):
    """Compatibility adapter for captured validation subprocesses."""

    if not capture_output and stdout is not subprocess.PIPE:
        raise ValueError("bounded process output must be captured")
    input_bytes = input.encode("utf-8") if text and input is not None else input
    try:
        completed = run_bounded_process(
            argv,
            cwd=pathlib.Path(cwd),
            env=env,
            input_bytes=input_bytes,
            timeout=timeout,
            stdout_limit=MAX_PROCESS_STDOUT_BYTES,
            stderr_limit=MAX_PROCESS_STDERR_BYTES,
        )
    except (BoundedOutputError, subprocess.TimeoutExpired, OSError, ValueError):
        fail(f"bounded subprocess failed: {pathlib.Path(argv[0]).name}")
        empty = "" if text else b""
        return subprocess.CompletedProcess(argv, 125, empty, empty)
    if check and completed.returncode:
        fail(f"bounded subprocess exited non-zero: {pathlib.Path(argv[0]).name}")
    if not text:
        return completed
    try:
        standard_output = completed.stdout.decode("utf-8", errors="strict")
        standard_error = completed.stderr.decode("utf-8", errors="strict")
    except UnicodeError:
        fail(f"bounded subprocess output is not UTF-8: {pathlib.Path(argv[0]).name}")
        standard_output = standard_error = ""
    return subprocess.CompletedProcess(
        argv,
        completed.returncode,
        standard_output,
        standard_error,
    )


def load_yaml(path: pathlib.Path):
    return yaml.load(read_text(path), Loader=DuplicateKeyLoader) or {}


def load_yaml_documents(path: pathlib.Path) -> list:
    return [
        document or {}
        for document in yaml.load_all(read_text(path), Loader=DuplicateKeyLoader)
    ]


def load_json(path: pathlib.Path):
    try:
        return json.loads(read_text(path))
    except (json.JSONDecodeError, ValueError):
        fail(f"{display_path(path)} is not valid JSON")
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


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(root))


def is_historical_evidence_path(path: pathlib.Path) -> bool:
    return path.is_relative_to(root / "docs/98.archive")


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
    match = re.search(
        r"allowed_branch_regex=['\"]\^\(([^)]+)\)/['\"]", branch_policy_text
    )
    if not match:
        return []
    return match.group(1).split("|")


def extract_pr_template_prefixes(text: str) -> list[str]:
    return [prefix.rstrip("/") for prefix in re.findall(r"`([a-z0-9-]+/)`", text)]


def has_provider_example_boundary_prompt(text: str) -> bool:
    required_terms = [
        "examples/aws",
        "examples/azure",
        "adjacent executable assets",
        "not live provider-latest guidance",
        "approved provider refresh spec",
    ]
    for line in text.splitlines():
        normalized = line.casefold()
        if all(term in normalized for term in required_terms):
            return True
    return False


tracked = set()
try:
    proc = bounded_process(
        ["git", "ls-files"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
        timeout=120,
    )
    tracked = set(proc.stdout.splitlines())
except Exception as exc:
    fail(f"git ls-files failed: {exc}")

for tracked_path in sorted(tracked):
    if re.fullmatch(r"\.claude/[^/]+\.local\.md", tracked_path):
        fail(
            f"ignored local Claude/Hookify runtime rule must not be tracked: {tracked_path}"
        )
    if tracked_path == ".env":
        fail(".env must remain untracked; commit .env.example only")
    tracked_name = pathlib.Path(tracked_path).name
    if tracked_name == "progress.md":
        fail(f"retired progress ledger must remain untracked: {tracked_path}")
    if re.search(r"(^temp_|_(new|old|backup)(\.|$))", tracked_name):
        fail(
            f"tracked temporary or backup-style file name is not allowed: {tracked_path}"
        )

requirements_stage = root / "docs/01.requirements"
if requirements_stage.exists():
    for requirement_doc in sorted(requirements_stage.glob("*.md")):
        if requirement_doc.name == "README.md":
            continue
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+\.md", requirement_doc.name):
            fail(
                "active PRDs must use numeric route "
                f"docs/01.requirements/<####-numbering>-<feature-or-system>.md: {rel(requirement_doc)}"
            )
        if not re.fullmatch(r"\d{4}-.+\.md", requirement_doc.name):
            fail(
                "active PRD filename must start with a four-digit numeric prefix: "
                f"{rel(requirement_doc)}"
            )

specs_stage = root / "docs/03.specs"
if specs_stage.exists():
    for spec_entry in sorted(specs_stage.iterdir()):
        if spec_entry.name == "README.md":
            continue
        if spec_entry.is_dir():
            if not re.fullmatch(r"\d{4}-.+", spec_entry.name):
                fail(
                    "active Spec folder must start with a four-digit numeric prefix: "
                    f"{rel(spec_entry)}"
                )
            continue
        if spec_entry.is_file():
            fail(
                f"docs/03.specs may contain only README.md and numbered Spec folders: {rel(spec_entry)}"
            )

env_ignore_check = subprocess.run(
    ["git", "check-ignore", "-q", ".env"], cwd=root, timeout=120
)
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
    duplicated_example_keys = sorted(
        key for key, count in collections.Counter(env_example_keys).items() if count > 1
    )
    if duplicated_example_keys:
        fail(
            ".env.example contains duplicate keys: "
            + ", ".join(duplicated_example_keys)
        )
    if env_path.exists():
        env_keys = parse_env_keys(env_path)
        duplicated_env_keys = sorted(
            key for key, count in collections.Counter(env_keys).items() if count > 1
        )
        if duplicated_env_keys:
            fail(".env contains duplicate keys: " + ", ".join(duplicated_env_keys))
        missing_env_keys = sorted(set(env_example_keys) - set(env_keys))
        extra_env_keys = sorted(set(env_keys) - set(env_example_keys))
        if missing_env_keys:
            fail(
                ".env is missing keys from .env.example: " + ", ".join(missing_env_keys)
            )
        if extra_env_keys:
            fail(
                ".env has keys not present in .env.example: "
                + ", ".join(extra_env_keys)
            )


claude_local_rule_paths = sorted((root / ".claude").glob("*.local.md"))
for local_rule_path in claude_local_rule_paths:
    local_rule_rel = rel(local_rule_path)
    local_rule_ignore_check = subprocess.run(
        ["git", "check-ignore", "-q", local_rule_rel], cwd=root, timeout=120
    )
    if local_rule_ignore_check.returncode == 1:
        fail(f"{local_rule_rel} must remain ignored by Git")
    elif local_rule_ignore_check.returncode not in {0, 1}:
        fail(
            f"git check-ignore failed while validating local rule ignore contract: {local_rule_rel}"
        )

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
            fail(
                f"{local_rule_rel} has unsupported Hookify event: {metadata.get('event')}"
            )
        if "action" in metadata and metadata.get("action") not in {"warn", "block"}:
            fail(
                f"{local_rule_rel} has unsupported Hookify action: {metadata.get('action')}"
            )
        if "pattern" not in metadata and "conditions" not in metadata:
            fail(f"{local_rule_rel} must define Hookify pattern or conditions")

allowed_top_level_docs = {
    "01.requirements",
    "02.architecture",
    "03.specs",
    "05.operations",
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
for name in sorted(actual_docs - allowed_top_level_docs):
    fail(f"docs top-level folder is not allowed: docs/{name}")
for name in sorted(allowed_top_level_docs - actual_docs):
    fail(f"required docs top-level folder is missing: docs/{name}")

for provider in ["aws", "azure"]:
    example_docs = root / "examples" / provider / "docs"
    if example_docs.exists():
        fail(
            f"retired example docs root must be absent after ADM-006: {rel(example_docs)}"
        )

sample_app_dir = root / "examples/sample-app"
sample_app_kustomization = sample_app_dir / "kustomization.yaml"
sample_app_source = read_text(sample_app_kustomization)
sample_app_resources = load_yaml(sample_app_kustomization)
sample_app_yaml = {
    path.name for path in sample_app_dir.iterdir() if path.suffix in {".yaml", ".yml"}
}
for path in sample_app_dir.iterdir():
    if path.suffix in {".yaml", ".yml"} and (path.is_symlink() or not path.is_file()):
        fail("examples/sample-app YAML copy member must be a regular file")
for error in sample_app_copyset_errors(
    sample_app_yaml, sample_app_resources, sample_app_source
):
    fail(error)

for active_reference_file in [
    "service-stable.yaml",
    "service-canary.yaml",
    "virtual-service.yaml",
    "destination-rule.yaml",
    "peer-authentication.yaml",
]:
    if not (root / "gitops/workloads/adminer" / active_reference_file).is_file():
        fail(
            f"gitops/workloads/adminer missing fuller active reference file: {active_reference_file}"
        )

sample_app_external_secret = read_text(sample_app_dir / "external-secret.yaml")
for phrase in [
    "secret/apps/<appname>/config",
    "remoteRef.key",
    "apps/<appname>/config",
    "ClusterSecretStore path",
]:
    if phrase not in sample_app_external_secret:
        fail(
            f"examples/sample-app/external-secret.yaml missing app secret path contract phrase: {phrase}"
        )
if "key: secret/apps/<appname>/config" in sample_app_external_secret:
    fail(
        "examples/sample-app/external-secret.yaml remoteRef.key must exclude the Vault mount prefix"
    )

github_native_markdown = [
    root / ".github/PULL_REQUEST_TEMPLATE.md",
    root / ".github/SECURITY.md",
]
for github_doc in github_native_markdown:
    if github_doc.exists() and has_markdown_frontmatter(github_doc):
        fail(f"{rel(github_doc)} must remain frontmatter-free GitHub-native Markdown")


document_registry = load_registry(root)
template_locations = {}
for profile in document_registry.profiles:
    if profile.template is None:
        continue
    location = profile.template.relative_to("docs/99.templates")
    existing = template_locations.get(profile.template.name)
    if existing is not None and existing != location.as_posix():
        fail(
            "registry template basenames must be unique: "
            f"{profile.template.name}: {existing}, {location.as_posix()}"
        )
    template_locations[profile.template.name] = location.as_posix()


def template_path(template_name: str) -> pathlib.Path:
    location = template_locations.get(template_name)
    if not location:
        fail(f"template mapping points to an unknown template: {template_name}")
    return root / "docs/99.templates" / location


template_root = root / "docs/99.templates/templates"


physical_form_paths = collect_physical_form_paths(root, template_root)
registry_form_references = [
    (profile.profile_id, profile.template)
    for profile in document_registry.profiles
    if profile.template is not None
]
registry_profiles_by_id = {
    profile.profile_id: profile for profile in document_registry.profiles
}


def is_derived_template_profile(profile) -> bool:
    if profile.mode != "template" or not profile.source_profile_ids:
        return False
    source_profiles = [
        registry_profiles_by_id.get(source_id)
        for source_id in profile.source_profile_ids
    ]
    return any(
        source_profile is not None and source_profile.template == profile.template
        for source_profile in source_profiles
    )


registry_form_owners = [
    (profile.profile_id, profile.template)
    for profile in document_registry.profiles
    if profile.template is not None and not is_derived_template_profile(profile)
]


canonical_form_errors = canonical_form_contract_errors(
    physical_form_paths,
    registry_form_references,
    registry_form_owners,
)
for error in canonical_form_errors:
    fail(error)


form_sources = {
    form_path: read_text(root / form_path) for form_path in physical_form_paths
}
for error in canonical_form_content_errors(
    form_sources, registry_form_owners, registry_profiles_by_id
):
    fail(error)


template_support_root = root / "docs/99.templates/support"
if template_support_root.exists():
    fail("docs/99.templates/support is a retired transition surface")


def canonical_markdown_owns_generic_residue(path: pathlib.Path) -> bool:
    try:
        profile = classify_path(
            document_registry,
            pathlib.PurePosixPath(rel(path)),
        )
    except DocumentContractError:
        return False
    if profile.placeholder_policy != "forbidden":
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
tracked_active_paths = bounded_process(
    ["git", "-C", str(root), "ls-files", "-z"],
    cwd=root,
    stdout=subprocess.PIPE,
    timeout=120,
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
        relative_path.as_posix() in {"README.md", "AGENTS.md", "CLAUDE.md"}
        or relative_path.parts[0] in TARGET_ROOTS
    ):
        continue
    path = root / relative_path
    if (
        path.suffix not in active_residue_suffixes
        or not path.is_file()
        or path.is_symlink()
    ):
        continue
    if path.is_relative_to(root / "docs/99.templates/templates"):
        continue
    if path.is_relative_to(root / "tests/fixtures"):
        continue
    if is_historical_evidence_path(path):
        continue
    if path.suffix == ".md" and canonical_markdown_owns_generic_residue(path):
        continue
    for line_number in generic_template_residue_lines(read_text(path)):
        fail(f"active non-structural template residue in {rel(path)}:{line_number}")

reference_template_path = template_path("research.template.md")
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


active_template_routing_reference_files = [
    root / ".agents/skills/docs-stage-routing/SKILL.md",
    root / "scripts/provider_write_guard.py",
]
for path in active_template_routing_reference_files:
    text = read_text(path)
    if "99.templates/registry.json" not in text:
        fail(
            f"{rel(path)} must route exact template selection through docs/99.templates/registry.json"
        )

legacy_denylist_literals = {
    "operation" + ".template.md": "deprecated operations policy template route",
    "platform" + "-" + "team": "deprecated owner value",
    "Related " + "References": "deprecated README related-document heading",
}
legacy_scan_roots = [
    root / "docs",
    root / ".agents",
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
        if candidate.suffix not in legacy_scan_suffixes and candidate.name not in {
            "AGENTS.md",
            "RTK.md",
        }:
            continue
        text = read_text(candidate)
        for literal, replacement in legacy_denylist_literals.items():
            if literal in text:
                fail(f"{rel(candidate)} contains {replacement} literal: {literal}")

legacy_postmortems = "11" + ".postmortems"
legacy_learning = "50" + ".Learning"
legacy_stage_range = "00" + "~" + "11"
legacy_docs_range = "01" + "~" + "99"
legacy_stage_label = "Stage " + "11"
legacy_harness = "H" + "100"
legacy_harness_examples = "examples/" + "harness-100"
old_docs_path_refs = ["docs/" + name for name in sorted(old_top_level_docs)] + [
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
# `str(root)` catches a direct run, but `scripts/qa.py` always hands this
# validator an isolated snapshot directory, so that entry can never match the
# real checkout path. Match an absolute filesystem path that ends at this
# repository's own directory name instead, which holds under any root. The
# lookbehind keeps a remote URL such as `https://github.com/owner/hy-home.k8s.git`
# out, because a URL is an identity rather than a machine-local path.
local_checkout_path = re.compile(
    r"(?<![\w:/])/(?:[^\s`'\"()]+/)?hy-home\.k8s(?![\w.-])"
)
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
for scan_root in scan_roots:
    candidates = [scan_root] if scan_root.is_file() else scan_root.rglob("*")
    for path in candidates:
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".toml", ".json", ".yml", ".yaml", ".sh"}:
            continue
        text = read_text(path)
        for pattern in stale_patterns:
            if pattern in text:
                fail(f"stale docs path reference found in {rel(path)}: {pattern}")
        if local_checkout_path.search(text):
            fail(f"local checkout path found in {rel(path)}")
        for pattern in legacy_contract_patterns:
            if pattern in text and not any(
                marker in text for marker in legacy_contract_markers
            ):
                fail(
                    f"legacy runtime contract reference lacks historical/superseded note in {rel(path)}: {pattern}"
                )

active_stale_contract_roots = [
    root / "docs/01.requirements",
    root / "docs/02.architecture",
    root / "docs/03.specs",
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
    root / "docs/05.operations",
    root / "docs/90.references",
]
migration_evidence_ledger_path = (
    root
    / "docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md"
)


def is_currentness_evidence_only(path: pathlib.Path) -> bool:
    return path == migration_evidence_ledger_path


if not is_currentness_evidence_only(migration_evidence_ledger_path):
    fail("migration evidence ledger currentness exception must match its exact path")
if is_currentness_evidence_only(root / "docs/90.references/README.md"):
    fail("migration evidence ledger currentness exception must not widen to Stage 90")

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
        if stale_shell_job_name in text:
            fail(f"active authored docs must not list stale CI job name in {rel(path)}")
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


git_push_pattern = re.compile(r"\bgit\s+push\b")


def is_inert_prohibition(line: str, pattern: re.Pattern, markdown_prose: bool) -> bool:
    if not markdown_prose:
        return False
    label = re.match(r"^ {0,3}(?:[-*+]\s+)?(?:prohibited-example|do-not-run):", line)
    if not label:
        return False
    quoted = list(re.finditer(r"(?<!`)`([^`\n]+)`(?!`)", line))
    if not any(
        match.start() >= label.end() and pattern.search(match.group(1))
        for match in quoted
    ):
        return False
    unquoted = re.sub(r"(?<!`)`[^`\n]+`(?!`)", "", line)
    return not pattern.search(unquoted)


def is_bare_or_main_push(line: str, markdown_prose: bool) -> bool:
    stripped = line.strip()
    return (
        stripped == "git push" or "git push origin main" in stripped
    ) and not is_inert_prohibition(line, git_push_pattern, markdown_prose)


def is_unmarked_command(
    lines: list[str],
    index: int,
    label: str,
    pattern: re.Pattern,
    markers: list[str],
    markdown_prose: bool,
) -> bool:
    return bool(
        pattern.search(lines[index])
        and not is_inert_prohibition(lines[index], pattern, markdown_prose)
        and (
            label == "kubectl get secret yaml/json"
            or not has_nearby_marker(lines, index, markers)
        )
    )


allowed_push_branch = re.compile(
    r"\bgit\s+push\s+origin\s+(?:feat|fix|docs|refactor|chore|ci|release|hotfix|codex|dependabot)/\S+"
)


command_boundary_rules = [
    (
        "kubectl apply/patch",
        re.compile(r"\bkubectl\b.*\b(?:apply|patch)\b"),
        [
            "human-approved",
            "break-glass",
            "bootstrap-only",
            "bootstrap only",
            "operator-approved",
            "dry-run",
        ],
    ),
    (
        "kubectl create clusterrolebinding",
        re.compile(r"\bkubectl\b.*\bcreate\s+clusterrolebinding\b"),
        [
            "human-approved",
            "break-glass",
            "bootstrap-only",
            "bootstrap only",
            "operator-approved",
            "dry-run",
        ],
    ),
    (
        "kubectl get secret yaml/json",
        re.compile(
            r"\bkubectl\b.*\bget\s+secrets?\b.*"
            r"\s(?:-o(?:=|\s*)|--output(?:=|\s+))"
            r"(?:(['\"])(?:yaml|json)\1(?!\w)|(?:yaml|json)\b)"
        ),
        [],
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
        [
            "external secret operation",
            "operator-approved",
            "human-approved",
            "break-glass",
        ],
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
        [
            "human-approved",
            "break-glass",
            "bootstrap-only",
            "bootstrap only",
            "operator-approved",
        ],
    ),
    (
        "kubeconfig mutation",
        re.compile(
            r"\b(?:aws\s+eks\s+update-kubeconfig|az\s+aks\s+get-credentials|kubectl\s+config)\b"
        ),
        ["--kubeconfig", "--file", "temporary kubeconfig", "임시 kubeconfig"],
    ),
]

command_boundary_roots = authored_command_roots + [root / "examples"]
for command_root in command_boundary_roots:
    candidates = (
        command_root.rglob("*")
        if command_root == root / "examples"
        else command_root.rglob("*.md")
    )
    for path in sorted(candidates):
        if not path.is_file():
            continue
        if command_root == root / "examples" and path.suffix not in {
            ".md",
            ".yaml",
            ".yml",
            ".sh",
            ".tf",
            ".bicep",
        }:
            continue
        lines = read_text(path).splitlines()
        visible_indices = (
            {index for index, _ in visible_markdown_lines("\n".join(lines))}
            if path.suffix == ".md"
            else set()
        )
        for index, line in enumerate(lines):
            markdown_prose = index in visible_indices
            if is_bare_or_main_push(line, markdown_prose):
                fail(
                    f"{rel(path)} contains bare/main direct push example; use feature branch + PR flow: line {index + 1}"
                )
            elif git_push_pattern.search(line) and not is_inert_prohibition(
                line, git_push_pattern, markdown_prose
            ):
                if not allowed_push_branch.search(line) or not is_pr_flow_push(
                    lines, index
                ):
                    fail(
                        f"{rel(path)} contains push example without nearby PR-flow context: line {index + 1}"
                    )
            for label, pattern, markers in command_boundary_rules:
                if is_unmarked_command(
                    lines, index, label, pattern, markers, markdown_prose
                ):
                    fail(
                        f"{rel(path)} has unmarked {label} example near line {index + 1}"
                    )

markdown_direct_push_roots = [
    root / "README.md",
    root / "docs/README.md",
    root / "gitops",
    root / "infrastructure",
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
        visible_indices = {
            index for index, _ in visible_markdown_lines("\n".join(lines))
        }
        for index, line in enumerate(lines):
            if is_bare_or_main_push(line, index in visible_indices):
                fail(
                    f"{rel(path)} contains bare/main direct push example; use feature branch + PR flow: line {index + 1}"
                )

docs_readme_path = root / "docs/README.md"
docs_readme_text = read_text(docs_readme_path)
for phrase in [
    "## 문서 역할과 언어 계약",
    "AI Agent Requirements",
    "사람이 읽는 안내와 요약은 한국어를 우선",
]:
    if phrase not in docs_readme_text:
        fail(
            f"{rel(docs_readme_path)} missing docs language/template contract phrase: {phrase}"
        )

workflow_paths = sorted((root / ".github").glob("**/*.yml")) + sorted(
    (root / ".github").glob("**/*.yaml")
)
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
            label = (
                step.get("name")
                or step.get("uses")
                or (step.get("run") or "").strip().splitlines()[0:1]
            )
            if isinstance(label, list):
                label = label[0] if label else "<unnamed>"
            seen[str(label)] += 1
        for label, count in seen.items():
            if label and label != "<unnamed>" and count > 1:
                fail(
                    f"duplicate workflow step in {rel(workflow)} job {job_id}: {label}"
                )

codeowners_path = root / ".github/CODEOWNERS"
codeowners_text = read_text(codeowners_path)
if not re.search(r"^/\.github/\s+@buenhyden(?:\s|$)", codeowners_text, re.MULTILINE):
    fail(".github/CODEOWNERS must assign /.github/ ownership to @buenhyden")

pull_request_template_path = root / ".github/PULL_REQUEST_TEMPLATE.md"
pull_request_template_text = read_text(pull_request_template_path)
for phrase in [
    "NOT_RUN",
    "- [ ] Every validation lane is explicitly classified as `PASS`, `NOT_RUN`, `FAIL`, `DEFER`, or `NOT_APPLICABLE`.",
]:
    if phrase not in pull_request_template_text:
        fail(f"{rel(pull_request_template_path)} missing QA evidence phrase: {phrase}")

ci_path = root / ".github/workflows/ci.yml"
try:
    ci_data = load_yaml(ci_path)
except Exception as exc:
    fail(f"CI workflow parse failed for {rel(ci_path)}: {exc}")
    ci_data = {}

# The focused CI contract owns triggers, one-job topology and failure propagation.
# This owner checks consistency between executable branch vocabulary and docs.
ci_jobs = ci_data.get("jobs") or {}
summary_job = ci_jobs.get("ci-summary") or {}
branch_policy_text = "\n".join(
    str(step.get("run") or "") for step in summary_job.get("steps") or []
)
for phrase in [
    "BASE_REF",
    "HEAD_REF",
    "allowed_branch_regex",
    "PR base branch must be main",
    "branch-policy result=",
]:
    if phrase not in branch_policy_text:
        fail(f"{rel(ci_path)} ci-summary missing validation phrase: {phrase}")

branch_prefixes = extract_ci_branch_policy_prefixes(branch_policy_text)
if not branch_prefixes:
    fail(f"{rel(ci_path)} ci-summary must define supported branch prefixes")
expected_branch_message = (
    "PR source branch must start with one of: "
    + format_branch_prefixes(branch_prefixes)
)
if expected_branch_message not in branch_policy_text:
    fail(f"{rel(ci_path)} ci-summary message must match its allowed_branch_regex")

pr_template_path = root / ".github/PULL_REQUEST_TEMPLATE.md"
pr_template_text = read_text(pr_template_path)

for phrase in [
    "Workflow triggers and job ownership reviewed",
    "No live cluster mutation",
    "approved prefix",
    "`main`",
]:
    if phrase not in pr_template_text:
        fail(f"{rel(pr_template_path)} missing GitHub/GitOps review phrase: {phrase}")
for phrase in [
    "any exception must update CI `ci-summary` and governance in the same change",
    "No PR targeting `main` bypasses the CI metadata check",
    "Draft/WIP status is intentional",
    "`test`: Tests or validation updates",
    "`chore`: Maintenance updates",
    "[`.cz.toml`](../.cz.toml)",
]:
    if phrase not in pr_template_text:
        fail(f"{rel(pr_template_path)} missing CI metadata clarification: {phrase}")
if not has_provider_example_boundary_prompt(pr_template_text):
    fail(
        f"{rel(pr_template_path)} missing provider example checklist line with "
        "examples/aws, examples/azure, adjacent executable assets, provider-latest, "
        "and approved provider refresh spec terms"
    )

# Harness implementation surfaces: existence and cross-reference contracts only.
# Wrapper script existence is already enforced by the scripts inventory, so it
# is not re-validated here.
approval_boundaries_path = root / ".agents/governance/approval-and-safety.md"
if not approval_boundaries_path.exists():
    fail(f"required harness surface is missing: {rel(approval_boundaries_path)}")
if "## 8. Harness Impact" not in pr_template_text:
    fail(
        f"{rel(pr_template_path)} missing Harness Impact section heading: ## 8. Harness Impact"
    )
canonical_task_form_text = read_text(
    root / "docs/99.templates/templates/specs/task.template.md"
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
        f"{rel(pr_template_path)} approved branch prefixes must match {rel(ci_path)} ci-summary "
        f"SSoT: expected {format_branch_prefixes(branch_prefixes)} got {format_branch_prefixes(pr_branch_prefixes)}"
    )
for prefix in branch_prefixes:
    prefix_label = f"{prefix}/"
    if prefix not in pr_template_text:
        fail(
            f"{rel(pr_template_path)} missing approved source branch prefix from "
            f"{rel(ci_path)} ci-summary: {prefix_label}"
        )

labeler_path = root / ".github/labeler.yml"
labeler_data = load_yaml(labeler_path)
test_label_globs = set(collect_strings(labeler_data.get("area/tests") or []))
for expected_glob in ["tests/**", "infrastructure/verify/**"]:
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
            fail(
                f"{rel(workflow)} contains forbidden live mutation or publish command: {command}"
            )

    try:
        workflow_data = load_yaml(workflow)
    except Exception:
        continue
    if workflow.name == "labeler.yml" and "concurrency" not in workflow_data:
        fail(f"{rel(workflow)} must declare workflow-level concurrency")
    for job_id, job in (workflow_data.get("jobs") or {}).items():
        if "timeout-minutes" not in job:
            fail(f"{rel(workflow)} job {job_id} must declare timeout-minutes")
        for step in job.get("steps") or []:
            run_block = str(step.get("run") or "")
            if re.search(r"\$\{\{\s*needs(?:\.|\[)[^}]*\.result\s*\}\}", run_block):
                fail(
                    f"{rel(workflow)} job {job_id} run block expands needs.*.result directly"
                )

# Native metadata/permission/hook registration belongs to agent-governance.
# tests.test_k8s_pre_edit_hook owns path/root/denial behavior independently.

scripts_dir = root / "scripts"
tracked_script_paths = sorted(
    root / tracked_path
    for tracked_path in tracked
    if pathlib.PurePosixPath(tracked_path).parent == pathlib.PurePosixPath("scripts")
    and pathlib.PurePosixPath(tracked_path).suffix in {".py", ".sh"}
)
for script_path in tracked_script_paths:
    if script_path.suffix != ".py":
        continue
    if not script_path.is_file():
        fail(f"tracked Python script is missing from the worktree: {rel(script_path)}")
        continue
    try:
        ast.parse(read_text(script_path), filename=rel(script_path))
    except SyntaxError as exc:
        fail(f"tracked Python script syntax failed for {rel(script_path)}: {exc.msg}")

script_paths = sorted(scripts_dir.glob("*.sh"))
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
    for pattern in disallowed_script_absolute_path_patterns:
        if pattern.search(script_text):
            fail(f"{rel(script)} contains a hardcoded absolute machine path")

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
kube_linter_exclusions = (kube_linter_config.get("checks") or {}).get("exclude") or []
if kube_linter_exclusions != expected_kube_linter_exclusions:
    fail(
        ".kube-linter.yaml checks.exclude must match the documented exclusion order: "
        + ", ".join(expected_kube_linter_exclusions)
    )

kube_linter_text = read_text(kube_linter_config_path)
for exclusion in expected_kube_linter_exclusions:
    match = re.search(
        rf'^\s*-\s+"{re.escape(exclusion)}"\s+#\s*(.+)$', kube_linter_text, re.MULTILINE
    )
    if not match:
        fail(
            f".kube-linter.yaml exclusion must have an inline rationale comment: {exclusion}"
        )
        continue
    rationale = match.group(1).strip()
    if len(rationale) < 12 or "TODO" in rationale or "TBD" in rationale:
        fail(f".kube-linter.yaml exclusion rationale is too weak: {exclusion}")

gitops_dir = root / "gitops"


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
            if key in {
                "containers",
                "initContainers",
                "ephemeralContainers",
            } and isinstance(item, list):
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


def collect_container_image_entries(
    scope: pathlib.Path,
) -> list[tuple[pathlib.Path, str]]:
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
            fail(
                f"{rel(path)} contains a container image field that is not a nonempty string"
            )
            continue
        if image_uses_latest(image):
            fail(f"{rel(path)} must not use latest container image tag: {image}")
        if not image_has_explicit_version(image):
            fail(
                f"{rel(path)} container image must use an explicit tag or sha256 digest: {image}"
            )

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
    fail(
        "gitops/clusters/local/appproject-apps.yaml clusterResourceWhitelist must be empty"
    )
if not apps_namespace_kind_whitelist:
    fail(
        "gitops/clusters/local/appproject-apps.yaml namespaceResourceWhitelist must not be empty"
    )
for kind in sorted(workload_manifest_kinds - apps_namespace_kind_whitelist):
    fail(
        f"gitops/workloads manifest kind is not allowed by apps AppProject namespaceResourceWhitelist: {kind}"
    )

policy_apps_namespace_kinds = {"ExternalSecret"}
expected_apps_namespace_kind_whitelist = (
    workload_manifest_kinds | policy_apps_namespace_kinds
)
if apps_namespace_kind_whitelist != expected_apps_namespace_kind_whitelist:
    fail(
        "gitops/clusters/local/appproject-apps.yaml namespaceResourceWhitelist must equal "
        "active workload kinds plus policy-optional ExternalSecret: "
        + ", ".join(sorted(expected_apps_namespace_kind_whitelist))
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
            create_namespace_applications.append(
                (path, name, namespace if isinstance(namespace, str) else "")
            )
    elif kind == "ApplicationSet":
        template_spec = (
            ((document.get("spec") or {}).get("template") or {}).get("spec")
        ) or {}
        destination = template_spec.get("destination") or {}
        namespace = destination.get("namespace")
        if has_sync_option(template_spec, "CreateNamespace=true"):
            create_namespace_application_sets.append(
                (path, name, namespace if isinstance(namespace, str) else "")
            )

namespace_manifest_files: dict[str, str] = {}
for path, document in gitops_yaml_documents_under(gitops_dir / "platform/namespaces"):
    if document.get("kind") == "Namespace":
        namespace_name = (document.get("metadata") or {}).get("name")
        if isinstance(namespace_name, str) and namespace_name:
            namespace_manifest_files[namespace_name] = rel(path)

if create_namespace_applications or create_namespace_application_sets:
    for _, name, namespace in (
        create_namespace_applications + create_namespace_application_sets
    ):
        fail(
            f"GitOps Application/ApplicationSet must not use CreateNamespace=true: {name} -> {namespace}"
        )

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
        template_spec = (
            ((document.get("spec") or {}).get("template") or {}).get("spec")
        ) or {}
        destination = template_spec.get("destination") or {}
        namespace = destination.get("namespace")
        if (
            rel(path) == "gitops/clusters/local/applicationset-apps.yaml"
            and isinstance(namespace, str)
            and namespace
        ):
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

infrastructure_dir = root / "infrastructure"
infrastructure_shell_paths = sorted(
    [infrastructure_dir / "bootstrap-local.sh"]
    + list((infrastructure_dir / "verify").glob("*.sh"))
)
for script in infrastructure_shell_paths:
    if not script.exists():
        fail(f"infrastructure shell entrypoint is missing: {rel(script)}")
        continue
    if not os.access(script, os.X_OK):
        fail(f"infrastructure shell entrypoint must be executable: {rel(script)}")
    if not read_text(script).startswith("#!/usr/bin/env bash\n"):
        fail(
            f"infrastructure shell entrypoint must start with bash shebang: {rel(script)}"
        )

# ADR-0043 retired the external Traefik reference files; k8s routes are
# Ingress objects served by the dedicated k8s router.
if (root / "traefik").exists():
    fail("traefik/ was retired by ADR-0043; declare k8s routes as Ingress objects")

executable_reference_source_suffixes = {
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
executable_reference_sources = {}
for tracked_path in sorted(tracked):
    if tracked_path.startswith(("docs/98.archive/", "tests/fixtures/")):
        continue
    path = root / tracked_path
    if (
        not path.is_file()
        or path.is_symlink()
        or path.suffix not in executable_reference_source_suffixes
    ):
        continue
    source_path = pathlib.PurePosixPath(tracked_path)
    if source_path.suffix == ".md":
        try:
            if is_opaque_evaluation_output(document_registry, source_path):
                verify_opaque_evaluation_output(root, source_path)
                continue
        except DocumentContractError:
            # The document-profile gate reports unsupported current paths.
            pass
    executable_reference_sources[pathlib.PurePosixPath(tracked_path)] = read_text(path)

validation_surface_contract = load_json(root / "scripts/validation/registry.json")
try:
    executable_suffixes = executable_suffixes_from_registry(validation_surface_contract)
except ValueError as exc:
    fail(f"validation executable suffix ownership differs: {exc}")
    executable_suffixes = frozenset()

executable_reference_diagnostics = (
    validate_current_executable_references(
        root,
        tracked_paths=frozenset(pathlib.PurePosixPath(path) for path in tracked),
        source_texts=executable_reference_sources,
        executable_suffixes=executable_suffixes,
        historical_path_exists=lambda target: reachable_git_path_exists(root, target),
    )
    if executable_suffixes
    else ()
)
for diagnostic in executable_reference_diagnostics:
    fail(str(diagnostic))

secret_scanner_text = read_text(scripts_dir / "check-secret-handling.sh")
for phrase in [
    "examples/sample-app",
    '-name "gitops"',
    '-name "kubernetes"',
    "value=<redacted>",
]:
    if phrase not in secret_scanner_text:
        fail(
            f"{rel(scripts_dir / 'check-secret-handling.sh')} missing examples secret-scan contract phrase: {phrase}"
        )

for obsolete in ["k3d_kubeconfig.yaml"]:
    if obsolete in tracked:
        fail(f"obsolete tracked file remains: {obsolete}")
for tracked_path in tracked:
    if tracked_path.startswith(
        "docs/" + legacy_postmortems + "/"
    ) or tracked_path.startswith("docs/" + legacy_learning + "/"):
        fail(f"obsolete tracked docs path remains: {tracked_path}")


if failures:
    print("=== repository quality ===")
    for item in failures:
        print(item)
    sys.exit(1)

print("[PASS] repository quality gates passed")
