---
title: "W03 Q-07 Renumbering Preparation"
version: "2.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0212"
---

# W03 Q-07 Renumbering Preparation Technical Specification (Spec)

## Overview

### Intent

This approved change contract is the Q-07 preparation half of the W03 stage of the external v14.7 execution package (`REQ:n` below is line n of `_workspace/workspace_execution_tasks_v14_7_revision_20261113_r1/tasks/TASK-hy-home-k8s-W03.md`, a read-only input; the cutover contract `dependencies/contracts/Q07-FINAL-CUTOVER.md` of the same package is cited by its stage letter). The requirement fixes Q-07 as a separate terminal transition after W11: the actual paths, document IDs and allocation bounds change only once W11 and every applicable `docs/` work are complete, and before that W03 does "survey, design, isolated rehearsal and consumer preparation" only (REQ:141, REQ:672 DOC-12 `수행`, REQ:823 D-17). The old non-reuse and reservation rule is applied before the transition and is reformed for the new space into the blocking of duplicate and stale requests (REQ:672, REQ:143). Real renumbering must not enter a W03 or W11 completion condition (REQ:137, REQ:918).

The user decided on 2026-11-14 to follow the requirement (W03-D75, answer "Follow REQ: prep package (Recommended)"), which amends W03-D30: that decision of 2026-11-13 said that nothing assumes or prepares the renumbering until all `docs/` work is finished, and the requirement says W03 prepares it while keeping the current number space. This package is the one W03 package that does so. It lands before the closing report (SPEC-0211), which reassigns the live DOC-12 row to Q07 after W11 (W03-D74); it does not close that row. The [Plan](plan.md) orders the work and the [Task](tasks/tsk-0001-w03-q07-renumbering-preparation.md) records execution.

