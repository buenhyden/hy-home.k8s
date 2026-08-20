---
title: 'Workspace Research Full-Corpus Reverification Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-08-20
artifact_id: "SPEC-0062"
---

# Workspace Research Full-Corpus Reverification Technical Specification (Spec)

## Overview

This specification designs a new full-corpus reverification cycle over the
existing [`2026-08-08-wer`](../../90.references/research/2026-08-08-wer/README.md)
research pack. The direct human request enumerates the same topic families that
the pack already projects onto thirty-six `REQ-WERPC-*` owner rows, including
harness and loop engineering, provider integration, the common agent
environment, Spec-driven SDLC, the full development and operations document
families, Diataxis, LLM-WIKI, Kubernetes, infrastructure, delivery, QA,
security, verification and validation, AI agents, model routing, and memory
management.

The repository completed its previous full-corpus observation on 2026-08-17
and corrected one claim on 2026-08-18. This cycle does not replace that record.
It establishes a new observation date of 2026-08-20, checks every external and
workspace evidence class again, preserves prior observations, and records only
the resulting delta. The current pack remains the sole research owner: this
cycle creates no new research folder, topic report, requirement owner, or
parallel source ledger.

The terminal baseline is fourteen Markdown files, thirty-six request-owner
rows, ninety source IDs, and one hundred thirty-five claim IDs. The cycle
deliberately separates public-source currency, repository-static
implementation evidence, and deeper operational evidence. Every owner row is
revisited, including rows whose runtime or human-evidence boundary is already
closed. A new public contract or repository selector may change such a row's
analysis, but a static result does not prove provider runtime, hosted execution,
live-cluster behavior, or user and operator validation.

Direct human approval on 2026-08-20 authorizes the design in this draft Spec.
Execution remains unauthorized until this written Spec and its reciprocal Plan
are separately reviewed and approved. No separate PRD or Architecture
Description is required or part of this standalone lifecycle.

## Strategic Boundaries & Non-goals

### In scope

- Map every human-requested category and sub-area onto the closed set of thirty-six
  `REQ-WERPC-*` owner rows.
- Re-observe the current official or primary external sources for all thirty-six
  rows on 2026-08-20.
- Re-observe the current workspace selectors for all thirty-six rows at the
  execution branch's pinned baseline and terminal revision.
- Record external and workspace results independently, including changed,
  unchanged, unreachable, superseded, contradicted, confirmed, absent, and
  drifted states where applicable.
- Recalculate each row's As-Is state, gap, target, evidence depth, rejected
  inference, deferred boundary, owner, safe follow-up, and refresh trigger.
- Integrate accepted findings as dated H3 sections into the existing eleven
  topical owners and append source and claim records to the existing ledger.
- Re-project the scope application index and reconcile the pack and collection
  indexes after all topic content is final.
- Inspect the repository's configured GitHub Actions and the approved read-only
  remote metadata classes without dispatching, rerunning, approving, merging, or
  changing any remote resource.
- Remove only task-owned one-off artifacts after their final consumer and record
  the cleanup result.
- Use logical-unit commits with per-task review and one whole-branch review.

### Out of scope and non-goals

- Creating a new dated research pack, duplicate topic report, parallel ledger,
  or new `REQ-WERPC-*` owner.
- Renumbering, rewriting, or deleting an existing requirement, source, claim, or
  dated observation.
- Treating external guidance as proof of this workspace's implementation or
  effectiveness.
- Live Kubernetes, Argo CD, Vault, ESO, gateway, registry, infrastructure, or
  recovery inspection.
- Provider authentication, entitlement, discovery, delegated execution, hook
  delivery, model resolution, or native memory retention evidence.
- Workflow dispatch, rerun, approval, merge, environment mutation, ruleset
  mutation, branch-protection mutation, secret access, or credential recovery.
- User, operator, stakeholder, accessibility, or intended-use validation without
  a separately authorized named activity.
