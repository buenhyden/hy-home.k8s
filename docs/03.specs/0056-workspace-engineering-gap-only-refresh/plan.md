---
title: 'Workspace Engineering Gap-only Research Refresh Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-08-10
artifact_id: "SPEC-0056-PLAN-0001"
---

# Workspace Engineering Gap-only Research Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The primary controller uses
> executing-plan checkpoints while a fresh worker owns each implementation
> task and separate workers perform specification/content and quality review.

**Goal:** Add only previously unresearched or externally under-sourced
`Partial` evidence to the existing `0001-workspace-engineering` pack, with explicit
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
  `docs/90.references/research/0001-workspace-engineering/`; no new research directory or
  addendum is created.
- The only research-pack files eligible for modification are `README.md`,
  `m0004-spec-driven-sdlc-and-document-contracts.md`,
  `m0008-ci-cd-github-actions-and-qa.md`,
  `m0007-kubernetes-infrastructure-and-security.md`, and
  `m0012-source-coverage.md`.
- Every requested category receives exactly one admission result:
  `complete-existing`, `admit-unresearched`,
  `admit-under-sourced-partial`, or `exclude-deep-evidence`.
- Only `admit-unresearched` and `admit-under-sourced-partial` authorize new
  external-source or claim rows.
- All accepted new source and claim evidence uses check date `2026-08-10`;
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
[Spec 0056](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md)
without reopening completed
`docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md`.
The research pack already maps 32 requested topics to twelve reference owners
and contains dated source and claim registers. Most requested categories have
adequate official-source coverage. The work therefore treats the broad request
as an admission corpus, not as permission to rewrite every topic.

The planned output is an in-place evidence refresh. The directory keeps its
`0001-workspace-engineering` identity while every additive section and ledger row records a
separate `2026-08-10 gap-only source refresh` boundary. Lifecycle documents,
indexes, the standalone registry relation, and durable progress evidence are
execution metadata and do not become research-topic owners.

The written Spec was approved by the human on 2026-08-09, and the human then
selected subagent-driven execution. WERG-000 therefore activates this Plan,
the reciprocal [Task](plan.md),
their Spec/index owners, and the exact ADR-0022 standalone relation atomically.

## Context

### Current research state

- The pack contains one README plus twelve existing references.
- The README has 32 sequential `REQ-WERPC-*` rows.
- PRD, AD, Policy, and Runbook currently rely primarily on local
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

- PRD and AD profile, lifecycle, and template facts:
  `docs/99.templates/registry.json` and
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
  [Task](plan.md).

### Candidate primary-source families

Workers must verify the exact current official pages before accepting any
claim. The candidate owners are:

- ISO/IEC/IEEE requirements-engineering and architecture-description
  standards for PRD/AD semantics;
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

### Legacy Task ledger inputs

This Task is the execution-evidence owner for the approved gap-only refresh of
the existing `docs/90.references/research/0001-workspace-engineering/` pack. It admits
only previously unresearched questions or externally under-sourced `Partial`
questions, keeps authenticated/provider-runtime/hosted/remote/live evidence
out of scope, and records one logical commit per non-empty work package.

The written Spec is approved and the human selected subagent-driven execution.
WERG-000 activates this Task with the reciprocal
[Spec](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md) and
[Plan](plan.md) through
the exact ADR-0022 standalone relation before any external research or pack
edit begins.

- [Active Spec 055](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md)
- [Active implementation Plan](plan.md)
- [ADR-0022 direct-approval standalone lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Existing 2026-08-08 WER research pack](../../90.references/research/0001-workspace-engineering/README.md)
- Terminal predecessor: `docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md`
- Document taxonomy decision: `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Document contracts registry](../../99.templates/registry.json)
## Goals & In-Scope

- Activate a new Spec 055 standalone execution relation only after Plan
  approval and without changing `programLineage`.
- Produce a complete, reviewable admission result for every original requested
  category plus the newly explicit Verification/Validation request.
- Strengthen admitted PRD, AD, Policy, Runbook, and Release semantics with
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

- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md`
- Modify: `docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/99.templates/registry.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: approved Spec 055, ADR-0022, exact Plan/Task paths, and the current
  sorted `standaloneExecutions` array.
- Produces: one unique active standalone relation for Spec `055`, with exact
  Plan and Task identities and `approvalMode: spec-body-record`.

- [x] **Step 1: Record the exact draft baseline and human approval**

Run:

```bash
git status --short --branch
git log -1 --oneline
rg -n "status: draft|pending written Spec approval|0056-workspace-engineering-gap-only-refresh" \
  docs/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md \
  docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md \
  docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records \
  docs/03.specs/README.md \
  docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md \
  docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records
```

Expected: clean planning baseline; Spec, Plan, and Task are draft; no Spec 055
standalone registry row exists.

- [x] **Step 2: Apply the atomic active relation**

Use `apply_patch` to:

1. set Spec, Plan, and Task frontmatter to `status: active`;
1. replace pending Plan/Task text in Spec 055 with reciprocal rendered links;
1. record the exact direct-human approval and no-separate-PRD/AD standalone
   lifecycle statements in Spec 055;
1. add the reciprocal Spec 055 traceability row to ADR-0022;
1. mark all three README index rows `Active`;
1. insert the exact sorted registry object:

```json
{
  "spec": "055",
  "plan": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md",
  "task": "docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records",
  "state": "active",
  "reason": "Direct human-approved gap-only external-source refresh of the existing 2026-08-08 WER pack without separate PRD/AD authority",
  "decision": "0022",
  "approvalMode": "spec-body-record"
}
```

1. mark WERG-000 `In Review` with the exact changed-path and approval evidence.

- [x] **Step 3: Run focused activation validation**

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

- [x] **Step 4: Obtain specification and quality review**

Dispatch one specification reviewer and one quality reviewer against only the
WERG-000 diff. Correct every Critical or Important finding before commit.

- [x] **Step 5: Stage, run the canonical commit gates, and commit**

Run the affected and staged lanes for the exact changed paths, then plain
pre-commit, the direct aggregate, all-files pre-commit, formatter review, and
both diff checks. Commit only after the final exact index is clean:

```bash
git commit -m "docs: activate WER gap-only research refresh"
```

### Task 2: WERG-001 — classify the complete requested scope

**Files:**

- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the user's complete category list, the 32 existing request rows,
  every existing `SRC-WERPC-*` and `CLM-WERPC-*` row, and all thirteen files
  in the current pack. The five candidate owners bound possible writes; they
  do not narrow the read-only comparison corpus.
- Produces: one admission record per requested category and an exact admitted
  question set used by WERG-002 and WERG-003.

- [x] **Step 1: Write and run the admission RED probe**

Create the task-local checker at the exact temporary path and run its bounded
self-test plus baseline mode:

```bash
python3 /tmp/werg-gap-refresh-check.py --self-test
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --pack docs/90.references/research/0001-workspace-engineering --expected-pack-files 13 --expected-request-rows 32 --extra-topic verification-validation --expect baseline-gap
```

The checker parses the README request matrix, all thirteen pack files, and all
source/claim tables. It prints only identifiers, missing field names, and
paths—never page bodies or secret data.

Expected RED: Verification/Validation has no independent research owner and
the four local-only document-family rows plus Release's SemVer-only external
basis fail the source-class assertion.

- [x] **Step 2: Build the complete admission matrix**

For each requested topic, record in the Task:

```text
requested topic | existing REQ owner | existing report#heading |
existing source IDs | existing claim IDs | admission state | exact reason
```

The reason must identify either the material missing question, the adequate
existing source/claim boundary, or the deeper evidence that makes the topic
`exclude-deep-evidence`.

- [x] **Step 3: Verify admission completeness and uniqueness**

Run the reviewed-matrix mode:

```bash
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --pack docs/90.references/research/0001-workspace-engineering --expected-pack-files 13 --expected-request-rows 32 --extra-topic verification-validation --require-complete
```

The command requires:

- one row per requested topic;
- only the four closed admission states;
- no duplicate requested topic or owner;
- no `complete-existing` or `exclude-deep-evidence` row in the admitted set;
- exact owner/heading existence for every existing reference; and
- no new web-source row before the admitted set is reviewed.

- [x] **Step 4: Obtain independent admission review**

The reviewer must compare every final row—`complete-existing`, both admitted
states, and `exclude-deep-evidence`—with all thirteen current pack files, not
only its README status or the five writable owners. A topic is removed from
the admitted set when the existing report already has a direct official
source, exact local mapping, uncertainty boundary, and refresh trigger for the
same question. A false `complete-existing` or `exclude-deep-evidence` result is
an Important finding and blocks browsing.

- [x] **Step 5: Record the reviewed result and commit**

Append a bounded `2026-08-09 Gap-only admission` subsection to the existing
ledger, update WERG-001 evidence and progress, run focused profile/link/diff
checks plus the canonical commit gates, and commit:

```bash
git commit -m "docs: classify WER gap-only research scope"
```

### Task 3: WERG-002 — research document families and Verification/Validation

**Files:**

- Modify: `docs/90.references/research/0001-workspace-engineering/README.md`
- Modify: `docs/90.references/research/0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md`
- Modify: `docs/90.references/research/0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md`
- Modify: `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the reviewed WERG-001 admitted rows, official primary pages, local
  document profiles/templates, Spec 052 decisions, and the quality-lane owner.
