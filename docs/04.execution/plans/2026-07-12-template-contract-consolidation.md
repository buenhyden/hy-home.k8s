---
title: 'Template Contract Consolidation Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-12
---

# Template Contract Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate Stage 99 support and non-README template forms around the
Spec 026 registry, remove the legacy harness Task form, and preserve a measured
compatibility window for the not-yet-migrated authored corpus.

**Architecture:** A durable type-to-source ledger records the evidence used to
change each form. Stage 99 support owns rationale, the registry owns exact
machine facts, each document type has one canonical structural form, and a
temporary explicit compatibility fixture keeps the current authored population
valid until Specs 029–030 replace legacy heading enforcement.

**Tech Stack:** Markdown, HTML comments, JSON registry/fixtures, Python 3,
Bash, Git, `rg`, `pre-commit`, and repository quality gates.

## Global Constraints

- Spec 026 registry/schema/classifier must be complete and green before this Plan starts.
- Change only Stage 99 support, non-README template forms, direct Stage 00 mirrors, compatibility fixtures/gates, and execution evidence.
- In `docs/99.templates/README.md` and `docs/99.templates/templates/README.md`, change inventory and target-link rows only; Spec 028 owns every other README layout/body change.
- Keep authored non-README document bodies structurally unchanged; Spec 030 owns
  their migration. Bounded dead-link/current-claim cleanup and retirement
  annotations required by duplicate-form removal were allowed and performed.
- Do not otherwise rewrite completed Plans/Tasks, audits, research snapshots,
  ADR history, or Archive Tombstones.
- Keep OpenAPI, GraphQL, and protobuf forms native and frontmatter-free.
- Every form change requires a reviewed row in `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` first.
- Label ISO/NIST sources as standards and Diátaxis, Spec Kit, Nygard ADR, Kubernetes style, GitHub README guidance, and Google SRE as practices/guidance.
- Do not quote paid standards; record adopted concepts and local decisions.
- Merge unique protected-surface and approval content into the standard Task
  form before retiring the duplicate harness Task starter.
- Authoring instructions belong in support prose or HTML comments, never authored H2 sections.
- Compatibility debt must be explicit, counted, owned by Spec 030, and forbidden from growing.
- Use `apply_patch` for content changes; do not read secrets, mutate live systems, push, or publish.

---

## Overview

This plan implements Spec 027 as six testable tasks: execution lineage,
research ledger, support ownership, canonical forms, compatibility and legacy
cleanup, and closure.

## Context

The current support layer repeats full route and lifecycle tables, the Task
template exposes authoring-only sections, several forms repeat intent or
traceability, and a duplicate harness Task starter creates a second form for
the same `sdlc/task` role. Removing those forms without a compatibility
window would make the current authored population fail before Spec 030 can
migrate it.

## Goals & In-Scope

- Establish a type-to-source decision ledger for every template family.
- Replace duplicated support facts with registry ownership links.
- Give every routed non-README document type one canonical form.
- Merge repeated intent, guidance, and traceability sections.
- Delete the legacy harness Task form and every active reference to it.
- Keep registry validation and the legacy repository quality gate green while
  recording finite compatibility debt.

## Non-Goals & Out-of-Scope

- README profile/template/body redesign.
- Authored document body migration.
- Production CommonMark parsing or strict semantic enforcement.
- Cloud document relocation and protected-surface runtime hardening.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Research decision ledger | `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md` | Record authority, observation/version, adoption, rejection, local extension, and refresh trigger before form edits. |
| Support ownership | Six non-README files in `docs/99.templates/support/` | Explain responsibilities and link exact facts to registry. |
| Canonical forms | `docs/99.templates/templates/{common,sdlc}/**` except README forms | Own minimal sections and conditional author comments. `governance/reference` and `governance/template-support` each use a dedicated common form; neither reuses the content Reference form. |
| Legacy deletion | Retired duplicate harness Task starter and bounded active/history references | Merge unique Task safety concepts, then remove the duplicate role and dead links. |
| Compatibility contract | `tests/fixtures/document-contracts/template-compatibility.json`, `scripts/validate-repo-quality-gates.sh`, registry headings | Freeze old authored heading aliases without making them canonical. |
| Direct Stage 00 mirrors | `documentation-protocol.md`, `document-stage-routing.md`, `stage-authoring-matrix.md` | Route agents to registry/support and remove copied full tables. |
| Inventory-only handoff | `docs/99.templates/README.md`, `docs/99.templates/templates/README.md` | Add/remove form path rows only; preserve current README profile/body. |
| Execution evidence | Spec 027, this Plan, same-topic Task, Stage 03/04 indexes | Maintain reciprocal lineage and validation evidence. |

