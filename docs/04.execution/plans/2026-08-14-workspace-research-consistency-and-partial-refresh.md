---
title: 'Workspace Research Consistency and Partial Refresh Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-14
---

# Workspace Research Consistency and Partial Refresh Plan

## Overview

This Plan executes the combined constraint-consistency and `Partial`
re-observation cycle designed by
[Spec 057](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md)
over the existing `2026-08-08-wer` research pack.

**Goal.** Reconcile the pack against its current repository shape and record a
dated 2026-08-14 delta for the twelve `Partial` requirement rows, without
creating a new pack, a duplicate report, or a new requirement ID.

**Architecture.** Eight logical work packages in a fixed order. Cleanup runs
before research so no research cites a path scheduled for removal. Scope
re-projection and cross-link reconciliation run after all content changes so
link validation observes the terminal repository shape. Four research packages
are mutually disjoint by owner file and are the only parallel stage.

**Tooling.** Python validators under `scripts/`, `pre-commit`, `git`, and
read-only public documentation fetches. No cluster, hosted CI, provider
runtime, or credential-bearing access.

Direct human approval on 2026-08-14 authorizes this standalone execution relation.
No separate PRD or ARD is required or part of this standalone lifecycle.

## Context

The active pack holds thirteen topic reports plus a README, 33 `REQ-WERPC`
owners, 73 source IDs, and 77 claim IDs. Its scope application index records
that all twelve `Partial` rows are blocked by four evidence classes that
repository-static work cannot obtain: live cluster and effective RBAC, hosted
CI run outcomes, provider runtime behavior, and human usability or stakeholder
judgement.

The immediately preceding refresh, owned by the standalone execution registered
for spec `056`, re-tested the same twelve rows on 2026-08-12 and promoted none.
This Plan therefore targets a dated delta, not promotion.

### Global constraints

Copied verbatim from the owning Spec. Every work package inherits these.

- New sources continue from `SRC-WERPC-074`; new claims continue from
  `CLM-WERPC-010-01`. No existing ID is renumbered, reordered, or rewritten.
- Findings are appended as dated `2026-08-14` subsections to existing reports.
  No new research folder and no duplicate report.
- Workspace observation and external source result are recorded as separate
  evidence. An unreachable source is recorded as `unreachable`, never as
  `unchanged`, and the prior observation date is preserved.
- Retained `Partial` or `DEFER` names the missing evidence, the owning
  authority, the safe collection boundary, and the refresh trigger.
- Only two deletion targets are permitted: tracked `graphify-out/2026-06-04/`
  and untracked local `sessions/` files. Every other candidate is reported.
- `.worktrees/docs-sdlc-governance-consolidation` and its branch are never
  modified.
- Research subagents are read-only. All tracked-file mutation is performed by
  the primary agent.
- Each work package is one non-empty logical commit.
- Temporary files live only under the session scratchpad path and are absent
  before terminal validation.

## Goals & In-Scope

- Register and activate the standalone Spec/Plan/Task relation for spec `057`.
- Build the closed topic ledger mapping all twenty-three requested topics onto
  existing `REQ-WERPC` owners plus the three admitted new owners.
- Admit `REQ-WERPC-034` (Spec), `REQ-WERPC-035` (Task), and `REQ-WERPC-036`
  (Plan) as coverage-matrix owners over existing document-family research.
- Execute the two approved one-off removals behind a consumer check.
- Re-observe the workspace and re-check external sources for `REQ-WERPC-006`,
  `008`, `009`, `014`, `020`, `022`, `023`, `025`, `026`, `028`, `032`, `033`.
- Re-project the ten governance scopes and re-test the five unowned canonical
  paths.
- Reconcile the pack README, source and claim ledger, scope application index,
  collection README, and durable progress ledger.
- Close with repository-static validation evidence and lifecycle `done`.

## Non-Goals & Out-of-Scope

- Creating a new dated research pack, a duplicate report, or a new
  `REQ-WERPC` requirement ID.
- Live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry inspection.
- Hosted CI execution, deployment, promotion, or rollback evidence.
- Provider-runtime discovery, authentication, delegated execution, or model
  resolution evidence.
- Modifying `.worktrees/docs-sdlc-governance-consolidation` or its branch.
- Any manifest, workflow, permission, hook, or policy mutation.
- Promoting a `DEFER` boundary on the strength of a static or metadata `PASS`.
- Editing Stage 98 archive content.

## Work Breakdown

