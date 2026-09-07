---
title: "Adopt Common Knowledge and Prompt Surfaces"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0075-TSK-0001"
---

# Task: Adopt Common Knowledge and Prompt Surfaces

## Overview

This Task owns execution for [SPEC-0075](../spec.md) through the ordered work
packages in [the plan](../plan.md). It records per-package results, the
evidence lane each result belongs to, the approval boundaries observed, and the
limits that remain unobserved. It is in progress: the packages below record their
actual state, and a row that has not run says so rather than anticipating an
outcome.

WP-001 and WP-002 landed before this record was reconciled, so the earlier
`queued` state understated the tree. That gap is corrected here rather than
backdated: the rows carry the commits that produced them.

## Inputs

- [SPEC-0075](../spec.md) for the change contract and the criteria.
- [Implementation Plan](../plan.md) for ordered packages, entry gates, and exit
  evidence.
- [Work lifecycle](../../../../.agents/workflows/work-lifecycle.md) for intake,
  bounded implementation, and completion.
- [Approval and safety](../../../../.agents/governance/approval-and-safety.md)
  for protected actions.
- [Document authoring](../../../../.agents/governance/document-authoring.md)
  and the Stage 99 registry for profile selection and template routing.
- [Quality policy](../../../../.agents/governance/quality.md) for lane
  meanings, the completion sequence, and the handoff fields.
- Baseline observation: branch `docs/0074-0075-governance-design`, base
  `f5f355f1465dbce217dfbd5ab163b301be879ae7`, twenty-one gates passing under
  `python3 scripts/qa.py full`.
- Upstream observation: `msitarzewski/agency-agents` head
  `1454492577d1af4884722837f491fef14b501e21`, authored 2026-09-05, MIT
  licensed, observed 2026-09-06.

## Task Table

