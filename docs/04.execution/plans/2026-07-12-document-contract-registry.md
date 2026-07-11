---
title: 'Document Contract Registry Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-12
---

# Document Contract Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the versioned Stage 99 registry, schema, classifier, and
fixtures that give every approved Markdown path exactly one document profile
or explicit exception.

**Architecture:** JSON Schema 2020-12 validates one declarative registry;
`scripts/document_contracts.py` owns importable registry and path interfaces,
and `scripts/validate-document-contract-registry.py` is a thin CLI/self-test
adapter. Compatibility mode reports later-tranche migration debt while
configuration errors and uncovered or ambiguous routes always fail.

**Tech Stack:** JSON Schema 2020-12, Python 3.11+, `jsonschema` 4.x, JSON,
Git, Bash, Markdown, `pre-commit`, and the repository quality gate.

## Global Constraints

- Work only in the isolated modernization worktree and its `codex/` branch.
- Use baseline SHA `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d` and require exactly 433 approved baseline Markdown paths.
- Approved root files are `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `README.md`; do not create a root `DESIGN.md`.
- Approved roots are `_workspace`, `.agents`, `.claude`, `.codex`, `.github`, `docs`, `examples`, `gitops`, `infrastructure`, `policy`, `scripts`, `secrets`, `tests`, and `traefik`.
- Keep `RTK.md`, `graphify-out/**`, `.worktrees/**`, ignored files, and followed symlink targets outside the classified corpus.
- Persist routes as exact paths or anchored regular expressions only; declaration order and first-match precedence have no meaning.
- Keep the five-key authored baseline `title`, `type`, `status`, `owner`, `updated`; add only the existing Archive Tombstone extension.
- README and native/control exception profiles forbid frontmatter.
- Keep affected-surface validator selection outside this registry; Spec 031 owns it.
- This tranche validates registry/config and path classification. Spec 029 owns the production Markdown parser and strict authored-body semantics.
- Do not read secret values or ignored authentication, log, token, certificate, kubeconfig, shell-history, or diagnostic content.
- Use `apply_patch` for content edits, run focused validation before every commit, and do not push or mutate live systems.

---

## Overview

This plan implements Spec 026 in five independently reviewable units: execution
lineage, schema and fixtures, the registry loader/classifier, full-corpus route
population, and compatibility-gate closure.

## Context

The current repository repeats document routes, key sets, state domains, and
template ownership in support prose and a large shell validator. Spec 026
replaces those parallel machine owners with one protected JSON contract while
leaving human rationale in Markdown.

## Goals & In-Scope

- Create a closed JSON Schema and one versioned document-profile registry.
- Provide reusable Python interfaces for schema loading, route matching, and
  fixed-plus-dynamic target enumeration.
- Cover every profile and exception class with positive and focused negative
  fixture cases.
- Account for all 433 baseline Markdown paths and all new target Markdown.
- Wire compatibility validation into the repository quality gate without
  enabling strict authored-document enforcement.

## Non-Goals & Out-of-Scope

- Production CommonMark/frontmatter semantic parsing, link ownership, and
  template-residue enforcement, which belong to Spec 029.
- README body migration, which belongs to Spec 028.
- Authored non-README migration and cloud relocation, which belong to Spec 030.
- CI selector or protected runtime behavior changes.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Machine contract | `docs/99.templates/support/document-profiles.schema.json`, `document-profiles.json` | Own persisted profile, route, metadata, state, heading, template, mode, and exception values. |
| Registry library | `scripts/document_contracts.py` | Own typed registry loading, deterministic route matching, corpus enumeration, and diagnostics consumed by Specs 029–031. |
| Registry CLI | `scripts/validate-document-contract-registry.py` | Expose repository validation and fixture self-test without duplicating library logic. |
| Contract fixtures | `tests/fixtures/document-contracts/registry-cases.json` | Define valid and one-fault invalid registry/config cases with exact rule IDs. |
| Governance consumer | `docs/99.templates/support/documentation-contract.md`, `frontmatter-schema.md`, `template-routing.md` | Explain ownership and link to the registry without copying complete tables. |
| Gate consumer | `scripts/validate-repo-quality-gates.sh`, `scripts/README.md`, `tests/README.md` | Invoke registry self-test and repository compatibility classification. |
| Execution evidence | Spec 026, this Plan, same-topic Task, Stage 03/04 indexes | Maintain reciprocal lineage and command evidence. |

### Persisted interfaces

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
```

`load_registry()` maps persisted JSON `id`, `class`, and `statusDomain` to the
typed `profile_id`, `profile_class`, and `status_domain` fields and exposes the
persisted `frontmatter`, `headings`, `template`, and `mode` values without
lossy defaults. It also exposes template inheritance through
`source_profile_ids`, placeholder handling through `placeholder_policy`, and
the progress fragment relationship through `append_contract`.

`enumerate_target_markdown()` is the only API that computes baseline/current
differences and returns the complete `TargetInventory`; Spec 029 consumers
iterate its `current_paths` field. With the canonical default
`include_paths=()`, `current_paths` contains only tracked index entries returned
by `git ls-files --stage -z`. A caller that must validate a named pre-stage file
passes that repository-relative path explicitly through `include_paths`; the
library never discovers all untracked files. All tuple fields are sorted by
their POSIX path string. `new_paths` is exactly
`current_paths - baseline_paths`.
Symlink entries remain visible in the two `*_symlink_paths` evidence fields but
are excluded from Markdown content validation and are never dereferenced.

### Exact profile and status-domain matrix

The registry must persist the following matrix without a global status
fallback. The empty domain means the profile forbids or does not interpret
frontmatter. Helper Spec profiles use the parent Spec lifecycle.

| Profile IDs | Class | Mode | Frontmatter | Exact `statusDomain` |
| --- | --- | --- | --- | --- |
| `sdlc/prd` | `sdlc` | `authored` | `required` | `draft`, `active`, `done`, `archived` |
| `sdlc/ard`, `sdlc/adr` | `sdlc` | `authored` | `required` | `draft`, `active`, `accepted`, `archived` |
| `sdlc/spec`, `sdlc/api-spec`, `sdlc/agent-design`, `sdlc/data-model`, `sdlc/tests` | `sdlc` | `authored` | `required` | `draft`, `active`, `done`, `archived` |
| `sdlc/plan`, `sdlc/task` | `sdlc` | `authored` | `required` | `draft`, `active`, `done`, `archived` |
| `sdlc/guide`, `sdlc/policy`, `sdlc/runbook`, `sdlc/incident`, `sdlc/postmortem` | `sdlc` | `authored` | `required` | `draft`, `active`, `accepted`, `archived` |
| `content/reference` | `common` | `authored` | `required` | `draft`, `active`, `accepted`, `done`, `archived` |
| `governance/reference`, `governance/memory`, `governance/template-support` | `governance` | `authored` | `required` | `draft`, `active`, `accepted`, `done`, `archived` |
| `content/archive-tombstone` | `common` | `authored` | `required` | `archived` |
| `governance/progress-ledger` | `governance` | `frontmatter-free` | `forbidden` | empty |
| `governance/progress-entry` | `governance` | `template` | `forbidden` | empty |
| every other `template/*` exact form profile | source class | `template` | exact source copy | exact source `statusDomain` copy |
| all `readme/*` profiles | `readme` | `frontmatter-free` | `forbidden` | empty |
| provider shims and GitHub-native control Markdown | `exception` | `frontmatter-free` | `forbidden` | empty |
| provider-native metadata and native contracts | `exception` | `native` | `not-applicable` | empty |
| generated records | `exception` | `generated` | `not-applicable` | empty |
| declared program exclusions | `exception` | `non-target` | `not-applicable` | empty |

These SDLC domains are copied exactly from the current canonical
`docs/99.templates/support/sdlc-governance.md`; Spec 026 does not narrow or
rename a state. Common and governance families retain the current validator's
five-state compatibility vocabulary because no narrower canonical lifecycle is
approved. Any later normalization must be a separately approved migration
decision with corpus evidence, not an implicit registry edit.

Every profile row also persists an exact `headings` object and `template`
value. Native, generated, and non-target profiles use empty heading tuples and
`template: null`; authored profiles use the canonical form path established by
Spec 027. `governance/progress-ledger` is the exact
`docs/00.agent-governance/memory/progress.md` route, has no frontmatter or form,
and requires only the H2 `Work Entries`. `governance/progress-entry` is the
frontmatter-free `progress.template.md` append fragment: it has no H2 contract
and carries `AppendContract(parent_profile_id='governance/progress-ledger',
parent_h2='Work Entries', entry_heading_level=3, section_heading_level=4,
required_sections=('Metadata', 'Progress', 'Memory', 'Evidence', 'Handoff'))`.
Authored/frontmatter-free source profiles use `source_profile_ids=()`,
`placeholder_policy='forbidden'`, and `append_contract=None`. Template profiles
use their declared source tuple and `placeholder_policy='template-only'`;
progress entry is the only template profile with a non-null append contract.

### Template-mode route contract

Every tracked `docs/99.templates/templates/**/*.template.md` path must resolve
to one exact-route profile in `mode: template`; a broad template-directory
exception is forbidden. Except for the progress append fragment, each template
profile:

- uses ID `template/<source-profile-id>` and one exact route to its form;
- sets `sourceProfileIds` to exactly one authored/frontmatter-free source
  profile, copies that source profile's `frontmatter`, `statusDomain`, and
  `headings` values without alteration, and points `template` to its own route;
- sets `placeholderPolicy: template-only`, allowing documented placeholders in
  form values/body while the corresponding source profile remains
  `placeholderPolicy: forbidden`; and
- is covered by a fixture that compares inherited objects for deep equality.

The current shared `common/readme.template.md` temporarily uses
`template/readme/common` with all six README source IDs. That row is valid only
while their frontmatter and heading objects are identical; Spec 028 must replace
or split the row in the same commit that makes README profile structures
diverge. The legacy `harness-task-contract.template.md` has its own exact
`template/sdlc/task-legacy-harness` row sourced from `sdlc/task` until Spec 027
deletes both the form and row. The progress form is the sole inheritance
exception: `governance/progress-entry` uses the explicit `AppendContract` above
instead of copying the ledger's H2 contract. Inventory rows such as
`docs/99.templates/templates/README.md` are routed as README documents, not as
forms.

Diagnostics use `RULE_ID path expected=<value> actual=<value> owner=<profile-or-stage>`.
Required rule IDs are `REGISTRY_SCHEMA`, `REGISTRY_PROFILE_ID`,
`REGISTRY_ROUTE_KIND`, `REGISTRY_ROUTE_ANCHOR`, `REGISTRY_ROUTE_AMBIGUOUS`,
`REGISTRY_ROUTE_UNCOVERED`, `REGISTRY_TEMPLATE`, `REGISTRY_BASELINE_SHA`, and
`REGISTRY_BASELINE_COUNT`.

## Work Breakdown

| Task | Description | Primary validation | Commit |
| --- | --- | --- | --- |
| DCR-001 | Start reciprocal Spec/Plan/Task lineage | Six reciprocal links and three index rows | `docs(execution): start document registry tranche` |
| DCR-002 | Define schema and fixture contract | Draft 2020-12 schema plus nine fixture cases | `feat(docs): define document profile registry schema` |
| DCR-003 | Implement loader and deterministic classifier | Self-test RED/GREEN and mini-corpus cases | `feat(validation): add document registry classifier` |
| DCR-004 | Populate profiles and classify the approved corpus | 433 baseline paths, zero overlaps/gaps | `feat(docs): classify document contract corpus` |
| DCR-005 | Integrate compatibility gate and close evidence | Quality gate, all-files, reciprocal completion | `docs(validation): close document registry evidence` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Contract | `python3 scripts/validate-document-contract-registry.py --self-test` | All positive and negative fixture expectations pass. |
| VAL-PLN-002 | Corpus | `python3 scripts/validate-document-contract-registry.py --root . --mode compatibility` | Baseline=433, uncovered=0, ambiguous=0. |
| VAL-PLN-003 | Repository | `bash scripts/validate-repo-quality-gates.sh .` | Required gates pass; no new strict migration rejection. |
| VAL-PLN-004 | Formatting | `git diff --check` and `pre-commit run --all-files` | No whitespace error; all applicable hooks pass. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Broad regex hides an incorrect route | High | Require `^...$`, reject overlaps, and add exact negative overlap cases. |
| Dynamic files obscure fixed baseline accounting | High | Report baseline and new-target sets separately and assert SHA/count. |
| Registry validator becomes a second semantic parser | High | Limit this tranche to configuration, paths, and fixture data; hand Markdown semantics to Spec 029. |
| Provider symlinks double-count files | Medium | Use Git tree entries and never recurse through symlink targets. |
| New dependency is absent in CI | High | Add an explicit `python3 -c` preflight and fail with install-owner guidance. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate:** Each task runs its focused RED/GREEN assertion and changed-file pre-commit checks.
- **Sandbox / Canary Rollout:** Compatibility mode classifies the real checkout but does not reject known body migration debt.
- **Human Approval Gate:** Required for a new universal key, profile family, exception class, remote publication, or live mutation.
- **Rollback Trigger:** Baseline count changes, any route overlap/gap, historical evidence loss, or current quality-gate regression.
- **Prompt / Model Promotion Criteria:** Not applicable; provider models and prompts are unchanged.

---

### Task 1: Start the Canonical Execution Chain

**Files:**

- Modify: `docs/03.specs/026-document-contract-registry/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-document-contract-registry.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: approved PRD 005, ARD 0008, ADRs 0015/0016, and Spec 026.
- Produces: active lineage with Task IDs `DCR-001` through `DCR-005` and exact links used by later evidence closure.

