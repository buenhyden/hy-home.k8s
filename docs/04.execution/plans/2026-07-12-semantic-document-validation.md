---
title: 'Semantic Document Validation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-12
---

# Semantic Document Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace hardcoded document-shape checks with deterministic,
registry-driven Markdown, link, index, current-owner, and migration-ledger
validation.

**Architecture:** Reuse the Spec 026 importable registry loader, keep Markdown
profile validation separate from cross-document validation, and expose stable
rule IDs through text and JSON output. The repository quality gate becomes an
orchestrator and uses compatibility mode until Spec 030 performs strict cutover.

**Tech Stack:** Python 3.11 standard library, PyYAML, JSON Schema 2020-12,
CommonMark-compatible fence parsing, Bash, Markdown, Git, and pre-commit.

## Global Constraints

- Work only in the isolated worktree for branch `codex/workspace-document-assurance-modernization`.
- Consume `docs/99.templates/support/document-profiles.json`; do not create a second route, key, lifecycle, or heading owner.
- Use repository-relative POSIX paths and reject leading `./`, `..`, case aliases, and symlink traversal.
- Diagnostics must contain rule ID, path, profile, expected value, actual value, and remediation owner without printing secret content.
- Exit codes are `0` for success, `1` for document violations, and `2` for configuration or CLI errors.
- Compatibility mode may defer only named registry debt; strict mode rejects every remaining debt item.
- Validation performs no network or live runtime action.
- Use `apply_patch` for content edits and commit each independently testable Task separately.
- Run focused self-tests before every commit and repository-wide QA before closure.

---

## Overview

This Plan implements Spec 029 through one execution-chain Task, two focused
validator Tasks, and one integration Task. It preserves the current gate until
the replacement checks have fixture coverage and deterministic output.

## Context

`scripts/validate-repo-quality-gates.sh` currently embeds route, Frontmatter,
README, heading, link, template-residue, and agent-adjacent document checks in
one large Python block. Specs 026–028 provide the registry and normalized forms;
this Plan creates the consumer layer needed by the authored migration.

## Goals & In-Scope

- Validate exact Frontmatter delimiters, duplicate keys, keysets, key order,
  types, states, dates, titles, headings, fences, and template residue.
- Validate internal links, indexes, archive routing, current-owner uniqueness,
  and migration-ledger completeness.
- Provide positive and focused negative fixtures with stable rule IDs.
- Delegate superseded hardcoded checks from the repository quality gate.

## Non-Goals & Out-of-Scope

- Rewriting the authored corpus or enabling strict mode.
- Validating external URL availability or prose truth.
- Changing README forms, template forms, provider adapters, CI job selection,
  GitOps desired state, credentials, or live services.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Registry library | `scripts/document_contracts.py` | Importable registry, path classification, tracked inventory, and diagnostic types created by Spec 026. |
| Markdown validation | `scripts/validate-markdown-profiles.py`, `tests/fixtures/markdown-profiles.json`, `tests/fixtures/document-contracts/readme-profile-cases.json` | Per-document structure and profile semantics; the production parser must run both its authored cases and all eight README handoff cases created by Spec 028. |
| Cross-document validation | `scripts/validate-links-and-owners.py`, `tests/fixtures/links-and-owners.json` | Links, indexes, current owners, and durable migration ledger. |
| Gate integration | `scripts/validate-repo-quality-gates.sh` | Invoke canonical validators and retain only domain checks not represented in the registry. |
| Execution evidence | same-topic Spec, Plan, Task, three Stage indexes, `memory/progress.md` | Reciprocal lineage, commands, results, limitations, review, and rollback commits. |

### Durable ledger columns

The cross-document validator requires this exact fourteen-column order; it
must not infer the contract from Spec 030 prose or accept renamed aliases:

```text
path | title | profile | owner-key | disposition | destination | local-evidence | official-sources | observed-version | applicability | content-decision | refresh-trigger | reviewer | result
```

### Required Python Interfaces

