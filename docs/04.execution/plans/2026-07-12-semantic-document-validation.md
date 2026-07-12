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
- Compatibility mode may defer only an exact item from one of the two finite,
  Spec-030-owned debt consumers defined below. The registry schema has no debt
  field and must never be described as owning migration debt. Strict mode
  rejects every debt item.
- Validation performs no network or live runtime action.
- Use `apply_patch` for content edits and commit each independently testable Task separately.
- Run focused self-tests before every commit and repository-wide QA before closure.
- Every repository-changing logical unit updates
  `docs/00.agent-governance/memory/progress.md`. A review-remediation commit is
  a separate logical unit and appends its own progress entry.

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

### Compatibility Debt Owners

Compatibility is finite and fail-closed. It reads only these files; a CLI flag,
environment variable, path glob, inline comment, or code-local allow-list may
not create debt:

| Consumer | Schema and permitted scope | Owner and removal transition |
| --- | --- | --- |
| `tests/fixtures/document-contracts/template-compatibility.json` | Existing schema v1 plus exact `affectedPaths` records under each `compatibilityDebt` profile. Each record contains `path`, sorted `ruleIds`, and sorted `tokens`. Aggregate profile/path/occurrence counts remain frozen with `growthAllowed: false`. Only legacy heading aliases and forbidden residue already named by this file may defer. | Spec 030. ADM-003 through ADM-006 remove a path record in the same logical unit that makes the path canonical; ADM-007 removes the last empty debt definitions after strict validation. |
| `tests/fixtures/document-contracts/semantic-compatibility-debt.json` | Schema v1 with top-level `schemaVersion`, `owner`, `growthAllowed`, and `items`. Each item has exactly `ruleId`, `path`, `profile`, `expected`, `actual`, `ownerTask`, and `removeWhen`. The initial and only permitted item is `LEDGER-MISSING` for `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`, profile `content/reference`, owner task `ADM-002`, with `removeWhen` equal to `ledger exists, has the exact fourteen columns, and covers the inventory once`. | Spec 030 / ADM-002. ADM-002 creates and stages the durable ledger, proves completeness, and removes the `LEDGER-MISSING` item in the same commit. An empty file may remain until ADM-007, but `growthAllowed` stays false. |

`LEDGER-MISSING` is therefore a represented compatibility item, not an
implicit absence check. In compatibility mode that exact item emits `DEFER`
and exit 0. In strict mode it emits `FAIL` and exit 1. A missing ledger after
the item is removed is an ordinary `LEDGER-MISSING` violation and cannot defer.
No other link, index, owner, ledger, frontmatter, or body rule is permitted in
the semantic debt file without a separately approved Plan amendment.
The Spec 030 Plan must consume these two files at ADM-002/ADM-007; its stale
reference to registry debt does not authorize adding debt fields or records to
`document-profiles.json`.

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
class AppendContext:
    parent_path: PurePosixPath
    parent_profile: DocumentProfile
    parent_h2: str

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
                      profile: DocumentProfile, mode: str,
                      append_context: AppendContext | None = None) -> list[Diagnostic]: ...
def validate_cross_document_contracts(root: Path, mode: str) -> list[Diagnostic]: ...
```

The definitions through `classify_path()` are the exact Spec 026 public API.
Both validators iterate `enumerate_target_markdown(root).current_paths`; neither
may implement a second inventory walk or dereference the recorded symlink
entries.

### Deterministic Owner Key

The cross-document validator computes a current-owner key only from repository
content already admitted by the registry:

1. Candidate documents are `mode: authored` and have frontmatter status
   `active` or `accepted`. Exclude profile `content/archive-tombstone`, every
   class `readme` or `exception`, every mode `template`, `frontmatter-free`,
   `generated`, `native`, or `non-target`, and paths matching
   `^docs/90\.references/(?:research|audits)/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/`,
   `^docs/90\.references/cloud-examples/`, or
   `^examples/(?:aws|azure)/docs/`. Plans and Tasks with status `done` are
   completed evidence and are excluded by the status rule.
2. `role` is the validated frontmatter `type` value after Unicode NFKC,
   case-folding, collapsing every run of characters for which Python
   `str.isalnum()` is false to `-`, and
   trimming `-`.
3. `scope` is the validated frontmatter `title` after the same normalization
   and removal of the one exact profile-family suffix (`product requirements`,
   `architecture requirements`, `architecture decision record`, `technical
   specification`, `implementation plan`, or leading `task`) when present.
4. `lineage` is the normalized repository-relative destination of the first
   local link, in document order, inside `## Traceability` that resolves to a
   Stage 01 PRD or Stage 03 `spec.md`. If no such link exists, use the
   candidate's own canonical feature key: Stage 01 filename without `.md`,
   Stage 03 feature directory name, Stage 04 filename without date and `.md`,
   otherwise the repository-relative path without suffix. URL fragments and
   queries are removed before normalization.