### Canonical non-README heading contract

The registry `headings.required` and each form must agree on these exact H2
sequences; headings in parentheses are conditional comments, not required
literal headings:

| Profile | Required H2 sequence |
| --- | --- |
| `sdlc/prd` | `Overview`, `Vision`, `Problem Statement`, `Personas`, `Key Use Cases`, `Functional Requirements`, `Success / Acceptance Criteria`, `Scope and Non-goals`, `Risks, Dependencies, and Assumptions`, `Traceability` |
| `sdlc/ard` | `Overview`, `Boundaries & Non-goals`, `Quality Attributes`, `System Overview & Context`, `Data Architecture`, `Infrastructure & Deployment`, `Traceability` |
| `sdlc/adr` | `Overview`, `Context`, `Decision`, `Explicit Non-goals`, `Consequences`, `Alternatives`, `Traceability` |
| `sdlc/spec` | `Overview`, `Strategic Boundaries & Non-goals`, `Contracts`, `Core Design`, `Data Modeling & Storage Strategy`, `Interfaces & Data Structures`, `Edge Cases & Error Handling`, `Failure Modes & Fallback / Human Escalation`, `Verification Commands`, `Success Criteria & Verification Plan`, `Traceability` |
| `sdlc/api-spec` | `Overview`, `Scope & Non-goals`, `API Style`, `Authentication & Authorization`, `Endpoint / Operation Catalog`, `Request / Response Schemas`, `Error Model`, `Data Contract Compatibility`, `Non-Functional Requirements`, `Machine-readable Contract Files`, `Verification`, `Traceability` |
| `sdlc/agent-design` | `Overview`, `Scope & Non-goals`, `Agent Role`, `Inputs / Outputs`, `Orchestration Model`, `Tools & Permissions`, `Prompt / Policy Contract`, `Context & Memory Strategy`, `Guardrails`, `Failure Modes & Fallback`, `Evaluation Plan`, `Observability`, `Traceability` |
| `sdlc/data-model` | `Overview`, `Scope & Non-goals`, `Entities / Aggregates`, `Relationships`, `Schema / Structures`, `Validation & Integrity Rules`, `Storage Strategy`, `Privacy / Security`, `Migration & Compatibility`, `Traceability` |
| `sdlc/tests` | `Overview`, `Verification Goals`, `TDD Scope`, `Test Matrix`, `Contract & Integration Tests`, `Non-Functional Tests`, `Fixtures / Datasets`, `How to Run`, `Evidence & Reporting`, `Traceability` |
| `sdlc/plan` | `Overview`, `Context`, `Goals & In-Scope`, `Non-Goals & Out-of-Scope`, `Work Breakdown`, `Verification Plan`, `Risks & Mitigations`, `Completion Criteria`, `Traceability` |
| `sdlc/task` | `Overview`, `Inputs`, `Task Table`, `Approval and Safety Boundaries`, `Verification Summary`, `Traceability` |
| `sdlc/guide` | `Overview`, `Guide Type`, `Target Audience`, `Prerequisites`, `Step-by-step Instructions`, `Common Pitfalls`, `Traceability` |
| `sdlc/policy` | `Overview`, `Policy Scope`, `Applies To`, `Controls`, `Exceptions`, `Verification`, `Review Cadence`, `Traceability` |
| `sdlc/runbook` | `Overview`, `Runbook Type`, `When to Use`, `Procedure or Checklist`, `Verification Steps`, `Observability and Evidence Sources`, `Safe Rollback or Recovery Procedure`, `Traceability` |
| `sdlc/incident` | `Overview`, `Incident Metadata`, `Impact`, `Timeline`, `Response State`, `Evidence`, `Follow-up Actions`, `Traceability` |
| `sdlc/postmortem` | `Overview`, `Incident Link and Impact Summary`, `Root Cause Analysis`, `Contributing Factors`, `What Went Well`, `What Went Wrong`, `Action Items`, `Prevention and Verification`, `Documentation Feedback Loop`, `Traceability` |
| `content/reference` | `Overview`, `Reference Type`, `Authority Boundary`, `Scope`, `Definitions / Facts`, `Sources`, `Review and Freshness`, `Related Documents` |
| `content/archive-tombstone` | `Overview`, `Original Document`, `Archive Decision`, `Current Replacement`, `Current Implementation Evidence`, `Archive Index`, `Related Documents` |
| `governance/reference` | `Overview`, `Authority Boundary`, `Governance Context`, `Current Contract`, `Validation and Refresh`, `Related Documents` |
| `governance/memory` | `Problem`, `Context`, `Resolution`, `Prevention`, `Related Progress` |
| `governance/template-support` | `Overview`, `Purpose`, `Owned Contract`, `Authoring Rules`, `Validation Contract`, `Related Documents` |
| `governance/progress-ledger` | `Work Entries` |

