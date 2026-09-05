#!/usr/bin/env python3
"""Validate affected-surface routing and tracked-path coverage."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, NoReturn, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validation.repository.bounded_io import (  # noqa: E402
    BoundedInputError,
    BoundedOutputError,
    read_bytes as read_bounded_bytes,
    run as run_bounded_process,
)

_schema_spec = importlib.util.spec_from_file_location(
    "_affected_schema_owner", Path(__file__).with_name("json_schema_validation.py")
)
if _schema_spec is None or _schema_spec.loader is None:
    raise ImportError("local schema owner is unavailable")
_schema_owner = importlib.util.module_from_spec(_schema_spec)
_schema_spec.loader.exec_module(_schema_owner)
SchemaEvaluationError = _schema_owner.SchemaEvaluationError
schema_errors = _schema_owner.schema_errors


CONTRACT_PATH = PurePosixPath("scripts/validation/registry.json")
SCHEMA_PATH = PurePosixPath("scripts/validation/registry.schema.json")
CI_WORKFLOW_PATH = PurePosixPath(".github/workflows/ci.yml")
QUALITY_GATE_PATH = PurePosixPath("scripts/validate-repo-quality-gates.sh")
SELECTOR_LANES = ("affected", "staged", "all-files", "ci")
LANES = (
    "affected",
    "staged",
    "all-files",
    "message/manual",
    "ci",
    "remote/live",
    "inventory",
)
PROTECTED_LEVELS = ("none", "review", "protected")
EVIDENCE_LANES = ("repo-static", "ci", "remote/live")
MAX_PATH_INPUT_BYTES = 4 * 1024 * 1024
MAX_GIT_STDOUT_BYTES = 16 * 1024 * 1024
MAX_GIT_STDERR_BYTES = 256 * 1024
MAX_JSON_INPUT_BYTES = 8 * 1024 * 1024
EXPECTED_CI_JOBS = {"qa": "qa"}

PATH_INPUT_VALIDATORS = frozenset(
    ("document-contract-registry", "links-and-owners", "markdown-profiles")
)
SAFE_ARG = re.compile(r"^[A-Za-z0-9_./:@%+=,-]+$")
INTERPRETER_CONTRACTS = {
    "bash": {
        "evalShort": frozenset(("c",)),
        "evalLong": frozenset(("--command",)),
        "scriptSuffixes": (".sh",),
    },
    "python3": {
        "evalShort": frozenset(("c",)),
        "evalLong": frozenset(),
        "scriptSuffixes": (".py",),
    },
    "node": {
        "evalShort": frozenset(("e", "p")),
        "evalLong": frozenset(("--eval", "--print")),
        "scriptSuffixes": (".js", ".mjs", ".cjs"),
    },
}


class ContractError(ValueError):
    """A stable affected-surface contract or selection failure."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def fail(code: str, detail: str) -> NoReturn:
    raise ContractError(code, detail)


