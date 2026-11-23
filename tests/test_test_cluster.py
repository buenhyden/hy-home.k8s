"""Workspace-owned test cluster contract (W09-ENV): selective, isolated, owned."""

from __future__ import annotations

import importlib.util
import importlib
import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
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


def git_init(root: Path) -> None:
    subprocess.run(
        ["/usr/bin/git", "init", "--quiet", str(root)],
        check=True,
        capture_output=True,
        timeout=10,
    )


class TestClusterTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="test-cluster-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        git_init(self.root)
        self.admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=self.root / "admission-state"
        )
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
        record = {
            "run_id": run,
            "cluster": f"hyk8s-test-{run}",
            "authority": "fixture:approval",
        } | extra
        (directory / "state.json").write_text(json.dumps(record))

    def lease(self, run: str) -> str:
        return self.admission.reserve(
            run,
            "cluster",
            ["platform-namespaces"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": f"hyk8s-test-{run}", "pid": 999999999, "start_ticks": 1},
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
        command = CLUSTER.create_command(
            "hyk8s-test-abc12345", "abc12345", 40123, "hyk8s-owned-abc12345"
        )
        text = " ".join(command)
        self.assertIn("--api-port 127.0.0.1:40123", text)
        self.assertIn("--no-lb", command)
        self.assertIn("--kubeconfig-update-default=false", command)
        self.assertIn("--kubeconfig-switch-context=false", command)
        self.assertIn("--agents 0", text)
        self.assertIn("hy-home.k8s/run=abc12345", text)
        self.assertIn("--network hyk8s-owned-abc12345", text)
        self.assertIn("--servers-memory", command)
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
        self.state("abc12345", admission_token=self.lease("abc12345"))
        listed = {"hyk8s-test-abc12345", "hyhome", "hyk8s-test-ffff0000"}
        labels = {"hyk8s-test-abc12345": "abc12345", "hyk8s-test-ffff0000": "ffff0000"}
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            if command[:3] == ["k3d", "cluster", "delete"]:
                listed.discard(command[3])
            return ""

        with (
            mock.patch.object(
                CLUSTER, "list_clusters", side_effect=lambda: clusters(*sorted(listed))
            ),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(CLUSTER, "_run", side_effect=run),
        ):
            CLUSTER.down(self.root, "abc12345", admission=self.admission)
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_NOT_OWNED"):
                CLUSTER.down(self.root, "ffff0000", admission=self.admission)
        self.assertEqual(
            [call for call in calls if call[:3] == ["k3d", "cluster", "delete"]],
            [["k3d", "cluster", "delete", "hyk8s-test-abc12345"]],
        )
        self.assertFalse((self.root / ".workspace-test" / "abc12345").exists())

    def test_sweep_removes_owned_orphans_and_leaves_others(self) -> None:
        self.state(
            "dead0001",
            pid=999999999,
            pid_start_ticks=1,
            admission_token=self.lease("dead0001"),
        )
        listed = {"hyk8s-test-dead0001", "hyk8s-test-gone0002", "hyhome"}
        labels = {"hyk8s-test-dead0001": "dead0001", "hyk8s-test-gone0002": "gone0002"}
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            if command[:3] == ["k3d", "cluster", "delete"]:
                listed.discard(command[3])
            return ""

        with (
            mock.patch.object(
                CLUSTER, "list_clusters", side_effect=lambda: clusters(*sorted(listed))
            ),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(CLUSTER, "_run", side_effect=run),
        ):
            result = CLUSTER.sweep(self.root, admission=self.admission)
        self.assertEqual(
            [call for call in calls if call[:3] == ["k3d", "cluster", "delete"]],
            [["k3d", "cluster", "delete", "hyk8s-test-dead0001"]],
        )
        self.assertEqual(result["unowned"], ["hyk8s-test-gone0002"])

    def test_up_deletes_its_cluster_when_a_step_fails(self) -> None:
        calls = []
        listed = set()
        networks = set()
        network = "hyk8s-owned-abc12345"

        def run(command, **kwargs):
            calls.append(command)
            if command[:3] == ["docker", "network", "create"]:
                networks.add(command[-1])
            if command[:3] == ["docker", "network", "inspect"]:
                return json.dumps(
                    {
                        "Name": network,
                        "Driver": "bridge",
                        "Internal": True,
                        "EnableIPv6": False,
                        "Options": {
                            "com.docker.network.bridge.gateway_mode_ipv4": "isolated"
                        },
                        "Labels": {"hy-home.k8s/run": "abc12345"},
                    }
                )
            if command[:2] == ["docker", "inspect"]:
                if any("NanoCpus" in item for item in command):
                    return "2000000000"
                return json.dumps({network: {}})
            if command[:3] == ["docker", "network", "ls"]:
                return "\n".join(sorted(networks))
            if command[:3] == ["k3d", "cluster", "create"]:
                listed.add(command[3])
            if command[:2] == ["kubectl", "apply"]:
                raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: apply")
            if command[:3] == ["k3d", "cluster", "delete"]:
                listed.discard(command[3])
            if command[:3] == ["docker", "network", "rm"]:
                networks.discard(command[3])
            return ""

        with (
            mock.patch.object(CLUSTER, "_run", side_effect=run),
            mock.patch.object(CLUSTER, "_write_kubeconfig"),
            mock.patch.object(CLUSTER, "_verify_loopback"),
            mock.patch.object(CLUSTER.CLUSTER_ENV, "arm_expiry_timer"),
            mock.patch.object(CLUSTER.CLUSTER_ENV, "require_product_disk_cap"),
            mock.patch.object(
                CLUSTER, "list_clusters", side_effect=lambda: clusters(*sorted(listed))
            ),
            mock.patch.object(
                CLUSTER,
                "labelled_runs",
                side_effect=lambda: {name: "abc12345" for name in listed},
            ),
            mock.patch.object(CLUSTER, "free_port", return_value=40123),
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_STEP_FAILED"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                    admission=self.admission,
                )
        self.assertIn(["k3d", "cluster", "delete", "hyk8s-test-abc12345"], calls)
        self.assertIn(["docker", "network", "rm", network], calls)
        first_apply = next(
            i for i, command in enumerate(calls) if command[:2] == ["kubectl", "apply"]
        )
        self.assertTrue(
            any(c[:3] == ["docker", "update", "--cpus=2"] for c in calls[:first_apply])
        )
        self.assertTrue(
            any(
                c[:2] == ["docker", "inspect"] and "NanoCpus" in " ".join(c)
                for c in calls[:first_apply]
            )
        )
        self.assertFalse((self.root / ".workspace-test" / "abc12345").exists())
        self.assertEqual(self.admission.active_for_run("abc12345"), [])

    def test_up_refuses_network_creation_if_expiry_timer_is_unverified(self) -> None:
        calls = []
        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=[]),
            mock.patch.object(CLUSTER.CLUSTER_ENV, "require_product_disk_cap"),
            mock.patch.object(
                CLUSTER.CLUSTER_ENV,
                "arm_expiry_timer",
                side_effect=ValueError("CLUSTER_TIMER: unavailable"),
                create=True,
            ),
            mock.patch.object(
                CLUSTER,
                "_run",
                side_effect=lambda command, **kw: calls.append(command) or "",
            ),
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_TIMER"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                    admission=self.admission,
                )
        self.assertFalse(
            any(
                command[:3]
                in (["docker", "network", "create"], ["k3d", "cluster", "create"])
                for command in calls
            )
        )
        self.assertEqual(self.admission.active_for_run("abc12345"), [])

    def test_timer_must_be_active_and_stale_token_cannot_delete_new_run(self) -> None:
        commands = []

        def run(command, **kwargs):
            commands.append(command)
            return "yes" if command[0] == "loginctl" else "inactive"

        with mock.patch.object(CLUSTER.CLUSTER_ENV, "_user_bus", return_value={}):
            with self.assertRaisesRegex(ValueError, "CLUSTER_TIMER"):
                CLUSTER.CLUSTER_ENV.arm_expiry_timer(
                    run, self.root, "abc12345", "0" * 32, 60
                )
        self.assertTrue(any(command[0] == "systemctl" for command in commands))
        token = self.admission.reserve(
            "abc12345",
            "cluster",
            ["platform-namespaces"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": "hyk8s-test-abc12345"},
        )
        self.state("abc12345", status="up", admission_token=token)
        with mock.patch.object(CLUSTER, "_run") as external:
            self.assertEqual(
                CLUSTER.expire(
                    self.root, "abc12345", "0" * 32, admission=self.admission
                ),
                {"kept": "abc12345"},
            )
        external.assert_not_called()
        self.assertEqual(self.admission.active_for_run("abc12345")[0]["token"], token)

    def test_direct_up_obeys_a_worker_reservation_before_any_external_action(
        self,
    ) -> None:
        admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=self.root / "admission-state"
        )
        budget = {
            "cpu": 1,
            "memory_mib": 512,
            "disk_mib": 512,
            "seconds": 60,
            "instances": 0,
        }
        admission.reserve(
            "worker001", "worker", ["w", "x", "y", "z"], budget, {"worker": "fixture"}
        )
        with (
            mock.patch.object(CLUSTER, "_run") as external,
            mock.patch.object(CLUSTER.CLUSTER_ENV, "require_product_disk_cap"),
        ):
            with self.assertRaisesRegex(Exception, "ENV_LIMIT"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                    admission=admission,
                )
        external.assert_not_called()

    def test_product_workload_cannot_start_without_a_proven_disk_cap(self) -> None:
        app = self.root / "gitops/apps/root/product-demo-app.yaml"
        app.write_text(application("product-demo", {"path": "gitops/product/demo"}))
        pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "demo", "namespace": "apps"},
        }
        admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=self.root / "admission-state"
        )

        def render(root, path):
            return [pod] if path == "gitops/product/demo" else RENDERED[path]

        with (
            mock.patch.object(CLUSTER, "render", side_effect=render),
            mock.patch.object(CLUSTER, "_run", return_value="") as external,
        ):
            for selected in ("product-demo", "platform-network-policies"):
                with (
                    self.subTest(selected=selected),
                    self.assertRaisesRegex(Exception, "CLUSTER_DISK_LIMIT"),
                ):
                    CLUSTER.up(
                        self.root,
                        [selected],
                        run_id="abc12345",
                        authority="fixture:approval",
                        admission=admission,
                    )
        self.assertFalse(
            any(
                call.args[0][:3]
                in (
                    ["k3d", "cluster", "create"],
                    ["docker", "network", "create"],
                    ["kubectl", "apply", "-k"],
                )
                for call in external.call_args_list
            )
        )
        self.assertEqual(admission.active_for_run("abc12345"), [])

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
                            admission=self.admission,
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
            mock.patch.object(CLUSTER.CLUSTER_ENV, "require_product_disk_cap"),
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
                    admission=self.admission,
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
            mock.patch.object(CLUSTER, "labelled_runs", return_value={}),
            mock.patch.object(CLUSTER.CLUSTER_ENV, "require_product_disk_cap"),
            mock.patch.object(CLUSTER, "_run") as run,
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_EXISTS"):
                CLUSTER.up(
                    self.root,
                    ["platform-network-policies"],
                    run_id="abc12345",
                    authority="fixture:approval",
                    admission=self.admission,
                )
        run.assert_not_called()

    def test_down_keeps_a_lease_when_owned_resources_remain_unverified(self) -> None:
        run_id = "abc12345"
        token = self.admission.reserve(
            run_id,
            "cluster",
            ["platform-namespaces"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": "hyk8s-test-abc12345"},
        )
        self.state(run_id, status="up", admission_token=token)
        with (
            mock.patch.object(
                CLUSTER, "list_clusters", return_value=clusters("hyk8s-test-abc12345")
            ),
            mock.patch.object(
                CLUSTER, "labelled_runs", return_value={"hyk8s-test-abc12345": run_id}
            ),
            mock.patch.object(CLUSTER, "_run", return_value=""),
        ):
            with self.assertRaisesRegex(CLUSTER.ClusterError, "CLUSTER_CLEANUP"):
                CLUSTER.down(self.root, run_id, admission=self.admission)
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

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
        self.state(
            "dead0001",
            pid=999999999,
            pid_start_ticks=1,
            admission_token=self.lease("dead0001"),
        )
        self.state("live0002", pid=999999999, status="up")
        self.state("lost0003", pid=999999999, pid_start_ticks=1)
        listed = clusters("hyk8s-test-dead0001", "hyk8s-test-live0002")
        labels = {"hyk8s-test-dead0001": "dead0001", "hyk8s-test-live0002": "live0002"}

        def run(command, **kwargs):
            raise CLUSTER.ClusterError("CLUSTER_STEP_FAILED: delete")

        with (
            mock.patch.object(CLUSTER, "list_clusters", return_value=listed),
            mock.patch.object(CLUSTER, "labelled_runs", return_value=labels),
            mock.patch.object(CLUSTER, "_run", side_effect=run),
        ):
            result = CLUSTER.sweep(self.root, admission=self.admission)
        self.assertEqual(result["failed"], ["hyk8s-test-dead0001"])
        self.assertEqual(result["kept"], ["hyk8s-test-live0002"])
        self.assertTrue((self.root / ".workspace-test/lost0003").exists())

    def test_sweep_expires_only_the_owned_run_and_recovers_intent_only_lease(
        self,
    ) -> None:
        expired, future = "expired1", "future01"
        self.state(
            expired,
            status="up",
            expires_at=0,
            pid=999999999,
            admission_token=self.lease(expired),
        )
        self.state(future, status="up", expires_at=time.time() + 60, pid=999999999)
        intent_token = self.admission.reserve(
            "intent01",
            "cluster",
            ["platform-namespaces"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": "hyk8s-test-intent01", "pid": 99999999, "start_ticks": 1},
        )
        listed = {"hyk8s-test-expired1", "hyk8s-test-future01"}

        def run(command, **kwargs):
            if command[:3] == ["k3d", "cluster", "delete"]:
                listed.discard(command[3])
            return ""

        with (
            mock.patch.object(
                CLUSTER, "list_clusters", side_effect=lambda: clusters(*sorted(listed))
            ),
            mock.patch.object(
                CLUSTER,
                "labelled_runs",
                return_value={
                    "hyk8s-test-expired1": expired,
                    "hyk8s-test-future01": future,
                },
            ),
            mock.patch.object(CLUSTER, "_run", side_effect=run),
        ):
            result = CLUSTER.sweep(self.root, admission=self.admission)
        self.assertEqual(result["deleted"], ["hyk8s-test-expired1"])
        self.assertEqual(result["kept"], ["hyk8s-test-future01"])
        self.assertEqual(self.admission.active_for_run("intent01"), [])
        self.assertFalse(self.admission.child_receipt_path(intent_token).exists())

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


class AdmissionTest(unittest.TestCase):
    def test_distinct_repositories_share_limits_and_unknown_absence_keeps_a_lease(self):
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="admission-shared-") as temporary:
            base = Path(temporary)
            roots = [base / "first", base / "second"]
            for root in roots:
                git_init(root)
            shared = base / "account-ledger"
            first, second = (admission_type(root, state_dir=shared) for root in roots)
            budget = {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 0,
            }
            first_token = first.reserve(
                "first001", "worker", ["a", "b", "c"], budget, {"owner": "fixture"}
            )

            def reserve_second():
                return second.reserve(
                    "second01", "worker", ["d", "e"], budget, {"owner": "fixture"}
                )

            with self.assertRaisesRegex(Exception, "ENV_LIMIT"):
                reserve_second()
            with self.assertRaisesRegex(Exception, "ENV_STATE"):
                first.release(first_token, lambda _: None)
            self.assertEqual(first.recover(lambda _: None), [])
            with self.assertRaisesRegex(Exception, "ENV_LIMIT"):
                reserve_second()
            first.release(first_token, lambda _: True)
            self.assertIsInstance(reserve_second(), str)


class IsolatedNetworkTest(unittest.TestCase):
    def test_owned_network_requires_internal_isolated_gateway_and_exact_label(self):
        environment = importlib.import_module("test_cluster_environment")
        command = environment.create_network_command("hyk8s-owned-abc12345", "abc12345")
        self.assertIn("--internal", command)
        self.assertIn("com.docker.network.bridge.gateway_mode_ipv4=isolated", command)
        self.assertIn("hy-home.k8s/run=abc12345", command)
        for internal, gateway, ipv6 in (
            (False, "isolated", False),
            (True, "nat", False),
            (True, "isolated", True),
        ):
            network = {
                "Name": "hyk8s-owned-abc12345",
                "Driver": "bridge",
                "Internal": internal,
                "EnableIPv6": ipv6,
                "Options": {"com.docker.network.bridge.gateway_mode_ipv4": gateway},
                "Labels": {"hy-home.k8s/run": "abc12345"},
            }
            with self.subTest(internal=internal, gateway=gateway, ipv6=ipv6):
                with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
                    environment.verify_network(
                        lambda command: json.dumps(network),
                        "hyk8s-owned-abc12345",
                        "abc12345",
                    )
        with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
            environment.verify_node_network(
                lambda command: json.dumps({"hyk8s-owned-abc12345": {}, "bridge": {}}),
                "hyk8s-test-abc12345",
                "hyk8s-owned-abc12345",
            )


if __name__ == "__main__":
    unittest.main()
