---
title: 'Audit: Remediation and Integration Roadmap'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Remediation and Integration Roadmap

## Overview

This report owns cross-report finding normalization, dependencies, priorities,
target state, canonical implementation owners, cutover sequence, rollback, and
the residual `DEFER` backlog. WGIA-001 establishes the integration form only;
WGIA-009 populates the reviewed roadmap after the topical audits.

## Reference Type

Dated repository-static integrated audit roadmap. It is not an implementation
owner, permission grant, deletion authority, Current-pointer owner, or approval
to change active policy and operations.

## Authority Boundary

Source reports retain their findings and evidence. This roadmap may deduplicate
and order only reviewed findings, then route accepted work to canonical owners.
It cannot rescore source evidence, resolve an ambiguous approved decision,
change Current navigation, or promote deeper evidence.

## Scope

Included: cross-report identifiers, dependencies, priorities, target-state
outcomes, implementation owners, verification, blockers, cutover, rollback,
and residual uncertainty. Excluded: unreviewed topic conclusions, direct
canonical remediation, Current cutover, deletion, remote actions, and closure.

## Definitions / Facts

### Integration Inputs

The eight focused reports are draft inputs. Each currently contains one
foundation finding and a report-local owner/source boundary. WGIA-009 may admit
a finding here only after its required fields and source-report review are
complete.

### Roadmap Record Convention

Each integrated row requires: integrated ID, source finding IDs, affected
request scopes, problem statement, dependency, priority, target state,
canonical implementation owner, validation, verification, rollback, blocker,
evidence depth, and status. Unknown owners or unresolved approved-decision
conflicts fail closed to `DEFER`.

### Foundation Dependency Map

| Phase | Inputs | Output boundary | Initial state |
| --- | --- | --- | --- |
| Topical audit | WGIA-002 through WGIA-008 | Reviewed report-local findings | Complete; all source reviews Approved. |
| Integrated disposition | Reviewed source findings plus cleanup candidates | 12 deduplicated rows and fifteen `Integrate` one-shot decisions in WGIA-009 | `In Review`; seven admitted actions and five `DEFER` rows. |
| Canonical remediation | Seven admitted unambiguous roadmap rows | Two reviewed `Correct` rows in WGIA-010, two reviewed `Correct` rows in WGIA-011, two `Integrate` rows routed to existing WORK-013, and one `Integrate` row routed to existing WORK-001 | WGIA-010/011 reviews and exact staged full gates are `Approved`/PASS. |
| Atomic cutover | Complete pack plus machine/current projections | Sole Current transition in WGIA-012 | `DEFER` pending cutover gates. |
| Cleanup | Proof-complete `Delete` rows | Exact removals in WGIA-013 | No WGIA row is admitted as `Delete`; `Delete=0`. Spec 052 WORK-001 retains its separate future zero-referent transition, and WGIA-013 owns only the then-current reviewed WGIA disposition. |
| Closure | Re-audit, full QA, reviews, and logical history | WGIA-014 terminal handoff | `DEFER` pending all prior work. |

### Integrated WGIA-009 Remediation Register

The 12 reviewed topical and disposition inputs are deduplicated once each below. Status is an
admission decision, not implementation approval: only unambiguous `Correct` or
`Integrate` rows route to WGIA-010/011 or the already approved WORK-013/WORK-001 owners;
architecture, credential, provider, registry, and live decisions remain
`DEFER`. Source reports retain finding truth.

