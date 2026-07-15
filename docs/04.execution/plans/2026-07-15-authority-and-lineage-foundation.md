---
title: 'Authority and Lineage Foundation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-15
---

# Authority and Lineage Foundation Implementation Plan

## Overview

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement registry-owned program lineage, predecessor-gated execution
admission, and evidence-backed Current audit dispositions for Spec 034.

**Architecture:** Registry v6 replaces the untyped single-program `specs` list
with closed, typed `programs`, `tranches`, and `followUps` relations. The
registry validator owns data shape, identity, ordering, and repository-path
integrity; the cross-document validator owns frontmatter-state, reciprocal-link,
historical-exception, execution-admission, and duplicate-authority checks.
Current audit facts remain immutable while a dated remediation overlay records
HEAD-backed dispositions.

**Tech Stack:** Markdown, YAML frontmatter, JSON Schema 2020-12, Python 3,
Git-index inspection, repository Markdown parsers, pre-commit, and Git.

### Global Constraints

- Only Spec 034 has an active Plan/Task pair while it is the first unfinished
  PRD-006 tranche; Specs 035-040 remain approved contracts without execution
  admission.
- PRD-005, ARD-0008, ADR-0016, Specs 026-033, and their completed Plan/Task
  bodies are immutable historical evidence.
- The production registry accepts only schema v6. Legacy v5 lineage input is
  exercised only by a self-test migration fixture and is never a production
  compatibility branch.
- No relationship key is added to document frontmatter.
- Stage 00 may explain lifecycle concepts but may not own an unvalidated exact
  lifecycle or program-membership table.
- Audit observation rows, priorities, scores, and observation SHA remain
  unchanged; remediation facts are appended to the mutable overlay only.
- Repository-static PASS never claims provider-runtime, remote GitHub, secret,
  Vault, Kubernetes, Argo CD, or live-system readiness.
- Use `apply_patch` for manual file edits, test-first changes, independent
  requirements and quality review, and one logical commit per work package.
- The known `os.mkfifo` unsupported-filesystem failure is recorded as a bounded
  Spec 039 follow-up; every other all-files hook must pass.

## Context

[Spec 034](../../03.specs/034-authority-and-lineage-foundation/spec.md)
defines the first dependency-ready tranche of the approved PRD-006 program.
Current schema v5 stores one object containing PRD `005`, ARD `0008`, and a
flat list that incorrectly treats Spec 033 as an original tranche. The typed
`Registry` object does not expose that object, so no production semantic check
can reject overlap, missing decisions, invalid order, state drift, or an
execution Plan attached to a blocked successor.

The Current WEIA roadmap already has repository evidence for RMD-005, RMD-009,
RMD-011, RMD-013, and RMD-032, but its integrated register does not yet record
their normalized post-observation dispositions. Two Stage 00 rules also repeat
the same exact lifecycle transition table even though Stage 99 is the machine
owner.

### File and interface map

| Unit | Exact owners | Responsibility |
| --- | --- | --- |
| Registry schema/data | `docs/99.templates/support/document-profiles.schema.json`, `docs/99.templates/support/document-profiles.json` | Own the closed v6 lineage declaration. |
| Typed loader | `scripts/document_contracts.py` | Expose immutable lineage objects and reject malformed or non-repository relations. |
| Registry mutation proof | `scripts/validate-document-contract-registry.py`, `tests/fixtures/document-contracts/registry-cases.json` | Prove v6 production rejection and isolated legacy migration. |
| Cross-document proof | `scripts/validate-links-and-owners.py`, `tests/fixtures/links-and-owners.json` | Compare lineage with document state, links, historical exceptions, and Plan/Task admission. |
| Stage 00 summaries | `docs/00.agent-governance/rules/stage-authoring-matrix.md`, `docs/00.agent-governance/rules/document-stage-routing.md` | Explain the pre-edit procedure without copying exact state tables. |
| Current audit overlay | `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md` | Record dated HEAD dispositions without rewriting observations. |
| Execution evidence | This Plan, its paired Task, Stage 04 indexes, Spec 034, and the migration ledger | Preserve authorization, results, reviews, and rollback boundaries. |

### Registry v6 interface

Production `programLineage` uses this exact shape and remains ordered by PRD
number. Relation `order` values are contiguous and one-based.

