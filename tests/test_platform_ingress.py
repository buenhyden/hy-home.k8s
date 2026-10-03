"""Repository ingress contract: parsed identities and backend ownership."""

import copy
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "platform_ingress", ROOT / "scripts/validation/platform/ingress.py"
)
INGRESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INGRESS)


def desired_documents():
    paths = (
        "gitops/workloads/adminer/ingress.yaml",
        "gitops/workloads/adminer/service.yaml",
        "gitops/platform/cert-manager/cluster-issuer-mkcert.yaml",
        "gitops/platform/headlamp/headlamp-ingress.yaml",
        "gitops/platform/kiali/kiali-ingress.yaml",
        "gitops/platform/ingress-routes/apex-redirects.yaml",
    )
    return [
        doc for name in paths for doc in yaml.safe_load_all((ROOT / name).read_text())
    ]


def ingress(docs, name):
    return next(
        doc
        for doc in docs
        if doc.get("kind") == "Ingress" and doc["metadata"]["name"] == name
    )


def copy_declarations(root):
    paths = (
        "gitops/apps/root/platform-headlamp-app.yaml",
        "gitops/apps/root/platform-kiali-app.yaml",
        "gitops/apps/root/platform-ingress-nginx-app.yaml",
        "gitops/apps/root/platform-rollouts-app.yaml",
        "infrastructure/argocd/values-local.yaml",
    )
    for name in paths:
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)


def change_chart(root, chart, change):
    path = root / f"gitops/apps/root/platform-{chart}-app.yaml"
    app = yaml.safe_load(path.read_text())
    values = yaml.safe_load(app["spec"]["source"]["helm"]["values"])
    change(values)
    app["spec"]["source"]["helm"]["values"] = yaml.safe_dump(values)
    path.write_text(yaml.safe_dump(app))


