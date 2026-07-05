---
title: 'SDLC Lifecycle Contract Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-06
---

# SDLC Lifecycle Contract Technical Specification

## Overview

This specification defines the repository contract for SDLC lifecycle routing,
stage handoff, numeric lineage, archive preservation metadata, active-surface
limits, and `_workspace` staging boundaries in `hy-home.k8s`.

The work builds on the existing template and governance system instead of
creating a parallel framework. Stage 01 requirements, Stage 02 architecture,
Stage 03 specs, Stage 04 execution, Stage 05 operations, Stage 98 archive
tombstones, Stage 99 templates, and Stage 00 agent governance must describe the
same lifecycle rules and be validated by repository quality gates.

## Strategic Boundaries & Non-goals

In scope:

- Codify the SDLC flow from `docs/01.requirements/` through
  `docs/04.execution/`, with operations and archive handoff rules where they
  apply.
- Define status transition expectations for PRD, ARD, ADR, Spec, Plan, Task,
  operations, and archive tombstone documents.
- Preserve the existing numeric route contracts for PRDs and specs:
  `docs/01.requirements/<###-Numbering>-<feature-or-system>.md` and
  `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
- Define feature lineage and handoff link expectations across PRD,
  architecture, spec, plan, task, operations, and archive documents.
- Update archive rules so tombstones preserve original path, archive date,
  archive reason, and replacement/current location in frontmatter.
- Treat `docs/01~04` accumulation as an active-surface problem: identical
  active purpose, role, or feature lineage must not have multiple current
  owners.
- Clarify `_workspace` as a temporary, non-secret, repo-support staging
  surface for analysis scratch, dry-run logs, migration ledgers, and generated
  audit work products.
- Add deterministic validation for the lifecycle and archive rules where the
  repository can check them locally.

Out of scope:

- Live Kubernetes, Argo CD, Vault, ESO, GitHub remote, branch protection,
  ruleset, CI provider, credential, or third-party mutation.
- Secret value inspection.
- Rewriting all historical documents unless they are active current-contract
  surfaces or block validation.
- Creating new template families when the existing Stage 99 template support
  contracts already own the rule.
- Changing Stage 04 plans and tasks away from the existing date-based naming
  route.
- Preserving full archived document bodies by default. Tombstones preserve
  traceability metadata; full snapshots require an explicit exception rule.

## Related Inputs

- **PRD**: No dedicated PRD exists for this governance follow-up. The approved
  user request and existing Stage 00/99 contracts are the controlling inputs.
- **ARD**: No new architecture requirement is required because this change
  affects repository documentation governance and validation.
- **Related ADRs**: Not applicable.
- **Template contracts**:
  - `../../99.templates/support/template-routing.md`
  - `../../99.templates/support/frontmatter-schema.md`
  - `../../99.templates/support/sdlc-governance.md`
  - `../../99.templates/support/documentation-contract.md`
  - `../../99.templates/support/common-documentation-governance.md`
  - `../../99.templates/support/legacy-cleanup-rules.md`
- **Stage 00 governance**:
  - `../../00.agent-governance/rules/document-stage-routing.md`
  - `../../00.agent-governance/rules/stage-authoring-matrix.md`
  - `../../00.agent-governance/rules/documentation-protocol.md`
  - `../../00.agent-governance/rules/quality-standards.md`
- **Archive contract**:
  - `../../98.archive/README.md`
  - `../../99.templates/templates/common/archive-tombstone.template.md`
- **Validation owner**: `../../../scripts/validate-repo-quality-gates.sh`
- **External basis**:
  - NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
  - GitHub status checks: https://docs.github.com/articles/about-status-checks
  - GitHub protected branches: https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  - Diataxis: https://diataxis.fr/
  - Google developer documentation style guide: https://developers.google.com/style/

## Contracts

- **Lifecycle Contract**:
  - PRDs move through `draft -> active -> done | archived`.
  - ARDs and ADRs move through `draft -> active -> accepted | archived`.
  - Specs move through `draft -> active -> done | archived`.
  - Plans and tasks move through `draft -> active -> done | archived`.
  - Guides, policies, runbooks, incidents, and postmortems move through
    `draft -> active -> accepted | archived` when they become durable
    operations contracts.
  - Archive tombstones always use `status: archived`.
- **Numbering Contract**:
  - Stage 01 PRDs use `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
  - Stage 03 specs use `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
  - A new numeric identifier is the highest active or archived identifier in
    the same routed family plus one.
  - Related PRD and spec identifiers should match when they describe the same
    feature lineage. If older lineage cannot match because of historical
    numbering, the relationship must be explicit in Related Documents.
  - Stage 04 plan and task documents remain date-based execution records.
- **Handoff Contract**:
  - PRDs link to architecture and specs or explicitly state that no separate
    architecture document is required.
  - Architecture documents link upstream PRDs and downstream specs when they
    exist.
  - Specs link upstream PRD/architecture inputs and downstream plan/task
    evidence.
  - Plans link the spec they execute and the task evidence they expect.
  - Tasks link parent plan/spec and record validation evidence.
  - Operations documents link the spec, task, incident, or policy owner that
    promoted them.
  - Archive tombstones link the original path and replacement/current location.
- **Archive Contract**:
  - Archive frontmatter must include the standard keys plus archive-specific
    traceability keys: `original_path`, `archived_on`, `archive_reason`, and
    `replacement`.
  - Tombstone bodies remain concise metadata records by default.
  - Full original body preservation requires a documented snapshot exception
    and must not make the archive route ambiguous.
- **Active-Surface Contract**:
  - For each stage, only one active document may own a given role, purpose, and
    feature lineage.
  - Superseded, duplicate, obsolete, migrated, or currentness-conflicting
    documents move to archive or are rewritten as historical evidence.
  - The repository should prefer deterministic duplicate and legacy-route
    checks over arbitrary hard count limits.
- **Workspace Staging Contract**:
  - `_workspace` stores temporary, non-secret repo-support artifacts used while
    preparing durable documentation, validation, or migration outputs.
  - Allowed examples include route inventories, generated audit scratch,
    dry-run logs, migration ledgers, and non-secret scan summaries.
  - Prohibited examples include credentials, tokens, auth files, shell history,
    kubeconfigs, cloud auth material, browser profiles, SSH keys, provider
    caches, and secret-bearing diagnostics.
  - Durable decisions are promoted to Stage 03, Stage 04, Stage 90, Stage 00,
    or Stage 99 owners before handoff.

## Core Design

The implementation is a contract overlay with three logical units.

First, update the lifecycle contract surfaces. Stage 99 support documents and
Stage 00 routing rules should use the same status transition table, numbering
rules, handoff link expectations, archive metadata requirement, and
active-surface duplicate policy. README files may point to these owners but
must not duplicate their full governance bodies.

Second, update authored current surfaces that prove the contract. The active
PRD and spec routes are already numeric, so this pass should verify rather
than churn them. The Stage 03 README should include this specification in its
index, and `_workspace/README.md` should continue to state that the directory
is temporary repo-support staging rather than a place for diagnostics, auth
material, or private local history.

Third, update validation. The repository quality gate should reject legacy
date-based PRDs, unnumbered active spec folders, archive tombstones missing
archive traceability keys, README frontmatter, and tracked `_workspace`
artifacts that violate the staging boundary. Where active duplicate lineage
cannot be inferred safely, validation should document the limit and keep the
check to deterministic path, frontmatter, and explicit metadata evidence.

## Data Modeling & Storage Strategy

No runtime storage, database, Kubernetes resource, or external system is
introduced.

The durable state is stored in Git through:

- Stage 03 specifications;
- Stage 04 execution plans and tasks;
- Stage 00 governance rules;
- Stage 99 template support contracts and template forms;
- Stage 98 archive tombstones;
- repository validation scripts.

Archive tombstones use extended frontmatter metadata:

```yaml
title: '<Archived Document Title>'
type: content/archive-tombstone
status: archived
owner: platform
updated: YYYY-MM-DD
original_path: docs/<original-path>.md
archived_on: YYYY-MM-DD
archive_reason: superseded
replacement: docs/<replacement-path>.md
```

The allowed `archive_reason` values should be small and operational:
`superseded`, `duplicate`, `obsolete`, `migrated`, and `historical-baseline`.

## Interfaces & Data Structures

### Core Interfaces

Lifecycle checks are expressed as deterministic repository scans rather than
runtime APIs.

```text
sdlc_document:
  path: routed markdown path
  type: namespaced frontmatter type
  status: lifecycle status
  owner: platform
  updated: ISO date
  lineage_id: optional numeric path prefix
  related_documents: explicit markdown links