5. The serialized key is `role|scope|lineage`. Empty components produce
   `OWNER-KEY-MISSING`; malformed links produce the relevant `LINK-*` rule;
   two candidates with the same serialized key produce one sorted
   `OWNER-DUPLICATE` diagnostic naming all paths. Matching excluded documents
   never suppresses or creates a current-owner diagnostic.

Fixture cases assert NFKC/case/punctuation normalization, suffix removal,
first-upstream-link selection, fallback lineage, exclusions, missing
components, and duplicate ordering. No title similarity, model judgment, Git
history, or live lookup participates.

### Declared Index Contracts

`scripts/validate-links-and-owners.py` owns one immutable
`DECLARED_INDEXES` tuple for these three Stage indexes; it is cross-document
validator configuration not represented by the profile registry:

| Index | Tree target | Table anchor and row href | Status semantics | Exclusions |
| --- | --- | --- | --- | --- |
| `docs/03.specs/README.md` | `docs/03.specs/[0-9][0-9][0-9]-*/spec.md` | `### Current Spec Index`; first cell contains exactly one href `./<feature>/spec.md` | `Active`, `Done`, `Archived` map case-insensitively to target frontmatter `active`, `done`, `archived` | README files and feature-local helper documents |
| `docs/04.execution/plans/README.md` | `docs/04.execution/plans/*.md` | first Markdown table after `## Item Index`; href `./<filename>.md` | same mapping | `README.md` |
| `docs/04.execution/tasks/README.md` | `docs/04.execution/tasks/*.md` | H3 anchor with code points `U+BB38 U+C11C U+0020 U+C778 U+B371 U+C2A4`; href `./<filename>.md` | same mapping | `README.md` |

For each declaration, the actual key is the normalized repository-relative
target path and the row key is its resolved href. Each actual target appears
exactly once in the fenced tree and exactly once in the declared table; every
row resolves to exactly one actual target; duplicate hrefs are
`INDEX-DUPLICATE`, absent actual rows are `INDEX-MISSING`, non-target rows are
`INDEX-STALE`, status mismatches are `INDEX-STATUS`, and tree duplicates or
omissions are `INDEX-TREE`. Table alignment rows, headings, comments, fenced
examples outside the declared tree block, external links, and nested tables
outside the named anchor are excluded. Diagnostics sort by index path, rule,
and target key.

### Stable CLI Contract

Both semantic validators implement identical result behavior:

- Text output is one sorted line per result:
  `PASS|DEFER|FAIL RULE_ID path profile expected=<json> actual=<json> owner=<json>`.
  A clean run emits one deterministic `PASS` summary line.
- JSON output is one object with keys in this order: `schemaVersion`, `mode`,
  `outcome`, `counts`, `diagnostics`. Diagnostics use the `Diagnostic` field
  order and the same sort as text. JSON goes to stdout; configuration and CLI
  errors go to stderr without partial result JSON.
- Exit `0` means no diagnostics or compatibility mode with only exact `DEFER`
  items; exit `1` means at least one non-deferred document violation (and any
  debt in strict mode); exit `2` means malformed registry/debt/configuration or
  invalid CLI usage. Unknown items are never downgraded.
- `--self-test` calls the production entry point. `--inventory` is read-only,
  mutually exclusive with `--self-test`, and follows the same deterministic
  JSON/error contract. All modes are repository-static and tracked-only plus
  explicit `--include-path` values.

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
| Compatibility mode hides new drift | High | Only exact records from the two finite debt consumers may defer; unmatched failures remain exit 1. |
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
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: active Spec 029 and this approved Plan.
- Produces: Task IDs `SMDV-001` through `SMDV-004` and reciprocal links used by closure validation.

- [x] **Step 1: Run the exact failing lineage and index assertion**

