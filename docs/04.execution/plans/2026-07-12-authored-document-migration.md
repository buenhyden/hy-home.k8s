---
title: 'Authored Document Migration Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-12
---

# Authored Document Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the approved authored-document corpus to strict document
profiles while preserving historical evidence, consolidating duplicate cloud
documentation, and publishing durable per-document research decisions.

**Architecture:** Generate a read-only inventory from Spec 029, promote reviewed
rows to one durable Current research ledger, and migrate one ownership family at
a time. Every wave clears named compatibility debt, passes link/owner checks,
receives independent review, and ends at a rollback commit before the next wave.

**Tech Stack:** Markdown, YAML Frontmatter, Python 3 validators, Git and `git mv`,
official primary-source research, `rg`, pre-commit, and repository quality gates.

## Global Constraints

- Work only in the isolated worktree for branch `codex/workspace-document-assurance-modernization`.
- Baseline identity is commit `8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d` and its approved 433-Markdown target corpus; separately account for program-created documents.
- Allowed dispositions are exactly `preserve`, `transform`, `merge`, `relocate`, `tombstone`, and `delete`.
- Preserve completed Plan/Task evidence, accepted ADR history, dated audit/research facts, archive Tombstones, generated-owner boundaries, and provider-native metadata.
- Do not blindly rewrite files or replace topic-specific content with template prose.
- Every migrated current authored document needs one durable research row; external technical claims use applicable official primary sources.
- Repository-only decisions record `external-topic: not applicable` with a concrete reviewed reason.
- Do not read, enumerate, move, or delete ignored `.env`, token, key, certificate, kubeconfig, shell-history, local-setting, or diagnostic content.
- README redesign belongs to Spec 028; this Plan may make relocation-driven index/link updates only.
- Validators belong to Spec 029; this Plan consumes their public interfaces and changes only named migration-debt records at strict cutover.
- Protected machine surfaces and behavior belong to Spec 032; this Plan changes only their authored documentation and links.
- Use `apply_patch` for edits, `git mv` for one-to-one relocations, and a separate logical commit for every migration wave.

---

## Overview

This Plan implements Spec 030 in seven reviewable waves: execution-chain
startup, durable inventory, Stages 01–03, Stages 04–05, remaining governance and
reference bodies, AWS/Azure consolidation, and strict cutover.

## Context

The approved corpus contains five PRDs, five ARDs, eleven ADRs, twenty-nine
Stage 03 artifacts, forty-three Plans, forty-five Tasks, twenty-four Guide/
Policy/Runbook documents, thirty-five non-README Stage 90 documents, thirty-one
Archive Tombstones, and fifty-nine AWS/Azure example-local Markdown files.
Compatibility mode must stay available until these families are reconciled.

## Goals & In-Scope

- Apply profile-specific Frontmatter, status, section, and authority rules.
- Remove copied authoring instructions, duplicated sections, stale authority
  claims, broken links, and duplicate current owners.
- Preserve historical facts and destructive-change rollback evidence.
- Consolidate AWS/Azure prose into dated provider snapshots while keeping
  executable examples and implementation entrypoints.
- Enable strict document validation with zero migration debt.

## Non-Goals & Out-of-Scope

- Rewriting historical evidence for current style or technology versions.
- Changing Action identities, workflow permissions, agent roles/models,
  Kubernetes manifests, infrastructure behavior, policy behavior, secrets, or
  live cluster/Vault/Argo CD state.
- Creating a root `DESIGN.md`.

## File and Interface Map

| Unit | Files | Responsibility |
| --- | --- | --- |
| Durable evidence | `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md` | Full disposition, topic-source, content decision, reviewer, result, and refresh evidence. |
| Active design | `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**` | Current requirement, architecture, decision, and technical-contract content. |
| Execution and operations | `docs/04.execution/**`, `docs/05.operations/**` | Historical execution evidence and current operational guidance/control/procedure. |
| Governance and references | non-README `docs/00.agent-governance/**`, Current Stage 90, `docs/98.archive/**` | Canonical governance, current research, and historical/current authority boundaries. |
| Cloud snapshots | `docs/90.references/cloud-examples/{aws,azure}/2026-07-12-*-example-snapshot.md` | Dated official-source comparison and retained unique cloud-example knowledge. |
| Executable examples | `examples/{aws,azure}/**` excluding deleted `docs/**` | Executable Terraform/Bicep/Kubernetes/GitOps assets and entrypoint links. |
| Strict cutover | document profile registry debt records and `scripts/validate-repo-quality-gates.sh` | Remove compatibility debt and enforce strict repository validation. |

