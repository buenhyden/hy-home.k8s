---
title: "Common Agent Governance"
version: "1.1.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-10"
---

# Common Agent Governance

## Overview

This is the single common policy, role and skill authority for this GitOps
workspace. Its files are read through explicit gateways or native skill
loaders; the entire directory is not an automatic instruction loader.

## Structure

| Path | Responsibility |
| --- | --- |
| [governance/sdlc.md](governance/sdlc.md) | Normative lifecycle and terminology |
| `governance/` | Approval, safety, quality, Git, documents, context and model policy |
| [roles/README.md](roles/README.md) | Responsibility selection and common handoff contracts |
| [roles/registry.json](roles/registry.json) | Role IDs, permissions, skill references and native paths |
| `skills/<id>/` | Callable common procedure packages; registry determines the package set |
| `workflows/` | Ordinary lifecycle/delegation procedures, explicitly read |
| `knowledge/` | Hand-maintained pointers to canonical owners; states no policy of its own |
| `prompts/` | Input and output contracts for repeatable authoring requests |

### Skill package

A package holds `SKILL.md` and the `agents/` sidecar both providers read. It may
hold three more directories when the procedure needs them: `references/` for
Markdown the steps point at instead of restating, `scripts/` for a helper the
steps run, and `assets/` for a file the output is built from. Reaching for one
is a judgment about what the material is — a step belongs in `SKILL.md`, and
everything else belongs where a reader can skip it.

The package stays a closed set. `SKILL.md` names every file in those
directories, so nothing a provider loads is unreachable from the procedure that
owns it, and an empty directory is refused rather than left as a placeholder.

Two boundaries keep the new directories from becoming second authorities, and
both are enforced rather than advised. A skill script is a helper and never a
gate: `scripts/validation/registry.json` refuses a gate whose script lives in a
package, so editing a skill can never change what QA enforces. An asset is a
resource and never a document template: Stage 99 owns those and the route that
reaches them, so the name `*.template.md` is refused here.

## Configuration Boundary

Provider differences and native adapters live in [.claude/](../.claude/README.md)
and [.codex/](../.codex/README.md). Edit common meaning here; retain native syntax
there. No role copies or provider generator own a second policy.
ADR-0036 (`docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`)
adopts `knowledge/` and `prompts/`; each is delivered with a Stage 99 profile,
affected-surface coverage and at least one named consumer, so a directory
without a reader is not created. Evaluation, rule and script directories stay
unadopted, each for its own reason: root `evals/` holds evaluation case and
response data, `scripts/run-agent-evaluations.py` owns runner behavior, and
`scripts/validation/registry.json` owns gate selection; a rule directory would
duplicate policy `governance/` already owns; and `scripts/` already owns
executable tooling at the repository root, which a package-local helper does
not displace because it can never be a registered gate. MIG-0009's memory retirement
remains effective.

## Validation

Run `python3 scripts/validate-agent-governance.py --root .` for role, skill,
permission and routing contracts; run `python3 scripts/qa.py full` for final
repository-static evidence. No generator is used. Native discovery, invocation,
permissions and hook delivery require separate evidence from a fresh session.

## Operations

Read [work lifecycle](workflows/work-lifecycle.md),
[agent execution](governance/agent-execution.md) and
[approval and safety](governance/approval-and-safety.md) before acting. Select
[roles](roles/README.md), then explicitly read the chosen role and its required
skills. Both providers expose the same common skill packages for explicit
invocation. A skill does not grant permission to write, send, deploy or read
secrets. [Quality](governance/quality.md) owns evidence semantics, while the
execution registry owns mutable gate commands and limits.

## Related Documents

- Document profiles and templates (`docs/99.templates/README.md`)
- [Repository documentation](../docs/README.md)
- Memory retirement: MIG-0009 through the archive index (`docs/98.archive/README.md`)
- Authority decision (`docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`)
