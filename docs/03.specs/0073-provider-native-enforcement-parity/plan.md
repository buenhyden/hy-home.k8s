---
title: "Provider Native Enforcement Parity Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0073-PLAN-0001"
---

# Provider Native Enforcement Parity Implementation Plan

## Global Constraints

- One work package is one logical commit. Rollback is `git revert` of that
  commit; no history rewrite, force update, branch deletion, or worktree
  removal is authorized.
- A behavior change demonstrates its failing case before its fix and shows the
  passing result after it.
- The staged profile gates each logical commit; the full profile gates handoff.
- Repository-static results never report as native discovery, native
  enforcement, hosted CI, or live behavior.
- Push, pull-request creation, merge, and hosted execution are not authorized
  by this plan and are not implied by any passing check in it.

## Overview

This plan executes
[SPEC-0073](spec.md) to make the declared execution scope structured on both
providers, give the capability-to-model binding one owner, extend the
pre-action guard to the shell tool class, and reconcile the capability
statements, gate reachability, retired-path residue, and research observations
that remained after the SPEC-0072 static migration.

Completion means the ten specification criteria hold on the final working
tree, the native observations that could be made are recorded, and the ones
that could not are recorded as `DEFER` with a reason and a next owner.

## Context

The common authority under `.agents/` is in place and the governance validator
passes on the current tree. The asymmetry this plan removes is inside that
validator: the Claude native key set admits and checks a scope field, and the
Codex native key set admits none, so a Codex role's boundary is prose only.

Two decisions describe incompatible topologies. ADR-0034 is accepted and
prescribes a governance root the repository no longer has; ADR-0035 is proposed
and describes the root the repository does have. Work that depends on the
current topology therefore has no accepted decision to stand on, which is why
the lineage correction is the first package.

The installed clients were observed on 2026-09-06 as `claude 2.1.261` and
`codex-cli 0.140.0`. The Codex client reports a stable hook surface and the
Codex documentation describes a per-agent sandbox field; both contradict the
current Codex provider notes. Eleven of twelve Codex projections name models
absent from that client's catalog.

The repository carries pre-existing staged work for
[SPEC-0054](../0054-sdlc-document-and-agent-governance-consolidation/spec.md)
taxonomy cutover. That index and the untracked personal provider files are
outside this plan's write boundary.

## Goals & In-Scope

- Record the decision lineage so the current topology has an accepted owner.
- Declare a machine-readable execution scope for every role on both providers.
- Bind capability tier to native model once and validate every projection.
- Extend the pre-action guard to shell-mediated repository writes.
- Make every tracked validator reachable from a supported profile.
- Reduce duplicated rule implementations and duplicated profile membership.
- Set the commit and handoff evidence proportion in Git policy.
- Correct provider capability statements against a named client identity.
- Remove retired-provider and retired-path residue from tracked configuration.
- Add the untrusted input, cost and throughput, and loop termination
  boundaries missing from common policy.
- Reconcile Stage 90 research baseline rows with the current tree.

## Non-Goals & Out-of-Scope

- Role membership, permission-class semantics, handoff edges, and the meaning
  of any responsibility body.
- The QA runner's bounded-execution guarantees and the archive cutover
  contracts with their sealed recovery evidence.
- Any Stage 03 package whose work is in flight, including the SPEC-0054
  taxonomy cutover currently staged in this working tree.
- The user's staged index, `.claude/settings.local.json`, `.claude/*.local.md`,
  `_workspace/` contents, and `policy/` Kubernetes policy code.
- Live cluster, Argo CD, Vault, cloud, remote Git, hosted CI, and provider
  authentication.
- Adopting an external agent catalog as a role roster.
- Retiring cutover validators, tests, or fixtures whose migration is not sealed.

## Work Breakdown

| ID     | Work package                                                                                                                                                                    | Depends on     | Entry gate                        | Exit evidence                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| WP-001 | Record the decision lineage: mark ADR-0034 superseded by ADR-0035 and accept ADR-0035, leaving both decision bodies intact                                                      | None           | VAL-PNP-001 approved              | Lifecycle and link validation on the changed decisions; reviewed decision log                         |
| WP-002 | Remove retired-provider and retired-path residue from the pre-commit exclusion, the label glob, the Stage 99 provider-shim route, the tests index row, and the root stage table | WP-001         | VAL-PNP-009 approved              | Repository quality, document contract registry, and a filesystem sweep showing no remaining reference |
| WP-003 | Register the GitHub Actions security validator in the validation-surface contract so it is reachable from the handoff and CI profiles                                           | WP-002         | VAL-PNP-005 approved              | Failing reachability test before, passing after; profile listing showing the new membership           |
| WP-004 | Reduce duplicated rule implementations and duplicated profile membership to one owner each                                                                                      | WP-003         | VAL-PNP-006 approved              | Before-and-after gate comparison; focused tests for each consolidated rule                            |
| WP-005 | Set the commit and handoff evidence proportion in Git policy and align its quality-policy cross-reference                                                                       | WP-004         | VAL-PNP-007 approved              | Reviewed policy text against the canonical completion sequence                                        |
| WP-006 | Add the per-provider capability-to-model binding to the role registry and schema and validate every projection against it                                                       | WP-001         | VAL-PNP-003 approved              | Failing binding tests before, passing after; governance validator                                     |
| WP-007 | Declare a native execution scope for every Codex role and widen the governance validator's native key set and parity rule                                                       | WP-006         | VAL-PNP-002 approved              | Failing scope tests before, passing after; governance validator                                       |
| WP-008 | Align every Codex role model with the observed client catalog through the registry binding                                                                                      | WP-006, WP-007 | VAL-PNP-003 approved              | Governance validator; recorded client and catalog identity in the Task                                |
| WP-009 | Align every Claude role model and permission mode with the registry binding and the documented native value vocabulary                                                          | WP-006         | VAL-PNP-002, VAL-PNP-003 approved | Governance validator; focused native metadata tests                                                   |
| WP-010 | Extend the pre-action guard to the shell tool class and name the residual interpreter-mediated class in the approval boundary                                                   | WP-009         | VAL-PNP-004 approved              | Failing guard tests before, passing after; reviewed approval boundary                                 |
| WP-011 | Correct the provider notes and adapter READMEs to describe native capability against a named client identity                                                                    | WP-010         | VAL-PNP-008 approved              | Reviewed provider notes; recorded observation in the Task                                             |
| WP-012 | Add the untrusted input boundary, the cost and throughput boundary, and the loop termination criteria to their common policy owners                                             | WP-011         | VAL-PNP-004, VAL-PNP-007 approved | Reviewed policy text; profile and link validation                                                     |
| WP-013 | Reconcile Stage 90 research baseline rows with the current tree, keeping historical observations dated and unedited                                                             | WP-012         | VAL-PNP-010 approved              | Path existence sweep; reference pack route test                                                       |
| WP-014 | Mirror the pre-action guard as a Codex native hook, conditional on observing the client's event payload shape                                                                   | WP-010, WP-011 | Native observation recorded       | Guard mirror tests, or a recorded `DEFER` with the observation and next owner                         |