### Durable Ledger Interface

```text
path | title | profile | owner-key | disposition | destination | local-evidence | official-sources | observed-version | applicability | content-decision | refresh-trigger | reviewer | result
```

## Work Breakdown

| Task | Deliverable | Primary validation | Commit |
| --- | --- | --- | --- |
| ADM-001 | Reciprocal execution chain | Lineage assertion | `docs(execution): start authored document migration` |
| ADM-002 | Baseline disposition and research ledger | Inventory/ledger validation | `docs(migration): inventory authored document dispositions` |
| ADM-003 | Stage 01–03 normalization | Path-prefix compatibility checks | `docs(migration): normalize active sdlc design documents` |
| ADM-004 | Stage 04–05 normalization | Execution/operations compatibility checks | `docs(migration): normalize execution and operations documents` |
| ADM-005 | Governance/reference/archive normalization | Link, owner, and preserve-boundary checks | `docs(migration): normalize governance references and archive links` |
| ADM-006 | AWS/Azure consolidation | Zero example-local docs and valid snapshot links | `docs(migration): consolidate cloud example documentation` |
| ADM-007 | Strict cutover and closure | Strict validators, quality gate, all-files pre-commit | `chore(docs): cut over document profiles to strict validation` |

## Verification Plan

| ID | Level | Command | Pass criteria |
| --- | --- | --- | --- |
| VAL-030-001 | Inventory | `validate-links-and-owners.py --inventory --format json` | Every approved and program-created target is classified once. |
| VAL-030-002 | Wave | `validate-markdown-profiles.py --mode compatibility --path-prefix PATH` | Completed wave has no document debt. |
| VAL-030-003 | Research | strict link/owner validator | Every migrated current document has one complete durable row. |
| VAL-030-004 | Cloud | directory-based `git ls-files examples/aws/docs examples/azure/docs` source/ledger comparison | All 59 source paths have durable ledger rows before deletion; no example-local SDLC Markdown remains afterward. |
| VAL-030-005 | Strict | all three document validators in strict mode | Zero debt, unknown route, duplicate owner, incomplete ledger, or broken link. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical facts are silently modernized | High | Preserve bodies and change only incorrect current-authority routing. |
| Destructive consolidation loses unique content | High | Ledger source set, official comparison, independent review, and rollback commit precede deletion. |
| README ownership is violated | High | Limit README work to approved relocation-driven rows using Spec 028 forms. |
| Research rows become generic citations | High | Require applicability, adopted/rejected guidance, content decision, and refresh trigger per path. |
| One wave obscures unrelated changes | High | Stage only the exact family plus its ledger rows and execution evidence. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate:** Each wave clears its path-prefix debt and passes link/owner validation.
- **Sandbox / Canary Rollout:** Compatibility mode remains canonical through ADM-006.
- **Human Approval Gate:** Required before deletion, accepted-ADR supersession, remote push, merge, or protected/live changes.
- **Rollback Trigger:** Unique-content loss, historical evidence drift, duplicate current owner, incomplete research, or unresolved link regression.
- **Prompt / Model Promotion Criteria:** Not applicable; agent model changes are outside Spec 030.

---

### Task 1: Start Reciprocal Execution Lineage

**Files:**

