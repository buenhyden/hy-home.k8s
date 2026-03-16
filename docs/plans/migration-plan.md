---
layer: "meta"
---
# Implementation Plan: Documentation and Agent Migration

- **Status**: Active
- **Type**: Plan
- **layer**: meta

**Overview (KR):** 단계별 파일 이동 및 수정 계획을 통해 중단 없이 문서 구조를 최신 상태로 마이그레이션합니다.

## Phase 1: Preparation

- [ ] Create `docs/operations/postmortems/` directory.

## Phase 2: Directory Migration

- [ ] Move `docs/incidents/*.md` to `docs/operations/incidents/`.
- [ ] Update internal links in moved files.

## Phase 3: Root File Updates

- [ ] Update `README.md`.
- [ ] Update `OPERATIONS.md`.
- [ ] Update `ARCHITECTURE.md`.
- [ ] Update `CODE_OF_CONDUCT.md`.
- [ ] Update `CONTRIBUTING.md`.
- [ ] Update `COLLABORATING.md`.

## Phase 4: Agent Refactor

- [ ] Update `AGENTS.md`.
- [ ] Update `CLAUDE.md`.
- [ ] Update `GEMINI.md`.

## Related Documents

- [docs/adr/0005-documentation-normalization.md](../adr/0005-documentation-normalization.md)
- [docs/specs/path-alignment-spec.md](../specs/path-alignment-spec.md)