Conditional AI-agent content remains an HTML comment within the owning section,
not an extra required H2.

`governance/reference` has the same five frontmatter keys as
`content/reference` but a different literal `type`, authority boundary, and
heading contract, so it uses
`docs/99.templates/templates/common/governance-reference.template.md`.
`governance/template-support` uses
`docs/99.templates/templates/common/template-support.template.md`; its
topic-specific details belong inside `Owned Contract` and `Authoring Rules`,
not as copied route/profile tables or arbitrary extra H2s. These decisions make
the two routed governance types independently testable while preserving exactly
one form per routed type.

The progress ledger is not generated from a whole-document form. It remains a
frontmatter-free document with H2 `Work Entries`. The canonical
`progress.template.md` is instead the `governance/progress-entry` append
fragment and contains no H1, H2, or frontmatter: each entry starts with H3
`YYYY-MM-DD - <workstream-title>` and contains exact H4 sections `Metadata`,
`Progress`, `Memory`, `Evidence`, and `Handoff`. Its metadata bullets stay
inside `Metadata`. Appending a fragment under `Work Entries` must not replace
the ledger title or existing entries.

## Work Breakdown

| Task | Description | Primary validation | Commit |
| --- | --- | --- | --- |
| TCC-001 | Start reciprocal execution lineage | Spec/Plan/Task/index link assertion | `docs(execution): start template consolidation tranche` |
| TCC-002 | Publish the type-to-source decision ledger | Ten family rows with all required evidence fields | `docs(research): record template format evidence` |
| TCC-003 | Consolidate support ownership | No copied complete registry tables | `docs(governance): consolidate template support ownership` |
| TCC-004 | Normalize canonical non-README forms | Heading matrix and native-format checks | `refactor(templates): normalize document forms` |
| TCC-005 | Delete legacy Task form and establish compatibility | Zero active legacy refs; old/new gates green | `refactor(templates): remove legacy harness task form` |
| TCC-006 | Close evidence and hand off Stage 99 README bodies | Full QA and explicit Spec 028 handoff | `docs(templates): close consolidation evidence` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Research | Focused ledger assertion in Task 2 | Every family has source/date/version/adopt/reject/extension/refresh. |
| VAL-PLN-002 | Structure | Registry compatibility validation | Canonical headings/forms match; debt count does not grow. |
| VAL-PLN-003 | Legacy | `rg -n -e 'task-legacy-har[n]ess' -e 'Suggested Types' -e 'Working Rules' docs/99.templates docs/00.agent-governance scripts tests` | The retired duplicate marker has zero matches. Remaining authored-heading terms are inventoried as finite Spec 030 fixture/gate debt, completed historical evidence, or Stage 99 README/body debt owned by Specs 028/030; no new occurrence is allowed. |
| VAL-PLN-004 | Repository | Quality gate and all-files pre-commit | Existing corpus and new contracts pass together. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Unique safety behavior is deleted with the legacy form | High | Move exact approval, static/live, secret, rollback, and evidence fields into Task before deletion. |
| Canonical headings immediately break authored documents | High | Freeze finite legacy aliases in a compatibility fixture consumed only until Spec 030. |
| Support Markdown becomes a second registry | High | Remove complete machine tables and link exact values to JSON. |
| External guidance is misrepresented as a standard | Medium | Record source kind and rejected guidance in every ledger row. |
| README scope leaks into this tranche | High | Restrict both Stage 99 README edits to inventory and target-link rows and review the diff. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate:** Each template family passes exact heading/frontmatter/native-format assertions.
- **Sandbox / Canary Rollout:** Current gate and new registry run together in compatibility mode.
- **Human Approval Gate:** Required for a new document role, metadata key, template route, remote publication, or live mutation.
- **Rollback Trigger:** Authored corpus becomes unclassifiable, compatibility debt grows, unique legacy content is lost, or README body scope expands.
- **Prompt / Model Promotion Criteria:** Not applicable.