| Candidate ID | Source findings | Request IDs | Problem | Dependency | Priority | Target state | Canonical implementation owner | Validation | Verification | Rollback | Blocker | Evidence depth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WGA-RMP-GOV-001 | `WGA-GOV-002`, `WGA-GOV-003` | `REQ-WGA-001`, `REQ-WGA-002`, `REQ-WGA-012` | Root `README.md` presents thin `AGENTS.md` as a canonical owner and omits/misclassifies the `.gemini/` versus `.agents/` adapter boundary. | WGIA-002 reviews Approved; WGIA-009 admission complete before WGIA-010. | P1 owner-routing integrity | `README.md#canonical-owners` points to the Stage 00 policy SSoT; `README.md#top-level-areas` names all four tracked surface classes without promoting provider runtime. | `README.md` human onboarding owner; Stage 00 and `harness-contract.json` remain classification sources. | Deterministic root-routing regression plus governance closure, harness contract/semantics/currentness, strict profile, and strict link checks. | Reviewer confirms the human overview resolves to one policy owner, retains thin gateways, includes `.gemini/`, distinguishes `.agents/`, and keeps runtime claims `DEFER`. | Revert only the later bounded `README.md` correction; current Stage 00 and adapter files require no rollback. | None for repository-static owner correction; runtime remains outside the row. | `repository-static` | `Implemented: Corrected in WGIA-010; reviews Approved` |
| WGA-RMP-DOC-001 | `WGA-DOC-002` | `REQ-WGA-016`, `REQ-WGA-019`, `REQ-WGA-023` | The broad Release request has no current contract and is not explicitly mapped to approved DOC-G5, which already rejects the narrower release-notes type. | WGIA-003 reviews Approved; integrate with queued WORK-013 without reopening DOC-G5 or creating a duplicate WGIA implementation. | P1 semantic owner routing | Preserve no first-class release-notes type, execute WORK-013's deliberate-absence text, and record whether the broader Release request resolves to an existing evidence owner or remains explicitly unmapped. | Approved Spec 052 DOC-G5; WDTC Plan and Task WORK-013 for execution; current Stage 99/Stage 05 owners remain unchanged. | WORK-013 evidence plus registry/profile/lifecycle/links and the zero-dimension Release probe. | Reviewer confirms the broad-versus-narrow distinction, the DOC-G5 decision, and no new release-notes route. | Revert only later WORK-013 text if required; do not remove or reopen approved DOC-G5. | WORK-013 is queued; WGIA-010 records integration/no-duplicate evidence rather than implementing a second route. | `repository-static` | `Integrated by WGIA-010: no duplicate delta; WORK-013 queued` |
| WGA-RMP-DOC-002 | `WGA-DOC-003` | `REQ-WGA-018`, `REQ-WGA-019` | Approved DOC-G1 owns `how-to`, `tutorial`, `concept`; heading/template/current-guide evidence exists, but registry enum enforcement and all-eight-guide validation remain unimplemented. | WGIA-003 reviews Approved; integrate with queued WORK-013 without fresh taxonomy design or duplicate implementation. | P1 approved-control completion | Execute WORK-013: enforce the three-value registry enum, validate all eight `how-to` guides, and record DOC-G2/DOC-G3 deliberate absences without creating routes. | Approved Spec 052 DOC-G1 through DOC-G3; WDTC Plan/Task WORK-013 and Stage 99 registry/template owners. | Invalid-value negative fixture, registry/profile/lifecycle/links, and explicit eight-guide migration/validation evidence. | Reviewer confirms the approved enum is enforced, all eight guides pass, and no tutorial/explanation route was created. | Revert only the bounded WORK-013 registry/template/lifecycle implementation while preserving approved Spec 052. | WORK-013 is queued; WGIA-010 records integration/no-duplicate evidence rather than implementing a second route. | `repository-static` | `Integrated by WGIA-010: no duplicate delta; WORK-013 queued` |
| WGA-RMP-DSP-001 | `WGA-DSP-001` | `REQ-WGA-025`, `REQ-WGA-026` | Approved Spec 052 WORK-001 names fifteen one-shot active-corpus data/script/test paths, but every path still has current consumers; seven legacy-name active owners are noncandidates. | WGIA-009 review plus existing WORK-001; resolve archive/lifecycle imports, RIA/data indexes, aggregate/docs/test references, protected-evidence and allowlist coupling before any zero-referent transition. | P1 approved cleanup integration | Preserve all fifteen paths until WORK-001 migrates their exact consumers, passes its zero-referent and post-change gates, and independently proves any later `Delete` decision. | Approved Spec 052 Plan/Task WORK-001; current data, script, test, archive, lifecycle, RIA, secret-handling, and index owners remain authoritative until migration. | Exact fifteen-path/full-hash/current-consumer probe; active-corpus, archive-cutover, document-lifecycle, RIA, secret-handling, registry/profile/link and full-gate checks. | Independent WORK-001 review confirms every live consumer is removed or migrated and no filename-only inference or duplicate WGIA implementation exists. | Revert only the later bounded WORK-001 consumer-migration/deletion unit if a post-change gate fails; retain this integration evidence and current files. | Live imports and data/test/protection consumers are nonzero; current decision is `Integrate`, not `Delete`. | `repository-static` | `Admitted: Integrate with WORK-001` |
| WGA-RMP-HAR-001 | `WGA-HAR-003` | `REQ-WGA-017` | The observation-state `scripts/README.md` human inventory omitted tracked import-only helpers `scripts/archive_cutover_manifest.py` and `scripts/reference_information_architecture.py`; observation inventory is 47 scripts = 41 CLI + six helpers. | WGIA-005 reviews Approved; WGIA-009 admission complete before WGIA-011 changes only the human index. | P2 human inventory completeness | `scripts/README.md` names all 47 tracked script files, identifies the six import-only helpers, and preserves the existing production semantic owners/callers. | `scripts/README.md` human inventory owner; current scripts, contracts, validators, tests, and fixtures retain production ownership. | Re-run the deterministic observation/current 47 = 41 + 6 probe with zero missing human-index paths, then strict registry/profile/link and focused harness checks. | Reviewer confirms both missing helper rows are present, no CLI/helper is misclassified, and no aggregate/helper is promoted to a duplicate semantic owner. | Revert only the later bounded `scripts/README.md` inventory correction; production scripts/contracts/tests require no rollback. | None for the bounded repository-static human-index correction. | `repository-static` | `Implemented: Corrected in WGIA-011; reviews Approved` |
| WGA-RMP-KNW-001 | `WGA-KNW-002` | `REQ-WGA-022` | LLM-WIKI README and generated output retain 2026-05-10 source/review metadata although all six RIA-declared inputs and the producer/output changed later; byte equality alone does not prove on-source-change review. | WGIA-006 reviews Approved; WGIA-009 admission complete before WGIA-010 changes the current knowledge owners. | P1 freshness evidence integrity | Review all six declared inputs and current owner links; record current review metadata in the README and generator; regenerate output through the producer without adding a runtime/search claim or hand editing. | `docs/90.references/llm-wiki/README.md` for review/freshness declaration; `scripts/generate-llm-wiki-index.sh` for emitted metadata; target documents retain fact/policy ownership. | Generator `--check`, three focused RIA generator-relation tests, strict profiles/links, and deterministic declared-input last-change versus review-date proof. | Reviewer confirms six-input review, current links, truthful metadata, generator-only output, and continued reference-only boundary. | Revert only the later bounded README/generator/generated-output logical unit; canonical targets and memory contracts require no rollback. | None for the bounded source-review/generated-owner correction; runtime lookup remains outside the row. | `repository-static` | `Implemented: Corrected in WGIA-010; reviews Approved` |
| WGA-RMP-SEC-CLAUDE-001 | `WGA-SEC-002` | `REQ-WGA-024` | Claude's observation-state tracked allow patterns permitted broad `cat`, `grep`, `git`, and read-only `kubectl` command families while the deny list did not encode shared secret-read and ordinary remote-mutation approval stops. | WGIA-008 reviews Approved; WGIA-009 admission complete for repository-static adapter correction; provider-native loading/effective permission remains separate. | P0 approval-boundary integrity | Narrow repository-static provider permissions to exact fixed Git/validator commands, prohibit wildcard and caller-selected-root allows, and encode the complete deny contract without claiming native enforcement. | `.claude/settings.json` adapter owner and `scripts/validate-agent-provider-config.py` sole permission-semantic validator; `docs/00.agent-governance/rules/approval-boundaries.md` retains shared-policy authority. | Exact production-set, broad-command, wildcard, alternate-root, complete deny-tuple, and every-deny-removal mutation tests plus provider-config and strict document checks. | Independent reviewer confirms allowed commands cannot statically subsume secret reads, arbitrary roots/suffixes, or unapproved push/merge; all 62 denies are focused-owned; provider-runtime claims remain `DEFER`. | Revert only the bounded adapter-policy correction; shared approval policy remains unchanged. | Native consumption/effective enforcement remains `DEFER`, but does not block the tracked adapter correction. | `repository-static` | `Implemented: Corrected in WGIA-011; reviews Approved` |
| WGA-RMP-SEC-SCAN-001 | `WGA-SEC-003` | `REQ-WGA-024` | The bounded secret-handling lane passes, but redacted current-worktree and history Gitleaks probes produce untriaged candidates and transient compiled-test noise, so clean-worktree/history coverage is not established. | Approved non-disclosing security triage of `BLK-WGA-SEC-002`; exact false-positive classification before any allowlist change. | P1 secret-scanning evidence integrity | Define deterministic redacted current-tree/history scan scope, exclude transient build artifacts structurally, rotate/revoke any real credential, and admit only exact reviewed false-positive rules. | `.gitleaks.toml`, `.pre-commit-config.yaml`, and `.github/workflows/ci.yml` owners with the security/credential owner for triage. | Redacted positive/negative fixtures, clean tracked-worktree scan, and reviewed history scan with no payload disclosure. | Security reviewer confirms every candidate is rotated or exactly classified and broad allowlisting is absent. | Revert only scan-scope/allowlist changes; never restore a confirmed credential. | `BLK-WGA-SEC-002`: credential/security triage is not authorized in WGIA-009. | `repository-static` | `DEFER: credential/security triage required` |
| WGA-RMP-SEC-KSM-001 | `WGA-SEC-004` | `REQ-WGA-024` | Kube-state-metrics is bound to a cluster-wide role that can list/watch Secret metadata and mounts its service-account token, without a focused least-privilege justification or negative gate. | Collector/version capability and owner decision, then separately approved live canary before rollout. | P1 least privilege | Remove Secret access unless a documented collector requirement proves it necessary; otherwise scope the permission and add a regression that rejects reintroduction. | `gitops/platform/monitoring/kube-state-metrics.yaml` manifest owner. | Static RBAC subject/rule equality and negative least-privilege fixtures. | Approved live canary confirms required metrics remain available without broader Secret access; live verification stays separately authorized. | Restore the prior RBAC rule only through an approved bounded rollback if the canary proves a documented required metric regression. | Collector requirements and live cluster metrics/effective authorization were not observed. | `repository-static` | `DEFER: owner design and live canary required` |
| WGA-RMP-SEC-NET-001 | `WGA-SEC-005` | `REQ-WGA-024` | Six egress-oriented NetworkPolicies do not establish ingress/default-deny coverage, and four tracked namespaces have no NetworkPolicy object. | Namespace traffic inventory, local-home-lab exception/architecture decision, and later authorized CNI/live probes. | P1 network isolation | Define an explicit namespace baseline, default-deny policy, and narrowly documented exceptions, including a deliberate decision for every tracked namespace. | `gitops/platform/network-policies/` policy owner and namespace workload owners. | Static namespace/policy coverage, ingress/egress/default-deny negative fixtures, and GitOps manifest checks. | Authorized live connectivity tests prove intended flows and deny unintended flows without relying on manifest presence alone. | Revert the bounded policy set atomically if an approved connectivity canary fails; retain the reviewed baseline decision. | Traffic intent, exception architecture, CNI implementation, and live enforcement are unavailable. | `repository-static` | `DEFER: architecture and live evidence required` |
| WGA-RMP-SEC-ADM-001 | `WGA-SEC-006` | `REQ-WGA-024` | Adminer lacks the repository-static hardening visible on other raw pod templates, while no tracked PSA labels or admission-policy owner enforces a baseline; local KubeLinter exclusions further make the exception deliberate but incomplete. | Workload compatibility review, explicit local-home-lab exception/admission decision, and later authorized rollout/admission verification. | P1 workload hardening | Harden Adminer or document the narrow exception, and decide a repository-owned PSA/admission baseline without misrepresenting pre-merge lint as live admission. | `gitops/workloads/adminer/rollout.yaml`, namespace owners, and the existing policy-gate owner. | Static security-context/service-account-token checks, admission-policy fixtures if adopted, and KubeLinter/policy gates. | Approved rollout and admission evidence confirms the workload remains functional and the baseline is actually enforced. | Revert only the bounded workload/admission change if an approved rollout fails; retain documented exceptions and evidence. | Hardening/exception/admission design and live workload behavior are unavailable. | `repository-static` | `DEFER: design and live evidence required` |
| WGA-RMP-SEC-SC-001 | `WGA-SEC-007` | `REQ-WGA-024` | Non-latest image checks pass, but Argo tracks `main`, raw images use tags rather than digests, Helm artifacts lack repository-visible identity/signature evidence, and no SBOM/provenance/signature consumer is established. | Threat-model the actual Git/image/chart consumers, registry capabilities, update process, and rollback needs before an architecture decision. | P2 supply-chain architecture | Record a deliberate immutable-identity and provenance policy per consumed artifact class, then adopt or explicitly defer digest/signature/SBOM verification with an operational update path. | Argo bootstrap/application-set, image-manifest, Helm chart, and CI policy owners by artifact class. | Static mutable-reference negative fixtures plus signature/SBOM consumer contract checks only for adopted controls. | Authorized deployment evidence confirms promoted artifact identity and rollback remain reproducible; registry/live verification stays separately approved. | Revert only the adopted verification/pinning mechanism to the reviewed prior reference while preserving the threat-model decision. | Architecture, registry identity, signature trust roots, and live reconciliation were not observed. | `repository-static` | `DEFER: architecture and registry/live evidence required` |

