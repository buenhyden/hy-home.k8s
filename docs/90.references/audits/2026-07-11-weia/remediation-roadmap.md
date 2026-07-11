---
title: 'Audit: Integrated Remediation Roadmap'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Audit: Integrated Remediation Roadmap

## Overview

이 문서는 2026-07-11 implementation audit의 5개 보고서에서 나온 실행 가능
행 80개를 근본 원인과 후속 소유자 기준으로 32개 canonical finding으로
정규화한 통합 로드맵이다. 원 보고서는 관찰 SHA의 사실과 점수를 계속
소유하며, 이 문서는 중복 제거, 의존 순서, 목표 운영 모델, 선택지와 후속
SDLC 경로만 소유한다.

## Purpose

- Give every non-implemented audit row exactly one canonical disposition.
- Order remediation by safety, integrity, dependency, and evidence readiness.
- Select a proportionate target operating model without importing every external
  practice.
- Route active changes to future approved PRD, ARD, ADR, Spec, Plan, Task, Guide,
  Policy, or Runbook owners; Stage 90 authorizes none of those changes.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Source checked: 2026-07-11
- Refresh trigger: any owner report, disposition, dependency, target-state decision,
  or linked follow-up evidence changes.

## Authority Boundary

- **Authoritative for**:
  - Cross-report canonical finding IDs, de-duplication, dependency order,
    target-state recommendation, and follow-up routing.
  - Mapping all 80 actionable source rows to one disposition.
- **Not authoritative for**:
  - Repository facts, counts, scores, provider availability, live readiness, or
    finding evidence owned by the five source reports.
  - Active requirements, architecture decisions, specifications, plans, tasks,
    guides, policies, runbooks, code, configuration, manifests, credentials, or
    operations.

## Scope

- Includes actionable findings from Tasks 7-11, historical `HL-001` through
  `HL-007`, retained `SEC-001` through `SEC-014`, the 2026-07-05 roadmap, target
  operating model, alternatives, phases, adoption gates, and exact acceptance
  routes.
- Excludes rewriting source-report evidence, duplicating volatile inventory or
  availability facts, implementing active controls, live/provider/remote checks,
  and changing historical audit bodies.

## Definitions / Facts

### Normalization Rules

- A canonical finding groups source rows only when they share one root cause,
  dependency chain, and first follow-up owner. Secondary reports remain linked
  evidence, not co-owners.
- The owner report is the sole fact/score owner. This roadmap records source row
  IDs rather than repeating time-sensitive observations.
- Priority is the highest source priority in the group. A lower-priority row can
  depend on a higher-priority canonical finding without being promoted by prose.
- `Historical mapping` means lineage, not closure. `HL-*` findings are superseded
  by the current audit controls; current `SEC-*` findings are retained and none is
  claimed closed.
- Proposed artifact names are code literals until approved and created.

### Canonical Finding Register — 1 of 2

