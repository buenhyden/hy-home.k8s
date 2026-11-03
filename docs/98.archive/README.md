# 98.archive

> 활성 stage를 떠난 문서를 위한 검증하지 않는 기록 보관소다.

## Overview

`98.archive/`는 더 이상 현재가 아닌 문서를 둘 수 있는 자리다.
[ADR-0053](../02.architecture/decisions/0053-unvalidated-archive.md)에 따라 어떤
검증기도 이 디렉터리를 읽지 않는다. profile, lifecycle, 링크, catalog, 보존 단위,
인용 규칙, migration 기록이 없으며, 변경 시에는 secret 검사만 실행된다.
formatter와 Markdown lint도 이 경로를 제외한다.

예전에 보관하던 본문, tombstone, migration 원장과 Retention Catalog는
[SPEC-0140](../03.specs/0140-archive-check-removal/spec.md)에서 삭제했다. 원본은
Git history가 복구하고, 각 문서의 요약은 그 주제를 소유한 현재
`docs/01.requirements/`·`docs/02.architecture/` 문서의 `Traceability` 아래
`Archived Lineage` 표에 있다.

## Structure

```text
98.archive/
├── README.md
├── completed/
│   └── 03.specs/
├── migrations/
└── superseded/
    ├── 01.requirements/
    ├── 02.architecture/
    │   ├── decisions/
    │   └── descriptions/
    ├── 03.specs/
    └── 05.operations/
```

- `completed/`: 끝나서 반영된 작업.
- `superseded/`: 후속 문서가 대체한 문서.
- `migrations/`: 예전 migration 원장 자리. 새 migration 기록은 만들지 않는다.

빈 디렉터리는 `.gitkeep`으로 유지한다.

## Usage

1. 현재 문서는 이 디렉터리 대신 현재 owner를 링크한다. 이 디렉터리를 가리키는
   링크는 검사하지 않으며, 대상이 없어도 실패하지 않는다.
2. 더 이상 현재가 아닌 문서는 삭제하거나 이 디렉터리의 해당 disposition으로
   옮긴다. 어느 쪽도 별도 기록이나 증명이 필요 없다.
3. 삭제 전 보관 내용은 마지막으로 그 내용을 담은 커밋 `69445fca`에서 찾는다.

   ```bash
   git ls-tree -r --name-only 69445fca -- docs/98.archive
   git show 69445fca:docs/98.archive/<path>
   ```

## Related Documents

- [Docs README](../README.md)
- [Document Lifecycle](../../.agents/governance/document-lifecycle.md)
- [ADR-0053: Unvalidated Archive](../02.architecture/decisions/0053-unvalidated-archive.md)
