---
title: 'Workspace Document Contract Normalization Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-07-04
---

# Workspace Document Contract Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize active and historical workspace documents to the current frontmatter, section, template, README, CI/QA, and validator contracts while preserving historical evidence.

**Architecture:** Execute an audit-first documentation normalization in six logical commits. Contract sources are updated before authored documents, active SDLC documents are normalized before historical evidence, and validator changes are added only after the target shape is proven deterministic.

**Tech Stack:** Markdown with YAML frontmatter, Bash, embedded Python validator logic, GitHub Actions YAML, OpenAPI YAML, GraphQL SDL, proto3, `rg`, `jq`, and repository validation scripts.

---

## Overview

This plan implements
[Workspace Document Contract Normalization](../../03.specs/014-workspace-document-contract-normalization/spec.md).
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
    `docs/03.specs`, `docs/04.execution/plans`,
    `docs/04.execution/tasks`, `docs/05.operations`,
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

## File Responsibility Map

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
| `docs/04.execution/plans/*`, `docs/04.execution/tasks/*`, `docs/00.agent-governance/memory/progress.md` | Execution evidence, status, and reusable memory. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Audit and inventory document contract drift. | `docs/90.references/audits/**`, task/progress | VAL-SPC-001, VAL-SPC-006 | Audit report lists drift classes and remediation routing; repo quality gate passes. |
| PLN-002 | Normalize support contracts and template forms. | `docs/99.templates/support/**`, `docs/99.templates/templates/**`, validator | VAL-SPC-001, VAL-SPC-006 | Support contracts, templates, and validator route/profile maps agree. |
| PLN-003 | Apply active SDLC document profiles. | `docs/01.requirements` to `docs/05.operations`, README indexes | VAL-SPC-002 | Active docs match frontmatter, section, route, and README contracts. |
| PLN-004 | Normalize historical evidence contracts. | `docs/98.archive`, old Stage 04 records, audits, progress | VAL-SPC-003 | Historical facts are preserved and separated from current instructions. |
| PLN-005 | Align references, CI/QA, and formatting contracts. | `docs/90.references/**`, `.github`, CI/QA docs, scripts/tests README | VAL-SPC-004, VAL-SPC-005 | Reference and automation docs match official sources and repo-local workflows. |
| PLN-006 | Reconcile final validator and governance gates. | `scripts/validate-repo-quality-gates.sh`, Stage 00/Stage 99 docs, plan/task/progress | VAL-SPC-006, VAL-SPC-007 | Full local validation and final subagent review pass. |

## Implementation Tasks

### Task 1: Audit and Inventory Document Contract Drift

**Files:**
- Create: `docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md`
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

Create `docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md` with these sections:

```markdown
---
title: 'Workspace Document Contract Normalization Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-04
---

# Workspace Document Contract Normalization Audit

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
git add docs/90.references/audits/2026-07-04-workspace-document-contract-normalization-audit.md docs/90.references/audits/README.md docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md docs/00.agent-governance/memory/progress.md
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
- `harness-task-contract.template.md` remains supplemental, not a structural
  route for `docs/04.execution/tasks/*.md`.
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
git add docs/99.templates docs/00.agent-governance/rules scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(templates): Normalize document contract profiles"
```

Expected:

- Commit contains contract/template/validator changes and evidence only.

### Task 3: Active SDLC Document Application

**Files:**
- Modify: `docs/01.requirements/**`
- Modify: `docs/02.architecture/**`
- Modify: `docs/03.specs/**`
- Modify: `docs/04.execution/plans/**`
- Modify: `docs/04.execution/tasks/**`
- Modify: `docs/05.operations/**`
- Modify as needed: related README indexes
- Modify: task/progress evidence

- [ ] **Step 1: Generate active document candidate list**

Run:

```bash
find docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution/plans docs/04.execution/tasks docs/05.operations -type f -name '*.md' | sort
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
rg -n "^---$|^title:|^type:|^status:|^owner:|^updated:" docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution/plans docs/04.execution/tasks docs/05.operations
```

Expected:

- Non-README authored docs expose consistent frontmatter.
- README files remain frontmatter-free.

- [ ] **Step 3: Apply required sections**

Compare each document family to its template:

- PRD: `prd.template.md`
- ARD: `ard.template.md`
- ADR: `adr.template.md`
- Spec and helper specs: `spec.template.md`, `api-spec.template.md`,
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
rg -n "tests?\\.md|runbook|Verification|Validation|Rollback|Recovery|Success Criteria|Acceptance Criteria|current contract|superseded" docs/03.specs docs/05.operations/runbooks docs/04.execution
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
rg -n "^## Link Basis$|^## Related Documents$|^---$" -g 'README.md' docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations
```

Expected:

- README files contain canonical sections and no frontmatter.

- [ ] **Step 6: Validate and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/00.agent-governance/memory/progress.md
git commit -m "docs(sdlc): Apply active document profiles"
```

Expected:

- Active SDLC normalization passes repository gates.

### Task 4: Historical Evidence Normalization

**Files:**
- Modify: `docs/98.archive/**`
- Modify: older `docs/04.execution/plans/**`
- Modify: older `docs/04.execution/tasks/**`
- Modify: `docs/90.references/audits/**`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify as needed: archive and audit README indexes

- [ ] **Step 1: Classify historical surfaces**

Run:

```bash
find docs/98.archive docs/90.references/audits docs/04.execution/plans docs/04.execution/tasks -type f -name '*.md' | sort
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
rg -n "current and target|during the migration|after Phase|\\.claude/(hooks)|deprecated README heading|type:[ ]operations" docs/04.execution/plans docs/04.execution/tasks
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
git add docs/98.archive docs/04.execution/plans docs/04.execution/tasks docs/90.references/audits docs/00.agent-governance/memory/progress.md
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
git add docs/90.references .github docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md scripts/README.md tests/README.md scripts/validate-repo-quality-gates.sh docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(qa): Align references and CI QA contracts"
```

Expected:

- Reference, CI/QA, and formatting alignment passes repository gates.

### Task 6: Final Validator and Governance Reconciliation

**Files:**
- Modify: `scripts/validate-repo-quality-gates.sh`
- Modify as needed: `docs/00.agent-governance/**`
- Modify as needed: `docs/99.templates/**`
- Modify: `docs/04.execution/plans/2026-07-04-workspace-document-contract-normalization.md`
- Modify: `docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

- [ ] **Step 1: Re-run final drift scans**

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

- [ ] **Step 2: Add final deterministic validator checks**

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

- [ ] **Step 3: Run full validation bundle**

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

- [ ] **Step 4: Request final independent review**

Dispatch a read-only reviewer with this brief:

```text
Review the workspace document contract normalization branch. Verify that:
1. The implementation satisfies docs/03.specs/014-workspace-document-contract-normalization/spec.md.
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

- [ ] **Step 5: Complete evidence and commit**

Run:

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
git add scripts/validate-repo-quality-gates.sh docs/00.agent-governance docs/99.templates docs/04.execution/plans/2026-07-04-workspace-document-contract-normalization.md docs/04.execution/tasks/2026-07-04-workspace-document-contract-normalization.md
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

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence loses meaning during normalization. | High | Preserve old facts in explicit `Historical Context`, `Evidence`, or `Superseded Contract` sections. |
| Validator false positives block valid historical or generated docs. | High | Normalize documents first; add only path-scoped deterministic checks with documented exceptions. |
| Large diffs become hard to review. | Medium | Keep six logical commits and run spec/quality reviews after every task. |
| README files become contract duplicates. | Medium | Keep README updates to overview, index, link basis, and related documents. |
| External standards drift while implementation is in progress. | Medium | Use official/current links and record source refresh date in reference docs. |
| CI/QA docs overclaim deployment automation. | Medium | Treat `.github/workflows/ci.yml` and local scripts as repo-local source of truth; document non-QA workflows separately. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, `bash -n scripts/validate-repo-quality-gates.sh`, `bash scripts/validate-repo-quality-gates.sh .`, focused drift scans, and final subagent review.
- **Sandbox / Canary Rollout**: Not applicable; this is repo-static documentation and validator work.
- **Human Approval Gate**: Required before push, merge, live runtime action, CI trigger changes, secret handling changes, or branch cleanup.
- **Rollback Trigger**: Revert the logical task commit that introduced a validator false positive, broken link, or contract contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable; provider prompts and agent surfaces are documentation contracts, not model promotion artifacts, unless a later task touches them explicitly.

## Completion Criteria

- [ ] Audit inventory completed and indexed.
- [ ] Stage 99 support contracts and templates normalized.
- [ ] Active SDLC documents normalized.
- [ ] Historical evidence normalized and preserved.
- [ ] References, CI/QA, and formatting guidance aligned.
- [ ] Final validator gates reconciled.
- [ ] Full local validation bundle passed.
- [ ] Final independent review returned READY.
- [ ] Finishing branch workflow completed according to user choice.

## Related Documents

- **Spec**: [Workspace Document Contract Normalization Spec](../../03.specs/014-workspace-document-contract-normalization/spec.md)
- **Tasks**: [Workspace Document Contract Normalization Tasks](../tasks/2026-07-04-workspace-document-contract-normalization.md)
- **Template Routing Contract**: [Template Routing](../../99.templates/support/template-routing.md)
- **Frontmatter Schema**: [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md)
- **Documentation Contract**: [Template Documentation Contract](../../99.templates/support/documentation-contract.md)
- **CI/QA Guide**: [CI/CD and QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