- [ ] **Step 1: Run the failing reciprocal-link assertion**

```bash
python3 - <<'PY'
from pathlib import Path
spec = Path('docs/03.specs/026-document-contract-registry/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-document-contract-registry.md')
task = Path('docs/04.execution/tasks/2026-07-12-document-contract-registry.md')
assert task.exists()
for source, target in ((spec, '../../04.execution/plans/2026-07-12-document-contract-registry.md'),
                       (spec, '../../04.execution/tasks/2026-07-12-document-contract-registry.md'),
                       (plan, '../../03.specs/026-document-contract-registry/spec.md'),
                       (plan, '../tasks/2026-07-12-document-contract-registry.md'),
                       (task, '../../03.specs/026-document-contract-registry/spec.md'),
                       (task, '../plans/2026-07-12-document-contract-registry.md')):
    assert target in source.read_text(encoding='utf-8'), (source, target)
PY
```

Expected: FAIL because the Task and reciprocal execution links do not exist.

- [ ] **Step 2: Create the active Task record and reciprocal links**

Create the Task from `task.template.md`, remove template authoring sections,
and use this exact task table:

```markdown
| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| DCR-001 | Start reciprocal execution lineage | doc | Reciprocal-link assertion | platform | Done |
| DCR-002 | Define schema and registry fixtures | contract | Schema fixture runner | platform | Queued |
| DCR-003 | Implement loader and deterministic classifier | guardrail | Registry self-test | platform | Queued |
| DCR-004 | Populate profiles and classify approved corpus | contract | 433-path compatibility result | platform | Queued |
| DCR-005 | Integrate gate and close evidence | validation | Full QA bundle | platform | Queued |
```

