.PHONY: test lint build

# Test target for CI detection
# Currently this service only contains K8s manifests.
# Add actual test commands when application source is available.
test:
	@echo "=== backend-service-2 test ==="
	@echo "No unit tests configured (K8s manifests only)"
	@echo "Running kustomize validation instead..."
	@$(MAKE) lint

# Lint/validate Kustomize manifests
lint:
	@echo "=== Validating Kustomize manifests ==="
	@if command -v kustomize >/dev/null 2>&1; then \
		kustomize build base --enable-helm 2>/dev/null || kustomize build base; \
	else \
		echo "kustomize not found, skipping validation"; \
	fi

# Build placeholder (for future use)
build:
	@echo "No build step configured for backend-service-2"
