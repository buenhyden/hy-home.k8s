"""Parsed ingress cross-references for the current local GitOps platform.

Chart/operator Services are checked against their pinned owner declarations;
this is repository evidence, not a claim that those Services were rendered.
"""

from collections.abc import Iterable, Mapping
from pathlib import Path
import re

import yaml


HOST_SUFFIX = "hy-k8s.home.arpa"
ISSUER = "mkcert-ca-issuer"
REDIRECT = "nginx.ingress.kubernetes.io/permanent-redirect"
SSL_REDIRECT = "nginx.ingress.kubernetes.io/ssl-redirect"

# Identity, route, backend and TLS secret are repository-specific desired state.
ROUTES = {
    ("apps", "adminer"): ("adminer", "/", "adminer", 8080, "adminer-tls"),
    ("headlamp", "headlamp"): ("headlamp", "/", "headlamp", 4466, "headlamp-tls"),
    ("istio-system", "kiali"): ("kiali", "/kiali", "kiali", 20001, "kiali-tls"),
    **{
        ("ingress-nginx", f"apex-{name}"): (
            "",
            f"/{name}",
            "ingress-nginx-controller",
            80,
            "hy-k8s-apex-tls",
        )
        for name in ("argo", "kiali", "headlamp", "rollouts", "adminer")
    },
}


def _get(value, *keys):
    for key in keys:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def _one(value):
    return value[0] if isinstance(value, list) and len(value) == 1 else None


def _load(root: Path, relative: str):
    path = root / relative
    try:
        parent = path
        while parent != root:
            if parent.is_symlink():
                return None
            parent = parent.parent
        if not path.is_file() or path.stat().st_size > 131072:
            return None
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return None
    return value if isinstance(value, Mapping) else None


def _chart(root, name, chart, repo, version, namespace, release=None):
    app = _load(root, f"gitops/apps/root/platform-{name}-app.yaml")
    source = _get(app, "spec", "source")
    destination = _get(app, "spec", "destination")
    if not all(
        (
            _get(app, "apiVersion") == "argoproj.io/v1alpha1",
            _get(app, "kind") == "Application",
            _get(app, "metadata", "name") == f"platform-{name}",
            _get(source, "repoURL") == repo,
            _get(source, "chart") == chart,
            _get(source, "targetRevision") == version,
            _get(source, "helm", "releaseName") == (release or name),
            _get(destination, "namespace") == namespace,
            _get(destination, "server") == "https://kubernetes.default.svc",
        )
    ):
        return None
    try:
        values = yaml.safe_load(_get(source, "helm", "values"))
    except (TypeError, yaml.YAMLError):
        return None
    return values if isinstance(values, Mapping) else None


def _owner_declarations(root):
    headlamp = _chart(
        root,
        "headlamp",
        "headlamp",
        "https://kubernetes-sigs.github.io/headlamp/",
        "0.41.0",
        "headlamp",
    )
    kiali = _chart(
        root,
        "kiali",
        "kiali-operator",
        "https://kiali.org/helm-charts",
        "2.10.0",
        "istio-system",
    )
    nginx = _chart(
        root,
        "ingress-nginx",
        "ingress-nginx",
        "https://kubernetes.github.io/ingress-nginx",
        "4.12.0",
        "ingress-nginx",
    )
    return {
        ("headlamp", "headlamp", 4466): all(
            (
                _get(headlamp, "service", "port") == 4466,
                _get(headlamp, "service", "type") == "ClusterIP",
                _get(headlamp, "nameOverride") in (None, ""),
                _get(headlamp, "fullnameOverride") in (None, ""),
                _get(headlamp, "namespaceOverride") in (None, ""),
                _get(headlamp, "ingress", "enabled") in (None, False),
                _get(headlamp, "httpRoute", "enabled") in (None, False),
                _get(headlamp, "extraManifests") in (None, []),
            )
        ),
        ("istio-system", "kiali", 20001): all(
            (
                _get(kiali, "cr", "create") is True,
                _get(kiali, "cr", "name") in (None, "kiali"),
                _get(kiali, "cr", "namespace") in (None, "", "istio-system"),
                _get(kiali, "watchNamespace") in (None, "", "istio-system"),
                _get(kiali, "cr", "spec", "deployment", "namespace")
                in (None, "", "istio-system"),
                _get(kiali, "cr", "spec", "deployment", "instance_name")
                in (None, "kiali"),
                _get(kiali, "cr", "spec", "deployment", "remote_cluster_resources_only")
                in (None, False),
                _get(kiali, "cr", "spec", "deployment", "ingress", "enabled")
                in (None, False),
                _get(kiali, "cr", "spec", "deployment", "service_type")
                in (None, "ClusterIP"),
                _get(kiali, "cr", "spec", "deployment", "additional_service_yaml")
                in (None, {}),
                _get(kiali, "cr", "spec", "server", "port") in (None, 20001),
                _get(kiali, "cr", "spec", "server", "web_root") == "/kiali",
            )
        ),
        ("ingress-nginx", "ingress-nginx-controller", 80): _get(
            nginx, "controller", "service", "type"
        )
        == "LoadBalancer"
        and _get(nginx, "controller", "service", "nodePorts", "http") == 30080
        and _get(nginx, "controller", "service", "nodePorts", "https") == 30443
        and _get(nginx, "nameOverride") in (None, "")
        and _get(nginx, "fullnameOverride") in (None, "")
        and _get(nginx, "namespaceOverride") in (None, "")
        and _get(nginx, "controller", "name") in (None, "controller")
        and _get(nginx, "controller", "enabled") in (None, True)
        and _get(nginx, "controller", "service", "enabled") in (None, True)
        and _get(nginx, "controller", "service", "external", "enabled") in (None, True)
        and _get(nginx, "controller", "service", "enableHttp") in (None, True)
        and _get(nginx, "controller", "service", "enableHttps") in (None, True)
        and _get(nginx, "controller", "service", "ports", "http") in (None, 80)
        and _get(nginx, "controller", "service", "ports", "https") in (None, 443)
        and _get(nginx, "controller", "service", "allocateLoadBalancerNodePorts")
        in (None, True)
        and _get(nginx, "controller", "allowSnippetAnnotations") in (None, False)
        and _get(nginx, "controller", "config", "allow-snippet-annotations")
        in (None, False, "false"),
    }


