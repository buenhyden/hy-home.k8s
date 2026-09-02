---
title: 'Workspace Governance Audit and Remediation Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-09
artifact_id: "SPEC-0055"
---

# Workspace Governance Audit and Remediation Technical Specification (Spec)

## Overview

This specification defines a new current-state workspace governance audit pack
at `docs/90.references/audits/2026-08-09-wgia/`. The work inventories the
repository's purpose, roles, operating contracts, spec-driven development,
SDLC, documentation, CI/CD, GitHub Actions, QA, formatting, linting, syntax and
test controls, validation and verification semantics, templates, fixtures,
scripts, integration guides, LLM-WIKI, security, memory, harness and loop
engineering, integrated AI-agent orchestration, and every current AI-agent
role. It also identifies blockers, conflicting authorities, dormant controls,
Legacy or Deprecated surfaces, and one-shot documents or scripts.

The audit is not complete when it only reports drift. Within the approved
repository-static scope, findings that conflict with the workspace purpose are
reconciled in their canonical owners, mutable cross-links are migrated, and
proven Legacy, Deprecated, duplicate, or one-shot files are removed after a
fail-closed disposition gate. The resulting pack becomes the sole Current
audit pointer. Earlier audit packs remain immutable, source-commit-bounded
historical evidence rather than active policy or compatibility owners.

The primary consumers are developers, operators, documentation writers,
governance stewards, quality and security reviewers, and AI agents.

Direct human approval on 2026-08-09 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle. The
same approval authorizes this design and its reciprocal
[Plan](plan.md)
and
[Task](README.md#task-records).
The active direct-approval standalone execution relation is governed by
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md);
No separate PRD or AD program authority is asserted.

## Strategic Boundaries & Non-goals

### Authorized scope

- Freeze the observation identity to an exact tracked Git commit and inspect
  current repository content through bounded, read-only inventory commands.
- Create one ten-file audit pack with a pack index, eight focused category
  reports, and one integrated remediation roadmap.
- Map all 30 requested scopes to exactly one primary file and heading, with
  current canonical-owner evidence and explicit evidence depth.
- Compare intended purpose and active contracts against current governance,
  provider, documentation, CI, QA, script, fixture, template, agent, memory,
  security, and knowledge-routing surfaces.
- Correct conflicting or duplicated current rules in their canonical Stage
  00, Stage 03-05, Stage 90, Stage 99, `.github`, `scripts`, `tests`, or
  provider-adapter owners when the approved contract is unambiguous.
- Migrate mutable links, indexes, Reference Information Architecture (RIA)
  projections, fixtures, tests, and generated lookup outputs required to make
  the new audit pack the sole Current audit owner.
- Remove tracked Legacy, Deprecated, duplicate, or one-shot artifacts only
  after exact provenance, zero-consumer, replacement-owner, and post-delete
  validation evidence exists.
- Use logical-unit commits, task-scoped independent review, a whole-branch
  review, and repository-static verification before branch finishing.

### Protected surfaces and non-goals

- Existing `docs/98.archive/**` payloads and digests are immutable.
- The six existing audit packs remain historical evidence. Their observation
  bodies are not rewritten to look current, and they are not deleted merely
  because their findings have successors.
- The audit pack is descriptive Stage 90 material. It never becomes the active
  owner for policy, permissions, document routes, lifecycle, templates,
  workflows, scripts, agents, memory, or security controls.
- A file is not Legacy, Deprecated, or one-shot merely because its name,
  fixture, validator, or evidence text contains one of those words.
- No approved PRD, AD, ADR, Spec, or operations policy is silently overturned.
  A genuine decision conflict becomes an explicit blocker and human escalation.
- No live Kubernetes, Argo CD, Vault, ESO, cloud, provider-runtime, hosted-CI,
  remote, credential-bearing, secret-reading, push, merge, or publication
  action is authorized by this specification.
- Repository-static PASS never establishes provider discovery, authenticated
  execution, effective permissions, hosted workflow behavior, or live platform
  readiness.
- No compatibility README, redirect, copied policy, generated-output edit, or
  tracked temporary research artifact is introduced to make cutover pass.

## Contracts

### C-WGA-001 — one current audit owner

