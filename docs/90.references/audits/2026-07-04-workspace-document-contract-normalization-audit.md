---
title: 'Reference: Workspace Document Contract Normalization Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
---

# Reference: Workspace Document Contract Normalization Audit

## Overview

This audit records the T-001 repo-static inventory for workspace document
contract normalization. It captures current frontmatter, section, template,
reference, CI/QA, archive, and historical-evidence drift classes so later
normalization tasks can change the right owner surfaces without blurring
active policy and dated evidence.

## Purpose

- Preserve a dated implementation snapshot before aggressive document
  normalization.
- Separate validator-blocking defects from improvement candidates that need
  contract, template, authored-document, archive, reference, CI/QA, or
  validator follow-up.
- Give T-002 through T-006 concrete evidence and routing without redefining
  active governance in this audit file.

## Reference Type

- Type: dated-implementation-audit
- Source checked: 2026-07-04
- Refresh trigger: rerun when frontmatter schema, template routing,
  repository validators, Stage 03/04/05 document contracts, CI/QA workflow
  docs, archive rules, or reference folder roles change.

## Authority Boundary

- **Authoritative for**:
  - Repo-static audit findings observed on 2026-07-04.
  - Drift categories and recommended remediation routing for the
    workspace-document-contract-normalization execution stream.
  - Evidence boundaries between active contracts, historical evidence, and
    reference snapshots.
- **Not authoritative for**:
  - Active governance policy, template requirements, CI workflow behavior,
    operations runbooks, incident response procedure, or validation script
    semantics.
  - GitHub Actions run status for this branch unless a separate remote check
    is inspected.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret,
    provider runtime, paid-job, or external-service readiness.

## Scope

- Covers `_workspace`, `.github`, `docs/01.requirements`,
  `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`,
  `docs/05.operations`, `docs/90.references`, `docs/98.archive`,
  `docs/99.templates`, `scripts`, and `tests` as document-governance evidence.
- Focuses on frontmatter profile consistency, README boundaries, template
  route parity, active/historical wording separation, SDLC/spec/tests/runbook
  consistency, CI/QA evidence lanes, and automation opportunities.
- Excludes live validation, secret inspection, remote CI inspection, workflow
  semantic changes, provider account changes, and runtime mutation.

## Definitions / Facts

### Inventory Snapshot