def _reject_duplicate_pairs(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(
                "SURFACE-JSON-DUPLICATE-KEY",
                "JSON object contains a duplicate key",
            )
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            read_bounded_bytes(path, max_bytes=MAX_JSON_INPUT_BYTES).decode("utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
        )
    except (BoundedInputError, UnicodeError, json.JSONDecodeError) as exc:
        fail("SURFACE-JSON", f"{path}: {exc}")


def normalize_path(raw: str) -> str:
    if not raw or raw == ".":
        fail("SURFACE-PATH-NORMALIZATION", "path must not be empty")
    if raw.startswith("./"):
        fail("SURFACE-PATH-NORMALIZATION", "path must not start with './'")
    if "\\" in raw:
        fail("SURFACE-PATH-NORMALIZATION", "path must use POSIX separators")
    path = PurePosixPath(raw)
    if path.is_absolute():
        fail("SURFACE-PATH-NORMALIZATION", "path must be repository-relative")
    if ".." in path.parts:
        fail("SURFACE-PATH-NORMALIZATION", "path must not contain '..'")
    normalized = path.as_posix()
    if normalized != raw or raw.endswith("/") or "//" in raw:
        fail("SURFACE-PATH-NORMALIZATION", "path must already be normalized")
    return normalized


def match_route(path: str, route: dict[str, str]) -> bool:
    if route["kind"] == "exact":
        return path == route["value"]
    if route["kind"] == "regex":
        pattern = route["value"]
        if not pattern.startswith("^") or not pattern.endswith("$"):
            fail("SURFACE-REGEX-ANCHOR", pattern)
        try:
            return re.fullmatch(pattern[1:-1], path) is not None
        except re.error as exc:
            fail("SURFACE-REGEX", f"{pattern}: {exc}")
    fail("SURFACE-ROUTE-KIND", route["kind"])


def _unique_ids(rows: Sequence[dict[str, Any]], kind: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        identifier = row["id"]
        if identifier in indexed:
            fail(f"SURFACE-{kind}-ID", f"duplicate id {identifier!r}")
        indexed[identifier] = row
    return indexed


def _validate_direct_script_argv(identifier: str, argv: Sequence[str]) -> str | None:
    approved_commands = {
        "unit-tests": [
            "python3",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-t",
            ".",
        ],
        "pre-commit": ["pre-commit", "run", "--all-files"],
    }
    if identifier in approved_commands and list(argv) == approved_commands[identifier]:
        return None
    if any(SAFE_ARG.fullmatch(argument) is None for argument in argv):
        fail(
            "SURFACE-VALIDATOR-ARGV",
            f"{identifier} argv must not require shell parsing or expansion",
        )

    executable = argv[0]
    interpreter = INTERPRETER_CONTRACTS.get(executable)
    if interpreter is None:
        fail(
            "SURFACE-VALIDATOR-EXECUTABLE",
            f"{identifier} executable token {executable!r} is not exactly one of "
            + ", ".join(sorted(INTERPRETER_CONTRACTS)),
        )

    arguments = list(argv[1:])
    if not arguments:
        fail("SURFACE-VALIDATOR-ARGV-SCRIPT", f"{identifier} has no script operand")

    options: list[str] = []
    script_operand: str | None = None
    after_option_boundary = False
    for argument in arguments:
        if script_operand is not None:
            break
        if not after_option_boundary and argument == "--":
            after_option_boundary = True
            continue
        if not after_option_boundary and argument.startswith("-"):
            options.append(argument)
            if argument.startswith("--"):
                if any(
                    argument == flag or argument.startswith(f"{flag}=")
                    for flag in interpreter["evalLong"]
                ):
                    fail(
                        "SURFACE-VALIDATOR-ARGV-EVAL",
                        f"{identifier} may not use {executable} evaluation option {argument!r}",
                    )
            elif set(argument[1:]).intersection(interpreter["evalShort"]):
                fail(
                    "SURFACE-VALIDATOR-ARGV-EVAL",
                    f"{identifier} may not use {executable} evaluation option {argument!r}",
                )
            continue
        script_operand = argument

    if script_operand is None:
        fail("SURFACE-VALIDATOR-ARGV-SCRIPT", f"{identifier} has no script operand")
    if options:
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} first post-executable operand must be the script path or '--'",
        )
    try:
        normalized_script = normalize_path(script_operand)
    except ContractError:
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} script operand must be a normalized repository path",
        )
    if not normalized_script.endswith(interpreter["scriptSuffixes"]):
        fail(
            "SURFACE-VALIDATOR-ARGV-SCRIPT",
            f"{identifier} script {normalized_script!r} does not match {executable}",
        )
    return normalized_script


def validator_script_paths(
    root: Path,
    raw_contract: dict[str, Any] | None = None,
    *,
    raw_schema: dict[str, Any] | None = None,
) -> frozenset[str]:
    """Return executable artifact identities from the validated owner contract."""

    contract = validate_contract(root, raw_contract, raw_schema=raw_schema)
    return frozenset(
        script
        for row in contract["validators"]
        if (script := _validate_direct_script_argv(row["id"], row["argv"])) is not None
    )


