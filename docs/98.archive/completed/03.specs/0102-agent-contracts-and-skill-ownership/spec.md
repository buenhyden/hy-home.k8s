---
title: "Agent Contracts and Skill Ownership"
version: "1.1.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102"
---

# Agent Contracts and Skill Ownership Technical Specification

## Overview

This work unit renews the repository's agent contracts across shared governance, skills, native adapters, validation, and their consumers. The 2026-09-29 investigation found 17 registered roles, 17 canonical skills, 17 Claude role projections, 17 Codex role projections, and one homogeneous 19-case synthetic agent evaluation corpus. The approved design direction is incremental convergence at existing owners. Implementation and static acceptance are complete; the dated closure supplement in Task 0008 records the final R35 disposition and separately bounded external evidence.

The user approved the incremental design, this Spec, and ADR-0047 on 2026-09-29, then authorized Plan drafting. Initial document state was committed in `8e811506`; the approved Spec transitioned to `active`. The request owner subsequently approved the Plan and implementation on 2026-09-29; the linked Tasks record that execution scope. No historical SPEC-0072 or SPEC-0099 approval is inherited. The current [Requirement Package](../../01.requirements/0003-workspace-agent-governance-platform.md), [Architecture Description](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), accepted [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md), and accepted [ADR-0047](../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md) are inputs with their distinct authority states. ADR-0047 now records the separately approved `accepted` state after its initial commit.

The request's R01–R39 labels are aliases for this work unit, not new durable Requirement IDs. The final traceability table maps them to criteria and maps those criteria to full current `REQ-0003-*` IDs. Requirements stay solution-independent; this Spec owns change-specific behavior.

