---
title: 'Authored Document Migration Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-12
---

# Authored Document Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the approved authored-document corpus to strict document
profiles while preserving historical evidence, consolidating duplicate cloud
documentation, and publishing durable per-document research decisions.

**Architecture:** Generate a read-only inventory from Spec 029, promote reviewed
rows to one durable Current research ledger, and migrate one ownership family at
a time. Every wave clears named compatibility debt, passes link/owner checks,
receives independent review, and ends at a rollback commit before the next wave.

**Tech Stack:** Markdown, YAML Frontmatter, Python 3 validators, Git and `git mv`,
official primary-source research, `rg`, pre-commit, and repository quality gates.

## Global Constraints

- Work only in the isolated worktree for branch `codex/workspace-document-assurance-modernization`.
- Baseline identity is commit `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d` and its approved 433-Markdown target corpus; separately account for program-created documents.
- Allowed dispositions are exactly `preserve`, `transform`, `merge`, `relocate`, `tombstone`, and `delete`.
- Preserve completed Plan/Task evidence, accepted ADR history, dated audit/research facts, archive Tombstones, generated-owner boundaries, and provider-native metadata.
- Do not blindly rewrite files or replace topic-specific content with template prose.
- Every migrated current authored document needs one durable research row; external technical claims use applicable official primary sources.
- Repository-only decisions record `external-topic: not applicable` with a concrete reviewed reason.
- Do not read, enumerate, move, or delete ignored `.env`, token, key, certificate, kubeconfig, shell-history, local-setting, or diagnostic content.
- README redesign belongs to Spec 028; this Plan may make relocation-driven index/link updates only.
- Validators belong to Spec 029; this Plan consumes their public interfaces and
  changes only the two finite Spec-030-owned debt fixtures at the transitions
  named below. The profile registry never contains migration debt.
- Protected machine surfaces and behavior belong to Spec 032; this Plan changes only their authored documentation and links.
- Use `apply_patch` for edits, `git mv` for one-to-one relocations, and a separate logical commit for every migration wave.

---

## Overview

This Plan implements Spec 030 in seven reviewable waves: execution-chain
startup, durable inventory, Stages 01–03, Stages 04–05, remaining governance and
reference bodies, AWS/Azure consolidation, and strict cutover.

## Context

The approved corpus contains five PRDs, five ARDs, eleven ADRs, twenty-nine
Stage 03 artifacts, forty-three Plans, forty-five Tasks, twenty-four Guide/
Policy/Runbook documents, thirty-five non-README Stage 90 documents, thirty-one
Archive Tombstones, and fifty-nine AWS/Azure example-local Markdown files.
Compatibility mode must stay available until these families are reconciled.

## Goals & In-Scope

- Apply profile-specific Frontmatter, status, section, and authority rules.
- Remove copied authoring instructions, duplicated sections, stale authority
  claims, broken links, and duplicate current owners.
- Preserve historical facts and destructive-change rollback evidence.
- Consolidate AWS/Azure prose into dated provider snapshots while keeping
  executable examples and implementation entrypoints.
- Enable strict document validation with zero migration debt.

## Non-Goals & Out-of-Scope

- Rewriting historical evidence for current style or technology versions.
- Changing Action identities, workflow permissions, agent roles/models,
  Kubernetes manifests, infrastructure behavior, policy behavior, secrets, or
  live cluster/Vault/Argo CD state.
- Creating a root `DESIGN.md`.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Durable evidence | `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md` | Full disposition, topic-source, content decision, reviewer, result, and refresh evidence. |
| Active design | `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**` | Current requirement, architecture, decision, and technical-contract content. |
| Execution and operations | `docs/04.execution/**`, `docs/05.operations/**` | Historical execution evidence and current operational guidance/control/procedure. |
| Governance and references | non-README `docs/00.agent-governance/**`, Current Stage 90, `docs/98.archive/**` | Canonical governance, current research, and historical/current authority boundaries. |
| Cloud snapshots | `docs/90.references/cloud-examples/{aws,azure}/2026-07-12-*-example-snapshot.md` | Dated official-source comparison and retained unique cloud-example knowledge. |
| Executable examples | `examples/{aws,azure}/**` excluding deleted `docs/**` | Executable Terraform/Bicep/Kubernetes/GitOps assets and entrypoint links. |
| Finite shape debt | `tests/fixtures/document-contracts/template-compatibility.json`, `scripts/validate-repo-quality-gates.sh` | ADM-003 through ADM-006 remove exact canonicalized path records and refresh the complete-fixture digest/mutation proof in the same commit. |
| Finite semantic debt | `tests/fixtures/document-contracts/semantic-compatibility-debt.json` | ADM-002 removes the sole ledger-missing item in the commit that creates the complete ledger; ADM-007 removes the empty compatibility container. |
| Strict cutover | the two finite debt fixtures and `scripts/validate-repo-quality-gates.sh` | Remove empty compatibility containers and enforce strict repository validation; never add, remove, or describe registry debt. |

### Durable Ledger Interface

```text
path | title | profile | owner-key | disposition | destination | local-evidence | official-sources | observed-version | applicability | content-decision | refresh-trigger | reviewer | result
```

### Inventory Count Transition

SMDV-003 closed with 467 current paths, but ADM-001 added the authored Task as
a normal registry target. ADM-002 Step 1 therefore starts from 468 current
paths (`baseline=433`, `new=37`). ADM-002 then creates the durable ledger as a
normal `content/reference` target and passes its exact path through the
validator's supported `--include-path` option before staging. The final ADM-002
inventory and ledger therefore contain 469 paths (`baseline=433`, `new=38`),
including exactly one self-row for the ledger. ADM-003 and every later task
start from 469/current and 38/new until that task's independently declared
creation, relocation, or deletion manifest proves a different count. The
ledger is never made non-target to avoid this transition.

### Pre-ADM Hard Dependency

No ADM Task may start until the logical commit
`fix(plans): align semantic debt removal lifecycle` contains this Plan and the
Spec 029 Plan together with one canonical append-only entry in
`docs/00.agent-governance/memory/progress.md`, and proves their handoff is
identical: the sole semantic item is removed by ADM-002; exact template-shape
path records are removed by ADM-003 through ADM-006; ADM-007 cleans only empty
debt containers and switches the wrapper to strict; the profile registry is
never a debt owner. This Plan correction satisfies the planning dependency
when that exact three-file commit passes focused QA. It does not authorize
migration implementation by itself.

For ADM-003 through ADM-006, each Task first exports its exact matched debt
records to an ignored `_workspace/adm-NNN-debt-removals.json` manifest. The
manifest records sorted path/rule/token tuples and exact before/removed/after
path, obligation, occurrence, and union counts. Independent review approves
that finite manifest before edits. In the same wave commit, every path in it is
canonicalized, its exact records are removed from
`template-compatibility.json`, all aggregate caps are recomputed downward, and
the complete semantic fixture digest plus every existing and affected-path /
rule-cap / union-count mutation proof is refreshed in
`scripts/validate-repo-quality-gates.sh`. Set equality is mandatory: no
canonicalized debt path may remain, and no record for an untouched path may be
removed.

Before ADM-002 creates any ledger row, run this fixture-owned coverage gate.
It is the executable ownership contract for all 266 pre-registered shape-debt
paths: ADM-003 owns 34, ADM-004 owns 120, ADM-005 owns 73, and ADM-006 owns 39.
The sets are pairwise disjoint and their union is the complete fixture path
set; a stranded or multiply owned path blocks ADM-002.

