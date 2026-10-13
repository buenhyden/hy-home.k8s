---
title: "Provider Native Permission and Hook Hardening"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0114-TSK-0001"
parent_ids: ["SPEC-0114-PLAN-0001"]
---

# Task: Provider Native Permission and Hook Hardening

## Overview

Execute the nine work units of the [Plan](../plan.md) for
[SPEC-0114](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0114](../spec.md) and its [Plan](../plan.md).
- Operator requests on 2026-10-13: allow the needed commands in
  `.claude/settings.json`; review deletion denies; review the whole
  permission set for security and risk; check that `.agents`, `.claude`
  and `.codex` fulfil their roles; review `.codex/config.toml` and both
  hooks and apply the changes. The operator chose to allow push, pull
  request creation and merge on Claude and network access in the Codex
  workspace sandbox. After the independent review on 2026-10-14 the
  operator chose to keep every push at ask and to turn the Codex workspace
  network off.
- Read-only reviews on main `3897353ebc815410eed2a3e3606d3cfa3149b97b`:
  the governance validator passed (17 roles, 18 skills, 51 projections);
  the write guard exited 0 for a `NotebookEdit` payload and for a
  Bash-carried `apply_patch` envelope.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | Claude secret read and secret-output denies | platform | completed | PASS | EVD-010 |