def _declared_ingresses(root):
    errors = []
    argo = _load(root, "infrastructure/argocd/values-local.yaml")
    argo_ingress = _get(argo, "server", "ingress")
    argo_tls = _one(_get(argo_ingress, "extraTls"))
    argo_host = f"argo.{HOST_SUFFIX}"
    if not all(
        (
            _get(argo, "global", "domain") == argo_host,
            _get(argo_ingress, "enabled") is True,
            _get(argo_ingress, "ingressClassName") == "nginx",
            _get(argo_ingress, "hostname") == argo_host,
            _get(argo_ingress, "tls") is False,
            _get(argo_tls, "hosts") == [argo_host],
            _get(argo_tls, "secretName") == "argocd-local-tls",
            _get(argo_ingress, "annotations", "cert-manager.io/cluster-issuer") is None,
            _get(argo_ingress, "annotations", SSL_REDIRECT) in (None, "true"),
        )
    ):
        errors.append("INGRESS_DECLARATION argocd/bootstrap")

    rollouts = _chart(
        root,
        "rollouts",
        "argo-rollouts",
        "https://argoproj.github.io/argo-helm",
        "2.40.9",
        "argo-rollouts",
        "argo-rollouts",
    )
    dashboard = _get(rollouts, "dashboard")
    ingress = _get(dashboard, "ingress")
    host = f"rollouts.{HOST_SUFFIX}"
    tls = _one(_get(ingress, "tls"))
    if not all(
        (
            _get(dashboard, "enabled") is True,
            _get(ingress, "enabled") is True,
            _get(ingress, "ingressClassName") == "nginx",
            _get(ingress, "hosts") == [host],
            _get(tls, "hosts") == [host],
            _get(tls, "secretName") == "rollouts-dashboard-tls",
            _get(ingress, "annotations", "cert-manager.io/cluster-issuer") == ISSUER,
            _get(ingress, "annotations", SSL_REDIRECT) == "true",
        )
    ):
        errors.append("INGRESS_DECLARATION argo-rollouts/dashboard")
    return errors


