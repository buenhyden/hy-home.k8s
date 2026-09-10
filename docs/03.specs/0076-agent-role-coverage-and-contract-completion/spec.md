---
title: "Agent Role Coverage and Contract Completion Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-10"
layer: "specs"
artifact_id: "SPEC-0076"
---

# Agent Role Coverage and Contract Completion Technical Specification (Spec)

## Overview

The agent registry admits twelve roles. The responsibility router at
`.agents/roles/README.md` declares seven domain boundaries, and the role bodies
read six of them: documentation three times, infrastructure three, operations
twice, quality twice, security once and supervision once. No role reads the
architecture boundary, while twenty-nine accepted decisions under
`docs/02.architecture/decisions/` and seven descriptions under
`docs/02.architecture/descriptions/` stay current. The router therefore
declares a responsibility that no admitted role carries.

The same router states that the supervisor's permission class is orchestration
rather than authoring and that governance maintenance requires an explicitly
scoped authoring owner. The registry contains no such owner. Tracked trees that
`.agents/knowledge/project-map.md` names are in the same position: the common
governance tree, the two provider adapters, the hosted `.github/` surface, the
policy rules, the non-validator part of `scripts/`, and the evaluation harness
under `evals/`. The supervisor, whose whole contract is routing, lists five of
its eleven peers in `handoff_to`.

The evaluation harness is a distinct case rather than one more uncovered
directory. `evals/README.md` states that role definitions are owned by
`.agents/` and that this folder owns evaluation cases, judgment criteria and
the fixed inputs that make cycles comparable. Measuring whether a role behaves
as its contract claims is a different responsibility from authoring that
contract, and the harness scores five criteria derived from the registry
without re-stating it. It receives its own role rather than being folded into
the governance-authoring boundary.

This specification closes those gaps by admitting five roles, repairing the
routing and reciprocity defects, and recording the external catalogue that
suggested part of the coverage shape as provenance in its existing Stage 90
owner. It changes no permission class, no provider block and no projection
rendering rule. Consumers are the agent registry, the two provider projection
roots, the responsibility router and the evaluation harness.

## Strategic Boundaries & Non-goals

Authorised scope is registry role membership, the neutral role bodies those
entries own, the provider projections the registry derives, the router item
index, and five evaluation cases for the admitted roles.

Protected surfaces keep their current contracts. The four permission classes
are schema-fixed at four members and are not extended. The provider blocks,
their capability model bindings and their permission scopes are unchanged. The
projection rendering contract enforced by `scripts/validate-agent-governance.py`
is unchanged, so every projection stays byte-derivable from the registry. Skill
packages under `.agents/skills/` keep their current membership and content.
GitOps desired state, cluster assets and document stage contracts are untouched.

Explicit non-goals:

- No new skill package. Admitted roles reference existing skills only.
- No output-schema enforcement across the existing twelve roles. The
  `Outputs` sections stay prose; converting them to an enforced hand-off schema
  is a separate change with its own validator work.
- No scenario-to-role sequence layer. Routing stays a supervisor decision
  rather than a declared table.
- No evaluation cases for the five existing roles that lack them. That gap is
  recorded here and left to a later package.
- No evaluation-methodology skill package. `agent-evaluator` references the
  one existing skill whose stated purpose covers harness and ownership
  auditing, and the absence of a dedicated evaluation procedure is recorded as
  a known gap rather than closed here.
- No upstream prompt text is copied, no upstream converter or installer is
  executed, and no upstream role is imported.

## Contracts

- **C1 Boundary coverage.** Every responsibility boundary the router declares
  is read by at least one admitted role body.
- **C2 Tree ownership.** Every tracked tree the project map names has either
  exactly one role authorised to author it or a recorded statement that it
  carries no authoring owner by intent.
- **C3 Routing completeness.** `supervisor.handoff_to` contains every other
  admitted role and never itself.
- **C4 Least privilege.** Each admitted role carries an existing permission
  class and a write boundary stated in its body. No admitted role widens a
  class, and a role whose subject puts a broader tool within reach narrows the
  class default through `native_scope_override` rather than through prose.
- **C5 Derivable projections.** Each admitted role produces one Claude
  Markdown projection and one Codex TOML projection whose metadata and
  canonical read list are derived from the registry entry alone.
- **C6 Provenance boundary.** External catalogue material is comparison
  evidence recorded by its Stage 90 owner. It authorises no admission by
  itself, and admission rests on a documented local gap.