The requirement says D-17 `옛 번호 재사용 금지의 한정 이행을 구현한다` (REQ:823) and DOC-12 `옛 비재사용·예약 규칙은 전환 이전에 적용하고 새 공간의 중복/낡은 요청 차단으로 개편한다` (REQ:672). This Spec reads them as follows: the limited non-reuse migration that W03 implements is the SPEC-0180 reservation, applied before the transition and completed where checks 1 and 2 of WORK-003 find a hole; the reform into the new-space duplicate and stale-request rule belongs to the Q-07 task (Q07-FINAL-CUTOVER stage B, line 21: the old global non-reuse, lineage accumulation and reserved bound are reformed as the policy of the new baseline's current space). W03-D75 ("confirms or completes the limited non-reuse migration") supports that reading. The smallest package that meets the requirement has three parts and no required code change. (1) A survey recorded in the Task of every number space, its allocator or producer, its references and its consumers, read from the tree at implementation. (2) A design of the isolated transition and a rehearsal of it in a scratch copy outside the repository, whose output is recorded in the Task and which renames nothing in the repository. (3) A confirmation of what the retired-identity reservation of SPEC-0180 already enforces and, only where the survey finds a hole that the requirement still needs closed before the transition, the completion of that reservation.

Facts observed at `main` `eb017bfe`, refreshed at `035143d1` where a line moved (every one is re-read at implementation and the Task records the observed value):

- Identity machinery. `artifact_identity_reuse_diagnostics` (`scripts/document_lifecycle.py` line 446) raises `LIFECYCLE-IDENTITY-REUSE` for a new owner of an identity that the comparison base holds at another path or that a retired set reserves. The retired set is `lineage_retired_identities` (line 1075): the identity tokens in the first cell of each `Archived Lineage` data row, read with children by prefix. `scripts/validate-document-lifecycle.py` (lines 1370 to 1372) builds it from the proposed and the base texts and memoizes it per commit in the cumulative-history path (`retired_between`, lines 1954 to 1960). `scripts/document-generator.py` (lines 205 to 220) refuses a new document with `GENERATOR-IDENTITY` by the same function over the current tree, and `expected_artifact_id` (`scripts/validate-markdown-profiles.py` line 497) derives the identity from the path number, so the path number is the identity.
- No allocator. The generator derives the identity from the caller's target path; no code chooses, reserves or counts the next number, and no `high_water` or `reserved_history` store exists in the registry or the scripts. The only gate on a stale or concurrent request is `GENERATOR-OCCUPIED` on the path, `GENERATOR-IDENTITY` on the tree and lineage at generation time, and the lifecycle comparison against the base at commit and merge time. The requirement's `발급 상한` (allocation bound) is therefore the highest number present plus the reservations, and not a stored value (the survey confirms).
- Number spaces by registry `path_pattern` and `artifact_id_pattern`: `REQ`, `AD`, `ADR`, `SPEC` (with `SPEC-NNNN-PLAN-0001` and `SPEC-NNNN-TSK-NNNN` nested in the package number), `GDE`, `POL`, `RUN`, incident `inc-YYYY-NNNN` (with `-PM`), and the Stage 90 packs `AUD`, `RES`, `DATA` with members `m-NNNN`. The tree at `eb017bfe` holds `docs/01.requirements` 0001 to 0004, descriptions 0004 to 0007, decisions 37 documents with gaps (0002 to 0061; 25 numbers appear among deleted paths in Git history), guides 0010, policies 0001, 0003, 0004, 0005, 0007, runbooks 0001 to 0004 and 0007 to 0012, audits 0001, research 0001 and 0002, and one Spec package, 0161.
- Consumers. 97 tracked files (96 at `eb017bfe`; re-read at implementation) outside `docs/` and `graphify-out/` name `SPEC-`, `REQ-` or `ADR-` identities (21 under `tests/`, 14 under `scripts/`, the rest across `gitops/`, `infrastructure/` and `.agents/governance/`); the work residue ledger `docs/03.specs/work-residue-ledger.json` names Task and Spec IDs. Whether each reference is a live link, a historical citation of a commit, an annotation or a fixed test expectation is the survey's classification.

### Owning Requirements

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view and no component changes. Identity stays a function of the path number (`expected_artifact_id`), and the reservation stays the one derivation of `artifact_identity_reuse_diagnostics`. This package adds a recorded design and rehearsal evidence and, on the conditional path only, a reservation completion.

## Scope

### In Scope

`소비자 준비` (consumer preparation, REQ:141, REQ:672) means the per-file consumer table of the survey, classes A and B in particular (the file, the line, what it names and the edit the Q-07 task makes), handed to the Q-07 task. No consumer is edited in this package or before Q-07.

- In scope (writer W03; the Task and records, plus a code or document edit only on the conditional path of the Contracts section "Non-reuse confirmation"): in the Task of this package, the survey record, the design record, the rehearsal record and the non-reuse confirmation, each as evidence rows or appended tables; in the SPEC-0161 Task, this package's own evidence row(s) and the frontmatter `version` and `updated`; on the conditional path only, the `Archived Lineage` rows of the owning Stage 01 and 02 documents, with their frontmatter `version` and `updated`, and the failing-first tests of the identity suites (`tests/test_document_artifact_identity.py`, `tests/test_document_generator.py`, `tests/test_document_lifecycle_cumulative_history.py`), re-read at the base; this package, the Stage 03 README entry and reviewed `.secrets.baseline` entries; at closure, the completed-spec lineage row of this package in the Archived Lineage table of REQ-0003, as sibling closures do.

### Non-goals

- Not in this package: any change of a real path, document ID, anchor, allocation bound, Stage directory name (`01`, `02`, `03`, `90`, `98`, `99` keep their names, REQ:141) or of `docs/99.templates/` placement; consuming SPEC-0001 or any new real number as a test (REQ:672 verification: `실제 새1번을 시험으로 소모하지 않는다`); any committed mapping file, rehearsal script or old-to-new table in the repository (the Q-07 task derives them again from the tree at its own time, Q07-FINAL-CUTOVER stage B); the reform itself of the old rule into the new-space duplicate and stale-request rule (designed and rehearsed here, implemented by the Q-07 task, W03-D76); removal of `Archived Lineage` or of any historical record (REQ:147 applies after the transition); a Registry Schema Version change; a SemVer reset (REQ:143, REQ:864: numbering and Contract Version are independent); the closure of DOC-12 or any edit of its live row or ledger entry (SPEC-0211 reassigns it, W03-D74); the Q-07 task itself, W04 to W11 work, and hosted CI.
- No push, PR or merge without the user's approval. Open question: none. This Spec stays `draft` until its approval receipt exists.

#### Decisions (W03-D75, W03-D76)

On 2026-11-14 the user decided (W03-D75, answer "Follow REQ: prep package (Recommended)"): W03-D30 is amended to the requirement; W03 prepares the Q-07 transition while keeping the current number space; one W03 package, landing before the closing report (SPEC-0211), surveys the actual ID, reference, allocator and consumer set, designs and rehearses the isolated transition in scratch only, and confirms or completes the limited non-reuse migration of old numbers together with SPEC-0180's retired-identity reservation; no real path, document ID or allocation bound changes before W11 and every applicable `docs/` work is complete. The same day the user answered the two design questions this package raised (W03-D76). The decision rows W03-D75 and W03-D76 are recorded in the SPEC-0161 Task by an earlier commit (the SPEC-0195 package commit, with W03-D74; neither is on `main` at `035143d1`), before this package lands, and this package appends no decision row. Open question: none.

- **Guard against a stale or old-number request (W03-D76, answer "Next-number rule (Recommended)").** After the transition the old identities and the `Archived Lineage` reservation are gone (REQ:147), and duplicate and stale requests must stay refused (REQ:143). A request prepared against the old numbers (for example `docs/03.specs/0213-x/spec.md`) is path-valid and its identity is free in the new space. The guard is a next-number rule: a new identity in a numbered space must equal the highest number in the comparison base plus one, which also keeps `1..N` without gaps. Consequences: no registry key and no schema change (the Registry Schema Version level is NO_CHANGE, below); a code rule in the Q-07 task; the habit of leaving gaps ends in the new space and the second of two concurrent branches renumbers at merge. Rejected: a baseline token in the registry (a key an earlier strict parser rejects, MAJOR) and reliance on the base duplicate rule alone (it admits old-number requests and leaves the hole the requirement names). This package designs the rule and rehearses it in the scratch copy (case 6) and records the diagnostics.
- **When the guard code lands (W03-D76, answer "With Q-07 after W11 (Recommended)").** The guard is implemented by the Q-07 task after W11 and every applicable `docs/` work, together with the reform of the old rule, not in W03: no allocation bound changes before W11 (REQ:141), and a rule that only means anything from a new baseline has nothing to guard now. Consequences: this package changes no code on the recommended path and adds no dormant rule; the only code it may edit is the conditional reservation completion of the Contracts section.

## Behavior Contract

### Normal Behavior

Contracts:

#### Survey record (WORK-001)

The Task records, read from the tree and Git at the implementation base (not from this Spec), one row per number space with these fields: the space and its registry profile; the path and identity grammar; the count `N`, the numbers present and the gaps; the allocator or producer (the generator, a manual path choice, a derived identity such as the Plan and Task numbers inside a Spec package); the reserved set (retired identities held by `Archived Lineage` rows, and by Git history only); every reference kind that names a member (frontmatter `artifact_id` and `parent_ids`, relationship links and anchors, README indexes and Stage 03 and Stage 90 owner tables, the residue ledger, `.agents/knowledge/` maps, `.github/` and CI paths, scripts, tests, `gitops/` and `infrastructure/` annotations, `.secrets.baseline` path keys, the workspace memory index); and the consumer class of each reference. Consumer classes: (A) live link or derived value that the Q-07 task rewrites in the same change; (B) a fixed test expectation or validator literal that the Q-07 task updates; (C) a historical citation tied to a commit, release, tag, `CHANGELOG` entry or PR, whose meaning stays inside that commit and is not re-read as a new number (Q07-FINAL-CUTOVER stage B, line 21); (D) a domain identifier that is not a document number and is excluded (cluster, namespace and resource names, Vault paths, product versions, template identifiers: REQ:285, REQ:776). The denominator and the exclusions are stated with the file counts. The survey is read-only; no number or string is replaced.

The survey also records the current sentences that the transition must amend and hands them to the Q-07 task, edited by no one here: `REQ-0003-FR-0023` ("Identifiers in existing decision history are not reassigned") and its acceptance row, and the sentence of `.agents/governance/document-lifecycle.md` ("Stable identities are append-only and never reused. Retired identities are reserved by the first column of the owners' `Archived Lineage`"); their amendment follows the user's standing decision that a rule conflicting with the current requirement changes to match it (EVD-018) and is part of the transition, not of this package. The survey also records the absences that the design relies on: no stored allocation bound, no reserved-history file, no allocator other than the generator, and for each space whether any non-document consumer pins a number. A consumer that cannot move (an external, immutable reference such as a published release or tag) or a real preservation hold is a narrow question for the user (REQ:823, REQ:815); finding none is recorded as the result.

#### Transition design record (WORK-002)

The design is a recorded decision set in the Task, not a document or a script in the repository. It fixes:

- **Mapping rules.** Spec: every existing package is closed by the Q-07 task first (Q07-FINAL-CUTOVER stage C, REQ:141), so the Spec space holds 0 packages and the next real new Spec receives `SPEC-0001` in the existing four-digit form; its Plan and Task numbers restart inside the package by their patterns. Every other numbered space is renumbered by ascending old number to `1..N` with no gaps, in the existing four-digit width; the Stage 90 pack members `m-NNNN` are renumbered inside their pack and each pack number by its space; incidents are per-year spaces keyed by the year folder, which is a date and is not renumbered. An empty space stays empty and receives no placeholder `0001`. Stage directory names, `docs/99.templates/`, domain identifiers and every SemVer value stay as they are (REQ:143, REQ:864, REQ:890).
- **Mapping contract.** The old-to-new mapping is derived from the tree, per file, per identity and per anchor, one to one, and the transition refuses a collision, a many-to-one entry and a missing entry. It lives only in a temporary location outside the final current `docs/` (Q07-FINAL-CUTOVER stage B) and is never committed.
- **Move procedure.** A two-step move through collision-free intermediate names, a candidate built in isolation, and a rollback to a recorded recovery point; a worktree alone does not isolate the shared allocation or memory state, so the rehearsal also names every shared store it did not touch.
- **Reservation after the transition.** The rule that replaces the `Archived Lineage` reservation: the reserved set is the identities of the comparison base (existing code path, `retired` empty), duplicates in the current tree stay refused, and the stale-request guard is the next-number rule of W03-D76, implemented by the Q-07 task. Git history keeps its own meaning: a replay of an earlier commit is judged under that commit's own base, and the design names how the cutover commit is judged (it renumbers every document, so the unmodified `LIFECYCLE-IDENTITY-REUSE` draws diagnostics there; the rehearsal measures them and the Q-07 task decides the boundary of the history replay, never a relaxation of the check).
- **SemVer.** Not reset. Document, Contract and Registry Schema versions follow their own policy (ADR-0061); the design records each object that would change at the transition and its level.

#### Isolated rehearsal (WORK-002)

The rehearsal runs on a scratch copy of the tree at the base, made outside the repository by `git clone --no-hardlinks <repo> <tmp>` into a temporary directory (a clone, because check 1, cases 4 and 6 and the base comparisons need history; no `git worktree`, no change to this repository's Git state), which is removed afterwards. The renumbering is applied there with a throwaway script that is not committed. The Task records the exact command text, the counts per space, the diagnostic counts per rule ID that the unmodified strict validators draw on the transformed copy, and these cases, each with its expected refusal and its observed result (REQ:672 verification, Q07-FINAL-CUTOVER stage D):

1. An old-space identity or path used in the new space (the old and new space confused).
2. A reference whose target was renumbered but not rewritten (wrong target reference).
3. A numbered document absent from the mapping (missing entry), a many-to-one or colliding mapping, a stale source hash, a half-moved mapping, an unresolved hold and an incomplete Task (Q07-FINAL-CUTOVER stage D); each must refuse the transition, and any of these the throwaway script cannot express is stated as left to the Q-07 task.
4. Two concurrent generations of the same next number (concurrent issue), run as two scratch copies merged.
5. A rerun of the transition on the transformed copy, which must not reset the numbers or remove new work (rerun reset).
6. A stale generation request with an old number after the transition (W03-D76), with two recorded results: unguarded (the hole demonstrated with the validators as they are) and guarded (a throwaway scratch-only patch implementing the W03-D76 next-number rule, never committed). The rule is defined over the staged, ci and explicit-ref base modes, over nested numbers (Plan, Task and `m-NNNN` take the next number inside their parent), over the per-year incident space, and over the case where the highest number is deleted and then re-added (the Task records the outcome against REQ:143). Stated plainly: after the transition a number deleted in an earlier commit is not refused by the base-held reservation, because the reservation reads only the comparison base and the `Archived Lineage` is gone; that is a recorded gap against REQ:143, handed to the Q-07 task, which decides its closure.
7. After the transformed copy is built: the first new Spec takes `SPEC-0001`, the next `SPEC-0002`, the Plan and Task of the first are generated and validated, all in the scratch copy; the real tree is shown unchanged and no real `SPEC-0001` exists.
8. Current links resolve to the new targets, and the real tree is unchanged, proved by the `git status --porcelain --ignored`, `git for-each-ref` and `git worktree list` records and `HEAD` before and after (Verification Commands).

The rehearsal uses the repository's validators as they are; a failure that shows a defect or a missing rule is recorded as a finding for the Q-07 task with its expected change, and is not fixed here unless it falls on the conditional path below.

#### Non-reuse confirmation (WORK-003)

SPEC-0180 (completed; recovery proof in REQ-0003) already enforces before the transition: `LIFECYCLE-IDENTITY-REUSE` rejects a new owner of an identity that the base holds or that an `Archived Lineage` first cell reserves, with children by prefix, in the staged, ci and explicit-ref comparisons and in the memoized cumulative-history path, and the generator applies it to the current tree and lineage. This is KEEP_VERIFIED under REQ:129 and the package does not rebuild it. It confirms, and records with the commands, three things:

1. The coverage claim: every identity deleted at any commit of Git history, in each number space, is either present in the tree or reserved by an `Archived Lineage` first cell. A read-only comparison in the scratch copy lists the remainder per space (`ADR` has deleted numbers at base, so the survey checks that its lineage rows name them; none is assumed).
2. The enforcement claim: the existing tests for the retired set and the generator refusal pass at the base, and each reserved sample of each space is refused by the generator and the lifecycle check.
3. The limit: the rule is the old global never-reuse rule and is applied until the transition; it is not removed or weakened here.

**Conditional path.** If the remainder of check 1 is not empty, or a space is not refused in check 2, the package completes the reservation by the smallest means that matches the existing design: an `Archived Lineage` row in the owning document for a remainder identity (documents only, no code), or, if a consumer fails to read a reserved space, a failing-first test and the smallest code edit in `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py` or `scripts/document-generator.py`, then the passing run. Any code edit on this path draws the Registry Schema Version question: none of the files above is the registry, so the level is NO_CHANGE unless the edit changes registry bytes, in which case it is MAJOR when an earlier validator rejects the new entry (ADR-0061; the reading of SPEC-0210) and the Task records the base value, the level and the reason. A finding that needs a change outside this list stops the work and goes to the user.

#### Registry Schema Version

No registry byte changes (W03-D76: the guard is a code rule with no registry key, implemented by the Q-07 task), so the level is NO_CHANGE and the Task records it. If the conditional path edits the registry, the Task records the base value read at implementation, the level (MAJOR for a key or rule that an earlier strict parser rejects, MINOR only if every consumer tolerates it) and the reason; the level is never chosen here without that reading.

#### Residue records

This package appends only its own evidence row(s) to the SPEC-0161 Task and the closure row at closure. It does not touch the live DOC-12 row, its ledger entry, W03-H20 or W03-H24, which SPEC-0211 and W03-D74 own. The survey, design and rehearsal records are the input of SPEC-0211's report and of the Q-07 task; DOC-12's resume condition stays Q07 after W11. Any follow-up that this package finds and that no owner holds becomes a `Residue Handoff` row of the SPEC-0161 Task with its ledger entry in the same change (ADR-0060), and `python3 scripts/validate-work-residue-ledger.py --root .` passes before and after.

Data modeling and storage strategy:

Nothing is stored in the repository except Task records and, on the conditional path, `Archived Lineage` rows. The rehearsal copy and its throwaway script live in a temporary directory outside the repository and are removed after the run; their outputs are recorded as counts, rule IDs, case results and hashes.

Interfaces and data structures:

No interface changes. The recorded survey table, the mapping rules, the rehearsal case table and the non-reuse check results are Task content. Each failing-first test of the conditional path fails on the base and then passes, and the cases that already pass are recorded as regression cases, not as failing-first.

### Failure and Edge Cases

Edge cases and error handling:

- A space with no members (Stage 90 data packs, incidents) stays empty after the transition and receives no placeholder.
- The `SPEC-0161` Task and any other Spec package are closed by the Q-07 task before the Spec space is reset; the rehearsal treats the Spec space as `0` packages and does not depend on the package contents.
- A reference inside a quoted commit, tag, release or `CHANGELOG` entry keeps its old meaning and is class C; a string that looks like an ID but is a domain identifier is class D.
- Tool availability: the validators need `ruamel.yaml` from the hashed lock (`.github/requirements/ci-validation.txt`); if it is absent at implementation, the check that needs it is recorded as an unavailable tool and an install into a scratch environment is a network step that needs the user's approval, not an assumption.
- A sibling package that lands first and changes a profile, a path pattern or an identity rule is picked up by a re-read of the base; the survey is dated at the SHA it read.

Failure modes and fallback or human escalation:

If the survey finds a consumer that cannot be updated by the Q-07 task, a preservation hold, or an authority conflict, the author stops and asks the user a single specific question in the form of REQ:823 (conflict ID, exact file and line, current approval and implementation, requirement clause, consumer and effect, the options, a recommendation, the single decision, the scope preserved until the answer). If the rehearsal needs a real path, ID or allocation change, if a check fails twice with no new information, or if a repair would widen the scope, the author stops and names the next owner. No suppression, test weakening or relaxed check ends the loop. Rollback: the package adds only documents (and, on the conditional path, lineage rows or code); revert the implementation commit, and before that delete the package commit. The scratch copy is deleted after the run.

## Acceptance Criteria

### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| VAL-Q07PREP-001 | Every reference to a numbered identity found by the survey is classified A to D with the denominator and exclusions stated; held or immovable consumers are listed, or the result is "none found" with the search command; the Task holds the survey record per number space, the absences (no stored bound, no reserved-history store, no other allocator) and the transition design record (mapping rules, mapping contract, move procedure, reservation after the transition, next-number guard, SemVer position). |
| VAL-Q07PREP-002 | The scratch rehearsal output is recorded with its command text, the per-space counts, the per-rule diagnostic counts and the eight cases with their observed results; the real tree is unchanged (clean status, same `HEAD`, no `SPEC-0001`, no renamed path, the status, `for-each-ref`, `worktree list` and `HEAD` records equal); the non-reuse confirmation records checks 1 to 3 and, if the conditional path ran, the completed reservation with failing-first and passing results; the Registry Schema Version level (NO_CHANGE) is recorded; the live DOC-12 row and its ledger entry are untouched (the row stays stale until SPEC-0211 edits it); exact-index QA and the commit hooks pass. |

### Evidence Requirements

- The four strict document validators over the tree before and after, with equal diagnostics.
- `git status --porcelain --ignored`, `git for-each-ref`, `git worktree list` and `git rev-parse HEAD` before and after the rehearsal (ignored `__pycache__` directories from validator runs are noted, not counted as a change); a scan showing no `SPEC-0001` and no renamed path in the repository.
- The read-only coverage comparison of check 1, with its command text, run in the scratch copy; the existing identity tests (`python3 scripts/run-contract-tests.py --root . --suite document` and `--suite document-lifecycle`).
- On the conditional path only: a failing-first run of each new test on a scratch copy of the base and then the passing run; `ruff check scripts tests` and `ruff format --check scripts tests`.
- `python3 scripts/validate-work-residue-ledger.py --root .` before and after the ledger step; markdownlint over the edited Markdown; `python3 scripts/validation/repository/quality.py --root .`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## References

### Normative and Evidence

No separate reference list is kept; the requirement, architecture and decision owners this Spec relies on are linked in [Lifecycle Traceability](#lifecycle-traceability) below.

### Historical and Navigation

No separate reference list is kept; this Spec holds no historical or navigation links beyond the [Plan](plan.md) and the Task that its Overview names.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-Q07PREP-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Survey record of identities, consumers and holds read at the base; design record. |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-Q07PREP-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Scratch rehearsal cases, non-reuse checks, strict validators, unchanged real tree. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-Q07PREP-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Scratch rehearsal cases, non-reuse checks, strict validators, unchanged real tree. |