`docs/90.references/audits/2026-08-09-wgia/` becomes the sole Current audit
pack. The collection README, RIA contract, producer, schema, fixtures, tests,
and current-owner checks agree on that identity. The prior Current pack becomes
a source-commit-pinned historical snapshot without body rewriting.

### C-WGA-002 — exact requested-scope ownership

The new pack README contains exactly 30 sequential request rows. Every row has
one primary report-and-heading owner, at least one current workspace evidence
surface, a verdict, and an evidence-depth boundary. Secondary reports link to
the primary owner instead of duplicating its complete analysis.

### C-WGA-003 — canonical authority preservation

The audit states what a current owner does; it does not copy the current rule
as a competing authority. Exact routes and document forms remain owned by the
Stage 99 registry, agent execution policy remains in Stage 00, SDLC behavior
remains in its Stage 01-05 owner chain, and machine contracts remain in their
declared JSON, schema, producer, and validator owners.

### C-WGA-004 — evidence and verdict integrity

Each material finding identifies its expected state, observed state, exact
evidence, evidence depth, verdict, impact, disposition, remediation owner,
verification command, uncertainty, and blocker state. An unavailable evidence
lane is `DEFER`; absence of evidence is never promoted to success.

### C-WGA-005 — validation and verification separation

`Validation` means that inputs, syntax, structure, schemas, routes, and
contracts are well-formed and admissible. `Verification` means that the
implemented result satisfies the approved Spec, requirements, and acceptance
criteria. QA documentation and automation preserve both terms and name the
evidence that supports each result.

### C-WGA-006 — purpose-conflict remediation

When a current rule or system conflicts with the repository purpose, the work
updates the canonical owner and all affected projections in one reviewed unit.
Historical findings retain their dated truth. Ambiguous policy or architecture
choices are not guessed; they block that remediation until an owner decision.

### C-WGA-007 — deletion by proof

Removal requires an exact tracked path and source commit, zero current
consumers and rendered links, a surviving canonical replacement, a historical
evidence route, and green focused plus full post-delete checks. Failure of any
condition yields `DEFER`, not deletion.

### C-WGA-008 — atomic current-pointer cutover

Audit README navigation, document profiles, RIA baselines and transitions,
LLM-WIKI or other generated lookup outputs, mutable links, fixtures, and tests
change atomically. No interval may expose two Current audits or a Current audit
whose tracked members and baseline identity disagree.

### C-WGA-009 — blocker visibility

Every blocker records its cause, impact, release condition, owner, affected
requirements, and evidence depth. A blocked row cannot be reported as aligned,
resolved, verified, or validated.

### C-WGA-010 — logical history and cleanup

Design, activation, pack foundation, each topic group, canonical remediation,
machine-contract cutover, approved deletions, and closure use distinct logical
commits. One-off work products remain only in the ignored SDD workspace and
are deleted after final review.

## Core Design

### Audit pack components

| File | Primary responsibility |
| --- | --- |
| `README.md` | Overview, observation identity, reading order, evidence vocabulary, exact 30-row request coverage, report index, and Current-pack boundary. |
| `workspace-purpose-governance-and-operating-contracts.md` | Repository purpose, roles, governance hierarchy, operating contract, approval boundaries, provider shims, overview consistency, and canonical-owner conflicts. |
| `spec-driven-sdlc-documentation-and-templates.md` | Spec-driven flow, SDLC, document types, templates, document contracts, README contracts, authoring routes, integration guides, and documentation drift. |
| `ci-cd-github-actions-qa-and-validation.md` | CI/CD, GitHub Actions, QA, formatting, linting, syntax, tests, Validation, Verification, workflow security, lane selection, result evidence, and dormant controls. |
| `harness-loop-fixtures-scripts-and-blockers.md` | Harness and loop state machines, operating scripts, fixtures, failure recovery, retry/stop behavior, blocker model, and script-to-validator ownership. |
| `llm-wiki-memory-and-knowledge-management.md` | LLM-WIKI, deterministic knowledge routing, short-term, long-term, domain-scoped, and provider-local auxiliary memory with freshness, promotion, retention, and conflict rules. |
| `ai-agents-integrated-and-role-specific-agents.md` | AI-agent system, supervisor/integrated-agent orchestration, current roster, every role's responsibility, adapter coverage, model routing, handoff, admission, evaluation, and runtime evidence limits. |
| `security-and-approval-boundaries.md` | Repository, supply-chain, workflow, agent, secret, GitOps, infrastructure, permission, destructive-action, and live/remote approval controls. |
| `legacy-deprecated-and-one-shot-disposition-ledger.md` | Candidate inventory, source commits, consumers, replacement owners, Keep/Integrate/Correct/Delete/DEFER decisions, deletion evidence, and historical routing. |
| `remediation-and-integration-roadmap.md` | Cross-report finding register, dependencies, priorities, target state, canonical implementation owners, cutover sequence, rollback, and residual DEFER backlog. |

