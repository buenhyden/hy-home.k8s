---
title: 'Workspace Document Contract Normalization Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
artifact_id: "PLAN-0014"
---

# Workspace Document Contract Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize active and historical workspace documents to the current frontmatter, section, template, README, CI/QA, and validator contracts while preserving historical evidence.

**Architecture:** Execute an audit-first documentation normalization in six logical commits. Contract sources are updated before authored documents, active SDLC documents are normalized before historical evidence, and validator changes are added only after the target shape is proven deterministic.

**Tech Stack:** Markdown with YAML frontmatter, Bash, embedded Python validator logic, GitHub Actions YAML, OpenAPI YAML, GraphQL SDL, proto3, `rg`, `jq`, and repository validation scripts.

---

## Overview

This plan implements
[Workspace Document Contract Normalization](spec.md).
It extends the prior workspace document governance hardening pass by applying
the current document contract to active documents and historical evidence.

The strategy is full normalization with evidence preservation. Historical
records may be edited to match current frontmatter and section contracts, but
old facts remain preserved in explicit historical, evidence, or superseded
sections.

## Context

The previous hardening pass aligned Stage 99 template support contracts,
provider entrypoints, README profile expectations, CI/QA documentation, and
validator coverage. This plan performs the broader application pass requested
by the user:

- Normalize every document type against its template.
- Clean duplicate or conflicting frontmatter keys and sections.
- Apply contract and governance changes back to templates and validators.
- Include historical evidence and archive material in the normalization scope.
- Keep SDLC content under `docs`.
- Use official or primary external sources for standards claims.
- Commit each logical task separately.

### Legacy Task ledger inputs

This document tracks implementation and verification work for workspace
document contract normalization. It keeps audit, contract, active document,
historical evidence, reference, CI/QA, validator, and final review work
traceable to the parent Spec and Plan.

- **Parent Spec**:
  [Workspace Document Contract Normalization Spec](spec.md)
- **Parent Plan**:
  [Workspace Document Contract Normalization Plan](plan.md)
## Goals & In-Scope

- **Goals**:
  - Produce a durable audit inventory for remaining document contract drift.
  - Normalize Stage 99 support contracts and template forms as the source of
    truth.
  - Apply frontmatter and section profiles to active SDLC documents.
  - Normalize historical evidence without deleting unique historical facts.
  - Align references, CI/QA, and formatting guidance with official sources and
    repo-local workflow behavior.
  - Reconcile validator coverage with the final contract shape.
- **In Scope**:
  - `_workspace`, `.github`, `docs/01.requirements`, `docs/02.architecture`,
    `docs/03.specs`, `docs/03.specs/plans`,
    `docs/03.specs/tasks`, `docs/05.operations`,
    `docs/90.references`, `docs/98.archive`, and `docs/99.templates`.
  - `scripts/validate-repo-quality-gates.sh` deterministic checks.
  - README indexes when folder content or profile language changes.
  - Progress ledger updates.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Introduce a new top-level docs taxonomy.
  - Replace the Stage 00 governance model.
  - Redesign GitOps runtime resources.
  - Add new product features or live cluster behavior.
- **Out of Scope**:
  - Live Kubernetes, Argo CD, Vault, cloud, paid service, or external provider
    mutation.
  - Secret value inspection.
  - Remote push, merge, or branch deletion until finishing flow.
  - CI trigger or branch protection changes unless separately approved.

### File Responsibility Map