- Updating policy, manifests, workflows, runtime configuration, or application
  code merely because research identifies a target state.
- Modifying, restaging, reverting, or incorporating the unrelated RIA changes
  that were already staged in the primary checkout when this cycle began.
- Publishing, pushing, merging, or deleting a branch without the terminal human
  choice required by the finishing workflow.

## Contracts

### C-WRFR-001 — closed thirty-six-row corpus

The request maps to exactly the existing thirty-six `REQ-WERPC-*` owners.
Every row is processed exactly once. A finding outside that set is recorded as
an out-of-ledger observation and cannot create a new owner in this cycle.

### C-WRFR-002 — full-corpus means dual re-observation

Every owner row records an external observation and a workspace observation as
independent fields. One field cannot be inferred from the other, and failure to
obtain one does not erase the evidence obtained for the other.

### C-WRFR-003 — primary-source evidence

Technical claims prefer official documentation, official repositories, and
standards-body publications. Search summaries may locate a source but cannot
substitute for reading it. A material technical claim uses two independent
primary sources when two appropriate sources exist. Public catalogs for paid
standards support edition, status, and public scope only; they do not support
unread clause-level claims.

### C-WRFR-004 — current facts carry a current observation

Version, release, feature, API, permission, and policy facts are checked on
2026-08-20. The record carries the exact URL or repository revision, observed
state, uncertainty, rejected inference, and refresh trigger. Historical source
rows retain their original check dates.

### C-WRFR-005 — unreachable is not unchanged

If an official source cannot be read through the bounded fallback chain, its
result is `unreachable` with the exact failure class. Authentication, rate
limits, or access controls are not bypassed. An unreachable result can preserve
an earlier claim with uncertainty but cannot refresh its observation date.

### C-WRFR-006 — evidence depth is fail-closed

A repository-static or public-documentation `PASS` proves only that evidence
depth. Provider runtime, hosted CI outcome, live infrastructure behavior, and
human judgement remain `DEFER` unless this cycle contains separately authorized
evidence of the required class. The prior blocking-class closure is cited, not
silently promoted or repeatedly presented as a new failure.

### C-WRFR-007 — append into the existing owners

Accepted findings are appended under `### 2026-08-20 full-corpus
reverification` in the existing topical documents. Existing body text, dates,
IDs, and claims remain byte-preserved unless a separately identified mechanical
cross-link or count projection requires correction. A factual contradiction is
recorded as an additive correction rather than destructive history rewriting.

### C-WRFR-008 — single allocator and integration writer

Research subagents are read-only evidence producers. They do not edit repository
files, allocate identifiers, stage, or commit. The orchestrating implementation
task is the sole allocator of new `SRC-WERPC-*` and `CLM-WERPC-*` identifiers and
the sole writer for shared ledgers and indexes.

### C-WRFR-009 — source and claim continuity

New source identifiers continue at `SRC-WERPC-091` without a duplicate, gap,
reservation, or renumbering. New claims use the cycle block
`CLM-WERPC-013-NN`, starting at `01` and remaining contiguous within that
block. A re-observed existing source receives a new source record only when the
new observation is material to the cycle's claim or freshness boundary.

### C-WRFR-010 — remote GitHub observation is read-only

Any remote GitHub query must be allowlisted in the Plan, target the approved
repository and branch, project only sanitized metadata, and execute at most once
per approved evidence class unless the Plan defines a reviewed fail-closed
recovery. Raw bodies, logs, tokens, secret-bearing fields, workflow mutation,
dispatch, rerun, approval, merge, and configuration changes are prohibited.

### C-WRFR-011 — one-off artifact ownership

Temporary artifacts are created only in the plan-specific ignored workspace or
an exact approved `/tmp` path. Before creation, the path must be absent and not a
symlink. While retained, it must be a current-user regular file with restrictive
permissions. Only artifacts created by this cycle may be removed, and each is
removed after its final consumer with an exact absence check.

