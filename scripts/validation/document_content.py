"""Current README matrix relationships selected by the Markdown document gate.

The document registry owns profiles and forms. This module checks relationships
between a few current router tables and the repository entries they describe.
It neither reads raw evaluation output nor grades a historical document.
"""

from __future__ import annotations

import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Sequence

from validation.repository.bounded_io import (
    BoundedInputError,
    open_parent,
    read_text as bounded_read_text,
    stable_file_state,
)


Table = tuple[list[str], list[list[str]]]
TableReader = Callable[[str, str], Table | None]
Finding = tuple[str, str, str]


@dataclass(frozen=True)
class Matrix:
    title: str
    header: tuple[str, ...]
    source: str
    expected: tuple[str, ...] = ()
    key_columns: tuple[int, ...] = (0,)


AREA_HEADER = (
    "Area",
    "Purpose and owner",
    "Lifecycle and config",
    "Dependencies, routes, secrets",
    "Validation and operations",
)
GITOPS_MATRIXES = (
    Matrix(
        "Service Coverage Matrix",
        AREA_HEADER,
        "gitops-service",
        ("clusters/local", "apps/root"),
    ),
    Matrix(
        "External Service Contract Matrix",
        (
            "Contract",
            "Host / service",
            "Port",
            "Database or Vault path",
            "Secret keys",
            "TLS / CA",
            "Rotation responsibility",
            "Namespace convention",
            "Validation",
        ),
        "fixed",
        ("Vault API", "Valkey auth"),
    ),
    Matrix(
        "Secret Management Responsibility Matrix",
        (
            "Responsibility",
            "Source / auth contract",
            "Destination / naming rule",
            "Owner boundary",
            "Value handling",
            "Validation",
        ),
        "fixed",
        (
            "ClusterSecretStore vault-backend",
            "ArgoCD argocd-external-valkey",
            "ArgoCD argocd-notifications-secret",
            "Sample app ExternalSecret",
        ),
    ),
    Matrix(
        "AppProject Allow-list Rationale Matrix",
        (
            "Project",
            "Allow-list surface",
            "Current allowed kinds",
            "Evidence class",
            "Tightening boundary",
            "Validation",
        ),
        "fixed",
        (
            "apps|clusterResourceWhitelist",
            "apps|active namespaceResourceWhitelist",
            "apps|policy namespaceResourceWhitelist",
            "platform|platform AppProject allow-lists",
        ),
        (0, 1),
    ),
    Matrix(
        "Workload Image and Kind Policy Matrix",
        (
            "Surface",
            "Current image policy",
            "Resource-kind policy",
            "Current evidence",
            "Deferred boundary",
            "Validation",
        ),
        "fixed",
        ("gitops/workloads/*", "gitops/platform/*", "examples/sample-app/*"),
    ),
    Matrix(
        "Namespace Ownership Matrix",
        (
            "Surface",
            "Namespace surface",
            "Declared namespace owner",
            "Current behavior",
            "Remaining boundary",
            "Validation",
        ),
        "fixed",
        ("root Application", "apps ApplicationSet", "platform root Applications"),
    ),
)
INFRA_MATRIXES = (
    Matrix("Infrastructure Coverage Matrix", AREA_HEADER, "infrastructure"),
    Matrix(
        "Host Runtime Prerequisite Matrix",
        (
            "Prerequisite",
            "Repository SSoT",
            "Owner / responsibility",
            "Validation / evidence",
            "Failure boundary",
        ),
        "fixed",
        (
            "Host shell and Docker context",
            "kubectl and k3d context",
            "kubeconfig and TLS trust",
            "Port and network contracts",
            "Host networking constraints",
        ),
    ),
    Matrix(
        "Bootstrap Boundary Matrix",
        (
            "Boundary",
            "Repository responsibility",
            "Operator / external responsibility",
            "Allowed command surface",
            "Verification / evidence",
            "Failure boundary",
        ),
        "fixed",
        (
            "k3d cluster creation",
            "ArgoCD installation",
            "root app application",
            "Vault connection contract",
            "PostgreSQL and Valkey connection contract",
        ),
    ),
)
MATRIXES: dict[str, tuple[Matrix, ...]] = {
    "examples/README.md": (
        Matrix(
            "Example Role Matrix",
            (
                "Example path",
                "Role",
                "Active source of truth",
                "Validation",
            ),
            "examples",
        ),
    ),
    ".github/repository-surface.md": (
        Matrix(
            "Workflow Responsibility Matrix",
            (
                "Workflow",
                "Role",
                "Trigger / scope",
                "Required evidence",
                "Boundary",
            ),
            "workflows",
        ),
    ),
    "gitops/README.md": GITOPS_MATRIXES,
    "gitops/platform/README.md": (
        Matrix("Platform Coverage Matrix", AREA_HEADER, "platform"),
    ),
    "gitops/workloads/README.md": (
        Matrix(
            "Workload Coverage Matrix",
            (
                "Workload",
                "Purpose and owner",
                "Lifecycle and config",
                "Dependencies, routes, secrets",
                "Validation and operations",
            ),
            "workloads",
        ),
    ),
    "infrastructure/README.md": INFRA_MATRIXES,
    "infrastructure/verify/README.md": (
        Matrix(
            "Infrastructure Test Inventory",
            (
                "Test script",
                "Type",
                "Preconditions",
                "Result semantics",
                "Retention / command surface",
            ),
            "verify",
        ),
    ),
    "docs/05.operations/README.md": (
        Matrix(
            "Operations Routing Matrix",
            (
                "필요 상황",
                "사용할 위치",
                "시작 템플릿",
            ),
            "operations-routing",
            (
                "guide.template.md",
                "policy.template.md",
                "runbook.template.md",
                "incident.template.md",
                "postmortem.template.md",
            ),
            (2,),
        ),
    ),
    "docs/05.operations/incidents/README.md": (
        Matrix(
            "Incident Boundary Matrix",
            (
                "Artifact",
                "Path rule",
                "Template",
                "Creation rule",
                "Current state",
            ),
            "incidents",
            ("Incident Record", "Postmortem"),
        ),
    ),
}
INDEX_FOLDERS = frozenset(
    {
        "docs/05.operations/guides/README.md",
        "docs/05.operations/policies/README.md",
        "docs/05.operations/runbooks/README.md",
    }
)
LINK = re.compile(r"\]\(([^)]+)\)")
BACKTICKS = re.compile(r"`([^`]+)`")
MAX_DIRECTORY_ENTRIES = 1024
MAX_INCIDENT_ENTRIES = 4096


