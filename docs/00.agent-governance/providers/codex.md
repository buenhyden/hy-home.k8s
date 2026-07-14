---
title: 'Reference: Codex Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Codex Provider Notes

## Overview

Guidance for Codex (GPT) execution in the `hy-home.k8s` repository.

### Role

Codex sessions act as a peer provider to Claude and Gemini. This document defines how Codex interacts with the shared governance model while maintaining its own runtime baseline.

## Authority Boundary

### Permission & Hook Boundary

Codex uses official `AGENTS.md`, configuration, sandbox, and approval-mode
surfaces for its native execution boundary. Unlike Claude's `settings.json`,
`.codex/hooks.json` is a context/validation bridge only. It can orchestrate
validation events (e.g., `pre-validate`, `post-validate`) where supported, but
the Codex agent must still honor governance constraints and run explicit
repo-backed validation before handoff.

Codex subagents are explicit orchestration only when requested by the user; use
`.codex/agents/*.toml` role adapters and do not inline full role definitions
when a local adapter exists.

### Runtime Tooling Boundary

Codex should follow `RTK.md` for shell command guidance. If `rtk` is not on
PATH but `/home/hy/.local/bin/rtk --version` works, record the PATH limitation.
If `rtk gain` cannot initialize its tracking database, do not inspect private
databases or credential files; run the underlying command directly and record
the limitation in the active task evidence.

## Governance Context

### Official Source Basis

Checked on 2026-07-06:

- Codex custom instructions with `AGENTS.md`: <https://developers.openai.com/codex/guides/agents-md>
- Codex subagents: <https://developers.openai.com/codex/subagents>
- Codex CLI/config/approval modes: <https://developers.openai.com/codex/cli>

### Loading Model

- Start with the Codex/GPT gateway: `AGENTS.md`
- Follow the JIT loading sequence defined in `docs/00.agent-governance/rules/bootstrap.md`
- Load the local Codex runtime baseline: `.codex/CODEX.md`

### Context Strategy

- Codex uses `.codex/agents/*.toml` as provider-native role adapters for the local agent roster.
- Hook event wiring is defined in `.codex/hooks.json`, which points to the repository's shared lifecycle hook implementations where the runtime consumes that file.
- `.codex/hooks.json` is strictly for event wiring (context and validation) and is **not** a permission gate.
- Shared skills, workflows, and output styles resolve through `.codex/{skills,workflows,output-styles}` symlinks to the `.agents/` SSoT. Codex-specific rules stay in this provider note and Stage 00 rules; `.codex/rules/` is only a placeholder/adapter surface unless populated by a future approved adapter change.

## Current Contract

### Execution Expectations

- **Symmetry**: Codex follows the same three-surface local role parity rules as Claude and the local/Antigravity adapter while using Codex-native TOML metadata. This static parity does not assert Gemini CLI runtime parity.
- **GitOps-First**: Adhere strictly to the workspace constraints; never write plaintext secrets.
- **Language**: Produce human-facing responses in Korean, but keep governance and policy documents in English.

### QA Evidence Resolution

- Resolve `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
  `remote/live` semantics plus handoff fields from
  [`rules/quality-standards.md`](../rules/quality-standards.md).
- Tracked `.codex/agents/*.toml` and `.codex/hooks.json` are repo-static
  configuration. They do not prove native Codex discovery, role use, event
  delivery, sandbox enforcement, approval handling, or remote execution.
- Preserve Codex-native `model`, `model_reasoning_effort`, sandbox, and approval
  validation while the provider-neutral role contract owns only shared role
  semantics.

## Validation and Refresh

Run the provider-neutral role check, roster-currentness check, and repository
quality gate after changing Codex adapters, model metadata, or hook wiring:

```bash
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Recheck the official source basis when Codex changes its `AGENTS.md`, subagent,
sandbox, approval, or configuration contract. Repository-static PASS does not
establish native discovery, sandbox enforcement, or event delivery.

## Related Documents

- [AGENTS.md Provider Notes](agents-md.md)
- [Bootstrap Governance](../rules/bootstrap.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Model Selection Policy](../model-policy.md)
