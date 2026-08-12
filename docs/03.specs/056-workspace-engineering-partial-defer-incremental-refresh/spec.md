---
title: 'Workspace Engineering Partial/DEFER Incremental Research Refresh Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-08-12
---

# Workspace Engineering Partial/DEFER Incremental Research Refresh Technical Specification (Spec)

## Overview

This specification designs a closed-ledger incremental refresh of the existing
[`2026-08-08-wer`](../../90.references/research/2026-08-08-wer/README.md)
research pack. It targets unresolved `Partial` and explicitly qualified
`DEFER` evidence without repeating the completed broad research owned by
[Spec 053](../053-workspace-engineering-research-pack-consolidation/spec.md)
or the completed gap-only refresh owned by
[Spec 055](../055-workspace-engineering-gap-only-refresh/spec.md).

The human requester selected the closed Gap Ledger approach on 2026-08-11 and
approved read-only inspection of GitHub Actions and repository settings for
`buenhyden/hy-home.k8s`. Public official sources, current repository-static
evidence, and bounded GitHub remote metadata are admissible. Authenticated
provider execution, credential or secret values, live Kubernetes or
infrastructure state, and remote mutation remain outside the evidence
boundary.

No new research pack or parallel topic report is created. Accepted findings
are appended as dated incremental sections to the existing canonical reports,
then reconciled through the pack README, source/claim ledger, and scope index.

Direct human approval on 2026-08-12 authorizes this standalone execution relation.
No separate PRD or ARD is required or part of this standalone lifecycle.
The same approval authorizes this design and its reciprocal
[Plan](../../04.execution/plans/2026-08-11-workspace-engineering-partial-defer-incremental-refresh.md)
and
[Task](../../04.execution/tasks/2026-08-11-workspace-engineering-partial-defer-incremental-refresh.md).
The active direct-approval standalone execution relation is governed by
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md);
no separate PRD or ARD program authority is asserted.

## Strategic Boundaries & Non-goals

### Authorized scope

- Start with the twelve request rows whose base status is `Partial`:
  `REQ-WERPC-006`, `008`, `009`, `014`, `020`, `022`, `023`, `025`,
  `026`, `028`, `032`, and `033`.
- Admit a `Verified` row with a `DEFER` qualifier only when a changed official
  source or permitted GitHub remote observation could materially change the
  recorded result. Do not reopen all qualified rows by default.
- Reconcile every admitted external claim with an exact repository path or
  selector and record `As-Is`, evidence gap, bounded target, required follow-up
  evidence, and refresh trigger.
- Inspect GitHub workflow inventory, recent run metadata, rulesets or branch
  protection, required checks, Actions permissions, environments, OIDC, and
  artifact metadata only through read-only commands that do not expose secret
  or variable values.
- Use official or primary sources first. Preserve source context, edition,
  checked date, uncertainty, adopted scope, and rejected inference.
- Integrate results into existing `2026-08-08-wer` owners as 2026-08-11 dated
  sections and update only the shared README, source/claim ledger, and scope
  index projections required by accepted findings.
- Use disjoint research workstreams, independent review, deterministic
  repository-static validation, and one logical commit per work unit.

### Protected surfaces and non-goals

- Do not create a new dated research folder, add a duplicate report, or
  recreate a predecessor pack.
- Do not re-research an existing `Verified` result merely because its prose
  names a runtime or live `DEFER` boundary.
- Do not modify GitHub settings, rerun a workflow, push, create a pull request,
  or read secret or variable values.
- Do not authenticate to Claude, Codex, a Kubernetes cluster, infrastructure
  provider, Vault, ESO, registry, artifact store, or other live service for
  this research.
- Do not treat a GitHub API `404`, permission denial, redaction, or missing
  response field as proof that a feature or control is absent.
- Do not convert research recommendations into implementation changes to
  workflows, GitOps, RBAC, policies, providers, models, or memory contracts.
- Do not modify `docs/98.archive/**`, protected Current or retired audit-pack
  bodies, RIA baselines, or unrelated user work.
- Do not retain downloaded pages, raw API responses, extracted JSON, or other
  one-off evidence files in the tracked tree.

## Contracts

### C-PDRR-001 — closed admission ledger

