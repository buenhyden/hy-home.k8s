---
title: "Handoff Prompt Contract"
version: "0.1.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-09-07"
---

# Handoff Prompt Contract

## Overview

Identifier `handoff`. Assemble the request that produces a work handoff for the
owning Task, so the next owner receives the same fields every time rather than
whatever the session happened to remember.

## Authority Boundary

The handoff fields belong to the
[quality policy](../governance/quality.md#handoff-evidence-contract); this
contract reuses them and redefines none. A handoff records authority; it never
grants it, and a recorded boundary is not a standing authorization.

## Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Branch | `git rev-parse --abbrev-ref HEAD` | Part of the snapshot the evidence describes |
| Head commit | `git rev-parse HEAD` | Part of the snapshot the evidence describes |
| Changed path set | `git status --porcelain` | The scope the handoff covers |
| Committed scope | `git log --oneline main..HEAD` | The logical units already landed on this branch |

The subject input is `Branch`. When it is empty the contract refuses, because
a handoff without a snapshot describes no state.

## Output

The handoff fields the quality policy lists, in its order, each either filled or
explicitly marked `none` or `DEFER` with a reason. No field is omitted.

## Validation

A produced handoff is reviewed against the quality policy's field list before it
is written into the owning Task. A field that silently disappeared fails review.

## Refusal Conditions

- No acceptance identifier or owning Task is supplied, so the handoff would have
  no destination.
- The request asks for a lane result that was not observed, which would report
  an unobserved result as evidence.
- The request asks to include credentials, environment dumps or raw provider
  transcripts.

## Related Documents

- [Common Prompt Contracts](README.md)
- [Quality and Evidence Policy](../governance/quality.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)