Set this Plan to `status: active`; add `Plan` and `Task` links to Spec 026;
add `Spec` and `Task` links to this Plan; add `Spec` and `Plan` links to the
Task. Add active rows dated `2026-07-12` to the three indexes.

- [ ] **Step 3: Re-run the reciprocal-link assertion**

Run the Step 1 command. Expected: PASS with no output.

- [ ] **Step 4: Validate and commit**

```bash
git diff --check
pre-commit run --files docs/03.specs/026-document-contract-registry/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-document-contract-registry.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-document-contract-registry.md docs/04.execution/tasks/README.md
git add docs/03.specs/026-document-contract-registry/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-document-contract-registry.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-document-contract-registry.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): start document registry tranche"
```

Expected: checks PASS and one logical commit is created.

---

### Task 2: Define the Closed Registry Schema and Fixture Contract

**Files:**

- Create: `docs/99.templates/support/document-profiles.schema.json`
- Create: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `tests/README.md`

**Interfaces:**

- Consumes: the `DocumentProfile` shape frozen by ADR 0015 and Spec 026.
- Produces: JSON Schema `$id` `https://hy-home.k8s/schemas/document-profiles-1.schema.json` and fixture cases consumed by `run_self_test()`.

- [ ] **Step 1: Add the nine-case fixture before the validator exists**

