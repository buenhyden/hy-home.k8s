---
title: "Provider Native Permission and Hook Hardening"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0114"
---

# Provider Native Permission and Hook Hardening Technical Specification (Spec)

## Overview

On 2026-10-13 the operator asked whether `.agents`, `.claude` and `.codex`
fulfil their roles, and to harden `.claude/settings.json` permissions and
hooks and `.codex/config.toml` and its hooks. A read-only review on main
`3897353e` found the governance structure sound: the governance validator
passes, all 17 roles have a neutral owner and one projection per provider,
and no provider file copies policy. The defects are in native controls:

- Claude permission rules match command text from its first character
  (code.claude.com/docs/en/permissions), so option-first and positional
  forms escape the current deny list, and secret paths and secret-printing
  commands are not denied.
- The shared write guard ignores `NotebookEdit`, reports some blocks on
  stdout where the model does not read them, and fails open on any exit
  other than 2, on timeout, and on a Codex session started outside the
  repository; a heredoc `apply_patch` run through Bash skips patch checks.
- The project Codex config sets only memories. Current Codex documentation
  gives `ignore_default_excludes` a default of true, so secret-named
  environment variables reach shell commands, and no project rules mirror
  the Claude deny list.

The operator chose to allow push, pull request creation and merge on
Claude, with `--admin` merges denied, and to allow network access in the
Codex workspace sandbox. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-provider-permission-hardening.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - Claude deny additions for secret reads and output, option-first
    cluster and tool mutation, and deletion and history destruction;
  - Claude allow for read-only Git and GitHub commands, `git push`,
    `gh pr create`, `gh pr merge` and `git merge`; ask for `gh api` and
    `git -C`; `disableBypassPermissionsMode`;
  - the shared write guard and both hook adapters: `NotebookEdit` and
    `notebook_path`, block reasons on stderr, fail-closed adapters, a
    realistic timeout, Bash-carried patch envelopes, and a Codex hook path
    that does not depend on the session directory;
  - Codex project `approval_policy`, `sandbox_mode`, workspace network,
    `[shell_environment_policy]`, and `.codex/rules/default.rules`;
  - validator constants and tests, provider notes and READMEs, REQ-0003
    links, and session probes.
- Non-goals:
  - an operating-system sandbox for Claude;
  - personal, user-level or managed settings and project trust;
  - trimming the dated evidence chronology in `.codex/provider.md`;
  - changing the approval policy: an operator request remains the approval
    for push, pull request and merge, and allow only removes the native
    prompt.

## Contracts

- No existing Claude deny entry is removed and no wildcard allow such as
  `Bash(*)` is admitted; validators keep exact equality of the native
  lists and the Codex config.
- Every added deny or forbidden rule names a concrete escape it closes.
  Pattern limits that remain (refspec `:branch` deletion, `git -C`
  variants, programs that open files themselves, shell scripts that a
  prefix rule sees as one argv) are residual risk, never claimed covered.
- A hook adapter that cannot run the guard, or a guard that fails
  unexpectedly, blocks the call with a reason on stderr.
- Repository-declared settings are not runtime evidence. Enforcement claims
  cite a session probe that uses dry-run or missing targets only.

## Core Design

`scripts/validate-agent-governance.py` owns the Claude permission
constants, the Codex config constant and the hook checks.
`scripts/provider_write_guard.py` owns the boundary both adapters forward
to. Each work unit changes the native file, its validator constant and a
focused rejection test together. Codex rules use `prefix_rule` with
`decision = "forbidden"`; the validator pins the rules file.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

- Claude deny additions: `Read(./secrets/**)`, `Read(~/.kube/**)`,
  `Read(~/.ssh/**)`, `Read(~/.vault-token)`, `Read(~/.config/gh/**)`,
  `Read(~/.claude/.credentials.json)`, `Read(~/.codex/auth.json)`,
  `Read(//proc/*/environ)`; `gh auth token`, `vault print token`,
  `kubectl` raw access, `k3d kubeconfig`, `kubectl * secret`,
  `helm get values`, `export -p`, `declare -x`, `declare -p`;
  option-first `kubectl * <verb> *` for each denied verb plus `cp`, `debug`,
  `attach`, `run`, `proxy`; helm `install`, `upgrade`, `uninstall`,
  `delete`, `rollback`; Vault `kv delete`, `kv destroy`,
  `kv metadata delete`, `delete`, `secrets disable`, `policy write`,
  `token create`, `login`; Argo CD option-first `app sync` and
  `app delete`, `app rollback`, `account generate-token`, `cluster rm`;
  `k3d * delete`, `k3d cluster stop`; recursive and force removal
  variants, `find * -delete`, `sudo`; positional `git push` force, delete,
  mirror and prune; forced `git branch` deletion; forced `git checkout`
  and `git switch`; `git stash drop` and `clear`; `git filter-branch`,
  `git filter-repo`, `git update-ref -d`, `git reflog expire`,
  `git gc --prune`, forced `git worktree remove`, `git config --global`;
  `gh secret`, `gh variable`, `gh repo delete`, `gh repo edit`,
  `gh release delete`, `gh run cancel`, `gh pr merge * --admin`.