The request owner subsequently authorized package completion and commit/push/merge/branch-worktree cleanup on 2026-09-29. This narrowly authorizes the operator-directed R35 wording correction recorded in [Task 0008](tasks/tsk-0008-final-verification.md#closure-supplement). Native, account, editor and live observations remain explicitly deferred to their named operators; package completion does not claim them as PASS.

## Strategic Boundaries & Non-goals

- In scope: `.agents/` common policy, roles, skills, knowledge, prompts, workflows and their dedicated resources; `.claude/` and `.codex/` native adapters; `.github/` static CI contracts; repository validation, tests, evaluation corpus, related navigation and reciprocal current links. `gitops/`, `infrastructure/`, `examples/`, and `policy/` are inspected as consumers and safe fixtures; their live declarations change only if a later approved Plan names a necessary scoped fix.
- No new role or native agent is justified. No empty output-style, editor, Traefik, or command directory is created to meet a checklist. The external Traefik workspace is outside this repository; local ingress and router contracts remain here.
- Original implementation boundary (later remote integration approval is recorded above): no live cluster, Argo CD, Vault/OpenBao, cloud, provider account, or GitHub remote mutation; no secrets, credential values, raw transcript, personal/global configuration scan or edit; no push, PR, merge, destructive Git cleanup, or deployment. Operator approval remains necessary for protected actions.
- Existing governance, Stage 99 document profiles, the role registry, validation registry, GitOps reconciliation, and Stage 98 retained bodies keep their current authority. A successor decision may change future policy, never rewrite an accepted ADR or frozen/archive evidence. No parallel progress or recovery ledger is added.
- Native discovery, resolved model, hook delivery, authenticated execution, hosted CI, and live state are separate evidence lanes. A static PASS cannot satisfy any other lane. Unavailable account cost/RPM/TPM or native capabilities are recorded `DEFER`, not filled with assumed limits.

## Contracts

### Authority, lifecycle, and ownership

The neutral `.agents/roles/registry.json` owns role identities, permission classes, skill references, handoffs, and provider projection paths. Role bodies own responsibilities; shared policy owns approvals, safety, quality, document routing, and memory; Stage 99 owns document form. Skills describe procedures and cannot grant permissions. Provider adapters declare native syntax and supported behavior only. Manual derived projections have no generator; updates to the registry and affected Claude/Codex files must be reviewed together. The `governance-steward` may not edit its own role contract; any such change requires a separately approved operator-owned scope.

All 17 current role identities remain. The target disposition after Spec and Plan approval is file-specific; no role is merged or deleted:

| Neutral role body | Disposition | Preserved or changed contract |
| --- | --- | --- |
| `architect` | Keep | Stage 02 structural owner. |
| `code-reviewer` | Keep | Independent correctness review. |
| `doc-writer` | Keep | Author only after canonical owner is settled and delegated. |
| `docs-researcher` | Keep | Source evidence without policy authority. |
| `gitops-reviewer` | Keep | Read-only reconciliation review; add new skill reference only with proven consumer. |
| `incident-responder` | Keep | Incident triage and RCA, separate from implementation. |
| `k8s-implementer` | Keep | Scoped GitOps author; add new skill reference only with proven consumer. |
| `security-auditor` | Keep | Independent security review. |
| `supervisor` | Modify | Approval, resume, and bounded handoff routing. |
| `network-reviewer` | Modify | Align imported security posture procedure with network/isolation remit. |
| `observability-reviewer` | Modify | Resolve read-only review versus authoring `ops-runbook` skill reference. |
| `wiki-curator` | Modify | R23 navigation and owner-map consumers. |
| `quality-engineer` | Modify | Clarify central gate selection and dedicated-checker evidence. |
| `ci-workflow-engineer` | Modify | Remove or justify K8s-only vulnerability skill in hosted CI remit. |
| `repo-tooling-engineer` | Modify | Common tool versus skill-dedicated resource ownership. |
| `agent-evaluator` | Modify | Evaluation corpus and broad workspace-audit skill fit. |
| `governance-steward` | Operator-directed correction completed | Manual projection maintenance wording corrected under the request owner's closure instruction; self-edit prohibition, registry entry and projections preserved. |

Empty `skill_refs` is valid where no skill fits; filler references are prohibited. All current 17 skill packages remain; no merge or deletion is supported by the investigated consumers:

| Canonical skill | Disposition | Preserved or changed contract |
| --- | --- | --- |
| `docs-stage-conformance`, `docs-stage-routing` | Keep | Narrow document repair versus route selection. |
| `execution-plan`, `requirements-to-design` | Keep | Approved Spec planning versus requirement/architecture tracing. |
| `risk-report`, `task-breakdown`, `rca-methodology`, `vulnerability-patterns` | Keep | Unique report, decomposition, root-cause, and security-pattern uses. |
| `archive-cutover` | Modify | R23 current link routing while preserving immutable Stage 98 disposition. |
| `deployment-strategies` | Modify | Reconcile text saying five strategies with six in its reference. |
| `gitops-workflow` | Modify | Mark external-service preflight and operator reconciliation boundary. |
| `incident-postmortem` | Modify | Correct current owner/link paths without altering incident history. |
| `k8s-security-audit` | Modify | Separate security/secret posture from new declaration relationship check. |
| `k8s-validate` | Modify | Delegate cross-file selectorless relation check; keep generic manifest validity. |
| `knowledge-map` | Modify | R23 route to current owner/README instead of individual Stage authority. |
| `ops-runbook` | Modify | Correct owner/link paths and keep authoring separate from read-only observability review. |
| `workspace-harness-audit` | Modify | Align R23/R25/R32 actual consumer and validator boundaries. |
| `external-service-contract-audit` | Add | Proven selectorless cross-file gap; no duplicate role or agent. |

A same-name system or user skill does not become this repo's canonical package. All 17 existing Claude skill symlinks and Codex `agents/openai.yaml` sidecars remain; add one of each for the approved new skill. All 17 native agent files per provider remain; edit only files whose registry responsibilities, skill references, model, or scope change. No claim of native discovery follows from file parity.

The shared `work-lifecycle.md` and `delegated-development.md` remain distinct; both receive bounded stop/resume evidence at their own workflow boundaries. Hosted `ci.yml`, `labeler.yml`, `greetings.yml`, `stale.yml`, and `generate-changelog.yml` remain separate by trigger, permission, output, and required-check role. CI remains QA, not deployment. The four `.agents/prompts/{handoff,change-review,commit-message,doc-update}.md` contracts and matching `.claude/commands/` adapters remain; `handoff` and `doc-update` receive scoped input/output and authority fixes. A provider output style may express presentation only when installed support and a real consumer are shown; it never overrides safety or evidence fields.

### Command and hosted-workflow dispositions

The current four Claude slash commands remain thin adapters to the four common prompt contracts; Codex has no corresponding command tree. `scripts/qa.py` remains the quick/staged/full/ci aggregate entrypoint, `scripts/run-validation-lane.py` remains its bounded lower-level executor, and `scripts/validation/registry.json` remains the gate-selection owner. `scripts/provider_write_guard.py` remains the shared implementation called by the Claude and Codex hook adapters. Git `scripts/githooks/{pre-commit,commit-msg,pre-push}` and `chained-hook.sh` remain distinct from full QA's manual pre-commit stage. `scripts/prompt-input.py` receives bounded capture and honest incomplete-result reporting. `scripts/run-agent-evaluations.py` moves with its exclusive corpus to `.agents/evaluations/run-agent-evaluations.py`; all registry, test, documentation, and case-path consumers change in the same unit. The five hosted workflows remain separate; `ci.yml` preserves its required `ci-summary`, while labeler, greetings, stale, and changelog retain their distinct metadata/maintenance/artifact roles. No command is deleted before caller-zero or an approved expiring compatibility route is proven. Each retained or changed entrypoint must have documented arguments, cwd, input/output, exit/timeout, side effects, privilege and cost where applicable. No editor command is invented from `.editorconfig` alone.

### Document authority and history

Current documents outside `docs/` must not preserve execution authority through direct individual numbered-stage document references, whether Markdown links or plain paths. The target route is the current owner and its stage/collection README navigation. The revised validator must normalize relative and absolute paths, reference links, HTML, wiki links, GitHub blob/raw URLs, URL encoding, case and path separators. All direct individual numbered-stage document links outside `docs/` are prohibited, including a historical link; historical evidence inside `docs/` retains its existing citation and retention rules. Plain-text paths that preserve a current authority dependency also fail semantic review. An executable machine input is allowed only through the exact exception below. A machine exception is enumerated by exact **consumer + target + access kind**, with no blanket wildcard for a directory, file type, or provider. Current consumers include `.agents/knowledge/domains.md`, `.agents/README.md`, relevant role/skill bodies, `infrastructure/README.md`, provider notes, `.github/repository-surface.md`, `scripts/validate-links-and-owners.py`, and `tests/test_documentation_link_boundary.py`. Generated outputs and existing links are checked together. Historical retained text is not bulk-rewritten; Stage 98 disposition and recovery contracts continue to apply. A successor to ADR-0036 owns the structural change; the old decision remains intact.

### Skill bundles and dedicated validation

`SKILL.md` remains required and is the reachability root for optional `scripts/`, `references/`, and `assets/` resources. Existing reachable resources are already allowed. The current narrow prohibitions on `assets/*.template.md` and registering a skill-local script as a global gate must be revised only for a demonstrated dedicated output template or dedicated validator. A resource must be regular, inside its package after path resolution, reachable through a valid declared reference, and free of orphan, duplicate-owner, symlink escape, or unsafe suffix ambiguity. Transitive references are checked through a bounded, cycle-safe traversal; an arbitrary directory-name blacklist is not the contract. The shared `scripts/validation/registry.json` remains the exclusive owner of global gate selection, argv, profile membership, and PASS/FAIL meaning; it may explicitly call an approved skill-owned checker. `scripts/validate-agent-governance.py`, `scripts/validate-affected-surfaces.py`, their positive and negative fixtures, pre-commit, and CI consumers must agree. Dedicated asset placement does not transfer approval authority to a skill.

### External service contract audit

The proposed skill audits existing selectorless Service and EndpointSlice declarations and their service consumers without contacting endpoints or reading secret values. It joins Service namespace/name/port/protocol with **all** matching EndpointSlices via `kubernetes.io/service-name`, validates address type, endpoints and named backend ports, and reports missing, ambiguous, conflicting, malformed, mismatched, or path-escaping declarations. Multiple EndpointSlices per Service are valid, including repeated identical endpoints across slices, which the aggregate deduplicates. Every named Service port must have compatible aggregate backend coverage; an endpoint with incompatible protocol or target port is rejected. A Service frontend port may differ from a backend endpoint port. The current Valkey example is Service `6379` to backend `26379`; PostgreSQL write/read `15432`/`15433`, Loki `3100`, Tempo `3200`, and Alloy `4317`/`4318` provide secret-free fixtures. Selector-managed Services are not falsely judged by the selectorless join. Namespace, label, named-port, protocol, addressType, and supported address forms must agree; invalid YAML or absent required references fail deterministically. The checker emits bounded, redacted path/field diagnostics and a nonzero exit on a required contract failure.

The skill's reference material covers actual HTTP(S) OpenBao/Prometheus/Grafana, TCP PostgreSQL/Valkey, and OTLP Alloy contracts: owner, endpoint/address and port shape, secret **reference names** only, access boundary, protocol-specific failure/retry owner, and local declaration link. It does not duplicate `k8s-validate` schema checks, `k8s-security-audit` security posture, ESO/Vault secret handling, or Rego policy. `k8s-implementer` uses the result before a scoped GitOps edit; `gitops-reviewer` uses it for independent structure review; network and observability reviewers may reuse the report. No new agent is created.

### Knowledge, handoff, model, and hooks

`.agents/knowledge/` currently routes by pointer, while reviewed recurring facts may already be promoted to canonical policies, skills, operations, or reference owners. A proposed bounded domain fact record contains `owner`, `scope`, `source`, `observed_at`, `valid_for`, `invalidated_by`, `review_status`, and `sensitivity`; it states whether it is advisory, current at its owner, expired, or withdrawn. It never duplicates a policy body or grants authority. Before promotion, correction, or deletion, the actor rechecks the current source, owner, sensitivity, and approval state. Secret values, personal data, raw transcripts, and stale approvals cannot enter it. A derived cache is invalidated when source HEAD/hash, scope, approval, or validity changes.

The existing quality-policy handoff is extended through its current Task and prompt consumer, not a central ledger. Resume must identify branch, worktree, HEAD/divergence base, relevant file hashes, staged/unstaged status, changed consumers, current approval and revocation state, completed/failed/DEFER lanes, command limits, partial output, remaining work, rollback, next owner, and budget state when known. A stale branch/HEAD/hash, revoked approval, concurrent writer, missing/redacted source, expired fact, or partial subprocess result blocks dependent mutation and names the next owner. Rechecking is required even when the saved note says PASS. The handoff does not echo secret or full subprocess output.

Task profiles select the existing model tier based on risk and complexity; a selection never changes a role's permission class. Provider files bind only supported model and reasoning values. The selected model is confirmed in an authorized native run before runtime claims; failed/unsupported model and unavailable account cost, RPM, TPM, subscription or API-budget observations are `DEFER` with owner and retry trigger. Prose budgets are advisory, not native hard enforcement. A bounded cost/retry check must exercise unsupported model or rejected attempt, elapsed budget exhaustion, shared-budget contention, `Retry-After`, and no implicit move to a more expensive model. Parallelism, retry, and cost controls use observed limits; no speculative generic model runner or native config key is added. `scripts/prompt-input.py` must bound subprocess output **during capture**, preserve explicit truncated/failed evidence, and avoid converting an incomplete success stream to an apparent complete result. Hook adapters keep their current shared guard and must prove static payload shape and exit behavior separately from reviewed trust state, native event delivery, and actual sandbox enforcement.

## Core Design

Implementation follows the accepted owner graph without a broad tree rewrite. First, the successor ADR and current policy/validator consumers settle R23 and the narrow skill bundle exception. Then role-skill-projection references, domain knowledge/handoff, dedicated external-service skill and its gate, evaluation ownership, and command consumers change in logical units. The approved Plan will order those units and name rollback/commit boundaries; this Spec does not authorize or pre-write that Plan.

A feature-to-role map remains: `k8s-implementer` authors scoped bootstrap/GitOps changes; `gitops-reviewer`, `network-reviewer`, `observability-reviewer`, and `security-auditor` independently review their evidence; `ci-workflow-engineer` owns hosted CI configuration; `repo-tooling-engineer` owns non-gate tooling; `quality-engineer` owns validation registration/results; `architect` owns Stage 02 structure; `doc-writer` writes only a settled delegated document; `wiki-curator` routes navigation; `incident-responder` owns triage/RCA; `supervisor` resolves disputed ownership. Bootstrap and live reconciliation remain operator actions. Policy `policy/conftest`, secret references under GitOps/Vault, external services, and examples keep their specialist review boundaries. No role receives live cluster authority from a skill or example.

## Data Modeling & Storage Strategy

- Durable role and skill identities remain in `.agents/roles/registry.json`; procedure bodies remain under `.agents/skills/<id>/`. Manual Claude/Codex projections and symlinks/sidecars are derived from that registry but are tracked files, not generated artifacts.
- Stage 03 Spec/Plan/Task remains the work package; the approved Plan and linked Tasks now own execution. The temporary investigation inventory and design report are evidence for authoring only and do not become a second durable owner.
- Current root `evals/` contains README plus 19 JSON cases and 19 synthetic responses, all agent-governance cases. Move this entire corpus and its exclusive grader `scripts/run-agent-evaluations.py` under `.agents/evaluations/` with `agent-evaluator` ownership only after approval. Keep shared regression tests in `tests/` and gate registration in `scripts/validation/registry.json`; update case paths, `.agents/README.md`, `scripts/README.md`, `tests/test_agent_evaluations.py`, `tests/archive_generation_fixture.py`, knowledge map, and all exact consumers atomically. Do not retain an empty root `evals/`. A split tree has no current product/model corpus; leaving root unchanged preserves ambiguous ownership. The same 19 expected failure sets must match before and after; synthetic case text is data, never an instruction.
- A bounded fact record, if approved, stays in the existing knowledge/owner contract with explicit invalidation, not a new progress ledger or private global cache. Retained Stage 98 bodies and Git recovery objects remain immutable.

## Interfaces & Data Structures

| Interface | Input | Output / owner | Compatibility and safety |
| --- | --- | --- | --- |
| Role registry → native projection | registered role, class, skill refs, provider bindings | one registered projection per admitted provider | Reject missing/extra projection, unauthorized permission increase, invalid model/skill reference; preserve manual tracking. |
| Skill bundle validator | `SKILL.md`, linked relative resources, registry gate reference | accepted resource graph or deterministic error | Traverse transitive links cycle-safely, reject unresolved references/escape/orphan/symlink misuse; approved dedicated template/validator only. |
| External-service checker | scoped tracked YAML paths and declared selectorless Service/EndpointSlice relation | redacted structured findings and exit code | Multiple slices, differing frontend/backend ports, names/protocol/address types; no runtime call or secret value. |
| Link/owner validator | current authored/provider/script consumers, normalized references | exact authority dependency finding | Permit only enumerated consumer/target/access-kind machine exceptions; preserve historical evidence semantics. |
| Handoff/prompt input | snapshot, current approval, bounded subprocess result | Task evidence and next-owner decision | Fail closed on stale/revoked/partial/over-limit state; no credentials or raw transcript. |
| Eval grader | agent case JSON and synthetic response | exact expected failure set per case | Preserve 19-case baseline after location move; untrusted case text never dispatches a tool. |
| QA runner | registry-selected lane and exact working-tree/index/base input | PASS/FAIL/SKIP/DEFER with snapshot identity | No silent fallback; local/full, staged, hosted, native and live are separate. |

Native skill exposure follows each provider's actual discovery and invocation contract: `.claude/skills` symlinks to canonical packages; Codex scans project `.agents/skills` and current `agents/openai.yaml` declares explicit-only invocation. Exact known package existence is not runtime selection. `/skill-stocktake` is unavailable in the investigated catalog; repository-scoped inventory and evals supply equivalent local evidence without global cache writes. Use an installed `skill-creator` package explicitly only after the new skill is approved, distinguishing system and user-local copies.

## Edge Cases & Error Handling

- Reject broken, unresolvable cyclic, escaping, or unsupported skill-resource references, but accept legitimate cycle-safe transitive traversal and dedicated resources under their owner. Registering an unreviewed skill script as a global gate fails.
- Reject a normalized individual numbered-stage authority dependency outside `docs/` even when hidden in reference/HTML/wiki syntax, blob/raw URL, URL encoding, case variation, or separator variation. Historical citations outside `docs/` do not receive a direct-link exception; enumerated machine reads receive only their exact exception, never a wildcard.
- Accept multiple valid EndpointSlices for one selectorless Service, repeated identical endpoints deduplicated in the aggregate, split multiport Alloy coverage, and differing Service/backend ports. Reject an unmatched service name or namespace, conflicting duplicate endpoint/port, missing aggregate named-port coverage, protocol/target-port or addressType mismatch, malformed manifest, invalid address, and accidental selector-managed classification. Never print Secret data.
- Reject stale handoff HEAD/file hash/branch, revoked or missing approval, conflicting writer, expired fact, deleted source, or a partial/truncated subprocess result before a dependent write. The failure states the source and next owner without exposing values.
- A missing required validator, schema, provider runtime, or hosted run cannot silently become PASS. Optional tools may SKIP with a reason; absent authority or environment is DEFER. Static projection parity does not imply native discovery/hook delivery.
- A CI/command migration must retain its required check and exit semantics until all callers are converted. Editor command IDs and `.vscode/` remain uncreated until an installed editor and actual consumer are observed.

## Failure Modes & Fallback / Human Escalation

Each logical implementation unit preserves the prior owner and caller route until new positive and negative tests pass and consumer-zero is verified. On a failed validator, stop and repair the current owner; do not weaken a gate or reroute errors to SKIP. On ambiguous document or policy ownership, `supervisor` resolves routing and `architect` owns structural decisions; `doc-writer` does not decide either. On unavailable native trust, authentication, model, account budget, hosted CI, or live authority, mark that lane DEFER with owner and retry trigger. A failed resume or partial output returns to an operator-reviewed Task checkpoint. Operator-only changes include any `governance-steward` self-contract revision, protected external action, or live secret/cluster operation.

## Verification Commands

The later approved Plan must run focused T01–T33 cases, then the applicable affected/staged/full quality sequence on exact changed bytes. Baseline at `efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`: `python3 scripts/validate-agent-governance.py --root .` passed with 2 providers, 17 roles, 4 classes, 17 skills, 67 handoffs and 51 projections; `python3 scripts/run-agent-evaluations.py --root .` passed 19 synthetic expected-failure sets (0 recorded agent responses, 12 negative cases). These are repository-static baseline results, not this draft's post-change verification. `python3 scripts/qa.py full` passed 22/22 gates on the same unchanged main snapshot of 1,234 tracked paths, including unit discovery, agent-evaluation cases, and one manual-stage pre-commit gate. It cannot be reused for this draft or later modified bytes. Hosted CI, native provider, and live lanes were not run.

After implementation, run focused validator and test commands named in the Plan, `python3 scripts/qa.py quick` for affected working-tree bytes, `python3 scripts/qa.py staged` for each exact logical index, and `python3 scripts/qa.py full` once on the final working tree. Inspect `git diff --check` and cached diff before each requested commit. CI requires its immutable checkout SHA and run identity; native provider and live checks require separate authorized observations. The QA registry owns actual argv and gate membership; this Spec does not duplicate its mutable gate count or limits.

## Success Criteria & Verification Plan

Each criterion below is testable after an approved Plan. `T01`–`T33` retain the **original meanings** from the supplied `08-수용시험-시나리오.md`; they are planned intents, not present test files or executed PASS claims. A criterion may require several original scenarios.

| Criterion | Observable acceptance condition | Planned test |
| --- | --- | --- |
| VAL-ACS-001 | Registry/role/permission/skill/handoff map has one current owner; all 17 roles have explicit keep/modify disposition and no unjustified new role. | T10, T28 |
| VAL-ACS-002 | All 17 skill packages have explicit keep/modify disposition, actual consumer, and no unjustified merge/deletion. | T03, T04, T22, T29 |
| VAL-ACS-003 | Shared policy has one owner per rule and documented exception; duplicate or contradictory current authority fails. | T21 |
| VAL-ACS-004 | Claude/Codex hook payload, exit, failure and trust boundaries are separated from runtime delivery claims. | T12, T24 |
| VAL-ACS-005 | Native projections match admitted registry roles and preserve least privilege; no manual projection is called generated. | T10, T30 |
| VAL-ACS-006 | Knowledge routes to current source with review/expiry metadata and no duplicate authority. | T25 |
| VAL-ACS-007 | Four prompt contracts and Claude adapters preserve inputs, outputs, forbidden conditions, and failures. | T26 |
| VAL-ACS-008 | Both common workflows state entry, branch, approval, stop, partial failure, resume and terminal condition without copying skill bodies. | T21, T26, T31 |
| VAL-ACS-009 | CLI, slash, hook, CI and observed editor entrypoints have caller, args, cwd, output, exit, timeout, side-effect and privilege contracts; deleted aliases have zero callers. | T06, T32 |
| VAL-ACS-010 | Shared result fields survive each provider's supported output style; presentation grants no authority. | T27 |
| VAL-ACS-011 | Current role/skill/adapter/policy/validator contradictions close at one owner with consumers updated. | T03 |
| VAL-ACS-012 | Dedicated skill references/scripts/assets/templates are reachable and safe; global gate selection stays central. | T01, T02, T04, T05, T06, T24, T29 |
| VAL-ACS-013 | Risk/complexity profile selects a supported model without changing permission; unknown cost/RPM/TPM is DEFER. | T11, T13, T30 |
| VAL-ACS-014 | Bounded facts carry all eight metadata keys and invalidation/review lifecycle; secrets and stale approval are rejected. | T14, T15, T25 |
| VAL-ACS-015 | Both provider adapters preserve common semantics; static parity and runtime result remain separate. | T11, T12, T23, T30 |
| VAL-ACS-016 | Gateway, project and scoped instruction precedence matches actual provider behavior without copied policy. | T13, T27 |
| VAL-ACS-017 | Git pre-commit, commit-msg, pre-push and QA lane boundaries retain failure propagation and exact input scope. | T16, T32 |
| VAL-ACS-018 | Editor shortcut/command changes occur only for an observed installation and consumer; otherwise recorded DEFER. | T17, T32 |
| VAL-ACS-019 | API/subscription, rate/cost and retry controls state measurement/approval limits without false hard enforcement. | T05, T18 |
| VAL-ACS-020 | CI QA and independent metadata/release workflows retain required checks, least privilege and immutable action identities. | T12, T16, T19, T23, T24, T31 |
| VAL-ACS-021 | Issue/Project tracking uses a real observed consumer; no unapproved external tool integration is required. | T19 |
| VAL-ACS-022 | Handoff invalidates stale branch/HEAD/hash/approval/cache and stops concurrent or partial resume safely. | T14, T15, T26 |
| VAL-ACS-023 | Current outside-doc authority references route through the current owner/README; normalized syntax and exact machine exceptions pass. | T07, T08, T09 |
| VAL-ACS-024 | Skill improvement cites primary source guidance and separates source evidence from local convention and native behavior. | T04 |
| VAL-ACS-025 | Valid skill-local dedicated templates/checkers are admitted; orphan, escape, unsafe argv, and unregistered gate remain rejected. | T01, T02 |
| VAL-ACS-026 | Single-skill assets live with that package; shared libraries remain shared only for independent domain consumers. | T01, T02, T03, T29 |
| VAL-ACS-027 | New external-service skill proves unique gap, real consumers, correct Service/EndpointSlice join and safe diagnostics; no extra agent. | T04, T22, T29 |
| VAL-ACS-028 | Infrastructure/GitOps/network/observability/secret/external-service/CI/docs responsibilities have no orphan or privilege widening. | T10, T28 |
| VAL-ACS-029 | External agency patterns are adapted only after local gap, permission and evaluation checks; license obligations preserved for copied material. | T10, T22, T30 |
| VAL-ACS-030 | Governance covers execution, approval, quality, docs, Git, provider and incident boundaries with a single owner each. | T21, T24 |
| VAL-ACS-031 | Shared contracts and admitted provider files are placed at correct owners; absent surfaces remain absent without consumers. | T07, T08, T11, T13, T23 |
| VAL-ACS-032 | Homogeneous 19-case eval corpus/grader moves atomically with all consumers and identical expected failure sets; synthetic instructions remain data. | T20 |
| VAL-ACS-033 | Stale versions/paths/claims are corrected and static/native/hosted/live statements match observed evidence. | T09, T21, T25, T33, T05, T06 |

R35–R39 are cross-cutting completeness checks over the same criteria and the original scenario mapping below. R35 uses T28; R36 uses T29 and T33; R37 uses T30; R38 uses T31; R39 uses T32 and T33. No group is complete from prose alone. The final implementation must report changed paths, consumer conversions, passing checks, deferred runtime lanes, reviewer disposition, rollback and next owner in its package-local Tasks.

### Original Acceptance Scenario Mapping

These are the 33 supplied scenario IDs and subjects, preserved without reassigning an ID to a new test. Their expected results remain the acceptance conditions in the supplied scenario text and the criteria above. The later Plan binds each to a concrete test command, type, version, and evidence lane.

| Scenario | Original subject | Request aliases / Spec criteria |
| --- | --- | --- |
| T01 | Legitimate skill-owned bundle | R12,R25,R26; VAL-ACS-012, VAL-ACS-025, VAL-ACS-026 |
| T02 | Unsafe resource path | R12,R25,R26; VAL-ACS-012, VAL-ACS-025, VAL-ACS-026 |
| T03 | Ownership and duplication | R02,R11,R26; VAL-ACS-002, VAL-ACS-011, VAL-ACS-026 |
| T04 | Trigger, function, and counterexample | R02,R12,R24,R27; VAL-ACS-002, VAL-ACS-012, VAL-ACS-024, VAL-ACS-027 |
| T05 | Missing required tool | R12,R19,R34; VAL-ACS-012, VAL-ACS-019, VAL-ACS-033 |
| T06 | Working directory and error contract | R09,R12,R34; VAL-ACS-009, VAL-ACS-012, VAL-ACS-033 |
| T07 | Forbidden document link | R23,R31; VAL-ACS-023, VAL-ACS-031 |
| T08 | Allowed document navigation | R23,R31; VAL-ACS-023, VAL-ACS-031 |
| T09 | Plain-text authority dependency | R23,R33,R34; VAL-ACS-023, VAL-ACS-033 |
| T10 | Role scope and delegation | R01,R05,R28,R29; VAL-ACS-001, VAL-ACS-005, VAL-ACS-028, VAL-ACS-029 |
| T11 | Canonical-to-native mapping | R13,R15,R31; VAL-ACS-013, VAL-ACS-015, VAL-ACS-031 |
| T12 | Hook error and re-entry | R04,R15,R20; VAL-ACS-004, VAL-ACS-015, VAL-ACS-020 |
| T13 | Native trust and discovery | R13,R16,R31; VAL-ACS-013, VAL-ACS-016, VAL-ACS-031 |
| T14 | Stale handoff | R14,R22; VAL-ACS-014, VAL-ACS-022 |
| T15 | Memory promotion and deletion | R14,R22; VAL-ACS-014, VAL-ACS-022 |
| T16 | Partial staging and Git hooks | R17,R20; VAL-ACS-017, VAL-ACS-020 |
| T17 | Editor action | R18; VAL-ACS-018 |
| T18 | Budget, limit, and retry | R19; VAL-ACS-019 |
| T19 | PR and ticket trust boundary | R20,R21; VAL-ACS-020, VAL-ACS-021 |
| T20 | Evaluation cutover | R32; VAL-ACS-032 |
| T21 | Disposition and resume | R03,R08,R30,R33,R34; VAL-ACS-003, VAL-ACS-008, VAL-ACS-030, VAL-ACS-033 |
| T22 | New value and provenance | R02,R27,R29; VAL-ACS-002, VAL-ACS-027, VAL-ACS-029 |
| T23 | Template distribution | R15,R20,R31; VAL-ACS-015, VAL-ACS-020, VAL-ACS-031 |
| T24 | Prevent operational contact | R04,R12,R20,R30; VAL-ACS-004, VAL-ACS-012, VAL-ACS-020, VAL-ACS-030 |
| T25 | Knowledge ownership and currency | R06,R14,R33; VAL-ACS-006, VAL-ACS-014, VAL-ACS-033 |
| T26 | Prompt input/output contract | R07,R08,R22; VAL-ACS-007, VAL-ACS-008, VAL-ACS-022 |
| T27 | Output style and precedence | R10,R16; VAL-ACS-010, VAL-ACS-016 |
| T28 | Preserve responsibility through role changes | R01,R28,R35; VAL-ACS-001, VAL-ACS-028 |
| T29 | Skill consolidation and dedicated bundle transition | R02,R12,R26,R27,R36; VAL-ACS-002, VAL-ACS-012, VAL-ACS-026, VAL-ACS-027, VAL-ACS-025 |
| T30 | Agent names, membership, and permission transition | R05,R13,R15,R29,R37; VAL-ACS-005, VAL-ACS-013, VAL-ACS-015, VAL-ACS-029, VAL-ACS-031 |
| T31 | Workflow consolidation and execution boundary | R08,R20,R38; VAL-ACS-008, VAL-ACS-020 |
| T32 | Command addition, removal, and compatibility transition | R09,R17,R18,R39; VAL-ACS-009, VAL-ACS-017, VAL-ACS-018, VAL-ACS-033 |
| T33 | Reproduce recent path and version changes | R33,R34,R36,R39; VAL-ACS-033, VAL-ACS-002, VAL-ACS-012, VAL-ACS-025, VAL-ACS-009, VAL-ACS-017, VAL-ACS-018 |

## Traceability

The full user request alias mapping below prevents an item from disappearing into a grouped paragraph. Current Requirement IDs remain the durable need; criterion IDs are this Spec's acceptance contract. ADR-0047 is an accepted scoped amendment; the approved Plan bounds implementation.

### Request Alias Traceability

| Request alias | Spec criterion / planned test |
| --- | --- |
| R01 | VAL-ACS-001; T10, T28 |
| R02 | VAL-ACS-002; T03, T04, T22, T29 |
| R03 | VAL-ACS-003; T21 |
| R04 | VAL-ACS-004; T12, T24 |
| R05 | VAL-ACS-005; T10, T30 |
| R06 | VAL-ACS-006; T25 |
| R07 | VAL-ACS-007; T26 |
| R08 | VAL-ACS-008; T21, T26, T31 |
| R09 | VAL-ACS-009; T06, T32 |
| R10 | VAL-ACS-010; T27 |
| R11 | VAL-ACS-011; T03 |
| R12 | VAL-ACS-012; T01, T02, T04, T05, T06, T24, T29 |
| R13 | VAL-ACS-013; T11, T13, T30 |
| R14 | VAL-ACS-014; T14, T15, T25 |
| R15 | VAL-ACS-015; T11, T12, T23, T30 |
| R16 | VAL-ACS-016; T13, T27 |
| R17 | VAL-ACS-017; T16, T32 |
| R18 | VAL-ACS-018; T17, T32 |
| R19 | VAL-ACS-019; T05, T18 |
| R20 | VAL-ACS-020; T12, T16, T19, T23, T24, T31 |
| R21 | VAL-ACS-021; T19 |
| R22 | VAL-ACS-022; T14, T15, T26 |
| R23 | VAL-ACS-023; T07, T08, T09 |
| R24 | VAL-ACS-024; T04 |
| R25 | VAL-ACS-025; T01, T02 |
| R26 | VAL-ACS-026; T01, T02, T03, T29 |
| R27 | VAL-ACS-027; T04, T22, T29 |
| R28 | VAL-ACS-028; T10, T28 |
| R29 | VAL-ACS-029; T10, T22, T30 |
| R30 | VAL-ACS-030; T21, T24 |
| R31 | VAL-ACS-031; T07, T08, T11, T13, T23 |
| R32 | VAL-ACS-032; T20 |
| R33 | VAL-ACS-033; T09, T21, T25, T33 |
| R34 | VAL-ACS-033; T05, T06, T09, T21, T33 |
| R35 | VAL-ACS-001, VAL-ACS-028; T28 |
| R36 | VAL-ACS-002, VAL-ACS-012, VAL-ACS-025–027; T29, T33 |
| R37 | VAL-ACS-005, VAL-ACS-013, VAL-ACS-015, VAL-ACS-029, VAL-ACS-031; T30 |
| R38 | VAL-ACS-008, VAL-ACS-020; T31 |
| R39 | VAL-ACS-009, VAL-ACS-017, VAL-ACS-018, VAL-ACS-033; T32, T33 |

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-001 | T10, T28: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-002 | T03, T04, T22, T29: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-003 | T21: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-004 | T12, T24: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-005 | T10, T30: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-006 | T25: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-007 | T26: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-008 | T21, T26, T31: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-009 | T06, T32: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-010 | T27: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-011 | T03: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-012 | T01, T02, T04, T05, T06, T24, T29: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-013 | T11, T13, T30: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-014 | T14, T15, T25: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-015 | T11, T12, T23, T30: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-016 | T13, T27: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-017 | T16, T32: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-018 | T17, T32: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-019 | T05, T18: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-020 | T12, T16, T19, T23, T24, T31: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-021 | T19: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-022 | T14, T15, T26: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-023 | T07, T08, T09: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-024 | T04: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-025 | T01, T02: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-026 | T01, T02, T03, T29: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-027 | T04, T22, T29: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-028 | T10, T28: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-029 | T10, T22, T30: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-030 | T21, T24: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-031 | T07, T08, T11, T13, T23: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-032 | T20: named focused fixture/review, then affected/staged/full QA as applicable |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ACS-033 | T09, T21, T25, T33, T05, T06: named focused fixture/review, then affected/staged/full QA as applicable |

### Related Inputs and Documents

- Current requirement: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md). Current architecture: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Existing decision: [ADR-0036](../../02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md); accepted scoped amendment [ADR-0047](../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md) governs the amended boundaries.
- Stage 03 [index](../README.md) and [Stage 99 authoring contract](../../99.templates/README.md) own navigation and form. The [approved Plan](plan.md) records implementation order; the Tasks below own execution evidence.

### Execution Tasks

- [TSK-0001: Document lifecycle and approval](tasks/tsk-0001-lifecycle-and-approval.md)
- [TSK-0002: Document authority and normalized links](tasks/tsk-0002-document-authority-links.md)
- [TSK-0003: Skill resource and central gate ownership](tasks/tsk-0003-skill-resource-ownership.md)
- [TSK-0004: External service contract audit](tasks/tsk-0004-external-service-contracts.md)
- [TSK-0005: Knowledge, resume and bounded prompt input](tasks/tsk-0005-knowledge-and-handoff.md)
- [TSK-0006: Role and provider contract alignment](tasks/tsk-0006-role-and-provider-contracts.md)
- [TSK-0007: Evaluation owner cutover](tasks/tsk-0007-evaluation-owner-cutover.md)
- [TSK-0008: Final verification and handoff](tasks/tsk-0008-final-verification.md)
