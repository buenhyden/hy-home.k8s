# Agent Scope: Plans

## Metadata

layer: "agent-scope"
governance: "docs/00.agent/rules/global-persona.md"

## Directives

1. [Verification-First]:
   모든 실행 계획은
   [Plans](file:///home/hy/projects/hy-home.k8s/docs/05.plans/README.md)
   에 정의된 검증 절차를 포함해야 한다.

## Content Requirements

- 단계별 구현 세부 사항이 명확해야 한다.
- 각 단계에 대한 구체적인 검증 방법(테스트 케이스 등)이 포함되어야 한다.
- 영향도 분석 및 대안 계획(Fallback)이 포함되어야 한다.

## Related Templates

- [Plan Template](file:///home/hy/projects/hy-home.k8s/docs/99.templates/plan.template.md)

## Success Criteria

- [ ] 구현 단계가 논리적이고 구체적인가?
- [ ] 검증 도구 및 방법이 명시되었는가?
- [ ] 롤백 전략이 포함되었는가?
- [ ] 리소스 및 일정 고려 사항이 포함되었는가?
