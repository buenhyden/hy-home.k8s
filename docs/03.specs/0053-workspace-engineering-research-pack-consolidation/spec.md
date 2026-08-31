---
title: 'Workspace Engineering Research Pack Consolidation Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-08-09
artifact_id: "SPEC-0053"
---

# Workspace Engineering Research Pack Consolidation Technical Specification (Spec)

## Overview

This specification defines a new dated workspace engineering research pack at
`docs/90.references/research/0001-workspace-engineering/`. The pack re-researches the full
requested scope against current official or primary external sources and the
current repository, integrates the valid findings and provenance from all 25
files in the `2026-07-04-wer`, `2026-07-07-wer`, and `2026-08-07-wer` packs,
rewrites mutable current cross-links, and removes all three predecessor pack
directories after fail-closed coverage and reference gates pass.

The primary consumers are developers, operators, technical writers, governance
stewards, quality engineers, security engineers, and AI agents working in the
`hy-home.k8s` repository. The pack is descriptive Stage 90 reference material;
it does not become an active policy, provider permission, deployment, or live
runtime owner.

This specification is a successor to completed
[Spec 017](../0017-workspace-engineering-research-pack/spec.md). It does not
reopen or rewrite Spec 017's terminal evidence. It also records a deliberate
conflict with the active [Spec 052](../0052-document-taxonomy-consolidation/spec.md)
archive route: the human-approved replacement removes the three old live packs
without creating replacement Stage 98 records, while preserving provenance in
Git history and the new migration ledger. The affected mutable requirements,
architecture, plans, contracts, validators, and fixtures must be reconciled
before deletion.

Direct human approval on 2026-08-08 authorizes this standalone execution relation.
No separate PRD or AD is required or part of this standalone lifecycle. The
typed relationship is governed by
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md).

## Strategic Boundaries & Non-goals

### Authorized scope

- Read-only external research using official provider, product, standards,
  and upstream project sources checked on 2026-08-08.
- Current repository inspection across governance, provider adapters, hooks,
  contracts, templates, scripts, tests, workflows, GitOps, infrastructure,
  policy, and documentation owners.
- A new pack index plus twelve focused Stage 90 references.
- A lossless file- and material-section disposition ledger for all 25 old pack
  files.
- Mutable current cross-link, research index, audit note, contract, validator,
  and fixture changes required for the cutover.
- Removal of the three predecessor pack directories after all pre-deletion
  gates pass.
- Logical-unit commits, task-scoped reviews, a whole-branch review, and local
  repository-static validation.

### Protected surfaces and non-goals

- Existing `docs/98.archive/**` records are immutable. Their sealed historical
  links continue to resolve against each record's `source_commit` and are not
  rewritten.
- This work does not rewrite Git history. Deleted live files remain recoverable
  from their source commits.
- This work does not change runtime agent roles, provider model assignments,
  hook permissions, CI deployment behavior, GitOps desired state, or platform
  manifests merely because research identifies a gap. Recommendations route to
  canonical owners as follow-up work.
- No live Kubernetes, Argo CD, Vault, ESO, cloud, provider-runtime, hosted-CI,
  remote, credential-bearing, secret-reading, push, merge, or publication
  action is authorized by this specification.
- No compatibility README, redirect file, duplicated research reference,
  tracked migration script, or scratch artifact remains at an old pack path.

## Contracts

### C-WER-001 — single live pack owner

`docs/90.references/research/0001-workspace-engineering/` becomes the sole live research
pack owner for the requested topics. The three predecessor directories do not
exist after cutover.

### C-WER-002 — exact scope ownership

The new pack README maps each requested topic to exactly one primary reference
and at least one current workspace evidence surface. Secondary discussion uses
cross-links rather than copying the primary owner's complete analysis.

### C-WER-003 — claim provenance

Every material statement is recognizable as a workspace fact, external fact,
dated predecessor fact, analysis, or recommendation. External facts carry an
exact URL, checked date, and refresh trigger. Analysis names its inputs, and
recommendations name a canonical follow-up owner.

### C-WER-004 — evidence-depth separation

Repository-static configuration and validation never prove provider discovery,
authentication, model resolution, permissions, event delivery, hosted CI,
remote execution, or live platform readiness. Those lanes remain
`Unverified` or `Deferred` unless evidence at the required depth exists.

