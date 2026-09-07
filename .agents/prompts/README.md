---
title: "Common Prompt Contracts"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-07"
---
# Common Prompt Contracts

## Overview

Repeatable authoring requests reach an agent as prose retyped per session, so
their inputs and their refusal conditions cannot be validated. This surface
gives each such request a contract: what it needs, how that input is produced,
what shape the answer takes, and when no answer is produced.

## Scope

A contract identifier is its file stem. Each contract states required inputs
with the exact read-only command that produces each, the output shape, the
validation applied to a produced draft, and the conditions under which it
refuses. It states no permission and no approval boundary; those keep their
owners in the agent registry and the approval policy.

The consumer is [`scripts/prompt-input.py`](../../scripts/prompt-input.py),
which assembles the declared inputs and writes the request to standard output.
It makes no model call and no network access, and it writes nothing to the
repository or to Git state. A produced draft is transient output the user
accepts, edits or discards.

## Item Index

- [handoff](handoff.md): assemble a work handoff from the fields the quality
  policy already owns.
- [change-review](change-review.md): assemble a review request over a local
  difference.
- [commit-message](commit-message.md): assemble a commit-message draft request
  from the staged difference only.
- [doc-update](doc-update.md): locate the canonical owner for a change and
  request a proposed difference against it.

## Add and Find

1. Read [document authoring](../governance/document-authoring.md) and select
   the prompt profile from the Stage 99 registry before adding a contract.
2. Confirm the identifier does not collide with an existing skill identifier or
   command entry point.
3. Declare only read-only commands as inputs. A contract that declares a
   command which writes to the repository or changes Git state is rejected.
4. State refusal conditions explicitly. A contract with no refusal condition
   produces a draft describing nothing when its input is empty.
5. Index every new contract in the Item Index above.

## Related Documents

- [Governance Hub](../README.md)
- [Quality and Evidence Policy](../governance/quality.md)
- [Approval and Safety](../governance/approval-and-safety.md)
- [Scripts](../../scripts/README.md)