## Core Design

### Coverage matrix and the five admitted roles

The gap is established by intersecting the project map's tracked trees with the
registry's authoring roles. `docs/` is covered by `doc-writer`, `wiki-curator`
and `docs-researcher`; `gitops/` and `infrastructure/` by `k8s-implementer`
with four read-only reviewers; `tests/` and the validator lane of `scripts/` by
`quality-engineer`; `secrets/` deliberately by no writer. The uncovered
remainder is the common governance tree, the two provider adapters, the hosted
surface, the policy rules, the non-validator tooling and the evaluation
harness. Five roles close it.

| Role | Permission class | Capability tier | Write boundary | Skills |
| --- | --- | --- | --- | --- |
| `architect` | scoped-authoring | top | `docs/02.architecture/**` | `requirements-to-design`, `docs-stage-routing` |
| `governance-steward` | scoped-authoring | top | `.agents/**`, `.claude/**`, `.codex/**` | `workspace-harness-audit`, `knowledge-map` |
| `ci-workflow-engineer` | scoped-authoring | worker | `.github/**` | `vulnerability-patterns`, `risk-report` |
| `repo-tooling-engineer` | scoped-authoring | worker | `scripts/**` entries absent from `scripts/validation/registry.json`, `policy/conftest/**` | `workspace-harness-audit`, `docs-stage-conformance` |
| `agent-evaluator` | scoped-authoring | worker | `evals/**`, `scripts/run-agent-evaluations.py`, its regression test under `tests/` | `workspace-harness-audit` |

### architect and the documentation boundary

The architecture boundary owns structural views and durable decisions. Giving
it a reviewer would leave the decisions themselves unowned, so `architect` is
an authoring role bounded to `docs/02.architecture/**`. It writes successor
decisions rather than editing accepted ones, retains superseded records in the
decision log, and traces structural change to complete Requirement Package
member identifiers and the owning Spec.

This creates one boundary that must be made explicit rather than left to
reading order. `doc-writer` currently claims any document at its canonical
owner. Its role body gains a second exclusion beside the existing sourcing and
navigation ones: a Stage 02 structural decision belongs to `architect`, and a
document whose canonical owner is Stage 02 reaches `doc-writer` only when
`architect` has settled the decision it records. The reciprocal statement in
`architect` routes prose-level document repair back to `doc-writer`, so neither
role can claim the other's half by silence.

A guardrail adapted from external catalogue material applies here: a decision
that does not name the alternatives considered and the property given up is not
recorded. The wording is this repository's; the idea is provenance.

### governance-steward and the harness write boundary

The router already states that governance maintenance needs an explicitly
scoped authoring owner and that the supervisor is not it. `governance-steward`
is that owner. Its boundary is the common governance tree and both provider
adapter trees, which are the surfaces that define how every other role
behaves. The evaluation harness is deliberately outside it, so the role that
authors a contract is not also the role that scores conformance to it.

Two guardrails follow from that reach. First, a change to the registry entry,
role body or projection of `governance-steward` itself is a stop condition: the
role does not widen its own authority, and such a change needs the operator.
Second, every registry or projection change records the result of
`scripts/validate-agent-governance.py` as repository-static evidence, kept
separate from provider discovery and runtime enforcement, which this role
cannot establish.

### ci-workflow-engineer

The hosted surface holds five workflows, a dependency policy, a labeler, a
branch ruleset, a CODEOWNERS file and a security validator dedicated to it. The
router says CI triggers, permissions, concurrency and non-lane jobs stay
governance-owned; naming that owner is what this role does.

Its guardrails are the ones the hosted surface actually fails on: widening a
workflow `permissions` block, introducing a `pull_request_target` trigger, or
referencing a third-party action by a mutable tag rather than an immutable
commit identifier are stop conditions that need operator approval. Local
execution of a workflow's steps stays local evidence and is never reported as a
hosted result.

### repo-tooling-engineer

`quality-engineer` owns validation design and the validators it is assigned.
The remainder of `scripts/` is not validation: the provider write guard is a
safety boundary, and the archive and document-lifecycle tooling implements the
document contract. `policy/conftest/` holds the policy rules that the lanes
evaluate rather than the lanes themselves. Those are this role's boundary.

