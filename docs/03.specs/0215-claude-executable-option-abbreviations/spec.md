---
title: "Claude Executable Option Abbreviations"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0215"
---

# Claude Executable Option Abbreviations Technical Specification (Spec)

## Overview

This change contract closes a gap that SPEC-0214 opened. SPEC-0214 (completed; Git history, closure commit `83d3f5c1`) lets an agent run delivery commands, push among them, without a native prompt. The tracked `.claude/settings.json` denies the executable-carrying Git options by their exact names: `Bash(git *--upload-pack*)`, `Bash(git *--receive-pack*)` and `Bash(git *--exec*)` (lines 223-225 at `83d3f5c1`).

An automated security review on 2026-11-14 found that Git accepts any unique abbreviation of a long option. `--rece=`, `--e=`, `--ex=` and `--upl=` therefore reach the same options without matching those rules, and each can run an arbitrary program, for example against a local-path remote. The review rated the gap HIGH.

This package:

- appends five prefix denies;
- mirrors them in the validator pin;
- adds failing-first decision regressions;
- corrects the provider-note sentence that says executable-carrying options are denied.

The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-claude-executable-option-abbreviations.md) records execution.

## Strategic Boundaries & Non-goals

- In scope:
  - `permissions.deny` of `.claude/settings.json`, five appended rules, and nothing else in that file;
  - `CLAUDE_REQUIRED_DENY_PERMISSIONS` and its comment in `scripts/validate-agent-governance.py`;
  - the decision test in `tests/test_agent_governance.py`;
  - the executable-option sentence of the permission bullet in `.claude/provider.md` (line 62 at `83d3f5c1`), with the frontmatter `version`;
  - this package and the Stage 03 README entry.
- Not in this package:
  - every existing allow, ask and deny rule, which stays unchanged and in order;
  - `git pull` and `git clone`, which match no allow rule and keep the default prompt;
  - the Codex rules, configuration and provider note; hooks; `scripts/provider_write_guard.py`; workflows; remote settings;
  - `.agents/governance/git.md`, which does not state the executable-option rule;
  - any registry, so the Registry Schema Version is NO_CHANGE.
- Relation to SPEC-0214:
  - SPEC-0214 was finished and accepted before this finding.
  - The lifecycle check refuses an edit to a finished package's Spec or Plan (`LIFECYCLE-PACKAGE-EXIT` R4, `scripts/document_lifecycle.py` lines 1190-1199).
  - This fix is therefore its own package in the same pull request.
- No commit, push, PR or merge of this package without the user's approval.
- Open question: none.

### Decisions

The user's answers on 2026-11-14 (Asia/Seoul), verbatim:

1. "Fix before merge (Recommended)": deny the abbreviations before the SPEC-0214 pull request merges.
2. "New package, same PR (Recommended)": record the fix in a new package in the same pull request, because R4 refuses edits to SPEC-0214.

Derived by the drafter from those answers. These are for review and are not user decisions:

- Only the commands that an allow rule reaches need a prefix deny: push, fetch and ls-remote. Pull and clone keep the default prompt, and the generic `--upl` rule covers them as well.
- The exact-name rules stay, and the prefix rules complete them.

## Contracts

- **Deny list.** `permissions.deny` keeps its 257 rules unchanged and in order and appends these five, for 262 in total. The second rule is a push rule: its full text is `Bash(`, then the Git push command and a space, then the argument part `*--e*` and `)`. `.claude/settings.json` and the tests own the exact strings.

| Rule | Matches | Basis in the Git 2.43 `--help-all` lists |
| --- | --- | --- |
| `Bash(git *--rece*)` | `--receive-pack` from `--rece` on, in any position | push: `--[no-]receive-pack`; `--rec` also matches `--recurse-submodules` |
| the push rule with argument part `*--e*` | push `--exec` from `--e` on | push: `--[no-]exec`; no other push long option starts with `e` |
| `Bash(git *--upl*)` | `--upload-pack` from `--upl` on, for fetch, and for pull and clone, which are prompted anyway | fetch: `--up` also matches `--update-head-ok` and `--update-shallow`; pull: `--up` also matches `--update-shallow` |
| `Bash(git ls-remote *--u*)` | ls-remote `--upload-pack` from `--u` on | ls-remote: no other long option starts with `u` |
| `Bash(git ls-remote *--exe*)` | ls-remote `--exec` from `--exe` on | ls-remote: `--ex` also matches `--exit-code` |

- **Derivation.**
  - The option lists of the push, fetch, pull, clone and ls-remote commands were read from Git 2.43 `--help-all`, which also lists hidden options.
  - The shortest unique prefix was computed over every long option of each command, including the `--no-` forms.
  - No push or fetch was run with these options. The session's permission layer refuses push probes, and it was not routed around.
  - SPEC-0214's dry runs observed the abbreviation behavior itself: `--forc`, `--del`, `--prune-` and `--refm` were accepted, and `--for` and `--ref` were refused as ambiguous.