```bash
python3 - <<'PY'
import re
from pathlib import Path

spec = Path('docs/03.specs/029-semantic-document-validation/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-semantic-document-validation.md')
task = Path('docs/04.execution/tasks/2026-07-12-semantic-document-validation.md')
task_table_anchor = '### ' + ''.join(map(chr, (0xBB38, 0xC11C, 0x20, 0xC778, 0xB371, 0xC2A4)))
indexes = {
    Path('docs/03.specs/README.md'): {
        'tree_h2': '## Document Index',
        'tree_line': '├── 029-semantic-document-validation/',
        'table_kind': 'after-anchor',
        'table_anchor': '### Current Spec Index',
        'href': './029-semantic-document-validation/spec.md',
    },
    Path('docs/04.execution/plans/README.md'): {
        'tree_h2': '## Item Index',
        'tree_line': '├── 2026-07-12-semantic-document-validation.md',
        'table_kind': 'first-after-h2',
        'table_anchor': '## Item Index',
        'href': './2026-07-12-semantic-document-validation.md',
    },
    Path('docs/04.execution/tasks/README.md'): {
        'tree_h2': '## Item Index',
        'tree_line': '├── 2026-07-12-semantic-document-validation.md',
        'table_kind': 'after-anchor',
        'table_anchor': task_table_anchor,
        'href': './2026-07-12-semantic-document-validation.md',
    },
}
expected = {
    spec: {
        '../../04.execution/plans/2026-07-12-semantic-document-validation.md',
        '../../04.execution/tasks/2026-07-12-semantic-document-validation.md',
    },
    plan: {
        '../../03.specs/029-semantic-document-validation/spec.md',
        '../tasks/2026-07-12-semantic-document-validation.md',
    },
    task: {
        '../../03.specs/029-semantic-document-validation/spec.md',
        '../plans/2026-07-12-semantic-document-validation.md',
    },
}
assert task.exists(), task
for source, hrefs in expected.items():
    found = re.findall(r'\[[^]]*\]\(([^)]+)\)', source.read_text(encoding='utf-8'))
    for href in hrefs:
        assert found.count(href) == 1, (source, href, found.count(href))

def unique_line(lines, value):
    matches = [i for i, line in enumerate(lines) if line == value]
    assert len(matches) == 1, (value, matches)
    return matches[0]

def after_blanks(lines, start):
    while start < len(lines) and not lines[start]:
        start += 1
    return start

alignment = re.compile(r'^\|(?:\s*:?-+:?\s*\|)+$')

for index, contract in indexes.items():
    text = index.read_text(encoding='utf-8')
    lines = text.splitlines()

    tree_h2 = unique_line(lines, contract['tree_h2'])
    tree_open = after_blanks(lines, tree_h2 + 1)
    assert tree_open < len(lines) and lines[tree_open] == '```text', (index, 'tree-open')
    tree_close = next((i for i in range(tree_open + 1, len(lines)) if lines[i] == '```'), None)
    assert tree_close is not None, (index, 'tree-close')
    tree_body = lines[tree_open + 1:tree_close]
    assert tree_body.count(contract['tree_line']) == 1, (index, contract['tree_line'])
    outside_tree = lines[:tree_open] + lines[tree_close + 1:]
    assert contract['tree_line'] not in outside_tree, (index, 'tree-line-outside-fence')

    anchor = unique_line(lines, contract['table_anchor'])
    if contract['table_kind'] == 'after-anchor':
        table_start = after_blanks(lines, anchor + 1)
    else:
        table_start = next((i for i in range(anchor + 1, len(lines)) if lines[i].startswith('|')), None)
        assert table_start is not None, (index, 'first-table-after-h2')
    assert table_start + 2 < len(lines), (index, 'table-short')
    assert lines[table_start].startswith('|') and alignment.fullmatch(lines[table_start + 1]), (index, 'table-header')
    table_end = table_start + 2
    while table_end < len(lines) and lines[table_end].startswith('|'):
        table_end += 1
    table_rows = lines[table_start + 2:table_end]
    assert table_rows, (index, 'table-data')
    target_rows = []
    for row in table_rows:
        hrefs = re.findall(r'\[[^]]*\]\(([^)]+)\)', row)
        if contract['href'] in hrefs:
            target_rows.append(row)
    assert len(target_rows) == 1, (index, contract['href'], len(target_rows))
    assert re.findall(r'\[[^]]*\]\(([^)]+)\)', target_rows[0]).count(contract['href']) == 1
    outside_table = '\n'.join(lines[:table_start] + lines[table_end:])
    assert f']({contract["href"]})' not in outside_table, (index, 'href-outside-table')
