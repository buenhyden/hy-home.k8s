---
title: 'Template Path Numbering Contract Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-13
---

# Template Path Numbering Contract Technical Specification

## Overview

This specification defines the approved design for normalizing SDLC template
routing for Stage 01 product requirements and Stage 03 specifications. It
converts active PRD filenames from date-based names to stable numeric names
and aligns template forms, support contracts, governance references, README
indexes, and validation logic around the same route contract.

The implementation must keep template forms separate from support contracts:
template files stay under `docs/99.templates/templates/**`, while routing,
frontmatter, governance, cleanup, and validation rules stay under
`docs/99.templates/support/**` and the owning Stage 00 or validator surfaces.

## Strategic Boundaries & Non-goals

This specification owns the route design and validation boundary for the
numbered PRD and numbered Stage 03 spec contracts.

In scope:

- Rename the four active PRD files in `docs/01.requirements/` from
  `YYYY-MM-DD-<feature-or-system>.md` to
  `<###-Numbering>-<feature-or-system>.md`.
- Update the PRD route contract to
  `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
- Update the Stage 03 route contract to
  `docs/03.specs/<###-Numbering>-<feature-id>/spec.md` and apply the same
  numbered feature-folder placeholder to helper documents and native contracts.
- Keep actual Stage 03 folder names as they already exist, such as
  `004-argo-rollouts-progressive-delivery/`.
- Update cross-links, examples, support contracts, Stage README files, and
  validators in the same logical unit.

Out of scope:

- Renumbering Stage 02 architecture requirements or decisions.
- Renaming Stage 04 plans or tasks, which remain date-based execution records.
- Rewriting authored document content beyond links, path examples, currentness
  notes, and template-contract residue required by the new route.
- Creating duplicate PRD aliases or compatibility copies.
- Changing live infrastructure, provider runtime configuration, GitOps desired
  state, secrets, credentials, CI semantics, or external services.

## Contracts

- **Path Contract**:
  - PRDs use `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
  - Stage 03 specs use
    `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
  - Stage 03 helper docs and native contracts use the same numbered feature
    folder.
  - Stage 04 plans and tasks remain date-based.
- **Governance Contract**:
  - Template forms remain in `docs/99.templates/templates/**`.
  - Route, frontmatter, governance, cleanup, and validation rules remain in
    `docs/99.templates/support/**`, Stage 00 governance, and validators.
  - README files remain entrypoints and indexes; they do not own the complete
    route contract.
- **Evidence Contract**:
  - Each implementation commit records focused validation evidence.
  - Historical path literals may remain only when clearly historical and not
    advertised as current route contracts.

## Core Design

Existing PRDs will be renamed in historical and current README order:

| Old path | New path |
| --- | --- |
| `docs/01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md` | `docs/01.requirements/001-argo-rollouts-progressive-delivery.md` |
| `docs/01.requirements/2026-05-17-argo-notifications-slack.md` | `docs/01.requirements/002-argo-notifications-slack.md` |
| `docs/01.requirements/2026-06-01-workspace-agent-governance-platform.md` | `docs/01.requirements/003-workspace-agent-governance-platform.md` |
| `docs/01.requirements/2026-06-02-current-local-gitops-platform.md` | `docs/01.requirements/004-current-local-gitops-platform.md` |

The two PRDs created on `2026-05-17` follow the current
`docs/01.requirements/README.md` index order: Rollouts first, Notifications
second.

The new structural route patterns are:

| Role | Target Pattern | Template |
| --- | --- | --- |
| Product requirement | `docs/01.requirements/<###-Numbering>-<feature-or-system>.md` | `docs/99.templates/templates/sdlc/requirements/prd.template.md` |
| Technical specification | `docs/03.specs/<###-Numbering>-<feature-id>/spec.md` | `docs/99.templates/templates/sdlc/specs/spec.template.md` |
| API contract doc | `docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md` | `docs/99.templates/templates/sdlc/specs/api-spec.template.md` |
| Agent design | `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md` | `docs/99.templates/templates/sdlc/specs/agent-design.template.md` |
| Data model | `docs/03.specs/<###-Numbering>-<feature-id>/data-model.md` | `docs/99.templates/templates/sdlc/specs/data-model.template.md` |
| Test design | `docs/03.specs/<###-Numbering>-<feature-id>/tests.md` | `docs/99.templates/templates/sdlc/specs/tests.template.md` |
| OpenAPI contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml` | `docs/99.templates/templates/sdlc/specs/openapi.template.yaml` |
| GraphQL contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql` | `docs/99.templates/templates/sdlc/specs/schema.template.graphql` |
| Protobuf contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto` | `docs/99.templates/templates/sdlc/specs/service.template.proto` |

## Data Modeling & Storage Strategy

This work changes documentation paths and route contracts only. It does not
introduce runtime data models, persistence schemas, migrations, or storage
changes.

Path state is stored in Git history through renames, README indexes, support
contracts, validator mappings, and cross-links. No compatibility alias files
will be created.

## Interfaces & Data Structures

### Core Interfaces

The route map is the main interface between authored documents, templates, and
validation:

```text
authored document path -> template route -> frontmatter profile -> required headings
```

The implementation plan should update these surfaces together:

- `docs/99.templates/templates/sdlc/requirements/prd.template.md`
- `docs/99.templates/templates/sdlc/specs/*.template.md`
- `docs/99.templates/templates/sdlc/specs/openapi.template.yaml`
- `docs/99.templates/templates/sdlc/specs/schema.template.graphql`
- `docs/99.templates/templates/sdlc/specs/service.template.proto`
- `docs/99.templates/templates/sdlc/architecture/*.template.md`
- `docs/99.templates/templates/sdlc/execution/*.template.md`
- `docs/99.templates/templates/sdlc/operations/*.template.md`
- `docs/99.templates/templates/common/reference.template.md`
- `docs/99.templates/README.md`
- `docs/99.templates/support/sdlc-governance.md`
- `docs/99.templates/support/template-routing.md`
- `docs/99.templates/support/frontmatter-schema.md` if route notes mention old
  path forms
- `docs/01.requirements/README.md`
- `docs/03.specs/README.md`
- `docs/00.agent-governance/rules/document-stage-routing.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `scripts/validate-repo-quality-gates.sh`
- Any authored Markdown link that points to the old PRD filenames or the old
  unnumbered Stage 03 placeholder.

#### API Contract

No external API is introduced. The API-related route contract is limited to
the feature-local documentation path:
`docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md`.

#### Agent Role & IO Contract

Agents working on this implementation must treat repository files as the source
of truth, avoid live runtime mutation, preserve historical evidence boundaries,
and run explicit validation before handoff.

Inputs:

- This specification.
- Current template support contracts.
- Current Stage 01 and Stage 03 README indexes.
- Validator output.

Outputs:

- Renamed PRD files.
- Updated route contracts and cross-links.
- Validation evidence and logical commits.

#### Tools & Tool Contract

- `git mv` should be used for PRD renames.
- `apply_patch` should be used for manual file edits.
- `rg` should be used for stale path and contract scans.
- `bash scripts/validate-repo-quality-gates.sh .` is the repository quality
  gate.
- No tool may inspect secret values or mutate live infrastructure.

#### Prompt / Policy Contract

Implementation agents must keep the route contract precise and avoid adding
new README sections unless the README already owns an index or navigation
summary. Durable rules belong in support contracts or Stage 00 governance.

#### Memory & Context Strategy

Reusable lessons should be recorded in
`docs/00.agent-governance/memory/progress.md` only after implementation
evidence exists. The memory entry should note that Stage 01 PRDs and Stage 03
specs use numeric identity, while Stage 04 execution records remain date-based.

#### Guardrails

- Do not create duplicate compatibility files for old PRD paths.
- Do not rewrite historical execution evidence unless a path is an active link
  or current route claim.
- Do not promote old date-based PRD routes as current contract.
- Do not rename Stage 04 plans or tasks.
- Do not mutate live infrastructure, credentials, secrets, provider runtime
  configuration, or external services.

#### Evaluation

Evaluation is repository-static:

- Structural route mapping equality between `docs/99.templates/README.md`,
  `docs/99.templates/support/template-routing.md`, and
  `scripts/validate-repo-quality-gates.sh`.
- Absence of active links to the four old date-based PRD filenames.
- Absence of active contract text that advertises the old PRD or unnumbered
  Stage 03 route patterns as current.
- Repository quality gate pass.

## Edge Cases & Error Handling

- **Same-date PRDs**: use current README order as the deterministic tie-breaker.
- **Historical path evidence**: leave old paths only when clearly historical
  and not used as current route guidance.
- **Validator conflict**: update the validator in the same logical unit as the
  support contract.
- **Broken links after rename**: fix active links before committing the rename
  unit.

## Failure Modes & Fallback / Human Escalation

- **Validation fails because the route is uncovered**: update the support
  contract and validator mapping together, then rerun validation.
- **Validation fails because historical evidence contains old paths**: classify
  the match as historical evidence or update the active-link wording.
- **A PRD number conflict appears**: stop and ask for the desired numbering.
- **A requested change would affect live or protected surfaces**: stop and
  request explicit approval.

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/01\\.requirements/YYYY-MM-DD-<feature-or-system>|docs/03\\.specs/<feature-id>" docs/99.templates docs/00.agent-governance scripts docs/01.requirements docs/03.specs
rg -n "2026-05-17-argo-rollouts-progressive-delivery|2026-05-17-argo-notifications-slack|2026-06-01-workspace-agent-governance-platform|2026-06-02-current-local-gitops-platform" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

The second `rg` command should return only intentional historical evidence or
no matches after active links are updated.

## Success Criteria & Verification Plan

- **VAL-SPC-019-001**: Every non-README Markdown file under
  `docs/01.requirements/` matches exactly one PRD structural template route.
- **VAL-SPC-019-002**: Every non-README Markdown spec helper under
  `docs/03.specs/*/` matches the numbered feature-folder route.
- **VAL-SPC-019-003**: Template README mapping and
  `support/template-routing.md` remain identical.
- **VAL-SPC-019-004**: `scripts/validate-repo-quality-gates.sh` normalizes the
  new placeholders: `<###-Numbering>-<feature-or-system>` and
  `<###-Numbering>-<feature-id>`.
