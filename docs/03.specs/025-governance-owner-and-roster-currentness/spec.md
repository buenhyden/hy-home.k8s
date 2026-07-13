---
title: 'Governance Owner and Roster Currentness Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-13
---

# Governance Owner and Roster Currentness Technical Specification

## Overview

This design defines one bounded repository-normalization cycle with three
connected outcomes:

1. make the Stage 90 audit information architecture expose one unambiguous
   Current pack while preserving dated evidence;
2. reconcile every active Stage 03 Spec and Stage 04 Plan with its actual
   lifecycle, execution evidence, and current owner; and
3. implement RMD-004 through a new, narrow canonical Spec for the ten-role,
   thirty-adapter roster and canonical-owner currentness contract.

The design is repository-static. It does not authorize live Kubernetes,
Argo CD, Vault, provider-runtime, credential, secret-value, or third-party
mutation.

## Strategic Boundaries & Non-goals

In scope are the Stage 90 audit indexes and pack metadata, every canonical
Stage 03 parent Spec, every canonical Stage 04 Plan, the new RMD-004 execution
chain, the active Stage 00 roster/current-owner summaries, and deterministic
repository validation for those facts.

Out of scope are broad rewrites of dated audit bodies, semantic changes to
provider agent roles, model promotion, new provider capabilities, unrelated
RMD findings, live runtime proof, and bulk archival based only on document age
or completion.

## Contracts

- **Config Contract**: The three provider adapter directories expose the same
  ten role stems using provider-native file formats and metadata.
- **Data / Interface Contract**: Spec, Plan, Task, audit-pack, and owner links
  form explicit repository-relative lineage; Task records own execution state.
- **Governance Contract**: One active document owns each current fact.
  Completed evidence remains `done`; only genuinely conflicting and fully
  replaced records become Archive Tombstones.

### Approved Decisions

- Use evidence-based selective Archive, not age-based or completion-based
  Archive.
- Keep completed Specs and Plans in their canonical stages when they remain
  valid design or execution evidence.
- Archive only when a document conflicts with the current contract, a successor
  fully absorbs its scope, a replacement exists, and unique evidence remains
  available elsewhere.
- Audit every Spec and Plan in the workspace, not only documents directly
  named by RMD-004.
- Keep dated audit report bodies as evidence snapshots; normalize navigation,
  pack role, and current-owner metadata around them.
- Do not reopen the completed lifecycle of Spec 015 for new work. Create a new
  RMD-004 owner so the 2026-07-04 completed normalization and the new
  currentness implementation have separate Plan and Task evidence.
- Work in an isolated `.worktrees/` worktree and commit each logical unit
  separately.

### Baseline Evidence

The design audit found:

- twenty parent Specs under `docs/03.specs/*/spec.md`;
- four Specs marked `active` and sixteen marked `draft`;
- every Spec from 009 through 024 has completed Stage 04 execution evidence,
  so all sixteen `draft` states are lifecycle drift;
- forty-one canonical Stage 04 Plans, all `type: sdlc/plan` and `status: done`;
- forty Plans have same-basename Task records, while the remaining
  decision-follow-up Plan is evidenced by the differently named Phase 1 audit
  Task;
- one 967-line completed execution plan is misplaced as an active
  `content/reference` inside the Current Stage 90 audit pack;
- sixteen Plan-to-Task relationships need explicit clickable linkage or
  correction;
- ten completed Plans retain unchecked historical execution instructions even
  though their Task evidence is complete; and
- the provider adapter inventory contains ten shared role stems in each of
  `.claude/agents`, `.agents/agents`, and `.codex/agents`, while three active
  harness-catalog statements still describe an eight-role roster.

### Design Alternatives

### Selected: Evidence-Preserving Normalization

Normalize lifecycle and ownership in place, retain completed records, and
introduce a new narrow RMD-004 owner. This preserves execution provenance and
avoids conflating completed and new work.

### Rejected: Reopen Spec 015

Reusing Spec 015 would reduce the number of documents, but its original Plan
and Task are already complete. Reopening it would mix two implementation
lifecycles and make acceptance evidence ambiguous.

### Rejected: Archive-Heavy Consolidation