- Produces: additive dated source rows, bounded claim rows, document-family
  semantics, an explicit Verification/Validation matrix, and reconciled README
  ownership/status cells.

- [x] **Step 1: Reproduce the focused external-basis RED**

Run the evidence checker against the activation commit before browsing:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/0001-workspace-engineering --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --phase baseline --check-date 2026-08-10
```

The command emits exact missing field and owner identifiers while showing:

- PRD, AD, Policy, and Runbook README rows use local-only source wording;
- Release uses SemVer plus local absence evidence but no broader approval and
  evidence source; and
- the QA owner has no externally sourced definition table whose columns are
  `Term`, `Question`, `Actor`, `Input`, `Evidence`, `Failure meaning`, and
  `Workspace mapping`.

Expected: all admitted rows fail at least one asserted external-basis field.

- [x] **Step 2: Research official primary sources**

Assign one documentation-research worker to requirements/architecture and one
to policy/runbook/release/V&V. Each worker must:

1. open and read the complete relevant official page;
2. capture the exact URL and title;
3. record check date `2026-08-10`;
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

- [x] **Step 3: Allocate source and claim IDs without renumbering**

Mechanically read the maximum existing numeric suffix for `SRC-WERPC-*` and
`CLM-WERPC-*`. Allocate contiguous new IDs only for accepted claims. Assert
that every old row is byte-identical before the insertion point and retains
its original checked date.

- [x] **Step 4: Integrate the two owner reports**

Use `apply_patch` to:

- add a `2026-08-10 gap-only source refresh` subsection to the SDLC reference;
- update only admitted document-family rows or add linked analysis below the
  matrix;
- preserve Spec 052 DOC-G1 and DOC-G5 as accepted local decisions;
- add the seven-column Verification/Validation matrix to the QA reference;
- map the terms to validation, verification, tests, review, release, and
  operations without redefining `quality-standards.md`; and
- update README source/status cells and add a new request row only if WERG-001
  proved no current request owner.

- [x] **Step 5: Run focused GREEN probes**

Run:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/0001-workspace-engineering --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --phase final --check-date 2026-08-10 --allowed-owner README.md --allowed-owner m0004-spec-driven-sdlc-and-document-contracts.md --allowed-owner m0008-ci-cd-github-actions-and-qa.md --allowed-owner m0007-kubernetes-infrastructure-and-security.md --allowed-owner m0012-source-coverage.md
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

- [x] **Step 6: Obtain content and quality review**

The content reviewer checks source fidelity, terminology, Spec 052 decision
preservation, and absence of policy invention. The quality reviewer checks
table contracts, identifiers, links, profiles, concision, and no duplicated
topic owner. Correct every Critical or Important finding.

- [x] **Step 7: Validate and commit**

Run focused source/claim/selector probes, strict registry/profile/links, RIA,
affected/staged lanes, plain and all-files pre-commit, aggregate, formatter
review, and diff checks. Commit:

```bash
git commit -m "docs: research WER document and validation gaps"
```

### Task 4: WERG-003 — research exact Kubernetes security deltas

**Files:**

- Modify when non-empty: `docs/90.references/research/0001-workspace-engineering/README.md`
- Modify when non-empty: `docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md`
- Modify when non-empty: `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: the reviewed WERG-001 Kubernetes subquestion admissions, current
  Kubernetes report, exact manifests/configuration, and official upstream
  sources.
- Produces: only non-duplicative K8s source/claim rows and analysis, or a
  reviewed no-op result with no empty topic commit.

- [x] **Step 1: Run the line-level duplication and gap RED probe**

For each candidate subquestion, compare the exact current report paragraphs,
source rows, claim rows, and workspace selectors. Admit a subquestion only
when at least one of these is missing:

- a direct official source for the precise claim;
- an exact current workspace selector;
- an uncertainty/deeper-evidence boundary; or
- a refresh trigger.

Expected: already complete general NetworkPolicy, Pod Security, and image-tag
explanations are rejected; only exact subquestions that remain absent proceed.

2026-08-10 execution evidence: the exact planned `kubernetes` command returned
`PASS kubernetes` on the pre-edit baseline because that mode confirms admission
markers and the existing NetworkPolicy boundary rather than new-row absence.
The companion content probe for `SRC-WERPC-060`, `CLM-WERPC-008-01`, and the
dated refresh heading returned exit 1. Line-level comparison admitted the three
question deltas and rejected Namespace ingress/default-deny as duplicate.

- [x] **Step 2: Research the admitted official sources**

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

Result: official Kubernetes, kube-state-metrics v2.14.0, Argo CD, Helm,
Sigstore, SLSA, and GitHub primary sources were checked on 2026-08-10 and
allocated only as `SRC-WERPC-060`–`065`. No Namespace NetworkPolicy source was
added.

- [x] **Step 3: Reconcile exact workspace evidence**

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

Result: the report records exact kube-state-metrics ClusterRole/container,
Adminer Rollout and linter-field, root/ApplicationSet revision, Helm chart,
bootstrap, and tag-only image selectors. Inspection was repository-static; no
Secret value, cluster, registry, hosted workflow, or remote system was queried.

