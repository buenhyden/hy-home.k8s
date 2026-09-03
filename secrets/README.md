# secrets

## Overview

`secrets/`는 로컬 개발에 필요한 **민감 파일의 보관 경로**다. 이 폴더의 실제
자료는 저장소에 추적되지 않는다. 추적되는 것은 디렉터리 형태를 유지하는
`certs/.gitkeep`과 이 README뿐이다.

폴더 이름과 달리 이곳은 비밀값의 소유자가 아니라 **로컬 파일이 놓이는 자리**다.
클러스터가 소비하는 비밀값의 canonical 소유자는 Vault와 External Secrets
Operator이며, 저장소에는 그 참조만 존재한다.

### Audience

- Platform maintainers
- 로컬 플랫폼을 부트스트랩하는 개발자

### Scope

#### In Scope

- 로컬 TLS 인증서와 키의 배치 경로 (`certs/`)
- 해당 경로의 추적 금지 경계

#### Out of Scope

- 클러스터 비밀값의 선언과 동기화 — `gitops/platform/eso/` 소유
- 비밀값 탐지 규칙과 baseline — `scripts/check-secret-handling.sh`, `.secrets.baseline` 소유
- 인증서 발급 절차의 canonical 설명 — `.env.example`와 부트스트랩 스크립트 소유

## Structure

| 경로 | 책임 | 추적 여부 |
| --- | --- | --- |
| `certs/.gitkeep` | 디렉터리 형태 유지 | 추적됨 |
| `certs/*.pem`, `*.crt`, `*.srl`, `*.p12` | mkcert 등으로 로컬 발급한 인증서와 키 | `.gitignore`로 제외 |

## Configuration Boundary

- `.gitignore`가 `secrets/certs/*.pem`, `*.srl`, `*.crt`, `*.p12`를 제외한다.
  새 확장자를 쓰기 전에 제외 규칙을 먼저 추가한다.
- 키 자료를 저장소에 커밋하지 않는다. 커밋된 적이 있다면 즉시 회전한다.
- 경로 값은 `.env.example`의 `CERT_DIR`, `CERT_FILE`, `KEY_FILE`, `ROOT_CA_FILE`이
  소유한다. 이 README는 그 값을 재정의하지 않는다.
- 이 폴더는 클러스터 비밀값을 정의하지 않는다. 워크로드가 쓰는 비밀값은 ESO를
  통해 Vault에서 온다.

## Validation

| 검증기 | 확인 대상 |
| --- | --- |
| `secret-handling` | 추적된 파일에 평문 비밀값이 없음 |
| `repository-quality` | 저장소 전역 품질 규칙 |

실행:

```bash
bash scripts/check-secret-handling.sh .
bash scripts/validate-repo-quality-gates.sh .
```

PASS는 추적된 바이트에 대한 증적이다. 로컬 워크트리에 놓인 추적되지 않는 키
파일의 안전성은 증명하지 않는다.

## Operations

- 로컬 인증서 발급 명령과 필요한 파일 목록은 `.env.example` 상단 주석을 따른다.
- 인증서를 교체한 뒤에는 Traefik dynamic config가 참조하는 경로가 그대로인지
  확인한다.
- 키 파일 권한은 소유자 전용으로 유지한다. 이 경계는 운영자가 소유하며 저장소
  검증이 대신 확인하지 않는다.

## Related Documents

- [Traefik](../traefik/README.md)
- [Infrastructure](../infrastructure/README.md)
- [GitOps](../gitops/README.md)
- [Scripts](../scripts/README.md)
