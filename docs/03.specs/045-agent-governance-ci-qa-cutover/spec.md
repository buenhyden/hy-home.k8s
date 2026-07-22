---
title: 'Agent Governance CI and QA Cutover Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: 2026-07-22
---

# Agent Governance CI and QA Cutover Technical Specification (Spec)

## Overview

This Spec adds an agent-governance-specific static validation lane on top of
the always-start CI, affected-surface selection, `ci-summary`, full-SHA, and
least-permission foundation provided by Spec 039. It combines the machine
harness contract, 12-role/48-adapter parity, provider-native configuration,
role evaluation and admission evidence, and active-corpus legacy cutover into
one reproducible QA contract.

Provider authentication and actual model/agent discovery remain local/manual
canaries that do not inject repository secrets into GitHub. A static CI PASS is
not evidence that the Claude, Codex, or Gemini CLI consumed the configuration
or executed an authenticated model.

The source and security decision cutoff is **2026-07-10 10:00 Asia/Seoul**.
Implementation follows the official contracts for
[GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use),
[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
and [`pre-commit`](https://pre-commit.com/).

## Strategic Boundaries & Non-goals

- **In scope**: Agent-governance static job, path-to-validator selection,
  contract/schema/parity/config/eval/legacy fixtures, aggregate result wiring,
  full-SHA Action identity, least permissions, the local QA sequence, and
  legacy consumer cutover.
- **Dependencies**: The CI/QA evidence topology in
  [Spec 039](../039-github-ci-qa-evidence/spec.md) and the 12/48 roster and
  evaluation contract in
  [Spec 044](../044-agent-roster-evaluation-and-admission/spec.md) must precede
  this Spec.
- **Protected boundaries**: The workflow does not require or output provider
  credentials, model tokens, secret values, or private transcripts. It does
  not introduce `pull_request_target`, broad write permissions, or mutable
  third-party Action tags.
- **Non-goals**: Changing GitHub branch protection, claiming the state of
  remote required checks, automating provider installation or login, mutating
  a live cluster, replacing authenticated canaries with static CI, or rewriting
  historical ADR/archive content as current policy.

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
- related PRD, ARD, ADR, Spec, Plan, Task, and template/contract routes;
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
   currentness.

The workflow and every third-party Action are pinned to a full commit SHA and
default to the minimum `contents: read` permission. Additional permissions are
granted only when the job-specific consumer and threat boundary are
documented. Agent-governance static checks receive no repository write,
issue/PR write, package, deployment, or id-token permission.

Provider-auth canaries run only in the local/manual lane and retain redacted
evidence for each Claude, Codex, and Gemini version, effective project
configuration, agent discovery, model resolution, and applicable
hook/policy/configuration result. GitHub Actions secrets are not added to run
canaries remotely.

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

1. The new harness contract/schema and validator accept every current
   consumer.
2. The four provider/local surfaces and canonical documentation reference the
   new roster/model/evidence owner.
3. Positive and negative fixtures prove the new owner and rejection of the old
   owner.
4. Only then remove the active-surface `10 roles / 30 adapters / 3 surfaces`
   claim, the Gemini absent/`DEFER` claim, duplicate roster/model/readiness
   matrices, stale provider-hook wording, the old semantics contract, and
   unconsumed adapters.
5. Preserve historical facts in superseded ADRs and archive records through a
   superseding relation and explicit historical allowlist, while preventing
   them from appearing as active currentness sources.

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

Canary evidence remains a separate redacted record for each provider. Do not
store authentication material in CI artifacts or GitHub secrets. Spec 046
consumes the static result and local canary result independently.

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
- **Canary interface**: provider/version/configuration
  source/discovery/model/configuration result -> secret-free local record that
  is not combined with the CI static verdict.

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
- If a canary would require moving provider authentication into a CI secret,
  stop and request separate approval from the platform/security owner.
- Failure of all-files or formatter review blocks the logical commit and
  downstream Spec closure.

## Verification Commands

```bash
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
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
to exist in this draft. Together with existing/focused validators they must
cover selector positive/negative cases, workflow security/aggregate topology,
credential-free evidence separation, consumer-first migration, zero stale
active legacy, and the required QA ordering/formatter rerun.

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
  counts of stale `10/30/3`, Gemini absent/`DEFER`, duplicate matrices, and
  stale hook/semantics contracts are zero.
- **VAL-AGQC-008**: Historical exceptions remain only through
  superseding/archive relations and do not enter active currentness queries or
  the generated roster.

## Traceability

- **PRD**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **ARD**: [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **CI foundation**: [Spec 039](../039-github-ci-qa-evidence/spec.md)
- **Roster/eval predecessor**: [Spec 044](../044-agent-roster-evaluation-and-admission/spec.md)
- **Successor**: [Spec 046](../046-agent-governance-program-closure/spec.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-001 | Selector and aggregate fixtures prove the Spec 039 CI ownership boundary. |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-002 | Workflow-security fixtures prove full-SHA and least-permission enforcement. |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-003 | Static contract and parity fixtures produce identical local/CI verdicts. |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-004 | Evidence-lane fixtures keep provider credentials and canaries outside GitHub CI. |
| [REQ-PRD-FUN-14](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-007 | Consumer migration and active scans prove safe legacy removal. |
| [REQ-PRD-FUN-14](../../01.requirements/003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AGQC-008 | Historical scans prove intentional records remain non-current. |
| [REQ-PRD-MET-11](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGQC-005 | Task evidence proves the mandatory QA lane ordering. |
| [REQ-PRD-MET-11](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGQC-006 | All-files and formatter rerun fixtures prove clean completion. |
| [REQ-PRD-MET-12](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGQC-007 | Active-corpus scans report zero stale current claim. |
| [REQ-PRD-MET-12](../../01.requirements/003-workspace-agent-governance-platform.md#success--acceptance-criteria) | VAL-AGQC-008 | Historical relation validation prevents old evidence from becoming current. |
