"""Parsed ingress cross-references for the current local GitOps platform.

Chart/operator Services are checked against their owner declarations (the Application owns chart version);
this is repository evidence, not a claim that those Services were rendered.
"""

from collections.abc import Iterable, Mapping
from pathlib import Path
import re

import yaml


HOST_SUFFIX = "hy-k8s.home.arpa"
ISSUER = "mkcert-ca-issuer"
ROUTER_ADDRESS = "172.18.0.240"

# The one declaration of the ingress controller identity (SPEC-0119). A
# controller swap edits it in the same change as the manifests.
# Traefik serves IngressClass `nginx` through its Ingress-NGINX provider, so the
# class and the annotation set keep their ingress-nginx names (SPEC-0121).
CONTROLLER = {
    "kind": "traefik",
    "ingressClass": "nginx",
    "namespace": "traefik",
    "application": {
        "name": "traefik",
        "chart": "traefik",
        "repo": "https://traefik.github.io/charts",
        "release": "traefik",
    },
    "service": {
        "name": "traefik",
        "httpPort": 80,
        "nodePorts": {"http": 30080, "https": 30443},
    },
    "annotationPrefix": "nginx.ingress.kubernetes.io/",
    "annotations": {
        "sslRedirect": "ssl-redirect",
        "permanentRedirect": "permanent-redirect",
        "serviceUpstream": "service-upstream",
        "upstreamVhost": "upstream-vhost",
        "appRoot": "app-root",
    },
    "forbiddenSuffix": "-snippet",
}


def _annotation(controller, intent):
    return controller["annotationPrefix"] + controller["annotations"][intent]


def _routes(controller):
    """Identity, route, backend and TLS secret are repository-specific desired state."""
    service = controller["service"]
    return {
        ("apps", "adminer"): ("adminer", "/", "adminer", 8080, "adminer-tls"),
        ("headlamp", "headlamp"): ("headlamp", "/", "headlamp", 4466, "headlamp-tls"),
        ("istio-system", "kiali"): ("kiali", "/kiali", "kiali", 20001, "kiali-tls"),
        **{
            (controller["namespace"], f"apex-{name}"): (
                "",
                f"/{name}",
                service["name"],
                service["httpPort"],
                "hy-k8s-apex-tls",
            )
            for name in ("argo", "kiali", "headlamp", "rollouts", "adminer")
        },
    }


ROUTES = _routes(CONTROLLER)


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


def _chart(root, name, chart, repo, namespace, release=None):
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


def _controller_values_ok(values, controller):
    """Chart value checks specific to the declared controller chart."""
    nodes = controller["service"]["nodePorts"]
    nginx = _get(values, "providers", "kubernetesIngressNGINX")
    web = _get(values, "ports", "web")
    websecure = _get(values, "ports", "websecure")
    return (
        _get(values, "service", "spec", "type") == "LoadBalancer"
        and _get(values, "service", "annotations", "metallb.io/loadBalancerIPs")
        == ROUTER_ADDRESS
        and _get(web, "nodePort") == nodes["http"]
        and _get(websecure, "nodePort") == nodes["https"]
        and _get(web, "exposedPort") in (None, controller["service"]["httpPort"])
        and _get(websecure, "exposedPort") in (None, 443)
        and _get(values, "service", "enabled") in (None, True)
        and _get(values, "service", "single") in (None, True)
        and _get(values, "service", "nameOverride") in (None, "")
        and _get(values, "nameOverride") in (None, "")
        and _get(values, "fullnameOverride") in (None, "")
        and _get(values, "namespaceOverride") in (None, "")
        and _get(values, "ingressClass", "enabled") is False
        and _get(values, "providers", "kubernetesCRD", "enabled") is False
        and _get(values, "providers", "kubernetesIngress", "enabled") is False
        and _get(nginx, "enabled") is True
        and _get(nginx, "ingressClass") in (None, controller["ingressClass"])
        and _get(nginx, "controllerClass") in (None, "k8s.io/ingress-nginx")
        and _get(nginx, "allowSnippetAnnotations") in (None, False)
        and _get(nginx, "publishService", "enabled") is True
        and _get(nginx, "proxyRequestBuffering") is True
        and _get(web, "http", "aliasHeadersStrategy") == "delete"
        and _get(websecure, "http", "aliasHeadersStrategy") == "delete"
        and "hsts@file" in (_get(websecure, "http", "middlewares") or ())
        and _get(
            values,
            "providers",
            "file",
            "content",
            "http",
            "middlewares",
            "hsts",
            "headers",
            "stsSeconds",
        )
        == 31536000
    )