### C-WER-005 — lossless disposition before deletion

Every predecessor file and every material section whose owner differs from its
file-level owner has a reviewed disposition. An omission is valid only when it
is supported as stale or duplicate; absence from the new pack is not evidence
of intentional disposition.

### C-WER-006 — mutable-reference closure

Every mutable tracked reference to a predecessor path is updated to the new
owner or annotated as a dated observation with a current lookup link. Existing
Stage 98 payload references are excluded because their historical resolution
is source-commit-relative.

### C-WER-007 — control-preserving contract migration

Snapshot guards, contracts, validators, and fixtures that encode predecessor
paths are changed together with focused tests. The migration preserves
provenance, deterministic routing, fail-closed validation, and negative
coverage; it does not disable a lane to make deletion pass.

### C-WER-008 — clean cutover

Deletion occurs only after the new pack, coverage ledger, source ledger,
mutable links, and contract projections validate. No tracked one-off,
temporary, duplicate, redirect, or compatibility artifact remains after the
cutover.

## Core Design

### Component ownership

| Artifact | Primary scope and responsibility |
| --- | --- |
| `README.md` | Pack boundary, source priority, reading order, evidence classes, and requirement-to-owner coverage matrix. |
| `workspace-governance-and-common-agent-environment.md` | Workspace purpose, operating contract, shared Claude/Codex environment, common rules, governance, templates, scripts, and integration routes. |
| `harness-and-loop-engineering.md` | Harness elements; Observe/Plan/Act/Verify/Learn loop; evaluation, recovery, termination, memory, and workspace application requirements. |
| `provider-implementation-status.md` | Claude and Codex upstream surfaces, local adapters, hooks, permissions, subagents, implementation status, parity limits, and common-system options. |
| `spec-driven-sdlc-and-document-contracts.md` | Spec-driven development, SDLC governance, and PRD, AD, ADR, guide, incident, postmortem, policy, release, and runbook roles and rules. |
| `documentation-architecture-and-diataxis.md` | Diataxis tutorial, how-to, reference, and explanation modes; workspace mapping; authoring rules; implementation gaps. |
| `llm-wiki-and-knowledge-routing.md` | LLM-WIKI structure, deterministic indexes, JIT retrieval, authority routing, freshness, and drift controls. |
| `kubernetes-infrastructure-and-security.md` | Kubernetes, infrastructure, GitOps, RBAC, NetworkPolicy, secrets, policy-as-code, supply-chain, and security boundaries. |
| `ci-cd-github-actions-and-qa.md` | CI/CD, GitHub Actions, formatting, linting, testing, syntax validation, workflow security, promotion, rollback, and evidence lanes. |
| `ai-agents-and-agency-agents.md` | AI-agent system design, pinned `msitarzewski/agency-agents` evidence, roster comparison, Adopt/Adapt/Skip decisions, and admission rules. |
| `agent-model-routing-and-configuration.md` | Task-characteristic model selection, product-surface separation, reasoning controls, evaluation, fallback, cost/latency, and promotion. |
| `agent-memory-tiers-and-management.md` | Working short-term, durable long-term, domain-scoped, and provider-local auxiliary memory with lifecycle controls. |
| `source-coverage.md` | Old-file and material-section disposition, source commits, checked dates, new owners, omissions, and cutover evidence. |

### Research flow

```text
old pack corpus + current repository + official external sources
                              |
                              v
             source, claim, and coverage inventories
                              |
                              v
       current verification + analysis + disposition decision
                              |
                              v
          twelve scope owners + one pack index + one ledger
                              |
                              v
      mutable cross-link and machine-contract projection migration
                              |
                              v
        coverage/reference gates -> old pack deletion -> full QA
```

### Source priority

1. Canonical repository owners for local implementation and policy.
2. Official provider, product, standards, and upstream project documentation.
3. Tracked repository files and deterministic repository-static output.
4. Official issues and release notes needed to interpret current behavior.
5. Clearly labeled non-authoritative market or secondary material.

OpenAI, Anthropic, Kubernetes, GitHub, Diataxis, NIST, CISA, SLSA, Argo CD,
External Secrets Operator, Vault, OPA, and other applicable official sources
are used for their owned topics. The `msitarzewski/agency-agents` repository is
inspected at a recorded commit rather than through an unpinned branch view.