```bash
python3 - <<'PY'
import json
import pathlib

fixture = json.loads(pathlib.Path(
    'tests/fixtures/document-contracts/template-compatibility.json'
).read_text())
debt_paths = {
    affected['path']
    for profile in fixture['compatibilityDebt']
    for affected in profile['affectedPaths']
}
support_paths = {
    'docs/99.templates/support/common-documentation-governance.md',
    'docs/99.templates/support/documentation-contract.md',
    'docs/99.templates/support/frontmatter-schema.md',
    'docs/99.templates/support/legacy-cleanup-rules.md',
    'docs/99.templates/support/sdlc-governance.md',
    'docs/99.templates/support/template-routing.md',
}
adm003 = {path for path in debt_paths if path.startswith((
    'docs/01.requirements/', 'docs/02.architecture/requirements/',
    'docs/02.architecture/decisions/', 'docs/03.specs/',
))}
adm004 = {path for path in debt_paths if path.startswith((
    'docs/04.execution/plans/', 'docs/04.execution/tasks/',
    'docs/05.operations/',
))}
adm006 = {path for path in debt_paths if path.startswith((
    'examples/aws/docs/', 'examples/azure/docs/',
))}
adm005 = debt_paths - adm003 - adm004 - adm006
assert support_paths <= adm005
assert all(path.startswith((
    'docs/00.agent-governance/', 'docs/90.references/', 'docs/98.archive/',
)) or path in support_paths for path in adm005)
waves = {'ADM-003': adm003, 'ADM-004': adm004, 'ADM-005': adm005, 'ADM-006': adm006}
assert {name: len(paths) for name, paths in waves.items()} == {
    'ADM-003': 34, 'ADM-004': 120, 'ADM-005': 73, 'ADM-006': 39,
}
names = list(waves)
for index, left in enumerate(names):
    for right in names[index + 1:]:
        assert waves[left].isdisjoint(waves[right]), (left, right)
assert set().union(*waves.values()) == debt_paths
assert len(debt_paths) == 266
PY
```

Before any content mutation, the same Task must freeze
`_workspace/adm-NNN-allowed-document-paths.nul`. Its sorted `documentPaths`
come from the reviewed migration/debt manifest, are a subset of the Task's
tracked eligible paths from `git ls-files`, include every path named by a debt
tuple, and may add only the Task's exact declared new destinations or
relocation-only README paths. README paths and the Task's explicit exclusions
are absent unless that Task's Files list names the exact README path. Record the
manifest path count and SHA-256 in the Task evidence and obtain independent
approval before the first edit. The count/SHA are immutable for the wave.

After edits, define `fixed` as the exact ledger, Task, progress, compatibility
fixture, quality-gate consumer, and other non-document evidence files listed by
that ADM Task. The staged document set must equal the paths from the frozen
allowed manifest that actually differ from `HEAD`; it must be a subset of the
frozen manifest, contain no excluded path, and include every path whose debt
record was removed. The complete cached set must equal that changed-document
set union `fixed`. Deriving an allowed or expected set from a post-edit broad
directory diff is prohibited.

## Work Breakdown

| Task | Deliverable | Primary validation | Commit |
| --- | --- | --- | --- |
| ADM-001 | Reciprocal execution chain | Lineage assertion | `docs(execution): start authored document migration` |
| ADM-002 | Baseline disposition and research ledger | Inventory/ledger validation | `docs(migration): inventory authored document dispositions` |
| ADM-003 | Stage 01–03 normalization | Full-corpus JSON filtered to exact reviewed paths | `docs(migration): normalize active sdlc design documents` |
| ADM-004 | Stage 04–05 normalization | Execution/operations compatibility checks | `docs(migration): normalize execution and operations documents` |
| ADM-005 | Governance/reference/archive normalization | Link, owner, and preserve-boundary checks | `docs(migration): normalize governance references and archive links` |
| ADM-006 | AWS/Azure consolidation | Zero example-local docs and valid snapshot links | `docs(migration): consolidate cloud example documentation` |
| ADM-007 | Strict cutover and closure | Strict validators, quality gate, all-files pre-commit | `chore(docs): cut over document profiles to strict validation` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-030-001 | Inventory | `validate-links-and-owners.py --inventory --format json` | Pre-ledger 468/current is exact; ADM-002 final inventory uses the ledger `--include-path` and classifies 469/current and 38/new exactly once, including its pinned self-row. |
| VAL-030-002 | Wave | `validate-markdown-profiles.py --mode compatibility --format json` plus deterministic filtering | RED preserves the validator exit code and selects a nonempty all-`DEFER` diagnostic set; every batch and GREEN gate select exact reviewed path sets, and GREEN selects zero diagnostics. |
| VAL-030-003 | Research | strict link/owner validator | Every migrated current document has one complete durable row. |
| VAL-030-004 | Cloud | directory-based `git ls-files examples/aws/docs examples/azure/docs` source/ledger comparison | All 59 source paths have durable ledger rows before deletion; no example-local SDLC Markdown remains afterward. |
| VAL-030-005 | Strict | all three document validators in strict mode | Zero debt, unknown route, duplicate owner, incomplete ledger, or broken link. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical facts are silently modernized | High | Preserve bodies and change only incorrect current-authority routing. |
| Destructive consolidation loses unique content | High | Ledger source set, official comparison, independent review, and rollback commit precede deletion. |
| README ownership is violated | High | Limit README work to approved relocation-driven rows using Spec 028 forms. |
| Research rows become generic citations | High | Require applicability, adopted/rejected guidance, content decision, and refresh trigger per path. |
| One wave obscures unrelated changes | High | Stage only the exact family plus its ledger rows and execution evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate:** Each wave consumes one full-corpus Markdown JSON result,
  filters it deterministically to the reviewed exact path set, proves the RED
  selection is nonempty and all `DEFER`, proves every batch/GREEN selection is
  empty, and passes link/owner validation without masking either validator exit
  code.
- **Sandbox / Canary Rollout:** Compatibility mode remains canonical through ADM-006.
- **Human Approval Gate:** Required before deletion, accepted-ADR supersession, remote push, merge, or protected/live changes.
- **Rollback Trigger:** Unique-content loss, historical evidence drift, duplicate current owner, incomplete research, or unresolved link regression.
- **Prompt / Model Promotion Criteria:** Not applicable; agent model changes are outside Spec 030.

---

### Task 1: Start Reciprocal Execution Lineage

**Files:**

- Modify: `docs/03.specs/030-authored-document-migration/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-authored-document-migration.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: active Spec 030, completed Specs 026–029, and this Plan.
- Produces: Task IDs `ADM-001` through `ADM-007` and reciprocal execution lineage.

- [x] **Step 1: Run RED lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
 Path('docs/03.specs/030-authored-document-migration/spec.md'),
 Path('docs/04.execution/plans/2026-07-12-authored-document-migration.md'),
 Path('docs/04.execution/tasks/2026-07-12-authored-document-migration.md'),
]
assert all(path.exists() for path in paths), paths
for source in paths:
    text = source.read_text(encoding='utf-8')
    for target in paths:
        if target != source:
            assert target.name in text, (source, target)
PY
```

Expected: FAIL because the execution Task and reciprocal links do not exist.

- [x] **Step 2: Create the active Task and exact seven-row table**

Use the five canonical Frontmatter keys, `status: active`, and one row for every
`ADM-001` through `ADM-007` Work Breakdown item with its exact command and
commit message.

- [x] **Step 3: Add reciprocal links and active index rows**

Update Spec, Plan, Task, and the three Stage indexes only. Preserve all unrelated
index order and content.

- [x] **Step 4: Run GREEN lineage and focused QA**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [Path('docs/03.specs/030-authored-document-migration/spec.md'), Path('docs/04.execution/plans/2026-07-12-authored-document-migration.md'), Path('docs/04.execution/tasks/2026-07-12-authored-document-migration.md')]
for source in paths:
    text = source.read_text(encoding='utf-8')
    assert source.exists()
    for target in paths:
        if target != source:
            assert target.name in text
PY
git diff --check
pre-commit run --files docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md
```

Expected: assertion and applicable hooks PASS.

- [x] **Step 5: Commit**

```bash
git add docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/03.specs/030-authored-document-migration/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-authored-document-migration.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
    'docs/04.execution/tasks/README.md',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected and len(actual) == 7, (sorted(actual), sorted(expected))
