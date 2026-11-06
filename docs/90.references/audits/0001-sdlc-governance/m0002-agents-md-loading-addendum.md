---
title: "AGENTS.md Loading Addendum"
version: "0.1.0"
type: "reference/audit"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "references"
artifact_id: "AUD-0001-m0002"
---

# Reference: AGENTS.md Loading Addendum

## Overview

This dated addendum to [m0001](./m0001-sdlc-governance-audit.md) records how
the two providers load folder `AGENTS.md` files, observed on 2026-11-06 at
`main` `296e3379`. It also records that m0001 was rewritten after
publication. Readers are the operator and agents that change provider
behavior.

## Reference Type

A dated assurance assessment. It informs SPEC-0149 and the folder rule
reading obligation in `.agents/governance/agent-execution.md`.

## Authority Boundary

This report holds observations and findings only. Provider loading rules live
in `.claude/provider.md`, `.codex/provider.md` and
`.agents/governance/agent-execution.md`.

## Scope

The question: does each provider receive the `AGENTS.md` of every folder it
works in? Excluded: user-level provider settings and managed settings.

### Criteria and Inspected Surface

| Criterion | In-scope surface |
| --- | --- |
| Native loading | Claude Code 2.1.319 and codex-cli 0.166.0 documentation |
| Hook delivery to the model | `scripts/provider_write_guard.py` output and both adapters |
| Stage 90 member immutability | `docs/90.references/AGENTS.md` rule 3 and m0001 history |

## Definitions / Facts

### Observed Evidence

| Observation | Source and input | Result |
| --- | --- | --- |
| Claude reads `AGENTS.md` only when no `CLAUDE.md` exists at or above the working directory; the setting that loads both is ignored in project and local settings | code.claude.com/docs/en/memory, read 2026-11-06 | This repository has a root `CLAUDE.md`, so Claude loads none of the 16 `AGENTS.md` files |
| Claude's session context held `CLAUDE.md` and its imports, and no `AGENTS.md` | This session's system context | Matches the documentation |
| Codex builds its instruction chain once per run from the project root down to the working directory | learn.chatgpt.com/docs/agent-configuration/agents-md, read 2026-11-06 | A folder off that path is not loaded |
| The shared guard reported its guidance as `systemMessage`; Claude shows that field to the user, while `additionalContext` reaches the model | code.claude.com/docs/en/hooks, read 2026-11-06; guard at `296e3379` | The guard's guidance never reached the model |
| m0001 was published in `73b1df48` and then edited in `d4338908`, `041add36`, `342fbe6c`, `2071e8c2` and `c3e343a0` | `git log` of the member | Rule 3 was not followed; no validator enforces it |
| A Codex probe in `docs/03.specs` stopped with a usage-limit error until 2026-11-09 18:37 | `codex exec -s read-only`, 2026-11-06 | F-06 stays UNKNOWN |

### Findings and Gaps

| Finding or gap | Severity | Evidence |
| --- | --- | --- |
| F-08: The shared guard's guidance and any folder rules never reached the model because it used the user-facing `systemMessage` | P1 | Hooks documentation; guard output |
| F-09: Neither provider loaded folder `AGENTS.md` files outside its native path; Claude loaded none | P1 | Memory and Codex documentation |
| F-10: m0001 was rewritten five times after publication against rule 3 | P2 | m0001 history |

## Sources

Claude Code memory and hooks documentation and the Codex AGENTS.md and hooks
documentation, read 2026-11-06; repository history at `296e3379`.

## Review and Freshness

Refresh when either provider changes how it loads instructions or hooks, or
when the guard output changes.

### Remediation

| Remediation | Owner | Due or decision date |
| --- | --- | --- |
| F-08 and F-09: the guard supplies each target's folder `AGENTS.md` chain, root excluded, through `additionalContext`, once per session (SPEC-0149) | platform | Done 2026-11-06 under SPEC-0149; criteria accepted (REQ-0003 Archived Lineage) |
| F-09 for reads: Claude now loads each folder `AGENTS.md` through a sibling one-line `CLAUDE.md` import on a read, write or edit (read and write observed, edit documented), and a session-start hook re-injects the reading instruction after a compaction (SPEC-0151) | platform | Done 2026-11-06 |
| F-10: later changes to this pack go into a new dated member; m0001 is left as it now stands, because restoring its published bytes would restore links to a deleted package; `validate-document-contract-registry.py` now refuses such a rewrite against the staged index, including a rename Git pairs (`REFERENCE_PUBLISHED_REWRITE`, SPEC-0150); an unpaired delete-and-add escapes it, and the lifecycle validator separately refuses a `published` member returning to `draft` | platform | Decided and enforced 2026-11-06 |
| F-06: repeat the Codex probe after the limit resets | operator | 2026-11-09 or later |

### Verification State

Claude delivery and Codex delivery are recorded in the SPEC-0149 Task, recovered
with `git show ea4e36be:docs/03.specs/0149-agents-md-hook-context/tasks/tsk-0001-agents-md-hook-context.md`.
Codex delivery is unobserved until the usage limit resets; whether codex-cli
0.166.0 accepts `hookSpecificOutput`, or rejects it together with the
`systemMessage` beside it, is unverified. The once-per-session record does
not survive a context compaction, so rules supplied before one are not
supplied again.

## Related Documents

- [Audit pack](./README.md)
- [m0001 SDLC governance audit](./m0001-sdlc-governance-audit.md)
- [Agent Execution Policy](../../../../.agents/governance/agent-execution.md)