- Claude allow additions: `git log`, `git show`, `git fetch`,
  `git ls-remote`, `git push`, `git merge`, `gh pr view`, `gh pr checks`,
  `gh pr list`, `gh pr diff`, `gh pr create`, `gh pr merge`, `gh run view`,
  `gh run list`. Ask: `gh api`, `git -C`.
- Claude hook matcher `Bash|Write|Edit|MultiEdit|NotebookEdit`; Codex
  matcher unchanged (`Bash|apply_patch`); both timeouts raised to cover the
  guard's bounded Git and selector calls.
- Codex config adds `approval_policy = "on-request"`,
  `sandbox_mode = "workspace-write"`,
  `[sandbox_workspace_write] network_access = true` and
  `[shell_environment_policy] inherit = "core"`,
  `ignore_default_excludes = false`.
- `.codex/rules/default.rules` forbids the same command families as the
  Claude deny list, in argv-prefix form.

## Edge Cases & Error Handling

- A deny may block a harmless command such as a forced removal of one
  file; the agent then uses a narrower command or asks the operator.
- A Codex key the installed `codex-cli 0.162.1` rejects is removed and
  recorded rather than kept as a claim.
- If a probe shows a rewriting hook or wrapper bypasses a rule, the Task
  records it and that criterion is not accepted.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert of the package commits; the validators then
require the previous native files again. Codex project files apply only to
a trusted project; the operator owns that trust and hook re-trust.

## Verification Commands

- `python3 -m unittest tests.test_agent_governance tests.test_provider_write_guard`
  from the documented validation environment (test module names follow
  the repository).
- `python3 scripts/validate-agent-governance.py`.
- `codex execpolicy check --pretty --rules .codex/rules/default.rules -- <cmd>`
  for each forbidden family.
- `"$VALIDATION_VENV/bin/python" scripts/qa.py staged` per logical commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-PERM-001 | Claude secret read and secret-output denies are present; a test rejects their loss; a session probe is refused. |
| VAL-PERM-002 | Option-first cluster and tool mutation denies are present; a test rejects their loss; a namespaced `kubectl` delete probe is refused. |
| VAL-PERM-003 | Deletion and history-destroying denies are present; a test rejects their loss; a forced recursive removal of a missing path and a dry-run positional branch-delete push are refused. |
| VAL-PERM-004 | The named read-only, push, pull request and merge commands are allow, `--admin` merge is denied, `gh api` and `git -C` are ask, bypass mode is disabled, and tests still reject a wildcard allow. |
| VAL-PERM-005 | The guard checks `NotebookEdit` paths and Bash-carried patch envelopes, prints block reasons on stderr, and both adapters block on guard failure or a missing interpreter; each case has a failing-then-passing test. |
| VAL-PERM-006 | The Codex config sets approval, sandbox, network and environment filtering, the validator pins it, and the installed client accepts it. |
| VAL-PERM-007 | `.codex/rules/default.rules` forbids the Claude deny families; `codex execpolicy check` reports `forbidden` for each family and the validator pins the file. |
| VAL-PERM-008 | The Codex hook resolves the guard without the session directory and blocks when it cannot; a test covers a session outside the repository. |
| VAL-PERM-009 | Provider notes and READMEs describe the lists, the probe results and the residual limits, and REQ-0003 links SPEC-0114. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-001 | Secret guardrail; validator, test and probe. |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-002 | No live mutation without operator action; validator, test and probe. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-003 | Forbidden actions have direct negative tests and probes. |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-004 | Approval and oversight stay with the operator; exact lists. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-005 | Fail-closed guard with direct negative tests. |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-006 | Secret environment and sandbox guardrail on Codex. |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-007 | Native claims kept per provider; execpolicy check. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-008 | Missing-root fallback is a direct negative test. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PERM-009 | Repository-declared and runtime evidence kept apart. |