| ID                                    | Upstream criterion | Work item                                                                  | Owner    | Status | Result      | Evidence    |
| ------------------------------------- | ------------------ | -------------------------------------------------------------------------- | -------- | ------ | ----------- | ----------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-CKP-002        | Author the successor decision and mark the prior decision superseded        | platform | Done | ADR-0036 restates ADR-0035's authority-location, skill-routing, gateway, preservation and validation clauses and revises only the unadopted-directory clause; it records the reason each remaining optional directory stays unadopted and why the adopted surface is not the retired generated index. ADR-0035 carries `superseded_by` and a reciprocal successor row with its body intact; both decisions are indexed | Commits `4583e88c`, `22ff2f4d`; strict lifecycle and link validation PASS |
| [WORK-002](../plan.md#work-breakdown) | VAL-CKP-002        | Align the governance README and the context-and-memory routing sentence     | platform | Done | The governance README structure table names both surfaces, the configuration boundary states the adopted position with a per-directory reason for the three that stay unadopted, and the authority-decision link moves to ADR-0036. The context-and-memory routing sentence names the map without granting it authority | Commit `38136bec`; `grep -rn "are not adopted" .agents/ docs/02.architecture/` returns no match; staged profile 6 gates PASS |
| [WORK-003](../plan.md#work-breakdown) | VAL-CKP-003        | Add the knowledge and prompt profiles with templates                        | platform | Done | Two profiles were added with their templates: `governance/knowledge` requires a Pointer Index, `governance/prompt` requires inputs, output, validation and refusal conditions. Both joined the governance lifecycle domain, which the registry validator requires before it will accept a status value. The two surface READMEs reuse the collection-index router by path extension | Commit `d05cd6ee`; registry 735 paths, uncovered=0, ambiguous=0; staged profile 6 gates PASS |
| [WORK-004](../plan.md#work-breakdown) | VAL-CKP-001        | Create the knowledge surface and register it in the surface contract        | platform | Done | The surface holds a README, a project map over fourteen top-level trees and a domain index over ten domains, each row carrying an owner path, an entry path and a validity condition. Registered in the validation-surface contract and admitted by the governance validator's closed-directory check | Commit `346c392a`; affected-surface contract 1054 paths, surfaces 22/22, uncovered=0; staged profile 12 gates PASS |
| [WORK-005](../plan.md#work-breakdown) | VAL-CKP-004        | Add the knowledge owner-path and non-duplication validator                  | platform | Done | The validator fails on a row naming an absent path, on a twelve-word span reproduced from an owner the document points at, and on a document missing from the README index. Six behaviour tests plus a registration test and a repository test | Commit `346c392a`; 8 tests PASS. Mutation check: removing the refusal path and bypassing the allowlist each produce a failing suite, so the tests are not vacuous |
| [WORK-006](../plan.md#work-breakdown) | VAL-CKP-001        | Wire the knowledge consumers at the navigation skill and the intake step    | platform | Done | The navigation skill reads the project map for the owning tree and the domain index for the entry document, and verifies each row against the tree rather than trusting it. The work-lifecycle intake step names the surface at the point where owning documents are selected | Commit `e2bc5bf9`; staged profile 12 gates PASS |
| [WORK-007](../plan.md#work-breakdown) | VAL-CKP-001        | Create the prompt surface with its four contracts                           | platform | Done | Four contracts with a README. Each declares its inputs with the exact read-only command producing them, its output shape, its validation rule, its refusal conditions, and by name the subject input whose emptiness triggers refusal | Commit `e2bc5bf9`; staged profile 12 gates PASS |
| [WORK-008](../plan.md#work-breakdown) | VAL-CKP-005        | Implement the deterministic prompt input builder                            | platform | Done | The builder resolves a contract, runs only allowlisted read-only commands, and writes the assembled request to standard output. Unknown identifier exits 2; an empty subject exits 3 with no draft; the commit-message contract reads the staged difference and not the working tree; no invocation changes Git state and the module imports no network library | Commit `e2bc5bf9`; 10 tests PASS. Refusal was first demonstrated by execution — `change-review` exited 3 against an empty local difference — before the tests existed; the tests were written after the implementation rather than before it, and mutation checks stand in for the missing red phase |
| [WORK-009](../plan.md#work-breakdown) | VAL-CKP-001        | Add the command entry points and retire the VS Code surface                 | platform | Done | Four command entry points, one per contract, each invoking the builder with its identifier. `.claude/commands/*.md` resolved to no document profile, so `common/provider-native-command` was added with its template instead of leaving the path uncovered. No identifier collides with a skill identifier. The VS Code retirement this row also covered had already landed in commits `e3c0d405` and `45e31a9b` before this Task resumed | Commit `e2bc5bf9`; registry 748 paths, uncovered=0; staged profile 12 gates PASS |
| [WORK-010](../plan.md#work-breakdown) | VAL-CKP-006, VAL-CKP-010 | Consolidate the responsibility documents and carry every consumer      | platform | Partial | The router's reference to a root `DESIGN.md` was repaired, and so were the four other active governance documents that made the same claim: the file has never existed in this repository's history, so the clause was removed and the absence stated once in the SDLC owner. The seven category documents were not consolidated; that half is deferred with its reason below | Commit pending in this change; strict link and owner validation PASS. `git log --all -- DESIGN.md` returns no commit |
| [WORK-011](../plan.md#work-breakdown) | VAL-CKP-007        | Correct the reference pack and add the current dated observation            | platform | Done | The filename guidance no longer forbids the `m####-` identity prefix its own registry mandates; the prefix is now stated as an identity rather than an ordering key. The duplicated navigation link was removed, and three direct cross-links into the Archive were replaced by one link to the Archive index, which is the routing owner. Four retired `Stage 00` labels were replaced where the sentence describes the present. A dated 2026-09-07 observation records the two-provider, twelve-role, thirty-six-projection registry beside the four-provider observation, whose wording, subject and date are unchanged, and adds the three-way capability comparison the pack lacked | Commit pending in this change; strict link, owner and profile validation PASS on the index snapshot |
| [WORK-012](../plan.md#work-breakdown) | VAL-CKP-008        | Record the upstream re-observation and the zero-adoption conclusion         | platform | Done | Upstream `main` was re-observed on 2026-09-07 at `647c8baa42b6842afb4a97bf2c0950d45ba88e8b`, dated 2026-09-06, with `license.spdx_id` `MIT` and `pushed_at` `2026-09-06T20:47:20Z`. That head is beyond `1454492577d1af4884722837f491fef14b501e21`, which this Task's Inputs recorded on 2026-09-06; the earlier reading is superseded additively, not corrected in place. The registry role count is unchanged at twelve and no role is adopted | External metadata read over a public endpoint, 2026-09-07. It establishes the branch head and licence field at that moment and nothing about file content |
| [WORK-013](../plan.md#work-breakdown) | VAL-CKP-009        | Give each duplicated rule one execution owner with retention reasons        | platform | Done | The premise was checked before anything was removed and does not hold: `hadolint` is declared only in `.pre-commit-config.yaml`, no validation script runs it, and the repository tracks no Dockerfile. There is no duplicate execution to reassign, and removing the hook would drop future coverage rather than move ownership, so it is retained with that reason recorded. The action-pinning pair was verified as a deliberate interlock: `validate-github-actions-security.py` forbids `unpinned-uses` suppression, so the validator guards the linter's rule. The commit hook suite inside the full profile is retained because the override below makes the commit-time run inert here | Direct inspection of `.pre-commit-config.yaml`, `scripts/`, and the tracked file list; `scripts/validate-github-actions-security.py` lines 164-170 |
| [WORK-014](../plan.md#work-breakdown) | VAL-CKP-011        | Record the commit-tooling limitation with a user-run remedy                 | platform | Done | The global `core.hooksPath` is `/home/hy/.codex/git-hooks`, so the repository's installed `.git/hooks/pre-commit` and `commit-msg` do not run at commit time and the conventional-commit check does not either. Recorded as a limitation, never as a working control, with the repository-local remedy `git config --local core.hooksPath .git/hooks` for the user to run. The global configuration was not modified | `git config --global core.hooksPath` and `git config core.hooksPath` observed 2026-09-07; recorded in the CI/QA reference guide |

## Approval and Safety Boundaries

Authorized for this Task: reading repository files and official public
documentation; local edits within the paths the specification authorizes;
non-destructive local validation; a task-owned branch; and reviewed logical
local commits.

Not authorized and not performed: push, pull-request creation, merge, release,
remote workflow dispatch, or branch-protection change; any live Kubernetes,
ArgoCD, Vault, or cloud operation; reading or storing credentials, tokens,
private keys, kubeconfig, plaintext secrets, shell history, environment dumps,
or raw session records; modification of user configuration outside the
repository, including the global hook path and user editor settings;
`git reset --hard`, `git clean`, unapproved stash operations, rebase, amend,
force update, branch deletion, or worktree removal; installation of the
upstream persona catalog or execution of unreviewed external scripts.

The successor decision revises one clause of an accepted decision. That
revision is the authorized scope of this Task; widening it to other clauses,
or adopting a directory the decision keeps unadopted, requires separate
approval.

No entry point this Task creates makes a paid model call mandatory, and no
commit-time hook gains a network dependency.

Two pre-existing stashes target removed authority roots and one would
reintroduce the retired progress ledger. They are left untouched; their
disposition is the user's to make. `_workspace/task-3-trace-fix-report.md` and
the empty `_workspace/repo-support/` directory are pre-existing untracked
residue owned by earlier work and are not removed by this Task.

## Verification Summary

Thirteen of fourteen work packages have executed; WP-010 is partial. Each ran
the staged profile against its own index snapshot before its commit and
reported every gate passing. The gate count per commit varies because the lane
selects validators from the changed paths: six gates for policy-text-only
changes, twelve once `scripts/` and `.agents/` paths were in scope.

Two results correct the specification's own premises rather than confirming
them, and are recorded as findings rather than folded silently into a pass:

- WP-013's premise does not hold. The container-manifest linter has one
  execution owner already and the repository tracks no Dockerfile, so there was
  no duplicate to reassign and removing the hook would have dropped coverage.
  The plan's guard clause required stopping and recording that, which is what
  happened. The action-pinning interlock the same package describes was checked
  and does hold.
- The `DESIGN.md` reference WP-010 was to repair was not one stale link but
  five, in five separate active governance documents, naming a file that has
  never existed in this repository's history. All five were corrected.

Two limits are recorded as limits, not as controls:

- The global `core.hooksPath` on this workstation points outside the repository,
  so the commit-time hooks and the conventional-commit check do not run here.
  The remedy is repository-local and belongs to the user.
- Native runtime evidence remains mostly absent. Two observations exist and are
  narrow: this session listed the four command identifiers, which is discovery
  and not invocation; and the Claude write-guard adapter blocked every shell and
  file tool while the affected-surface contract was inconsistent, which
  demonstrates fail-closed behaviour for this client only.

No repository-static result in this Task is reported as provider-runtime,
hosted, or live evidence.

The pre-change baseline is recorded: `python3 scripts/qa.py full` reported
twenty-one gates passing on the working tree containing the two draft
specifications. Any gate that stops passing during implementation is a
regression of the change that preceded it.

One observation is already recorded as a limitation rather than a control: on
this workstation the global `core.hooksPath` points outside the repository, so
the repository's commit-time hooks, including the conventional-commit check, do
not run at commit time. The global configuration is not modified; WP-014
records a repository-local remediation the user runs.

Deferred items, each with its blocker and next owner:

- Whether either client loads a knowledge document or a prompt contract.
  Blocker: each requires a fresh authenticated session. Next owner: the user.
  Command-entry discovery is observed; contract loading is not.
- WP-010's second half: consolidating the seven category documents under
  `.agents/roles/` into the responsibility router. Blocker: none technical. It
  is deferred because it removes seven files and repoints consumers in eleven
  role bodies and one Stage 90 index, which is a distinct ownership change from
  the surface adoption this Task delivered and deserves its own review unit.
  Next owner: the user, to schedule it.
- Direct cross-links from active documents into `docs/98.archive/` beyond the
  research README corrected here. The document README forbids them for active
  Stage 01/02/03/05/90 documents, and a sweep found further instances in
  `docs/90.references/research/0001-workspace-engineering/`. Most remaining
  instances sit inside sealed decision bodies, which are not rewritten. Blocker:
  the boundary between a sealed lineage record and an active router needs a
  decision. Next owner: the user.
- Statements in SPEC-0054's Spec and Plan that keep root `DESIGN.md` as the
  UI owner. They are change-contract text owned by that package, not by this
  one, so they were left intact rather than edited across an ownership
  boundary. Next owner: SPEC-0054.
- The pin disagreement recorded as `CLM-WERPC-016-03` in the reference pack
  remains open and was not adjudicated here.

No repository-static result in this Task is reported as provider-runtime,
hosted, or live evidence.

## Traceability

[SPEC-0075](../spec.md) owns the criteria and [the plan](../plan.md) owns the
ordered packages and their entry gates. This Task owns results and limits.

### Lifecycle Traceability

| Criterion / work item                 | Result      | Evidence                                                          |
| ------------------------------------- | ----------- | ----------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done        | ADR-0036 accepted, ADR-0035 superseded with a reciprocal row, both indexed |
| [WORK-002](../plan.md#work-breakdown) | Done        | No active file states the superseded position; staged profile PASS        |
| [WORK-003](../plan.md#work-breakdown) | Done         | Two profiles with templates; registry 735 paths, uncovered=0 |
| [WORK-004](../plan.md#work-breakdown) | Done         | Surface registered; affected-surface 1054 paths, uncovered=0 |
| [WORK-005](../plan.md#work-breakdown) | Done         | Validator with 8 tests; two mutations each fail the suite |
| [WORK-006](../plan.md#work-breakdown) | Done         | Navigation skill and work-lifecycle intake read the surface |
| [WORK-007](../plan.md#work-breakdown) | Done         | Four contracts, each naming its subject input by name |
| [WORK-008](../plan.md#work-breakdown) | Done         | Builder with 10 tests; refusal first shown by execution |
| [WORK-009](../plan.md#work-breakdown) | Done         | Four entry points; new profile covers the previously uncovered path |
| [WORK-010](../plan.md#work-breakdown) | Partial      | DESIGN.md repaired in five documents; consolidation deferred |
| [WORK-011](../plan.md#work-breakdown) | Done         | Prefix contradiction, duplicate link and archive links resolved |
| [WORK-012](../plan.md#work-breakdown) | Done         | Head 647c8baa dated 2026-09-06, MIT; role count unchanged |
| [WORK-013](../plan.md#work-breakdown) | Done         | Premise disproved: no duplicate execution owner exists |
| [WORK-014](../plan.md#work-breakdown) | Done         | Global hooksPath override recorded with a local remedy |