| ID       | Work package                                 | Depends on            | Entry gate               | Exit evidence                                                                    |
| -------- | -------------------------------------------- | --------------------- | ------------------------ | -------------------------------------------------------------------------------- |
| WRCP-000 | Activate the standalone execution            | Written Plan approval | Clean tree; Spec `draft` | Registry entry, ADR reciprocity, three `active` statuses, indexes, commit        |
| WRCP-001 | Topic ledger and approved cleanup            | WRCP-000              | Active relation          | Closed 22-row ledger, consumer check, two removals, worktree observation, commit |
| WRCP-002 | Governance, agents, model, memory refresh    | WRCP-001              | Ledger frozen            | Dated sections for `006`, `026`, `028`, `032`, commit                            |
| WRCP-003 | Kubernetes, infrastructure, security refresh | WRCP-001              | Ledger frozen            | Dated section for `008`, `009`, `025`, commit                                    |
| WRCP-004 | Guide, Diátaxis, SDLC refresh                | WRCP-001              | Ledger frozen            | Dated sections for `014`, `020`, commit                                          |
| WRCP-005 | CI/CD, Actions, QA, V&V refresh              | WRCP-001              | Ledger frozen            | Dated section for `022`, `023`, `033`, commit                                    |
| WRCP-006 | Scope re-projection and reconciliation       | WRCP-002..005         | All research committed   | Scope index, README, ledger, collection README agree, commit                     |
| WRCP-007 | Validation closure and lifecycle done        | WRCP-006              | Content complete         | Full lane evidence, progress ledger, three `done` statuses, commit               |

### Task 1: WRCP-000 — activate the standalone execution

**Files:**

- Modify: `docs/03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md`
- Modify: `docs/04.execution/plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Create: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Modify: `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: approved `VAL-WRCP-001`–`011` from the owning Spec.
- Produces: an `active` standalone relation for spec `057`, and Task rows
  `WRCP-000`–`WRCP-007` that later packages mark complete.

- [ ] **Step 1: Create the Task from the current template.** Copy
      `docs/99.templates/templates/sdlc/execution/task.template.md` to
      `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`.
      Remove every author prompt. Set frontmatter `status: active`. Its H2 profile
      is fixed: `Overview`, `Inputs`, `Task Table`, `Approval and Safety
Boundaries`, `Verification Summary`, `Traceability`. Set `WRCP-000` to
      `In Progress` and `WRCP-001`–`WRCP-007` to `Queued`.

- [ ] **Step 2: Record the pre-activation validator result.** Run:

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  ```

  Expected: `PASS CROSS-DOCUMENT`. Record the exact line in the Task. Do not
  fabricate a failure; a valid draft state is a valid baseline.

- [ ] **Step 3: Add the reciprocal ADR relation.** In
      `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`,
      append this row to the relation table that already ends with the Spec 056
      row:

  ```markdown
  | Direct human approval recorded in the Spec body | N/A — fifth typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 057](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) |
  ```

  Also update the ADR prose that enumerates the covered Specs so it names
  Spec 057.

- [ ] **Step 4: Add the ADR link to the Spec.** In the Spec's
      `### Related Documents` list, add:

  ```markdown
  - [ADR-0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
  ```

  This satisfies the reciprocity the `STANDALONE-EXECUTION-ADR` check requires.

- [ ] **Step 4b: Convert the deferred Traceability links.** Every
      `Spec criterion` cell in this Plan's `### Lifecycle Traceability` table
      currently reads `N/A — approved Spec 057 criterion ...; reciprocal rendered
link is deferred to WRCP-000 activation`, and every `Expected Task` cell
      defers the same way. Replace both columns with rendered links now that
      both targets exist: the criterion cell links the Spec, and the
      `Expected Task` cell links the new Task. Then add to the Spec's
      `### Related Documents` a rendered link to this Plan and to the Task.

  Three checks bind here and must all hold afterwards. `BODY-LINK-SOURCE` and
  `BODY-LINK-TARGET` require a rendered link or an explicit exclusion in each
  cell. `BODY-LINK-RECIPROCAL` requires the linked Spec to link back to this
  Plan, which is why the Spec edit is part of the same step.
  `STANDALONE-EXECUTION-RECIPROCAL` requires Plan and Task to link each other
  and both to link the owning Spec. Run the two validators after this step and
  before Step 5; a partial conversion fails all three at once.

- [ ] **Step 5: Add the approval statements to the Spec.** Insert these two
      lines verbatim into the Spec's `## Overview`, as their own paragraph:

  ```markdown
  Direct human approval on 2026-08-14 authorizes this standalone execution relation.
  No separate PRD or ARD is required or part of this standalone lifecycle.
  ```

  The validator matches these by exact regex. Do not reword them.

- [ ] **Step 6: Register the standalone execution.** In
      `docs/99.templates/support/document-profiles.json`, append this object to the
      `standaloneExecutions` array, after the `"spec": "056"` object:

  ```json
  {
    "spec": "057",
    "plan": "docs/04.execution/plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md",
    "task": "docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md",
    "state": "active",
    "reason": "Direct human-approved combined constraint-consistency and Partial re-observation cycle over the existing 2026-08-08 WER pack without separate PRD/ARD authority",
    "decision": "0022",
    "approvalMode": "spec-body-record"
  }
  ```

- [ ] **Step 7: Set all three statuses to active.** Change frontmatter
      `status: draft` to `status: active` in the Spec and in this Plan. The Task is
      already `active` from Step 1. The registry `state` and all three `status`
      values must be identical or `STANDALONE-EXECUTION-STATE` fails.