Archiving every superseded or old record would shrink the active tree, but it
would remove useful completed execution bodies and force broad inbound-link
rewrites. Completion alone is not an Archive reason.

## Core Design

```text
Stage 90 dated audit evidence
  -> one parent Current pointer and pack registry
  -> Current audit remediation finding RMD-004
  -> Stage 03 Spec 025 owns roster/current-owner acceptance
  -> Stage 04 Plan orders implementation
  -> Stage 04 Task owns execution evidence
  -> Stage 00 owns durable governance and roster facts
  -> validator enforces deterministic projections
```

The ownership boundaries are:

| Surface | Canonical responsibility |
| --- | --- |
| `docs/90.references/audits/` | Dated findings, scores, evidence, and remediation routing. |
| `docs/03.specs/025-governance-owner-and-roster-currentness/` | RMD-004 design and acceptance contract. |
| `docs/04.execution/plans/` | Ordered implementation, risk, rollback, and verification gates. |
| `docs/04.execution/tasks/` | Actual completion state and verification evidence. |
| `docs/00.agent-governance/` | Durable current roster, role, provider-adapter, and canonical-owner policy. |
| `scripts/validate-repo-quality-gates.sh` and fixtures | Deterministic rejection of roster and owner-pointer drift. |

Secondary documents may summarize these facts only by linking to the canonical
owner. They must not create another roster-count or ownership authority.

The term `owner` is qualified throughout this work:

- **implementation-contract owner**: Spec 025 owns RMD-004 acceptance and
  validation requirements;
- **durable-policy owner**: Stage 00 owns the current governance and roster
  facts after implementation; and
- **execution-evidence owner**: the Stage 04 Task owns what was actually run
  and verified.

The deterministic owner-pointer allowlist is:

| Fact or responsibility | Canonical owner path | Enforcement surface |
| --- | --- | --- |
| Bootstrap authority and loading order | `docs/00.agent-governance/rules/bootstrap.md` | Harness catalog governance pointer. |
| Role/persona responsibility contract | `docs/00.agent-governance/rules/persona.md` | Harness catalog roster section. |
| Stage authoring ownership | `docs/00.agent-governance/rules/stage-authoring-matrix.md` | Harness catalog owner-routing section. |
| Current provider roster and adapter inventory | `docs/00.agent-governance/harness-catalog.md` | Exact role rows and provider adapter rows. |
| Completed ninth/tenth role implementation | `docs/04.execution/tasks/2026-07-06-observability-and-network-review-agents.md` | Harness catalog evidence pointer and Spec 025 lineage. |
| RMD-004 completion evidence | `docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md` | Spec 025 and its same-topic Plan. |
| Document/template ownership contract | `docs/99.templates/support/documentation-contract.md` | Harness catalog documentation-owner pointer. |
| Authored-document route contract | `docs/99.templates/support/template-routing.md` | Harness catalog template-route pointer. |

The validator checks only these declared path relationships and exact roster
sets. It does not infer ownership from arbitrary prose.

## Data Modeling & Storage Strategy

The normalization uses existing Markdown/frontmatter entities rather than a
new registry format. Lifecycle stays in the supported scalar `status` field;
lineage and current-owner declarations stay in human-readable Related
Documents or ownership tables because the current frontmatter schema does not
support custom supersession keys.

No historical body migration or runtime data migration is required. The only
file relocation is the completed Stage 90 execution plan moving to its
canonical Stage 04 Plan route. Archive operations, if later proven necessary,
use the existing central Tombstone schema and index-only access rule.

### Audit Information Architecture

### Parent Audit Index

`docs/90.references/audits/README.md` will own only:

- one Current audit-pack pointer;
- one registry of dated packs and their pack role;
- definitions for Current, Historical, and Resolved pack roles;
- the shared evidence and preservation vocabulary; and
- the rule that active consumers use the Current pointer rather than selecting
  a dated report ad hoc.

Pack role is distinct from document frontmatter lifecycle. For example, a
Historical pack can contain accepted or done evidence without requiring every
report to be archived.

### Dated Pack Indexes

