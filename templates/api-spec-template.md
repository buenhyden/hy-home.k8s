---
openapi: 3.1.0
info:
  title: '[API Name / Feature] API Specification'
  description: '[Brief description of the API]'
  version: 'v1.x.x'
status: 'Draft | Proposed | Approved | Deprecated'
prd_reference: '[Link to PRD]'
spec_reference: '[Link to Tech Spec]'
adr_reference: '[Link to ADR]'
tags: ['api', 'contract', 'specification']
layer: 'app' # meta | infra | gitops | app | ops
---

# API Specification Template ([API Name / Feature])

> **Status**: Draft / Proposed / Approved / Deprecated
> **Version**: v1.x.x
> **Base URL**: `https://api.example.com/v1`
> **Related PRD**: [Link to PRD]
> **Related Technical Spec**: [Link to Tech Spec]
> **Related ADR**: [Link to ADR]

> **Purpose**: Define the exact contract, data models, and security requirements for an API feature before implementation begins. This document must be approved by human developers before Coder Agents execute it.

---

## 0. Canonical Location & Artifacts

This API contract MUST be stored under `docs/api/<feature>/` (contract-first).

### 0.1 Recommended Structure

```text
docs/api/<feature>/
  README.md        # The main specification document (this template)
  openapi.yaml            # OR schema.proto OR schema.graphql
  changelog.md            # Keep a Changelog format
```

### 0.2 Allowed Contract Formats

- OpenAPI 3.x (YAML or JSON) for REST APIs.
- GraphQL SDL for GraphQL APIs.
- Protobuf (`.proto`) for gRPC APIs.

### 0.3 Versioning & Breaking Changes

- API contracts MUST be versioned (recommended: URL path prefix like `/v1/`).
- Breaking changes MUST NOT be made within an existing major version. Breaking changes MUST be released as a new major version (e.g., `/v2/`) or via an explicitly documented and approved version negotiation strategy.

### 0.4 Changelog

Each API contract MUST include `docs/api/<feature>/changelog.md` using Keep a Changelog sections:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

### 0.5 Governance

- Contract-first governance: `.agent/rules/2000-API_Governance/2000-api-governance.md`
- API design standards: `.agent/rules/0000-Agents/0010-api-design-standard.md`

### 0.6 API Governance Checklist (Fill Before Design)

_Description: This document defines the team's working agreements, development processes, and collaboration SLAs as per the 0202-collaboration-and-sla-standard.md rules._

- **layer:** [meta | infra | gitops | app | ops]

> This document follows the **API Governance Pillar (2000)** and **OpenAPI 3.1.0** standards.
> Ensure all endpoints adhere to RESTful/GraphQL standards and versioning policies.

| Item           | Check Question                              | Required | Alignment Notes |
| -------------- | ------------------------------------------- | -------- | --------------- |
| Protocol       | REST / GraphQL / gRPC / Webhook?            | Must     |                 |
| Versioning     | Is the major version in the URL or Header?  | Must     |                 |
| Auth           | Is AuthN/AuthZ scheme defined (JWT/Scopes)? | Must     |                 |
| Validation     | Are all inputs validated via Zod/Pydantic?  | Must     |                 |
| Error Handling | Standardized JSON error schema used?        | Must     |                 |
| Rate Limiting  | Are quotas/throttling defined?              | Must     |                 |
| Documentation  | Is OpenAPI/Swagger generated from this?     | Must     |                 |

---

## 1. Overview & Use Cases

**Objective**: Briefly describe the problem this API solves and its primary consumers (e.g., Web Client, Mobile App, 3rd Party Integration).

**Use Cases**:

- UC1: User can retrieve a list of widgets with pagination.
- UC2: User can create a new widget.

---

## 2. Resource Definitions

**Resource Models**: Define the core domain entities using OpenAPI 3.1 schema definitions.

_Example: Widget Resource_

```yaml
components:
  schemas:
    Widget:
      type: object
      required:
        - id
        - name
        - status
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
        name:
          type: string
          minLength: 1
          description: Widget name
        status:
          type: string
          enum: [active, archived]
        created_at:
          type: string
          format: date-time
```

---

## 3. Endpoints Contract

Define all endpoints using RESTful plural nouns (no verbs in paths). Be sure to include explicit validation rules (e.g., via Zod, Pydantic, or JSON Schema) for all inputs.

### 3.1. `[METHOD] /v1/[resource]` (Operation ID: `[operationId]`)

**Summary**: [Short summary]
**Tags**: [[Tag1], [Tag2]]

**Request**:

- **Parameters**:
  - `limit` (int, default 20, in: query)
  - `cursor` (string, optional, in: query)
- **Body**: (If applicable)
  - Content-Type: `application/json`
  - Schema: `$ref: '#/components/schemas/[ResourceName]'`

**Responses**:

- **200 OK**:
  - Description: [Success message]
  - Schema: `$ref: '#/components/schemas/[ResponseName]'`
  - Example:
    ```json
    {
      "data": [...],
      "meta": { "next_cursor": "abc" }
    }
    ```
- **400 Bad Request**:
  - $ref: '#/components/responses/BadRequest'

---

## 4. Webhooks & Events (Optional)

Define asynchronous event payloads or webhook triggers from this service.

- **Trigger**: [Event Name, e.g., `widget.created`]
- **Payload Schema**: [Define the JSON payload structure]
- **Security**: [e.g., HMAC Signature Verification via `X-Signature` header]

---

## 5. Authentication & Security

- **Auth Method**: [BearerAuth | OAuth2 | APIKey]
- **Required Scopes/Roles**: e.g., `widget:read`, `widget:write`

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

---

## 6. Non-Functional Requirements (NFRs)

- **Latency**: e.g., < 200ms (p95)
- **Rate Limit**: e.g., 100 requests / minute per user
- **Idempotency**: e.g., `X-Idempotency-Key` header required for `POST/PUT` operations

---

## 7. Error Handling

Define known failure states and their corresponding standard HTTP status codes.

- **400 Bad Request**: Validation failure (e.g., missing required field).
- **401 Unauthorized**: Missing or invalid token.
- **403 Forbidden**: Valid token, but lacks required role.
- **404 Not Found**: Target resource ID does not exist.
- **429 Too Many Requests**: Rate limit exceeded.

**Standard Error Schema**:

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Programmatic error code
        message:
          type: string
          description: User-facing message
        details:
          type: array
          items:
            type: object
            properties:
              field: { type: string }
              message: { type: string }
```

---

## 8. Versioning Strategy

- **API Version**: (e.g., v1)
- **Breaking Change Policy**: State how changes will be handled (e.g., major version bump in URL `/v2/` or via Accept headers).
