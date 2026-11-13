---
title: "W03 SemVer Vocabulary and Version Fields"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0190"
---

# W03 SemVer Vocabulary and Version Fields Technical Specification (Spec)

## Overview

This approved change contract applies the SemVer section of the v14.7 2026-11-13 revision of the W03 task (`SEMVER-POLICY.md` sections 2, 3, 4 and 6) to this repository. A 2026-11-13 survey found three gaps. First, `.agents/knowledge/glossary.md` defines none of the eight terms the revision asks for (Public Contract, Compatibility, Contract Version, Registry Schema Version, Document Revision, Prerelease, Build Metadata, Baseline Namespace). Second, version values are checked by three different grammars: `docs/99.templates/contracts/frontmatter.schema.json` (`^[0-9]+\.[0-9]+\.[0-9]+$`), `docs/99.templates/contracts/document-profile.schema.json`, whose three contract `version` patterns differ among themselves (line 48 for `shared_contract` allows leading zeros and a lowercase prerelease but no build metadata; line 163 for an `adopted` contract and line 845 for `common_forms` allow the numeric core only, leading zeros included) and `scripts/validate-agent-governance.py` for the native skill envelope (`[0-9]+\.[0-9]+\.[0-9]+`), so `01.2.3` and `1.02.3` pass while SemVer 2.0.0 refuses them; only `scripts/release.py` holds the full grammar. Third, the version paragraph of `.agents/governance/document-authoring.md` does not say which values are SemVer and which are not, and has no rule for the `0.y.z` range or for several changes in one edit. The [Task](tasks/tsk-0001-w03-semver-vocabulary.md) records execution and the [Plan](plan.md) orders the work. W05 owns any further SemVer regression when a new consumer compares versions; W06 owns tag and pull request consumption.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): in the SPEC-0161 Task the decision row W03-D45 and its evidence row (package commit); a new module `scripts/semver_grammar.py` holding the one SemVer 2.0.0 grammar; `scripts/release.py` building its tag pattern from it; `scripts/validate-agent-governance.py` (the native skill envelope `version` check); `scripts/run-contract-tests.py` (the `document` suite gains the new test module); the `version` pattern of `frontmatter.schema.json` and the three contract `version` patterns of `document-profile.schema.json` (lines 48, 163 and 845); the eight common glossary terms; the version paragraph of `document-authoring.md`; tests; `scripts/README.md` for the new module; each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README entry and reviewed `.secrets.baseline` entries.
- Not in this package: any change of an existing version value (all 205 Markdown `version` values and the registry contract versions already meet the strict grammar); the registry `schema_version`, which stays the integer 10 and is named a Registry Schema Version, not SemVer; artifact identities and Q-07 numbering (W03-D30); input package edition labels such as `v14.7` or `repository-vocabulary v14.5`, which are not SemVer and are not converted; a version comparison for documents, which no current consumer needs; the edition-mention pattern at `scripts/document_contracts.py` line 1487, which reads edition labels in prose and stays; tags, CHANGELOG and GitHub Release (W06; `scripts/release.py` keeps its behavior).
- No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: the glossary edition, decided by W03-D45 before the package commit.

## Contracts