- [ ] **Step 8: Register Plan and Task in their stage indexes.** Add one tree
      entry and one table row for each new file in
      `docs/04.execution/plans/README.md` and `docs/04.execution/tasks/README.md`.
      Match the existing row shape exactly, including the status column and the
      date column value `2026-08-14`.

- [ ] **Step 9: Stage everything, then validate.** Index checks read tracked
      paths only, so an unstaged new file reports as a non-target row:

  ```bash
  git add docs/03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md \
          docs/04.execution/plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md \
          docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md \
          docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md \
          docs/99.templates/support/document-profiles.json \
          docs/04.execution/plans/README.md docs/04.execution/tasks/README.md
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  git diff --check && git diff --cached --check
  ```

  Expected: `PASS` from all three validators, exit 0, no whitespace errors.

- [ ] **Step 10: Commit.**

  ```bash
  git commit -m "docs: activate workspace research consistency refresh"
  ```

### Task 2: WRCP-001 — topic ledger and approved cleanup

**Files:**

- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Delete: `graphify-out/2026-06-04/` (five tracked files)

**Interfaces:**

- Consumes: the active relation from Task 1.
- Produces: a frozen thirty-six-row topic ledger in the Task, and a terminal
  repository shape that Tasks 3–6 may safely cite.

- [ ] **Step 1: Write the closed topic ledger into the Task.** Add a
      `### Topic ledger` subsection under `## Inputs` with one row per requested
      topic. Columns: `Request line`, `Primary owner`, `Disposition`. Use exactly
      these owners, and no others:

  | Request line                                     | Primary owner   | Disposition        |
  | ------------------------------------------------ | --------------- | ------------------ |
  | Harness engineering                              | `REQ-WERPC-001` | reconfirm-verified |
  | Loop engineering                                 | `REQ-WERPC-002` | reconfirm-verified |
  | Workspace application system, environment, rules | `REQ-WERPC-003` | reconfirm-verified |
  | Claude implementation status                     | `REQ-WERPC-004` | reconfirm-verified |
  | Codex implementation status                      | `REQ-WERPC-005` | reconfirm-verified |
  | Claude/Codex common environment and rules        | `REQ-WERPC-006` | refresh-partial    |
  | Spec-driven development                          | `REQ-WERPC-007` | reconfirm-verified |
  | Kubernetes                                       | `REQ-WERPC-008` | refresh-partial    |
  | Infrastructure                                   | `REQ-WERPC-009` | refresh-partial    |
  | SDLC                                             | `REQ-WERPC-010` | reconfirm-verified |
  | PRD                                              | `REQ-WERPC-011` | reconfirm-verified |
  | ARD                                              | `REQ-WERPC-012` | reconfirm-verified |
  | ADR                                              | `REQ-WERPC-013` | reconfirm-verified |
  | Guide                                            | `REQ-WERPC-014` | refresh-partial    |
  | Incident                                         | `REQ-WERPC-015` | reconfirm-verified |
  | Postmortem                                       | `REQ-WERPC-016` | reconfirm-verified |
  | Policy                                           | `REQ-WERPC-017` | reconfirm-verified |
  | Release                                          | `REQ-WERPC-018` | reconfirm-verified |
  | Runbook                                          | `REQ-WERPC-019` | reconfirm-verified |
  | Documentation and Diátaxis                       | `REQ-WERPC-020` | refresh-partial    |
  | LLM-WIKI                                         | `REQ-WERPC-021` | reconfirm-verified |
  | CI/CD                                            | `REQ-WERPC-022` | refresh-partial    |
  | GitHub Actions                                   | `REQ-WERPC-023` | refresh-partial    |
  | QA                                               | `REQ-WERPC-024` | reconfirm-verified |
  | Security                                         | `REQ-WERPC-025` | refresh-partial    |
  | AI agent systems                                 | `REQ-WERPC-026` | refresh-partial    |
  | agency-agents                                    | `REQ-WERPC-027` | reconfirm-verified |
  | Task-fit model and configuration                 | `REQ-WERPC-028` | refresh-partial    |
  | Short-term memory                                | `REQ-WERPC-029` | reconfirm-verified |
  | Long-term memory                                 | `REQ-WERPC-030` | reconfirm-verified |
  | Domain-scoped memory                             | `REQ-WERPC-031` | reconfirm-verified |
  | Memory management                                | `REQ-WERPC-032` | refresh-partial    |
  | Verification and Validation                      | `REQ-WERPC-033` | refresh-partial    |
  | Spec document family                             | `REQ-WERPC-034` | admit-new-owner    |
  | Task document family                             | `REQ-WERPC-035` | admit-new-owner    |
  | Plan document family                             | `REQ-WERPC-036` | admit-new-owner    |

- [ ] **Step 2: Assert the ledger is closed.** Confirm exactly twelve
      `refresh-partial` rows with IDs `006`, `008`, `009`, `014`, `020`, `022`,
      `023`, `025`, `026`, `028`, `032`, `033`, and exactly three
      `admit-new-owner` rows with IDs `034`, `035`, `036`. Any other count means
      the request changed again — stop and report rather than widening the
      ledger silently.

