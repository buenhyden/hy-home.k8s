---
title: 'Workspace Engineering Gap-only Research Refresh Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-09
---

# Workspace Engineering Gap-only Research Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The primary controller uses
> executing-plan checkpoints while a fresh worker owns each implementation
> task and separate workers perform specification/content and quality review.

**Goal:** Add only previously unresearched or externally under-sourced
`Partial` evidence to the existing `2026-08-08-wer` pack, with explicit
Verification/Validation treatment, exact workspace reconciliation, logical
commits, and no deeper-evidence overclaim.

**Architecture:** Execution begins with a deterministic admission gate over the
complete requested scope. Only admitted questions reach official-source
research; accepted claims are integrated into five existing research owners,
reviewed independently, and closed through the repository's exact affected,
staged, aggregate, all-files, and diff lanes. Spec 053 remains terminal; Spec
055 receives its own ADR-0022 standalone relation only when execution is
activated.

**Tech Stack:** Markdown using registry-selected Spec, Plan, Task, snapshot-pack,
and reference profiles; official web sources; current Git-tracked repository
evidence; Python 3 standard-library read-only probes; existing document,
Reference Information Architecture, affected-surface, pre-commit, and
repository-quality validators.

**Global constraints:**

- Research output remains inside
  `docs/90.references/research/2026-08-08-wer/`; no new research directory or
  addendum is created.
- The only research-pack files eligible for modification are `README.md`,
  `spec-driven-sdlc-and-document-contracts.md`,
  `ci-cd-github-actions-and-qa.md`,
  `kubernetes-infrastructure-and-security.md`, and
  `source-coverage-and-migration-ledger.md`.
- Every requested category receives exactly one admission result:
  `complete-existing`, `admit-unresearched`,
  `admit-under-sourced-partial`, or `exclude-deep-evidence`.
- Only `admit-unresearched` and `admit-under-sourced-partial` authorize new
  external-source or claim rows.
- All accepted new source and claim evidence uses check date `2026-08-09`;
  original rows and their dates remain unchanged.
- Official standards, government, product, or upstream project owners are the
  default source class. Search-result pages are never cited as authority.
- Repository-static evidence never proves provider discovery, authentication,
  effective permissions, hosted CI, remote state, credentials, secret values,
  CNI enforcement, cluster reconciliation, or live behavior.
- No runtime/provider, GitHub, GitOps, Kubernetes, infrastructure, RBAC,
  NetworkPolicy, workload, image, chart, release, document-profile, policy, or
  validator behavior changes merely because research identifies a gap.
- Existing `docs/98.archive/**`, the Current audit RIA contract, terminal Spec
  053 evidence, and deleted predecessor-pack history remain unchanged.
- Fetched pages, extracts, query outputs, and scratch matrices are not tracked.
  One-off local artifacts are removed before closure.
- Each work package receives implementation, specification/content review,
  quality review, focused validation, and one logical Conventional Commit.
- External browsing starts only after WERG-000 activates the approved
  reciprocal execution relation.
- Hosted, provider-runtime, remote, credential-bearing, and live lanes remain
  `DEFER` throughout this Plan.

---

## Overview

This Plan executes approved
[Spec 055](../../03.specs/055-workspace-engineering-gap-only-refresh/spec.md)
without reopening completed
`docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md`.
The research pack already maps 32 requested topics to twelve reference owners
and contains dated source and claim registers. Most requested categories have
adequate official-source coverage. The work therefore treats the broad request
as an admission corpus, not as permission to rewrite every topic.

The planned output is an in-place evidence refresh. The directory keeps its
`2026-08-08-wer` identity while every additive section and ledger row records a
separate `2026-08-09 gap-only source refresh` boundary. Lifecycle documents,
indexes, the standalone registry relation, and durable progress evidence are
execution metadata and do not become research-topic owners.

The written Spec was approved by the human on 2026-08-09. This Plan and its
reciprocal Task remain `draft` until the human chooses an execution mode. WERG-000
then activates Spec, Plan, Task, their indexes, and the exact ADR-0022
standalone relation atomically.

## Context

### Current research state

- The pack contains one README plus twelve existing references.
- The README has 32 sequential `REQ-WERPC-*` rows.
- PRD, ARD, Policy, and Runbook currently rely primarily on local
  profile/template/validator evidence.
- Release currently uses SemVer plus a verified local profile/template absence
  result; the report distinguishes a broader release record from release notes
  but lacks a complete external approval/evidence basis.
- The QA reference covers lane/result semantics but does not own an explicit
  external Verification/Validation definition and responsibility matrix.
- The Kubernetes reference already covers RBAC, NetworkPolicy, Pod Security,
  mutable identity, and evidence-depth boundaries generally. Only exact
  subquestions that fail line-level admission may receive additions.

### Canonical workspace comparison owners

- PRD and ARD profile, lifecycle, and template facts:
  `docs/99.templates/support/document-profiles.json` and
  `docs/99.templates/templates/sdlc/**`.