### Processing flow

```text
exact main SHA + tracked inventory + canonical owners
                         |
                         v
     request coverage + evidence-depth inventory
                         |
                         v
       category audits + conflict/duplicate analysis
                         |
                         v
       disposition ledger + integrated remediation map
                         |
                         v
  canonical-owner fixes + mutable consumer migration
                         |
                         v
       zero-consumer deletion gate + dry-run checks
                         |
                         v
  RIA Current cutover + post-cutover re-audit + full QA
```

### Audit phases

1. **Foundation**: freeze source identity, enumerate tracked surfaces, create the
   exact pack structure and 30-row coverage matrix.
2. **Governance and documentation**: audit purpose, authority, operating
   contracts, spec-driven SDLC, documentation, templates, README rules, and
   integration guides.
3. **Delivery and quality**: audit CI/CD, GitHub Actions, formatting, linting,
   syntax, tests, validation, verification, fixtures, scripts, and blockers.
4. **Agent and knowledge systems**: audit harness, loop, LLM-WIKI, memory,
   integrated orchestration, individual roles, providers, model routing,
   evaluation, and handoff.
5. **Security and cleanup**: audit approval and security boundaries, classify
   Legacy/Deprecated/one-shot candidates, and remediate proven conflicts.
6. **Cutover and closure**: update machine projections and current navigation,
   perform approved deletions, re-audit the target tree, and close lifecycle
   only after independent review and full gates pass.

### Evidence-depth vocabulary

| Depth | Meaning |
| --- | --- |
| `repository-static` | Tracked content, Git identity, deterministic local parsing, rendering, or repository tests. |
| `hosted` | GitHub-hosted workflow, ruleset, artifact, environment, or remote service evidence. |
| `provider-runtime` | Authenticated provider discovery, configuration consumption, model resolution, permission, hook, or agent execution evidence. |
| `live` | Cluster, GitOps reconciliation, Vault/ESO, network, credential, cloud, deployment, or operator rehearsal evidence. |

### Finding verdict vocabulary

Every finding uses exactly one of:

- `Aligned`: the current owner and directly supporting evidence satisfy the
  expected repository-static contract;
- `Partial`: only a bounded subset is implemented or evidenced;
- `Gap`: required local behavior or ownership is absent;
- `Conflict`: two current claims disagree or a current claim contradicts the
  workspace purpose or approved authority;
- `Legacy`: a superseded compatibility surface remains but has a current
  replacement;
- `Deprecated`: an active owner explicitly rejects the current surface or value;
- `One-shot candidate`: an artifact may be temporary, but deletion proof is not
  yet complete; or
- `DEFER`: the evidence or decision belongs to an unavailable, unapproved, or
  explicitly later lane.

## Data Modeling & Storage Strategy

### Request coverage record

The README owns 30 rows with the following columns:

| Field | Meaning |
| --- | --- |
| Request ID | Sequential `REQ-WGA-001` through `REQ-WGA-030`. |
| Requested scope | One original user-requested category. |
| Primary owner | Exactly one report and heading. |
| Workspace evidence | At least one canonical file, contract, script, workflow, fixture, or generated owner. |
| Evidence depth | The strongest observed depth, never an inferred one. |
| Verdict | One closed vocabulary value. |

### Finding record

Each material audit row exposes this conceptual shape:

```typescript
interface GovernanceAuditFinding {
  id: string;
  requestIds: string[];
  scope: string;
  expectedState: string;
  observedState: string;
  evidence: Array<{ path: string; anchorOrSelector: string }>;
  evidenceDepth: "repository-static" | "hosted" | "provider-runtime" | "live";
  verdict:
    | "Aligned"
    | "Partial"
    | "Gap"
    | "Conflict"
    | "Legacy"
    | "Deprecated"
    | "One-shot candidate"
    | "DEFER";
  impact: string;
  disposition: "Keep" | "Integrate" | "Correct" | "Delete" | "DEFER";
  canonicalOwner: string;
  verification: string[];
  blocker: null | { cause: string; releaseCondition: string; owner: string };
}
```

Markdown remains the authored storage format. Machine-owned identities and
transitions stay in existing JSON, schema, producer, and validator owners.
A new machine contract is introduced only if the implementation plan proves
that existing RIA, document-profile, or validation-surface interfaces cannot
close an invariant without duplicated parsing.

### Cleanup disposition record

| Field | Meaning |
| --- | --- |
| Candidate path | Exact tracked path. |
| Source commit | Full Git commit used for recovery and historical interpretation. |
| Candidate class | Legacy, Deprecated, duplicate, or one-shot. |
| Current consumers | Exact rendered-link, contract, import, workflow, or invocation inventory. |
| Replacement owner | Surviving canonical owner and heading or interface. |
| Decision | Keep, Integrate, Correct, Delete, or DEFER. |
| Evidence | Commands, outputs, source rows, and review references supporting the decision. |
| Post-delete gates | Focused and aggregate commands that must remain green. |

`Delete` is admissible only when current consumers are zero after migration and
the replacement owner is tracked, unique, and valid. The ledger retains the
row after deletion so provenance and the reason remain reviewable.

### Current audit transition

The current audit transition is atomic:

1. Record the exact prior Current baseline and its source commit.
2. Preserve the prior pack bytes as historical snapshot evidence.
3. Register the new pack paths and expected profiles.
4. Update RIA current-pack identities, allowed transition, generator output,
   fixtures, tests, and collection indexes in one unit.
5. Reject two Current rows, missing members, baseline drift, or a transition
   that cannot resolve the prior source commit.

## Interfaces & Data Structures

### Canonical-owner lookup interface

Each audit report distinguishes:

- **policy owner**: the file that is allowed to define the rule;
- **machine owner**: the schema, registry, contract, or producer that enforces
  exact values;
- **human index**: the README or guide that routes readers to the owner;
- **evidence producer**: the script, test, workflow, fixture, or command that
  reports a result; and
- **historical snapshot**: dated evidence that cannot redefine current state.

An artifact may hold more than one role only when the current contract says so.
The audit flags prose that duplicates exact route tables, active policy copied
into Stage 90, generated output edited by hand, or tests treated as the owner of
their production contract.

### Agent-system interface

The agent audit separates:

- the integrated supervisor/orchestrator contract;
- shared harness, loop, checkpoint, memory, approval, validation, and handoff
  behavior;
- the exact current role inventory and each role's responsibility, inputs,
  outputs, prohibited actions, stop conditions, and downstream handoff;
- provider-specific tracked adapters and native/runtime discovery boundaries;
- model routing, fitness, evaluation, admission, promotion, and rollback; and
- repository-static configuration from provider-runtime execution evidence.

Counts are derived from the current machine owner at the observation commit;
they are not copied from an older audit as present-tense truth.

### QA lane interface

Every QA lane names:

- trigger and affected surface;
- exact command and tool identity;
- formatting, linting, syntax, unit, integration, contract, security, or policy
  responsibility;
- Validation or Verification result class;
- local, staged, all-files, CI, hosted, provider, or live evidence depth;
- fallback and SKIP semantics;
- artifact or handoff record; and
- owner of remediation when the lane fails.

Dormant configuration, including a formatter configuration without any current
consumer, must be resolved through evidence: either admit one scoped consumer
with overlap and rollback proof or remove the dormant configuration and its
claims. Presence alone is not coverage.

## Edge Cases & Error Handling

- **More than one Current audit**: reject the cutover; do not choose by date.
- **New pack member or request row is missing or duplicated**: block activation
  until exact shape and ownership are restored.
