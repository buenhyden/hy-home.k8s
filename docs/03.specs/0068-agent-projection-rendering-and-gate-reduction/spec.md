---
title: 'Agent Projection Rendering and Gate Reduction Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: draft
owner: platform
updated: 2026-09-02
artifact_id: "SPEC-0068"
---

# Agent Projection Rendering and Gate Reduction Technical Specification (Spec)

## Overview

Twelve agent roles are declared once in `.agents/registry.json` and then written
out three times by hand: a provider-neutral body under `.agents/agents/`, a
Claude projection under `.claude/agents/`, and a Codex projection under
`.codex/agents/`. The three bodies are byte-identical. Only the frontmatter
binding differs, and that binding has drifted into three generations of model
strings, none of which the Claude runtime accepts as written.

[ADR-0030](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
already decided against this shape. It requires provider directories to hold
"thin metadata and configuration required by their runtimes" that "do not
duplicate common policy", places point-in-time model and provider evidence in
Stage 90 Data rather than Stage 00 contracts, and bounds permanent static
validation of the agent surface to three responsibilities. The tracked surface
satisfies none of the three clauses. This Spec is a conformance repair, not a
new architectural decision, and no successor ADR is required.

This Spec makes the provider projections a rendered artifact of the registry,
moves the tier-to-model binding into the registry that already owns the tier,
and retires the validators and fixtures whose question disappears once the
duplication does.

Measured counts below are point-in-time audit evidence recorded on 2026-09-02.
They are not permanent governance invariants.

## Strategic Boundaries & Non-goals

In scope: the tier-to-model and permission-to-tool bindings in
`.agents/registry.json` and its schema; a renderer that derives
`.claude/agents/*.md` and `.codex/agents/*.toml` from the registry and the
Stage 00 responsibility bodies; the merged agent-surface validator; retirement
of the unwired checkpoint surface and the stale provider-evidence surface;
the Stage 99 profiles and templates covering the four runtime asset families;
the phantom `memory/` references; the WP-011 compatibility residue; and the
links in closed records that point at retired contracts.

Out of scope: role membership, permission-class semantics, handoff edges, the
meaning of any responsibility body, the agent loop lifecycle contract, the
governance CI topology contract, hook scripts and their wiring, live runtime
verification of any kind, and any model family beyond the current generation the
human owner authorized.

This Spec changes declaration, derivation, and gate inventory. It does not
claim that any rendered projection was discovered, loaded, authenticated, or
executed by a provider runtime. Repository-static parity proves that the tracked
bytes match the registry, and nothing further.

## Contracts

- **C1 — Single binding owner.** `.agents/registry.json` is the sole machine
  owner of the capability tier, its per-provider native model binding, and the
  permission-class tool baseline. No other tracked file declares a model value
  for a role.
- **C2 — Projections are derived.** Every path named in a role's `projections`
  map for a provider other than `neutral` is reproducible from the registry and
  the Stage 00 responsibility bodies. A tracked projection that differs from its
  render fails closed.
- **C3 — No inert directives.** No instruction file carries an import directive
  that its consuming runtime does not resolve. Cross-file scope is expressed as
  an instruction the agent can act on, not as syntax the runtime ignores.
- **C4 — One profile per asset family.** Each tracked runtime asset family has
  exactly one Stage 99 profile whose template matches the family's file format.
  No profile covers two families, and no tracked runtime asset family is
  uncovered.
- **C5 — A retired contract leaves no live link.** Deleting a contract file
  leaves no resolvable link to it. Closed records keep the historical fact as
  literal text rather than as a broken link.
- **C6 — A gate exists only if invoked.** Every validator under `scripts/` that
  targets the agent surface is reachable from a lane in
  `scripts/validation/registry.json` or from a gate or delegated check in
  `docs/00.agent-governance/contracts/agent-governance-ci.json`. A validator
  whose only consumers are its own tests is not a gate.
- **C7 — Tier declaration binds.** A role's rendered model value is the binding
  of the tier its registry entry names. A projection may not carry a binding
  from a tier the registry did not assign.

## Core Design

### Binding relocation

The registry gains `capability_tiers`, keyed by the anchor that
`capability_tier_ref` already resolves to, and each `permission_classes` entry
gains a native tool baseline. The audit found the existing tool assignment is
already a total function of permission class with exactly one exception, so the
baseline reproduces eleven of twelve roles and `docs-researcher` carries a
role-level override.

Both tiers bind to the current generation of each provider's family, which the
human owner authorized explicitly. That authorization is what the model
selection policy requires before a promotion; the conformance argument alone
would not carry it.

Claude binds through the account-available aliases that
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
names as the candidate surface: `opus` for the top tier and `sonnet` for the
worker tier. An alias resolves to the current model of its family at load time,
so the repository does not have to be edited when a generation ships. This
closes the drift class at its source instead of re-checking it with a gate. The
strings `sonnet 4.6`, `Sonnet 5`, and `opus 4.8` are retired; none of them is a
value the runtime accepts as written.

Codex has no alias surface, so each tier names a concrete identifier. Stage 90
research member
[RES-0001-m0010](../../90.references/research/0001-workspace-engineering/m0010-agent-model-routing-and-configuration.md)
records the current published workload assignment as of its 2026-08-23
observation: `gpt-5.6` for the most demanding work, `gpt-5.6-terra` for
read-heavy analysis, and `gpt-5.6-luna` for narrow high-volume work. The top
tier binds `gpt-5.6` and the worker tier binds `gpt-5.6-terra`, whose read-heavy
description matches the review-dominated worker set.

The audit initially read `gpt-5.6-terra` on `docs-researcher` and
`quality-engineer` as drift from the Stage 00 fixture. The reverse is true: that
fixture's cutoff is 2026-07-10 and the Stage 90 observation is 2026-08-23, so
those two roles were current and the other ten were not. This is one more reason
the fixture is the wrong owner for a value that changes on the provider's
schedule rather than the repository's.

Two roles are promoted by tier rather than by generation. `incident-responder`
and `security-auditor` are declared `#top` by the registry and carry the worker
binding in their projections. C7 resolves the contradiction toward the registry,
which is the authority.

Per RES-0001-m0010, a published model identifier is a dated documentation fact,
not proof of account availability, entitlement, resolution, fitness, or absence
of silent fallback. Every claim in this Spec about a model value is a claim
about tracked configuration bytes and nothing more.

### Renderer

`scripts/render-agent-projections.py` reads the registry and the Stage 00
responsibility bodies and emits both provider projections. It runs in two modes:
`--write` updates the tree, and `--check` compares the render against the tree
and exits non-zero on any difference. The check mode is what the gate invokes,
so drift is detected without the gate holding a second copy of the rendering
rules.

The renderer replaces the inert `@import` directive required by C3. Neither
consuming runtime resolves it: Claude Code's memory import syntax is `@path`
rather than `@import path` and does not apply to subagent bodies, and the Codex
`developer_instructions` field is a plain TOML string. The rendered bootstrap
names the same files as an explicit read instruction the agent can act on.

### Gate reduction

The audit found 12,663 lines of agent-surface validator and contract guarding
1,800 lines of projection whose bodies are triplicated: 8,178 lines across nine
validators and 4,485 lines across seven contract and schema files. Two surfaces
are retired outright.

The checkpoint surface — `scripts/validate-agent-checkpoint.py` and
`docs/00.agent-governance/contracts/agent-checkpoint.schema.json`, 2,408 lines —
is referenced by no lane, no CI gate, and no delegated check. Its only consumers
are its own test module and a test fixture inventory, so it fails C6.

The provider evidence surface — `provider-runtime-evidence.json` and its schema,
`validate-agent-provider-config.py`, `validate-agent-provider-canaries.py`, and
the `validate-agent-provider-evidence.py` wrapper, 3,195 lines — holds a fixture
whose cutoff is 2026-07-10 while its own observation history records 2026-07-28,
four of whose six canary records are synthetic and not executed, and which
carries the same invalid model strings this Spec removes. ADR-0030 places
point-in-time provider evidence in Stage 90 Data, so a Stage 00 contract is the
wrong owner regardless of staleness. Git history is the recovery path.

`validate-agent-harness-contract.py` and `validate-agent-harness-semantics.py`
merge into `scripts/validate-agent-registry-projection.py`, which covers the
three permanent responsibilities ADR-0030 names: registry and schema validity,
provider projection conformance, and semantic and permission integrity. Render
parity is one of its assertions rather than a separate comparison of three
hand-maintained copies.

`validate-agent-governance-ci.py`, `validate-agent-legacy-cutover.py`, and
`validate-agent-loop-lifecycle.py` remain. They own CI topology, retirement
proof, and the loop contract, which are not agent-surface static validation.

### Stage 99 profile rewiring

Four runtime asset families exist and three profiles cover them, incorrectly.
`exception/local-agent-asset` covers both `.agents/agents/` and
`.agents/skills/` and points at a Codex-named template; `.codex/agents/*.toml`
is covered by nothing because every profile pattern is Markdown-only. The
profiles split one per family, each with a template in the family's own format.

## Data Modeling & Storage Strategy

The registry gains two structures, both validated by
`.agents/contracts/agent-registry.schema.json`.

`capability_tiers` is an array of objects with a required `id` matching the
anchor in `capability_tier_ref`, and a `bindings` object keyed by provider `id`.
Each binding carries the provider's native configuration keys and nothing else:
`model` for Claude, and `model` with `model_reasoning_effort` for Codex. The
schema constrains provider keys to the declared `providers` list so a binding
cannot name an unknown provider.

Each `permission_classes` entry gains `claude_tools`, an array of Claude tool
names that is the baseline for every role in that class. A role entry may carry
an optional `tools_override` array that replaces, rather than extends, the
baseline; replacement is chosen because the single existing exception both adds
and removes tools relative to its class.

No new file is introduced to hold binding data. The retired
`provider-runtime-evidence.json` is not relocated: its content is point-in-time
observation whose owner is a closed Spec, and Git history is its recovery path
under ADR-0030's consumer-zero-plus-recovery rule.

## Interfaces & Data Structures

`scripts/render-agent-projections.py`:

| Invocation | Behavior | Exit |
| --- | --- | --- |
| `--root . --write` | Writes both provider projections for every role | `0` on success |
| `--root . --check` | Compares render against tree, reports each differing path | `0` identical, `1` on any difference |

The renderer emits a stable byte sequence: keys in the registry-declared order,
LF line endings, one trailing newline, and TOML string values escaped for the
Codex `developer_instructions` and `description` fields.

`scripts/validate-agent-registry-projection.py --root . [--mode strict]` reports
one line per assertion in the repository's existing PASS/FAIL vocabulary and
exits non-zero on any FAIL. Its diagnostic codes are `REGISTRY-SCHEMA-INVALID`,
`REGISTRY-TIER-UNKNOWN`, `REGISTRY-PROVIDER-UNKNOWN`, `PROJECTION-MISSING`,
`PROJECTION-ORPHANED`, `PROJECTION-RENDER-DIFFERS`, `PROJECTION-BINDING-DIFFERS`,
and `PROJECTION-PERMISSION-DIFFERS`.

## Edge Cases & Error Handling

A role naming a tier absent from `capability_tiers` fails with
`REGISTRY-TIER-UNKNOWN` rather than rendering an empty model value, because an
absent binding would otherwise produce a projection the runtime silently
defaults.

A binding naming a provider absent from `providers` fails with
`REGISTRY-PROVIDER-UNKNOWN` at schema validation, before the renderer runs.

A projection file present under a provider root with no corresponding registry
role fails with `PROJECTION-ORPHANED`. The renderer does not delete it; removal
of a role is a registry change that must be authored deliberately.

A role whose `supported_providers` omits a provider produces no projection for
that provider, and an existing file at that path is an orphan by the rule above.

A `description` or responsibility body containing a double quote, a backslash,
or a newline is escaped for TOML rather than emitted literally, because
`developer_instructions` is a multi-line basic string and an unescaped delimiter
would produce a file that parses as different content than it renders.

A tracked projection differing from its render only in trailing whitespace or
line endings still fails `PROJECTION-RENDER-DIFFERS`, because byte parity is the
contract and a normalizing comparison would admit an editor's rewrite as
equivalent.

## Failure Modes & Fallback / Human Escalation

If the renderer is absent or raises, the gate reports FAIL rather than skipping
the assertion. A rendering surface that cannot run is not evidence that the tree
matches it.

If render parity fails during ordinary work, the resolution is to re-run
`--write` and review the diff, not to edit the projection. A projection edit
that the registry does not produce is drift by construction and will fail again.

Rollback for any step is a Git revert of that step's commit. No step mutates a
sealed Stage 98 payload, and no step is externally visible, so no rollback
requires coordination beyond the repository.

Escalate to the human owner when the render would change a model value for a
role beyond the two promotions this Spec authorizes, when a closed record's link
cannot be lowered to literal text without changing the record's meaning, or when
retiring a gate would leave an assertion in this Spec's contracts unproven.

## Verification Commands

```bash
python3 scripts/render-agent-projections.py --root . --check
python3 scripts/validate-agent-registry-projection.py --root . --mode strict
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 -m unittest discover --start-directory tests --top-level-directory tests
bash scripts/validate-repo-quality-gates.sh .
```

Every command above is repository-static. None of them proves native discovery,
model resolution, authentication, or execution by a provider runtime.

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-APR-001 | The registry declares every tier-to-model binding and permission-to-tool baseline, and no other tracked file declares a model value for a role | Registry schema validation plus a repository sweep for model values outside the registry |
| VAL-APR-002 | Both provider projections render reproducibly from the registry and Stage 00 bodies for all twelve roles | `render-agent-projections.py --check` exits `0` |
| VAL-APR-003 | Every rendered binding is the current generation of its provider family, and no projection carries a superseded generation string | Rendered-value assertion plus absence sweep for `sonnet 4.6`, `Sonnet 5`, `opus 4.8`, `gpt-5.5`, `gpt-5.3-codex` |
| VAL-APR-004 | Each role's rendered binding is the binding of the tier its registry entry names | Tier-parity assertion covering all twelve roles, including the two promotions |
| VAL-APR-005 | No tracked instruction file carries an import directive its runtime does not resolve | Absence sweep for `@import` across `.agents/`, `.claude/`, `.codex/` |
| VAL-APR-006 | The checkpoint surface is removed and no lane, CI gate, delegated check, or test references it | Deletion plus consumer-zero sweep |
| VAL-APR-007 | The provider evidence surface is removed and no live consumer or link remains | Deletion plus consumer-zero sweep and strict link validation |
| VAL-APR-008 | The two harness validators are replaced by one validator covering the three ADR-0030 responsibilities, and the wrapper gate is gone | Merged validator strict run plus absence of the retired entrypoints |
| VAL-APR-009 | Every remaining agent-surface validator is reachable from a lane or the CI contract | Reachability sweep over `scripts/validation/registry.json` and `agent-governance-ci.json` |
| VAL-APR-010 | Each of the four runtime asset families has exactly one Stage 99 profile whose template matches its file format, and none is uncovered | Strict document contract registry run with zero uncovered and zero ambiguous paths |
| VAL-APR-011 | No tracked file references the absent `docs/00.agent-governance/memory/` directory, in prose or in a path pattern | Absence sweep across settings, contracts, and the Stage 99 registry |
| VAL-APR-012 | The WP-011 compatibility residue is removed and no retired-form reference remains outside sealed payloads | Absence sweep for the retired markers |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| N/A — ADR-0030 thin-projection clause | VAL-APR-001 | Single-owner binding audit across registry and tracked tree |
| N/A — ADR-0030 thin-projection clause | VAL-APR-002 | Render parity check across both providers |
| N/A — authorized current-generation binding | VAL-APR-003 | Rendered-value assertion and superseded-string absence sweep |
| N/A — approved tier promotion | VAL-APR-004 | Tier-parity assertion over the full role set |
| N/A — drift and inert-directive retirement | VAL-APR-005 | Import-directive absence sweep |
| N/A — ADR-0030 three-responsibility bound | VAL-APR-006 | Consumer-zero proof and deletion evidence |
| N/A — ADR-0030 Stage 90 evidence placement | VAL-APR-007 | Consumer-zero proof, deletion evidence, strict link validation |
| N/A — ADR-0030 three-responsibility bound | VAL-APR-008 | Merged validator strict run and retired-entrypoint absence |
| N/A — gate reachability contract | VAL-APR-009 | Lane and CI contract reachability sweep |
| N/A — approved profile rewiring | VAL-APR-010 | Strict registry coverage run with zero uncovered paths |
| N/A — drift retirement | VAL-APR-011 | Phantom-path absence sweep |
| N/A — legacy and deprecated retirement | VAL-APR-012 | Retired-marker absence sweep |

### Related Documents

- [Package router](README.md)
- [Current Spec Index](../README.md#current-spec-index)
- [ADR-0030 — authority-first SDLC and agent governance convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- [Agent Registry](../../../.agents/registry.json)
- [Model Selection Policy](../../00.agent-governance/policies/model-selection.md)
- [Claude Provider](../../00.agent-governance/providers/claude.md)
- [Codex Provider](../../00.agent-governance/providers/codex.md)
- [Quality Policy](../../00.agent-governance/policies/quality.md)
