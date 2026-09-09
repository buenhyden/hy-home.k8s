---
title: "Codex Native Adapter"
version: "1.2.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-09"
---

# Codex Native Adapter

## Overview

Common policy, role meaning and procedures live in [the common authority](../.agents/README.md).
This directory owns only Codex syntax, support notes and native connections.

## Structure

- `agents/`: native role definitions with explicit common file reads.
- `CODEX.md`: explicitly read provider baseline.
- [provider.md](provider.md): provider-specific loading and support contract.
- `hooks.json`: the pre-action guard registration, judged by the same
  validator rule family as the Claude side. Registration is tracked
  configuration; it is not evidence that the installed client discovered,
  loaded or delivered the hook.
- `hooks/pre-tool-use.sh`: the Codex adapter for the shared write boundary. It
  names its provider and forwards the payload; the boundary itself is owned by
  `scripts/provider_write_guard.py`. This directory holds no shared logic.
- No project `commands/` or `prompts/` directory is adopted. The neutral
  `.agents/prompts/` contracts are read explicitly and are consumed by
  `scripts/prompt-input.py`; Claude additionally projects them as native
  commands. That projection is a Claude affordance, not shared policy, so its
  absence here is a declared difference rather than missing work.
- No project `skills/`, `rules/` or `config.toml` is adopted. Codex
  project skills reside in `.agents/skills/`, which is the client's documented
  project skill root. `config.toml` stays unadopted so one file owns the hook
  registration; see [provider.md](provider.md) for the client identity each
  capability claim was observed against.

## Configuration Boundary

Edit [roles/registry.json](../.agents/roles/registry.json) and the selected
canonical role for common contracts. Update native references in both adapters
when paths change. The registry owns the capability tier to model binding and
the permission class to `sandbox_mode` binding; a projection restates those
values and the validator rejects any that drift. Native files do not prove
model access, role discovery or permission enforcement. No generator is used.

## Validation

`python3 scripts/validate-agent-governance.py --root .` checks registry, native
syntax, exact role/skill references, link boundaries and permission parity.
`python3 scripts/qa.py full` checks the final repository snapshot. Actual native
loading, invocation and hook events are separate checks requiring a fresh
session and applicable authorization.

## Operations

Read [the provider baseline](CODEX.md), then the selected common
role and its required procedures. Common skill invocation is explicit-only;
it cannot grant extra tools or approval. Edit procedures once under
`.agents/skills/`. Personal local settings and memory are not common policy.

## Related Documents

- [Common work lifecycle](../.agents/workflows/work-lifecycle.md)
- [Approval and safety](../.agents/governance/approval-and-safety.md)
- [Quality](../.agents/governance/quality.md)
- [Model selection](../.agents/governance/model-selection.md)