- Current document decisions, including Guide taxonomy and the narrow
  no-release-notes decision:
  `docs/03.specs/052-document-taxonomy-consolidation/spec.md`.
- Validation lane and result meanings:
  `docs/00.agent-governance/rules/quality-standards.md` and
  `docs/00.agent-governance/contracts/validation-surfaces.json`.
- Kubernetes desired-state evidence:
  `gitops/platform/monitoring/kube-state-metrics.yaml`,
  `gitops/platform/network-policies/`, `gitops/platform/namespaces/`,
  `gitops/workloads/adminer/rollout.yaml`, `.kube-linter.yaml`, and Argo CD
  Application manifests under `gitops/apps/root/`.
- Execution evidence owner:
  [Task](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md).

### Candidate primary-source families

Workers must verify the exact current official pages before accepting any
claim. The candidate owners are:

- ISO/IEC/IEEE requirements-engineering and architecture-description
  standards for PRD/ARD semantics;
- NIST CSF, SP 800-53, SSDF, and other directly relevant official guidance for
  policy, assurance, release evidence, and control verification;
- Google SRE official books/workbook for repeatable operational procedure,
  recovery, and evidence expectations;
- NASA Systems Engineering Handbook or an equivalent official systems source
  for Verification/Validation terminology;
- SemVer, SLSA, and GitHub artifact-attestation documentation for the bounded
  version/provenance distinction;
- Kubernetes official RBAC good practices, NetworkPolicy, Pod Security
  Standards/Admission, image documentation, and the kube-state-metrics
  upstream project for the exact platform questions;
- Helm official provenance and Argo CD official revision-tracking guidance for
  chart and Git identity questions.

Candidate status is not evidence. Each accepted row must link the exact page
that directly supports the claim.

## Goals & In-Scope

- Activate a new Spec 055 standalone execution relation only after Plan
  approval and without changing `programLineage`.
- Produce a complete, reviewable admission result for every original requested
  category plus the newly explicit Verification/Validation request.
- Strengthen admitted PRD, ARD, Policy, Runbook, and Release semantics with
  official external evidence while preserving local facts and accepted
  decisions.
- Add explicit, externally sourced Verification/Validation definitions and a
  workspace responsibility/evidence/failure matrix.
- Add only Kubernetes and infrastructure security subquestions that a
  deterministic comparison proves are absent or externally under-sourced.
- Append source and claim rows with exact provenance, uncertainty, owner, and
  refresh boundaries.
- Reconcile README ownership, status, links, and checked-date wording without
  altering unaffected rows.
- Remove one-off artifacts, pass independent reviews and all repository-static
  gates, and close the standalone lifecycle honestly.

## Non-Goals & Out-of-Scope

- Full re-research or prose refresh of already adequate harness, loop,
  workspace, Claude, Codex, common-environment, SDD, SDLC, Diataxis, LLM-WIKI,
  CI/CD, GitHub Actions, QA, security, AI-agent, Agency Agents, model-routing,
  or memory coverage.
- A new research pack, addendum, replacement report, redirect, compatibility
  document, or copied source register.
- A new Release document family, profile, route, template, status domain,
  lifecycle, or validator.
- Remediation of Kubernetes RBAC, NetworkPolicy, Pod Security, workload
  security context, image tags, chart identity, Git revisions, or admission
  controls.
- Authentication, provider runtime, hosted workflows, branch protection,
  artifact inspection, secret access, cluster access, deployment, remote
  publication, push, merge, or live validation.
- Modification of existing audit packs, RIA currentness, Stage 98, terminal
  historical evidence, or Spec 052 execution state.
- A validator or lifecycle-contract expansion without a reproduced exact
  closure diagnostic and separate human approval.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WERG-000 | Activate the approved standalone execution path | Plan review | Human execution-mode choice | Reciprocal active Spec/Plan/Task/index/registry state; strict lifecycle gates; review; commit |
| WERG-001 | Classify the complete requested scope through the gap-admission gate | WERG-000 | Active exact observation tree | Complete admission matrix, no duplicate research authorization, review, commit |
| WERG-002 | Research document-family and Verification/Validation gaps | WERG-001 | Admitted question set | Official source/claim rows, updated document and QA owners, review, commit |
| WERG-003 | Research exact Kubernetes security deltas | WERG-001 | At least one admitted Kubernetes subquestion | Additive K8s source/claim rows or reviewed no-op, security/content review, optional commit only when non-empty |
| WERG-004 | Reconcile pack index, ledger, cross-links, and one-off cleanup | WERG-002, WERG-003 | Topic reviews approved | Exact owner/source/claim/link closure, clean residue audit, review, commit |
| WERG-005 | Run terminal validation, whole-branch review, lifecycle closure, and branch finish | WERG-004 | All content commits clean | Final gates, independent reviews, terminal or explicitly blocked lifecycle evidence, closure commit, finish choice |

