---
layer: "meta"
---
# Documentation Hardening Phase 3 Final Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Achieve 100% documentation integrity and metadata compliance across all core documentation folders.

**Architecture:** Systematic remediation using surgical string replacements (Batch remediations) and verification via a custom Python-based integrity scanner.

**Tech Stack:** Markdown, Shell (find/sed), Python (Verification)

---

## Task 1: Fix Persistent Broken Links

**Files:**

- Modify: `docs/agentic/lifecycle.md:90-95`
- Modify: `docs/manuals/README.md:18-22`
- Modify: `docs/runbooks/2026-03-15-documentation-maintenance.md:23-26`

**Step 1: Repair lifecycle.md links**
Fix malformed bracket/parentheses syntax.

- Target: `Documentation Validation` -> `../operations/2026-03-15-documentation-validation.md`
- Target: `Incident Management` -> `../operations/2026-03-19-incident-management.md`

**Step 2: Correct manuals/README.md relative path**
Update `[AGENTS.md](../../AGENTS.md)` to correctly point to the root from the `manuals/` subdirectory.

**Step 3: Fix documentation-maintenance.md placeholder**
Replace `[.*.md]` with `[2026-03-15-documentation-validation.md]`.

**Step 4: Verify links**
Run: `python3 -c "import os; print(os.path.exists('docs/operations/2026-03-19-incident-management.md'))"`
Expected: PASS

**Step 5: Commit**
`git commit -m "docs: fix persistent broken links in core documentation"`

---

## Task 2: Metadata & ID Normalization

**Files:**

- Modify: `docs/adr/0000-lazy-loading-implementation.md`
- Modify: `docs/adr/0001-k3d-local-cluster.md`
- Modify: `docs/adr/0002-argocd-gitops.md`
- Modify: `docs/adr/0003-documentation-taxonomy-standard.md`
- Modify: `docs/adr/0004-documentation-refactor-decision.md`
- Modify: `docs/adr/0005-documentation-normalization.md`

**Step 1: Fix accidental code fence in ADR 0000**
Remove the leading triple backticks incorrectly placed at the start of the file.

**Step 2: Consolidate Authors/Deciders into Owner**
Replace redundant fields in H1 blocks with a single `Owner: buenhyden` field.

**Step 3: Remove duplicate layer tags**
Ensure only one `layer:` tag exists in the file (keep the one in YAML frontmatter).

**Step 4: Commit**
`git commit -m "docs: normalize ADR metadata and consolidate owners"`

---

## Task 3: Template Compliance & Korean Overview

**Files:**

- Modify: `docs/ard/2026-03-16-agent-instruction-system-ard.md`

**Step 1: Add missing Overview (KR)**
Inject the following after the metadata block:
`**Overview (KR):** AI 에이전트가 리포지토리를 자율적으로 탐색하고 지침을 단계적으로 로드하기 위한 명세 및 아키텍처 구조를 정의합니다.`

**Step 2: Final integrity scan**
Run the comprehensive Python link scanner across all docs.

**Step 3: Commit**
`git commit -m "docs: add missing Korean overview and finalize template compliance"`