Before external refresh work, every candidate receives exactly one admission
state: `admit-public-source-refresh`, `admit-github-remote-read`,
`retain-defer-evidence-unavailable`, or `exclude-duplicate`. The twelve base
`Partial` rows are mandatory candidates. A qualified `Verified` row may enter
only with an explicit material-change reason. Topics absent from the ledger
cannot gain new source, claim, or report content.

### C-PDRR-002 — evidence-state closure

Every admitted candidate terminates as `Verified`, `Partial`, `DEFER`, or
`Contradicted`. A retained `Partial` or `DEFER` result names the unavailable
evidence, follow-up owner or authority, safe collection boundary, and refresh
trigger. A static or remote metadata PASS cannot establish provider-runtime,
stakeholder, credential-bearing, cluster, or live effectiveness.

### C-PDRR-003 — source and claim provenance

Every new source has a unique ID, primary URL, checked date, source status,
adopted scope, rejected inference, and refresh trigger. Every new claim has a
unique ID, supporting source IDs, exact workspace paths or selectors,
uncertainty, and evidence depth. Existing IDs are never renumbered or silently
rewritten.

### C-PDRR-004 — GitHub remote read boundary

GitHub inspection is limited to read-only metadata for
`buenhyden/hy-home.k8s`: workflow definitions and identities, recent run
status, rulesets or branch protection, required checks, Actions permissions,
environment names and protection metadata, OIDC configuration metadata, and
artifact identity or retention metadata. Commands that mutate remote state or
return secret or variable values are forbidden. Access failures remain
`UNPROVEN` and map to `Partial` or `DEFER`, never to `ABSENT`.

### C-PDRR-005 — existing-pack integration

Accepted findings are appended to their existing canonical report under a
dated 2026-08-11 subsection. The pack README, source/claim ledger, and scope
application index are updated atomically with the final owner projections. No
new research folder or duplicate report is permitted.

### C-PDRR-006 — logical work units and cleanup

Design, execution contracts, admission, each disjoint research workstream,
integration, review fixes, and lifecycle closure are separate non-empty logical
commits. Workflow-owned temporary files live only under exact `/tmp` paths,
are content-bounded and non-secret, and are deleted with an explicit absence
check before terminal validation.

## Core Design

The refresh uses five bounded components.

1. **Gap Ledger Controller** freezes the candidate set, baseline status,
   unresolved question, allowed evidence, forbidden evidence, canonical owner,
   and admission decision. It rejects an unknown request ID or unapproved topic.
2. **Research Workstreams** independently cover agent/provider/model/memory;
   Kubernetes/infrastructure/security; documentation/Diátaxis/Guide; and
   CI/CD/GitHub Actions/QA/Verification and Validation. Each workstream uses
   official sources and only its named report owners.
3. **GitHub Remote Reader** records exact read-only queries, collection time,
   repository identity, response class, non-secret identifiers, and
   limitations. It emits no mutation and stores no raw response in the tree.
4. **Workspace Reconciler** maps each accepted claim to exact local evidence
   and produces `As-Is -> Gap -> bounded Target -> follow-up evidence` records.
   It cannot promote a recommendation into implementation authority.
5. **Integration and Review Gate** appends dated sections, reconciles shared
   projections, runs deterministic checks, and requires content, quality, and
   security approval before closure.

The control flow is:

`candidate freeze -> admission -> source/remote observation -> workspace
reconciliation -> status closure -> existing-owner integration -> validation
and independent review -> logical commit and cleanup`.

Research workstreams may gather evidence concurrently, but a single integration
owner serializes shared README, ledger, and scope-index edits. No two workers
edit the same canonical report.

## Data Modeling & Storage Strategy

The task-local Gap Ledger uses one row per candidate with the fields:

| Field | Meaning |
| --- | --- |
| Request ID | Existing `REQ-WERPC-*` identity |
| Baseline status | Current base status and bounded qualifier |
| Unresolved question | Exact externally answerable gap |
| Admission state | One closed `C-PDRR-001` value |
| Material-change reason | Required for a qualified `Verified` row |
| Canonical owner | Existing report and heading |
| Workspace selectors | Exact current local evidence targets |
| Allowed evidence | Official public or permitted GitHub metadata |
| Forbidden evidence | Provider, credential, secret, cluster, or live scope |
| Final disposition | `Verified`, `Partial`, `DEFER`, or `Contradicted` |
| Follow-up evidence | Missing proof and responsible authority |
| Refresh trigger | Date, release, setting change, or evidence availability |

