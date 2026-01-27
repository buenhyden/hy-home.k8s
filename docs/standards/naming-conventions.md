# Standard: Naming Conventions

To maintain a clean and parseable repository, all contributions MUST adhere to these naming standards.

## 📁 Repository Structure

- **Directories**: Use lowercase with hyphens (`kebab-case`).
  - *Correct*: `user-service`, `infrastructure-controllers`
  - *Incorrect*: `UserService`, `infrastructure_controllers`
- **Files**: Use lowercase with hyphens (`kebab-case`).
  - *Extension*: Use `.yaml` for Kubernetes manifests (avoid `.yml`).

## 🎡 Kubernetes Resources

- **Names**: `kebab-case`.
  - *Example*: `name: auth-server-svc`
- **Labels**: Use the standard `app.kubernetes.io/` prefix where possible.
  - `app.kubernetes.io/name`: Name of the application.
  - `app.kubernetes.io/instance`: Unique name of the deployment.
  - `app.kubernetes.io/version`: Version of the app.
  - `app.kubernetes.io/component`: Component role (e.g., `frontend`, `db`).

## 🌿 Git Strategy

- **Branches**:
  - `feature/APP_NAME-SHORT_DESC`
  - `fix/APP_NAME-ISSUE_ID`
  - `docs/TOPIC`
- **Tags**: Semantic Versioning (`vMAJOR.MINOR.PATCH`).
  - *Example*: `v1.2.0`

## 💬 Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
`type(scope): subject`

- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Scope**: The application or component name (e.g., `istio`, `user-api`).
