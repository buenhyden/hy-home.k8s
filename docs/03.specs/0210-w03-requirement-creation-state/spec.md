---
title: "W03 Requirement Creation State"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0210"
---

# W03 Requirement Creation State Technical Specification (Spec)

## Overview

### Intent

This approved change contract repairs residue W03-H43 of the W03 stage of the external v14.7 execution package. The `requirement` lifecycle domain of the Stage 99 registry has the states `draft`, `in-review` and `approved` and the transitions `in-review` to `draft`, `draft` to `in-review` and `in-review` to `approved`. Every state has an inbound transition, so `creation_states(domain)` in `scripts/document_lifecycle.py`, which takes the declared `initial_states` or else the states without an inbound edge, yields none. The lifecycle creation rule `LIFECYCLE-CREATE` therefore refuses every new Requirement, whatever its status, and the document generator of SPEC-0192 refuses `sdlc/requirement` with `GENERATOR-STATUS` (W03-D48, question 3: the generator refuses the profile until the registry admits a creation state, and a repair handoff carries the repair). The handoff is W03-H43, a live `Residue Handoff` row of the SPEC-0161 Task with an entry in `docs/03.specs/work-residue-ledger.json`, recorded by EVD-058. The task file asks for a real generate, parse and validate round trip for every role and for the lifecycle of each role to be one contract that the producers and consumers share (REQ:222, REQ:293, REQ:663); a role that no tool may create meets neither. On 2026-11-14 the user decided a small W03 package after SPEC-0206 that adds a creation state to the `requirement` domain with failing-first tests (W03-D71, answer "Small W03 package (Recommended)"; its three design choices are W03-D73, see Decisions). This package declares `initial_states: ["draft"]` for the `requirement` domain, lets the registry check accept that declaration, makes `sdlc/requirement` generable, and raises the Registry Schema Version at the level ADR-0061 sets. The [Task](tasks/tsk-0001-w03-requirement-creation-state.md) records execution and the [Plan](plan.md) orders the work.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of lifecycle domains; the creation rule has one derivation (`creation_states`), and this package gives it one more declared input rather than a second rule. The flow of the lifecycle creation rule and of the generator is unchanged.

## Scope

### In Scope

- In scope (writer W03 for the registry, with W05 for validator and test code; each W05 file is edited under the same-change rule of `docs/99.templates/AGENTS.md` rule 1 and is recorded as a delegation by the closing records package, SPEC-0209, or by this Task if that package has merged): the `requirement` entry of `lifecycle_domains` in `docs/99.templates/registry.json` (the one key `initial_states`) and the `schema_version` value; the lifecycle domain rule of the strict registry check in `scripts/document_contracts.py` (the initial-state clause and the modern-state clause named in the Contracts section); the constants that hold the registry MAJOR number, `REGISTRY_MAJOR` and `READABLE_REGISTRY_MAJORS` in `scripts/document_authority.py` and `DOC_REGISTRY_MAJOR` in `scripts/provider_write_guard.py`, and the version `const` or pattern of `docs/99.templates/contracts/document-profile.schema.json`, exactly as the package that last raised the MAJOR number touched them; `tests/test_document_artifact_identity.py`, `tests/test_document_generator.py`, `tests/test_task_acceptance_contract.py` (the `REGISTRY_LIFECYCLE_DOMAIN` and `LIFECYCLE-CREATE` cases) and `tests/test_document_lifecycle_cumulative_history.py` (the `LIFECYCLE-CREATE` cases), re-read at the implementation base; any current policy sentence that states the gap, found by the survey in the Task (none at `eb017bfe`); each edited document's frontmatter `version` and `updated`; in the SPEC-0161 Task this package's own evidence row(s), the closure of W03-H43 and, through the ledger cycle at acceptance, the matching entry of `docs/03.specs/work-residue-ledger.json`, and the completed-spec lineage row of this package in the Archived Lineage table of REQ-0003 at closure, as sibling closures do (the decision rows W03-D71 to W03-D73 are already recorded by the SPEC-0194 implementation commit and are not appended here); this package, the Stage 03 README entry and reviewed `.secrets.baseline` entries.

### Non-goals

- Not in this package: any change of the `states`, `transitions` or `profile_ids` of any domain, so the `in-review` to `draft` rework edge stays; the other domains, none of which lacks a creation state (the survey in the Task confirms it); any template, profile, form, relationship or the frontmatter schema; any existing Requirement document; the lifecycle meaning of a Requirement state, which W04 owns; Q-07 numbering and number allocation (W03-D30); the work residue ledger design (SPEC-0191); a status input for the generator (W03-D48 keeps none); hosted CI.
- No push, PR or merge without the user's approval. Open question: none. This Spec stays `draft` until its approval receipt exists.

