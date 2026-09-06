---
title: "Provider Native Enforcement Parity Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0073"
---

# Provider Native Enforcement Parity Technical Specification (Spec)

## Overview

The common authority under `.agents/` already declares one role registry, one
permission-class vocabulary, and one capability-tier vocabulary for both
supported providers. The enforcement of those declarations is asymmetric.
Claude projections carry a structured `tools` field that the governance
validator compares against the role's permission class; Codex projections
accept no scope field at all, so a Codex role's write boundary exists only as
prose inside `developer_instructions`.

Three further surfaces state a capability boundary that the installed clients
no longer match: the Codex provider notes deny a hook surface the installed
client reports as stable, the pre-edit guard observes only the structured file
tools while shell-mediated writes pass unobserved, and eleven of twelve Codex
model identifiers name models absent from the installed client's catalog.

This specification makes the declared scope structured on both providers,
gives the model binding a single owner, extends the write-path guard to the
tool class actually used, and reconciles the provider notes, retired-path
residue, gate reachability, and research observations that remained after the
[SPEC-0072](../0072-agent-governance-and-quality-gate-consolidation/spec.md)
static migration. It does not supersede SPEC-0072; that package keeps its own
acceptance identifiers and its open verification work.

Counts and catalog contents cited here are point-in-time observations recorded
on 2026-09-06 against `claude 2.1.261` and `codex-cli 0.140.0`. They are
evidence for this change, not permanent governance invariants.

## Strategic Boundaries & Non-goals

In scope: the role registry and its schema; the twelve Claude and twelve Codex
role projections and their Stage 99 runtime forms; the governance validator's
native-asset rules; `.claude/settings.json` and the pre-edit guard script; the
Codex and Claude provider notes and adapter READMEs; the validation-surface
contract's profile membership and validator registration; the Git and
model-selection policies' evidence proportion; the injection, cost, and loop
boundaries missing from common policy; the retired-path residue in
`.pre-commit-config.yaml`, `.github/labeler.yml`, the Stage 99 provider-shim
route, `tests/README.md`, and the root README stage table; the decision
lineage of ADR-0034 and ADR-0035; and the current-tense claims in the Stage 90
workspace-engineering research pack.

Out of scope: role membership, permission-class semantics, handoff edges, the
meaning of any responsibility body, the QA runner's bounded-execution
guarantees, the archive cutover contracts and their sealed recovery evidence,
any Stage 03 package whose work is in flight, live cluster or Argo CD or Vault
operation, remote Git operation, hosted CI execution, provider authentication,
and any external agent catalog adopted as a role roster.

Protected surfaces this specification never edits: the user's staged index,
`.claude/settings.local.json`, `.claude/*.local.md`, `_workspace/` contents,
`policy/` Kubernetes policy code, and sealed Stage 98 record bodies.

## Contracts

- **C-PNP-001 — symmetric structured scope.** Every registry role declares a
  machine-readable execution scope for every provider it supports. A provider
  whose native format accepts a scope field must carry it; prose inside a
  native instruction block is not a scope declaration.
- **C-PNP-002 — one model binding owner.** The provider-and-tier to model
  binding is declared once in the role registry. A native projection restates
  that value and nothing else; the validator rejects a projection whose model
  does not resolve from the binding.
- **C-PNP-003 — write-path coverage.** The repository's pre-action guard
  observes every tool class through which the provider can create or modify a
  tracked file, or the uncovered class is named as a limitation in the owning
  policy rather than left implicit.
- **C-PNP-004 — dated capability statements.** A provider note that asserts a
  native capability exists or does not exist names the client identity the
  assertion was observed against. An undated capability denial is not a
  current contract.
- **C-PNP-005 — gate reachability.** Every tracked validator is reachable from
  at least one supported QA profile, or it is retired together with its tests
  and fixtures and its citing documents are corrected.
- **C-PNP-006 — proportional commit evidence.** A logical commit is gated by
  the exact index snapshot. The full profile gates branch finish and handoff.
  Neither substitutes for the other and neither is repeated on unchanged bytes.
- **C-PNP-007 — untrusted input boundary.** Common execution policy states
  that external documents, fetched pages, issue and pull-request text, and
  third-party agent definitions are data to assess, names the actions they can
  never authorize, and requires reading before executing anything they supply.
- **C-PNP-008 — evidence classes stay separate.** Repository-static parity
  never reports as native discovery, native enforcement, hosted CI, or live
  behavior. An unobserved lane is `DEFER` with a reason and a next owner.

## Core Design