def validate(root: Path, rendered_documents: Iterable[Mapping]) -> list[str]:
    """Return fixed-code findings; never include untrusted manifest values."""
    errors = []
    ingresses = {}
    services = {}
    issuers = []
    for doc in rendered_documents:
        if not isinstance(doc, Mapping):
            errors.append("INGRESS_DOCUMENT malformed")
            continue
        kind = doc.get("kind")
        if kind == "ClusterIssuer" and _get(doc, "metadata", "name") == ISSUER:
            issuers.append(doc)
        if kind not in ("Ingress", "Service"):
            continue
        metadata = _get(doc, "metadata")
        namespace = _get(metadata, "namespace")
        name = _get(metadata, "name")
        if not all(
            isinstance(part, str)
            and len(part) <= 63
            and re.fullmatch(r"[a-z0-9](?:[-a-z0-9]*[a-z0-9])?", part)
            for part in (namespace, name)
        ):
            errors.append("INGRESS_IDENTITY malformed")
            continue
        identity = (namespace, name)
        if kind == "Ingress":
            if identity in ingresses:
                errors.append(f"INGRESS_DUPLICATE {namespace}/{name}")
            ingresses[identity] = doc
        elif identity in services:
            errors.append(f"INGRESS_SERVICE_DUPLICATE {namespace}/{name}")
        else:
            services[identity] = doc

    if not (
        len(issuers) == 1
        and issuers[0].get("apiVersion") == "cert-manager.io/v1"
        and _get(issuers[0], "spec", "ca", "secretName") == "mkcert-root-ca"
    ):
        errors.append("INGRESS_ISSUER_OWNER mkcert-ca-issuer")
    owners = _owner_declarations(root)
    errors.extend(_declared_ingresses(root))
    for identity, (subdomain, path, service, port, secret) in ROUTES.items():
        label = "/".join(identity)
        doc = ingresses.get(identity)
        if doc is None:
            errors.append(f"INGRESS_MISSING {label}")
            continue
        if (
            doc.get("apiVersion") != "networking.k8s.io/v1"
            or doc.get("kind") != "Ingress"
        ):
            errors.append(f"INGRESS_GVK {label}")
        if isinstance(doc.get("spec"), Mapping) and "defaultBackend" in doc["spec"]:
            errors.append(f"INGRESS_DEFAULT_BACKEND {label}")
        expected_host = f"{subdomain}.{HOST_SUFFIX}" if subdomain else HOST_SUFFIX
        rule = _one(_get(doc, "spec", "rules"))
        route = _one(_get(rule, "http", "paths"))
        if not all(
            (
                _get(doc, "spec", "ingressClassName") == "nginx",
                _get(rule, "host") == expected_host,
                _get(route, "path") == path,
                _get(route, "pathType") == "Prefix",
            )
        ):
            errors.append(f"INGRESS_ROUTE {label}")
        backend = _get(route, "backend")
        if not all(
            (
                _get(backend, "service", "name") == service,
                _get(backend, "service", "port", "number") == port,
                _get(backend, "service", "port", "name") is None,
                _get(backend, "resource") is None,
            )
        ):
            errors.append(f"INGRESS_BACKEND {label}")
        tls = _one(_get(doc, "spec", "tls"))
        if _get(tls, "hosts") != [expected_host] or _get(tls, "secretName") != secret:
            errors.append(f"INGRESS_TLS {label}")
        annotations = _get(doc, "metadata", "annotations")
        if not isinstance(annotations, Mapping) or any(
            isinstance(key, str)
            and key.startswith("nginx.ingress.kubernetes.io/")
            and key.endswith("-snippet")
            for key in annotations
        ):
            errors.append(f"INGRESS_ANNOTATION {label}")
        apex = identity[0] == "ingress-nginx"
        expected_redirect = (
            f"https://{identity[1][5:]}.{HOST_SUFFIX}/" if apex else None
        )
        if (
            _get(annotations, SSL_REDIRECT) != "true"
            or _get(annotations, REDIRECT) != expected_redirect
        ):
            errors.append(f"INGRESS_REDIRECT {label}")
        expected_issuer = ISSUER if not apex or identity[1] == "apex-argo" else None
        if _get(annotations, "cert-manager.io/cluster-issuer") != expected_issuer:
            errors.append(f"INGRESS_ISSUER {label}")
        if identity == ("apps", "adminer"):
            if (
                _get(annotations, "nginx.ingress.kubernetes.io/service-upstream")
                != "true"
                or _get(annotations, "nginx.ingress.kubernetes.io/upstream-vhost")
                != "adminer.apps.svc.cluster.local"
            ):
                errors.append(f"INGRESS_MESH {label}")
        elif (
            identity == ("istio-system", "kiali")
            and _get(annotations, "nginx.ingress.kubernetes.io/app-root") != "/kiali"
        ):
            errors.append(f"INGRESS_APP_ROOT {label}")

        owner = services.get((identity[0], service))
        if owner is not None:
            service_ports = _get(owner, "spec", "ports")
            if not (
                owner.get("apiVersion") == "v1"
                and owner.get("kind") == "Service"
                and isinstance(service_ports, list)
                and sum(
                    isinstance(item, Mapping) and item.get("port") == port
                    for item in service_ports
                )
                == 1
            ):
                errors.append(f"INGRESS_OWNER {label}")
        elif not owners.get((identity[0], service, port), False):
            errors.append(f"INGRESS_OWNER {label}")

    for identity in sorted(ingresses.keys() - ROUTES.keys()):
        errors.append(f"INGRESS_UNKNOWN {'/'.join(identity)}")
    return errors