Decisions (W03-D73):

On 2026-11-14 the user decided the three choices this package raised, each the recommended option; the decision row W03-D73 is recorded in the SPEC-0161 Task by the SPEC-0194 implementation commit, before this package lands, with W03-D70 to W03-D72 (W03-D71 is the intake answer "Small W03 package (Recommended)"). Open question: none.

- **Repair choice.** "Declare initial_states (Recommended)": the `requirement` domain declares `initial_states: ["draft"]` and keeps the `in-review` to `draft` rework edge. The alternative, deleting that edge, is rejected: it removes a transition the registry grants, refuses a Requirement returned to `draft` that was valid before, and is also a MAJOR change.
- **Level.** "MAJOR, after 0206 (Recommended)": the Registry Schema Version is raised at the MAJOR level, for the reason in the Contracts section.
- **Order.** The same answer: this package lands after SPEC-0206 and before SPEC-0209, so that SPEC-0209 records the W05 files this package edits; if SPEC-0209 has merged first, this Task records the delegation itself.

## Behavior Contract

### Normal Behavior

Contracts:

- **Choice.** The `requirement` domain declares `"initial_states": ["draft"]`, the key that the `spec-plan` and `task` domains already carry. `creation_states` already prefers a declared list, so `scripts/document_lifecycle.py` needs no change, and `LIFECYCLE-CREATE` and the generator both read the one function (SPEC-0192). The alternative, deleting the `in-review` to `draft` edge so that `draft` has no inbound edge, is rejected: it removes a rework path that the registry grants, refuses a Requirement returned to `draft` that was valid before, and is also a MAJOR change; it is the decision recorded above.
- **Registry check.** The strict registry check, `REGISTRY_LIFECYCLE_DOMAIN` in `scripts/document_contracts.py`, refuses an initial state that has an inbound edge, except the local Task first-recording set. It is amended in two places and nowhere else. First, the exemption extends to the `requirement` family when its `initial_states` equal `["draft"]`: that state is `mutable` and the edge into it is the rework edge, so a document is created in `draft` and may return to it. Second, the modern-state clause (`expected_initial_states` and the `family in {"spec-plan", "task"}` test at `scripts/document_contracts.py` lines 2012 to 2017), which today requires `["draft"]` of `spec-plan` and the Task set of `task` (`["draft"]` when the Task first-recording extension is absent), gains the `requirement` family with `["draft"]`, so a registry that drops the declaration, or declares `in-review` or `approved`, is refused. No other family is exempted, and no general rule such as "a mutable initial state may have an inbound edge" is added, because it would admit a mistaken declaration on a family whose derived creation state is already correct.
- **Lifecycle reader.** `scripts/document_lifecycle.py` is not changed. `creation_states` of the `requirement` domain returns `("draft",)`, a new Requirement at `draft` is admitted by `LIFECYCLE-CREATE`, and one at `in-review` or `approved` is still refused with the expected set `('draft',)`. The transitions are not changed, so a Requirement may still move `draft` to `in-review`, `in-review` to `draft` and `in-review` to `approved`, and no transition is added.
- **Generator.** `scripts/document-generator.py` is not changed: the status rule reads `creation_states`, and the requirement template carries `status: "draft"`. `sdlc/requirement` becomes generable by the registry rule and by the status rule. The round-trip test gains one sample target path for it, and the completeness assertion no longer adds `sdlc/requirement` to the sample set by hand: the sample set must equal the generable set computed from the registry. The fresh document draws the authoring findings of its form (the Requirement package member and identity rules, the starter H1, empty sections and sample rows) and no `FM-` rule and no identity rule, the same contract as every other generable profile (SPEC-0192). The template's sample member IDs (`REQ-0001-FR-0001`) do not start with the package prefix that the sample path `docs/01.requirements/9001-sample.md` derives (`REQ-9001-`), so the fresh document very probably draws `REQUIREMENT-PACKAGE-MEMBER-ID` (`scripts/validate-markdown-profiles.py` lines 795 to 808), which `AUTHORING_RULES` of `tests/test_document_generator.py` (lines 143 to 151) does not list; `IDENTITY_RULES` already holds `REQUIREMENT-PACKAGE-IDENTITY`. The smaller correct repair is to add `REQUIREMENT-PACKAGE-MEMBER-ID` to `AUTHORING_RULES` as an authoring finding, because the member IDs are sample rows that the author replaces, and because a sample path numbered `0001` would collide with the existing Requirement and leave the `9001` fixture convention. The failing-first run records the actual rule set of the fresh Requirement; any rule outside the recorded authoring and identity sets stops the work.
- **Registry Schema Version (ADR-0061, `document-authoring.md`; REQ:877 and REQ:878).** Level: MAJOR. The new entry is a valid registry for the code of this package only. A reader of the earlier edition rejects it: its strict registry check refuses an initial state that has an inbound edge outside the Task extension, so `load_registry` raises `REGISTRY_LIFECYCLE_DOMAIN`, and the readers promise to load every MINOR and PATCH number of the MAJOR number they implement. The policy text says a MAJOR change is one that breaks a registry or consumer that was valid before, and the task file says that fixing every consumer in the same pull request does not remove the break (REQ:877), and that an added key a strict parser rejects is not automatically MINOR (REQ:878); the repair also tightens an obligation, since a registry must now declare the Requirement creation state. A MINOR level would be correct only if the earlier validator accepted the value, and it does not. No level below MAJOR holds, and NO_CHANGE does not apply because the registry bytes change. The new number is the MAJOR number that follows the value the last package left, with MINOR and PATCH at zero (the registry is at `13.0.0` or later when this lands, so the number is read at the base and is not fixed here). One edit raises the highest affected level once: the `initial_states` entry and the value are one change. The Task records the base value, the level and this reason, and the readers of the MAJOR number accept the new number and keep listing the earlier one for the history reader, as the preceding MAJOR packages (SPEC-0205, SPEC-0207) set it.
- **Policy text.** No current policy sentence states the gap at `eb017bfe`: the generator sentences of `document-authoring.md`, `docs/99.templates/README.md` and `scripts/README.md` say that a new document starts from the generator and name no exception for a Requirement, and the refusal is recorded only in the frozen SPEC-0192 package and in the tests. `.agents/governance/document-lifecycle.md` (W04) holds no creation-state sentence for a Requirement either (its creation lines concern Spec, Plan and Task authoring only), and it is left untouched. The survey greps the three files, that policy and the stage 01 README again at the implementation base; a sentence that states the gap is corrected, and a text that names the registry version takes the new value.
- **Residue records.** At acceptance the closure of W03-H43 follows the ledger cycle as EVD-059 and EVD-062 did: one evidence row in the SPEC-0161 Task cites the user's acceptance of both criteria, the live `Residue Handoff` row of W03-H43 becomes terminal with that row as its Closure, its entry in `docs/03.specs/work-residue-ledger.json` is made terminal with that closure and then deleted, `python3 scripts/validate-work-residue-ledger.py --root .` passes before and after each step, and the legacy cells stay as recorded. This package appends no decision row: W03-D73 is already recorded by the SPEC-0194 implementation commit. The package commit appends only its own evidence row(s), and the closure adds the REQ-0003 completed-spec lineage row.

