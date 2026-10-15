#!/usr/bin/env python3
"""Focused tests for private live-verification temporary storage."""

from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = (
    ROOT / "infrastructure/verify/verify-gitops.sh",
    ROOT / "infrastructure/verify/verify-external-services.sh",
    ROOT / "infrastructure/verify/verify-ingress-tls.sh",
)
SHARED_TMP_REDIRECT = re.compile(r"(?:[0-9]+)?>>?\s*(/tmp/[^\s;&|]+)")
STUB = r"""#!/usr/bin/python3
from __future__ import annotations

import json
import os
import signal
import stat
import sys
import time
from pathlib import Path


tool = Path(sys.argv[0]).name
args = sys.argv[1:]
tmpdir = Path(os.environ["TMPDIR"])
log = Path(os.environ["STUB_LOG"])


def append(line: str) -> None:
    with log.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


for candidate in tmpdir.iterdir():
    if candidate.is_dir():
        mode = stat.S_IMODE(candidate.stat().st_mode)
        append(f"DIR\t{candidate}\t{mode:o}")

try:
    stdout_target = Path(os.readlink("/proc/self/fd/1"))
except OSError:
    stdout_target = None

if stdout_target is not None and stdout_target.is_relative_to(tmpdir):
    append(f"OUT\t{stdout_target}")
    if barrier := os.environ.get("STUB_BARRIER"):
        barrier_path = Path(barrier)
        (barrier_path / os.environ["STUB_RUN_ID"]).touch()
        deadline = time.monotonic() + 3
        while len(tuple(barrier_path.iterdir())) < 2:
            if time.monotonic() >= deadline:
                sys.exit(90)
            time.sleep(0.01)
    if os.environ.get("STUB_FAIL_REDIRECT") == tool:
        sys.exit(int(os.environ["STUB_FAIL_STATUS"]))

if os.environ.get("STUB_MODE") == "block" and tool == "kubectl" and "version" in args:
    signal.signal(signal.SIGINT, lambda *_: sys.exit(130))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    Path(os.environ["STUB_READY"]).touch()
    while True:
        time.sleep(1)

if os.environ.get("STUB_FAIL_TOOL") == tool:
    sys.exit(1)

if tool == "curl":
    append("CURL\t" + "\t".join(args))

if tool == "curl" and os.environ.get("STUB_UNTRUSTED_TLS") == "1":
    if any(arg.startswith("-k") or arg == "--insecure" for arg in args):
        print("HTTP/2 200")
        sys.exit(0)
    sys.exit(60)

VALUES = {
    ("svc", "valkey-external", "{.spec.ports[0].port}"): "6379",
    ("svc", "valkey-external", "{.spec.ports[0].targetPort}"): "26379",
    ("svc", "loki-external", "{.spec.ports[0].port}"): "3100",
    ("svc", "tempo-external", "{.spec.ports[0].port}"): "3200",
    ("svc", "alloy-external", "{.spec.ports[0].port}"): "4317",
    ("endpointslice", "valkey-external-1", "{.ports[0].port}"): "26379",
    ("endpointslice", "valkey-external-1", "{.endpoints[0].addresses[0]}"): "192.168.0.13",
    ("endpointslice", "loki-external-1", "{.endpoints[0].addresses[0]}"): "192.168.0.13",
    ("endpointslice", "tempo-external-1", "{.endpoints[0].addresses[0]}"): "192.168.0.13",
    ("endpointslice", "alloy-external-1", "{.endpoints[0].addresses[0]}"): "192.168.0.13",
    ("svc", "ingress-nginx-controller", "{.spec.type}"): "LoadBalancer",
    ("svc", "ingress-nginx-controller", "{.status.loadBalancer.ingress[0].ip}"): "127.0.0.2",
    ("ingress", "argocd-server", "{.spec.rules[0].host}"): "argo.hy-k8s.home.arpa",
    ("ingress", "argocd-server", "{.spec.tls[0].hosts[0]}"): "argo.hy-k8s.home.arpa",
    ("ingress", "argocd-server", "{.spec.tls[0].secretName}"): "argocd-local-tls",
    ("secret", "argocd-local-tls", "{.type}"): "kubernetes.io/tls",
    ("appproject", "platform", '{.spec.clusterResourceWhitelist[?(@.kind=="ClusterSecretStore")].kind}'): "ClusterSecretStore",
    ("ingress", "headlamp", "{.spec.tls[0].secretName}"): "headlamp-tls",
    ("ingress", "kiali", "{.spec.tls[0].secretName}"): "kiali-tls",
}

if tool == "rm":
    os.execv("/usr/bin/rm", ["rm", *args])
elif tool == "curl":
    if "https://hy-k8s.home.arpa/argo" in args:
        print("HTTP/2 302\nlocation: https://argo.hy-k8s.home.arpa/")
    else:
        print("HTTP/2 200")
elif tool == "kubectl" and "version" not in args:
    append("KUBECTL\t" + "\t".join(args))
    get_index = args.index("get")
    kind = args[get_index + 1]
    if kind == "nodes":
        print(os.environ.get("STUB_NODES", "\n".join(["node Ready control-plane 1d v1"] * 4)))
    elif kind == "deploy":
        print("1", end="")
    elif kind == "ipaddresspool":
        print("192.168.0.240-192.168.0.250", end="")
    elif kind == "svc,endpointslice":
        if os.environ.get("STUB_FAIL_PLATFORM_LIST") == "1":
            sys.exit(1)
        services = {
            "valkey-external": [
                ("tcp-valkey", 6379, int(os.environ.get("STUB_VALKEY_TARGET_PORT", "26379")))
            ],
            "loki-external": [("http", 3100, 3100)],
            "tempo-external": [("http", 3200, 3200)],
            "alloy-external": [("grpc-otlp", 4317, 4317), ("http-otlp", 4318, 4318)],
        }
        items = []
        slices = {}
        for name, ports in services.items():
            items.append({
                "kind": "Service", "metadata": {"name": name},
                "spec": {"type": os.environ.get("STUB_SERVICE_TYPE", "ClusterIP"), "clusterIP": os.environ.get("STUB_CLUSTER_IP", "10.43.0.10"), "ports": [
                    {"name": label, "port": frontend, "targetPort": backend}
                    for label, frontend, backend in ports
                ]},
            })
            slices[name] = {
                "kind": "EndpointSlice", "addressType": "IPv4",
                "metadata": {"name": name + "-1", "labels": {"kubernetes.io/service-name": name}},
                "ports": [
                    {"name": label, "protocol": "TCP", "port": backend}
                    for label, frontend, backend in ports
                ],
                "endpoints": [{"addresses": ["192.168.0.13"]}],
            }
            items.append(slices[name])
        if os.environ.get("STUB_EXTRA_SLICE"):
            name = os.environ["STUB_EXTRA_SLICE"]
            items.append({
                "kind": "EndpointSlice", "addressType": "IPv4",
                "metadata": {"name": name + "-2", "labels": {"kubernetes.io/service-name": name}},
                "ports": [{"name": services[name][0][0], "protocol": "TCP", "port": services[name][0][2]}],
                "endpoints": [{"addresses": ["192.168.0.99"]}],
            })
        if os.environ.get("STUB_EXTRA_ADDRESS"):
            name = os.environ["STUB_EXTRA_ADDRESS"]
            slices[name]["endpoints"].append({"addresses": ["192.168.0.99"]})
        if os.environ.get("STUB_EXTRA_PORT"):
            name = os.environ["STUB_EXTRA_PORT"]
            slices[name]["ports"].append({"name": "rogue", "protocol": "TCP", "port": 9999})
        if os.environ.get("STUB_EMPTY_SLICE"):
            name = os.environ["STUB_EMPTY_SLICE"]
            slices[name]["endpoints"] = []
        if os.environ.get("STUB_SPLIT_ALLOY"):
            items.append({
                "kind": "EndpointSlice", "addressType": "IPv4",
                "metadata": {"name": "alloy-external-2", "labels": {"kubernetes.io/service-name": "alloy-external"}},
                "ports": [slices["alloy-external"]["ports"].pop()],
                "endpoints": [{"addresses": ["192.168.0.13"]}],
            })
        print(json.dumps({"items": items}))
    elif kind == "application" and "yaml" in args:
        print("metadata:\n  annotations:\n    note: 'path: gitops/apps/root targetRevision: main'\nspec:\n  source:\n    path: " + os.environ.get("STUB_GITOPS_SOURCE", "gitops/apps/root") + "\n    targetRevision: " + os.environ.get("STUB_GITOPS_REVISION", "main"))
    elif "jsonpath={.status.health.status}" in args:
        print(os.environ.get("STUB_APP_HEALTH", "Healthy"), end="")
    elif "jsonpath={.status.sync.status}" in args:
        print(os.environ.get("STUB_APP_SYNC", "Synced"), end="")
    else:
        name = args[get_index + 2]
        jsonpath = next(
            value.removeprefix("jsonpath=")
            for value in args
            if value.startswith("jsonpath=")
        )
        if kind == "application":
            value = os.environ.get("STUB_GITOPS_SOURCE", "gitops/apps/root") if jsonpath == "{.spec.source.path}" else os.environ.get("STUB_GITOPS_REVISION", "main")
        else:
            value = VALUES[(kind, name, jsonpath)]
        if (kind, name, jsonpath) == (
            "svc", "valkey-external", "{.spec.ports[0].targetPort}"
        ):
            value = os.environ.get("STUB_VALKEY_TARGET_PORT", value)
        print(value, end="")
"""