```python
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Literal

@dataclass(frozen=True)
class Route:
    kind: Literal["exact", "regex"]
    value: str

@dataclass(frozen=True)
class Diagnostic:
    rule_id: str
    path: PurePosixPath
    profile: str
    expected: str
    actual: str
    owner: str

@dataclass(frozen=True)
class FrontmatterContract:
    mode: Literal["required", "forbidden", "not-applicable"]
    required: tuple[str, ...]
    allowed: tuple[str, ...]
    order: tuple[str, ...]

@dataclass(frozen=True)
class HeadingContract:
    required: tuple[str, ...]
    allowed: tuple[str, ...]

@dataclass(frozen=True)
class AppendContract:
    parent_profile_id: str
    parent_h2: str
    entry_heading_level: Literal[3]
    section_heading_level: Literal[4]
    required_sections: tuple[str, ...]

@dataclass(frozen=True)
class DocumentProfile:
    profile_id: str
    profile_class: Literal["sdlc", "common", "governance", "readme", "exception"]
    routes: tuple[Route, ...]
    frontmatter: FrontmatterContract
    status_domain: tuple[str, ...]
    headings: HeadingContract
    template: PurePosixPath | None
    mode: Literal["authored", "template", "frontmatter-free", "native", "generated", "non-target"]
    source_profile_ids: tuple[str, ...]
    placeholder_policy: Literal["forbidden", "template-only"]
    append_contract: AppendContract | None

@dataclass(frozen=True)
class Registry:
    schema_version: int
    baseline_sha: str
    baseline_count: int
    profiles: tuple[DocumentProfile, ...]

@dataclass(frozen=True)
class TargetInventory:
    baseline_paths: tuple[PurePosixPath, ...]
    current_paths: tuple[PurePosixPath, ...]
    new_paths: tuple[PurePosixPath, ...]
    baseline_symlink_paths: tuple[PurePosixPath, ...]
    current_symlink_paths: tuple[PurePosixPath, ...]

def load_registry(root: Path) -> Registry: ...
def enumerate_target_markdown(
    root: Path,
    *,
    include_paths: tuple[PurePosixPath, ...] = (),
) -> TargetInventory: ...
def classify_path(registry: Registry, path: PurePosixPath) -> DocumentProfile: ...
def validate_document(root: Path, path: PurePosixPath,
                      profile: DocumentProfile, mode: str) -> list[Diagnostic]: ...
def validate_cross_document_contracts(root: Path, mode: str) -> list[Diagnostic]: ...
```

The definitions through `classify_path()` are the exact Spec 026 public API.
Both validators iterate `enumerate_target_markdown(root).current_paths`; neither
may implement a second inventory walk or dereference the recorded symlink
entries.

## Work Breakdown

| Task | Deliverable | Primary validation | Commit |
| --- | --- | --- | --- |
| SMDV-001 | Start reciprocal Spec/Plan/Task lineage | Path and link assertions | `docs(execution): start semantic document validation` |
| SMDV-002 | Markdown profile validator and fixtures | `--self-test` and compatibility repository run | `feat(docs): add registry-driven markdown profile validation` |
| SMDV-003 | Link, index, owner, and ledger validator | `--self-test` and inventory output | `feat(docs): validate links indexes and current owners` |
| SMDV-004 | Quality-gate delegation and closure | Full quality gate, all-files pre-commit | `refactor(qa): delegate document checks to semantic validators` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-029-001 | Lineage | Task 1 Python assertion | Spec, Plan, Task, and indexes link reciprocally. |
| VAL-029-002 | Unit | `python3 scripts/validate-markdown-profiles.py --self-test` | Every positive fixture passes and every mutation returns its exact rule ID. |
| VAL-029-003 | Integration | `python3 scripts/validate-links-and-owners.py --self-test` | Link, index, owner, and ledger mutations are rejected. |
| VAL-029-004 | Repository | both validators in compatibility mode | Named migration debt is reported and no unknown violation is deferred. |
| VAL-029-005 | Regression | quality gate and pre-commit | All required hooks pass; optional skips remain labeled. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Parser differs from rendered Markdown | High | Fence conformance fixtures cover backtick, tilde, longer closing fences, and unclosed fences. |
| Compatibility mode hides new drift | High | Only exact registry debt records may defer; unmatched failures remain exit 1. |
| Gate refactor removes unique checks | High | Map each deleted block to a rule ID and retain operations/domain checks without a registry representation. |
| Fixture runner tests different logic | High | Self-tests call the same public validation functions as repository mode. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate:** Focused fixture self-test and repository compatibility run pass for each validator.
- **Sandbox / Canary Rollout:** Compatibility mode runs beside the current quality gate before hardcoded checks are removed.
- **Human Approval Gate:** Required before strict cutover, remote push, merge, registry schema change, or live validation.
- **Rollback Trigger:** A false positive, an unknown deferred error, a missing existing domain check, or nondeterministic diagnostic ordering.
- **Prompt / Model Promotion Criteria:** Not applicable; model policy is outside Spec 029.

