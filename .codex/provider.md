---
title: "Codex Provider Notes"
version: "1.1.0"
type: "governance/provider"
status: "active"
owner: "platform"
updated: "2026-09-06"
---

# Codex Provider Notes

## Overview

Describe Codex-native loading and configuration without duplicating shared
execution policy or the agent roster.

## Authority Boundary

`AGENTS.md` is the thin Codex gateway; `.codex/CODEX.md` is the local
baseline. Native sandbox, approval, and configuration surfaces govern the
running client. The neutral registry owns shared role and permission meaning.

## Governance Context

Load the gateway, [work lifecycle](../.agents/workflows/work-lifecycle.md), relevant
responsibility, and current Task. Codex TOML role projections carry native
model and reasoning metadata; configured values alone do not prove provider
resolution or tool enforcement.

## Current Contract

Codex discovers project packages at `.agents/skills/<id>/SKILL.md`. Their
`agents/openai.yaml` sets `allow_implicit_invocation: false`; use explicit
invocation and read the selected role. `.codex/CODEX.md` is an explicitly read
team document, not a special automatic entry filename.

- Use `.codex/agents/*.toml` projections selected by the neutral registry when
  authorized delegation and the current runtime mechanism are available.
- Explicitly read required `.agents/skills/<id>/SKILL.md`
  procedures selected by the role. Root AGENTS and native role instructions
  require these reads; they do not register native skills.
- Use native sandbox and approval controls. Each role projection declares the
  `sandbox_mode` its registry permission class binds; that is configuration the
  validator checks, not proof the client applied it.
- Observed on `codex-cli 0.153.4` (2026-09-06): the client reports `hooks` as a
  stable feature, and the documented surfaces are `.codex/hooks.json` and a
  `[hooks]` table in `.codex/config.toml`. `hooks.json` is adopted; the inline
  table is not, so one file holds the registration and the two cannot disagree.
  It registers `PreToolUse` on `Bash|apply_patch` and runs the same guard
  script the Claude side runs. The documented payload carries `tool_name` and
  `tool_input`, and `tool_input.command` for `Bash` and `apply_patch`, which is
  the shape the guard already reads. `CLAUDE_PROJECT_DIR` is absent here, so
  the guard derives the repository root from Git.
- That registration is tracked configuration checked by the governance
  validator and exercised against Codex-shaped payloads in
  `tests/test_k8s_pre_edit_hook.py`. Neither establishes that this client
  delivered the event. Run explicit repository validation and do not infer
  event delivery from a file.
- Keep provider-local memory advisory and re-observe repository/task state on
  resume. Shared context and safety rules live in policies, not this note.
- Follow `RTK.md` for shell tooling. Record an unavailable tool or runtime
  instead of inspecting private configuration to manufacture readiness.

## Validation and Refresh

Validate registry/projection semantics and native configuration after relevant
changes. Check the intended installed client's documented configuration when a
native capability changes, and name the client identity a capability claim was
observed against. An undated capability denial is not a current contract. Separately evidence discovery, authenticated
execution, model resolution, sandbox/approval behavior, and event delivery;
repository-static PASS establishes none of them.

## Related Documents

- [Codex Baseline](CODEX.md)
- [Agent Registry](../.agents/roles/registry.json)
- [Model Selection](../.agents/governance/model-selection.md)
- [Quality Policy](../.agents/governance/quality.md)