Use these exact case names and expected rule IDs:

```json
{
  "schemaVersion": 1,
  "cases": [
    {"name": "valid-minimal", "mutation": "none", "expected": []},
    {"name": "duplicate-profile-id", "mutation": "duplicate-profile-id", "expected": ["REGISTRY_PROFILE_ID"]},
    {"name": "unsupported-route-kind", "mutation": "route-kind-glob", "expected": ["REGISTRY_ROUTE_KIND"]},
    {"name": "unanchored-regex", "mutation": "drop-regex-end-anchor", "expected": ["REGISTRY_ROUTE_ANCHOR"]},
    {"name": "overlapping-route", "mutation": "add-overlapping-exact-route", "expected": ["REGISTRY_ROUTE_AMBIGUOUS"]},
    {"name": "uncovered-route", "mutation": "remove-sample-route", "expected": ["REGISTRY_ROUTE_UNCOVERED"]},
    {"name": "missing-template", "mutation": "point-to-missing-template", "expected": ["REGISTRY_TEMPLATE"]},
    {"name": "wrong-baseline-sha", "mutation": "change-baseline-sha", "expected": ["REGISTRY_BASELINE_SHA"]},
    {"name": "wrong-baseline-count", "mutation": "change-baseline-count", "expected": ["REGISTRY_BASELINE_COUNT"]}
  ]
}
```

