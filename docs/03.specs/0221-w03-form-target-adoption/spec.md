---
title: "W03 Form Target Adoption"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-17"
artifact_id: "SPEC-0221"
---

# W03 Form Target Adoption Technical Specification (Spec)

## Overview

### Intent

The 4.2.0 W03-FORMS prompt compares the current common forms with the package's template design targets, definition model 4.0.0. Those targets changed after the 3.0.1 targets that the completed W03-FORMS work checked. The new targets name concrete H2 and H3 headings and section IDs for each role. Twelve roles in this repository differ from them: requirement, architecture, spec, plan, guide, runbook, policy, incident, postmortem, root README, stage README, service README and skill. Only the task role already matches. On 2026-11-17 the user chose to adopt the candidate in full for those roles, and the choice is recorded in the [Task](tasks/tsk-0001-w03-form-target-adoption.md). The package marks the targets as a design proposal, not workspace adoption. This Spec is the adoption contract for this repository.

This Spec changes the heading tree of each role's common form, its templates and every current document of that role. It keeps every sentence and every recorded fact. The [Plan](plan.md) orders the work role by role.

### Owning Requirements

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the governance requirements. That includes the single registry owner of forms and the rule that a form change moves its consumers in the same change. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view. Accepted [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) gives the registry common form model that this Spec extends. It changes neither document.

## Scope

### In Scope

- The Stage 99 registry `common_forms` entries of the twelve roles. Each gets the target H2 and H3 titles, their order and the target section IDs, such as `requirement.intent` and `requirement.intent.1`. Each also gets content and requiredness rules, and keeps a local extension only where this Spec names one.
- The profile body contracts, policy rule ID bindings and TemplateDefinitions that name a moved section. Each changed TemplateDefinition gets a MAJOR `contract_version` increase and a migration record.
- The physical templates of those roles: 17 files under `docs/99.templates/templates/`.
- Every current document of those roles outside `docs/98.archive/`:
  - 4 Requirements and 4 Architecture Descriptions;
  - 1 operations guide and 10 runbooks;
  - 5 operations policies and 10 governance rules;
  - 19 skills and workflows;
  - the root README, 21 stage and collection READMEs and 21 service READMEs.
- A `retained_form` extension on the spec and plan forms. It is bound to the identities `SPEC-0161`, `SPEC-0161-PLAN-0001`, `SPEC-0221` and `SPEC-0221-PLAN-0001` in their approved status, so those approved and frozen files keep their accepted form and are not edited.
- The validators and tests that name a moved section by ID or title, and the governance and Stage 99 prose that names a moved heading.

### Non-goals

- Table columns and the typed `tables`, `metadata_policy`, `relationships` and `lifecycle` members of the targets. Current tables and their columns stay unchanged. The difference is recorded as residue for a later scoped change.
- The task role, whose headings already match. Its section IDs stay unchanged.
- The forms of other roles: ADR, AGENTS, workspace README, reference reports and packs, the knowledge map, vocabulary, prompt, governance document and role, and evaluation. The target roles decision, research, audit, data-reference and agent-instructions have no form of that name here; their mapping is residue.
- Completed records in `docs/98.archive/` and Git history.
- Renumbering, which stays with Q07-CUTOVER. No push, merge, secret read, cluster access or remote setting change without the user's separate request.

## Behavior Contract

### Normal Behavior

Each document moves by one map, and nothing is deleted:

- **keep:** the section keeps its title.
- **rename:** the section is retitled in place.
- **H4:** the former H3 and its body move unchanged under the named new H3, as an H4 with the former title. Its anchor text stays the same.
- **new:** the new H3 holds a statement written only from facts the same document or its named owner already holds. A template gets an author prompt instead.

The prose under a removed H2 moves to the first H3 of the H2 that receives it. A local H3 extension keeps its title and moves to the H2 named in the map, and the body contract of its profile names that H2.