- [ ] **Step 3: Run the consumer check before deleting anything.**

  ```bash
  rtk proxy grep -rn "graphify-out/2026-06-04" \
    --include="*.md" --include="*.json" --include="*.py" \
    --include="*.sh" --include="*.yaml" --include="*.yml" \
    docs/ scripts/ tests/ .github/ .claude/ .codex/ .agents/ .gemini/ \
    .pre-commit-config.yaml .gitignore
  ```

  Expected: zero matches. If any match appears, abandon the removal, record
  `consumer-found` and `reported-only`, and continue to Step 6.

- [ ] **Step 4: Remove the superseded snapshot.**

  ```bash
  git rm -r graphify-out/2026-06-04/
  ```

  Expected: five files staged for deletion.

- [ ] **Step 5: Remove the untracked local session files.**

  ```bash
  rm -f sessions/2026-08-11-session.md \
        sessions/2026-08-12-base-directory-for-this-skill-home-hy-cl.md \
        sessions/2026-08-12-session.md
  git status --porcelain sessions/
  ```

  Expected: empty output, because `sessions/` is ignored by `.gitignore:96`
  and produces no tracked diff.

- [ ] **Step 6: Record the cleanup rows and the worktree observation.** Add a
      `### Cleanup record` subsection to the Task with one row per target using
      columns `Target`, `Tracking state`, `Consumer check`, `Action`. Add a third
      row for `.worktrees/docs-sdlc-governance-consolidation` with
      `untracked-ignored`, `not-applicable`, `reported-only`, and this note: its
      branch is 32 commits ahead of and 58 behind `main`, so it holds unmerged
      work and is an explicit non-goal of this cycle.

- [ ] **Step 7: Validate and commit.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  bash scripts/validate-repo-quality-gates.sh .
  git add -A docs/04.execution/tasks/ graphify-out/
  git commit -m "chore: remove superseded graphify snapshot and freeze topic ledger"
  ```

  Expected: all three `PASS`, and the contract-registry path count is
  **unchanged**. `scripts/document_contracts.py` `_within_target_scope`
  returns `False` when the first path segment is `graphify-out`, so the
  deleted `GRAPH_REPORT.md` was never counted. A count that does drop means
  something other than this removal was staged — stop and inspect before
  committing.

### Task 3: WRCP-002 — governance, agents, model, memory refresh

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/workspace-governance-and-common-agent-environment.md`
- Modify: `docs/90.references/research/2026-08-08-wer/ai-agents-and-agency-agents.md`
- Modify: `docs/90.references/research/2026-08-08-wer/agent-model-routing-and-configuration.md`
- Modify: `docs/90.references/research/2026-08-08-wer/agent-memory-tiers-and-management.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`

**Interfaces:**

- Consumes: the frozen topic ledger from Task 2.
- Produces: dated `2026-08-14` sections for `REQ-WERPC-006`, `026`, `028`,
  `032`, and ledger rows starting at `SRC-WERPC-074` and `CLM-WERPC-010-01`.

- [ ] **Step 1: Read the registered sources for these four rows.** Open
      `source-coverage-and-migration-ledger.md` and list every `SRC-WERPC-*` row
      whose adopted scope covers common-system, AI-agent-system, model-routing, or
      memory evidence. Record the exact URLs and their `Checked on` dates. These
      are the only external sources this package re-checks.

- [ ] **Step 2: Re-observe the workspace.** For each requirement, re-read its
      canonical owner and record the delta against the prior dated observation:

  | Requirement     | Canonical owner to re-read                                                                                   |
  | --------------- | ------------------------------------------------------------------------------------------------------------ |
  | `REQ-WERPC-006` | `docs/00.agent-governance/harness-catalog.md`                                                                |
  | `REQ-WERPC-026` | `docs/00.agent-governance/harness-catalog.md` and `docs/00.agent-governance/contracts/harness-contract.json` |
  | `REQ-WERPC-028` | `docs/00.agent-governance/model-policy.md` and `docs/00.agent-governance/contracts/agent-model-fitness.json` |
  | `REQ-WERPC-032` | `docs/00.agent-governance/memory/README.md`                                                                  |

  Record `no-change` explicitly when nothing moved. Silence is not evidence.

- [ ] **Step 3: Re-check the external sources.** Fetch each URL from Step 1.
      Record one of `unchanged`, `changed`, or `unreachable` per source, with the
      observation date `2026-08-14`. An HTTP error is `unreachable`; preserve the
      prior `Checked on` date and do not alter the claim.

- [ ] **Step 4: Append the dated sections.** In each of the four report files,
      add a section titled `## 2026-08-14 consistency and Partial re-observation`.
      Each section states, per requirement: the workspace delta, the external
      result, the final disposition, and — when the disposition stays `Partial` or
      `DEFER` — the missing evidence, owning authority, safe boundary, and refresh
      trigger. Do not edit any existing section.