| Canonical ID | Owner report and source rows | Root cause and evidence pointer | Priority | Dependencies | Historical mapping | Disposition / first owner |
| --- | --- | --- | --- | --- | --- | --- |
| RMD-001 | [Platform/security](kubernetes-infrastructure-security.md), SEC-006 | Secret-bearing bootstrap lacks a verified-TLS default and expiring break-glass contract; evidence remains in the owner row. | P0 | None | Current finding retained; 2026-07-05 secret/live route narrowed | Adopt: Stage 03 Spec `vault-eso-transport-and-secret-exposure-hardening`. |
| RMD-002 | [Platform/security](kubernetes-infrastructure-security.md), SEC-008 | Secret values cross observable process boundaries; no protected input/cleanup/redaction contract exists. | P0 | None | Current finding retained; supersedes generic secret-evidence summarizer wording | Adopt: same Stage 03 security Spec, separate acceptance case. |
| RMD-003 | [Platform/security](kubernetes-infrastructure-security.md), SEC-007, SEC-009 | Vault/ESO transport, identity, version, audience, rotation, and rollback are not one verified compatibility contract. | P1 | RMD-001, RMD-002 | Current findings retained | Adopt: same Stage 03 security Spec after safe bootstrap design. |
| RMD-004 | [Governance/provider](governance-harness-loop-providers.md), GOV-002 | Active roster/currentness prose and canonical owner pointers can drift from the adapter inventory. | P1 | None | Supersedes actionable remainder of HL-001 | Adopt: Stage 03 Spec `governance-owner-and-roster-currentness`. |
| RMD-005 | [Governance/provider](governance-harness-loop-providers.md), GOV-006 | Secondary integration summaries and Current labels lack one tested pointer contract. | P2 | Task 13 index reconciliation | Maps 2026-07-05 README/index checker | Adopt minimally: Stage 03 Spec `governance-reference-integration-consolidation` only if Task 13 leaves a repeatable gap. |
| RMD-006 | [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md), DOC-001, DOC-004, LIN-003, LIN-004, LIN-005, FM-004 | Path links and scalar status do not prove requirement-to-criterion-to-result coverage or consistent cross-stage lifecycle state. | P1 | RMD-004 | No older ID; consolidates six current rows | Adopt: Stage 03 Spec `sdlc-semantic-lineage-and-lifecycle-enforcement`. |
| RMD-007 | [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md), LIN-006 | Forward/reverse lifecycle transitions lack reusable approver, reason, evidence, and immutable-archive rules. | P1 | RMD-006 | No older ID | Adopt: Stage 03 Spec `sdlc-state-transition-evidence`. |
| RMD-008 | [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md), LIN-001, LIN-002 | Historical numbering exceptions and reciprocal handoffs are linked but not deterministically reconciled. | P2 | RMD-006 | Historical mismatches preserved, not renamed | Adopt: Stage 03 Spec `sdlc-numbering-and-lineage-exceptions`, then Stage 04 Task `sdlc-link-and-state-reconciliation`. |
| RMD-009 | [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md), FM-002, FM-006, FM-007 | Authored value semantics do not distinguish valid titles/dates from placeholders or invalid/future dates. | P1 | RMD-006 | No older ID | Adopt: Stage 04 Task `frontmatter-value-validation`. |
| RMD-010 | [Lifecycle/frontmatter](sdlc-document-lifecycle-frontmatter.md), DOC-010, DOC-011 | Incident and Postmortem routes exist without a non-fabricated readiness exercise and action-closure proof. | P2 | RMD-006 | Replaces generic live-readiness route for this family | Adopt: Stage 04 Task `incident-response-tabletop-readiness`; do not create fake `INC-*` records. |
| RMD-011 | [CI/QA](ci-qa-automation-pipeline-workflow.md), CICD-005 and QA-015; secondary [platform/security](kubernetes-infrastructure-security.md), SEC-001 and SEC-002 | No executable path-to-validator dependency model joins CI selection, bounded local feedback, and explicit DEFER semantics. | P1 | RMD-004 | Current security findings retained; consolidates 2026-07-05 QA/GitOps summarizers | Adopt: Stage 03 Spec `path-to-validator-and-affected-surface-contract`. |
| RMD-012 | [Platform/security](kubernetes-infrastructure-security.md), SEC-003 and SEC-011; secondary [CI/QA](ci-qa-automation-pipeline-workflow.md), QA-007 | Parser/render/schema/tool fallbacks are not one tool-identity and evidence-depth contract, so a narrower lane can be mistaken for stronger proof. | P1 | RMD-011 | Current security findings retained | Adopt: Stage 03 Spec `platform-security-validation-evidence-contract`; Stage 04 shell-parser alignment is a child task. |
| RMD-013 | [CI/QA](ci-qa-automation-pipeline-workflow.md), QA-014 | AI-agent all-files triggers are fragmented across active gateways, workflow, postflight, adapters, and guide. | P1 | RMD-011 | No older ID | Adopt: Stage 03 Spec `ai-agent-validation-obligation-alignment`. |
| RMD-014 | [CI/QA](ci-qa-automation-pipeline-workflow.md), SUP-001; secondary [platform/security](kubernetes-infrastructure-security.md), SEC-012 | Third-party Action execution identity is mutable and pin enforcement is deliberately disabled. | P1 | RMD-011, RMD-012 | Current security finding retained; narrows 2026-07-05 supply-chain route | Adopt: Stage 03 Spec `github-actions-immutable-dependency-identity`. |