class PlatformIngressTest(unittest.TestCase):
    def test_current_desired_state(self):
        self.assertEqual(INGRESS.validate(ROOT, desired_documents()), [])

    def test_wrong_api_identity_fails(self):
        docs = copy.deepcopy(desired_documents())
        ingress(docs, "adminer")["apiVersion"] = "extensions/v1beta1"
        self.assertIn("INGRESS_GVK apps/adminer", INGRESS.validate(ROOT, docs))

    def test_backend_port_and_missing_service_fail(self):
        docs = copy.deepcopy(desired_documents())
        ingress(docs, "adminer")["spec"]["rules"][0]["http"]["paths"][0]["backend"][
            "service"
        ]["port"]["number"] = 9000
        self.assertIn("INGRESS_BACKEND apps/adminer", INGRESS.validate(ROOT, docs))
        docs = [doc for doc in desired_documents() if doc.get("kind") != "Service"]
        self.assertIn("INGRESS_OWNER apps/adminer", INGRESS.validate(ROOT, docs))

    def test_ambiguous_backend_port_and_missing_issuer_fail(self):
        docs = copy.deepcopy(desired_documents())
        ingress(docs, "adminer")["spec"]["rules"][0]["http"]["paths"][0]["backend"][
            "service"
        ]["port"]["name"] = "http"
        self.assertIn("INGRESS_BACKEND apps/adminer", INGRESS.validate(ROOT, docs))
        docs = [
            doc for doc in desired_documents() if doc.get("kind") != "ClusterIssuer"
        ]
        self.assertIn(
            "INGRESS_ISSUER_OWNER mkcert-ca-issuer", INGRESS.validate(ROOT, docs)
        )

    def test_apex_path_redirect_and_tls_must_match_identity(self):
        docs = copy.deepcopy(desired_documents())
        item = ingress(docs, "apex-kiali")
        item["spec"]["rules"][0]["http"]["paths"][0]["path"] = "/adminer"
        item["spec"]["tls"][0]["hosts"] = ["wrong.hy-k8s.home.arpa"]
        item["metadata"]["annotations"][
            "nginx.ingress.kubernetes.io/permanent-redirect"
        ] = "https://adminer.hy-k8s.home.arpa/"
        errors = INGRESS.validate(ROOT, docs)
        self.assertIn("INGRESS_ROUTE ingress-nginx/apex-kiali", errors)
        self.assertIn("INGRESS_TLS ingress-nginx/apex-kiali", errors)
        self.assertIn("INGRESS_REDIRECT ingress-nginx/apex-kiali", errors)

    def test_unknown_ingress_fails(self):
        docs = copy.deepcopy(desired_documents())
        item = copy.deepcopy(ingress(docs, "headlamp"))
        item["metadata"]["name"] = "shadow"
        docs.append(item)
        self.assertIn("INGRESS_UNKNOWN headlamp/shadow", INGRESS.validate(ROOT, docs))

    def test_generated_service_and_bootstrap_declarations_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_declarations(root)
            app = root / "gitops/apps/root/platform-headlamp-app.yaml"
            app.write_text(app.read_text().replace("chart: headlamp", "chart: unknown"))
            self.assertIn(
                "INGRESS_OWNER headlamp/headlamp",
                INGRESS.validate(root, desired_documents()),
            )
            shutil.copyfile(ROOT / "gitops/apps/root/platform-headlamp-app.yaml", app)
            argo = root / "infrastructure/argocd/values-local.yaml"
            argo.write_text(
                argo.read_text().replace(
                    "    tls: false",
                    "    tls: false\n    annotations:\n"
                    "      cert-manager.io/cluster-issuer: mkcert-ca-issuer\n"
                    "      nginx.ingress.kubernetes.io/ssl-redirect: 'false'",
                )
            )
            self.assertIn(
                "INGRESS_DECLARATION argocd/bootstrap",
                INGRESS.validate(root, desired_documents()),
            )

    def test_chart_service_generation_controls_fail_closed(self):
        cases = (
            (
                "ingress-nginx",
                lambda v: v["controller"]["service"].update(enabled=False),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v["controller"]["service"].update(
                    external={"enabled": False}
                ),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v["controller"]["service"].update(ports={"http": 81}),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v.update(fullnameOverride="other"),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v["controller"].update(name="other"),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v["controller"].update(allowSnippetAnnotations=True),
                "ingress-nginx/apex-argo",
            ),
            (
                "ingress-nginx",
                lambda v: v["controller"].update(
                    config={"allow-snippet-annotations": "true"}
                ),
                "ingress-nginx/apex-argo",
            ),
            (
                "headlamp",
                lambda v: v.update(fullnameOverride="other"),
                "headlamp/headlamp",
            ),
            (
                "headlamp",
                lambda v: v.update(namespaceOverride="other"),
                "headlamp/headlamp",
            ),
            (
                "headlamp",
                lambda v: v.update(ingress={"enabled": True}),
                "headlamp/headlamp",
            ),
            (
                "headlamp",
                lambda v: v.update(httpRoute={"enabled": True}),
                "headlamp/headlamp",
            ),
            (
                "headlamp",
                lambda v: v.update(extraManifests=["kind: Ingress"]),
                "headlamp/headlamp",
            ),
            ("kiali", lambda v: v["cr"].update(name="other"), "istio-system/kiali"),
            (
                "kiali",
                lambda v: v["cr"].update(namespace="other"),
                "istio-system/kiali",
            ),
            (
                "kiali",
                lambda v: v["cr"]["spec"].update(
                    deployment={"remote_cluster_resources_only": True}
                ),
                "istio-system/kiali",
            ),
            (
                "kiali",
                lambda v: v["cr"]["spec"].update(
                    deployment={"ingress": {"enabled": True}}
                ),
                "istio-system/kiali",
            ),
        )
        for chart, change, identity in cases:
            with (
                self.subTest(chart=chart, identity=identity),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                copy_declarations(root)
                change_chart(root, chart, change)
                self.assertIn(
                    f"INGRESS_OWNER {identity}",
                    INGRESS.validate(root, desired_documents()),
                )

    def test_malformed_ingress_fails_without_exception(self):
        docs = copy.deepcopy(desired_documents())
        ingress(docs, "adminer")["spec"]["rules"] = None
        self.assertIn("INGRESS_ROUTE apps/adminer", INGRESS.validate(ROOT, docs))

    def test_malformed_identity_is_not_echoed(self):
        docs = copy.deepcopy(desired_documents())
        ingress(docs, "adminer")["metadata"]["name"] = "bad\nsecret-value"
        errors = INGRESS.validate(ROOT, docs)
        self.assertIn("INGRESS_IDENTITY malformed", errors)
        self.assertFalse(any("secret-value" in error for error in errors))

    def test_unreviewed_default_backend_and_snippet_fail(self):
        docs = copy.deepcopy(desired_documents())
        item = ingress(docs, "adminer")
        item["spec"]["defaultBackend"] = {
            "service": {"name": "unreviewed", "port": {"number": 8080}}
        }
        item["metadata"]["annotations"][
            "nginx.ingress.kubernetes.io/server-snippet"
        ] = "return 200;"
        errors = INGRESS.validate(ROOT, docs)
        self.assertIn("INGRESS_DEFAULT_BACKEND apps/adminer", errors)
        self.assertIn("INGRESS_ANNOTATION apps/adminer", errors)


if __name__ == "__main__":
    unittest.main()