---

### Task 1: Start the Canonical Execution Chain

**Files:**

- Modify: `docs/03.specs/027-template-contract-consolidation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: done Spec 026 evidence and active Spec 027.
- Produces: active `TCC-001` through `TCC-006` execution lineage.

- [x] **Step 1: Run the failing lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
spec = Path('docs/03.specs/027-template-contract-consolidation/spec.md')
plan = Path('docs/04.execution/plans/2026-07-12-template-contract-consolidation.md')
task = Path('docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md')
assert task.exists()
links = [(spec, '../../04.execution/plans/2026-07-12-template-contract-consolidation.md'),
         (spec, '../../04.execution/tasks/2026-07-12-template-contract-consolidation.md'),
         (plan, '../../03.specs/027-template-contract-consolidation/spec.md'),
         (plan, '../tasks/2026-07-12-template-contract-consolidation.md'),
         (task, '../../03.specs/027-template-contract-consolidation/spec.md'),
         (task, '../plans/2026-07-12-template-contract-consolidation.md')]
for source, target in links:
    assert target in source.read_text(), (source, target)
PY
```

Expected: FAIL because the Task does not exist.

- [x] **Step 2: Create Task and reciprocal links**

Create an active Task containing exact rows `TCC-001` through `TCC-006`, with
the descriptions and validation columns from Work Breakdown, `platform` owner,
the first row `Done`, and remaining rows `Queued`. Set this Plan active and add
reciprocal links/index rows dated `2026-07-12`.

- [x] **Step 3: Re-run lineage and commit**

```bash
python3 - <<'PY'
from pathlib import Path
for path in ('docs/03.specs/027-template-contract-consolidation/spec.md','docs/04.execution/plans/2026-07-12-template-contract-consolidation.md','docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md'):
    assert Path(path).exists()
PY
git diff --check
git add docs/03.specs/027-template-contract-consolidation/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-template-contract-consolidation.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): start template consolidation tranche"
```

Expected: PASS and one commit.

---

### Task 2: Publish the Type-to-Source Decision Ledger

**Files:**

- Create: `docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`

**Interfaces:**

- Consumes: the ten source-family rows in Spec 027.
- Produces: columns `Family`, `Source kind`, `Authority and link`, `Observed`, `Version/revision`, `Adopted guidance`, `Rejected guidance and reason`, `Local extension`, `Refresh trigger`, `Affected forms`.

- [x] **Step 1: Run the missing-ledger RED assertion**

```bash
test -f docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md
```

Expected: exit 1 because the file does not exist.

- [x] **Step 2: Create the ten complete family rows**

Use the families and primary sources exactly named in Spec 027: PRD; ARD; ADR;
Spec/Plan/Task/tests; native API contracts; agent design; Guide/Reference/README;
Policy/Runbook; Incident/Postmortem; Archive/memory/progress. Set observed date
`2026-07-12`; include source revision/year or `living guidance observed
2026-07-12`; distinguish adopted concepts from repository-specific fields;
record at least one rejected item and one refresh trigger per row.

- [x] **Step 3: Add authority and non-copying boundaries**

State that the ledger is evidence, not the route/schema owner; paid standard
text is not reproduced; provider facts need refresh on official model/tool
contract change; and local Frontmatter fields are repository extensions.

- [x] **Step 4: Assert complete rows**

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md').read_text()
for column in ('Source kind','Observed','Version/revision','Adopted guidance','Rejected guidance and reason','Local extension','Refresh trigger','Affected forms'):
    assert column in text, column