def validate_contract(
    root: Path,
    raw_contract: dict[str, Any] | None = None,
    *,
    raw_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema = (
        copy.deepcopy(raw_schema)
        if raw_schema is not None
        else load_json(root / SCHEMA_PATH)
    )
    contract = (
        copy.deepcopy(raw_contract)
        if raw_contract is not None
        else load_json(root / CONTRACT_PATH)
    )
    try:
        errors = schema_errors(schema, contract)
    except SchemaEvaluationError:
        fail("SURFACE-SCHEMA-DEFINITION", "invalid local JSON Schema")
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        fail("SURFACE-SCHEMA", f"{location}: {error.message}")

    if tuple(contract["lanes"]) != LANES:
        fail("SURFACE-LANE", "lane order or membership differs from the contract")
    if tuple(contract["protectedLevels"]) != PROTECTED_LEVELS:
        fail("SURFACE-PROTECTED-LEVEL", "protected level order differs")
    if tuple(contract["evidenceLanes"]) != EVIDENCE_LANES:
        fail("SURFACE-EVIDENCE-LANE", "evidence lane order differs")

    validators = _unique_ids(contract["validators"], "VALIDATOR")
    ci_jobs = _unique_ids(contract["ciJobs"], "CI-JOB")
    surfaces = _unique_ids(contract["surfaces"], "SURFACE")
    outputs: set[str] = set()

    path_input_validators = {
        identifier
        for identifier, validator in validators.items()
        if validator.get("pathInput") == "include-existing-markdown"
    }
    if path_input_validators != PATH_INPUT_VALIDATORS:
        fail(
            "SURFACE-VALIDATOR-PATH-INPUT",
            "include-existing-markdown ownership differs from the exact document validator set",
        )

    for validator in validators.values():
        if any(lane not in LANES for lane in validator["lanes"]):
            fail("SURFACE-VALIDATOR-LANE", validator["id"])
        _validate_direct_script_argv(validator["id"], validator["argv"])
        if validator["evidenceLane"] not in EVIDENCE_LANES:
            fail("SURFACE-EVIDENCE-LANE", validator["id"])
        status = validator["fallback"]["status"]
        if (not validator["optional"] and status != "FAIL") or (
            validator["optional"] and status not in {"DEFER", "SKIP"}
        ):
            fail("SURFACE-FALLBACK", validator["id"])

    for job in ci_jobs.values():
        if job["output"] in outputs:
            fail("SURFACE-CI-OUTPUT", f"duplicate output {job['output']!r}")
        outputs.add(job["output"])
        if job["evidenceLane"] != "ci":
            fail("SURFACE-EVIDENCE-LANE", job["id"])
    if {
        identifier: job["output"] for identifier, job in ci_jobs.items()
    } != EXPECTED_CI_JOBS:
        fail(
            "SURFACE-CI-JOB",
            "CI job IDs and selector outputs differ from the exact contract",
        )

    route_keys: set[tuple[str, str, str]] = set()
    for surface in surfaces.values():
        if any(item not in validators for item in surface["validators"]):
            fail("SURFACE-VALIDATOR-REFERENCE", surface["id"])
        if any(item not in ci_jobs for item in surface["ciJobs"]):
            fail("SURFACE-CI-JOB-REFERENCE", surface["id"])
        if surface["protectedLevel"] not in PROTECTED_LEVELS:
            fail("SURFACE-PROTECTED-LEVEL", surface["id"])
        if surface["evidenceLane"] not in EVIDENCE_LANES:
            fail("SURFACE-EVIDENCE-LANE", surface["id"])
        if surface["fallback"]["status"] != "FAIL":
            fail(
                "SURFACE-SURFACE-FALLBACK",
                f"{surface['id']} is non-optional and must fail closed",
            )
        for route in surface["routes"]:
            if route["kind"] == "exact":
                normalize_path(route["value"])
            else:
                pattern = route["value"]
                if not pattern.startswith("^") or not pattern.endswith("$"):
                    fail("SURFACE-REGEX-ANCHOR", pattern)
                try:
                    re.compile(pattern)
                except re.error as exc:
                    fail("SURFACE-REGEX", f"{pattern}: {exc}")
            key = (surface["id"], route["kind"], route["value"])
            if key in route_keys:
                fail("SURFACE-ROUTE-DUPLICATE", f"{surface['id']}: {route}")
            route_keys.add(key)
    profiles = contract["profiles"]
    for profile, identifiers in profiles.items():
        if any(identifier not in validators for identifier in identifiers):
            fail("SURFACE-PROFILE-REFERENCE", profile)
    if profiles["full"] != profiles["ci"] or set(profiles["full"]) != set(validators):
        fail(
            "SURFACE-PROFILE-COVERAGE",
            "full and ci must cover every gate in the same order",
        )
    return contract


def _case_alias(contract: dict[str, Any], path: str) -> bool:
    for surface in contract["surfaces"]:
        for route in surface["routes"]:
            if (
                route["kind"] == "exact"
                and route["value"].casefold() == path.casefold()
            ):
                return route["value"] != path
            if route["kind"] == "regex":
                pattern = route["value"]
                try:
                    if re.fullmatch(pattern[1:-1], path, flags=re.IGNORECASE):
                        return not match_route(path, route)
                except re.error:
                    continue
    return False


def classify_path(contract: dict[str, Any], raw_path: str) -> dict[str, Any]:
    path = normalize_path(raw_path)
    matches = [
        surface
        for surface in contract["surfaces"]
        if any(match_route(path, route) for route in surface["routes"])
    ]
    if not matches:
        if _case_alias(contract, path):
            fail("SURFACE-PATH-CASE-ALIAS", path)
        fail("SURFACE-PATH-UNMATCHED", path)
    if len(matches) != 1:
        fail(
            "SURFACE-PATH-AMBIGUOUS",
            f"{path}: {sorted(surface['id'] for surface in matches)}",
        )
    return matches[0]


def shared_skill_link_target(root: Path, path: PurePosixPath) -> str | None:
    """Allow only individual adapters registered against canonical skill files."""
    if len(path.parts) != 3 or path.parts[:2] != (".claude", "skills"):
        return None
    registry_path = ".agents/roles/registry.json"
    reject_symlink_traversal(root, registry_path, require_present=True)
    registry = load_json(root / registry_path)
    skill_path = f".agents/skills/{path.name}/SKILL.md"
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        fail("SURFACE-PATH-SYMLINK", path.as_posix())
    if not any(
        isinstance(row, dict)
        and row.get("id") == path.name
        and row.get("path") == skill_path
        for row in registry["skills"]
    ):
        return None
    reject_symlink_traversal(root, skill_path, require_present=True)
    return f"../../.agents/skills/{path.name}"


def reject_symlink_traversal(
    root: Path,
    raw_path: str,
    *,
    require_present: bool = False,
) -> None:
    normalized = normalize_path(raw_path)
    path = PurePosixPath(normalized)
    current = root
    for part in path.parts[:-1]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if require_present:
                fail("SURFACE-PATH-MISSING", raw_path)
            return
        except OSError as exc:
            fail("SURFACE-PATH-NODE", f"{raw_path}: {exc}")
        if stat.S_ISLNK(mode):
            fail("SURFACE-PATH-SYMLINK", raw_path)
        if not stat.S_ISDIR(mode):
            fail("SURFACE-PATH-NODE", raw_path)

    final = root / path
    try:
        mode = final.lstat().st_mode
    except FileNotFoundError:
        if require_present:
            fail("SURFACE-PATH-MISSING", raw_path)
        return
    except OSError as exc:
        fail("SURFACE-PATH-NODE", f"{raw_path}: {exc}")

    if stat.S_ISLNK(mode):
        expected_target = shared_skill_link_target(root, path)
        if expected_target is None:
            fail("SURFACE-PATH-SYMLINK", raw_path)
        try:
            actual_target = final.readlink().as_posix()
        except OSError as exc:
            fail("SURFACE-PATH-SYMLINK", f"{raw_path}: {exc}")
        if actual_target != expected_target:
            fail("SURFACE-PATH-SYMLINK", raw_path)
        return
    if not stat.S_ISREG(mode):
        fail("SURFACE-PATH-NODE", raw_path)


def _repository_migration_proof(root: Path) -> Any:
    """Call the canonical proof with fixed sibling owners in a temporary scope."""

    owners = (
        "document_authority",
        "archive_cutover_manifest",
        "archive_recovery",
        "document_contracts",
        "archive_validation",
    )
    missing = object()
    aliases = ("json_schema_validation", *owners)
    previous = {name: sys.modules.get(name, missing) for name in aliases}
    private_names: list[str] = []
    try:
        directory = Path(__file__).resolve(strict=True).parent
        sys.modules["json_schema_validation"] = _schema_owner
        for owner in owners:
            path = (directory / f"{owner}.py").resolve(strict=True)
            if path.parent != directory:
                raise ImportError("canonical migration owner is unavailable")
            name = f"_affected_migration_{id(missing):x}_{owner}"
            while name in sys.modules:
                name += "_private"
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                raise ImportError("canonical migration owner is unavailable")
            module = importlib.util.module_from_spec(spec)
            private_names.append(name)
            sys.modules[name] = module
            sys.modules[owner] = module
            spec.loader.exec_module(module)
        archive = sys.modules["archive_validation"]
        proof = archive.repository_migration_proof(root)
        if not isinstance(proof, archive.MigrationProof) or any(
            not isinstance(item, archive.MigrationDisposition)
            for item in proof.dispositions.values()
        ):
            raise ValueError("canonical migration proof type differs")
        return proof
    except Exception:
        fail("SURFACE-MIGRATION-PROOF", "canonical migration proof is unavailable")
    finally:
        for name, module in previous.items():
            if module is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
        for name in private_names:
            sys.modules.pop(name, None)


def _path_is_absent(root: Path, path: str) -> bool:
    try:
        (root / path).lstat()
    except FileNotFoundError:
        return True
    except OSError:
        fail("SURFACE-PATH-NODE", "path state is unavailable")
    return False


def select_paths(
    contract: dict[str, Any],
    paths: Sequence[str],
    lane: str,
    root: Path | None = None,
    *,
    collect_unmatched: bool = False,
) -> dict[str, Any]:
    if lane not in SELECTOR_LANES:
        fail("SURFACE-LANE", lane)
    validators_by_id = {row["id"]: row for row in contract["validators"]}
    validator_ids: set[str] = set()
    ci_job_ids: set[str] = set()
    unmatched_paths: set[str] = set()
    maximum = 0
    migration_proof = None
    for raw_path in paths:
        if root is not None:
            reject_symlink_traversal(root, raw_path)
        try:
            surface = classify_path(contract, raw_path)
        except ContractError as exc:
            if exc.code != "SURFACE-PATH-UNMATCHED":
                raise
            surface = None
            if root is not None and _path_is_absent(root, raw_path):
                if migration_proof is None:
                    migration_proof = _repository_migration_proof(root)
                disposition = migration_proof.dispositions.get(raw_path)
                target = migration_proof.targets.get(raw_path)
                if disposition is not None or target is not None:
                    if (
                        disposition is None
                        or disposition.record_path not in migration_proof.records
                        or not isinstance(disposition.source_bytes, bytes)
                        or disposition.action
                        not in {"moved", "merged", "replaced", "deleted"}
                        or not isinstance(target, str)
                        or target == raw_path
                        or migration_proof.targets.get(
                            disposition.target, disposition.target
                        )
                        != target
                    ):
                        fail(
                            "SURFACE-MIGRATION-PROOF",
                            "source disposition is unavailable",
                        )
                    reject_symlink_traversal(root, raw_path)
                    if not _path_is_absent(root, raw_path):
                        raise exc
                    try:
                        reject_symlink_traversal(root, target, require_present=True)
                        surface = classify_path(contract, target)
                    except ContractError:
                        fail(
                            "SURFACE-MIGRATION-TARGET",
                            "current terminal surface is unavailable",
                        )
            if surface is None:
                if collect_unmatched:
                    unmatched_paths.add(normalize_path(raw_path))
                    continue
                raise
        for identifier in surface["validators"]:
            if lane in validators_by_id[identifier]["lanes"]:
                validator_ids.add(identifier)
        ci_job_ids.update(surface["ciJobs"])
        maximum = max(maximum, PROTECTED_LEVELS.index(surface["protectedLevel"]))
    return {
        "validators": sorted(validator_ids),
        "ciJobs": sorted(ci_job_ids),
        "protectedLevel": PROTECTED_LEVELS[maximum],
        "unmatchedPaths": sorted(unmatched_paths),
    }


def json_output(result: dict[str, Any]) -> str:
    return json.dumps(
        result,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def github_output(contract: dict[str, Any], result: dict[str, Any]) -> str:
    selected = set(result["ciJobs"])
    return "\n".join(
        f"{job['output']}={'true' if job['id'] in selected else 'false'}"
        for job in sorted(contract["ciJobs"], key=lambda row: row["output"])
    )


def validate_required_validators_have_a_runner(
    contract: Mapping[str, Any], root: Path
) -> None:
    """Required static checks belong to the shared full/ci profiles."""
    for validator in contract["validators"]:
        if not validator["optional"] and validator["evidenceLane"] == "repo-static":
            if validator["id"] not in contract["profiles"]["full"]:
                fail("SURFACE-VALIDATOR-RUNNER", validator["id"])
    if not (root / "scripts/qa.py").is_file():
        fail("SURFACE-VALIDATOR-RUNNER", "shared QA entrypoint is missing")


def read_nul_paths(path: Path) -> list[str]:
    try:
        payload = read_bounded_bytes(path, max_bytes=MAX_PATH_INPUT_BYTES)
    except BoundedInputError:
        fail("SURFACE-PATH-TRANSPORT", "path input is unavailable or unsafe")
    if not payload:
        return []
    if not payload.endswith(b"\0"):
        fail("SURFACE-PATH-TRANSPORT", "NUL path input must be terminated")
    records = payload[:-1].split(b"\0")
    if any(record == b"" for record in records):
        fail("SURFACE-PATH-TRANSPORT", "NUL path input contains an empty record")
    try:
        return [record.decode("utf-8") for record in records]
    except UnicodeDecodeError as exc:
        fail("SURFACE-PATH-TRANSPORT", f"path input must be UTF-8: {exc}")


def tracked_paths(root: Path) -> list[str]:
    try:
        completed = run_bounded_process(
            ["git", "ls-files", "-z"],
            cwd=root,
            timeout=15,
            stdout_limit=MAX_GIT_STDOUT_BYTES,
            stderr_limit=MAX_GIT_STDERR_BYTES,
        )
    except (BoundedOutputError, OSError, subprocess.SubprocessError, ValueError):
        fail("SURFACE-GIT-INVENTORY", "bounded Git inventory failed")
    if completed.returncode != 0:
        fail("SURFACE-GIT-INVENTORY", "Git inventory exited non-zero")
    payload = completed.stdout
    if payload and not payload.endswith(b"\0"):
        fail("SURFACE-GIT-INVENTORY", "git ls-files output is not NUL terminated")
    try:
        return [record.decode("utf-8") for record in payload.split(b"\0") if record]
    except UnicodeDecodeError as exc:
        fail("SURFACE-GIT-INVENTORY", f"tracked path must be UTF-8: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        contract = validate_contract(root)
        validate_required_validators_have_a_runner(contract, root)
        paths = tracked_paths(root)
        observed_surfaces = {
            (
                reject_symlink_traversal(root, path, require_present=True),
                classify_path(contract, path)["id"],
            )[1]
            for path in paths
        }
        print(
            "[PASS] affected surface validation passed: "
            f"paths={len(paths)} surfaces={len(observed_surfaces)}/"
            f"{len(contract['surfaces'])} validators={len(contract['validators'])} "
            f"ci_jobs={len(contract['ciJobs'])} uncovered=0 ambiguous=0"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc.code}: {exc.detail}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
