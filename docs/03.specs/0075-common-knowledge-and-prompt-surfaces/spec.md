---
title: "Common Knowledge and Prompt Surfaces Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0075"
---

# Common Knowledge and Prompt Surfaces Technical Specification (Spec)

## Overview

The common authority under `.agents/` owns policy, roles, callable skills and
two lifecycle workflows. It deliberately owns no knowledge index and no prompt
contract. The governance README records optional memory, rule, prompt and
script directories as unadopted; ADR-0035 decides that optional memory, rules,
prompts, evaluations and scripts folders are not created; and the
context-and-memory policy states that no governance memory directory remains
and that durable knowledge routes to the responsible policy, skill, operating
document or reference owner. A prior generated knowledge index was retired on
2026-08-31 as a duplicate navigation control plane.

The authorized request is to introduce a knowledge surface and a prompt
surface now. Creating directories while those statements stand would leave the
repository asserting two contradictory contracts, so this specification treats
the change as a decision revision whose first work item is the successor
decision, not as a file addition.

The revision is deliberately narrow. A successor decision carries every other
ADR-0035 clause forward unchanged and revises only the clause that forbids the
two adopted directories, following the pattern ADR-0035 itself used when it
superseded ADR-0034. Evaluation, rule and script directories stay unadopted
with recorded reasons: the evaluation harness under `evals/` already owns the
runner, the cases and a registered validation surface, so moving it would cost
runner, path-selection, profile and continuous-integration edits for no gain,
and the other two have no consumer.

The retired knowledge index is not recreated. What the earlier tool did was
generate a navigation plane that duplicated the routing the stage indexes
already owned. The adopted surface is hand-maintained pointer material bound by
a non-duplication rule and validated against the owners it points at.

Introducing the two surfaces touches adjacent material that is already
inaccurate, and correcting it in the same review unit is cheaper and safer than
leaving it. Seven responsibility documents under `.agents/roles/` carry no
registry entry and restate what the concrete role bodies already state. The
Stage 90 research pack carries wording that reads as forbidding the filename
prefix its own registry mandates, a duplicated navigation link, a retired stage
label, a dated four-provider observation stated without its successor, and an
upstream comparison pin the upstream has since advanced beyond. On this
workstation a global hook path override makes the repository's own commit-time
hooks inert, which the commit-message contract must account for rather than
assume away.

## Strategic Boundaries & Non-goals

Authorized scope covers a new architecture decision, `.agents/README.md`,
`.agents/governance/context-and-memory.md`, the new `.agents/knowledge/` and
`.agents/prompts/` directories, `.agents/roles/`, `docs/99.templates/`,
`docs/90.references/research/`, `scripts/`, `tests/`, `.claude/commands/`,
`.pre-commit-config.yaml` and the repository validation registry.
Every change is a reviewable local commit.

Protected surfaces stay unchanged. `gitops/`, `infrastructure/`, `traefik/`,
`policy/` and `examples/` are read as evidence of the platform this governance
serves; no behavioural change is made in them. No live Kubernetes, ArgoCD or
Vault operation occurs. No push, pull request, merge, release or remote
workflow dispatch occurs. No credential, token, kubeconfig, plaintext secret,
shell history or environment dump is read, printed or stored. Configuration
under the user's home directory, including the global hook path, is not
modified; the conflict it creates is documented with a user-run remediation
procedure instead.

Explicit non-goals. `.agents/evaluations/`, `.agents/rules/` and
`.agents/scripts/` are not created. The retired progress ledger is not revived
and no second progress ledger is introduced. No separate orchestrator, state
machine or loop runtime is built; the existing work-lifecycle stop conditions
remain the loop contract. No role is adopted from the upstream persona
catalog. No hosted continuous integration workflow for automated review is
created while no credential exists to run it, because an unrunnable workflow
file would present an inactive control as an active one. No editor integration is
added and nothing is placed under `.vscode/`, because this workspace does not
use VS Code and a recommendation or task file there would name a surface no one
runs. No entry point makes a
paid model call mandatory, and no commit-time hook gains a network dependency.
Guard ownership, patch parsing and permission-scope honesty are owned by
SPEC-0074 and are not reopened here.

