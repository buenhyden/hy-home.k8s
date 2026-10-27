---
title: "Single Main Trunk Branch Strategy"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-10-27"
layer: "architecture"
artifact_id: "ADR-0052"
---

# ADR-0052: Single Main Trunk Branch Strategy

## Overview

This repository keeps one long-lived branch, `main`, and develops each change
on a short-lived feature branch that merges back through a reviewed pull
request. It adds no `dev` integration branch and no long-lived release
branch. The decision records an evaluation the repository did not have: the
existing rules said how to use `main`, not why `main` alone is enough.

## Context

On 2026-10-27 the only long-lived branch on GitHub is `main`; the others
are open feature branches. Each Spec package is
developed on an owned feature branch, often in a linked worktree, and merged
when `ci-summary`, `style-pr` and `independent-review` pass
([Git policy](../../../.agents/governance/git.md)). One operator works with
agents as additional concurrent writers.

Three facts bound the choice:

- **Deployment follows `main`.** Twelve Argo CD declarations track
  `targetRevision: main` with automated sync, so a merge to `main` is the
  deployment ([ADR-0029](0029-mutable-target-revision-retention.md)). A
  separate integration branch would either deploy nothing or need its own
  cluster.
- **Releases are tags on reviewed `main` commits.** `scripts/release.py` is
  the only producer of SemVer tags and GitHub Releases, bound to an exact
  reviewed `main` commit ([ADR-0048](0048-local-qa-and-semver-release-ownership.md)).
  No version is supported in parallel with another.
- **Review already happens per branch.** Each feature branch carries its own
  Spec, Task evidence, hosted checks and independent review before merge.

The sources read on 2026-10-27 agree on when a long-lived integration branch
pays off. [Trunk-Based Development](https://trunkbaseddevelopment.com/)
recommends one trunk and short-lived branches, with release branches cut
just in time only when needed. [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
is branch, pull request, review, merge and delete. Driessen's
[git-flow](https://nvie.com/posts/a-successful-git-branching-model/) uses a
long-lived `develop` and release branches, and its 2020 note recommends a
simpler workflow for continuous delivery and keeps git-flow for explicitly
versioned software with several supported versions.

## Decision

Keep `main` as the only long-lived branch. Develop on short-lived feature
branches, one per independently reviewable Spec package, merge them through
pull requests, and delete them after merge. Cut a release branch only when a
released version needs a fix that `main` cannot carry, and delete it after
that release. The short-lived `release/<tag>` preparation branch that
`scripts/release.py` opens for every release pull request is a feature
branch in this sense and is not affected.

## Explicit Non-goals

- Changing branch protection, rulesets or required checks.
- Changing the deployment model decided in ADR-0029 or the release producer
  decided in ADR-0048.
- Prescribing branch name prefixes.

## Consequences

- One integration point: a merged change is the deployed and releasable
  state, so there is no second branch to keep in sync or to merge twice.
- Review cost stays per change. A long-lived `dev` branch would add a second
  review and merge for every change with one operator, and its conflicts
  would surface later.
- No staging of several changes before deployment. A change that must not
  deploy yet stays on its feature branch or is disabled in its manifest.
- A hotfix to an older release has no standing branch; it needs a
  just-in-time release branch, which has not been needed.

Reopen this decision when a second operator or environment is added, when
two released versions must be supported at once, or when ADR-0029 is
reopened.

## Alternatives

- **A long-lived `dev` integration branch (git-flow).** Rejected: no
  environment deploys it, every change would merge twice, and its source
  recommends it for parallel supported versions, which this repository does
  not have.
- **Permanent release branches.** Rejected: releases are tags on reviewed
  `main` commits, and no released version is maintained separately.
- **Direct commits to `main`.** Rejected: the Git policy merges every change
  through a pull request after hosted checks and independent review, and
  feature branches carry the Spec and Task evidence.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| N/A — first branch-strategy decision; ADR-0029 and ADR-0048 constrain it as stated in Context | Supersedes no decision | [SPEC-0127](../../03.specs/0127-adr-lineage-and-branch-strategy/spec.md) |