PY
```

Expected: FAIL because the Task, its exact reciprocal hrefs, and its two unique
index representations do not exist. The existing Spec and Plan each already
have one tree entry and one table row; do not add duplicates.

- [x] **Step 2: Create the execution Task from the canonical Task form**

Use frontmatter `title: 'Task: Semantic Document Validation'`,
`type: sdlc/task`, `status: active`, `owner: platform`, and
`updated: 2026-07-12`. The direct program approvals explicitly promote this
new Task from the canonical draft start to `active`; record that promotion in
Inputs. Use exactly the six canonical H2 headings `Overview`, `Inputs`, `Task
Table`, `Approval and Safety Boundaries`, `Verification Summary`, and
`Traceability`, and exactly the five table columns `ID | Work item | Owner |
Status | Evidence`. Add four rows: `SMDV-001` is `Done`; `SMDV-002` through
`SMDV-004` are `Queued`; Owner is `platform`. Every Evidence cell names the
logical commit from Work Breakdown and its exact primary validation command:
SMDV-001 uses `python3 scripts/validate-document-contract-registry.py --root . --mode compatibility`,
SMDV-002 uses `python3 scripts/validate-markdown-profiles.py --self-test`,
SMDV-003 uses `python3 scripts/validate-links-and-owners.py --self-test`, and
SMDV-004 uses `bash scripts/validate-repo-quality-gates.sh .`.
Fill every safety field with the repository-static, tracked-only,
no-secret/no-live boundary and rollback by logical commit.

- [x] **Step 3: Add reciprocal links and index rows**

Use the six exact hrefs from Step 1. Verify or update the existing Spec and Plan
index rows in place; do not add them again. Add exactly one Task tree entry and
one Task table row dated `2026-07-12`. Append one canonical progress entry for
this logical unit.

- [x] **Step 4: Run the lineage assertion again**

Stage the exact seven-file scope first, then run Step 1 and:

```bash
git add docs/03.specs/029-semantic-document-validation/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
```

Expected: lineage PASS with no output; registry remains 9 cases, 60 profiles,
27 templates; inventory is exactly 467 target Markdown paths
(`baseline=433`, `new=36`) and README 72.

- [x] **Step 5: Run focused document QA**

```bash
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --files \
  docs/03.specs/029-semantic-document-validation/spec.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
test "$(git diff --cached --name-only | wc -l)" -eq 7
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/03.specs/029-semantic-document-validation/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-semantic-document-validation.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-semantic-document-validation.md',
    'docs/04.execution/tasks/README.md',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