### Canonical Finding Register — 2 of 2

| Canonical ID | Owner report and source rows | Root cause and evidence pointer | Priority | Dependencies | Historical mapping | Disposition / first owner |
| --- | --- | --- | --- | --- | --- | --- |
| RMD-015 | [Governance/provider](governance-harness-loop-providers.md), CLA-003, COD-003, GEM-003, COM-002 | Provider parity checks do not cover every provider-required model/tool/effort/scope field, while runtime model resolution remains a separate evidence lane. | P1 | RMD-004, RMD-016 | HL-005/006 context; no runtime claim | Adopt: Stage 04 Task `provider-adapter-semantic-parity`; role-body semantics remain outside this owner. |
| RMD-016 | [Governance/provider](governance-harness-loop-providers.md), HAR-008, CLA-002, COD-002, GEM-001, GEM-002, COM-003 | Provider intent, native registration/config, hook or permission consumption, and availability have no comparable redacted canary contract; Gemini runtime intent and Codex project defaults are undecided. | P1 | RMD-004 | Supersedes HL-005/006; maps 2026-07-05 provider-parity checker | ADR-first, then Stage 04 Task `provider-native-readiness-canaries`; each provider reports independently. |
| RMD-017 | [Governance/provider](governance-harness-loop-providers.md), HAR-007 | No approved per-server MCP ownership, threat, scope, egress, logging, disable, and native-connection evidence contract exists. | P1 | RMD-016 | Supersedes HL-007 | Adopt only for intended servers: Stage 03 Spec `provider-mcp-inventory-and-security`. |
| RMD-018 | [Governance/provider](governance-harness-loop-providers.md), HAR-004; secondary [agents/vibe](ai-agents-model-routing-vibe-coding.md), VIBE-009 | Retry and risk-stop rules lack task-instantiated attempts, changed hypotheses, budgets, terminal reasons, and deterministic non-convergence rejection. | P1 | RMD-013 | Supersedes HL-002 | Adopt: Stage 03 Spec `bounded-retry-and-termination-contract`; the AI risk contract links to it. |
| RMD-019 | [Governance/provider](governance-harness-loop-providers.md), HAR-006; secondary [agents/vibe](ai-agents-model-routing-vibe-coding.md), COMMON-003 | Compaction and role handoff have prose fields but no recoverable, provider-neutral, secret-safe checkpoint/output schema. | P2 | RMD-018 | Supersedes HL-004 | Adopt: Stage 03 Spec `recoverable-compaction-and-handoff-evidence`. |
| RMD-020 | [Agents/vibe](ai-agents-model-routing-vibe-coding.md), ROLE-001, ROLE-002, ROLE-003, ROLE-004, ROLE-005, ROLE-006, ROLE-007, ROLE-008, ROLE-009, ROLE-010, COMMON-005, UP-001, UP-002; secondary [governance/provider](governance-harness-loop-providers.md), HAR-005 | Role quality, safety, cost, refusal, routing, and model fitness lack versioned corpora, incumbent baselines, independent adjudication, and privacy-bounded result evidence. | P1 | RMD-015, RMD-016, RMD-019, RMD-032 | Supersedes HL-003; rejects duplicate-role response | Adopt: Stage 03 Spec `agent-role-contract-and-evaluation`; create only change-justified corpora. |
| RMD-021 | [Agents/vibe](ai-agents-model-routing-vibe-coding.md), COMMON-002, UP-003 | The canonical role/tool taxonomy omits existing reviewers and upstream adaptation lacks a repeated-gap, least-privilege, non-overlap admission gate. | P1 | RMD-004, RMD-020 | Replaces broad upstream persona adoption | Adopt: existing-role taxonomy fixture first; Stage 03 Spec `agent-role-admission-and-upstream-adaptation` only for a concrete proposal. |
| RMD-022 | [Agents/vibe](ai-agents-model-routing-vibe-coding.md), VIBE-001, VIBE-002, VIBE-003, VIBE-005, VIBE-006, VIBE-007, VIBE-008, VIBE-010 | Retained AI-assisted work lacks one R0-R3 risk overlay joining pre-edit criteria, diff/provenance, independent review, least privilege, rollback, human approval, and operator-only execution. | P1 | RMD-013, RMD-016, RMD-018, RMD-019 | New current control; does not create a permission system | Adopt: Stage 03 Spec `risk-bounded-ai-assisted-development`. |
| RMD-023 | [Platform/security](kubernetes-infrastructure-security.md), SEC-004, SEC-005 | Live GitOps/TLS checks do not separate strict readiness from diagnostics or require complete state, trust, timeout, and recovery evidence. | P1 | RMD-003, RMD-012 | Current findings retained; narrows historical live-readiness route | Adopt: Stage 03 Spec `platform-live-assurance-modes`; live Task requires separate approval. |
| RMD-024 | [Platform/security](kubernetes-infrastructure-security.md), SEC-010 | NetworkPolicy desired state has no CNI/version-bound positive and negative behavioral proof with cleanup. | P1 | RMD-012, RMD-023 | Current finding retained | Adopt: Stage 03 Spec `network-policy-behavioral-assurance`; execute only through an approved live Task/Runbook. |
| RMD-025 | [Platform/security](kubernetes-infrastructure-security.md), PLAT-008 | Recovery procedures exist without a time-bound, redacted rehearsal proving sequence and restored reconciliation. | P2 | RMD-023 | Maps historical live-readiness route | Adopt: Stage 04 Task `platform-recovery-rehearsal` after strict-mode fixtures. |
| RMD-026 | [Platform/security](kubernetes-infrastructure-security.md), SEC-013 | Actual image/chart/Action consumers lack a threat-modelled assurance scope; broad SBOM/provenance/scanner adoption has no universal consumer. | P2 | RMD-014 | Current finding retained and narrowed; supersedes broad 2026-07-05 supply-chain proposal | ADR/ARD-first: Stage 02 ARD `platform-supply-chain-assurance-scope`. |
| RMD-027 | [Platform/security](kubernetes-infrastructure-security.md), SEC-014 | Admin-equivalent Argo CD destinations lack one principal/source, review, audit, revocation, and break-glass evidence model. | P1 | RMD-023 | Current finding retained | Adopt: Stage 03 Spec `argocd-admin-boundary-assurance`; quarterly evidence remains read-only and approved. |
| RMD-028 | [Governance/provider](governance-harness-loop-providers.md), HAR-001 | The documented Observe procedure has no named deterministic consumer for common machine-readable task state. | P3 | Phases A-D complete; a later harness Spec identifies the consumer | No older ID; optional task-state evidence lane | Telemetry-gated: Stage 03 Spec `harness-task-state-contract`; representative fixtures record source/evidence lane and owner and reject a missing Observe block without claiming provider execution. |
| RMD-029 | [CI/QA](ci-qa-automation-pipeline-workflow.md), CICD-009 | Application/service delivery metrics lack a named service and valid deployment/failure/recovery/rework event model. | P3 | Phases A-D complete; service, owner, privacy, retention, and events named | Maps the 2026-07-05 DORA proposal route | Telemetry-gated: Stage 03 Spec `service-delivery-metrics-pilot`; one service has documented joins, owner/privacy/retention, five reproducible queries, baseline output, and tests rejecting CI-only proxies. |
| RMD-030 | [CI/QA](ci-qa-automation-pipeline-workflow.md), QA-003 | Tracked Prettier configuration has neither an explicit dormant disposition nor a scoped execution consumer. | P3 | Phases A-D complete; representative dry run and overlap analysis | Replaces generic formatter automation wording | Decision-gated: Stage 03 Spec `prettier-scope-and-consumer-decision`; the dry run quantifies touched paths/conflicts, chooses removal or one pinned scoped consumer, and defines alignment, migration, and rollback. |
| RMD-031 | [CI/QA](ci-qa-automation-pipeline-workflow.md), SUP-008 | Changelog preview retention has no named release/audit consumer and the remote default is unverified. | P3 | Phases A-D complete; consumer proven or transient disposition selected | Maps the 2026-07-05 optional artifact route | Decision-gated: Stage 04 Task `changelog-artifact-consumer-and-retention-decision`; it records the consumer or transient status and tests duration/deletion/rollback or consistent transient labels. |
| RMD-032 | [Agents/vibe](ai-agents-model-routing-vibe-coding.md), COMMON-004 | Generic/static adapter shape can pass while responsibility, outputs, stop rules, prohibited actions, and handoffs drift across intended local role surfaces. | P1 | RMD-004, RMD-016 | Split from provider parity; provider fields stay with RMD-015 | Adopt: Stage 04 Task `local-role-semantic-contract-validation`; positive/negative fixtures cover all ten responsibilities and intended local surfaces, fail wrong/missing semantics or local-body drift, and do not redefine Task 7 provider metadata. |