```json
{
  "programLineage": {
    "programs": [
      {
        "prd": "005",
        "ard": "0008",
        "tranches": [
          {
            "spec": "026",
            "order": 1,
            "state": "done",
            "reason": "Original ADR-0016 tranche",
            "decision": "0016"
          }
        ],
        "followUps": [
          {
            "spec": "033",
            "order": 1,
            "state": "done",
            "reason": "Post-program template lifecycle follow-up",
            "decision": "0017",
            "evidenceMode": "successor-record"
          }
        ]
      }
    ]
  }
}
```

`evidenceMode` is `reciprocal-body` for mutable/future follow-ups and
`successor-record` only for the ADR-0017-governed Spec 033 historical
exception. Original tranches have no evidence-mode field. PRD, ARD, ADR, and
Spec paths are derived by exact numeric-prefix discovery and must resolve to
one tracked regular file with the expected document profile.

## Goals & In-Scope

- Upgrade the registry and its typed projection from v5 to v6.
- Declare PRD-005 original Specs 026-032 and historical follow-up Spec 033.
- Declare PRD-006 original Specs 034-040 in dependency order.
- Reject duplicate programs, duplicate or overlapping members, non-contiguous
  order, unknown paths, wrong states, absent decisions, invalid evidence modes,
  and follow-ups that predate their program.
- Enforce reciprocal mutable lineage while preserving the exact historical
  Spec 033 exception.
- Enforce that only the first unfinished tranche has a current Plan/Task pair.
- Replace unvalidated Stage 00 lifecycle tables with pointers to Stage 99.
- Add evidence-backed remediation dispositions for the five named RMD findings.
- Close Spec 034 only after complete repository-static validation and two-stage
  independent review.

## Non-Goals & Out-of-Scope

- Archive envelope implementation or Tombstone conversion.
- Plan/Task corpus movement or Stage 01-05 migration.
- Lifecycle transition-evidence predicates owned by Spec 035.
- Stage 90 information-architecture changes owned by Spec 038.
- GitHub workflow or FIFO portability changes owned by Spec 039.
- Rewriting completed or accepted evidence to manufacture reciprocal links.
- Live provider, remote CI, Kubernetes, Vault, ESO, Argo CD, or secret access.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| ALF-001 | Introduce typed registry v6 program relations | Approved Spec 034 and active Plan/Task | Registry RED/GREEN fixtures, strict production load, and one logical commit |
| ALF-002 | Enforce cross-document lineage and execution admission; retire duplicate Stage 00 tables | ALF-001 | Cross-document mutation fixtures and strict current-corpus PASS |
| ALF-003 | Normalize the Current audit remediation overlay | ALF-002 | Exact five-finding overlay with repository evidence and preserved observation rows |
| ALF-004 | Run full gates, independent review, and close the tranche | ALF-003 | Done Spec/Plan/Task, review verdicts, rollback boundary, and no admitted successor Plan/Task |

### Task 1: Introduce Typed Registry v6 Program Relations

**Files:**

- Modify: `docs/99.templates/support/document-profiles.schema.json`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `scripts/document_contracts.py`
- Modify: `scripts/validate-document-contract-registry.py`
- Modify: `tests/fixtures/document-contracts/registry-cases.json`
- Modify: `scripts/README.md`
- Modify: `docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md`

**Interfaces:**

- Consumes: registry v5 profiles/current-owner/reference-pack contracts and
  ADR-0017 lineage semantics.
- Produces: `ProgramRelation`, `ProgramFollowUp`, and `ProgramLineage`
  dataclasses; `Registry.program_lineage: tuple[ProgramLineage, ...]`; strict
  v6 diagnostics used by Task 2.

- [ ] **Step 1: Add RED lineage mutation cases**

Add cases for duplicate programs, duplicate members, tranche/follow-up overlap,
non-contiguous order, unknown PRD/ARD/ADR/Spec, wrong relation state, missing
decision, invalid evidence mode, future/predating follow-up, and production
legacy-v5 input. Expected stable rule IDs are:

