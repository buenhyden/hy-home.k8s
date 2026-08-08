---
title: 'Task: Workspace Governance Audit and Remediation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-09
---

# Task: Workspace Governance Audit and Remediation

## Overview

This Task is the durable execution and evidence ledger for the approved
[Workspace Governance Audit and Remediation Plan](../plans/2026-08-09-workspace-governance-audit-and-remediation.md)
and [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md).
It tracks the exact ten-file Current audit pack, canonical-owner audit and
remediation, machine-contract cutover, evidence-gated cleanup, independent
reviews, terminal verification, and lifecycle closure.

Detailed worker and review reports live under the ignored SDD directory
`.superpowers/sdd/2026-08-09-workspace-governance-audit-and-remediation/` while
the branch is active. This Task records only durable results, exact evidence,
limitations, logical commits, and unresolved blockers.

## Inputs

- [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../plans/2026-08-09-workspace-governance-audit-and-remediation.md)
- [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Audit collection](../../90.references/audits/README.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- [RIA data owner](../../90.references/data/reference-information-architecture.json)
- Direct human design approval and Spec approval on 2026-08-09

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WGIA-000 | VAL-WGA-001, VAL-WGA-012 | Activate Spec/Plan/Task and standalone execution relation | primary agent | Done | Active reciprocal execution is registered. Approval-date regression reproduced RED and is GREEN after exact ISO calendar-date parsing; focused checks and the complete repository quality gate pass. | Spec 054, ADR-0022, reciprocal Plan/Task, indexes, `standaloneExecutions` row, links/owners fixture/self-test; strict registry 492 paths; Markdown profiles 0; strict links PASS; Ruff/compile/diff PASS; Python review Approved; Spec review finding fixed. |
| WGIA-001 | VAL-WGA-001, VAL-WGA-002 | Freeze observation identity and establish exact pack/finding contracts | assigned worker | Done | Bounded draft successor foundation is complete: ten declared files, 30 sequential request rows with one linked report/heading owner and current evidence each, nine profile-compliant report forms, closed finding/source/review/freshness conventions, and no Current-pointer or Stage 98 change. | [Focused evidence](#wgia-001-focused-evidence): initial exact pack/request probe RED at 0/0; malformed missing/duplicate/unknown member, duplicate-owner, incomplete-field, invalid-vocabulary, and Stage 98 fixtures rejected; GREEN 10 files/30 rows/9 reports/14 conceptual finding fields/8 verdicts/4 depths; exact evidence-path existence, strict registry 502 paths, Markdown profiles 0, strict links/owners and complete repository quality gate PASS; specification, quality, and Python reviews Approved. |
| WGIA-002 | VAL-WGA-002, VAL-WGA-003 | Audit purpose, roles, governance, operating contracts, and provider shims | assigned worker | Queued | Not executed. | Governance report, owner matrix, finding register, focused gates and reviews. |
| WGIA-003 | VAL-WGA-002, VAL-WGA-004 | Audit SDD, SDLC, documentation, templates, README rules, and guides | assigned worker | Queued | Not executed. | Documentation report, registry/template evidence, focused gates and reviews. |
| WGIA-004 | VAL-WGA-002, VAL-WGA-005 | Audit CI/CD, GitHub Actions, QA, formatting, lint, syntax, tests, fixtures, Validation and Verification | assigned worker | Queued | Not executed. | Delivery/QA report, lane matrix, dormant-control disposition, gates and reviews. |
| WGIA-005 | VAL-WGA-002, VAL-WGA-006 | Audit harness, loop, scripts, fixtures, checkpoints, blockers, recovery, and handoff | assigned worker | Queued | Not executed. | Harness/loop report, state/owner matrices, focused gates and reviews. |
| WGIA-006 | VAL-WGA-002, VAL-WGA-007 | Audit LLM-WIKI, knowledge routing, and memory classes | assigned worker | Queued | Not executed. | Knowledge/memory report, generator and lifecycle evidence, reviews. |
| WGIA-007 | VAL-WGA-002, VAL-WGA-008 | Audit integrated orchestration and every current AI-agent role | assigned worker | Queued | Not executed. | Exact role/adaptor/model/evaluation matrix, focused gates and reviews. |
| WGIA-008 | VAL-WGA-002, VAL-WGA-009 | Audit security and approval boundaries | assigned worker | Queued | Not executed. | Security report, trust/control matrix, static gate evidence and review. |
| WGIA-009 | VAL-WGA-010, VAL-WGA-012 | Build disposition ledger and integrated remediation roadmap | assigned worker | Queued | Not executed. | Candidate/consumer ledger, roadmap, review dispositions, focused gates. |
| WGIA-010 | VAL-WGA-003, VAL-WGA-004, VAL-WGA-007, VAL-WGA-012 | Correct accepted governance, documentation, and knowledge owner conflicts | assigned worker | Queued | Not executed. | RED/GREEN tests, canonical-owner diffs or reviewed no-delta evidence. |
| WGIA-011 | VAL-WGA-005, VAL-WGA-006, VAL-WGA-008, VAL-WGA-009, VAL-WGA-012 | Correct accepted delivery, harness, agent, and security owner conflicts | assigned worker | Queued | Not executed. | RED/GREEN tests, owner-family commits or reviewed no-delta evidence. |
| WGIA-012 | VAL-WGA-011 | Cut over the sole Current audit and mutable consumers atomically | assigned worker | Queued | Not executed. | RIA/profile/index/link RED/GREEN, protected historical baseline, atomic commit. |
| WGIA-013 | VAL-WGA-010 | Delete only proof-complete candidate artifacts | assigned worker | Queued | Not executed. | Zero-consumer proof, isolated/staged post-delete validation, exact deletions or reviewed no-deletion result. |
| WGIA-014 | VAL-WGA-001–012 | Re-audit, close criteria, run terminal QA/reviews, clean residue, and hand off branch finishing | primary agent | Queued | Not executed. | Criterion walk, complete gates, whole-branch review, logical commit ledger, done lifecycle. |

## Approval and Safety Boundaries

- **Allowed Paths**: repository-static owners under root governance adapters,
  `docs/00.agent-governance/**`, `docs/01.requirements/**` through
  `docs/05.operations/**`, `docs/90.references/**` except protected historical
  bodies unless navigation metadata is explicitly mutable, `docs/99.templates/**`,
  `.github/**`, `scripts/**`, `tests/**`, and exact proven deletion candidates.
- **Forbidden Paths**: every existing `docs/98.archive/**` payload, digest,
  envelope, and record; unrelated user changes; user/global provider config;
  secret values; remote or live resources.
- **Approval Required**: any change to approved PRD/ARD/accepted ADR/operations
  policy, ambiguous architecture or authority, live/provider/hosted/remote
  action, credential handling, destructive external action, push, PR, or merge.
- **Static Validation**: exact work-package checks plus strict registry,
  Markdown profiles, links/owners, RIA, generated-index checks, affected
  validators, archive validation, full quality gate, harness, diff checks, and
  pre-commit when available.
- **Live Validation**: `DEFER`; this execution has no live, hosted, provider-
  runtime, authenticated, credential-bearing, or remote authorization.
- **Secret / Vault Handling**: do not read, print, copy, rotate, or write secret
  values. Static secret-reference and policy structure may be inspected.
- **Rollback Plan**: keep every non-empty work package in a logical commit;
  revert the affected unit. Current-pointer and deletion changes are separate
  commits validated in staged or isolated trees before commit.
- **Evidence Location**: this Task, the ten-file audit pack, canonical owner
  diffs and tests, durable progress, Git commits, and ignored task/review
  reports while execution is active.

## Verification Summary

WGIA-000 activation is complete. No topic audit, canonical remediation,
Current pointer cutover, or deletion is complete. The
2026-07-11 audit remains Current until WGIA-012 passes atomically. Repository-
static evidence will be recorded per work package; hosted, provider-runtime,
remote, credential-bearing, and live evidence remains `DEFER`.

WGIA-001 is complete as a bounded draft successor foundation. Its conservative
`Partial` findings establish source and owner inventories; focused, staged,
and complete repository validation pass, and specification, quality, and
Python reviews are Approved. It does not complete WGIA-002 through WGIA-009 or
promote any scope to `Aligned`.

### WGIA-001 Focused Evidence

- **Scope and changed paths**: the exact ten files under
  `docs/90.references/audits/2026-08-09-wgia/`, this Task's WGIA-001 evidence,
  the bounded Plan/progress entries, and the README profile inventory fixture,
  validator expectations, and fixture documentation. No Current audit collection pointer,
  `referenceCurrentPacks`, RIA owner/schema/producer/test, historical pack body,
  or Stage 98 path changed.
- **Acceptance IDs**: VAL-WGA-001 and the WGIA-001 foundation portion of
  VAL-WGA-002.
- **Observation and inventory**: `git rev-parse HEAD` returned exact SHA
  `50628b84165479b03efc0a25be075a49c91a9aef`; `git ls-tree -r --name-only
  <SHA> | wc -l` returned 848. Bounded path counts include 461 `docs/`, 48
  `scripts/`, 67 `tests/`, 16 `.github/`, 35 `.agents/`, 17 `.claude/`, 18
  `.codex/`, 13 `.gemini/`, 81 `gitops/`, and 44 protected Stage 98 files.
- **RED**: the pre-creation exact shell probe exited 1 with
  `WGIA-PACK-EXACT FAIL expected=10 actual=0` and
  `WGIA-REQUEST-EXACT FAIL expected=30 actual=0`.
- **Negative probes**: an in-memory Node probe rejected missing and duplicate
  members, corrected unknown-member input, duplicate owner, incomplete finding,
  invalid verdict, invalid evidence depth, and synthetic Stage 98 delta with
  their closed failure codes. No new machine contract or tracked fixture was
  created.
- **GREEN**: the post-write Node parser returned
  `WGIA-PACK-EXACT PASS files=10 requests=30 reports=9` and
  `WGIA-FINDING-CONTRACT PASS`; each finding has one ID heading plus 13 labeled
  fields, for 14 conceptual fields total, and uses the closed eight-verdict and
  four-depth vocabularies.
- **Evidence normalization**: quality-review fix round 2 replaced generic
  finding/source evidence in all nine reports with exact repository-relative
  paths and selectors. The observation-commit probe passed 203 references over
  94 unique paths with zero missing and zero broad-directory values; the
  selector probe passed 122 unique references with zero invalid heading, JSON
  key, script, workflow, manifest, or configuration selectors.
- **Focused profiles and links**:
  `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
  returned zero violations; `python3 scripts/validate-links-and-owners.py
  --root . --mode strict` returned `PASS CROSS-DOCUMENT`.
- **Focused registry and diff**:
  `python3 scripts/validate-document-contract-registry.py --root . --mode
  strict` passed with 502 paths, zero uncovered, and zero ambiguous. The first
  untracked-file `git diff --no-index --check` probe found one trailing blank
  line in four reports; removing only those lines made the exact ten-file rerun
  pass. The first complete gate run then reproduced
  `README program-created active paths must equal the current new inventory`.
  GREEN added the exact lexicographic WGIA snapshot-pack README row and advanced
  only active/program-created counts from 51/6 to 52/7 while preserving
  baseline67, active-baseline45, retired-baseline22, retired-program-created1,
  and retired23. Registry and Markdown self-tests, `git diff --check`, and
  `git diff --cached --check` pass; the observation-commit Stage 98 diff is
  empty. Final count commands return 10 pack files and 30 request rows.
- **Lane results**: targeted `PASS`; affected/staged checks and the complete
  `bash scripts/validate-repo-quality-gates.sh .` lane `PASS` with final exit
  0. Formatter-review and rerun are `SKIP` because no formatter was invoked.
  Hosted CI and remote/live are `DEFER` because no hosted, provider-runtime,
  authenticated, credential-bearing, remote, or live action was authorized.
- **Tool limitation**: RTK 0.34.3 is available, but `rtk gain` failed to
  initialize its tracking database with error code 14. Per the Codex provider
  contract, underlying read-only/focused commands were used without inspecting
  private databases or credential files. Recorded tool versions are Git 2.43.0,
  Python 3.12.3, and Node v24.16.0.
- **Reviewer and disposition**: specification review, final quality re-review,
  and the README-inventory Python review are `Approved` with no remaining
  Critical or Important finding. The foundation remains `draft`; WGIA-014 owns
  final whole-branch review.
- **Rollback**: remove only the exact ten new pack files and revert the bounded
  WGIA-001 Task/progress entries before any later task consumes them.
- **Residual risk and next owner**: source inventories are intentionally
  incomplete topical analysis. WGIA-002 through WGIA-009 own audit/review;
  WGIA-012 alone owns Current cutover.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WGIA-000](../plans/2026-08-09-workspace-governance-audit-and-remediation.md#work-breakdown) | Done. | RED: the different valid approval date was rejected with `STANDALONE-EXECUTION-APPROVAL`. GREEN: links/owners self-test accepts both valid dates and rejects the invalid calendar date. Strict registry reports 492 paths with 0 uncovered/ambiguous; Markdown profiles report 0 violations; strict links, Ruff, Python compile, cached diff, and complete repository quality gate pass. Python review is Approved; the Spec review's sole index-drift finding was fixed and no other Critical/Important finding remained. |
| N/A — WGIA-001 shares the Plan and Spec sources above | Done as a bounded draft foundation. | Exact observation SHA; RED 0/0 pack/request probe and README current-inventory mismatch; malformed-fixture rejection; GREEN 10 files, 30 sequential request rows, 9 reports, 14 conceptual finding fields, 8 verdicts, 4 evidence depths, and exact observation-commit evidence paths; strict registry 502 paths, Markdown profiles 0, strict links/owners, cached/worktree diff, and complete repository quality gate PASS; specification, quality, and Python reviews Approved; Stage 98 and Current-pointer boundaries preserved. WGIA-014 owns whole-branch review. |
| N/A — WGIA-002 shares the Plan and Spec sources above | Queued. | Governance audit and review evidence will be recorded here. |
| N/A — WGIA-003 shares the Plan and Spec sources above | Queued. | SDLC/document/template audit evidence will be recorded here. |
| N/A — WGIA-004 shares the Plan and Spec sources above | Queued. | CI/QA/Validation/Verification audit evidence will be recorded here. |
| N/A — WGIA-005 shares the Plan and Spec sources above | Queued. | Harness/loop/script/blocker audit evidence will be recorded here. |
| N/A — WGIA-006 shares the Plan and Spec sources above | Queued. | LLM-WIKI and memory audit evidence will be recorded here. |
| N/A — WGIA-007 shares the Plan and Spec sources above | Queued. | Integrated and role-specific agent audit evidence will be recorded here. |
| N/A — WGIA-008 shares the Plan and Spec sources above | Queued. | Security/approval audit evidence will be recorded here. |
| N/A — WGIA-009 shares the Plan and Spec sources above | Queued. | Candidate disposition and integrated roadmap evidence will be recorded here. |
| N/A — WGIA-010 shares the Plan and Spec sources above | Queued. | Governance/documentation/knowledge remediation evidence will be recorded here. |
| N/A — WGIA-011 shares the Plan and Spec sources above | Queued. | Delivery/harness/agent/security remediation evidence will be recorded here. |
| N/A — WGIA-012 shares the Plan and Spec sources above | Queued. | Atomic Current transition evidence will be recorded here. |
| N/A — WGIA-013 shares the Plan and Spec sources above | Queued. | Exact deletion or reviewed no-deletion evidence will be recorded here. |
| N/A — WGIA-014 shares the Plan and Spec sources above | Queued. | Terminal criterion, QA, review, residue, and closure evidence will be recorded here. |