GitHub remote observations use a separate task-local record:

| Field | Meaning |
| --- | --- |
| Repository | Exact `buenhyden/hy-home.k8s` identity |
| Query | Redacted, read-only command or API route |
| Collected at | UTC timestamp |
| Evidence class | workflow, run, ruleset, permission, environment, OIDC, artifact |
| Result | observed, redacted, forbidden, unavailable, or error |
| Non-secret identity | Name, ID, SHA, status, conclusion, or policy metadata |
| Limitation | Missing permission, retention window, API ambiguity, or other bound |

Durable findings remain in the existing Markdown reports and source/claim
ledger. Raw pages, API payloads, and scratch transforms are ephemeral. Only
source-backed summaries, identifiers, and bounded observations are committed.

## Interfaces & Data Structures

The admission interface consumes the current README request matrix and emits a
closed candidate ledger. It must preserve all request IDs and reject duplicate,
missing, or unexpected candidates.

The research interface consumes a candidate row and emits:

- zero or more source records;
- zero or more claim records;
- one workspace reconciliation record;
- one final disposition; and
- one explicit reason when no new source or claim is admitted.

The GitHub reader may use only commands equivalent to:

```bash
gh repo view buenhyden/hy-home.k8s --json nameWithOwner,defaultBranchRef
gh workflow list --repo buenhyden/hy-home.k8s --all
gh run list --repo buenhyden/hy-home.k8s --limit 20 --json databaseId,workflowName,headSha,status,conclusion,createdAt,updatedAt,event
gh api repos/buenhyden/hy-home.k8s/actions/permissions
gh api repos/buenhyden/hy-home.k8s/actions/permissions/workflow
gh api repos/buenhyden/hy-home.k8s/rulesets
gh api repos/buenhyden/hy-home.k8s/branches/main/protection
```

An execution Plan may add other read-only GitHub routes only when it proves
that they cannot return secret or variable values. Endpoints for Actions
secrets, Dependabot secrets, Codespaces secrets, environment secrets,
repository variables, dispatch, rerun, approval, deployment, or mutation are
forbidden.

The integration interface writes only existing report owners plus README,
source/claim ledger, and scope index. It preserves older dated sections and
uses new IDs after the current maximum.

## Edge Cases & Error Handling

- A source changed after collection: preserve the observed date and revision;
  refresh only when the named trigger fires.
- An official page is rate-limited or unavailable: use an official upstream
  source when available, record the fallback and limitation, otherwise retain
  `Partial` or `DEFER`.
- GitHub returns `404` or `403`: classify the observation as unavailable or
  permission-limited. Do not infer that the feature is disabled or absent.
- GitHub returns redacted fields: store only the redaction state and public
  metadata; never attempt an alternate endpoint that exposes a value.
- A recent workflow run failed: record the observed status and failure stage
  only when the API exposes it. Do not infer a root cause without direct logs
  and an admitted evidence boundary.
- A claim has no exact workspace selector: it cannot be integrated and remains
  `Partial` or `DEFER` with the missing owner recorded.
- A candidate duplicates existing sufficient evidence: use
  `exclude-duplicate`; do not add a new source or claim row.
- A result implies an implementation change: record a bounded target and route
  it to a future approved Spec; do not edit the implementation in this work.
- A temporary file survives its work unit: terminal validation fails until the
  exact owned path is removed and absence is proven.

## Failure Modes & Fallback / Human Escalation

- Stop before research if the candidate ledger is not closed, unique, and
  reviewed.
- Stop a workstream if an official source conflicts with an approved workspace
  contract and record the conflict for human disposition; do not choose policy
  by inference.
- Stop GitHub inspection if a command could expose a secret or variable value,
  requires mutation, or targets a repository other than the approved one.
- Stop integration if a worker touches an unowned report, an archive or RIA
  protected surface, or changes an existing source/claim identity.