- [ ] **Step 2: Run the missing-schema RED check**

```bash
python3 - <<'PY'
from pathlib import Path
assert Path('docs/99.templates/support/document-profiles.schema.json').exists()
PY
```

Expected: FAIL because the schema has not been created.

- [ ] **Step 3: Add the schema with closed objects**

Define root keys `$schema`, `$id`, `schemaVersion`, `baseline`, `target`,
`profiles`, and `programLineage`; require all seven and set
`additionalProperties: false`. A profile requires `id`, `class`, `mode`,
`routes`, `frontmatter`, `statusDomain`, `headings`, `template`,
`sourceProfileIds`, `placeholderPolicy`, and `appendContract`; route
objects allow only `{kind: exact|regex, value}`; frontmatter allows only
`mode`, `required`, `allowed`, and `order`; headings allows only `required` and
`allowed`. `appendContract` is either null or a closed object with
`parentProfileId`, `parentH2`, fixed heading levels `3` and `4`, and ordered
`requiredSections`. Require unique string arrays and `minItems: 1` for
`profiles`.

- [ ] **Step 4: Validate schema syntax and fixture shape**

```bash
python3 - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator
schema = json.loads(Path('docs/99.templates/support/document-profiles.schema.json').read_text())
Draft202012Validator.check_schema(schema)
cases = json.loads(Path('tests/fixtures/document-contracts/registry-cases.json').read_text())
assert len(cases['cases']) == 9
assert len({case['name'] for case in cases['cases']}) == 9
PY
```

Expected: PASS with no output.

- [ ] **Step 5: Document and commit the fixture interface**