- Modify: `docs/03.specs/030-authored-document-migration/spec.md`
- Modify: `docs/03.specs/README.md`
- Modify: `docs/04.execution/plans/2026-07-12-authored-document-migration.md`
- Modify: `docs/04.execution/plans/README.md`
- Create: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`
- Modify: `docs/04.execution/tasks/README.md`

**Interfaces:**

- Consumes: active Spec 030, completed Specs 026–029, and this Plan.
- Produces: Task IDs `ADM-001` through `ADM-007` and reciprocal execution lineage.

- [ ] **Step 1: Run RED lineage assertion**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
 Path('docs/03.specs/030-authored-document-migration/spec.md'),
 Path('docs/04.execution/plans/2026-07-12-authored-document-migration.md'),
 Path('docs/04.execution/tasks/2026-07-12-authored-document-migration.md'),
]
assert all(path.exists() for path in paths), paths
for source in paths:
    text = source.read_text(encoding='utf-8')
    for target in paths:
        if target != source:
            assert target.name in text, (source, target)
PY
```

Expected: FAIL because the execution Task and reciprocal links do not exist.

- [ ] **Step 2: Create the active Task and exact seven-row table**

Use the five canonical Frontmatter keys, `status: active`, and one row for every
`ADM-001` through `ADM-007` Work Breakdown item with its exact command and
commit message.

- [ ] **Step 3: Add reciprocal links and active index rows**

Update Spec, Plan, Task, and the three Stage indexes only. Preserve all unrelated
index order and content.

- [ ] **Step 4: Run GREEN lineage and focused QA**

```bash
python3 - <<'PY'
from pathlib import Path
paths = [Path('docs/03.specs/030-authored-document-migration/spec.md'), Path('docs/04.execution/plans/2026-07-12-authored-document-migration.md'), Path('docs/04.execution/tasks/2026-07-12-authored-document-migration.md')]
for source in paths:
    text = source.read_text(encoding='utf-8')
    assert source.exists()
    for target in paths:
        if target != source:
            assert target.name in text
PY
git diff --check
pre-commit run --files docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md
```

Expected: assertion and applicable hooks PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): start authored document migration"
```

---

### Task 2: Publish the Baseline Disposition and Research Ledger

**Files:**

- Create: `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`
- Modify: `docs/90.references/research/2026-07-07-wer/README.md`
- Modify: `docs/04.execution/tasks/2026-07-12-authored-document-migration.md`

**Interfaces:**

- Consumes: Spec 029 `--inventory --format json` output and Spec 027 type-to-source matrix.
- Produces: exact fourteen-column durable ledger consumed by strict cross-document validation.

- [ ] **Step 1: Generate ignored scratch inventory**

```bash
python3 scripts/validate-links-and-owners.py --root . --inventory --format json > _workspace/document-migration-inventory.json
python3 -m json.tool _workspace/document-migration-inventory.json >/dev/null
```

Expected: valid JSON and no tracked `_workspace` child.

- [ ] **Step 2: Run RED ledger validation**

```bash
python3 scripts/validate-links-and-owners.py --root . --mode strict
```

Expected: exit 1 with `LEDGER-MISSING` or `LEDGER-INCOMPLETE`.

- [ ] **Step 3: Create the durable ledger**

Use the common Reference profile and one table with exactly the fourteen
columns declared above. Add one row per inventory path. Each row names baseline
or program-created local evidence, disposition, destination, applicable
official source or reviewed non-applicability reason, content decision, refresh
trigger, reviewer, and initial `inventory-reviewed` result.

- [ ] **Step 4: Verify completeness and tracked boundary**

```bash
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
git ls-files _workspace
```

Expected: compatibility exit 0; tracked output is exactly `_workspace/README.md`.

- [ ] **Step 5: Commit**

```bash
git add docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/90.references/research/2026-07-07-wer/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md
git commit -m "docs(migration): inventory authored document dispositions"
```

---

### Task 3: Normalize Stage 01–03 Documents

**Files:**

- Modify: non-README Markdown under `docs/01.requirements/`
- Modify: non-README Markdown under `docs/02.architecture/requirements/`
- Modify: non-README Markdown under `docs/02.architecture/decisions/`
- Modify: `spec.md`, `agent-design.md`, `api-spec.md`, `data-model.md`, and `tests.md` under `docs/03.specs/`
- Modify: durable migration ledger

**Interfaces:**

- Consumes: final registry, templates, compatibility diagnostics, and ledger rows.
- Produces: debt-free current design documents without altering accepted-decision history.

- [ ] **Step 1: Capture RED diagnostics for the three path prefixes**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/01.requirements --format json > _workspace/stage01-debt.json
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/02.architecture --format json > _workspace/stage02-debt.json
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/03.specs --format json > _workspace/stage03-debt.json
```