- [ ] **Step 5: Register sources and claims.** Append new `SRC-WERPC-*` rows
      starting at `074` and new `CLM-WERPC-010-*` rows starting at `01` to the
      ledger. Every source row carries a unique ID, primary URL, checked date,
      source status, adopted scope, rejected inference, and refresh trigger. Every
      claim row carries a unique ID, supporting source IDs, exact workspace paths,
      uncertainty, and evidence depth. Renumber nothing.

- [ ] **Step 6: Mark the Task row and validate.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  git diff --check
  ```

  Expected: `PASS` from both validators, exit 0.

- [ ] **Step 7: Commit.**

  ```bash
  git add docs/90.references/research/2026-08-08-wer/ docs/04.execution/tasks/
  git commit -m "docs: refresh agent governance and memory evidence"
  ```

### Task 4: WRCP-003 — Kubernetes, infrastructure, security refresh

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`

**Interfaces:**

- Consumes: the frozen topic ledger from Task 2, and the next free ledger IDs
  after Task 3.
- Produces: a dated `2026-08-14` section covering `REQ-WERPC-008`, `009`,
  `025`.

- [ ] **Step 1: Read the registered sources.** From the ledger, collect the
      URLs and `Checked on` dates for `SRC-WERPC-023`–`034` and
      `SRC-WERPC-060`–`065`, which are the registered Kubernetes, Argo CD, Helm,
      Gatekeeper, ESO, Vault, Sigstore, SLSA, and NIST sources for these rows.

- [ ] **Step 2: Re-observe the workspace.** Re-read `gitops/`, `policy/`,
      `infrastructure/`, and `traefik/` for the exact selectors the existing
      claims cite. Record each selector as `present-unchanged`, `present-changed`,
      or `absent`, with the exact path and line anchor.

- [ ] **Step 3: Re-check the external sources.** Fetch each URL from Step 1 and
      record `unchanged`, `changed`, or `unreachable`, dated `2026-08-14`.

- [ ] **Step 4: Hold the live boundary.** Do not run `kubectl`, `k3d`, `helm`,
      `argocd`, or `vault`. Effective RBAC, admission behavior, reconciliation
      state, real traffic, and Secret backend state stay `DEFER`. A manifest that
      states an intent is evidence of intent, never of effect.

- [ ] **Step 5: Append the dated section.** Add
      `## 2026-08-14 consistency and Partial re-observation` to
      `kubernetes-infrastructure-and-security.md`, covering all three requirements
      with the four required retention fields for each.

- [ ] **Step 6: Register sources and claims.** Continue the `SRC-WERPC-*` and
      `CLM-WERPC-010-*` sequences from wherever Task 3 stopped. Read the ledger
      first to find the current maximum; do not assume.

- [ ] **Step 7: Validate and commit.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  git add docs/90.references/research/2026-08-08-wer/ docs/04.execution/tasks/
  git commit -m "docs: refresh Kubernetes infrastructure and security evidence"
  ```

### Task 5: WRCP-004 — Guide, Diátaxis, SDLC, and document-family refresh

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/documentation-architecture-and-diataxis.md`
- Modify: `docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`

**Interfaces:**

- Consumes: the frozen topic ledger from Task 2, and the next free ledger IDs
  after Task 4.
- Produces: dated `2026-08-14` sections covering `REQ-WERPC-014` and `020`,
  plus the dated evidence that `REQ-WERPC-034`, `035`, and `036` will anchor
  to when Task 7 registers them in the coverage matrix.

- [ ] **Step 1: Read the prior Diátaxis source history.** The pack records that
      the published Diátaxis site returned HTTP 429 on three attempts and that the
      claims were instead verified against the upstream source repository
      registered as `SRC-WERPC-067`. Re-check `SRC-WERPC-067` first. Attempt the
      published site once; if it 429s again, record `unreachable` and move on.

- [ ] **Step 2: Re-observe the workspace.** Re-read
      `docs/99.templates/support/document-profiles.json` for the profile enum and
      `docs/05.operations/guides/` for the current Guide inventory. Record whether
      the `DOC-G1` enum enforcement gap is still open.

- [ ] **Step 3: Respect the settled decisions.** Approved `DOC-G2` and `DOC-G3`
      already decline tutorial and explanation profiles, resting on the framework's
      own instruction not to create empty structures. Do not reopen them, and do
      not propose those profiles. Record them as decided, not as gaps.

- [ ] **Step 4: Append the dated sections.** Add
      `## 2026-08-14 consistency and Partial re-observation` to both report files,
      with the four retention fields per requirement.

