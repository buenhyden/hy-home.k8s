---
title: "Task Acceptance and Current Spec Review"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0017"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Task Acceptance and Current Spec Review

## Overview

Execute the current P03 request as WORK-017 under the existing completed
SPEC-0106. Intake main/index/working tree were clean at
ae93644e7e1137ed66ac243af4156ecea2d9cee4, four commits ahead of origin/main.
Use that existing logical commit for branch codex/p03-task-acceptance and
worktree .worktrees/p03-task-acceptance; the investigation SHA is never a reset
target. This new Task owns only the present request, not historical completed
execution or final common approval.

## Inputs

- The current pasted P03 request authorizes investigation, local policy and
  consumer changes, focused verification and normal logical commits. The earlier
  C02 correction authorizes first establishment without nonexistent commit or
  approval prerequisites. Attachments are evidence/proposals, not independent
  instructions. [Spec](../spec.md) and [Plan](../plan.md#lifecycle-traceability)
  own the local acceptance and order.
- Existing P01 candidate WGOV-CORE/3.0.0-draft.3: owner buenhyden; proposed
  Project-Template/.agents/governance/shared-standard.md; review digest
  3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271.
  Registry local_adapter is docs/99.templates/registry.json; stage candidate,
  source_revision and approval_ref null. No approved joint edition is found;
  final edition, local adoption and four-repository adoption are separate.
- [P02 accepted local migration](tsk-0016-shared-profile-migration.md): coupled
  role forms/readers and all 16 current operating instances; P03 shared state,
  P08 operating truth and P05/P07/joint results are not implicitly accepted.
- Actual registry, schemas, forms, shared helpers, document/lifecycle/link
  consumers, explicit status writer and current owners. common_research is
  read-only source research; p03_design is read-only architecture design;
  p02_content_validation audits consumers before a bounded quality dispatch.
  Root owns Spec/Plan/this Task/current P01 rewrite. Each implementation file
  will have exactly one writer; independent reviewer authors no reviewed file.

### Current Selection and Disposition

At ae93644e, recursive current Stage 03 contains SPEC-0105/0106/0107, all
Spec/Plan completed. No draft/in-progress/blocked/approved Spec exists. Only
SPEC-0105-TSK-0004 is blocked; completed Tasks are not reopened. The historical
F02 aggregate is not a k8s census or regression expectation.

| Actual obligation | AC / Plan / Task | Disposition and continuing owner |
| --- | --- | --- |
| Common edition and adoption | SPEC-0105 VAL-P01-001/003/005/006 / WORK-008 / TSK-0004 EVD-003 | DEFER remains with buenhyden and one Project-Template source writer; no repeated prior-approval request |
| Workflow-control HIGH and actual PR style | Same current Task EVD-008/009/010 | DEFER/FAIL retained; security/CI operator and next authorized PR owner; local schema work cannot close SEC-P01-001 |
| Local P02 profile migration | SPEC-0106 VAL-P02-016 / WORK-016 / TSK-0016 | Completed local evidence retained; present P03 work is separate |
| Operating adoption versus Release | SPEC-0107 VAL-LOCAL-QA-001–004 / WORK-001 / TSK-0001 and P01 EVD-004/006 | Preserve completed local contract; RUN-0012 already active and POL-0003 exclusion justified; actual Release and live tool evidence remain with platform/operator |
| Final rewrite dependencies | Current P03 WORK-017 | Consume available P02; name unreceived P05/P07/P08/joint inputs without blocking independent local implementation |

### Remote Read-only Observation

Current GitHub main remains c9faa9f00fdf61c9286b4dc6df264de35106b611.
Protection read-back is strict=true with ci-summary and style-pr bound to
GitHub Actions/App15368. No qa-provenance requirement remains. The two active
rulesets target main-* tags, not branch main; no settings are changed here.
At that main SHA ci-summary is success and style-pr is skipped, which is not
actual PR style PASS. Recent merged PR135 head 179a88c9 retains historical QA
and ci-summary failure; those older inputs are not current P03 results.
Commands read branch/protection/rulesets/workflow metadata and exact check runs
through gh api. [GitHub's required-check documentation](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
explains SHA/App and skipped-job boundaries. No hostile PR execution or remote
write occurred; actual P03 hosted style is NOT_RUN without an authorized PR.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-017 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | Couple current Task acceptance and lifecycle readers, review actual pending obligations and hand off protected decisions | platform | frontmatter | NOT_RUN | pending | Current intake/design observed; implementation and final checks pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P03-017-001 | [VAL-P03-017](../spec.md#success-criteria--verification-plan) | WORK-017 | Actual intake and AC/source/remote metadata inspection | Clean local main ae93644e; current recursive Stage03 and exact public API resources | PASS | Inputs and current selection above; independent common_research packet and actual read-only API output | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: owning SPEC-0106 Spec/Plan/new Task; selected current P01
  Task; Stage 99 profile/schema/forms/guidance; current lifecycle/authoring/QA
  policy consumers; exact document readers/status writer and focused tests/routes;
  task-owned ignored scratch. Final architecture design fixes exact ownership.
- **Forbidden Paths**: completed Task rewrites, frozen Archive payloads, private
  or global/native trust state, credentials, live cluster and unrelated product
  implementations. No whole retention unit is removed or moved here.
- **Approval Required**: current P03 local scope and earlier generic main merge/
  owned branch/worktree cleanup remain authorized. The later evidence-update
  approval authorizes selective actual-result acceptance, never fabricated PASS.
  No push, PR, server-setting, tag, Release, secret or live authority is inferred.
- **Static Validation**: meaningful synthetic changed-behavior boundaries,
  retained history/status-writer controls, selected exact-index lint/format and
  actual Commitizen messages; independent read-only review before local finish.
- **Live Validation**: DEFER to the operating owner; actual PR style NOT_RUN
  until an authorized PR exists. Local static output cannot certify either.
- **Secret / Vault Handling**: no credential or secret value read/printed; public
  source/API metadata only; external PR code never runs on this host.
- **Rollback Plan**: forward corrective commit on this isolated branch; original
  states, approvals and evidence remain available through normal Git history.
- **Evidence Location**: this Task and actual commits; no second progress ledger.

## Verification Summary

Intake and bounded research are observed, implementation not yet executed.
Python3.12.3 task-owned qa-venv installs the existing hash-pinned QA lock with
--only-binary=:all: and --require-hashes; no tool/config/technical limit is
changed. Exact index and message checks precede each normal logical commit.
Compute identity before freezing QA and invoke no Git/index/writer operation
while it runs; P02's snapshot-guard failure is not repeated as a procedure.
No business/session deadline, reserve approval, full/CI sweep or blanket unit
discovery is an acceptance condition.