PY
git commit -m "docs(execution): start authored document migration"
```

Expected: exactly seven staged paths. A fresh reviewer verifies reciprocal
lineage, the seven Task rows, lifecycle/index state, progress evidence, and
the exact staged set. Roll back with `git revert <ADM-001-commit>`.

---

### Task 2: Publish the Baseline Disposition and Research Ledger

**Files:**

- Create: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`
- Modify: `tests/fixtures/document-contracts/semantic-compatibility-debt.json`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the post-ADM-001 `--inventory --format json` envelope whose
  `documents[].path` is the exact sorted 468-path `current_paths` set, the same
  validator's explicit `--include-path` transition to 469 after ledger
  creation, and the Spec 027 type-to-source matrix.
- Produces: exact fourteen-column durable ledger consumed by strict
  cross-document validation and an empty semantic-debt item set.

- [ ] **Step 1: Generate ignored scratch inventory**

```bash
python3 scripts/validate-links-and-owners.py --root . --inventory --format json > _workspace/document-migration-inventory.json
python3 -m json.tool _workspace/document-migration-inventory.json >/dev/null
python3 - <<'PY'
import json
import pathlib
import sys

sys.path.insert(0, 'scripts')
from document_contracts import enumerate_target_markdown

data = json.loads(pathlib.Path('_workspace/document-migration-inventory.json').read_text())
assert list(data) == [
    'schemaVersion', 'mode', 'outcome', 'counts', 'documents', 'diagnostics'
]
assert data['schemaVersion'] == 1
assert data['mode'] == 'inventory' and data['outcome'] == 'PASS'
assert data['counts'] == {
    'baseline': 433, 'current': 468, 'new': 37, 'documents': 468
}
assert data['diagnostics'] == []
expected = [
    path.as_posix()
    for path in enumerate_target_markdown(pathlib.Path('.')).current_paths
]
actual = [item['path'] for item in data['documents']]
assert actual == expected == sorted(actual) and len(set(actual)) == 468
PY
```

Expected: the one deterministic pre-ledger inventory envelope, exact counts,
and exact ordered 468-path equality pass; no tracked `_workspace` child is
created. This snapshot is input to ledger creation, not the final ADM-002
inventory.

- [ ] **Step 2: Run RED ledger validation**

```bash
python3 scripts/validate-links-and-owners.py --root . --mode strict
```

Expected: exit 1 with `LEDGER-MISSING` or `LEDGER-INCOMPLETE`.

- [ ] **Step 3: Create the durable ledger**

Use the common Reference profile and one table with exactly the fourteen
columns declared above. Its body has exactly these eight H2 sections in order:
`Overview`, `Reference Type`, `Authority Boundary`, `Scope`,
`Definitions / Facts`, `Sources`, `Review and Freshness`, and
`Related Documents`. The sole fourteen-column table is directly under
`Definitions / Facts`; do not create an earlier path-header table. Start with
one row per Step 1 `documents[].path`, then
add the ledger's own row before producing the final inventory. No other path
may appear. The ledger frontmatter is pinned to title `Document Migration
Evidence Ledger`, type `content/reference`, status `active`, owner `platform`,
and updated date `2026-07-13`; its inventory classification is pinned to
profile `content/reference`, class `common`, mode `authored`, empty `ownerKey`,
and origin `program-created`. Its ledger self-row literals are pinned by the
Step 4 assertion. Every other row names baseline or program-created local
evidence, disposition, destination, applicable official source or reviewed
non-applicability reason, content decision, refresh trigger, reviewer, and
initial `inventory-reviewed` result. Every table cell serializes a literal pipe
as `&#124;`, especially `path`, `title`, and `owner-key`; multiple source links
or URLs are separated with `<br>`, never a raw `|`. A nonempty title uses the
inventory title when present, otherwise the first visible H1, otherwise
`PurePosixPath(path).stem`. All six disposition values are limited to
`preserve`, `transform`, `merge`, `relocate`, `tombstone`, or `delete`.
Destination is required even for `delete`, which uses an explicit reviewed
`not applicable - no successor approved` value. The ledger self-row owner-key
remains empty, and every row still requires the other thirteen cells.

Disposition assignment is deterministic and ordered. First, all 59 tracked
`examples/aws/docs/**` and `examples/azure/docs/**` source paths are `merge`
rows targeting their provider snapshot; this rule takes precedence for the 39
cloud paths that also have shape debt. Next, every remaining path in the exact
266-path fixture coverage set is `transform` with itself as destination,
including completed-history documents and the structurally scoped Spec
027/031 handoff paths. Every other current path, including the new ledger
self-row, is `preserve` with itself as destination. The final 469-row ledger
must therefore contain exactly `preserve=183`, `transform=227`, and `merge=59`,
with zero `relocate`, `tombstone`, or `delete` rows at ADM-002.

- [ ] **Step 4: Verify completeness and tracked boundary**

In the same edit that makes the durable ledger complete, remove the one exact
`LEDGER-MISSING` / `ADM-002` item from
`semantic-compatibility-debt.json`. Keep its schema, owner, and
`growthAllowed: false` container until ADM-007. Before staging, prove strict
mode sees no ledger violation and compatibility has no `DEFER` or
`DEBT-UNUSED` semantic item.

