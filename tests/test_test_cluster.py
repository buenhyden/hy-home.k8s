"""Workspace-owned test cluster contract (W09-ENV): selective, isolated, owned."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "test_cluster", ROOT / "scripts/test_cluster.py"
)
assert SPEC is not None and SPEC.loader is not None
CLUSTER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLUSTER
SPEC.loader.exec_module(CLUSTER)


def application(name: str, source: dict) -> str:
    return json.dumps(
        {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {"name": name, "namespace": "argocd"},
            "spec": {"source": source, "destination": {"namespace": "x"}},
        }
    )


RENDERED = {
    "gitops/platform/namespaces": [
        {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "apps"}},
        {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "platform"}},
    ],
    "gitops/platform/network-policies": [
        {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": "p", "namespace": "apps"},
        }
    ],
    "gitops/platform/eso": [
        {
            "apiVersion": "external-secrets.io/v1",
            "kind": "ExternalSecret",
            "metadata": {"name": "s", "namespace": "apps"},
        }
    ],
    "gitops/clusters/local": [
        {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "ApplicationSet",
            "metadata": {"name": "workloads", "namespace": "argocd"},
        }
    ],
    "gitops/platform/orphan": [
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "c", "namespace": "nowhere"},
        }
    ],
}


def clusters(*names: str) -> list[dict]:
    return [{"name": name} for name in names]


class TestClusterTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="test-cluster-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        apps = self.root / "gitops/apps/root"
        apps.mkdir(parents=True)
        for name, source in {
            "platform-namespaces": {"path": "gitops/platform/namespaces"},
            "platform-network-policies": {"path": "gitops/platform/network-policies"},
            "platform-eso-config": {"path": "gitops/platform/eso"},
            "platform-cert-manager": {"chart": "cert-manager"},
            "platform-cluster-config": {"path": "gitops/clusters/local"},
            "platform-orphan": {"path": "gitops/platform/orphan"},
        }.items():
            (apps / f"{name}-app.yaml").write_text(application(name, source))
        render = mock.patch.object(
            CLUSTER, "render", side_effect=lambda root, path: RENDERED[path]
        )
        render.start()
        self.addCleanup(render.stop)
        sleep = mock.patch.object(CLUSTER.time, "sleep")
        sleep.start()
        self.addCleanup(sleep.stop)
        self.catalog = CLUSTER.catalog(self.root)

    def state(self, run: str, **extra) -> None:
        directory = self.root / ".workspace-test" / run
        directory.mkdir(parents=True)
        (directory / "state.json").write_text(
            json.dumps(
                {
                    "run_id": run,
                    "cluster": f"hyk8s-test-{run}",
                    "authority": "fixture:approval",
                }
                | extra
            )
        )

    def test_plan_adds_the_namespace_provider_in_order(self) -> None:
        plan = CLUSTER.plan(self.catalog, ["platform-network-policies"])
        self.assertEqual(plan, ["platform-namespaces", "platform-network-policies"])

    def test_plan_refuses_whole_or_unsupported_selections(self) -> None:
        for selection, code in (
            ([], "SELECTION_EMPTY"),
            (["all"], "SELECTION_WHOLE"),
            (["*"], "SELECTION_WHOLE"),
            (["platform-*"], "SELECTION_WHOLE"),
            (["platform-cluster-config"], "SELECTION_ROOT"),
            (["platform-cert-manager"], "SELECTION_UNSUPPORTED"),
            (["platform-eso-config"], "SELECTION_UNSUPPORTED"),
            (["platform-orphan"], "SELECTION_UNSUPPORTED"),
            (["missing"], "SELECTION_UNKNOWN"),
        ):
            with self.subTest(selection=selection):
                with self.assertRaisesRegex(CLUSTER.ClusterError, code):
                    CLUSTER.plan(self.catalog, selection)

    def test_plan_refuses_a_closure_over_the_limit(self) -> None:
        with mock.patch.object(CLUSTER, "APP_LIMIT", 1):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "SELECTION_LIMIT"):
                CLUSTER.plan(self.catalog, ["platform-network-policies"])

    def test_cluster_command_binds_loopback_and_never_the_default_kubeconfig(
        self,
    ) -> None:
        command = CLUSTER.create_command("hyk8s-test-abc12345", "abc12345", 40123)
        text = " ".join(command)
        self.assertIn("--api-port 127.0.0.1:40123", text)
        self.assertIn("--no-lb", command)
        self.assertIn("--kubeconfig-update-default=false", command)
        self.assertIn("--kubeconfig-switch-context=false", command)
        self.assertIn("--agents 0", text)
        self.assertIn("hy-home.k8s/run=abc12345", text)
        for forbidden in ("192.168.", "0.0.0.0", "--port", "--volume", "secrets"):
            self.assertNotIn(forbidden, text)

    def test_tools_run_with_the_run_kubeconfig_only(self) -> None:
        state = self.root / ".workspace-test" / "abc12345"
        environment = CLUSTER.tool_environment(
            state, {"KUBECONFIG": "/home/u/.kube/config", "PATH": "/usr/bin"}
        )
        self.assertEqual(environment["KUBECONFIG"], str(state / "kubeconfig"))
        self.assertNotIn("/home/u/.kube/config", json.dumps(environment))

    def test_down_deletes_only_an_owned_cluster(self) -> None:
        self.state("abc12345")
        listed = clusters("hyk8s-test-abc12345", "hyhome", "hyk8s-test-ffff0000")
        labels = {"hyk8s-test-abc12345": "abc12345", "hyk8s-test-ffff0000": "ffff0000"}
        calls = []
        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=listed),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(
                CLUSTER, "_run", side_effect=lambda command, **kw: calls.append(command)
            ),
        ):
            CLUSTER.down(self.root, "abc12345")
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_NOT_OWNED"):
                CLUSTER.down(self.root, "ffff0000")
        self.assertEqual(calls, [["k3d", "cluster", "delete", "hyk8s-test-abc12345"]])
        self.assertFalse((self.root / ".workspace-test" / "abc12345").exists())

    def test_sweep_removes_owned_orphans_and_leaves_others(self) -> None:
        self.state("dead0001", pid=999999999)
        listed = clusters("hyk8s-test-dead0001", "hyk8s-test-gone0002", "hyhome")
        labels = {"hyk8s-test-dead0001": "dead0001", "hyk8s-test-gone0002": "gone0002"}
        calls = []
        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=listed),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(
                CLUSTER, "_run", side_effect=lambda command, **kw: calls.append(command)
            ),
        ):
            result = CLUSTER.sweep(self.root)
        self.assertEqual(calls, [["k3d", "cluster", "delete", "hyk8s-test-dead0001"]])
        self.assertEqual(result["unowned"], ["hyk8s-test-gone0002"])

    def test_up_deletes_its_cluster_when_a_step_fails(self) -> None:
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            if command[:2] == ["kubectl", "apply"]:
                raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: apply")
            return ""

        with (
            mock.patch.object(CLUSTER, "_run", side_effect=run),
            mock.patch.object(CLUSTER, "_write_kubeconfig"),
            mock.patch.object(CLUSTER, "_verify_loopback"),
            mock.patch.object(CLUSTER, "list_clusters", return_value=[]),
            mock.patch.object(CLUSTER, "free_port", return_value=40123),
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_STEP_FAILED"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                )
        self.assertEqual(calls[-1], ["k3d", "cluster", "delete", "hyk8s-test-abc12345"])
        self.assertFalse((self.root / ".workspace-test" / "abc12345").exists())

    def test_up_names_its_authority_or_is_refused_before_any_action(self) -> None:
        with mock.patch.object(CLUSTER, "_run") as run:
            for authority in (None, "", "   ", 123):
                with self.subTest(authority=authority):
                    with self.assertRaisesRegex(
                        CLUSTER.ClusterError, "CLUSTER_AUTHORITY"
                    ):
                        CLUSTER.up(
                            self.root,
                            ["platform-network-policies"],
                            run_id="abc12345",
                            authority=authority,
                        )
            run.assert_not_called()
        self.assertFalse((self.root / ".workspace-test" / "abc12345").exists())
        # Mocked so a regression can never reach a real cluster tool.
        with (
            mock.patch.object(
                CLUSTER, "_run", side_effect=AssertionError("live tool reached")
            ),
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
            self.assertRaises(SystemExit) as exited,
        ):
            CLUSTER.main(["--root", str(self.root), "up", "platform-network-policies"])
        self.assertEqual(exited.exception.code, 2)
        self.assertIn("--authority", stderr.getvalue())

    def test_probe_refuses_a_run_that_names_no_authority(self) -> None:
        self.state("abc12345", authority=None)
        with mock.patch.object(CLUSTER, "_run") as run:
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_AUTHORITY"):
                CLUSTER.probe(
                    self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24"
                )
        run.assert_not_called()

    def test_labels_are_read_from_the_node_containers(self) -> None:
        output = "hyk8s-test-abc12345 abc12345\nhyk8s-test-abc12345 abc12345\n"
        with mock.patch.object(CLUSTER, "_run", return_value=output) as run:
            self.assertEqual(
                CLUSTER.labelled_runs(), {"hyk8s-test-abc12345": "abc12345"}
            )
        command = run.call_args.args[0]
        self.assertEqual(command[:4], ["docker", "ps", "-a", "--filter"])
        self.assertIn("label=hy-home.k8s/run", command)

    def test_probe_reads_the_pod_result_and_requires_a_closed_port_control(
        self,
    ) -> None:
        self.state("abc12345")
        outcomes = {
            ("hyk8s-probe-open", "443"): "rc=0",
            ("hyk8s-probe-open", "1"): "rc=1",
            ("hyk8s-probe-denied", "443"): "rc=1",
        }

        def run(command, **kwargs):
            if command[:2] == ["kubectl", "run"]:
                namespace = command[command.index("-n") + 1]
                return outcomes[(namespace, command[-1])]
            return ""

        with mock.patch.object(CLUSTER, "_run", side_effect=run):
            result = CLUSTER.probe(
                self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24"
            )
        self.assertEqual((result["valid"], result["denied"]), (True, True))
        outcomes[("hyk8s-probe-open", "1")] = "rc=0"
        with mock.patch.object(CLUSTER, "_run", side_effect=run):
            result = CLUSTER.probe(
                self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24"
            )
        self.assertEqual(result["valid"], False)

    def test_a_failed_delete_leaves_state_that_sweep_can_reclaim(self) -> None:
        def run(command, **kwargs):
            if command[:2] == ["kubectl", "apply"] or command[:3] == [
                "k3d",
                "cluster",
                "delete",
            ]:
                raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: step")
            return ""

        with (
            mock.patch.object(CLUSTER, "_run", side_effect=run),
            mock.patch.object(CLUSTER, "_write_kubeconfig"),
            mock.patch.object(CLUSTER, "_verify_loopback"),
            mock.patch.object(
                CLUSTER,
                "list_clusters",
                side_effect=[[], clusters("hyk8s-test-abc12345")],
            ),
            mock.patch.object(CLUSTER, "free_port", return_value=40123),
        ):
            with self.assertRaises(CLUSTER.ClusterError):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority=" fixture:approval ",
                )
        record = json.loads(
            (self.root / ".workspace-test/abc12345/state.json").read_text()
        )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["authority"], "fixture:approval")

    def test_up_refuses_a_name_that_already_exists(self) -> None:
        with (
            mock.patch.object(
                CLUSTER, "list_clusters", return_value=clusters("hyk8s-test-abc12345")
            ),
            mock.patch.object(CLUSTER, "_run") as run,
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_EXISTS"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                )
        run.assert_not_called()

    def test_run_ids_are_short_ascii(self) -> None:
        for bad in ("abc", "ABC12345", "\u00e9bc12345", "a" * 9, "../x"):
            with self.subTest(run_id=bad):
                with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_SCHEMA"):
                    CLUSTER._state_dir(self.root, bad)

    def test_a_dependency_cycle_is_a_stable_error(self) -> None:
        apps = {
            "a": {"status": "supported", "requires": ["b"], "reason": None},
            "b": {"status": "supported", "requires": ["a"], "reason": None},
        }
        with self.assertRaisesRegex(CLUSTER.ClusterError, "SELECTION_CYCLE"):
            CLUSTER.plan(apps, ["a"])

    def test_probe_without_a_pod_result_is_invalid_and_targets_are_validated(
        self,
    ) -> None:
        self.state("abc12345")

        def run(command, **kwargs):
            if command[:2] == ["kubectl", "run"]:
                namespace = command[command.index("-n") + 1]
                port = command[-1]
                if namespace == "hyk8s-probe-denied":
                    return ""
                return "rc=0" if port == "443" else "rc=1"
            return ""

        with mock.patch.object(CLUSTER, "_run", side_effect=run):
            result = CLUSTER.probe(
                self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24"
            )
        self.assertEqual((result["valid"], result["denied"]), (False, False))
        commands = []
        with mock.patch.object(
            CLUSTER, "_run", side_effect=lambda c, **k: commands.append(c) or "rc=0\r\n"
        ):
            CLUSTER.probe(self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24")
        script = [c for c in commands if c[:2] == ["kubectl", "run"]][0]
        self.assertTrue(script[script.index("-c") + 1].startswith("sleep 2;"))
        for target in ("x; echo rc=0 #:443", "-e:443", "host", "h:port"):
            with self.subTest(target=target):
                with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_SCHEMA"):
                    CLUSTER.probe(self.root, "abc12345", target, "192.168.0.0/24")

    def test_sweep_continues_reports_live_runs_and_drops_stale_state(self) -> None:
        self.state("dead0001", pid=999999999)
        self.state("live0002", pid=999999999, status="up")
        self.state("lost0003", pid=999999999)
        listed = clusters("hyk8s-test-dead0001", "hyk8s-test-live0002")
        labels = {"hyk8s-test-dead0001": "dead0001", "hyk8s-test-live0002": "live0002"}

        def run(command, **kwargs):
            raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: delete")

        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=listed),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(CLUSTER, "_run", side_effect=run),
        ):
            result = CLUSTER.sweep(self.root)
        self.assertEqual(result["failed"], ["hyk8s-test-dead0001"])
        self.assertEqual(result["kept"], ["hyk8s-test-live0002"])
        self.assertFalse((self.root / ".workspace-test/lost0003").exists())

    def test_status_skips_foreign_names_and_checks_labels(self) -> None:
        self.state("abc12345")
        listed = clusters(
            "hyk8s-test-abc12345", "hyk8s-test-a-b", "hyk8s-test-def67890"
        )
        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=listed),
            mock.patch.object(CLUSTER, "labelled_runs", return_value={}),
        ):
            result = CLUSTER.status(self.root)
        self.assertEqual(
            result,
            [
                {"name": "hyk8s-test-abc12345", "owned": False},
                {"name": "hyk8s-test-a-b", "owned": False},
                {"name": "hyk8s-test-def67890", "owned": False},
            ],
        )

    def test_probe_waits_for_each_namespace_service_account(self) -> None:
        self.state("abc12345")
        commands = []

        def run(command, **kwargs):
            commands.append(command)
            if command[:3] == ["kubectl", "get", "serviceaccount"]:
                waits = sum(1 for c in commands if c[:3] == command[:3])
                if waits < 2:
                    raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: not found")
                return "default"
            return "rc=1"

        with (
            mock.patch.object(CLUSTER, "_run", side_effect=run),
            mock.patch.object(CLUSTER.time, "sleep"),
        ):
            CLUSTER.probe(self.root, "abc12345", "192.168.0.13:443", "192.168.0.0/24")
        first_run = next(
            i for i, c in enumerate(commands) if c[:2] == ["kubectl", "run"]
        )
        waited = [
            c
            for c in commands[:first_run]
            if c[:3] == ["kubectl", "get", "serviceaccount"]
        ]
        self.assertGreaterEqual(len(waited), 3)

    def test_probe_policy_denies_the_production_lan_and_allows_dns(self) -> None:
        policy = CLUSTER.probe_policy("192.168.0.0/24")
        self.assertEqual(policy["spec"]["policyTypes"], ["Egress"])
        destinations = [to for rule in policy["spec"]["egress"] for to in rule["to"]]
        self.assertIn(
            {"ipBlock": {"cidr": "0.0.0.0/0", "except": ["192.168.0.0/24"]}},
            destinations,
        )


if __name__ == "__main__":
    unittest.main()
