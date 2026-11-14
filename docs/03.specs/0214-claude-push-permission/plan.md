---
title: "Claude Delivery Permissions and CI/CD Governance Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0214-PLAN-0001"
parent_ids: ["SPEC-0214"]
---

# Claude Delivery Permissions and CI/CD Governance Implementation Plan

## Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds five constraints:

1. Only `Bash(gh release create:*)` and `Bash(gh workflow run:*)` leave the deny list; no other existing deny is removed, reordered or weakened.
2. No allow is added beyond the Spec list.
3. No test reads a live provider, the network or a remote.
4. `.codex/rules/`, `.codex/config.toml`, hooks, workflows and remote settings are untouched, and in `.codex/` only the provider note's parity sentence changes.
5. The diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Write the failing regressions and the new pin first, then change the tracked settings. Then amend the release-ownership text and add the delivery boundary once in the Git policy, point both provider notes and the release runbook at it, and record the residual risk. [Task 0001](tasks/tsk-0001-claude-push-permission.md) owns execution and evidence.

## Context

Read at `main` `511e106f`:

- **Settings and pin.** `.claude/settings.json` holds 20 allow, 3 ask and 197 deny rules plus `disableBypassPermissionsMode`. `scripts/validate-agent-governance.py` pins the three lists by ordered equality (lines 90-320 and 1537-1547); the two denies the user lifted sit at settings lines 46-47 and validator lines 137-138.
- **Tests.** `tests/test_agent_governance.py` asserts push as `ask` (lines 1292-1302), keeps `gh release delete` and `gh run cancel` denied (lines 1355-1356), and decides commands with the matcher model `_bash_rule_matches` (lines 1107-1123).
- **Provider notes.** `.claude/provider.md` lines 50-53 say that every push, `gh api` and `git -C` ask, because a `:branch` or `+branch` refspec cannot be matched. That holds for `:branch`, but `+branch` is matchable as `git push * +*`. `.codex/provider.md` lines 63-64 call the Codex rules a subset of the Claude deny families, which the lifted denies make untrue.
- **Git option parsing.** Git accepts a unique prefix of a long option and clusters short options. The kept push denies therefore miss `--de`, `--m`, `--pru`, `--al`, `--b`, `--force-w`, `-uf`, `-ud` and similar forms once push is allowed. Scratch dry runs on Git 2.43 confirmed the cases the Spec lists.
- **Policy.**
  - The policy files require the user's decision for push, PR creation and merge (git.md line 22; approval-and-safety.md line 52; work-lifecycle line 122), but no per-call native prompt; PR creation and merge are already allowed on that basis.
  - Git.md lines 67-69 require explicit approval for each force push, branch deletion and amend, and git.md lines 58-59 and 127 forbid hook bypass and tag rewrites outright.
  - Git.md lines 112-133 and ADR-0048 lines 146-147 make `scripts/release.py` the sole producer.
- **Release runbook.** Runbook 0012 lines 35-38 and 112-116 name the operator as the only executor of `publish --execute`, while ADR-0048 lines 174-175 require only the applicable authority.
- **Codex.** Codex asks before every network command (`.codex/config.toml` lines 3-6, 8 and 12) and forbids a prefix subset that includes `gh release create` and `gh workflow run` (rules lines 72-73), with a pinned digest (validator line 37).
- **Hosted protection.** Hosted `main` protection was read back on 2026-11-11T23:46Z (SPEC-0161 Task lines 230 and 235). Tag rulesets and feature branches have no read-back.
- **Local configuration.** `push.default` is `current` in this clone, and the primary checkout is on `main` (observed 2026-11-14).
- **Rule IDs.** `git.md` carries rule code `GIT` in `pending` state, and SPEC-0199 (approved, not yet merged) adopts rule IDs for it.
- **Architecture.** AD-0006 (governance view, release-production row at line 72), ADR-0048 (one release producer) and ADR-0052 (single `main` trunk) apply, and none is departed from. Interfaces: the three settings lists, the validator tuples and the test module. Migration: none. Rollback: revert the implementation commit.

## Goals & In-Scope

- The final allow, ask and deny lists, with their validator pin and failing-first regressions, including the unique-prefix and cluster cases.
- The amended git.md release-ownership text and the `#### Agent delivery commands` subsection; the Claude provider note replacement; the Codex provider note's parity sentence; the runbook 0012 executor lines; the Stage 03 README entry.
- The residual risk, including what policy forbids but no rule denies and the code the allowed commands run, and the three enforcement layers, recorded once and linked.

## Non-Goals & Out-of-Scope