| Role | New H2 / H3 | From |
| --- | --- | --- |
| requirement | Overview / Problem and Outcome; Stakeholders | keep |
| requirement | Scope / In Scope; Constraints and Exclusions | keep |
| requirement | Requirements / Functional Requirements; Quality Requirements (stays conditional) | keep |
| requirement | Traceability / Sources | rename Source and Constraints |
| requirement | Traceability / Verification Links | rename Downstream Links; H4 Acceptance Conditions and Verification Method (Acceptance Criteria H2 removed) |
| requirement | Traceability: local H3 Lifecycle Traceability and Archived Lineage | keep |
| architecture | Context and Boundaries / System Boundary | keep; H4 Purpose and Readers, Context |
| architecture | Context and Boundaries / Constraints | keep |
| architecture | Structure / Building Blocks; Interfaces | keep; rename Contracts |
| architecture | Runtime Behavior / Normal Flow; Failure and Recovery | rename Runtime and Deployment; rename Failure Boundaries |
| architecture | Quality Scenarios / Scenarios; Trade-offs | rename Quality and Risks; new |
| architecture | Decisions and Adoption / Decisions; Adoption Boundaries | rename Decision Links with H4 Requirement Mapping; rename Currentness and Lineage |
| architecture | Decisions and Adoption: local H3 Lifecycle Traceability and Archived Lineage | moved from Traceability |
| spec | Overview / Goal; Consumers | rename Intent with H4 Owning Requirements; new |
| spec | Scope / In Scope; Out of Scope | keep; rename Non-goals |
| spec | Behavior Contract / Inputs and Outputs; Failure Behavior | rename Normal Behavior; rename Failure and Edge Cases |
| spec | Acceptance Criteria / Criteria; Verification Strategy | keep; rename Evidence Requirements with H4 References (References H2 removed) |
| spec | Acceptance Criteria: local H3 Lifecycle Traceability | moved from References |
| plan | Overview / Outcome; Constraints | rename Goal and Boundary; rename Assumptions with H4 Global Constraints, Risks and Mitigations, Escalation (Risks H2 removed) |
| plan | Dependencies / Prerequisites; Shared Resources | keep; new |
| plan | Work Breakdown / Work Units; Dependency Edges | rename Work Breakdown with H4 Change and Rollback; rename Dependency Order |
| plan | Verification Plan / Selected Checks; Evidence Plan | rename Verification Matrix; rename Stage Placement |
| plan | Promotion Map / Durable Owners; Consumer Updates | rename Owner and Receipt (receipt table); rename Durable Meaning |
| guide | Purpose / Audience; Outcome | new; keep with H4 Boundaries |
| guide | Prerequisites / Environment; Authority | keep; rename Permissions |
| guide | Procedure / Steps; Expected Results | rename Actions; rename Expected Result |
| guide | Troubleshooting / Symptoms; Next Action | rename Troubleshooting; rename Exceptions |
| guide | Troubleshooting: local H3 Lifecycle Traceability | moved from Verification |
| runbook | Trigger and Scope / Trigger; Targets | rename Trigger and Outcome; rename Scope |
| runbook | Preflight / Authority; Environment | rename Authority and Access; rename Safety Checks |
| runbook | Procedure / Steps; Stop Conditions | rename Actions; keep |
| runbook | Verification / Expected Results; Unverified Conditions | rename Service Checks; rename Evidence |
| runbook | Verification: local H3 Lifecycle Traceability | moved from Validation |
| runbook | Escalation / Next Owner; Recovery or Forward Repair | rename Escalation; rename Rollback (stays conditional on a state change) |
| runbook | Escalation: local H3 Recovery Procedures | moved from Recovery |
| policy | Purpose and Scope / Objective; Applies To | keep; keep with H4 Exclusions |
| policy | Rules / Requirements; Exceptions | keep; rename Exception Conditions with H4 Approval and Review |
| policy | Enforcement / Mechanisms; Limits | rename Enforcement; new |
| policy | Ownership / Owner; Review Triggers | rename Authority with H4 Responsibilities; rename Change and Adoption |
| policy | Ownership: local H3 Lifecycle Traceability | keep |
| incident | Impact / Affected Users; Observed Scope | keep; rename Severity and Duration with H4 Event, Current Status |
| incident | Response / Timeline; Actions | rename Events with H4 Decisions; rename Mitigation |
| incident | Resolution / Verified State; Remaining Work | rename Recovery Verification; rename Follow-up Owners with H4 Evidence Sources |
| incident | Resolution: local H3 Lifecycle Traceability | moved from Evidence |
| postmortem | Facts / Timeline; Impact | rename Incident Reference with H4 Review Scope; rename Observed Impact with H4 Detection and Response |
| postmortem | Causes / Contributing Factors; Uncertainty | keep with H4 Causal Analysis; new |
| postmortem | Actions / Prevention; Owners and Checks | rename Actions; rename Verification with H4 Source Records, Review Decision |
| postmortem | Actions: local H3 Lifecycle Traceability | moved from Corrective Actions |
| root README | Purpose / Audience; Outcome | rename Project Role; new with H4 Boundaries |
| root README | Getting Started / Prerequisites; First Use | keep; rename First Verified Path |
| root README | Repository Map / Current Paths; Owners | rename Directories; rename Canonical Entry Points |
| root README | Support / Help; Related Documentation | rename Support and Ownership; rename Current Documentation |
| stage README | Responsibility / Purpose; Excluded Responsibilities | rename Purpose and Readers with H4 Inputs and Outputs; new |
| stage README | Current Contents / Paths; Owners | rename Current Items; rename Classification |
| stage README | Usage / Entry Points; Checks | rename Create and Review with H4 Upstream and Downstream, Policy and Templates; rename Transition and Exit |
| service README | Service / Purpose; Interfaces | rename Service Role; rename Inputs and Outputs with H4 Security Boundary |
| service README | Usage / Prerequisites; Selected Start | rename Supported Environment; rename Local Workflow |
| service README | Checks / Readiness; Failure Handling | rename Checks; rename Observability and Recovery with H4 Runbook Links |
| skill | Trigger / When to Use; When Not to Use | keep with H4 Inputs; keep |
| skill | Trigger: local H3 Authority Boundary | moved from Purpose and Trigger |
| skill | Procedure / Steps; Failure Handling | keep |
| skill | Outputs / Artifacts; Handoff | rename Outputs; rename Completion and Handoff |
| skill | Verification / Checks; Limits | keep; new |

