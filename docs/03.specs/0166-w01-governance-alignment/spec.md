---
title: "W01 Governance Alignment"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0166"
---

# W01 Governance Alignment Technical Specification (Spec)

## Overview

This approved change contract carries out the W01 stage of the external v14.7 execution package: the governance owners state one meaning for approval, adoption, contract editions, extensions, derived copies, conflict resolution, result reuse, document roles and hosted CI scope. [SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md) assigned these files to W01 and recorded the user's decisions (current v14.7 requirements prevail; CI-SCOPE and POLICY-ROLE adopted). A read-only survey at `e3d72466` recorded 19 items, 5 that already fit and 14 that need a change; the [Task](tasks/tsk-0001-w01-governance-alignment.md) records it. Registry, schema, template, validator, test and workflow changes are handed to W03, W05 and W06 with exact interfaces. The [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W01): `.agents/knowledge/glossary.md`, `.agents/governance/document-authoring.md`, `sdlc.md`, `quality.md`, `git.md`, `.agents/workflows/work-lifecycle.md`; this package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Handed over, not changed here, each with the interface and resume condition below: registry and template work (W03), lifecycle semantics per role (W04), checks and tests (W05), hosted CI with its requirement and decision change (W06), approval-reuse tests (W07).
- The current hosted CI contract stays as it is: REQ-0003 FR-0017 and acceptance criterion 11, and accepted ADR-0048, limit hosted CI to metadata and style. CI-SCOPE is recorded only as an adopted target; changing that contract is one W06 change set (see Interfaces).
- Kept, with evidence in the Task: the glossary structure, columns, 33 common term IDs and RFC 2119/8174 statement; GOV-05 single-operator role separation; GOV-08 approval reuse text; SUP-12; lowercase must and should.
- No retroactive change to accepted ADRs, completed Task evidence or Archived Lineage.
- No push, PR or merge without separate approval.
- Open question: none. CI-SCOPE and POLICY-ROLE were decided on 2026-11-12 (SPEC-0161 EVD-018); this change does not amend FR-0017 or ADR-0048.

## Contracts

- **Approval and adoption (GOV-03, GOV-04, R147-03, QA-C01).** Merged into the existing shared-contract paragraph of `document-authoring.md`, which already separates candidate, approval, local adoption and joint adoption. Added there: an approved or adopted edition records past authority and does not freeze the contract; a later approved target supersedes it through a recorded change. Approval is never inferred from a role name, hash, signature or registry value; absent evidence stays unverified, and no new ledger is created. The target record names the contract ID, version, single authoring owner, approval reference with approver and date, scope, exceptions, effective point, migration, rollback and consumer edition; today's registry carries `contract_id`, `version`, `stage` (`candidate` or `adopted`), `owner`, `approval_ref` and `extensions`, and W03 adds the rest. Partial adoption is never reported as full, and an approved compatible edition coexisting is not a defect by itself. "Independent review" becomes the owner's semantic review under the quality policy; shared adoption still needs application evidence from each repository.
- **Extension points (GOV-02).** Same owner: a regional extension may bind paths, commands, environments, native syntax, quality targets and deployment. It states its condition, owner, verification, review point and removal criterion; it never weakens or removes a common required condition, and a path or edition difference alone is no permanent exception. Standardization never forces one language, folder layout, CLI or quality number on every product.
- **Derived copies (GOV-06).** Same owner: each derived or generated copy names its source and edition and changes only through the source; a derived-only edit is a defect for the owning check (W05).
- **Conflict order (GOV-07).** `sdlc.md` replaces "neither side is presumed correct" with: resolve in the order current user requirement, approved contract, implementation and tests; change producer, reader, schema, current guidance and tests in one change set; an unapproved test expectation never becomes policy, and a test is never edited alone to make a violation pass. The order never authorizes a protected action: approval and safety rules still bind, and no package or agent message counts as user approval.
- **Three axes (R147-07).** `sdlc.md` distinguishes the document STAGE (owner and place), the SDLC phase (work step) and the Git point (before, during or after commit, push, PR or merge), and points to the lifecycle policy for status, acceptance, promotion and exit per role.
- **Policy role (POLICY-ROLE).** `sdlc.md` only: Policy is one document role with one common form, placed as `governance/rule` or `operation/policy`; a Rule is a normative unit with a stable ID inside a Policy, not a document role. `document-authoring.md` points there.
- **Result reuse and check timing (R147-20).** `quality.md`: a result is reused only when input bytes and history, configuration, tool identity, environment, scope, mode, trust, guarantee and consumer are the same, and reuse never drops a required security, regression or artifact check. A check that runs after an action observes it; it never claims to have blocked it.
- **Hosted CI target (CI-SCOPE).** `quality.md` adds one sentence beside the current hosted lane: the user adopted on 2026-11-12 a target in which PR-time hosted CI runs the affected implementation and product leaves with a read-only token and no secrets; until the W06 change set lands, FR-0017 and ADR-0048 govern and the hosted jobs are `ci-summary` and `style-pr`. The glossary `TERM-CI` becomes "Orchestration that integrates changes and runs the hosted checks the quality policy selects", with its Policy Owner moved to the quality policy.
- **Terms.** `git.md` no longer calls an integration "accepted"; `sdlc.md` says the operator approves an ADR whose status becomes `accepted`.
- **Glossary links.** Every Policy Owner cell is a relative Markdown link to an existing file.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. Each meaning has one W01 owner: contract editions, extensions and derived copies in `document-authoring.md`; axes, Policy role and conflict order in `sdlc.md`; reuse, check timing and the hosted target in `quality.md`. Other files point to them, and the glossary defines terms and links to the owners without copying procedures. Constraining decisions: [ADR-0048](../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md) keeps governing hosted CI (unchanged here); [ADR-0058](../../02.architecture/decisions/0058-repository-vocabulary-in-knowledge-surface.md) places term meaning in the glossary, which this change follows.