```bash
set -u
overall_rc=0
ledger_path='docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md'
final_inventory='_workspace/document-migration-final-inventory.json'

inventory_rc=0
python3 scripts/validate-links-and-owners.py --root . --inventory --format json \
  --include-path "$ledger_path" >"$final_inventory" || inventory_rc=$?
if [ "$inventory_rc" -ne 0 ]; then
  overall_rc="$inventory_rc"
fi
if [ "$overall_rc" -eq 0 ]; then
  python3 -m json.tool "$final_inventory" >/dev/null || overall_rc=$?
fi
if [ "$overall_rc" -eq 0 ]; then
  python3 - "$final_inventory" "$ledger_path" <<'PY' || overall_rc=$?
import json
import pathlib
import sys

sys.path.insert(0, 'scripts')
from document_contracts import enumerate_target_markdown

inventory = json.loads(
    pathlib.Path(sys.argv[1]).read_text()
)
ledger_path = sys.argv[2]
assert list(inventory) == [
    'schemaVersion', 'mode', 'outcome', 'counts', 'documents', 'diagnostics'
]
assert inventory['counts'] == {
    'baseline': 433, 'current': 469, 'new': 38, 'documents': 469
}
assert inventory['diagnostics'] == []
inventory_paths = [item['path'] for item in inventory['documents']]
expected = [
    path.as_posix()
    for path in enumerate_target_markdown(
        pathlib.Path('.'), include_paths=(pathlib.PurePosixPath(ledger_path),)
    ).current_paths
]
assert inventory_paths == expected == sorted(inventory_paths)
assert len(inventory_paths) == len(set(inventory_paths)) == 469
own_inventory = next(item for item in inventory['documents'] if item['path'] == ledger_path)
assert own_inventory == {
    'path': ledger_path,
    'profile': 'content/reference',
    'profileClass': 'common',
    'mode': 'authored',
    'title': 'Document Migration Evidence Ledger',
    'status': 'active',
    'ownerKey': '',
    'origin': 'program-created',
}
ledger = pathlib.Path(ledger_path).read_text().splitlines()
assert [line[3:] for line in ledger if line.startswith('## ')] == [
    'Overview', 'Reference Type', 'Authority Boundary', 'Scope',
    'Definitions / Facts', 'Sources', 'Review and Freshness',
    'Related Documents',
]
header = (
    '| path | title | profile | owner-key | disposition | destination | '
    'local-evidence | official-sources | observed-version | applicability | '
    'content-decision | refresh-trigger | reviewer | result |'
)
start = ledger.index(header)
definitions_index = ledger.index('## Definitions / Facts')
sources_index = ledger.index('## Sources')
assert definitions_index < start < sources_index
assert ledger.count(header) == 1
rows = []
for line in ledger[start + 2:]:
    if not line.startswith('|'):
        break
    cells = [cell.strip() for cell in line.strip('|').split('|')]
    assert len(cells) == 14, (len(cells), line)
    rows.append(cells)
ledger_paths = [
    row[0].removeprefix('`').removesuffix('`').replace('&#124;', '|')
    for row in rows
]
assert ledger_paths == inventory_paths
assert len(ledger_paths) == len(set(ledger_paths)) == 469
inventory_by_path = {item['path']: item for item in inventory['documents']}
dispositions = {'preserve', 'transform', 'merge', 'relocate', 'tombstone', 'delete'}
for row in rows:
    path = row[0].removeprefix('`').removesuffix('`')
    item = inventory_by_path[path]
    source = pathlib.Path(path).read_text(encoding='utf-8')
    visible_h1 = next(
        (line[2:].strip() for line in source.splitlines() if line.startswith('# ')),
        '',
    )
    expected_title = item['title'] or visible_h1 or pathlib.PurePosixPath(path).stem
    assert row[0] == f'`{item["path"].replace("|", "&#124;")}`', (path, row[0])
    assert row[1] == expected_title.replace('|', '&#124;'), (path, row[1])
    assert row[2] == item['profile'].replace('|', '&#124;'), (path, row[2])
    assert row[3] == item['ownerKey'].replace('|', '&#124;'), (path, row[3])
    assert row[4] in dispositions, (path, row[4])
    assert all(row[index] for index in range(14) if index != 3), (path, row)
    assert all('|' not in cell and '\r' not in cell and '\n' not in cell for cell in row)
    if row[4] == 'delete':
        assert row[5] == 'not applicable - no successor approved', (path, row[5])
own_row = rows[ledger_paths.index(ledger_path)]
assert own_row == [
    f'`{ledger_path}`',
    'Document Migration Evidence Ledger',
    'content/reference',
    '',
    'preserve',
    f'`{ledger_path}`',
    'Spec 030 ADM-002',
    'external-topic: not applicable - repository-specific migration evidence',
    '2026-07-13',
    'repository-specific',
    'retain as durable migration evidence owner',
    'each ADM task',
    'independent reviewer',
    'inventory-reviewed',
]
PY
fi

if [ "$overall_rc" -eq 0 ]; then
  markdown_report='_workspace/document-migration-markdown-compatibility.json'
  markdown_rc=0
  python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
    --format json --include-path "$ledger_path" >"$markdown_report" || markdown_rc=$?
  if [ "$markdown_rc" -ne 0 ]; then
    overall_rc="$markdown_rc"
  else
    python3 - "$markdown_report" "$ledger_path" <<'PY' || overall_rc=$?
import json
import pathlib
import sys

report = json.loads(pathlib.Path(sys.argv[1]).read_text())
ledger_path = sys.argv[2]
assert list(report) == [
    'schemaVersion', 'mode', 'outcome', 'counts', 'diagnostics'
]
assert report['mode'] == 'compatibility'
assert not [item for item in report['diagnostics'] if item['path'] == ledger_path]
PY
  fi
fi

if [ "$overall_rc" -eq 0 ]; then
  compatibility_rc=0
  python3 scripts/validate-links-and-owners.py --root . --mode compatibility \
    --include-path "$ledger_path" || compatibility_rc=$?
  strict_rc=0
  python3 scripts/validate-links-and-owners.py --root . --mode strict \
    --include-path "$ledger_path" || strict_rc=$?
  if [ "$compatibility_rc" -ne 0 ]; then
    overall_rc="$compatibility_rc"
  elif [ "$strict_rc" -ne 0 ]; then
    overall_rc="$strict_rc"
  fi
fi

if [ "$overall_rc" -eq 0 ]; then
  tracked_workspace="$(git ls-files _workspace)" || overall_rc=$?
  if [ "$overall_rc" -eq 0 ] && [ "$tracked_workspace" != '_workspace/README.md' ]; then
    overall_rc=1
  fi
fi
exit "$overall_rc"
```

Expected: final inventory is 469/current and 38/new, the pinned ledger
classification and self-row pass, both modes exit 0, and the ordered ledger
path list equals the exact final `documents[].path` list with no omission,
extra, or duplicate. Tracked `_workspace` output is exactly
`_workspace/README.md`; any earlier nonzero result survives the final check.

- [ ] **Step 5: Commit**

```bash
set -e
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/90.references/research/2026-07-07-wer/README.md \
  tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md
git diff --check
pre-commit run --files \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/90.references/research/2026-07-07-wer/README.md \
  tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/90.references/research/2026-07-07-wer/README.md \
  tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
    'docs/90.references/research/2026-07-07-wer/README.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
    'tests/fixtures/document-contracts/semantic-compatibility-debt.json',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected and len(actual) == 5, (sorted(actual), sorted(expected))
PY
git commit -m "docs(migration): inventory authored document dispositions"
```

Expected: `git diff --check` and focused hooks pass against the tracked ledger
and links, then the same five paths are re-added after any hook rewrite. A
nonzero staging, diff, hook, exact-set, or commit result terminates this block
immediately; no later re-stage or commit may mask an earlier failure. A
fresh reviewer verifies exactly five staged paths and the final
469-path inventory/ledger set equality, pinned self-row, the exact fourteen
columns, semantic debt `items: []`, strict and compatibility results, and the
ignored boundary. Roll back only with
`git revert <ADM-002-commit>` so the ledger and its one represented missing-ledger
item return atomically.

---

### Task 3: Normalize Stage 01–03 Documents

**Files:**

- Modify: non-README Markdown under `docs/01.requirements/`
- Modify: non-README Markdown under `docs/02.architecture/requirements/`
- Modify: non-README Markdown under `docs/02.architecture/decisions/`
- Modify: `spec.md`, `agent-design.md`, `api-spec.md`, `data-model.md`, and `tests.md` under `docs/03.specs/`
- Modify: durable migration ledger
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: final registry, templates, compatibility diagnostics, and ledger rows.
- Produces: debt-free current design documents without altering accepted-decision
  history, with the exact 34 Stage 01–03 shape-debt paths and their aggregate
  caps removed.

- [ ] **Step 1: Capture RED diagnostics for the three directory boundaries**

```bash
report=_workspace/adm-003-markdown-red.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" docs/01.requirements docs/02.architecture docs/03.specs <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
boundaries = sys.argv[2:]
selected = [d for d in data['diagnostics'] if any(
    d['path'] == boundary or d['path'].startswith(boundary + '/')
    for boundary in boundaries
)]
assert selected and all(d['outcome'] == 'DEFER' for d in selected)
PY
```

Expected: valid JSON inventories; every reported item names an exact record in
the finite template compatibility fixture.

Create `_workspace/adm-003-debt-removals.json` from the exact diagnostic tuples
matched by `template-compatibility.json`. Freeze the exact before counts,
removed counts, and arithmetic after counts for paths, per-rule obligations,
occurrences, and union. Independent review must approve this manifest before
Step 2. Its reviewed `documentPaths` must be tracked, non-README paths under
the five exact Files families above and include every debt-tuple path. Freeze
the sorted paths as `_workspace/adm-003-allowed-document-paths.nul`; record and
independently approve its count and SHA-256 in Task evidence before any
mutation. These are compatibility-fixture records, never registry records.
The manifest must contain exactly the 34 ADM-003 paths proven by the
pre-ADM-002 coverage gate.

- [ ] **Step 2: Build exact NUL-delimited family batches**

Generate ignored batch manifests from tracked files, never from a directory
argument passed to a formatter. Each manifest contains at most five exact paths
and is one 2–5 minute edit/validation checkpoint.

