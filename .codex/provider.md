---
title: "Codex Provider Notes"
version: "1.6.0"
type: "governance/provider"
status: "active"
owner: "platform"
updated: "2026-10-15"
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
responsibility, and current Task. [Codex bindings](bindings.json) own concrete
model, reasoning, skill and native scope values; TOML role projections consume
those values under the neutral registry's role and permission-class ceiling.
Configured values alone do not prove provider resolution or tool enforcement.

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
- Use native sandbox and approval controls. [Codex bindings](bindings.json)
  map the neutral registry's permission class to a native `sandbox_mode`;
  [Claude bindings](../.claude/bindings.json) separately map that class to a
  native `tools` allowlist. Each role projection consumes its provider's
  binding. The validator checks this configuration, not whether a client
  applied it.
- Observed on `codex-cli 0.153.4` (2026-09-06): the client reports `hooks` as a
  stable feature, and the documented surfaces are `.codex/hooks.json` and a
  `[hooks]` table in `.codex/config.toml`. `hooks.json` is adopted; the inline
  table is not, so one file holds the registration and the two cannot disagree.
  The project `.codex/config.toml` holds `[memories]` with
  `generate_memories = false` and `use_memories = false` and, since SPEC-0114,
  `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`,
  no workspace network access and `[shell_environment_policy]` with
  `inherit = "core"` and `ignore_default_excludes = false`; the validator
  rejects any other key or table, including `[hooks]`. `codex-cli 0.162.1`
  rejected an invalid `sandbox_mode` in this file on 2026-10-13, so the project
  layer is parsed. A later session observed that a dummy secret-named variable
  was absent, but did not isolate which setting removed it.
  `.codex/rules/default.rules` forbids, as argv prefixes, a subset of the
  command families the Claude deny list covers, and the validator pins its
  digest; option-first and reordered forms are not expressible as prefixes,
  so without sandbox network a network command still needs approval. The hook
  registration exits 2 when its adapter cannot be found, and a changed hook
  needs the user's review through `/hooks`. The memory keys were
  found in the installed `codex-cli 0.162.1` binary on 2026-10-13 (static evidence);
  Codex applies a project config only to a trusted project, so the effect is
  separate runtime evidence.
  It registers `PreToolUse` on `Bash|apply_patch` and runs `.codex/hooks/pre-tool-use.sh`,
  this provider's own adapter for the shared guard at
  `scripts/provider_write_guard.py`. The documented payload carries `tool_name`
  and `tool_input`, and `tool_input.command` for `Bash` and `apply_patch`.
  `CLAUDE_PROJECT_DIR` is absent here, so the adapter derives the repository
  root from Git and forwards it as data.