The split between the two is decided by registry membership rather than by
reading a filename. `scripts/validation/registry.json` is the execution
registry that owns validator commands and profile membership; it registers
twenty executables today. A script it registers is validation-lane content and
stays in `quality-engineer`'s assigned scope, reaching `repo-tooling-engineer`
only by explicit delegation in the active Task. A script under `scripts/` that
the registry does not name is `repo-tooling-engineer`'s by default. Neither
role changes registry membership on its own, because admitting or removing a
lane member changes what QA evidence means.

One registered member is carved out by name. `scripts/run-agent-evaluations.py`
is the evaluation runner, and its behaviour is the other half of the contract
that `evals/` states; separating the criteria from the code that fires them
would leave a broken criterion with no owner able to repair it. That file and
its regression test belong to `agent-evaluator`. Its lane membership and
profile selection stay where every other lane member's do.

Its distinguishing guardrail is that a failure surfaced by repository tooling
carries a stable identifier and the path to a fix rather than a raw traceback,
and that no change to this tooling may relax the boundary that
`scripts/provider_write_guard.py` enforces. Relaxing that boundary is a stop
condition regardless of the reason offered.

### agent-evaluator

`evals/` scores recorded responses against five criteria — `groundedness`,
`authority`, `boundary`, `success-claim` and `handoff` — derived from the
registry so that a case never restates a role's permission class. Negative
cases carry an `expect` declaration naming exactly which criteria must fire,
which is what keeps the harness from holding only responses written to pass.
Designing that measurement, keeping the criteria honest about what they do not
prove, and reporting what a cycle established is a responsibility no admitted
role carries.

`agent-evaluator` owns it. Its assets are the cases and recorded responses
under `evals/`, and its contract extends to the runner and the runner's
regression test because a criterion and the code that fires it are one unit.

Two boundaries keep it from becoming a second governance owner. First, the
folder's own contract places role and skill definitions under `.agents/`, so
this role produces improvement findings naming the role or skill procedure at
fault and the observed failure, and hands the edit to `governance-steward`.
Writing the contract and scoring conformance to it stay in different hands.
Second, the harness executes no provider. A passing run where every response
is `synthetic` is evidence of harness wiring and criterion behaviour only, and
reporting it as agent quality is a stop condition; agent quality needs
`recorded` responses and the session evidence that produced them.

The guardrail adapted from external catalogue material is that a criterion
must state what it cannot judge. The existing criteria already do — string and
pattern matching covers enumerated failure shapes rather than meaning — and a
new criterion that omits that statement is not admitted.

### Routing and reciprocity repairs

`supervisor.handoff_to` is extended from five entries to the full peer roster
of sixteen. The supervisor's contract is to decide which responsibility owns a
piece of work, and a routing table that omits six owners cannot express six
correct decisions. Each admitted role receives handoff edges to `supervisor`
for unresolved ownership and to `security-auditor` where its subject can turn
into a security judgment. `agent-evaluator` and `governance-steward` carry the
edge in both directions: an evaluation finding reaches the harness owner's
counterpart for the contract edit, and a contract change reaches the evaluator
for a measurement that can detect its effect.

`doc-writer` gains the reciprocal navigation sentence that `wiki-curator`
already carries, so the pair state their shared edge from both sides in the way
`network-reviewer` and `security-auditor` already do.

### External provenance handling

`docs/90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md`
is the existing owner of the `msitarzewski/agency-agents` comparison. It pins
the tree at `ebe9c99acb5c96f9468de368d8bead775387d1a7`, records an
adopt/adapt/reject rule, and its most recent cycle set the trigger to refresh
when a role is proposed for adoption. Proposing five roles fires that trigger,
so the reference receives an additive re-observation cycle recording the
current upstream head, the unchanged licence field, the division-directory
shape of the catalogue and the decision actually taken.

The decision taken is adapt, not adopt. No upstream role, file, name or prose
enters this repository. What the catalogue contributed is the observation that
four of the five responsibilities this workspace lacked an owner for have
named counterparts in a large external roster, which strengthens the local gap
argument without supplying its evidence. The fifth, evaluation, has no
counterpart there and rests entirely on the local folder contract. Each admitted role's guardrails are written against
this repository's boundaries, and the local gap in the project map is what
justifies admission.

## Data Modeling & Storage Strategy

`.agents/roles/registry.json` remains the single machine truth for role
identity, permission class, capability tier, supported providers, skill
references, handoff edges and projection paths. Admitting a role appends one
object to `roles[]`; `skills[]`, `providers[]` and `permission_classes[]` are
unchanged. The registry stays validated against `registry.schema.json`, whose
role object forbids additional properties, so no new field is introduced.