```json
[
  "REGISTRY_PROGRAM_DUPLICATE",
  "REGISTRY_PROGRAM_MEMBER_DUPLICATE",
  "REGISTRY_PROGRAM_MEMBER_OVERLAP",
  "REGISTRY_PROGRAM_RELATION_ORDER",
  "REGISTRY_PROGRAM_PATH",
  "REGISTRY_PROGRAM_STATE",
  "REGISTRY_PROGRAM_DECISION",
  "REGISTRY_PROGRAM_EVIDENCE_MODE",
  "REGISTRY_PROGRAM_CHRONOLOGY",
  "REGISTRY_SCHEMA"
]
```

- [ ] **Step 2: Run the registry self-test and confirm RED**

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
```

Expected: non-zero with the first unimplemented lineage mutation or missing
v6 typed projection; existing 59 cases remain unchanged.

- [ ] **Step 3: Replace the production schema/data with the closed v6 shape**

Set the schema identity and version exactly as follows, require a non-empty
`programs` array, close every object with `additionalProperties: false`, and
encode the relation fields shown in the v6 interface above:

```json
{
  "$id": "https://hy-home.k8s/schemas/document-profiles-6.schema.json",
  "schemaVersion": 6
}
```

Populate PRD-005 with tranches 026-032 plus follow-up 033, and PRD-006 with
tranches 034-040 plus an empty `followUps` list. Use actual document states and
ADR-0016/ADR-0017 decision identifiers.

- [ ] **Step 4: Add the typed loader and semantic checks**

Add immutable types with these exact fields:

```python
@dataclass(frozen=True)
class ProgramRelation:
    spec_id: str
    order: int
    state: str
    reason: str
    decision_id: str


@dataclass(frozen=True)
class ProgramFollowUp(ProgramRelation):
    evidence_mode: Literal["reciprocal-body", "successor-record"]


@dataclass(frozen=True)
class ProgramLineage:
    prd_id: str
    ard_id: str
    tranches: tuple[ProgramRelation, ...]
    follow_ups: tuple[ProgramFollowUp, ...]
```

Validate unique/sorted programs, contiguous one-based relation order, no member
overlap, one tracked regular profile-correct owner for every numeric ID,
frontmatter state parity, accepted governing ADRs, and follow-up chronology.
Chronology uses the governing ADR's immutable accepted frontmatter as the
admission key: `(date.fromisoformat(updated), int(decision_id))`. A follow-up
key must be greater than or equal to the maximum original-tranche admission
key; on the same date its numeric ADR ID must be greater. Follow-up `order`
remains a separate contiguous sequence and is never inferred from Spec number.
Expose `program_lineage` on `Registry`. Keep the legacy converter private to
the registry self-test; `load_registry()` must reject v5 production data.

- [ ] **Step 5: Run focused and strict registry checks**

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
```

Expected: self-test count increases by every new case; strict mode reports zero
uncovered and zero ambiguous paths and loads two programs.

- [ ] **Step 6: Document the v6 script responsibility and commit**

Update only the `validate-document-contract-registry.py` and
`document_contracts.py` inventory rows in `scripts/README.md`. Record commands
and results in the paired Task, then commit:

```bash
git add docs/99.templates/support/document-profiles.schema.json docs/99.templates/support/document-profiles.json scripts/document_contracts.py scripts/validate-document-contract-registry.py tests/fixtures/document-contracts/registry-cases.json scripts/README.md docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md
git commit -m "refactor(contracts): add registry v6 program lineage"
```

### Task 2: Enforce Cross-Document Lineage and Execution Admission

**Files:**

- Modify: `scripts/validate-links-and-owners.py`
- Modify: `tests/fixtures/links-and-owners.json`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify: `scripts/README.md`
- Modify: `docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md`

**Interfaces:**

- Consumes: `Registry.program_lineage`, parsed document profiles/status/body
  links, and active Stage 04 Plan/Task relations.
- Produces: `_program_lineage_diagnostics(context, program_lineage)` with stable
  `PROGRAM-LINEAGE-*` diagnostics and a duplicate-fact scan.

- [ ] **Step 1: Add RED cross-document cases**

Extend the isolated fixture tree with PRD, ARD, accepted ADR, original Spec,
historical follow-up, Plan, and Task records. Add cases expecting:

```json
[
  "PROGRAM-LINEAGE-STATE",
  "PROGRAM-LINEAGE-RECIPROCAL",
  "PROGRAM-LINEAGE-HISTORICAL-EXCEPTION",
  "PROGRAM-LINEAGE-EXECUTION-GATE",
  "PROGRAM-LINEAGE-DUPLICATE-AUTHORITY"
]
```