- [ ] **Step 4b: Re-observe the Spec, Task, and Plan document families.** These
      three families are described in the document-family contract matrix but had
      no coverage-matrix owner until this cycle. Re-read their canonical
      workspace evidence and their profile and template contracts:

  | Family | Canonical path             | Profile and template                                                               |
  | ------ | -------------------------- | ---------------------------------------------------------------------------------- |
  | Spec   | `docs/03.specs/`           | `sdlc/spec` profile; `docs/99.templates/templates/sdlc/specs/spec.template.md`     |
  | Task   | `docs/04.execution/tasks/` | `sdlc/task` profile; `docs/99.templates/templates/sdlc/execution/task.template.md` |
  | Plan   | `docs/04.execution/plans/` | `sdlc/plan` profile; `docs/99.templates/templates/sdlc/execution/plan.template.md` |

  For each, record the enforced H2 profile, the lifecycle states the repository
  actually uses, the reciprocity rules its validator enforces, and what the
  matrix row already claims. Append the result to the existing document-family
  section of `spec-driven-sdlc-and-document-contracts.md` under the same dated
  `2026-08-14` heading. Do not restate the matrix row; record only what this
  re-observation adds or corrects.

  Assign each family a status from the evidence you actually gathered. Per
  `C-WRCP-010` the admission itself neither raises nor lowers a status, so a
  family whose structural contract is enforced but whose effectiveness is
  unmeasured is `Verified` on the contract and `DEFER` on the effect — say both.

- [ ] **Step 5: Register sources and claims.** Continue both sequences from the
      current maximum found in the ledger.

- [ ] **Step 6: Validate and commit.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  git add docs/90.references/research/2026-08-08-wer/ docs/04.execution/tasks/
  git commit -m "docs: refresh Guide and documentation architecture evidence"
  ```

### Task 6: WRCP-005 — CI/CD, Actions, QA, V&V refresh

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/ci-cd-github-actions-and-qa.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`

**Interfaces:**

- Consumes: the frozen topic ledger from Task 2, and the next free ledger IDs
  after Task 5.
- Produces: a dated `2026-08-14` section covering `REQ-WERPC-022`, `023`,
  `033`.

- [ ] **Step 1: Re-observe the workspace.** Re-read `.github/workflows/`,
      `.pre-commit-config.yaml`,
      `docs/00.agent-governance/contracts/validation-surfaces.json`, and
      `docs/00.agent-governance/rules/quality-standards.md`. Record the workflow
      inventory, declared permissions, action pinning, and concurrency settings as
      static declarations.

- [ ] **Step 2: Re-check the external sources.** Re-check the registered
      GitHub Actions, SLSA, pre-commit, pip, and NASA verification and validation
      sources. Record `unchanged`, `changed`, or `unreachable`, dated
      `2026-08-14`.

- [ ] **Step 3: Do not query the GitHub remote.** The prior cycle used an
      explicitly approved read-only metadata batch. This cycle has no such
      approval, so hosted metadata is out of scope. Carry the prior dated
      observations forward by reference and do not re-fetch them.

- [ ] **Step 4: Keep the verification and validation distinction exact.** A
      green static lane is verification of conformance. It is never validation of
      intended use. Any sentence that blurs the two is a defect in this package.

- [ ] **Step 5: Append the dated section.** Add
      `## 2026-08-14 consistency and Partial re-observation` to
      `ci-cd-github-actions-and-qa.md` covering all three requirements with the
      four retention fields each.

- [ ] **Step 6: Register sources and claims.** Continue both sequences from the
      current maximum found in the ledger.

