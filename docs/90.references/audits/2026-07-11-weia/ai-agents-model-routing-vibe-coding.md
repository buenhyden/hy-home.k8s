---
title: 'Audit: AI Agents, Model Routing, Agency-Agents, and Vibe Coding'
type: content/reference
status: draft
owner: platform
updated: 2026-07-11
---

# Audit: AI Agents, Model Routing, Agency-Agents, and Vibe Coding

## Overview

이 dated implementation audit는 Current research의 로컬 AI 역할, 고정된
`agency-agents` 비교, 역할별 모델 라우팅 가설, risk-bounded vibe-coding 기준을
audit observation SHA의 repository evidence와 대조한다. 이 보고서는 역할 책임,
instruction, tool/permission 의도, output, handoff, eval, upstream adoption, 그리고
vibe-coding 통제를 소유한다.

[Task 7 provider audit](governance-harness-loop-providers.md)는 adapter inventory,
provider/local declaration, native loading/registration, settings/hooks/config,
entitlement와 runtime availability evidence의 단독 소유자다. 이 보고서는 그 사실과
confidence를 링크로 소비하며 provider metadata나 native availability를 다시 세거나
재채점하지 않는다.

## Purpose

- Score each local role's responsibility, instruction, output, handoff, and
  role-specific eval readiness without inferring provider behavior.
- Compare reusable pinned `agency-agents` patterns by responsibility and local need,
  not upstream volume.
- Own conditional role-specific default, escalation, fallback, and eval
  recommendations while leaving active declarations and availability with Task 7.
- Score specification, acceptance, diff, test/static, review, provenance,
  secret/permission, rollback, stopping, and high-risk boundaries for vibe coding.
- Route every active recommendation to a future canonical SDLC owner with measurable
  acceptance evidence.

## Reference Type

- Type: dated-implementation-audit
- Audit observation SHA: `a85df194bbb8ebc61187b905afaef7f95215cc2f`
- Research/model cutoff: `2026-07-10 10:00 KST`
- Pinned upstream revision:
  `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`
- Source checked: 2026-07-11
- Refresh trigger: local role body, role-eval, role-admission, upstream pin/format,
  vibe-control, Task 7 provider facts, or audit-method change.

## Authority Boundary

- **Authoritative for**:
  - The 31 report-local controls and their evidence at the audit observation SHA.
  - Local role responsibility, instruction, tool/permission intent, output, handoff,
    semantic-contract, and evaluation findings.
  - Pinned upstream reuse classifications and role-specific conditional routing
    recommendations.
  - Vibe-coding risk controls and follow-up routes.
- **Not authoritative for**:
  - Active agents, adapters, model policy, tools, permissions, provider settings,
    hooks, configs, CI, scripts, manifests, or live operations.
  - Adapter counts, provider metadata, native loading/registration, account
    entitlement, model resolution, or runtime availability; Task 7 owns those facts.
  - Any claim that a candidate model is locally available, selected, or approved.

## Scope

- Includes the ten existing local role responsibilities and shared body contract,
  pinned upstream pattern comparison, role admission, FinOps threshold, conditional
  role/model routing, and risk-bounded vibe coding.
- Excludes adapter/provider rescoring, credential or secret inspection, provider
  execution, inference benchmarking, remote CI, and live Kubernetes/Argo CD/Vault/ESO
  actions.
- Existing roles are improved before a new role is proposed. Upstream catalog breadth
  is discovery evidence only.

## Definitions / Facts

### Evidence and Scoring Basis