### Task 1: WERG-000 — activate the approved standalone execution path

**Files:**

- Modify: `docs/03.specs/055-workspace-engineering-gap-only-refresh/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: approved Spec 055, ADR-0022, exact Plan/Task paths, and the current
  sorted `standaloneExecutions` array.
- Produces: one unique active standalone relation for Spec `055`, with exact
  Plan and Task identities and `approvalMode: spec-body-record`.

- [ ] **Step 1: Record the exact draft baseline and human approval**

Run:

```bash
git status --short --branch
git log -1 --oneline
rg -n "status: draft|pending written Spec approval|055-workspace-engineering-gap-only-refresh" \
  docs/03.specs/055-workspace-engineering-gap-only-refresh/spec.md \
  docs/04.execution/plans/2026-08-09-workspace-engineering-gap-only-refresh.md \
  docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md \
  docs/03.specs/README.md \
  docs/04.execution/plans/README.md \
  docs/04.execution/tasks/README.md
```

Expected: clean planning baseline; Spec, Plan, and Task are draft; no Spec 055
standalone registry row exists.

- [ ] **Step 2: Apply the atomic active relation**

Use `apply_patch` to:

1. set Spec, Plan, and Task frontmatter to `status: active`;
1. replace pending Plan/Task text in Spec 055 with reciprocal rendered links;
1. mark all three README index rows `Active`;
1. insert the exact sorted registry object:

```json
{
  "spec": "055",
  "plan": "docs/04.execution/plans/2026-08-09-workspace-engineering-gap-only-refresh.md",
  "task": "docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md",
  "state": "active",
  "reason": "Direct human-approved gap-only external-source refresh of the existing 2026-08-08 WER pack without separate PRD/ARD authority",
  "decision": "0022",
  "approvalMode": "spec-body-record"
}
```

1. mark WERG-000 `In Review` with the exact changed-path and approval evidence.

- [ ] **Step 3: Run focused activation validation**

Run:

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
git diff --check
```

Expected: registry self-test and strict validation pass; Markdown violations
are zero; links/owners pass; no unowned active execution component exists.

- [ ] **Step 4: Obtain specification and quality review**

Dispatch one specification reviewer and one quality reviewer against only the
WERG-000 diff. Correct every Critical or Important finding before commit.

- [ ] **Step 5: Stage, run the canonical commit gates, and commit**

Run the affected and staged lanes for the exact changed paths, then plain
pre-commit, the direct aggregate, all-files pre-commit, formatter review, and
both diff checks. Commit only after the final exact index is clean:

```bash
git commit -m "docs: activate WER gap-only research refresh"
```

### Task 2: WERG-001 — classify the complete requested scope

**Files:**

- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the user's complete category list, the 32 existing request rows,
  every existing `SRC-WERPC-*` and `CLM-WERPC-*` row, and all thirteen files
  in the current pack. The five candidate owners bound possible writes; they
  do not narrow the read-only comparison corpus.
- Produces: one admission record per requested category and an exact admitted
  question set used by WERG-002 and WERG-003.

- [ ] **Step 1: Write and run the admission RED probe**

Create the task-local checker at the exact temporary path and run its bounded
self-test plus baseline mode:

```bash
python3 /tmp/werg-gap-refresh-check.py --self-test
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --pack docs/90.references/research/2026-08-08-wer --expected-pack-files 13 --expected-request-rows 32 --extra-topic verification-validation --expect baseline-gap
```

The checker parses the README request matrix, all thirteen pack files, and all
source/claim tables. It prints only identifiers, missing field names, and
paths—never page bodies or secret data.

Expected RED: Verification/Validation has no independent research owner and
the four local-only document-family rows plus Release's SemVer-only external
basis fail the source-class assertion.

- [ ] **Step 2: Build the complete admission matrix**

For each requested topic, record in the Task:

```text
requested topic | existing REQ owner | existing report#heading |
existing source IDs | existing claim IDs | admission state | exact reason
```

The reason must identify either the material missing question, the adequate
existing source/claim boundary, or the deeper evidence that makes the topic
`exclude-deep-evidence`.

- [ ] **Step 3: Verify admission completeness and uniqueness**

Run the reviewed-matrix mode:

```bash
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --pack docs/90.references/research/2026-08-08-wer --expected-pack-files 13 --expected-request-rows 32 --extra-topic verification-validation --require-complete
```

The command requires:

- one row per requested topic;
- only the four closed admission states;
- no duplicate requested topic or owner;
- no `complete-existing` or `exclude-deep-evidence` row in the admitted set;
- exact owner/heading existence for every existing reference; and
- no new web-source row before the admitted set is reviewed.

- [ ] **Step 4: Obtain independent admission review**