```bash
mkdir -p _workspace/adm-003-batches
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
debt = json.loads(pathlib.Path('_workspace/adm-003-debt-removals.json').read_text())
selected = set(debt['documentPaths'])
eligible = set(subprocess.check_output([
    'git', 'ls-files', 'docs/01.requirements',
    'docs/02.architecture/requirements', 'docs/02.architecture/decisions',
    'docs/03.specs',
], text=True).splitlines())
excluded = {p for p in eligible if pathlib.PurePosixPath(p).name == 'README.md'}
assert selected and selected <= eligible and not selected & excluded
assert {item['path'] for item in debt['debtTuples']} <= selected
payload = b''.join(p.encode() + b'\0' for p in sorted(selected))
pathlib.Path('_workspace/adm-003-allowed-document-paths.nul').write_bytes(payload)
print(len(selected), hashlib.sha256(payload).hexdigest())
d = pathlib.Path('_workspace/adm-003-batches')
paths = sorted(selected)
for i in range(0, len(paths), 5):
    (d / f'documents-{i // 5 + 1:02d}.nul').write_bytes(
        b''.join(p.encode() + b'\0' for p in paths[i:i + 5]))
PY
```

Expected: the independently recorded count/SHA matches; every frozen allowed
path occurs in exactly one NUL batch, no README is present, and no unreviewed
eligible path is self-authorized.

After editing one batch, set `ADM_BATCH` to that exact reviewed manifest and
run this full-corpus result filtered to only its NUL path set:

```bash
batch=${ADM_BATCH:?set ADM_BATCH to the exact reviewed ADM-003 batch manifest}
case "$batch" in _workspace/adm-003-batches/documents-*.nul) ;; *) exit 1;; esac
report="${batch%.nul}-green.json"; validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" "$batch" <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
```

- [ ] **Step 3: Transform PRD and ARD batches**

Apply exact key order and family state domain, retain topic-specific requirements,
merge duplicate opening intent, and move all upstream/downstream relationships
to the profile-owned Traceability section. For each `documents-*.nul` manifest
containing PRD/ARD paths,
edit only those at-most-five paths, update their ledger rows, run the
compatibility validator on each exact path, and mark that 2–5 minute checkpoint
complete before opening the next manifest.

- [ ] **Step 4: Transform ADR and Spec batches**

Preserve accepted ADR decisions and consequences. Remove copied form guidance,
merge duplicate sections, correct contradictory current-owner links, and record
every content choice and official source in the ledger. Repeat the same
at-most-five-path checkpoint for each remaining `documents-*.nul` manifest; do not combine
manifests in one edit/review checkpoint.

- [ ] **Step 5: Run GREEN exact-wave validation**

Remove exactly the manifest records from `template-compatibility.json` in the
same edit checkpoint that canonicalizes their paths. Recompute every aggregate
cap downward and refresh the complete fixture semantic digest and all mutation
proofs in `scripts/validate-repo-quality-gates.sh`. Assert the post-fixture
counts equal the manifest's exact arithmetic and that its removal tuple set is
disjoint from remaining records.

```bash
report=_workspace/adm-003-markdown-green.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" _workspace/adm-003-allowed-document-paths.nul <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
```

Expected: the exact reviewed wave selects no diagnostic and no broken/duplicate
owner finding remains.

- [ ] **Step 6: Review and commit**

```bash
git diff --check
git ls-files -z docs/01.requirements docs/02.architecture docs/03.specs \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  | xargs -0 -r -n 5 pre-commit run --files
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md \
  tests/fixtures/document-contracts/template-compatibility.json \
  scripts/validate-repo-quality-gates.sh
xargs -0 git add -- < _workspace/adm-003-allowed-document-paths.nul
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
manifest = pathlib.Path('_workspace/adm-003-allowed-document-paths.nul').read_bytes()
allowed = {p.decode() for p in manifest.split(b'\0') if p}
debt = json.loads(pathlib.Path('_workspace/adm-003-debt-removals.json').read_text())
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
fixed = {'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
         'docs/00.agent-governance/memory/progress.md',
         'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
         'scripts/validate-repo-quality-gates.sh',
         'tests/fixtures/document-contracts/template-compatibility.json'}
assert len(allowed) == debt['allowedDocumentPathCount']
assert hashlib.sha256(manifest).hexdigest() == debt['allowedDocumentPathsSha256']
changed = {p for p in allowed if subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', p]).returncode == 1}
assert not {p for p in allowed if pathlib.PurePosixPath(p).name == 'README.md'}
assert {item['path'] for item in debt['debtTuples']} <= changed
assert actual == changed | fixed and fixed <= actual, (sorted(actual - (changed | fixed)), sorted((changed | fixed) - actual))
print(f'ADM-003 exact staged count: {len(actual)}')
PY
git commit -m "docs(migration): normalize active sdlc design documents"
```

Expected: focused hooks PASS and commit contains only the reviewed exact wave,
ledger/Task evidence, fixture, and digest consumer. A fresh reviewer compares
the debt-removal manifest to document diffs, proves exact before - removed =
after counts and complete digest/mutation refresh, and records the printed
staged count. Roll back with `git revert <ADM-003-commit>` so documents, ledger,
fixture records/caps, digest, and mutation proofs return atomically.

---

### Task 4: Normalize Stage 04–05 Documents

**Files:**

- Modify: non-README Markdown under `docs/04.execution/plans/`
- Modify: non-README Markdown under `docs/04.execution/tasks/`
- Modify: non-README Markdown under `docs/05.operations/guides/`
- Modify: non-README Markdown under `docs/05.operations/policies/`
- Modify: non-README Markdown under `docs/05.operations/runbooks/`
- Modify: canonical real incident/postmortem documents if they exist
- Modify: durable migration ledger
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: Plan/Task/Guide/Policy/Runbook/Incident/Postmortem profiles.
- Produces: preserved execution facts and role-separated operational documents,
  with the exact 120 ADM-004 shape-debt paths and their aggregate caps removed.

- [ ] **Step 1: Capture RED directory-boundary diagnostics**

```bash
report=_workspace/adm-004-markdown-red.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" docs/04.execution docs/05.operations <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
boundaries = sys.argv[2:]
selected = [d for d in data['diagnostics'] if any(
    d['path'] == boundary or d['path'].startswith(boundary + '/')
    for boundary in boundaries
)]
assert selected and all(d['outcome'] == 'DEFER' for d in selected)
PY
```

Expected: valid JSON with only named migration debt.

Create and independently review
`_workspace/adm-004-debt-removals.json` with the exact matched
path/profile/rule/token tuples and exact before/removed/after path,
obligation, occurrence, and union counts. No later step may remove a tuple not
present in this frozen manifest. Its `documentPaths` must be a reviewed subset
of tracked eligible non-README execution/operations paths, include every debt
tuple path, and exclude the same-topic Task because that file is fixed evidence.
Freeze `_workspace/adm-004-allowed-document-paths.nul`, record its count and
SHA-256 in Task evidence, and obtain independent approval before any mutation.
The manifest must contain exactly the 120 ADM-004 paths proven by the
pre-ADM-002 coverage gate.

- [ ] **Step 2: Build exact NUL-delimited execution/operations batches**

```bash
mkdir -p _workspace/adm-004-batches
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
debt = json.loads(pathlib.Path('_workspace/adm-004-debt-removals.json').read_text())
selected = set(debt['documentPaths'])
eligible = set(subprocess.check_output([
    'git', 'ls-files', 'docs/04.execution/plans',
    'docs/04.execution/tasks', 'docs/05.operations',
], text=True).splitlines())
fixed_task = 'docs/04.execution/tasks/2026-07-12-authored-document-migration.md'
excluded = {p for p in eligible if pathlib.PurePosixPath(p).name == 'README.md'} | {fixed_task}
assert selected and selected <= eligible and not selected & excluded
assert {item['path'] for item in debt['debtTuples']} <= selected
payload = b''.join(p.encode() + b'\0' for p in sorted(selected))
pathlib.Path('_workspace/adm-004-allowed-document-paths.nul').write_bytes(payload)
print(len(selected), hashlib.sha256(payload).hexdigest())
d = pathlib.Path('_workspace/adm-004-batches')
paths = sorted(selected)
for i in range(0, len(paths), 5):
    (d / f'documents-{i // 5 + 1:02d}.nul').write_bytes(
        b''.join(p.encode() + b'\0' for p in paths[i:i + 5]))
PY
```

