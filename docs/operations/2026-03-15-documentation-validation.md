# Documentation Validation Runbook

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-15
- **layer:** ops

**Overview (KR):** 프로젝트 문서의 무결성(링크, 메타데이터, 템플릿 준수)을 정기적으로 검증하고 유지보수하기 위한 실행 지침입니다.

## Prerequisites
- Python 3.x
- `grep`, `find` utilities

## Execution Steps

### 1. Link Integrity Check
Run the following script to identify broken internal links:

```bash
python3 -c '
import os, re
docs_dir = "docs"
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".md"):
            fpath = os.path.join(root, f)
            with open(fpath, "r") as md:
                content = md.read()
                links = re.findall(r"\[.*?\]\((?!http)(.*?)\)", content)
                for l in links:
                    l_path = l.split("#")[0]
                    if not l_path: continue
                    full_l = os.path.normpath(os.path.join(root, l_path))
                    if not os.path.exists(full_l):
                        print(f"BROKEN: {fpath} -> {l}")
'
```

### 2. Metadata Compliance
Verify that all files in `docs/` have the `layer:` metadata in their frontmatter.

### 3. Template Validation
Check if new ADRs and ARDs follow the latest templates in `templates/`.