## Contracts

**Single owner with a named consumer.** Each new surface has exactly one owner
and at least one named consumer that reads it at a stated point with stated
inputs. A surface without a consumer is not created, and a README alone is not
a consumer.

**No duplicated authority.** A knowledge document points at canonical owners
and never restates the policy, design or procedure it points at. It is
hand-maintained and contains no generated link map. A prompt contract states
inputs, outputs and refusal conditions; it does not restate role permissions or
approval boundaries, which remain owned by the registry and the approval
policy.

**Narrow decision revision.** The successor decision changes exactly the clause
that forbids the two adopted directories and carries every other clause forward
unchanged. After the change no file states the superseded position.

**Deterministic prompt inputs.** The prompt builder collects only the inputs a
contract declares, through commands the contract names, and performs no model
call and no network access. The commit-message contract accepts the staged
difference only, never rewrites a message the user has written, and produces a
draft judged by the existing conventional-commit rule.

**One profile per form.** Each new physical document form maps to exactly one
document profile with one template. Existing profiles are reused where they
already fit rather than duplicated.

**Consumer succession before removal.** A document is consolidated or removed
only after its distinct current meaning and every consumer reference are
carried to the successor in the same change, with no dangling link.

**Observation integrity.** A past observation keeps its original wording,
subject and date. Currency is added as a new dated observation beside it, never
by rewriting the old one into the present tense.

**One execution owner per rule.** Removing a duplicate execution never removes
the rule, weakens a contract, or converts a required-tool failure into a skip.

## Core Design

### Decision revision and policy alignment

A successor architecture decision supersedes ADR-0035. It restates that
decision's authority-location, skill-routing, gateway, preservation and
validation clauses unchanged, and revises only the unadopted-directory clause
to adopt a knowledge surface and a prompt surface. It records the continued
non-adoption of evaluation, rule and script directories with the reason for
each, and it distinguishes the adopted knowledge surface from the retired
generated index by the non-duplication rule and the validation that enforces
it. The governance README's structure table and configuration boundary, and
the context-and-memory policy's routing sentence, are amended in the same
change so no file states the superseded position.

### Knowledge surface

`.agents/knowledge/` holds three documents. The README states the surface
contract, including the non-duplication rule and what belongs elsewhere. The
project map names which top-level tree owns what and the entry document for
each. The domain index names, per domain, the canonical owner, the entry path
and the condition under which the entry stays valid. Domains follow the
platform this repository operates: Kubernetes and GitOps desired state,
networking and ingress, Vault and External Secrets, observability, and
documents and validation.

Consumers are the existing `knowledge-map` skill, whose stated purpose is
already navigation audit and which gains this surface as a named input; the
`wiki-curator` and `docs-researcher` roles that already reference that skill;
and the work-lifecycle intake step that selects owning documents for a task.

A validator checks that every owner and entry path a knowledge row names
exists, and that a knowledge document does not reproduce policy text from the
owners it points at. That second check is what keeps the surface a map rather
than a second authority.

### Prompt surface

`.agents/prompts/` holds a README and one contract per repeatable request:
work handoff, change review, commit-message drafting and documentation update.
A contract states its identifier, purpose, required inputs with the command
that produces each, the output shape, the validation applied to the output, and
the conditions under which it refuses to produce output. The handoff contract
reuses the handoff fields the quality policy already owns rather than
redefining them.