- **One grammar.** `scripts/semver_grammar.py` exports `SEMVER_PATTERN`, the SemVer 2.0.0 grammar without anchors or `v` prefix: numeric core without leading zeros, optional prerelease whose numeric identifiers have no leading zero, optional build metadata, with the same five capture groups `scripts/release.py` reads today (major, minor, patch, prerelease, build). `scripts/release.py` builds its tag pattern as `v` + `SEMVER_PATTERN` + `\Z`, so `parse_version` and its tests stay unchanged and pass; the skill envelope check uses `re.fullmatch`. `validate-agent-governance.py` refuses a skill envelope `version` that does not fully match it.
- **Schemas.** The `version` pattern of `frontmatter.schema.json` and the three contract `version` patterns of `document-profile.schema.json` become `^` + `SEMVER_PATTERN` + `$`. A test asserts that each schema pattern equals that string, so the copies cannot drift.
- **Cases.** The case file `SEMVER-CASES.json` of the v14.7 revision fixes the expected results: `0.1.0`, `1.2.3`, `1.0.0-rc.1`, `1.2.3+build.007` and `1.2.3-rc.1+sha.abc` are accepted; `1.2`, `01.2.3`, `1.02.3`, `1.2.03`, `v1.2.3`, `1.2.3-01`, `1.2.3-`, `1.2.3+` and `1.2.3.4` are refused, by the module, by each schema pattern and by the skill envelope check. The precedence cases (`1.9.0` < `1.10.0`, `1.0.0-rc.2` < `1.0.0-rc.10` < `1.0.0`, and equal precedence for `1.2.3+build.1` and `1.2.3+build.2`) are checked through the existing `release.py` precedence function. The cases are copied into a new test module `tests/test_semver_grammar.py`, registered in the `document` suite of `scripts/run-contract-tests.py`; they are not read from `_workspace/`.
- **Glossary.** The common Repository Vocabulary table gains eight rows, each with the seven existing columns (Term ID, Term, Korean, Definition, Not to Confuse, Policy Owner, Contract Version). The Contract Version cell is the edition recorded by the SPEC-0161 decision row of this package (W03-D45, recorded with the package commit); the Korean cells are `공개 계약`, `호환성`, `계약 판본`, `레지스트리 스키마 판본`, `문서 개정 판본`, `사전 배포판`, `빌드 메타데이터` and `기준선 번호 공간`. The terms are TERM-PUBLIC-CONTRACT (the observable promise a consumer relies on), TERM-COMPATIBILITY (whether earlier valid producers and consumers keep working without breaking that promise), TERM-CONTRACT-VERSION (the SemVer version of a shared contract's consumable meaning; one contract ID at one version means one meaning), TERM-REGISTRY-SCHEMA-VERSION (the version of the data structure that code reading the registry expects, kept apart from profile content), TERM-DOCUMENT-REVISION (the SemVer `version` of one document's normative content), TERM-PRERELEASE (the hyphen part of a SemVer value, which ranks below its release), TERM-BUILD-METADATA (the plus part, which never affects precedence) and TERM-BASELINE-NAMESPACE (the current scope that keeps document identities apart; identities are not versions, and renumbering never resets a version). Each row names its policy owner and a Not to Confuse cell; no existing row changes.
- **Version paragraph.** `document-authoring.md` keeps its sentences and adds: a version value is a SemVer 2.0.0 string with no `v`, checked by the shared grammar; Document Revision, Contract Version and Registry Schema Version are separate objects, and an artifact identity or a package edition label is not a version; in `0.y.z` an incompatible change and a feature raise the minor and a compatible fix raises the patch; one edit raises the highest affected level once, and an unchanged object keeps its version; a commit type such as `docs:` does not by itself decide the level.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The grammar has one owner in code and four declared copies in the JSON schemas that a test pins to it.

## Data Modeling & Storage Strategy

No data changes. The registry `schema_version` stays the integer 10.

## Interfaces & Data Structures

`scripts/semver_grammar.py`: `SEMVER_PATTERN: str` and `is_semver(value: str) -> bool`. No other function.

## Edge Cases & Error Handling

- A value with surrounding spaces or a `v` prefix is refused; a tag keeps its `v` in `scripts/release.py` only.
- Build metadata with leading zeros (`+build.007`) is accepted, as SemVer 2.0.0 allows.
- An uppercase prerelease such as `1.0.0-RC.1` becomes valid in `document-profile.schema.json`, as SemVer 2.0.0 allows; no current value uses one.

## Failure Modes & Fallback / Human Escalation

If any current document, template or registry value fails the strict grammar, the author stops and asks the user rather than editing the value. If a strict document validator gains a diagnostic, the change is fixed before commit.

## Verification Commands

- Record the four strict document validators before and after; diagnostics must be equal.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite agent-governance`, `--suite release` and `--suite tooling`.
- `git grep -n -E '^version: ' -- '*.md'`: every value fully matches `SEMVER_PATTERN`.
- `ruff check scripts tests`, `ruff format --check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SEMVER-001 | `scripts/semver_grammar.py` owns the grammar; `release.py`, the skill envelope check and the four schema patterns use or equal it; the case tests fail first and then pass; existing release tests pass unchanged. |
| VAL-SEMVER-002 | The glossary has the eight terms with the edition W03-D45 records, Korean cells and owners, and the version paragraph carries the added rules; validator diagnostics over the tree are unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SEMVER-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Knowledge surface check; read of each new term against the revision text. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SEMVER-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Case tests; strict validators over the tree; exact-index QA. |