- Ignored personal settings; `gh api` and `git -C`; the Codex rules, configuration, hooks, bindings and projections; workflows; remote protection and rulesets; `scripts/release.py` behavior; ADR-0048 and AD-0006; any registry, so the Registry Schema Version is NO_CHANGE.
- New denies for tag force and delete, `gh release edit` and `upload`, or `gh workflow enable` and `disable`, which the user's answers leave to policy.
- SPEC-0161 rows, its residue ledger entries and any W03 decision number.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DELIVERYPERM-001](spec.md#success-criteria--verification-plan) | Write the failing decision and mutation tests and update the three validator tuples and their comment, show the whole validator failing on the old settings, then change the three settings lists. | Spec and Plan approval. | [Task 0001](tasks/tsk-0001-claude-push-permission.md) | Failing then passing tests and validator; `agent-governance` suite. |
| WORK-002 | [VAL-DELIVERYPERM-002](spec.md#success-criteria--verification-plan) | Amend the git.md release-ownership text and add the delivery subsection (as `GIT-R###` rows if SPEC-0199 has merged), replace the Claude provider note lines and the Codex parity sentence, amend the runbook 0012 executor lines and add the Stage 03 README entry; run the document and exact-index checks. | WORK-001; the merge state of SPEC-0199 at rebase. | [Task 0001](tasks/tsk-0001-claude-push-permission.md) | Strict document validators, affected-surface routing, ruff, staged QA and commit hooks. |

## Verification Plan

- Record the four strict document validators and the governance validator before any change.
- Failing-first order:
  1. Change the tests and run them. Each new `allow` and `deny` expectation and the two new mutations fail.
  2. Change the validator tuples. `python3 scripts/validate-agent-governance.py --root .` fails with `AGENT-NATIVE-PERMISSION` on the old settings.
  3. Change the settings. Everything passes.

  The forced-merge mutation and the kept `gh release delete` and `gh run cancel` cases pass before and after, and are recorded as regressions.
- Write the two hook-bypass deny strings and their test commands with the structured edit tool inside the repository. A local plugin hook outside the repository refuses shell command lines that contain the hook-bypass option, even as text. Record any such refusal as a tool limit and never work around it.
- Architecture compliance: the work stays within AD-0006, ADR-0048 and ADR-0052, keeps one release producer, and adds no component, gate or diagnostic. A departure returns the Spec to `in-review`.
- Optional, not required: a read-only authenticated read-back of `main` protection and the tag rulesets through `gh api`, which asks; and a new-session probe of a few rules by the Claude client. Each is recorded as hosted or provider-runtime evidence, or as `DEFER` with the operator as next owner.
- Commit and merge order: rebase on `main` before each commit. If SPEC-0199 has merged, write the git.md changes as `GIT-R###` rows; otherwise name them to SPEC-0199. Record the risk class `high` (a permission change), and list each changed permission and protected action in the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **A policy-forbidden command runs without a prompt.** Possible, Severe: HIGH, accept as the user's decision, and mitigate. Owner: platform. This covers a tag rewrite, a Release made outside the producer, and a workflow enable or disable. The git.md subsection and the Claude provider note name each one, and an agent that meets such a request stops and asks. Remote tag rewrites that use a force or delete option or `+` stay denied. Review cue: a moved or missing tag, a Release whose Task lacks a producer record, or a disabled workflow.
- **A force, delete, mirror or prune push slips through an option form the deny list cannot express.** Unlikely, Severe: MEDIUM, mitigate and record. Owner: platform. Unique prefixes and two-letter clusters are denied. Clusters of three or more letters with `f` or `d` after the second position cannot be expressed and stay residual. Hosted protection blocks force pushes and deletion on `main` (observed 2026-11-11, not a current guarantee). Review cue: a forced update or deletion that no Task records.
- **A feature branch or tag is deleted by a `:<ref>` refspec without a prompt.** Possible, Moderate: MEDIUM, accept and record. Owner: platform. No pattern can express it. The option forms that a pattern can express stay denied, the pushing checkout keeps the branch and its reflog (reflog expiry and pruning stay denied), and git.md lines 67-69 still require explicit approval. Review cue: a missing remote branch or tag.
- **Allowed commands run working-tree code without a prompt.** Possible, Severe: HIGH, accept and record. Owner: platform. This covers the release producer and the Git hooks that commit, push and merge run. Both are repository files under review and exact-index QA. An edit to `scripts/release.py` or a hook belongs to its own reviewed change before it is run. Review cue: a diff to either surface in the same change as its use.
- **A direct push to `main` through a form the deny list misses.** Unlikely, Severe: MEDIUM, mitigate. Owner: platform. The implicit-destination, `@`, `heads/main` and option-only denies cover the forms a checkout on `main` makes most easily. Hosted protection was observed on 2026-11-11 but is not a current guarantee. Review cue: a `main` commit that no pull request introduced.
- **Agents meet over-denial.** Likely, Minor: LOW, accept. A bare push from a feature branch, a branch name containing a denied fragment, or a commit message containing a flag's text is refused; the agent names the branch, renames it, or rewords the message.
- **A Release is published on an ambiguous request.** Unlikely, Severe: MEDIUM, mitigate. Owner: operator. The amended rule and runbook require a request that names the version and assets, a producer run, and a Task record with a read-back. The producer refuses a non-`main` source, a tag collision and changelog drift.
- **The client matches rules differently from the model.** Possible, Moderate: MEDIUM, monitor. Owner: platform. The evidence is labelled repository-static; an optional new-session probe records runtime matching.
- **The git.md edit conflicts with SPEC-0199.** Likely, Minor: LOW, mitigate. Owner: platform. Apply the rebase rule above.
- **The Claude and Codex difference is misread.** Possible, Minor: LOW, mitigate. The git.md subsection and the Codex parity sentence say where Codex is stricter and where Claude denies more.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` only with its approval receipt. No hosted or runtime claim is made from repository-static checks.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| One release producer: who may publish (the owner, or an agent on the owner's request naming the version) and how a Release stays traceable (Task record of the request, command, tag, target SHA and read-back) | [Git Policy](../../../.agents/governance/git.md) | `#### Release ownership` |
| Agent delivery boundary: delivery commands allowed on the user's request, which binds one operation and one subject; forced merge and direct pushes to `main` forbidden outright; other protected Git operations kept under their existing approval rules; Claude settings, Codex approval and hosted protection kept as separate layers | [Git Policy](../../../.agents/governance/git.md) | `#### Agent delivery commands` |
| Executor of the release producer's `publish --execute` | [Main release preparation runbook](../../05.operations/runbooks/0012-main-release-preparation-runbook.md) | Preconditions, Authority and Access, and the `--execute` step |
