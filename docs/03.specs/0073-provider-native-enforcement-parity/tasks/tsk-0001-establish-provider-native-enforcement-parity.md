---
title: "Establish Provider Native Enforcement Parity"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0073-TSK-0001"
---

# Task: Establish Provider Native Enforcement Parity

## Overview

Execute SPEC-0073-PLAN-0001 as fourteen ordered work packages, each delivered
as one logical commit gated by its exact index snapshot, with the full profile
run once on the final tree before handoff. This record owns execution results,
per-lane evidence, and the limits that remain unobserved.

Execution is under way. WORK-006 delivered the model alignment that WORK-008
and WORK-009 had planned separately, because a binding validator cannot land
before the values it validates; WORK-009 now carries only the permission mode.

## Inputs

- [SPEC-0073](../spec.md)
- [SPEC-0073-PLAN-0001](../plan.md)
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
- [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [ADR-0035](../../../02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md)
- [SPEC-0072](../../0072-agent-governance-and-quality-gate-consolidation/spec.md)
- Baseline commit `a57887cbf8d34eed248cb33438073635380966e3` on branch
  `codex/governance-follow-up`; local `main` and `origin/main` both at
  `4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`
- Client identity observed 2026-09-06: `claude 2.1.261`, `codex-cli 0.140.0`,
  `python 3.12.3`, `pre-commit 4.5.1`

## Task Table

| ID                                    | Upstream criterion | Work item                                                                       | Owner    | Status | Result       | Evidence                                                   |
| ------------------------------------- | ------------------ | ------------------------------------------------------------------------------- | -------- | ------ | ------------ | ---------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-PNP-001 | Record the decision lineage for the current governance topology | platform | Done | ADR-0034 superseded with a reciprocal successor row; ADR-0035 accepted; the index, AD-0006 and REQ-0003 name the current owner | Commit `7bfbf1dd`; staged profile, six gates |
| [WORK-002](../plan.md#work-breakdown) | VAL-PNP-009 | Remove retired-provider and retired-path residue from tracked configuration | platform | Done | Dead pre-commit exclusion, two removed-provider globs, one deleted-test index row and one contradicted stage claim removed | Commit `ce0adb53`; staged profile, six gates |
| [WORK-003](../plan.md#work-breakdown) | VAL-PNP-005 | Make the GitHub Actions security validator reachable from a supported profile | platform | Done | Gate registered on the all-files and CI lanes; its first run found a one-day artifact retention against the seven-day contract | Commit `1f6420ee`; reachability test RED then GREEN |
| [WORK-004](../plan.md#work-breakdown) | VAL-PNP-006 | Reduce duplicated rule implementations and profile membership to one owner | platform | Done | Duplicate Vault and ESO heredoc removed, 441 to 306 lines, both gates still passing; two reported duplications kept as distinct rules | Commit `41648686`; staged profile, seven gates |
| [WORK-005](../plan.md#work-breakdown) | VAL-PNP-007 | Set the commit and handoff evidence proportion in Git policy | platform | Done | The staged profile gates a logical commit; the full profile gates branch finish and handoff | Commit `43711f02`; staged profile, six gates |
| [WORK-006](../plan.md#work-breakdown) | VAL-PNP-003 | Add the per-provider capability-to-model binding to the registry and schema | platform | Done | Binding declared for both providers; twenty-three of twenty-four projections realigned; drift now fails on both sides | Binding tests RED then GREEN; governance validator |
| [WORK-007](../plan.md#work-breakdown) | VAL-PNP-002 | Declare a native execution scope for every Codex role and widen the parity rule | platform | Done | Each permission class binds one Codex sandbox scope; twelve projections carry it and widening or dropping it fails closed | Commit `edf960a3`; scope tests RED then GREEN |
| [WORK-008](../plan.md#work-breakdown) | VAL-PNP-003 | Align every Codex role model with the observed client catalog | platform | Done | Delivered inside WORK-006; the installed client catalog listed only `gpt-5.5`, `gpt-5.4-mini` and `gpt-5.3-codex-spark`, so eleven of twelve prior values named absent models | Governance validator; catalog observed 2026-09-06 |
| [WORK-009](../plan.md#work-breakdown) | VAL-PNP-002 | Align every Claude role model and permission mode with the registry binding | platform | Blocked | Models delivered inside WORK-006 as documented aliases. The Claude permission mode is not applied: `tools` already gives an enforced structured scope, and the subagent effect of `permissionMode` was not observed on this client | `DEFER` pending a native observation; next owner platform |
| [WORK-010](../plan.md#work-breakdown) | VAL-PNP-004 | Extend the pre-action guard to the shell tool class and name the residual class | platform | Done | Guard matcher covers the shell tool; redirect, tee and in-place sed targets are reported; out-of-repo, read-only and unparsed commands stay silent and exit zero | Commit `3093e158`; five new guard cases |
| [WORK-011](../plan.md#work-breakdown) | VAL-PNP-008 | Correct provider notes to describe native capability against a named client | platform | Done | Capability statements name the client they were observed against; the Codex hook denial is replaced by a supported-but-not-adopted statement | Commit `5c017dde`; observed `claude 2.1.261` and `codex-cli 0.140.0` |
| [WORK-012](../plan.md#work-breakdown) | VAL-PNP-007 | Add the untrusted input, cost and throughput, and loop termination boundaries | platform | Done | Untrusted input, cost and throughput, and loop termination boundaries added at their policy owners | Commit `724719fb`; profile and link validation |
| [WORK-013](../plan.md#work-breakdown) | VAL-PNP-010 | Reconcile Stage 90 research baseline rows with the current tree | platform | Done | Six baselines framed as dated observation with current owners named; two present-tense column headers corrected; one duplicated router link removed | Commit `de1f7858`; path sweep and staged profile |
| [WORK-014](../plan.md#work-breakdown) | VAL-PNP-004 | Mirror the pre-action guard as a Codex native hook after observing the payload | platform | Blocked | Not started. The Codex event payload shape was not observed, and no authorized fresh Codex session was run | `DEFER`; `sandbox_mode` remains the only Codex structured control |
| [WORK-015](../plan.md#work-breakdown) | VAL-PNP-009 | Route current documents to sealed evidence through the archive index | platform | Done | The retention commit removed the navigational exemption for Migration ledgers; four current documents still linked one directly and the index reached neither ledger they cite. Index navigation added, four links rerouted, seven terminal Task records left untouched | `archive-cutover` PASS, records=25; `tests.test_archive_cutover` 37 cases OK |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/`, `.agents/roles/registry.json`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.agents/roles/registry.schema.json`, `.claude/agents/`,
  `.claude/settings.json`, `.claude/hooks/`, `.claude/provider.md`,
  `.claude/README.md`, `.codex/agents/`, `.codex/provider.md`,
  `.codex/README.md`, `.codex/hooks.json`, `.github/labeler.yml`,
  `.pre-commit-config.yaml`, `README.md`, `docs/02.architecture/decisions/`,
  `docs/03.specs/0073-provider-native-enforcement-parity/`,
  `docs/03.specs/0062-workspace-research-full-corpus-reverification/tasks/`
  (current records only), `docs/98.archive/README.md`,
  `docs/03.specs/README.md`, `docs/90.references/research/`,
  `docs/99.templates/registry.json`, `docs/99.templates/templates/runtime/`,
  `scripts/validate-agent-governance.py`, `scripts/validation/registry.json`,
  `infrastructure/tests/verify-contracts-static.sh`, `tests/`
- **Forbidden Paths**: the user's staged index and every path it touches,
  `.claude/settings.local.json`, `.claude/*.local.md`, `_workspace/` contents,
  `policy/`, `gitops/`, `infrastructure/` outside the named contract script,
  `secrets/`, sealed record bodies under `docs/98.archive/`
- **Approval Required**: commit authorization per logical package; separate
  authorization for push, pull-request creation, merge, branch cleanup, and any
  hosted or provider-authenticated execution
- **Static Validation**: `python3 -m unittest` for the focused modules,
  `python3 scripts/validate-agent-governance.py --root .`,
  `python3 scripts/qa.py staged` per package, `python3 scripts/qa.py full` once
  before handoff, `git diff --check` and `git diff --cached --check`
- **Live Validation**: `DEFER` — no cluster, Argo CD, Vault, cloud, remote Git,
  or hosted CI operation is authorized by this Task
- **Secret / Vault Handling**: no credential, token, authentication file,
  environment dump, plaintext secret, shell history, or provider transcript is
  read, printed, or recorded; validator failure messages name paths and
  expected values only
- **Rollback Plan**: `git revert` of the owning package commit; a corrective
  change is a new forward commit, never a history rewrite
- **Evidence Location**: this record

## Verification Summary

Twelve work packages landed as twelve logical commits, each gated by the staged
profile against its exact index. Two remain `DEFER` with a reason and a next
owner, and one gate fails for a cause outside this package.

**Repository-static lanes.** Every commit passed `python3 scripts/qa.py staged`
on its own index. The handoff `python3 scripts/qa.py full` selected twenty
gates over 1026 paths and returned twenty `PASS` after the dispositions below.
Its first run returned seventeen `PASS` and three `FAIL`.

- `archive-cutover` failed `ARCHIVE-DIRECT-CURRENT-LINK` on `.agents/README.md`
  and three `blocked` SPEC-0062 Task records that linked a Migration ledger
  directly, and `unit-tests` failed three `tests/test_archive_cutover.py` cases
  from the same cause. The rule that made those links illegal arrived with the
  Spec 0052 retention commit, which removed the navigational exemption for
  Migration ledgers; `archive-cutover` runs only on the all-files and CI lanes,
  so no staged run could have selected it. WORK-015 repaired both: the archive
  index now reaches MIG-0004 and MIG-0009, the four current documents cite them
  through the index, and the seven `done` SPEC-0062 records stay untouched
  because a terminal record is exempt from the rule and must not be rewritten.
- `pre-commit` reported that `ruff format` rewrote three test files this change
  added. The formatter output was reviewed and committed explicitly.

All three are resolved; the rerun over the final tree passed every gate.

**Negative evidence recorded.** A drifting model on either provider, a widened
or missing Codex sandbox scope, a validator with no profile membership, and a
Codex projection carrying an unknown key all fail closed, each demonstrated
before its fix and shown passing after it.

**Lanes that produced no evidence.** Native discovery, native enforcement,
model resolution, authenticated provider operation, hosted CI execution, and
live infrastructure behavior are `DEFER`: no fresh provider session was run, no
push was made, and no cluster was inspected. No editor-extension behavior was
observed either, because neither provider extension is installed here.

**Review disposition.** Self-reviewed against the diff of each commit. No
independent reviewer has examined this work.

**Rollback.** Each package is one commit; `git revert` of that commit reverses
it. No history was rewritten and no branch was pushed, merged, or deleted.

**Residual risk.** The capability binding and the Codex sandbox scope are
tracked configuration whose runtime effect is unobserved. The write-path guard
still cannot see a program that opens files itself. A rule that only the
all-files and CI lanes select can be broken by a staged-only change and stay
invisible until handoff, which is how WORK-015's defect reached a commit.

**Next owner.** platform, for the two `DEFER` packages and any authorized
native observation.

## Traceability

### Lifecycle Traceability

| Criterion / work item                 | Result                                                    | Evidence                                                          |
| ------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Recorded the decision lineage without rewriting either decision body | Commit `7bfbf1dd`; document lifecycle and link validation |
| [WORK-002](../plan.md#work-breakdown) | Removed five tracked entries that could never match or hold true | Commit `ce0adb53`; repository quality and filesystem sweep |
| [WORK-003](../plan.md#work-breakdown) | Registered the orphan gate and fixed the violation its first run found | Commit `1f6420ee`; reachability test and profile listing |
| [WORK-004](../plan.md#work-breakdown) | Removed one duplicate implementation; kept three distinct rules | Commit `41648686`; both gates re-run after removal |
| [WORK-005](../plan.md#work-breakdown) | Stated the commit and handoff evidence proportion | Commit `43711f02`; quality policy cross-reference |
| [WORK-006](../plan.md#work-breakdown) | Capability tier now determines the native model on both providers | Binding tests and governance validator negative cases |
| [WORK-007](../plan.md#work-breakdown) | Codex roles now carry an enforced structured scope | Commit `edf960a3`; widening and removal both fail closed |
| [WORK-008](../plan.md#work-breakdown) | Codex models realigned to the observed client catalog | Governance validator; recorded catalog identity |
| [WORK-009](../plan.md#work-breakdown) | Model half delivered; permission mode deferred without runtime evidence | `DEFER` recorded with its reason |
| [WORK-010](../plan.md#work-breakdown) | Shell writes are observed advisorily; the residual class is named | Commit `3093e158`; approval boundary text |
| [WORK-011](../plan.md#work-breakdown) | Native capability claims carry a client identity | Commit `5c017dde` |
| [WORK-012](../plan.md#work-breakdown) | Three missing boundaries added at their owners | Commit `724719fb` |
| [WORK-013](../plan.md#work-breakdown) | Stage 90 baselines read as dated observation | Commit `de1f7858` |
| [WORK-014](../plan.md#work-breakdown) | Not executed; gated on an unobserved payload shape | `DEFER` with next owner |
| [WORK-015](../plan.md#work-breakdown) | Archive cutover and its unit cases recovered without editing a terminal record | `archive-cutover` PASS; 37 archive cutover cases OK |
