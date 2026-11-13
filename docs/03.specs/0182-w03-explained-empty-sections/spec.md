---
title: "W03 Explained Empty Sections"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0182"
---

# W03 Explained Empty Sections Technical Specification (Spec)

## Overview

This approved change contract closes handoff W03-H18 of the W03 stage of the external v14.7 execution package. The common section contract gives every required section the empty policy `explain_none_or_not_applicable`, and the W03 task (line 333) says an empty section states, as the lifecycle allows, the reason nothing is done or present and the follow-up condition, never a bare `N/A`, comment or placeholder; semantic review judges whether an explanation is sufficient (line 331). The form-only migrations wrote bare statements instead: 151 lines in about 60 files, every one the only body of a required, always-present H3 (the skill, AGENTS, policy, Stage README and Service README forms have no conditional H3 to omit). They are 57 in the 17 native skills, 4 in two common workflows (`work-lifecycle.md`, which both gateways load every session, and `delegated-development.md`), 43 in the 16 folder `AGENTS.md` files, 8 English and 9 `Exclusions` lines in governance and operations policies, and 30 Korean README lines (three of them in `.github/repository-surface.md`, a README profile) (`Runbook Links`, `Observability and Recovery`, `Security Boundary`, `Classification`, `Transition and Exit`, `Local Workflow`). On 2026-11-13 the user chose to keep pointer lines that name where content lives, correcting only wrong ones (W03-D31). The [Task](tasks/tsk-0001-w03-explained-empty-sections.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for the check): the files that hold one of the 151 bare lines; the seven AGENTS pointer lines that cite a nonexistent "Purpose text" (`docs/AGENTS.md` lines 38 and 96, `docs/01.requirements/AGENTS.md`, `docs/05.operations/AGENTS.md`, `examples/AGENTS.md` twice and `tests/AGENTS.md` line 62), which become "the opening text of Allowed Surface"; `scripts/validate-markdown-profiles.py` (the `BODY-SECTION-BARE` rule) and its tests, including the `agents_body()` fixtures in `tests/test_common_form_tree.py` that use bare lines; one sentence of `.agents/governance/document-authoring.md`; where a file has frontmatter, its `version` and `updated` (skills: `metadata.version` and `metadata.updated`) and no other key; an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: form requiredness; any section with content; other frontmatter keys; skill bundle files; the root `AGENTS.md` heading count; the gateway line limit; accepted ADR bodies; completed evidence.
- No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Reason table.** Each bare line is replaced by the sentence for its section below, with the document's own noun where it reads "this skill", "this folder" or "this policy". The language follows the file: English in `.agents/`, native skills and folder `AGENTS.md`; Korean in READMEs and Korean policies. A line for which the sentence is untrue for that document, the singleton sections (`Allowed Surface`, `Required Checks`, `Local Obligations`, README `Local Workflow`), the root `AGENTS.md` (which has no parent `AGENTS.md`), skills that already state their own stop conditions, and the Korean `Exclusions` line of policy 0007 get a document-specific sentence of the same shape (reason, then follow-up condition), listed in the Task for review. Semantic review judges sufficiency.

| Form | Section | Reason and follow-up condition |
| --- | --- | --- |
| Skill | Inputs | This skill takes no input beyond the user's request and the files its Steps name; if a step comes to need another input, list it here. |
| Skill, workflow | Outputs | This procedure defines no output format of its own beyond the results its Steps describe; if it needs one, define it here. |
| Skill | Failure Handling | This skill has no failure branch of its own; a failing step is reported and the work lifecycle's bounded-attempt stop rule applies. If a step needs its own recovery, add it here. |
| Skill | Checks | This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here. |
| Skill | Completion and Handoff | This skill completes and hands off through the work lifecycle's Completion steps and adds no field beyond what its Steps state; if it needs one, list it here. |
| Workflow | When Not to Use | This procedure names no repository work it must not be used for; if such a case is found, state it here. |
| AGENTS | Non-goals | This folder adds no non-goal beyond the parent `AGENTS.md` and the governance policies; if work here must be excluded, state it here. |
| AGENTS | Handoff | This folder hands off through the work lifecycle's Completion steps with no extra field; if it needs one, state it here. |
| AGENTS | Evidence and Limits | This folder adds no evidence rule beyond the quality policy's handoff contract; if a check here has a limit to report, state it here. |
| AGENTS | Protected Actions | This folder adds no protected action beyond the approval and safety policy; if work here can start one, name it here. |
| AGENTS | Stop and Escalate | This folder adds no stop condition beyond the work lifecycle's stop rule and the approval and safety policy; if work here needs its own, state it here. |
| Policy | Exclusions | This policy excludes no subject within its scope; if one is excluded, name it and its owner here. |
| Policy | Exception Conditions | This policy defines no exception condition of its own; exceptions follow the approval and safety policy's operator approval route. If this policy needs its own, state it here. |
| Policy | Approval and Review | This policy defines no exception approval or review step of its own; the approval and safety policy's operator approval route applies. If it needs its own, state it here. |
| Policy | Change and Adoption | This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here. |
| README | Runbook Links | `이 문서는 runbook이나 운영 가이드 링크를 따로 두지 않는다. 연결할 운영 문서가 생기면 여기에 연결한다.` |
| README | Observability and Recovery | `이 문서는 운영 관측과 복구만을 다루는 내용을 따로 두지 않는다. 그런 내용을 두게 되면 여기에 적는다.` |
| README | Security Boundary | `이 문서는 secret, credential, 권한 경계만을 다루는 내용을 따로 두지 않는다. 그런 내용을 두게 되면 여기에 적는다.` |
| README | Classification | `이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.` |
| README | Transition and Exit | `이 README는 상태, 승격, 종료 규칙을 따로 두지 않는다. 그런 규칙을 두게 되면 여기에 적는다.` |