The consumer is a deterministic input builder under `scripts/`. Given a
contract identifier it collects exactly the declared inputs and writes the
assembled request to standard output. It makes no model call and no network
access, so no entry point makes a paid call mandatory and no commit-time hook
gains a network dependency. Editor tasks invoke the builder, and one Claude
command entry point per contract invokes it as well; the four identifiers do
not collide with any existing skill identifier. Codex reads the contract file
explicitly, as it already does for roles and skills, because the project skill
directory under `.codex/` is a retired surface and is not recreated for
symmetry.

The commit-message contract reads the staged difference only. Its output is a
draft the user accepts, edits or discards; the builder never writes a commit
message, never amends one, and never runs a Git command that changes state.

### Document profiles

Two profiles are added: one for a knowledge document and one for a prompt
contract, each with a required frontmatter set, a required section set and one
template. The two surface READMEs reuse the existing collection-index profile
by extending its path expression, because they are routers of the same kind
that profile already describes. No new schema or registry is introduced, and
the meta-profile that accompanies each physical template form is added for the
two new templates only.

### Responsibility document consolidation

The seven category documents become sections of the responsibility router that
already indexes them. Their distinct meaning is the domain boundary statement,
which the router absorbs; the concrete role bodies keep the guardrails, inputs,
outputs and handoffs they already own. Every consumer reference is carried to
a section anchor in the same change, including the Stage 90 index that maps
each category to requirement identifiers and repository path scopes. If link
validation shows a consumer that a section anchor cannot serve, that category
document is retained and the reason recorded rather than the link broken.

### Reference pack correction and upstream re-observation

The research pack's filename guidance is reworded so the registry-mandated
identity prefix is explicitly outside the prohibition on ordering prefixes. The
duplicated navigation link is removed. The retired stage label is replaced by
the current authority name where the sentence describes the present, and left
in place with its date where it describes a past observation. The dated
four-provider observation keeps its wording and date and gains a current dated
observation of the two-provider registry beside it.

The upstream persona catalog is re-observed and the new head identity, date and
licence are recorded as a new observation; the retained comparison pin keeps
its own date and wording. The conclusion is recorded explicitly: the catalog is
a division-organized set of persona prompt files, the existing twelve-role
roster has no concrete gap it fills for this workspace, and no role is adopted.
The catalog remains provenance for ideas, not admission or policy authority.

### Commit tooling

Command entry points are added for the four prompt contracts under
`.claude/commands/`, each invoking the builder with its identifier. No editor
surface is added: this workspace does not use VS Code, so `.vscode/` is removed
and its two validation routes are retired with it. The builder stays runnable
from the shell, which is the path the entry points wrap.

The global hook path override that makes the repository's commit-time hooks
inert on this workstation is documented with its consequence — the
conventional-commit check and the commit hook suite do not run at commit time
here — and with a repository-local remediation the user runs themselves. The
global configuration is not modified. Because that override is in effect, the
commit hook suite's execution inside the full validation profile is retained
rather than treated as duplication.

### Duplicate execution

The container-manifest linter runs both as a commit hook and inside a
validation script. The script becomes its single execution owner, because it
also serves the narrower lanes the hook does not reach, and the duplicate hook
entry is removed only after the script's file scope is proven to cover the
hook's. The action-pinning check exists in both a third-party linter and a
repository validator, but the validator contains a guard preventing the
linter's rule from being disabled, so the pair is a deliberate interlock and
both are retained with that reason recorded.

## Data Modeling & Storage Strategy

No database, index, cache or retrieval service is introduced. All new state is
tracked Markdown, tracked JSON registry entries and tracked Python under
version control.

The knowledge surface stores pointers, not content: an owner path, an entry
path and a validity condition per row. It stores no summary that would drift
from its source, and it is written by hand so no generation step can
reintroduce the retired navigation plane. The prompt surface stores contracts,
not results; a produced draft is transient output on standard output and is
never written into the repository by the builder.

Document profiles and templates extend the existing Stage 99 registry. The
responsibility router absorbs the category documents' text; the removed files
remain recoverable from Git history at their original paths, and the successor
relation is recorded through the lifecycle contract rather than by rewriting
history.

