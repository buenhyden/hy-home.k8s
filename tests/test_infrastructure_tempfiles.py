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

VALUES = {
    ("svc", "postgres-write-external", "{.spec.ports[0].port}"): "15432",
    ("svc", "postgres-read-external", "{.spec.ports[0].port}"): "15433",
    ("svc", "vault-external", "{.spec.ports[0].port}"): "8200",
    ("svc", "valkey-external", "{.spec.ports[0].port}"): "6379",
    ("svc", "prometheus-external", "{.spec.ports[0].port}"): "9090",
    ("svc", "loki-external", "{.spec.ports[0].port}"): "3100",
    ("svc", "tempo-external", "{.spec.ports[0].port}"): "3200",
    ("svc", "alloy-external", "{.spec.ports[0].port}"): "4317",
    ("svc", "grafana-external", "{.spec.ports[0].port}"): "3000",
    ("endpointslice", "valkey-external-1", "{.ports[0].port}"): "6379",
    ("endpointslice", "valkey-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.9",
    ("endpointslice", "prometheus-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.10",
    ("endpointslice", "loki-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.13",
    ("endpointslice", "tempo-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.12",
    ("endpointslice", "alloy-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.11",
    ("endpointslice", "grafana-external-1", "{.endpoints[0].addresses[0]}"): "172.18.0.14",
    ("svc", "ingress-nginx-controller", "{.spec.type}"): "LoadBalancer",
    ("svc", "ingress-nginx-controller", "{.status.loadBalancer.ingress[0].ip}"): "127.0.0.2",
    ("ingress", "argocd-server", "{.spec.rules[0].host}"): "argocd.127.0.0.1.nip.io",
    ("ingress", "argocd-server", "{.spec.tls[0].hosts[0]}"): "argocd.127.0.0.1.nip.io",
    ("ingress", "argocd-server", "{.spec.tls[0].secretName}"): "argocd-local-tls",
    ("secret", "argocd-local-tls", "{.type}"): "kubernetes.io/tls",
    ("appproject", "platform", '{.spec.clusterResourceWhitelist[?(@.kind=="ClusterSecretStore")].kind}'): "ClusterSecretStore",
    ("ingress", "headlamp", "{.spec.tls[0].secretName}"): "headlamp-tls",
    ("ingress", "kiali", "{.spec.tls[0].secretName}"): "kiali-tls",
}

if tool == "rm":
    os.execv("/usr/bin/rm", ["rm", *args])
elif tool == "curl":
    print("HTTP/2 200")
elif tool == "kubectl" and "version" not in args:
    get_index = args.index("get")
    kind = args[get_index + 1]
    if kind == "svc,endpointslice":
        print("postgres-write-external postgres-read-external vault-external valkey-external")
        print("prometheus-external loki-external tempo-external alloy-external grafana-external")
    elif kind == "application":
        print("path: gitops/apps/root")
        print("targetRevision: main")
    elif "jsonpath={.status.health.status}" in args:
        print("Healthy", end="")
    else:
        name = args[get_index + 2]
        jsonpath = next(
            value.removeprefix("jsonpath=")
            for value in args
            if value.startswith("jsonpath=")
        )
        print(VALUES[(kind, name, jsonpath)], end="")
"""


EXPECTED_PASSES = {
    "verify-gitops.sh": "[PASS] GitOps contract check passed",
    "verify-external-services.sh": "[PASS] external service contract checks passed",
    "verify-ingress-tls.sh": "[PASS] ingress/TLS contract checks passed",
}

FAILURES = {
    "verify-gitops.sh": ("rg", "root-platform path contract mismatch"),
    "verify-external-services.sh": ("rg", "missing postgres-write-external"),
    "verify-ingress-tls.sh": ("curl", "https fallback endpoint is not reachable"),
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
                fail_tool, diagnostic = FAILURES[script.name]

                result = self.run_script(script, tmpdir, log, STUB_FAIL_TOOL=fail_tool)

                self.assertEqual(result.returncode, 1)
                self.assertIn(f"[FAIL] {diagnostic}", result.stderr)
                output_paths = self.logged_paths(log, "OUT")
                self.assertTrue(output_paths)
                self.assertTrue(
                    all(path.is_relative_to(tmpdir) for path in output_paths)
                )
                self.assertTrue(all(not path.parent.exists() for path in output_paths))
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