The reviewer must compare every final row—`complete-existing`, both admitted
states, and `exclude-deep-evidence`—with all thirteen current pack files, not
only its README status or the five writable owners. A topic is removed from
the admitted set when the existing report already has a direct official
source, exact local mapping, uncertainty boundary, and refresh trigger for the
same question. A false `complete-existing` or `exclude-deep-evidence` result is
an Important finding and blocks browsing.

- [ ] **Step 5: Record the reviewed result and commit**

Append a bounded `2026-08-09 Gap-only admission` subsection to the existing
ledger, update WERG-001 evidence and progress, run focused profile/link/diff
checks plus the canonical commit gates, and commit:

```bash
git commit -m "docs: classify WER gap-only research scope"
```

### Task 3: WERG-002 — research document families and Verification/Validation

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md`
- Modify: `docs/90.references/research/2026-08-08-wer/ci-cd-github-actions-and-qa.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the reviewed WERG-001 admitted rows, official primary pages, local
  document profiles/templates, Spec 052 decisions, and the quality-lane owner.
- Produces: additive dated source rows, bounded claim rows, document-family
  semantics, an explicit Verification/Validation matrix, and reconciled README
  ownership/status cells.

- [ ] **Step 1: Reproduce the focused external-basis RED**

Run the evidence checker against the activation commit before browsing:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/2026-08-08-wer --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --phase baseline --check-date 2026-08-09
```

The command emits exact missing field and owner identifiers while showing:

- PRD, ARD, Policy, and Runbook README rows use local-only source wording;
- Release uses SemVer plus local absence evidence but no broader approval and
  evidence source; and
- the QA owner has no externally sourced definition table whose columns are
  `Term`, `Question`, `Actor`, `Input`, `Evidence`, `Failure meaning`, and
  `Workspace mapping`.

Expected: all admitted rows fail at least one asserted external-basis field.

- [ ] **Step 2: Research official primary sources**

Assign one documentation-research worker to requirements/architecture and one
to policy/runbook/release/V&V. Each worker must:

1. open and read the complete relevant official page;
2. capture the exact URL and title;
3. record check date `2026-08-09`;
4. state the adopted scope and rejected inference;
5. state the refresh trigger;
6. map the claim to exact workspace paths/selectors; and
7. mark paywalled abstract-only or unavailable normative text as a limitation.

The research must distinguish:

- product requirements from technical architecture requirements;
- normative policy from executable procedure;
- runbook execution/recovery evidence from incident facts;
- version semantics from release approval, provenance, rollout, and rollback
  records;
- Verification of implementation/design conformance from Validation of
  requirement satisfaction or intended use; and
- external definitions from the repository's canonical lane vocabulary.

- [ ] **Step 3: Allocate source and claim IDs without renumbering**

Mechanically read the maximum existing numeric suffix for `SRC-WERPC-*` and
`CLM-WERPC-*`. Allocate contiguous new IDs only for accepted claims. Assert
that every old row is byte-identical before the insertion point and retains
its original checked date.

- [ ] **Step 4: Integrate the two owner reports**

Use `apply_patch` to:

- add a `2026-08-09 gap-only source refresh` subsection to the SDLC reference;
- update only admitted document-family rows or add linked analysis below the
  matrix;
- preserve Spec 052 DOC-G1 and DOC-G5 as accepted local decisions;
- add the seven-column Verification/Validation matrix to the QA reference;
- map the terms to validation, verification, tests, review, release, and
  operations without redefining `quality-standards.md`; and
- update README source/status cells and add a new request row only if WERG-001
  proved no current request owner.

- [ ] **Step 5: Run focused GREEN probes**

Run:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/2026-08-08-wer --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --phase final --check-date 2026-08-09 --allowed-owner README.md --allowed-owner spec-driven-sdlc-and-document-contracts.md --allowed-owner ci-cd-github-actions-and-qa.md --allowed-owner kubernetes-infrastructure-and-security.md --allowed-owner source-coverage-and-migration-ledger.md
```

Record the resolved full commit in the Task. The command requires:

- every admitted document-family row to reference at least one new official
  source ID;
- every new source row to have URL/date/adopted/rejected/refresh fields;
- every new claim row to have source, workspace evidence, uncertainty, status,
  and owner;
- the Verification/Validation matrix to contain both terms exactly once and
  all seven columns; and
- unchanged request/source/claim IDs and original check dates.

- [ ] **Step 6: Obtain content and quality review**

The content reviewer checks source fidelity, terminology, Spec 052 decision
preservation, and absence of policy invention. The quality reviewer checks
table contracts, identifiers, links, profiles, concision, and no duplicated
topic owner. Correct every Critical or Important finding.

- [ ] **Step 7: Validate and commit**

Run focused source/claim/selector probes, strict registry/profile/links, RIA,
affected/staged lanes, plain and all-files pre-commit, aggregate, formatter
review, and diff checks. Commit:

```bash
git commit -m "docs: research WER document and validation gaps"
```

### Task 4: WERG-003 — research exact Kubernetes security deltas

