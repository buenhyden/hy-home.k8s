---
title: "Local QA and SemVer Release Ownership"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-10-07"
layer: "architecture"
artifact_id: "ADR-0048"
---

# ADR-0048: Local QA and SemVer Release Ownership

## Overview

Record the user-requested design for local quality validation and explicit
SemVer releases in the public `hy-home.k8s` repository.
[SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) owns the change
contract and its Task owns implementation and observed evidence. This proposed
decision establishes no completed migration, release publication, Project
activation, authenticated remote setting or native hook delivery.

The change is a scoped amendment to the delivery and CI-projection boundaries
of [ADR-0031](0031-current-corpus-retention-and-validation-ownership.md) and
[ADR-0036](0036-common-knowledge-and-prompt-surfaces.md). Their remaining owner,
document and approval contracts continue to apply. It does not supersede their
whole documents or rewrite their accepted text.

## Context

The previous delivery model combined local editing and index checks with
hosted QA and per-main-push SHA tags. Hosted full QA was later removed, leaving
its `NOT_RUN` evidence, an isolated hosted check and now-obsolete job
projections. A tag-triggered changelog artifact does not provide committed
release history. Small document edits also select broad checks whose
implementation-regression purpose differs from content conformance.

The request owner now selects local QA, removal of obsolete or duplicate
execution after coverage transfer, and one SemVer tag/Release producer with
main release notes prepared through a PR. Working exact-index isolation,
bounded execution and sound result reuse should survive that change. General
Archive integrity must remain distinct from proof that a past cutover once
completed. The repository's actual purpose is GitOps desired state, bootstrap
assets and external-service interfaces; other workspaces do not become test
targets merely because the same general request names them.

## Decision

### One local validation graph

The existing validation registry owns local gate identity, argv, affected
selection and profiles. Quality policy owns evidence classes, budgets, reuse
and delivery meaning; each validator owns its independent failure rule.
Checks cover document forms, templates, frontmatter, relations, links and
lifecycle, plus contracts for the repository's actual platform and tooling
surfaces. Reusable regression tests demonstrate those admitted contracts;
Spec or Task identities and past inventory counts are not recurring success
criteria.

Ordinary document edits select content conformance. A validator or shared
implementation change selects its meaningful named behavioral, Archive and
security regressions and affected purpose gates. The later user-directed
retirement removes the long local full/ci sweep and blanket unit discovery
from completion, including global QA-contract changes. An explicit audit
selects bounded named checks for its actual purpose and input rather than
reinstating the sweep. Required tools, execution time, output limits and
native execution approval are resolved before implementation.

Editing uses focused and affected checks. Logical commits validate the exact
index, required lint and format on that final index immediately before commit,
and the actual Commitizen message. Push is transport, and integration or
postmerge checks refresh only evidence whose input changed. A successful leaf
is reused only for identical declared bytes, configuration, tool identity,
scope, mode, trust and relevant base/history. Path equality alone is
insufficient. Parsing and Git reads may be shared within one run without
creating another state owner or weakening failure diagnostics.

The hosted `ci-summary` job owns branch metadata validation and its
branch-policy verdict. Missing metadata, an invalid PR base or source branch,
or an unexpected event/ref fails closed; PR branch policy is not applicable
on main. A separate hosted PR style check may run the same declared style
rules against its distinct merge SHA/run; it does not inherit local PASS.
Historical hosted full, unit and document-content QA stay `NOT_RUN` when
unexecuted and do not become current completion gates when the metadata
summary or style check succeeds. Deployment style
evidence requires an actual deployment workflow and run. Actual remote
required checks remain an observed external boundary.

### Coverage transfer before retirement

Retire proven one-off, legacy, deprecated, duplicate, conflicting and
excessive execution by transferring each unique ongoing rule, removing its
caller and registration, then removing dedicated helpers, fixtures and tests.
Keep necessary results in the existing Task or historical evidence owner.
Do not create a replacement inventory ledger or a new test suite tied to this
Spec's identifiers.

Recurring Archive checks retain safe-path, integrity and source-recovery
contracts. A fixed migration census or cutover completion proof is historical
evidence unless a distinct current consumer requires it. Historical readers
needed to interpret retained material are not removed merely because their
input is old. Frozen records and prior failures or `NOT_RUN` results are not
rewritten.

### Retain evaluation evidence without recurring grading

The ownership clarification dated 2026-09-09 in
[ADR-0036](0036-common-knowledge-and-prompt-surfaces.md) records the evaluation
corpus and runner ownership observed at that time. Its root-level corpus and
standalone grading runner are historical predecessors, not current execution
owners. SPEC-0107 retires that fixed corpus, runner and recurring registration;
this decision transfers the continuing evidence responsibility to
`.agents/evaluations/` and its form responsibility to Stage 99. ADR-0036 remains
unchanged as decision history, and its dated clarification does not reactivate
the retired grading path.

Keep `.agents/evaluations/` as the evidence domain for actual comparisons of
the same task without and with a Skill. Harness task definitions, paired raw
outputs and scores remain distinct; `results.md` alone owns representative
aggregate scores, status, reviewer and date. Stage 99 owns their bounded
profiles and canonical forms, and the local templates router links to that
single form owner. Raw outputs are preserved as observations without format
rewrites; existing secret and safe-path controls still apply.

The common Skill index retains membership authority and common governance
retains evaluation procedure and stop conditions. Only actual evaluation
cycles update the outputs, scores and aggregate, with granularity, trial count,
signals, grader and criterion IDs, partial-score reasons and human calibration
recorded in the score. A representative aggregate requires its task, complete
paired outputs and score. Missing observations remain gaps, and changed
contracts require current criteria and distinct new evidence.

