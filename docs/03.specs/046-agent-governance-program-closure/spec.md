---
title: 'Agent Governance Program Closure Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-22
---

# Agent Governance Program Closure Technical Specification (Spec)

## Overview

This Spec is the strict final integrator for the workspace agent-governance
program. It unifies every criterion from the existing document-lifecycle Specs
038-040 and agent-governance Specs 041-045, and proves the machine contract,
bounded loop, 12-role/48-adapter parity, role evaluation and model fitness,
CI/QA, and legacy cutover through one closure matrix.

The authenticated native canaries for the Claude, Codex, and Gemini CLIs must
all be `PASS`. If any CLI is absent or unauthenticated, uses an unsupported
model or configuration, fails discovery, or reports `SKIP`, `DEFER`, or
`FAIL`, the program remains active and this Spec is not complete. A
repository-static PASS or the presence of a local/Antigravity adapter cannot
substitute for this requirement.

The provider, model, and source baseline is frozen at **2026-07-10 10:00
Asia/Seoul**. Because final verification occurs later, each canary records the
cutoff decision separately from the current runtime observation. Closure
reuses the official provider documentation and release sources in the Spec
042/044 source ledger and does not adopt a new unofficial model claim as
closure evidence.

## Strategic Boundaries & Non-goals

- **In scope**: closure of Spec 038-045 criteria; upstream PRD/ARD/ADR
  traceability; the canonical contract and schema; loop recovery; the exact
  12/48 roster; three provider canaries; evaluation and model fitness;
  CI/QA/all-files; zero stale active legacy artifacts; an independent
  whole-branch review; and a clean worktree with logical history.
- **Protected boundaries**: Secret and authentication values and private
  transcripts are neither read nor retained. A canary is read-only or a
  provider-native bounded test; it does not change a live cluster, GitHub
  settings, or an external deployment.
- **Non-goals**: waiver-based closure for a failing or absent provider; an
  unobserved PASS claim for a remote workflow or branch protection; a live
  Kubernetes, Argo CD, or Vault readiness claim; automatic push, PR, merge, or
  release execution; or adding a new feature in the final tranche.

## Contracts

Closure is the conjunction below in the stated order; partial credit and
majority voting are not permitted.

1. Specs 038, 039, and 040 each have an allowed done state and committed
   evidence.
2. Every criterion in Specs 041, 042, 043, 044, and 045 is PASS, with no
   unresolved required DEFER.
3. The links, status, index, registry, and lineage across PRD 003, ARD 0006,
   ADR 0019, and Specs 041-046 agree.
4. The canonical machine harness contract and schema are the sole current
   owner for all four surfaces, provider notes, validators, and the evaluation
   manifest.
5. The bounded-retry, no-progress-stop, and checkpoint/compaction recovery
   rehearsals pass.
6. The canonical role set contains exactly 12 roles, the four surfaces contain
   exactly 48 adapters, and semantic parity and provider-native schema checks
   pass.
7. The authenticated canaries for the Claude, Codex, and Gemini CLIs each pass
   independently.
8. The incumbent/candidate evaluations and model/reasoning profiles for all 12
   roles pass the approved thresholds and independent adjudication.
9. Agent-governance CI/QA, repository tests, all-files pre-commit, formatter
   review, rerun, and diff checks report a clean PASS.
10. The active corpus contains zero stale legacy or deprecated owners, claims,
    adapters, or contracts.
11. Independent requirements and quality/security reviewers issue approval
    verdicts for the whole branch, and every finding is fixed and re-reviewed.
12. The worktree is clean and commit history aligns with the logical units of
    the Specs, Plans, and Tasks.

The static, provider-runtime, remote-CI, and live-platform evidence lanes stay
distinct through closure. Only this program's three required provider-runtime
canaries are closure-required PASS results. Out-of-scope remote branch
protection, deployment, and live-cluster state may remain DEFER when an owner
and trigger are recorded. Closure fails if such a DEFER is represented as PASS
or summarized as something the program proved.

## Core Design

### Closure matrix

For each PRD requirement and predecessor criterion, the final integrator creates
one row containing:

- the owning document and criterion ID;
- the implementation commit or commit range;
- the verification command and evidence digest;
- the result class and execution time;
- the requirements-reviewer and quality/security-reviewer verdicts; and
- the limitation, residual risk, rollback, and next owner/trigger.

After the matrix is generated, a deterministic validator rejects missing
criteria, duplicate evidence owners, required rows that are not PASS, stale
commits, and ownerless DEFER results. The closure body links canonical Task
evidence and digests instead of copying raw logs.