for family in ('PRD','ARD','ADR','Spec, Plan, Task, tests','API and native contracts','Agent design','Guide, Reference, README','Policy and Runbook','Incident and Postmortem','Archive, memory, progress'):
    assert family in text, family
PY
```

Expected: PASS.

- [x] **Step 5: Index and commit**

```bash
git diff --check
git add docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md docs/90.references/research/2026-07-07-wer/README.md
git commit -m "docs(research): record template format evidence"
```

Expected: commit succeeds.

---

### Task 3: Consolidate Stage 99 Support Ownership

**Files:**

- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/99.templates/support/README.md`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `docs/04.execution/plans/2026-07-12-template-contract-consolidation.md`

**Interfaces:**

- Consumes: `document-profiles.json`, the research ledger, and the legacy gate's
  exact Stage 99 support-status consumer.
- Produces: one responsibility owner per rule, links instead of complete copied
  route/state/profile tables, and `active` enforcement for exactly the six
  canonical non-README support documents.

- [x] **Step 1: Capture duplicated machine tables as RED evidence**

```bash
rg -n '^## (Current Route Map|Lifecycle State Contract|Profile Families)|^\| (Product requirement|PRD|`sdlc/)' docs/99.templates/support
```

Expected: matches in routing, governance, and frontmatter support documents.

- [x] **Step 2: Rewrite support responsibilities**

Keep `documentation-contract.md` for surface ownership, `sdlc-governance.md`
for lifecycle rationale and handoff semantics, `common-documentation-governance.md`
for common-role rationale, `frontmatter-schema.md` for metadata rationale,
`template-routing.md` for route-selection procedure, and
`legacy-cleanup-rules.md` for migration/removal policy. Replace exact complete
tables with links to registry profile IDs and include research-ledger links.
Before removing the copied lifecycle table, assert the registry domains equal
the current canonical values exactly: PRD and Spec/Plan/Task use
`draft, active, done, archived`; ARD/ADR and Operations use
`draft, active, accepted, archived`; Tombstone uses only `archived`. Do not
rename, narrow, or expand those domains in this tranche. Record any proposed
future lifecycle normalization in the research decision ledger as deferred,
with a required dedicated migration decision, corpus transition evidence, and
owner; it is not enacted by Spec 027.

- [x] **Step 3: Set canonical support lifecycle**

Change the six canonical support documents from `status: draft` to
`status: active`, preserve the five-key order, and update the support index
descriptions without changing its README profile layout.

- [x] **Step 4: Verify no second machine owner and commit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git add docs/99.templates/support
git commit -m "docs(governance): consolidate template support ownership"
```

Expected: compatibility and legacy gate PASS.

---

### Task 4: Normalize Canonical Non-README Forms

**Files:**

- Modify: all Markdown forms under `docs/99.templates/templates/common/` except the README template
- Modify: all Markdown forms under `docs/99.templates/templates/sdlc/`
- Modify: `docs/99.templates/templates/common/progress.template.md` as an append fragment, not a whole-document form
- Create: `docs/99.templates/templates/common/governance-reference.template.md`
- Create: `docs/99.templates/templates/common/template-support.template.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/validate-document-contract-registry.py` fixed profile IDs and
  semantic digest; the registry library remains out of scope
- Modify: `tests/fixtures/document-contracts/registry-cases.json` profile and
  template coverage rows
- Create: `tests/fixtures/document-contracts/template-compatibility.json`

**Interfaces:**

- Consumes: the exact heading matrix in this Plan and the research ledger.
- Produces: canonical required headings plus finite `legacyRequiredAnyOf` aliases
  keyed by profile for Spec 030 removal, synchronized through the thin CLI
  contract and registry coverage fixture without changing the registry library.

Controller resolution for Task 4: the unchanged quality gate treated new form
headings as immediate authored-corpus requirements and retained whole-document
Reference/memory/progress assertions. Task 4 is therefore authorized to make
`scripts/validate-repo-quality-gates.sh` consume the registry and finite
`template-compatibility.json` debt baseline, update only inventory/link rows in
the two Stage 99 README indexes, and replace those obsolete assertions. The
authored corpus, hook/provider files, and registry library remain out of scope.