```

```text
archive_tombstone:
  path: docs/98.archive/**/*.md
  type: content/archive-tombstone
  status: archived
  original_path: original document path
  archived_on: ISO date
  archive_reason: controlled reason
  replacement: replacement path or none
```

## API Contract

This feature exposes no external API and creates no machine-readable service
contract.

## Agent Role & IO Contract

- **Agent Role**: Repository documentation governance worker.
- **Inputs**: Approved user request, this spec, current Stage 00/99 contracts,
  active authored docs, archive tombstones, validator behavior, and official
  external source principles listed in Related Inputs.
- **Outputs**: Updated lifecycle contracts, adjusted archive/frontmatter
  schema, current document touch-ups, validator checks, and Stage 04 evidence.
- **Success Definition**: The repository describes and validates one coherent
  SDLC lifecycle contract across Stage 00, Stage 01-05, Stage 98, Stage 99,
  `_workspace`, and quality gates.

## Tools & Tool Contract

- Use `rg`, `find`, and existing repository validation scripts for local
  evidence gathering.
- Use `apply_patch` for manual edits.
- Use `git mv` only when route changes require renames.
- Treat networked sources as read-only research inputs unless the user
  explicitly approves an external mutation.
- Do not inspect secret values or normalize private local auth material into
  tracked files.

## Prompt / Policy Contract

AI agents must follow Stage 00 bootstrap, provider rules, and template routing
before editing SDLC documents. If a README section begins to carry the full
lifecycle contract, move that contract body to the owning support/governance
document and keep the README as an entrypoint.

## Memory & Context Strategy

Durable completion evidence belongs in Stage 04 tasks and the Stage 00 progress
memory. Temporary inventories may exist under `_workspace` during execution
only when they are non-secret and task-scoped.

## Guardrails

- Do not mutate live infrastructure, CI provider settings, branch protection,
  secrets, credentials, or external services.
- Do not add another lifecycle contract document when an existing Stage 99 or
  Stage 00 owner can be updated.
- Do not add arbitrary README sections.
- Do not keep duplicate active documents with the same feature lineage and
  purpose.
- Do not preserve full archived bodies by default unless a snapshot exception
  is explicitly documented.

## Evaluation

- **Structural checks**: route, frontmatter, archive metadata, and README
  boundary scans.
- **Contract checks**: Stage 00 and Stage 99 wording describe the same
  lifecycle, numbering, handoff, archive, and `_workspace` rules.
- **Evidence checks**: Stage 04 task record includes commands and pass/fail
  results.
- **Manual review**: inspect touched contract surfaces for stale or conflicting
  descriptions.

## Edge Cases & Error Handling

- **Historical numbering gaps**: Keep gaps. Do not renumber older documents
  just to make a sequence contiguous.
- **Existing PRD/spec mismatch**: Preserve historical IDs and make
  relationship links explicit instead of bulk-renaming completed lineage.
- **Archive replacement unavailable**: Use `replacement: none` and explain the
  current owner in the tombstone body.
- **Ambiguous duplicate purpose**: Record a task finding for human review
  instead of deleting or archiving by guess.
- **Raw `_workspace` file contains possible secret material**: Leave it
  untracked, do not quote its content, and report the boundary issue.

## Failure Modes & Fallback / Human Escalation

- **Validator cannot infer duplicate lineage safely**: Limit validation to
  deterministic route and metadata checks; document duplicate review as a
  manual governance rule.
- **Archive metadata conflicts with current schema**: Update
  `frontmatter-schema.md`, archive template, and validator in the same logical
  unit.
- **Contract surfaces disagree after edits**: Stop, compare Stage 00, Stage 98,
  Stage 99, and validator wording, then repair before final validation.
- **Live validation or external mutation appears necessary**: Escalate to the
  user because this specification is repo-static by design.

## Verification Commands

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
rg -n "YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>|docs/03\\.specs/[a-z][^/]+/spec\\.md" docs/00.agent-governance docs/99.templates docs/01.requirements docs/03.specs scripts
find docs/01.requirements -maxdepth 1 -type f -name '*.md' -print | sort
find docs/03.specs -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort
```