**Files:**

- Modify when non-empty: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify when non-empty: `docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md`
- Modify when non-empty: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the reviewed WERG-001 Kubernetes subquestion admissions, current
  Kubernetes report, exact manifests/configuration, and official upstream
  sources.
- Produces: only non-duplicative K8s source/claim rows and analysis, or a
  reviewed no-op result with no empty topic commit.

- [ ] **Step 1: Run the line-level duplication and gap RED probe**

For each candidate subquestion, compare the exact current report paragraphs,
source rows, claim rows, and workspace selectors. Admit a subquestion only
when at least one of these is missing:

- a direct official source for the precise claim;
- an exact current workspace selector;
- an uncertainty/deeper-evidence boundary; or
- a refresh trigger.

Expected: already complete general NetworkPolicy, Pod Security, and image-tag
explanations are rejected; only exact subquestions that remain absent proceed.

- [ ] **Step 2: Research the admitted official sources**

Assign a Kubernetes documentation researcher and require complete official
page reading for the admitted subset. Candidate questions are:

- whether kube-state-metrics requires cluster-wide Secret metadata
  `list/watch`, which metric surface depends on it, and what the upstream
  least-privilege boundary actually supports;
- namespace ingress/default-deny semantics and the dependency on a supporting
  network plugin;
- Pod Security Standards/Admission plus pod/container hardening and service
  account token boundaries for the exact Adminer workload comparison; and
- immutable Git revision, image digest, Helm provenance, and signed/provenance
  evidence distinctions.

Reject any inference about live enforcement, actual collected metrics,
artifact validity, signer identity, or cluster behavior.

- [ ] **Step 3: Reconcile exact workspace evidence**

Use read-only inspection of:

```text
gitops/platform/monitoring/kube-state-metrics.yaml
gitops/platform/network-policies/
gitops/platform/namespaces/
gitops/workloads/adminer/rollout.yaml
.kube-linter.yaml
gitops/apps/root/
```

Record only object kind/name, rule/resource/verb, policy type, security-context
field presence, revision value, and image/chart identity. Do not inspect
secrets or query a cluster.

- [ ] **Step 4: Integrate only accepted non-duplicate findings**

Append a dated subsection, allocate contiguous source/claim IDs, update only
the Kubernetes or Security README cells whose basis changed, and preserve all
existing general analysis. If no subquestion survives review, update only Task
and progress with the no-op evidence and skip the topic commit.

- [ ] **Step 5: Obtain Kubernetes security and content review**

The security reviewer checks least-privilege wording, threat/evidence depth,
no remediation-by-research, and no sensitive value access. The content reviewer
checks official-source fidelity and duplication. Correct every Critical or
Important finding.

- [ ] **Step 6: Validate and commit only a non-empty research delta**

Run source/claim/selector probes, strict document gates, RIA, affected/staged,
aggregate, plain/all-files pre-commit, formatter review, and diff checks. When
the reviewed research delta is non-empty, commit:

```bash
git commit -m "docs: research WER Kubernetes security gaps"
```

When the result is a reviewed no-op, make no empty commit and retain the result
in the next non-empty Task evidence commit.

### Task 5: WERG-004 — reconcile pack index, ledger, links, and cleanup

**Files:**

- Modify: `docs/90.references/research/2026-08-08-wer/README.md`
- Modify: `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/2026-08-08-wer/ci-cd-github-actions-and-qa.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md`
- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: reviewed WERG-001 admission state and all accepted WERG-002/003
  source, claim, heading, and owner results.
- Produces: one internally consistent five-owner research delta with no broken
  links, duplicate owner, stale date implication, or one-off residue.

- [ ] **Step 1: Write the integration RED probe**