- If remote access is unavailable, complete public-source and local-static
  research and retain the affected remote questions as `DEFER` with the exact
  failed query class. Do not weaken the completion criteria.
- Roll back only the failing logical commit in dependency order. Never reset the
  branch, overwrite unrelated work, or weaken a validator to preserve a claim.
- Escalate a disputed evidence interpretation, scope expansion, remote mutation,
  implementation change, or live validation request to the human before action.

## Verification Commands

The execution Plan must define a task-local deterministic checker for the
candidate set, source/claim additions, workspace selectors, remote evidence
redaction, final dispositions, and temporary-file absence. It must include
positive and negative self-tests before using the checker on production files.

Canonical repository-static validation includes:

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-reference-information-architecture.py --self-test
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
git diff --cached --check
```

GitHub remote commands are read-only and produce redacted summaries rather
than tracked raw payloads. Their success proves only metadata observed at the
recorded time. Their failure proves only that the query was unavailable.

## Success Criteria & Verification Plan

| Criterion | Success condition | Verification evidence |
| --- | --- | --- |
| VAL-PDRR-001 | The mandatory twelve `Partial` rows and every conditionally admitted qualified row form one closed, unique ledger. | Checker self-test, exact production candidate count, independent admission review |
| VAL-PDRR-002 | Every candidate has one admission state and one final disposition with a refresh trigger. | Ledger schema and negative mutation checks |
| VAL-PDRR-003 | Every new source and claim has complete provenance and no existing ID is renumbered or rewritten. | Before/after ledger comparison, ID uniqueness and field checks |
| VAL-PDRR-004 | Every accepted claim maps to exact workspace evidence and a bounded target without implementation mutation. | Selector existence checks, scoped diff review |
| VAL-PDRR-005 | GitHub inspection is read-only, repository-bounded, non-secret, timestamped, and limitation-aware. | Command allowlist, redaction inspection, security review |
| VAL-PDRR-006 | Existing reports receive dated incremental sections and no new research pack or duplicate report appears. | Exact path allowlist, README owner mapping, residue check |
| VAL-PDRR-007 | `Partial` and `DEFER` retention names the missing evidence, authority, safe boundary, and follow-up trigger. | Content contract and independent review |
| VAL-PDRR-008 | Shared README, source/claim ledger, and scope index agree with all final owner projections and counts. | Integration checker and strict links/owners validation |
| VAL-PDRR-009 | One-off files are absent and protected archive/RIA/audit surfaces remain unchanged. | Exact absence and protected-diff checks |
| VAL-PDRR-010 | Focused, affected, staged, aggregate, all-files, formatter, diff, and independent review gates pass before closure. | Task evidence with exact commands, results, and review verdicts |

## Traceability

This draft is a research-only design requested directly by the human. It does
not create a PRD or ARD, activate an execution Plan, or authorize external
research until the written Spec is separately approved. After approval, a
reciprocal Plan and Task may be authored under the repository's standalone
execution rules.

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — direct human request for a closed Partial/DEFER candidate ledger | VAL-PDRR-001 | Candidate-set checker and independent admission review |
| N/A — direct human request for explicit status closure | VAL-PDRR-002 | Ledger schema and mutation tests |
| N/A — direct human request for official-source provenance | VAL-PDRR-003 | Source/claim ledger comparison and uniqueness checks |
| N/A — direct human request for workspace reconciliation | VAL-PDRR-004 | Exact selector and scoped-diff review |
| N/A — direct human approval for read-only GitHub Actions/settings inspection | VAL-PDRR-005 | Command allowlist, redaction check, and security review |
| N/A — direct human request to integrate into the existing pack | VAL-PDRR-006 | Exact path and duplicate-owner checks |
| N/A — direct human request to retain explicit evidence boundaries | VAL-PDRR-007 | Content contract and independent review |
| N/A — direct human request for updated references and cross-links | VAL-PDRR-008 | Integration and strict link validation |
| N/A — direct human request for one-off cleanup and protected-surface safety | VAL-PDRR-009 | Absence and protected-diff checks |
| N/A — direct human request for logical commits and terminal verification | VAL-PDRR-010 | Task evidence, full gates, and closure review |
