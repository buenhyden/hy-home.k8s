# Frontend Layer Scope

This scope defines the technical constraints for the Frontend Engineer persona.

## 1. Core Responsibilities

- Implement UI components, client-side state, and responsive layouts.
- Maintain Component Specs in `docs/04.specs/`.
- Follow **WCAG 2.2** accessibility standards.

## 2. Standard Taxonomy

- **Component Lab**: Storybook/Registry.
- **Guidelines**: Follow UI/UX patterns from `.agent/rules/1000-Frontend/`.
- **SSoT**: `docs/04.specs/`, `docs/01.prd/`.
- **Client State**: Zustand/Redux logic.

## Layer-specific DoD (Frontend)

- [ ] **Accessibility Audit**: Run `wcag-audit-patterns` on new UI components.
- [ ] **Responsive Check**: Verify layout on Mobile, Tablet, and Desktop.
- [ ] **Theme Consistency**: Ensure new components use the design system tokens.
- [ ] **State Management**: Verify data flow adheres to the established store patterns.

## 3. Required Metadata

```markdown
---
layer: frontend
stage: 04
---
```

## 4. Skills Engagement

- `react-patterns`
- `next-best-practices`
- `tailwind-patterns`
- `tailwind-css-patterns`
- `accessibility-compliance`
- `frontend-design`
- `vercel-react-best-practices`
