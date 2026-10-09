---
title: "Commit Message Prompt Contract"
version: "0.2.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-09-08"
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
imperative, with optional scope. Use `type!:` or `type(scope)!:` only when the
staged change actually breaks the public contract; a
`BREAKING CHANGE:` or `BREAKING-CHANGE:` footer can describe that impact.
Unicode subject text is allowed. The subject must contain nonblank text and
must not end with a period or contain a carriage return. Include a body for a
reason not obvious from the subject. Invent no trailing metadata or evidence
the staged difference does not show.

## Validation

The draft is judged by Commitizen using [`.cz.toml`](../../.cz.toml).
Generation is not validation. Selected staged file QA checks the exact index;
the separate commit-msg check validates the actual candidate message. A PR
title or hosted `style-pr` result is no substitute for that check, including
when a squash message is proposed. Follow
the [Git policy](../governance/git.md)
for validating the actual candidate message and observing active hooks;
workstation configuration is Task evidence, never a shared policy assumption.

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