- [x] **Step 1: Create compatibility debt fixture before form edits**

The fixture must contain `owner: "Spec 030"`, `growthAllowed: false`, and one
entry per changed profile with `canonical`, `legacyRequiredAnyOf`, and
`baselinePathCount`. Include aliases such as `Related Documents` for canonical
`Traceability`, `Current Hypothesis / Response State` for `Response State`, and
the old Task guidance headings only as forbidden residue, never accepted body
requirements.

Add a `canonicalFormCoverage` array with one object per routed authored profile:
`profile`, `form`, `frontmatterType`, and ordered `requiredHeadings`. Include
explicit rows for `governance/reference` and `governance/template-support` that
point to the two dedicated forms. Assert profile IDs and form paths are unique;
assert every registry profile with `mode: authored` has exactly one row.

Add `templateModeCoverage` with one row for every tracked `*.template.md` form:
`profile`, `form`, `sourceProfiles`, `placeholderPolicy`, and
`appendContract`. Its path set must equal the filtered tracked Git inventory,
every row must classify to its declared exact-route `mode: template` profile,
and every non-progress row must deep-equal its source profile's frontmatter,
status domain, and headings. The progress row instead declares
`profile: governance/progress-entry`, source
`governance/progress-ledger`, `placeholderPolicy: template-only`, and the exact
H3/H4 append contract. Keep the legacy harness row only until Task 5 deletes
the form and row together.

- [x] **Step 2: Run exact-heading RED assertion**

```bash
python3 - <<'PY'
from pathlib import Path
task = Path('docs/99.templates/templates/sdlc/execution/task.template.md').read_text()
assert '## Approval and Safety Boundaries' in task
assert '## Working Rules' not in task
assert '## Suggested Types' not in task
assert '## Traceability' in task
PY
```

Expected: FAIL on the current Task form.

- [x] **Step 3: Normalize every Markdown form to the heading matrix**

Use only minimal placeholders and HTML comments. Merge repeated `Purpose` or
`Summary` text into `Overview`; replace parent/canonical input headings with
one final `Traceability`; keep factual Incident chronology out of Postmortem;
keep Guide instructions distinct from Runbook procedure; preserve native
OpenAPI/GraphQL/protobuf files byte-for-byte unless their owner comment is stale.

Create the two dedicated governance forms with the exact five-key frontmatter
order, their literal type values, and the heading sequences above. Do not copy
the content Reference `Definitions / Facts` or `Sources` sections into either
form. Keep placeholder prompts in HTML comments so generated documents must
replace them with topic-specific content.

Add their exact-route `mode: template` profiles in the registry in the same
step, sourced respectively from `governance/reference` and
`governance/template-support`, with deep-equal frontmatter/status/headings and
`placeholderPolicy: template-only`. No new form may rely on a directory-wide
template exception.

Rewrite `progress.template.md` as a fragment beginning with H3
`YYYY-MM-DD - <workstream-title>`, followed by H4 `Metadata`, `Progress`,
`Memory`, `Evidence`, and `Handoff`. Move Date/Layer/Status/Tags bullets below
`Metadata`; remove the template H1 and every H2 so appending it cannot create a
second ledger-level section.

- [x] **Step 4: Add protected Task safety fields before legacy deletion**

Under `Approval and Safety Boundaries`, require fields `Allowed Paths`,
`Forbidden Paths`, `Approval Required`, `Static Validation`, `Live Validation`,
`Secret / Vault Handling`, `Rollback Plan`, and `Evidence Location`. Mark
GitOps/Kubernetes/operations impact as conditional fields within this section.

- [x] **Step 5: Update registry headings and run compatibility checks**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
fixture = json.loads(Path('tests/fixtures/document-contracts/template-compatibility.json').read_text())
registry = json.loads(Path('docs/99.templates/support/document-profiles.json').read_text())
registry_by_id = {profile['id']: profile for profile in registry['profiles']}
rows = fixture['canonicalFormCoverage']
profiles = [row['profile'] for row in rows]
forms = [row['form'] for row in rows]
assert len(profiles) == len(set(profiles))
assert len(forms) == len(set(forms))
authored = {profile['id']: profile for profile in registry['profiles'] if profile['mode'] == 'authored'}
assert set(profiles) == set(authored)
for row in rows:
    profile = authored[row['profile']]
    assert row['form'] == profile['template']
    assert row['frontmatterType'] == row['profile']
    assert row['requiredHeadings'] == profile['headings']['required']
    text = Path(row['form']).read_text()
    assert f"type: {row['frontmatterType']}" in text
    assert [line[3:] for line in text.splitlines() if line.startswith('## ')] == row['requiredHeadings']