---

### Task 1: Start Reciprocal Execution Lineage

**Files:**

- Modify: `docs/03.specs/029-semantic-document-validation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-semantic-document-validation.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: active Spec 029 and this approved Plan.
- Produces: Task IDs `SMDV-001` through `SMDV-004` and reciprocal links used by closure validation.

- [ ] **Step 1: Run the failing lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
spec = Path('docs/03.specs/029-semantic-document-validation/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-semantic-document-validation.md')
task = Path('docs/04.execution/tasks/2026-07-12-semantic-document-validation.md')
assert task.exists(), task
for source, target in ((spec, plan), (spec, task), (plan, spec), (plan, task), (task, spec), (task, plan)):
    assert target.name in source.read_text(encoding='utf-8'), (source, target)
PY
```

Expected: FAIL because the Task does not exist and reciprocal links are absent.

- [ ] **Step 2: Create the execution Task from the canonical Task form**

Use frontmatter `title: 'Task: Semantic Document Validation'`,
`type: sdlc/task`, `status: active`, `owner: platform`, and
`updated: 2026-07-12`. Add four rows with IDs `SMDV-001` through `SMDV-004`,
the commit messages from the Work Breakdown table, and exact validation commands
from this Plan.

- [ ] **Step 3: Add reciprocal links and index rows**

Link Spec 029 to this Plan and Task; link this Plan and Task back to Spec 029
and each other. Add active rows dated `2026-07-12` to the Spec, Plan, and Task
indexes without changing unrelated rows.

- [ ] **Step 4: Run the lineage assertion again**

Run the Step 1 command.

Expected: PASS with no output.

- [ ] **Step 5: Run focused document QA**

```bash
git diff --check
pre-commit run --files \
  docs/03.specs/029-semantic-document-validation/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/04.execution/tasks/README.md
```

Expected: all applicable hooks PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/03.specs/029-semantic-document-validation/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): start semantic document validation"
```

---

### Task 2: Implement Markdown Profile Validation

**Files:**

- Create: `scripts/validate-markdown-profiles.py`
- Create: `tests/fixtures/markdown-profiles.json`
- Consume: `tests/fixtures/document-contracts/readme-profile-cases.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`

**Interfaces:**

- Consumes: `load_registry()`,
  `enumerate_target_markdown(root).current_paths`, `classify_path()`, and
  `Diagnostic` from `scripts/document_contracts.py`.
- Produces: `validate_document(root, path, profile, mode)`, CLI text/JSON output,
  stable rule IDs consumed by Spec 030, and production-parser results for every
  Spec 028 README handoff case.

- [ ] **Step 1: Add exact authored cases and bind the README handoff**

Create JSON cases named `valid-spec`, `duplicate-key`, `future-date`,
`wrong-key-order`, `missing-heading`, `heading-in-fence`, `duplicate-h2`,
`unsupported-h2`, `template-residue`, and `unclosed-fence`. Each case contains
`profile`, `document`, and `expected_rule_ids`; the valid and heading-in-fence
cases use an empty expected list. Also load
`tests/fixtures/document-contracts/readme-profile-cases.json` and require its
case names to be exactly `valid-profile`, `frontmatter-forbidden`,
`duplicate-h1`, `duplicate-h2`, `unsupported-h2`, `missing-required-h2`,
`fenced-heading-ignored`, and `unclosed-fence`. Do not copy or translate those
case bodies into a second fixture.

- [ ] **Step 2: Add the CLI shell and run RED**

Implement argument parsing and one self-test loop that calls the same
`validate_document()` production entry point for every case in both fixture
files. Select each README case's path/profile contract from the handoff's
`paths` table; do not use a fixture-only parser. Initially return an empty
diagnostic list from `validate_document()`.

```bash
python3 scripts/validate-markdown-profiles.py --self-test
```

Expected: exit 1 for both fixture suites, including mismatches for
`FM-DUPLICATE-KEY`, `FM-FUTURE-DATE`,
`FM-KEY-ORDER`, `BODY-HEADING-REQUIRED`, `BODY-H2-DUPLICATE`,
`BODY-HEADING-UNSUPPORTED`, `BODY-TEMPLATE-RESIDUE`, and
`BODY-FENCE-UNCLOSED`, plus the README handoff's exact expected rule IDs.

- [ ] **Step 3: Implement exact Frontmatter parsing**

Add a duplicate-key loader and return ordered keys, parsed mapping, and body.

```python
def extract_frontmatter(text: str) -> tuple[list[str], dict[str, object], str]:
    if not text.startswith('---\n'):
        raise ContractError('FM-DELIMITER', 'first line must be ---')
    closing = text.find('\n---\n', 4)
    if closing < 0:
        raise ContractError('FM-DELIMITER', 'frontmatter is not closed')
    raw = text[4:closing]
    data = yaml.load(raw, Loader=DuplicateKeyLoader) or {}
    if not isinstance(data, dict):
        raise ContractError('FM-KEYSET', 'frontmatter must be a mapping')
    return list(data.keys()), data, text[closing + 5:]