Retire the fixed synthetic grading runner and its recurring QA registration
after consumer disposition while retaining this evidence capacity. Existing
document gates check the authored profiles, links and relationships; they do
not grade outputs, validate scoring accuracy or establish full Skill coverage.
Supplied Skill contracts are reference inputs until separately admitted by
their current owners. Synthetic comparisons establish no native automatic
selection, actual command execution, authorization or runtime enforcement.

### One release producer and compatibility contract

Retain Commitizen as the authored message contract through `.cz.toml` and
`.gitmessage`, with explicitly bounded generated-message exceptions. The
local `scripts/release.py` surface is the sole SemVer tag and GitHub Release
producer. It prepares main release notes in `CHANGELOG.md` on a
release-preparation branch for a main-targeted PR. Development pushes do not
publish versions or generate a competing changelog owner.

Publication binds one reviewed main commit, strict SemVer value, committed
changelog content and Release/tag identity. It refuses a nonmain source or
conflicting existing tag, never moves tags and never repeats QA as part of
publishing. Required assets are attached to the draft before publication, so
the sequence supports immutable Releases without claiming that the remote
setting is enabled. Existing `main-<full SHA>` refs stay historical and are
not moved or republished.

The public compatibility contract consists of supported CLI commands and
options, machine JSON schemas, governed document profiles and frontmatter,
GitOps desired state and external-service interfaces. For released 1.0-or-later
contracts, incompatible changes raise major, compatible additions raise minor
and compatible corrections raise patch. The operator chooses the initial 0.y
version and compatibility promise from reviewed release scope; Git history
does not authorize an arbitrary first release. The release identifies the
repository contract rather than certifying deployment or runtime acceptance.

### Work and publication evidence

Issues own requests and priorities, Specs own acceptance contracts, Tasks own
execution and actual evidence, and Projects display work. One-way metadata
and links connect these owners; complete Spec/Task copies and bidirectional
status overwrites are excluded. Remote field updates and Release publication
remain actual external operations with their applicable authority and evidence.

## Explicit Non-goals

This decision does not change live Kubernetes, Argo CD, Vault, cloud or external
service state, provider trust or credentials. It does not rewrite completed
Tasks, accepted predecessor decisions, frozen Archive bodies or existing tags.
It does not create a Release document family, a parallel QA registry or a
permanent progress ledger. It does not assert that local success satisfies
unobserved remote protection, nor weaken an observed native restriction.

## Consequences

Each delivery stage has an explicit responsibility, and small edits avoid
unrelated regression discovery. Release history has one committed owner and
one publisher. Preserved input identity and ongoing integrity contracts keep
the reduction reviewable and reversible through ordinary forward corrections.

Evaluation records remain reviewable without making every development change
run a synthetic grader. Maintainers must arrange actual paired trials and
scoring when an evaluation is needed; document conformance alone cannot show
that a Skill improves results or replace human calibration.

The repository gives up independent hosted full, unit and document-content QA
and per-push hosted attestation; hosted PR style remains a distinct final
defense for its own input.
Maintainers must provide local tools and retain meaningful local evidence.
Affected selection and reuse require accurate dependencies; a mistake can
omit a necessary check, so changes to that graph need focused refusal cases,
named unit regressions and the affected purpose gates. Release
publication still depends on authenticated remote state, and any existing
server-required checks need an explicitly observed transition.

## Alternatives

- Keep local and hosted full QA at every delivery stage. This preserves an
  independent hosted observation but retains repeated work and conflicts with
  the selected local execution model.
- Remove failing or slow checks without transferring their unique rules.
  This reduces runtime but loses ongoing protection and obscures actual
  failures; consumer and coverage disposition are required instead.
- Run one full local suite for every edit and commit. This is simpler to
  select but makes routine document work depend on unrelated regressions and
  repeats the same successful leaves.
- Remove the whole evaluation evidence domain with its obsolete grader. This
  reduces maintained surfaces but loses the requested comparison and review
  capacity. Retain the evidence domain and its forms without recurring grading.
- Retain separate per-push SHA-tag and release producers. This preserves the
  old publication path but splits release identity and changelog ownership.
- Synchronize Issue, Spec, Task and Project bodies and statuses both ways.
  This provides editable copies but makes the authoritative execution state
  ambiguous and adds reconciliation machinery without a distinct owner.

## Traceability

The decision applies the single-owner and retirement requirements
REQ-0003-FR-0001, REQ-0003-FR-0016, REQ-0003-FR-0024 and REQ-0003-FR-0030;
the delivery and evidence requirements REQ-0003-FR-0005, REQ-0003-FR-0017,
REQ-0003-FR-0018, REQ-0003-FR-0026 and REQ-0003-NFR-0002; the Archive boundary
REQ-0003-FR-0027; release requirement REQ-0003-FR-0029; paired evaluation
requirement REQ-0003-FR-0031; and consumer migration
REQ-0003-IF-0001 in [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md).
[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) carries
the structural view. SPEC-0107 owns behavior, acceptance and implementation;
its Task alone records commands and actual results.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0031](0031-current-corpus-retention-and-validation-ownership.md) | Scoped amendment: local QA selection and delivery replace the CI-projection obligation; the single validation registry and remaining ownership contracts continue | [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
| [ADR-0036](0036-common-knowledge-and-prompt-surfaces.md) | Scoped amendment: local validation and explicit release ownership; common governance and provider boundaries continue | [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
| [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) | Updated structural view; no whole-document supersession | [SPEC-0107](../../03.specs/0107-local-qa-and-release/spec.md) |
