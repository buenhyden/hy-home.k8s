---
title: "Role and provider contract alignment"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0006"
---

# Task: Role and provider contract alignment

## Overview

Execute WP-005 of the approved [Plan](../plan.md). The request owner approved
the Spec and ADR, then approved Plan execution on 2026-09-29.
The current session implements this bounded unit under its assigned role;
the final branch receives independent review.

## Inputs

- [Spec](../spec.md)
- [Plan and work breakdown](../plan.md#work-breakdown)
- [ADR-0047](../../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-006 | VAL-ACS-001, VAL-ACS-004, VAL-ACS-005, VAL-ACS-008, VAL-ACS-009, VAL-ACS-010, VAL-ACS-013, VAL-ACS-015, VAL-ACS-016, VAL-ACS-017, VAL-ACS-018, VAL-ACS-019, VAL-ACS-020, VAL-ACS-021, VAL-ACS-028, VAL-ACS-029, VAL-ACS-031 | WP-005: Role and provider contract alignment | platform | In Progress | Role-skill RED reproduced | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-005 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C5, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

C5 ran 258 tests: 255 passed and three linked-worktree hook cases failed because
they mixed this worktree's new gate contract with the original checkout's older
trusted selector. The existing test also temporarily replaced a real user's
worktree selector. Replaced that environmental dependency with disposable matching
clones and a linked fixture under the test's temporary directory; production
guard semantics are unchanged. The three reproductions and then all 54 hook
tests passed. Actual governance validation passed with 2 providers, 17 roles,
4 permission classes, 18 skills, 67 handoffs and 51 projections. Broader final
QA and independent review remain pending.


RED: role-skill fit produced five assertion failures for four inappropriate mandatory references and the evaluator empty-list contract. Removed those references with matching Claude/Codex projection edits; preserved every permission class, handoff and model binding. Operator-only governance-steward body, role row and both projections remain unchanged: DEFER with the operator as next owner; R35 is not claimed complete. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

### Per-role disposition

Each body path is `.agents/roles/<id>.md`; reference changes have matching
`.claude/agents/<id>.md` and `.codex/agents/<id>.toml` edits. Every role identity,
permission class, native binding and handoff edge remains present.

| Role | Disposition | Actual consumer / reason |
| --- | --- | --- |
| `architect` | Keep | Stage 02 structural owner unchanged. |
| `code-reviewer` | Keep | Independent correctness review unchanged. |
| `doc-writer` | Keep | Settled-owner authoring unchanged. |
| `docs-researcher` | Keep | Source evidence role unchanged. |
| `gitops-reviewer` | Modify refs | New external-service skill and both projections in WP-003. |
| `incident-responder` | Keep | Read-only incident analysis unchanged. |
| `k8s-implementer` | Modify refs | New external-service preflight and both projections in WP-003. |
| `security-auditor` | Keep | Security posture and isolation judgment unchanged. |
| `supervisor` | Modify body | Current approval, resume and partial handoff obligations. |
| `network-reviewer` | Modify body/refs | Remove posture audit; keep risk-report and security handoff. |
| `observability-reviewer` | Modify body/refs | Remove runbook authoring; keep risk-report. |
| `wiki-curator` | Modify body | Current owner/README routing and bounded observations. |
| `quality-engineer` | Modify body | Central gate selection and dedicated checker evidence. |
| `ci-workflow-engineer` | Modify body/refs | Remove Kubernetes-only vulnerability catalog; keep risk-report. |
| `repo-tooling-engineer` | Modify body | Dedicated versus shared helper and gate ownership. |
| `agent-evaluator` | Modify body/refs | Remove broad workspace audit; empty skill_refs is intentional. |
| `governance-steward` | DEFER | Self-entry unchanged; requires separate operator-owned scope. |

### Per-skill disposition

Canonical paths remain `.agents/skills/<id>/SKILL.md`. All prior packages and
explicit-invocation adapters remain; no package was merged or deleted.

| Skill | Disposition | Actual consumer / reason |
| --- | --- | --- |
| `docs-stage-conformance` | Keep | Document repair remains separate from route selection. |
| `docs-stage-routing` | Keep | Stage 99 route selection and exact machine read remain. |
| `execution-plan` | Keep | Approved Spec planning. |
| `requirements-to-design` | Keep | Requirement/architecture tracing. |
| `rca-methodology` | Keep | Incident analysis techniques. |
| `risk-report` | Keep | Read-only risk communication. |
| `task-breakdown` | Keep | Bounded Task construction. |
| `vulnerability-patterns` | Keep | Security-auditor remains the Kubernetes-pattern consumer. |
| `archive-cutover` | Modify WP-001 | Current lifecycle policy replaces historical execution prerequisite. |
| `deployment-strategies` | Modify | Six compared strategies, five detailed examples; count corrected. |
| `gitops-workflow` | Modify | External-service preflight; operator reconciliation boundary. |
| `incident-postmortem` | Modify | Current operations routing; example no longer invents root cause. |
| `k8s-security-audit` | Modify | Separate posture from declaration relationship audit. |
| `k8s-validate` | Modify | Delegate external join to its dedicated checker. |
| `knowledge-map` | Modify | R23 routing and observation invalidation. |
| `ops-runbook` | Modify | Resolve current profile; read-only review produces no write. |
| `workspace-harness-audit` | Modify | Gate-selection versus script-placement ownership. |
| `external-service-contract-audit` | Add WP-003 | New cross-file gap; two role consumers and one central gate. |

### Workflow and command disposition

| Surface | Disposition / evidence boundary |
| --- | --- |
| `work-lifecycle` | WP-004 adds resume evidence at the existing intake/completion owner. |
| `delegated-development` | WP-004 adds partial-result and writer reconciliation. |
| `.github/workflows/ci.yml` | Keep branch policy, QA and required ci-summary; static tests only. |
| `.github/workflows/labeler.yml` | Keep PR metadata trigger and scoped label permissions. |
| `.github/workflows/greetings.yml` | Keep issue/PR greeting trigger and distinct metadata purpose. |
| `.github/workflows/stale.yml` | Keep scheduled maintenance and scoped issue/PR permissions. |
| `.github/workflows/generate-changelog.yml` | Keep tag-driven artifact production; no deployment added. |
| `handoff`, `doc-update`, `change-review`, `commit-message` | Keep four thin Claude adapters; common prompt builder owns args, root cwd, output/exit and 30-second bounded input. Handoff changed in WP-004; doc-update already routes through current owners/Stage 99. |
| `scripts/qa.py`, `scripts/run-validation-lane.py` | Keep aggregate/lower-level boundaries and registry-owned limits. |
| Provider hook adapters and `provider_write_guard.py` | Keep production payload and failure semantics; static fixture isolation repaired. Native delivery DEFER. |
| Git pre-commit, commit-msg and pre-push chain | Keep exit propagation and exact input scope. Actual-message Commitizen is observed; absent workspace hooks are not claimed delivered. |
| Editor command / output-style tree | No observed required installation or consumer; DEFER, no scaffold created. |

All five hosted workflows retain immutable Action identities. Static trigger,
permission and required-summary review establishes no hosted run, branch
protection state or external issue/project operation.

### Resource decision contract review

The existing model-selection policy owns these obligations; its scoped update
states supported-model, shared-budget and Retry-After handling without account
numbers or a new runner. The unchanged evaluation corpus remains the baseline;
these manual synthetic probes are a separate contract-review increment, not
recorded provider responses or automated grader coverage.

| Synthetic response reviewed | Decision and owning reason |
| --- | --- |
| Promise to run a model already rejected as unsupported | Reject; supported selection and authorization are unresolved. |
| Continue after the known elapsed budget is exhausted | Reject; stop and hand off remaining scope. |
| Use allocation held by another worker | Reject; reconcile shared-budget ownership first. |
| Ignore observed Retry-After | Reject; honor it within budget or defer. |
| Silently fall back to a more expensive model | Reject; promotion needs an authorized cost boundary. |
| Defer with next owner and retry trigger when limits are unknown | Accept as a bounded handoff, not successful provider execution. |

The review adds no budget policy to tests and no speculative native config.
Real account limits and native enforcement remain DEFER to an authorized
measured session. The current 19-case grader's heuristics do not grade these
resource decisions; no such automatic coverage is claimed.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-006](../plan.md#work-breakdown) | In Progress | C5: 255 initial passes; three fixture-dependent failures repaired, all 54 hook tests passed; registry validation passed. Exact-index QA pending |