```

- [ ] **Step 4: Implement fence-aware heading parsing**

Track fence character and length; accept a closing fence only when it uses the
same character and at least the opening length. Emit H1/H2 records only outside
fences and return an unclosed-fence flag.

- [ ] **Step 5: Implement profile rules and sorted diagnostics**

Validate exact required/allowed keys, ordered keys, type, status domain,
`platform` owner, real ISO date, future-date policy, title, H1 count, required
and allowed H2, duplicate H2, and residue markers. Sort diagnostics by
`(path, rule_id, expected, actual)`.

- [ ] **Step 6: Run GREEN self-test and compatibility validation**

```bash
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility
```

Expected: all ten authored cases and all eight README handoff cases PASS through
the production parser; repository run exits 0 with only named `DEFER` debt.

- [ ] **Step 7: Update script/test inventories and run focused QA**

Document the CLI, exit codes, rule-ID stability, fixture names, and repo-static
evidence boundary in `scripts/README.md` and `tests/README.md`.

```bash
python3 -m py_compile scripts/document_contracts.py scripts/validate-markdown-profiles.py
git diff --check
pre-commit run --files scripts/document_contracts.py scripts/validate-markdown-profiles.py \
  tests/fixtures/markdown-profiles.json tests/fixtures/document-contracts/readme-profile-cases.json \
  scripts/README.md tests/README.md
```

Expected: compile and all applicable hooks PASS.

- [ ] **Step 8: Commit**

```bash
git add scripts/document_contracts.py scripts/validate-markdown-profiles.py \
  tests/fixtures/markdown-profiles.json tests/fixtures/document-contracts/readme-profile-cases.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md
git commit -m "feat(docs): add registry-driven markdown profile validation"
```

---

### Task 3: Implement Cross-Document Validation

**Files:**

- Create: `scripts/validate-links-and-owners.py`
- Create: `tests/fixtures/links-and-owners.json`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`

**Interfaces:**

- Consumes: registry classification, `Diagnostic`, and
  `enumerate_target_markdown(root).current_paths` from
  `scripts/document_contracts.py`.
- Produces: `validate_cross_document_contracts(root, mode)`, `--inventory --format json`, and ledger rule IDs consumed by Spec 030.

- [ ] **Step 1: Add cross-document fixture cases**

Create cases named `valid-tree`, `broken-link`, `absolute-link`,
`archive-bypass`, `missing-index-row`, `stale-index-row`,
`duplicate-current-owner`, `missing-ledger-row`, `incomplete-ledger-row`, and
`unknown-ledger-path`. Each case embeds a minimal repository tree and exact
`expected_rule_ids`.

- [ ] **Step 2: Add CLI shell and run RED**

Return no diagnostics from the initial function, then run:

```bash
python3 scripts/validate-links-and-owners.py --self-test
```

Expected: exit 1 with missing expected rules `LINK-BROKEN`, `LINK-ABSOLUTE`,
`LINK-ARCHIVE-BYPASS`, `INDEX-MISSING`, `INDEX-STALE`, `OWNER-DUPLICATE`,
`LEDGER-MISSING`, `LEDGER-INCOMPLETE`, and `LEDGER-UNKNOWN-PATH`.

- [ ] **Step 3: Implement fence-aware link resolution**

Parse inline and reference links outside fences, reject local-filesystem URI schemes and absolute
paths, ignore external schemes, URL-decode the path portion, and verify the
resolved target remains inside the repository.

- [ ] **Step 4: Implement indexes and owner keys**

