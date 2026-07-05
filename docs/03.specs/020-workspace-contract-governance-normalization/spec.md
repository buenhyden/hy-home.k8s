---
title: 'Workspace Contract Governance Normalization Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-05
---

# Workspace Contract Governance Normalization Technical Specification

## Overview

This specification defines a staged documentation and governance normalization
contract for `hy-home.k8s`. It covers the repository-wide authored document
surface, template and frontmatter contracts, Stage 00 governance, CI/QA
documentation, protected surfaces, and the `_workspace` directory boundary.

The work has two linked goals. First, define `_workspace` as an isolated
repo-support staging surface for temporary analysis data, dry-run logs,
migration ledgers, and generated audit scratch that are safe to keep inside
the repository tree. Second, use that boundary to run a repository-wide
frontmatter, section, template, contract, governance, and validation drift
audit, then remediate only current-contract violations that are clearly
supported by existing templates and governance.

The design follows the existing repository pattern: specifications live under
Stage 03, execution plans and task evidence live under Stage 04, reusable
template rules live under `docs/99.templates/support/**`, agent execution rules
live under Stage 00, and validators enforce the documented contracts.

## Strategic Boundaries & Non-goals

In scope:

- Define the role, allowed contents, prohibited contents, lifecycle, and
  cleanup expectations for `_workspace`.
- Align `_workspace` with Stage 00 protected-surface rules, template support
  contracts, README inventory expectations, and repository quality gates.
- Audit the target repository surfaces listed by the user for:
  - frontmatter key order and allowed key/value sets;
  - namespaced `type` values and document-type profiles;
  - duplicate or conflicting sections;
  - template residue and legacy key/section/value patterns;
  - README scope violations where entrypoints carry full governance bodies;
  - stale CI/CD, QA, formatting, linting, syntax-check, workflow, and
    automation descriptions;
  - current-route and cross-link drift after recent Stage 01 and Stage 03
    route normalization.
- Apply targeted remediation where the owning contract is clear.
- Record audit evidence and final validation in Stage 04 task evidence and the
  canonical progress ledger.

Out of scope:

- Live Kubernetes, Argo CD, Vault, ESO, cloud, GitHub remote, credential,
  provider runtime, or third-party mutation.
- Secret value inspection.
- Broad prose rewrites that are not required by template, governance,
  validator, or current-route contracts.
- Creating another template family or another route table when an existing
  support contract already owns the rule.
- Promoting `_workspace` into a place for personal diagnostics, shell history,
  token caches, auth files, or secret-bearing local logs.
- Merging, pushing, or opening a pull request without explicit user approval.

## Related Inputs

- **User request**: Normalize repository-wide document type, frontmatter,
  template, contract, governance, README, CI/CD, QA, formatting, linting, and
  `_workspace` role boundaries across the listed repository surfaces.
- **PRD**: No dedicated PRD exists for this repository governance
  normalization. The approved user request and current Stage 00/99 contracts
  are the controlling inputs.
- **ARD**: No new architecture requirement is required because this is a
  documentation and validation governance change.
- **Related ADRs**: Not applicable.
- **Template contracts**:
  - `../../99.templates/support/documentation-contract.md`
  - `../../99.templates/support/frontmatter-schema.md`
  - `../../99.templates/support/template-routing.md`
  - `../../99.templates/support/sdlc-governance.md`
  - `../../99.templates/support/common-documentation-governance.md`
  - `../../99.templates/support/legacy-cleanup-rules.md`
- **Stage 00 governance**:
  - `../../00.agent-governance/rules/document-stage-routing.md`
  - `../../00.agent-governance/rules/documentation-protocol.md`
  - `../../00.agent-governance/rules/stage-authoring-matrix.md`
  - `../../00.agent-governance/rules/approval-boundaries.md`
  - `../../00.agent-governance/rules/quality-standards.md`
- **Validation owner**: `../../../scripts/validate-repo-quality-gates.sh`
- **External basis**:
  - Diataxis: https://diataxis.fr/
  - Google developer documentation style guide: https://developers.google.com/style
  - GitHub Docs contributing model: https://docs.github.com/contributing
  - NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final

## Contracts

- **Workspace Staging Contract**:
  - `_workspace` is a repository-local support staging area for temporary,
    non-secret, task-scoped analysis artifacts.
  - Allowed examples include generated audit scratch, dry-run logs, migration
    ledgers, route inventories, non-secret scan summaries, and disposable
    evidence used to prepare Stage 04 task records.
  - Prohibited examples include credentials, tokens, auth files, shell history,
    personal diagnostics, secret-bearing local logs, kubeconfigs, cloud auth
    material, browser profiles, SSH keys, and provider cache files.
  - Durable decisions must move out of `_workspace` into the canonical owner:
    Stage 03 specs, Stage 04 plans/tasks, Stage 90 references/audits, Stage 00
    governance, or template support docs.