The register maps all 80 actionable source rows exactly once. Grouping does not
transfer fact ownership: RMD-011, RMD-012, RMD-014, RMD-018, RMD-019, RMD-020,
and RMD-022 explicitly identify secondary reports while retaining one
owner report for the underlying evidence.

### RMD-004 closure evidence

RMD-004 is closed by [Spec 025](../../../03.specs/025-governance-owner-and-roster-currentness/spec.md),
its [implementation Plan](../../../04.execution/plans/2026-07-11-governance-owner-and-roster-currentness.md)
and [evidence Task](../../../04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md),
the durable [harness catalog](../../../00.agent-governance/harness-catalog.md),
and the focused
[`validate-agent-roster-currentness.py`](../../../../scripts/validate-agent-roster-currentness.py)
guardrail. This closure is repository-static and does not change the original
finding, priority, score, or live/provider evidence boundary.

### Historical Lineage Map

| Historical finding or roadmap item | Current canonical disposition |
| --- | --- |
| HL-001 | RMD-004; corrected research fact is accepted, active currentness repair remains. |
| HL-002 | RMD-018. |
| HL-003 | RMD-020, with provider-neutral trial evidence consumed by role evals. |
| HL-004 | RMD-019. |
| HL-005 and HL-006 | RMD-016; static, provider-native, remote, and live lanes remain independent. |
| HL-007 | RMD-017. |
| SEC-001/002/003/011 | RMD-011/RMD-012; retained, not superseded. |
| SEC-004/005/010 | RMD-023/RMD-024; retained, not superseded. |
| SEC-006/007/008/009 | RMD-001/RMD-002/RMD-003; retained, not superseded. |
| SEC-012/013/014 | RMD-014/RMD-026/RMD-027; retained; SEC-013 remains narrowed to actual consumers. |
| 2026-07-05 audit/index, provider, QA, GitOps, secret, live, DORA/optional automation, and supply-chain opportunities | Replaced by RMD-005, RMD-016, RMD-011/RMD-012, RMD-001 through RMD-003, RMD-023 through RMD-025, RMD-028 through RMD-031, and RMD-014/RMD-026 respectively. |

