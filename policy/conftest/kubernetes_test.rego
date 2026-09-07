# Executable proof that every deployment-safety rule still fires. A policy that
# stops matching is a silent loss of coverage, so each rule has both a
# triggering and a non-triggering case.
package main

import rego.v1

test_plaintext_secret_is_denied if {
	count(deny) == 1 with input as {
		"apiVersion": "v1",
		"kind": "Secret",
		"metadata": {"name": "db-credentials"},
	}
}

test_external_secret_is_allowed if {
	count(deny) == 0 with input as {
		"apiVersion": "external-secrets.io/v1",
		"kind": "ExternalSecret",
		"metadata": {"name": "db-credentials"},
	}
}

test_application_create_namespace_is_denied if {
	count(deny) == 1 with input as {
		"kind": "Application",
		"metadata": {"name": "adminer"},
		"spec": {"syncPolicy": {"syncOptions": ["CreateNamespace=true"]}},
	}
}

test_application_without_create_namespace_is_allowed if {
	count(deny) == 0 with input as {
		"kind": "Application",
		"metadata": {"name": "adminer"},
		"spec": {"syncPolicy": {"syncOptions": ["ServerSideApply=true"]}},
	}
}

test_application_set_create_namespace_is_denied if {
	count(deny) == 1 with input as {
		"kind": "ApplicationSet",
		"metadata": {"name": "workloads"},
		"spec": {"template": {"spec": {"syncPolicy": {"syncOptions": ["CreateNamespace=true"]}}}},
	}
}

test_app_project_wildcard_cluster_group_is_denied if {
	count(deny) == 1 with input as {
		"kind": "AppProject",
		"metadata": {"name": "platform"},
		"spec": {"clusterResourceWhitelist": [{"group": "*", "kind": "Namespace"}]},
	}
}

test_app_project_wildcard_namespace_kind_is_denied if {
	count(deny) == 1 with input as {
		"kind": "AppProject",
		"metadata": {"name": "platform"},
		"spec": {"namespaceResourceWhitelist": [{"group": "apps", "kind": "*"}]},
	}
}

test_app_project_explicit_surfaces_are_allowed if {
	count(deny) == 0 with input as {
		"kind": "AppProject",
		"metadata": {"name": "platform"},
		"spec": {"namespaceResourceWhitelist": [{"group": "apps", "kind": "Deployment"}]},
	}
}

test_latest_container_tag_is_denied if {
	count(deny) == 1 with input as {
		"kind": "Deployment",
		"metadata": {"name": "adminer"},
		"spec": {"template": {"spec": {"containers": [{"image": "adminer:latest"}]}}},
	}
}

test_latest_init_container_tag_is_denied if {
	count(deny) == 1 with input as {
		"kind": "Deployment",
		"metadata": {"name": "adminer"},
		"spec": {"template": {"spec": {"initContainers": [{"image": "busybox:latest"}]}}},
	}
}

# The Deployment shape is not assumed: a CronJob nests its pod template deeper,
# and a tag there is the same deployment risk.
test_latest_tag_is_denied_outside_the_deployment_shape if {
	count(deny) == 1 with input as {
		"kind": "CronJob",
		"metadata": {"name": "backup"},
		"spec": {"jobTemplate": {"spec": {"template": {"spec": {"containers": [{"image": "backup:latest"}]}}}}},
	}
}

test_pinned_container_tag_is_allowed if {
	count(deny) == 0 with input as {
		"kind": "Deployment",
		"metadata": {"name": "adminer"},
		"spec": {"template": {"spec": {"containers": [{"image": "adminer:5.4.1"}]}}},
	}
}
