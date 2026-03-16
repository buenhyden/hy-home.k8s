# Agent Instruction Files Refactor Plan

- **Status**: Completed
- **layer:** meta

**Overview (KR):** AGENTS.md, GEMINI.md, CLAUDE.md 파일을 점진적 공개(Progressive Disclosure) 원칙에 따라 리팩토링하고, 지연 로딩을 위한 허브 문서를 구축합니다.

**Architecture:** Root files stay < 50 lines (essentials only). All detailed persona/rule mappings delegate to `docs/agent-instructions.md`. Scoped `docs/*/AGENTS.md`, `CLAUDE.md`, `GEMINI.md` files receive updated persona and rule references from `.agent/rules/` categories.

**Tech Stack:** Markdown, `@`-import syntax (CLAUDE/GEMINI), repo-relative links

---

## Task 1: Reset staged AGENTS.md and rewrite root AGENTS.md

**Files:**

- Modify: `AGENTS.md`

**Step 1:** Unstage and overwrite AGENTS.md with concise progressive-disclosure version.

Root file must:

- Be < 50 lines
- Link to `docs/agent-instructions.md`
- Reference actual repo paths only (no `ARCHITECTURE.md`, `web/`, `app/`, `server/`, `tests/`)
- Map each `docs/` subtree to its persona

**Step 2:** Verify content length and links.

**Step 3:** Stage the file.

```bash
git add AGENTS.md
```

---

## Task 2: Update root CLAUDE.md

**Files:**

- Modify: `CLAUDE.md`

## Related Documents

- [docs/prd/documentation-system-prd.md](../prd/documentation-system-prd.md)
- [docs/specs/documentation-system-spec.md](../specs/documentation-system-spec.md)

**Step 1:** Keep cluster bootstrap commands. Add link to `docs/agent-instructions.md`. Keep `@./.claude/CLAUDE.md` import. No skill restrictions.

**Step 2:** Stage.

```bash
git add CLAUDE.md
```

---

## Task 3: Update root GEMINI.md

**Files:**

- Modify: `GEMINI.md`

**Step 1:** Keep thin shim structure. Add link to `docs/agent-instructions.md`. Clarify skill usage is unrestricted.

**Step 2:** Stage.

```bash
git add GEMINI.md
```

---

## Task 4: Create docs/agent-instructions.md (lazy-loading hub)

**Files:**

- Create: `docs/agent-instructions.md`

**Step 1:** Write hub file with each doc scope section:

- Each section: persona, applicable `.agent/rules/` category, template link, and link to scoped AGENTS.md
- Sections: adr, ard, prd, specs, plans, runbooks, incidents, operations
- Skills: explicitly state any runtime-provided skill may be used

**Step 2:** Stage.

```bash
git add docs/agent-instructions.md
```

---

## Task 5: Update scoped docs/*/AGENTS.md files

**Files:**

- Modify: `docs/adr/AGENTS.md`, `docs/ard/AGENTS.md`, `docs/prd/AGENTS.md`, `docs/specs/AGENTS.md`, `docs/plans/AGENTS.md`, `docs/runbooks/AGENTS.md`, `docs/incidents/AGENTS.md`, `docs/operations/AGENTS.md`

**Step 1:** Each file gets explicit `.agent/rules/` rule references relevant to its persona (from `.agent/rules/` category mapping). Add "Skills: any runtime-provided skill" line.

**Step 2:** Stage all.

```bash
git add docs/*/AGENTS.md
```

---

## Task 6: Update scoped docs/*/CLAUDE.md and GEMINI.md

**Files:**

- Modify: `docs/adr/CLAUDE.md`, `docs/specs/CLAUDE.md`, etc. (8 files each for CLAUDE and GEMINI)

**Step 1:** Each CLAUDE.md: add explicit bias statement + `@../../.claude/CLAUDE.md` (already exists, verify correctness).
Each GEMINI.md: same pattern with `@../../.claude/GEMINI.md`.

**Step 2:** Stage all.

```bash
git add docs/*/CLAUDE.md docs/*/GEMINI.md
```

---

## Task 7: Verify links and commit

**Step 1:** Run pre-commit lint.

```bash
pre-commit run markdownlint-cli2 --all-files
```

**Step 2:** Fix any lint errors.

**Step 3:** Commit.

```bash
git commit -m "refactor: agent instruction files with progressive disclosure and lazy-loading hub"
```