- [x] **Step 4: Integrate only accepted non-duplicate findings**

Append a dated subsection, allocate contiguous source/claim IDs, update only
the Kubernetes or Security README cells whose basis changed, and preserve all
existing general analysis. If no subquestion survives review, update only Task
and progress with the no-op evidence and skip the topic commit.

Result: the dated report subsection, contiguous `SRC-WERPC-060`–`065`, claims
`CLM-WERPC-008-01`–`06`, and only the Kubernetes/Security README cells were
updated. The delta is non-empty; review and commit gates remain pending.

- [x] **Step 5: Obtain Kubernetes security and content review**

The security reviewer checks least-privilege wording, threat/evidence depth,
no remediation-by-research, and no sensitive value access. The content reviewer
checks official-source fidelity and duplication. Correct every Critical or
Important finding.

- [x] **Step 6: Validate and commit only a non-empty research delta**

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

- Modify: `docs/90.references/research/0001-workspace-engineering/README.md`
- Modify: `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/0001-workspace-engineering/m0004-spec-driven-sdlc-and-document-contracts.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/0001-workspace-engineering/m0008-ci-cd-github-actions-and-qa.md`
- Modify only when required by accepted evidence:
  `docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: reviewed WERG-001 admission state and all accepted WERG-002/003
  source, claim, heading, and owner results.
- Produces: one internally consistent five-owner research delta with no broken
  links, duplicate owner, stale date implication, or one-off residue.

- [x] **Step 1: Write the integration RED probe**

Run the integration mode against the exact pre-research commit recorded by
WERG-001:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py integration --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/0001-workspace-engineering --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --check-date 2026-08-10 --allowed-owner README.md --allowed-owner m0004-spec-driven-sdlc-and-document-contracts.md --allowed-owner m0008-ci-cd-github-actions-and-qa.md --allowed-owner m0007-kubernetes-infrastructure-and-security.md --allowed-owner m0012-source-coverage.md
```

The checker rejects a missing or non-40-hex commit. It parses the final README,
ledger, and three content owners and fails on:

- a new source or claim ID without exactly one ledger row;
- an admitted question without a surviving linked owner;
- a new `2026-08-10` claim that inherits the old `2026-08-08` wording;
- an old source row whose date or content changed;
- a duplicate heading owner;
- an external claim without workspace evidence or uncertainty;
- a broken relative anchor; or
- a research-pack path outside the exact five-owner allowlist.

2026-08-10 result: the integration probe was already GREEN after the reviewed
WERG-002 and WERG-003 fixes; no false RED was fabricated. Earlier REDs for date
drift, promoted request ownership, nested Markdown links, missing uncertainty
labels, and one external fragment are preserved in the Task evidence.

- [x] **Step 2: Reconcile README and ledger projections**

Use `apply_patch` to make the request matrix, source rows, claim rows, report
links, and dated refresh boundary agree. Keep the pack's original Snapshot
Contract and existing report index intact.

Result: the README and ledger now state the exact 13-file, 33-request,
65-source, 65-claim closure and five-owner boundary without changing the
Snapshot Contract or Report Index.

- [x] **Step 3: Inventory and bound one-off residue**

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

Result: residue PASS. The checker and current NUL path file are present;
`/tmp/werg-ledger-before.md` is absent. No untracked research download or
tracked scratch path exists, and nothing unrelated was removed.

- [x] **Step 4: Run GREEN integration and document gates**

After Step 2 reconciliation and Step 3 bounded cleanup, rerun the exact
integration command from Step 1 and require exit `0`. Then require registry
self/strict, Markdown profiles, strict links/owners, RIA self/production, and
`git diff --check` to pass.

- [x] **Step 5: Obtain independent integration review**

The reviewer checks exact five-owner scope, ID continuity, old-row stability,
request ownership, dates, cross-links, source/claim fidelity, and cleanup.

- [x] **Step 6: Run canonical gates and commit**

Run affected/staged, plain pre-commit, direct aggregate, all-files,
formatter-review/rerun, and diff checks. Commit:

```bash
git commit -m "docs: reconcile WER gap-only research evidence"
```

### Task 6: WERG-005 — terminal validation, review, and closure

**Files:**

- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/plan.md`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records`
- Modify: `docs/99.templates/registry.json`
- Modify: `docs/00.agent-governance/memory/progress.md`

**Interfaces:**

- Consumes: all logical commits, final admission/source/claim/owner inventories,
  task reviews, and repository-static validation evidence.
- Produces: terminal standalone lifecycle state when existing closure contracts
  accept it, or an explicit blocked handoff that does not weaken a validator.

- [x] **Step 1: Run a whole-branch scope and evidence audit**

Compare `main...HEAD` and require:

- only approved lifecycle/evidence files plus the five research owners;
- no change under `docs/98.archive/**`, audit-pack members, GitOps,
  infrastructure, policy, workflows, provider surfaces, or secret state;
- one admission result per requested category;
- exact new source/claim rows and no old-row drift;
- no unsupported deeper-evidence success claim;
- no tracked one-off artifact; and
- one logical commit per non-empty work package.

- [x] **Step 2: Obtain fresh whole-branch reviews**

Dispatch independent specification/content, quality, and security reviewers.
Correct all Critical and Important findings in forward-only logical commits,
then repeat the affected review scope.

- [x] **Step 3: Propose terminal lifecycle state in the exact index**

Set Spec, Plan, Task, index rows, progress, and the Spec 055 standalone registry
row to `done` as one staged proposal. Run focused lifecycle, registry,
links/owners, and closure checks before committing.

If the existing closure validator emits an exact Spec 055 authority diagnostic,
stop. Do not add an allowlist, test, or validator exception without a separate
human approval that names the exact contract path and expected negative
coverage.

- [x] **Step 4: Run targeted checks, delete owned scratch, and run the terminal canonical sequence**

Resolve the WERG-001 baseline, run the complete targeted checker sequence on
the final reconciled snapshot, then remove only the exact owned temporary
paths and prove their absence:

```bash
WERG_ADMISSION_COMMIT="$(git log -1 --format=%H --grep='^docs: classify WER gap-only research scope$')"
test "${#WERG_ADMISSION_COMMIT}" -eq 40
python3 /tmp/werg-gap-refresh-check.py --self-test
python3 /tmp/werg-gap-refresh-check.py admission --root . --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --pack docs/90.references/research/0001-workspace-engineering --expected-pack-files 13 --expected-request-rows 33 --extra-topic verification-validation --require-complete
python3 /tmp/werg-gap-refresh-check.py evidence --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/0001-workspace-engineering --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --phase final --check-date 2026-08-10 --allowed-owner README.md --allowed-owner m0004-spec-driven-sdlc-and-document-contracts.md --allowed-owner m0008-ci-cd-github-actions-and-qa.md --allowed-owner m0007-kubernetes-infrastructure-and-security.md --allowed-owner m0012-source-coverage.md
python3 /tmp/werg-gap-refresh-check.py kubernetes --root . --pack docs/90.references/research/0001-workspace-engineering --report docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md --ledger docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --require-line-level-admission
python3 /tmp/werg-gap-refresh-check.py integration --root . --baseline-ref "$WERG_ADMISSION_COMMIT" --pack docs/90.references/research/0001-workspace-engineering --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --check-date 2026-08-10 --allowed-owner README.md --allowed-owner m0004-spec-driven-sdlc-and-document-contracts.md --allowed-owner m0008-ci-cd-github-actions-and-qa.md --allowed-owner m0007-kubernetes-infrastructure-and-security.md --allowed-owner m0012-source-coverage.md
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

Result: the terminal repository-static sequence passed and the owned scratch
absence was recorded in closure commit `22002d91`. Hosted, provider-runtime,
remote, credential-bearing, and live evidence remains `DEFER`.

- [x] **Step 5: Commit terminal closure or record the blocker**

When all terminal gates and reviews pass, commit:

```bash
git commit -m "docs: close WER gap-only research refresh"
```

If closure is blocked, keep lifecycle `active`/`In Review`, commit only truthful
non-terminal evidence when it is independently useful, and request direction.

Result: `22002d91` closed the lifecycle with truthful validation evidence and
was merged through `79e44638`.

- [x] **Step 6: Finish the development branch**

Use `superpowers:finishing-a-development-branch` to verify the clean branch and
present the user-owned choices: local merge, push and PR, keep, or discard. Do
not merge, push, remove the worktree, or delete the branch without the selected
choice.

Result: the selected branch finish is evidenced by merge commit `79e44638`; no
hosted, provider-runtime, remote, credential-bearing, or live behavior is
claimed by this repository-static record.

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
python3 /tmp/werg-gap-refresh-check.py kubernetes --root . --pack docs/90.references/research/0001-workspace-engineering --report docs/90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md --ledger docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md --task docs/03.specs/0056-workspace-engineering-gap-only-refresh/README.md#task-records --require-line-level-admission
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

### Legacy Task verification evidence

WERG-000 activation is complete. The human selected subagent-driven execution
on 2026-08-09, and the reciprocal active Spec/Plan/Task/index relation plus one
sorted ADR-0022 standalone registry row have been applied across the exact nine
authorized activation paths. No web research, research-pack content change,
hosted/provider/live action or secret access is claimed by this repository-static
activation state.

Focused rerun results at the in-review boundary are registry self-test PASS
(132 cases, 64 profiles, 30 templates), registry strict PASS (505 paths; zero
uncovered or ambiguous), Markdown profiles strict PASS (zero violations),
strict links PASS, and diff-check PASS. The initial strict-links RED is resolved
by the exact Spec body approval statements, ADR-0022 reciprocal traceability
row, and rendered Spec criterion link. The earlier production RIA diagnostic
was the expected pre-staging exact-index authority boundary; RIA was not rerun
in this narrow focused-fix round and remains part of the exact staged gate.

Independent WERG-000 specification/content and quality reviews are Approved
with no remaining Critical or Important finding. Both reviews confirmed the
exact nine-path activation, direct-approval semantics, reciprocal links,
sorted standalone relation, and unchanged `programLineage` and research pack.

The exact nine-path index then passed RIA self-test and production validation,
affected and staged lanes, the direct repository aggregate, plain pre-commit,
all-files pre-commit, formatter review, and both worktree/cached diff checks.
No hook changed a tracked file. Hosted, provider-runtime, remote,
credential-bearing, and live evidence remains `DEFER`.

Independent Plan review is Approved with no remaining Critical or Important
finding after correcting the written-approval state, full 13-file admission
review, exact task-local probe interfaces, reciprocal draft exclusion, and
terminal scratch-cleanup order.

WERG-001 created the task-local standard-library checker at the exact planned
temporary path. Its 23-case fixture-based self-test passes and baseline mode reproduces the
expected missing independent Verification/Validation owner plus the local-only
PRD, AD, Policy, and Runbook source classes and Release's SemVer-only external
basis. The complete matrix below reads all 13 pack files and classifies all 32
existing request rows plus Verification/Validation without adding a source,
claim, request, or web-evidence row.

The first quality review found that the checker did not yet pin the exact
topic-to-state mapping/admitted set and that several path-boundary self-tests
were placeholders. The GREEN checker now pins all 33 states and eight admitted
topics, routes every derived owner path through the symlink-safe root boundary,
and exercises state, membership, field, path, ID, date, anchor, and residue
negative fixtures, including old-row mutation, outside-root path, symlink-root,
and symlink-owner rejection. The first content review approved every classification and
source/claim mapping after identifying a transient self-test missing-path error
and one malformed Markdown delimiter; both mechanical defects are corrected.
The final quality re-review is Approved with no remaining Critical or Important
finding. The full-pack content reviewer likewise approved all 33 states, source
and claim mappings, the eight-topic admitted set, and the duplicate rejection
for namespace ingress/default-deny semantics after the two mechanical fixes.

WERG-002 reproduced the six admitted external-basis gaps before browsing, then
checked official primary sources for PRD, AD, Policy, Release, Runbook,
Verification, and Validation on 2026-08-10. It added only `SRC-WERPC-053`–`059`
and `CLM-WERPC-007-01`–`08`; all prior source and claim rows remain unchanged.
The SDLC owner now distinguishes the five admitted document families, while
the QA owner contains one exact seven-column row each for Verification and
Validation. The matrix preserves repository `VAL-*` identifiers as criterion
IDs and does not infer intended-use, operator, hosted, or live validation from
a repository-static PASS.

The first WERG-002 content review corrected two overstatements: DOC-G10 is an
approved Spec 052 decision with queued, not executed, WORK-013, and no source
supported the removed break-glass attribution. The first quality review aligned
the actual 2026-08-10 research date with Spec and Plan and added explicit SDLC,
release-readiness, and operations mappings. Its second round exposed two
task-local checker defects: the historical `verification-validation` admission
row did not recognize the promoted `Verification/Validation` request owner,
and a nested Markdown-link regex produced false broken anchors. The corrected
checker preserves the 32-row admission evidence, validates the final 33-row
promotion and current owner anchor, parses nested links safely, and passes 28
self-test cases at SHA-256
`12580e30cd70872c112b1f7279f556de3868804284be8faa67652c7707e93363`.
Final WERG-002 content and quality re-reviews are Approved with zero remaining
Critical or Important findings.

The exact eight-path WERG-002 index then passed RIA self-test and production,
affected and staged lanes, the direct repository aggregate, plain pre-commit,
all-files pre-commit, formatter review, and both worktree/cached diff checks.
No hook or formatter changed a tracked file. The eight paths are Spec 055, its
Plan and Task, durable progress, pack README, SDLC report, QA report, and the
source/claim ledger. Hosted, provider-runtime, remote, credential-bearing, and
live evidence remains `DEFER`.

WERG-003 compared each admitted line-level question against the existing
report, source/claim rows, and exact repository selectors. The exact planned
`kubernetes` command returned `PASS kubernetes` before editing because its
contract verifies the admission markers and existing NetworkPolicy boundary;
the companion content-absence probe for `SRC-WERPC-060`,
`CLM-WERPC-008-01`, and the dated subsection returned exit 1. Official sources
checked on 2026-08-10 produced only `SRC-WERPC-060`–`065` and
`CLM-WERPC-008-01`–`06`. The report explicitly rejects repeat research for
Namespace ingress/default-deny and preserves effective RBAC, actual metrics,
Adminer compatibility/admission, Argo reconciliation, artifacts, trust policy,
registry, hosted, remote, and live results as `DEFER`. Independent Kubernetes
security/content review and commit gates remain pending.

Independent WERG-003 content review is Approved with no Critical or Important
finding. The first security review identified one inaccurate phrase that called
the default-mounted ServiceAccount token unrestricted even though modern
Kubernetes uses bounded, rotating projected tokens and default permissions are
separate from mount behavior. The corrected report now distinguishes the
default automatic credential mount from a deliberately bounded projected
token. Final security re-review is Approved with no remaining Critical or
Important finding.

The exact six-path WERG-003 index then passed RIA self-test and production,
affected and staged lanes, the direct repository aggregate, plain pre-commit,
all-files pre-commit, formatter review, and both worktree/cached diff checks.
No hook or formatter changed a tracked file. The six paths are the WERG Plan,
Task, durable progress, pack README, Kubernetes/Security report, and
source/claim ledger.

WERG-004 found the reviewed WERG-002/003 result already GREEN under the exact
integration command, so it did not fabricate a new RED. The reconciliation
adds one bounded README summary and one ledger result section: 13 pack files,
33 request owners, 65 source IDs, 65 claim IDs, exact five-owner changed-path
scope, frozen-row stability, truthful dates, and resolved relative anchors.
The residue checker reports only `/tmp/werg-gap-refresh-check.py` and
`/tmp/werg-paths.nul`; `/tmp/werg-ledger-before.md` is absent. These scratch
paths remain only until WERG-005 terminal targeted validation and lanes.
Independent WERG-004 integration review is Approved with no Critical or
Important finding; it confirms the exact counts, five-owner scope, frozen-row
stability, date and link closure, unchanged Snapshot Contract/Report Index,
and truthful residue boundary.

The exact five-path WERG-004 index then passed RIA self-test and production,
affected and staged lanes, the direct repository aggregate, plain pre-commit,
all-files pre-commit, formatter review, and both worktree/cached diff checks.
No hook or formatter changed a tracked file. The five paths are the WERG Plan,
Task, durable progress, pack README, and source/claim ledger.

Before each logical commit, the implementation owner must record the exact
RED/GREEN result, independent specification/content and quality disposition,
affected/staged paths, aggregate and pre-commit outcomes, formatter mutations,
diff checks, residual risks, and deeper-evidence `DEFER` boundary. WERG-003
must make no empty topic commit when review admits no new Kubernetes evidence.

### 2026-08-09 Gap-only admission matrix

Admission source baseline: `SRC-WERPC-052`; claim baseline: `CLM-WERPC-006-08`.
Ranges below are inclusive, and `N/A` means that the current pack has no
independent request owner or source/claim row for that exact requested topic.

| Requested topic         | Existing REQ owner            | Existing report#heading                                                               | Existing source IDs                                              | Existing claim IDs                                                            | Admission state               | Exact reason                                                                                                                                                                                                                                                          |
| ----------------------- | ----------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Harness                 | `REQ-WERPC-001`               | `m0002-harness-and-loop-engineering.md#harness-baseline`                                    | `SRC-WERPC-009`–`SRC-WERPC-013`                                  | `CLM-WERPC-002-01`                                                            | `complete-existing`           | Official Codex sources, exact local harness owners, the static/runtime uncertainty boundary, and refresh triggers already answer the requested harness-elements question.                                                                                             |
| Loop                    | `REQ-WERPC-002`               | `m0002-harness-and-loop-engineering.md#loop-baseline`                                       | `SRC-WERPC-009`–`SRC-WERPC-013`                                  | `CLM-WERPC-002-02`–`CLM-WERPC-002-03`                                         | `complete-existing`           | The loop states, retry and termination rules, local machine contract, provider-runtime limit, and source refresh boundary are already explicit.                                                                                                                       |
| Workspace application   | `REQ-WERPC-003`               | `m0001-workspace-governance-and-common-agent-environment.md#workspace-application-baseline` | `SRC-WERPC-004`–`SRC-WERPC-013`                                  | `CLM-WERPC-002-04`                                                            | `complete-existing`           | The current report maps provider-neutral rules to exact workspace gateways and keeps native discovery and runtime application outside static evidence.                                                                                                                |
| Claude                  | `REQ-WERPC-004`               | `m0003-provider-implementation-status.md#claude-baseline`                                   | `SRC-WERPC-004`–`SRC-WERPC-008`                                  | `CLM-WERPC-002-05`–`CLM-WERPC-002-06`                                         | `complete-existing`           | Anthropic's memory, settings, hooks, subagents, permissions, and MCP surfaces are directly sourced and separated from unobserved local runtime delivery.                                                                                                              |
| Codex                   | `REQ-WERPC-005`               | `m0003-provider-implementation-status.md#codex-baseline`                                    | `SRC-WERPC-009`–`SRC-WERPC-013`                                  | `CLM-WERPC-002-07`                                                            | `complete-existing`           | Official Codex instruction, configuration, hook, subagent, sandbox, approval, and MCP surfaces already have local-adapter and runtime limits.                                                                                                                         |
| Common system           | `REQ-WERPC-006`               | `m0001-workspace-governance-and-common-agent-environment.md#common-system-baseline`         | `SRC-WERPC-004`–`SRC-WERPC-013`                                  | `CLM-WERPC-002-08`–`CLM-WERPC-002-09`                                         | `exclude-deep-evidence`       | The static common control plane is documented; closing provider parity, discovery, effective permissions, model resolution, or execution requires excluded provider-runtime evidence rather than more desk research.                                                  |
| Spec-driven development | `REQ-WERPC-007`               | `m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline`         | `SRC-WERPC-014`                                                  | `CLM-WERPC-003-01`                                                            | `complete-existing`           | Spec Kit primary guidance and the exact local Spec-to-Plan-to-Task mapping already establish the practice model, limits, and refresh trigger.                                                                                                                         |
| Kubernetes              | `REQ-WERPC-008`               | `m0007-kubernetes-infrastructure-and-security.md#kubernetes-baseline`                       | `SRC-WERPC-023`–`SRC-WERPC-034`                                  | `CLM-WERPC-004-01`–`CLM-WERPC-004-11`                                         | `admit-under-sourced-partial` | General NetworkPolicy, admission, secrets, GitOps, and security boundaries are complete, but exact kube-state-metrics Secret metadata RBAC, Adminer service-account hardening, and immutable revision and provenance distinctions lack direct question-level sources. |
| Infrastructure          | `REQ-WERPC-009`               | `m0007-kubernetes-infrastructure-and-security.md#infrastructure-baseline`                   | `SRC-WERPC-027`, `SRC-WERPC-032`–`SRC-WERPC-034`                 | `CLM-WERPC-004-01`, `CLM-WERPC-004-07`–`CLM-WERPC-004-11`                     | `exclude-deep-evidence`       | Static bootstrap, GitOps, gateway, recovery, and supply-chain boundaries are mapped; remaining k3d, gateway, registry, hosted-CI, cloud, reconciliation, and health questions require excluded live or hosted evidence.                                               |
| SDLC                    | `REQ-WERPC-010`               | `m0004-spec-driven-sdlc-and-document-contracts.md#spec-driven-development-baseline`         | `SRC-WERPC-015`–`SRC-WERPC-016`                                  | `CLM-WERPC-003-02`–`CLM-WERPC-003-03`                                         | `complete-existing`           | NIST SSDF, the ISO lifecycle abstract, and local typed lifecycle contracts already bound SDLC roles without claiming clause-level conformance or effectiveness.                                                                                                       |
| PRD                     | `REQ-WERPC-011`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | N/A — local-only evidence                                        | `CLM-WERPC-003-03`                                                            | `admit-under-sourced-partial` | The typed local PRD contract is verified, but no direct external requirements-engineering source distinguishes product requirements, stakeholders, acceptance evidence, and architecture handoff.                                                                     |
| AD                     | `REQ-WERPC-012`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | N/A — local-only evidence                                        | `CLM-WERPC-003-03`                                                            | `admit-under-sourced-partial` | The typed local AD contract is verified, but no direct external architecture-requirements source distinguishes constraints, quality attributes, interfaces, risks, and decision handoff.                                                                             |
| ADR                     | `REQ-WERPC-013`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | `SRC-WERPC-017`                                                  | `CLM-WERPC-003-03`–`CLM-WERPC-003-04`                                         | `complete-existing`           | AWS ADR guidance and the local profile already cover significant-decision context, consequences, lifecycle, and the boundary between benchmark and workspace policy.                                                                                                  |
| Guide                   | `REQ-WERPC-014`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | `SRC-WERPC-020`                                                  | `CLM-WERPC-003-03`, `CLM-WERPC-003-08`–`CLM-WERPC-003-09`                     | `complete-existing`           | Diátaxis directly sources the how-to distinction and the report maps it to the typed Guide while preserving the unresolved usability and exhaustive-classification boundary.                                                                                          |
| Incident                | `REQ-WERPC-015`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | `SRC-WERPC-018`                                                  | `CLM-WERPC-003-03`, `CLM-WERPC-003-05`                                        | `complete-existing`           | Google SRE incident guidance and the typed local family already distinguish response and recovery evidence from unobserved runtime exercise.                                                                                                                          |
| Postmortem              | `REQ-WERPC-016`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | `SRC-WERPC-018`                                                  | `CLM-WERPC-003-03`, `CLM-WERPC-003-05`                                        | `complete-existing`           | Google SRE learning and action-follow-through guidance plus the local template cover purpose and limits without claiming action closure.                                                                                                                              |
| Policy                  | `REQ-WERPC-017`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | N/A — local-only evidence                                        | `CLM-WERPC-003-03`                                                            | `admit-under-sourced-partial` | The workspace has a typed policy contract, but no direct external source defines normative policy ownership, applicability, exceptions, review, and the separation from executable procedure.                                                                         |
| Release                 | `REQ-WERPC-018`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | `SRC-WERPC-019`                                                  | `CLM-WERPC-003-06`–`CLM-WERPC-003-07`                                         | `admit-under-sourced-partial` | SemVer covers version meaning and the local profile absence is proven, but release approval, provenance, rollout, rollback, and evidence-record purpose remain externally under-sourced.                                                                              |
| Runbook                 | `REQ-WERPC-019`               | `m0004-spec-driven-sdlc-and-document-contracts.md#document-family-contract-matrix`          | N/A — local-only evidence                                        | `CLM-WERPC-003-03`                                                            | `admit-under-sourced-partial` | The typed procedure contract exists, but no direct external operations source defines safe prerequisites, executable steps, verification, rollback, escalation, and evidence capture.                                                                                 |
| Diátaxis                | `REQ-WERPC-020`               | `m0005-documentation-architecture-and-diataxis.md#diátaxis-baseline`                        | `SRC-WERPC-020`                                                  | `CLM-WERPC-003-08`–`CLM-WERPC-003-09`                                         | `complete-existing`           | The official four-mode model, exact local profile mapping, incomplete tutorial and explanation boundary, and taxonomy-change refresh trigger already answer the requested documentation analysis.                                                                     |
| LLM-WIKI                | `REQ-WERPC-021`               | `m0006-llm-wiki-and-knowledge-routing.md#llm-wiki-baseline`                                 | `SRC-WERPC-021`–`SRC-WERPC-022`                                  | `CLM-WERPC-003-10`–`CLM-WERPC-003-13`                                         | `complete-existing`           | llms.txt and MCP Resources are directly sourced, the deterministic local owner map is exact, and publication, search, RAG, retrieval, authorization, and runtime remain explicitly deeper evidence.                                                                   |
| CI/CD                   | `REQ-WERPC-022`               | `m0008-ci-cd-github-actions-and-qa.md#cicd-baseline`                                        | `SRC-WERPC-035`–`SRC-WERPC-044`                                  | `CLM-WERPC-005-01`–`CLM-WERPC-005-02`, `CLM-WERPC-005-06`–`CLM-WERPC-005-10`  | `exclude-deep-evidence`       | Static topology, gating, dependency, artifact, identity, and supply-chain boundaries are sourced; promotion, rollback, hosted execution, environment approval, and deployment outcomes require excluded hosted or live evidence.                                      |
| GitHub Actions          | `REQ-WERPC-023`               | `m0008-ci-cd-github-actions-and-qa.md#github-actions-baseline`                              | `SRC-WERPC-035`–`SRC-WERPC-041`                                  | `CLM-WERPC-005-03`–`CLM-WERPC-005-04`, `CLM-WERPC-005-07`–`CLM-WERPC-005-10`  | `exclude-deep-evidence`       | Workflow syntax, secure use, permissions, pinning, concurrency, artifacts, OIDC, and attestations are sourced; effective settings, tokens, runs, rulesets, secrets, environments, and artifacts require excluded hosted or administrative evidence.                   |
| QA                      | `REQ-WERPC-024`               | `m0008-ci-cd-github-actions-and-qa.md#qa-baseline`                                          | `SRC-WERPC-035`–`SRC-WERPC-044`                                  | `CLM-WERPC-005-05`–`CLM-WERPC-005-06`                                         | `complete-existing`           | The repository already defines formatting, linting, syntax, contract, test, security, result, retry, and formatter-review lanes with explicit static, hosted, browser, and live limits.                                                                               |
| Security                | `REQ-WERPC-025`               | `m0007-kubernetes-infrastructure-and-security.md#security-baseline`                         | `SRC-WERPC-023`–`SRC-WERPC-034`                                  | `CLM-WERPC-004-02`–`CLM-WERPC-004-06`, `CLM-WERPC-004-09`, `CLM-WERPC-004-11` | `admit-under-sourced-partial` | The general control layers and live boundary are complete, but exact workload least privilege, service-account token, immutable revision, Helm provenance, and signed-artifact distinctions need direct question-level primary sources.                               |
| AI-agent systems        | `REQ-WERPC-026`               | `m0009-ai-agents-and-agency-agents.md#ai-agent-systems-baseline`                            | `SRC-WERPC-045`–`SRC-WERPC-046`                                  | `CLM-WERPC-006-01`, `CLM-WERPC-006-03`, `CLM-WERPC-006-05`                    | `exclude-deep-evidence`       | Static roles, admission rules, provider configuration, reviewer, and rollback boundaries are sourced; discovery, permission enforcement, delegation, execution, evaluation quality, and effectiveness require excluded runtime evidence.                              |
| agency-agents           | `REQ-WERPC-027`               | `m0009-ai-agents-and-agency-agents.md#agency-agents-baseline`                               | `SRC-WERPC-047`–`SRC-WERPC-048`                                  | `CLM-WERPC-006-02`–`CLM-WERPC-006-03`                                         | `complete-existing`           | The pinned upstream tree, license, source-level converter and installer comparison, local admission rule, rejected inference, and repeat trigger already answer the catalog-system question.                                                                          |
| Model routing           | `REQ-WERPC-028`               | `m0010-agent-model-routing-and-configuration.md#model-routing-baseline`                     | `SRC-WERPC-045`–`SRC-WERPC-046`, `SRC-WERPC-049`–`SRC-WERPC-050` | `CLM-WERPC-006-04`–`CLM-WERPC-006-05`                                         | `exclude-deep-evidence`       | Static tier, configuration, fitness, promotion, fallback, and provider boundaries are documented; actual resolution, availability, same-suite fitness, cost, latency, canary, and fallback behavior require excluded provider-runtime evidence.                       |
| Short-term memory       | `REQ-WERPC-029`               | `m0011-agent-memory-tiers-and-management.md#short-term-memory-baseline`                     | `SRC-WERPC-049`–`SRC-WERPC-052`                                  | `CLM-WERPC-006-06`                                                            | `complete-existing`           | The atomic redacted advisory checkpoint contract and repository-wins rule already define short-term memory while actual checkpoint and provider-memory use remain bounded.                                                                                            |
| Long-term memory        | `REQ-WERPC-030`               | `m0011-agent-memory-tiers-and-management.md#long-term-memory-baseline`                      | `SRC-WERPC-049`–`SRC-WERPC-052`                                  | `CLM-WERPC-006-07`                                                            | `complete-existing`           | Durable canonical ownership, provenance, review, retention, conflict, and redaction rules are explicit and do not overclaim provider persistence.                                                                                                                     |
| Domain-scoped memory    | `REQ-WERPC-031`               | `m0011-agent-memory-tiers-and-management.md#domain-scoped-memory-baseline`                  | `SRC-WERPC-049`–`SRC-WERPC-052`                                  | `CLM-WERPC-006-07`                                                            | `complete-existing`           | Spec, Runbook, Incident, and Postmortem domain authority and archive routing are already defined with retrieval and provider-integration limits.                                                                                                                      |
| Memory management       | `REQ-WERPC-032`               | `m0011-agent-memory-tiers-and-management.md#memory-management-baseline`                     | `SRC-WERPC-049`–`SRC-WERPC-052`                                  | `CLM-WERPC-006-06`–`CLM-WERPC-006-08`                                         | `exclude-deep-evidence`       | Static lifecycle, redaction, conflict, and auxiliary-store precedence are sourced; provider retention, deletion, compaction, connected-resource behavior, and actual retrieval require excluded provider or connected-runtime evidence.                               |
| verification-validation | N/A — no existing request row | N/A — no independent research owner                                                   | N/A — no independent external source row                         | N/A — no independent claim row                                                | `admit-unresearched`          | The pack uses validation and verification terms but has no independent owner or source-backed matrix distinguishing conformance questions from requirement satisfaction or intended-use questions and their evidence.                                                 |

