---
title: "Close the Stage 03 Backlog"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0084-TSK-0001"
---

# Task: Close the Stage 03 Backlog

## Overview

This Task records the round: the survey each disposition starts from, the two
contract gaps it closes, the edges it takes, the retentions, the repairs those
retentions prove necessary, and the closure. It records observed results only
and never promotes a repository-static result to hosted, provider-runtime, or
live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: on 2026-09-16 the request owner approved this round with blanket
  authorization for individual completion, move, and deletion, and chose the
  registry gap-fills, the frontmatter reader consolidation, and the retention
  moves over the narrower alternatives offered.
- The survey reads the registry's own domain, profile, unit, mode, and class
  definitions, so a candidate here is a candidate the gates recognize.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SBC-001 | Record the survey of every remaining Stage 03 package | platform | Done | Sixteen packages recorded below with anchor state, non-terminal members, and consumers | This Task |
| WORK-002 | VAL-SBC-002 | Close the two registry gaps as gap-fills | platform | Done | Two profiles and one domain changed, 14 added and 4 removed lines, no existing document newly in violation | Recorded below |
| WORK-003 | VAL-SBC-003 | Close SPEC-0071, SPEC-0078, SPEC-0062, and SPEC-0054 | platform | Queued | Pending | Lifecycle gate |
| WORK-004 | VAL-SBC-004 | Withdraw SPEC-0048 and SPEC-0051 and cancel their Tasks | platform | Queued | Pending | Lifecycle gate |
| WORK-005 | VAL-SBC-005 | Repair SPEC-0006's stale sibling path and close it | platform | Queued | Pending | Link gate |
| WORK-006 | VAL-SBC-006 | Retain SPEC-0068 and SPEC-0070 in `superseded/` | platform | Queued | Pending | Archive gates |
| WORK-007 | VAL-SBC-007 | Record the dated disposition note of every package that stays | platform | Queued | Pending | This Task and the stage index |
| WORK-008 | VAL-SBC-008 | Resolve the duplicated frontmatter readers to one owner | platform | Queued | Pending | Unit tests and full QA |
| WORK-009 | VAL-SBC-009 | Retain every package that reached `done` in `completed/` | platform | Queued | Pending | Link, lifecycle, and archive gates |
| WORK-010 | VAL-SBC-010 | Repair the consumers the retention proves wrong | platform | Queued | Pending | Full QA and the unit-test suite |
| WORK-011 | VAL-SBC-011 | Close SPEC-0077 with its blocked criteria recorded as deferrals | platform | Queued | Pending | Lifecycle gate and this Task |
| WORK-012 | VAL-SBC-012 | Close this package with its results | platform | Queued | Pending | Staged and full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: the sixteen Stage 03 packages this round disposes of, their
  consumers in documents, in `scripts/` and in `tests/`, the `sdlc/spec` profile
  and the `spec-plan` domain in `docs/99.templates/registry.json`, the Stage 98
  index, the Stage 03 index, `.gitleaks.toml`, and this package.
- **Forbidden Paths**: frozen records, sealed ledgers, and retained bodies under
  `docs/98.archive/`; every registry key, profile, domain, state, and edge other
  than the two named; `gitops/`, `infrastructure/`, `policy/`, `secrets/`,
  `.github/`.
- **Approval Required**: the disposition of each package in this round, granted
  on 2026-09-16. Push, pull request, and merge are not approved.
- **Static Validation**: focused checks per work item, `python3 scripts/qa.py
  staged` per logical commit, and one `python3 scripts/qa.py full` on the final
  tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed. The `.gitleaks.toml` change moves one path-exact
  allowlist entry and reads no secret.
- **Rollback Plan**: Revert the commits before integration; after integration a
  retained unit is frozen and only a forward decision changes it.
- **Evidence Location**: This Task record.

### Survey

Read on 2026-09-16 at `e062290e`, the tree SPEC-0083 closed on. Every package
below is one SPEC-0083 surveyed and returned. The disposition column states the
terminal state this round takes it to, and the reason column states the observed
fact that decides it.