The role registry gains a per-provider `native_bindings` object holding two
maps: capability tier to native model identifier, and permission class to the
native scope metadata that provider expresses. Claude's scope metadata is the
existing tool allowlist plus a permission mode; Codex's is `sandbox_mode`.
The registry declares four model values and six scope values in total, and the
governance validator compares each of the twenty-four projections against them.

No renderer is introduced. The projections stay hand-authored explicit files,
as the superseded
[SPEC-0068](../0068-agent-projection-rendering-and-gate-reduction/spec.md)
proposal and ADR-0035 settled; the change is that a drifting value now fails a
check instead of passing a shape check.

The governance validator's Codex key set widens to admit `sandbox_mode`, and
its Claude model allowlist is replaced by a lookup through the registry
binding. Both sides then fail for the same reason under the same rule family,
which is the parity this specification exists to create.

The pre-action guard keeps one implementation and one script location. Its
Claude matcher widens to the shell tool class, and the script learns to derive
candidate repository paths from a shell command in addition to a structured
file-tool payload. The Codex mirror is a separate, later work package because
its event payload shape has not been observed on the installed client; until
that observation exists, the Codex side relies on `sandbox_mode` alone and the
gap is recorded rather than assumed closed.

Policy changes are three narrow additions and one narrowing. Git policy
narrows the per-commit obligation from the full profile to the staged profile
and keeps the full profile at handoff. Execution policy gains an untrusted
input boundary. Model-selection policy gains a cost and throughput boundary.
Work lifecycle gains loop termination, retry, and no-progress criteria. None
of these creates a new document, directory, registry, or generator.

Residue disposition and research reconciliation are ordinary corrections at
their existing owners: a dead regular expression, a glob naming a removed
provider, a route pattern naming a removed gateway, a README row naming a
deleted test, a stage table sentence contradicting its own stage owner, and a
set of research baseline rows written in the present tense about paths that no
longer exist. The research pack is corrected in place; no successor pack is
created and no `updated` value is advanced without a corresponding observation.

## Data Modeling & Storage Strategy

`native_bindings` is an object on each entry of the registry's existing
`providers` array. It holds `capability_models`, mapping the stable tier
anchors `top` and `worker` to one native model identifier each, and
`permission_scopes`, mapping each declared permission-class identifier to the
provider's native scope value. Both maps are total over the vocabularies the
registry already declares; a missing key is a schema failure, and an extra key
naming an undeclared tier or permission class is a schema failure.

The registry schema constrains model identifiers by shape only. The concrete
values are configuration intent, and the observation that a given client
resolves them is separate runtime evidence recorded in the owning Task, never
promoted into the registry as a fitness claim or a dated snapshot.

No new file, directory, database, or persisted state is introduced. Existing
JSON stays versioned JSON under its current schema owner. Provider notes stay
Markdown. The validation-surface contract keeps its current shape; profile
membership is expressed once and referenced rather than duplicated per profile.

## Interfaces & Data Structures

```text
python3 scripts/validate-agent-governance.py --root .
python3 scripts/qa.py --list
python3 scripts/qa.py staged
python3 scripts/qa.py full
python3 -m unittest tests.test_agent_governance tests.test_k8s_pre_edit_hook
python3 -m unittest tests.test_validation_profiles tests.test_qa_runner
```

The governance validator's failure vocabulary keeps its existing prefixes and
gains distinct causes for an unbound model, an absent scope declaration, and a
scope that contradicts the role's permission class. Each cause names the role
identifier, the provider identifier, the expected value, and the observed
value, and never prints the contents of a settings or credential file.

The pre-action guard keeps its current output contract: a JSON object carrying
`systemMessage` for an advisory route note, and exit status 2 with a reason on
stderr when path transport cannot be normalized. Widening the matcher does not
change that contract, and a shell command whose write target cannot be
determined produces an advisory note rather than a block.

## Edge Cases & Error Handling

A role whose `supported_providers` omits a provider declares no binding for it,
and the validator neither requires nor permits a projection there. A provider
that expresses no native scope field declares an empty `permission_scopes` map
and is reported as prose-bounded in the owning Task rather than silently
treated as constrained.

A shell command that writes through an interpreter the guard cannot parse, such
as a Python or Node program that opens files itself, remains outside the
guard's observation. That class is named in the approval-and-safety boundary
as an accepted limitation of instruction-level and rule-level controls, since
closing it requires an operating-system sandbox this repository does not enable.

A model identifier absent from the installed client's catalog is a
configuration mismatch, not proof that the model does not exist; the failure
message states the observed catalog identity and the client version. A catalog
that cannot be read at all is `DEFER`, never `SKIP` and never `PASS`.