- **Canonical owner is ambiguous**: record `Conflict` and escalate; do not
  duplicate the rule into the audit pack.
- **Historical audit contradicts current state**: retain the dated statement
  and route current readers to the new owner; never rewrite the old observation.
- **A candidate name says legacy but it is an active validator or contract**:
  classify by consumers and authority, not by filename, and retain it.
- **A candidate has no current rendered link but is invoked by CI, a script,
  import, schema reference, fixture, or machine contract**: it is not
  zero-consumer and cannot be deleted.
- **A one-shot artifact contains unique evidence**: integrate the evidence into
  a durable owner before deletion or mark the candidate `DEFER`.
- **A finding needs live or credential-bearing proof**: retain `DEFER` and name
  the approved future task or runbook; do not run the action during this work.
- **Validation and Verification disagree**: report both. A well-formed artifact
  can still fail its requirement, and a behavior claim without valid input or
  contract evidence cannot pass.
- **Generated LLM-WIKI or index drift**: change its canonical sources, rerun the
  generator, and verify with `--check`; never hand-edit generated output.
- **Deletion makes a snapshot link fail**: use source-commit-relative historical
  resolution only when the current RIA contract proves the exact bytes and
  disposition; otherwise restore the file and stop.
- **Post-remediation audit still reports the same conflict**: do not close the
  work item; fix the canonical owner or record a real unresolved blocker.
- **Stage 98 appears in the branch diff**: stop and revert that change.
- **A task-created temporary file remains tracked**: integrate durable content
  into its owner or delete the temporary file before closure.

## Failure Modes & Fallback / Human Escalation

| Failure mode | Safe fallback | Human escalation condition |
| --- | --- | --- |
| Existing approved documents mandate incompatible owners or outcomes | Preserve both unchanged, mark `Conflict`, and stop that remediation. | The conflict requires changing a PRD, AD, accepted ADR, active Spec, or operations policy. |
| RIA cannot represent the new Current transition without weakening snapshot integrity | Keep the prior Current pointer and produce the new pack as non-current draft evidence. | A schema or lifecycle decision is required rather than a bounded projection extension. |
| Legacy/Deprecated/one-shot candidate lacks complete consumer proof | Retain the file with `DEFER` and record the missing evidence. | Deletion is required for another load-bearing task or current security property. |
| Dormant formatter or QA control has unsafe overlap | Retain it as dormant with an explicit non-coverage statement until a decision is approved. | Activation or removal changes a protected workflow or broad authored corpus. |
| Provider, hosted, remote, or live evidence is unavailable | Preserve the repository-static result and `DEFER` the deeper lane. | The deeper evidence is required to decide a current destructive or permission change. |
| Canonical remediation causes focused validation failure | Revert the uncommitted logical unit and repair the owner or its fixtures. | Passing would require disabling, bypassing, or weakening the failed gate. |
| Post-delete validation fails | Restore the deletion unit before commit. | The replacement owner or historical resolution remains ambiguous. |
| Task review finds a plan-mandated defect | Enter the bounded SDD fix loop and retain all review evidence. | A load-bearing finding remains after the review cap or conflicts with this Spec. |

No push, merge, worktree removal, remote publication, or destructive external
action occurs until `finishing-a-development-branch` presents the human-owned
integration choice.

## Verification Commands

Baseline, focused, and terminal repository-static validation includes:

```bash
git diff --check
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-github-actions-security.py --root .
python3 scripts/validate-ci-python-contract.py --root .
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-roster-currentness.py --root .
python3 scripts/archive_validation.py
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
```

The implementation plan must verify each command's current CLI before treating
this list as executable evidence. A missing optional external tool may use only
the repository's documented fallback and must remain `SKIP` or bounded fallback
evidence rather than being reported as native-tool PASS.

Focused tests must cover at least:

- exact new pack membership and exact 30-row coverage;
- single-Current selection and old-Current-to-historical transition;
- baseline source-commit and protected historical-byte drift;
- missing, duplicate, and unknown report members;
- duplicate canonical owners and broken current links;
- deletion disposition missing source commit, consumer inventory, replacement,
  reason, or post-delete evidence;