### Finding Convention

Every material roadmap finding keeps the complete pack field set and closed
audit verdict/depth vocabularies. Integrated priority and status never replace
the source verdict, evidence, uncertainty, blocker, or canonical owner.

#### WGA-RMP-001 — Reviewed topical findings are deduplicated and routed

- **Request IDs**: all request rows through their primary source-report owners.
- **Scope**: cross-report admission, dependency, remediation, cutover, rollback, and residual-backlog structure.
- **Expected state**: WGIA-009 integrates only complete, reviewed source findings, deduplicates each once, routes unambiguous work to one current owner, and fails architecture/credential/live decisions closed.
- **Observed state**: 12 source rows are represented exactly once; WGIA-010 corrected GOV/KNW and recorded no-duplicate integration for both DOC rows with queued WORK-013, WGIA-011 implemented HAR/CLAUDE and its fresh reviews are Approved, the disposition row integrates fifteen candidates with existing WORK-001, and SCAN/KSM/NET/ADM/SC remain explicit `DEFER`.
- **Evidence**: `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-006--purpose-conflict-remediation`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#failure-modes--fallback--human-escalation`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-009--disposition-ledger-and-integrated-roadmap`; `docs/90.references/audits/2026-08-09-wgia/workspace-purpose-governance-and-operating-contracts.md#finding-convention`; `docs/90.references/audits/2026-08-09-wgia/spec-driven-sdlc-documentation-and-templates.md#finding-convention`; `docs/90.references/audits/2026-08-09-wgia/harness-loop-fixtures-scripts-and-blockers.md#finding-convention`; `docs/90.references/audits/2026-08-09-wgia/llm-wiki-memory-and-knowledge-management.md#finding-convention`; `docs/90.references/audits/2026-08-09-wgia/security-and-approval-boundaries.md#finding-convention`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#wgia-009-focused-evidence`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: WGIA-010/011 and the existing WORK-013/WORK-001 owners receive only bounded work with exact ownership and rollback, while uncertain or unauthorized security work cannot leak into implementation.
- **Disposition**: `Integrate`.
- **Canonical owner**: source reports for findings; current Stage 00-05/90/99, workflow, script, test, and manifest surfaces for implementation.
- **Verification**: exact 12-ID uniqueness/status probe; source-finding existence; owner/dependency/validation/verification/rollback/blocker completeness; strict link/profile/registry and independent WGIA-009 reviews.
- **Uncertainty**: WGIA-011 full-gate outcome remains pending; all architecture, credential, registry, provider, and live decisions stay explicit in five `DEFER` rows.
- **Blocker**: none for the integrated roadmap; each deferred row carries its own release condition.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-RMP-001 | policy owner | `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#c-wga-003--canonical-authority-preservation`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#finding-record` | Admission and implementation boundary. |
| SRC-WGA-RMP-002 | human index | `docs/90.references/audits/README.md#audit-pack-registry`; `docs/03.specs/054-workspace-governance-audit-and-remediation/spec.md#traceability`; `docs/04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md#new-audit-pack` | Request routing and planned report ownership. |
| SRC-WGA-RMP-003 | evidence producer | `scripts/validate-document-contract-registry.py#main`; `scripts/validate-markdown-profiles.py#main`; `scripts/validate-links-and-owners.py#main`; `docs/04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md#verification-summary` | Admission and closure evidence. |
| SRC-WGA-RMP-004 | historical snapshot | `docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md#target-operating-model` | Dated comparison only; no current priority authority. |

## Review and Freshness

- Review status: fresh WGIA-010 specification/content and quality reviews are
  `Approved` for its four changed row states. WGIA-009 admission remains
  Approved; WGIA-011's two changed row states have fresh reviews `Approved`
  and an exact staged complete repository quality gate PASS.
- Review disposition: GOV/KNW are implemented and reviewed, both DOC rows are
  integrated without a duplicate delta, HAR/CLAUDE are implemented, reviewed,
  and full-gate complete, and five rows remain `DEFER` unchanged.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: source reports for dated findings and canonical active
  surfaces for implementation.
- Refresh triggers: source finding, review, dependency, priority, target state,
  canonical owner, validation, verification, rollback, blocker, cutover,
  deletion, observation commit, or residual-risk change.
- Hosted, provider-runtime, remote, credential-bearing, and live evidence
  remains `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../04.execution/plans/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Disposition Ledger](legacy-deprecated-and-one-shot-disposition-ledger.md)