Repository facts are read from audit observation SHA
`a85df194bbb8ebc61187b905afaef7f95215cc2f` with `git show`/`git ls-tree`, not
from the evolving branch. The exact 12 fields and maturity formula come from the
[pack audit method](README.md#audit-method). Static evidence cannot receive maturity
4. Every actionable row has one P0-P3 priority, canonical future owner, and measurable
acceptance evidence; no-action and excluded rows use the exact required value.

The fixed provider inputs are the Task 7 `CLA-*`, `COD-*`, `GEM-*`, and `COM-*`
controls plus their confidence. This report never converts a tracked declaration or
official catalog entry into local availability. All model recommendations below remain
conditional on the Task 7 native canary and the role eval named here.

### Local Role Controls

Every local body has `Runtime Bootstrap`, `Role`, `When to Use`, `Inputs`, `Outputs`,
`Guardrails`, `Handoff / Escalation`, and `Postflight`. The controls below assess the
role contract, not the provider adapter metadata or native execution surface.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ROLE-001 | Current AI-agent research; local supervisor body | Supervisor converts multi-scope work into bounded delegation, assigns completion evidence, synthesizes results, and escalates unsafe or incoherent outcomes. | At the observation SHA, `.agents/agents/supervisor.md` defines routing inputs, delegation rationale/output, governance guardrails, protocol handoff, and postflight; no golden delegation/synthesis eval result exists. | 2 repository-static | Partial | Verified repo-static | Complementary: the role contract is concrete, but routing, termination, long-context retention, and delegated-output synthesis quality are unmeasured. | Add a supervisor eval corpus before changing routing or candidate defaults. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Seeded multi-scope cases measure correct worker selection, scope/approval assignment, termination, evidence completeness, synthesis defects, cost/latency, and rollback against an approved threshold. |
| ROLE-002 | Current AI-agent research; local code-reviewer body | Code review produces read-only, file-evidenced, severity-ranked findings and a bounded verdict, escalating security and GitOps ownership. | `.agents/agents/code-reviewer.md` declares diff inputs, structured findings, severity/verdict outputs, read-only guardrails, and specialist handoffs; no seeded-defect precision/recall record exists. | 2 repository-static | Partial | Verified repo-static | Complementary: output shape is documented but missed-defect, false-positive, severity, citation, and unauthorized-edit behavior are not evaluated. | Add role-specific review fixtures instead of adding a second general reviewer. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | A versioned seeded-defect set reports false-negative/positive rates, severity agreement, valid file citations, no unauthorized edits, and explicit escalation accuracy. |
| ROLE-003 | Current AI-agent research; Stage 99 routing | Documentation work selects one canonical route/template, preserves metadata/headings/indexes, cites sources, validates links, and escalates ownership ambiguity. | `.agents/agents/doc-writer.md` names document inputs, template/path/metadata/Related Documents outputs, draft-state and README/index guardrails, validation evidence, and supervisor/incident handoff; no authored-output quality eval exists. | 2 repository-static | Partial | Verified repo-static | Complementary: strong instructions exist, but unsupported-claim, duplication, route-selection, template-completeness, and Korean clarity thresholds are not measured. | Evaluate the existing doc-writer before considering any upstream writer persona. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | Golden document-routing cases score exact target/template, required metadata/headings/index updates, source support, link validity, non-duplication, Korean clarity, and rollback. |
| ROLE-004 | Current AI-agent research; local GitOps reviewer body | GitOps review remains read-only and detects Argo CD target, Kustomize ownership, sync/release risk, AppProject, and secret/RBAC concerns with correct handoffs. | `.agents/agents/gitops-reviewer.md` defines manifest inputs, sync/Kustomize/release-risk outputs, review-only/GitOps-first guardrails, and implementer/security/supervisor handoffs; no seeded GitOps judgment eval exists. | 2 repository-static | Partial | Verified repo-static | Complementary: repository instructions do not quantify missed high-risk ownership/sync findings or reviewer agreement. | Add GitOps-specific evals before any role/model migration or sign-off claim. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Seeded Application/ApplicationSet/Kustomize/AppProject defects meet approved missed-high-risk and false-positive limits, cite exact evidence, refuse live mutation, and agree with an independent domain review. |
| ROLE-005 | Current AI-agent research; incident/postmortem boundary | Incident response reconstructs a faithful timeline, impact, uncertainty, next investigation, and postmortem handoff while remaining read-only and blameless. | `.agents/agents/incident-responder.md` defines logs/symptoms inputs, timeline/impact/remediation outputs, read-only/blameless guardrails, and security/implementation/supervisor handoffs; no tabletop role eval exists. | 2 repository-static | Partial | Verified repo-static | Complementary: timeline fidelity, causal uncertainty, severity, unsafe-action refusal, and recovery-approval handoff are untested. | Include role performance in the separately approved incident tabletop rather than creating a new incident persona. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Tabletop fixtures measure timeline accuracy, unsupported-cause rate, severity, provenance, read-only refusal, security escalation, human approval handoff, and postmortem-ready output. |
| ROLE-006 | Current AI-agent research; local Kubernetes implementer body | Kubernetes implementation writes only bounded GitOps desired state, never plaintext secrets or direct cluster changes, and hands a minimal validation-ready diff to reviewers. | `.agents/agents/k8s-implementer.md` defines target/end-state inputs, manifest and validation-handoff outputs, GitOps/no-secret guardrails, and GitOps/security/supervisor handoffs; no manifest-generation eval corpus exists. | 2 repository-static | Partial | Verified repo-static | Complementary: schema/Kustomize correctness, minimal-diff behavior, secret safety, out-of-scope edits, and review handoff quality are not behaviorally evaluated. | Add fixture-backed manifest authoring evals before changing write authority or model routing. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Representative changes pass schema/Kustomize/static gates, remain inside delegated paths, add no plaintext secret, keep a minimal diff, record failures, and receive independent GitOps/security review. |
| ROLE-007 | Current AI-agent research; local network reviewer body | Network review stays manifest-static and detects ingress, DNS/TLS, routing, and NetworkPolicy structure while escalating isolation/RBAC and forbidding live probes. | `.agents/agents/network-reviewer.md` defines precise paths, `file:line` findings, manifest-static/no-probe guardrails, and security/GitOps/supervisor handoffs; no seeded network eval exists. | 2 repository-static | Partial | Verified repo-static | Corrective: the body is specific, but routing/isolation/TLS false-negative thresholds are absent and Task 7 records incomplete exact-field validator coverage. | Evaluate role judgment and consume Task 7 semantic-parity remediation without duplicating provider metadata. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Seeded ingress/DNS/TLS/NetworkPolicy cases meet an approved missed-high-risk threshold, cite exact lines, perform no live probe, and route isolation/RBAC issues correctly; Task 7 parity acceptance remains linked. |
| ROLE-008 | Current AI-agent research; local observability reviewer body | Observability review stays manifest-static and detects scrape, alert, dashboard, retention, SLO, and error-budget defects without making live-query claims. | `.agents/agents/observability-reviewer.md` defines monitoring/SLO inputs, evidenced findings, no-live-query guardrails, and implementation/security/GitOps/supervisor handoffs; no behavior eval exists. | 2 repository-static | Partial | Verified repo-static | Corrective: SLO/alert interpretation quality and false-negative thresholds are absent, while Task 7 records incomplete exact-field validator coverage. | Adapt SRE vocabulary into the existing role and evaluate it before proposing a broader SRE agent. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | Seeded scrape/alert/SLO/error-budget defects meet approved accuracy thresholds, contain evidence and correct handoff, make no live-state claim, and link Task 7 parity acceptance. |
| ROLE-009 | Current AI-agent research; local security auditor body | Security review remains read-only, reports severity/evidence/remediation, stops on plaintext secret exposure, preserves least privilege, and escalates implementation or incident response. | `.agents/agents/security-auditor.md` defines scoped audit inputs, sign-off/block outputs, stop and least-privilege guardrails, and implementation/incident/supervisor handoffs; no missed-critical eval exists. | 2 repository-static | Partial | Verified repo-static | Complementary: missed-critical rate, severity consistency, secret non-disclosure, refusal, and human approval behavior are unmeasured. | Establish a high-risk security eval and independent human review gate before role/model changes. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | Seeded RBAC/network/secret/policy cases meet a zero-or-approved missed-critical threshold, preserve redaction, refuse unsafe actions, cite evidence, and receive independent/human adjudication. |
| ROLE-010 | Current AI-agent research; local wiki curator body | Wiki curation changes only generated/canonical-owner link surfaces, never creates policy, vector stores, secret access, live mutation, or unrelated artifacts, and hands new durable docs to doc-writer. | `.agents/agents/wiki-curator.md` defines generator/source inputs, link/index outputs, explicit no-policy/no-secret/no-live/no-vector-store guardrails, and doc/security/supervisor handoffs; four core phrases are deterministically checked, but no curation eval exists. | 2 repository-static | Partial | Verified repo-static | Complementary: link-owner accuracy, generator idempotence, stale-link routing, artifact refusal, and rollback quality are not behaviorally measured. | Evaluate the existing wiki-curator before considering an onboarding or knowledge-management persona. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | Fixtures score canonical-owner/link accuracy, generator idempotence, no duplicated policy/vector store/artifacts, correct doc-writer handoff, bounded cost, and clean rollback. |

### Shared Role-System Controls

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COMMON-001 | Current AI-agent research; Subagent Protocol | Every role has one shared body skeleton, explicit scope import, bounded bootstrap, guardrails, handoff/escalation, and postflight without forcing provider metadata equivalence. | Fixed-tree inspection at the observation SHA shows the same eight required sections and role-body contract on the local role surfaces. This is repository-static skeleton evidence only; provider-specific validator depth and native consumption are separate controls. | 2 repository-static | Implemented | Verified repo-static | No missing assessed static skeleton element; validation and native-consumption confidence remain outside this static-shape verdict. | Preserve one shared role-body skeleton and link validator/provider facts to their owning controls. | N/A — no action | N/A — no action | N/A — no action |
| COMMON-002 | Subagent Protocol Tool Scoping; approval boundaries | Role intent assigns supervisor orchestration, every review role to read-only capability, and authoring roles to bounded writes; outer provider permissions and human approval remain separate. | The protocol names role/tool groups but its read-only reviewer list omits `network-reviewer` and `observability-reviewer`; their bodies still say review-only/no live probe or query. Approval boundaries forbid direct live/secret/destructive actions. Task 7 owns provider-native tool metadata and enforcement confidence. | 1 documented/routed | Partial | Verified repo-static | Corrective: two existing review roles lack a canonical protocol tool-group entry even though their bodies state read-only intent; this row does not infer or rescore native enforcement. | Reconcile the protocol's role/tool taxonomy for all ten roles and continue linking provider metadata/enforcement to Task 7. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | A role/tool responsibility fixture classifies every existing role exactly once as supervisor, read-only reviewer, or bounded author, rejects omitted/duplicate roles and write authority for network/observability, and leaves provider-specific fields with Task 7. |
| COMMON-003 | Current AI-agent research secondary QA application | Every author/reviewer/supervisor handoff records scope, changed paths, acceptance evidence, PASS/SKIP/FAIL, unavailable lanes, reviewer, and residual risk in a reusable output contract. | Role bodies define inputs, outputs, handoffs, and postflight, and Stage 04 task records provide evidence locations; there is no common required handoff schema or validator joining these fields. | 2 repository-static | Partial | Verified repo-static | Missing: role prose can be complete while a returned handoff omits scope, command results, skipped lanes, reviewer, or residual risk. | Define one provider-neutral output/handoff schema with role-specific extensions and no secret-bearing payload. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | Positive fixtures for all ten roles contain scope, changed paths, acceptance IDs, commands/results, PASS/SKIP/FAIL, limitations, reviewer/handoff, residual risk, and rollback; missing fields fail without requiring identical provider metadata. |
| COMMON-004 | Current research semantic-validator analysis; Task 7 COM-002 | Static validation detects role responsibility, output, guardrail, and handoff drift across every intended local surface without duplicating provider metadata ownership. | `validate-repo-quality-gates.sh` applies common runtime-phrase checks and Claude/Codex scope parity to Claude and Codex adapters, plus four wiki-curator phrases on those two surfaces. For Gemini/local `.agents` bodies it checks matching stem presence but performs no required-body or role-semantic validation. Task 7 separately owns provider fields and native-schema gaps. | 2 repository-static | Partial | Verified repo-static | Corrective: Claude/Codex generic shape can pass while role meaning drifts, and Gemini/local bodies can drift beyond stem presence; Task 11 has no cross-surface role-contract fixtures distinct from Task 7 provider metadata fixtures. | Add role-body semantic fixtures for all ten responsibilities on every intended local surface and keep provider fields/native schemas in Task 7's owner. | P1 near-term integrity | New Stage 04 Task: local-role-semantic-contract-validation | Positive and negative fixtures cover each role and intended local surface for scope, outputs, stop rules, prohibited actions, and handoff targets; wrong/missing semantics or a Gemini/local body drift fails while no Task 7 provider field is redefined. |
| COMMON-005 | NIST SSDF PW.7/PW.8; provider best practice; Current research eval gate | Every role has a versioned task corpus, baseline, quality/safety/cost metrics, independent adjudication, rollback, and retained run evidence before a routing or responsibility change. | Role-specific eval gates are described only in Current research. The observation tree contains no common agent-eval harness, role corpus, baseline run, threshold record, or comparative adoption artifact. | 0 absent | Gap | Verified repo-static | Missing: static role shape and deterministic repository gates cannot establish instruction-following, judgment quality, refusal, or candidate-model fitness. | Specify a minimal offline eval contract and implement only role corpora justified by an affected change. | P1 near-term integrity | New Stage 03 Spec: agent-role-contract-and-evaluation | The Spec defines dataset provenance/privacy, per-role metrics, incumbent baseline, pass/fail and variance thresholds, independent adjudication, cost/latency capture, retained redacted results, rollback, and a rule that no model/role promotion occurs without passing evidence. |

### Pinned `agency-agents` Adoption Controls

The pinned catalog is used for reusable responsibility and evaluation patterns, not
for its raw volume. `Adapt`, `Already covered`, `Skip`, and `Telemetry-gated` are
decisions for this snapshot; none installs an upstream file or changes the roster.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UP-001 | Pinned SRE/incident personas; Current overlap register | `Adapt`: add SLO, error-budget, burn-rate, timeline, severity, and recovery-evidence vocabulary only to existing observability/incident roles after role eval. | Existing bodies split manifest-static observability from read-only incident analysis. Current research identifies reusable SRE/incident vocabulary but no approved body/eval change exists at the observation SHA. | 1 documented/routed | Partial | Verified repo-static | Complementary: useful metrics vocabulary is researched but not tied to local fixtures, thresholds, or a bounded body change. | Adapt the smallest vocabulary into existing roles; do not create a broad live SRE role. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | A non-overlap diff adds only evidence-oriented SLO/incident fields, role fixtures show improved accuracy with no live authority, and both roles retain their existing handoffs/rollback. |
| UP-002 | Pinned engineering code-reviewer; Current overlap register | `Adapt`: use evidence citation, finding precision, false-negative/positive, and severity-agreement metrics to improve existing code/GitOps review roles. | Local reviewers already own bounded findings and handoffs. The pinned pattern supplies measurable success ideas, but no local metric thresholds or comparative run exist. | 1 documented/routed | Partial | Verified repo-static | Complementary: the reusable evaluation pattern is not operationalized; another generic reviewer would duplicate scope. | Adapt metrics into ROLE-002/ROLE-004 evals and retain the existing two-role boundary. | P2 planned improvement | New Stage 03 Spec: agent-role-contract-and-evaluation | Approved seeded cases and thresholds measure evidence validity, precision/recall, severity agreement, no-edit behavior, and correct cross-review handoff without adding a role. |
| UP-003 | Pinned DevOps automator, testing, IAM/compliance personas | `Adapt`: reuse automation, QA-eval, IAM, and compliance lenses only through existing supervisor, implementer, reviewers, workflows, and security role when a concrete repeated gap exists. | The local roster separates authoring, GitOps, network, observability, code, and security responsibilities. Current research finds reusable lenses but no distinct unowned deliverable or tool boundary. | 1 documented/routed | Partial | Verified repo-static | Complementary: pattern reuse has no common evidence-backed adaptation checklist; a broad mutation-capable DevOps/QA/IAM agent would blur authority. | Add a pattern-adaptation checklist and route each concrete gap to the existing owner before considering roster expansion. | P2 planned improvement | New Stage 03 Spec: agent-role-admission-and-upstream-adaptation | Every proposed adaptation names repeated evidence, existing owner, exact responsibility delta, least privilege, eval threshold, handoff, rollback, and non-overlap; speculative broad-agent proposals are rejected. |
| UP-004 | Pinned technical-writer, onboarding, orchestrator patterns; local catalog | `Already covered`: local doc-writer, wiki-curator, supervisor, protocol, templates, and canonical indexes own these responsibilities more specifically. | The fixed role bodies and canonical owners cover document routing, link curation, decomposition, delegation, completion evidence, and bounded memory/handoff. | 2 repository-static | Implemented | Verified repo-static | No local responsibility gap justifies parallel writer, onboarding, or orchestrator roles. | Improve the existing roles through their owner/eval route; preserve one supervisor. | N/A — no action | N/A — no action | N/A — no action |
| UP-005 | Pinned persona memory and thin converter patterns | `Skip`: do not import persona-owned memory or thin generated adapters that omit local scope, guardrails, handoff, postflight, model/effort/tool boundaries. | Stage 00 owns durable memory, local bodies own scoped contracts, and adapters are hand-maintained. Current research shows direct converted output lacks required local contract fields. | N/A — excluded as an unnecessary direct-import pattern | Not in scope | Conditional | Unnecessary: direct import would compete with canonical memory and weaken local/provider contracts; future generation is a separate design, not a current need. | Keep direct import skipped; reassess generation only after Task 7 native schemas/canaries and a demonstrated maintenance problem. | N/A — no action | N/A — no action | N/A — no action |
| UP-006 | Pinned FinOps persona; New-Role Admission Gate | `Telemetry-gated`: current adoption decision is Skip until repeated cost work, approved telemetry, distinct scope, data owner, least privilege, eval, handoff, retention, and non-overlap are all demonstrated. | At the observation SHA no approved cost-observability requirement, telemetry pipeline, role corpus, repeated task evidence, or distinct non-overlap case exists. Existing supervisor/observability/reporting can absorb bounded static discussion. | N/A — excluded until telemetry and demand thresholds are met | Not in scope | Conditional | Excluded: creating FinOps now would be an evidence-free role and could imply access to cost/account data that is neither approved nor available. | Keep FinOps skipped. Reopen only through an approved cost-observability requirement after the threshold is evidenced. | N/A — no action | N/A — no action | N/A — no action |

### Conditional Role-Specific Model Routing Recommendations

`C / O / G` means Claude / OpenAI Codex / Gemini. Candidate names and lifecycle
come from the Current research cutoff. Task 7 remains the sole owner of active
declarations, auth/entitlement surface, native registration, model resolution, and
availability confidence. Every row below is a conditional evaluation hypothesis;
`retain` means keep the active canonical owner unchanged.

| Role | Risk, context, and tool need | Conditional default | Escalation | Fallback boundary | Required eval gate | Cost/latency recommendation | Adoption decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `supervisor` | Long-context decomposition, cross-role synthesis, approvals, termination; orchestration tools | C Opus 4.8; O Sol/medium; G 3.5 Flash Stable | Ambiguous/high-risk plan or failed synthesis: C Fable 5; O Sol/high then max; G 3.1 Pro Preview only with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite only for bounded preprocessing, never completion judgment | ROLE-001 plus COMMON-005 | Compare total task cost, latency, retries, and synthesis defects against incumbent; no promotion without an approved bound. | Conditional — retain until Task 7 canary and eval both pass. |
| `code-reviewer` | Read-only diff analysis, seeded defect sensitivity, citations | C Sonnet 5; O Terra; G 3.5 Flash | Conflicting/high-risk findings: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O Luna/5.4 Mini; G Flash-Lite for inventory only | ROLE-002 plus COMMON-005 | Optimize cost only after false negatives, positives, severity, and citation thresholds remain within bound. | Conditional — retain; improve eval before model. |
| `doc-writer` | Source synthesis, templates, links, multilingual clarity, bounded write tools | C Sonnet 5; O Terra; G 3.5 Flash | Conflicting sources/architecture: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O Luna/5.4 Mini; G Flash-Lite for bounded formatting | ROLE-003 plus COMMON-005 | Compare unsupported claims, route/link defects, latency, and cost per accepted document. | Conditional — retain; no writer role expansion. |
| `gitops-reviewer` | High-impact desired-state ownership and sync-risk review, read-only | C Sonnet 5; O Terra; G 3.5 Flash | Ownership/sync/release ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller candidate only for inventory, never risk sign-off | ROLE-004 plus independent domain review | Cost reduction cannot raise missed-high-risk rate; capture reviewer agreement and latency. | Conditional — retain until seeded GitOps eval and Task 7 canary pass. |
| `incident-responder` | Long, incomplete evidence; causal uncertainty; approval-sensitive recovery | C Opus 4.8; O Sol/high; G 3.5 Flash | Severe ambiguity: C Fable 5; O Sol/max plus independent review; G 3.1 Pro Preview with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite only for evidence extraction | ROLE-005 plus tabletop/human approval | Optimize evidence-extraction cost separately; never trade severity or unsafe-action refusal for latency. | Conditional — retain; live response stays human/operator owned. |
| `k8s-implementer` | Bounded write tools, cross-resource schema/security, minimal diff | C Sonnet 5; O Terra; G 3.5 Flash | Cross-resource/security ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller candidate only for schema-bounded transform with independent review | ROLE-006 plus GitOps/security gates | Measure accepted-patch rate, rework, gate failures, latency, and cost; one critical secret/scope miss fails adoption. | Conditional — retain until eval, Task 7 canary, and rollback pass. |
| `network-reviewer` | Routing/isolation/TLS evidence, no live probes | C Sonnet 5; O Terra; G 3.5 Flash | Routing/isolation/TLS ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller candidate for inventory only, never isolation/TLS sign-off | ROLE-007 plus Task 7 semantic-parity acceptance | Cost/latency optimization follows false-negative and evidence thresholds. | Conditional — retain; validator completion precedes migration. |
| `observability-reviewer` | Scrape/alert/SLO interpretation, manifest-static only | C Sonnet 5; O Terra; G 3.5 Flash | Alert/SLO ambiguity: C Opus 4.8; O Sol; G 3.1 Pro Preview | Smaller candidate for inventory only, never live/SLO sign-off | ROLE-008 plus Task 7 semantic-parity acceptance | Measure defect accuracy, unsupported live claims, evidence quality, latency, and cost. | Conditional — retain; adapt SRE vocabulary before model changes. |
| `security-auditor` | Missed-critical minimization, refusal, redaction, independent/human sign-off | C Opus 4.8; O Sol/high; G 3.5 Flash | Critical uncertainty: C Fable 5 where entitled; O Sol/max plus independent review; G 3.1 Pro Preview with lifecycle acceptance | C Sonnet 5; O Terra; G Flash-Lite only as evidence collector, never finding downgrade/sign-off | ROLE-009 plus human adjudication | Cost is secondary to missed-critical/refusal/redaction thresholds; capture latency without weakening sign-off. | Conditional — retain until zero-or-approved missed-critical gate and Task 7 canary pass. |
| `wiki-curator` | Deterministic link/index curation, source-owner fidelity, bounded writes | C Sonnet 5; O Terra; G 3.5 Flash | Conflicting owners/large synthesis: C Opus 4.8; O Sol; G 3.1 Pro Preview | C Haiku 4.5; O Luna/5.4 Mini; G Flash-Lite for bounded curation | ROLE-010 plus generator idempotence | Compare valid owner/link changes, rejected artifacts, latency, and cost per accepted refresh. | Conditional — retain; no onboarding persona. |

### Risk-Bounded Vibe-Coding Controls

Vibe coding is prompt-led rapid exploration, not an assurance or approval mode.
R0 disposable exploration may be informal only while it remains disposable. Any
retained change enters R1; infrastructure, GitOps, identity, secrets, network,
security policy, CI/hooks, and agent governance are R2 proposal/review surfaces; R3
live/high-impact execution remains human/operator owned.

| ID | Benchmark | Expected control | Repository evidence | Maturity | Verdict | Confidence | Gap | Recommendation | Priority | Follow-up owner | Acceptance evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VIBE-001 | Current risk-bounded vibe research; NIST SSDF PW.1.2 | Before generation, retained work has an owning requirement/specification, risk tier, scope/non-goals, affected owners, exception path, and prohibited actions. | Agentic rules require explicit success criteria, affected paths, validation and limitations; Stage 01-04 templates route intent and execution. The active owners do not define the R0-R3 vibe tiers or a mandatory AI-assisted risk classification. | 2 repository-static | Partial | Verified repo-static | Complementary: general specification exists, but throwaway exploration can be promoted without an explicit R1/R2 reclassification and owner/risk record. | Add a risk-bounded AI-assisted development contract that links, rather than duplicates, canonical SDLC owners. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | Fixtures require every retained AI-assisted change to record R1/R2 classification, owner, scope/non-goals, prohibited actions, affected lanes, exception/approval route, and reject unlabeled promotion from disposable R0. |
| VIBE-002 | Current vibe research; Claude best practices; NIST PW.8 | Acceptance criteria are executable before editing and cover positive, negative, security, evidence, and completion conditions appropriate to risk. | Agentic rules require success criteria and validation commands; Spec/Plan/Task templates provide acceptance/evidence surfaces. No deterministic check proves criteria are executable, risk-complete, or written before generation. | 2 repository-static | Partial | Verified repo-static | Corrective: vague criteria can satisfy document shape while leaving the model or reviewer unable to falsify completion. | Define criterion quality fixtures and require negative/security evidence for R2 changes. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | Positive fixtures contain observable pre-edit criteria and matching command/result owners; negative fixtures reject subjective completion, missing R2 negative/security cases, post-hoc criteria, and unevidenced exceptions. |
| VIBE-003 | Current vibe research; Git workflow and logical-unit commit contract | AI-assisted diffs remain small, isolated, one logical control at a time, with complete changed-file inventory and out-of-scope/lockfile/policy/credential-path detection. | Git workflow and task plans require scoped logical commits and diff review; worktrees are supported. No deterministic size/concern threshold or required changed-file classification exists for AI-authored diffs. | 2 repository-static | Partial | Verified repo-static | Complementary: logical-unit prose does not detect oversized mixed-purpose diffs or hidden sensitive-surface expansion. | Add risk-based diff inventory/review evidence rather than a universal line-count gate. | P2 planned improvement | New Stage 03 Spec: risk-bounded-ai-assisted-development | R1/R2 fixtures record every changed path, concern/owner, generated/dependency artifact, out-of-scope decision, and split rationale; mixed unrelated controls or unexplained sensitive paths fail review. |
| VIBE-004 | Current vibe research; primary CI/QA audit; NIST PW.7/PW.8 | Changed-file/affected-lane feedback and canonical completion gates run with exact PASS/SKIP/FAIL evidence; test/static failures cannot be summarized away. | [CI/QA audit](ci-qa-automation-pipeline-workflow.md) owns the exact pre-commit, all-files, CI DAG, formatter/linter/parser/static/security lanes. Agentic and postflight contracts require deterministic evidence and honest unavailable/SKIP reporting. | 3 deterministic local+CI enforcement | Implemented | Verified repo-static | No missing assessed repository-static QA lane contract; provider obedience, remote execution, and live readiness remain separately excluded. | Preserve the primary CI/QA owner and link it from AI-agent handoffs instead of copying commands into every role. | N/A — no action | N/A — no action | N/A — no action |
| VIBE-005 | Current vibe research; OWASP X03; independent-review guidance | Retained R1 work receives independent diff/evidence review; R2 uses a separately scoped domain reviewer and human approval, not the generating agent's tests or summary. | Reviewer roles and subagent handoffs exist, and GitHub PR flow supports human review. The observation SHA has no deterministic rule requiring author/reviewer separation for every R1 or specialist/human approval evidence for R2. | 1 documented/routed | Partial | Verified repo-static | Missing: self-review can be presented without an independent reviewer, especially when the same agent authored tests and implementation. | Require risk-tiered reviewer identity and independence evidence while preserving human authority. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | R1 evidence names a non-author reviewer and disposition; R2 names domain reviewer plus human approver, records conflicts, and rejects generating-agent-only sign-off or reviewer identity reuse. |
| VIBE-006 | Current vibe research; NIST PS.3.2; OWASP LLM03 | Retained work records source/prompt context as appropriate, agent/tool/model declaration, dependencies/suppliers, changed files, commands/results, approvals, artifact identity, and rollback provenance without secrets. | Task/commit evidence records paths, commands and results; pinned research records external sources. No common requirement records AI source context, resolved runtime identity, dependency/artifact hashes, or approval provenance for every applicable R1/R2 change. | 1 documented/routed | Partial | Verified repo-static | Missing: a reviewer may reproduce repository checks but not establish which AI/tool/source/dependency or approval produced the proposed artifact. | Define a privacy-bounded provenance manifest only for consumers that need it; never record prompts or data containing secrets. | P2 planned improvement | New Stage 03 Spec: risk-bounded-ai-assisted-development | Applicable R1/R2 fixtures record redacted source/tool/model declaration, changed paths, dependency/artifact identity or explicit N/A, commands/results, reviewer/approval, and rollback link; secret-bearing prompt/output storage fails. |
| VIBE-007 | Current vibe research; OWASP LLM01/05/06; approval boundaries | Model output and external content remain untrusted; tools, egress, paths, credentials, and permissions are least privilege, secret values stay forbidden, and high-impact authorization occurs outside the model. | Approval boundaries, role guardrails, secret scans and policy gates provide deterministic repository controls. Task 7 separately records provider-native permission/settings confidence and unverified runtime consumption; this row does not rescore it. | 3 deterministic local+CI enforcement | Partial | Conditional | Complementary: strong static controls exist, but provider/runtime enforcement and untrusted-output mediation are not proven; a model recommendation cannot grant authority. | Preserve static secret/policy gates and require Task 7 native-canary evidence before any tool/permission expansion. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | Negative fixtures reject secret access/output, shell/path/query use of unsanitized model text, external write/egress expansion, and model-authorized high-impact calls; R2 evidence links the relevant Task 7 canary and human approval. |
| VIBE-008 | Current vibe research; approval-boundary rollback matrix | Before R1/R2 approval, rollback names the exact logical commit/config/data predecessor, recovery owner, preconditions, command/procedure, and verification evidence. | Approval boundaries name rollback by protected surface and Plans/Tasks provide rollback fields. The observation SHA has no common check that each AI-assisted change's rollback is executable, current, data-safe, and independently reviewed. | 2 repository-static | Partial | Verified repo-static | Corrective: `git revert` prose can be insufficient for migrations, policies, external state, or dependent resources, and no rehearsal evidence is required. | Require risk-specific rollback evidence; R2 rollback must be reviewed before approval and R3 remains operator-owned. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | R1 fixtures link the logical predecessor and verification; R2 fixtures include dependency/data impact, reviewed recovery steps and rollback test or justified limitation; stale, destructive, ownerless, or post-hoc rollback fails. |
| VIBE-009 | Current vibe research; bounded loop; Task 7 HAR-004 | Work stops and escalates on scope drift, repeated failure, missing dependency/owner/evidence, sensitive file, permission/test/gate weakening, target mismatch, stale approval, secret exposure, or rollback uncertainty; retries are bounded. | Role bodies contain handoff/escalation and agentic rules require harness repair after repeated failure. Task 7 HAR-004 owns the absent common retry budget/attempt schema; no active R0-R3 stopping contract binds every condition above. | 1 documented/routed | Partial | Verified repo-static | Missing: agents can continue ambiguous retries without a shared attempt budget or risk-tiered stop reason even though escalation routes exist. | Link the risk-tier stop taxonomy to HAR-004's bounded-attempt owner and require explicit final stop/escalation evidence. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | Fixtures enforce attempt budget, stop reason, last evidence, unchanged approval scope, owner/handoff, and next safe action; repeated unchanged failures, sensitive-path discovery, test weakening, secret exposure, or rollback uncertainty terminate rather than loop. |
| VIBE-010 | Current vibe research; OWASP X03/LLM06; approval boundaries | R2 protected surfaces permit AI analysis or patch proposal only with domain review and human approval; R3 live/high-impact action is never autonomous and requires operator identity, target, preflight, stop, rollback, and post-action evidence. | Active approval boundaries protect GitOps/live cluster, Vault/secrets, workflows, governance, cloud, GitHub mutation, paid jobs, and external action. Task 7 shows provider enforcement is not uniform and native consumption is unverified. | 2 repository-static | Partial | Conditional | Corrective: active boundaries are surface-based but do not explicitly label retained AI work R2/R3, and tracked instructions cannot prove provider or operator enforcement. | Add an AI-assisted risk overlay that points to the existing approval matrix; do not create a competing permission system. | P1 near-term integrity | New Stage 03 Spec: risk-bounded-ai-assisted-development | R2 fixtures require specialist review, deterministic evidence, human approval and rollback before proposal acceptance; R3 fixtures reject agent execution and require operator target/identity, fresh approval, preflight/stop/recovery/postflight evidence with Task 7 limitations explicit. |

### Score and Distribution Summary

| Category | Total controls | Applicable controls | Maturity numerator | Denominator | Implementation | Maturity distribution (`0/1/2/3/4`, applicable only) | Verdict distribution (`Implemented/Partial/Gap/Not in scope`) | Confidence distribution (`Verified repo-static/Unverified live/Conditional`, applicable only) | N/A exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| Local roles | 10 | 10 | 20 | 40 | 50.0% | `0/0/10/0/0` | `0/10/0/0` | `10/0/0` | None |
| Shared role system | 5 | 5 | 7 | 20 | 35.0% | `1/1/3/0/0` | `1/3/1/0` | `5/0/0` | None |
| Pinned upstream adoption | 6 | 4 | 5 | 16 | 31.3% | `0/3/1/0/0` | `1/3/0/2` | `4/0/0` | UP-005 direct import; UP-006 FinOps until telemetry/demand threshold |
| Vibe coding | 10 | 10 | 19 | 40 | 47.5% | `0/3/5/2/0` | `1/9/0/0` | `8/0/2` | None |
| **Overall** | **31** | **29** | **51** | **116** | **44.0%** | **`1/7/19/2/0`** | **`3/25/1/2`** | **`27/0/2`** | **2 controls** |

The arithmetic is `51 / (4 * 29) = 51 / 116 = 44.0%`. UP-005 and
UP-006 are excluded because direct import is unnecessary and FinOps lacks its
telemetry/demand precondition. No maturity 4 is awarded: no role inference eval,
provider-runtime result, or live/operational vibe evidence belongs to this fixed
snapshot. The score is descriptive and grants no model, tool, role, or live authority.

### Priority and Adoption Summary

- No P0 immediate-safety finding is asserted from this repository-static audit.
- P1 concentrates on high-risk role evals, semantic drift, shared eval absence,
  R2/R3 specification/review/permission/rollback/stopping, and Task 7 canary
  prerequisites.
- P2 covers bounded role-quality, output/handoff, upstream metric adaptation,
  diff inventory, and privacy-bounded provenance improvements.
- `Already covered` writer/onboarding/orchestration patterns require no role change.
- Direct persona memory/thin import is `Skip`; FinOps is `Telemetry-gated` with a
  current Skip decision until an approved cost-observability requirement and evidence
  pipeline meet the New-Role Admission Gate.
- Every candidate model route is Conditional. The active owner remains unchanged if
  Task 7 native availability or the role-specific eval fails.

## Comparison Analysis

- The ten roles have clear repository-static responsibilities and handoffs. The main
  weakness is not roster breadth but the absence of behavioral evals and deterministic
  role-semantic fixtures.
- Tool and permission intent is least-privilege at the role layer. Provider-native
  enforcement, registration, declaration, and availability remain separate Task 7
  facts and are not reopened here.
- Pinned upstream patterns are useful for metrics and vocabulary. They do not justify
  direct imports, persona memory, broad mutation agents, duplicate writers/reviewers,
  or FinOps without telemetry.
- The repository has strong deterministic static QA and secret/policy lanes. It lacks
  one active risk-tier contract connecting disposable prompt-led exploration to R1
  retained work, R2 protected proposals, and R3 operator-only execution.
- Model routing should be evidence-driven: role risk and eval trigger escalation;
  fallback reduces scope/authority; cost/latency optimization follows safety and
  quality thresholds.

## Automation Opportunities

- Add local role-semantic positive/negative fixtures without duplicating Task 7
  provider metadata fixtures.
- Build a small offline role-eval harness only after the owning Spec defines dataset
  provenance, privacy, metrics, variance, adjudication, and retention.
- Add a provider-neutral handoff evidence schema that links the primary CI/QA owner
  rather than copying commands into role bodies.
- Automate R1/R2 evidence-shape checks only after the risk-bounded AI-assisted
  development Spec defines consumers and exception semantics.
- Do not automate roster generation or model migration until Task 7 native schemas,
  canaries, role eval, and rollback are proven.

## Residual Risks

- This audit does not prove that any provider discovered an agent, enforced tools,
  resolved a model, authenticated an account, or produced a correct inference.
- Static role bodies can drift semantically beyond the phrases currently checked.
- Eval datasets can encode blind spots, leak sensitive material, or overfit; provenance,
  access, independent adjudication, and versioned holdouts are required.
- Candidate model lifecycle, availability, quality, cost, and latency can change after
  the fixed cutoff and must not silently update this dated audit.
- R2/R3 instructions are not a substitute for provider/native controls, downstream
  authorization, specialist review, human approval, or operator-owned recovery.

## Sources

- [Audit pack README and method](README.md)
- [Task 7 Governance, Harness, Loop, and Provider audit](governance-harness-loop-providers.md)
- [Primary CI/QA audit](ci-qa-automation-pipeline-workflow.md)
- [Current AI Agents Roster and Gap Analysis](../../research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md)
- [Current Provider Implementation Status](../../research/2026-07-07-wer/provider-implementation-status.md)
- [Current Harness and Loop Engineering](../../research/2026-07-07-wer/harness-and-loop-engineering.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Model Policy](../../../00.agent-governance/model-policy.md)
- [Agentic Rules](../../../00.agent-governance/rules/agentic.md)
- [Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- Pinned `agency-agents` commit:
  <https://github.com/msitarzewski/agency-agents/commit/9f3e401ccd09aa0ee0ef8e015226d0647908e01e>
- Pinned division/tree/linter/converter/tools/license sources listed in the Current AI
  agent research source ledger.
- NIST SP 800-218 SSDF 1.1: <https://csrc.nist.gov/pubs/sp/800/218/final>
- OWASP X03 Inappropriate Trust in AI Generated Code:
  <https://owasp.org/Top10/2025/X01_2025-Next_Steps/#x032025-inappropriate-trust-in-ai-generated-code-vibe-coding>
- OWASP Gen AI LLM01, LLM03, LLM05, and LLM06 source URLs listed in the Current
  AI-agent research ledger.
- Anthropic Claude Code security/best practices, OpenAI Codex safety, and Gemini CLI
  trusted-folder/sandbox sources listed in the Current AI-agent research ledger.

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-11
- Next review trigger: local role responsibility/body/eval/validator change, upstream
  pin or converter/linter change, active new-role decision, cost telemetry requirement,
  Task 7 provider/canary evidence change, vibe-risk contract, or audit method change.
- Refresh method: retain the old observation SHA, select a new dated audit or advance
  the snapshot explicitly, consume Task 7 facts without restating them, rerun each
  applicable role/upstream/vibe control, and recalculate numerator, denominator,
  distributions, and N/A exclusions.

## Related Documents

- **Audit pack**: [2026-07-11 WEIA README](README.md)
- **Implementation plan**: [WEIA implementation plan](../../../04.execution/plans/2026-07-11-workspace-engineering-research-audit-integration.md)
- **Task 7 canonical provider audit**: [Governance, Harness, Loop, and Provider Parity](governance-harness-loop-providers.md)
- **Current research pack**: [2026-07-07 WER README](../../research/2026-07-07-wer/README.md)
- **Parent audits index**: [Audits README](../README.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