- Native prerequisites reviewed on 2026-09-08: the
  [official hook documentation](https://learn.chatgpt.com/docs/hooks) requires
  a trusted project `.codex/` layer and review/trust of the current non-managed
  hook definition. The interactive `/hooks` command inspects sources and their
  review state. The user owns that trust decision; do not change global trust
  or bypass hook review to manufacture runtime acceptance.
- The earlier 0.153.4 smoke session did not establish hook delivery. It ran in
  a disposable clone with `--ephemeral --ignore-user-config --sandbox read-only`.
  It completed, but emitted no hook-delivery event and reported a skill-context
  budget failure. `--ignore-user-config` did not isolate every user role/skill
  discovery surface. Explicit role/skill file reads, agent-reported denial and
  an absent probe file do not establish native discovery, resolved role model
  or hook enforcement. The SPEC-0086 Task (`docs/98.archive/README.md`)
  owns that attempt's evidence; SPEC-0072's Task recorded it first and
  transferred it here on 2026-09-24 when SPEC-0072 closed on its static half.
  At that point the next owner was the user/operator for a reviewed project/hook
  trust state and an explicitly authorized observable session.
- On `codex-cli 0.155.1` (2026-09-27) an authorized `--sandbox read-only`
  session in this worktree again reported the skill-context budget message.
  It listed none of the project skills, which matches implicit invocation being
  off. It discovered none of the `.codex/agents/*.toml` roles and did not expose
  an exact model identifier. It refused a probe write fail-closed, because
  `bwrap` could not start the sandbox. Hook delivery was `DEFER` for that
  attempt: the user declined a trust bypass. The SPEC-0086 Task owns that
  evidence; at that point the user and operator owned the project and hook
  trust state.
- Root cause and repair (2026-09-27, `codex-cli 0.155.1`). The roles were
  undiscovered because this checkout was not a trusted project: user config
  trusted only `/home/hyunyoun`, and an untrusted project ignores every project
  `.codex/` layer, including `agents/` and `hooks.json`. A one-invocation `-c`
  trust override did not load the layer. After the user added a persisted
  `trust_level = "trusted"` entry for this checkout, all 17 projections became
  spawnable. The first spawn then failed with HTTP 400, because
  `gpt-5.3-codex-spark` "is not supported when using Codex with a ChatGPT
  account" and is absent from `codex debug models`. At that observation the
  registry `worker` tier bound `gpt-6-sol`, which the catalog described as the
  "Workhorse model for coding and everyday work". A spawned `code-reviewer` then reported `gpt-6-sol`,
  `high`, and `read-only`. A probe `apply_patch` was rejected by the read-only
  sandbox, and no hook event was observed in that session. The later
  SPEC-0114 observation below supersedes only that delivery gap.
- SPEC-0096 (2026-09-27) rebound the Codex tiers. `gpt-5.5`, a legacy model
  that retires from Codex on 2026-10-14, and `gpt-5.3-codex-spark` gave way to
  `gpt-6-sol` for both tiers. At that revision supervisor and architect used
  `native_model_override.codex = gpt-6-astra`; the current override is in
  [Codex bindings](bindings.json), not the neutral registry. Rollout records
  of spawned threads show that the client
  applied each bound model and `model_reasoning_effort`. The SPEC-0096 Task owns
  the rationale and the evidence.
- The intended boundary for a non-authoring role on this provider is the
  operating-system `sandbox_mode` mapped by its binding under the neutral class
  ceiling. A delivered hook does not establish sandbox enforcement. On this host,
  `bwrap` failed and commands ran outside the sandbox after approval in the
  SPEC-0114 observation, so isolation remains unverified here. A role in a
  mutation-capable class uses the hook for scoped path decisions, not as an
  operating-system file or network boundary.
- Response contract observed in the installed client on 2026-09-06:
  `PreToolUse` accepts `permissionDecision`, `permissionDecisionReason` and
  `systemMessage`, and treats `decision:approve`, `continue:false`,
  `stopReason` and `suppressOutput` as unsupported. A non-zero exit that writes
  a reason to standard error blocks the call. The shared guard emits only
  `systemMessage` and the exit-with-reason form, so no unsupported field is
  relied on as a control here.
- The guard's shell observation is advisory on this provider as it is on the
  other: it reports recognized redirection, `tee` and in-place `sed` targets
  and blocks nothing, and it detects no interpreter-mediated or otherwise
  indirect write. A patch envelope is different: its file headers reach the
  structured path pipeline and receive the same evaluation a structured write
  receives.
- That registration is tracked configuration checked by the governance
  validator and exercised against Codex-shaped payloads in
  `tests/test_k8s_pre_edit_hook.py`. These static checks do not establish event
  delivery. The operator's new trusted Codex session on 2026-10-14 observed a
  `PreToolUse` denial on an `apply_patch` probe with no file created after
  `/hooks` review (SPEC-0114 Task EVD-022). It also observed a dummy
  secret-named environment variable absent and a network approval prompt;
  those observations do not prove the environment filter's specific cause or
  sandbox isolation. Keep config parsing, hook delivery, rule matching, approval
  and sandbox enforcement as separate evidence lanes.
  The active SPEC-0115 Task also records this chat's native hook denials while
  an intermediate validation Registry edit was incomplete, followed by a
  bounded repair and selected repository checks. That is further hook invocation
  evidence, not proof that the sandbox started.
- Use the shared workspace memory store from
  [context and memory](../.agents/governance/context-and-memory.md) instead of
  native memory, and re-observe repository/task state on resume. Shared context and safety rules live in policies, not this note.
- Reviewed and not adopted on 2026-10-27 (SPEC-0125): no project MCP server
  is registered in `.codex/config.toml`, no IDE shortcut or code-action
  configuration is tracked, and no model-generated test cases or hook-based
  automatic memory collection are used. Adding any of them is a separate
  scoped change.
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