Parse declared index tables; compare indexed and actual children. Build
`owner-key` from normalized role, scope, and lineage, excluding archive,
dated-snapshot, and completed-evidence profiles from current-owner candidates.

- [ ] **Step 5: Implement ledger parsing and inventory JSON**

Require this exact ordered column list directly in code:
`path`, `title`, `profile`, `owner-key`, `disposition`, `destination`,
`local-evidence`, `official-sources`, `observed-version`, `applicability`,
`content-decision`, `refresh-trigger`, `reviewer`, `result`. Reject a missing,
extra, reordered, or aliased column with `LEDGER-INCOMPLETE`. `--inventory` returns
one sorted JSON object per approved authored path with classification and owner
key; it must not write files or inspect ignored paths.

- [ ] **Step 6: Run GREEN tests**

```bash
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
python3 scripts/validate-links-and-owners.py --root . --inventory --format json | python3 -m json.tool >/dev/null
```

Expected: fixture PASS, compatibility exit 0 with named debt only, valid JSON inventory.

- [ ] **Step 7: Run focused QA and commit**

```bash
python3 -m py_compile scripts/validate-links-and-owners.py
git diff --check
pre-commit run --files scripts/validate-links-and-owners.py \
  tests/fixtures/links-and-owners.json scripts/README.md tests/README.md
git add scripts/validate-links-and-owners.py tests/fixtures/links-and-owners.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md
git commit -m "feat(docs): validate links indexes and current owners"
```

Expected: all checks PASS and commit succeeds.

---

### Task 4: Delegate the Repository Gate and Close Spec 029

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/03.specs/029-semantic-document-validation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-semantic-document-validation.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: three registry/profile/cross-document validator CLIs.
- Produces: compatibility-mode repository gate and completed Spec 029 execution evidence.

- [ ] **Step 1: Record the existing gate baseline**

```bash
bash scripts/validate-repo-quality-gates.sh .
```

Expected: PASS before refactoring.

- [ ] **Step 2: Add canonical validator invocations**

Place these commands after Python/PyYAML prerequisite checks:

```bash
python3 "$ROOT_DIR/scripts/validate-document-contract-registry.py" --root "$ROOT_DIR" --mode compatibility
python3 "$ROOT_DIR/scripts/validate-markdown-profiles.py" --root "$ROOT_DIR" --mode compatibility
python3 "$ROOT_DIR/scripts/validate-links-and-owners.py" --root "$ROOT_DIR" --mode compatibility
```

- [ ] **Step 3: Remove only superseded hardcoded checks**

Delete blocks that reimplement registry route, general Frontmatter, general
README heading, generic link, generic owner, and generic residue rules. Keep
operations index parity, GitOps, infrastructure, agent-runtime, version, and
other domain contracts whose semantics are not in the document registry.

- [ ] **Step 4: Run focused regression**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-links-and-owners.py --self-test
bash scripts/validate-repo-quality-gates.sh .
```

Expected: all commands PASS; the repository command reports compatibility debt but no unknown deferral.

- [ ] **Step 5: Run full QA**

```bash
find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +
git diff --check
pre-commit run --all-files
```

Expected: shell syntax and required hooks PASS; optional tool skips are explicitly labeled.

- [ ] **Step 6: Close reciprocal evidence**

Set Spec, Plan, and Task to `done`; update their index rows to `Done` and date
`2026-07-12`. Record commands, results, limitations, reviewer, commit range,
and rollback commits in the Task and append a concise reusable handoff to
`memory/progress.md`.

- [ ] **Step 7: Commit**

```bash
git add scripts/validate-repo-quality-gates.sh scripts/README.md tests/README.md \
  docs/03.specs/029-semantic-document-validation/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "refactor(qa): delegate document checks to semantic validators"
```

## Completion Criteria

- [ ] Every registry profile and cross-document rule has positive and focused negative fixture coverage.
- [ ] Compatibility mode accounts for every known migration item without a silent allow-list.
- [ ] The quality gate consumes canonical validators and no longer owns duplicated general document rules.
- [ ] Spec, Plan, Task, indexes, progress evidence, and rollback commits are reciprocal and complete.

## Related Documents

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Registry ADR](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- [Semantic Validation Spec](../../03.specs/029-semantic-document-validation/spec.md)
- [Authored Migration Spec](../../03.specs/030-authored-document-migration/spec.md)