Data modeling and storage strategy:

One key is added to one registry entry and one number changes in the registry. The JSON schema already allows `initial_states` on any domain (a nonempty array of unique strings), so no schema shape changes apart from the version value the schema holds. Nothing else is stored.

Interfaces and data structures:

- Registry: `lifecycle_domains[family="requirement"].initial_states = ["draft"]`; top-level `schema_version` raised at the MAJOR level.
- `scripts/document_contracts.py`: the initial-state clause and the modern-state clause of the lifecycle domain rule, as above. `creation_states` and `LifecycleDomain.initial_states` are reused unchanged.
- Tests. Each new behavior fails first on the implementation base and then passes; the regression cases below already pass and are recorded as such, not as failing-first. A new Requirement refused at every status and a generator that refuses the profile are the gap, so those fail first.
  - `CreationStatesTest` in `tests/test_document_artifact_identity.py` (the case at line 294): `creation_states` of `sdlc/requirement` equals `("draft",)` (fails first); the case "a domain whose every state has an inbound edge yields none" moves to a synthetic domain value, because no registry domain keeps that shape any longer.
  - `REGISTRY_LIFECYCLE_DOMAIN` cases in `tests/test_task_acceptance_contract.py` (the cases at lines 535 to 562, beside the existing spec-plan and Task cases): a `requirement` entry with `["draft"]` is accepted (fails first, because the clause refuses it today); a `requirement` entry without `initial_states`, or with `["in-review"]`, `["approved"]` or `["draft", "in-review"]`, is refused (the missing and wrong-set cases fail first; the repository registry raising no `REGISTRY_LIFECYCLE_DOMAIN` is a regression case once the entry exists); `["draft"]` on another family is still refused, built from a synthetic added inbound edge to `draft` on that family (regression case, already passing).
  - `LIFECYCLE-CREATE` cases in `tests/test_document_lifecycle_cumulative_history.py` (the cases near lines 448 and 508) and `tests/test_task_acceptance_contract.py` (the cases near line 289): a new Requirement at `draft` draws no `LIFECYCLE-CREATE` (fails first); at `in-review` and at `approved` it draws one with the expected set `('draft',)` (regression cases, already passing); the three transitions are unchanged and an `in-review` to `draft` edge is still accepted (regression case, already passing).
  - Generator cases in `tests/test_document_generator.py`: `sdlc/requirement` joins `SAMPLES` with a target path and identity of the form the profile derives (fails first as the round trip is refused today); `AUTHORING_RULES` gains `REQUIREMENT-PACKAGE-MEMBER-ID` as the failing-first run shows; the completeness assertion at line 305 drops the hand-added `sdlc/requirement`, so the sample set equals the generable set; the round trip equals the template with only the shared markers replaced. The test `test_requirement_has_no_creation_state_and_is_refused` (line 527) is removed, because it asserts the gap this package closes; the refusal of a template status outside the creation set stays with the existing `test_template_status_outside_the_creation_states_is_refused` for `sdlc/spec`, which is not parametrized, and one new case edits the Requirement template status to `approved` and expects `GENERATOR-STATUS` (fails first only through its absent sample path, then passes).
  - Version cases are not edited: the tests of SPEC-0207 read the MAJOR constants, so the raise needs no test edit; the Task shows them passing.

