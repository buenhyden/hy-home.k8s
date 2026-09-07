---
title: "Provider Native Enforcement Parity Technical Specification"
version: "1.1.1"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0073"
---

# Provider Native Enforcement Parity Technical Specification (Spec)

## Overview

The common authority under `.agents/` already declared one role registry, one
permission-class vocabulary, and one capability-tier vocabulary for both
supported providers. At drafting, the enforcement of those declarations was
asymmetric: Claude projections carried a structured `tools` field the
governance validator compared against the role's permission class, while Codex
projections accepted no scope field at all, so a Codex role's write boundary
existed only as prose inside `developer_instructions`.

Three further surfaces then stated a capability boundary the installed clients
no longer matched. The Codex provider notes denied a hook surface the client
reported as stable, the pre-edit guard observed only the structured file tools
while shell-mediated writes passed unobserved, and eleven of twelve Codex model
identifiers named models absent from the installed client's catalog.

Those conditions are the ones this package addressed, not the current state of
the tree. Both providers now declare a structured scope the validator reads
from one registry, each provider registers its own thin adapter over one
shared guard program, every native model resolves from the capability binding,
and the provider notes date their capability statements. The single registered
script this package left behind was replaced by that adapter pair under
[SPEC-0074](../0074-provider-write-guard-ownership-and-enforcement-honesty/spec.md),
which moved the guard program out of a provider directory so no provider owns a
control the other depends on. This paragraph is stated in the past tense on purpose:
VAL-PNP-010 forbids a document from asserting a present-tense state the tree
contradicts, and a specification whose work has landed is bound by that rule
like any other current document.

This specification made the declared scope structured on both providers,
gave the model binding a single owner, extended the write-path guard to the
tool class actually used, and reconciled the provider notes, retired-path
residue, gate reachability, and research observations that remained after the
[SPEC-0072](../0072-agent-governance-and-quality-gate-consolidation/spec.md)
static migration. It does not supersede SPEC-0072; that package keeps its own
acceptance identifiers and its open verification work.

Counts and catalog contents cited here are point-in-time observations recorded
on 2026-09-06 against `claude 2.1.261` and `codex-cli 0.140.0`. Both clients
moved during execution and were re-observed the same day as `claude 2.1.263`
and `codex-cli 0.153.4`; the earlier reading is kept as the observation this
specification was drafted against rather than rewritten to match the later
tree. They are evidence for this change, not permanent governance invariants.

## Strategic Boundaries & Non-goals

In scope: the role registry and its schema; the twelve Claude and twelve Codex
role projections and their Stage 99 runtime forms; the governance validator's
native-asset rules; `.claude/settings.json`, `.codex/hooks.json`, and the one
pre-edit guard script both providers register; the Codex and Claude provider
notes and adapter READMEs; the validation-surface contract's profile membership
and validator registration; the Git and model-selection policies' evidence
proportion; the injection, cost, and loop boundaries missing from common
policy; the domain memory layer's routing to its operating owner; the
retired-path residue in `.pre-commit-config.yaml`, `.github/labeler.yml`, the
Stage 99 provider-shim route, `tests/README.md`, and the root README stage
table; the decision lineage of ADR-0034 and ADR-0035; the current-tense claims
in the Stage 90 workspace-engineering research pack; the handoff evidence
contract's snapshot and boundary fields; the empty evaluation boundary under
`evals/` and the runner and index row it needs; and the absent project editor
configuration together with the ignore pattern that kept it untracked.

Every surface named here is listed as an allowed path in the package Task,
which owns the concrete write boundary. A surface reached during execution but
absent from that list is a boundary defect to reconcile and record, not a
silent widening.

Out of scope: role membership, permission-class semantics, handoff edges, the
meaning of any responsibility body, the QA runner's bounded-execution
guarantees, the archive cutover contracts and their sealed recovery evidence,
any Stage 03 package whose work is in flight, live cluster or Argo CD or Vault
operation, remote Git operation, hosted CI execution, provider authentication,
and any external agent catalog adopted as a role roster.

One narrow exception applies to a record this package does not own: when a
repository gate rejects a specific line in such a record, the correction is
limited to the line the gate named and is recorded with the gate that forced
it. That happened once, to a `SPEC-0054` Task record carrying an absolute local
checkout path. Nothing else in an unowned package was touched, and the
exception never extends to that package's meaning, status, or work.

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
  and fixtures and its citing documents are corrected. A retired validator
  identifier does not return: a new rule takes a name no retired rule held, so
  that an identifier never carries a meaning its own history contradicts.
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

Each entry of the registry's `providers` array gains two sibling maps:
`capability_models`, from capability tier to native model identifier, and
`permission_scopes`, from permission class to the native scope value that
provider expresses. Claude's scope value is its tool allowlist; Codex's is
`sandbox_mode`. The registry declares four model values and six scope
entries, and the governance validator compares each of the twenty-four native
projections against them.

A role whose native authority genuinely differs from its permission class
declares `native_scope_override` rather than departing silently, so the
exception stays declared data that the validator reads instead of a role
identifier special-cased in validator code.

Claude's `permissionMode` is not bound. The tool allowlist is the enforced
structured scope, and whether `permissionMode` changes a subagent's authority
at all was not observed on this client; binding an unobserved field would
state a boundary the repository cannot show holds.

No renderer is introduced. The projections stay hand-authored explicit files,
as the superseded
[SPEC-0068](../0068-agent-projection-rendering-and-gate-reduction/spec.md)
proposal and ADR-0035 settled; the change is that a drifting value now fails a
check instead of passing a shape check.

The governance validator's Codex key set widens to admit `sandbox_mode`, and
its Claude model allowlist is replaced by a lookup through the registry
binding. Both sides then fail for the same reason under the same rule family,
which is the parity this specification exists to create.

The pre-action guard kept one implementation in one script location; SPEC-0074
later split the registration into a per-provider adapter over one shared
program while keeping the single implementation. Its
Claude matcher widens to the shell tool class, and the script learns to derive
candidate repository paths from a shell command in addition to a structured
file-tool payload. The Codex mirror stays a separate, later work package,
gated on observing the installed client's event payload shape rather than
assumed from the Claude side. That observation arrived during execution:
`codex-cli 0.153.4` documents `<repo>/.codex/hooks.json`, the `PreToolUse`
event, the `command` handler, and the `tool_name`, `tool_input`, and
`tool_input.command` fields the guard already reads. The mirror therefore
landed, both providers registered the one guard script, and the frozen
per-provider hook literal in the validator is replaced by one property
contract both are judged under. Native event delivery remains unobserved.

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

`capability_models` and `permission_scopes` are objects on each entry of the
registry's existing `providers` array. `capability_models` maps the stable tier
anchors `top` and `worker` to one native model identifier each;
`permission_scopes` maps each declared permission-class identifier to the
provider's native scope value. Both maps are total over the vocabularies the
registry already declares; a missing key is a schema failure, and an extra key
naming an undeclared tier or permission class is a schema failure. A role's
optional `native_scope_override` names a provider and the scope that replaces
the class default for that role alone.

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
python3 -m unittest tests.test_agent_evaluations
python3 -m unittest tests.test_validation_tooling_ownership
python3 scripts/validate-agent-governance.py --root .
python3 scripts/run-agent-evaluations.py --root .
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
| VAL-PNP-005 | Every tracked validator is reachable from a supported profile, or is retired with its tests, fixtures, and citing documents, and no retired identifier is re-registered                    | Validation-surface contract test, profile listing, and the retired-alias ban   |
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