### Three-provider authenticated canary gate

Each Claude, Codex, and Gemini CLI canary proves at least:

1. the installed CLI and version, plus execution time;
2. an authenticated account/session class without exposing a secret;
3. the effective project configuration and instruction source;
4. discovery of the canonical 12 roles from the native project agent
   directory;
5. a representative low-risk role invocation and its expected stop/output
   contract;
6. the configured model ID and reasoning/effort resolution, or the
   provider-native equivalent;
7. applicable settings, hook, policy, sandbox, approval, and MCP inventory
   status; and
8. redacted PASS evidence and rollback/cleanup.

The three results are separate records and cannot be replaced by the presence
of one aggregate file. If installation or login requires user action, closure
stops and escalates to a human. The agent neither infers nor automates
credential entry, renewal, or storage.

### Review and finish flow

1. Verify targeted predecessors and closure-matrix completeness.
2. Run affected, staged, test, all-files, formatter, rerun, and diff QA lanes.
3. Run fresh requirements and quality/security reviewers in sequence against
   the whole-branch diff from the main merge base.
4. Fix each Critical or Important finding and each contract mismatch, then
   repeat the corresponding review over the same scope.
5. Confirm a clean tree, logical commits, no one-off artifact, and no secret
   evidence.
6. Present the approved branch-completion options to the user. Perform a local
   merge, push, PR, or branch/worktree cleanup only with the corresponding
   explicit authority and finishing workflow.

## Data Modeling & Storage Strategy

The durable closure record remains in canonical Stage 04 Task/Plan evidence and
the criterion mapping in this Spec. Its minimum fields are the program/tranche
commit range, contract version, 12/48 inventory digest, per-provider canary
result and digest, loop-recovery result, evaluation-suite version, CI/QA
results, legacy scan, reviewer verdict, and rollback.

A provider canary record does not store tokens, credential paths or contents,
environment dumps, shell history, or raw private prompts or transcripts.
Authentication is recorded only as a non-secret status/class and redacted
result, not as a secret returned by the provider.

The ignored `.agent-work/checkpoint.json`, SDD progress, dry-run logs, and
migration scratch are not closure evidence owners. Promote required summaries
to the canonical Task, then remove one-off tracked artifacts and temporary
worktree output. Do not alter historical ADR or archive records; validate the
current owner and superseding relation instead.

## Interfaces & Data Structures

- **Predecessor interface**: Spec criterion ID -> implementation/evidence/reviewer/
  rollback row.
- **Canary interface**: provider, CLI version, auth class, config source, discovered
  role set, resolved model/effort, policy/config result, MCP status, timestamp, result,
  redacted digest.
- **Roster interface**: canonical 12-role set x four named surfaces -> exact 48 adapter
  inventory and semantic/schema findings.
- **Loop interface**: retry attempts, failure signature, changed hypothesis, budget,
  no-progress decision, checkpoint digest, recovery next action/verifier.
- **Eval interface**: suite/role/model/profile version, baseline comparison, quality,
  safety, cost, latency, adjudication, promotion/rollback decision.
- **Branch handoff**: merge base, HEAD, logical commits, clean status, validation summary,
  remote/live limitations, user-selected completion option.

## Edge Cases & Error Handling

- If the Claude or Gemini CLI is absent or unauthenticated, its canary is not
  PASS and the program does not close.
- Two passing providers out of three are not rounded up to an aggregate PASS.
- If only a subset is returned during runtime discovery, that provider canary
  is FAIL even when all 12 native agents exist statically.
- If a provider cannot resolve the cutoff model because of entitlement or
  lifecycle state, do not silently fall back; require the approved fallback
  and reevaluation defined by Specs 042 and 044.
- When all-files pre-commit creates a formatter diff, QA remains incomplete
  until the diff is reviewed, staged, and the check is rerun.
- If a change occurs after the whole-branch review, repeat the affected review
  and QA.
- If remote CI or a live cluster was not observed, do not infer PASS from local
  similarity.
- For untracked or ignored credential and diagnostic files, verify only path
  policy and a clean tracked tree; do not read their contents.

## Failure Modes & Fallback / Human Escalation

- Stop the program/status transition if any required predecessor criterion,
  provider canary, parity check, evaluation, CI/QA result, legacy scan, or
  reviewer verdict fails.
- When provider installation or authentication is required, present only
  commands and expected evidence that do not request a secret, so the user can
  approve and perform the action directly.
- If a canary requires a permission change, paid action, credential
  modification, or external mutation, do not perform it automatically;
  escalate to the platform/security owner.