def _entries(root: Path, folder: str) -> tuple[tuple[str, str], ...]:
    """Enumerate one pinned directory without following links or unbounded input."""
    directory = root / folder
    try:
        with open_parent(directory) as (parent, name):
            before = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode):
                raise BoundedInputError("document inventory is not a directory")
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
            descriptor = os.open(name, flags, dir_fd=parent)
            try:
                opened = os.fstat(descriptor)
                if stable_file_state(opened) != stable_file_state(before):
                    raise BoundedInputError("document inventory changed before scan")
                found: list[tuple[str, str]] = []
                with os.scandir(descriptor) as entries:
                    for count, entry in enumerate(entries, start=1):
                        if count > MAX_DIRECTORY_ENTRIES:
                            raise BoundedInputError(
                                "document inventory exceeds entry budget"
                            )
                        mode = entry.stat(follow_symlinks=False).st_mode
                        if stat.S_ISDIR(mode):
                            kind = "dir"
                        elif stat.S_ISREG(mode):
                            kind = "file"
                        else:
                            raise BoundedInputError(
                                "document inventory has unsafe entry"
                            )
                        found.append((entry.name, kind))
                after = os.fstat(descriptor)
                at_path = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if stable_file_state(opened) != stable_file_state(
                    after
                ) or stable_file_state(after) != stable_file_state(at_path):
                    raise BoundedInputError("document inventory changed during scan")
                return tuple(sorted(found))
            finally:
                os.close(descriptor)
    except OSError as exc:
        raise BoundedInputError("document inventory is unavailable or unsafe") from exc


def _children(root: Path, folder: str, kind: str) -> tuple[str, ...]:
    return tuple(
        name for name, entry_kind in _entries(root, folder) if entry_kind == kind
    )