- **Documentation Contract**:
  - README files remain entrypoints and indexes. They may summarize ownership
    and route readers to canonical contracts, but they must not accumulate full
    governance bodies.
  - Template forms remain under `docs/99.templates/templates/**`; reusable
    rules remain under `docs/99.templates/support/**`.
  - Stage 00 owns agent execution policy, protected-surface rules, provider
    behavior, approval boundaries, and governance routing.
  - Authored documents must contain topic-specific content and must not retain
    copied template instructions or generic placeholder sections.
- **Frontmatter Contract**:
  - Markdown authored documents must use only the key set allowed by their
    frontmatter profile.
  - Required key order is `title`, `type`, `status`, `owner`, `updated` unless
    the active schema explicitly defines an exception.
  - README files, GitHub-native Markdown control files, and native OpenAPI,
    GraphQL, and protobuf contracts remain frontmatter-free.
- **Governance Contract**:
  - Contract changes must update the owning support document, Stage 00 rule,
    validator, README index, and authored document references in the same
    logical unit when those surfaces would otherwise drift.
  - Historical evidence may preserve old facts only when clearly labeled as
    historical, migration, superseded, or baseline evidence.
- **Security Contract**:
  - The work follows NIST SSDF's principle of adding secure-development
    practices into SDLC governance by making secret handling, approval
    boundaries, protected surfaces, and validation explicit.
  - The repository must never normalize secret-bearing local artifacts into
    tracked documentation or `_workspace` staging.

## Core Design

The implementation plan should use a contract-first phased migration.

Phase 1 creates the design and plan. It writes this Stage 03 specification and
a Stage 04 plan that breaks the work into logical commits.

Phase 2 establishes the `_workspace` contract. The implementation should add
or update the smallest durable owner surfaces needed to define:

- purpose and ownership;
- allowed staging artifacts;
- prohibited local, credential, token, auth, shell-history, and diagnostic
  artifacts;
- retention and cleanup expectations;
- where durable outputs must be promoted;
- validation checks that can deterministically catch forbidden tracked files.

Phase 3 records an audit inventory. The implementation should scan the user
listed targets for document profiles, frontmatter, sections, template residue,
legacy keys, README governance duplication, CI/CD and QA wording, formatting
and linting references, validator coverage, and cross-link drift. Audit
evidence belongs in a Stage 04 task record or a Stage 90 audit report when the
finding set is large.

Phase 4 applies targeted remediation. Remediation should prioritize current
contract violations with a clear owner:

- invalid frontmatter key order or values;
- active docs with stale type values;
- README sections that duplicate governance bodies;
- template residue in authored documents;
- stale route examples or old Stage 01/03 route forms;
- CI/CD, QA, formatting, linting, or syntax-check claims that contradict
  current scripts or workflows;
- `_workspace` guidance that conflicts with protected-surface or secret
  handling rules.

Phase 5 closes validation and memory. Final evidence should include route and
legacy scans, repository quality gates, task closure, and a progress memory
entry that future agents can reuse.

## Data Modeling & Storage Strategy

No runtime data model, persistence schema, database, Kubernetes resource, or
external storage is introduced.

The work stores state in Git through:

- Stage 03 spec and Stage 04 plan/task evidence;
- template support contract updates;
- Stage 00 governance updates;
- README index updates;
- validator logic and deterministic scans;
- optional Stage 90 audit reports when the drift inventory is too large for a
  task record;
- `_workspace` staging artifacts only when they are non-secret, temporary, and
  useful for task execution.

Transition rules:

- Temporary `_workspace` artifacts must either be deleted before final closure
  or promoted into a canonical stage document when they become durable.
- Audit data that contains no secrets but is useful for future work should be
  summarized in Stage 04 evidence or Stage 90 audits rather than kept as raw
  scratch indefinitely.
- Any artifact that might contain credentials, tokens, auth material, shell
  history, or secret-bearing diagnostics must remain untracked and outside the
  `_workspace` contract.

## Interfaces & Data Structures

### Core Interfaces

The main interface is a deterministic audit record that can be represented in
Markdown task evidence or a Stage 90 audit table.

```text
finding_id: DOC-GOV-###
surface: path or path pattern
category: frontmatter | section | template | governance | qa | cicd | workspace | link
current_state: observed condition
expected_contract: owning contract or rule
severity: critical | important | minor
action: remediate | document | defer
owner_surface: canonical document or script
validation: command or manual check
```

The `_workspace` contract exposes this operational interface:

```text
artifact_path: _workspace/<task-or-date>/<artifact>
allowed_class: audit-scratch | dry-run-log | migration-ledger | route-inventory
promotion_target: Stage 04 task | Stage 90 audit | Stage 00 governance | delete
secret_risk: none | unknown | prohibited
retention: delete-before-close | promote-before-close | documented-exception
```

## API Contract (If Applicable)

No external API is introduced.

- **API Spec**: Not applicable.
- **Policy**: API and machine-readable contracts remain feature-local under
  `docs/03.specs/<###-Numbering>-<feature-id>/` when a future feature exposes
  one.
- **Machine-readable Contract**: Not applicable.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Agents inspect repository files, draft specs/plans/tasks,
  run deterministic scans, update documented contracts, and record evidence.
- **Inputs**:
  - User-approved scope and constraints.
  - Stage 00 governance.
  - Template support contracts.
  - Existing authored documents and active control surfaces.
  - Official external documentation references.
- **Outputs**:
  - Stage 03 spec.
  - Stage 04 plan and task evidence.
  - `_workspace` contract and related validation.
  - Targeted document, governance, template, README, and validator updates.
  - Progress memory entry.
- **Success Definition**:
  - Repository contracts explain `_workspace` unambiguously.
  - Current frontmatter, section, template, governance, CI/CD, QA, and
    cross-link drift is either remediated or recorded with a clear deferral.
  - Repository quality gates pass.

## Tools & Tool Contract (If Applicable)

- **Tool List**:
  - `rg`, `find`, `sed`, `git diff --check`, `git status`, `git log`.
  - `bash scripts/validate-repo-quality-gates.sh .`.
  - `git mv` when moving tracked files.
  - `apply_patch` for manual file edits.
- **Permission Boundary**:
  - Network access may be used for official documentation references.
  - No live runtime, secret, GitHub remote mutation, provider credential, push,
    merge, PR, or external service action is in scope without explicit user
    approval.
- **Failure Handling**:
  - If validation fails, fix the smallest owning contract or document surface.
  - If a finding is ambiguous, record it in the audit evidence instead of
    rewriting broad prose.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
  - Follow the repository's Stage 00 bootstrap, documentation protocol,
    template routing, and quality standards.
  - Use repo-native Stage 03 and Stage 04 paths; do not create
    `docs/superpowers/**`.
- **Policy Constraints**:
  - Preserve user changes and never revert unrelated work.
  - Use logical commits.
  - Keep Stage 03 specs, Stage 04 plans, and Stage 04 task evidence
    English-first.
- **Versioning Rule**:
  - Contract changes must include an `updated: 2026-07-05` frontmatter update
    only when the touched document owns the changed rule.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
  - Use Stage 04 task evidence for command outputs, scan summaries, and
    implementation status.
  - Use `_workspace` only for temporary non-secret scratch when a scan produces
    bulky intermediate output.
- **Long-term Memory**:
  - Add a concise progress ledger entry under
    `../../00.agent-governance/memory/progress.md` after final validation.
- **Retrieval Boundary**:
  - Future agents should retrieve durable contracts from Stage 00, Stage 99,
    Stage 04 evidence, and Stage 90 audits, not from raw `_workspace` scratch.

## Guardrails (If Applicable)

- **Input Guardrails**:
  - Do not treat generated, local, or ignored files as policy unless they are
    tracked and explicitly routed.
  - Do not inspect secret values.
- **Output Guardrails**:
  - Do not put auth files, tokens, shell history, or secret-bearing diagnostics
    into `_workspace` or tracked docs.
  - Do not add README sections that should be owned by support contracts or
    governance.
  - Do not leave template placeholder content in authored documents.
- **Blocked Conditions**:
  - Validation repeatedly fails because the owning contract is unclear.
  - A potential secret-bearing artifact is discovered.
  - A remediation would require live runtime or external service mutation.
- **Escalation Rule**:
  - Stop and ask for user approval before live actions, remote mutation,
    credential changes, secret inspection, branch integration, or destructive
    cleanup outside approved tracked-document edits.

## Evaluation (If Applicable)

- **Eval Types**:
  - Static repository validation.
  - Focused legacy-route and template-residue scans.
  - Frontmatter profile consistency checks.
  - `_workspace` allowed/prohibited artifact scans.
- **Metrics**:
  - Zero repository quality gate failures.
  - Zero current-route stale examples outside explicit migration evidence.
  - Zero frontmatter profile violations in routed Markdown files.
  - Zero tracked `_workspace` files that match prohibited auth, token, shell
    history, or secret-diagnostic patterns.
- **Datasets / Fixtures**:
  - Existing tracked repository files under the user listed targets.
  - Stage 99 template and support documents.
  - Stage 00 governance documents.
