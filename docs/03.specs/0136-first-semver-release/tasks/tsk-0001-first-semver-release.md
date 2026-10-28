---
title: "First SemVer Release"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0136-TSK-0001"
parent_ids: ["SPEC-0136-PLAN-0001"]
---

# Task: First SemVer Release

## Overview

Prepare and record the first SemVer release, `v0.1.0`, under RUN-0012. It
executes [SPEC-0136](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose `v0.1.0` for the first SemVer
  release.
- Start: main `65f1f4e7`, branch `release/v0.1.0`.
- Dependency: the `0.1.0` section exceeds GitHub's 125,000-character Release
  body limit, so `publish --execute` waits until
  SPEC-0137 (PR #192, `fix/release-body-limit`) is on `main`.

### Release Scope

Observed on main `65f1f4e7`. No `v*` tag exists. Nine historical
`main-<SHA>` tags exist; the latest, `main-3ff0ab62`, is from 2026-10-06 and
stays as history. Since that tag, 349 non-merge commits are on `main`
(`git log --no-merges main-3ff0ab62..65f1f4e7`): 234 `docs`, 44 `fix`, 20
`refactor`, 16 `feat`, 15 `chore`, 14 `test`, 4 `ci`, 1 `style` and 1 `docs!`.
Two are breaking: `docs(platform)!: adopt external data contract alignment`
and `refactor(qa): consolidate local validation and SemVer delivery`, whose
`BREAKING CHANGE:` footer retires the `ciJobs` entry and the `--partition`
mode. Because no `v*` tag exists, the `0.1.0` notes cover the whole repository
history, not only these commits.

| Public interface | Change class in this release |
| --- | --- |
| Supported CLI and options (`scripts/qa.py`, `scripts/release.py`, validators) | Added and changed; the `qa` `--partition` mode was removed |
| JSON Schema and registries | Changed |
| Document profiles and frontmatter | Changed |
| GitOps desired state | Changed, including the Traefik ingress cutover |
| External service interfaces | Changed by the marked breaking data-contract alignment |

As the first `0.y` release, `v0.1.0` makes no compatibility promise: any
public interface may change in a later `0.y` release.

### Tool Environment

On 2026-10-28 the first `prepare` preview stopped with
`RELEASE-TOOL-UNAVAILABLE` for `git-cliff`. The only installed copy is the
npm package under the user's NVM directory, outside the trusted system and
`~/.local/bin` locations that `scripts/run-validation-lane.py` accepts. The operator then installed that package's native
binary at `~/.local/bin/git-cliff` (`git-cliff 2.14.2`), which the resolver
accepts.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | Review the release scope and compatibility | platform | completed | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-SR-002](../spec.md#success-criteria--verification-plan) | Write the changelog section with the release tool | platform | completed | PASS | EVD-006 closes EVD-002 |
| WORK-003 | [VAL-SR-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | completed | PASS | EVD-009 closes EVD-003 |
| WORK-004 | [VAL-SR-004](../spec.md#success-criteria--verification-plan) | Record the publish preview and outcome | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Scope review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Release tool output and staged QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-SR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-SR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Publication observation | Exact main commit | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Scope review | Main `65f1f4e7`: `git tag`, commit-type counts since `main-3ff0ab62`, the breaking-change search, and the operator's version choice | PASS | Release Scope above: no `v*` tag, 497 commits, one marked breaking change, five public interface classes changed, and `v0.1.0` with no compatibility promise | yes | EVD-001 |
| EVD-006 | [VAL-SR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Release tool output and staged QA | Branch `release/v0.1.0` at `20527f43`: `python3 scripts/release.py --root . prepare --version v0.1.0 --initial-version`, then the same with `--write` | PASS | The preview and the write both reported 143862 bytes with SHA-256 `8b0810a3f38c6580e7433eeea124f9c5cbc9cd96712fcd3c4ac7ee7cf54e78bb`; `CHANGELOG.md` holds the `0.1.0` section dated 2026-10-28 under eleven headings, including Breaking Changes; staged QA runs on this commit | yes | EVD-002 |
| EVD-007 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Scope review | PR #191 independent review of `3960b995` | FAIL | EVD-005 stated 497 commits where `git log --no-merges main-3ff0ab62..65f1f4e7` gives 349, and named one breaking change where the notes list two; the review also found the 143,352-character notes exceed GitHub's 125,000-character Release body limit, which `publish` does not handle | yes | none |
| EVD-008 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Scope review | PR #191 re-review of `26b0543b`: `git log --no-merges main-3ff0ab62..65f1f4e7` and the two breaking commits `620e8f1b` and `7523ece4` | PASS | The Release Scope states 349 commits with the command, both breaking changes and that the notes cover the whole history; it supersedes the 497 count and single breaking change in EVD-005. The body limit is deferred to SPEC-0137 before publication | yes | EVD-007 |
| EVD-009 | [VAL-SR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | PR #191 independent review of `3960b995`, re-reviews of `26b0543b` and `ac590955`; heads `3960b995` (CI run `40646300977`), `26b0543b` (CI run `40647453961`) and `ac590955` (CI run `40652560974`) | PASS | The reviewer regenerated the `0.1.0` section byte-identically with git-cliff, matched the SHA-256, spot-checked entries against commits and approved after the scope corrections; `ci-summary`, `style-pr`, `label` and GitGuardian passed on each head | yes | EVD-003 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SR-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Accepted by the operator on 2026-10-28 | platform |
| [VAL-SR-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Accepted by the operator on 2026-10-28 | platform |
| [VAL-SR-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-009 | Accepted by the operator on 2026-10-28 | platform |
| [VAL-SR-004](../spec.md#success-criteria--verification-plan) | pending | none | Publication remains | operator |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md` and
  `CHANGELOG.md`.
- **Forbidden Paths**: historical tags, release tooling, validators and
  workflows.
- **Approval Required**: the operator chose `v0.1.0` on 2026-10-28. Push,
  pull request and merge follow RUN-0013. Tag and Release publication is the
  operator's `publish --execute`.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: none; a release proves no deployment.
- **Secret / Vault Handling**: no secret is read; publication uses the
  operator's own GitHub authority.
- **Rollback Plan**: revert the pull request before publication. After
  publication, a published tag is not moved; a later release supersedes it.
- **Evidence Location**: this Task.
- **Acceptance**: on 2026-10-28 the operator accepted VAL-SR-001 to
  VAL-SR-003. VAL-SR-004 waits for publication after SPEC-0137 is on `main`.

## Verification Summary

WORK-001 passed (EVD-008, closing EVD-007): 349 commits since `main-3ff0ab62`,
two breaking changes, no `0.y` compatibility promise. WORK-002 passed
(EVD-006): the release tool wrote the `0.1.0` section, regenerated
byte-identically in review. WORK-003 passed (EVD-009). The operator accepted
VAL-SR-001 to VAL-SR-003. WORK-004 remains: after this pull request and
SPEC-0137 merge, the operator runs the `publish` preview and `--execute` on
`main`, and this Task records the tag and Release or a `DEFER`.