PY
```

Expected: all applicable hooks PASS.

- [x] **Step 6: Commit**

```bash
git add docs/03.specs/029-semantic-document-validation/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "docs(execution): start semantic document validation"
```

Expected delta: one new target Markdown path, no profile/template/README count
change. Roll back with `git revert <SMDV-001-commit>`. A fresh independent
reviewer verifies hrefs, Task shape/status/table, counts, seven-path scope, and
command evidence in `.superpowers/sdd/smdv-task-1-review.md`; tracked review
remediation is a separate logical commit with its own progress entry.

---

### Task 2: Implement Markdown Profile Validation

**Files:**

- Create: `scripts/validate-markdown-profiles.py`
- Create: `tests/fixtures/markdown-profiles.json`
- Consume: `tests/fixtures/document-contracts/readme-profile-cases.json`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: `load_registry()`,
  `enumerate_target_markdown(root).current_paths`, `classify_path()`, and
  `Diagnostic` from `scripts/document_contracts.py`.
- Produces: `validate_document(root, path, profile, mode)`, CLI text/JSON output,
  stable rule IDs consumed by Spec 030, and production-parser results for every
  Spec 028 README handoff case.

- [ ] **Step 1: Add the profile/mode matrix and bind the README handoff**

`tests/fixtures/markdown-profiles.json` has `schemaVersion: 1`, one
`profileMatrix` row for every registry profile, and `mutationCases`. Each row
contains `profile`, `mode`, `applicability`, `fixturePath`, `positiveSource`,
and `negativeMutations`. Applicability is exactly one of `validate-document`,
`append-fragment`, `classification-only`, or `excluded`. Markdown routes in
modes `authored`, `template`, and `frontmatter-free` with declared structural
contracts use `validate-document`. Profiles in modes `native` or `generated`
whose frontmatter mode is `not-applicable` and whose required/allowed headings
are both empty use `classification-only`: empty headings mean structural N/A,
not "forbid every heading". Their positive and focused route/profile mismatch
cases run through production `classify_path()` and inventory selection while
`validate_document()` emits no invented structural rule. The registry profile
`governance/progress-entry` is explicitly applicable as
`applicability: append-fragment`: its positive case validates a canonical H3
entry with the five required H4 sections against the parent
`governance/progress-ledger` append contract, and focused negative cases remove
one required H4, use the wrong H3/H4 level, and target the wrong parent H2.
Those cases call the same production `validate_document()` entry point with an
explicit `AppendContext(parent_path, parent_profile, parent_h2)`; missing,
wrong-profile, and wrong-parent-H2 contexts fail with stable append rule IDs.
They are not fixture-only parsing. Only `non-target` uses
`applicability: excluded` with exact reason `non-target`. Self-test rejects
missing, duplicate, stale, or unjustified rows and asserts that
`governance/progress-entry` is never excluded. Every `validate-document` or
`append-fragment` row runs production positive and focused negative cases;
every `classification-only` row runs production classifier/inventory positive
and focused negative cases.

Render positive fixtures from the registry contract and canonical form with
fixed values, not from a current authored file. Parameterize negative
mutations by capability: delimiter/keyset/order/type/status/date, forbidden
frontmatter, H1/H2/fence, placeholder residue, and the progress-entry append
contract. Every
implemented rule ID has one mutation. Keep cases `valid-spec`, `duplicate-key`, `future-date`,
`wrong-key-order`, `missing-heading`, `heading-in-fence`, `duplicate-h2`,
`unsupported-h2`, `template-residue`, and `unclosed-fence`.

Also load
`tests/fixtures/document-contracts/readme-profile-cases.json` and require its
case names to be exactly `valid-profile`, `frontmatter-forbidden`,
`duplicate-h1`, `duplicate-h2`, `unsupported-h2`, `missing-required-h2`,
`fenced-heading-ignored`, and `unclosed-fence`. Run those exact bodies through
the production entry point with their path-selected profile; do not copy or
translate them. Separately generate one positive and supported negative case
for all six README profiles, so the root handoff does not stand in for profile
coverage.

- [ ] **Step 2: Add the CLI shell and run RED**

Implement argument parsing and one self-test loop that calls the same
`validate_document()` production entry point for every case in both fixture
files. Select each README case's path/profile contract from the handoff's
`paths` table; do not use a fixture-only parser. Initially return an empty
diagnostic list from `validate_document()`. Pass `append_context=None` for
ordinary documents and an explicit parent context for progress-entry cases;
classification-only profiles exercise the production classifier/inventory
path rather than a structural fixture parser.

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

Date validation is mode-specific. Authored documents require a real ISO
calendar date that is not future-dated under the repository date policy.
Template-mode forms may use the exact `YYYY-MM-DD` placeholder and do not run
the authored future-date rule; any other invalid template date still fails.
Positive and focused negative cases cover both branches.

- [ ] **Step 4: Implement fence-aware heading parsing**

Track fence character and length; accept a closing fence only when it uses the
same character and at least the opening length. Emit H1/H2 records only outside
fences and return an unclosed-fence flag.

- [ ] **Step 5: Implement profile rules and sorted diagnostics**

Validate exact required/allowed keys, ordered keys, type, status domain,
`platform` owner, mode-specific date policy, title, H1 count, required
and allowed H2, duplicate H2, and residue markers. Load path-level legacy
shape debt only from `template-compatibility.json`: extend each existing
profile debt row with sorted `affectedPaths` entries containing exact `path`,
`ruleIds`, and `tokens` from the frozen 466-path pre-Task baseline. The frozen
audit contract is one 266-path union with these exact no-growth caps:

| Rule | Exact finite baseline |
| --- | --- |
| `BODY-HEADING-REQUIRED` | 89 paths and 247 missing path/token obligations |
| `BODY-TEMPLATE-RESIDUE` | 188 paths and 410 occurrences; its overlap with required-heading debt is 51 paths, so the existing-debt union is 226 paths |
| `FM-DELIMITER` | 24 exact `governance/reference` paths |
| `BODY-HEADING-UNSUPPORTED` | 175 paths, 617 occurrences, and 422 exact path/token obligations after represented aliases and residue are removed |
| `BODY-H2-DUPLICATE` | 1 exact path and 1 token |

Store every rule on the affected path record, store sorted exact tokens where
the rule is token-bearing, and add aggregate rule caps plus
`unionPathCount: 266`. Self-test recomputes the per-rule and union counts from
the exact records and rejects missing/extra paths, tokens, occurrences,
overlap drift, or cap growth. A defer
requires an exact path/rule/token match and counts at or below every frozen
profile/path/occurrence cap. Strict mode fails the same item; new paths and
unknown tokens never defer. Do not add debt to the registry. Sort diagnostics by
`(path, rule_id, expected, actual)`.

Because `affectedPaths` changes the complete semantic projection of
`template-compatibility.json`, recompute its stable sorted-JSON SHA-256 with
`template_compatibility_semantic_sha256()` and pin the complete new digest in
`TEMPLATE_COMPATIBILITY_CONTRACT_V1` inside
`scripts/validate-repo-quality-gates.sh` in this same Task. Extend
`assert_template_compatibility_mutation_proof()` with at least one
`affectedPaths` mutation that changes an exact path, rule ID, or token and
prove `template_compatibility_contract_matches()` rejects it. Keep the owner,
growth, residue, and baseline-count mutations; add rule-cap and
`unionPathCount` mutations so the new finite-debt dimensions are also proven
immutable. This is a required consumer
update, not an allow-list, weakened digest projection, deferred failure, or
SMDV-004 gate-delegation change.

- [ ] **Step 6: Run GREEN self-test and compatibility validation**

```bash
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility
```

Expected: all named cases, all eight imported README cases, and every
applicable profile/mode row PASS through the production parser; repository run
exits 0 with only the exact 266-path union and its frozen per-rule caps reported
as named `DEFER` debt. Classification-only native/generated profiles remain
structural N/A, progress entries use explicit parent context, template date
placeholders pass only in template mode, and authored dates remain real and
not future. Inventory remains 467 target paths
(`baseline=433`, `new=36`), 60 profiles, 27 templates, and README 72.

- [ ] **Step 7: Update script/test inventories and run focused QA**

Document the CLI, exit codes, rule-ID stability, fixture names, and repo-static
evidence boundary in `scripts/README.md` and `tests/README.md`.

```bash
python3 -m py_compile scripts/document_contracts.py scripts/validate-markdown-profiles.py
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
readme_fixture_sha="50f8c8ab05267a9ddf059d72ca6950d4f05b14ad82010c0d9576eb7a9f1f68d0" # pragma: allowlist secret
test "$(sha256sum tests/fixtures/document-contracts/readme-profile-cases.json | cut -d' ' -f1)" = "$readme_fixture_sha"
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --files scripts/document_contracts.py scripts/validate-markdown-profiles.py \
  scripts/validate-repo-quality-gates.sh \
  tests/fixtures/markdown-profiles.json tests/fixtures/document-contracts/template-compatibility.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/00.agent-governance/memory/progress.md