### Admitted question set

Only these rows authorize WERG-002 or WERG-003 external research. The other 25
rows are duplicate-research stops or deeper-evidence exclusions.

| Requested topic         | Admitted question                                                                                                                                                                               | Next owner                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Kubernetes              | Exact kube-state-metrics Secret metadata RBAC, Adminer hardening and service-account token, and immutable revision/provenance distinctions missing from the existing general platform baseline. | WERG-003 Kubernetes researcher           |
| PRD                     | Externally source product-requirement purpose, actors, acceptance evidence, and architecture handoff without changing the local family.                                                         | WERG-002 documentation researcher        |
| AD                     | Externally source architecture-requirement purpose, quality attributes, constraints, interfaces, risks, and decision handoff.                                                                   | WERG-002 documentation researcher        |
| Policy                  | Externally source normative-policy purpose, ownership, applicability, exceptions, review, and separation from procedure.                                                                        | WERG-002 documentation researcher        |
| Release                 | Externally source release-record purpose beyond SemVer: approval, provenance, rollout, rollback, and evidence boundaries.                                                                       | WERG-002 documentation researcher        |
| Runbook                 | Externally source safe operational-procedure prerequisites, steps, verification, rollback, escalation, and evidence capture.                                                                    | WERG-002 documentation researcher        |
| Security                | Research only the exact workload, token, immutable revision, Helm provenance, and signed-artifact deltas shared with the admitted Kubernetes row.                                               | WERG-003 security researcher             |
| verification-validation | Add a source-backed seven-column Verification/Validation question matrix without redefining repository quality-lane vocabulary.                                                                 | WERG-002 QA and documentation researcher |