The neutral role body at `.agents/roles/<id>.md` holds prose the registry does
not encode: the role's judgment, its trigger, inputs, outputs, guardrails,
required evidence and escalation. Provider projections hold no independent
content; they are derived views and are regenerated rather than authored.

Evaluation cases add one JSON case under `evals/cases/` and one synthetic
response under `evals/responses/` per admitted role, following the existing
naming of `<role>-<scenario>.json` and `<role>-<scenario>.synthetic.md`. Each
added case declares its `expect` value, and at least one of the five is a
negative case so the additions prove criterion behaviour rather than only
harness wiring.

Nothing in this change stores secret material, and no evidence file records a
credential value.

## Interfaces & Data Structures

A registry role object carries `id`, `responsibility`, `permission_class`,
`capability_tier_ref`, `supported_providers`, `skill_refs`, `handoff_to` and
`projections`, with `native_scope_override` and `native_reasoning_override`
optional. `id` is a lowercase hyphenated token, `responsibility` is a sentence
between sixteen and three hundred sixty characters, `capability_tier_ref`
points at the `#top` or `#worker` anchor of the model-selection policy, and
`supported_providers` is exactly `["claude", "codex"]`.

The Claude projection is YAML frontmatter with exactly `name`, `description`,
`model` and `tools`, followed by a body whose first line is the fixed reading
sentence, whose middle lines are backtick-quoted repository paths one per line,
and whose last two lines are an empty line and the fixed applying sentence. Any
other prose in that body fails validation as a hidden instruction. The Codex
projection is TOML with `description`, `developer_instructions`, `name`,
`model`, `model_reasoning_effort` and `sandbox_mode`, serialised in that
canonical key order.

The read list for both projections is the role body, the registry, the work
lifecycle, and each referenced skill package in the registry's order. `model`,
`tools`, `model_reasoning_effort` and `sandbox_mode` are resolved from the
provider block's capability and permission bindings, so an admitted role
specifies none of them directly.

## Edge Cases & Error Handling

An admitted role whose `skill_refs` is empty is schema-valid and yields a
three-entry read list. This change does not use that form; each admitted role
references two existing skills whose stated purpose covers its work.

Two roles claiming the same path is the failure this change is most exposed to.
The write boundaries are disjoint by construction, and the three places they
come closest — `scripts/` between `repo-tooling-engineer` and
`quality-engineer`, `docs/02.architecture/**` between `architect` and
`doc-writer`, and the evaluation runner between `agent-evaluator` and
`repo-tooling-engineer` — are resolved by an explicit sentence in both bodies
rather than by precedence.

A handoff edge naming an unknown role or naming the role itself fails
`AGENT-REGISTRY-HANDOFF`. A skill reference outside `skills[]` fails
`AGENT-REGISTRY-SKILL`. A projection whose metadata keys, identity, model or
sandbox differ from the derived values fails `AGENT-NATIVE-METADATA`, as does
a projection the registry names but that does not exist, and a read list that
differs in membership or count fails `AGENT-NATIVE-REFERENCE`. These are deterministic and are the intended
detection path for a hand-edited projection.

An identifier collision with an existing role or skill is rejected by the
uniqueness constraints before any file is written.

## Failure Modes & Fallback / Human Escalation

The dependent failure mode is authority drift: `governance-steward` can reach
the files that define every role, including its own. Its body makes a
self-directed authority change a stop condition, and the operator is the owner
of that decision. The repository-static detection is that any diff touching the
`governance-steward` registry entry or projections is visible in the same
validator run that the role is required to report.

The second failure mode is an admitted role that never receives work, which
adds maintenance cost and dilutes routing. Evaluation cases for the five
admitted roles are the local check on that, and `REQ-0003-NFR-0001` requires
roster admission to rest on local need, least privilege and evaluation
evidence rather than on catalogue size. The cases added here are `synthetic`,
so what they establish is wiring and criterion behaviour; reading them as
evidence that an admitted role performs well is the misreading `evals/`
already names, and `agent-evaluator` treats it as a stop condition.

The third is an over-wide hosted-surface change. `ci-workflow-engineer` stops
rather than proceeds on permission widening, `pull_request_target` and mutable
action references, and escalates to the operator.