### C-WRFR-012 — isolated execution

Spec authoring and implementation occur in an isolated branch and linked
worktree based on the clean tracked `HEAD`. The primary checkout's staged RIA
changes are outside this cycle and remain untouched.

### C-WRFR-013 — logical commits and review gates

Lifecycle activation, baseline admission, the five research workstreams,
ledger and scope integration, cross-link reconciliation, and terminal closure
are separate logical units. Each implementation unit receives a spec-compliance
and quality review before its successor, followed by one whole-branch review.

## Core Design

The cycle uses one closed topic ledger, five research workstreams, and one
central integration path.

| Workstream | Owner rows | Research surface |
| --- | --- | --- |
| Agent engineering | 001, 002, 026–032 | Harness, loop, agents, agency-agents, model routing, memory tiers and management |
| Provider and common environment | 003–006 | Workspace application, shared rules, Claude, Codex |
| SDLC and documentation | 007, 010–021, 034–036 | Spec-driven development, document families, Diataxis, LLM-WIKI |
| Platform and security | 008, 009, 025 | Kubernetes, infrastructure, GitOps, identity, admission, supply chain, security |
| Delivery and quality | 022–024, 033 | CI/CD, GitHub Actions, QA, verification, validation |

Each workstream receives a pinned ledger slice and returns structured evidence;
it does not write. The central integrator validates that the union of returned
rows is exactly the thirty-six-row corpus, assigns identifiers, appends dated
sections, then updates shared projections in terminal order.

The data path is:

1. freeze the terminal owner, source, claim, status, and blocking-class baseline;
2. re-observe external sources;
3. re-observe exact workspace selectors;
4. classify external and workspace outcomes independently;
5. derive the current As-Is, gap, target, evidence depth, and follow-up boundary;
6. review the workstream evidence;
7. allocate source and claim identifiers centrally;
8. append topic findings and ledger rows;
9. re-project scopes and indexes;
10. reconcile links, counts, lifecycle state, and durable progress;
11. run the terminal validation and whole-branch review.

Unchanged rows use a concise observation record instead of duplicating the
existing analysis. Changed, superseded, or contradicted rows carry the detailed
source comparison and workspace impact.

## Data Modeling & Storage Strategy

The existing pack remains the persistence boundary. No database, schema file,
or parallel report store is introduced.

### Reverification row

Each of the thirty-six owner rows carries:

- request ID and canonical topical owner;
- external result and exact checked-on date;
- external source identities and observed revision or version;
- workspace result and exact commit or tree identity;
- workspace selectors and current observed state;
- As-Is, gap, and bounded target;
- adopted claim and rejected inference;
- evidence depth and final disposition;
- blocking class, missing evidence, safe follow-up, owner, and refresh trigger.

### Source row

Each new `SRC-WERPC-*` row carries owner topic, primary URL or exact repository
revision, source class, check date, adopted scope, rejected scope, uncertainty,
and refresh trigger.

### Claim row

Each new `CLM-WERPC-*` row carries the request owner, claim, supporting source
IDs and workspace selectors, evidence depth, final disposition, missing
evidence, safe boundary, and refresh trigger.

### Out-of-ledger observation

An observation outside the thirty-six owners carries a description, evidence,
reason it is outside the ledger, candidate canonical owner, and follow-up
boundary. It receives neither a new request ID nor an implementation mandate.

## Interfaces & Data Structures

### Research subagent input

| Field | Contract |
| --- | --- |
| Workstream | One of the five closed workstreams |
| Request IDs | Exact ordered owner subset |
| Baseline | Pinned pack and workspace commit |
| Source policy | Primary-source and bounded-fallback rules |
| Write authority | None |
| Forbidden evidence | Secrets, live mutation, remote mutation, unapproved runtime evidence |

### Research subagent output

The output uses the following ordered conceptual schema:

`REQ ID -> external sources -> current external contract -> workspace selectors
-> As-Is -> Gap -> Target -> application rules -> evidence depth -> rejected
inference -> DEFER or exclusion -> owner -> safe follow-up -> refresh trigger`.

Every requested ID must appear once, even when the result is unchanged or
unreachable. The output is rejected if an ID is missing, duplicated, outside the
assigned subset, or carries a final source or claim identifier.

### Integration order

The central integration order is topical documents, source and claim ledger,
scope application index, pack README, collection README, lifecycle documents,
and durable progress. Counts and cross-links are reconciled only after the
content and ledger are final.

## Edge Cases & Error Handling

An official page that redirects to a new official owner is `superseded`, not
unchanged. Both the previous and current identities remain in the record.

An official page that is temporarily unavailable follows a bounded chain:
official index, official versioned repository or release, then one official
mirror or catalog when applicable. Failure after that chain is `unreachable`.

Two primary sources that disagree produce an uncertainty record. The cycle
adopts neither interpretation beyond the common supported claim and names the
condition that would resolve the conflict.

A workspace selector that moved is updated only after repository-wide ownership
search proves the successor. A missing selector with no successor is `absent` or
`drifted`, not silently removed from evidence.

A changed external source with unchanged local implementation is still a
meaningful delta. A changed local selector with unchanged external guidance is
also a meaningful delta. Neither automatically changes the final disposition.

A static result for a structurally unreachable row records the refreshed public
and repository facts while retaining the blocking class. Repeating the prior
runtime absence is not represented as newly discovered evidence.

If a proposed source or claim duplicates an existing ledger record, the
integrator reuses the existing ID and records only the new observation where the
freshness contract requires it.

If any research result would require a policy, manifest, workflow, or runtime
change, the finding is routed to the canonical owner or a later approved Spec.
It is not implemented in this cycle.

## Failure Modes & Fallback / Human Escalation

Stop and escalate before any destructive action, credential-bearing access,
remote mutation, push, merge, publication, or plan defect that makes all paths
forward guesses.

If a source is blocked by authentication, authorization, rate limiting, or a
paid standard boundary, record the accessible evidence and the limitation. Do
not circumvent the boundary or substitute an unverified summary.

If a remote GitHub projection rejects a response, retain the sanitized guarded
artifact, record the exact failure, and stop that evidence class. Do not retry a
query or inspect raw output unless a reviewed Plan amendment authorizes a
fail-closed recovery.

If the isolated worktree baseline fails canonical validation, stop before
authoring research and ask whether to investigate the baseline or proceed with
a recorded limitation.

If a workstream review finds a Critical or Important defect, fix and re-review
within the bounded task loop. A finding cannot be hidden by proceeding to the
next integration unit.

If one-off cleanup would affect an unknown, foreign-owned, staged, or untracked
artifact outside this cycle's inventory, leave it untouched and report it.

## Verification Commands

