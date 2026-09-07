---
title: "Commit Message Prompt Contract"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-09-07"
---

# Commit Message Prompt Contract

## Overview

Identifier `commit-message`. Assemble the request that produces a Conventional
Commit draft for work already staged. The draft is a proposal the user accepts,
edits or discards; nothing in this contract commits, amends or stages.

## Authority Boundary

This contract shapes a request. It grants no permission to commit, and it does
not restate the Git policy that owns commit scope and history rules. The
builder that reads it runs only the commands named below.

## Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Staged difference | `git diff --cached` | The subject of the message; the working tree is deliberately excluded |
| Staged path set | `git diff --cached --name-only` | Lets the draft name the owner boundary the change sits in |
| Current branch | `git rev-parse --abbrev-ref HEAD` | Supplies the active work context |

No other command is declared, and the builder runs no command outside this
list.

The subject input is `Staged difference`. When it is empty the contract
refuses and no draft is produced.

## Output

One Conventional Commit message: a `type(scope): summary` subject in the
imperative, and a body stating the reason when it is not obvious from the
subject. No trailing metadata is invented, and no evidence is claimed that the
staged difference does not show.

## Validation

The draft is judged by the repository's existing conventional-commit rule
before use. On this workstation that rule does not run at commit time, because
the global hook path points outside the repository; it runs inside the full
validation profile instead. The draft is not treated as validated by having
been produced.

## Refusal Conditions

- The staged difference is empty. No draft is produced, because a message
  describing nothing is worse than no message.
- A commit message the user has already written is present. The contract never
  rewrites an authored message.
- The request would require reading unstaged or untracked content to describe
  the change.

## Related Documents

- [Common Prompt Contracts](README.md)
- [Git Policy](../governance/git.md)
- [Prompt input builder](../../scripts/prompt-input.py)
