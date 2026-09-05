---
title: "Codex Native Adapter"
version: "1.0.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-06"
---

# Codex Native Adapter

## Overview

Common policy, role meaning and procedures live in [the common authority](../.agents/README.md).
This directory owns only Codex syntax, support notes and native connections.

## Structure

- `agents/`: native role definitions with explicit common file reads.
- `CODEX.md`: explicitly read provider baseline.
- [provider.md](provider.md): provider-specific loading and support contract.
- No project `skills/`, `hooks/`, `hooks.json`, `rules/` or `config.toml` is adopted.
  Codex project skills reside in `.agents/skills/`.

## Configuration Boundary

Edit [roles/registry.json](../.agents/roles/registry.json) and the selected
canonical role for common contracts. Update native references in both adapters
when paths change; retain model and tool settings. Native files do not prove
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