### Target Operating Model

| Responsibility | Canonical owner | Target behavior and review boundary |
| --- | --- | --- |
| Governance | Stage 00 Governance Steward | Own rules, authority, approval boundaries, roster currentness, and canonical pointers; secondary documents link rather than restate. |
| Lifecycle | Stage 01-05 family owners plus Stage 99 route/schema owners | Body-owned semantic lineage and family-state evidence join intent to results; metadata expands only for a named consumer. |
| Harness | Stage 00 harness owners; Stage 03 contract owners | Observe/Plan/Act/Verify/Learn uses bounded retry, recoverable handoff, and explicit evidence lanes without pretending to be a provider runtime. |
| Provider | Provider notes/native adapters plus approved canary Tasks | Native discovery, config, hooks, permissions, models, and MCP are independently evidenced per provider; missing lanes are SKIP, never parity. |
| Agent | Existing ten-role roster and supervisor | Responsibilities stay non-overlapping; role changes and model promotions require semantic fixtures and versioned behavioral evals. |
| Delivery | CI/workflow, scripts, and QA owners | One path-to-validator model defines local RUN/DEFER and CI selection; completion uses exact PASS/SKIP/FAIL evidence. |
| Platform | GitOps/infrastructure owners | Desired state remains Git-owned; strict live assurance and recovery evidence require approved operator Tasks and rollback. |
| Security | Security owner with domain reviewers and human/operator approval | Secret transport/exposure, dependency identity, network behavior, and admin-equivalent access use least privilege and fail-safe defaults. |
| Evidence | Stage 04 Plan/Task owners; source reports remain dated snapshots | Every acceptance result names artifact, command/canary, tool/version, evidence lane, limitation, reviewer, and rollback without secrets. |
| Review | Independent role/domain reviewer; human for protected R2 and operator for R3 | Author evidence cannot self-approve protected work; conflicts, unavailable lanes, rejection, and residual risk stay explicit. |

