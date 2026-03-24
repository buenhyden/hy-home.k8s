# Agent Scope: Runbooks

## Metadata
layer: "agent-scope"
governance: "docs/00.agent/rules/global-persona.md"

## Directives
1. [Actionable-Only]:
   Runbook은 즉각 실행 가능한 단계별 절차를 포함해야 한다.
2. [Location]:
   Runbook은 `docs/09.runbooks/`에 저장되어야 한다.

## Content Requirements
- 사전 조건 및 준비 사항이 명시되어야 한다.
- 각 단계별 기대 결과와 확인 방법이 포함되어야 한다.
- 실패 시의 롤백/복구 절차가 명확해야 한다.

## Related Templates
- [Runbook Template](file:///home/hy/projects/hy-home.k8s/docs/99.templates/runbook.template.md)

## Success Criteria
- [ ] 숙련되지 않은 작업자도 따라할 수 있는가?
- [ ] 각 단계의 검증 방법이 포함되었는가?
- [ ] 롤백 프로세스가 정의되어 있는가?
