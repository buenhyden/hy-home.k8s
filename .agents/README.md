---
title: "Common Agent Governance"
version: "1.3.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-29"
---

# Common Agent Governance

## Overview

This is the single common policy, role and skill authority for this GitOps
workspace. Its files are read through explicit gateways or native skill
loaders; the entire directory is not an automatic instruction loader.

## Structure

| Path | Responsibility |
| --- | --- |
| [governance/](governance/) | Normative lifecycle and terminology (sdlc.md); approval, safety, quality, Git, documents, context and model policy |
| [roles/](roles/) | Responsibility selection and common handoff contracts; `roles/registry.json` holds role IDs, permissions, skill references and native paths |
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

The package stays a closed set. Every resource is reachable from `SKILL.md`,
either directly or through other package resources. The bounded traversal
allows nested directories and terminates cycles; it rejects empty directories,
orphans, symlinks and non-regular files. References are Markdown, scripts are
Python or shell, and assets are dedicated output resources.

`scripts/validation/registry.json` alone selects QA gates. It may select a
registered skill's checker under that package's `scripts/` directory; carrying
a checker does not register it or grant execution authority. Dedicated assets
may include `*.template.md` output forms. Stage 99 still owns shared document
profiles and templates; a package asset cannot replace their authority.

## Configuration Boundary

Provider differences and native adapters live in [.claude/](../.claude/)
and [.codex/](../.codex/). Edit common meaning here; retain native syntax
there. No role copies or provider generator own a second policy.
[Governance](governance/) and the prompt contracts
own `knowledge/` and `prompts/`; each is delivered with a Stage 99 profile,
affected-surface coverage and at least one named consumer, so a directory
without a reader is not created. Evaluation, rule and script directories stay
unadopted, each for its own reason: root `evals/` holds evaluation case and
response data, `scripts/run-agent-evaluations.py` owns runner behavior, and
`scripts/validation/registry.json` owns gate selection; a rule directory would
duplicate policy `governance/` already owns; and `scripts/` already owns
executable tooling at the repository root, which a dedicated package checker does
not displace; the central registry still selects every gate. MIG-0009's memory retirement
remains effective.

## Validation

Run `python3 scripts/validate-agent-governance.py --root .` for role, skill,
permission and routing contracts; run `python3 scripts/qa.py full` for final
repository-static evidence. No generator is used. Native discovery, invocation,
permissions and hook delivery require separate evidence from a fresh session.

## Operations

Read [work lifecycle](workflows/work-lifecycle.md),
[agent execution](governance/agent-execution.md) and the approval and safety
policy in `governance/` before acting. Select
[roles](roles/README.md), then explicitly read the chosen role and its required
skills. Both providers expose the same common skill packages for explicit
invocation. A skill does not grant permission to write, send, deploy or read
secrets. The quality policy in `governance/` owns evidence semantics, while the
execution registry owns mutable gate commands and limits.

## Related Documents

- Document profiles and templates (`docs/99.templates/README.md`)
- [Repository documentation](../docs/README.md)
- Memory retirement: MIG-0009 through the archive index (`docs/98.archive/README.md`)
- [Governance contracts](governance/)
