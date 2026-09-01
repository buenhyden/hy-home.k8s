---
title: 'Agent Governance CI and QA Cutover Technical Specification'
version: "1.0"
type: sdlc/spec
layer: "03.specs"
status: done
owner: platform
updated: 2026-08-01
artifact_id: "SPEC-0045"
---

# Agent Governance CI and QA Cutover Technical Specification (Spec)

## Overview

This Spec adds an agent-governance-specific repository-static validation lane
on top of the always-start CI, affected-surface selection, `ci-summary`,
full-SHA, and least-permission foundation provided by Spec 039. It combines
the machine harness contract, exact 12-role / 4-provider-surface / 48-tuple
repository inventory, closed CI validation, consumer-first legacy cutover,
local QA ordering, concurrent checkpoint isolation, and durable memory policy
into one reproducible repository-static contract.

Spec 044 is an observed prerequisite: reciprocal closure
`42864832c966744ac4e5cf8c28baa5bf31ac2765` and postflight
`279f81032528dbf732acc3a1a8bc232d11d2c246` preserve configured incumbents,
mapping readiness `PASS` 21 / `DEFER` 27, and repository-static evaluation
readiness without claiming observed evaluation, admission, model fitness,
promotion, canary, or runtime results.

The fixed provider/model/source cutoff is
**2026-07-10T10:00:00+09:00** (**2026-07-10T01:00:00Z**), as owned by
[`provider-runtime-evidence.json`](../../00.agent-governance/contracts/provider-runtime-evidence.json).
The date **2026-07-30** records only this Spec activation observation and does
not move that source boundary.

Spec 045 may close only the repository-static implementation and local QA
boundary. Hosted CI observation, branch protection, provider runtime and
authentication, native agent/model discovery, actual evaluation/admission/
promotion, remote execution, live systems, and provider resume/handoff
canaries remain `DEFER` here and belong to the successor Spec 046
workstream. A repository-static PASS never proves that Claude, Codex, Gemini,
or a hosted runner consumed or executed the tracked configuration.

The repository-static cutover is complete through terminal implementation
HEAD `ed89228546501dd11a7f4abad28e8ebb094fbd97`. At implementation baseline
`a886e061`, the terminal Python suite passed `741` tests and the repository
aggregate, all-files pre-commit, formatter review, and both diff checks passed
with a clean tracked tree. The test-only terminal delta then passed all `49`
related tests, the nested-subreaper isolation probe, file pre-commit, and
requirements/quality/security review. Whole-branch and successive remediation
reviews cover the complete base-to-HEAD range with
requirements `COMPLIANT` and quality/security `APPROVED`, all at Critical `0`,
Important `0`, and Minor `0`. The reciprocal closure commit identity is
intentionally left for the separately observed postflight record.

## Strategic Boundaries & Non-goals

- **In scope**: Agent-governance selector/job/`ci-summary` topology; closed
  CI contract/schema/fixture/test validation; consumer-first legacy cutover;
  the `.github/ABOUT.md` to `.github/README.md` canonical rename; local QA
  ordering and inventories; repository-static concurrent checkpoint/provider
  identity; durable memory retention, compaction, and archive policy; full-SHA
  Action identity; least permissions; and reciprocal closure evidence.
- **Dependencies**: The CI/QA evidence topology in
  [Spec 039](../0039-github-ci-qa-evidence/spec.md) and the 12/48 roster and
  evaluation contract in
  [Spec 044](../0044-agent-roster-evaluation-and-admission/spec.md) precede this
  Spec. Spec 044 closure `42864832` and postflight `279f8103` are the observed
  activation prerequisites.
- **Protected boundaries**: The workflow does not require or output provider
  credentials, model tokens, secret values, or private transcripts. It does
  not introduce `pull_request_target`, broad write permissions, or mutable
  third-party Action tags.
- **Non-goals**: Changing GitHub branch protection; claiming a hosted workflow
  or remote required-check result; automating provider installation or login;
  executing provider resume/handoff canaries; observing native agent/model
  discovery; running actual role evaluations, admission, or promotion;
  mutating a live cluster; replacing provider canaries with static CI; or
  rewriting historical ADR/archive content as current policy.