Positive fixtures must cover a mutable reciprocal follow-up, the exact Spec 033
`successor-record` exception, and a single Plan/Task pair for the first
unfinished tranche.

- [ ] **Step 2: Run the cross-document self-test and confirm RED**

Run:

```bash
python3 scripts/validate-links-and-owners.py --root . --self-test
```

Expected: non-zero because the new program mutation cases are not yet handled.

- [ ] **Step 3: Implement deterministic relation diagnostics**

Import the typed `Registry`, pass it through the existing raw-diagnostic
interface, and add lineage diagnostics before final sorting:

```python
def _raw_diagnostics(
    context: Context,
    registry: Registry,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
```

Immediately after the existing `_ledger_diagnostics(context)` extension, add:

```python
diagnostics.extend(
    _program_lineage_diagnostics(context, registry.program_lineage)
)
```

The `validate_cross_document_contracts()` call becomes:

```python
return _raw_diagnostics(
    context,
    registry,
    profiles_by_id,
    body_contracts,
    body_contract_path_prefixes,
)
```

The main strict CLI call becomes:

```python
diagnostics = _raw_diagnostics(
    context,
    registry,
    profiles_by_id,
    args.body_contracts,
    tuple(args.body_contract_path_prefix),
)
```

Update both production call sites to pass the loaded `registry` between
`context` and `profiles_by_id`. Isolated self-tests call
`_program_lineage_diagnostics()` with fixture `ProgramLineage` values directly;
they do not depend on the production registry's program set.

The helper must enforce these rules:

```text
relation state == target Spec frontmatter state
mutable draft/active original tranche -> Spec links PRD and ARD; mutable PRD/ARD link back
mutable draft/active follow-up -> Spec links PRD, ARD, and governing ADR; mutable upstream owners link back
done/accepted historical owner -> no body rewrite required
successor-record -> only PRD-005 / Spec-033 / ADR-0017 / roadmap overlay
dependency-ready tranche -> first tranche whose state is not done or archived
current Plan and Task -> exactly one pair and only for dependency-ready tranche
Stage 00 exact lifecycle table -> rejected unless registry-generated/validated
```

Use normalized repository-relative paths and parsed rendered links; do not use
substring matching or filesystem traversal outside the tracked inventory.

- [ ] **Step 4: Remove duplicate Stage 00 lifecycle tables**

In both Stage 00 rule documents, replace the copied family/transition table
with a short procedure pointing to the registry, frontmatter schema, SDLC
governance, and template routing contract. Preserve stage-routing and pre-edit
instructions that are unique to each document.

- [ ] **Step 5: Run focused and strict cross-document checks**

Run:

```bash
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts registry
```

Expected: all commands exit zero; Spec 033 passes only through the named
historical exception; no current Plan/Task points to Specs 035-040.

- [ ] **Step 6: Record results and commit**

```bash
git add scripts/validate-links-and-owners.py tests/fixtures/links-and-owners.json docs/00.agent-governance/rules/stage-authoring-matrix.md docs/00.agent-governance/rules/document-stage-routing.md scripts/README.md docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md
git commit -m "test(docs): enforce program lineage admission"
```

### Task 3: Normalize the Current Audit Remediation Overlay

**Files:**

- Modify: `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md`
- Modify: `docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md`

**Interfaces:**

- Consumes: original RMD rows, Spec 025/031/033 evidence, registry v6 results,
  and Current repository validators.
- Produces: a dated five-row remediation overlay; original observation facts
  remain byte-for-byte unchanged.

- [ ] **Step 1: Capture the immutable observation-row baseline**

Run this byte-preserving assertion:

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess

sha = "15b154d43c868c8a758e2021b1d7023f462ea0f4"  # pragma: allowlist secret
path = "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
ids = (b"RMD-005", b"RMD-009", b"RMD-011", b"RMD-013", b"RMD-032")

baseline = subprocess.check_output(["git", "show", f"{sha}:{path}"])
current = Path(path).read_bytes()

def selected_rows(payload: bytes) -> list[tuple[bytes, bytes]]:
    rows = []
    for line in payload.splitlines(keepends=True):
        for finding_id in ids:
            if line.startswith(b"| " + finding_id + b" |"):
                rows.append((finding_id, line))
    return rows

