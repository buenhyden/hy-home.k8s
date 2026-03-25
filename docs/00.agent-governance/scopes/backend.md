# Backend Layer Scope

This scope defines the technical constraints for the Backend Engineer persona.

## 1. Core Responsibilities

- Implement API logic, service layers, and database interactions.
- Maintain technical specifications in `docs/04.specs/`.
- Follow the **Clean Architecture** patterns as defined in `docs/02.ard/`.
- **Guidelines**: Follow REST/GraphQL patterns from `.agent/rules/0900-Backend/`.
- **SSoT**: `docs/04.specs/`, `docs/01.prd/`.

## Layer-specific DoD (Backend)

- [ ] **API Registry**: If a new endpoint is added, register it in `docs/04.specs/`.
- [ ] **Database Integrity**: Schema changes must have a corresponding migration spec.
- [ ] **Auth Enforcement**: All new routes must specify auth middleware requirements.
- [ ] **Error Handling**: Follow the standard `ErrorResponse` structure.

## 2. Standard Taxonomy

- **API Spec**: OpenAPI/Swagger definitions.
- **Data Repository**: Prisma/SQL optimization guides.
- **Service Logic**: Domain-driven design implementation.

## 3. Required Metadata

```markdown
---
layer: backend
stage: 04
---
```

## 4. Skills Engagement

- `nodejs-backend-patterns`
- `postgresql-optimization`
- `api-design-principles`
- `fastapi-pro`
- `better-auth-best-practices`
- `postgres-best-practices`
- `prisma-schema-optimize`
