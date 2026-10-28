---
title: "First SemVer Release"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0136"
---

# First SemVer Release Technical Specification (Spec)

## Overview

The repository has never published a SemVer release; its nine tags are
historical `main-<SHA>` tags. On 2026-10-28 the operator chose `v0.1.0` as the
first release. This Spec prepares it under
[RUN-0012](../../05.operations/runbooks/0012-main-release-preparation-runbook.md)
and the release contract of
[SPEC-0107](../0107-local-qa-and-release/spec.md). The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-first-semver-release.md) records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index, the REQ-0003 trace link
  and the `v0.1.0` section that `scripts/release.py prepare --write` writes to
  `CHANGELOG.md`.
- Non-goals:
  - publishing the tag or GitHub Release, which is the operator's
    `publish --execute` step after this pull request merges;
  - moving or deleting a historical `main-<SHA>` tag;
  - claiming deployment or live validation; a release is the repository's
    public contract history only.

## Contracts

- `v0.1.0` is an initial development version: every public interface may
  change in a later `0.y` release, and no compatibility promise holds before
  `1.0.0`.
- The release notes are the `CHANGELOG.md` section the release tool writes from
  the reviewed `main` history; they are not edited by hand.
- The Task records the scope review, the tool environment, the preview and the
  publication outcome or its `DEFER` cause.

## Core Design

RUN-0012 steps 1 to 3 run in this pull request; steps 4 to 6 run on `main`
after it merges.

## Data Modeling & Storage Strategy

One versioned section in `CHANGELOG.md`.

## Interfaces & Data Structures

`python3 scripts/release.py prepare --version v0.1.0 --initial-version` and
the same with `--write`; later `publish --version v0.1.0 --initial-version`.

## Edge Cases & Error Handling

- The tool accepts `git-cliff` only from a trusted path; an untrusted install
  stops preparation with `RELEASE-TOOL-UNAVAILABLE`.
- A dirty worktree or another branch stops `prepare`.

## Failure Modes & Fallback / Human Escalation

If publication cannot run, the Task records `DEFER` with its cause and the
operator as next owner. Reverting this pull request removes the section.

## Verification Commands

- `python3 scripts/release.py --root . prepare --version v0.1.0 --initial-version`
- `python3 scripts/qa.py staged` on each commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SR-001 | The Task records the release scope, the compatibility classification and the operator's version choice. |
| VAL-SR-002 | `CHANGELOG.md` holds the `v0.1.0` section the release tool wrote on `release/v0.1.0`, and staged QA passes. |
| VAL-SR-003 | An independent reviewer confirms the scope and notes, and the pull request's hosted checks pass. |
| VAL-SR-004 | After merge, the Task records the publish preview and either the published tag and Release or a `DEFER` with its cause. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SR-001 | Scope review |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SR-002 | Release tool output and staged QA |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SR-003 | Review and hosted checks |
| [REQ-0003-FR-0029](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SR-004 | Publication observation |