Research statements keep their observation dates. Currency is additive: a new
dated row beside the old one, never an edit that converts a past observation
into a present-tense claim. The two existing stashes target removed authority
roots, cannot apply cleanly, and one of them would reintroduce the retired
progress ledger; they are left untouched and their disposition is recorded, not
executed.

## Interfaces & Data Structures

**Knowledge row.** A domain or area name, the canonical owner path, the entry
path a reader opens first, and the condition under which the row stays valid.

**Prompt contract structure.** Identifier, purpose, input list with the command
that produces each input, output shape, validation rule, and refusal
conditions.

**Builder interface.** A contract identifier argument; the assembled request on
standard output; a non-zero status with a diagnostic when a declared input
cannot be produced within the allowed command set. No subcommand of the builder
writes to the repository or to Git state.

**Profile additions.** One knowledge-document profile and one prompt-contract
profile, each with a path expression, a required frontmatter set with fixed
type, a required section list, a template source and a status domain. The
collection-index profile's path expression is extended by the two surface
README paths.

**Editor task interface.** One task per prompt contract, each invoking the
builder with its identifier from the workspace root, alongside the existing
validation tasks.

## Edge Cases & Error Handling

A knowledge row whose owner or entry path does not exist fails validation. A
knowledge document that reproduces a span of policy text from an owner it
points at fails the non-duplication check. A knowledge document added without
its README index entry fails the folder-level navigation rule the repository
already enforces.

A prompt contract declaring an input command outside the allowed set fails
validation. A builder invocation for an unknown identifier fails with a
diagnostic rather than an empty draft. A commit-message invocation with an
empty staged difference produces a diagnostic and no draft, rather than a draft
describing nothing. A repository with no staged changes never causes the
builder to stage anything.

A category document consolidation that would leave a consumer without a
resolvable anchor stops and retains that document. A research correction that
would change the subject or date of a past observation is rejected in review; a
correction may only reword present-tense claims or add a new dated observation.

Removing the duplicate linter entry when the script's scope does not cover the
hook's scope is rejected, because that would drop coverage rather than move
ownership.

## Failure Modes & Fallback / Human Escalation

If the successor decision is not accepted, no directory is created; the surface
work stops at the decision and the remaining hygiene items may still proceed
independently, because none of them depends on the new surfaces.

If a new surface acquires no real consumer during implementation, that surface
is not delivered. A README describing an unused directory is the failure this
package exists to avoid, and delivering one would repeat the retired index.

If the non-duplication check proves unworkable in practice, the knowledge
surface is reduced to the project map and the domain index without further
documents, rather than relaxed into a second policy store.

If a baseline gate fails after a change, the failure is separated from the
recorded clean baseline of the current tree and treated as a regression of the
change. A repair is bounded: the same check failing twice with no new
information, two consecutive changes with no observable progress, a repair
requiring wider scope, or an unmet authority stops the work and reports it. No
contract, gate or test is weakened to end the loop.

Rollback is per logical commit through revert; each commit is scoped to one
owner boundary so reverting one does not strand another. Escalation goes to the
user for any push, pull request, merge, release, credentialed run, global
configuration change, or any decision that would widen approved scope or weaken
a control.

## Verification Commands

`python3 scripts/validate-agent-governance.py --root .` judges registry
integrity, role projections and the absence of retired surfaces after the
responsibility documents are consolidated.