### Kubernetes line-level admitted questions

| Candidate subquestion                                                                     | Decision         | Existing direct official source                            | Existing workspace selector                                           | Existing uncertainty boundary                                                         | Existing refresh trigger                                 | Exact reason                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| kube-state-metrics cluster-wide Secret metadata `list/watch` and dependent metric surface | Admit            | Missing for the precise metric and RBAC claim              | `gitops/platform/monitoring/kube-state-metrics.yaml`                  | Present: no effective permission or collected-metric inference                        | Missing for this precise question                        | General RBAC guidance does not establish whether this exact permission is required or which metric surface depends on it.                                                                    |
| Namespace ingress and default-deny semantics                                              | Reject duplicate | `SRC-WERPC-023`                                            | `gitops/platform/network-policies/` and `gitops/platform/namespaces/` | Present: CNI and effective traffic remain `DEFER`                                     | Present: CNI, namespace posture, or policy design change | The report already records egress-only intent, absent default-deny proof, CNI dependency, exact directories, and the live-test boundary.                                                     |
| Adminer Pod Security, pod/container hardening, and service-account token boundary         | Admit            | Missing for the exact workload comparison                  | `gitops/workloads/adminer/rollout.yaml`                               | Present: no admission or runtime behavior inference                                   | Missing for this exact workload question                 | General Pod Security and two monitoring examples do not establish the Adminer selector, token posture, or workload-specific delta.                                                           |
| Immutable Git revision, image digest, Helm provenance, and signed/provenance evidence     | Admit            | Partial: `SRC-WERPC-027`, `SRC-WERPC-032`, `SRC-WERPC-040` | GitOps application and workload image/Helm selectors                  | Present: no artifact validity, signer identity, reconciliation, or registry inference | Partial: general GitOps or supply-chain change only      | Existing sources do not directly separate branch revision immutability, image digest identity, Helm provenance, and signature or attestation verification for the exact workspace selectors. |

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

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: During research implementation, the exact five pack
  owners named by Spec 055; reciprocal Spec/Plan/Task/index/progress evidence;
  and the exact standalone registry row during activation or closure.