## Contracts

The agent-governance lane executes or is skipped with an explicit selection
result inside Spec 039's always-start workflow. `ci-summary` consumes the
lane's PASS, FAIL, or SKIP result and does not interpret a missing job as
success. A change to any of the following path classes selects
agent-governance static validation:

- root provider shims and tracked surfaces under `.agents`, `.claude`,
  `.codex`, and `.gemini`;
- rules, providers, contracts, and model/roster/evaluation owners under
  `docs/00.agent-governance`;
- related PRD, AD, ADR, Spec, Plan, Task, and template/contract routes;
- agent-governance validators, fixtures, pre-commit configuration, and CI
  workflows;
- owner surfaces consumed by legacy scans and generated rosters/indexes.

The lane performs at least the following checks:

1. syntax, reference, and version contracts for `harness-contract.json`, its
   schema, and `validation-surfaces.json`;
2. exact set equality for 12 canonical roles and 48 adapters;
3. required metadata and semantic parity for Claude, Codex, Gemini, and local
   model/effort/configuration fields;
4. role-specific scope, tools, prohibited actions, stop conditions, handoff,
   and evidence owner;
5. evaluation manifest/corpus version, baseline, threshold, adjudication,
   rollback, and admission negative fixtures;
6. legacy/deprecated claims and duplicate-owner scans across the active corpus;
7. root/provider links, governed README/index files, and generated-output
   currentness;
8. concurrent checkpoint namespace and provider/worktree/task identity
   isolation using synthetic repository-static fixtures; and
9. durable memory retention, compaction provenance, replacement, archive/GC,
   conflict, and sensitivity-policy validation.

AGQC-002 plans
`docs/00.agent-governance/contracts/agent-governance-ci.json`, its adjacent
schema, `scripts/validate-agent-governance-ci.py`,
`tests/fixtures/agent-governance-ci.json`, and focused tests as one closed
contract. AGQC-003 plans `scripts/validate-agent-legacy-cutover.py` and its
deterministic fixture/test coverage. Neither validator exists at activation;
their names describe required deliverables, not observed commands.

The workflow and every third-party Action are pinned to a full commit SHA and
default to the minimum `contents: read` permission. Additional permissions are
granted only when the job-specific consumer and threat boundary are
documented. Agent-governance static checks receive no repository write,
issue/PR write, package, deployment, or id-token permission.

Provider-auth and resume/handoff canaries are Spec 046-owned local/manual
evidence. When separately authorized, they retain redacted evidence for each
Claude, Codex, and Gemini version, effective project configuration, agent
discovery, model resolution, and applicable hook/policy/configuration result.
Spec 045 does not run them, and GitHub Actions secrets are not added to run
them remotely.

## Core Design

### Static CI control flow

1. The Spec 039 selector computes changed paths and whether global escalation
   applies.
2. When the agent-governance owner is selected, the static job uses an
   immutable checkout and pinned tools to run contract/schema checks before
   semantic, evaluation, and legacy checks.
3. Each check result has one of `PASS`, `FAIL`, `SKIP`, or `DEFER`, together
   with a reason and owner. Required static checks cannot use DEFER.
4. `ci-summary` validates job selection and results. The aggregate fails if a
   selected job is absent or a required check is SKIP or DEFER.
5. Remote workflow execution, branch protection, and authenticated provider
   canaries retain separate evidence lanes.

### Local agent QA sequence

A repository-changing AI Agent preserves the following order before each
logical commit:

1. **targeted**: validators and tests closest to the changed
   contract/adapter/fixture;
2. **affected**: every owner selected by the path-to-validator registry;
3. **staged**: hook, secret, and syntax checks against the changes that will
   actually enter the index;
4. **tests**: relevant unit, negative-fixture, integration, and self-tests;
5. **all-files**: `pre-commit run --all-files`;
6. **formatter review**: review the meaning and scope of every diff produced by
   a formatter;
7. **rerun**: rerun affected checks and all-files after formatting or fixes;
8. **diff checks**: verify `git diff --check`, the staged diff, status, and the
   logical-commit boundary.