Run the integration mode against the exact pre-research commit recorded by
WERG-001:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py integration --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/2026-08-08-wer --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --check-date 2026-08-09 --allowed-owner README.md --allowed-owner spec-driven-sdlc-and-document-contracts.md --allowed-owner ci-cd-github-actions-and-qa.md --allowed-owner kubernetes-infrastructure-and-security.md --allowed-owner source-coverage-and-migration-ledger.md
```

The checker rejects a missing or non-40-hex commit. It parses the final README,
ledger, and three content owners and fails on:

- a new source or claim ID without exactly one ledger row;
- an admitted question without a surviving linked owner;
- a new `2026-08-09` claim that inherits the old `2026-08-08` wording;
- an old source row whose date or content changed;
- a duplicate heading owner;
- an external claim without workspace evidence or uncertainty;
- a broken relative anchor; or
- a research-pack path outside the exact five-owner allowlist.

- [ ] **Step 2: Reconcile README and ledger projections**

Use `apply_patch` to make the request matrix, source rows, claim rows, report
links, and dated refresh boundary agree. Keep the pack's original Snapshot
Contract and existing report index intact.

- [ ] **Step 3: Inventory and bound one-off residue**

Review `git status --short`, tracked additions, ignored task scratch, `/tmp`
artifacts created by the task, and any downloaded source files. Remove only
workflow-owned one-off files; never clean unrelated user data or broad paths.

Run the exact residue check and remove any task-owned downloads or extracts by
their explicit paths. Retain the checker itself through WERG-005 terminal
targeted validation:

```bash
python3 /tmp/werg-gap-refresh-check.py residue --root . --owned-temp /tmp/werg-gap-refresh-check.py --owned-temp /tmp/werg-paths.nul --owned-temp /tmp/werg-ledger-before.md
git status --short
git ls-files --others --exclude-standard
```

The first residue invocation records the checker itself as expected owned
scratch and rejects any other `werg-*` temp path or tracked research download.
The Task records every exact path removed in this step; no wildcard or broad
directory cleanup is permitted. `/tmp/werg-gap-refresh-check.py`,
`/tmp/werg-paths.nul`, and `/tmp/werg-ledger-before.md` remain the only allowed
task-owned temporary paths until WERG-005 Step 4.

- [ ] **Step 4: Run GREEN integration and document gates**

After Step 2 reconciliation and Step 3 bounded cleanup, rerun the exact
integration command from Step 1 and require exit `0`. Then require registry
self/strict, Markdown profiles, strict links/owners, RIA self/production, and
`git diff --check` to pass.

- [ ] **Step 5: Obtain independent integration review**

The reviewer checks exact five-owner scope, ID continuity, old-row stability,
request ownership, dates, cross-links, source/claim fidelity, and cleanup.

- [ ] **Step 6: Run canonical gates and commit**

Run affected/staged, plain pre-commit, direct aggregate, all-files,
formatter-review/rerun, and diff checks. Commit:

```bash
git commit -m "docs: reconcile WER gap-only research evidence"
```

### Task 6: WERG-005 — terminal validation, review, and closure

**Files:**

- Modify: `docs/03.specs/055-workspace-engineering-gap-only-refresh/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/04.execution/plans/README.md`
- Modify: `docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md`
- Modify: `docs/04.execution/tasks/README.md`
- Modify: `docs/99.templates/support/document-profiles.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: all logical commits, final admission/source/claim/owner inventories,
  task reviews, and repository-static validation evidence.
- Produces: terminal standalone lifecycle state when existing closure contracts
  accept it, or an explicit blocked handoff that does not weaken a validator.

- [ ] **Step 1: Run a whole-branch scope and evidence audit**

Compare `main...HEAD` and require:

- only approved lifecycle/evidence files plus the five research owners;
- no change under `docs/98.archive/**`, audit-pack members, GitOps,
  infrastructure, policy, workflows, provider surfaces, or secret state;
- one admission result per requested category;
- exact new source/claim rows and no old-row drift;
- no unsupported deeper-evidence success claim;
- no tracked one-off artifact; and
- one logical commit per non-empty work package.

- [ ] **Step 2: Obtain fresh whole-branch reviews**

Dispatch independent specification/content, quality, and security reviewers.
Correct all Critical and Important findings in forward-only logical commits,
then repeat the affected review scope.

- [ ] **Step 3: Propose terminal lifecycle state in the exact index**

Set Spec, Plan, Task, index rows, progress, and the Spec 055 standalone registry
row to `done` as one staged proposal. Run focused lifecycle, registry,
links/owners, and closure checks before committing.

If the existing closure validator emits an exact Spec 055 authority diagnostic,
stop. Do not add an allowlist, test, or validator exception without a separate
human approval that names the exact contract path and expected negative
coverage.

- [ ] **Step 4: Run targeted checks, delete owned scratch, and run the terminal canonical sequence**

