---
title: "Change Review Prompt Contract"
version: "0.3.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-11-19"
---

# Change Review Prompt Contract

## Overview

Identifier `change-review`. Assemble the request that produces a review of a
local difference before it is committed or handed off, so the same review lens
is applied each time instead of whatever the session recalls.

## Authority Boundary

A review lens is not write access. This contract selects what a reviewer reads;
the agent registry keeps permission classes and the approval policy keeps
protected actions. The contract names no reviewer role and grants none.

## Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Local difference | `git diff` | The subject of the review |
| Staged difference | `git diff --cached` | Separates what is already staged from what is not |
| Changed path set | `git status --porcelain` | Establishes the owner boundaries the change touches |
| Whitespace check | `git diff --check` | A defect class a reviewer should not have to find by eye |
| Staged paths | `git diff --cached --name-only` | The exact path set that the staged checks ran on |

The subject inputs are `Local difference` and `Staged difference`. When both
are empty the contract refuses, because there is no difference to review.

The requesting author also supplies, once, the review packet that Git cannot,
so the reviewer does not reconstruct it ([QUAL-R055](../../docs/00.workspace/04.quality/quality.md#requirements)):

- the branch and the commit the difference sits on, or the new commit once
  made, so a later change can be classified against it; a repository with no
  commit yet has none;
- the risk class and its reason (QUAL-R016);
- the acceptance IDs the change claims to meet;
- for a change to a governance, role, skill or provider file, its Kubernetes
  impact: the GitOps or infrastructure consumers whose behavior it changes, or
  `none`. Such a change may select only document checks (for example
  `.agents/governance/`), so the reviewer checks this statement against
  `gitops/` and `infrastructure/`;
- the check results already observed on the candidate commit, with their
  snapshot, which the reviewer does not rerun to repeat a PASS;
- for a re-review, the reviewed commit, the earlier findings and the
  `scripts/review_delta.py` result (QUAL-R054);
- the scope left unreviewed, such as live or provider behavior.

## Output

An ordered finding list, one finding per root cause. Each finding names the
file and line, states the defect in one sentence, gives the concrete condition
under which it goes wrong, and carries its grade under
[QUAL-R053](../../docs/00.workspace/04.quality/quality.md#requirements). A finding without a failure
condition is a preference and is reported as `NOTE`.

## Validation

Findings are checked against the changed files before they are acted on. A
finding that names a path outside the changed set, or that neither difference
supports, is discarded rather than reported.

## Refusal Conditions

The builder enforces only the empty-subject refusal; the requesting agent
enforces the remaining conditions below.

- Both differences are empty, so there is nothing to review. An untracked-only
  path set does not establish a reviewable difference.
- The request asks for a verdict on live cluster, hosted, or provider-runtime
  behavior, which a local difference cannot establish.
- The request asks to review content the approval boundary excludes from
  reading, such as credentials or environment dumps.

## Related Documents

- [Common Prompt Contracts](README.md)
- [Agent Responsibilities](../roles/README.md)
- [Quality and Evidence Policy](../../docs/00.workspace/04.quality/quality.md)