Each dated pack will have a compact README that records its snapshot date,
scope, role, report inventory, successor or resolution pointer, and evidence
boundary. Missing pack READMEs will be added for the 2026-05-24, 2026-07-02,
2026-07-03, and 2026-07-04 packs.

Historical report bodies will not be merged, rewritten, or moved merely to
make the tree appear smaller. The 2026-07-05 pack's stale internal `Current`
labels will be corrected at the pack-navigation/currentness layer.

### Misplaced Execution Plan

`docs/90.references/audits/2026-07-11-weia/implementation-plan.md` will move to:

`docs/04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md`

It will become `type: sdlc/plan`, `status: done`. A compact same-basename Task
will record the completed audit-pack outputs, commits, validation, and scope
boundary. Stage 90 reports will link to that Stage 04 execution record instead
of owning an active execution plan.

### Spec Lifecycle and Current-Owner Design

### Disposition

| Specs | Target state | Rationale |
| --- | --- | --- |
| 004, 005, 008 | `active` | Continuing current implementation or operations contracts. |
| 006 | `active`, narrowed | Retains historical harness-gap baseline and unresolved runtime boundary; does not own RMD-004 roster currentness. |
| 009, 010 | `done`, successor-linked | Completed legacy research/audit pack designs; 017/018 are successors, but completed evidence remains useful and non-conflicting once current ownership is explicit. |
| 011-014, 016-024 | `done` | Corresponding Plans and Tasks are complete. |
| 015 | `done` | The original agent-governance normalization lifecycle is complete. |
| 025 | `active` during implementation, `done` at verified closure | Sole RMD-004 current implementation contract. |

Feature-local `agent-design.md` under Spec 024 will be normalized to `done`
with its parent because the two review roles and all six provider projections
were implemented and verified.

### Overlap Lineage

The following chains will be documented as completed evolution, not parallel
current ownership:

- template/document governance:
  `011 -> 012 -> 013 -> 014 -> 020 -> 021 -> 022 -> 023`;
- research and audit:
  `009 -> 017` and `010 -> 018`; and
- agent governance:
  `006` historical gap context plus `015` completed normalization plus `024`
  completed role-addition evidence feed `025`, the current RMD-004 owner.

Spec 011, 016, and 019 will gain their missing Plan and Task links. Spec and
README index states will match frontmatter after normalization.

### Archive Decision Gate

A Spec or Plan may be replaced with a Tombstone only when all of these are
true:

1. its body materially conflicts with the current contract;
2. a named successor fully absorbs the relevant scope;
3. it no longer owns active acceptance or operations behavior;
4. the replacement path is stable; and
5. unique evidence remains in a retained Task, audit snapshot, or replacement.

If any condition is false, the record stays in place with corrected lifecycle
and lineage. This cycle does not pre-authorize an Archive candidate solely from
its identifier or date.

The known conflict candidates resolve as follows:

| Candidate lineage | Conflict | Fully absorbed | Active owner remains | Evidence retained | Decision |
| --- | --- | --- | --- | --- | --- |
| 009 -> 017 | No after lifecycle/current-owner labeling | Research scope is absorbed, but 009 is valid completed design evidence | No | Yes, 009 Plan/Task and dated pack | Retain 009 as `done`; link successor 017. |
| 010 -> 018 | No after lifecycle/current-owner labeling | Audit-pack scope is absorbed, but 010 is valid completed design evidence | No | Yes, 010 Plan/Task and dated pack | Retain 010 as `done`; link successor 018. |
| 006 -> 025 | No once RMD-004 ownership is removed | No; unresolved runtime boundaries remain | Yes, for harness runtime gaps only | Yes | Retain 006 as narrowed `active`. |
| 015 -> 025 | No; the 2026-07-04 normalization remains valid | No; 025 owns a new acceptance cycle | No | Yes, completed 015 Plan/Task | Retain 015 as `done`. |
| 024 -> 025 | No; it proves the ninth/tenth role delivery | No; 025 consumes rather than replaces that evidence | No | Yes, completed 024 Plan/Task | Retain 024 and its agent design as `done`. |

No known candidate meets all five Archive conditions in this cycle. A newly
discovered candidate must be recorded with the same five-column decision before
any Tombstone move.

### Plan Lifecycle and Evidence Design