## Verification Plan

Each work package runs its focused checks during implementation, then the
staged profile against its exact index snapshot before its commit. The full
profile runs once on the final working tree before handoff.

| Work package     | Focused checks                                                      | Evidence lane                                   |
| ---------------- | ------------------------------------------------------------------- | ----------------------------------------------- |
| WP-001           | Document lifecycle and link validation on the changed decisions     | Repository static                               |
| WP-002           | Repository quality, document contract registry, filesystem sweep    | Repository static                               |
| WP-003, WP-004   | Validation-surface contract test, QA runner tests, profile listing  | Repository static                               |
| WP-005, WP-012   | Markdown profile and link validation; policy review                 | Repository static                               |
| WP-006 to WP-009 | Governance registry and native metadata tests; governance validator | Repository static                               |
| WP-010           | Guard unit tests including the new tool class                       | Repository static                               |
| WP-011           | Provider note review against recorded client identity               | Repository static plus one recorded observation |
| WP-013           | Reference pack route test and path existence sweep                  | Repository static                               |
| WP-014           | Guard mirror tests                                                  | Provider runtime, or `DEFER`                    |
| Handoff          | Full profile on the final tree; both diff whitespace checks         | Repository static                               |

Native discovery, native enforcement, model resolution, authenticated
operation, and hosted execution are separate lanes. They are recorded in the
Task as observed results or as `DEFER` with a reason and a next owner, and a
passing repository-static profile never stands in for them.

## Risks & Mitigations

| Risk                                                                                                                | Impact                                                             | Mitigation                                                                                                           | Owner    |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | -------- |
| The governance validator pins the settings and native key sets exactly, so widening them can mask a real regression | A weakened contract passes                                         | Add the failing case first for every widened rule, and keep one distinct failure cause per condition                 | platform |
| The Codex hook event payload may not match the documented shape                                                     | A hook that silently never fires, or one that blocks ordinary work | Keep the mirror in its own package behind an observation gate; ship the sandbox scope independently                  | platform |
| A model identifier chosen from the observed catalog may not resolve for this account                                | A projection that cannot start                                     | Record catalog identity, revert the value in a forward corrective commit, and do not weaken the validator            | platform |
| Widening the guard matcher may produce false blocks on ordinary shell work                                          | Interrupted work                                                   | Keep the advisory output contract, revert the matcher change as its own commit if needed                             | platform |
| The working tree carries unrelated staged work                                                                      | Accidental capture in a commit                                     | Stage explicitly per package, inspect the cached diff before each commit, and never stage a path outside the package | platform |
| Correcting research rows could overwrite historical fact                                                            | Falsified record                                                   | Keep observation dates, add current owner references, and remove only present-tense assertions                       | platform |

## Completion Criteria

- All ten specification criteria hold on the final working tree.
- Every work package has a reviewed diff, a focused result, and a staged
  result, and the full profile passed once on the final tree.
- Every unobserved lane is recorded as `DEFER` with a reason and a next owner,
  and no unobserved lane is reported as passing.
- The package Task carries the canonical handoff fields, including failures,
  skipped optional tools, review disposition, rollback, and residual risk.
- No protected surface listed in the non-goals was modified.

## Traceability

### Lifecycle Traceability

| Spec criterion                                             | Work package   | Expected Task                                                              |
| ---------------------------------------------------------- | -------------- | -------------------------------------------------------------------------- |
| [VAL-PNP-001](spec.md#success-criteria--verification-plan) | WP-001         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-009](spec.md#success-criteria--verification-plan) | WP-002         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-005](spec.md#success-criteria--verification-plan) | WP-003         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-006](spec.md#success-criteria--verification-plan) | WP-004         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-007](spec.md#success-criteria--verification-plan) | WP-005, WP-012 | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-003](spec.md#success-criteria--verification-plan) | WP-006, WP-008 | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-002](spec.md#success-criteria--verification-plan) | WP-007, WP-009 | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-004](spec.md#success-criteria--verification-plan) | WP-010, WP-014 | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-008](spec.md#success-criteria--verification-plan) | WP-011         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
| [VAL-PNP-010](spec.md#success-criteria--verification-plan) | WP-013         | [tsk-0001](tasks/tsk-0001-establish-provider-native-enforcement-parity.md) |