Expected: valid JSON inventories; every reported item names an approved registry debt record.

- [ ] **Step 2: Build exact NUL-delimited family batches**

Generate ignored batch manifests from tracked files, never from a directory
argument passed to a formatter. Each manifest contains at most five exact paths
and is one 2–5 minute edit/validation checkpoint.

```bash
mkdir -p _workspace/adm-003-batches
git ls-files -z docs/01.requirements docs/02.architecture/requirements \
  | python3 -c 'import pathlib,sys; p=[x for x in sys.stdin.buffer.read().split(b"\0") if x and not x.endswith(b"/README.md")]; d=pathlib.Path("_workspace/adm-003-batches"); [(d / f"prd-ard-{i // 5 + 1:02d}.nul").write_bytes(b"\0".join(p[i:i+5]) + b"\0") for i in range(0, len(p), 5)]'
git ls-files -z docs/02.architecture/decisions docs/03.specs \
  | python3 -c 'import pathlib,sys; p=[x for x in sys.stdin.buffer.read().split(b"\0") if x and not x.endswith(b"/README.md")]; d=pathlib.Path("_workspace/adm-003-batches"); [(d / f"adr-spec-{i // 5 + 1:02d}.nul").write_bytes(b"\0".join(p[i:i+5]) + b"\0") for i in range(0, len(p), 5)]'
```

Expected: every owned non-README path occurs in exactly one NUL manifest.

- [ ] **Step 3: Transform PRD and ARD batches**

Apply exact key order and family state domain, retain topic-specific requirements,
merge duplicate opening intent, and move all upstream/downstream relationships
to the profile-owned Traceability section. For each `prd-ard-*.nul` manifest,
edit only those at-most-five paths, update their ledger rows, run the
compatibility validator on each exact path, and mark that 2–5 minute checkpoint
complete before opening the next manifest.

- [ ] **Step 4: Transform ADR and Spec batches**

Preserve accepted ADR decisions and consequences. Remove copied form guidance,
merge duplicate sections, correct contradictory current-owner links, and record
every content choice and official source in the ledger. Repeat the same
at-most-five-path checkpoint for each `adr-spec-*.nul` manifest; do not combine
manifests in one edit/review checkpoint.

- [ ] **Step 5: Run GREEN prefix validation**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/01.requirements
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/02.architecture
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/03.specs
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
```

Expected: no debt for the three completed prefixes and no broken/duplicate owner findings.

- [ ] **Step 6: Review and commit**

```bash
git diff --check
git ls-files -z docs/01.requirements docs/02.architecture docs/03.specs \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  | xargs -0 -r -n 5 pre-commit run --files
git add docs/01.requirements docs/02.architecture docs/03.specs \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md
git commit -m "docs(migration): normalize active sdlc design documents"
```

Expected: focused hooks PASS and commit contains only this wave plus evidence.

---

### Task 4: Normalize Stage 04–05 Documents

**Files:**

- Modify: non-README Markdown under `docs/04.execution/plans/`
- Modify: non-README Markdown under `docs/04.execution/tasks/`
- Modify: non-README Markdown under `docs/05.operations/guides/`
- Modify: non-README Markdown under `docs/05.operations/policies/`
- Modify: non-README Markdown under `docs/05.operations/runbooks/`
- Modify: canonical real incident/postmortem documents if they exist
- Modify: durable migration ledger

**Interfaces:**

- Consumes: Plan/Task/Guide/Policy/Runbook/Incident/Postmortem profiles.
- Produces: preserved execution facts and role-separated operational documents.

- [ ] **Step 1: Capture RED prefix diagnostics**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/04.execution --format json > _workspace/stage04-debt.json
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/05.operations --format json > _workspace/stage05-debt.json
```

