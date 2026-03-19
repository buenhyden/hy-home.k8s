---
layer: "meta"
---
# Phase 2: Documentation Hardening & Integrity Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Achieve 100% integrity and compliance across all documentation (ADR, ARD, PRD, Specs, Plans, Runbooks, Operations) by resolving identified audit gaps.

**Architecture:** Systematic batch-wise remediation following a "Scan-Fix-Verify" loop. Uses folder-specific templates as the source of truth.

**Tech Stack:** Markdown, Shell (grep/find), Markdownlint.

---

### Task 1: Reference & Link Integrity (All Folders)

**Files:**
- Modify: `docs/**/README.md`
- Modify: `docs/**/*.md` (Specific files with broken links)

**Step 1: Run comprehensive broken link scan**
Run: `find docs -name "*.md" -exec grep -oP '\[.*?\]\(\K.*?(?=\))' {} + | sort -u`
Expected: List of all internal links.

**Step 2: Fix identified broken links in ADR/ARD indices**
Target: `docs/adr/README.md`, `docs/ard/README.md`.

**Step 3: Fix cross-document references (e.g., Specs to Plans)**
Target: `docs/specs/README.md`.

**Step 4: Commit**
```bash
git add docs/
git commit -m "docs: fix broken relative links and index indices"
```

### Task 2: ID Uniqueness & Metadata Normalization

**Files:**
- Modify: All files in `docs/{adr,ard,prd,specs,plans,runbooks,operations}`

**Step 1: Scan for duplicate IDs in frontmatter**
Run: `grep -r "ID:" docs | cut -d':' -f2- | sort | uniq -c | grep -v " 1 "`

**Step 2: Resolve ID collisions by adding functional prefixes (e.g., PRD-001, SPEC-GITOPS-001)**
Update frontmatter for colliding files.

**Step 3: Ensure mandatory `layer:` metadata exists in all files**
Run: `grep -L "layer:" docs/**/*.md`

**Step 4: Commit**
```bash
git add docs/
git commit -m "docs: normalize document IDs and enforce layer metadata"
```

### Task 3: Naming Convention & Template Compliance

**Files:**
- Rename: Files in `docs/` not matching `YYYY-MM-DD-title.md` (except ADRs)
- Modify: Files in `docs/operations/` and `docs/runbooks/` to match templates.

**Step 1: Rename files to follow YYYY-MM-DD-title.md convention**
Exclude `docs/adr/` (sequential) and `README.md`.

**Step 2: Align Runbooks with `templates/runbook-template.md`**
Ensure `Overview (KR)`, `Prerequisites`, and `Verification` sections exist.

**Step 3: Align Operations with `templates/incident-template.md`**
Ensure `Timeline`, `RCA`, and `Action Items` exist for postmortems.

**Step 4: Commit**
```bash
git add docs/
git commit -m "docs: enforce naming conventions and template structures"
```
