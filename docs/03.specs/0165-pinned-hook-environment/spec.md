---
title: "Pinned Hook Environment"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0165"
---

# Pinned Hook Environment Technical Specification (Spec)

## Overview

This approved change contract makes the workspace commit hooks run their Python checks with one pinned validation environment, whatever shell or session starts the commit. The workspace hook's `language: system` entries (`python3 scripts/qa.py staged`, `python3 scripts/commit-message-exceptions.py`) run `python3` from `PATH`. On this machine `PATH` finds a system Python with jsonschema 4.10.3, while the lock `.github/requirements/ci-validation.txt` pins 4.26.0, and the interpreter pre-commit recorded at install time (`/tmp/hyhome-r10-validation`) no longer exists. Results therefore depend on the caller's `PATH`; SPEC-0161 to SPEC-0164 could commit only with a session scratch environment first on `PATH`. The user chose this repository fix on 2026-11-12. The [Plan](plan.md) orders the work; [Task 0001](tasks/tsk-0001-pinned-hook-environment.md) records evidence and acceptance.

## Strategic Boundaries & Non-goals

- In scope: `scripts/githooks/chained-hook.sh` (including its trust-boundary header comment), `tests/test_chained_git_hooks.py`, the hook paragraph and frontmatter of `.agents/governance/git.md`, the dependency-identity section of `scripts/README.md`, this package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Pinned by this change: the interpreter and `pre-commit` that run the workspace hook, its `language: system` Python entries, `scripts/qa.py` and the Python gates it runs with its own interpreter. Not pinned: shell validators, whose `python3` follows the closed system `PATH` that `scripts/qa.py` builds (their library identity stays observed separately, as `scripts/README.md` says), and `language: python` hooks such as Commitizen, which use pre-commit's own environments.
- The environment stays outside the checkout in an account-owned directory, as `scripts/README.md` already requires; the dispatcher now enforces both.
- The global hook keeps the caller's `PATH`.
- Not changed: `.pre-commit-config.yaml`, the lock file, `scripts/qa.py`, hosted workflows, `scripts/validation/registry.json` (the dispatcher and its test already route to `git-hook-chain-regressions`), `core.hooksPath` handling and the global-then-workspace order.
- Not done by this change: creating the environment or setting the option on any machine. Each operator does that once; the Task records this machine's setup.
- No push, PR or merge without separate approval.
- Open question: none.

## Contracts

- When a workspace hook will run, the dispatcher reads `git config --path --get hyhome.validationVenv` before running any hook. Git configuration is never a tracked file. The read honors every caller-controlled scope (system, global, local, worktree, `-c` and `GIT_CONFIG_*`), none of which a commit under review can write. `git config --global hyhome.validationVenv <path>` is the documented setting.
- The dispatcher exits 2 with `HOOK-ENV` and a repair message, and runs no hook, in any of these cases:
  - the option is unset or empty, or the value is not absolute;
  - its `realpath` is missing, or equals or lies below (path-component boundary, not string prefix) a worktree listed by `git worktree list` for this repository;
  - `bin/python3` or `bin/pre-commit` is not executable;
  - any file or directory under the environment, other than symbolic links, or the resolved target of `bin/python3`, is owned by an account other than the invoking user or root, or has the group- or other-write mode bit. The check covers everything inside the environment, including `bin/pre-commit`, `pyvenv.cfg` and every file under `site-packages`.
- The repair message names the option and prints the setup commands with the absolute lock path: build the environment under `umask 022` (or run `chmod -R go-w` on it afterwards), install the lock with `--require-hashes`, and set the option.
- A read error other than "unset" exits with Git's status and `HOOK-CONFIG`, as the global `core.hooksPath` read does.
- When the setting is valid, only the workspace hook command runs with `<venv>/bin` prepended to `PATH`. The prefix is an environment assignment on that one command, so the dispatcher's own `git` and `realpath` and the global hook keep the caller's `PATH`.
- A `pre-push` with no workspace hook stays a no-op and does not read the option.
- Every other dispatcher contract is unchanged: order, first non-zero status, the pre-push payload, the missing and non-executable hook messages, recursion refusal and duplicate suppression.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; this change adds no component. The dispatcher is already the single entry for every hook (`scripts/githooks/{pre-commit,commit-msg,pre-push}`), so selecting the environment there covers all three. The generated `.git/hooks/pre-commit` runs `pre-commit` from `PATH` when its recorded interpreter is missing, so the prefix also selects the pinned pre-commit; everything the workspace hook starts inherits the prefix. Ownership and mode are read from mode bits with GNU `find` (`-perm /022`, `-uid`), not `-w`, which is always true for root. The dispatcher already depends on GNU `realpath -e`, so this adds no portability loss.