### Failure and Edge Cases

Edge cases and error handling:

- A Requirement document created at `draft` and returned from `in-review` to `draft` is a legal edge both before and after.
- Every Requirement in the tree is `approved`; none is created or changed, and no strict validator may gain a diagnostic.
- The cumulative-history replay reads earlier registries by their own MAJOR number; a Requirement created in history under an earlier registry is not judged by this declaration.
- If `SPEC-0195` or a later form package has moved the Requirement template or its path, the sample target path is derived from the registry at the base, and the template status must still be `draft`.
- A document-authoring or README sentence that names the registry version takes the new number in the same change.

Failure modes and fallback or human escalation:

If the repair needs a change to `states`, `transitions`, another family, a template, a profile or the lifecycle reader, or if any existing document gains a diagnostic, the author stops and asks the user. If an earlier-MAJOR reader that this package did not list still accepts the new registry, or the history reader replays a registry of a MAJOR number that the new constants do not list, the author fixes the constant owner and never relaxes the strict check. Rollback is the revert of the implementation commit; before that, the delete of the package commit.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-REQCREATE-001 | The `requirement` domain declares `["draft"]`; `creation_states` returns it; the registry check accepts that declaration and refuses a missing or different one; `LIFECYCLE-CREATE` admits a new Requirement at `draft` and refuses `in-review` and `approved`; the three transitions are unchanged; each new test failed first and passes; no existing document gains a diagnostic. |
| VAL-REQCREATE-002 | `sdlc/requirement` is generated by the command, its round trip passes with no `FM-` rule and no `IDENTITY_RULES` finding, every remaining rule belonging to the recorded authoring set (which gains `REQUIREMENT-PACKAGE-MEMBER-ID` if the failing-first run shows it), and the sample set equals the generable set; the Registry Schema Version is raised at the MAJOR level with its reason recorded and the MAJOR readers accept it; any policy sentence that stated the gap is corrected; the W03-D71 row is recorded and the W03-H43 closure follows the ledger cycle at acceptance; exact-index QA and the commit hooks pass. |

### Evidence Requirements

- Record the four strict document validators before and after the change; diagnostics must be equal.
- A failing-first run of each new test on a scratch copy of the implementation base, then the passing run.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle` and `--suite validation-routing`; `python3 scripts/validate-affected-surfaces.py --root .`.
- One run of the generator command for a Requirement into a temporary copy of the tree, with the printed line recorded in the Task; nothing is generated into the repository.
- `python3 scripts/validate-work-residue-ledger.py --root .` before and after the ledger cycle.
- `ruff check scripts tests`, `ruff format --check scripts tests`; markdownlint over the edited Markdown; `python3 scripts/validation/repository/quality.py --root .`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## References

### Normative and Evidence

No separate reference list is kept; the requirement, architecture and decision owners this Spec relies on are linked in [Lifecycle Traceability](#lifecycle-traceability) below.

### Historical and Navigation

No separate reference list is kept; this Spec holds no historical or navigation links beyond the [Plan](plan.md) and the Task that its Overview names.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REQCREATE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Round-trip test for the Requirement profile; sample set equals the generable set. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REQCREATE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Registry check cases, creation-state and `LIFECYCLE-CREATE` cases with their refusal cases; strict validators over the tree. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REQCREATE-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Registry check cases, creation-state and `LIFECYCLE-CREATE` cases with their refusal cases; strict validators over the tree. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-REQCREATE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Failing-first tests; Registry Schema Version level and reason; exact-index QA. |