for profile in ('governance/reference', 'governance/template-support'):
    row = next(item for item in rows if item['profile'] == profile)
    assert row['form'].endswith(f"{profile.split('/')[-1]}.template.md")

template_rows = fixture['templateModeCoverage']
tracked_forms = {
    line for line in subprocess.check_output(
        ['git', 'ls-files', '--', 'docs/99.templates/templates'], text=True
    ).splitlines() if line.endswith('.template.md')
}
assert {row['form'] for row in template_rows} == tracked_forms
ledger = registry_by_id['governance/progress-ledger']
assert ledger['frontmatter']['mode'] == 'forbidden'
assert ledger['headings']['required'] == ['Work Entries']
for row in template_rows:
    profile = registry_by_id[row['profile']]
    assert profile['mode'] == 'template'
    assert profile['placeholderPolicy'] == row['placeholderPolicy'] == 'template-only'
    assert profile['sourceProfileIds'] == row['sourceProfiles']
    assert profile['appendContract'] == row['appendContract']
    assert profile['routes'] == [{'kind': 'exact', 'value': row['form']}]
    assert profile['template'] == row['form']
    if row['profile'] == 'governance/progress-entry':
        assert row['sourceProfiles'] == ['governance/progress-ledger']
        assert row['appendContract'] == {
            'parentProfileId': 'governance/progress-ledger',
            'parentH2': 'Work Entries',
            'entryHeadingLevel': 3,
            'sectionHeadingLevel': 4,
            'requiredSections': ['Metadata', 'Progress', 'Memory', 'Evidence', 'Handoff'],
        }
        text = Path(row['form']).read_text()
        assert not any(line.startswith(('# ', '## ')) for line in text.splitlines())
        assert [line[4:] for line in text.splitlines() if line.startswith('### ')] == ['YYYY-MM-DD - <workstream-title>']
        assert [line[5:] for line in text.splitlines() if line.startswith('#### ')] == row['appendContract']['requiredSections']
    else:
        assert row['appendContract'] is None
        for source_id in row['sourceProfiles']:
            source = registry_by_id[source_id]
            assert profile['frontmatter'] == source['frontmatter']
            assert profile['statusDomain'] == source['statusDomain']
            assert profile['headings'] == source['headings']