```

Expected: compile and all applicable hooks PASS.

- [ ] **Step 8: Commit**

```bash
git add scripts/document_contracts.py scripts/validate-markdown-profiles.py \
  scripts/validate-repo-quality-gates.sh \
  tests/fixtures/markdown-profiles.json tests/fixtures/document-contracts/template-compatibility.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/00.agent-governance/memory/progress.md
test "$(git diff --cached --name-only | wc -l)" -eq 9
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/04.execution/tasks/2026-07-12-semantic-document-validation.md',
    'scripts/README.md',
    'scripts/document_contracts.py',
    'scripts/validate-markdown-profiles.py',
    'scripts/validate-repo-quality-gates.sh',
    'tests/README.md',
    'tests/fixtures/document-contracts/template-compatibility.json',
    'tests/fixtures/markdown-profiles.json',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
PY
git commit -m "feat(docs): add registry-driven markdown profile validation"
```

Expected delta: two new non-target support files and no target-corpus,
profile/template, or README count change. Roll back with
`git revert <SMDV-002-commit>` so the fixture, its complete pinned digest, and
its mutation proof return together. A fresh reviewer checks matrix coverage,
production-entry-point use, debt matching, output/exit stability, exact
nine-path scope, readme-profile fixture byte identity, complete-fixture digest
pinning, the exact 266-path/per-rule cap recomputation, arbitrary
`affectedPaths` drift rejection, append-context and date-mode coverage, and
repository-static boundaries in
`.superpowers/sdd/smdv-task-2-review.md`.

---

### Task 3: Implement Cross-Document Validation

**Files:**

- Create: `scripts/validate-links-and-owners.py`
- Create: `tests/fixtures/links-and-owners.json`
- Create: `tests/fixtures/document-contracts/semantic-compatibility-debt.json`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-semantic-document-validation.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: registry classification, `Diagnostic`, and
  `enumerate_target_markdown(root).current_paths` from
  `scripts/document_contracts.py`.
- Produces: `validate_cross_document_contracts(root, mode)`, `--inventory --format json`, and ledger rule IDs consumed by Spec 030.

- [ ] **Step 1: Add cross-document fixture cases**

Create cases named `valid-tree`, `broken-link`, `absolute-link`,
`archive-bypass`, `missing-index-row`, `stale-index-row`,
`duplicate-current-owner`, `missing-ledger-row`, `incomplete-ledger-row`, and
`unknown-ledger-path`, plus focused owner normalization/exclusion and index
duplicate/status/tree cases. Each embeds a minimal repository tree and exact
`expected_rule_ids`; `valid-tree` exercises all three declared index contracts
and the fourteen-column ledger. Create the semantic debt file with the one
exact `LEDGER-MISSING` item specified above. Self-test proves growth, alias
keys, unknown rules, glob paths, duplicate items, and malformed removal
transitions are configuration errors with exit 2.

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

Implement the exact `DECLARED_INDEXES` and Deterministic Owner Key contracts
above. Assert href resolution, tree/table uniqueness, target frontmatter status,
exclusions, normalization, fallback lineage, and sorted duplicate diagnostics.
Do not discover indexes from heading similarity or prove links by basename.

- [ ] **Step 5: Implement ledger parsing and inventory JSON**

Require this exact ordered column list directly in code:
`path`, `title`, `profile`, `owner-key`, `disposition`, `destination`,
`local-evidence`, `official-sources`, `observed-version`, `applicability`,
`content-decision`, `refresh-trigger`, `reviewer`, `result`. Reject a missing,
extra, reordered, or aliased column with `LEDGER-INCOMPLETE`. `--inventory` returns
one sorted JSON object per approved authored path with classification and owner
key; it must not write files or inspect ignored paths.

In compatibility mode, only the exact absent durable-ledger debt item emits
DEFER. In strict mode it emits FAIL. Spec 030 ADM-002 creates and stages the
ledger, validates all rows, and removes that debt item in the same commit;
subsequent absence can never defer.

- [ ] **Step 6: Run GREEN tests**

```bash
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
inventory_json="$(mktemp /tmp/smdv-inventory.XXXXXX.json)"
trap 'rm -f "$inventory_json"' EXIT