| WORK-002 | [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | Claude option-first cluster and tool mutation denies | platform | completed | PASS | EVD-011 |
| WORK-003 | [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | Claude deletion and history-destroying denies | platform | completed | PASS | EVD-012 |
| WORK-004 | [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | Fail-closed shared guard and adapters | platform | completed | PASS | EVD-013 |
| WORK-005 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | Claude allow, ask and bypass mode | platform | completed | PASS | EVD-014 |
| WORK-006 | [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | Codex config security keys | platform | completed | PASS | EVD-015 |
| WORK-007 | [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | Codex forbidden rules | platform | completed | PASS | EVD-016 |
| WORK-008 | [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | Codex hook path independent of the session directory | platform | completed | PASS | EVD-017 |
| WORK-009 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | Provider notes, READMEs, REQ-0003 links and session probes | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | WORK-004 commit index | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | WORK-005 commit index | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | WORK-006 commit index | NOT_RUN | Pending | yes | none |
| EVD-007 | [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Focused checks and staged QA | WORK-007 commit index | NOT_RUN | Pending | yes | none |
| EVD-008 | [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | WORK-008 | Focused checks and staged QA | WORK-008 commit index | NOT_RUN | Pending | yes | none |
| EVD-009 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Focused checks and staged QA | WORK-009 commit index | NOT_RUN | Pending | yes | none |
| EVD-010 | [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | New `NativeDenyCoverageTests` in `tests/test_agent_governance.py` checks each named escape against the tracked deny list with a matcher that follows the documented rule semantics (text from the first character, `*` anywhere, `:*` as a trailing space wildcard). Before the change it failed for eight secret paths (`secrets/`, kube, ssh, Vault token, gh config, Claude and Codex credentials, `/proc/*/environ`) and eleven secret-printing commands (`gh auth token`, `vault print token`, a raw kubeconfig view, raw API reads, `k3d kubeconfig get`, option-first and slash-form `kubectl` secret reads, `helm get values`, `export -p`, `declare -x`, `declare -p`). Session probes in this session after the change: the Read tool on `secrets/probe-none-spec0114` and `kubectl -n probe-none-spec0114 get secret none` were refused, but `cat secrets/probe-none-spec0114` and `cat .env.probe-none-spec0114` ran (the existing `Read(./.env.*)` rule did not stop them either; the output carried an RTK-style `(os error 2)` suffix, so a user-level rewrite is the likely cause, not verified because private user configuration was not read). Bash path denies (`* secrets/*`, `* ./secrets/*`, `* .env*`, `*/.env*` and the credential paths) were therefore added, and both `cat` probes were then refused. In total 28 deny rules were added to `.claude/settings.json` and `CLAUDE_REQUIRED_DENY_PERMISSIONS` together; the module and `validate-agent-governance.py` passed. `qa.py staged` on the WORK-001 index passed | PASS | This Task; WORK-001 commit | yes | EVD-001 |
| EVD-011 | [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | New `test_option_first_cluster_and_tool_mutation_is_denied` lists 72 escapes: every denied `kubectl` verb behind `-n` and `--context`, plus `cp`, `debug`, `attach`, `run` and `proxy`; helm release install, upgrade, uninstall, delete and rollback; Vault kv delete, destroy and metadata delete, delete, secrets disable, policy write, token create and login; option-first Argo CD sync and delete, rollback, account token and cluster removal; k3d node and registry deletion and cluster stop. All 72 failed before the change. Fifty-five deny rules were added to `.claude/settings.json` and `CLAUDE_REQUIRED_DENY_PERMISSIONS` together; the governance module and validator passed. Session probe after the change: `kubectl -n probe-none-spec0114 delete pod none --dry-run=client` was refused. `qa.py staged` on the WORK-002 index passed | PASS | This Task; WORK-002 commit | yes | EVD-002 |
| EVD-012 | [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | New `test_deletion_and_history_destruction_is_denied` lists 42 escapes: recursive and force removal variants including `sudo` and `find -delete`; positional force, lease, delete, mirror and prune pushes; forced branch deletion; forced checkout and switch; stash drop and clear; filter-branch, filter-repo, ref deletion, reflog expiry, pruning gc, forced worktree removal and global Git config; GitHub secret, variable, repository deletion and edit, release deletion, run cancellation and admin merge. All 42 failed before the change. Forty-five deny rules were added to `.claude/settings.json` and `CLAUDE_REQUIRED_DENY_PERMISSIONS` together; the governance module and validator passed. Session probes after the change: a forced recursive removal of the missing `./probe-none-spec0114` and a dry-run positional branch-delete push of the missing `probe-none-spec0114` were refused. A refspec `:branch` deletion cannot be expressed as a rule and stays residual risk. `qa.py staged` on the WORK-003 index passed | PASS | This Task; WORK-003 commit | yes | EVD-003 |
| EVD-013 | [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | New `FailClosedGuardTests` in `tests/test_k8s_pre_edit_hook.py` failed on all five cases before the change: a `NotebookEdit` payload for `/etc/x.ipynb` and a Bash heredoc carrying an `apply_patch` envelope for `/etc/x` both exited 0; the guard had no fail-closed entry for an unexpected error; the selector rejection reason went to stdout; and both adapters exited 127 when `dirname` and `python3` were absent, which the runtimes treat as non-blocking. After the change the guard reads `notebook_path`, treats any line that is exactly the envelope marker as a patch, reports `HOOK-SURFACE-SELECTION` on stderr, and `guarded_main` turns any exception into `HOOK-INTERNAL` exit 2; each adapter traps errors, checks `python3` and the guard, and exits 2 with `HOOK-ADAPTER`. The Claude matcher now includes `NotebookEdit`. The selector-bound test now also counts the four Git probe sites (25 s) and failed against the 10 s registrations; both registrations are now 30 s. The hook, governance and registry-generation tests and the governance validator passed. `qa.py staged` on the WORK-004 index passed | PASS | This Task; WORK-004 commit | yes | EVD-004 |
| EVD-014 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | New `test_delivery_commands_are_allowed_and_raw_api_asks` failed for all fourteen delivery commands and both ask commands, and new `test_bypass_permissions_mode_must_stay_disabled` errored, before the change. Allow now adds `git log`, `git show`, `git fetch`, `git ls-remote`, branch push, `git merge`, `gh pr view`, `gh pr checks`, `gh pr list`, `gh pr diff`, `gh pr create`, `gh pr merge`, `gh run view` and `gh run list`; ask is now `gh api` and `git -C`; `permissions.disableBypassPermissionsMode` is `disable`, and the validator's exact comparison includes it, rejecting its removal or `enable`. Force, lease, delete, mirror, prune and `--admin` forms stay denied (WORK-003), and deny is evaluated before allow. The existing tests that reject a wildcard allow and an ask moved to allow still pass. The governance and hook tests and the governance validator passed. `qa.py staged` on the WORK-005 index passed | PASS | This Task; WORK-005 commit | yes | EVD-005 |
| EVD-015 | [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | New `test_codex_project_config_keeps_sandbox_and_secret_filtering` errored before the change because the project config held only `[memories]`. `.codex/config.toml` now sets `approval_policy = on-request`, `sandbox_mode = workspace-write`, `[sandbox_workspace_write] network_access = true` (operator choice) and `[shell_environment_policy] inherit = core`, `ignore_default_excludes = false`, and keeps memories disabled; `CODEX_CONFIG` pins it and the test rejects `never`, `danger-full-access`, `ignore_default_excludes = true` and `inherit = all`. Client acceptance on `codex-cli 0.162.1` in this trusted checkout: with `sandbox_mode` set to a bogus value `codex features list` failed with `unknown variant` in `sandbox_mode` (rc 1), proving the project layer is parsed; with the committed file it exited 0. Unknown keys may be ignored silently, so the environment filter's runtime effect is not yet observed. The governance tests and validator passed. `qa.py staged` on the WORK-006 index passed | PASS | This Task; WORK-006 commit | yes | EVD-006 |
| EVD-016 | [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Focused checks and staged QA | New `.codex/rules/default.rules` forbids, as argv prefixes, the secret-output, cluster and tool mutation, deletion, history-destruction and GitHub mutation families that the Claude deny list covers. `codex execpolicy check` on `codex-cli 0.162.1` returned `forbidden` for 21 representative commands (token and kubeconfig output, secret reads, Helm values, kubectl delete and rollout restart, a Helm release upgrade, Vault kv destroy, Argo CD sync, k3d cluster deletion, forced recursive removal, sudo, hard reset, positional force and delete pushes, forced branch deletion, stash clear, gh secret and workflow run) and no match for an ordinary branch push, `gh pr merge` and `git status`. New `test_codex_forbidden_rules_are_pinned` failed before the validator change (a weakened, an appended and a missing file were all accepted); `CODEX_RULES_SHA256` now pins the file. Residual: option-first forms such as `kubectl -n x delete` and push forms with other remotes are not expressible as prefixes; the workspace sandbox and approval policy remain the primary Codex controls. `qa.py staged` on the WORK-007 index passed | PASS | This Task; WORK-007 commit | yes | EVD-007 |
| EVD-017 | [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | WORK-008 | Focused checks and staged QA | New `test_the_codex_registration_blocks_outside_the_repository` runs the registered Codex command through `/bin/sh -c` with a valid payload. Before the change, from a directory outside any Git checkout, `git rev-parse` failed and `bash /.codex/hooks/pre-tool-use.sh` exited 127, which Codex treats as non-blocking. The registration now resolves the adapter path, exits 2 with `HOOK-ADAPTER` when the file is missing, and otherwise execs the adapter; the test passes outside (exit 2) and inside the repository (exit 0). The command keeps one `.codex/hooks/` token, so the validator still resolves the tracked script. The hook and governance tests and the governance validator passed. A changed hook needs re-trust through Codex `/hooks` before it runs; that trust is the operator's. `qa.py staged` on the WORK-008 index passed | PASS | This Task; WORK-008 commit | yes | EVD-008 |
| EVD-018 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Focused checks and staged QA | `.claude/provider.md` (v1.6.0) states the SPEC-0114 permission model: deny first, text matching from the first character, option-first, positional push and Bash secret-path denies, the session observation that a `Read` deny did not stop `cat`, the delivery allow list, the `gh api` and `git -C` ask list, disabled bypass mode, the fail-closed hook, and the residual pattern limits. `.codex/provider.md` (v1.5.0) states the new config keys, the parse evidence, the unobserved environment filter, the pinned rules and their prefix limit, the fail-closed registration and the re-trust requirement. `.claude/README.md` and `.codex/README.md` (v2.4.0) list the bypass setting, the config contents and `rules/default.rules`. REQ-0003 links SPEC-0114 from FR-0007, FR-0008, FR-0025, FR-0026 and FR-0028 (draft commit). Session probes recorded in EVD-010 to EVD-012 were refused after their changes. Repository quality, governance tests and `qa.py staged` on the WORK-009 index passed | PASS | This Task; WORK-009 commit | yes | EVD-009 |
| EVD-019 | [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | WORK-005 | Automated security review follow-up | An automated security review flagged that the allowed Git commands accept executable-carrying options. Eight deny rules now block `--upload-pack`, `--receive-pack`, `--exec`, `--output` and the short `-u` forms of `ls-remote` and `fetch` anywhere after `git`; deny is evaluated before allow. Ten new cases in `test_deletion_and_history_destruction_is_denied` pass, and eight of them fail on a copy without the new rules. A rule for `ext::` transports was dropped because a pattern ending in `::*` reads as the legacy trailing `:*` form; `protocol.ext.allow` is unset on Git 2.43, so Git keeps that transport off by default. `qa.py staged` on the follow-up index passed | PASS | This Task; follow-up commit | no | none |
| EVD-020 | [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Independent security review and fixes | A read-only security review of `3897353e..fac4738f` reported three HIGH findings: flag-first and refspec pushes (`--force-with-lease`, `-fu`, `-d`, `--prune`, `origin +main`, `origin :feat`) and flag-first `gh pr merge --admin` were allowed on Claude, and Codex workspace network plus prefix-only rules let reordered destructive commands run without approval. Fixes in the review-fix commit: on the operator's decision every push moved from allow to ask and the Codex workspace network is off; `gh pr merge --admin`, flag-first lease, delete and prune pushes are denied; a Codex rule forbids `gh pr merge --admin` (`forbidden` by `codex execpolicy check`) and the rules digest was updated; the allow test now evaluates deny, ask and allow in order and failed for six commands before the change. LOW fixes: `guarded_main` maps every non-zero result to 2 and a 25 s `GUARD_DEADLINE_SECONDS` alarm turns a hung probe into `HOOK-TIMEOUT` below the 30 s registration; both adapters no longer `exec` the interpreter, so any non-zero guard exit reaches the ERR trap and blocks with `HOOK-ADAPTER`; three new tests failed before and pass after. Documentation now states that the Codex rules cover a subset of the Claude families and lists flag-first and refspec forms. Accepted as trade-offs and recorded: broad Bash secret-path denies block some routine commands (`git add secrets/README.md`, text naming `.env` after a space, `kubectl auth can-i create`), text-obfuscated paths (`cat .en?`, input redirection) and bare `export` or `set` are not matched, a line that is exactly the patch marker in a non-patch heredoc can be blocked, and a nested repository would supply its own Codex adapter. Hook, governance and registry tests, the validator and `codex features list` passed. `qa.py staged` on the review-fix index passed | PASS | This Task; review-fix commit | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PERM-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-010 | Accept the secret read and secret-output denies; Bash path denies close the observed Read-deny gap | platform |
| [VAL-PERM-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-011 | Accept the option-first cluster and tool mutation denies | platform |
| [VAL-PERM-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-012 | Accept the deletion and history-destroying denies; refspec deletion stays residual | platform |
| [VAL-PERM-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-014, EVD-019 | Accept the delivery allow list, the ask list and the disabled bypass mode | platform |
| [VAL-PERM-005](../spec.md#success-criteria--verification-plan) | accepted | EVD-013 | Accept the fail-closed guard and adapters | platform |
| [VAL-PERM-006](../spec.md#success-criteria--verification-plan) | accepted | EVD-015 | Accept the Codex sandbox, approval, network and environment settings; the filter's runtime effect stays unobserved | platform |
| [VAL-PERM-007](../spec.md#success-criteria--verification-plan) | accepted | EVD-016 | Accept the Codex forbidden rules; option-first forms stay residual | platform |
| [VAL-PERM-008](../spec.md#success-criteria--verification-plan) | accepted | EVD-017 | Accept the fail-closed Codex hook registration; re-trust stays with the operator | platform |
| [VAL-PERM-009](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-009 checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package; `docs/03.specs/README.md`;
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`;
  `.claude/settings.json`, `.claude/hooks/k8s-pre-edit.sh`,
  `.claude/provider.md`, `.claude/README.md`; `.codex/config.toml`,
  `.codex/hooks.json`, `.codex/hooks/pre-tool-use.sh`,
  `.codex/rules/default.rules`, `.codex/provider.md`, `.codex/README.md`;
  `scripts/validate-agent-governance.py`,
  `scripts/provider_write_guard.py`; their tests under `tests/`.
- **Forbidden Paths**: removal of any existing deny entry; personal,
  user-level or managed settings; project trust; workflows; live cluster,
  Vault and secret material.
- **Approval Required**: the operator approved SPEC-0114 and its Plan for
  implementation on 2026-10-13 after reviewing the draft at `94bc4965`;
  push, pull request and merge are run only on an operator request.
- **Static Validation**: governance and guard tests, the governance
  validator, `codex execpolicy check` and staged QA from the documented
  validation environment.
- **Live Validation**: DEFER — probes use dry-run or missing targets and
  touch no live surface.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