| Metric | Result | Notes |
| --- | --- | --- |
| Focused docs Markdown count | 206 | Counted under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and `docs/99.templates`. |
| Frontmatter-authored Markdown count | 181 | All observed `type` values use `sdlc/`, `content/`, or `governance/` prefixes. |
| README count in focused docs | 23 | README files remained frontmatter-free. |
| Common template files without frontmatter | 2 | `readme.template.md` and `progress.template.md` are intentional exceptions that model frontmatter-free outputs. |
| `.github` Markdown files without frontmatter | 3 | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md` are active repository surfaces but not yet represented as frontmatter profiles. |
| Archive Tombstone count | 32 | All observed Tombstones use `type: content/archive-tombstone`, `status: archived`, and `owner: platform`. |
| Incident instances | 0 | `docs/05.operations/incidents/` currently contains only its README; the incident/postmortem folder contract is template and README-owned until an incident exists. |
| `_workspace` files | 0 | `_workspace` exists but did not contribute current document drift evidence in this scan. |

### Profile Counts

| Profile | Count |
| --- | ---: |
| `content/archive-tombstone` | 32 |
| `content/reference` | 15 |
| `governance/memory` | 1 |
| `governance/template-support` | 6 |
| `sdlc/adr` | 10 |
| `sdlc/agent-design` | 1 |
| `sdlc/api-spec` | 1 |
| `sdlc/ard` | 5 |
| `sdlc/data-model` | 1 |
| `sdlc/guide` | 9 |
| `sdlc/incident` | 1 |
| `sdlc/plan` | 30 |
| `sdlc/policy` | 8 |
| `sdlc/postmortem` | 1 |
| `sdlc/prd` | 5 |
| `sdlc/runbook` | 10 |
| `sdlc/spec` | 11 |
| `sdlc/task` | 33 |
| `sdlc/tests` | 1 |

## Findings

| Finding ID | Surface | Evidence | Decision | Routed Task |
| --- | --- | --- | --- | --- |
| WDCN-AUD-001 | Validator gate | `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .` passed after the plan/task residue fix. | No validator-blocking drift is open at T-001. Later changes must keep this gate green after each logical commit. | T-002 through T-006 |
| WDCN-AUD-002 | Frontmatter profiles | Focused scan found 181 authored frontmatter documents with only namespaced `sdlc/`, `content/`, and `governance/` profiles. README files stayed frontmatter-free. | Baseline is mostly implemented. Normalize remaining active surfaces by clarifying whether `.github` Markdown and common template exceptions are contract-owned profile exceptions. | T-002, T-005 |
| WDCN-AUD-003 | Stage 04 historical evidence | Active Stage 04 plans/tasks preserve completed phase and migration-era wording as dated execution evidence. Validator allows this, but readers can confuse old execution notes with current rules. | Preserve chronology but add clearer historical/superseded framing where old evidence could be read as current guidance. | T-003, T-004 |
| WDCN-AUD-004 | Template route parity | `docs/99.templates/support/template-routing.md`, `frontmatter-schema.md`, Stage 00 documentation rules, and `scripts/validate-repo-quality-gates.sh` define the current route and profile model. | Route model is implemented, but T-002 should reconcile all support docs, templates, and validators in one contract unit before broad authored-document edits. | T-002 |
| WDCN-AUD-005 | SDLC/spec/tests/runbook consistency | Stage 03/04/05 documents, `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`, `scripts/README.md`, and `tests/README.md` all separate repo-static evidence from live readiness. | No immediate contradiction found in the current CI/QA boundary. T-005 should still perform a dedicated official-source-backed pass before finalizing CI/CD, QA, and formatting claims. | T-005 |
| WDCN-AUD-006 | Incident folder contract | `docs/05.operations/incidents/` has no incident instance yet. Current route requires incident records under `docs/05.operations/incidents/YYYY/INC-###-<title>/` with the incident file named after the incident and `postmortem.md` beside it. | Keep README/template/validator surfaces aligned before the first real incident file is created. | T-002, T-003 |
| WDCN-AUD-007 | Archive evidence | `docs/98.archive/README.md` indexes 32 Tombstones and preserves the 01-05 mirror structure, including operations incidents. | Archive model is implemented. T-004 should normalize only metadata, framing, and route clarity; do not rehydrate old document bodies. | T-004 |
| WDCN-AUD-008 | Reference folder roles | `docs/90.references/README.md` already separates `audits`, `data`, `research`, `learning`, and `llm-wiki`. Audit status vocabulary is defined in `audits/README.md`. | Reference structure is implemented. T-005 should add CI/QA and formatting alignment evidence without turning references into active policies. | T-005 |
| WDCN-AUD-009 | Scripts README count | `scripts/README.md` describes 7 current shell scripts while the same README tree, inventory, classification matrix, and command contract list 8 scripts including `validate-harness.sh`. | Stale reference wording. Align scripts inventory counts and deletion precheck text during CI/QA/reference alignment. | T-005 |
| WDCN-AUD-010 | Coverage wording boundary | `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` states new application code maintains 90% coverage, while `tests/README.md` says `tests/` does not own app test-pyramid or co-located unit-test rules. The PR template narrows the policy to future testable application code where applicable. | Boundary wording mismatch, not a validator failure. Make the QA guide, tests README, and PR template use one coverage/validation-matrix contract. | T-005 |
| WDCN-AUD-011 | Prior audit historical evidence | `docs/90.references/audits/2026-07-03-workspace-document-governance-hardening-audit.md` records README heading and CI/QA hook-documentation findings that current files have since corrected. | Preserve the dated audit facts, but mark or contextualize them as resolved historical evidence so they are not mistaken for current drift. | T-004 |

## Comparison Analysis

