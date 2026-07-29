---
title: 'Reference: Gemini Provider Notes'
type: governance/reference
status: active
owner: platform
updated: 2026-07-29
---

# Gemini Provider Notes

## Overview

Gemini-specific guidance for `hy-home.k8s`.

## Authority Boundary

### File Name Compatibility

- Default context file is `GEMINI.md`.
- In this repository, keep `AGENTS.md` out of the Gemini loading path unless a
  future approved adapter change updates Stage 00; `AGENTS.md` is the Codex/GPT
  gateway.
- Track Gemini CLI project agents at `.gemini/agents/**` as repo-static
  project-surface evidence only. Track `.gemini/settings.json` only in the
  closed schema-linked form with empty `agents.overrides`; provider-specific
  tool aliases and model override promotion remain deferred. The project-agent
  frontmatter intentionally omits `tools` and `model`. Do not treat either
  repo-static surface as native discovery, parsing, event delivery,
  authenticated execution, policy loading, tool enforcement, or
  model-resolution evidence.

## Governance Context

### Official Source Basis

Cutoff-sensitive capability evidence was reconciled against
`2026-07-10 10:00 Asia/Seoul` on 2026-07-28:

- Gemini CLI release `v0.50.0`: <https://github.com/google-gemini/gemini-cli/releases/tag/v0.50.0>
- Gemini CLI release `v0.51.0-preview.0`: <https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0>
- Gemini CLI changelog: <https://geminicli.com/docs/changelogs/>
- Gemini CLI subagents: <https://geminicli.com/docs/core/subagents/>
- Gemini CLI memory: <https://geminicli.com/docs/tools/memory/>

The dated release ledger proves CLI releases before the cutoff, not local
installation or this repository's native registration. Current subagent and
memory pages are observation-time evidence unless a cutoff tag or native parser
proves the exact field. A read-only executable lookup on 2026-07-28 found no
Gemini CLI. This `ABSENT` installation observation leaves native discovery,
authentication, model resolution, event delivery, and delegated execution
unproven.

### Loading Model

- Keep root `GEMINI.md` thin; it imports `@docs/00.agent-governance/rules/bootstrap.md` (shared governance), `@docs/00.agent-governance/providers/gemini.md`, `@.agents/GEMINI.md`, and `@RTK.md`. It must not import `@AGENTS.md`, which is the GPT/Codex provider shim.
- Root `GEMINI.md` must load the existing hierarchy; it must not copy RTK, graphify, catalog, or governance policy blocks inline.
- Use `.agents/GEMINI.md` as the local/Antigravity adapter baseline; resolve the agent roster and model tier mapping from `docs/00.agent-governance/harness-catalog.md`.
- Use governance files under `docs/00.agent-governance/rules/*` as canonical policy.
- Keep provider-specific details here; avoid policy duplication.
- Keep local/Antigravity adapter wiring under the existing gateway hierarchy; do not create a parallel `.github/**` instruction layer for this repository or infer Gemini CLI native wiring.

### Antigravity Harness Structure (`.agents/`)

The `.agents/` directory is the tracked local/Antigravity adapter baseline for
this repository and the provider-neutral owner for shared skills, workflows,
and output styles. It is not the Gemini CLI native configuration directory.

- **Rules (`.agents/rules/`)**: Contains local/Antigravity workflow and behavior rules (e.g., `workspace-rules.md`); these are not Gemini CLI native policy files.
- **Workflows (`.agents/workflows/`)**: Defines orchestrated workflows (e.g., `qa-cicd-workflow.md` for pre/post-edit validation).
- **Skills (`.agents/skills/`)**: Houses provider-neutral shared skill definitions for the tracked local adapters; Gemini CLI native discovery or consumption is not established.
- **Hooks (`.agents/hooks.json`)**: Declares local/Antigravity behavioral wiring where a compatible runtime honors it. It invokes shared `docs/00.agent-governance/hooks/*.sh` scripts for Template-First routing and QA/CI/static validation, but it is neither a Claude-style permission gate nor Gemini CLI native settings.
- **Agents (`.agents/agents/*.md`)**: Local/Antigravity role adapters with
  `name`, `description`, and `model` frontmatter. They preserve role parity
  with Claude and Codex adapters without requiring Claude-style `tools:`
  frontmatter.

### Context Strategy

- Gemini CLI supports hierarchical context loading (global, ancestors, subdirectories).
- Treat any native or local provider recall as `provider-local-auxiliary`, not
  repository authority. Ignored `.agent-work/checkpoint.json` is
  `working-short-term`; `memory/progress.md` is the shared
  `durable-long-term` ledger; owning Specs, Runbooks, Incidents, and
  Postmortems hold `domain-scoped` knowledge. Repository evidence wins
  conflicts.