- **Root gateway.** The root `AGENTS.md` keeps each rewritten line on one physical line, so its gateway counts (23 content and 16 heading lines before) stay within `AGENT-NATIVE-REFERENCE`; the Task records the counts before and after.
- **Pointers (W03-D31).** A pointer line stays when its target exists and says what it claims; the seven "Purpose text" pointers are corrected as scoped. The Task records the selection rule for pointer lines and the sample checked.
- **Check.** `BODY-SECTION-BARE` refuses, in an authored document of a role with a form, a childless H2 or H3 whose whole body, up to the next heading, is one bare statement: `None is stated in this document.`, `This (file|policy|document|README|skill|procedure) (states|marks) no <words>.` with no further clause, or one Korean sentence that starts with `이 문서`, `이 README` or `이 정책`, ends with `없다.`, may contain commas, and has no reason connective (`이며`, `므로`, `때문`). It sits beside `BODY-SECTION-EMPTY` under the authored-mode guard, so templates and roles without a form are not checked, and it leaves the shared empty-body helpers unchanged. It is ongoing protection of the empty policy for every new document written from these forms, not a check of this one migration. Its limit is stated: a reworded bare statement passes it, and sufficiency stays with semantic review.
- **Policy text.** The document authoring policy says that an empty required section states its reason and follow-up condition and that a pointer names a real location.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes and no ADR changes. The forms and their empty policy stay in the registry ([ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)).

## Data Modeling & Storage Strategy

No stored data changes. One validator rule is added.

## Interfaces & Data Structures

- `scripts/validate-markdown-profiles.py`: `BODY-SECTION-BARE` beside `BODY-SECTION-EMPTY`, covering a childless H2 and an H3, each read up to the next heading.
- Tests: each bare shape fails; an explained none passes; a pointer passes; a reworded line passes (the stated limit); a template passes; a role without a form is not checked; the `agents_body()` fixtures use explained lines.

## Edge Cases & Error Handling

- Native skill bodies are loaded on invocation and `work-lifecycle.md` every session; the new sentences say only what the owners already state and add no obligation, and the reason table is reviewed before editing.
- Three lines already carry a reason or a pointer and stay unchanged, unmatched by the rule: `AGENTS.md` line 10 ("; it is a provider gateway"), `.agents/governance/approval-and-safety.md` line 166 (a pointer to the operator approval route) and `.agents/evaluations/README.md` line 67 (a router reason).

## Failure Modes & Fallback / Human Escalation

If a line's reason is stated by neither the document nor its owners, or a rewrite would change a rule's meaning, the author stops the package, leaves it uncommitted and asks the user; no bare line is kept and no exception is added to the rule. If any document outside the scoped files gains a diagnostic, the change is wrong and is fixed before commit.

## Verification Commands

- Before and after, record the four strict document validators; diagnostics after must equal those before, the new rule refusing nothing after the rewrite.
- Run the rule on the unchanged tree and record its refusals, which must be exactly the 148 bare lines other than the three retained ones, then none after.
- `python3 scripts/validate-agent-governance.py --root .` with the root gateway counts before and after.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite agent-governance`, `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-EMPTY-001 | Every bare line is replaced from the reason table or by a listed document-specific sentence, the seven pointers are corrected, and the Task lists each line before and after; `BODY-SECTION-BARE` refuses exactly the 148 bare lines other than the three retained ones on the unchanged tree, and nothing after; semantic review accepts the sentences. |
| VAL-EMPTY-002 | The policy sentence is updated, the root gateway counts stay within the limit, validator diagnostics over the tree are unchanged apart from the new rule, and exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EMPTY-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | `BODY-SECTION-BARE` and semantic review. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-EMPTY-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