- **Forbidden Paths**: `docs/98.archive/**`, Current or retired audit-pack
  member bodies, terminal Spec 053 evidence, GitOps, infrastructure, policy,
  workflow, provider, credential, secret, and runtime configuration unless a
  separate explicit approval names the exact change.
- **Approval Required**: Human execution-mode choice before WERG-000; separate
  human approval before any closure-authority/validator expansion, remote
  action, live action, deletion beyond workflow-owned one-off files, or scope
  expansion outside the exact five research owners.
- **Static Validation**: Admission/source/claim/selector/residue probes;
  strict registry, Markdown profiles, links/owners, RIA, affected/staged
  lanes, relevant tests, aggregate quality gate, plain/all-files pre-commit,
  formatter review, and both diff checks.
- **Live Validation**: `DEFER` — authenticated providers, hosted CI, remote
  repository state, credentials, Kubernetes runtime, CNI enforcement, and
  cluster behavior are explicitly outside this research refresh.
- **Secret / Vault Handling**: Do not read, print, copy, search for, or modify
  secret values. Repository-static secret-reference shapes may be named only
  when an admitted question requires them.
- **Rollback Plan**: Revert only the relevant logical commit in dependency
  order. Do not reset the branch, remove unrelated user work, or weaken a
  fail-closed validator to preserve a claimed result.