baseline_rows = selected_rows(baseline)
current_rows = selected_rows(current)
assert len(baseline_rows) == 5, len(baseline_rows)
assert len(current_rows) == 5, len(current_rows)
assert tuple(item[0] for item in baseline_rows) == ids, baseline_rows
assert tuple(item[0] for item in current_rows) == ids, current_rows
assert current_rows == baseline_rows, "observation rows changed"
print("PASS immutable RMD observation rows: 5/5 byte-equal")
PY
```

Expected: exact `PASS immutable RMD observation rows: 5/5 byte-equal`; any
missing, reordered, or byte-changed row fails before overlay authoring.

- [ ] **Step 2: Add the dated disposition overlay**

Append one table with the columns `Finding`, `HEAD disposition`,
`Repository evidence`, and `Retained boundary`. Record:

```text
RMD-005 -> closed for tested current-owner/current-pack pointer integration
RMD-009 -> closed for tracked authored value and placeholder validation
RMD-011 -> closed for repository-static path-to-validator selection; remote run DEFER
RMD-013 -> closed for repository-static AI-agent validation obligations; provider delivery DEFER
RMD-032 -> closed for intended local role semantic fixtures; provider-native behavior DEFER
```

Link every disposition to its owning Spec/Plan/Task and validator. State that
later Specs 035-040 own broader transition, CI, provider, archive, and closure
work and that no live readiness is inferred.

- [ ] **Step 3: Prove observation preservation and overlay integrity**

Re-run the exact byte-preserving Python assertion from Step 1 after editing;
it must still print `PASS immutable RMD observation rows: 5/5 byte-equal`.
Then run:

```bash
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts registry
git diff 15b154d43c868c8a758e2021b1d7023f462ea0f4 -- docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md
```

Expected: validators pass and the diff adds only the new overlay relative to
the original RMD rows.

- [ ] **Step 4: Record results and commit**

```bash
git add docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md
git commit -m "docs(audit): reconcile current lineage dispositions"
```

### Task 4: Validate and Close the Authority Foundation

**Files:**

- Modify: `docs/03.specs/034-authority-and-lineage-foundation/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-15-authority-and-lineage-foundation.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`

**Interfaces:**

- Consumes: ALF-001 through ALF-003 commits and independent reviewer verdicts.
- Produces: done Spec/Plan/Task evidence, a done Spec-034 registry relation,
  current indexes, and an explicit gate allowing Spec 035 planning only after
  this commit.

- [ ] **Step 1: Run the complete repository-static verification suite**

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts registry
python3 scripts/validate-links-and-owners.py --root . --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

Expected: the focused registry/profile/link commands pass. The canonical
aggregate and all-files runs preserve the already-reproduced `os.mkfifo`
unsupported-filesystem failure; if either reports any additional failure, do
not close the tranche.

Because the canonical aggregate exits at that FIFO self-test under `set -e`,
run the post-FIFO components individually and then execute an in-memory
diagnostic copy of the aggregate with only that exact self-test line removed:

```bash
python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD
python3 scripts/validate-vault-eso-contracts.py --self-test
python3 scripts/validate-vault-eso-contracts.py --root .
python3 scripts/validate-affected-surfaces.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-role-semantics.py --self-test
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py . --self-test
python3 scripts/validate-agent-roster-currentness.py .
sed '/validate-gitops-change-set.py" --self-test/d' scripts/validate-repo-quality-gates.sh | bash -s -- .
```

Expected: every individual command and the filtered diagnostic copy pass. The
filtered run is evidence about the remainder of the aggregate only; it is not
reported as a canonical repository-quality PASS, and the omitted self-test
remains DEFER until Spec 039.

- [ ] **Step 2: Dispatch independent requirements and quality review**

The requirements reviewer checks VAL-ALF-001 through VAL-ALF-007, historical
immutability, and the five audit dispositions. After every requirement issue is
fixed, a fresh quality reviewer checks correctness, fail-closed behavior,
fixture quality, scope, and documentation. Required verdicts are exactly
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`.

- [ ] **Step 3: Apply closure state atomically**