Rollback is bounded and does not depend on the sequence in which the change
landed: removing a role means deleting its registry object, its role body and
its two projections, restoring `supervisor.handoff_to`, and rerunning the
governance validator. Removing `agent-evaluator` additionally returns the
evaluation runner carve-out to the default tooling rule and removes the cases
it added. No cluster state, document lifecycle record or archive entry is
involved, so no recovery procedure beyond a Git revert is required.

## Verification Commands

Repository-static commands, run from the repository root:

- `python3 scripts/json_schema_validation.py` — the registry validates against
  `registry.schema.json` with seventeen role objects.
- `python3 scripts/validate-agent-governance.py` — registry and projection
  consistency, handoff and skill edges, and projection derivation for both
  providers.
- `python3 scripts/validate-markdown-profiles.py` — the admitted role bodies
  and this specification satisfy their profiles.
- `python3 scripts/validate-links-and-owners.py` — router index entries and the
  reciprocal role references resolve.
- `python3 scripts/validate-knowledge-surface.py` — project-map and domain-index
  owner paths still exist.
- `python3 scripts/run-agent-evaluations.py --root .` — case integrity and the
  scored result of every recorded response, including the added cases.
- `python3 scripts/qa.py quick` and `python3 scripts/qa.py full` — the changed
  snapshot and the final tree.

These establish repository-static evidence only. Native discovery of the
admitted roles by either provider, permission enforcement at runtime, model
resolution and authenticated operation are separate lanes that this
specification does not claim and that no static result promotes.

## Success Criteria & Verification Plan

| Criterion | Statement | Evidence |
| --- | --- | --- |
| VAL-ARCC-001 | Every responsibility boundary the router declares is read by at least one role body. | Router section anchors matched against role bodies; link and owner validation |
| VAL-ARCC-002 | The registry defines permission, skill, tier, handoff and projection for all seventeen roles at one owner. | Schema validation and governance validation |
| VAL-ARCC-003 | Each admitted role carries an existing permission class and a stated write boundary that widens nothing. | Registry permission class review against the four fixed classes |
| VAL-ARCC-004 | Both projections of each admitted role are derived from the registry and carry no independent policy. | Governance validation of metadata and canonical read lists |
| VAL-ARCC-005 | Each admitted role is justified by a named uncovered tree and carries an evaluation case. | Project-map intersection review and evaluation case presence |
| VAL-ARCC-006 | The external catalogue is recorded as provenance by its Stage 90 owner and adopts no upstream role or prose. | Reference cycle entry and diff review for absent upstream text |
| VAL-ARCC-007 | Repository-static results are reported separately from provider-runtime and live evidence. | Verification record separating the lanes |
| VAL-ARCC-008 | `supervisor.handoff_to` contains every peer role and not itself. | Governance validation and registry review |
| VAL-ARCC-009 | The specification and the admitted role bodies match exactly one document profile each. | Markdown profile validation |
| VAL-ARCC-010 | The `doc-writer` and `architect` boundary is stated from both sides with no orphaned reference. | Link and owner validation with reciprocal reference review |
| VAL-ARCC-011 | Evaluation ownership is separated from contract authoring, and the added cases run under the existing gate with declared expectations. | Agent evaluation gate result and boundary review of both role bodies |

## Traceability

Requirement inputs come from
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
and the current structural view in
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
The responsibility boundaries this package completes are declared by
[the responsibility router](../../../.agents/roles/README.md), and the machine
membership it changes is owned by
[the agent registry](../../../.agents/roles/registry.json). Projection
rendering and native enforcement honesty stay owned by
[SPEC-0073](../0073-provider-native-enforcement-parity/spec.md) and
[SPEC-0074](../0074-provider-write-guard-ownership-and-enforcement-honesty/spec.md),
whose contracts this package follows without changing. External catalogue
provenance is owned by
[RES-0001-m0009](../../90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md).
[Implementation Plan](plan.md) owns ordered work, entry and exit gates, and
rollback. Its package Task owns execution results, per-lane evidence, and the
limits that remain unobserved.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-001 | Boundary-to-role coverage review |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-002 | Registry schema and governance validation |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-003 | Permission class and write boundary review |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-004 | Projection derivation validation |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-005 | Local gap justification and evaluation case review |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-006 | Reference provenance cycle and diff review |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-007 | Evidence lane separation review |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-008 | Registry routing validation |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-009 | Markdown profile validation |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-010 | Link, owner and reciprocal reference validation |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCC-011 | Agent evaluation gate and evaluation-boundary review |