### Status vocabulary

Each current implementation comparison uses exactly one of:

- `Implemented`: local repository-static behavior is present and directly
  evidenced;
- `Partial`: only part of the required local behavior is present;
- `Missing`: the local behavior is absent;
- `Unverified`: available evidence cannot support the claim; or
- `Deferred`: the evidence belongs to an unauthorized or unavailable runtime,
  hosted, remote, live, or credential-bearing lane.

## Data Modeling & Storage Strategy

### Pack model

The pack is a dated Stage 90 snapshot. Each non-README document uses the
registry-selected `content/reference` profile and reference template. The
directory date is the observation identity, while each document's `Sources`
and `Review and Freshness` sections record claim-level currentness.

### Coverage record

The README coverage matrix stores:

| Field | Meaning |
| --- | --- |
| Request ID | Stable identifier for one original requested topic. |
| Requested topic | Human-readable scope item. |
| Primary owner | Exactly one new reference and section. |
| Workspace evidence | Current canonical file, contract, script, or manifest surface. |
| External source class | Official provider, standard, upstream project, or explicit secondary class. |
| Status | Implemented, Partial, Missing, Unverified, or Deferred. |

Required rows separately cover harness engineering, loop engineering,
workspace application environment and rules, Claude, Codex, their common
system, spec-driven development, Kubernetes, infrastructure, SDLC, every named
document family, Diataxis, LLM-WIKI, CI/CD, GitHub Actions, QA, security,
AI-agent systems, `agency-agents`, model routing, and memory tiers.

### Migration disposition record

The migration ledger contains one file-level row for each of the 25 old files
and extra rows when material sections split across owners. Each row stores:

| Field | Meaning |
| --- | --- |
| Old path | Exact predecessor path. |
| Source commit | Git object used for provenance and recovery. |
| Topic or heading | File-level subject or material section. |
| Verification | Current-source recheck result. |
| New owner | Surviving file and heading. |
| Disposition | Integrated, Corrected, Omitted as stale, or Omitted as duplicate. |
| Reason and evidence | Required for every omission and correction. |

No Stage 98 copy of the predecessor pack is created. Git history plus the
reviewed migration ledger preserve provenance without retaining duplicate live
or archive-pack documents.

### Lifecycle

1. Inventory and hash the old pack corpus.
2. Recheck old claims against current workspace and external sources.
3. Write the new pack and complete coverage and disposition records.
4. Migrate mutable links and machine-owned path projections.
5. Prove 25-of-25 file coverage and zero mutable predecessor references.
6. Delete all three old directories in one logical cutover unit.
7. Run full validation, independent review, and cleanup checks.

## Interfaces & Data Structures

### Reference analysis interface

Each material topic exposes this conceptual record:

```typescript
interface ResearchFinding {
  requestId: string;
  scope: string;
  claimClass:
    | "workspace-fact"
    | "external-fact"
    | "dated-predecessor-evidence"
    | "analysis"
    | "recommendation";
  status: "Implemented" | "Partial" | "Missing" | "Unverified" | "Deferred";
  workspaceEvidence: string[];
  externalSources: Array<{ url: string; checked: "2026-08-08" }>;
  analysis: string;
  canonicalOwner: string;
  refreshTrigger: string;
}
```

The interface is descriptive; the authored storage format remains Markdown.
Reviewers validate the same fields through headings and tables rather than a
new runtime parser unless the implementation plan justifies a deterministic
fixture for coverage or migration closure.

### Provider comparison boundary

Provider records separate API catalogs, Claude Code or Codex product behavior,
CLI configuration, tracked repository adapters, authenticated runtime
resolution, and hosted or remote execution. A model name or adapter value on
one surface cannot establish availability or behavior on another.

### Mutable-link interface

The cutover inventory classifies each old-path occurrence as:

- current navigational link: rewrite to the new owner;
- dated Stage 90 observation: retain the historical text and add a current
  lookup note when the document is mutable;
- machine-owned projection: update its canonical contract, fixture, and test;
- Stage 98 sealed payload: do not edit and exclude from current-reference
  closure; or
- stale invalid reference: remove with a recorded reason.

## Edge Cases & Error Handling