def _owner_declarations(root, controller):
    headlamp = _chart(
        root,
        "headlamp",
        "headlamp",
        "https://kubernetes-sigs.github.io/headlamp/",
        "headlamp",
    )
    kiali = _chart(
        root,
        "kiali",
        "kiali-operator",
        "https://kiali.org/helm-charts",
        "istio-system",
    )
    app = controller["application"]
    values = _chart(
        root,
        app["name"],
        app["chart"],
        app["repo"],
        controller["namespace"],
        app["release"],
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
        (
            controller["namespace"],
            controller["service"]["name"],
            controller["service"]["httpPort"],
        ): _controller_values_ok(values, controller)
        if controller["kind"] == "traefik"
        else values is not None,
    }


def _declared_ingresses(root, controller):
    errors = []
    argo = _load(root, "infrastructure/argocd/values-local.yaml")
    argo_ingress = _get(argo, "server", "ingress")
    argo_tls = _one(_get(argo_ingress, "extraTls"))
    argo_host = f"argo.{HOST_SUFFIX}"
    if not all(
        (
            _get(argo, "global", "domain") == argo_host,
            _get(argo_ingress, "enabled") is True,
            _get(argo_ingress, "ingressClassName") == controller["ingressClass"],
            _get(argo_ingress, "hostname") == argo_host,
            _get(argo_ingress, "tls") is False,
            _get(argo_tls, "hosts") == [argo_host],
            _get(argo_tls, "secretName") == "argocd-local-tls",
            _get(argo_ingress, "annotations", "cert-manager.io/cluster-issuer") is None,
            _get(argo_ingress, "annotations", _annotation(controller, "sslRedirect"))
            in (None, "true"),
        )
    ):
        errors.append("INGRESS_DECLARATION argocd/bootstrap")

    rollouts = _chart(
        root,
        "rollouts",
        "argo-rollouts",
        "https://argoproj.github.io/argo-helm",
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
            _get(ingress, "ingressClassName") == controller["ingressClass"],
            _get(ingress, "hosts") == [host],
            _get(tls, "hosts") == [host],
            _get(tls, "secretName") == "rollouts-dashboard-tls",
            _get(ingress, "annotations", "cert-manager.io/cluster-issuer") == ISSUER,
            _get(ingress, "annotations", _annotation(controller, "sslRedirect"))
            == "true",
        )
    ):
        errors.append("INGRESS_DECLARATION argo-rollouts/dashboard")
    return errors


def validate(
    root: Path, rendered_documents: Iterable[Mapping], controller=CONTROLLER
) -> list[str]:
    """Return fixed-code findings; never include untrusted manifest values."""
    errors = []
    routes = _routes(controller)
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
    owners = _owner_declarations(root, controller)
    errors.extend(_declared_ingresses(root, controller))
    for identity, (subdomain, path, service, port, secret) in routes.items():
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
                _get(doc, "spec", "ingressClassName") == controller["ingressClass"],
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
            and key.startswith(controller["annotationPrefix"])
            and key.endswith(controller["forbiddenSuffix"])
            for key in annotations
        ):
            errors.append(f"INGRESS_ANNOTATION {label}")
        apex = identity[0] == controller["namespace"]
        expected_redirect = (
            f"https://{identity[1][5:]}.{HOST_SUFFIX}/" if apex else None
        )
        if (
            _get(annotations, _annotation(controller, "sslRedirect")) != "true"
            or _get(annotations, _annotation(controller, "permanentRedirect"))
            != expected_redirect
        ):
            errors.append(f"INGRESS_REDIRECT {label}")
        expected_issuer = ISSUER if not apex or identity[1] == "apex-argo" else None
        if _get(annotations, "cert-manager.io/cluster-issuer") != expected_issuer:
            errors.append(f"INGRESS_ISSUER {label}")
        if identity == ("apps", "adminer"):
            if (
                _get(annotations, _annotation(controller, "serviceUpstream")) != "true"
                or _get(annotations, _annotation(controller, "upstreamVhost"))
                != "adminer.apps.svc.cluster.local"
            ):
                errors.append(f"INGRESS_MESH {label}")
        elif (
            identity == ("istio-system", "kiali")
            and _get(annotations, _annotation(controller, "appRoot")) != "/kiali"
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

    for identity in sorted(ingresses.keys() - routes.keys()):
        errors.append(f"INGRESS_UNKNOWN {'/'.join(identity)}")
    return errors
