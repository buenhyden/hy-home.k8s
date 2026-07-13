---
title: 'Authored Document Migration Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-12
---

# Authored Document Migration Technical Specification (Spec)

## Overview

This Spec migrates the tracked document population to the approved profiles,
consolidates duplicate ownership, removes template residue, repairs cross-links,
and relocates AWS and Azure SDLC prose into dated provider snapshots under
`docs/90.references`.

## Strategic Boundaries & Non-goals

This tranche changes authored and index documents after Specs 026–029 provide
stable contracts and compatibility validation. It preserves completed Plan and
Task evidence, accepted ADR history, dated research and audit facts, archive
Tombstones, generated-owner boundaries, provider-native metadata, and ignored
local state. It does not rewrite history for stylistic uniformity.

## Related Inputs

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- **Lineage ADR**: [Program-to-Tranche Document Lineage](../../02.architecture/decisions/0016-program-to-tranche-document-lineage.md)
- **Validation Spec**: [Semantic Document Validation](../029-semantic-document-validation/spec.md)
- **Current Audit**: [SDLC, Document Lifecycle, and Frontmatter](../../90.references/audits/2026-07-11-weia/sdlc-document-lifecycle-frontmatter.md)

## Contracts

- **Config Contract**: A migration inventory records each approved target
  Markdown path, profile, current owner, disposition, destination, source set,
  topic-research decision, and validation result at baseline SHA
  `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d`.
- **Data / Interface Contract**: Dispositions are `preserve`, `transform`,
  `merge`, `relocate`, `tombstone`, or `delete`; every non-preserve action names
  the canonical destination and rollback commit.
- **Governance Contract**: Unique topic content survives consolidation; copied
  governance and template instructions do not. Historical evidence stays
  historically accurate and never becomes current authority.

## Core Design

- **Component Boundary**: Current authored non-README documents in the approved
  433-file baseline corpus plus program-created authored documents. Stage 99
  support/templates, README bodies, provider gateways/adapters, validation
  selection, and protected machine surfaces remain owned by their preceding or
  following tranche as defined below. The only exception is structural
  canonicalization of thirteen paths already registered as finite Spec 030
  shape debt: six support documents, three Stage 00 authoring/routing rules,
  and four provider guidance documents. This exception does not transfer
  semantic or behavioral ownership.
- **Key Dependencies**: Specs 026–029, official topic sources, Git history, link
  graph, generated-file ownership, and current audit findings.
- **Tech Stack**: `git mv`, focused manual edits, registry validation, link and
  owner checks, and official-source ledgers. No blind global rewrite.

Migration waves:

1. Stage 01–03 active PRD, architecture, ADR, and Spec documents.
2. Stage 04–05 active execution and operations documents.
3. Remaining Stage 00 authored governance/reference bodies plus the thirteen
   pre-registered Spec 027/031 handoff paths under a structural-only exception.
4. All remaining shape-debt non-README Stage 90 references and Stage 98
   traceability records.
5. AWS and Azure provider snapshots and executable example indexes.
6. Cross-link-only follow-ups in README indexes owned by Spec 028, followed by
   strict validation cutover and residual legacy search.

Tranche handoff is binding:

| Path or responsibility | Canonical change owner | This Spec's allowed interaction |
| --- | --- | --- |
| `docs/99.templates/support/**` and non-README forms | Spec 027 | Consume final contracts. Structural-only canonicalization is authorized for exactly `common-documentation-governance.md`, `documentation-contract.md`, `frontmatter-schema.md`, `legacy-cleanup-rules.md`, `sdlc-governance.md`, and `template-routing.md`; no route, schema, form, or governance-semantic change. |
| README forms and every tracked `README.md`, including `_workspace/README.md` | Spec 028 | Request or apply relocation-driven index/link rows only; no profile/body redesign. |
| Validator parser, rule semantics, and fixture engine | Spec 029 | Consume the public interface and change no parser or rule behavior. ADM-003 through ADM-006 may synchronize only the frozen migration-count/self-test constants in `validate-markdown-profiles.py` with the shrinking Spec-030-owned fixture; an executable line guard rejects every other validator edit. ADM-007 owns the separately named strict-mode cutover. |
| Root provider shims, `.agents/**`, `.claude/**`, `.codex/**`, shared role semantics | Spec 031 | Excluded from authored migration; link to canonical owners only. Structural-only canonicalization is authorized for exactly `docs/00.agent-governance/providers/{agents-md,claude,codex,gemini}.md`; no provider or agent behavior change. |
| CI selector blocks and validation obligations | Spec 031 | Excluded except link repair. |
| Action identities/permissions, GitOps, infrastructure, policy, secrets, Traefik machine surfaces | Spec 032 | Do not change behavior; migrate only their authored documentation after the protected owner confirms links. |
| Remaining non-README authored documents in Stages 00–05, 90, and 98 | Spec 030 | Full disposition and topic-content migration owner. |