## Data Modeling & Storage Strategy

No new file or ledger. The contract record fields are policy meaning; their registry encoding is W03's.

## Interfaces & Data Structures

Handoff interfaces, each recorded in the Task with owner and resume condition:

- W03 (resume: this change accepted): add `approved_by`, `approved_at`, `scope`, `effective_from`, `migration`, `rollback` and `consumer_version` to `shared_contract`, map `owner` to the single authoring owner and `extensions` to exceptions with condition, owner, verification, review and removal fields, and add an `approved` stage between `candidate` and `adopted`; bind `governance/rule` and `operation/policy` to one Policy form.
- W04 (resume: W04 starts): state status, acceptance, promotion and exit per role and per axis in `document-lifecycle.md`.
- W05 (resume: W03 lands): a derived-copy drift check; `shared_contract` binding tests; a refusal of contradictory approval text; the `scripts/qa.py` reuse key with environment, guarantee and consumer.
- W06 (resume: W06 starts, user accepts a successor to ADR-0048): one change set with the successor ADR, the FR-0017 and criterion 11 amendment, `.github/workflows/ci.yml`, the mirrored CI scripts and tests, and the hosted-lane text in `quality.md`, `sdlc.md`, `git.md` and `work-lifecycle.md`.
- W07 (resume: W07 starts): allow and deny tests for low-risk approval reuse: a scoped reversible edit proceeds, a secret path or out-of-scope write is refused.

## Edge Cases & Error Handling

- Text that claims enforcement not yet implemented is refused in review; the hosted target is stated as a target with the observed jobs.
- Existing accepted ADR texts that use older wording stay as history.

## Failure Modes & Fallback / Human Escalation

If a wording change conflicts with an accepted ADR, the ADR wins until a successor ADR is accepted; the Task records the conflict and the owner.

## Verification Commands

- `python3 scripts/validate-document-contract-registry.py --root . --mode strict`, `validate-markdown-profiles.py`, `validate-links-and-owners.py` and `validate-document-lifecycle.py` in strict mode; `python3 scripts/validate-knowledge-surface.py --root .`; `python3 scripts/validate-agent-governance.py --root .`; `python3 scripts/run-contract-tests.py --root . --suite document` and `--suite agent-governance`.
- Phrase search, no current-owner hit after: `checks branch metadata`, `calling an integration accepted`, `independent review` in `document-authoring.md`, `neither side is presumed correct`.
- Anchor search, one hit each in its owner: `does not freeze the contract` and `never weakens or removes a common required condition` (`document-authoring.md`); `current user requirement, approved contract` and `one document role` (`sdlc.md`); `guarantee and consumer` and `never claims to have blocked` and `adopted on 2026-11-12 a target` (`quality.md`).
- `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-GOVALIGN-001 | The anchor search finds each Contracts item once in its named owner, the phrase search finds no current-owner hit, and each KEEP item has file:line evidence in the Task. |
| VAL-GOVALIGN-002 | Glossary Policy Owner links resolve and `TERM-CI` matches CI-SCOPE; the knowledge and strict document checks pass. |
| VAL-GOVALIGN-003 | The W03, W04, W05, W06 and W07 handoffs are recorded with owner, interface and resume condition; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVALIGN-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Knowledge and strict document checks. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVALIGN-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Phrase search and owner review. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVALIGN-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Handoff table; exact-index QA. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVALIGN-003 | [ADR-0048](../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md) | Unchanged; W06 handoff recorded. |