Set Spec 034, this Plan, and its Task to `done`; set the PRD-006 Spec-034
relation state to `done`; update the three indexes, ledger result/evidence, Task
results, verification summary, review verdicts, commit list, residual risk, and
rollback parent. Do not create the Spec 035 Plan/Task in this closure commit.

- [ ] **Step 4: Re-run closure validators and commit**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict --body-contracts registry
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
git diff --check
git add docs/03.specs/034-authority-and-lineage-foundation/spec.md docs/03.specs/README.md docs/04.execution/plans/2026-07-15-authority-and-lineage-foundation.md docs/04.execution/plans/README.md docs/04.execution/tasks/2026-07-15-authority-and-lineage-foundation.md docs/04.execution/tasks/README.md docs/99.templates/support/document-profiles.json docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
git commit -m "docs(execution): close authority lineage foundation"
```

Expected: closure validators pass, working tree is clean, and no current
Plan/Task references Specs 035-040.

If and only if the all-files run has no failure other than the independently
reproduced FIFO `Errno 95`, preserve that output in the Task and use this
bounded commit form after all component gates and remaining hooks pass:

```bash
env SKIP=strict-repository-quality git commit -m "docs(execution): close authority lineage foundation"
```

Any additional failure blocks closure; the skip must not be widened to another
hook or reused after Spec 039 fixes the portability defect.

## Verification Plan

| Work package | RED proof | GREEN proof | Durable evidence |
| --- | --- | --- | --- |
| ALF-001 | New v6 mutation fixtures fail before parser/schema support. | Registry self-test and strict mode pass with two programs. | Paired Task command results and logical commit. |
| ALF-002 | State/link/admission/duplicate-authority fixtures fail. | Cross-document self-test and strict corpus pass. | Fixture names, rule IDs, Stage 00 diff, and logical commit. |
| ALF-003 | Five original roadmap rows have no dated disposition overlay. | Overlay links exact repository evidence while original rows remain unchanged. | Baseline comparison and audit commit. |
| ALF-004 | Spec/Plan/Task and Spec-034 relation remain active. | All closure state and indexes agree after independent approval. | Task summary, review verdicts, rollback parent, and closure commit. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| v6 silently accepts legacy production shape | Ambiguous authority continues | Production schema is v6-only; legacy conversion is private self-test code. |
| Numeric lookup binds the wrong document | False lineage | Require exactly one tracked regular file with profile and numeric-prefix match. |
| Completed evidence is rewritten for reciprocity | Historical corruption | Enforce successor-record only for the exact Spec 033/ADR-0017 exception. |
| Active successor Specs are treated as executable | Parallel unauthorized work | Compute the first unfinished tranche and reject any other current Plan/Task. |
| Audit closure overclaims remote/live readiness | False assurance | Separate repo-static closure from provider/remote/live DEFER in every row. |
| New gate blocks on unrelated filesystem behavior | Premature scope expansion | Record only the known FIFO failure and route its fix to Spec 039. |

## Completion Criteria

- VAL-ALF-001 through VAL-ALF-007 have named automated or reviewed evidence.
- Registry v6 exposes two typed programs and rejects every negative relation
  fixture with stable diagnostics.
- Specs 026-032 are the only original PRD-005 tranches; Spec 033 is one
  historical follow-up; Specs 034-040 are the ordered PRD-006 tranches.
- Only Spec 034 owns a current Plan/Task while this Plan is active.
- The five RMD findings have dated, evidence-backed overlay dispositions and
  unchanged observation rows.
- Stage 00 has no unvalidated exact lifecycle owner table.
- Independent review returns both required approval verdicts.
- The closure commit leaves no unrecorded failure other than the explicitly
  routed FIFO portability issue.

## Traceability

- **Spec**: [Authority and Lineage Foundation](../../03.specs/034-authority-and-lineage-foundation/spec.md)
- **Task**: [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Decision**: [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ALF-001](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-001 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-002](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-001 / ALF-002 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-003](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-001 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-004](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-001 / ALF-002 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-005](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-003 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-006](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-002 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
| [VAL-ALF-007](../../03.specs/034-authority-and-lineage-foundation/spec.md#success-criteria--verification-plan) | ALF-002 / ALF-004 | [Authority and Lineage Foundation Task](../tasks/2026-07-15-authority-and-lineage-foundation.md) |