Expected: valid JSON with only named migration debt.

- [ ] **Step 2: Build exact NUL-delimited execution/operations batches**

```bash
mkdir -p _workspace/adm-004-batches
git ls-files -z docs/04.execution/plans docs/04.execution/tasks \
  | python3 -c 'import pathlib,sys; p=[x for x in sys.stdin.buffer.read().split(b"\0") if x and not x.endswith(b"/README.md")]; d=pathlib.Path("_workspace/adm-004-batches"); [(d / f"execution-{i // 5 + 1:02d}.nul").write_bytes(b"\0".join(p[i:i+5]) + b"\0") for i in range(0, len(p), 5)]'
git ls-files -z docs/05.operations \
  | python3 -c 'import pathlib,sys; p=[x for x in sys.stdin.buffer.read().split(b"\0") if x and not x.endswith(b"/README.md")]; d=pathlib.Path("_workspace/adm-004-batches"); [(d / f"operations-{i // 5 + 1:02d}.nul").write_bytes(b"\0".join(p[i:i+5]) + b"\0") for i in range(0, len(p), 5)]'
```

Expected: every owned non-README path occurs once; every manifest has no more
than five paths and is handled as a separate 2–5 minute checkpoint.

- [ ] **Step 3: Preserve completed execution evidence batch by batch**

Keep historical commands, results, limitations, and unchecked historical
instructions. Remove copied `Working Rules`, `Suggested Types`, target comments,
and duplicate relationship sections; do not convert historical facts into
current requirements. Complete and validate one `execution-*.nul` manifest at a
time, updating the ledger before continuing.

- [ ] **Step 4: Separate operational roles batch by batch**

Keep Guides explanatory, Policies normative, Runbooks executable, Incidents
factual, and Postmortems causal/learning-oriented. Move duplicate content to one
owner and replace it with a relative link. Complete and validate one
`operations-*.nul` manifest at a time, updating the ledger before continuing.

- [ ] **Step 5: Run GREEN validation and commit**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/04.execution
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/05.operations
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
git diff --check
git ls-files -z docs/04.execution docs/05.operations \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  | xargs -0 -r -n 5 pre-commit run --files
git add docs/04.execution docs/05.operations \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md
git commit -m "docs(migration): normalize execution and operations documents"
```

Expected: completed prefixes have no debt and commit succeeds.

---

### Task 5: Normalize Governance, Current References, and Archive Links

**Files:**

- Modify: non-README authored Markdown under `docs/00.agent-governance/`, excluding Spec 027 template mirrors and Spec 031 provider gateways
- Modify: `docs/90.references/audits/2026-07-11-weia/*.md`
- Modify: `docs/90.references/research/2026-07-07-wer/*.md`
- Modify: `docs/90.references/data/*.md`
- Modify: `docs/90.references/learning/*.md`
- Modify: `docs/98.archive/**/*.md` only where authority/index links are wrong
- Modify: durable migration ledger

**Interfaces:**

- Consumes: governance/reference/archive profiles and historical-path exclusions.
- Produces: one current authority per role while retaining dated and archive evidence.

- [ ] **Step 1: Capture RED diagnostics for remaining owned prefixes**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/00.agent-governance --format json > _workspace/stage00-debt.json
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/90.references --format json > _workspace/stage90-debt.json
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/98.archive --format json > _workspace/stage98-debt.json
```

Expected: valid JSON and no unregistered debt.

- [ ] **Step 2: Build exact NUL-delimited governance/reference batches**

Generate ignored manifests of at most five tracked paths for the owned Stage 00,
Stage 90, and Stage 98 sets. Exclude README paths and the stated Spec 027/031
ownership exceptions while constructing the manifests. Treat each manifest as
one 2–5 minute edit, ledger, and compatibility-validation checkpoint.