PY
bash scripts/validate-repo-quality-gates.sh .
```

Expected: all PASS and compatibility debt count equals the fixture baseline.

- [x] **Step 6: Commit canonical forms**

```bash
git diff --check
git add docs/99.templates/templates/common docs/99.templates/templates/sdlc docs/99.templates/support/document-profiles.json tests/fixtures/document-contracts/template-compatibility.json
git commit -m "refactor(templates): normalize document forms"
```

Expected: commit succeeds.

---

### Task 5: Delete the Legacy Task Form and Preserve Compatibility

**Files:**

- Delete: retired duplicate harness Task starter form under `templates/sdlc/specs/`
- Modify: `docs/99.templates/README.md` inventory/target-link rows only
- Modify: `docs/99.templates/templates/README.md` inventory/target-link rows only
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: `tests/fixtures/document-contracts/template-compatibility.json`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: files returned by the recorded pre-deletion legacy-reference
  inventory, solely for dead-link/current-claim cleanup or bounded historical
  wording that marks the duplicate retired

**Interfaces:**

- Consumes: canonical Task safety fields from Task 4.
- Produces: zero active references to the deleted form and dual-gate compatibility until Spec 030.

- [x] **Step 1: Record legacy-reference RED evidence**

Run and preserve the exact pre-deletion legacy query in the Task report before
editing. Expected: active references and the duplicate form are reported.

- [x] **Step 2: Delete the file with `apply_patch` and remove active references**

Delete the retired duplicate form. Remove its inventory rows, route prose, validator
locations/types, and Stage 00 selection guidance. Replace high-risk Task
guidance with a link to the standard Task form's `Approval and Safety
Boundaries` contract. Delete the duplicate exact-route registry profile and its
`templateModeCoverage` fixture row in the same change; leave the canonical
Task source/template profiles unchanged.

- [x] **Step 3: Make legacy heading enforcement explicitly temporary**

Modify the embedded structural template check to read
`template-compatibility.json`: canonical forms are checked against registry
headings; current authored files may satisfy only the declared legacy aliases;
unknown aliases and counts above `baselinePathCount` fail. Do not remove the
existing quality gate before Spec 029 is production-ready.

- [x] **Step 4: Prove Stage 99 README scope is inventory-only**

```bash
git diff --unified=0 -- docs/99.templates/README.md docs/99.templates/templates/README.md
```

Expected: changed hunks contain only form inventory/tree rows, target links,
and removal of the legacy form reference; no README heading/layout redesign.

- [x] **Step 5: Prove zero active legacy references**

```bash
test -z "$(find docs/99.templates/templates/sdlc/specs -maxdepth 1 -type f -iname '*harness*task*' -print)"
if rg -n 'task-legacy-har[n]ess|specialized starter that supplements' docs scripts tests .agents .claude .codex; then exit 1; fi
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
```

Expected: searches return no matches and both validators PASS.

- [x] **Step 6: Commit legacy removal**

```bash
git add docs scripts/validate-repo-quality-gates.sh scripts/validate-document-contract-registry.py tests/fixtures/document-contracts/template-compatibility.json tests/fixtures/document-contracts/registry-cases.json
git commit -m "refactor(templates): remove legacy harness task form"
```

Expected: commit succeeds.

---

### Task 6: Close Evidence and Hand Off README Body Ownership

**Files:**

- Modify: `docs/03.specs/027-template-contract-consolidation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-template-contract-consolidation.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: research, support, template, compatibility, and legacy-removal results.
- Produces: done evidence and an explicit statement that Spec 028 owns all Stage 99 README profile/body redesign.

- [x] **Step 1: Run the complete validation bundle**

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
rg -n 'task-legacy-har[n]ess|Suggested Types|Working Rules' docs/99.templates docs/00.agent-governance scripts tests
git diff --check
pre-commit run --all-files
```

Expected: validators PASS; the retired duplicate marker has zero matches; each
remaining `Suggested Types` or `Working Rules` match is classified as finite
Spec 030 fixture/gate evidence, completed historical evidence, or authored
Stage 99 README/body debt handed to Specs 028/030; hooks pass.

- [x] **Step 2: Record compatibility and README handoff evidence**

In the Task, record canonical/legacy heading counts, the Spec 030 removal owner,
the exact Stage 99 README inventory-only diff boundary, commands, PASS/SKIP,
reviewer, and rollback range. Link Spec 028 as README-form/body owner.

- [x] **Step 3: Close lifecycle and indexes**

Set Spec, Plan, and Task to `done`, all TCC rows to `Done`, and all three index
rows to `Done` dated `2026-07-12`.

- [x] **Step 4: Commit closure**

```bash
git add docs/03.specs/027-template-contract-consolidation/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-12-template-contract-consolidation.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-12-template-contract-consolidation.md docs/04.execution/tasks/README.md
git commit -m "docs(templates): close consolidation evidence"
```

Expected: commit succeeds.

## Completion Criteria

- [x] Ten type-to-source family rows are reviewed before form changes.
- [x] Support prose no longer owns complete route/state/profile tables.
- [x] Every non-README routed type has one canonical form and exact heading profile.
- [x] Legacy harness Task form and active references are zero.
- [x] Compatibility debt is finite, non-growing, and assigned to Spec 030.
- [x] Stage 99 README edits remained inventory-only and Spec 028 handoff is explicit.
- [x] Repository quality, all-files, and reciprocal lifecycle evidence pass.

## Related Documents

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Registry Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **Spec**: [Template Contract Consolidation](../../03.specs/027-template-contract-consolidation/spec.md)
- **Task**: [Template Contract Consolidation](../tasks/2026-07-12-template-contract-consolidation.md)