If an all-files run changes files, the initial run is not completion evidence.
Review and stage the changes, then repeat the relevant checks and all-files
until they produce a clean PASS. An optional tool may SKIP with a recorded
reason and owner, but a required-tool failure cannot be converted to SKIP.

### Legacy cutover order

Legacy deletion occurs only after consumer migration.

1. The current harness contract/schema and validator accept every active
   semantic consumer and remain the sole current role-semantics authority.
2. The four provider/local surfaces, aggregate, affected-surface registry,
   pre-commit and documentation inventories, and canonical documentation move
   to the harness owner.
3. The planned legacy-cutover validator proves zero active consumers of the
   legacy contract, schema, validator, fixture, and legacy-specific tests or
   allowlist entries. Positive and negative fixtures reject deletion while any
   consumer remains.
4. Only after that zero-consumer proof may the implementation remove
   `docs/00.agent-governance/contracts/agent-role-semantics.json`, its adjacent
   schema, `scripts/validate-agent-role-semantics.py`,
   `tests/fixtures/agent-role-semantics.json`, and their embedded self-test or
   focused compatibility assertions.
5. In the same consumer-first cutover, rename `.github/ABOUT.md` to canonical
   `.github/README.md` and update the registry route, repository-quality
   owner, documentation routes, fixtures, inventories, and every active
   reference before the old path disappears.
6. Remove stale active `10 roles / 30 adapters / 3 surfaces`,
   `.gemini`-surface-absent, duplicate roster/model/readiness, and provider-hook
   claims only after their consumers move. Preserve independently observed
   provider runtime `ABSENT` or `DEFER` evidence.
7. Preserve historical facts in superseded ADRs and archive records through a
   superseding relation and explicit historical allowlist, while preventing
   them from appearing as active currentness sources.

### Concurrent checkpoint and durable memory boundary

AGQC-005 extends repository-static loop/checkpoint evidence with a deterministic
non-secret identity tuple for repository, worktree, task, provider surface, and
provider/session instance. Synthetic fixtures reject cross-worktree,
cross-task, cross-provider, stale-base, or duplicate-writer resume and
overwrite attempts. Repository and canonical SDLC state remain authoritative
over every checkpoint claim.

The same package closes durable memory retention policy through explicit
owner, class, provenance, sensitivity, refresh/expiry, compaction source and
replacement, archive/GC disposition, conflict result, and handoff fields.
Fixture PASS proves only the tracked contract. It neither reads nor writes an
actual ignored checkpoint, provider-local memory, provider session, or
transcript and does not establish an actual provider resume or handoff.

### Spec 046 evidence boundary

AGQC-006 may close Spec 045 after repository-static contracts, local QA,
consumer migration, zero legacy, independent review, and reciprocal closure
evidence pass. Spec 046 separately owns provider canaries, hosted CI
observation, branch protection, actual evaluation/admission/promotion, native
runtime/auth/model discovery, remote execution, and live evidence. None of
those lanes may be promoted by a Spec 045 static or local result.

## Data Modeling & Storage Strategy

A CI selector result contains the changed path, selected owner, escalation,
expected job, and required/optional class. A static result contains the
validator ID, contract version, result class, evidence digest, and failure
summary. This data extends the Spec 039 aggregate schema instead of creating a
competing summary format.

The legacy inventory is maintained as a temporary migration ledger with
`claim`, `path`, `consumer`, `replacement`, `migrationStatus`,
`historicalException`, and `removalEvidence`. Delete the old contract only
after every row is `migrated` or an approved historical exception. One-time
raw scans and dry-run logs are not canonical documentation; retain only the
required conclusions and digests in Stage 04 Task evidence.

Checkpoint isolation fixtures contain non-secret identity labels and digests,
not provider credentials, raw session state, or actual ignored checkpoint
content. Durable memory records retain only reviewed summaries in canonical
owners and preserve compaction/archive provenance without retaining raw
prompts or transcripts.

Canary evidence remains a separate Spec 046-owned redacted record for each
provider. Do not store authentication material in CI artifacts or GitHub
secrets. Spec 046 consumes the Spec 045 static result and any separately
authorized provider result independently.

## Interfaces & Data Structures

- **Selector input/output**: changed paths -> selected static owners,
  escalation, expected jobs, and reason.