- **Matching model.** As in SPEC-0214, `_bash_rule_matches` (tests line 1123) matches a rule against the command text from its first character, and `*` matches any text.
  - Not denied, by design: `--recurse-submodules`, `--update-head-ok`, `--update-shallow`, `--exit-code`, and the negations `--no-receive-pack`, `--no-exec` and `--no-upload-pack`.
  - Over-denied, by design: a push whose text contains `--e` (a branch such as `feat/a--edit`); any Git command whose text contains `--rece` or `--upl`; an ls-remote whose text contains `--u` or `--exe`. Rename the branch or reword the text.
- **Residual risk.** The following are not covered:
  - A receive-pack or upload-pack program set in configuration (`remote.<name>.receivepack`, `remote.<name>.uploadpack`), which a plain push or fetch then runs. The rules see only the command text.
  - A quoted, escaped or variable option (`"--rece=sh"`, `$OPT`), as for every rule group.
  - Executable-carrying options of commands that no allow rule reaches. These keep the default prompt: clone `-u <path>`, `--u` and `--up`; archive `--exec` and its abbreviations.
  - `git merge -s <name>` runs a `git-merge-<name>` program found on `PATH`. The risk is low: the program must already exist, and the name cannot be a path.
- **Recorded checks.**
  - The independent review confirmed that `--output` on log and show is not abbreviable, so the exact deny `Bash(git *--output*)` is complete. A drafting probe that tried the abbreviation was refused by the session's permission layer and was not repeated.
  - The independent review checked the `git merge -s <name>` residual above: the strategy name selects a program on `PATH` and cannot carry a path.
- **Validator pin.** `CLAUDE_REQUIRED_DENY_PERMISSIONS` (line 134 at `83d3f5c1`) appends the same five rules at the end of the tuple. The comment above `CLAUDE_ASK_PERMISSIONS` adds executable-carrying option forms. No diagnostic, function or CLI option is added, and a mismatch stays `AGENT-NATIVE-PERMISSION`.
- **Provider note.** The `.claude/provider.md` sentence "Executable-carrying Git options (…) are denied" adds the denied abbreviations and the configured-program residual. The version goes from 1.9.0 to 1.9.1.
- **Failing-first regressions.** These are in `test_delivery_commands_are_allowed_and_raw_api_asks` (tests line 1277):
  - deny: push with `--rece=` and `--recei`; push with `--e=`, `--ex=` and `--exe`; fetch with `--upl=` and `--uplo`; pull with `--upl=`; ls-remote with `--u=`, `--up=` and `--exe=`;
  - over-denial asserted `deny`: a push of `feat/a--edit`;
  - allow guards: push with `--recurse-submodules=check`, fetch with `--update-shallow`, ls-remote with `--exit-code`;
  - against the settings before this change, the 12 deny expectations fail, because those settings decided `allow` or, for pull, the default prompt;
  - with the new pin and the old settings, `python3 scripts/validate-agent-governance.py --root .` exits non-zero with `AGENT-NATIVE-PERMISSION`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view. This change stays within it, and no component changes. As in SPEC-0214, the change is configuration plus its pin and tests: the tracked settings hold the single list, the validator holds the reviewed copy, and the tests decide commands with the matcher model. How a running Claude client matches the rules is separate runtime evidence (REQ-0003-FR-0009) and is not claimed.

## Data Modeling & Storage Strategy

No data changes. The settings file keeps its shape.

## Interfaces & Data Structures

No new interface. The validator CLI and its diagnostics are unchanged, and the test module stays in the `agent-governance` suite.

## Edge Cases & Error Handling

- A deny always wins over an allow or an ask.
- Git refuses an ambiguous abbreviation itself: push `--rec`, fetch `--up` and ls-remote `--ex`.
- The client judges a compound shell line, while the test model judges one command. The Task records only what the tests and the validator decide.

## Failure Modes & Fallback / Human Escalation

A later Git version can add an option that shares one of these prefixes. A prefix deny can then become an over-denial, or a prefix can become ambiguous. On a Git version change, rerun the derivation from `--help-all`. If an agent meets an executable-carrying option in a form no rule denies, it stops and asks the user. Rollback is a revert of the implementation commit: the five rules, the pin lines, the regressions and the provider-note sentence leave together.

## Verification Commands

- `python3 scripts/validate-agent-governance.py --root .`: fails first with the new pin and the old settings, then passes.
- `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`.
- The four strict document validators, `python3 scripts/validate-document-lifecycle.py --root . --mode staged` and `python3 scripts/validation/repository/quality.py --root .`.
- `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, `python3 scripts/qa.py staged` and the commit hooks on the exact index.
- Evidence limit: all of these are repository-static. They do not establish native rule matching.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-EXECOPT-001 | The deny list holds 262 rules: the 257 earlier rules unchanged and in order, plus the five prefix rules. The validator pin mirrors it, and the whole validator and the decision regressions fail first and then pass. |
| VAL-EXECOPT-002 | The decision regressions pass for every abbreviation, guard and over-denial case. The provider note states the denied abbreviations and the configured-program residual. The strict document validators, the repository quality check, ruff, exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EXECOPT-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Governance validator and decision regressions, failing first. |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EXECOPT-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Decision regressions, strict document validators, and review of the statement that keeps static and runtime evidence apart. |
