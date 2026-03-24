---
layer: "meta"
---
# API Specification (API.md)

_Target Location: `docs/api/<feature>/README.md`_
_Description: Defines the interface contract for REST/GraphQL/gRPC endpoints. This is a contract-first document._

## Overview (KR)
이 문서는 API의 인터페이스 규약을 정의합니다. 엔드포인트, 요청/응답 스키마, 인증 방식 및 에러 응답 표준을 포함하며 개발자와 클라이언트 간의 협업 기반이 됩니다.

---

## 1. API Metadata

- **Base URL**: `/api/v1`
- **Status**: [Draft | Approved | Deprecated]
- **layer**: [meta | infra | gitops | app | ops]
- **Standards**: OpenAPI 3.1.0 / RESTful

## 2. Governance Checklist (Senior)

| Item | Requirement | Status |
| :--- | :--- | :--- |
| **Versioning** | Major version in URL path | [Yes/No] |
| **Idempotency** | Required for POST/PUT via `X-Idempotency-Key` | [Yes/No] |
| **Pagination** | Cursor-based (recommended) or Limit/Offset | [Type] |
| **Rate Limiting** | X-RateLimit-Limit / Remaining headers | [Yes/No] |
| **Auth** | JWT / OAuth2 / API Key | [Type] |

## 3. Endpoint Specifications

### 3.1 `[METHOD] /path/to/resource`
**Operation ID**: `getJobs`

#### Request
- **Headers**:
  - `Authorization`: Bearer <JWT>
- **Query Params**:
  - `limit`: int (default 20)
  - `cursor`: string (optional)

#### Response (200 OK)
```json
{
  "data": [],
  "meta": {
    "has_next": true,
    "next_cursor": "..."
  }
}
```

## 4. Error Standards

| Status Code | Code | Meaning |
| :--- | :--- | :--- |
| 400 | `BAD_REQUEST` | Validation failed |
| 401 | `UNAUTHORIZED` | Token missing/invalid |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded |

## 5. Security & Authentication
- **Scheme**: Bearer JWT
- **Scopes**: `read:resources`, `write:resources`

## 6. Implementation Notes
- **Payload Compression**: Enabled (Gzip/Brotli)
- **Caching**: `Cache-Control: private, max-age=60`
- **Schema Reference**: `openapi.yaml` (link to file)