def _incident_records(root: Path) -> tuple[tuple[Path, ...], bool]:
    folder = "docs/05.operations/incidents"
    records: list[Path] = []
    invalid_location = False
    record_names = {"incident.md", "postmortem.md"}
    visited = 0
    for year, kind in _entries(root, folder):
        visited += 1
        if visited > MAX_INCIDENT_ENTRIES:
            raise BoundedInputError("incident inventory exceeds entry budget")
        if kind != "dir":
            invalid_location |= year in record_names
            continue
        year_folder = f"{folder}/{year}"
        for incident, kind in _entries(root, year_folder):
            visited += 1
            if visited > MAX_INCIDENT_ENTRIES:
                raise BoundedInputError("incident inventory exceeds entry budget")
            if kind != "dir":
                invalid_location |= incident in record_names
                continue
            record_folder = f"{year_folder}/{incident}"
            for filename, kind in _entries(root, record_folder):
                visited += 1
                if visited > MAX_INCIDENT_ENTRIES:
                    raise BoundedInputError("incident inventory exceeds entry budget")
                if kind == "dir":
                    invalid_location = True
                elif filename in record_names:
                    records.append(root / record_folder / filename)
    return tuple(records), invalid_location


def _key(cell: str) -> str:
    quoted = BACKTICKS.findall(cell)
    if len(quoted) == 1:
        return quoted[0]
    links = LINK.findall(cell)
    if len(links) == 1:
        return links[0].rsplit("/", 1)[-1]
    return cell.strip()


def _expected(root: Path, matrix: Matrix) -> tuple[str, ...]:
    source = matrix.source
    if source == "examples":
        return tuple(f"{name}/" for name in _children(root, "examples", "dir"))
    if source == "workflows":
        return tuple(
            name
            for name in _children(root, ".github/workflows", "file")
            if name.endswith(".yml")
        )
    if source == "platform":
        return _children(root, "gitops/platform", "dir")
    if source == "workloads":
        return _children(root, "gitops/workloads", "dir")
    if source == "infrastructure":
        entries = _entries(root, "infrastructure")
        dirs = (f"{name}/" for name, kind in entries if kind == "dir")
        files = (
            name for name, kind in entries if kind == "file" and name != "README.md"
        )
        return tuple(sorted((*dirs, *files)))
    if source == "verify":
        return tuple(
            name
            for name in _children(root, "infrastructure/verify", "file")
            if name.endswith(".sh")
        )
    return matrix.expected


def _row_keys(matrix: Matrix, row: Sequence[str]) -> tuple[str, ...]:
    if matrix.source == "infrastructure":
        return tuple(BACKTICKS.findall(row[0]))
    return ("|".join(_key(row[index]) for index in matrix.key_columns),)