Resolve the WERG-001 baseline, run the complete targeted checker sequence on
the final reconciled snapshot, then remove only the exact owned temporary
paths and prove their absence:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py --self-test
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --pack docs/90.references/research/2026-08-08-wer --expected-pack-files 13 --expected-request-rows 32 --extra-topic verification-validation --require-complete
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/2026-08-08-wer --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --phase final --check-date 2026-08-09 --allowed-owner README.md --allowed-owner spec-driven-sdlc-and-document-contracts.md --allowed-owner ci-cd-github-actions-and-qa.md --allowed-owner kubernetes-infrastructure-and-security.md --allowed-owner source-coverage-and-migration-ledger.md
python3 /tmp/werg-gap-refresh-check.py kubernetes --root . --pack docs/90.references/research/2026-08-08-wer --report docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md --ledger docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --require-line-level-admission
python3 /tmp/werg-gap-refresh-check.py integration --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/2026-08-08-wer --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --check-date 2026-08-09 --allowed-owner README.md --allowed-owner spec-driven-sdlc-and-document-contracts.md --allowed-owner ci-cd-github-actions-and-qa.md --allowed-owner kubernetes-infrastructure-and-security.md --allowed-owner source-coverage-and-migration-ledger.md
python3 /tmp/werg-gap-refresh-check.py residue --root . --owned-temp /tmp/werg-gap-refresh-check.py --owned-temp /tmp/werg-paths.nul --owned-temp /tmp/werg-ledger-before.md
rm -f /tmp/werg-gap-refresh-check.py /tmp/werg-ledger-before.md
test ! -e /tmp/werg-gap-refresh-check.py
test ! -e /tmp/werg-ledger-before.md
```

Record the checker SHA-256 and every subcommand result in the Task before
deletion. Then run and record, in order:

1. targeted admission/source/claim/owner/residue checks;
2. affected lane for the final changed paths;
3. staged lane for the exact final index;
4. relevant direct tests and `bash scripts/validate-repo-quality-gates.sh .`;
5. plain `pre-commit run` against the exact index;
6. `pre-commit run --all-files`;
7. formatter review and required reruns; and
8. `git diff --check`, `git diff --cached --check`, and exact scope review; and
9. exact post-lane cleanup and absence proof:

```bash
rm -f /tmp/werg-paths.nul
test ! -e /tmp/werg-paths.nul
git status --short
```

- [ ] **Step 5: Commit terminal closure or record the blocker**

When all terminal gates and reviews pass, commit:

```bash
git commit -m "docs: close WER gap-only research refresh"
```

If closure is blocked, keep lifecycle `active`/`In Review`, commit only truthful
non-terminal evidence when it is independently useful, and request direction.

- [ ] **Step 6: Finish the development branch**

Use `superpowers:finishing-a-development-branch` to verify the clean branch and
present the user-owned choices: local merge, push and PR, keep, or discard. Do
not merge, push, remove the worktree, or delete the branch without the selected
choice.

## Verification Plan

### Task-local deterministic checker contract

WERG-001 creates exactly `/tmp/werg-gap-refresh-check.py` with `apply_patch`.
It is a Python 3 standard-library-only, read-only checker except for temporary
fixture directories created by `tempfile.TemporaryDirectory`. It has five
subcommands: `admission`, `evidence`, `kubernetes`, `integration`, and
`residue`, plus `--self-test`. Every subcommand accepts `--root`, resolves it
to this repository, rejects symlinks and paths outside the root, emits only
path/identifier/field diagnostics, and returns `0` for the requested expected
state, `1` for a contract mismatch, and `2` for invalid invocation.

The self-test must cover duplicate/missing admission rows, an unknown state,
pack-count drift, missing or extra source/claim fields, old-row mutation,
non-40-hex baselines, missing/escaping workspace paths, duplicate IDs, an
unauthorized research owner, stale date inheritance, broken anchors, and
unexpected residue. The checker source is intentionally one-off: WERG-004
records its preliminary SHA-256 and self-test result, WERG-005 records the final
SHA-256 and targeted results, and only then deletes the exact file. No
repository validator or policy owner is changed to support it.

WERG-003 invokes the same checker exactly as follows before and after accepted
Kubernetes research:

```bash
python3 /tmp/werg-gap-refresh-check.py kubernetes --root . --pack docs/90.references/research/2026-08-08-wer --report docs/90.references/research/2026-08-08-wer/kubernetes-infrastructure-and-security.md --ledger docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md --task docs/04.execution/tasks/2026-08-09-workspace-engineering-gap-only-refresh.md --require-line-level-admission
```

Before any affected or staged lane, create its exact NUL input and validate the
input count:

```bash
git diff --cached --name-only -z > /tmp/werg-paths.nul
python3 -c 'from pathlib import Path; p=Path("/tmp/werg-paths.nul").read_bytes(); xs=[x for x in p.split(b"\0") if x]; assert xs and len(xs)==len(set(xs)); print(f"paths={len(xs)}")'
```

### Targeted evidence

- Admission completeness and four-state closure.
- Official source metadata and primary-owner URL validation.
- Source/claim identifier continuity and old-row stability.
- Exact workspace path/selector existence.
- Verification/Validation seven-column matrix and term uniqueness.
- Document-family decision preservation.
- Kubernetes duplicate-research rejection and evidence-depth separation.
- Five-owner research path allowlist.
- Broken-link, duplicate-owner, stale-date, and one-off-residue rejection.

### Repository contract commands

```bash
python3 scripts/validate-document-contract-registry.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --root . --self-test
python3 scripts/validate-reference-information-architecture.py --root .
bash scripts/validate-repo-quality-gates.sh .
pre-commit run
pre-commit run --all-files
git diff --check
git diff --cached --check
```

For affected and staged lanes, create a NUL-delimited exact path file and run:

```bash
git diff --cached --name-only -z > /tmp/werg-paths.nul
python3 scripts/run-validation-lane.py --root . --lane affected --paths-file /tmp/werg-paths.nul --delimiter nul
python3 scripts/run-validation-lane.py --root . --lane staged --paths-file /tmp/werg-paths.nul --delimiter nul
```

Each lane result is independent. A repository-static PASS never substitutes
for hosted, provider-runtime, remote, credential-bearing, or live evidence.

## Risks & Mitigations

| Risk | Impact | Mitigation | Owner |
| --- | --- | --- | --- |
| Broad request causes duplicate re-research | Churn and conflicting owners | WERG-001 four-state admission before browsing; reviewer rejects already complete topics | primary + content reviewer |
| Abstract-only or paywalled standard is overstated | Unsupported normative claim | Record abstract limitation, reject unavailable detail, and use another official owner only when it directly supports the claim | docs researcher |
| Verification/Validation terminology conflicts across sources | False universal definition | Preserve source context and map explicitly to the local quality owner without redefining it | QA/content reviewer |
| Release record analysis reopens DOC-G5 | Decision conflict | Separate broader release record from release notes and preserve Spec 052 as current decision authority | spec reviewer |
| Kubernetes general content is duplicated | Bloated or misleading report | Line-level admission against existing source/claim/selector/uncertainty/refresh fields | security reviewer |
| Research recommendation mutates implementation | Unauthorized behavior change | Exact five research-owner allowlist; manifests/configuration are read-only evidence | primary |
| Source or claim IDs drift | Broken provenance | Mechanical next-ID allocation, uniqueness parser, old-row byte-stability check | quality reviewer |
| New Spec creates unowned execution graph | Strict link failure | WERG-000 atomic ADR-0022 standalone relation and reciprocal links | primary |
| Terminal closure needs a new allowlist | Unapproved validator expansion | Stop on exact diagnostic and request separate human approval | primary |
| Formatter or detect-secrets changes unrelated files | Scope contamination | Review every mutation, restore only proven incidental changes, restage exact scope, rerun lanes | primary + quality reviewer |
| One-off research files remain | Repository residue | No tracked downloads; exact residue inventory and scoped cleanup | implementer |

## Completion Criteria

- Spec 055's ten `VAL-WERG-*` criteria have exact terminal evidence or a
  truthful blocker.
- Every requested topic has one reviewed admission state.
- Only admitted questions have new external source and claim rows.
- Every new source has official/primary URL, check date, adopted scope,
  rejected inference, and refresh trigger.
- Every new claim has source linkage, exact workspace evidence, uncertainty,
  status, and surviving owner.
- Verification and Validation are explicit, externally sourced, and mapped
  without redefining the canonical quality contract.
- Document-family additions preserve current local lifecycle and Spec 052
  decisions.
- Kubernetes additions are non-duplicate, evidence-depth bounded, and make no
  desired-state change.
- Research output changes only the exact five existing pack owners.
- Existing IDs, dates, anchors, terminal evidence, audit/RIA/Stage 98 content,
  and deleted predecessor history remain stable.
- No tracked or workflow-owned one-off residue remains.
- Each non-empty logical work package has review and commit evidence.
- Targeted, affected, staged, tests, aggregate, plain/all-files pre-commit,
  formatter/rerun, and diff results are recorded.
- Whole-branch specification/content, quality, and security reviews are
  Approved with no remaining Critical or Important finding.
- Hosted, provider-runtime, remote, credential-bearing, and live lanes remain
  explicit `DEFER`.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| N/A — VAL-WERG-001 uses approved Spec 055; WERG-000 adds its reciprocal link during atomic activation | WERG-001 | [Complete four-state admission matrix and review](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-002 shares the Spec source above | WERG-004 | [Exact five-owner research path set](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-003 shares the Spec source above | WERG-002, WERG-003 | [New source rows and source-fidelity reviews](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-004 shares the Spec source above | WERG-002, WERG-003, WERG-004 | [Claim rows, workspace selector checks, and owner closure](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-005 shares the Spec source above | WERG-002 | [External terminology plus responsibility/evidence/failure matrix](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-006 shares the Spec source above | WERG-002 | [Document-family comparison and Spec 052 decision review](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-007 shares the Spec source above | WERG-003 | [Kubernetes admission, source, duplication, and security review](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-008 shares the Spec source above | WERG-004, WERG-005 | [Identifier/date/history/protected-surface diff evidence](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-009 shares the Spec source above | WERG-004 | [One-off residue inventory and cleanup review](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |
| N/A — VAL-WERG-010 shares the Spec source above | WERG-000–005 | [Logical commit ledger and canonical validation/review evidence](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md#task-table) |

### Related documents

- **Approved Spec**:
  [Spec 055](../../03.specs/055-workspace-engineering-gap-only-refresh/spec.md)
- **Standalone execution decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Terminal predecessor design**:
  `docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md`
- **Document decision boundary**:
  `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- **Reciprocal Task**:
  [Task](../tasks/2026-08-09-workspace-engineering-gap-only-refresh.md)
- **Research owner**:
  [2026-08-08 WER pack](../../90.references/research/2026-08-08-wer/README.md)
