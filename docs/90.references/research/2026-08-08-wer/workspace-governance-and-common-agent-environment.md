---
title: 'Reference: Workspace Governance and Common Agent Environment'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Workspace Governance and Common Agent Environment

## Overview

This reference maps the shared workspace environment that Claude and Codex
adapters are intended to serve. Its design conclusion is a provider-neutral
control plane: the repository owns task scope, governance, evidence, recovery,
and durable knowledge; each provider owns how it discovers instructions,
configures tools, asks for approval, executes hooks, authenticates, and resolves
models. The distinction preserves portability without inventing provider parity.

## Reference Type

Repository-static implementation analysis supported by dated primary provider
sources, observed on 2026-08-08.

## Authority Boundary

Stage 00 is authoritative for shared workspace policy and contracts. This
reference does not change those policies, create a runtime permission, or
establish authenticated provider behavior. The `.claude/**` and `.codex/**`
trees are reviewed configuration surfaces only. Provider discovery, hook trust
and delivery, model resolution, external-tool authentication, CI execution, and
live platform readiness stay `DEFER` without separately authorized evidence.

## Scope

This owner covers REQ-WERPC-003 (workspace application) and REQ-WERPC-006
(common system). It covers application at work-item, session, project, provider,
and CI scope; harness and provider details are linked rather than duplicated.

## Definitions / Facts

### Common-system baseline

The catalog at
[`harness-catalog.md`](../../../00.agent-governance/harness-catalog.md) is the
repository's current common-harness inventory. It identifies thin gateways,
runtime baselines, roles/adapters, shared assets, hooks, validation, memory,
and escalation. `AGENTS.md` and `CLAUDE.md` are thin gateways, while
`.codex/CODEX.md` and `.claude/CLAUDE.md` contain provider-local baselines.
These are `Verified` as tracked files on the reviewed commit; no native provider
discovery was tested in this research task.

### Workspace-application baseline

The JIT workflow encoded in bootstrap and both runtime baselines is:

`bootstrap → preflight → persona → scope → provider → progress → postflight`.

It is a repeatable intake route, not evidence that a client automatically read
every document. The route binds provider behavior to canonical workspace owners
before substantial work, rather than embedding mutable policy in an individual
task prompt or provider adapter.

### Common Provider-Neutral Control Plane

| Plane element                    | Canonical owner                                                                | Required behavior                                                                                                                      | Evidence depth today                                                      |
| -------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Task contract                    | Stage 03 Spec and Stage 04 Plan/Task                                           | Name acceptance IDs, owned paths, authority, validation, rollback, and next owner.                                                     | `Verified` static document/registry contract.                             |
| Instruction routing              | `AGENTS.md`, `CLAUDE.md`, bootstrap, runtime baselines, scopes, provider notes | Enter via the appropriate gateway and load only the relevant JIT context.                                                              | `Verified` static routing; native discovery `DEFER`.                      |
| Authority and security           | `rules/agentic.md`, approval boundary, provider notes                          | Default to GitOps PR-ready repository work; no secrets, destructive Git, external writes, or live mutations without explicit approval. | `Verified` static rule; provider enforcement `DEFER`.                     |
| Templates and document ownership | Stage 99 template routing and document profiles                                | Choose a canonical document route before authoring, retain source/owner links.                                                         | `Verified` static contract.                                               |
| Evaluation                       | quality standards and validation-surface contract                              | Select affected validators and report independent `PASS`/`SKIP`/`FAIL`/`DEFER` lanes.                                                  | `Verified` static controls; hosted/live execution `DEFER`.                |
| Recovery                         | agent-loop/checkpoint contracts                                                | Repository-wins resume, bounded retries, redaction, no-progress escalation, compact handoff.                                           | `Verified` contract; actual ignored checkpoint/provider behavior `DEFER`. |
| Knowledge                        | memory README, `progress.md`, owning operational/SDLC records                  | Separate working, durable, domain, and provider-local auxiliary memory.                                                                | `Verified` static owner design; provider persistence `DEFER`.             |
| Provider adapters                | `.claude/agents/`, `.codex/agents/`, shared `.agents/` content                 | Preserve role, scope, guardrails, handoff, and postflight semantics while retaining native metadata.                                   | `Verified` static parity surface; runtime consumption `DEFER`.            |