Every section ID of a changed form takes the target form: `<role>.<group>` for an H2 and `<role>.<group>.<n>` for an H3, as the target names them. Stage and service READMEs keep their Korean bodies. Headings stay English.

### Failure and Edge Cases

- A document that keeps an old heading, an unregistered H3, a missing required H3 or a heading only inside a code fence, quote or HTML block fails the registry form check.
- A `new` section with no supporting fact in its document is not filled with filler or `N/A`. The role's requiredness for that section is then reconsidered in the Task. It does not pass silently.
- A link to a removed anchor fails the link check, and the link is repointed to the receiving section in the same change.
- A retained form admits only the four named identities in `approved` status. Any other Spec or Plan, or those identities in another status, takes the new tree.
- A validator or test that names a removed section ID fails until it reads the new ID. No alias for an old ID is kept, as `scripts/AGENTS.md` rule 3 requires.
- Rollback before merge deletes the branch. After merge, revert the merge commit, because Git history keeps every former tree.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-FORM-001 | The registry forms of the twelve roles carry the target H2 and H3 titles, order and section IDs, with their TemplateDefinitions at a new MAJOR version. The strict registry check passes. Focused negative tests refuse each role's former tree, a fenced or quoted heading and a missing required H3. |
| VAL-FORM-002 | Every template and current document of those roles passes the strict document validators under the new forms. Each moved section follows the map, with no dropped sentence and no empty or `N/A` section. Every link resolves. |
| VAL-FORM-003 | The four retained identities pass unchanged. A fifth Spec or Plan in the old tree is refused. The `document` contract suite and `python3 scripts/qa.py staged` pass, and the out-of-scope differences are recorded as residue. |

### Evidence Requirements

- The strict registry, markdown profile, link and owner, and lifecycle validators. The work residue ledger gate. The `document` suite of `scripts/run-contract-tests.py`. `python3 scripts/qa.py staged` through the commit hooks on each exact index.
- Focused RED and GREEN tests for each changed check.
- A sentence count before and after each document moves, recorded per role in the Task.
- Risk class `high` (governance forms, validators and policy text): an independent read-only review of the map, the new sections and the code diff before acceptance.

## References

### Normative and Evidence

- [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md), [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md).
- The package targets are evidence only. Their SHA-256 and the user's choice are in the Task.

### Historical and Navigation

- SPEC-0169 to SPEC-0203 (exited) moved these roles to the current forms. Their maps are recoverable from the REQ-0003 Archived Lineage.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Strict registry check and focused negative tests. |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict document validators and per-role sentence counts. |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORM-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Retained-form tests, `document` suite and staged QA. |