producer_probe_rc=0
false >"$inventory_json" || producer_probe_rc=$?
if [ "$producer_probe_rc" -eq 0 ]; then
  exit 1
fi
parser_probe_rc=0
printf '{' >"$inventory_json"
python3 -m json.tool "$inventory_json" >/dev/null 2>&1 || parser_probe_rc=$?
if [ "$parser_probe_rc" -eq 0 ]; then
  exit 1
fi

inventory_rc=0
python3 scripts/validate-links-and-owners.py --root . --inventory --format json >"$inventory_json" || inventory_rc=$?
if [ "$inventory_rc" -eq 0 ]; then
  python3 -m json.tool "$inventory_json" >/dev/null || inventory_rc=$?
fi
rm -f "$inventory_json"
trap - EXIT
exit "$inventory_rc"
```

Expected: fixture PASS, compatibility exit 0 with the exact ledger debt only,
the bounded negative probes preserve nonzero producer and parser status, the
real inventory producer exits 0 before its separate JSON parse exits 0, no
repository temporary file is created, and registry counts stay at 467 target paths
(`baseline=433`, `new=36`), 60 profiles, 27 templates, README 72.

- [ ] **Step 7: Run focused QA and commit**

```bash
python3 -m py_compile scripts/validate-links-and-owners.py
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --files scripts/validate-links-and-owners.py \
  tests/fixtures/links-and-owners.json tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/00.agent-governance/memory/progress.md