Expected: the independently recorded count/SHA matches; each frozen path occurs
once, every batch has no more than five paths, and README/fixed evidence paths
are absent. After each batch edit, run the same full-corpus validator and filter
to that exact batch only:

```bash
batch=${ADM_BATCH:?set ADM_BATCH to the exact reviewed ADM-004 batch manifest}
case "$batch" in _workspace/adm-004-batches/documents-*.nul) ;; *) exit 1;; esac
report="${batch%.nul}-green.json"; validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" "$batch" <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
```

- [ ] **Step 3: Preserve completed execution evidence batch by batch**

Keep historical commands, results, limitations, and unchecked historical
instructions. Remove copied `Working Rules`, `Suggested Types`, target comments,
and duplicate relationship sections; do not convert historical facts into
current requirements. Complete and validate one `documents-*.nul` manifest at a
time, updating the ledger before continuing.

- [ ] **Step 4: Separate operational roles batch by batch**

Keep Guides explanatory, Policies normative, Runbooks executable, Incidents
factual, and Postmortems causal/learning-oriented. Move duplicate content to one
owner and replace it with a relative link. Complete and validate the remaining
`documents-*.nul` manifests one at a time, updating the ledger before continuing.

- [ ] **Step 5: Run GREEN validation and commit**

Remove every and only manifest tuple from
`template-compatibility.json` in the same commit as its canonical document.
Recompute all caps downward and refresh the quality gate's complete-fixture
semantic digest and affected-path/rule-cap/union-count mutation proofs.

```bash
report=_workspace/adm-004-markdown-green.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" _workspace/adm-004-allowed-document-paths.nul <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git ls-files -z docs/04.execution docs/05.operations \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  | xargs -0 -r -n 5 pre-commit run --files
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md \
  tests/fixtures/document-contracts/template-compatibility.json \
  scripts/validate-repo-quality-gates.sh
xargs -0 git add -- < _workspace/adm-004-allowed-document-paths.nul
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
manifest = pathlib.Path('_workspace/adm-004-allowed-document-paths.nul').read_bytes()
allowed = {p.decode() for p in manifest.split(b'\0') if p}
debt = json.loads(pathlib.Path('_workspace/adm-004-debt-removals.json').read_text())
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
fixed = {'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
         'docs/00.agent-governance/memory/progress.md',
         'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
         'scripts/validate-repo-quality-gates.sh',
         'tests/fixtures/document-contracts/template-compatibility.json'}
assert len(allowed) == debt['allowedDocumentPathCount']
assert hashlib.sha256(manifest).hexdigest() == debt['allowedDocumentPathsSha256']
changed = {p for p in allowed if subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', p]).returncode == 1}
excluded = {p for p in allowed if pathlib.PurePosixPath(p).name == 'README.md'}
assert not excluded and 'docs/04.execution/tasks/2026-07-12-authored-document-migration.md' not in allowed
assert {item['path'] for item in debt['debtTuples']} <= changed
assert actual == changed | fixed and fixed <= actual, (sorted(actual - (changed | fixed)), sorted((changed | fixed) - actual))
print(f'ADM-004 exact staged count: {len(actual)}')
PY
git commit -m "docs(migration): normalize execution and operations documents"
```

Expected: the exact reviewed wave has no debt and commit succeeds. A fresh reviewer
proves document/removal set equality, exact count arithmetic, complete digest
and mutation refresh, and the printed staged count. Roll back with
`git revert <ADM-004-commit>` to restore the whole wave atomically.

---

### Task 5: Normalize Governance, Current References, and Archive Links

**Files:**

- Modify structurally only: every shape-debt non-README Markdown path under `docs/00.agent-governance/`
- Modify structurally only: every remaining shape-debt non-README Markdown path under `docs/90.references/`
- Modify structurally only: every remaining shape-debt non-README Markdown path under `docs/98.archive/`
- Modify structurally only: `docs/99.templates/support/common-documentation-governance.md`
- Modify structurally only: `docs/99.templates/support/documentation-contract.md`
- Modify structurally only: `docs/99.templates/support/frontmatter-schema.md`
- Modify structurally only: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify structurally only: `docs/99.templates/support/sdlc-governance.md`
- Modify structurally only: `docs/99.templates/support/template-routing.md`
- Modify: durable migration ledger
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: governance/reference/archive profiles and historical-path exclusions.
- Produces: one current authority per role while retaining dated and archive
  evidence, with exactly the 73 ADM-005 shape-debt paths canonicalized and
  their records removed. This wave changes only Frontmatter/section shape and
  duplicate template residue in the thirteen Spec 027/031 handoff paths; it
  preserves their facts, provider semantics, route/schema/form behavior, and
  the semantic ownership assigned to Specs 027 and 031.

- [ ] **Step 1: Capture RED diagnostics for remaining owned boundaries**

```bash
report=_workspace/adm-005-markdown-red.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" docs/00.agent-governance docs/90.references docs/98.archive docs/99.templates/support <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
boundaries = sys.argv[2:]
selected = [d for d in data['diagnostics'] if any(
    d['path'] == boundary or d['path'].startswith(boundary + '/')
    for boundary in boundaries
)]
assert selected and all(d['outcome'] == 'DEFER' for d in selected)
assert len({d['path'] for d in selected}) == 73
PY
```

Expected: valid JSON across exactly four RED boundaries, exactly 73 distinct
paths, and no unregistered debt.

Create and independently review
`_workspace/adm-005-debt-removals.json` from exact matched tuples in the finite
template compatibility fixture. Freeze exact before/removed/after counts for
paths, each rule, obligations, occurrences, and union. An unregistered
diagnostic fails; it is never converted into a registry record or new debt.
Its reviewed `documentPaths` must be a subset of the exact tracked Files
families, include every debt-tuple path, and exclude README, the progress
ledger, and durable migration ledger. It must contain all remaining broad
`docs/00.agent-governance`, `docs/90.references`, and `docs/98.archive` debt
plus the exact six support paths named in Files, for exactly 73 paths. Freeze
`_workspace/adm-005-allowed-document-paths.nul`; record and independently
approve its count and SHA-256 before mutation.

- [ ] **Step 2: Build exact NUL-delimited governance/reference batches**

Generate ignored manifests of at most five tracked paths for the structurally
owned Stage 00, Stage 90, Stage 98, and exact Stage 99 support sets. README,
progress, and durable-ledger paths remain excluded. The former seven handoff
exclusions are now included under the narrow structural-only exception in Spec
030; semantic, behavior, route, schema, form, and provider changes remain
forbidden. Treat each manifest as one 2–5 minute edit, ledger, and
compatibility-validation checkpoint.

```bash
mkdir -p _workspace/adm-005-batches
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
debt = json.loads(pathlib.Path('_workspace/adm-005-debt-removals.json').read_text())
selected = set(debt['documentPaths'])
eligible = set(subprocess.check_output([
    'git', 'ls-files', 'docs/00.agent-governance',
    'docs/90.references', 'docs/98.archive', 'docs/99.templates/support',
], text=True).splitlines())
excluded = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
} | {p for p in eligible if pathlib.PurePosixPath(p).name == 'README.md'}
assert selected and selected <= eligible and not selected & excluded
assert len(selected) == 73
assert {item['path'] for item in debt['debtTuples']} <= selected
payload = b''.join(p.encode() + b'\0' for p in sorted(selected))
pathlib.Path('_workspace/adm-005-allowed-document-paths.nul').write_bytes(payload)
print(len(selected), hashlib.sha256(payload).hexdigest())
d = pathlib.Path('_workspace/adm-005-batches')
paths = sorted(selected)
for i in range(0, len(paths), 5):
    (d / f'documents-{i // 5 + 1:02d}.nul').write_bytes(
        b''.join(p.encode() + b'\0' for p in paths[i:i + 5]))
PY
```