- [ ] **Step 7: Validate and commit.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  git add docs/90.references/research/2026-08-08-wer/ docs/04.execution/tasks/
  git commit -m "docs: refresh CI CD Actions and QA evidence"
  ```

### Task 7: WRCP-006 — scope re-projection and reconciliation

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/scope-application-index.md`
- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/90.references/research/README.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`

**Interfaces:**

- Consumes: every dated section and ledger row produced by Tasks 3–6.
- Produces: agreeing counts and owner projections across the scope index, the
  pack README, and the collection README, and the three admitted owner rows
  `REQ-WERPC-034`, `035`, and `036`.

- [ ] **Step 1: Re-derive the ten scope rows.** For each file under
      `docs/00.agent-governance/scopes/`, re-read its `Authority Boundary`
      file-ownership table and re-match it against each requirement's canonical
      owner. Update the scope-to-requirement map only where the registry actually
      changed, and say why.

- [ ] **Step 2: Re-test the five unowned canonical paths.** Search all ten
      scope documents for ownership of `.github/**`, `.agents/agents/**`,
      `traefik/`, `.pre-commit-config.yaml`, and root `policy/`:

  ```bash
  rtk proxy grep -rn "github\|\.agents\|traefik\|pre-commit\|policy/" \
    docs/00.agent-governance/scopes/
  ```

  Record each as still unowned or newly owned with the owning scope named.
  Adopting a path is a `meta` decision and is not performed here.

- [ ] **Step 3: Update the observation dates.** The scope index currently
      carries a 2026-08-10 scope observation date. Change it to `2026-08-14` and
      update the `updated:` frontmatter field.

- [ ] **Step 3b: Register the three admitted owners in the coverage matrix.**
      Add exactly three rows to the pack README's Requirement Coverage Matrix,
      immediately after `REQ-WERPC-033`, using the same column set as every
      existing row:

  | Request ID      | Requested topic | Primary owner                           | Workspace evidence         | External source class                                        | Status              |
  | --------------- | --------------- | --------------------------------------- | -------------------------- | ------------------------------------------------------------ | ------------------- |
  | `REQ-WERPC-034` | Spec            | the document-family matrix row for Spec | `docs/03.specs/`           | as recorded for that row, plus the 2026-08-14 re-observation | from Task 5 Step 4b |
  | `REQ-WERPC-035` | Task            | the document-family matrix row for Task | `docs/04.execution/tasks/` | as recorded for that row, plus the 2026-08-14 re-observation | from Task 5 Step 4b |
  | `REQ-WERPC-036` | Plan            | the document-family matrix row for Plan | `docs/04.execution/plans/` | as recorded for that row, plus the 2026-08-14 re-observation | from Task 5 Step 4b |

  Link each primary owner to the anchor of the document-family matrix section,
  the way rows `REQ-WERPC-011` through `REQ-WERPC-019` already do. Then state in
  the reconciliation subsection why these three were absent: the matrix
  described twelve families while the coverage matrix registered nine, and no
  prior request named Spec, Task, or Plan explicitly. Add no fourth owner —
  `C-WRCP-010` caps this at three.

- [ ] **Step 4: Update the pack README reconciliation.** Add a
      `### 2026-08-14 consistency and Partial re-observation reconciliation`
      subsection stating the admitted candidate count, the final disposition of
      each, the new source and claim ID ranges, and the resulting totals for
      physical files, request owners, source IDs, and claim IDs. Update every
      Status cell that actually changed, and state plainly when none did.

- [ ] **Step 5: Update the collection README.** In
      `docs/90.references/research/README.md`, confirm the `Item Index` tree and
      the `Research Pack Index` table still match the pack's real contents. The
      pack file count does not change in this cycle, so a correction here means an
      error existed before; fix it and say so.

- [ ] **Step 6: Assert cross-document agreement.** Confirm no status in the
      scope index differs from the pack README. The README is authoritative; the
      index yields to it.

- [ ] **Step 7: Validate and commit.**

  ```bash
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-reference-information-architecture.py --self-test
  git add docs/90.references/ docs/04.execution/tasks/
  git commit -m "docs: reproject scope index and reconcile cross-links"
  ```

### Task 8: WRCP-007 — validation closure and lifecycle done

**Files:**

- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `docs/03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md`
- Modify: `docs/04.execution/plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Modify: `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/03.specs/README.md`, `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: all committed content from Tasks 1–7.
- Produces: recorded validation evidence, a durable progress entry, and a
  `done` standalone relation.

- [ ] **Step 1: Run the full validation lane.**

  ```bash
  python3 scripts/validate-links-and-owners.py --self-test
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-document-contract-registry.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  python3 scripts/validate-reference-information-architecture.py --self-test
  python3 scripts/validate-affected-surfaces.py --root .
  bash scripts/validate-repo-quality-gates.sh .
  git diff --check && git diff --cached --check
  ```

  Record each exact result line in the Task's `## Verification Summary`.

- [ ] **Step 2: Compare against the recorded baseline.** The 2026-08-14
      pre-cycle baseline was `PASS` for the cross-document validator and the
      repository quality gates on a clean tree. The acceptance signal is absence
      of regression. A newly green lane that was already green proves nothing new;
      say so rather than claiming an improvement.

- [ ] **Step 3: Confirm no temporary file survives.**

  ```bash
  git status --porcelain --untracked-files=all | rtk proxy grep -v '^$' || echo CLEAN
  ```

  Expected: `CLEAN`, or only intended files. Nothing under the scratchpad path
  may be tracked.

- [ ] **Step 4: Append the durable progress entry.** In
      `docs/00.agent-governance/memory/progress.md`, record the branch, the
      baseline SHA, the eight work packages, the two removals, the twelve final
      dispositions, the new source and claim ID ranges, the validation results, and
      the explicit boundary that cluster, hosted, provider-runtime, and stakeholder
      evidence stayed `DEFER`.

- [ ] **Step 5: Close the lifecycle.** Set `status: done` in the Spec, this
      Plan, and the Task. Set `"state": "done"` in the spec `057` object in
      `standaloneExecutions`. All four values must match or
      `STANDALONE-EXECUTION-STATE` fails.

- [ ] **Step 6: Update the three stage indexes.** Change the status column for
      the Spec, Plan, and Task rows from `Active` to `Done` in
      `docs/03.specs/README.md`, `docs/04.execution/plans/README.md`, and
      `docs/04.execution/tasks/README.md`.

- [ ] **Step 7: Re-validate after the lifecycle flip.**

  ```bash
  git add -A docs/
  python3 scripts/validate-links-and-owners.py --root . --mode strict
  python3 scripts/validate-markdown-profiles.py --root . --mode strict
  bash scripts/validate-repo-quality-gates.sh .
  ```

  Expected: `PASS` from all three.

- [ ] **Step 8: Commit.**

  ```bash
  git commit -m "docs: close workspace research consistency refresh"
  ```

## Verification Plan

Each work package runs the focused lane before its commit; the final package
runs the full lane.

| Lane              | Command                                                                         | Applies to         |
| ----------------- | ------------------------------------------------------------------------------- | ------------------ |
| Cross-document    | `python3 scripts/validate-links-and-owners.py --root . --mode strict`           | Every package      |
| Markdown profile  | `python3 scripts/validate-markdown-profiles.py --root . --mode strict`          | Every package      |
| Contract registry | `python3 scripts/validate-document-contract-registry.py --root . --mode strict` | WRCP-000, 001, 007 |
| Reference IA      | `python3 scripts/validate-reference-information-architecture.py --self-test`    | WRCP-006, 007      |
| Affected surfaces | `python3 scripts/validate-affected-surfaces.py --root .`                        | WRCP-007           |
| Repository gates  | `bash scripts/validate-repo-quality-gates.sh .`                                 | WRCP-001, 007      |
| Whitespace        | `git diff --check && git diff --cached --check`                                 | Every package      |

Index checks resolve against tracked paths, so new files are staged before
validation. External fetch results are recorded as observations with dates and
never promoted into runtime or live claims.

## Risks & Mitigations

| Risk                                      | Impact                                       | Mitigation                                                                                         |
| ----------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| A deletion target has a live consumer     | Broken reference or validator regression     | `WRCP-001` Step 3 consumer check gates the removal; failure converts it to report-only             |
| Parallel research collides on ledger IDs  | Duplicate or skipped `SRC`/`CLM` IDs         | Subagents are read-only; the primary agent writes and reads the current maximum before each append |
| An external source is unreachable         | A claim looks stale or gets silently dropped | Record `unreachable`, preserve the prior date, change no status                                    |
| Static `PASS` misread as runtime proof    | False promotion of a `DEFER` boundary        | Every package restates the evidence boundary; `WRCP-005` Step 4 makes the V&V distinction explicit |
| Lifecycle status drifts across four files | `STANDALONE-EXECUTION-STATE` failure         | `WRCP-000` Step 7 and `WRCP-007` Step 5 flip all four values in one edit each                      |
| Plan or Task links a foreign Spec         | `STANDALONE-EXECUTION-SPEC-BOUNDARY` failure | Prior specs are referenced as code literals such as `056`, never as rendered links                 |
| Formatter reflows a wide table            | Large diff obscures the real change          | Review with `git diff --ignore-all-space` and confirm the row count delta                          |
| Cycle promotes nothing                    | Reads as wasted effort                       | The Spec defines a no-promotion outcome as success when the delta and boundaries are recorded      |

## Completion Criteria

- All eight work packages are committed as separate non-empty logical commits.
- The topic ledger holds exactly thirty-six rows, twelve `refresh-partial`
  dispositions, and exactly three `admit-new-owner` dispositions.
- Exactly two cleanup targets were removed, each behind a passing consumer
  check, and `.worktrees/docs-sdlc-governance-consolidation` is unchanged.
- Every one of the twelve requirements carries a dated `2026-08-14` section
  with a separated workspace observation and external source result, a final
  disposition, and the four retention fields when it stays `Partial` or
  `DEFER`.
- New `SRC-WERPC-*` and `CLM-WERPC-010-*` rows are unique and no existing ID was
  renumbered or rewritten.
- The scope index, pack README, and collection README agree on all counts and
  statuses.
- The full validation lane shows no regression against the 2026-08-14
  baseline.
- The Spec, this Plan, the Task, and the registry entry all read `done`.

## Traceability

### Lifecycle Traceability

| Spec criterion                                                                                | Work package  | Expected Task                                                                                                                                                     |
| --------------------------------------------------------------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [VAL-WRCP-001](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-001      | [WRCP-001](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record the thirty-six-row topic ledger with unique owners              |
| [VAL-WRCP-002](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-002..005 | [WRCP-002..005](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record separated workspace and external results per requirement   |
| [VAL-WRCP-003](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-002..005 | [WRCP-002..005](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record four retention fields per retained Partial or DEFER        |
| [VAL-WRCP-004](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-002..005 | [WRCP-002..005](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record ledger before/after comparison and ID uniqueness           |
| [VAL-WRCP-005](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-001      | [WRCP-001](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record consumer check result and the unchanged worktree                |
| [VAL-WRCP-006](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-002..005 | [WRCP-002..005](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record unchanged pack file inventory with dated sections only     |
| [VAL-WRCP-007](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-006      | [WRCP-006](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record scope re-derivation and the unowned-path re-test                |
| [VAL-WRCP-008](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-006      | [WRCP-006](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record cross-document agreement on counts and statuses                 |
| [VAL-WRCP-009](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-006      | [WRCP-006](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record reconciliation as the last content commit                       |
| [VAL-WRCP-010](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-007      | [WRCP-007](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record full lane results compared against the baseline                 |
| [VAL-WRCP-011](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md) | WRCP-000..007 | [WRCP-000..007](../tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md) will record one commit per package and terminal temporary-file absence |

### Related documents

Targets that do not yet exist, and prior Specs outside this standalone
relation, are recorded as code literals rather than rendered links.

- Owning Spec:
  `docs/03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md`
- Future reciprocal Task after activation:
  `docs/04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md`
- Decision source:
  `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Immediate predecessor cycle: spec `056`
- [Research pack README](../../90.references/research/2026-08-08-wer/README.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