Add `tests/README.md` inventory text stating that each registry case carries
one mutation and exact expected rule IDs and never contains secret data.

```bash
git diff --check
git add docs/99.templates/support/document-profiles.schema.json tests/fixtures/document-contracts/registry-cases.json tests/README.md
git commit -m "feat(docs): define document profile registry schema"
```

Expected: commit succeeds.

---

### Task 3: Implement the Registry Loader and Deterministic Classifier

**Files:**

- Create: `scripts/document_contracts.py`
- Create: `scripts/validate-document-contract-registry.py`
- Create: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/README.md`

**Interfaces:**

- Consumes: the schema and fixture contract from Task 2.
- Produces: the exact `Route`, `Diagnostic`, `FrontmatterContract`,
  `HeadingContract`, `DocumentProfile`, `Registry`, `TargetInventory`,
  `load_registry()`, `enumerate_target_markdown()`, and `classify_path()`
  interfaces above plus CLI flags `--root`, `--mode compatibility|strict`,
  `--profile`, repeatable `--include-path`, and `--self-test`.

- [ ] **Step 1: Add a minimal registry that classifies one sample path**

Use `schemaVersion: 1`, the exact baseline SHA/count, target root/file arrays
from Global Constraints, program lineage `prd: 005`, `ard: 0008`,
`specs: [026,027,028,029,030,031,032]`, and one temporary `test/sample`
profile restricted to the self-test fixture root. Populate its required
`sourceProfileIds: []`, `placeholderPolicy: forbidden`, and
`appendContract: null` fields so the minimal registry exercises the complete
schema.

- [ ] **Step 2: Run the missing-validator RED check**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
```

Expected: FAIL with `No such file or directory`.

- [ ] **Step 3: Implement the typed importable registry library**

In `scripts/document_contracts.py`, define the exact dataclasses and functions
from the File and Interface Map. Use `Draft202012Validator`, reject duplicate IDs
after schema validation, compile regex routes, require both `^` and `$`,
normalize POSIX relative paths, reject leading `./`, absolute paths,
backslashes, and `..`, require one match, and check every non-null template path
exists under the repository root.

- [ ] **Step 4: Implement and test the mode-aware baseline parser**

Run `git ls-tree -rz --full-tree <sha>` and parse each NUL-delimited record as
`<mode> SP <type> SP <object> TAB <path>`; do not use `--name-only`, because the
mode is required to identify `120000` symlinks. Expose an internal
`_parse_ls_tree_z(raw: bytes)` helper and verify it before adding enumeration:

```bash
python3 - <<'PY'
from scripts.document_contracts import _parse_ls_tree_z
oid = b'0' * 40
raw = (b'100644 blob ' + oid + b'\tdocs/a.md\0' +
       b'120000 blob ' + oid + b'\t.codex/skills\0')
entries = _parse_ls_tree_z(raw)
assert [(entry.mode, entry.path.as_posix()) for entry in entries] == [
    ('100644', 'docs/a.md'), ('120000', '.codex/skills')]
PY
```

Expected: PASS without resolving `.codex/skills`.

- [ ] **Step 5: Implement and test current-tree inventory assembly**

Enumerate current paths only from mode-aware `git ls-files --stage -z` records.
Do not invoke broad untracked discovery and do not walk the filesystem. For each
explicit `include_paths` value, reject an absolute/`..`/backslash path, reject
ignored paths, inspect the named entry with `Path.lstat()` without resolution,
and add it only if it is a regular approved Markdown path. Filter tracked
regular Markdown entries by approved roots/files and declared non-targets,
sort all sets, and return one `TargetInventory`. A `120000` entry is recorded
in the matching symlink evidence tuple, excluded from the content path tuples,
and never opened or treated as a directory. Implement
`enumerate_target_markdown()` as the single `TargetInventory` producer; do not
add a list-returning or discover-all-untracked alternate.

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
from scripts.document_contracts import enumerate_target_markdown
inventory = enumerate_target_markdown(Path('.'))
assert len(inventory.baseline_paths) == 433
assert inventory.new_paths == tuple(sorted(set(inventory.current_paths) - set(inventory.baseline_paths), key=str))
assert all(path not in inventory.current_paths for path in inventory.current_symlink_paths)
for path in inventory.current_paths:
    subprocess.run(['git', 'ls-files', '--error-unmatch', '--', path.as_posix()],
                   check=True, stdout=subprocess.DEVNULL)
