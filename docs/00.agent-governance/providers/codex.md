---
title: 'Reference: Codex Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-08-01
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

Cutoff-sensitive capability evidence was reconciled against
`2026-07-10 10:00 Asia/Seoul` on 2026-07-28:

- Codex release `rust-v0.144.1`: <https://github.com/openai/codex/releases/tag/rust-v0.144.1>
- Codex release `rust-v0.145.0-alpha.2`: <https://github.com/openai/codex/releases/tag/rust-v0.145.0-alpha.2>
- Codex custom instructions with `AGENTS.md`: <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- Codex subagents: <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- Codex configuration and approval surfaces: <https://learn.chatgpt.com/docs/config-file/config-reference>

The cutoff ledger records stable `0.144.1` and prerelease
`0.145.0-alpha.2` as published before the cutoff. The current config reference
is observation-time evidence; accepted `model_reasoning_effort` values and
model IDs remain model/client dependent until the intended runtime parses and
resolves them without silent fallback. A read-only `codex --version`
observation on 2026-07-28 returned `0.140.0`. The earlier user-reported
`0.145.0-alpha.27` is retained as a separate prior observation; neither
observation proves authentication, model availability, agent discovery, or
delegated execution.

### Loading Model

- Start with the Codex/GPT gateway: `AGENTS.md`
- Follow the JIT loading sequence defined in `docs/00.agent-governance/rules/bootstrap.md`
- Load the local Codex runtime baseline: `.codex/CODEX.md`

### Context Strategy

- Codex uses `.codex/agents/*.toml` as provider-native role adapters for the local agent roster.
- Hook event wiring is defined in `.codex/hooks.json`, which points to the repository's shared lifecycle hook implementations where the runtime consumes that file.
- `.codex/hooks.json` is strictly for event wiring (context and validation) and is **not** a permission gate.
- Shared skills, workflows, and output styles resolve through `.codex/{skills,workflows,output-styles}` symlinks to the `.agents/` SSoT. Codex-specific rules stay in this provider note and Stage 00 rules; `.codex/rules/` is only a placeholder/adapter surface unless populated by a future approved adapter change.
- Treat provider- or user-local recall as `provider-local-auxiliary`, ignored
  `.agent-work/checkpoint.json` as `working-short-term`,
  `memory/progress.md` as the shared `durable-long-term` ledger, and the owning
  Spec/Runbook/Incident/Postmortem as `domain-scoped`. Repository evidence wins
  conflicts.
- Repo-static loop and checkpoint validators enforce the atomic/redacted
  synthetic checkpoint contract, repository-wins resume,
  promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five
  bounded reviewed feedback destinations. They neither read nor write the ignored
  checkpoint and do not prove Codex discovery, event delivery, permissions,
  model resolution, authenticated execution, hosted CI, remote,
  credential-bearing, live, or actual checkpoint execution.

## Current Contract

### Execution Expectations

- **Symmetry**: Codex follows the same repo-static role parity rules as Claude, Gemini, and the local/Antigravity adapter while using Codex-native TOML metadata. This static parity does not assert provider runtime parity.
- **GitOps-First**: Adhere strictly to the workspace constraints; never write plaintext secrets.
- **Language**: Produce human-facing responses in Korean, but keep governance and policy documents in English.

### QA Evidence Resolution

- `contracts/harness-contract.json` version `1.0.0` is the provider-neutral
  machine owner. Its current `12 roles / 4 surfaces / 48 adapters` inventory is
  repository-static adapter evidence.
- `model-policy.md` owns shared tier/reasoning vocabulary, while
  `contracts/agent-model-fitness.json` version `1.1.0` owns exact
  role/provider incumbent, configured and observed value, candidate, reasoning,
  fallback, and decision state. All 12 Codex mappings remain `DEFER` because
  their support is current-only rather than fixed-cutoff runtime evidence;
  the global AREA-004 mapping result is `PASS` 21 / `DEFER` 27. Observed
  fitness, threshold, promotion, canary, and runtime remain `DEFER` for all 48
  tuples.
- Codex adapter `model` and `model_reasoning_effort` values remain configured
  incumbents until a future authorized, evidence-backed promotion. AREA-003
  repository-static evaluation readiness is complete, while observed
  same-suite evaluation and final admission remain `DEFER`.
- Keep `repo-static`, `provider-runtime`, `ci`, and `remote-live` evidence
  separate. A result in one class never proves another.
- Spec 045 retired the former role-semantics compatibility inputs after
  zero-consumer proof; the harness contract and harness-semantics validator
  are the current semantic owners.
- `contracts/agent-governance-closure.json` is the single Spec 046 program
  result-classification owner. Its repository-static PASS cannot promote
  Codex discovery, auth, model resolution, sandbox/approval enforcement,
  hosted, remote, live, or actual evaluation evidence.
- Resolve `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
  `remote/live` semantics plus handoff fields from
  [`rules/quality-standards.md`](../rules/quality-standards.md).
- Tracked `.codex/agents/*.toml` and `.codex/hooks.json` are repo-static
  configuration. They do not prove native Codex discovery, role use, event
  delivery, sandbox enforcement, approval handling, or remote execution.
- Preserve Codex-native `model`, `model_reasoning_effort`, sandbox, and approval
  validation while `contracts/harness-contract.json` owns shared role
  semantics.

## Validation and Refresh

Run the harness, provider/model, provider-neutral role, roster-currentness, and
repository quality checks after changing Codex adapters, model metadata, or
hook wiring:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-config.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-harness-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
python3 scripts/validate-agent-governance-closure.py --root .
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