- The workspace has a coherent current contract: frontmatter profiles are
  namespaced, README files are frontmatter-free, templates are split from
  support contracts, and repo-quality gates enforce many structural rules.
- The strongest remaining risk is not missing metadata; it is evidence
  interpretation. Completed Stage 04 work and archive snapshots can contain
  older wording that is true as history but false if read as current policy.
- `.github` Markdown is an active operational surface but currently sits
  outside the frontmatter profile table. This can remain a documented
  exception or become a common-profile route, but the decision should be
  explicit in template support contracts and validator behavior.
- The CI/QA documentation surfaces agree on the static-vs-live boundary. This
  audit did not inspect remote GitHub Actions runs and therefore makes no
  remote CI pass claim.
- The incident route is a high-value preflight contract because no real
  incident instance exists yet. Template and README agreement now reduces
  future incident documentation drift.
- Scripts inventory and coverage-policy wording are the clearest current
  reference/CI-QA improvement candidates discovered by the second-pass review.
- Prior dated audits may contain findings that were accurate when written but
  now read like stale current-state claims. T-004 should preserve the dates and
  add resolved or historical framing instead of deleting evidence.

## Implementation Checklist

| Item | Owner Surface | Action | Status |
| --- | --- | --- | --- |
| Record focused frontmatter inventory. | Audit report | Summarize profile counts, README boundary, and exceptions. | Done |
| Record validator status. | Audit report and task evidence | Store `git diff --check` and repository quality gate outcome. | Done |
| Register audit report. | `docs/90.references/audits/README.md` | Add the dated report to the audit index and structure map. | Done |
| Update Stage 04 task evidence. | Stage 04 task record | Mark T-001 done and record command evidence. | Done |
| Decide `.github` Markdown contract. | Template support and CI/QA docs | Either document as common README-like exceptions or add a dedicated profile/route. | Pending T-002/T-005 |
| Normalize historical Stage 04 evidence framing. | Stage 04 and archive docs | Preserve facts while marking superseded or historical execution notes. | Pending T-003/T-004 |
| Reconcile prior audit resolved findings. | Stage 90 audit references | Preserve dated facts while preventing old pending findings from reading as current drift. | Pending T-004 |
| Align scripts inventory count. | `scripts/README.md` | Reconcile shell-script count with the current inventory and deletion precheck wording. | Pending T-005 |
| Align coverage wording. | CI/QA guide, tests README, PR template | Use the same future app-code coverage and infrastructure validation-matrix boundary. | Pending T-005 |
| Reconcile CI/QA official-source basis. | `.github`, CI/QA guide, scripts/tests README, references | Compare repository claims to official GitHub Actions, Markdown, YAML, and spec-driven sources. | Pending T-005 |
| Add final validator parity evidence. | Validator, task record, progress memory | Confirm all changed surfaces pass deterministic checks. | Pending T-006 |

## Sources

- `git status --short --branch`
- `git diff --check`
- `bash -n scripts/validate-repo-quality-gates.sh`
- `bash scripts/validate-repo-quality-gates.sh .`
- Focused frontmatter inventory over target Markdown files.
- Validator-safe residue scan over `_workspace`, `.github`, `docs`,
  `examples`, `scripts`, `tests`, `.agents`, `.claude`, and `.codex`.
- Stage 04/05/90/98/99 README, template, and support-contract inspection.
- `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `.github/SECURITY.md`, `scripts/README.md`, and `tests/README.md`
  inspection.
- Read-only subagent cross-check for validator-blocking drift, active SDLC
  drift, historical evidence drift, and reference/CI-QA drift.

## Review and Freshness

- Review cadence: on contract or validator change.
- Last reviewed: 2026-07-04.
- Next review trigger: frontmatter schema changes, template route changes,
  CI/QA workflow changes, official-source refresh, archive policy changes, or
  final T-006 validation.

## Related Documents

- [Parent Spec](../../03.specs/014-workspace-document-contract-normalization/spec.md)
- [Parent Plan](../../04.execution/plans/2026-07-04-workspace-document-contract-normalization.md)
- [Task Evidence](../../04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md)
- [Audit Index](./README.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
