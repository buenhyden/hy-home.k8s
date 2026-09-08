# Deployment-safety rules for tracked Kubernetes and Argo CD manifests.
#
# This package is the single owner of these rules. Conftest is required by the
# policy gate rather than optional, so a manifest is never reported as policy
# clean by an engine that silently did not run.
package main

import rego.v1

resource_name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")

sync_options contains option if {
	input.kind == "Application"
	some option in input.spec.syncPolicy.syncOptions
}

sync_options contains option if {
	input.kind == "ApplicationSet"
	some option in input.spec.template.spec.syncPolicy.syncOptions
}

# Containers are located by walking the document rather than by assuming the
# Deployment shape, so a CronJob, a Rollout template, or any other nesting is
# covered by the same rule.
container_images contains image if {
	walk(input, [path, value])
	path[count(path) - 1] in {"containers", "initContainers"}
	is_array(value)
	some item in value
	is_object(item)
	image := item.image
	is_string(image)
}

wildcard_surfaces contains surface if {
	input.kind == "AppProject"
	some surface in {"clusterResourceWhitelist", "namespaceResourceWhitelist"}
	some entry in input.spec[surface]
	entry.group == "*"
}

wildcard_surfaces contains surface if {
	input.kind == "AppProject"
	some surface in {"clusterResourceWhitelist", "namespaceResourceWhitelist"}
	some entry in input.spec[surface]
	entry.kind == "*"
}

deny contains msg if {
	input.apiVersion == "v1"
	input.kind == "Secret"
	msg := sprintf("plaintext Kubernetes Secret manifest is not allowed: %s", [resource_name])
}

deny contains msg if {
	"CreateNamespace=true" in sync_options
	msg := sprintf("%s must not use CreateNamespace=true: %s", [input.kind, resource_name])
}

deny contains msg if {
	some surface in wildcard_surfaces
	msg := sprintf("AppProject wildcard %s is not allowed: %s", [surface, resource_name])
}

deny contains msg if {
	some image in container_images
	endswith(image, ":latest")
	msg := sprintf("container image must not use latest tag: %s uses %s", [resource_name, image])
}
