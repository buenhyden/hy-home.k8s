"""Platform assurance rejects unsafe render inputs and false schema claims."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validation/platform/assurance.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("platform_assurance", SCRIPT)
ASSURANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSURANCE)


class PlatformAssuranceTests(unittest.TestCase):
    def test_current_roots_include_example_and_are_closed_local_inputs(self):
        roots = ASSURANCE.discover_roots(ROOT)
        self.assertEqual(len(roots), 14)
        self.assertIn(Path("examples/sample-app"), roots)
        for relative in roots:
            with self.subTest(root=relative):
                ASSURANCE.check_kustomization(ROOT, relative)

    def test_remote_escape_symlink_and_plugin_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "gitops/platform/sample"
            package.mkdir(parents=True)
            manifest = package / "service.yaml"
            manifest.write_text(
                "apiVersion: v1\nkind: Service\nmetadata:\n  name: sample\n"
            )
            kustomization = package / "kustomization.yaml"
            for resources, extra in (
                (["https://example.org/service.yaml"], {}),
                (["../service.yaml"], {}),
                (["service.yaml"], {"generators": ["generator.yaml"]}),
            ):
                kustomization.write_text(
                    json.dumps(
                        {
                            "apiVersion": "kustomize.config.k8s.io/v1beta1",
                            "kind": "Kustomization",
                            "resources": resources,
                            **extra,
                        }
                    )
                )
                with self.assertRaises(ASSURANCE.AssuranceError):
                    ASSURANCE.check_kustomization(root, Path("gitops/platform/sample"))
            manifest.unlink()
            manifest.symlink_to(kustomization)
            kustomization.write_text(
                json.dumps(
                    {
                        "apiVersion": "kustomize.config.k8s.io/v1beta1",
                        "kind": "Kustomization",
                        "resources": ["service.yaml"],
                    }
                )
            )
            with self.assertRaises(ASSURANCE.AssuranceError):
                ASSURANCE.check_kustomization(root, Path("gitops/platform/sample"))

    def test_pinned_schema_rejects_invalid_builtin_and_tamper(self):
        corpus = ROOT / "scripts/validation/platform/schemas"
        schema = ASSURANCE.load_schema(corpus, "apps/v1:Deployment")
        invalid = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "bad"},
            "spec": {"replicas": "not-an-integer"},
        }
        self.assertTrue(ASSURANCE.schema_findings(schema, invalid))
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary)
            (copied / "manifest.json").write_bytes(
                (corpus / "manifest.json").read_bytes()
            )
            (copied / "deployment-apps-v1.json").write_text("{}")
            with self.assertRaises(ASSURANCE.AssuranceError):
                ASSURANCE.load_schema(copied, "apps/v1:Deployment")
            (copied / "deployment-apps-v1.json").write_bytes(
                (corpus / "deployment-apps-v1.json").read_bytes()
            )
            manifest = json.loads((copied / "manifest.json").read_text())
            manifest["schemas"]["v1:Service"] = manifest["schemas"][
                "apps/v1:Deployment"
            ]
            (copied / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaises(ASSURANCE.AssuranceError):
                ASSURANCE.load_schema(copied, "v1:Service")

    def test_unknown_gvk_cannot_become_schema_pass(self):
        self.assertEqual(ASSURANCE.schema_class("example.io/v1:Gadget"), "FAIL")
        self.assertEqual(
            ASSURANCE.schema_class("argoproj.io/v1alpha1:Rollout"), "DEFER"
        )
        self.assertEqual(ASSURANCE.schema_class("v1:Service"), "PASS")

    def test_cross_root_conflict_is_blocking_and_single_result(self):
        first = Path("gitops/platform/a")
        second = Path("gitops/platform/b")
        base = {"apiVersion": "v1", "kind": "ConfigMap", "metadata": {"name": "shared"}}
        changed = {**base, "data": {"key": "different"}}
        with (
            mock.patch.object(
                ASSURANCE, "discover_roots", return_value=[first, second]
            ),
            mock.patch.object(ASSURANCE, "_tool_is_pinned", return_value=True),
            mock.patch.object(ASSURANCE, "_render", side_effect=[[base], [changed]]),
        ):
            rows = ASSURANCE.run(ROOT, Path("/tmp/kustomize"))
        matching = [
            row
            for row in rows
            if row["target"] == second.as_posix() and row["depth"] == "product-semantic"
        ]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["result"], "FAIL")

    def test_project_whitelist_uses_group_and_kind(self):
        control = "gitops/clusters/local"
        workload = "gitops/platform/service"
        project = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "AppProject",
            "metadata": {"name": "platform", "namespace": "argocd"},
            "spec": {
                "clusterResourceWhitelist": [],
                "namespaceResourceWhitelist": [
                    {"group": "argoproj.io", "kind": "AppProject"},
                    {"group": "argoproj.io", "kind": "Application"},
                    {"group": "", "kind": "Service"},
                ],
            },
        }

        def app(path):
            return {
                "apiVersion": "argoproj.io/v1alpha1",
                "kind": "Application",
                "metadata": {"name": path.replace("/", "-"), "namespace": "argocd"},
                "spec": {
                    "project": "platform",
                    "source": {
                        "path": path,
                        "repoURL": "https://github.com/buenhyden/hy-home.k8s.git",
                        "targetRevision": "main",
                    },
                },
            }

        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "sample", "namespace": "apps"},
        }
        rendered = {
            control: [project, app(control), app(workload)],
            workload: [service],
        }
        self.assertEqual(ASSURANCE.validate_project_scope(rendered), set())
        changed = {**service, "apiVersion": "example.io/v1"}
        self.assertEqual(
            ASSURANCE.validate_project_scope(
                {control: rendered[control], workload: [changed]}
            ),
            {workload},
        )
        self.assertEqual(
            ASSURANCE.validate_project_scope(
                {
                    control: [
                        project,
                        app(control),
                        app(workload),
                        app("gitops/platform/missing"),
                    ],
                    workload: [service],
                }
            ),
            {control},
        )
        moved_project = {
            **project,
            "metadata": {**project["metadata"], "namespace": "other"},
        }
        self.assertIn(
            control,
            ASSURANCE.validate_project_scope(
                {
                    control: [moved_project, app(control), app(workload)],
                    workload: [service],
                }
            ),
        )
        wrong_source = app(workload)
        wrong_source["spec"]["source"]["repoURL"] = (
            "https://github.com/example/other.git"
        )
        self.assertIn(
            control,
            ASSURANCE.validate_project_scope(
                {control: [project, app(control), wrong_source], workload: [service]}
            ),
        )
        valid_source = app(workload)["spec"]["source"]
        for spec in (
            {"project": "platform"},
            {"project": "platform", "source": valid_source, "sources": [valid_source]},
            {"project": "platform", "source": {**valid_source, "plugin": {}}},
            {
                "project": "platform",
                "source": {
                    "repoURL": valid_source["repoURL"],
                    "targetRevision": "main",
                },
            },
        ):
            with self.subTest(spec=sorted(spec)):
                unsupported = {**app(workload), "spec": spec}
                self.assertIn(
                    control,
                    ASSURANCE.validate_project_scope(
                        {
                            control: [project, app(control), unsupported],
                            workload: [service],
                        }
                    ),
                )

    def test_workload_generator_requires_local_repo_and_revision(self):
        control = "gitops/clusters/local"
        workload = "gitops/workloads/demo"
        repo = "https://github.com/buenhyden/hy-home.k8s.git"
        project = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "AppProject",
            "metadata": {"name": "platform", "namespace": "argocd"},
            "spec": {
                "clusterResourceWhitelist": [],
                "namespaceResourceWhitelist": [
                    {"group": "argoproj.io", "kind": kind}
                    for kind in ("AppProject", "Application", "ApplicationSet")
                ],
            },
        }
        apps = {
            **project,
            "metadata": {"name": "apps", "namespace": "argocd"},
            "spec": {
                "clusterResourceWhitelist": [],
                "namespaceResourceWhitelist": [{"group": "", "kind": "Service"}],
            },
        }
        app = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {"name": "control", "namespace": "argocd"},
            "spec": {
                "project": "platform",
                "source": {"path": control, "repoURL": repo, "targetRevision": "main"},
            },
        }
        generator = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "ApplicationSet",
            "metadata": {"name": "apps", "namespace": "argocd"},
            "spec": {
                "generators": [
                    {
                        "git": {
                            "repoURL": repo,
                            "revision": "main",
                            "directories": [{"path": "gitops/workloads/*"}],
                        }
                    }
                ],
                "template": {
                    "spec": {
                        "project": "apps",
                        "source": {
                            "path": "{{path}}",
                            "repoURL": repo,
                            "targetRevision": "main",
                        },
                    }
                },
            },
        }
        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "demo", "namespace": "apps"},
        }
        rendered = {control: [project, apps, app, generator], workload: [service]}
        self.assertEqual(ASSURANCE.validate_project_scope(rendered), set())
        bad_generator = {
            **generator,
            "spec": {
                **generator["spec"],
                "generators": [
                    {
                        "git": {
                            **generator["spec"]["generators"][0]["git"],
                            "revision": "old-main",
                        }
                    }
                ],
            },
        }
        self.assertIn(
            control,
            ASSURANCE.validate_project_scope(
                {control: [project, apps, app, bad_generator], workload: [service]}
            ),
        )
        unsupported_generator = copy.deepcopy(generator)
        unsupported_generator["spec"]["template"]["spec"]["sources"] = [
            unsupported_generator["spec"]["template"]["spec"]["source"]
        ]
        self.assertIn(
            control,
            ASSURANCE.validate_project_scope(
                {
                    control: [project, apps, app, unsupported_generator],
                    workload: [service],
                }
            ),
        )


if __name__ == "__main__":
    unittest.main()