def _matrix_findings(
    root: Path, matrix: Matrix, text: str, table_reader: TableReader
) -> list[Finding]:
    table = table_reader(text, matrix.title)
    if table is None or not table[1]:
        return [("DOC-MATRIX-TABLE", matrix.title, "missing-or-ambiguous-table")]
    header, rows = table
    if tuple(header) != matrix.header:
        return [("DOC-MATRIX-HEADER", matrix.title, "header-differs")]
    found: list[Finding] = []
    keys: list[str] = []
    live_scripts: set[str] = set()
    operation_pairs: list[tuple[str, str]] = []
    for row in rows:
        if len(row) != len(header) or not all(cell.strip() for cell in row):
            found.append(("DOC-MATRIX-ROW", matrix.title, "empty-or-ragged-row"))
            continue
        row_keys = _row_keys(matrix, row)
        if not row_keys or any(not value for value in row_keys):
            found.append(("DOC-MATRIX-ROW", matrix.title, "missing-key"))
            continue
        keys.extend(row_keys)
        if matrix.source in {
            "gitops-service",
            "platform",
            "workloads",
            "infrastructure",
        }:
            if "owned by" not in row[1].casefold():
                found.append(
                    ("DOC-MATRIX-OWNER", matrix.title, "owner-boundary-missing")
                )
        if matrix.source == "verify":
            if (
                row[1] not in {"Static", "Live", "Live aggregate"}
                or "Tier" not in row[4]
            ):
                found.append(
                    ("DOC-MATRIX-BOUNDARY", matrix.title, "verification-class-missing")
                )
            if row[1] == "Live":
                live_scripts.add(row_keys[0])
        if matrix.source == "workflows" and row_keys[0] == "ci.yml":
            if not all(
                marker in row[4]
                for marker in (
                    "No deploy CD",
                    "direct Kubernetes mutation",
                    "external Vault mutation",
                )
            ):
                found.append(
                    ("DOC-MATRIX-BOUNDARY", matrix.title, "ci-boundary-missing")
                )
        if matrix.source == "examples" and row_keys[0] == "sample-app/":
            if "k3d" not in row[1] or "gitops/workloads" not in row[2]:
                found.append(
                    ("DOC-MATRIX-BOUNDARY", matrix.title, "sample-app-role-missing")
                )
        if matrix.source == "operations-routing":
            location, template = LINK.findall(row[1]), LINK.findall(row[2])
            if len(location) != 1 or len(template) != 1:
                found.append(
                    (
                        "DOC-MATRIX-TARGET",
                        matrix.title,
                        "one-location-and-template-required",
                    )
                )
            else:
                operation_pairs.append((location[0], template[0]))
        if matrix.title == "External Service Contract Matrix":
            if (
                "TLS" not in row[5]
                or "CA" not in row[5]
                or not any(word in row[6].casefold() for word in ("owner", "operator"))
                or "validate-infrastructure-contracts.sh" not in row[8]
            ):
                found.append(
                    (
                        "DOC-MATRIX-BOUNDARY",
                        matrix.title,
                        "external-service-boundary-missing",
                    )
                )
        if matrix.source == "incidents":
            incident_targets = {
                "Incident Record": (
                    "./<year>/inc-####-<slug>/incident.md",
                    "../../99.templates/templates/operations/incident.template.md",
                ),
                "Postmortem": (
                    "./<year>/inc-####-<slug>/postmortem.md",
                    "../../99.templates/templates/operations/postmortem.template.md",
                ),
            }
            expected_pair = incident_targets.get(row_keys[0])
            if expected_pair and (
                row[1].strip("`") != expected_pair[0]
                or len(LINK.findall(row[2])) != 1
                or LINK.findall(row[2])[0] != expected_pair[1]
            ):
                found.append(
                    ("DOC-MATRIX-TARGET", matrix.title, "incident-form-route-differs")
                )
    if len(keys) != len(set(keys)):
        found.append(("DOC-MATRIX-DUPLICATE", matrix.title, "duplicate-key"))
    try:
        expected = _expected(root, matrix)
    except BoundedInputError:
        found.append(("DOC-MATRIX-INPUT", matrix.title, "inventory-unavailable"))
        return found
    if sorted(keys) != sorted(expected):
        found.append(("DOC-MATRIX-PARITY", matrix.title, "row-target-set-differs"))
    if matrix.source == "operations-routing":
        locations = ("guides", "policies", "runbooks", "incidents", "incidents")
        expected_pairs = tuple(
            (f"./{folder}/README.md", f"../99.templates/templates/operations/{name}")
            for folder, name in zip(locations, expected, strict=True)
        )
        if tuple(operation_pairs) != expected_pairs:
            found.append(
                ("DOC-MATRIX-TARGET", matrix.title, "router-form-pair-differs")
            )
    if matrix.source == "verify":
        try:
            run_all = bounded_read_text(
                root / "infrastructure/verify/run-all.sh", max_bytes=8 * 1024 * 1024
            )
        except BoundedInputError:
            found.append(("DOC-MATRIX-TARGET", matrix.title, "run-all-unavailable"))
        else:
            called = set(re.findall(r'bash "\$script_dir/([^"]+\.sh)"', run_all))
            if called != live_scripts:
                found.append(
                    ("DOC-MATRIX-TARGET", matrix.title, "live-run-all-set-differs")
                )
    if matrix.source == "gitops-service":
        for item in expected:
            target = root / "gitops" / item
            try:
                mode = target.lstat().st_mode
            except OSError:
                mode = 0
            if not stat.S_ISDIR(mode):
                found.append(
                    ("DOC-MATRIX-TARGET", matrix.title, "service-directory-missing")
                )
    return found


