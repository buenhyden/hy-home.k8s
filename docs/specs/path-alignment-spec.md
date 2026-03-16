---
layer: "meta"
---
# Technical Specification: Path Alignment and Root Documentation Update

- **Status**: Active
- **Type**: Spec
- **layer**: meta

**Overview (KR):** 리포지토리의 필수 디렉토리 경로를 정규화하고, 루트 문서들을 현재 구조에 맞게 수정하여 일관성을 확보하는 기술 로그입니다.

## 1. Directory Migration

- Move everything from `docs/incidents/` to `docs/operations/incidents/`.
- Ensure `docs/operations/postmortems/` exists.
- Update `OPERATIONS.md` to point to these new locations.

## 2. Root Documentation Meta

- Update `README.md`, `ARCHITECTURE.md`, `CODE_OF_CONDUCT.md`, `COLLABORATING.md`, `CONTRIBUTING.md`, `OPERATIONS.md` with:

  ```yaml
  ---
  layer: "meta"
  ---
  ```

- Ensure `README.md` correctly links to `docs/plans/` and `docs/operations/`.

## 3. Agent Entrypoints Shimming

- `AGENTS.md`: Remove bulk info, point to `docs/agentic/`.
- `CLAUDE.md`: Lightweight entrypoint, delegating rules.
- `GEMINI.md`: Lightweight entrypoint, delegating rules.

## Related Documents

- [docs/adr/0005-documentation-normalization.md](../adr/0005-documentation-normalization.md)
- [docs/plans/migration-plan.md](../plans/migration-plan.md)