## Success Criteria & Verification Plan

- **VAL-SDLC-LC-001**: Stage 00 and Stage 99 contracts describe the same SDLC
  status transitions, numbering rules, and handoff expectations.
- **VAL-SDLC-LC-002**: Active PRD and spec routes use numeric path contracts;
  no legacy date-based active PRD or unnumbered active spec folder remains.
- **VAL-SDLC-LC-003**: Archive tombstone schema and template require
  `original_path`, `archived_on`, `archive_reason`, and `replacement`.
- **VAL-SDLC-LC-004**: `_workspace` remains a non-secret temporary
  repo-support staging area and is validated accordingly.
- **VAL-SDLC-LC-005**: Repository quality gates pass after documentation,
  template, archive, and validator updates.

## Related Documents

- **PRD**: No dedicated PRD; approved user request controls this follow-up.
- **ARD**: No dedicated ARD; this is a repository documentation governance
  contract update.
- **Related ADRs**: Not applicable.
- **Plan**: `../../04.execution/plans/2026-07-06-sdlc-lifecycle-contract.md`
- **Tasks**: `../../04.execution/tasks/2026-07-06-sdlc-lifecycle-contract.md`
- **Archive Index**: `../../98.archive/README.md`
- **Template Routing**: `../../99.templates/support/template-routing.md`
- **Frontmatter Schema**: `../../99.templates/support/frontmatter-schema.md`
