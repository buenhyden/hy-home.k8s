# Governance Memory

## Overview

This directory holds reusable governance memory documents. It is not a current
policy, runtime, or task-status authority, and it holds no progress ledger.

## Scope

Record current status, commands, verification, and handoff in the owning Spec
Task, never here. A memory document holds durable context that outlives one
work unit and that no policy, skill, operating document, or reference owner
already owns.

The former progress ledger, `progress.md`, was retired under Spec 0054 WP-012.
It contradicted this README by instructing readers to append new-work status,
and it named a removed `harness-catalog.md` as current runtime truth. Its bytes
remain recoverable from Git through
[MIG-0007](../../98.archive/migrations/0007-agent-progress-ledger-retirement.md),
which carries its source commit, blob, and content digest.

## Item Index

This directory currently holds no memory document. Add one only when the
durable-context test in `## Scope` is met.

## Add and Find

Route durable lessons to the responsible policy, skill, operating document, or
reference owner under
[context and memory policy](../policies/context-and-memory.md). Use the
[Archive index](../../98.archive/README.md) for retired routes.

## Related Documents

- [Governance Hub](../README.md)
- [Context and Memory](../policies/context-and-memory.md)
- [Work Lifecycle](../skills/work-lifecycle.md)
