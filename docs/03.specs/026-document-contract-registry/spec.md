---
title: 'Document Contract Registry Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-14
---

# Document Contract Registry Technical Specification (Spec)

## Overview

This Spec defines the single machine-readable registry for document routes,
frontmatter profiles, lifecycle state domains, section profiles, template
ownership, README profiles, and explicit classification/control exceptions. It is the
foundation for Specs 027 through 032.

## Strategic Boundaries & Non-goals

The registry owns exact values and relationships. Markdown support documents
own rationale and examples. It does not own affected-surface validator routing,
provider runtime configuration, topic content, or live operational state. It
does not introduce universal metadata fields or a root `DESIGN.md`.

## Contracts

- **Config Contract**: `docs/99.templates/support/document-profiles.json`
  declares current schema version `4`, profile definitions, path routes, exact or patterned
  exceptions, and template paths. It validates against
  `docs/99.templates/support/document-profiles.schema.json` using JSON Schema
  2020-12.
- **Data / Interface Contract**: Every routed tracked Markdown path resolves to
  exactly one profile. A profile declares required and allowed keys, ordered-key
  convention, types, states, required and allowed headings, and processing mode.
  `classification-only` means the registry classifies a path without owning or
  interpreting that file's frontmatter; it does not assert native runtime or
  provider consumption. The semantic projection is
  `DocumentProfileContract.v2`.
- **Governance Contract**: Stage 99 support owns the registry. Stage 00,
  templates, validators, README indexes, and CI link to or consume it and must
  not reproduce full route or lifecycle tables.

## Core Design

- **Component Boundary**: The two canonical Stage 99 contract paths above, a
  registry loader, and fixtures under `tests/fixtures/document-contracts/`.
  Human-readable support remains separate.
- **Key Dependencies**: JSON Schema 2020-12, a YAML parser that rejects duplicate
  keys, a CommonMark-aware body parser, and current repository path inventory.
- **Tech Stack**: Repository-local JSON plus the existing Python/shell quality
  gate stack; no network dependency at validation time.

The registry covers these profile classes:

- SDLC: PRD, ARD, ADR, Spec and helper Specs, Plan, Task, Guide, Policy,
  Runbook, Incident, and Postmortem.
- Common: Reference, Archive Tombstone, governance memory, and progress entry.
- Governance: reference and template support.
- README: repository, stage-index, collection-index, implementation,
  snapshot-pack, and workspace-staging.
- Explicit exceptions: root provider shims,
  `exception/local-agent-asset` for `.agents/**`,
  `exception/repository-runtime-baseline` for `.claude/CLAUDE.md` and
  `.codex/CODEX.md`, Claude-only `exception/provider-native-metadata`,
  GitHub-native control Markdown, generated records, and classification-only
  external-schema API contracts. `.gemini/**` stays uncovered until a
  separately approved Gemini CLI native design exists.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: `DocumentProfile` contains `id`, `routes`,
  `frontmatter`, `statusDomain`, `headings`, `template`, and `mode`. Each route
  is either an exact repository-relative path or an anchored regular expression;
  mixed implicit glob semantics are forbidden. Exact key sets use JSON Schema
  `required` and closed additional properties. Root provider shims and
  GitHub-native control profiles use `frontmatter-free` with frontmatter
  `forbidden`; local-agent assets, repository runtime baselines, Claude-native
  metadata, and native-contract profiles use `classification-only` with
  frontmatter `not-applicable`.
- **Migration / Transition Plan**: Start in compatibility mode, classify the
  fixed inventory, migrate templates and authored documents, then enable strict
  mode after uncovered and ambiguous routes reach zero.

## Interfaces & Data Structures

### Core Interfaces

```json
{
  "id": "sdlc/spec",
  "routes": [
    {"kind": "regex", "value": "^docs/03\\.specs/[0-9]{3}-[^/]+/spec\\.md$"}
  ],
  "frontmatter": {
    "required": ["title", "type", "status", "owner", "updated"],
    "allowed": ["title", "type", "status", "owner", "updated"]
  },
  "statusDomain": ["draft", "active", "done"],
  "template": "docs/99.templates/templates/sdlc/specs/spec.template.md"
}
```

The JSON Schema and this interface freeze the persisted shape; fixtures prove
conformance and must not become the owner of a different shape. Support prose
must not become a second parser input.

Path evaluation uses the following deterministic contract:

- Enumerate `git ls-files` at baseline SHA
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d` only under the approved target
  roots and root files, producing the approved 433-Markdown baseline inventory.
- Normalize to repository-relative POSIX paths with no leading `./`, `..`, or
  platform-specific separator and compare case-sensitively.
- Do not traverse ignored paths, `.worktrees/**`, or symlinked provider views;
  classify the tracked symlink entry, not a second copy of its target tree.
- Evaluate all exact and anchored-regex routes and require exactly one match;
  declaration order and first-match precedence have no meaning.
- Add every newly tracked Markdown file under an approved target root to the
  dynamic corpus. `RTK.md` and `graphify-out/**` remain explicit non-target,
  unchanged boundaries for this program.

## Edge Cases & Error Handling

- Reject a path that matches zero or multiple profiles.
- Reject duplicate YAML keys, unsupported keys, invalid scalar types, invalid or
  future authored dates, placeholder titles, and family-invalid states.
- Permit placeholders only in template mode and never in authored mode.
- Treat key order as a repository convention and report it separately from YAML
  data validity.
- Do not follow symlinked provider views twice when counting the inventory.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: The registry cannot represent a real path without overlapping
  another route.
- **Fallback**: Narrow the patterns or add a named exact exception with a fixture;
  do not add first-match precedence.
- **Human Escalation**: A new metadata key, profile family, or exception class
  requires a named consumer and an approved contract decision.

## Verification Commands

```bash
python3 scripts/validate-document-contract-registry.py --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode compatibility
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Positive fixtures cover every profile and exception class.
- **VAL-SPC-002**: Negative fixtures reject unsupported keys, status, date,
  title, duplicate key, uncovered route, and ambiguous route cases.
- **VAL-SPC-003**: All 433 approved baseline Markdown paths and every
  program-created target Markdown path receive exactly one classification;
  out-of-scope tracked Markdown remains unchanged and unclaimed.
- **VAL-SPC-004**: Stage 99 support and README indexes no longer need full copied
  route or lifecycle tables after their consuming Specs land.

## Traceability

### Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **ADR**: [Declarative Document Contract Registry](../../02.architecture/decisions/0015-declarative-document-contract-registry.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Audit**: [SDLC, Document Lifecycle, and Frontmatter](../../90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md)

### Delivery and References

- **Plan**: [Document Contract Registry Implementation Plan](../../04.execution/plans/2026-07-12-document-contract-registry.md)
- **Task**: [Document Contract Registry Task](../../04.execution/tasks/2026-07-12-document-contract-registry.md)
- **Next Spec**: [Template Contract Consolidation](../027-template-contract-consolidation/spec.md)
- **External Basis**: [JSON Schema object validation](https://json-schema.org/understanding-json-schema/reference/object), [YAML 1.2.2](https://yaml.org/spec/1.2.2/), and [GitHub Docs frontmatter convention](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