- **Evidence Location**: This Task, the reciprocal Plan, durable progress, and
  the five existing WER pack owners; ignored worker reports are supporting
  evidence only.
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
| [VAL-WERG-001](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md#success-criteria--verification-plan) | WERG-001 | [Complete four-state admission matrix and review](tasks/tsk-0002-werg-001.md) |
| N/A — VAL-WERG-002 shares the Spec source above | WERG-004 | [Exact five-owner research path set](tasks/tsk-0005-werg-004.md) |
| N/A — VAL-WERG-003 shares the Spec source above | WERG-002, WERG-003 | [New source rows and source-fidelity reviews](tasks/tsk-0003-werg-002.md) |
| N/A — VAL-WERG-004 shares the Spec source above | WERG-002, WERG-003, WERG-004 | [Claim rows, workspace selector checks, and owner closure](tasks/tsk-0003-werg-002.md) |
| N/A — VAL-WERG-005 shares the Spec source above | WERG-002 | [External terminology plus responsibility/evidence/failure matrix](tasks/tsk-0003-werg-002.md) |
| N/A — VAL-WERG-006 shares the Spec source above | WERG-002 | [Document-family comparison and Spec 052 decision review](tasks/tsk-0003-werg-002.md) |
| N/A — VAL-WERG-007 shares the Spec source above | WERG-003 | [Kubernetes admission, source, duplication, and security review](tasks/tsk-0004-werg-003.md) |
| N/A — VAL-WERG-008 shares the Spec source above | WERG-004, WERG-005 | [Identifier/date/history/protected-surface diff evidence](tasks/tsk-0005-werg-004.md) |
| N/A — VAL-WERG-009 shares the Spec source above | WERG-004 | [One-off residue inventory and cleanup review](tasks/tsk-0005-werg-004.md) |
| N/A — VAL-WERG-010 shares the Spec source above | WERG-000–005 | [Logical commit ledger and canonical validation/review evidence](tasks/tsk-0001-werg-000.md) |

### Related documents

- **Approved Spec**:
  [Spec 0056](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md)
- **Standalone execution decision**:
  [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- **Terminal predecessor design**:
  `docs/03.specs/053-workspace-engineering-research-pack-consolidation/spec.md`
- **Document decision boundary**:
  `docs/03.specs/052-document-taxonomy-consolidation/spec.md`
- **Reciprocal Task**:
  [Task](plan.md)
- **Research owner**:
  [2026-08-08 WER pack](../../90.references/research/0001-workspace-engineering/README.md)

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item                                                                                                 | Result    | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [WERG-000](plan.md#work-breakdown)                              | Completed | Reciprocal active owners and the ADR-0022 standalone relation passed focused review and the exact-index canonical commit gates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [VAL-WERG-001](../../03.specs/0056-workspace-engineering-gap-only-refresh/spec.md#success-criteria--verification-plan) | Completed | The exact 33-row four-state matrix and eight-row admitted set pass the task-local completeness and uniqueness probe plus independent full-pack content and checker-quality review.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| N/A — WERG-002 shares the Plan and Spec sources above                                                                 | Completed | `SRC-WERPC-053`–`059`, `CLM-WERPC-007-01`–`08`, `REQ-WERPC-033`, five document-family mappings, and the seven-column Verification/Validation matrix pass independent content/quality review plus the exact eight-path canonical commit gates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| N/A — WERG-003 shares the Plan and Spec sources above                                                                 | Completed | `SRC-WERPC-060`–`065`, `CLM-WERPC-008-01`–`06`, the dated Kubernetes/Security subsection, and two refreshed README owners contain only the three admitted deltas and pass independent content/security review plus the exact six-path canonical commit gates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| N/A — WERG-004 shares the Plan and Spec sources above                                                                 | Completed | Exact 13/33/65/65 pack, request, source, and claim counts plus five-owner integration/residue closure pass independent review and the exact five-path canonical commit gates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| N/A — WERG-005 shares the Plan and Spec sources above                                                                 | Completed | Whole-branch specification/content, quality, and security reviews, terminal repository-static validation, scratch cleanup, and lifecycle closure completed in `22002d91`; merge commit `79e44638` records the selected branch finish. Hosted, provider-runtime, remote, credential-bearing, and live evidence remains `DEFER`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| N/A — WERG-006 closure re-verification, 2026-08-10                                                                    | Completed | A seven-group disjoint re-verification tested all 33 requested rows against a four-element rule (official source, exact workspace reconciliation, named uncertainty boundary, refresh trigger). Result: 30 rows `covered`; `REQ-WERPC-004`, `REQ-WERPC-006`, and `REQ-WERPC-021` failed workspace reconciliation and were corrected in `b9e16079`; precision items were closed in `25b4a450`. Three limits are recorded honestly: the earlier WERG-005 reviews recorded `Approved` while these three defects were present, so review approval is not evidence of factual reconciliation; the `Spec 055` closure state additionally required registration in `POST_CLOSURE_SPEC_AUTHORITY_PATHS`, without which `validate-active-corpus-residue-closure.py` fails `CLOSURE-AUTHORITY-SCOPE`; and the WERG-002/WERG-003 all-files pre-commit statements were inaccurate, as corrected in the next row. |
| N/A — all-files pre-commit correction, 2026-08-10                                                                     | Corrected | The WERG-002 and WERG-003 evidence paragraphs state that the all-files pre-commit lane passed. Re-running `pre-commit run --all-files` on 2026-08-10 failed `detect-secrets` at `m0012-source-coverage.md:242` and `m0007-kubernetes-infrastructure-and-security.md:276`/`:288`. All three are Kubernetes RBAC prose about Secret objects, hold no credential value, and came from the WERG-003 rows; the commit-time hook did not catch them because it scans only changed files. The three false positives were recorded in `.secrets.baseline` after human approval on 2026-08-10. A before/after comparison confirms no entry, plugin, or custom exclusion pattern was removed. The lane now passes with no hook-induced file mutation.                                                                                                                                                 |