| Package | Anchor state | Non-terminal members | Disposition | Reason |
| --- | --- | --- | --- | --- |
| SPEC-0006 | active | none | `done` | Fifty-eight of its fifty-nine criteria name artifacts that exist; the residue is operator-owned runtime, which `completed/` admits. Its own text scopes it to a dated 2026-05-24 snapshot, and the gate it depended on was retired by SPEC-0072 |
| SPEC-0008 | active | none | stays `active` | It owns the current platform contract. Six accepted ADRs name it as their Spec, REQ-0004 traces to it, four operations documents carry it in a RACI row, and three test files pin its path. No successor exists |
| SPEC-0047 | active | five queued Tasks | stays `active` | Its CSASR-004 is obsolete by SPEC-0078's record, and its stash obligation is unowned: no validator covers the stash its Plan names. The obligation outlives the package |
| SPEC-0048 | draft | six queued Tasks | `withdrawn` | Its own dated note of 2026-09-14 recommends withdrawal and names the missing edge as the only blocker. GRCE-002 and 005 are met by CODEOWNERS, the labeler and the surface document, 004 by SPEC-0072 and SPEC-0073, 007 by the recorded main protection. The residual contract location `.agents/contracts/` does not exist |
| SPEC-0049 | draft | seven queued Tasks | stays `draft` | Genuinely unowned work: no `kustomize`, `kubeconform`, `kubeval` or `helm template` invocation exists anywhere in the repository, so PVSE-002 and 003 have no substitute. Its contract location must be re-planned before activation |
| SPEC-0050 | draft | seven queued Tasks | stays `draft` | The validation registry declares zero Terraform and zero Bicep validators, while two example READMEs publish commands no gate owns. The same re-planning applies |
| SPEC-0051 | draft | six queued Tasks | `withdrawn` | Its own dated note of 2026-09-14 recommends withdrawal: it requires a local-only fast-forward from a worktree that no longer exists while CI enforces pull requests into `main`, and it depends on a retired ledger |
| SPEC-0054 | active | tsk-0009 queued, tsk-0013 in-progress, tsk-0014 queued | `done` | Eleven of fourteen Tasks carry committed evidence. tsk-0009 is written against record forms ADR-0039 froze and names a `tombstones/` directory that does not exist; tsk-0013 holds accepted evidence with its residual scope reassigned; tsk-0014 is the closure record and its branch-completion half is overtaken |
| SPEC-0062 | active | three blocked Tasks, tsk-0011 in-progress | `done` | Seven Tasks are done and the 2026-08-29 closeout replaced the unfinished execution. The three blocked Tasks wait on an approved destructive replay and an execution environment the record itself states is absent; tsk-0011 states its work is complete and only the `done` edge remains |
| SPEC-0068 | superseded | none | retained in `superseded/` | Its body names SPEC-0072 as successor; the frontmatter could not carry it because the `sdlc/spec` profile declares an empty optional key list. Twenty-four sibling profiles declare `superseded_by` optional and no profile forbids it |
| SPEC-0070 | superseded | none | retained in `superseded/` | The same gap and the same successor. Its one live residue is three `.gitignore` lines that name a provider the roster no longer carries |
| SPEC-0071 | active | tsk-0001 in-progress | `done` | All thirteen criteria carry recorded evidence, and both its Spec and its Plan already state that closing to `done` is the next reviewed change |
| SPEC-0072 | active | tsk-0001 in-progress | stays `active` | Its native-runtime criteria need an operator observation the worker cannot perform. Closing would promote a repository-static result to runtime evidence, which its own record forbids. Its Task moves to `blocked`, which states that honestly |
| SPEC-0077 | active | tsk-0001 in-progress | `done` after WORK-005 | Five of eight criteria are met. Two gaps are authority-blocked: retiring two skills needs a new sealed migration, and routing `evals` needs a Stage 99 route. The third, resolving the duplicated frontmatter readers, has no blocker and is executed in this round |
| SPEC-0078 | draft | tsk-0001 queued | `done` | All six criteria carry evidence and all four of its commits are in history. Its own Task states that activation and closure are the first reviewed change after the merge that landed it, and that merge has happened |
| SPEC-0083 | done | none | retained in `completed/` | It closed its own round on this tree. Every member is terminal, so it is a finished unit awaiting disposition exactly as ADR-0039 describes |

Three facts in the table were read directly rather than taken from the survey
that reported them. The `sdlc/spec` profile declares `required` with eight keys,
`optional` empty and `forbidden` empty; `superseded_by` is optional in
twenty-four profiles, required in none and forbidden in none. The `spec-plan`
domain declares `draft` to `active`, `active` to `done`, `active` to
`superseded` and `active` to `withdrawn`, while the sibling
`requirement-architecture` domain declares `draft` to `withdrawn`.
`docs/98.archive/` holds `completed/`, `migrations/` and `superseded/` and no
`retired/`, so a withdrawn package stays at its Stage 03 path in this round.

### The two registry gap-fills

Applied on 2026-09-16. The change is fourteen added and four removed lines in
`docs/99.templates/registry.json`, and it was proved by comparing the parsed
registry before and after rather than by reading the diff alone.