- **Official source unavailable**: mark the finding `Unverified` or omit it
  with a ledger reason; do not substitute uncited recollection.
- **Provider sources disagree**: preserve product-surface-specific facts and
  dates instead of selecting one undocumented winner.
- **Repository and external sources disagree about local behavior**: repository
  evidence controls the local implementation claim; the external source stays
  as a benchmark.
- **Old content is useful but no longer current**: retain it only as clearly
  dated predecessor evidence when it remains relevant; otherwise record
  `Omitted as stale`.
- **Duplicate analysis spans old files**: select one new primary owner and
  record every secondary occurrence as `Omitted as duplicate` with a cross-link.
- **A predecessor file lacks a disposition**: deletion is blocked.
- **A required topic lacks exactly one owner**: pack completion is blocked.
- **A validator names an old path**: update the canonical contract and focused
  tests together; never disable the validation lane.
- **A current link occurs inside Stage 98 payload**: leave it unchanged because
  its resolution belongs to the record's source commit.
- **Post-deletion validation fails**: restore the deletion unit before any
  commit and fix the missing migration; do not weaken the failed gate.
- **Temporary research output exists**: move durable evidence into the source
  ledger or delete the one-off artifact before handoff.

## Failure Modes & Fallback / Human Escalation

| Failure mode | Safe fallback | Escalation condition |
| --- | --- | --- |
| Primary source cannot support a material conclusion | Use `Unverified` and retain the old live packs until the coverage gate is complete. | The missing conclusion changes pack structure, deletion safety, or provider status. |
| Migration ledger cannot account for all 25 files | Stop before deletion and complete the inventory. | A file's purpose or canonical owner remains ambiguous. |
| Existing PRD, AD, Spec, or Plan mandates archive retention | Amend the mutable lifecycle contract with the approved replacement and review it before deletion. | Two active requirements still prescribe incompatible outcomes. |
| Reference-information-architecture tests require an old pack | Migrate the contract and preserve equivalent negative coverage. | Passing requires weakening provenance or snapshot integrity. |
| Mutable audit rewrite would falsify dated evidence | Preserve the dated statement and add a separate current-lookup migration note. | The document is immutable or its evidence meaning would change. |
| Stage 98 change appears in the diff | Stop and revert that change. | Completion would require modifying an existing archive payload or digest. |
| Repeated task review rejects a plan-mandated choice | Use the bounded subagent fix loop and route a plan/spec conflict to the human. | A load-bearing finding remains after the review cap. |

The user must separately approve any expansion into remote publication, push,
merge, live mutation, secret access, credential use, or third-party state
change. None is necessary to produce the requested research pack.

## Verification Commands

Required repository-static commands:

```bash
git diff --check
python3 scripts/validate-reference-information-architecture.py --root .
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/archive_validation.py --root .
bash scripts/validate-harness.sh
bash scripts/validate-repo-quality-gates.sh .
```

Focused acceptance checks must also prove:

```bash
test -d docs/90.references/research/0001-workspace-engineering
test ! -e docs/90.references/research/2026-07-04-wer
test ! -e docs/90.references/research/2026-07-07-wer
test ! -e docs/90.references/research/2026-08-07-wer
```

The implementation plan must define deterministic coverage and zero-reference
commands that exclude only existing `docs/98.archive/**` payloads and generated
or ignored output. It must list the complete mutable search domain instead of
using a narrow path subset to claim repository-wide closure.

Pre-commit and Markdown-specific checks run when installed. Missing optional
tools are recorded as `SKIP` with the fallback evidence; they are not reported
as passing coverage. No live, provider-runtime, hosted, remote, credential, or
secret-value check is part of acceptance.

## Success Criteria & Verification Plan

