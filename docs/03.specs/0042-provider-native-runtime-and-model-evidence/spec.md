---
title: 'Provider-Native Runtime and Model Evidence Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-07-29
artifact_id: "SPEC-0042"
---

# Provider-Native Runtime and Model Evidence Specification

## Overview

This specification defines provider-native project surfaces, model and effort
selection, MCP/tool boundaries, and comparable runtime evidence for Claude,
Codex, and Gemini. Local/Antigravity remains a fourth tracked projection but is
not a substitute for a Gemini-native canary.

The current-source observation cutoff is **2026-07-10 10:00 Asia/Seoul**
(`2026-07-10 01:00 UTC`). A prior user report recorded Codex CLI
`0.145.0-alpha.27` present with Claude and Gemini absent. Read-only executable
re-observation on 2026-07-28 found Claude Code `2.1.220 (Claude Code)` and Codex CLI `0.140.0`
present while Gemini remained absent. The observations remain separately
provenanced inputs, not cutoff, authentication, completion, model-resolution,
or runtime-availability claims.

## Strategic Boundaries & Non-goals

- **Owns**: provider project paths, native metadata, secret-free settings,
  model/effort candidate evidence, MCP/tool inventory, installation/auth mode
  evidence, and controlled discovery/run canaries.
- **Depends on**: Spec 041's machine contract and exact projection schema.
- **Does not own**: shared role admission/eval corpus, loop recovery, GitHub
  credential storage, or final program closure.
- **Non-goals**: treating a parsed file as runtime readiness, modifying private
  user configuration, storing credentials, bypassing provider authentication
  policy, or declaring a model fit because it is merely newer.

## Contracts

### Provider surface contract

| Surface | Project files | Candidate metadata boundary | Runtime evidence |
| --- | --- | --- | --- |
| Local / Antigravity | `.agents/**`, root `GEMINI.md` adapter path | Local role `name`, `description`, `model`; shared asset references | Local adapter evidence only |
| Claude | `.claude/agents/*.md`, `.claude/settings.json`, root `CLAUDE.md` | `name`, `description`, `model`, least-privilege `tools`; other fields only when cutoff schema proves them | Authenticated Claude discovery and controlled delegated run |
| Codex | `.codex/agents/*.toml`, `.codex/config.toml`, root `AGENTS.md` | `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort` | Authenticated Codex discovery, config resolution, and controlled subagent run |
| Gemini | `.gemini/agents/*.md`, `.gemini/settings.json`, root `GEMINI.md` | `name`, `description`, `kind`, `tools`, `model`, `max_turns`, `timeout_mins`; settings-owned model/reasoning configuration | Authenticated Gemini discovery and controlled subagent run |

Tracked settings contain no API key, token, account identity, auth cache, or
private endpoint credential. User/home configuration is read only when the
human explicitly authorizes the exact diagnostic and no secret content is
captured.

The field lists above are observation-time candidates from live provider
documentation. They become cutoff-backed contract fields only when a dated
tag, release note, or historical snapshot proves availability by the cutoff;
otherwise implementation records observation-time confidence and requires the
native schema/config canary before promotion.

### Evidence classes and verdicts

Each provider emits separate `repo-static`, `native-discovery`, and
`authenticated-run` records. Verdicts are `PASS`, `FAIL`, `BLOCKED`, `ABSENT`,
or `DEFER`; only PASS satisfies the corresponding runtime gate. Spec 042 may
finish its repository-local tranche after the canary harness, redaction, and
result recording work passes even when a provider result is not PASS. Such a
result remains a provider-readiness limitation with an owner and retry trigger.
Spec 046 may close repository-local implementation with explicit `ABSENT` or
`DEFER` provider records, but it cannot claim the corresponding runtime PASS.

## Core Design

### Source ledger and cutoff confidence

The implementation records URL, publisher, publication or release date when
available, observation date, cutoff applicability, supported claim, and
confidence. Live documentation without a dated snapshot proves current syntax
at observation time but does **not** alone prove that every field existed at
the cutoff. Dated release notes/tags or a verified historical snapshot must
support cutoff-sensitive claims.

Primary sources:

- Claude: [subagents](https://code.claude.com/docs/en/sub-agents),
  [configuration](https://code.claude.com/docs/en/configuration),
  [hooks](https://code.claude.com/docs/en/hooks),
  [memory](https://code.claude.com/docs/en/memory), and
  [model configuration](https://code.claude.com/docs/en/model-config).
- Codex: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
  [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
  [configuration](https://learn.chatgpt.com/docs/config-file/config-reference),
  and [model catalog](https://developers.openai.com/api/docs/models).
- Gemini: [documentation](https://geminicli.com/docs/),
  [subagents](https://geminicli.com/docs/core/subagents/),
  [hooks](https://geminicli.com/docs/hooks/reference/),
  [project context](https://geminicli.com/docs/cli/gemini-md/),
  [model selection](https://geminicli.com/docs/cli/model/), and
  [generation settings](https://geminicli.com/docs/cli/generation-settings/).

### Role-specific model and effort policy

The following are **cutoff-bounded candidates**, not accepted assignments. A
candidate can be recorded from a dated provider source or local observation, but
it cannot become a current role assignment until the exact adapter syntax parses,
the permitted runtime resolves it without silent fallback, and Spec 044 fitness
evidence passes.

| Provider | High-complexity candidate | Focused worker candidate | Effort boundary |
| --- | --- | --- | --- |
| Claude | Dated cutoff evidence supports Opus 4.8 and `/effort xhigh`; exact configured ID/alias remains account- and runtime-resolved | Sonnet/Haiku family only when the cutoff source or runtime canary proves the exact identifier | Use only a model-supported native effort value observed by schema/runtime; aliases and organization allowlists may alter resolution |
| Codex | Dated cutoff evidence supports Codex 0.144.1 and GPT-5.6-related Codex app performance notes; exact CLI model IDs remain unresolved until runtime/config evidence | Current documented Codex model family or installed-runtime fallback only after exact parse/runtime evidence | `model_reasoning_effort` is model- and client-dependent; validate the exact value instead of treating documentation examples as universally accepted |
| Gemini | Gemini CLI release evidence before the cutoff may support CLI capability, but exact Gemini-native project model IDs remain unresolved until native parse/runtime evidence | Gemini CLI Auto/default or exact model ID only after cutoff source plus runtime evidence | Subagent `model` is independent of parent selection only when native docs/runtime prove it; reasoning settings require agent-scoped parse/runtime evidence |

Architecture, supervisor, security, and ambiguous cross-scope work start with a
high-capability candidate; routine editing, evidence collection, and narrow
validation start with a focused candidate. Spec 044 may change either choice
only from versioned eval and canary evidence. Actual model, effort, fallback
reason, limitation, latency, and cost observation are recorded per run.

The source ledger records aliases and exact configured and observed IDs
separately. Account/organization allowlists, model lifecycle, client version,
and fallback may change resolution. A model is promoted only after its exact
adapter syntax parses, a permitted runtime resolves it, and Spec 044's
role-specific evaluation passes. Silent fallback is a FAIL.

### Canary sequence

For each provider: verify installation provenance/version, validate secret-free
project config, confirm authenticated account mode without capturing identity
or tokens, list/discover the expected project role, run a bounded no-mutation
task, observe the actual selected model/effort where exposed, confirm tool and
stop boundaries, redact the result, and write a comparable evidence record.

## Data Modeling & Storage Strategy

A provider baseline record contains provider, cutoff, source ledger version,
CLI version/source, project paths, metadata schema version, configured and
observed model/effort, auth-mode class, MCP/tool allowlist, transition risk,
and evidence verdicts.

A canary record contains task ID, provider, adapter role, command class,
start/end time, expected/observed discovery, configured/observed model,
effort, allowed tool set, exit/result class, redaction check, limitation, and
evidence path. It contains no prompt transcript, credential, account name,
token, auth file path/content, or provider response body beyond a bounded
secret-free assertion.

## Interfaces & Data Structures

- Provider adapters consume canonical role semantics from Spec 041 and emit
  native metadata only.
- Provider notes own source/capability boundaries and link the comparable
  canary evidence; they do not duplicate role tables.
- MCP inventory records server name, owner, purpose, transport, trust boundary,
  credential class, allowed roles, data sensitivity, network requirement, and
  runtime verification state.
- Model decisions link role, fixture corpus, provider, model, effort, score,
  limitation, rollback, and canary result.
- The canary runner must support a dry, no-live-mutation task common to all
  three providers and stable result normalization.

## Edge Cases & Error Handling

- A candidate model may exist in documentation but not in the authenticated
  account/region/CLI. Record BLOCKED or FAIL; do not silently substitute.
- The provider may alias a model name. Record configured and observed values,
  and require an explicit mapping before PASS.
- A current live doc may describe post-cutoff syntax. Mark cutoff confidence
  unresolved until dated evidence is found.
- Gemini/Antigravity migration may change auth or path schema. Keep Gemini CLI
  and local/Antigravity evidence distinct even if context files migrate.
- A canary that requires network or external state must stay within the
  already approved provider scope and request any new authority explicitly.

## Failure Modes & Fallback / Human Escalation

- **CLI absent**: record ABSENT and provide the official installation path;
  installation/authentication requires the scoped execution approval.
- **Authentication blocked**: record BLOCKED with the non-secret mode and
  provider guidance; do not inspect auth caches or credentials.
- **Schema mismatch**: stop the affected provider projection and retain the
  last verified configuration while the contract is corrected.
- **Canary mutation risk**: abort before execution and redesign the fixture as
  read-only/no-op.
- **One provider not PASS**: record an owned provider-runtime-readiness
  limitation. Repository-local Specs 043–046 may continue and close after Spec
  042's tranche-owned static/canary-harness criteria pass and the record carries
  its limitation, owner, and retry trigger. Only that provider's runtime
  readiness remains open until a later authenticated rerun records PASS.

## Verification Commands

Spec 042 must implement focused validators/canaries with provider-specific
commands documented in the Task. The common repository gates remain:

```bash
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-config.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

The focused provider commands are implemented repository-static deliverables.
They validate comparable evidence records without promoting provider
discovery, authentication, model resolution, hosted CI, remote, or live
readiness.

## Success Criteria & Verification Plan

- **VAL-PNME-001**: All four tracked surfaces resolve their intended project
  paths without relabeling `.agents/**` as Gemini-native evidence.
- **VAL-PNME-002**: Provider metadata/settings parse against verified schemas;
  cutoff uncertainty is explicit and unsupported fields are rejected.
- **VAL-PNME-003**: Tracked project config and MCP inventory contain no secret
  values and declare owner, trust, role, and evidence boundaries.
- **VAL-PNME-004**: Every role/model candidate declares supported effort,
  fallback, and required Spec 044 fitness evidence.
- **VAL-PNME-005**: Claude discovery/run canary is executable, redacted, and
  records one allowed verdict; a non-PASS verdict keeps Claude runtime readiness
  open without failing the repository-local recording criterion.
- **VAL-PNME-006**: Codex discovery/run canary is executable, redacted, and
  records one allowed verdict; a non-PASS verdict keeps Codex runtime readiness
  open without failing the repository-local recording criterion.
- **VAL-PNME-007**: Gemini discovery/run canary is executable, redacted, and
  records one allowed verdict despite the transition boundary; a non-PASS
  verdict keeps Gemini runtime readiness open without failing the
  repository-local recording criterion.
- **VAL-PNME-008**: Comparable canary records pass redaction and distinguish
  static, discovery, and authenticated-run evidence.
- **VAL-PNME-009**: Focused provider validation, strict document checks,
  repository quality gate, and diff checks PASS.

Implementation commit `9c4dcc7b7572bfe8f436d81ee87ede872707cc73`
implements the closed provider evidence contract, exact ten-source ledger,
thirteen config and eight canary negative fixtures, four provider surfaces,
eight candidate-only model records, seven MCP boundaries, and twelve redacted
canary records. Focused, strict, lifecycle, aggregate, all-files, and diff
checks passed; requirements review returned `COMPLIANT` and quality/security
review returned `APPROVED`. Provider discovery, authenticated run, model
promotion, hosted CI, remote, credential-bearing, and live results remain
their recorded `DEFER` or `ABSENT` verdicts.

## Traceability

- **Program requirement**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Architecture**: [AD 0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Proposed decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Predecessor**: [Spec 041](../0041-stage-00-agent-governance-contract/spec.md)
- **Successor**: [Spec 043](../0043-agent-harness-loop-lifecycle/spec.md)
- **Execution Plan**: [Provider-Native Runtime and Model Evidence Implementation Plan](plan.md)
- **Task evidence**: [Provider-Native Runtime and Model Evidence Task](README.md#task-records)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements) | VAL-PNME-001 | Path ownership proves four distinct projections. |
| N/A — VAL-PNME-002 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-002 | Provider-schema fixtures prove supported metadata and cutoff confidence. |
| N/A — VAL-PNME-003 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-003 | Config/MCP validation proves secret-free tracked baselines. |
| N/A — VAL-PNME-004 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-004 | Model compatibility records prove effort and fallback boundaries. |
| N/A — VAL-PNME-005 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-005 | Claude canary harness and redacted verdict record provide an executable closure input. |
| N/A — VAL-PNME-006 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-006 | Codex canary harness and redacted verdict record provide an executable closure input. |
| N/A — VAL-PNME-007 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-007 | Gemini canary harness and redacted verdict record provide an executable closure input. |
| N/A — VAL-PNME-008 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-008 | Normalized redaction evidence proves comparable strict closure input. |
| N/A — VAL-PNME-009 shares the PRD-0003 source linked in VAL-PNME-001 | VAL-PNME-009 | Focused and aggregate QA prove provider tranche readiness. |