Expected: the recorded count/SHA matches 73; all README and fixed evidence
paths are absent; the thirteen narrowly authorized handoff paths are present;
and every frozen path occurs once in a batch of at most five paths. After each
batch edit, run the full-corpus validator and filter to that exact batch only:

```bash
batch=${ADM_BATCH:?set ADM_BATCH to the exact reviewed ADM-005 batch manifest}
case "$batch" in _workspace/adm-005-batches/documents-*.nul) ;; *) exit 1;; esac
report="${batch%.nul}-green.json"; validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" "$batch" <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
```

- [ ] **Step 3: Transform current governance and reference owners in batches**

Normalize sections and authority links in owned files. Preserve earlier dated
packs and record their snapshot boundary in the ledger without rewriting bodies.
For completed history and the thirteen handoff paths, restrict changes to
canonical Frontmatter order/values, canonical section naming/order, duplicate
template-residue removal, and link repair. Do not change historical facts or
Spec 027/031-owned route, schema, form, provider, or agent behavior.
Do not open a later manifest until all exact paths in the current manifest and
their ledger rows pass compatibility validation.

- [ ] **Step 4: Verify Tombstone preservation**

Ensure each Tombstone remains metadata-only, uses `status: archived`, links the
archive index, and does not regain the retired body.

- [ ] **Step 5: Run GREEN validation and commit**

Remove exactly the frozen manifest tuples from
`template-compatibility.json` as their paths become canonical, recompute every
cap downward, and refresh the complete-fixture semantic digest and all mutation
proofs in `scripts/validate-repo-quality-gates.sh` in this commit.

```bash
report=_workspace/adm-005-markdown-green.json
validator_rc=0
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility \
  --format json >"$report" || validator_rc=$?
if [ "$validator_rc" -ne 0 ]; then exit "$validator_rc"; fi
python3 - "$report" _workspace/adm-005-allowed-document-paths.nul <<'PY'
import json, pathlib, sys
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
paths = {p.decode() for p in pathlib.Path(sys.argv[2]).read_bytes().split(b'\0') if p}
assert paths
assert not [d for d in data['diagnostics'] if d['path'] in paths]
PY
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git add docs/00.agent-governance/memory/progress.md \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  tests/fixtures/document-contracts/template-compatibility.json \
  scripts/validate-repo-quality-gates.sh
xargs -0 git add -- < _workspace/adm-005-allowed-document-paths.nul
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
manifest = pathlib.Path('_workspace/adm-005-allowed-document-paths.nul').read_bytes()
allowed = {p.decode() for p in manifest.split(b'\0') if p}
debt = json.loads(pathlib.Path('_workspace/adm-005-debt-removals.json').read_text())
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
fixed = {'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
         'docs/00.agent-governance/memory/progress.md',
         'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
         'scripts/validate-repo-quality-gates.sh',
         'tests/fixtures/document-contracts/template-compatibility.json'}
assert len(allowed) == debt['allowedDocumentPathCount']
assert hashlib.sha256(manifest).hexdigest() == debt['allowedDocumentPathsSha256']
changed = {p for p in allowed if subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', p]).returncode == 1}
excluded = {p for p in allowed if pathlib.PurePosixPath(p).name == 'README.md'}
assert not excluded and {item['path'] for item in debt['debtTuples']} <= changed
assert actual == changed | fixed and fixed <= actual, (sorted(actual - (changed | fixed)), sorted((changed | fixed) - actual))
print(f'ADM-005 exact staged count: {len(actual)}')
PY
git commit -m "docs(migration): normalize governance references and archive links"
```

Expected: the exact reviewed wave passes and historical bodies remain preserved. A
fresh reviewer proves preserve-boundary compliance, document/removal set
equality, exact count arithmetic, complete digest/mutation refresh, and the
printed staged count. Roll back with `git revert <ADM-005-commit>` so content,
ledger, debt fixture, and digest consumer return together.

---

### Task 6: Consolidate AWS and Azure Documentation

**Files:**

- Create: `docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md`
- Create: `docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/README.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/aws/README.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/azure/README.md`
- Modify link/index rows only: `examples/README.md`
- Modify link/index rows only: `examples/aws/README.md`
- Modify link/index rows only: `examples/azure/README.md`
- Delete: `examples/aws/docs/**`
- Delete: `examples/azure/docs/**`
- Modify: durable migration ledger
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: Spec 028 README forms and the exact fifty-nine-file cloud source set.
- Produces: two dated provider snapshots, executable entrypoints, zero
  example-local SDLC Markdown, and no compatibility records for removed or
  canonicalized cloud documentation. Its frozen debt manifest contains exactly
  the 39 ADM-006 shape-debt paths proven by the pre-ADM-002 coverage gate; all
  59 source paths still receive `merge` dispositions and deletion review.

- [ ] **Step 1: Record RED source count and inbound links**

```bash
git ls-files -z examples/aws/docs examples/azure/docs > _workspace/cloud-doc-source-paths.nul
python3 - <<'PY'
import hashlib, pathlib
source = pathlib.Path('_workspace/cloud-doc-source-paths.nul').read_bytes()
paths = {p.decode() for p in source.split(b'\0') if p}
assert len(paths) == 59
exact_additions = {
    'docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md',
    'docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md',
    'docs/90.references/cloud-examples/README.md',
    'docs/90.references/cloud-examples/aws/README.md',
    'docs/90.references/cloud-examples/azure/README.md',
    'examples/README.md', 'examples/aws/README.md', 'examples/azure/README.md',
}
allowed = paths | exact_additions
payload = b''.join(p.encode() + b'\0' for p in sorted(allowed))
pathlib.Path('_workspace/adm-006-allowed-document-paths.nul').write_bytes(payload)
print(len(paths), hashlib.sha256(source).hexdigest())
print(len(allowed), hashlib.sha256(payload).hexdigest())
PY
rg -n 'examples/(aws|azure)/docs' README.md docs examples scripts tests > _workspace/cloud-doc-inbound-links.txt
```

Expected: source count `59`; the NUL file is the deletion review source of truth,
and the inbound-link file records every active relocation consumer.

Also create and independently review
`_workspace/adm-006-debt-removals.json` containing every exact finite-debt
tuple whose path is in the 59-file source set or another cloud path made
canonical by this wave. Record exact before/removed/after path, rule,
obligation, occurrence, and union counts. The NUL source set, durable ledger,
and debt-removal manifest must agree before deletion. Record and independently
approve both frozen manifest counts and SHA-256 values in Task evidence before
the first snapshot, README, or deletion mutation. The 59-path source manifest
is the immutable deletion set; the allowed manifest is exactly those deletions
plus the two snapshots and six explicitly named README paths.

- [ ] **Step 2: Build provider snapshots before deletion**

For each provider, record source files, retained unique knowledge, executable
asset mapping, official source URLs, observed date/version, applicable and
rejected guidance, refresh trigger, and authority boundary. Independent review
must confirm all 59 exact source paths have ledger rows and every `merge` or
`delete` row has a destination. Prove coverage before deletion:

```bash
python3 -c 'import pathlib,sys; paths=[x.decode() for x in pathlib.Path("_workspace/cloud-doc-source-paths.nul").read_bytes().split(b"\0") if x]; ledger=pathlib.Path("docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md").read_text(); missing=[p for p in paths if f"| `{p}` |" not in ledger]; print("\n".join(missing)); raise SystemExit(bool(missing) or len(paths) != 59)'
```

Expected: exit 0 with no missing path output.

- [ ] **Step 3: Update entrypoint and snapshot index rows**

Use the existing Spec 028 README profile sections. Change only inventory,
source-of-truth, and related-document links required by relocation.

- [ ] **Step 4: Delete the reviewed duplicate trees**

```bash
git rm --pathspec-from-file=_workspace/cloud-doc-source-paths.nul --pathspec-file-nul
```

Expected: the cached deletion set equals the reviewed 59-path manifest exactly;
executable assets remain.

- [ ] **Step 5: Run GREEN cloud assertions**

