package main

deny[msg] {
  input.apiVersion == "v1"
  input.kind == "Secret"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("plaintext Kubernetes Secret manifest is not allowed: %s", [name])
}

deny[msg] {
  input.kind == "Application"
  input.spec.syncPolicy.syncOptions[_] == "CreateNamespace=true"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("Application must not use CreateNamespace=true: %s", [name])
}

deny[msg] {
  input.kind == "ApplicationSet"
  input.spec.template.spec.syncPolicy.syncOptions[_] == "CreateNamespace=true"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("ApplicationSet must not use CreateNamespace=true: %s", [name])
}

deny[msg] {
  input.kind == "AppProject"
  whitelist := input.spec.clusterResourceWhitelist[_]
  whitelist.group == "*"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("AppProject must not allow wildcard cluster group: %s", [name])
}

deny[msg] {
  input.kind == "AppProject"
  whitelist := input.spec.clusterResourceWhitelist[_]
  whitelist.kind == "*"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("AppProject must not allow wildcard cluster kind: %s", [name])
}

deny[msg] {
  input.kind == "AppProject"
  whitelist := input.spec.namespaceResourceWhitelist[_]
  whitelist.group == "*"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("AppProject must not allow wildcard namespace group: %s", [name])
}

deny[msg] {
  input.kind == "AppProject"
  whitelist := input.spec.namespaceResourceWhitelist[_]
  whitelist.kind == "*"
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("AppProject must not allow wildcard namespace kind: %s", [name])
}

deny[msg] {
  image := input.spec.template.spec.containers[_].image
  endswith(image, ":latest")
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("container image must not use latest tag: %s uses %s", [name, image])
}

deny[msg] {
  image := input.spec.template.spec.initContainers[_].image
  endswith(image, ":latest")
  name := object.get(object.get(input, "metadata", {}), "name", "<unknown>")
  msg := sprintf("init container image must not use latest tag: %s uses %s", [name, image])
}
