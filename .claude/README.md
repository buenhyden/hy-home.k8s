---
title: "Claude Native Adapter"
version: "1.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-07"
---

# Claude Native Adapter

## Overview

Common policy, role meaning and procedures live in [the common authority](../.agents/README.md).
This directory owns only Claude syntax, support notes and native connections.

## Structure

- `agents/`: native role definitions with explicit common file reads.
- `CLAUDE.md`: explicitly read provider baseline.
- [provider.md](provider.md): provider-specific loading and support contract.
- `settings.json`: existing permissions and the registered pre-action hook.
- `hooks/k8s-pre-edit.sh`: the Claude adapter for the synchronous write
  boundary on the shell and structured file tools. It names its provider and
  forwards the payload; the boundary itself is owned by
  `scripts/provider_write_guard.py`, and each provider registers its own
  adapter, so no provider directory owns a control both providers depend on.
- `skills/<id>`: one relative link per common skill package.
- `commands/<id>.md`: one entry point per common prompt contract. Each one
  invokes `scripts/prompt-input.py` with its identifier and owns no contract
  of its own; `.agents/prompts/` keeps the inputs, output and refusal
  conditions.

## Configuration Boundary

Edit [roles/registry.json](../.agents/roles/registry.json) and the selected
canonical role for common contracts. Update native references in both adapters
when paths change. The registry owns the capability tier to model binding;
a projection restates that value and keeps its own tool settings. Native files
do not prove model access, role discovery or permission enforcement. No
generator is used.

## Validation

`python3 scripts/validate-agent-governance.py --root .` checks registry, native
syntax, exact role/skill references, link boundaries and permission parity.
`python3 scripts/qa.py full` checks the final repository snapshot. Actual native
loading, invocation and hook events are separate checks requiring a fresh
session and applicable authorization.

## Operations

Read [the provider baseline](CLAUDE.md), then the selected common
role and its required procedures. Common skill invocation is explicit-only;
it cannot grant extra tools or approval. Edit procedures once under
`.agents/skills/`. Personal local settings and memory are not common policy.

## Related Documents

- [Common work lifecycle](../.agents/workflows/work-lifecycle.md)
- [Approval and safety](../.agents/governance/approval-and-safety.md)
- [Quality](../.agents/governance/quality.md)
- [Model selection](../.agents/governance/model-selection.md)