- retained active files whose names contain Legacy or Deprecated vocabulary;
- Validation/Verification and evidence-depth vocabulary closure;
- LLM-WIKI generated-source drift;
- dormant formatting configuration disposition; and
- no Stage 98 change and no tracked temporary artifact.

## Success Criteria & Verification Plan

| Criterion | Success condition | Required evidence |
| --- | --- | --- |
| VAL-WGA-001 | The successor audit pack has exactly ten declared files and its README has exactly 30 sequential, unique request rows with one owner each. | Tracked-file count, pack parser, coverage audit, Markdown profiles, and strict links. |
| VAL-WGA-002 | Every material finding names expected/observed state, exact evidence, depth, verdict, impact, disposition, owner, verification, uncertainty, and blocker state. | Report schema review, deterministic table audit, and independent content review. |
| VAL-WGA-003 | Workspace purpose, roles, governance hierarchy, operating contracts, provider shims, and canonical owner boundaries are current and non-duplicative. | Stage 00/root owner inventory, conflict matrix, strict registry/links, and governance review. |
| VAL-WGA-004 | Spec-driven SDLC, document families, templates, document contracts, README rules, and integration guides are audited against current Stage 99 machine ownership. | Registry/template/source parity, Markdown profiles, lifecycle checks, and report evidence. |
| VAL-WGA-005 | CI/CD, GitHub Actions, formatting, linting, syntax, tests, fixtures, Validation, Verification, and result evidence are completely inventoried with dormant controls resolved or deferred. | Workflow/QA contract validators, affected-surface checks, fixture inventory, and report evidence. |
| VAL-WGA-006 | Harness, loop, scripts, retry/recovery/stop, blockers, checkpoint, handoff, and provider-boundary controls are audited without static-to-runtime inference. | Harness/loop/checkpoint/provider validators, script inventory, and evidence-depth review. |
| VAL-WGA-007 | LLM-WIKI and all four memory classes have current owners, lifecycle, freshness, conflict, redaction, retention, and generated-index boundaries. | LLM-WIKI generator check, memory contract evidence, links, and report review. |
| VAL-WGA-008 | Integrated orchestration and every current AI-agent role have unique responsibility, inputs, outputs, prohibited actions, stop/handoff, adapter, model, evaluation, and evidence-boundary coverage. | Current machine roster projection, harness semantics, model-fitness/admission checks, exact role matrix, and review. |
| VAL-WGA-009 | Security and approval boundaries cover repository, workflow, supply chain, agent, secret, GitOps, infrastructure, destructive, remote, and live surfaces without exposing sensitive values. | Security validators, secret/policy/static-infrastructure gates, approval matrix audit, and security review. |
| VAL-WGA-010 | Every Legacy, Deprecated, duplicate, or one-shot candidate has a full provenance and consumer disposition; only proof-complete Delete rows are removed. | Exact candidate ledger, zero-consumer scans, replacement-owner checks, post-delete clone or staged validation, and Git history. |
| VAL-WGA-011 | The new audit is the sole Current pointer, the prior Current pack is protected historical evidence, all mutable links and machine projections are migrated, and Stage 98 is unchanged. | RIA tests/production, collection index, strict links, generated indexes, branch diff, and archive validation. |
| VAL-WGA-012 | Purpose-conflicting current owners are corrected or explicitly blocked, the target tree is re-audited, all required gates pass, reviews approve, and logical commits preserve rollback. | As-Is/Target comparison, blocker closure, full repository gate, harness, task reviews, whole-branch review, and commit ledger. |

Success is repository-static unless a row carries separately authorized evidence
at a deeper level. Hosted, provider-runtime, remote, credential-bearing, and
live results remain `DEFER` unless independently observed and approved.

## Traceability