- **Static validator input/output**: canonical harness contract and tracked
  surfaces -> schema/parity/configuration/evaluation/legacy findings.
- **Aggregate interface**: selected job, actual conclusion, requiredness, result class ->
  single `ci-summary` verdict.
- **QA evidence interface**: lane, command, result, changed files, limitation, rerun,
  reviewer.
- **Legacy interface**: one-to-one migration from the old claim/owner to the
  replacement consumer; deletion is rejected while any consumer is unresolved.
- **Checkpoint isolation interface**: repository/worktree/task/provider/
  instance identity, base state, writer identity, resume verdict, and
  value-free conflict reason.
- **Durable memory interface**: memory class, canonical owner, provenance,
  sensitivity, retention/expiry, compaction replacement, archive/GC
  disposition, conflict verdict, and handoff.
- **Canary interface**: provider/version/configuration
  source/discovery/model/configuration result -> secret-free local record that
  is not combined with the CI static verdict and remains Spec 046-owned.

## Edge Cases & Error Handling

- Even for a docs-only change, changes to the machine contract, provider note,
  roster/model owner, or admission/evaluation rule select the static lane.
- `ci-summary` always exists and validates the skip reason even when a workflow
  job is conditionally skipped.
- An absent or unauthenticated provider CLI is a local canary FAIL/DEFER and is
  not masked by a static CI PASS.
- A historical ADR that retains an old `10/30/3` or Gemini-absent decision is
  classified as intentional history when it is not the current owner and its
  superseding relation is verified.
- Deletion stops if any active validator, script, template, or provider note
  still consumes the old contract.
- A partial `.github/ABOUT.md` to `.github/README.md` rename fails while either
  the old active path or a stale registry, quality-gate, fixture, inventory, or
  documentation reference remains.
- A checkpoint identity collision, stale base, cross-worktree/task/provider
  resume, or unowned durable memory record fails repository-static validation
  without reading the actual provider or ignored checkpoint payload.
- If a formatter changes a file outside the target, do not accept that change
  automatically. Confirm the owner and reason, then reassess the scope.

## Failure Modes & Fallback / Human Escalation

- If the static job cannot validate a required contract, it fails closed and
  reports the condition in Spec 039's `ci-summary`.
- Replace an Action that cannot satisfy full-SHA or least-permission
  requirements, or switch to local tool invocation; do not approve a mutable
  ref.
- If legacy consumer migration is incomplete, retain the old owner and record
  the active gap and follow-up owner. Do not weaken the validator to force the
  cutover.
- If checkpoint namespace isolation or durable retention/compaction/archive
  policy is incomplete, retain the Spec 043 baseline and record the missing
  identity or owner contract. Do not claim an actual provider resume/handoff.
- If a canary would require moving provider authentication into a CI secret,
  stop and request separate approval from the platform/security owner.
- Failure of all-files or formatter review blocks the logical commit and
  downstream Spec closure.

## Verification Commands