This separation follows the product evidence without collapsing it: Claude
documents persistent `CLAUDE.md` context and contextual auto memory, while
Codex documents `AGENTS.md` instruction chains and project configuration. Each
fact supports a provider edge; neither changes the local canonical owner.
[SRC-WERPC-004](source-coverage-and-migration-ledger.md#source-register) and
[SRC-WERPC-009](source-coverage-and-migration-ledger.md#source-register) record
the source boundaries.

### Application Rules by Scope

| Scope     | Apply                                                                                                                                 | Do not infer                                                                         | Security / failure response                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Work item | Bind a named request, acceptance criteria, owned paths, validation lane, evidence class, rollback, and handoff to one logical change. | A broad project policy is permission for unrelated files or external action.         | Stop/escalate when scope, authority, owner, or acceptance criterion is ambiguous.                                        |
| Session   | Rediscover tracked state; load scoped guidance; use the current task table and progress ledger; retain a compact redacted handoff.    | A prior conversation, auto memory, or ignored checkpoint overrules repository state. | Treat stale/conflicting memory as advisory; record limitation and re-plan from repository evidence.                      |
| Project   | Keep canonical policy, machine contracts, templates, validators, and durable progress under version control.                          | A repository file is automatically enforced by all clients.                          | Change the smallest canonical owner when a recurring defect demonstrates a control gap.                                  |
| Provider  | Map shared semantics to that provider's native instruction/config/hook/agent/MCP/sandbox/approval surface.                            | Equal adapter stems, filenames, or intent mean semantic/runtime equivalence.         | Record static config separately from discovery and authenticated execution; request provider-specific proof when needed. |
| CI        | Run selected static checks with bounded output and report exact path scope.                                                           | CI pass proves live cluster, provider runtime, remote action, or deployment health.  | Classify remote/live as `DEFER` unless it ran under approved authority and exact evidence is retained.                   |

### Workspace Gap and Target Matrix

| Area                        | Current evidence                                                                                                                                                                                                                                                                                         | Gap                                                                                                                      | Recommended target state                                                                                                          | Application rule                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Gateway consistency         | Root gateways point into the same bootstrap/quality/template network.                                                                                                                                                                                                                                    | Each provider discovers gateway files differently.                                                                       | Preserve provider-specific bridge/adapters and validate links, not identical discovery claims.                                    | Verify discovery with a provider-native inspection only when the claim is necessary.                       |
| Instructions                | The two root gateways are parallel, not chained: `CLAUDE.md` imports the shared bootstrap, the Claude provider note, `.claude/CLAUDE.md`, and `RTK.md`; `AGENTS.md` imports the same bootstrap, the Codex provider note, `.codex/CODEX.md`, and `RTK.md`. Neither imports the other. Checked 2026-08-10. | Gateway thinness and the no-cross-import rule are prose policy in the provider notes; no validator enforces them.        | Keep gateways thin, canonical policy once, task/scope detail JIT.                                                                 | Move repeated multi-step method to an owned skill/template, not duplicated gateway prose.                  |
| Hooks                       | Common scripts are wired in both provider trees.                                                                                                                                                                                                                                                         | Static wiring does not show trust, supported event, ordering, or block outcome.                                          | Use native permission/sandbox for authorization; hooks supply bounded context/validation/review evidence.                         | Treat a missing runtime hook as a `DEFER` limitation and run explicit quality gates.                       |
| Subagents                   | A role roster is represented on Claude and Codex surfaces.                                                                                                                                                                                                                                               | Parallel writers can collide; provider agent schemas/tools differ.                                                       | Delegate only bounded independent work, assign owned paths, collect source/evidence summaries, retain one integration owner.      | Avoid concurrent edits to shared owners; child inherits task boundary, not extra authority.                |
| MCP/external context        | Provider notes/config mention a baseline set.                                                                                                                                                                                                                                                            | Connection, OAuth/key availability, tool scope, and data flow are not inspected.                                         | Maintain an owner/sensitivity/approval inventory per enabled server.                                                              | Use read-only lookup by default; require explicit approval before writes or credential-bearing activation. |
| Sandboxing and approvals    | Repository policy identifies least-privilege and escalation boundaries.                                                                                                                                                                                                                                  | Client setting and current environment may differ.                                                                       | Default to bounded writable roots and on-request approval; state exact runtime settings only when observed.                       | Do not emulate an approval decision by changing a repository document.                                     |
| Codex project configuration | `.codex/CODEX.md`, hooks, and agents are tracked.                                                                                                                                                                                                                                                        | No project `.codex/config.toml` is tracked, so a local Codex model/sandbox/approval/MCP configuration cannot be claimed. | Keep intended provider guidance in the provider note; add a project config only through a separately approved configuration task. | Treat absence as a gap, not as a failed or unobserved runtime setting.                                     |
| Memory                      | Four authority classes and a progress ledger are explicit.                                                                                                                                                                                                                                               | Provider memory may be stale, private, or unreviewed.                                                                    | Repository-wins recovery; only reviewed/redacted lessons promote to durable/domain owners.                                        | Never write secret/raw transcript/tool output into durable memory.                                         |
| Models/runtime              | Role policy and adapters declare intended values.                                                                                                                                                                                                                                                        | Availability, reasoning options, and authentication are client/account dependent.                                        | Maintain configured/candidate/observed distinctions and evaluate before promotion.                                                | `DEFER` any resolved-model claim without the specific authenticated observation.                           |

### Target-State Rollout

The target is incremental and control-first. It does not require an external
platform migration or a new provider surface.

1. **Task discipline** — require every non-trivial task to declare owned paths,
   acceptance evidence, authority boundary, stop condition, and rollback before
   editing. Apply the state machine from the harness reference.
2. **Provider-edge honesty** — retain a per-provider matrix with static,
   discovery, and runtime columns. When a capability changes, refresh only the
   authoritative source row and affected adapter claim.
3. **Failure learning** — normalize a failure, prohibit identical no-progress
   retries, then revise the smallest shared rule/validator/template after
   review. Do not turn model prose into evidence.
4. **Controlled external context** — document each MCP/data source's owner,
   least privilege, sensitivity, refresh, and approval behavior before using it
   in a task that can mutate external state.
5. **CI/static evidence** — preserve exact local/CI results and limitations;
   add a separate approved lane rather than calling static validation live
   readiness.

### Failure and Security Boundaries

The control plane treats the following as boundary crossings rather than normal
retry candidates: permission denial, credential/secret exposure, destructive
live mutation risk, schema corruption, and an explicit user stop. The first four
escalate; the last aborts. A retry needs a different authorized action plus a
measurable progress delta. This supports security in two ways: it prevents
permission expansion by repetition and avoids turning raw diagnostics or
provider-local data into an unbounded knowledge store.

For this GitOps repository, the default execution proof is a reviewable desired
state change and repository-static checks. `kubectl apply`, controller sync,
secret mutation, force push, credential reads, and external publication stay
outside the default path. The provider's own permission feature may add
technical enforcement, but no repository declaration substitutes for explicit
human approval of the protected action.

## Sources

- **SRC-WERPC-004–008**: official Anthropic Claude Code documentation, checked
  2026-08-08, establishes product-specific surfaces only.
- **SRC-WERPC-009–013**: official OpenAI Codex documentation, first reviewed
  from `/tmp/openai-docs-cache/codex-manual.md` and its outline, checked
  2026-08-08.
- **Workspace evidence**: `AGENTS.md`, `CLAUDE.md`, `.claude/**`, `.codex/**`,
  `docs/00.agent-governance/{rules,providers,contracts}/**`, and
  `harness-catalog.md`, inspected in the WERPC worktree on 2026-08-08.

## Review and Freshness

Recheck this reference if a gateway, provider adapter, Stage 00 control,
validation contract, MCP inventory, or official provider document changes.
Provider discovery/authentication/runtime rows must be re-observed per client
and date; they cannot inherit freshness from a static-config review. The source
ledger keeps the URLs, date, claim boundary, and refresh triggers. WERPC-002 did
not inspect secret values, private configuration, accounts, or live systems.

## Related Documents

- [Harness and loop engineering](harness-and-loop-engineering.md)
- [Provider implementation status](provider-implementation-status.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Harness catalog](../../../00.agent-governance/harness-catalog.md)
- [Bootstrap governance](../../../00.agent-governance/rules/bootstrap.md)
