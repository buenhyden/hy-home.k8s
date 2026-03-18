# Phase 3 Documentation Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Achieve 100% link integrity, frontmatter consistency, and template compliance across all 160+ documentation files.

**Architecture:** Systematic remediation using batch processing. We will prioritize structural link fixes first, followed by frontmatter normalization, and final template alignment.

**Tech Stack:** Shell (grep/sed), Markdown, YAML.

---

### Task 1: Fix Reference & Link Integrity

**Files:**
- Modify: ~25 files identified in audit (e.g., `docs/runbooks/2026-03-07-sealed-secrets-local.md`, `docs/agentic/lifecycle.md`, etc.)

**Step 1: Bulk update "MOVED" links**
Update relative paths where files have been renamed (e.g., `../specs/2026-03-16-gitops-spec.md` -> `../specs/2026-03-16-gitops-spec.md` - check relative depth).

**Step 2: Fix legitimate BROKEN links in runbooks**
- Update `docs/runbooks/2026-03-07-sealed-secrets-local.md` to point to `./2026-03-07-local-gitops-argocd.md`.
- Update `docs/runbooks/2026-03-19-incident-response-runbook.md` to point to `../operations/2026-03-19-incident-management.md`.

**Step 3: Commit**
```bash
git add .
git commit -m "docs: fix broken and moved links across documentation"
```

---

### Task 2: Frontmatter & Metadata Normalization

**Files:**
- Modify: All files in `docs/adr`, `docs/runbooks`, and `docs/operations`.

**Step 1: Normalize YAML vs Markdown metadata**
Ensure ADRs use the `title:`, `status:`, `date:`, `authors:`, `deciders:`, `tags:`, `layer:` YAML block AND the H1/Metadata block strictly as per `templates/adr-template.md`.

**Step 2: Sync Layer Metadata Formatting**
Standardize `layer: 'infra'` (quoted/unquoted) and remove any duplicate `- layer:` items.

**Step 3: Commit**
```bash
git add .
git commit -m "docs: normalize frontmatter and metadata formatting"
```

---

### Task 3: Template Alignment (Specs & Runbooks)

**Files:**
- Modify: `docs/specs/*.md`, `docs/runbooks/*.md`.

**Step 1: Align Specs with `spec-template.md`**
Ensure all specs have a "Verification" section and "Related Documents" list.

**Step 2: Align Runbooks with `runbook-template.md`**
Ensure all runbooks have "Purpose", "Canonical References", and "Escalation Path" sections.

**Step 3: Commit**
```bash
git add .
git commit -m "docs: align specs and runbooks with official templates"
```