```bash
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-checkpoint.py --root . --self-test
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

The first two commands are planned Spec 045 deliverables and are not claimed
to exist at activation. Together with existing/focused validators they must
cover selector positive/negative cases, workflow security/aggregate topology,
credential-free evidence separation, consumer-first migration, zero stale
active legacy, concurrent checkpoint/provider identity, durable memory policy,
and the required QA ordering/formatter rerun.

## Success Criteria & Verification Plan

- **VAL-AGQC-001**: Spec 039's always-start workflow and `ci-summary`
  aggregate agent-governance lane selection and results without omissions.
- **VAL-AGQC-002**: Every third-party Action in the agent-governance job uses a
  full SHA, permissions are minimally read-only, and no forbidden write or
  OIDC permission exists.
- **VAL-AGQC-003**: Contract/schema, 12/48 parity, provider
  configuration/model/effort, role semantics, and evaluation/admission
  positive and negative fixtures produce identical CI and local verdicts.
- **VAL-AGQC-004**: Static CI evidence is separate from authenticated
  Claude/Codex/Gemini canary evidence, and provider credentials are not added
  to GitHub secrets.
- **VAL-AGQC-005**: Every logical commit records the order and results of
  targeted, affected, staged, tests, all-files, formatter review, rerun, and
  diff checks.
- **VAL-AGQC-006**: If `pre-commit run --all-files` creates changes, only a
  clean PASS after review and rerun qualifies as completion evidence.
- **VAL-AGQC-007**: After all active consumers move to the new owner, the
  counts of stale `10/30/3`, `.gemini`-surface-absent claims, duplicate
  matrices, stale hook/semantics contracts, old role-semantics contract/schema/
  validator/fixture/test ownership, `.github/ABOUT.md`, and orphan references
  are zero; `.github/README.md` is canonical and separately classified runtime
  `ABSENT`/`DEFER` evidence remains accurate.
- **VAL-AGQC-008**: Historical exceptions remain only through
  superseding/archive relations and do not enter active currentness queries or
  the generated roster.
- **VAL-AGQC-009**: Synthetic repository-static fixtures reject concurrent
  checkpoint identity collisions and cross-worktree/task/provider resume, and
  durable memory records validate retention, compaction replacement,
  archive/GC, conflict, sensitivity, and canonical-owner policy without
  reading or claiming actual provider checkpoint/resume/handoff state.
- **VAL-AGQC-010**: Independent requirements, quality, and security reviews
  plus focused, affected, staged, tests, all-files, formatter-review/rerun, and
  diff gates approve repository-static closure while hosted CI, branch
  protection, provider runtime/auth/model discovery, actual evaluation/
  admission/promotion, remote, live, and provider canary outcomes remain
  `DEFER` for Spec 046.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **AD**: [AD 0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **CI foundation**: [Spec 039](../0039-github-ci-qa-evidence/spec.md)
- **Roster/eval predecessor**: [Spec 044](../0044-agent-roster-evaluation-and-admission/spec.md)
- **Observed prerequisite**: Spec 044 closure `42864832` and postflight
  `279f8103`
- **Successor**: [Spec 046](../0046-agent-governance-program-closure/spec.md)
- **Execution Plan**: [Agent Governance CI and QA Cutover Implementation Plan](plan.md)
- **Task evidence**: [Agent Governance CI and QA Cutover Task](README.md#task-records)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-001 | Selector and aggregate fixtures prove the Spec 039 CI ownership boundary. |
| N/A — VAL-AGQC-002 shares the REQ-0003-NFR-0002 source linked above | VAL-AGQC-002 | Workflow-security fixtures prove full-SHA and least-permission enforcement. |
| N/A — VAL-AGQC-003 shares the REQ-0003-NFR-0002 source linked above | VAL-AGQC-003 | Static contract and parity fixtures produce identical local/CI verdicts. |
| N/A — VAL-AGQC-004 shares the REQ-0003-NFR-0002 source linked above | VAL-AGQC-004 | Evidence-lane fixtures keep provider credentials and canaries outside GitHub CI. |
| N/A — VAL-AGQC-007 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-007 | Consumer migration and active scans prove safe legacy removal. |
| N/A — VAL-AGQC-008 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-008 | Historical scans prove intentional records remain non-current. |
| N/A — VAL-AGQC-009 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-009 | Checkpoint identity and durable memory fixtures prove repository-static isolation and lifecycle policy. |
| N/A — VAL-AGQC-005 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-005 | Task evidence proves the mandatory QA lane ordering. |
| N/A — Acceptance criterion 11 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-006 | All-files and formatter rerun fixtures prove clean completion. |
| N/A — repeated VAL-AGQC-007 metric shares the PRD-0003 source linked above | VAL-AGQC-007 | Active-corpus scans report zero stale current claim. |
| N/A — repeated VAL-AGQC-008 metric shares the PRD-0003 source linked above | VAL-AGQC-008 | Historical relation validation prevents old evidence from becoming current. |
| N/A — repeated VAL-AGQC-009 metric shares the PRD-0003 source linked above | VAL-AGQC-009 | Synthetic isolation and memory-policy fixtures preserve the Spec 043 runtime boundary. |
| N/A — VAL-AGQC-010 shares the PRD-0003 source linked in VAL-AGQC-001 | VAL-AGQC-010 | Reciprocal closure and independent review prove only the repository-static Spec 045 transition. |