The Plan must instantiate exact path lists and task-local closed-corpus checks.
The terminal repository-static lane includes at least:

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --root . --require-settled-baselines
bash scripts/validate-repo-quality-gates.sh .
pre-commit run
pre-commit run --all-files
git diff --check
git diff --cached --check
```

The Plan additionally names exact domain validators for agent governance,
provider configuration, loop lifecycle, checkpoint semantics, GitHub Actions,
CI Python locks, affected surfaces, Kubernetes manifests, GitOps structure,
Vault and ESO contracts, security scanning, active-corpus boundaries, and the
research pack's 36-row/source/claim/cross-link invariants.

No command result is treated as provider-runtime, hosted-CI, live-cluster,
deployment, user, or stakeholder evidence unless a separate authorization
explicitly admits that evidence class.

## Success Criteria & Verification Plan

| ID | Criterion |
| --- | --- |
| VAL-WRFR-001 | Exactly 36 unique request rows are processed with no gap or extra owner |
| VAL-WRFR-002 | Every row has independent external and workspace observation records dated or pinned to the cycle baseline |
| VAL-WRFR-003 | Every human-requested category and sub-area maps to at least one canonical owner row |
| VAL-WRFR-004 | Current technical claims use reviewed primary sources with uncertainty and rejected inference recorded |
| VAL-WRFR-005 | Every workspace claim cites existing exact selectors and an explicit evidence depth |
| VAL-WRFR-006 | Changed, unchanged, unreachable, superseded, and contradicted outcomes are distinguished fail-closed |
| VAL-WRFR-007 | All retained Partial and DEFER boundaries name the blocking class, missing evidence, owner, safe follow-up, and trigger |
| VAL-WRFR-008 | Findings are appended to existing owners; no new research folder, duplicate report, or requirement owner exists |
| VAL-WRFR-009 | New sources start at `SRC-WERPC-091`; new claims start at `CLM-WERPC-013-01`; both sequences are unique, contiguous, and fully referenced |
| VAL-WRFR-010 | Pack, ledger, scope index, collection index, lifecycle, and durable progress projections agree |
| VAL-WRFR-011 | GitHub remote evidence is sanitized, read-only, allowlisted, and mutation-free |
| VAL-WRFR-012 | Task-owned one-off artifacts are absent after their last consumer; foreign artifacts and staged RIA changes are untouched |
| VAL-WRFR-013 | Each logical work unit has a commit, task review, and reproducible validation evidence |
| VAL-WRFR-014 | A whole-branch review reports no unresolved Critical or Important finding before completion |
| VAL-WRFR-015 | Canonical affected, staged, pre-commit, all-files, aggregate, formatter-review, and diff-check lanes pass on the terminal tree |

## Traceability

This Spec has no PRD or Architecture Description. Its authority is the direct
human approval recorded in `## Overview`. The predecessor full-corpus research
cycle is [Spec 0059](../0059-workspace-research-full-corpus-refresh/spec.md),
whose append-in-place, dual-evidence, blocking-class, and cleanup boundaries are
retained and strengthened here.

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — standalone, direct approval | VAL-WRFR-001 | Closed-corpus checker proves exact IDs 001 through 036 |
| N/A — standalone, direct approval | VAL-WRFR-002 | Per-row dual-observation schema and completeness check |
| N/A — standalone, direct approval | VAL-WRFR-003 | Human-request-to-owner coverage matrix comparison |
| N/A — standalone, direct approval | VAL-WRFR-004 | Independent source-fidelity reviews and ledger validation |
| N/A — standalone, direct approval | VAL-WRFR-005 | Exact-selector existence and evidence-depth checks |
| N/A — standalone, direct approval | VAL-WRFR-006 | Closed outcome vocabulary and mutation fixtures |
| N/A — standalone, direct approval | VAL-WRFR-007 | Blocking-class and follow-up completeness checks |
| N/A — standalone, direct approval | VAL-WRFR-008 | Pack inventory and duplicate-owner checks |
| N/A — standalone, direct approval | VAL-WRFR-009 | Source and claim identity continuity checks |
| N/A — standalone, direct approval | VAL-WRFR-010 | Registry, profile, RIA, link, count, and scope reconciliation |
| N/A — standalone, direct approval | VAL-WRFR-011 | Reviewed allowlist, sanitized schema, and remote mutation absence |
| N/A — standalone, direct approval | VAL-WRFR-012 | Exact temporary-artifact inventory and absence checks |
| N/A — standalone, direct approval | VAL-WRFR-013 | Task reviews and logical commit log |
| N/A — standalone, direct approval | VAL-WRFR-014 | Whole-branch review package and final reviewer verdict |
| N/A — standalone, direct approval | VAL-WRFR-015 | Terminal canonical validation sequence recorded in the Task |

### Related Documents

- [Spec 0059 — Workspace Research Full-Corpus Refresh](../0059-workspace-research-full-corpus-refresh/spec.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [Research collection contract](../../90.references/research/README.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