PY
```

Expected: PASS with tracked-only deterministic tuples and no dereferenced
provider view. Add focused self-test cases proving one explicitly included
untracked Markdown path is included and an ignored or symlink include is
rejected without traversal.

- [ ] **Step 6: Implement the thin CLI and fixture mutations through production functions**

Each of the nine fixture cases must clone the minimal registry in memory,
apply only its named mutation, call `validate_registry()` and
`classify_paths()`, and compare the ordered unique rule-ID set with `expected`.
The CLI imports these functions from `document_contracts`; it must not redefine
route matching or enumeration.

- [ ] **Step 7: Run self-test GREEN**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
```

Expected: `PASS document contract registry self-test: 9 cases`.

- [ ] **Step 8: Document CLI and commit**

Add a `scripts/README.md` inventory row with Tier A, repository-static scope,
all five CLI flags, tracked-only default semantics, explicit `--include-path`
behavior, `jsonschema` preflight, and PASS/FAIL semantics.

```bash
python3 -m py_compile scripts/document_contracts.py scripts/validate-document-contract-registry.py
git diff --check
git add scripts/document_contracts.py scripts/validate-document-contract-registry.py scripts/README.md docs/99.templates/support/document-profiles.json
git commit -m "feat(validation): add document registry classifier"
```

Expected: compilation and commit succeed.

---

### Task 4: Populate Profiles and Classify the Approved Corpus

**Files:**

- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`

**Interfaces:**

- Consumes: `matching_profile_ids()` and
  `enumerate_target_markdown().{baseline_paths,current_paths,new_paths}`.
- Produces: profile classes `sdlc`, `common`, `governance`, `readme`, and `exception` with zero route gaps or overlaps.

- [ ] **Step 1: Run the incomplete-registry RED check**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
```

Expected: FAIL with `REGISTRY_ROUTE_UNCOVERED` and real repository paths.

- [ ] **Step 2: Populate exact metadata profiles**

Declare the current types `sdlc/prd`, `sdlc/ard`, `sdlc/adr`, `sdlc/spec`,
`sdlc/api-spec`, `sdlc/agent-design`, `sdlc/data-model`, `sdlc/tests`,
`sdlc/plan`, `sdlc/task`, `sdlc/guide`, `sdlc/policy`, `sdlc/runbook`,
`sdlc/incident`, `sdlc/postmortem`, `content/reference`,
`content/archive-tombstone`, `governance/reference`, `governance/memory`, and
`governance/template-support`. Use required/allowed/order five-key arrays for
all authored profiles, the nine-key Tombstone array, and the exact class,
mode, frontmatter, and status-domain matrix above. Do not accept the current
global five-state vocabulary as a per-profile fallback.

- [ ] **Step 3: Populate README and exception profiles**

Declare six README IDs `readme/repository`, `readme/stage-index`,
`readme/collection-index`, `readme/implementation`, `readme/snapshot-pack`, and
`readme/workspace-staging` with forbidden frontmatter. Declare named exceptions
for root provider shims, provider-native metadata, GitHub-native control
Markdown, native contracts, generated records, and explicit program non-targets.

Declare `governance/progress-ledger` as the exact frontmatter-free ledger route
with required H2 `Work Entries`, and declare `governance/progress-entry` as the
exact progress fragment template route with the H3/H4 append contract above.
Then add one exact `mode: template` route for every other tracked
`*.template.md` form using the Template-mode route contract. The self-test must
compare every template row's inherited frontmatter, status, and headings with
its source profile and assert `placeholderPolicy: template-only`.

- [ ] **Step 4: Add one positive fixture per profile/exception class**