| Surface | Responsibility in This Plan |
| --- | --- |
| `docs/90.references/audits/YYYY-MM-DD-workspace-document-contract-normalization-audit.md` | Durable inventory of drift classes and remediation routing. |
| `docs/99.templates/support/**` | Canonical contracts for frontmatter, routing, SDLC/common governance, and cleanup rules. |
| `docs/99.templates/templates/**` | Minimal document forms with consistent frontmatter, required sections, and native machine-contract exceptions. |
| `docs/01.requirements` through `docs/05.operations` | Active SDLC documents normalized to current route/profile/section contracts. |
| `docs/98.archive`, old Stage 04 records, audits, progress entries | Historical evidence normalized while preserving old facts in explicit historical sections. |
| `docs/90.references/{research,audits,data,llm-wiki,learning}` | Reference profile alignment, source boundaries, generated-index contracts, and freshness rules. |
| `.github`, `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`, `scripts/README.md`, `tests/README.md` | CI/QA and automation contract alignment. |
| `scripts/validate-repo-quality-gates.sh` | Deterministic validation of the final document contract shape. |
| `docs/03.specs/*`, `docs/03.specs/*`, `docs/00.agent-governance/memory/progress.md` | Execution evidence, status, and reusable memory. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Audit and inventory document contract drift. | `docs/90.references/audits/**`, task/progress | VAL-SPC-001, VAL-SPC-006 | Audit report lists drift classes and remediation routing; repo quality gate passes. |
| PLN-002 | Normalize support contracts and template forms. | `docs/99.templates/support/**`, `docs/99.templates/templates/**`, validator | VAL-SPC-001, VAL-SPC-006 | Support contracts, templates, and validator route/profile maps agree. |
| PLN-003 | Apply active SDLC document profiles. | `docs/01.requirements` to `docs/05.operations`, README indexes | VAL-SPC-002 | Active docs match frontmatter, section, route, and README contracts. |
| PLN-004 | Normalize historical evidence contracts. | `docs/98.archive`, old Stage 04 records, audits, progress | VAL-SPC-003 | Historical facts are preserved and separated from current instructions. |
| PLN-005 | Align references, CI/QA, and formatting contracts. | `docs/90.references/**`, `.github`, CI/QA docs, scripts/tests README | VAL-SPC-004, VAL-SPC-005 | Reference and automation docs match official sources and repo-local workflows. |
| PLN-006 | Reconcile final validator and governance gates. | `scripts/validate-repo-quality-gates.sh`, Stage 00/Stage 99 docs, plan/task/progress | VAL-SPC-006, VAL-SPC-007 | Full local validation and final subagent review pass. |

### Implementation Tasks

> [!NOTE]
> The unchecked items below preserve the approved historical execution
> instructions. The linked `status: done` Task is the completion-state and
> evidence owner; these boxes are not a current work queue.

### Task 1: Audit and Inventory Document Contract Drift

**Files:**