| Criterion | Required outcome | Authoritative evidence |
| --- | --- | --- |
| VAL-WER-001 | The new pack contains its README and twelve declared references. | Exact tracked-file inventory. |
| VAL-WER-002 | Every original requested topic maps to exactly one primary owner and workspace evidence surface. | Reviewed README coverage matrix and deterministic uniqueness check. |
| VAL-WER-003 | All 25 predecessor files and split material sections have reviewed dispositions. | Migration ledger coverage check against the baseline inventory. |
| VAL-WER-004 | External facts use appropriate official or primary sources with URLs, 2026-08-08 checked dates, and refresh triggers. | Source-ledger review and per-reference `Sources` and `Review and Freshness` sections. |
| VAL-WER-005 | Workspace implementation claims match current canonical owners and use the five-state vocabulary. | Repo-backed evidence review and focused status scan. |
| VAL-WER-006 | Claude, Codex, and their common environment are compared without collapsing product or evidence surfaces. | Provider and common-environment reference review. |
| VAL-WER-007 | SDLC, every named document family, Diataxis, LLM-WIKI, CI/CD, GitHub Actions, QA, Kubernetes, infrastructure, security, agents, model routing, and memory are fully covered. | Requirement-to-owner matrix plus task-scoped reviews. |
| VAL-WER-008 | Mutable contracts, audits, indexes, links, validators, and fixtures route to the new owner without weakening controls. | Focused tests, strict link/owner validation, and zero mutable old-path reference inventory. |
| VAL-WER-009 | All three predecessor directories are deleted and no compatibility or one-off artifact remains. | Exact absence checks and tracked scratch/residue scan. |
| VAL-WER-010 | Existing Stage 98 records are unchanged and validate. | Archive-path diff and archive validation. |
| VAL-WER-011 | Each logical unit receives an implementation report, spec/quality review, and green required gates. | SDD ledger, commit inventory, and review packages. |
| VAL-WER-012 | The complete branch passes final review and full repository-static QA without claiming deeper evidence. | Whole-branch review, full command output, and final evidence-depth audit. |

## Traceability

- **Predecessor specification**:
  [Spec 017](../0017-workspace-engineering-research-pack/spec.md)
- **Related consolidation specification**:
  [Spec 052](../0052-document-taxonomy-consolidation/spec.md)
- **Conflicting program requirement**:
  [PRD-0008](../../01.requirements/0008-workspace-document-taxonomy-consolidation.md)
- **Conflicting architecture**:
  [AD-0011](../../02.architecture/descriptions/0011-document-taxonomy-consolidation-architecture.md)
- **Approved requirement source**: the 2026-08-08 human request and explicit
  approval in the current Codex task.
- **Governing standalone decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Execution artifacts**:
  [Plan](plan.md)
  and
  [Task](README.md#task-records).

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — the direct human-approved research consolidation has no separate PRD; PRD-0008 is a conflicting input to reconcile, not the authority for deletion. | VAL-WER-001 | Exact tracked-file inventory proves the declared pack shape. |
| N/A — VAL-WER-002 shares the direct approved requirement source above. | VAL-WER-002 | Coverage uniqueness validation and review prove one primary owner per requested topic. |
| N/A — VAL-WER-003 shares the direct approved requirement source above. | VAL-WER-003 | The baseline-to-ledger comparison proves all predecessor files and split sections have dispositions. |
| N/A — VAL-WER-004 shares the direct approved requirement source above. | VAL-WER-004 | Source-ledger and reference-section review prove URL, checked-date, and refresh-trigger coverage. |
| N/A — VAL-WER-005 shares the direct approved requirement source above. | VAL-WER-005 | Repository evidence review and focused status scans prove local-claim correctness. |
| N/A — VAL-WER-006 shares the direct approved requirement source above. | VAL-WER-006 | Provider and common-environment review proves evidence-surface separation. |
| N/A — VAL-WER-007 shares the direct approved requirement source above. | VAL-WER-007 | The requirement-to-owner matrix and task reviews prove full requested-scope coverage. |
| N/A — VAL-WER-008 shares the direct approved requirement source above. | VAL-WER-008 | Focused contract tests and strict link/owner validation prove control-preserving migration. |
| N/A — VAL-WER-009 shares the direct approved requirement source above. | VAL-WER-009 | Exact path-absence and residue scans prove predecessor and one-off cleanup. |
| N/A — VAL-WER-010 shares the direct approved requirement source above. | VAL-WER-010 | Archive-path diff and archive validation prove existing Stage 98 immutability. |
| N/A — VAL-WER-011 shares the direct approved requirement source above. | VAL-WER-011 | SDD ledger, commit inventory, and task review packages prove per-unit review. |
| N/A — VAL-WER-012 shares the direct approved requirement source above. | VAL-WER-012 | Whole-branch review, full QA, and evidence-depth audit prove terminal acceptance. |