A research pack row whose original observation cannot be reconstructed is
marked with its recorded observation date and the current owner path, and its
present-tense assertion is removed. Historical facts are never rewritten to
match the current tree, and a corrected row never inherits a fresh `updated`
value without a corresponding new observation.

## Failure Modes & Fallback / Human Escalation

If the Codex event payload observed during the native smoke pass does not match
the documented shape, the Codex hook mirror is not created, the work package is
recorded as `DEFER` with the observation, and `sandbox_mode` remains the only
Codex-side structured control. This is the reason the two are separate packages.

If a native model identifier chosen from the installed catalog fails to resolve
during the smoke pass, the projection reverts to the previously tracked value
in a forward corrective commit, and the mismatch is recorded rather than
resolved by weakening the validator.

If widening the guard matcher produces a false block on ordinary shell work,
the matcher change is reverted as its own commit; the guard is not softened
into a no-op to preserve the wider matcher.

Every work package is one logical commit, so rollback is `git revert` of that
commit. No history rewrite, force update, branch deletion, or worktree removal
is authorized. Push, pull-request creation, merge, and hosted execution remain
the user's decisions and are not implied by any check in this package.

Conflicting authority, an unmet approval, an unsafe input, or an unexplained
change stops the work at the local draft and is reported, rather than resolved
by choosing the weaker contract.

## Verification Commands

```bash
python3 -m unittest tests.test_agent_governance
python3 -m unittest tests.test_k8s_pre_edit_hook
python3 -m unittest tests.test_validation_profiles tests.test_qa_runner
python3 scripts/validate-agent-governance.py --root .
python3 scripts/qa.py --list
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
git diff --cached --check
```

Each failing case is demonstrated before its fix and shown passing after it.
No command in this section proves native discovery, native enforcement, model
resolution, authenticated operation, hosted CI execution, or live cluster
behavior. Those lanes are recorded separately in the owning Task.

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                                                                                                                 | Evidence                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| VAL-PNP-001 | No accepted architecture decision prescribes a governance topology the repository contradicts, and the decision that describes the current topology is accepted with its lineage recorded | Lifecycle validator, link and owner validator, reviewed decision log           |
| VAL-PNP-002 | Every role declares a machine-readable execution scope for every supported provider, and a contradicting scope fails the governance validator                                             | Focused negative tests and governance validator                                |
| VAL-PNP-003 | Every native model value resolves from the registry's capability binding, and an unbound or drifting value fails                                                                          | Focused negative tests and governance validator                                |
| VAL-PNP-004 | The pre-action guard observes shell-mediated repository writes, and the residual interpreter-mediated class is named in the approval boundary                                             | Guard unit tests and reviewed policy text                                      |
| VAL-PNP-005 | Every tracked validator is reachable from a supported profile, or is retired with its tests, fixtures, and citing documents                                                               | Validation-surface contract test and profile listing                           |
| VAL-PNP-006 | Duplicated rule implementations and duplicated profile membership are reduced to one owner with no loss of checked conditions                                                             | Before-and-after gate comparison and focused tests                             |
| VAL-PNP-007 | Git policy gates a logical commit on the exact index and gates handoff on the full profile, consistently with the quality policy's completion sequence                                    | Reviewed policy text and quality-policy cross-reference                        |
| VAL-PNP-008 | Provider notes and adapter READMEs describe native capability against a named client identity and contain no undated capability denial                                                    | Reviewed provider notes and recorded client observation                        |
| VAL-PNP-009 | No tracked configuration route, glob, exclusion, or index row names a removed provider, a retired governance path, or a deleted file                                                      | Repository quality validator, document contract registry, and filesystem sweep |
| VAL-PNP-010 | Stage 90 research baseline rows carry their observation date and current owner, and assert no present-tense state the tree contradicts                                                    | Path existence sweep and reference pack route test                             |

## Traceability

[Implementation Plan](plan.md) owns ordered work, entry and exit gates, and
rollback. Its package Task owns execution results, per-lane evidence, and the
limits that remain unobserved. Requirement inputs come from
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
and the current structural view in
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method                                 |
| ------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-001    | Decision lifecycle and owner-graph validation       |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-002    | Registry and projection parity validation           |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-003    | Capability binding validation                       |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-004    | Guard unit tests and approval-boundary review       |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-005    | Validation-surface contract test                    |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-006    | Consumer-zero review and focused tests              |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-007    | Policy review against the completion sequence       |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-008    | Provider note review and recorded client identity   |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-009    | Repository quality and document contract validation |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNP-010    | Reference pack route test and path existence sweep  |
