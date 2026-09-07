---
title: "Change Review Prompt Contract"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-09-07"
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

The subject input is `Local difference`. When it is empty the contract
refuses, because there is nothing to review.

## Output

An ordered finding list. Each finding names the file and line, states the defect
in one sentence, and gives the concrete condition under which it goes wrong. A
finding without a failure condition is a preference and is reported as such.

## Validation

Findings are checked against the changed files before they are acted on. A
finding that names a path outside the changed set, or that the diff does not
support, is discarded rather than reported.

## Refusal Conditions

- The difference is empty, so there is nothing to review.
- The request asks for a verdict on live cluster, hosted, or provider-runtime
  behavior, which a local difference cannot establish.
- The request asks to review content the approval boundary excludes from
  reading, such as credentials or environment dumps.

## Related Documents

- [Common Prompt Contracts](README.md)
- [Agent Responsibilities](../roles/README.md)
- [Quality and Evidence Policy](../governance/quality.md)
