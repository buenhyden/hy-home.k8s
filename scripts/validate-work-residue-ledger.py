"""Check the work residue ledger against the residue rows of the Task files.

The ledger holds residue pointers only; a Task and its EVD rows own execution
state, evidence and acceptance. This gate reads the files under one root, with
no Git history and no network, and refuses residue that exists only in
Markdown, only in JSON, drifts between them, or closes without a PASS row.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from json_schema_validation import SchemaEvaluationError, schema_errors  # noqa: E402
from validation.repository.bounded_io import BoundedInputError, read_text  # noqa: E402

LEDGER = "docs/03.specs/work-residue-ledger.json"
SCHEMA = "docs/99.templates/contracts/work-residue-ledger.schema.json"
REGISTRY = "docs/99.templates/registry.json"
MAX_BYTES = 4 * 1024 * 1024
STATES = ("open", "terminal")
TASK_GLOB = "docs/03.specs/*/tasks/*.md"
TASK_PATH = re.compile(r"docs/03\.specs/[^/]+/tasks/[^/]+\.md")
HANDOFF_ID = re.compile(r"W[0-9]{2}-H[0-9]{2}")
EXCLUDED_PREFIXES = ("docs/90.references/", "docs/98.archive/")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
TABLE_LINE = re.compile(r"^ {0,3}\|")
COPY_KEY = re.compile(r"^contract_id$|_digest$|_revision$|_ref$")
ROW_FIELDS = (
    ("state", "State"),
    ("owner", "Owner"),
    ("resume_condition", "Resume condition"),
)


class LedgerError(Exception):
    """The ledger could not be read."""


class Finding(NamedTuple):
    rule: str
    where: str
    detail: str

    def line(self) -> str:
        return f"FAIL {self.rule} {self.where} {self.detail}"


class Table(NamedTuple):
    heading: str
    header: list[str]
    rows: list[list[str]]


class TaskDoc(NamedTuple):
    tables: list[Table]
    evidence: dict[str, str]
    live: Table | None
    rows: list[dict[str, str]]


def _read(root: Path, rel: str) -> str:
    try:
        return read_text(root / rel, max_bytes=MAX_BYTES)
    except BoundedInputError as error:
        raise LedgerError(f"{rel} is unreadable: {error}") from error


def load_ledger(root: Path) -> dict[str, Any]:
    """Return the parsed ledger; the view and the gate read it one way."""

    try:
        data = json.loads(_read(root, LEDGER))
    except ValueError as error:
        raise LedgerError(f"{LEDGER} is not valid JSON") from error
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
        raise LedgerError(f"{LEDGER} has no entries list")
    return data


def _link_validator() -> Any:
    path = Path(__file__).with_name("validate-links-and-owners.py")
    name = "_work_residue_link_validator"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise LedgerError("the link validator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _tables(links: Any, text: str) -> Iterator[Table]:
    """Yield every visible table with the heading it sits under."""

    lines = links._visible_markdown(text).splitlines()
    heading, index = "", 0
    while index < len(lines):
        match = HEADING.match(lines[index])
        if match:
            heading, index = match.group(1), index + 1
            continue
        if (
            index + 1 < len(lines)
            and TABLE_LINE.match(lines[index])
            and TABLE_LINE.match(lines[index + 1])
        ):
            header = links._gfm_table_cells(lines[index])
            rule = links._gfm_table_cells(lines[index + 1])
            if (
                header
                and len(header) == len(rule)
                and all(re.fullmatch(r":?-+:?", cell) for cell in rule)
            ):
                rows: list[list[str]] = []
                index += 2
                while index < len(lines) and TABLE_LINE.match(lines[index]):
                    rows.append(links._gfm_table_cells(lines[index]))
                    index += 1
                yield Table(heading, header, rows)
                continue
        index += 1


def _is_residue_table(table: Table) -> bool:
    return (
        "Handoff" in table.heading
        or "Conflicts" in table.heading
        or any(row and HANDOFF_ID.fullmatch(row[0].strip()) for row in table.rows)
    )


def _task_doc(links: Any, text: str, block: dict[str, Any]) -> TaskDoc:
    tables = list(_tables(links, text))
    evidence = {
        row["Evidence"].strip(): row["Result"].strip()
        for row in links.task_base_evidence_rows(text) or []
    }
    spec = block["task_table"]
    columns = tuple(spec["columns"])
    named = [table for table in tables if table.heading == spec["heading"]]
    live: Table | None = None
    rows: list[dict[str, str]] = []
    section = links._exact_heading_section(text, f"## {spec['section']}")
    if section is not None and len(named) == 1:
        sub = links._exact_heading_section(section, f"### {spec['heading']}")
        first = None if sub is None else links._first_visible_table(sub)
        if first is not None and tuple(first[0]) == columns == tuple(named[0].header):
            live = named[0]
            rows = [dict(zip(columns, row, strict=True)) for row in first[1]]
    return TaskDoc(tables, evidence, live, rows)


def _texts(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(i, str) and i for i in value)


def _registry_block(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        registry = json.loads(_read(root, REGISTRY))
    except ValueError as error:
        raise LedgerError(f"{REGISTRY} is not valid JSON") from error
    block = registry.get("work_residue") if isinstance(registry, dict) else None
    table = block.get("task_table") if isinstance(block, dict) else None
    historical = block.get("historical_tables") if isinstance(block, dict) else None
    valid = (
        isinstance(table, dict)
        and isinstance(table.get("section"), str)
        and isinstance(table.get("heading"), str)
        and _texts(table.get("columns"))
        and isinstance(historical, list)
        and all(
            isinstance(item, dict)
            and isinstance(item.get("path"), str)
            and isinstance(item.get("heading"), str)
            for item in historical
        )
    )
    if not valid:
        raise LedgerError(f"{REGISTRY} has no valid work_residue block")
    return block, registry


def _copied_values(registry: dict[str, Any]) -> set[str]:
    found: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                text = item if isinstance(item, str) else ""
                if text.strip() and text != "unverified" and COPY_KEY.search(key):
                    found.add(text)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for key in ("shared_contract", "common_forms"):
        walk(registry.get(key))
    return found


def _strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _schema_findings(root: Path, data: dict[str, Any]) -> list[Finding]:
    try:
        schema = json.loads(_read(root, SCHEMA))
        errors = schema_errors(schema, data)
    except (ValueError, SchemaEvaluationError, LedgerError) as error:
        return [
            Finding("RESIDUE-SCHEMA", SCHEMA, f"the schema cannot be applied: {error}")
        ]
    found: dict[tuple[str, str], Finding] = {}
    for error in errors:
        path = list(error.absolute_path)
        if len(path) == 3 and path[0] == "entries" and path[2] == "state":
            where = str(data["entries"][path[1]].get("id", path[1]))
            found[("RESIDUE-TASK-STATUS", where)] = Finding(
                "RESIDUE-TASK-STATUS", where, "state is not one of open or terminal"
            )
        else:
            location = "/".join(str(part) for part in path) or "ledger"
            found[("RESIDUE-SCHEMA", location + error.message)] = Finding(
                "RESIDUE-SCHEMA", LEDGER, f"{location}: {error.message[:160]}"
            )
    if found:
        return list(found.values())
    ids = [entry["id"] for entry in data["entries"]]
    out: list[Finding] = []
    if len(set(ids)) != len(ids):
        out.append(Finding("RESIDUE-SCHEMA", LEDGER, "an entry id is duplicated"))
    if ids != sorted(ids):
        out.append(Finding("RESIDUE-SCHEMA", LEDGER, "entries are not sorted by id"))
    return out


def _path_problem(root: Path, rel: str) -> str | None:
    parts = PurePosixPath(rel).parts
    if rel.startswith("/") or ".." in parts:
        return "is outside the root"
    if rel.startswith(EXCLUDED_PREFIXES):
        return "is under Stage 90 or the archive"
    if not (root / rel).is_file():
        return "does not resolve under the root"
    return None


def check(root: Path) -> list[Finding]:
    """Return every finding for the tree under root."""

    root = Path(root)
    try:
        data = load_ledger(root)
        block, registry = _registry_block(root)
    except LedgerError as error:
        return [Finding("RESIDUE-SCHEMA", LEDGER, str(error))]
    found = _schema_findings(root, data)
    if found:
        return found
    links = _link_validator()
    historical = {
        (item["path"], item["heading"]) for item in block["historical_tables"]
    }
    docs: dict[str, TaskDoc] = {}
    for path in sorted(root.glob(TASK_GLOB)):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            docs[rel] = _task_doc(links, _read(root, rel), block)

    for rel, heading in sorted(historical):
        if rel not in docs:
            found.append(
                Finding(
                    "RESIDUE-SOURCE",
                    rel,
                    "registered historical table does not resolve to a current Task",
                )
            )
        elif not any(table.heading == heading for table in docs[rel].tables):
            found.append(
                Finding(
                    "RESIDUE-SOURCE",
                    rel,
                    f"registered historical table {heading!r} is absent",
                )
            )
    for rel, doc in docs.items():
        for table in doc.tables:
            if (
                table is not doc.live
                and _is_residue_table(table)
                and (rel, table.heading) not in historical
            ):
                found.append(
                    Finding(
                        "RESIDUE-MARKDOWN-ONLY",
                        rel,
                        f"table {table.heading!r} is neither the live table nor registered historical",
                    )
                )

    entries = {entry["id"]: entry for entry in data["entries"]}
    rows_by_task: dict[str, dict[str, dict[str, str]]] = {}
    for rel, doc in docs.items():
        indexed = rows_by_task.setdefault(rel, {})
        for row in doc.rows:
            ident, state, closure = (row[k].strip() for k in ("ID", "State", "Closure"))
            if ident in indexed:
                found.append(
                    Finding(
                        "RESIDUE-MARKDOWN-ONLY", ident, f"id is duplicated in {rel}"
                    )
                )
            indexed[ident] = row
            if state not in STATES:
                found.append(
                    Finding(
                        "RESIDUE-TASK-STATUS",
                        ident,
                        "State is not one of open or terminal",
                    )
                )
            elif state == "terminal":
                if doc.evidence.get(closure) != "PASS":
                    found.append(
                        Finding(
                            "RESIDUE-CLOSURE",
                            ident,
                            "Closure does not name a PASS row of its Task",
                        )
                    )
            else:
                if closure != "none":
                    found.append(
                        Finding(
                            "RESIDUE-CLOSURE", ident, "an open row carries a closure"
                        )
                    )
                entry = entries.get(ident)
                if entry is None:
                    found.append(
                        Finding(
                            "RESIDUE-MARKDOWN-ONLY",
                            ident,
                            f"open row in {rel} has no ledger entry",
                        )
                    )
                elif (
                    TASK_PATH.fullmatch(entry["source"]["path"])
                    and entry["source"]["path"] != rel
                ):
                    found.append(
                        Finding(
                            "RESIDUE-DRIFT",
                            ident,
                            f"field source differs: the row is in {rel}",
                        )
                    )

    copied = _copied_values(registry)
    for entry in data["entries"]:
        ident, source = entry["id"], entry["source"]["path"]
        is_task = TASK_PATH.fullmatch(source) is not None
        problem = _path_problem(root, source)
        if problem:
            found.append(Finding("RESIDUE-SOURCE", ident, f"source {problem}"))
        elif entry["kind"] in ("handoff", "conflict") and not is_task:
            found.append(
                Finding(
                    "RESIDUE-SOURCE",
                    ident,
                    f"a {entry['kind']} entry is sourced outside a Task",
                )
            )
        if (
            entry["kind"] == "adoption"
            and entry["source"]["registry_key"] not in registry
        ):
            found.append(
                Finding(
                    "RESIDUE-REGISTRY-COPY",
                    ident,
                    "registry_key is absent from the registry",
                )
            )
        for text in _strings(entry):
            if any(value in text for value in copied):
                found.append(
                    Finding(
                        "RESIDUE-REGISTRY-COPY",
                        ident,
                        "an entry string copies a registry contract value",
                    )
                )
                break
        if is_task:
            row = rows_by_task.get(source, {}).get(ident)
        else:
            row = next((r[ident] for r in rows_by_task.values() if ident in r), None)
        if entry["state"] == "open":
            if row is None and is_task and problem is None:
                found.append(
                    Finding(
                        "RESIDUE-JSON-ONLY",
                        ident,
                        f"open entry has no open live row in {source}",
                    )
                )
        else:
            closure = entry["closure"]
            closed = closure["path"]
            problem = _path_problem(root, closed)
            if problem:
                found.append(Finding("RESIDUE-SOURCE", ident, f"closure {problem}"))
            elif (
                closed not in docs
                or docs[closed].evidence.get(closure["evidence"]) != "PASS"
            ):
                found.append(
                    Finding(
                        "RESIDUE-CLOSURE",
                        ident,
                        "closure does not name a PASS row of a current Task",
                    )
                )
            if is_task and closed != source:
                found.append(
                    Finding(
                        "RESIDUE-CLOSURE",
                        ident,
                        "closure path differs from the source Task",
                    )
                )
            if is_task and (
                row is None
                or row["State"].strip() != "terminal"
                or row["Closure"].strip() != closure["evidence"]
            ):
                found.append(
                    Finding(
                        "RESIDUE-CLOSURE",
                        ident,
                        "the live row is not terminal with the same EVD ID",
                    )
                )
        if row is not None:
            for field, column in ROW_FIELDS:
                if row[column].strip() != entry[field]:
                    found.append(
                        Finding(
                            "RESIDUE-DRIFT",
                            ident,
                            f"field {field} differs between the entry and the row",
                        )
                    )
    return found


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(arguments.root).resolve()
    findings = check(root)
    for finding in findings:
        print(finding.line())
    if findings:
        return 1
    print(f"PASS work residue ledger: {len(load_ledger(root)['entries'])} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