### Target-State Options

| Option | Cost / benefit | Blast radius | Migration | Rollback | Prerequisites | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Minimal | Low cost; fixes P0 and obvious stale/value/filter defects, but leaves semantic lineage, behavioral eval, and fragmented assurance. | Small, mainly selected scripts/docs/config. | Patch each defect independently. | Revert logical changes. | P0 Spec and targeted Tasks. | Reject as the final state; acceptable only as the Phase A emergency slice. |
| Consolidated | Medium cost; highest cross-report benefit through shared contracts for lineage, validation, provider evidence, AI risk, and platform assurance. | Bounded to named owners and consumers; no repository-wide identifier migration. | Add fixtures and ledgers opt-in, reconcile current exceptions, then enable gates by phase. | Disable new gates/canaries while preserving existing paths and generated mappings. | Approved PRD/ARD/ADR, owner inventory, privacy/redaction rules, fixed fixtures, rollback owners. | **Default.** Lifecycle evidence scores this option highest, and the governance, CI/QA, platform/security, and agent audits independently prefer targeted consolidation. |
| Full redesign | Very high cost with no demonstrated incremental consumer value: universal IDs/metadata, generated adapters, expanded platform/release and assurance systems. | Repository-wide across active stages, templates, validators, adapters, CI, operations, and possibly runtime. | Dual-read/backfill, consumer cutover, compatibility retirement. | Retain old paths/forms and disable new required fields; migration ledger must survive. | Separate ADR, collision/consumer census, stable domains, dual validators, privacy and operational budget. | Defer. Reopen only when repeated failures show Consolidated cannot meet measured acceptance. |

