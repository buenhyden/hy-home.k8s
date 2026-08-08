---
title: 'Task: Workspace Engineering Research Pack Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-08
---

# Task: Workspace Engineering Research Pack Consolidation

## Overview

This Task records execution and review evidence for the ten WERPC work
packages that replace three dated research packs with one source-backed
`2026-08-08-wer` pack. Rows advance only after the logical commit, required
repository-static gates, implementation report, specification review, and
quality review are accepted.

External source observations are dated evidence, not live provider or platform
proof. No hosted CI, provider-runtime, remote, credential-bearing, secret-value,
or live-cluster result is produced or claimed.

## Inputs

- **Specification**:
  [Spec 053](../../03.specs/053-workspace-engineering-research-pack-consolidation/spec.md)
- **Plan**:
  [Workspace Engineering Research Pack Consolidation Implementation Plan](../plans/2026-08-08-workspace-engineering-research-pack-consolidation.md)
- **Standalone execution decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Predecessor specification**: `Spec 017` at
  `docs/03.specs/017-workspace-engineering-research-pack/spec.md`
- **Conflicting program**: `Spec 052` at
  `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- **Approved requirement source**: direct 2026-08-08 human request and explicit
  Spec 053 approval in the current Codex task
- **Design commit**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`
- **Execution branch base**: `37c714d04e1ab20816f2719fdc09f6dc42acef72`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WERPC-000 | VAL-WER-008, VAL-WER-011 | Activate reciprocal execution and supersede only WDTC-002/WORK-002 | platform | Done | Active reciprocal lifecycle is recorded; WDTC-002/WORK-002 is superseded to Spec 053 and WERPC-008; all required focused, diff, and repository quality checks passed before this logical commit | Design commit; strict registry, Markdown profile, and links/owners checks; repository quality gate; optional all-files pre-commit INTERRUPTED/SKIP with required-gate fallback; self-review; this logical commit |
| WERPC-000A | VAL-WER-008, VAL-WER-011 | Add typed direct-approval standalone execution lineage without changing program lineage | platform | Done | Closed schema-v8 relation, parser projection, structural/link/eligibility diagnostics, ADR-0022, exact-pair terminal eligibility, disjoint rendered execution graphs, and bounded post-closure ADR handling are implemented without changing existing program-lineage semantics | RED/GREEN mutation history remains in the progress ledger. Final staged evidence: registry self-test 132 cases and strict 501 paths; standalone link fixture 8 cases and full links self-test/strict PASS; eligibility 58 cases and production PASS; residue closure 25 cases and production PASS with frozen guards 13/29; affected unit tests 2/2 PASS; Markdown profiles and cached diff PASS; complete repository quality gate PASS; Python and governance reviews Approved. |
| WERPC-001 | VAL-WER-001, VAL-WER-002, VAL-WER-003 | Create exact pack shape, coverage matrix, source register, and predecessor disposition baseline | docs-researcher | Done | Created the exact thirteen-file pack with REQ-WERPC-001 through REQ-WERPC-032, one primary file-and-heading owner per request, current workspace evidence, three dated predecessor source-register entries, 25 full-hash file dispositions, and 35 text-exact H3 split rows | Exact 13/25 counts, Markdown profiles, strict registry, strict links/owners, diff check, full repository quality gate, self-review, and this logical commit |
| WERPC-002 | VAL-WER-004, VAL-WER-005, VAL-WER-006, VAL-WER-007 | Research governance, harness, loop, Claude, Codex, and common environment | docs-researcher | Done | Three detailed references define the harness/loop machine, workspace control plane, and Claude/Codex surface matrix; ten dated official primary-source rows and nine bounded claim rows distinguish static configuration, native discovery, and authenticated/runtime evidence; the collection index and README inventory contract include the new pack | Fresh-review RED: strict links/owners reported 26 collection-index omissions. Fix-round RED: the full gate exposed the missing new-pack README inventory row. GREEN: exact 13-file tree/table projections, active54/new7 README contract, Markdown profiles, registry self-test/strict, strict links, harness semantics, Reference IA production, cached diff, and the full repository gate PASS; documentation and Python fresh reviews Approved; this logical commit. |
| WERPC-003 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research spec-driven SDLC, document families, Diátaxis, and LLM-WIKI | docs-researcher | Queued | Not executed | Three references, complete document-family matrix, wiki/profile/link/full gates |
| WERPC-004 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research Kubernetes, infrastructure, GitOps, and security | security-auditor | Queued | Not executed | Platform/security reference, source and evidence-depth review, harness/full gates |
| WERPC-005 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research CI/CD, GitHub Actions, and QA | quality-engineer | Queued | Not executed | Delivery/QA reference, workflow inventory, source review, full gate |
| WERPC-006 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research AI agents, pinned agency-agents, model routing, and memory tiers | docs-researcher | Queued | Not executed | Three references, pinned upstream commit, provider and local-contract review |
| WERPC-007 | VAL-WER-008, VAL-WER-010, VAL-WER-011 | Migrate links, observations, indexes, machine contracts, validators, and fixtures | platform | Queued | Not executed | Classified occurrence ledger, focused RED/GREEN, strict/reference-IA/archive/full gates |
| WERPC-008 | VAL-WER-003, VAL-WER-008, VAL-WER-009, VAL-WER-010 | Prove readiness and delete the 25 predecessor files | platform | Queued | Not executed | 25/25 pre-gate, three absence checks, post-deletion validation, deletion commit |
| WERPC-009 | VAL-WER-001–012 | Run final audit/review/cleanup and close reciprocal lifecycle | supervisor | Queued | Not executed | Criterion walk, final QA, whole-branch review, residue scan, closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/**` except existing `docs/98.archive/**` records;
  `scripts/**` and `tests/**` only for path-contract and fixture migration
- **Forbidden Paths**: existing `docs/98.archive/**` records, `gitops/**`,
  `infrastructure/**`, `traefik/**`, `policy/**`, ignored credential/secret
  state, user stashes, and paths outside the isolated worktree
- **Approval Required**: any live, hosted, remote, credential-bearing,
  secret-reading, push, merge, publication, third-party mutation, or change to
  active runtime/provider/platform behavior
- **Static Validation**: focused commands in each Plan task and
  `bash scripts/validate-repo-quality-gates.sh .` before every commit
- **Live Validation**: `DEFER` — not authorized and not required for this
  descriptive research pack
- **Secret / Vault Handling**: no secret value, token, kubeconfig, ignored
  credential file, Vault payload, or provider credential is read or printed
- **Rollback Plan**: one logical commit per row; WERPC-008 is the isolated
  deletion commit; Git history retains the predecessor content
- **Evidence Location**: this Task, the new source/migration ledger, the
  progress ledger, Git commits, and the SDD ledger review packages

## Verification Summary

The specification and design commit are approved. WERPC-000 is done:
`python3 scripts/validate-document-contract-registry.py --root . --mode strict`,
`python3 scripts/validate-links-and-owners.py --root . --mode strict`,
`git diff --check`, and `bash scripts/validate-repo-quality-gates.sh .` passed
on the final pre-commit tree. The optional `pre-commit run --all-files` attempt
was interrupted after it stalled and rewrote only detect-secrets metadata in
`.secrets.baseline`; that incidental change was restored exactly and the
optional lane is `SKIP`, not `PASS`. The passing required strict, diff, and full
repository gate results are the fallback evidence. The results are
repository-static only; provider-runtime, hosted CI, remote, and live
validation remain `DEFER`.
WERPC-001 is done with the thirteen-file shape, request-owner matrix, dated
predecessor source-register interface, 25 full-hash file dispositions, and 35
text-exact H3 split rows. It does not claim external currentness: later topical
work must recheck predecessor URLs. Its strict registry, strict links/owners,
and full repository quality-gate results are repository-static only.
WERPC-000A implements the approved typed standalone-execution contract without
changing `programLineage`. Registry, links/owners, eligibility, residue closure,
the affected unit tests, Markdown profiles, cached diff, and the complete
repository quality gate passed on the final reviewed staged tree.
WERPC-002 is done: its source ledger has official, dated primary sources with
refresh triggers and claim boundaries; the topical references retain `DEFER`
for native discovery, authenticated/runtime, hosted CI, remote, and live
claims. The collection-index and README-inventory REDs were closed without
changing the immutable baseline, and both fresh reviews plus the final staged
Reference IA and complete repository quality gate passed. The attempted
Reference IA `--staged` variant is recorded as an inapplicable-mode `SKIP`; the
Plan's production `--root .` command passed. WERPC-003 through WERPC-009 are
not executed. Each remaining
row will record exact command results, review disposition, commit, limitation,
`SKIP`, or `DEFER` without converting repository-static evidence into a deeper
claim.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WERPC-000](../plans/2026-08-08-workspace-engineering-research-pack-consolidation.md#work-breakdown) | Done. | Active Spec/Plan/Task and collection indexes; bounded PRD-008/ARD-0011 exception; superseded WDTC-002/WORK-002 route; required strict, diff, and repository-quality checks passed; optional all-files pre-commit INTERRUPTED/SKIP with required-gate fallback; self-review. |
| N/A — WERPC-000A shares the Plan and Spec sources above | Done. | Typed standalone execution, exact-pair/approval/owner/state/overlap/terminal tests, bounded closure authority, two independent reviews, and the complete repository quality gate PASS. |
| N/A — WERPC-001 shares the Plan and Spec sources above | Done. | Exact thirteen-file pack; 32 unique request-primary-owner rows; three dated predecessor source entries; 25 file rows with matching full source commits; 35 text-exact H3 split dispositions; strict registry, strict links/owners, cached diff, and full repository quality gate PASS on the staged tree. |
| N/A — WERPC-002 shares the Plan and Spec sources above | Done. | Dated source/claim ledger (SRC-WERPC-004–013; CLM-WERPC-002-01–009); detailed harness/loop, provider-surface, and common-control-plane references; exact 13 tree/row collection projections; active54/new7 README inventory contract with baseline67/active47/retired20 preserved; documentation and Python fresh reviews Approved; final Reference IA production and complete repository quality gate PASS. |
| N/A — WERPC-003 shares the Plan and Spec sources above | Not executed. | SDLC/document/Diátaxis/LLM-WIKI research evidence pending. |
| N/A — WERPC-004 shares the Plan and Spec sources above | Not executed. | Kubernetes/infrastructure/security research evidence pending. |
| N/A — WERPC-005 shares the Plan and Spec sources above | Not executed. | CI/CD/GitHub Actions/QA research evidence pending. |
| N/A — WERPC-006 shares the Plan and Spec sources above | Not executed. | Agents/agency/model/memory research evidence pending. |
| N/A — WERPC-007 shares the Plan and Spec sources above | Not executed. | Link/contract/fixture migration evidence pending. |
| N/A — WERPC-008 shares the Plan and Spec sources above | Not executed. | Readiness and deletion evidence pending. |
| N/A — WERPC-009 shares the Plan and Spec sources above | Not executed. | Final criterion, QA, review, residue, and closure evidence pending. |