All forty-one existing canonical Plans remain `done`. The implementation will:

- replace raw path literals or malformed references with clickable Task links
  where Task evidence exists;
- explicitly link the differently named Phase 1 audit Task from its Plan;
- add the missing parent-Spec links for the SDLC lifecycle Plan and the current
  research-pack refresh Plan;
- declare `Parent Spec: N/A` for genuinely pre-Spec work rather than inventing
  retroactive ownership; and
- label unchecked sections in completed Plans as historical execution
  instructions, with the completed Task as the status and evidence owner.

Unchecked boxes in a completed Plan will not be blindly changed to checked.
Plan intention and Task evidence are different records and must remain so.

The Plan README will distinguish:

- current execution authority;
- completed execution records; and
- superseded lineage that remains useful evidence.

## Interfaces & Data Structures

The principal interfaces are repository path and evidence relationships:

```text
Audit finding ID -> owning Spec validation criterion
Owning Spec -> implementation Plan -> evidence Task
Stage 00 canonical fact -> provider-native projections
Canonical fact and projections -> repository quality-gate result
```

The role-stem set is derived from filenames and compared as a set across all
three provider directories. Current-owner checks use an explicit allowlisted
path/link contract declared by Spec 025 rather than interpreting free-form
prose.

### RMD-004 Canonical Contract

The new Spec will be:

`docs/03.specs/025-governance-owner-and-roster-currentness/spec.md`

It will own these acceptance facts:

- the canonical shared roster has exactly ten role stems;
- each of the Claude, Gemini, and Codex provider directories exposes exactly
  those ten stems;
- the repository therefore has thirty provider adapter files for those roles;
- the harness catalog links to canonical Stage 00, Stage 04, and Stage 99
  owners rather than restating their durable policy; and
- active roster facts cannot retain a stale eight-role statement.

The new same-topic Stage 04 Plan and Task will be the only execution pair for
RMD-004. The completed Spec 015 Plan/Task remain historical inputs, while Spec
024's Task remains the evidence that added the ninth and tenth roles.

### RMD-004 Implementation Components

### Canonical Roster Projection

The adapter directories are provider-native projections of one role-stem set.
The implementation will compare filenames, not require identical provider
metadata fields or identical bodies.

### Canonical Owner Pointers

Active secondary summaries will link to the actual owner for durable policy:

- Stage 00 for governance, role, provider, and harness policy;
- Stage 04 Task records for completion evidence; and
- Stage 99 for template and document-contract rules.

The exact link set will be declared in Spec 025 and enforced only where the
repository has a deterministic owner. The validator will not guess semantic
ownership from prose.

### Deterministic Validation

The repository quality gate will validate:

1. ten identical stems in each of the three provider adapter directories;
2. thirty adapters in aggregate;
3. absence of stale eight-role count claims in designated active roster
   surfaces; and
4. presence of required canonical-owner links in the harness catalog.

Positive and negative fixtures will cover:

- a valid ten-by-three roster;
- a missing role;
- provider stem mismatch;
- a stale eight-role statement; and
- a missing or incorrect canonical-owner pointer.

The test must fail for the intended reason and must not depend on provider
network availability or model resolution.

## Edge Cases & Error Handling

- If a document's completion evidence is missing or contradictory, leave its
  lifecycle unchanged and record the unresolved item in the Task.
- If an Archive candidate lacks a complete replacement or retained evidence,
  keep it in place with a lineage note.
- If a validator cannot distinguish historical quoted evidence from active
  currentness prose, narrow its path and section scope rather than using a
  repository-wide word ban.
- If provider adapter stems differ, do not auto-create or delete agents; fail
  validation and report the exact provider-specific set difference.
- No command in this cycle may inspect secret values or mutate live systems.
- Remote push, pull request creation, or remote merge requires separate user
  approval. The requested finish target is a local merge to `main`.

## Failure Modes & Fallback / Human Escalation

- **Failure mode**: lifecycle evidence disagrees across Spec, Plan, and Task.
  **Fallback**: preserve the current state, record the disagreement, and do not
  claim normalization for that document.
- **Failure mode**: an Archive candidate lacks a stable replacement or retained
  evidence. **Fallback**: keep it as a completed record with explicit lineage.