Consolidated is evidence-supported rather than preference-only: the
[lifecycle report Target-State Comparison](sdlc-document-lifecycle-frontmatter.md#target-state-comparison)
scores it `34/40` versus Minimal `31/40` and Full redesign `18/40`; the other
four reports independently recommend consolidated, consumer-bound changes and
reject file-count parity, universal scanner adoption, or role proliferation as
substitutes for evidence.

### Phased Follow-up Routes

| Phase | Canonical findings | First approved route | Exact phase acceptance |
| --- | --- | --- | --- |
| A — executable P0 safety | RMD-001, RMD-002 | Spec `vault-eso-transport-and-secret-exposure-hardening`, then Task `vault-bootstrap-safety-remediation` | An instrumented negative/positive suite proves verified TLS is default, untrusted endpoints fail, no secret appears in argv/env/output/temp capture, break-glass expires, cleanup survives failure/interrupt, and rollback restores the prior revision. |
| B — lifecycle traceability | RMD-004, then RMD-005 through RMD-010 | Spec `governance-owner-and-roster-currentness`, then Spec `sdlc-semantic-lineage-and-lifecycle-enforcement` and Plan/Task `sdlc-traceability-reconciliation` | Currentness fixtures reject stale roster/owner facts before fixed-tree lifecycle fixtures account for every applicable requirement and validation criterion, reconcile state and reciprocal links, reject invalid transitions/placeholders/dates, preserve historical identifiers, and complete a labeled tabletop without a fake incident. |
| C — provider and harness verification | RMD-011, RMD-013, RMD-016, RMD-015, RMD-017, RMD-018, RMD-019, RMD-032, RMD-020, RMD-021, in that dependency order | Spec `path-to-validator-and-affected-surface-contract`, Spec `ai-agent-validation-obligation-alignment`, ADR `provider-runtime-intent-and-canary-boundary`, Task `provider-native-readiness-canaries`, then provider parity, harness, local-role semantic, and role-eval owners | Path selection precedes the active validation rule; provider parity and local role-body semantics have separate fixtures; all intended role surfaces reject semantic drift before role eval; each provider reports native PASS/FAIL/SKIP independently; retry/handoff recovery rehearses; no role/model promotion occurs without a versioned baseline, threshold, adjudicator, cost/latency, and rollback. |
| D — delivery, supply chain, platform evidence, and AI risk | RMD-003, RMD-012, RMD-014, RMD-022, RMD-023, RMD-024, RMD-025, RMD-026, RMD-027, in that dependency order | In order: Spec `vault-eso-transport-and-secret-exposure-hardening` compatibility slice; Spec `platform-security-validation-evidence-contract`; Spec `github-actions-immutable-dependency-identity`; Spec `risk-bounded-ai-assisted-development`; Specs `platform-live-assurance-modes` and `network-policy-behavioral-assurance`; Task `platform-recovery-rehearsal`; ARD `platform-supply-chain-assurance-scope`; Spec `argocd-admin-boundary-assurance` | Each named owner meets its row acceptance before the next dependent route starts: tool/fallback evidence precedes immutable Actions, risk/platform fixtures consume prior contracts, recovery follows strict modes, the supply-chain ARD follows Action evidence, and Argo admin assurance follows live-mode boundaries. |
| E — optional optimization | RMD-028, RMD-029, RMD-030, RMD-031 | Independently: Specs `harness-task-state-contract`, `service-delivery-metrics-pilot`, `prettier-scope-and-consumer-decision`, and Task `changelog-artifact-consumer-and-retention-decision` | Each lane independently meets its own consumer trigger and exact row acceptance or remains deferred. A portfolio ADR may coordinate scheduling only after lane-owner decisions; it is never the first owner or an admission substitute. |

Phase ordering and the left-to-right order inside each row are dependency order, not
a commitment date. Phase A is only the executable P0 safety slice. RMD-022 cannot
start there: Phase D consumes RMD-013 validation, RMD-016 provider, RMD-018 retry,
and RMD-019 recoverable handoff evidence completed in Phase C. RMD-011 likewise
precedes RMD-013 in Phase C, so RMD-012 can consume its path-to-validator contract
in Phase D. No later phase may use static PASS to claim provider, remote, or live
readiness.

### First Canonical Artifact Ladder

Identifiers are assigned atomically by the owning stage after approval; this dated
reference does not reserve numbers. The following names are exact logical routes and
remain code literals until created.

| Artifact | First canonical owner/name | Exact acceptance before handoff |
| --- | --- | --- |
| PRD | Product Manager — `workspace-assurance-remediation` | Names RMD-001 through RMD-032, sponsor, in/out scope, phase outcomes, risk, success metrics, explicit defer/reject decisions, and approval boundaries. |
| ARD | System Architect — `workspace-assurance-operating-model` | Assigns all ten target-model responsibilities, data/evidence flows, trust boundaries, failure modes, dependencies, migration, and rollback with no dual owner. |
| ADR | System Architect — `consolidated-workspace-assurance-target-state` | Records Minimal/Consolidated/Full alternatives, why Consolidated wins, irreversible consequences, reopen triggers, and rollback decision owner. |
| Spec | Security Engineer — `vault-eso-transport-and-secret-exposure-hardening` | Meets RMD-001 through RMD-003 positive/negative/redaction/version/rotation/rollback criteria before any secret-bearing execution. |
| Plan | QA/Tech Lead — `workspace-assurance-remediation-plan` | Orders phases and logical changes, names fixtures/canaries/reviewers, stop conditions, unavailable lanes, migration, rollback, and no-live-without-approval gates. |
| Task | Engineer/QA — `vault-bootstrap-safety-remediation` | Records changed paths, exact commands/results, instrumented zero-secret capture, TLS failures/success, reviewer approval, rollback rehearsal, and residual risk. |
| Guide | Technical Writer — `workspace-assurance-evidence-guide` | A reader can select repo-static/provider/remote/live lanes, interpret PASS/SKIP/FAIL/DEFER, find the canonical owner, and avoid readiness overclaims in tested examples. |
| Policy | Operations/Security — `risk-bounded-ai-assisted-change-policy` | Defines R0-R3 authority, reviewer/human/operator gates, prohibited actions, provenance/privacy, exception expiry, stop conditions, and enforcement owner without duplicating provider permissions. |
| Runbook | Operations Engineer — `secure-vault-eso-bootstrap-and-recovery-runbook` | An approved rehearsal follows preflight, trust setup, protected input, verification, stop, cleanup, rollback, redaction, and postflight steps and restores the declared prior state. |

### Adoption, Rejection, and Reopen Decisions

- **Adopt now through approved SDLC work**: P0 Vault/bootstrap protections;
  canonical currentness; semantic lifecycle; path-to-validator selection;
  risk-based AI work; immutable Action identity; provider-native evidence
  boundaries; strict platform assurance for actual protected consumers.
- **Keep existing families/roles**: PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy,
  Runbook, Reference, README, and the ten-role roster. Improve them through their
  owners and evals rather than duplicating them.
- **Reject now**: a Release family without an ADR/consumer; universal frontmatter
  `id`/`created`/`review_due`/`supersedes`; direct upstream persona memory or thin
  adapter imports; duplicate writer/reviewer/orchestrator, broad DevOps, or live SRE
  roles; automatic CodeQL/dependency-review/SBOM/provenance/Scorecard adoption with
  no applicable artifact and response consumer; provider file-count parity as
  runtime proof.
- **Telemetry-gated**: RMD-028 task-state automation, RMD-029 service-delivery
  metrics, RMD-030 Prettier adoption/removal, and RMD-031 artifact retention;
  FinOps or other new roles; heavier eval automation. Each stays deferred until
  its own consumer and measured threshold exist.
- **ADR-first**: Full redesign; native Gemini CLI adoption or formal non-adoption;
  consequential Codex project-default changes; new Release or environment family;
  platform artifact assurance architecture; any permission/tool expansion or
  roster-generation system.
- **Rejection evidence is durable**: a rejected/deferred proposal records the
  missing consumer or threshold and its reopen trigger. External popularity,
  upstream volume, or tool availability alone never satisfies the trigger.

## Sources

- [Audit pack design and method](README.md)
- [Implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- [Governance, Harness, Loop, and Provider Parity](governance-harness-loop-providers.md)
- [SDLC Document Lifecycle and Frontmatter](sdlc-document-lifecycle-frontmatter.md)
- [CI, QA, Automation, Pipeline, and Workflow](ci-qa-automation-pipeline-workflow.md)
- [Kubernetes Infrastructure and Security](kubernetes-infrastructure-security.md)
- [AI Agents, Model Routing, and Vibe Coding](ai-agents-model-routing-vibe-coding.md)
- [Current research pack](../../research/2026-07-07-wer/README.md)
- [Historical 2026-07-05 roadmap](../2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md)

## Review and Freshness

- Review cadence: on owner report or disposition change
- Last reviewed: 2026-07-11
- Next review trigger: source finding closes/changes, Task 13 index reconciliation,
  approved target-state ADR, new consumer/telemetry, or acceptance evidence lands.
- Refresh method: preserve the prior mapping, reread each owner report at its stated
  observation SHA, account for every actionable row once, and change priority or
  disposition only with linked owner evidence.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- **Parent audits index**: [Audits README](../README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