```bash
mkdir -p _workspace/adm-005-batches
git ls-files -z docs/00.agent-governance docs/90.references docs/98.archive \
  | python3 -c 'import pathlib,sys; excluded={b"docs/00.agent-governance/rules/documentation-protocol.md",b"docs/00.agent-governance/rules/document-stage-routing.md",b"docs/00.agent-governance/rules/stage-authoring-matrix.md",b"docs/00.agent-governance/providers/agents-md.md",b"docs/00.agent-governance/providers/claude.md",b"docs/00.agent-governance/providers/codex.md",b"docs/00.agent-governance/providers/gemini.md"}; p=[x for x in sys.stdin.buffer.read().split(b"\0") if x and not x.endswith(b"/README.md") and x not in excluded]; d=pathlib.Path("_workspace/adm-005-batches"); [(d / f"governance-reference-{i // 5 + 1:02d}.nul").write_bytes(b"\0".join(p[i:i+5]) + b"\0") for i in range(0, len(p), 5)]'
```

Expected: the seven exact handoff-owned paths are absent; every remaining
candidate occurs once in a manifest of no more than five paths.

- [ ] **Step 3: Transform current governance and reference owners in batches**

Normalize sections and authority links in owned files. Preserve earlier dated
packs and record their snapshot boundary in the ledger without rewriting bodies.
Do not open a later manifest until all exact paths in the current manifest and
their ledger rows pass compatibility validation.

- [ ] **Step 4: Verify Tombstone preservation**

Ensure each Tombstone remains metadata-only, uses `status: archived`, links the
archive index, and does not regain the retired body.

- [ ] **Step 5: Run GREEN validation and commit**

```bash
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/00.agent-governance
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/90.references
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility --path-prefix docs/98.archive
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
git diff --check
git add docs/00.agent-governance docs/90.references docs/98.archive \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md
git commit -m "docs(migration): normalize governance references and archive links"
```

Expected: all owned prefixes pass and historical bodies remain preserved.

---

### Task 6: Consolidate AWS and Azure Documentation

**Files:**

- Create: `docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md`
- Create: `docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/README.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/aws/README.md`
- Modify link/index rows only: `docs/90.references/cloud-examples/azure/README.md`
- Modify link/index rows only: `examples/README.md`
- Modify link/index rows only: `examples/aws/README.md`
- Modify link/index rows only: `examples/azure/README.md`
- Delete: `examples/aws/docs/**`
- Delete: `examples/azure/docs/**`
- Modify: durable migration ledger

**Interfaces:**

- Consumes: Spec 028 README forms and the exact fifty-nine-file cloud source set.
- Produces: two dated provider snapshots, executable entrypoints, and zero example-local SDLC Markdown.

- [ ] **Step 1: Record RED source count and inbound links**

```bash
git ls-files -z examples/aws/docs examples/azure/docs > _workspace/cloud-doc-source-paths.nul
python3 -c 'import pathlib; p=[x for x in pathlib.Path("_workspace/cloud-doc-source-paths.nul").read_bytes().split(b"\0") if x]; print(len(p)); raise SystemExit(0 if len(p) == 59 else 1)'
rg -n 'examples/(aws|azure)/docs' README.md docs examples scripts tests > _workspace/cloud-doc-inbound-links.txt
```

Expected: source count `59`; the NUL file is the deletion review source of truth,
and the inbound-link file records every active relocation consumer.

- [ ] **Step 2: Build provider snapshots before deletion**

For each provider, record source files, retained unique knowledge, executable
asset mapping, official source URLs, observed date/version, applicable and
rejected guidance, refresh trigger, and authority boundary. Independent review
must confirm all 59 exact source paths have ledger rows and every `merge` or
`delete` row has a destination. Prove coverage before deletion:

```bash
python3 -c 'import pathlib,sys; paths=[x.decode() for x in pathlib.Path("_workspace/cloud-doc-source-paths.nul").read_bytes().split(b"\0") if x]; ledger=pathlib.Path("docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md").read_text(); missing=[p for p in paths if f"| `{p}` |" not in ledger]; print("\n".join(missing)); raise SystemExit(bool(missing) or len(paths) != 59)'
```