## Data Modeling & Storage Strategy

One Git option, `hyhome.validationVenv`. No repository file stores machine paths.

## Interfaces & Data Structures

- Git option `hyhome.validationVenv`: absolute path of a virtual environment built from `.github/requirements/ci-validation.txt` with `--require-hashes`.
- Diagnostics: `[git hook] HOOK-ENV: …` (exit 2) and `[git hook] HOOK-CONFIG: …` (Git's status).

## Edge Cases & Error Handling

- `~` in the value is expanded by `git config --path`; a symlinked environment is checked at its resolved path; paths with spaces or non-ASCII characters are quoted everywhere.
- A local `include.path` could pull the option from a tracked file; that needs an operator opt-in, and the value must still name an environment outside every worktree, owned by the invoking user or root.
- Limits, recorded and not checked: the dispatcher does not prove that the environment matches the lock (a stale environment passes until it is rebuilt); the parent directories of the environment are not checked; a check-then-exec gap remains for an owner-only directory; a recorded `INSTALL_PYTHON` that still exists runs pre-commit with that interpreter, although the hook entries still find `python3` under the prefix.
- Further limits: the base interpreter's standard and system libraries are outside the environment and not checked; symbolic links inside it are skipped, not followed; on a machine with `umask 002`, `__pycache__` files Python writes later are group-writable, so a later commit is refused until `chmod -R go-w` is run again, and the repair message says so.

## Failure Modes & Fallback / Human Escalation

A broken or missing environment blocks the commit with the repair commands; the operator rebuilds it from the lock. Unsetting the option also blocks, so it is no way around a check. Disabling a hook or changing `core.hooksPath` to pass a check stays forbidden (Git policy).

## Verification Commands

- `python3 -m unittest tests.test_chained_git_hooks`, with the new cases failing before the dispatcher change and passing after. The existing cases gain a valid synthetic environment in `setUp` (`bin/python3` a symbolic link to the test's own interpreter, `bin/pre-commit` an executable stub) and keep their assertions. New cases:
  - the workspace hook sees `<venv>/bin` first on `PATH`;
  - the global hook's `PATH` is unchanged;
  - unset, empty, relative, missing, inside the checkout, inside another worktree, no `bin/python3`, no `bin/pre-commit`, group-writable and other-writable directory, `bin`, `bin/pre-commit` or a file under `site-packages`, a 775 environment as `umask 002` builds it, and a foreign owner each exit 2 with `HOOK-ENV` and run no hook;
  - a sibling path that shares the checkout's name as a string prefix is accepted;
  - a symlinked environment, `~` expansion, and a path with spaces and non-ASCII characters work;
  - a `git` shim for `config` gives `HOOK-CONFIG`;
  - `pre-push` with no workspace hook needs no option;
  - `commit-msg` gets the prefix.

  Mode cases set mode bits; the foreign-owner case uses a `find` shim, so no case depends on running as non-root.
- The `git-hook-chain-regressions` gate (`python3 tests/test_chained_git_hooks.py`), selected for the dispatcher and its test by `scripts/validation/registry.json`.
- `bash -n scripts/githooks/chained-hook.sh` and the shell checks selected by `python3 scripts/qa.py staged`.
- A real commit on this machine with the option set and the scratch environment removed from `PATH`; the Task records the interpreter and jsonschema version the hook's `python3` reports.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-HOOKENV-001 | Every dispatcher case listed in Verification Commands fails before the change where it is new, and passes after it, with the existing assertions unchanged. |
| VAL-HOOKENV-002 | `git.md` and `scripts/README.md` state the option, the setup from the lock, the trust boundary and the pinned and unpinned sets; exact-index QA and the commit hooks pass on a commit made with the option set and no scratch environment on `PATH`, and the hook's `python3` reports jsonschema 4.26.0. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HOOKENV-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Synthetic dispatcher tests. |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-HOOKENV-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Owner text, exact-index QA and a real commit. |