- **Failure mode**: roster validation detects provider drift. **Fallback**:
  fail with exact set differences; do not synthesize provider agent files.
- **Human escalation**: any live-system action, secret access, provider-runtime
  change, model-policy change, remote publication, or destructive Git action.

## Verification Commands

Each logical commit will run focused checks before the full closeout bundle.
The final bundle will include:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
```

Focused assertions will additionally verify:

- one Current audit pointer and one pack-registry row per dated audit pack;
- all twenty-one Spec index entries match their frontmatter lifecycle;
- every retained Plan has explicit Task evidence or a documented N/A/exception;
- the relocated audit Plan and new compact Task have reciprocal links;
- the three provider adapter stem sets are equal and contain ten entries; and
- negative roster/current-owner fixtures are rejected.

Optional tools that are unavailable will be reported as skipped, not passed.

### Complete Spec Disposition Ledger

This ledger is the implementation input for all twenty baseline Specs. Spec
025 is the new design record and is therefore not part of the pre-change count.

| Spec | Current | Execution evidence | Target | Current owner or successor | Archive result |
| --- | --- | --- | --- | --- | --- |
| 004 Rollouts | active | `2026-05-18-argo-rollouts-progressive-delivery.md` Task | active | 004 current delivery contract | Retain. |
| 005 Notifications | active | `2026-05-18-argo-notifications-slack.md` Task | active | 005 current delivery contract | Retain. |
| 006 Harness gaps | active | Multiple done harness Tasks; unresolved runtime boundary | active, narrowed | 006 runtime-gap boundary; 025 owns RMD-004 | Retain. |
| 008 Current GitOps | active | `2026-06-02-current-implementation-docs-alignment.md` Task | active | 008 current platform contract | Retain. |
| 009 Harness research pack | draft | `2026-07-02-workspace-harness-research-pack.md` Task | done | successor 017 | Retain done. |
| 010 Harness audit pack | draft | `2026-07-02-workspace-harness-implementation-audit-pack.md` Task | done | successor 018 | Retain done. |
| 011 Template migration | draft | `2026-07-03-template-contract-governance-migration.md` Task | done | successor chain through 023 | Retain; add missing links. |
| 012 Template audit | draft | `2026-07-03-template-governance-audit-enhancement.md` Task | done | successor chain through 023 | Retain. |
| 013 Document hardening | draft | `2026-07-03-workspace-document-governance-hardening.md` Task | done | successor chain through 023 | Retain. |
| 014 Document normalization | draft | `2026-07-04-workspace-document-contract-normalization.md` Task | done | successor chain through 023 | Retain. |
| 015 Agent normalization | draft | `2026-07-04-agent-governance-contract-normalization.md` Task | done | 025 owns new RMD-004 cycle | Retain done. |
| 016 Control-surface hardening | draft | `2026-07-04-active-control-surface-governance-hardening.md` Task | done | completed control-surface design | Retain; add missing links. |
| 017 Engineering research | draft | `2026-07-04-workspace-engineering-research-pack.md` and 2026-07-10 Tasks | done | Current research maintenance lineage | Retain done. |
| 018 Engineering audit | draft | `2026-07-05-workspace-engineering-implementation-audit-pack.md` Task | done | 2026-07-11 Current audit successor | Retain done. |
| 019 Path numbering | draft | `2026-07-05-template-path-numbering-contract.md` Task | done | completed path contract | Retain; add missing links. |
| 020 Contract governance | draft | `2026-07-05-workspace-contract-governance-normalization.md` Task | done | successor chain through 023 | Retain. |
| 021 SDLC lifecycle | draft | `2026-07-06-sdlc-lifecycle-contract.md` Task | done | durable lifecycle support docs own policy | Retain done. |
| 022 Control/cloud docs | draft | `2026-07-06-control-cloud-doc-normalization.md` Task | done | completed normalization design | Retain done. |
| 023 Stage03/04 closure | draft | `2026-07-06-stage03-04-repo-static-gap-closure.md` Task | done | completed closure evidence | Retain done. |
| 024 Review agents | draft | `2026-07-06-observability-and-network-review-agents.md` Task | done | 025 consumes role-delivery evidence | Retain Spec and agent design as done. |

### Complete Plan Evidence Ledger

All forty-one baseline Plans are already `done`. `Task` below names the
evidence record; `same` means the Task uses the same filename under
`docs/04.execution/tasks/`. Every row remains in Stage 04 unless later evidence
passes the five-condition Archive gate.

| Plan | Task | Link action | Target / Archive result |
| --- | --- | --- | --- |
| `2026-05-09-github-qa-ci-remediation.md` | same | Verify reciprocal link | done / retain |
| `2026-05-09-scripts-inventory-remediation.md` | same | Verify reciprocal link | done / retain |
| `2026-05-10-agent-first-harness-llm-wiki-hooks.md` | same | Verify reciprocal link | done / retain |
| `2026-05-17-template-crosslink-fix.md` | same | Correct false “no Task” statement | done / retain |
| `2026-05-18-argo-notifications-slack.md` | same | Verify reciprocal link | done / retain |
| `2026-05-18-argo-rollouts-progressive-delivery.md` | same | Verify reciprocal link | done / retain |
| `2026-05-22-docs-governance-full-ab-hardening.md` | same | Verify reciprocal link | done / retain |
| `2026-05-22-workspace-purpose-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-05-24-p3-gitops-secret-runtime-remediation.md` | same | Verify reciprocal link | done / retain |
| `2026-05-28-workspace-skill-expansion.md` | same | Add explicit clickable Task link | done / retain |
| `2026-05-30-antigravity-governance.md` | same | Add explicit clickable Task link | done / retain |
| `2026-05-31-codex-governance-harness-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-06-01-claude-agent-surface-restoration.md` | same | Verify reciprocal link | done / retain |
| `2026-06-01-stage-00-canonical-adapter-redesign.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-current-implementation-docs-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-docs-01-05-current-implementation-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-phase-1-decision-follow-up.md` | `2026-06-02-phase-1-governance-alignment-audit.md` | Add named exception link | done / retain |
| `2026-06-02-phase-2-governance-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-phase-3-protected-surface-hardening.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-phase-4-eso-vault-runtime-diagnosis.md` | same | Verify reciprocal link | done / retain |
| `2026-06-02-stage-00-codex-harness-coverage-reconciliation.md` | same | Verify reciprocal link | done / retain |
| `2026-06-04-harness-four-element-alignment.md` | same | Verify reciprocal link | done / retain |
| `2026-06-05-harness-governance-v2-overlay.md` | same | Verify reciprocal link | done / retain |
| `2026-07-02-workspace-harness-implementation-audit-pack.md` | same | Add explicit clickable Task link | done / retain |
| `2026-07-02-workspace-harness-research-pack.md` | same | Add explicit clickable Task link | done / retain |
| `2026-07-03-template-contract-governance-migration.md` | same | Verify reciprocal link | done / retain |
| `2026-07-03-template-governance-audit-enhancement.md` | same | Verify reciprocal link | done / retain |
| `2026-07-03-workspace-document-governance-hardening.md` | same | Label unchecked instructions historical | done / retain |
| `2026-07-04-active-control-surface-governance-hardening.md` | same | Add explicit clickable Task link | done / retain |
| `2026-07-04-agent-governance-contract-normalization.md` | same | Add Task link; label unchecked instructions historical | done / retain |
| `2026-07-04-workspace-document-contract-normalization.md` | same | Label unchecked instructions historical | done / retain |
| `2026-07-04-workspace-engineering-research-pack.md` | same | Add Task link; label unchecked instructions historical | done / retain |
| `2026-07-05-template-path-numbering-contract.md` | same | Add Task link; label unchecked instructions historical | done / retain |
| `2026-07-05-workspace-contract-governance-normalization.md` | same | Add Task link; label unchecked instructions historical | done / retain |
| `2026-07-05-workspace-engineering-implementation-audit-pack.md` | same | Add Task link; label unchecked instructions historical | done / retain |
| `2026-07-06-control-cloud-doc-normalization.md` | same | Verify reciprocal link | done / retain |
| `2026-07-06-observability-and-network-review-agents.md` | same | Add explicit clickable Task link | done / retain |
| `2026-07-06-sdlc-lifecycle-contract.md` | same | Add Spec/Task links; label unchecked instructions historical | done / retain |
| `2026-07-06-stage03-04-repo-static-gap-closure.md` | same | Label unchecked instructions historical | done / retain |
| `2026-07-07-workspace-engineering-research-pack-refresh.md` | same | Add Spec/Task links | done / retain |
| `2026-07-10-current-research-pack-fact-first-hardening.md` | same | Add Task link; label unchecked instructions historical | done / retain |

The relocated 2026-07-11 audit-integration Plan and the new RMD-004 Plan are
new records and will be added after this baseline ledger, each with a
same-basename Task and reciprocal links.

### Logical Commit Boundaries

1. `docs(audits): normalize audit pack information architecture`
   - parent/pack indexes and currentness;
   - relocation of the completed audit execution Plan;
   - compact completion Task and reciprocal links.
2. `docs(specs): reconcile lifecycle and current ownership`
   - all Spec states, successor/current-owner lineage, missing links, and index.
3. `docs(plans): reconcile execution evidence links`
   - all Plan/Task link repairs, historical-instruction labels, and Plan index.
4. `docs(governance): define roster currentness contract`
   - Spec 025, its Plan and Task scaffold, and related lineage links.
5. `fix(governance): enforce canonical roster and owner pointers`
   - Stage 00 currentness corrections and deterministic validation fixtures.
6. `docs(governance): close roster currentness evidence`
   - Task evidence, lifecycle closure, indexes, memory, and final validation.

Commit boundaries may be split further if a review discovers an independently
revertible unit. They must not be collapsed into one repository-wide commit.

### Subagent-Driven Execution

After the written design and implementation plan are approved, execution will
use fresh subagents per logical task. Each task receives:

1. an implementation subagent;
2. a specification-compliance review;
3. a quality review; and
4. fixes and re-review before the task is considered complete.

Subagents share the worktree, so only one implementation subagent may edit at
a time unless their file ownership is explicitly disjoint. The primary agent
retains responsibility for final integration, validation, and branch finishing.

## Success Criteria & Verification Plan

- The audit index has one unambiguous Current pointer and all dated packs are
  classified.
- The completed Stage 90 execution plan is represented as a done Stage 04
  Plan with Task evidence.
- Every Spec and Plan has evidence-aligned lifecycle and explicit lineage.
- No completed Plan is archived solely for being old or done.
- Spec 025 is the only active RMD-004 owner during implementation.
- Stage 00 reports ten shared role stems and thirty provider adapters without
  stale eight-role currentness prose.
- Deterministic positive and negative validation passes.
- `git diff --check`, repository quality gates, and
  `pre-commit run --all-files` pass or an environment limitation is explicitly
  recorded.
- Work is committed in logical units and is ready for an explicitly approved
  local merge to `main`.

## Traceability

- [Current Audit Pack](../../90.references/audits/2026-07-11-weia/README.md)
- [Remediation Roadmap](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
- [Spec Stage](../README.md)
- [Execution Plan](../../04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md)
- [Execution Task](../../04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md)
- [Plan Stage](../../04.execution/plans/README.md)
- [Task Stage](../../04.execution/tasks/README.md)
- [Agent Governance Normalization Spec](../015-agent-governance-contract-normalization/spec.md)
- [Workspace Harness Gap Spec](../006-workspace-harness-gap-analysis/spec.md)
- [Observability and Network Agents Spec](../024-observability-and-network-review-agents/spec.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Document Stage Routing](../../00.agent-governance/rules/document-stage-routing.md)
- [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- [Archive Index](../../98.archive/README.md)
### Related inputs

- **PRD**: No product PRD is required. The approved requirement is repository
  governance and lifecycle normalization based on the Current audit findings.
- **ARD**: No infrastructure ARD is changed. The existing Stage 00 canonical
  core and provider-adapter architecture remains in force.
- **Related ADRs**: No new architectural decision is needed unless execution
  discovers that canonical ownership cannot be represented by the existing
  Stage 00/03/04/99 boundaries.
- **Audit input**: RMD-004 and GOV-002 in the 2026-07-11 Current audit pack.
