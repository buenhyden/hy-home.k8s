# PRD: Documentation and Agent Structure Refactor

- **Status**: Active
- **layer**: meta

**Overview (KR):** 리포지토리의 문서 구조와 AI 에이전트 지침을 2026년 3월 표준에 맞게 재구축하여 문서 가독성과 에이전트 효율성을 높이는 프로젝트입니다.

## Vision

Standardize the repository's documentation and agent entrypoints to ensure metadata compliance, path alignment, and efficient lazy-loading of instructions.

## Requirements

- [REQ-DOC-01] All documentation must include `layer:` metadata in frontmatter.
- [REQ-DOC-02] Path Alignment: Move `docs/incidents/` to `docs/operations/incidents/`.
- [REQ-DOC-03] Root documentation (`README`, `OPERATIONS`, `ARCHITECTURE`) must match actual directory structure.
- [REQ-AGENT-01] `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` must be lightweight shims delegating to `docs/agentic/`.
- [REQ-AGENT-02] Implement lazy-loading of instructions based on task scope.
- [REQ-AGENT-03] Ensure agents have full skill autonomy.

## Success Criteria

- [x] All root markdown files include `layer: "meta"`.
- [x] `docs/incidents/` is moved and link integrity is maintained.
- [x] AGENTS.md, CLAUDE.md, GEMINI.md are under 50 lines and use modular imports.
- [x] Pre-commit hooks pass without errors.