`python3 scripts/validate-document-contract-registry.py --root . --mode strict`
and `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
judge that each new form resolves to exactly one profile with its template.

`python3 scripts/validate-links-and-owners.py --root . --mode strict` judges
consumer succession and the research pack corrections.

`python3 -m unittest discover -s tests -t .` judges the prompt builder and the
knowledge validation regressions.

`python3 scripts/qa.py staged` judges the exact index during work, and
`python3 scripts/qa.py full` judges the final tree.

The recorded baseline of the current tree is twenty-one gates passing under
`python3 scripts/qa.py full`. Any gate that stops passing after a change is a
regression of that change. Invoking a document validator directly rather than
through the quality entry point compares against the Git index and is not a
substitute for the lane the entry point selects.

These commands produce repository-static evidence only. They do not establish
that either client discovered a surface or loaded a contract. Those require a
fresh session and are reported separately.

## Success Criteria & Verification Plan

VAL-CKP-001. Each new surface names its owner and at least one consumer that
reads it at a stated point with stated inputs, and no delivered surface lacks
one. Proven by consumer review and the added validation.

VAL-CKP-002. The successor decision revises only the unadopted-directory clause
and carries every other clause forward unchanged, and after the change no file
states the superseded position. Proven by decision review and a repository
search for the superseded wording.

VAL-CKP-003. Each new physical document form maps to exactly one profile with
one template, and the two surface READMEs resolve through the existing
collection-index profile. Proven by the document contract registry and markdown
profile validators.

VAL-CKP-004. No knowledge document restates policy, design or procedure text
from an owner it points at, none is generated, and every owner and entry path
it names exists. Proven by the added validation and by review against the
canonical owners.

VAL-CKP-005. The prompt builder collects only declared inputs, makes no model
call and no network access, writes nothing to the repository or Git state, and
the commit-message contract accepts the staged difference only. Proven by unit
tests over the builder.

VAL-CKP-006. Consolidated responsibility documents carry their distinct meaning
and every consumer reference to the successor in the same change, with no
dangling link, and any document that cannot be served by an anchor is retained
with the reason recorded. Proven by link and owner validation and reference
pack review.

VAL-CKP-007. Past observations keep their wording, subject and date; currency
appears as an added dated observation; and the corrected filename guidance no
longer contradicts the prefix its own registry mandates. Proven by document
review and link validation.

VAL-CKP-008. The upstream catalog remains provenance only, the current head
identity and licence are recorded with their observation date, and the registry
role count is unchanged. Proven by registry role count and document review.

VAL-CKP-009. Each duplicated rule ends with one execution owner, no rule is
lost, no required-tool failure becomes a skip, and the retained interlock and
the retained profile-level hook suite each record why they are retained. Proven
by comparing full profile results before and after.

VAL-CKP-010. Owner transition, mutual links, stale claim removal and orphan
consumer cleanup are delivered in the same review unit as the change that
causes them. Proven by diff scope review and link validation.

VAL-CKP-011. The commit-tooling limitation, namely the global hook path
override, is recorded as evidence with a named remediation the user runs, and
is not reported as a working control. Proven by review of the package Task
evidence.

## Traceability

Requirement inputs come from
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
and the current structural view in
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
The decision this package revises is
[ADR-0035](../../02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md),
whose unadopted-directory clause the first work item replaces through a
successor decision while carrying every other clause forward. Provider guard
ownership, patch parsing and permission-scope honesty are owned by
[SPEC-0074](../0074-provider-write-guard-ownership-and-enforcement-honesty/spec.md),
which this package follows in execution order without depending on its
contract. [Implementation Plan](plan.md) owns ordered work, entry and exit
gates, and rollback. Its package Task owns execution results, per-lane
evidence, and the limits that remain unobserved.

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method                                  |
| ------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-001    | Surface owner and consumer review                    |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-002    | Decision review and superseded-wording search        |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-003    | Document contract registry and profile validation    |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-004    | Non-duplication validation against canonical owners  |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-005    | Prompt builder unit tests                            |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-006    | Link and owner validation with consumer succession   |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-007    | Reference pack review and link validation            |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-008    | Registry role count and upstream provenance review   |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-009    | Full profile gate comparison before and after        |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-010    | Diff scope review and link validation                |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CKP-011    | Package Task evidence review                         |