Remove every and only tuple in the approved ADM-006 debt manifest from
`template-compatibility.json`, recompute all aggregate caps downward, and
refresh the quality gate's complete-fixture digest plus affected-path,
rule-cap, and union-count mutation proofs in this same commit.

```bash
test -z "$(git ls-files examples/aws/docs examples/azure/docs)"
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

Expected: no tracked cloud-doc path, no broken links, and compatibility PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md \
  docs/00.agent-governance/memory/progress.md \
  tests/fixtures/document-contracts/template-compatibility.json \
  scripts/validate-repo-quality-gates.sh
xargs -0 git add -A -- < _workspace/adm-006-allowed-document-paths.nul
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
manifest = pathlib.Path('_workspace/adm-006-allowed-document-paths.nul').read_bytes()
allowed = {p.decode() for p in manifest.split(b'\0') if p}
deletions_raw = pathlib.Path('_workspace/cloud-doc-source-paths.nul').read_bytes()
deletions = {p.decode() for p in deletions_raw.split(b'\0') if p}
debt = json.loads(pathlib.Path('_workspace/adm-006-debt-removals.json').read_text())
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
fixed = {'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
         'docs/00.agent-governance/memory/progress.md',
         'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
         'scripts/validate-repo-quality-gates.sh',
         'tests/fixtures/document-contracts/template-compatibility.json'}
assert len(deletions) == debt['deletionPathCount'] == 59 and deletions <= allowed
assert len(allowed) == debt['allowedDocumentPathCount']
assert hashlib.sha256(manifest).hexdigest() == debt['allowedDocumentPathsSha256']
assert hashlib.sha256(deletions_raw).hexdigest() == debt['deletionPathsSha256']
changed = {p for p in allowed if subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', p]).returncode == 1}
assert changed == allowed and {item['path'] for item in debt['debtTuples']} <= changed
assert actual == changed | fixed and fixed <= actual, (sorted(actual - (changed | fixed)), sorted((changed | fixed) - actual))
print(f'ADM-006 exact staged count: {len(actual)}')
PY
git commit -m "docs(migration): consolidate cloud example documentation"
```

Expected: the staged set is exactly the printed reviewed set, including all 59
deletions, two snapshots, relocation-only README link rows, ledger/Task
evidence, fixture, and digest consumer. A fresh reviewer proves 59-source
coverage, unique-content preservation, tuple set equality, exact count
arithmetic, and complete digest/mutation refresh. Roll back with
`git revert <ADM-006-commit>` so deletions and every supporting record return
atomically.

---

### Task 7: Enable Strict Validation and Close Spec 030

**Files:**

- Modify: `tests/fixtures/document-contracts/template-compatibility.json` to remove the final empty debt definitions and refresh its complete digest contract
- Delete: `tests/fixtures/document-contracts/semantic-compatibility-debt.json` after proving `items` is empty
- Modify: `scripts/validate-markdown-profiles.py`
- Modify: `scripts/validate-links-and-owners.py`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: durable migration ledger
- Modify: Spec 030, this Plan, same-topic Task, their indexes, and `memory/progress.md`

**Interfaces:**

- Consumes: zero-debt migrated corpus, two empty finite debt consumers, and strict Spec 029 validators.
- Produces: strict repository quality gate and completed migration evidence.

- [ ] **Step 1: Run RED strict bundle before debt removal**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
```

Expected: the corpus passes strict before cleanup, both debt consumers contain
zero path/item records, and compatibility has no `DEFER` or `DEBT-UNUSED`.
Any remaining failure identifies an exact path and rule; do not remove an
underlying record before its owning ADM wave passes.

- [ ] **Step 2: Remove empty debt containers and switch the wrapper to strict**

Remove the now-empty `compatibilityDebt`, rule-cap, and union-count debt
definitions from `template-compatibility.json`, then recompute and pin its
complete semantic digest and refresh the mutation proof for the resulting
debt-free schema. Delete the empty
`semantic-compatibility-debt.json`. Change the semantic validator invocations
in `scripts/validate-repo-quality-gates.sh` from `compatibility` to `strict`.
Update both production semantic validators and their self-tests atomically:
strict mode treats the retired semantic debt file and absent template
`compatibilityDebt` container as the canonical zero-debt state; it does not
silently recreate either source. Compatibility mode after retirement fails
closed as configuration exit 2 with stable `DEBT-SOURCE-MISSING`, so the
quality wrapper must switch every production invocation to strict in this same
commit. Self-tests prove both absent-source strict PASS and compatibility
exit 2 for each validator.
Do not alter profile routes, registry data, or registry semantics. In
particular, `docs/99.templates/support/document-profiles.json` is neither a
debt owner nor an ADM-007 file.

- [ ] **Step 3: Run GREEN strict and residue checks**

```bash
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
set +e
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility
markdown_compat_rc=$?
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
links_compat_rc=$?
set -e
test "$markdown_compat_rc" -eq 2
test "$links_compat_rc" -eq 2
rg -n 'harness-task-contract|SNIPPET LIBRARY|Suggested Types' docs examples .agents .claude .codex scripts
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

Expected: validators and required hooks PASS; residue search has no active-authority finding; optional skips are labeled.

- [ ] **Step 4: Close evidence and lifecycle**

Set Spec, Plan, and Task to `done`, update index rows, finish every ledger result
and reviewer field, record destructive rollback commits and review decisions,
and append the strict-cutover handoff to `memory/progress.md`.

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/document-contracts/template-compatibility.json \
  tests/fixtures/document-contracts/semantic-compatibility-debt.json \
  scripts/validate-markdown-profiles.py \
  scripts/validate-links-and-owners.py \
  scripts/validate-repo-quality-gates.sh \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
python3 - <<'PY'
import subprocess
expected = {
    'docs/00.agent-governance/memory/progress.md',
    'docs/03.specs/030-authored-document-migration/spec.md',
    'docs/03.specs/README.md',
    'docs/04.execution/plans/2026-07-12-authored-document-migration.md',
    'docs/04.execution/plans/README.md',
    'docs/04.execution/tasks/2026-07-12-authored-document-migration.md',
    'docs/04.execution/tasks/README.md',
    'docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md',
    'scripts/validate-repo-quality-gates.sh',
    'scripts/validate-markdown-profiles.py',
    'scripts/validate-links-and-owners.py',
    'tests/fixtures/document-contracts/semantic-compatibility-debt.json',
    'tests/fixtures/document-contracts/template-compatibility.json',
}
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert actual == expected and len(actual) == 13, (sorted(actual), sorted(expected))
assert 'docs/99.templates/support/document-profiles.json' not in actual
PY
git commit -m "chore(docs): cut over document profiles to strict validation"
```

Expected: exactly thirteen staged paths, including both validator producers and
the deleted empty semantic
fixture, and no registry file. A fresh reviewer proves both fixtures were empty
before cleanup, both self-tests prove retired-source behavior, strict results
before and after are identical and clean, compatibility fails closed with exit
2 only after retirement, the quality wrapper switches atomically, the
complete template fixture digest/mutations are current, lifecycle evidence is
closed, and the exact staged set holds. Roll back with
`git revert <ADM-007-commit>` to restore compatibility mode and both empty debt
containers together with both validator behaviors, without restoring any
removed migration debt.

## Completion Criteria

- [ ] Every approved and program-created target has one profile or native exception.
- [ ] Every migrated current authored document has one complete durable research row.
- [ ] Duplicate current owners, template residue, unsupported sections, and broken links are zero.
- [ ] AWS/Azure example-local SDLC Markdown is zero and executable entrypoints resolve.
- [ ] Strict mode and the full repository QA bundle pass.

## Related Documents

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Authored Migration Spec](../../03.specs/030-authored-document-migration/spec.md)
- [Authored Migration Task](../tasks/2026-07-12-authored-document-migration.md)
- [Semantic Validation Plan](./2026-07-12-semantic-document-validation.md)
- [Affected Surface Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