- **VAL-SPC-019-005**: Active Markdown links do not point to the old four
  date-based PRD paths.
- **VAL-SPC-019-006**: Active contract text does not advertise
  `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` or
  `docs/03.specs/<feature-id>/spec.md` as the current route.
- **VAL-SPC-019-007**: `git diff --check` passes.
- **VAL-SPC-019-008**: `bash scripts/validate-repo-quality-gates.sh .` passes.

## Traceability

- **Templates README**: [../../99.templates/README.md](../../99.templates/README.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **SDLC Template Governance**: [../../99.templates/support/sdlc-governance.md](../../99.templates/support/sdlc-governance.md)
- **Template Documentation Contract**: [../../99.templates/support/documentation-contract.md](../../99.templates/support/documentation-contract.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Document Stage Routing Rules**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
- **Diataxis**: <https://diataxis.fr/>
- **Google Developer Documentation Style Guide**: <https://developers.google.com/style>
- **GitHub Docs Best Practices**: <https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs>
- **NIST SSDF SP 800-218**: <https://csrc.nist.gov/pubs/sp/800/218/final>
- **Plan**: [../../04.execution/plans/2026-07-05-template-path-numbering-contract.md](../../04.execution/plans/2026-07-05-template-path-numbering-contract.md)
- **Task**: [../../04.execution/tasks/2026-07-05-template-path-numbering-contract.md](../../04.execution/tasks/2026-07-05-template-path-numbering-contract.md)
### Related inputs

- **User request**: Normalize `docs/99.templates/**`, update PRD and Stage 03
  route contracts, rename the existing four PRDs to numeric filenames, update
  cross-links, and commit by logical unit.
- **Current PRD stage**: `docs/01.requirements/README.md` and the four active
  date-based PRD files.
- **Current Stage 03 structure**: `docs/03.specs/README.md` and existing
  numbered spec folders.
- **Template support contracts**:
  `docs/99.templates/support/documentation-contract.md`,
  `docs/99.templates/support/sdlc-governance.md`,
  `docs/99.templates/support/template-routing.md`, and
  `docs/99.templates/support/frontmatter-schema.md`.
- **Validator**: `scripts/validate-repo-quality-gates.sh`.
- **External basis**: Diataxis, Google developer documentation style guidance,
  GitHub Docs writing guidance, and NIST SSDF.