Expected: exit 0 with no missing path output.

- [ ] **Step 3: Update entrypoint and snapshot index rows**

Use the existing Spec 028 README profile sections. Change only inventory,
source-of-truth, and related-document links required by relocation.

- [ ] **Step 4: Delete the reviewed duplicate trees**

```bash
git rm -r examples/aws/docs examples/azure/docs
```

Expected: only the two documentation trees are staged for deletion; executable assets remain.

- [ ] **Step 5: Run GREEN cloud assertions**

```bash
test -z "$(git ls-files examples/aws/docs examples/azure/docs)"
python3 scripts/validate-markdown-profiles.py --root . --mode compatibility
python3 scripts/validate-links-and-owners.py --root . --mode compatibility
git diff --check
```

Expected: no tracked cloud-doc path, no broken links, and compatibility PASS.

- [ ] **Step 6: Commit**

```bash
git add docs/90.references/cloud-examples examples \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md
git commit -m "docs(migration): consolidate cloud example documentation"
```

---

### Task 7: Enable Strict Validation and Close Spec 030

**Files:**

- Modify: `docs/99.templates/support/document-profiles.json` only to remove completed Spec 030 debt records
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify: durable migration ledger
- Modify: Spec 030, this Plan, same-topic Task, their indexes, and `memory/progress.md`

**Interfaces:**

- Consumes: zero-debt migrated corpus and strict Spec 029 validators.
- Produces: strict repository quality gate and completed migration evidence.

- [ ] **Step 1: Run RED strict bundle before debt removal**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
```

Expected: any remaining failure identifies an exact path and rule; do not remove debt records until the underlying path passes.

- [ ] **Step 2: Remove only cleared migration-debt records and switch the wrapper to strict**

Change the three document-validator invocations in
`scripts/validate-repo-quality-gates.sh` from `compatibility` to `strict`.
Do not alter profile routes or semantics in this Task.

- [ ] **Step 3: Run GREEN strict and residue checks**

```bash
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
rg -n 'harness-task-contract|SNIPPET LIBRARY|Suggested Types' docs examples .agents .claude .codex scripts
bash scripts/validate-repo-quality-gates.sh .
git diff --check
pre-commit run --all-files
```

Expected: validators and required hooks PASS; residue search has no active-authority finding; optional skips are labeled.

- [ ] **Step 4: Close evidence and lifecycle**

Set Spec, Plan, and Task to `done`, update index rows, finish every ledger result
and reviewer field, record destructive rollback commits and review decisions,
and append the strict-cutover handoff to `memory/progress.md`.

- [ ] **Step 5: Commit**

```bash
git add docs/99.templates/support/document-profiles.json scripts/validate-repo-quality-gates.sh \
  docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md \
  docs/03.specs/030-authored-document-migration/spec.md docs/03.specs/README.md \
  docs/04.execution/plans/2026-07-12-authored-document-migration.md docs/04.execution/plans/README.md \
  docs/04.execution/tasks/2026-07-12-authored-document-migration.md docs/04.execution/tasks/README.md \
  docs/00.agent-governance/memory/progress.md
git commit -m "chore(docs): cut over document profiles to strict validation"
```

## Completion Criteria

- [ ] Every approved and program-created target has one profile or native exception.
- [ ] Every migrated current authored document has one complete durable research row.
- [ ] Duplicate current owners, template residue, unsupported sections, and broken links are zero.
- [ ] AWS/Azure example-local SDLC Markdown is zero and executable entrypoints resolve.
- [ ] Strict mode and the full repository QA bundle pass.

## Related Documents

- [Program PRD](../../01.requirements/005-workspace-document-assurance-modernization.md)
- [Operating Model ARD](../../02.architecture/requirements/0008-workspace-document-assurance-operating-model.md)
- [Authored Migration Spec](../../03.specs/030-authored-document-migration/spec.md)
- [Semantic Validation Plan](./2026-07-12-semantic-document-validation.md)
- [Affected Surface Spec](../../03.specs/031-affected-surface-agent-qa/spec.md)