| Requested scope | Requirement | Primary pack owner | Spec criterion |
| --- | --- | --- | --- |
| Purpose | REQ-WGA-001 | `workspace-purpose-governance-and-operating-contracts.md` | VAL-WGA-003 |
| Roles | REQ-WGA-002 | `workspace-purpose-governance-and-operating-contracts.md` | VAL-WGA-003 |
| CI/CD | REQ-WGA-003 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| GitHub Actions | REQ-WGA-004 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Spec-driven development | REQ-WGA-005 | `spec-driven-sdlc-documentation-and-templates.md` | VAL-WGA-004 |
| Harness engineering | REQ-WGA-006 | `harness-loop-fixtures-scripts-and-blockers.md` | VAL-WGA-006 |
| Loop engineering | REQ-WGA-007 | `harness-loop-fixtures-scripts-and-blockers.md` | VAL-WGA-006 |
| QA | REQ-WGA-008 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Formatting | REQ-WGA-009 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Linting | REQ-WGA-010 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Overview | REQ-WGA-011 | `README.md` | VAL-WGA-001 |
| Operating contracts | REQ-WGA-012 | `workspace-purpose-governance-and-operating-contracts.md` | VAL-WGA-003 |
| Fixtures | REQ-WGA-013 | `harness-loop-fixtures-scripts-and-blockers.md` | VAL-WGA-005, VAL-WGA-006 |
| Blockers | REQ-WGA-014 | `harness-loop-fixtures-scripts-and-blockers.md` | VAL-WGA-006, VAL-WGA-012 |
| General checks | REQ-WGA-015 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Templates | REQ-WGA-016 | `spec-driven-sdlc-documentation-and-templates.md` | VAL-WGA-004 |
| Scripts | REQ-WGA-017 | `harness-loop-fixtures-scripts-and-blockers.md` | VAL-WGA-006 |
| Integration guides | REQ-WGA-018 | `spec-driven-sdlc-documentation-and-templates.md` | VAL-WGA-004 |
| Documents and documentation | REQ-WGA-019 | `spec-driven-sdlc-documentation-and-templates.md` | VAL-WGA-004 |
| Verification | REQ-WGA-020 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| Validation | REQ-WGA-021 | `ci-cd-github-actions-qa-and-validation.md` | VAL-WGA-005 |
| LLM-WIKI | REQ-WGA-022 | `llm-wiki-memory-and-knowledge-management.md` | VAL-WGA-007 |
| SDLC | REQ-WGA-023 | `spec-driven-sdlc-documentation-and-templates.md` | VAL-WGA-004 |
| Security | REQ-WGA-024 | `security-and-approval-boundaries.md` | VAL-WGA-009 |
| Legacy and Deprecated documents | REQ-WGA-025 | `legacy-deprecated-and-one-shot-disposition-ledger.md` | VAL-WGA-010 |
| One-shot documents and scripts | REQ-WGA-026 | `legacy-deprecated-and-one-shot-disposition-ledger.md` | VAL-WGA-010 |
| Memory tiers and management | REQ-WGA-027 | `llm-wiki-memory-and-knowledge-management.md` | VAL-WGA-007 |
| AI Agents | REQ-WGA-028 | `ai-agents-integrated-and-role-specific-agents.md` | VAL-WGA-008 |
| Integrated AI Agent | REQ-WGA-029 | `ai-agents-integrated-and-role-specific-agents.md` | VAL-WGA-008 |
| Individual AI Agents | REQ-WGA-030 | `ai-agents-integrated-and-role-specific-agents.md` | VAL-WGA-008 |

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — direct human approval and Spec approval on 2026-08-09 authorize this standalone design and active execution; no separate PRD/AD program owner is asserted | VAL-WGA-001 | Exact ten-file pack and 30-row coverage audit. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-002 | Finding-field completeness audit and independent content review. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-003 | Purpose, authority, operating-contract, and canonical-owner evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-004 | Registry, template/source, Markdown profile, and SDLC evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-005 | CI, GitHub Actions, QA, fixture, Validation, and Verification evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-006 | Harness, loop, checkpoint, script, blocker, and provider-boundary evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-007 | LLM-WIKI generator and memory-lifecycle evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-008 | Integrated-agent and exact role/adaptor/model evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-009 | Security, secret, policy, infrastructure, and approval-boundary evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-010 | Candidate disposition, zero-consumer, replacement, and post-delete evidence. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-011 | RIA Current transition, mutable links, generated indexes, and archive immutability. |
| N/A — the same direct approval governs this standalone design | VAL-WGA-012 | Target re-audit, blocker closure, full gates, reviews, and logical history. |