- Create: `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Capture repository status**

Run:

```bash
git status --short --branch
git rev-parse HEAD
```

Expected:

- Current branch is not `main`.
- Working tree is clean before the task starts.
- HEAD SHA is recorded in the task evidence.

- [ ] **Step 2: Inventory frontmatter profiles**

Run:

```bash
python3 - <<'PY'
import pathlib, re, yaml, collections
root = pathlib.Path('.')
rows = []
for path in sorted(root.glob('docs/**/*.md')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        rows.append((str(path), 'NO_FRONTMATTER', '', ''))
        continue
    data = yaml.safe_load(match.group(1)) or {}
    rows.append((str(path), data.get('type', ''), data.get('status', ''), ','.join(data.keys())))
for path, typ, status, keys in rows:
    print(f'{path}\t{typ}\t{status}\t{keys}')
PY
```

Expected:

- Output is captured or summarized in the audit report.
- README files without frontmatter are not treated as drift.

- [ ] **Step 3: Inventory section and residue drift**

Run:

```bash
rg -n "Use this[ ]template|Target:[ ]docs/|deprecated README heading|Related Folders|type:[ ]operations|owner:[ ]deprecated owner value|\\.claude/(hooks)|Security Without Hooks|Not yet supported|Key Differences|during the migration|after Phase|current and target|Phase [1-4]" \
  _workspace .github docs examples scripts tests 2>/dev/null || true
```

Expected:

- Matches are classified as active, historical, template starter, generated,
  or ignored local-only evidence.
- Active and historical drift classes are routed to Tasks 2 through 6.

- [ ] **Step 4: Inventory route and validator parity**

Run:

```bash
rg -n "Current Route Map|Template-Folder Mapping|required_stage_templates|template_expected_types|template_locations" \
  docs/99.templates docs/00.agent-governance scripts/validate-repo-quality-gates.sh
```

Expected:

- Audit records whether route/profile maps agree or identifies exact drift.

- [ ] **Step 5: Write the audit report**

Create `docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md` with these sections:

```markdown
---
title: 'Workspace Document Contract Normalization Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
---

# Workspace Document Contract Normalization Audit



### Legacy Task supplemental evidence

### Phase View

### Phase 1: Audit

- [x] T-001 Audit and inventory document contract drift.

### Phase 2: Contract Sources

- [x] T-002 Normalize support contracts and template forms.

### Phase 3: Active Documents

- [x] T-003 Apply active SDLC document profiles.

### Phase 4: Historical Evidence

- [x] T-004 Normalize historical evidence contracts.

### Phase 5: References and CI/QA

- [x] T-005 Align references, CI/QA, and formatting contracts.

### Phase 6: Final Validation

- [x] T-006 Reconcile final validator and governance gates.
## Overview

## Reference Type

## Authority Boundary

## Findings

## Remediation Routing

## Validation Evidence

## Review and Freshness

## Related Documents
```

Expected:

- Findings table includes drift category, affected path pattern, current state,
  target contract, task routing, and risk.
- Historical evidence normalization is explicitly in scope.

- [ ] **Step 6: Update indexes and evidence**

Update:

- `docs/90.references/audits/README.md` with the new audit row.
- The task record with T-001 evidence.
- `docs/00.agent-governance/memory/progress.md` with a progress entry.

- [ ] **Step 7: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md docs/90.references/audits/README.md docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(audit): Inventory document contract drift"
```

Expected:

- Both validation commands pass.
- Commit is created with only Task 1 files.

### Task 2: Contract and Template Normalization

**Files:**

- Modify: `docs/99.templates/support/documentation-contract.md`
- Modify: `docs/99.templates/support/frontmatter-schema.md`
- Modify: `docs/99.templates/support/template-routing.md`
- Modify: `docs/99.templates/support/sdlc-governance.md`
- Modify: `docs/99.templates/support/common-documentation-governance.md`
- Modify: `docs/99.templates/support/legacy-cleanup-rules.md`
- Modify: `docs/99.templates/templates/**`
- Modify as needed: `docs/00.agent-governance/rules/document-stage-routing.md`
- Modify as needed: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify as needed: `scripts/validate-repo-quality-gates.sh`
- Modify: task/progress evidence

- [ ] **Step 1: Compare support contracts to template forms**

Run:

```bash
rg -n "type: sdlc/|type: content/|type: governance/|title:|status:|owner:|updated:" docs/99.templates/support docs/99.templates/templates
rg -n "## Overview|## Related Documents|## Verification|## Success Criteria|## Review and Freshness|## Authority Boundary" docs/99.templates/templates
```

Expected:

- Each Markdown template has the frontmatter keys required by its type.
- README and progress templates remain frontmatter-free.
- Native OpenAPI, GraphQL, and proto templates remain native.

- [ ] **Step 2: Normalize template forms**

Apply these rules:

- Frontmatter key order is `title`, `type`, `status`, `owner`, `updated`.
- Template forms keep only starter structure and concise instructions.
- Reusable rules move to support contracts.
- The duplicate harness Task starter remained supplemental at this point, not
  a structural route; Spec 027 later retired it.
- Incident layout remains
  `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md`
  and `postmortem.md`.

- [ ] **Step 3: Normalize support contracts**

Update support docs so they explicitly define:

- SDLC profiles.
- Common documentation profiles.
- Machine-contract exceptions.
- README frontmatter-free rule.
- Historical evidence normalization rule.
- Legacy cleanup rule for current vs historical evidence separation.

Expected:

- No support doc treats a completed migration phase as current guidance.
- No support doc duplicates full README inventory content.

- [ ] **Step 4: Update deterministic validator profile maps**

If support or template profile maps changed, update
`scripts/validate-repo-quality-gates.sh` so expected types and routes match.

Run after changes:

```bash
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
```

Expected:

- Validator passes at current head.
- Failure messages mention path and drift class.

- [ ] **Step 5: Focused residue scans**

Run:

```bash
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md 2>/dev/null || true
rg -n "operations-template|type:[ ]operations|owner:[ ]deprecated owner value|deprecated README heading|Use this[ ]template|Target:[ ]docs/" docs README.md AGENTS.md CLAUDE.md GEMINI.md .agents .claude .codex scripts 2>/dev/null || true
rg -n "Phase [1-4]|during the migration|after Phase|current and target" docs/99.templates/support 2>/dev/null || true
```

Expected:

- Active contract matches are removed or justified.
- Template files may retain starter markers.
- Historical evidence is routed to Task 4 if not corrected here.

- [ ] **Step 6: Update evidence and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/99.templates docs/00.agent-governance/rules scripts/validate-repo-quality-gates.sh docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(templates): Normalize document contract profiles"
```

Expected:

- Commit contains contract/template/validator changes and evidence only.

### Task 3: Active SDLC Document Application

**Files:**

- Modify: `docs/01.requirements/**`
- Modify: `docs/02.architecture/**`
- Modify: `docs/03.specs/**`
- Modify: `docs/03.specs/**`
- Modify: `docs/03.specs/**`
- Modify: `docs/05.operations/**`
- Modify as needed: related README indexes
- Modify: task/progress evidence

- [ ] **Step 1: Generate active document candidate list**

Run:

```bash
find docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs/plans docs/03.specs/tasks docs/05.operations -type f -name '*.md' | sort
```

Expected:

- List excludes `docs/98.archive`.
- README files are identified separately from authored documents.

- [ ] **Step 2: Apply frontmatter profiles**

For each non-README Markdown file in active SDLC stages:

- Match path to `docs/99.templates/support/template-routing.md`.
- Apply expected `type`.
- Keep only required keys unless the support schema explicitly allows more.
- Normalize key order to `title`, `type`, `status`, `owner`, `updated`.

Run after edits:

```bash
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs/plans docs/03.specs/tasks docs/05.operations
```

Expected:

- Non-README authored docs expose consistent frontmatter.
- README files remain frontmatter-free.

- [ ] **Step 3: Apply required sections**

Compare each document family to its template:

- PRD: `prd.template.md`
- AD: `ad.template.md`
- ADR: `adr.template.md`
- Spec and helper specs: `spec.template.md`, `interface.template.md`,
  `agent-design.template.md`, `data-model.template.md`, `tests.template.md`
- Plan: `plan.template.md`
- Task: `task.template.md`
- Operations: `guide.template.md`, `policy.template.md`,
  `runbook.template.md`, `incident.template.md`, `postmortem.template.md`

Expected:

- Required sections are present or intentionally merged under equivalent
  current-contract headings documented in Task evidence.
- Template instructions are not copied into authored docs.

- [ ] **Step 4: Resolve spec/tests/runbook contradictions**

Run:

```bash
rg -n "tests?\\.md|runbook|Verification|Validation|Rollback|Recovery|Success Criteria|Acceptance Criteria|current contract|superseded" docs/03.specs docs/05.operations/runbooks docs/03.specs
```

Expected:

- Test design belongs in Stage 03 helper test specs or Stage 04 task evidence.
- Executable recovery steps belong in runbooks.
- Plans own execution order and risk, not operational procedures.

- [ ] **Step 5: Update README indexes**

For every folder whose contents or document status changed, update its
`README.md` index row and link basis only. Do not add new README contract
bodies.

Run:

```bash
rg -n "^## Link Basis$|^## Related Documents$|^---$" -g 'README.md' docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs docs/05.operations
```

Expected:

- README files contain canonical sections and no frontmatter.

- [ ] **Step 6: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/01.requirements docs/02.architecture docs/03.specs docs/03.specs docs/05.operations docs/00.agent-governance/memory/progress.md
git commit -m "docs(sdlc): Apply active document profiles"
```

Expected:

- Active SDLC normalization passes repository gates.

### Task 4: Historical Evidence Normalization

**Files:**

- Modify: `docs/98.archive/**`
- Modify: older `docs/03.specs/**`
- Modify: older `docs/03.specs/**`
- Modify: `docs/90.references/audits/**`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify as needed: archive and audit README indexes

- [ ] **Step 1: Classify historical surfaces**

Run:

```bash
find docs/98.archive docs/90.references/audits docs/03.specs/plans docs/03.specs/tasks -type f -name '*.md' | sort
```

Expected:

- Historical and current Stage 04 records are classified before edits.
- Current plan/task files for this work remain active evidence, not historical
  evidence.

- [ ] **Step 2: Normalize archive Tombstones**

For `docs/98.archive/**/*.md`:

- Use `type: content/archive-tombstone`.
- Use `status: archived`.
- Preserve old document identity and archive reason.
- Do not reintroduce obsolete docs into active indexes.

Run:

```bash
rg -n "type: content/archive-tombstone|status: archived|## Historical Context|## Evidence|## Related Documents" docs/98.archive
```

Expected:

- Archive files have current frontmatter and evidence sections.

- [ ] **Step 3: Normalize old plans and tasks**

For old Stage 04 records:

- Preserve execution evidence.
- Move obsolete commands or old current-state claims under `Historical Context`
  or `Superseded Contract` when they conflict with current contracts.
- Keep active Stage 04 documents English-first.

Run:

```bash
rg -n "current and target|during the migration|after Phase|\\.claude/(hooks)|deprecated README heading|type:[ ]operations" docs/03.specs/plans docs/03.specs/tasks
```

Expected:

- Remaining matches are either removed, current-contract accurate, or labeled
  as historical evidence.

- [ ] **Step 4: Normalize audit and progress evidence**

For audit and progress records:

- Preserve chronological evidence.
- Add current/historical separation where old instructions would otherwise be
  mistaken for current rules.
- Do not rewrite unique evidence into false current claims.

Run:

```bash
rg -n "deprecated README heading|\\.claude/(hooks)|Use this[ ]template|Target:[ ]docs/|type:[ ]operations|owner:[ ]deprecated owner value" docs/90.references/audits docs/00.agent-governance/memory/progress.md
```

Expected:

- Remaining matches are clearly historical evidence or template context.

- [ ] **Step 5: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/98.archive docs/03.specs/plans docs/03.specs/tasks docs/90.references/audits docs/00.agent-governance/memory/progress.md
git commit -m "docs(archive): Normalize historical evidence contracts"
```

Expected:

- Historical normalization passes repository gates.

### Task 5: References, CI/QA, and Formatting Alignment

**Files:**

- Modify: `docs/90.references/research/**`
- Modify: `docs/90.references/data/**`
- Modify: `docs/90.references/llm-wiki/**`
- Modify: `docs/90.references/learning/**`
- Modify: `.github/**`
- Modify: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`
- Modify: `scripts/README.md`
- Modify: `tests/README.md`
- Modify as needed: `scripts/validate-repo-quality-gates.sh`
- Modify: task/progress evidence

- [ ] **Step 1: Reconcile reference profiles**

Run:

```bash
find docs/90.references -type f -name '*.md' | sort
rg -n "## Reference Type|## Authority Boundary|## Sources|## Review and Freshness|## Related Documents|type: content/reference" docs/90.references
```

Expected:

- Reference docs expose reference type, authority boundary, source/freshness
  rules, and related links.
- Generated LLM wiki remains generated-index content.

- [ ] **Step 2: Refresh official-source basis**

Use only official or primary sources for standards claims:

- GitHub Actions documentation and workflow syntax.
- SLSA provenance.
- OpenSSF Scorecard.
- CommonMark.
- YAML 1.2.2.
- OpenAPI Specification.
- GraphQL Specification.
- Protocol Buffers proto3 guide.
- GitHub Spec Kit documentation.
- OWASP SAMM.

Expected:

- Any new or changed external claim includes a source link.
- No broad market-scan claim is added without source support.

- [ ] **Step 3: Compare CI/QA docs with workflows and scripts**

Run:

```bash
sed -n '1,240p' .github/workflows/ci.yml
sed -n '1,220p' .github/ABOUT.md
sed -n '1,240p' docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md
sed -n '1,240p' scripts/README.md
sed -n '1,200p' tests/README.md
```

Expected:

- `ci.yml` is documented as the required QA gate.
- `generate-changelog.yml`, `labeler.yml`, `greetings.yml`, and `stale.yml`
  are documented as maintenance or release-evidence automation, not QA gates.
- Local equivalents for repo-quality and manifest-static checks are accurate.

- [ ] **Step 4: Align formatting and native contracts**

Run:

```bash
rg -n "CommonMark|Markdown|YAML|OpenAPI|GraphQL|protobuf|proto3|formatting|frontmatter" docs/90.references docs/99.templates .github docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md
```

Expected:

- Markdown formatting claims reference CommonMark/GitHub Markdown only where
  appropriate.
- YAML frontmatter claims are compatible with YAML 1.2.2.
- Native machine contract templates are not converted to Markdown.

- [ ] **Step 5: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/90.references .github docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md scripts/validate-repo-quality-gates.sh docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records docs/00.agent-governance/memory/progress.md
git commit -m "docs(qa): Align references and CI QA contracts"
```

Expected:

- Reference, CI/QA, and formatting alignment passes repository gates.

### Task 6: Final Validator and Governance Reconciliation

**Files:**

- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify as needed: `docs/00.agent-governance/**`
- Modify as needed: `docs/99.templates/**`
- Modify: `docs/03.specs/0014-workspace-document-contract-normalization/plan.md`
- Modify: `docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [x] **Step 1: Re-run final drift scans**

Run:

```bash
rg -n "Use this[ ]template|Target:[ ]docs/|deprecated README heading|Related Folders|type:[ ]operations|owner:[ ]deprecated owner value|\\.claude/(hooks)|Security Without Hooks|Not yet supported|Key Differences|during the migration|after Phase|current and target|Phase [1-4]" \
  _workspace .github docs examples scripts tests .agents .claude .codex 2>/dev/null || true
rg -n "^---$" -g 'README.md' README.md .github docs examples scripts tests .agents .claude .codex 2>/dev/null || true
```

Expected:

- Remaining matches are templates, native examples, generated files, or
  explicitly historical evidence.
- README frontmatter scan returns no active drift.

- [x] **Step 2: Add final deterministic validator checks**

Only add checks proven deterministic by Tasks 1 through 5. Candidate checks:

- Active and historical document profile conformance by path.
- README frontmatter absence.
- README canonical section headings.
- Template residue absence outside templates and explicit historical evidence.
- Stage 99 route/support/validator parity.
- Native machine-contract exceptions.

Expected:

- Checks are path-scoped.
- Failure messages name path and drift class.
- Historical evidence is not falsely rejected after normalization.

- [x] **Step 3: Run full validation bundle**

Run:

```bash
git diff --check
bash -n scripts/validate-repo-quality-gates.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json
```

If GitOps, infrastructure, policy, examples YAML, tests, or Traefik files were
changed, also run:

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

Expected:

- Required commands pass.
- Optional tool skips are recorded as limitations.

- [x] **Step 4: Request final independent review**

Dispatch a read-only reviewer with this brief:

```text
Review the workspace document contract normalization branch. Verify that:
1. The implementation satisfies docs/03.specs/0014-workspace-document-contract-normalization/spec.md.
2. Stage 99 support contracts, templates, Stage 00 governance docs, and scripts/validate-repo-quality-gates.sh agree.
3. Active SDLC docs and historical evidence follow the current frontmatter, section, and template contracts.
4. Historical facts remain preserved and are separated from current instructions.
5. README files are frontmatter-free and do not duplicate support/governance bodies.
6. References, CI/QA docs, and formatting claims match official sources and repo-local workflows.
7. git diff --check and bash scripts/validate-repo-quality-gates.sh . pass.
Return READY or list findings with file/line references.
```

Expected:

- Reviewer returns READY or all findings are fixed and re-reviewed.

- [x] **Step 5: Complete evidence and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add scripts/validate-repo-quality-gates.sh docs/00.agent-governance docs/99.templates docs/03.specs/0014-workspace-document-contract-normalization/plan.md docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records
git commit -m "docs(validation): Reconcile document governance gates"
```

Expected:

- Final reconciliation commit is created.
- Plan and task evidence mark all tasks complete.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Diff hygiene | `git diff --check` | No output and exit 0. |
| VAL-PLN-002 | Syntax | Repository gate syntax | `bash -n scripts/validate-repo-quality-gates.sh` | No output and exit 0. |
| VAL-PLN-003 | Repository | Document, workflow, script, and template gates | `bash scripts/validate-repo-quality-gates.sh .` | Prints `[PASS] repository quality gates passed`. |
| VAL-PLN-004 | Harness | Full repo-static harness validation | `bash scripts/validate-harness.sh` | Prints `PASS harness repo-static validation`; optional tool skips are recorded. |
| VAL-PLN-005 | Runtime config syntax | JSON/TOML/YAML touched-surface syntax | `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` and YAML/TOML parser checks when touched | Exit 0. |
| VAL-PLN-006 | Historical evidence | Current vs historical separation | Focused `rg` scans from Task 6 | Remaining legacy strings are labeled historical, template starter, or generated evidence. |
| VAL-PLN-007 | Review | Final independent review | Subagent reviewer brief in Task 6 | READY or all findings fixed and re-reviewed. |

### Legacy Task verification evidence

- **Required Commands**:
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Conditional Commands**:
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-policy-gates.sh .`
- **Review Evidence**:
  - Spec compliance reviewer result after each task.
  - Code quality reviewer result after each task.
  - Final independent reviewer result for the full branch.

### Execution Evidence

### T-001 Audit and Inventory Document Contract Drift

Status: Done.

Evidence:

- Added the dated audit report:
  [Workspace Document Contract Normalization Audit](../../90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md).
- Updated the audit report index in
  [Audit References README](../../90.references/audits/README.md).
- Focused docs Markdown inventory counted 206 Markdown files, 181 authored
  frontmatter documents, 23 README files, 2 intentional common-template
  frontmatter-free exceptions, and 32 archive Tombstones.
- `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` were recorded as active frontmatter-free repository
  surfaces that need explicit contract treatment in T-002 or T-005.
- Read-only subagent cross-check found no validator-blocking drift and added
  three follow-up routes: scripts README count drift, coverage wording
  boundary drift, and resolved prior-audit findings that need historical
  framing.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.

### T-002 Normalize Support Contracts and Template Forms

Status: Done.

Evidence:

- Clarified `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` as frontmatter-free GitHub-native control Markdown in
  template support contracts, Stage 00 routing rules, and the repository
  quality gate.
- Extended reference template/support vocabulary with
  `dated-implementation-audit`, `data-catalog`, and `source-ledger` so new
  Stage 90 reference documents match observed repository usage.
- Clarified incident record routing: the incident file must live under
  `docs/05.operations/incidents/YYYY/INC-###-<title>/` and its filename must
  match the incident folder; `postmortem.md` remains in the same folder.
- Clarified that `docs/00.agent-governance/memory/<topic>.md` excludes the
  reserved `progress.md` route.
- Documented the required-heading extraction algorithm: literal `##`
  template headings are required unless they contain placeholders or are
  marked optional or if-applicable.
- Updated `docs/00.agent-governance/hooks/k8s-pre-edit.sh` so mismatched
  incident folder/file IDs produce an early route note instead of a misleading
  incident-template classification.
- Added official GitHub source links for PR template and security policy
  GitHub-native Markdown behavior.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Pre-edit hook simulation for
  `docs/05.operations/incidents/2026/INC-001-demo/INC-002-other.md` emitted a
  route note that the incident filename must match the folder.
- Focused flat-template route scan — PASS.
- Focused support stale migration wording scan — PASS.
- Broad legacy residue scan found only historical Stage 04/progress evidence
  and template starter markers, not current support-contract drift.

### T-003 Apply Active SDLC Document Profiles

Status: Done.

Evidence:

- Updated the parent spec so active repository-control Markdown under
  `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and
  `.github/SECURITY.md` is modeled as a frontmatter-free GitHub-native control
  surface instead of a missing authored-document profile.
- Added `repository-control` evidence and `control` validator scope to the
  document contract profile model used by the spec.
- Updated the Operations README and Incidents README so active authoring
  guidance requires incident records to use
  `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` and
  postmortems to use `postmortem.md` in the same incident folder.
- Confirmed the repository has no tracked incident record files that need live
  path migration in this task.
- Rechecked the official GitHub pull request template and security policy docs
  while preserving `.github` control Markdown as frontmatter-free.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Focused active-rule scan for GitHub-native control Markdown,
  `repository-control`, and incident folder/file equality terms — PASS.

### T-004 Normalize Historical Evidence Contracts

Status: Done.

Evidence:

- Added a resolution overlay to the 2026-07-03 workspace document governance
  hardening audit so dated README heading, README delimiter, CI/QA hook-path,
  and provider traceability findings remain preserved as baseline evidence
  without reading as current drift.
- Updated the 2026-07-03 audit checklist statuses from pending remediation
  labels to resolved historical-item labels where current scans and later task
  evidence show the drift is closed.
- Updated the audit index to mark the 2026-07-03 audit as a resolved snapshot.
- Added a resolution overlay to the 2026-07-04 normalization audit and marked
  completed T-002/T-003/T-004 checklist items done while keeping T-005 and
  T-006 pending.
- Clarified archive Tombstone interpretation in the archive README and common
  documentation governance: Tombstones and archive index rows are historical
  evidence, while current replacements own active contracts.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Deprecated README related-heading scan across active surfaces — PASS with no
  matches.
- Active CI/QA hook-path drift scan over `tests/README.md`, the CI/CD QA
  guide, and `scripts/README.md` — PASS with no matches.
- Focused README metadata scan over representative README files — PASS with no
  matches.
- Incident record inventory under `docs/05.operations/incidents` — no tracked
  incident records requiring migration.

### T-005 Align References, CI/QA, and Formatting Contracts

Status: Done.

Evidence:

- Reconciled `scripts/README.md` with the current tracked script inventory:
  eight `scripts/*.sh` files, including `validate-harness.sh`, are present and
  retained.
- Aligned coverage wording across the CI/CD QA guide, `tests/README.md`, and
  `.github/PULL_REQUEST_TEMPLATE.md`: future testable application code keeps
  the 90% target where applicable, while Bash/YAML/Markdown infrastructure
  changes use validation-matrix evidence instead of application coverage
  claims.
- Refreshed the Stage 90 spec/SDLC/CI/QA/formatting research reference with
  official GitHub Actions workflow syntax/events, CommonMark 0.31.2, YAML
  1.2.2, and pre-commit sources checked on 2026-07-04.
- Updated the research README index to show the refreshed CI/formatting source
  basis.
- Updated the 2026-07-04 normalization audit so scripts inventory, coverage
  wording, and CI/QA official-source alignment are marked done in T-005.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- Script inventory scan found eight tracked `scripts/*.sh` files.
- Focused stale scan for the old seven-script wording, old coverage wording,
  and old pending T-005 marker — PASS with no matches.
- Focused source/coverage scan confirmed GitHub Actions workflow syntax,
  CommonMark 0.31.2, YAML 1.2.2, pre-commit, and coverage boundary terms are
  present on the intended reference and CI/QA surfaces.

### T-006 Reconcile Final Validator and Governance Gates

Status: Done.

Evidence:

- Re-ran the final validation bundle after T-001 through T-005 and confirmed
  no additional deterministic validator changes were needed beyond the
  contract/profile checks already added earlier in this branch.
- `bash scripts/validate-harness.sh` passed the repo-static bundle:
  repository quality gates, GitOps structure, Kubernetes manifest syntax,
  secret handling, policy gates, static infrastructure contracts, and diff
  hygiene.
- Broad Task 6 drift scan still returns expected historical plans/tasks,
  progress ledger evidence, template starter markers, generated validator
  literals, and example migration phases; repo-quality gates pass and README
  frontmatter scan returned no matches.
- Final independent reviewer `019f2a3e-0dd4-7292-95cb-9da3038e30f3` reported
  no blocking correctness, security, scope-control, template-route,
  frontmatter, or section-contract issues. The reviewer found only stale T-006
  completion tracking, which this entry and the companion audit/index updates
  resolve.
- Remote GitHub Actions run status was not inspected; this task records
  repo-static validation only.

Validation:

- `git diff --check` — PASS.
- `bash -n scripts/validate-repo-quality-gates.sh` — PASS.
- `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- `bash scripts/validate-harness.sh` — PASS.
- `jq empty .agents/hooks.json .claude/settings.json .codex/hooks.json` —
  PASS.
- `bash infrastructure/tests/verify-contracts-static.sh` — PASS.
- Task 6 README frontmatter scan — PASS with no matches.
- Optional local tooling limitation: `kube-linter` was not installed and was
  skipped by `validate-k8s-manifests.sh`; `conftest` was not installed and
  `validate-policy-gates.sh` used the built-in fallback.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence loses meaning during normalization. | High | Preserve old facts in explicit `Historical Context`, `Evidence`, or `Superseded Contract` sections. |
| Validator false positives block valid historical or generated docs. | High | Normalize documents first; add only path-scoped deterministic checks with documented exceptions. |
| Large diffs become hard to review. | Medium | Keep six logical commits and run spec/quality reviews after every task. |
| README files become contract duplicates. | Medium | Keep README updates to overview, index, link basis, and related documents. |
| External standards drift while implementation is in progress. | Medium | Use official/current links and record source refresh date in reference docs. |
| CI/QA docs overclaim deployment automation. | Medium | Treat `.github/workflows/ci.yml` and local scripts as repo-local source of truth; document non-QA workflows separately. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, `bash -n scripts/validate-repo-quality-gates.sh`, `bash scripts/validate-repo-quality-gates.sh .`, focused drift scans, and final subagent review.
- **Sandbox / Canary Rollout**: Not applicable; this is repo-static documentation and validator work.
- **Human Approval Gate**: Required before push, merge, live runtime action, CI trigger changes, secret handling changes, or branch cleanup.
- **Rollback Trigger**: Revert the logical task commit that introduced a validator false positive, broken link, or contract contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable; provider prompts and agent surfaces are documentation contracts, not model promotion artifacts, unless a later task touches them explicitly.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `T-001 through T-006` is limited to these Workspace Document Contract Normalization owners and Task-Table surfaces:
  - `docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records`
  - `docs/03.specs/0014-workspace-document-contract-normalization/spec.md`
  - `docs/03.specs/0014-workspace-document-contract-normalization/plan.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Workspace Document Contract Normalization work items and linked evidence owners.
- **Approval Required**: Human approval is required before Workspace Document Contract Normalization protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Workspace Document Contract Normalization outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `git diff --check`
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-harness.sh`
- **Live Validation**: DEFER — Workspace Document Contract Normalization is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Workspace Document Contract Normalization; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Document Contract Normalization change set for `T-001 through T-006` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Document Contract Normalization evidence remains in:
  - `docs/03.specs/0014-workspace-document-contract-normalization/README.md#task-records`
  - `docs/03.specs/0014-workspace-document-contract-normalization/spec.md`
  - `docs/03.specs/0014-workspace-document-contract-normalization/plan.md`
  - `.github/ABOUT.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`
## Completion Criteria

- [x] Audit inventory completed and indexed.
- [x] Stage 99 support contracts and templates normalized.
- [x] Active SDLC documents normalized.
- [x] Historical evidence normalized and preserved.
- [x] References, CI/QA, and formatting guidance aligned.
- [x] Final validator gates reconciled.
- [x] Full local validation bundle passed.
- [x] Final independent review returned no blocking findings after stale
  tracking fix.
- [x] Branch is ready for a separate finishing flow; no push, merge, or branch
  cleanup was performed in this validation commit.

## Traceability

- **Spec**: [Workspace Document Contract Normalization Spec](spec.md)
- **Tasks**: [Workspace Document Contract Normalization Tasks](README.md#task-records)
- **Template Routing Contract**: [Template Routing](../../99.templates/support/document-contract.md)
- **Frontmatter Schema**: [Frontmatter Schema](../../99.templates/support/document-contract.md)
- **Documentation Contract**: [Template Documentation Contract](../../99.templates/support/document-contract.md)
- **CI/QA Guide**: [CI/CD and QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)

### Legacy Task traceability

- **Spec**:
  [Workspace Document Contract Normalization Spec](spec.md)
- **Plan**:
  [Workspace Document Contract Normalization Plan](plan.md)
- **Template Routing Contract**:
  [Template Routing](../../99.templates/support/document-contract.md)
- **Frontmatter Schema**:
  [Frontmatter Schema](../../99.templates/support/document-contract.md)
