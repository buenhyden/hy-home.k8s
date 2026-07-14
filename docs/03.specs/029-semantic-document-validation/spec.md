---
title: 'Semantic Document Validation Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-12
---

# Semantic Document Validation Technical Specification (Spec)

## Overview

This Spec implements registry-driven document validation with explicit parsing,
positive and negative fixtures, compatibility and strict modes, and stable
diagnostics. It replaces hardcoded route, key, status, and heading assumptions
inside the current repository quality gate.

## Strategic Boundaries & Non-goals

This tranche validates structure and repository semantics. It does not judge
the truth of every prose claim, execute live infrastructure, or treat external
link availability as proof of technical correctness. It does not rewrite the
document population; Spec 030 owns migration.

## Contracts

- **Config Contract**: Validators load versioned registries and fail closed on
  malformed schema, duplicate profile IDs, invalid patterns, or missing forms.
- **Data / Interface Contract**: Diagnostics name the path, profile, rule ID,
  expected value, actual value, and remediation owner without printing secret
  content.
- **Governance Contract**: Compatibility mode reports known migration debt;
  strict mode rejects it. New exceptions require fixtures and an owner.

## Core Design

- **Component Boundary**: Frontmatter extractor, strict YAML mapping loader,
  Markdown block parser, route classifier, profile validator, link/index checker,
  duplicate-owner detector, template-residue detector, and fixture runner.
- **Key Dependencies**: Specs 026–028 and the fixed tracked-file inventory.
- **Tech Stack**: Python or the existing repository-supported runtime, JSON
  Schema 2020-12, YAML 1.2-compatible parsing, and no validation-time network.

Validation layers:

1. File classification and explicit exception handling.
2. Exact frontmatter delimiter, mapping, key, type, order, and value checks.
3. Body structure with fenced-code-aware H1/H2 parsing.
4. Template required/allowed section and residue checks.
5. Cross-link, README inventory, and duplicate-current-owner checks.
6. Compatibility-debt accounting followed by strict cutover.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Fixtures are small repository trees with expected
  rule IDs and exit codes. They cover positive and one-fault negative cases per
  profile and cross-document constraint.
- **Migration / Transition Plan**: Introduce the validator without replacing the
  current gate, compare results, migrate the corpus, then make the new validator
  canonical and remove duplicated hardcoded rules.

## Interfaces & Data Structures

### Core Interfaces

```text
validate --root PATH --mode compatibility|strict
validate --self-test
result: PASS | FAIL | SKIP | DEFER
diagnostic: RULE_ID path expected actual owner
```

## Edge Cases & Error Handling

- Parse only an exact first-line frontmatter delimiter and reject an unclosed
  block; YAML frontmatter is a repository preprocessing convention, not GFM.
- Reject duplicate mapping keys before generic YAML construction can overwrite
  them.
- Validate real calendar dates and future-date policy separately from JSON
  Schema `format` annotations.
- Ignore Markdown headings inside fenced code but reject malformed or unclosed
  fences according to CommonMark parsing behavior.
- Avoid following symlinks into duplicate provider views or ignored worktrees.
- Treat generated files and immutable historical bodies only by their declared
  profile, not by authored-current rules.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: The new parser disagrees with GitHub/CommonMark rendering.
- **Fallback**: Add a minimal conformance fixture and correct the parser; do not
  add a path-specific waiver for parser bugs.
- **Human Escalation**: A semantic rule with no deterministic signal remains a
  review checklist item rather than a false automated guarantee.

## Verification Commands

```bash
python3 scripts/validate-markdown-profiles.py --self-test
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Every registry profile and cross-document rule has a positive
  fixture and at least one focused negative fixture.
- **VAL-SPC-002**: Invalid duplicate keys, dates, titles, states, sections,
  routes, owner duplication, and README inventory are rejected deterministically.
- **VAL-SPC-003**: Compatibility output accounts for every known migration item;
  strict mode passes after Spec 030 with no silent allow-list.
- **VAL-SPC-004**: The repository quality gate consumes the new validators and
  removes superseded hardcoded profile logic.

Implementation closed through SMDV-004. The quality wrapper now delegates
registry classification, Markdown profiles, and cross-document semantics to
the three canonical strict-mode CLIs. It retains the complete
template-compatibility fixture digest/mutation proof and workspace-specific
operations, GitOps, infrastructure, agent-runtime, CI/QA, security, and
supply-chain checks. Spec 030 ADM-007 completed the strict-mode transition;
compatibility mode is retained only for historical migration evidence and is
not the current quality-gate contract. Repository-static PASS does not
establish live cluster or provider readiness.

## Traceability

### Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Registry Spec**: [Document Contract Registry](../026-document-contract-registry/spec.md)
- **README Spec**: [README and Workspace Profiles](../028-readme-workspace-profiles/spec.md)

### Delivery and References

- **Execution Plan**: [Semantic Document Validation Implementation Plan](../../04.execution/plans/2026-07-12-semantic-document-validation.md)
- **Execution Task**: [Task: Semantic Document Validation](../../04.execution/tasks/2026-07-12-semantic-document-validation.md)
- **Next Spec**: [Authored Document Migration](../030-authored-document-migration/spec.md)
- **Parsing Basis**: [CommonMark](https://spec.commonmark.org/0.31.2/) and [JSON Schema validation](https://json-schema.org/draft/2020-12/json-schema-validation)