git add scripts/validate-links-and-owners.py tests/fixtures/links-and-owners.json \
  tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  scripts/README.md tests/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md \
  docs/00.agent-governance/memory/progress.md
test "$(git diff --cached --name-only | wc -l)" -eq 7
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/04.execution/tasks/2026-07-12-semantic-document-validation.md',
    'scripts/README.md',
    'scripts/validate-links-and-owners.py',
    'tests/README.md',
    'tests/fixtures/document-contracts/semantic-compatibility-debt.json',
    'tests/fixtures/links-and-owners.json',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
PY
git commit -m "feat(docs): validate links indexes and current owners"
```

Expected: all checks PASS and commit succeeds.

Expected delta: three new non-target support files and no target-corpus,
profile/template, or README count change. Roll back with
`git revert <SMDV-003-commit>`. A fresh reviewer checks link/index/owner
algorithms, ledger schema and removal transition, output/exit stability, exact
seven-path scope, and ignored/secret boundaries in
`.superpowers/sdd/smdv-task-3-review.md`.

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
SMDV-004 owns this later delegation and removal of superseded hardcoded
validation only. It does not postpone, repeat, or undo SMDV-002's required
complete-fixture digest pin and `affectedPaths` mutation proof.

- [ ] **Step 4: Run focused regression**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-links-and-owners.py --self-test
bash scripts/validate-repo-quality-gates.sh .
```

Expected: all commands PASS; the repository command reports compatibility debt but no unknown deferral.
Registry counts remain exactly 467 target paths (`baseline=433`, `new=36`),
60 profiles, 27 templates, and README 72.

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

The Task keeps exactly its six canonical H2 headings. Set all four Task rows to
`Done`; every Evidence cell records its logical commit and exact validation
command. Compatibility remains canonical until Spec 030 ADM-007, and this Task
does not remove either finite debt consumer.

- [ ] **Step 7: Commit**

```bash
git add scripts/validate-repo-quality-gates.sh scripts/README.md tests/README.md \
  docs/03.specs/029-semantic-document-validation/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-semantic-document-validation.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-semantic-document-validation.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
test "$(git diff --cached --name-only | wc -l)" -eq 10
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/03.specs/029-semantic-document-validation/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-semantic-document-validation.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-semantic-document-validation.md',
    'docs/04.execution/tasks/README.md',
    'scripts/README.md',
    'scripts/validate-repo-quality-gates.sh',
    'tests/README.md',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
PY
git commit -m "refactor(qa): delegate document checks to semantic validators"
```

Expected delta: no new target and no change from 467 targets
(`baseline=433`, `new=36`), 60 profiles, 27 templates, or README 72. Roll back
with `git revert <SMDV-004-commit>`; retain the two validator feature commits
when restoring only the wrapper. A fresh reviewer maps every deleted block to
a new rule or a retained domain check, verifies lifecycle/progress evidence and
the exact ten-path scope, and records
`.superpowers/sdd/smdv-task-4-review.md`. Any tracked remediation is a new
logical unit with its own progress entry.

## Completion Criteria

- [ ] Every registry profile and cross-document rule has positive and focused negative fixture coverage.
- [ ] Compatibility mode accounts for every known migration item without a silent allow-list.
- [ ] `LEDGER-MISSING` has one exact Spec-030-owned representation and ADM-002 removal transition.
- [ ] Every registry profile has exactly one deterministic matrix row; every structural profile/mode, the `governance/progress-entry` append fragment, every native/generated classification-only row, and every cross-document rule has the matching production-entry-point positive and focused negative coverage.
- [ ] The quality gate consumes canonical validators and no longer owns duplicated general document rules.
- [ ] Spec, Plan, Task, indexes, progress evidence, and rollback commits are reciprocal and complete.

## Related Documents

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Registry ADR](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- [Semantic Validation Spec](../../03.specs/029-semantic-document-validation/spec.md)
- [Semantic Validation Task](../tasks/2026-07-12-semantic-document-validation.md)
- [Authored Migration Spec](../../03.specs/030-authored-document-migration/spec.md)