EXPECTED_PASSES = {
    "verify-gitops.sh": "[PASS] GitOps contract check passed",
    "verify-external-services.sh": "[PASS] external service contract checks passed",
    "verify-ingress-tls.sh": "[PASS] ingress/TLS contract checks passed",
}

FAILURES = {
    "verify-gitops.sh": (
        {"STUB_GITOPS_SOURCE": "wrong/path"},
        "root-platform path contract mismatch",
    ),
    "verify-external-services.sh": (
        {"STUB_EXTRA_ADDRESS": "loki-external"},
        "loki-external EndpointSlice address or readiness mismatch",
    ),
    "verify-ingress-tls.sh": (
        {"STUB_FAIL_TOOL": "curl"},
        "https fallback endpoint TLS trust or reachability failed",
    ),
}

SIGNAL_CHILD_LAUNCHER = (
    "import os, signal, sys; "
    "signal.pthread_sigmask(signal.SIG_UNBLOCK, (signal.SIGINT, signal.SIGTERM)); "
    "os.execv(sys.argv[1], sys.argv[1:])"
)


class InfrastructureTemporaryFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="infrastructure-tempfiles-")
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        for tool in ("kubectl", "curl", "rg", "rm"):
            path = self.bin / tool
            path.write_text(STUB, encoding="utf-8")
            path.chmod(0o755)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def environment(self, tmpdir: Path, log: Path, **values: str) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "PATH": f"{self.bin}:{environment['PATH']}",
                "TMPDIR": str(tmpdir),
                "STUB_LOG": str(log),
                **values,
            }
        )
        return environment

    def run_script(
        self, script: Path, tmpdir: Path, log: Path, **values: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/usr/bin/bash", str(script)],
            cwd=ROOT,
            env=self.environment(tmpdir, log, **values),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def logged_paths(self, log: Path, kind: str) -> list[Path]:
        if not log.exists():
            return []
        return [
            Path(fields[1])
            for line in log.read_text(encoding="utf-8").splitlines()
            if (fields := line.split("\t"))[0] == kind
        ]

    def terminate_process_group(self, process: subprocess.Popen[str]) -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)

    def test_predictable_absolute_tmp_redirects_are_rejected(self) -> None:
        violations: list[str] = []
        for script in SCRIPTS:
            for number, line in enumerate(
                script.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if target := SHARED_TMP_REDIRECT.search(line):
                    violations.append(
                        f"{script.relative_to(ROOT)}:{number}: {target.group(1)}"
                    )

        self.assertEqual(violations, [])

    def test_concurrent_success_uses_private_independent_directories(self) -> None:
        for script in SCRIPTS:
            with self.subTest(script=script.name):
                tmpdir = self.root / f"success-{script.stem}"
                barrier = self.root / f"barrier-{script.stem}"
                tmpdir.mkdir()
                barrier.mkdir()
                logs = [self.root / f"{script.stem}-{index}.log" for index in range(2)]
                processes = [
                    subprocess.Popen(
                        ["/usr/bin/bash", str(script)],
                        cwd=ROOT,
                        env=self.environment(
                            tmpdir,
                            logs[index],
                            STUB_BARRIER=str(barrier),
                            STUB_RUN_ID=str(index),
                        ),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        start_new_session=True,
                    )
                    for index in range(2)
                ]
                completed: set[subprocess.Popen[str]] = set()
                results: list[tuple[str, str]] = []
                try:
                    for process in processes:
                        results.append(process.communicate(timeout=10))
                        completed.add(process)
                finally:
                    for process in processes:
                        if process not in completed:
                            self.terminate_process_group(process)

                parents: list[Path] = []
                for index, process in enumerate(processes):
                    stdout, stderr = results[index]
                    self.assertEqual(process.returncode, 0, stderr)
                    self.assertIn(EXPECTED_PASSES[script.name], stdout)
                    output_paths = self.logged_paths(logs[index], "OUT")
                    self.assertTrue(output_paths)
                    run_parents = {path.parent for path in output_paths}
                    self.assertEqual(len(run_parents), 1)
                    parent = run_parents.pop()
                    parents.append(parent)
                    self.assertEqual(parent.parent, tmpdir)
                    directory_rows = {
                        fields[1]: int(fields[2], 8)
                        for line in logs[index].read_text(encoding="utf-8").splitlines()
                        if (fields := line.split("\t"))[0] == "DIR"
                    }
                    self.assertEqual(directory_rows[str(parent)] & 0o077, 0)
                    self.assertFalse(parent.exists())

                self.assertNotEqual(parents[0], parents[1])
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_failure_status_diagnostics_and_cleanup_are_preserved(self) -> None:
        for script in SCRIPTS:
            with self.subTest(script=script.name):
                tmpdir = self.root / f"failure-{script.stem}"
                tmpdir.mkdir()
                log = self.root / f"failure-{script.stem}.log"
                failure_values, diagnostic = FAILURES[script.name]

                result = self.run_script(script, tmpdir, log, **failure_values)

                self.assertEqual(result.returncode, 1)
                self.assertIn(f"[FAIL] {diagnostic}", result.stderr)
                output_paths = self.logged_paths(log, "OUT")
                self.assertTrue(output_paths)
                self.assertTrue(
                    all(path.is_relative_to(tmpdir) for path in output_paths)
                )
                self.assertTrue(all(not path.parent.exists() for path in output_paths))
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_service_queries_keep_platform_namespace(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "external-namespace"
        tmpdir.mkdir()
        log = self.root / "external-namespace.log"

        result = self.run_script(script, tmpdir, log)

        self.assertEqual(result.returncode, 0, result.stderr)
        queries = [
            line.split("\t")[1:]
            for line in log.read_text(encoding="utf-8").splitlines()
            if line.startswith("KUBECTL\t")
        ]
        self.assertTrue(queries)
        self.assertTrue(all(query[:2] == ["-n", "platform"] for query in queries))
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_cluster_not_ready_nodes_do_not_count_as_ready(self) -> None:
        script = ROOT / "infrastructure/verify/verify-cluster.sh"
        tmpdir = self.root / "cluster-not-ready"
        tmpdir.mkdir()
        log = self.root / "cluster-not-ready.log"

        result = self.run_script(
            script,
            tmpdir,
            log,
            STUB_NODES="\n".join(["node NotReady control-plane 1d v1"] * 4),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("expected at least 4 Ready nodes", result.stderr)

    def test_gitops_requires_healthy_and_synced_apps(self) -> None:
        script = ROOT / "infrastructure/verify/verify-gitops.sh"
        for state in ({"STUB_APP_HEALTH": "Degraded"}, {"STUB_APP_SYNC": "OutOfSync"}):
            with self.subTest(state=state):
                tmpdir = self.root / f"gitops-{next(iter(state.values()))}"
                tmpdir.mkdir()
                log = self.root / f"gitops-{next(iter(state.values()))}.log"

                result = self.run_script(script, tmpdir, log, **state)

                self.assertEqual(result.returncode, 1)
                self.assertIn("[FAIL]", result.stderr)
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_gitops_ignores_annotation_decoys_for_source_contract(self) -> None:
        script = ROOT / "infrastructure/verify/verify-gitops.sh"
        for field, value in (
            ("STUB_GITOPS_SOURCE", "wrong/path"),
            ("STUB_GITOPS_REVISION", "wrong"),
        ):
            with self.subTest(field=field):
                tmpdir = self.root / field
                tmpdir.mkdir()
                result = self.run_script(
                    script, tmpdir, self.root / f"{field}.log", **{field: value}
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("contract mismatch", result.stderr)
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_ingress_rejects_untrusted_tls(self) -> None:
        script = ROOT / "infrastructure/verify/verify-ingress-tls.sh"
        tmpdir = self.root / "ingress-untrusted"
        tmpdir.mkdir()
        log = self.root / "ingress-untrusted.log"

        result = self.run_script(script, tmpdir, log, STUB_UNTRUSTED_TLS="1")

        self.assertEqual(result.returncode, 1)
        self.assertIn("https fallback endpoint", result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_ingress_router_probes_use_local_ca_without_insecure_mode(self) -> None:
        script = ROOT / "infrastructure/verify/verify-ingress-tls.sh"
        tmpdir = self.root / "ingress-router"
        tmpdir.mkdir()
        log = self.root / "ingress-router.log"

        result = self.run_script(script, tmpdir, log, CHECK_K8S_ROUTER="true")

        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [
            line.split("\t")[1:]
            for line in log.read_text(encoding="utf-8").splitlines()
            if line.startswith("CURL\t")
        ]
        self.assertEqual(len(calls), 3)
        for args in calls:
            with self.subTest(args=args):
                self.assertIn("--cacert", args)
                self.assertEqual(
                    args[args.index("--cacert") + 1],
                    str(ROOT / "secrets/certs/rootCA.pem"),
                )
                self.assertFalse(any(arg.startswith("-k") for arg in args))
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_service_target_port_failure_keeps_cleanup(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "external-target-port"
        tmpdir.mkdir()
        log = self.root / "external-target-port.log"

        result = self.run_script(script, tmpdir, log, STUB_VALKEY_TARGET_PORT="6379")

        self.assertEqual(result.returncode, 1)
        self.assertIn("[FAIL] valkey Service targetPort mismatch", result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_services_reject_extra_routes(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        for field, service in (
            ("STUB_EXTRA_SLICE", "loki-external"),
            ("STUB_EXTRA_ADDRESS", "valkey-external"),
            ("STUB_EXTRA_PORT", "alloy-external"),
            ("STUB_EMPTY_SLICE", "tempo-external"),
        ):
            with self.subTest(field=field):
                tmpdir = self.root / field
                tmpdir.mkdir()
                result = self.run_script(
                    script, tmpdir, self.root / f"{field}.log", **{field: service}
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("[FAIL]", result.stderr)
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_services_accept_split_named_ports(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "split-alloy"
        tmpdir.mkdir()
        result = self.run_script(
            script, tmpdir, self.root / "split-alloy.log", STUB_SPLIT_ALLOY="1"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_services_reject_non_clusterip_service_type(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        for service_type in ("ExternalName", "NodePort"):
            with self.subTest(service_type=service_type):
                tmpdir = self.root / service_type
                tmpdir.mkdir()
                result = self.run_script(
                    script,
                    tmpdir,
                    self.root / f"{service_type}.log",
                    STUB_SERVICE_TYPE=service_type,
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Service type mismatch", result.stderr)
                self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_services_reject_headless_service(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "headless"
        tmpdir.mkdir()
        result = self.run_script(
            script,
            tmpdir,
            self.root / "headless.log",
            STUB_CLUSTER_IP="None",
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("headless Service", result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_services_report_missing_python_before_listing(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "missing-python"
        tmpdir.mkdir()
        (self.bin / "mktemp").symlink_to("/usr/bin/mktemp")
        env = self.environment(tmpdir, self.root / "missing-python.log")
        env["PATH"] = str(self.bin)

        result = subprocess.run(
            ["/usr/bin/bash", str(script)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("python3 is required", result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_external_service_list_failure_has_diagnostic_and_cleanup(self) -> None:
        script = ROOT / "infrastructure/verify/verify-external-services.sh"
        tmpdir = self.root / "external-list-failure"
        tmpdir.mkdir()
        log = self.root / "external-list-failure.log"

        result = self.run_script(script, tmpdir, log, STUB_FAIL_PLATFORM_LIST="1")

        self.assertEqual(result.returncode, 1)
        self.assertIn("[FAIL] cannot list platform external services", result.stderr)
        self.assertEqual(list(tmpdir.iterdir()), [])

    def test_cleanup_failure_turns_success_into_failure(self) -> None:
        for script in SCRIPTS:
            with self.subTest(script=script.name):
                tmpdir = self.root / f"cleanup-failure-{script.stem}"
                tmpdir.mkdir()
                log = self.root / f"cleanup-failure-{script.stem}.log"

                result = self.run_script(script, tmpdir, log, STUB_FAIL_TOOL="rm")

                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    "[FAIL] cannot remove private temporary directory", result.stderr
                )
                self.assertEqual(len(tuple(tmpdir.iterdir())), 1)

    def test_cleanup_failure_preserves_existing_nonzero_status(self) -> None:
        script = ROOT / "infrastructure/verify/verify-gitops.sh"
        tmpdir = self.root / "combined-failure"
        tmpdir.mkdir()
        log = self.root / "combined-failure.log"

        result = self.run_script(
            script,
            tmpdir,
            log,
            STUB_FAIL_TOOL="rm",
            STUB_FAIL_REDIRECT="kubectl",
            STUB_FAIL_STATUS="42",
        )

        self.assertEqual(result.returncode, 42)
        self.assertIn("[FAIL] cannot remove private temporary directory", result.stderr)
        self.assertEqual(len(tuple(tmpdir.iterdir())), 1)

    def test_int_and_term_preserve_status_and_cleanup(self) -> None:
        for script in SCRIPTS:
            for sent_signal, expected_status in (
                (signal.SIGINT, 130),
                (signal.SIGTERM, 143),
            ):
                with self.subTest(script=script.name, signal=sent_signal.name):
                    tmpdir = self.root / f"signal-{script.stem}-{sent_signal.name}"
                    tmpdir.mkdir()
                    log = self.root / f"signal-{script.stem}-{sent_signal.name}.log"
                    ready = self.root / f"ready-{script.stem}-{sent_signal.name}"
                    process = subprocess.Popen(
                        [
                            sys.executable,
                            "-I",
                            "-c",
                            SIGNAL_CHILD_LAUNCHER,
                            "/usr/bin/bash",
                            str(script),
                        ],
                        cwd=ROOT,
                        env=self.environment(
                            tmpdir,
                            log,
                            STUB_MODE="block",
                            STUB_READY=str(ready),
                        ),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        start_new_session=True,
                    )
                    completed = False
                    try:
                        deadline = time.monotonic() + 3
                        while not ready.exists() and time.monotonic() < deadline:
                            time.sleep(0.01)
                        self.assertTrue(ready.exists(), "blocking stub did not start")

                        os.killpg(process.pid, sent_signal)
                        _stdout, stderr = process.communicate(timeout=5)
                        completed = True

                        self.assertEqual(process.returncode, expected_status, stderr)
                        observed = set(self.logged_paths(log, "DIR"))
                        self.assertEqual(len(observed), 1)
                        self.assertTrue(all(not path.exists() for path in observed))
                        self.assertEqual(list(tmpdir.iterdir()), [])
                    finally:
                        if not completed:
                            self.terminate_process_group(process)


if __name__ == "__main__":
    unittest.main()