- **How to Run**:
  - Use the verification commands in this specification and the implementation
    plan.

## Edge Cases & Error Handling

- **Empty `_workspace`**: Treat it as an uninitialized staging surface and
  define the contract before adding any durable artifacts.
- **Historical evidence with old route text**: Preserve it only when the
  surrounding prose marks it as historical, baseline, migration, or
  superseded.
- **README with policy detail**: Reduce to an entrypoint summary and link to
  the canonical owner instead of duplicating the policy.
- **Template support date drift**: Update `updated` only for documents whose
  owned rules actually changed.
- **Cloud example snapshots**: Keep them outside active SDLC frontmatter
  migration unless a future approved spec promotes a scoped refresh.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `_workspace` contains or appears to contain credentials,
  token caches, shell history, or secret-bearing diagnostics.
  - **Fallback**: Do not read secret values. Record the path class, stop if
    needed, and ask for user approval before cleanup or deletion.
  - **Human Escalation**: Required.
- **Failure Mode**: Repo-wide remediation becomes too broad for one safe
  commit.
  - **Fallback**: Split by owner surface: `_workspace`, template support,
    Stage 00 governance, active authored docs, validators, and evidence.
  - **Human Escalation**: Required only if scope changes materially.
- **Failure Mode**: Official external guidance conflicts with local contract.
  - **Fallback**: Prefer repo contract for immediate implementation and record
    the external-source gap for a future governance update.
  - **Human Escalation**: Required if the conflict affects security,
    credentials, or protected surfaces.

## Verification Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
find _workspace -maxdepth 4 -type f | sort
rg -n "(token|secret|credential|auth|history|kubeconfig|ssh|password)" _workspace
rg -n "TBD|TODO|\\{Feature Name\\}|\\[Feature Name\\]" docs AGENTS.md CLAUDE.md GEMINI.md README.md DESIGN.md
rg -n "docs/superpowers|docs/api/" docs AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
rg -n "type: (prd|ard|adr|spec|plan|task|guide|policy|runbook|incident|postmortem|reference)$" docs
```

Expected notes:

- The `_workspace` secret-risk scan should return no tracked allowed files. If
  `_workspace` is empty, record PASS with an empty inventory.
- Placeholder scans may find intentional template placeholders under
  `docs/99.templates/templates/**`; classify those separately from authored
  document residue.

## Success Criteria & Verification Plan

- **VAL-SPC-020-001**: `_workspace` has a documented role, allowed artifact
  classes, prohibited artifact classes, retention rules, and promotion targets.
- **VAL-SPC-020-002**: `_workspace` does not contain tracked auth, token,
  shell-history, secret-bearing diagnostic, kubeconfig, SSH, or provider
  credential artifacts.
- **VAL-SPC-020-003**: Frontmatter audit evidence identifies all routed
  Markdown documents with invalid key order, unsupported keys, unsupported
  `type` values, or stale owner/status values.
- **VAL-SPC-020-004**: Template residue and legacy section audit evidence
  distinguishes active contract violations from template files and historical
  evidence.
- **VAL-SPC-020-005**: README files remain entrypoints and indexes, with
  governance bodies routed to Stage 00 or template support owners.
- **VAL-SPC-020-006**: CI/CD, QA, formatting, linting, syntax-check,
  automation, pipeline, and workflow descriptions point to current local
  scripts, GitHub workflow owners, or explicitly documented deferred gaps.
- **VAL-SPC-020-007**: Route and cross-link scans reflect the numbered Stage
  01 PRD and Stage 03 feature-folder contracts.
- **VAL-SPC-020-008**: `git diff --check` passes.
- **VAL-SPC-020-009**: `bash scripts/validate-repo-quality-gates.sh .` passes.
- **VAL-SPC-020-010**: Stage 04 task evidence and progress memory record the
  final audit/remediation result and any accepted deferrals.

## Related Documents

- **Template Documentation Contract**: [../../99.templates/support/documentation-contract.md](../../99.templates/support/documentation-contract.md)
- **Template Routing Contract**: [../../99.templates/support/template-routing.md](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [../../99.templates/support/frontmatter-schema.md](../../99.templates/support/frontmatter-schema.md)
- **Legacy Cleanup Rules**: [../../99.templates/support/legacy-cleanup-rules.md](../../99.templates/support/legacy-cleanup-rules.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Quality Gate**: [../../../scripts/validate-repo-quality-gates.sh](../../../scripts/validate-repo-quality-gates.sh)
- **Future Plan**: `../../04.execution/plans/2026-07-05-workspace-contract-governance-normalization.md`
- **Future Task Evidence**: `../../04.execution/tasks/2026-07-05-workspace-contract-governance-normalization.md`