The other three handoff exceptions are exactly
`docs/00.agent-governance/rules/documentation-protocol.md`,
`docs/00.agent-governance/rules/document-stage-routing.md`, and
`docs/00.agent-governance/rules/stage-authoring-matrix.md`. Together with the
six support and four provider paths above, these thirteen files may receive
only Frontmatter/section-order normalization, duplicate template-residue
removal, and link repair. Historical facts and all Spec 027/031-owned semantic,
route, schema, form, provider, agent, CI, and validation behavior remain
unchanged.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: The temporary working ledger is ignored under
  `_workspace`. Its reviewed, non-secret rows are promoted in full to the
  durable Current-pack owner
  `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`.
  The Stage 04 Task links that ledger and stores counts, decisions, commands,
  limitations, reviewer, and commit ranges. Every migrated current authored
  document has a durable research row with path, title, type, local evidence,
  official source URL, observed date/version, applicability, adopted or rejected
  guidance, section/content decision, and refresh trigger. Temporary rows may
  contain only the same non-secret fields and are disposable after promotion.
- **Migration / Transition Plan**: Inventory and compare before each wave,
  migrate one document family or scope cluster, validate, review, commit, and
  retain a rollback point before starting the next wave.

AWS and Azure migration rules:

- Merge unique, still-valid technical knowledge into dated provider snapshot
  references under `docs/90.references/cloud-examples/{aws,azure}/`.
- Revalidate technical claims against official provider documentation and label
  observation date, version boundary, and refresh trigger.
- Keep only executable manifests, configurations, and their implementation
  entrypoint README files under `examples/**`.
- Retire duplicate PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, and Runbook
  files; create Tombstones only where lineage or inbound references require it.

Research rules apply to every current authored document, not only cloud
snapshots. A document with external technology, standard, provider, security,
or operational claims requires at least one applicable official primary source
in addition to repository evidence. A purely repository-specific document uses
the type-format source from Spec 027 and records `external-topic: not applicable`
with a concrete reason. Historical `preserve` records are not rewritten to
current external facts; the ledger records their snapshot boundary and whether
any current-authority claim must be removed or rerouted.

## Interfaces & Data Structures

### Core Interfaces

```text
path | title | profile | owner-key | disposition | destination | local-evidence | official-sources | observed-version | applicability | content-decision | refresh-trigger | reviewer | result
```

The `owner-key` is the normalized role, scope, and lineage tuple used to reject
multiple current owners without treating historical snapshots as active.

## Edge Cases & Error Handling

- Preserve unique facts before deleting or merging a duplicate surface.
- Use `git mv` for relocations where one-to-one history exists; use merge plus
  Tombstone when multiple sources become one owner.
- Do not update historical commands merely because current tooling changed;
  repair only links or authority claims that incorrectly present them as current.
- Do not read or modify ignored `.env`, local settings, tokens, keys,
  certificates, shell history, kubeconfig, or diagnostic logs.
- Do not edit generated outputs directly; update their owner or generator.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Two sources contain incompatible, currently plausible facts.
- **Fallback**: Verify against repository evidence and official dated sources,
  record the boundary, and retain unresolved historical context without two
  current owners.
- **Human Escalation**: A conflict with an accepted ADR requires a superseding
  ADR decision rather than an undocumented content choice.

## Verification Commands

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root .
bash scripts/validate-repo-quality-gates.sh .
rg -n "harness-task-contract|SNIPPET LIBRARY|Suggested Types" docs examples .agents .claude .codex scripts
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Every approved baseline target Markdown path and every
  program-created target Markdown path has one profile or exception and strict
  mode has zero migration debt.
- **VAL-SPC-002**: Duplicate current owners, authored placeholders, template
  residue, unsupported sections, and broken internal links are zero.
- **VAL-SPC-003**: Example-local SDLC prose is zero; provider snapshots and
  executable example indexes account for every retained unique source.
- **VAL-SPC-004**: Preserved historical records retain their evidence meaning,
  and every destructive disposition has review and rollback evidence.
- **VAL-SPC-005**: Every migrated current authored document has a complete
  durable Stage 90 topic/title research row; external claims have applicable
  official sources, and repository-only decisions have a reviewed
  non-applicability reason. The ledger can be revalidated after `_workspace`
  scratch is removed.
- **VAL-SPC-006**: The tranche responsibility table has no uncoordinated
  multi-owner edit; README changes after relocation are link/index-only and
  provider/protected surfaces remain with Specs 031 and 032.

## Related Documents

- **Execution Plan**: [Authored Document Migration Implementation Plan](../../04.execution/plans/2026-07-12-authored-document-migration.md)
- **Execution Task**: [Authored Document Migration Task](../../04.execution/tasks/2026-07-12-authored-document-migration.md)
- **Validation Spec**: [Semantic Document Validation](../029-semantic-document-validation/spec.md)
- **Next Spec**: [Affected Surface and Agent QA](../031-affected-surface-agent-qa/spec.md)
- **ADR Practice**: [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- **Documentation Classification Aid**: [Diátaxis](https://diataxis.fr/)