Add `profileCoverage` entries containing exact sample `path` and `profile`.
The self-test must assert every registry profile ID appears exactly once in
that fixture collection and each sample classifies to the declared ID. Add a
separate `templateCoverage` row for every tracked `*.template.md` path; assert
the set equals `git ls-files 'docs/99.templates/templates/**/*.template.md'`,
each path has one exact template-mode route, and the progress fragment is the
only row governed by `appendContract` instead of source-object equality.

- [ ] **Step 5: Run full-corpus GREEN validation**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
```

Expected: self-test PASS; repository output includes
`PASS baseline=433 new=<program-created-count> uncovered=0 ambiguous=0`.

- [ ] **Step 6: Commit the complete registry**

```bash
git diff --check
git add docs/99.templates/support/document-profiles.json tests/fixtures/document-contracts/registry-cases.json
git commit -m "feat(docs): classify document contract corpus"
```

Expected: commit succeeds.

---

### Task 5: Integrate Compatibility Validation and Close the Tranche

**Files:**

- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/03.specs/026-document-contract-registry/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-document-contract-registry.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-document-contract-registry.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: completed registry CLI and exact owner paths.
- Produces: one quality-gate invocation and completed reciprocal evidence for Spec 027.

- [ ] **Step 1: Run the missing-integration RED assertion**

```bash
python3 - <<'PY'
from pathlib import Path
gate = Path('scripts/validate-repo-quality-gates.sh').read_text()
assert 'validate-document-contract-registry.py" --self-test' in gate
assert 'validate-document-contract-registry.py" --root "$ROOT_DIR" --mode compatibility' in gate
PY
```

Expected: FAIL because the quality gate does not invoke the new validator.

- [ ] **Step 2: Replace copied machine-owner claims with registry links**

In the three support documents, state that JSON owns exact routes, key sets,
states, headings, and templates; keep rationale and examples; remove copied
full tables only when the registry contains their facts. Do not redesign Stage
99 README bodies in this tranche.

- [ ] **Step 3: Add dependency preflight and compatibility invocations**

In the `repo-quality-static` dependency step, change the install command to
`python -m pip install --disable-pip-version-check pyyaml jsonschema`. Immediately
after the existing PyYAML preflight, require `python3 -c 'import jsonschema'`;
invoke registry self-test and repository compatibility classification before
the embedded legacy checks. Keep the old checks active as compatibility gates
through Spec 030. Do not change Action references, permissions, or CI selector
semantics in this task.

- [ ] **Step 4: Run the complete verification bundle**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

Expected: every applicable check PASS; optional tool skips remain labeled.

- [ ] **Step 5: Close lifecycle and evidence**

Set Spec 026, this Plan, and its Task to `done`; set all DCR rows to `Done`;
record commands, PASS/SKIP limitations, reviewer, and rollback commit range;
update the three index rows to `Done`; link Spec 027 as the next consumer.

- [ ] **Step 6: Commit closure**

```bash
git add docs/99.templates/support/documentation-contract.md docs/99.templates/support/frontmatter-schema.md docs/99.templates/support/template-routing.md scripts/validate-repo-quality-gates.sh .github/workflows/ci.yml docs/03.specs/026-document-contract-registry/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-document-contract-registry.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-document-contract-registry.md docs/04.execution/tasks/README.md
git commit -m "docs(validation): close document registry evidence"
```

Expected: one closure commit and a clean focused diff.

## Completion Criteria

- [ ] Registry schema, data, loader, classifier, and fixtures exist.
- [ ] Baseline 433 and every new target Markdown path classify exactly once.
- [ ] Nine negative/positive config cases and profile coverage pass.
- [ ] Support docs point to one machine owner without premature README redesign.
- [ ] Repository quality and all-files validation pass in compatibility mode.
- [ ] Reciprocal Spec/Plan/Task links and index states are complete.

## Related Documents

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Planned Tasks**: `../tasks/2026-07-12-document-contract-registry.md` (created by DCR-001)