- Do not close an independent-review finding with a waiver. If the requirement
  must change, update the upstream PRD, ARD, ADR, or Spec first, then revalidate.
- If integration conflicts with a user change or requires a remote action,
  stop at a clean branch handoff and obtain the user's decision.

## Verification Commands

```bash
python3 scripts/validate-agent-governance-closure.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-canaries.py --root . --require-pass claude,codex,gemini
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

`validate-agent-governance-closure.py` is a planned Spec 046 deliverable and is
not claimed to exist in this draft. It must aggregate every predecessor
criterion, exact owner/version, three authenticated provider PASS records,
review verdict, clean-tree/logical-history evidence, and required limitation
without converting a missing result into PASS.

## Success Criteria & Verification Plan

- **VAL-AGPC-001**: Every required criterion in Specs 038-045 and its upstream
  lineage has committed PASS evidence, with no unresolved required DEFER.
- **VAL-AGPC-002**: The canonical roster contains exactly 12 roles and the four
  surfaces contain exactly 48 adapters; native schema and semantic parity
  checks pass.
- **VAL-AGPC-003**: The authenticated native canaries for the Claude, Codex, and
  Gemini CLIs each pass independently, and secret-free evidence is retained.
- **VAL-AGPC-004**: The machine harness contract and schema are the sole current
  owner, and every consumer, adapter, and validator uses the same version.
- **VAL-AGPC-005**: The bounded-retry/no-progress termination and
  checkpoint/compaction recovery rehearsals reconstruct the approved next
  action and verifier.
- **VAL-AGPC-006**: Versioned evaluation and model fitness for all 12 roles meet
  quality and safety thresholds, provider canaries, independent adjudication,
  and rollback requirements.
- **VAL-AGPC-007**: Agent-governance CI, repository tests, all-files pre-commit,
  formatter review and rerun, and diff checks report a clean PASS.
- **VAL-AGPC-008**: There are zero active stale legacy or deprecated claims,
  duplicate current owners, old consumers or contracts, or orphan adapters;
  history remains only through non-current relations.
- **VAL-AGPC-009**: Independent whole-branch requirements and quality/security
  reviews are approved, the worktree is clean, and remote/live limitations and
  the completion option are handed off accurately.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **ARD**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Document-lifecycle prerequisites**: [Spec 038](../038-reference-information-architecture/spec.md),
  [Spec 039](../039-github-ci-qa-evidence/spec.md), and
  [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **Agent-governance predecessors**: [Spec 041](../041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../042-provider-native-runtime-and-model-evidence/spec.md),
  [Spec 043](../043-agent-harness-loop-lifecycle/spec.md),
  [Spec 044](../044-agent-roster-evaluation-and-admission/spec.md), and
  [Spec 045](../045-agent-governance-ci-qa-cutover/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-MET-02](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-001 | Predecessor and lineage validation proves the complete reciprocal program chain. |
| [REQ-PRD-FUN-08](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-002 | Four-surface exact set and native semantic/schema validation prove 12/48 parity. |
| [REQ-PRD-MET-06](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-002 | Exact inventory validation reports zero role or adapter drift. |
| [REQ-PRD-FUN-09](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-003 | Three authenticated canary records prove native discovery, config, and model resolution. |
| [REQ-PRD-MET-07](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-003 | Canary aggregation rejects any provider result other than PASS. |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-004 | Contract/schema and consumer-version validation prove a single machine owner. |
| [REQ-PRD-MET-08](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-004 | Provider metadata and adapter projections validate against the current contract version. |
| [REQ-PRD-FUN-11](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-005 | Retry/no-progress fixtures and checkpoint recovery prove bounded loop behavior. |
| [REQ-PRD-MET-09](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-005 | Recovery rehearsal reconstructs the approved next action and verifier. |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-006 | Versioned role corpus and provider mapping prove role/model fitness. |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-006 | Canary, adjudication, threshold, and rollback evidence prove promotion fitness. |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-007 | Static CI, tests, all-files, formatter rerun, and diff evidence prove completion QA. |
| [REQ-PRD-MET-11](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-007 | Required local and CI lanes all report clean PASS. |
| [REQ-PRD-FUN-14](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-008 | Active-corpus and consumer scans prove zero stale legacy. |
| [REQ-PRD-MET-12](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGPC-008 | History remains only through validated non-current relations. |
| [REQ-PRD-FUN-15](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGPC-009 | Independent review and clean handoff prevent catalog-driven or waiver closure. |