def _index_findings(
    root: Path,
    path: PurePosixPath,
    text: str,
    table_reader: TableReader,
    index_columns: tuple[str, ...],
    optional_columns: tuple[str, ...],
) -> list[Finding]:
    table = table_reader(text, "문서 인덱스")
    if table is None:
        return [("DOC-INDEX-TABLE", "문서 인덱스", "missing-or-ambiguous-table")]
    header, rows = table
    extra = header[len(index_columns) :]
    if (
        tuple(header[: len(index_columns)]) != index_columns
        or len(extra) != len(set(extra))
        or any(column not in optional_columns for column in extra)
    ):
        return [("DOC-INDEX-HEADER", "registry README index columns", "header-differs")]
    found: list[Finding] = []
    names: list[str] = []
    for row in rows:
        if len(row) != len(header) or not all(cell.strip() for cell in row):
            found.append(
                ("DOC-INDEX-ROW", "complete document row", "empty-or-ragged-row")
            )
            continue
        targets = LINK.findall(row[0])
        if len(targets) != 1 or not re.fullmatch(r"\./[^/]+\.md", targets[0]):
            found.append(
                ("DOC-INDEX-ROW", "one direct document link", "invalid-target")
            )
            continue
        names.append(targets[0][2:])
    if len(names) != len(set(names)):
        found.append(("DOC-INDEX-DUPLICATE", "unique document rows", "duplicate-key"))
    try:
        actual = tuple(
            name
            for name in _children(root, path.parent.as_posix(), "file")
            if name.endswith(".md") and name != "README.md"
        )
    except BoundedInputError:
        found.append(
            ("DOC-INDEX-INPUT", "safe document inventory", "inventory-unavailable")
        )
        return found
    if sorted(names) != sorted(actual):
        found.append(
            (
                "DOC-INDEX-PARITY",
                "every current document indexed",
                "row-target-set-differs",
            )
        )
    return found


def validate_document_content(
    root: Path,
    path: PurePosixPath,
    text: str,
    table_reader: TableReader,
    *,
    index_columns: tuple[str, ...],
    optional_index_columns: tuple[str, ...],
) -> list[Finding]:
    """Return bounded path/rule facts for one current authored router."""

    relative = path.as_posix()
    found: list[Finding] = []
    for matrix in MATRIXES.get(relative, ()):
        found.extend(_matrix_findings(root, matrix, text, table_reader))
    if relative in INDEX_FOLDERS:
        found.extend(
            _index_findings(
                root,
                path,
                text,
                table_reader,
                index_columns,
                optional_index_columns,
            )
        )
    if (
        relative in {"README.md", "docs/README.md"}
        and "99.templates/README.md" not in text
    ):
        found.append(
            ("DOC-AUTHOR-GUIDE", "link to Stage 99 author guide", "guide-link-missing")
        )
    if relative == ".github/repository-surface.md":
        required_refs = (
            ".agents/governance/git.md",
            "workflows/ci.yml",
            "scripts/qa.py",
            "PULL_REQUEST_TEMPLATE.md",
            ".agents/governance/quality.md",
        )
        if not all(reference in text for reference in required_refs):
            found.append(
                (
                    "DOC-ROUTER-OWNER",
                    "GitHub policy and gate owners",
                    "owner-link-missing",
                )
            )
        if (
            "PR source branches must start" in text
            or "Default PR target is `main`" in text
        ):
            found.append(
                ("DOC-ROUTER-OWNER", "single branch-policy owner", "copied-policy")
            )
    if relative == "examples/sample-app/README.md":
        if (
            "gitops/workloads/adminer/" not in text
            or "active GitOps desired state" not in text
        ):
            found.append(
                (
                    "DOC-ROUTER-BOUNDARY",
                    "sample app example versus active state",
                    "boundary-missing",
                )
            )
    if relative == "docs/05.operations/incidents/README.md":
        incident_root = root / "docs/05.operations/incidents"
        record_groups = (
            ("incident.md", "No tracked incident records."),
            ("postmortem.md", "No tracked postmortems."),
        )
        try:
            actual, invalid_location = _incident_records(root)
        except BoundedInputError:
            found.append(
                (
                    "DOC-INCIDENT-INPUT",
                    "safe incident inventory",
                    "inventory-unavailable",
                )
            )
            return found
        if invalid_location:
            found.append(
                ("DOC-INCIDENT-PATH", "year/incident-id/form path", "path-differs")
            )
        for filename, absence_phrase in record_groups:
            records_exist = any(entry.name == filename for entry in actual)
            if records_exist == (absence_phrase in text):
                found.append(
                    (
                        "DOC-INCIDENT-STATE",
                        f"accurate {filename} availability",
                        "state-differs",
                    )
                )
        for entry in actual:
            parts = entry.relative_to(incident_root).parts
            if (
                len(parts) != 3
                or not re.fullmatch(r"[0-9]{4}", parts[0])
                or not re.fullmatch(
                    r"inc-[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*", parts[1]
                )
            ):
                found.append(
                    ("DOC-INCIDENT-PATH", "year/incident-id/form path", "path-differs")
                )
    return found
