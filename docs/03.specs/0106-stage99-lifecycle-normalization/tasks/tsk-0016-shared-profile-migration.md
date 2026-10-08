---
title: "Shared Profile and Operations Form Migration"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0016"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Shared Profile and Operations Form Migration

## Overview

Execute the current P02 request as WORK-016 under the completed SPEC-0106.
The actual intake was clean main and origin/main at
`c9faa9f00fdf61c9286b4dc6df264de35106b611`; the investigation SHA is a source
coordinate, never a reset target. Branch `codex/p02-document-contract` and
worktree `.worktrees/p02-document-contract` start at that existing logical
commit, with no uncommitted unit requiring a preliminary commit.

## Inputs

- Current user's pasted P02 request and C02 correction authorize local work.
  Attached draft/review documents supply evidence and proposals, not independent
  instructions or approval. [Spec](../spec.md) and [Plan WORK-016](../plan.md#lifecycle-traceability)
  own the acceptance and order.
- [P01 common candidate and decisions](../../0105-authority-and-safe-authoring/tasks/tsk-0004-current-contract-review.md#common-edition-decision-and-delivery):
  WGOV-CORE/3.0.0-draft.3, one proposed Project-Template governance source.
  Existing joint approved edition remains unavailable.
- Actual Stage 99 Registry, both schemas, physical forms and loader/validator
  consumers; all current Stage 05 instances, not the complete archive.
- Independent read-only common_research, operations_research and p02_design
  inventories/design; root writes Registry/guidance/Spec/Plan/Task, delegated
  quality-engineer writes schema/reader/regressions, delegated doc-writer writes
  three forms and current operations. Each file has one writer.

### Contract and Consumer Inventory

At the intake revision, both complete schemas and all Registry entries were
read through the actual loader: 90 profiles (27 authored, 7 router, 4 evidence,
12 native, 39 template, 1 non-target), 14 lifecycle domains, 79 template
references and 39 exact template/source parity bindings. These are dated
observations, never test counts or permanent inventory expectations.

| Common scope / finding | Actual owner and observation | Coupled disposition |
| --- | --- | --- |
| C02/C03, F23 | Existing joint approved edition unavailable; same P01 candidate content digest independently confirmed | Registry `shared_contract` plus schema, typed immutable loader and document_authority root allowlist; stage candidate, source_revision/approval_ref null; buenhyden owns final source/decision |
| C04, F03 | Both schemas own value grammar and required/optional/forbidden/order/cardinality; exact matchers route all profiles and native envelopes | Keep existing valid six-key/frontmatter/parent/supersession and native consumers; add optional section-content/order flags only to three operating roles and their forms |
| C05 | task_execution/task-items-v2, Markdown/link/lifecycle readers and sync-task-status.py already share status derivation | Keep single-row frontmatter source; multi-row rows are authored and explicit writer generates header. Clarify form/README/policy guidance; retain role enums pending P03 |
| C04 README | Six common router profiles use identity-free five-section core/active constant; three authored pack-anchor profiles and Archive catalog are distinct | Preserve actual matched paths, language and provider projections; update Stage 99 guidance and current renamed-section navigation only |
| C12, F03/F24/F29 | Three old role forms use separate Type/Traceability headings; generic checker counts H3 alone as body | Six-H2 role cores plus moved relationship section, substantive-body/order checks and Registry-bound owner-lineage lookup; all actual current operating instances migrated |
| F19 | RUN-0012 already active1.0.0 after P01; POL-0003's reciprocal exclusion is justified | Preserve active status and explicit exclusion; no repeated promotion or reopened parent |

The existing authored frontmatter schema needs no new extension or key removal.
Registry root binding is not copied into every document. Internal schema_version
10 identifies the local representation, not the common edition or approval.
No new local WGOV source, template-support ledger, progress table or native
execution claim is introduced.

### Current Operations Review and P08 Handoff

Every row below was independently read and then migrated. For each artifact,
the selected profile matches its registered form; the six role sections contain
authored content; owner remains platform, ID and active state are preserved,
and Related Documents retains the Lifecycle Traceability table and prior
reciprocal links or justified exclusion. This is separate from live evidence,
which was not produced by the migration. P08/platform owns product-specific
truth and actual operator/live verification.

| Artifact | Profile / form | Item content and reference disposition | Current owner / state | Actual evidence and remaining boundary |
| --- | --- | --- | --- | --- |
| GDE-0010 | operation/guide / guide form | QA explanation, concept audience, local/hosted/runtime distinctions; RUN-0011/0012 pointers retained | platform / active | Static guidance review; no hosted/runtime observation |
| POL-0001 | operation/policy / policy form | PLAT controls and live exception responsibility; preserve old external exceptions anchor, update current pointers | platform / active | Static controls, actual live exception records not reauthenticated |
| POL-0003 | operation/policy / policy form | cert-manager/Istio/Kiali controls and explicit no-eligible-reciprocal-source exclusion | platform / active | CPU exception lower-bound wording remains P08 semantic review; no invented rule |
| POL-0004 | operation/policy / policy form | Rollouts/Notifications/Headlamp controls, secret owner, historic SPEC-0004/0005 exclusion | platform / active | Existing manual promotion approval boundary; live behavior unobserved |
| POL-0005 | operation/policy / policy form | Observability control register and RUN-0007/0008/0009 references | platform / active | External observability owner boundaries retained; live metrics/logs unobserved |
| POL-0007 | operation/policy / policy form | Workload admission, deployment/network/security/GitOps modules and verification responsibilities | platform / active | Static implementation references; no deployment or secret check run |
| RUN-0001 | operation/runbook / runbook form | Bootstrap and unique external EndpointSlice recovery; POL-0001 and architecture references | platform / active | Intended steps preserved; live bootstrap not run |
| RUN-0002 | operation/runbook / runbook form | ESO/Vault diagnosis, CoreDNS/CA recovery and approved break-glass boundaries | platform / active | No credential value read or recovery executed |
| RUN-0003 | operation/runbook / runbook form | cert-manager/Istio/Kiali prechecks and symptom-specific recovery; POL-0003 linkage | platform / active | Static review; no live status/reset/sync |
| RUN-0004 | operation/runbook / runbook form | Headlamp auth and recovery; remove token-producing stdout command, private operator handoff | platform / active | Independent security review PASS for repair; no token issuance or exposure observed |
| RUN-0007 | operation/runbook / runbook form | Kiali 401/DNS/CA/endpoints/egress branches and external workspace handoff | platform / active | No availability or connectivity observation |
| RUN-0008 | operation/runbook / runbook form | ArgoCD metrics/relabeling diagnosis; RUN-0009 still owns prom helper | platform / active | No external Prometheus query or chart mutation |
| RUN-0009 | operation/runbook / runbook form | Alloy metric/log/remote-write branches and canonical prom query helper | platform / active | External credentials and observability service remain outside scope |
| RUN-0010 | operation/runbook / runbook form | Procedure 1–5 including Vault integration regrouped; CA-validated status-only HTTPS replaces insecure/body-printing check | platform / active | Independent security review PASS; absent CA holds TLS verdict; no actual TLS/deployment result |
| RUN-0011 | operation/runbook / runbook form | Stage90 classification, consumer transfer and Archive disposition; existing owner references | platform / active | Static guidance; frozen bytes and retention state unchanged |
| RUN-0012 | operation/runbook / runbook form | Existing P01 active release preflight and reciprocal SPEC-0107 relation | platform / active | P01 CLI/help evidence retained; trusted git-cliff and real publication DEFER |

No current Incident/Postmortem artifact exists at this snapshot. Their distinct
detected/resolved/published forms and state meanings remain supported.

### Common Adoption and Continuing Owners

WGOV-CORE/3.0.0-draft.3 uses the same candidate bytes with SHA-256
`3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
Joint owner buenhyden; proposed single source
`Project-Template/.agents/governance/shared-standard.md`; source commit and
approval reference not created. The digest identifies review content only.
The existing local Registry is the adapter; Kubernetes/GitOps/bootstrap/external
service procedures and current language/native/state mappings are explicit
extensions. Final edition approval, local adoption and four-repository adoption
are pending separately, with unread repositories never marked adopted.

P03 receives the existing Spec/Plan execution-state vocabulary and missing Task
superseded transition as shared migration decisions needing provenance, plus
the chosen generated-header option. Keep Requirement approved, ADR accepted,
operations active, Incident resolved and Postmortem published meanings intact.
P08 receives the three role forms, all migrated current instances, the per-row
review above and actual live/product limitations. Stage 99/platform owns the
durable adapter and readers after local implementation acceptance; buenhyden
owns the joint source/edition decision. SEC-P01-001 HIGH remains with the P01
security/CI operator for workflow-changing PRs and releases, separate from
this local document migration.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-016 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | Migrate the shared profile adapter and current operating forms with truthful handoffs | platform | frontmatter | PASS | pending | EVD-016 independent implementation review and EVD-018 final exact-index QA PASS; closing acceptance and local integration remain pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-016-001 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Intake and source inspection | Actual clean main c9faa9f; current Registry/schema/form/consumer/operations graph | PASS | Inputs above and subsequent bounded inventory in this Task | pending |
| EVD-P02-016-002 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Scope commit index/message | Three Spec/Plan/initial-draft Task paths; actual commit 30f52bfa716449140ae9c94ece3882f426177f7e | PASS | qa.py staged: six selected gates PASS; actual commitizen message check PASS; normal commit, unchanged registered Task form source | pending |
| EVD-P02-016-003 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | New binding/content/order/lineage regressions | tests.test_shared_contract_binding, test_operations_section_contract, test_operations_lineage_contract; Python3.12.3 and hash-pinned dependencies | PASS | 11 synthetic tests PASS after RED; initial wrong API invocation errors preserved as setup mistake, corrected API RED had 3 expected missing-schema/typed errors | pending |
| EVD-P02-016-004 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Retained exact form and Task writer controls | Stage05 template parity method, row-summary/result method, two writer preservation/single-row methods | PASS | Four named existing methods PASS; no all-tests discovery or full/CI sweep | pending |
| EVD-P02-016-005 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent operations/security review | All 16 current artifacts; changed RUN-0004 token and RUN-0010 TLS instructions | PASS | operations_research and doc-writer per-row packet; server_security_review scoped PASS; no live/secret commands | pending |
| EVD-P02-016-006 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent parser review | Placeholder checkbox, empty checkbox, anchor-only and TODO-only fence inputs | FAIL | p01_review MEDIUM content boundary finding; root routes focused repair and re-review before acceptance | pending |
| EVD-P02-016-007 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Repair the EVD-006 content-boundary FAIL | Seven previously accepted placeholder variants plus meaningful checklist/code/anchor text controls | PASS | quality-engineer RED seven expected failures then GREEN seven content/lineage methods; scoped Ruff check/format PASS; independent final review pending | pending |
| EVD-P02-016-008 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent recovery placement review | RUN-0010 abort and RUN-0002 troubleshooting/SAN remediation originally remained under Procedure/Verification | FAIL | p01_review MEDIUM role-placement finding; actual commands and approvals retained for repair | pending |
| EVD-P02-016-009 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Repair EVD-008 role placement | Recovery-specific submodules moved under Recovery and Escalation in two runbooks | PASS | doc-writer unique-command/section and diff checks PASS; forward checks remain Procedure/Verification; independent final review pending | pending |
| EVD-P02-016-010 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | First integrated staged QA | 33-path index tree 68369cdb06580595916b5c0cf4c9eb49d10aad6c after scope commit | FAIL | Existing selector chose 17 leaves: 16 PASS, selected-style FAIL. Narrow diagnosis found MD033 at POL-0001's compatibility anchor; canonical broad scripts/tests routes also selected unrelated Archive/Kubernetes leaves, recorded as observations rather than new acceptance gates | pending |
| EVD-P02-016-011 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Exact document selection repair | Document-only paths, registry route, near-name other scripts, mixed GitOps input | PASS | quality-engineer RED 11 expected failures then five GREEN methods; new exact routes preserve other product and mixed-change behavior; all 16 new focused methods PASS after integration | pending |
| EVD-P02-016-012 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Repair EVD-010 style cause | POL-0001 compatibility anchor; pinned markdownlint-cli2 v0.22.1 | PASS | Single-line documented MD033 exception preserves old fragment; exact-file lint PASS; pinned Ruff check/format on changed Python PASS; final changed-index staged check still required | pending |
| EVD-P02-016-013 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Integrated staged QA after style/selection repair | 36-path index tree 29b3aa9cc25f17d7c5241141fe7d1492503c2c6f | PASS | qa.py staged rc0: all 12 selected gates PASS; this snapshot precedes the EVD-015 helper-route repair, whose final index requires fresh checks | pending |
| EVD-P02-016-014 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent future-scope review | Standalone document_contracts.py and document_authority.py changes | FAIL | p01_review MEDIUM: first narrow route dropped historical guards although these helpers also own Archive contracts; Stage 99 input still selected them in EVD-013, so that result is not invalidated retroactively | pending |
| EVD-P02-016-015 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Restore shared-helper historical guards | Exact shared-document-history-readers route and standalone/narrow/mixed/near-name synthetic inputs | PASS | quality-engineer RED both helper subcases, then six focused tests GREEN; shared helpers select Archive plus document gates, other readers remain narrow, product and mixed routes retained; Ruff and JSON parse PASS | pending |
| EVD-P02-016-016 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Independent final implementation review | Actual repaired working diff; p01_review code-reviewer did not author any changed file | PASS | Placeholder content, recovery placement, compatibility anchor, candidate null proof, identities/states and helper historical guards re-reviewed; no unresolved required finding. Reviewer ran six standalone scope-selection methods PASS; final index and closing disposition still require observation | pending |
| EVD-P02-016-017 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Changed-index integrated QA snapshot guard | 36-path tree e5c39c46a9f4a3223f0e1087cb1894b5958a828f | FAIL | All 12 leaves PASS but aggregate rc1: source HEAD/index/files changed during QA. Root ran git write-tree during execution, which can update raw-index cache metadata; no unstaged content difference observed. This is not final QA PASS. Identify input before the next run and invoke no Git/index/writer command while it runs | pending |
| EVD-P02-016-018 | [VAL-P02-016](../spec.md#success-criteria--verification-plan) | WORK-016 | Final frozen implementation index and message | 36-path tree 8c00fa96b8cf45069621b3d5c2dc573607220670; unchanged pinned tools/config/trust; no Git/index/writer during QA | PASS | qa.py staged aggregate rc0, all 12 selected gates PASS including final lint/format and both snapshot guards; actual implementation message previously PASS and used unchanged; normal commit d67bc63ee446fbb2b9c8ab5a69a0ec3a6944746d preserves the checked tree | pending |

### Executed Commands and Input Identity

Commands below run from `.worktrees/p02-document-contract`; interactive shell
uses `rtk proxy` and the hash-pinned Python 3.12.3 environment at
`_workspace/qa-venv`. QA executes the registered selected leaves read-only in
an isolated exact-index snapshot. Its PASS never authenticates approval,
external links, provider delivery, hosted PR style or live operations.

```bash
_workspace/qa-venv/bin/python -m unittest tests.test_shared_contract_binding tests.test_operations_section_contract tests.test_operations_lineage_contract tests.test_document_scope_selection -v
_workspace/qa-venv/bin/python -m unittest tests.test_document_strict_cutover.Stage05TerminalOwnershipTests.test_operation_templates_share_authored_lifecycle_and_fields tests.test_task_execution_contract.TaskExecutionContractTests.test_status_summary_and_result_are_checked_from_rows tests.test_task_summary_writer.TaskSummaryWriterTests.test_explicit_write_preserves_all_other_bytes_and_file_mode tests.test_task_summary_writer.TaskSummaryWriterTests.test_one_row_frontmatter_marker_and_matching_multirow_are_noops -v
_workspace/qa-venv/bin/python scripts/qa.py staged
_workspace/qa-venv/bin/python -m pre_commit run commitizen --hook-stage commit-msg --commit-msg-filename _workspace/p02-scope-message.txt
_workspace/qa-venv/bin/python -m pre_commit run commitizen --hook-stage commit-msg --commit-msg-filename _workspace/p02-implementation-message.txt
```

The actual UTF-8 messages were checked with the pinned Commitizen grammar:
`docs: record shared profile migration scope` (committed 30f52bf) and
`feat: migrate shared operations profiles and consumers` (PASS, committed d67bc63).
Focused GREEN observations precede the final changed-index checks; they do not
stand in for them. Required lint/format is the selected-style leaf in staged QA,
not a separate repeated hook leaf. Normal Git hooks remain connected; no
skip, trust override or hook change is used.

## Approval and Safety Boundaries

- **Allowed Paths**: Stage 99 Registry/schema/forms/README; current operations;
  document-authoring policy; exact document readers, central impact routes and focused regressions;
  owning SPEC-0106 Spec/Plan/Task; owned worktree scratch.
- **Forbidden Paths**: frozen archive bodies, private/global/native trust state,
  live cluster, secrets, credentials and unrelated implementations.
- **Approval Required**: current P02 authorizes local edits, selected validation
  and normal commits. Final common edition and joint adoption await actual
  buenhyden decisions; no repeated request for nonexistent prior approval.
  The user's earlier explicit main merge and development branch/worktree cleanup
  instruction remains the selected local finish, confirmed in independent
  read-only scope review. Verify clean main and exact reviewed ancestry, use
  fast-forward only and remove only this owned branch/worktree after preserving
  unique evidence. P01's exact server approval grants no new remote/live scope.
- **Static Validation**: synthetic content/schema regressions, retained Task
  writer/status controls and selected final-index document/style/message checks.
- **Live Validation**: DEFER to P08 operating owner; no command here certifies
  current service availability, trusted release tools or publication.
- **Secret / Vault Handling**: no values read or printed. Replace unsafe token
  output guidance and distinguish HTTPS reachability from certificate trust.
- **Rollback Plan**: forward correction in this branch; Git owns original bytes.
- **Evidence Location**: this Task, actual commits and selected QA receipts.

## Verification Summary

The coupled implementation is committed at d67bc63 with the exact EVD-018
index, all 12 selected gates and both snapshot guards PASS. EVD-017 retains the
prior aggregate FAIL separately from its passing leaves; the corrected run
identified input before QA and invoked no Git/index/writer during execution.
Independent parser, recovery-placement and
shared-helper selection FAILs and their subsequent repairs are all retained.
The style repair preserves the old fragment with a documented single-line
MD033 exception; five current links use the canonical new fragment. The
36-path integrated input passed all 12 selected gates. The subsequent exact
shared-helper route repair preserves Archive guards for helpers that own
historical contracts; standalone Markdown/link readers remain narrow and mixed
product changes retain their checks. Stage 99 machine-contract and shared-helper
routes keep historical-contract/integrity checks without rewriting frozen
payloads. Broader selector cleanup belongs to P07, not an added omnibus gate.
Completed parents stay completed. Shared authority/state and
language decisions go to P03, operating truth and live verification to P08.
No remote/live PASS, common-edition approval or joint adoption is inferred.

### Local Acceptance and Finish Preparation

This evidence commit follows the actual ready implementation commit with the
legal in-progress transition. The single Task row keeps its frontmatter marker;
there is no second authored status field. Closing acceptance will assess
VAL-P02-016 against the actual implementation, independent review and checks,
then record the legal completed transition. This local scope does not require
fabricated joint approval or live evidence. P01's common-decision/HIGH Task is
not closed by this work.

The selected finish is clean-main fast-forward integration, followed by only
the owned P02 branch/worktree removal. Root main was clean at c9faa9f before
finish preparation. Unique acceptance/review/failure evidence is in this Task
and Git; the original shared candidate remains in the main checkout's P01
scratch with its recorded digest. Owned tool environments and temporary message
files are disposable; preserve any otherwise unique public receipt before
worktree removal. Actual final closing-index checks, integration and cleanup
will be reported only after they occur; no remote push/PR/release is included.