- Repo-static loop and checkpoint validators enforce the atomic/redacted
  synthetic checkpoint contract, repository-wins resume,
  promotion/refresh/expiry/archive-GC/conflict, compaction, handoff, and five
  bounded reviewed feedback destinations. They neither read nor write ignored
  checkpoints and do not establish Gemini CLI discovery, event delivery,
  permissions, model resolution, authenticated execution, hosted CI, remote,
  credential-bearing, live, or actual checkpoint execution.
- The tracked local adapter workflow may be used only by a runtime that
  explicitly supports it. Do not infer Gemini CLI agent registration from
  `.agents/agents/**`.
- Prefer modular imports for large context sets.
- Keep instructions concise and non-duplicative across hierarchy.
- Avoid introducing provider-specific guidance outside the existing `GEMINI.md` + `.agents/**` + `docs/00.agent-governance/**` hierarchy.

## Current Contract

### Gemini CLI Native Surface

Gemini CLI native project agents are tracked under `.gemini/agents/**` as
repo-static adapter files. They use the fixed native metadata projected by Spec
044: exactly `name`, `description`, `kind: local`, `max_turns`, and
`timeout_mins`. They do not declare generic `tools` aliases or an exact
`model`. Candidate models and reasoning profiles remain candidate-only in
`contracts/agent-model-fitness.json`; each Gemini tuple points to its candidate
there rather than to nonexistent adapter metadata. The minimal settings file
does not prove runtime interpretation. Native discovery, parsing, event
delivery, policy loading, authenticated execution, settings interpretation,
tool enforcement, and model resolution remain `DEFER` or `ABSENT` until a
provider-runtime canary proves them.

The provider-neutral machine owner is
`contracts/harness-contract.json` version `1.0.0`. Its current inventory is
exactly `12 roles / 4 surfaces / 48 adapters`. This is repo-static adapter
parity only; it does not promote Gemini CLI runtime discovery, tool execution,
or model resolution.

### Model Policy (Gemini)

- Refer to `docs/00.agent-governance/model-policy.md` and
  `docs/00.agent-governance/contracts/provider-runtime-evidence.json` for
  candidate tiers and cutoff confidence.
- Current `.agents/**` model labels are local/Antigravity adapter evidence
  only. They are not Gemini CLI native model-resolution evidence.
- Gemini CLI pro/flash/Auto candidates remain candidate-only until a permitted
  runtime canary and Spec 044 role fitness evidence promote an exact ID. The
  model-fitness contract records the pending candidate IDs and reasoning
  profiles; `.gemini/agents/**` deliberately does not mirror them. Neither the
  contract nor the adapter files prove provider-side availability, resolution,
  or execution.

### Execution Expectations

- Use JIT loading: bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight.
- Keep user-facing responses in Korean.
- Keep governance and technical control docs in English.
- Use `contracts/harness-contract.json` as the machine roster owner and
  `harness-catalog.md` as its readable runtime view.

### QA Evidence Resolution

- Keep the harness evidence classes `repo-static`, `provider-runtime`, `ci`,
  and `remote-live` separate. A tracked local adapter is repo-static evidence
  only and never proves Gemini CLI runtime discovery or use.
- The legacy role-semantics contract is readable compatibility input with zero
  semantic consumers until Spec 045 and is not current authority.
- Resolve `affected`, `staged`, `all-files`, `message/manual`, `ci`, and
  `remote/live` semantics plus handoff fields from
  [`rules/quality-standards.md`](../rules/quality-standards.md).
- Tracked `.agents/agents/*.md` and `.agents/hooks.json` are repo-static
  local/Antigravity adapter configuration. They do not prove Gemini CLI native
  discovery, role use, event delivery, policy loading, model resolution,
  permission enforcement, or remote execution.
- Preserve local adapter model metadata and role semantics without presenting
  them as Gemini CLI native model selection or runtime wiring.

## Validation and Refresh

Run the harness, shared role-semantic, provider-config, roster, and repository
quality checks after changing local/Antigravity agents, Gemini project-agent
metadata, hooks, model metadata, or the root shim:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-config.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-agent-role-semantics.py --root .
python3 scripts/validate-agent-roster-currentness.py .
bash scripts/validate-repo-quality-gates.sh .
```

Refresh the official source basis when Gemini CLI context or agent-registry
behavior changes. Tracked `.agents/**` files provide local adapter evidence
only; tracked `.gemini/agents/**` files provide repo-static Gemini
project-surface evidence only. Native discovery, event, policy, settings
interpretation, tool enforcement, and model behavior require separately
approved runtime evidence.

## Related Documents

- [Bootstrap Governance](../rules/bootstrap.md)
- [Local Harness Catalog](../harness-catalog.md)
- [Model Selection Policy](../model-policy.md)
- [Subagent Protocol](../subagent-protocol.md)