| Gap | Before | After | Scope proof |
| --- | --- | --- | --- |
| A superseded spec cannot name its successor | `sdlc/spec` declared `optional` empty, so the allowed key set was exactly the eight required keys | `superseded_by` is optional and last in `order` | The only profiles that differ from their previous form are `sdlc/spec` and its template pair; `required` and `forbidden` are unchanged |
| A draft spec or plan cannot be withdrawn | `spec-plan` declared `draft` to `active`, `active` to `done`, `active` to `superseded`, and `active` to `withdrawn` | `draft` to `withdrawn` is declared, grouped with the other `draft` edge | The only domain that differs is `spec-plan`; its `states` are unchanged and the `task` domain is unchanged, so `queued` still reaches no terminal state directly |

Neither is a relaxation. The allowed key set is computed as required plus
optional, so widening `optional` admits one key and exempts no document from any
assertion; `superseded_by` is now optional in twenty-five profiles, required in
none, and forbidden in none. The `withdrawn` state already existed in the
`spec-plan` domain and only its approach was missing, which the sibling
`requirement-architecture` domain has always declared.

The template pair was not optional. `_assert_template_source_parity` in
`scripts/validate-document-contract-registry.py` requires every template profile
to inherit its source profile's class, frontmatter, headings, and body contract
exactly, exempting only `artifact_id` and `layer`. Changing `sdlc/spec` alone
split that pair, so `common/template-sdlc-spec` carries the same key. The
template document itself gains nothing, because the key is optional.

Observed after the change, on the same index: `document-contract-registry` PASS
over 800 paths with no uncovered or ambiguous path, `markdown-profiles` PASS
with no violation, `document-lifecycle` PASS in strict mode, `links-and-owners`
PASS over the whole corpus, and `python3 scripts/run-archive-contract-tests.py`
PASS with five modules and 87 tests. No existing document became a violation,
which is the evidence that distinguishes a gap-fill from a relaxation.

### Consumers that must move before a retention

| Consumer | Pins | Repair |
| --- | --- | --- |
| `tests/test_archive_validation.py` | SPEC-0054 as its stand-in for a present current document | Repoint to a package that stays |
| `tests/test_archive_cutover.py` | SPEC-0054 as its stand-in for an active package | Repoint to a package that stays |
| `.gitleaks.toml` and `tests/test_qa_runner.py` | a path-exact allowlist entry inside SPEC-0062's Plan | Move the entry with the retention |
| `.codex/provider.md` | SPEC-0072's Task path | No move; SPEC-0072 stays active |
| `docs/01.requirements/0003-workspace-agent-governance-platform.md` | SPEC-0006, SPEC-0071, SPEC-0077, SPEC-0078, SPEC-0083 | Repoint each to its retained path |
| This package | SPEC-0083 in its Spec, Plan and Task | Repoint when SPEC-0083 is retained in this same round |

## Verification Summary

Pending. The results of each work item are recorded here as they are observed.

This record, its Spec and its Plan were created in their zero-indegree states
because the lifecycle gate compares a change with its base, where this package
did not yet exist. Activation followed as its own reviewed change in `10847dc2`,
and WORK-001 is recorded from that point.

Every result recorded here is repository-static. No hosted CI run, provider
runtime, live cluster, or network action is claimed by any of them, and push,
pull request, and merge stay with the request owner.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | The survey of all sixteen packages is recorded below. |
| [WORK-002](../plan.md#work-breakdown) | Done. | Registry gap-fill recorded below; five focused gates and 87 archive contract tests pass. |
| [WORK-003](../plan.md#work-breakdown) | Queued. | Lifecycle gate. |
| [WORK-004](../plan.md#work-breakdown) | Queued. | Lifecycle gate. |
| [WORK-005](../plan.md#work-breakdown) | Queued. | Link gate. |
| [WORK-006](../plan.md#work-breakdown) | Queued. | Archive gates. |
| [WORK-007](../plan.md#work-breakdown) | Queued. | This Task and the stage index. |
| [WORK-008](../plan.md#work-breakdown) | Queued. | Unit tests and full QA. |
| [WORK-009](../plan.md#work-breakdown) | Queued. | Link, lifecycle, and archive gates. |
| [WORK-010](../plan.md#work-breakdown) | Queued. | Full QA and the unit-test suite. |
| [WORK-011](../plan.md#work-breakdown) | Queued. | Lifecycle gate and this Task. |
| [WORK-012](../plan.md#work-breakdown) | Queued. | Staged and full QA. |
