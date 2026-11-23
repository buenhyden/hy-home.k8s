"""Synthetic VM admission, ownership, and network boundary regressions for P07."""

from __future__ import annotations

import contextlib
import errno
import http.server
import importlib
import io
import json
import os
import socketserver
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def vm_module():
    return importlib.import_module("test_cluster_vm")


def host_module():
    return importlib.import_module("test_cluster_vm_lifecycle")


class VmBoundaryTest(unittest.TestCase):
    def test_local_vm_http_endpoints_bound_one_client_and_three_second_reads(self):
        vm = vm_module()
        transport = importlib.import_module("test_cluster_vm_transport")
        server_type = transport.BoundedHTTPServer
        self.assertTrue(issubclass(server_type, http.server.HTTPServer))
        self.assertFalse(issubclass(server_type, socketserver.ThreadingMixIn))
        accepted = mock.Mock()
        with mock.patch.object(
            http.server.HTTPServer,
            "get_request",
            return_value=(accepted, ("127.0.0.1", 41000)),
        ):
            server = server_type.__new__(server_type)
            self.assertIs(server.get_request()[0], accepted)
        accepted.settimeout.assert_called_once_with(3)

        with tempfile.TemporaryDirectory(prefix="p07-vm-http-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32)
            fake_server = mock.Mock(server_port=40223)
            with (
                mock.patch.object(
                    owned,
                    "_owner",
                    return_value={"dummy_port": 49152, "dummy_nonce": "a" * 32},
                ),
                mock.patch.object(
                    transport, "BoundedHTTPServer", return_value=fake_server
                ) as create,
                mock.patch.object(
                    transport.threading.Thread, "start", return_value=None
                ),
            ):
                self.assertEqual(
                    transport.metadata(owned, "ssh-ed25519 SYNTHETIC"), 40223
                )
                transport.start_dummy(owned)
            self.assertEqual(create.call_count, 2)

    def test_official_image_stream_is_bounded_and_rejects_redirected_origin(self):
        vm = vm_module()
        transport = importlib.import_module("test_cluster_vm_transport")
        payload = b"synthetic official image bytes"

        class Response(io.BytesIO):
            def __init__(self, data, url):
                super().__init__(data)
                self.url = url

            def geturl(self):
                return self.url

        class Opener:
            def __init__(self, data, url):
                self.data, self.url = data, url

            def open(self, request, **_kwargs):
                self_test.assertEqual(request.full_url, transport.SOURCE_URL)
                return Response(self.data, self.url)

        self_test = self
        with tempfile.TemporaryDirectory(prefix="p07-vm-download-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32)
            owned.paths.directory.mkdir(parents=True)
            deadline = int(time.time()) + 60
            with mock.patch.object(owned, "_record_files", return_value=None):
                with mock.patch.object(
                    transport.urllib.request,
                    "build_opener",
                    return_value=Opener(payload, transport.SOURCE_URL),
                ):
                    transport.download_source(owned, deadline)
                self.assertEqual(owned.paths.source.read_bytes(), payload)
                owned.paths.source.unlink()
                with mock.patch.object(
                    transport.urllib.request,
                    "build_opener",
                    return_value=Opener(payload, "https://example.invalid/other.img"),
                ):
                    with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                        transport.download_source(owned, deadline)
                self.assertFalse(owned.paths.source.exists())
                with (
                    mock.patch.object(transport, "SOURCE_LIMIT", 8),
                    mock.patch.object(
                        transport.urllib.request,
                        "build_opener",
                        return_value=Opener(payload, transport.SOURCE_URL),
                    ),
                ):
                    with self.assertRaisesRegex(vm.VmError, "VM_IMAGE"):
                        transport.download_source(owned, deadline)

    def test_intent_only_vm_recovery_requires_dead_creator_and_absent_exact_unit(self):
        vm = vm_module()
        admission_type = importlib.import_module("environment_admission").Admission
        live_ticks = vm._process_start(os.getpid())
        self.assertIsInstance(live_ticks, int)
        cases = (
            ("dead-absent", 99999999, 1, "not-found", False, False),
            ("live-absent", os.getpid(), live_ticks, "not-found", True, False),
            ("dead-loaded", 99999999, 1, "loaded", True, False),
            ("dead-unknown", 99999999, 1, "unknown", True, False),
            ("dead-extra-file", 99999999, 1, "not-found", True, True),
        )
        for label, pid, ticks, load_state, retained, extra_file in cases:
            with (
                self.subTest(label=label),
                tempfile.TemporaryDirectory(prefix="p07-vm-intent-") as temporary,
            ):
                root = Path(temporary)
                subprocess.run(
                    ["/usr/bin/git", "init", "--quiet", str(root)],
                    check=True,
                    capture_output=True,
                    timeout=10,
                )
                admission = admission_type(root, state_dir=root / "ledger")
                run_id = "p07vm001"
                paths = vm.paths_for(root, run_id)
                token = admission.reserve(
                    run_id,
                    "cluster",
                    ["selected"],
                    {
                        "cpu": 3,
                        "memory_mib": 4096,
                        "disk_mib": 4096,
                        "seconds": vm_module().VM_SECONDS,
                        "instances": 1,
                    },
                    {
                        "unit": vm.unit_name(run_id),
                        "vm_dir": str(paths.directory),
                        "deadline": int(time.time()) + vm_module().VM_SECONDS,
                        "pid": pid,
                        "start_ticks": ticks,
                    },
                )
                if extra_file:
                    paths.directory.parent.mkdir(parents=True, mode=0o700)
                    (paths.directory.parent / "unexpected-file").write_bytes(
                        b"not owned by VM"
                    )

                def runner(command, **_kwargs):
                    if command[:3] == ["systemctl", "--user", "stop"]:
                        self.assertEqual(
                            command[-1], f"hyk8s-owned-{run_id}-{token}.timer"
                        )
                        return subprocess.CompletedProcess(
                            command, 0, stdout="", stderr=""
                        )
                    self.assertEqual(command[:3], ["systemctl", "--user", "show"])
                    self.assertIn(f"{vm.unit_name(run_id)}.service", command)
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout=f"LoadState={load_state}\nActiveState=inactive\nMainPID=0\n",
                        stderr="",
                    )

                with mock.patch.object(vm, "_user_bus", return_value={}):
                    host_module().recover_vm_intents(
                        root, admission, lambda _root, _run: None, runner=runner
                    )
                active = {row["token"] for row in admission.active_for_run(run_id)}
                self.assertEqual(token in active, retained)
                self.assertFalse(paths.directory.exists())

    def test_vm_sweep_keeps_active_state_and_never_recovers_failed_cleanup_as_k3d(self):
        vm = vm_module()
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-sweep-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            token = admission.reserve(
                "p07vm001",
                "cluster",
                ["selected"],
                {
                    "cpu": 1,
                    "memory_mib": 512,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 1,
                },
                {"unit": "hyk8s-test-p07vm001-vm"},
            )
            runtime = root / ".workspace-test/p07vm001"
            (runtime / "vm").mkdir(parents=True)
            marker = runtime / "vm/owned-raw-marker"
            marker.write_bytes(b"owned")
            record = {
                "run_id": "p07vm001",
                "environment_kind": "vm",
                "admission_token": token,
                "unit": "hyk8s-test-p07vm001-vm",
                "status": "up",
                "expires_at": time.time() + 60,
            }
            (runtime / "state.json").write_text(json.dumps(record))
            with (
                mock.patch.object(cluster, "labelled_runs", return_value={}),
                mock.patch.object(cluster, "list_clusters", return_value=[]),
                mock.patch.object(cluster, "_run", return_value=""),
                mock.patch.object(vm, "is_active", return_value=True, create=True),
                mock.patch.object(
                    host_module(),
                    "down_host",
                    side_effect=vm.VmError("VM_OWNERSHIP: live unit"),
                ) as down,
            ):
                self.assertIn(
                    record["unit"], cluster.sweep(root, admission=admission)["kept"]
                )
                down.assert_not_called()
                self.assertTrue(marker.exists())
                record.update(status="failed", expires_at=0)
                (runtime / "state.json").write_text(json.dumps(record))
                with mock.patch.object(
                    cluster.CLUSTER_ENV, "vm_start_inflight", return_value=False
                ):
                    self.assertIn(
                        record["unit"],
                        cluster.sweep(root, admission=admission)["failed"],
                    )
            self.assertTrue(marker.exists())
            self.assertEqual(admission.active_for_run("p07vm001")[0]["token"], token)

    def test_stale_vm_status_and_sweep_require_live_exact_unit(self):
        vm = vm_module()
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-vm-stale-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            token = admission.reserve(
                "p07vm001",
                "cluster",
                ["selected"],
                {
                    "cpu": 1,
                    "memory_mib": 512,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 1,
                },
                {"unit": "hyk8s-test-p07vm001-vm"},
            )
            runtime = root / ".workspace-test/p07vm001"
            (runtime / "vm").mkdir(parents=True)
            marker = runtime / "vm/owned-raw-marker"
            marker.write_bytes(b"owned")
            record = {
                "run_id": "p07vm001",
                "environment_kind": "vm",
                "admission_token": token,
                "unit": "hyk8s-test-p07vm001-vm",
                "status": "up",
                "expires_at": time.time() + 60,
            }
            (runtime / "state.json").write_text(json.dumps(record))
            with (
                mock.patch.object(cluster, "labelled_runs", return_value={}),
                mock.patch.object(cluster, "list_clusters", return_value=[]),
                mock.patch.object(cluster, "_run", return_value=""),
                mock.patch.object(vm, "is_active", return_value=False, create=True),
                mock.patch.object(
                    host_module(),
                    "down_host",
                    side_effect=vm.VmError("VM_OWNERSHIP: stale unit"),
                ) as down,
            ):
                rows = [
                    row
                    for row in cluster.status(root)
                    if row.get("environment_kind") == "vm"
                ]
                self.assertEqual(len(rows), 1)
                self.assertFalse(rows[0]["owned"])
                swept = cluster.sweep(root, admission=admission)
                self.assertNotIn(record["unit"], swept["kept"])
                self.assertIn(record["unit"], swept["failed"])
                down.assert_called_once()
            self.assertTrue(marker.exists())
            self.assertEqual(admission.active_for_run("p07vm001")[0]["token"], token)

    def test_failed_conversion_keeps_prep_lease_while_staging_file_remains(self):
        vm = vm_module()
        base_token = "a" * 32
        active, released, budgets = {base_token}, [], []

        class Admission:
            def __init__(self, root):
                self.root = root

            def reserve(self, run_id, kind, closure, budget, intent):
                self.assert_parent(intent)
                budgets.append(budget)
                active.add("prep-token")
                return "prep-token"

            def assert_parent(self, intent):
                if intent.get("parent_token") != base_token:
                    raise AssertionError("prep is not bound to the full VM lease")

            def release(self, token, absence):
                if absence({}) is True:
                    active.remove(token)
                    released.append(token)
                else:
                    raise ValueError("ENV_STATE: preparation absence unverified")

        def runner(command, **kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-staging-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", base_token, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline)

            def download(_deadline):
                owned.paths.source.write_bytes(b"source")

            def convert(_image):
                (owned.paths.directory / "disk.failed.tmp").write_bytes(b"partial")
                raise vm.VmError("VM_IMAGE: synthetic conversion failure")

            with (
                mock.patch.object(vm, "Admission", Admission),
                mock.patch.object(
                    owned, "_require_parent_lease", return_value={}, create=True
                ),
                mock.patch.object(owned, "_own_cgroup_caps", return_value={}),
                mock.patch.object(owned, "_start_dummy", return_value=None),
                mock.patch.object(owned, "_stop_dummy", return_value=None),
                mock.patch.object(owned, "_download_source", side_effect=download),
                mock.patch.object(owned, "prepare", side_effect=convert),
            ):
                with self.assertRaises(Exception):
                    owned.controller(deadline)
            self.assertIn("prep-token", active)
            self.assertEqual(released, [])
            self.assertEqual(budgets[0]["disk_mib"], 512)
            self.assertTrue((owned.paths.directory / "disk.failed.tmp").exists())

    def test_verified_vm_down_releases_only_bound_preparation_child(self):
        vm = vm_module()
        admission_module = importlib.import_module("environment_admission")
        admission_type = admission_module.Admission
        # A VM run (cluster 3 + preparation 1) fills the 4-CPU host; one extra
        # fixture CPU lets an unrelated worker coexist for this release check.
        with (
            mock.patch.dict(admission_module.HOST_BUDGET, cpu=5),
            tempfile.TemporaryDirectory(prefix="p07-vm-child-lease-") as temporary,
        ):
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            outer = admission.reserve(
                "p07vm001",
                "cluster",
                ["selected"],
                {
                    "cpu": 3,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": 60,
                    "instances": 1,
                },
                {
                    "unit": "hyk8s-test-p07vm001-vm",
                    "vm_dir": str(vm.paths_for(root, "p07vm001").directory),
                },
            )
            prep = admission.reserve(
                "p07vm001",
                "worker",
                [],
                {
                    "cpu": 1,
                    "memory_mib": 256,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 0,
                },
                {
                    "parent_token": outer,
                    "vm_source": str(vm.paths_for(root, "p07vm001").source),
                },
            )
            unrelated = admission.reserve(
                "p07vm001",
                "worker",
                [],
                {
                    "cpu": 1,
                    "memory_mib": 256,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 0,
                },
                {"purpose": "separate worker"},
            )
            record = {
                "run_id": "p07vm001",
                "environment_kind": "vm",
                "status": "up",
                "admission_token": outer,
                "unit": vm.unit_name("p07vm001"),
                "workspace_id": admission.workspace_id,
                "binding_id": admission.binding_id,
            }
            parent = vm.paths_for(root, "p07vm001").directory.parent
            parent.mkdir(parents=True, mode=0o700)
            state = parent / "state.json"
            state.write_text(json.dumps(record))
            state.chmod(0o600)
            with (
                mock.patch.object(vm.VmRun, "stop_owned", return_value=True),
                mock.patch.object(vm.VmRun, "payload_absent", return_value=True),
                mock.patch.object(vm.CLUSTER_ENV, "disarm_expiry_timer") as disarm,
            ):
                host_module().down_host(
                    importlib.import_module("test_cluster"),
                    root,
                    record,
                    admission=admission,
                )
            self.assertEqual(disarm.call_count, 1)
            active = {row["token"] for row in admission.active_for_run("p07vm001")}
            self.assertNotIn(outer, active)
            self.assertNotIn(prep, active)
            self.assertEqual(active, {unrelated})

    def test_stop_keeps_private_state_when_unit_absence_is_unverified(self):
        vm = vm_module()
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-stop-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(int(time.time()) + 60)
                marker = owned.paths.directory / "owned-marker"
                marker.write_text("fixture")
                self.assertFalse(owned.stop_owned())
            self.assertTrue((owned.paths.directory / "owner.json").exists())
            self.assertTrue(marker.exists())
            self.assertTrue(any(command[0] == "systemctl" for command in commands))

    def test_cleanup_preserves_unrecorded_replacement_file(self):
        vm = vm_module()

        def runner(command, **kwargs):
            output = (
                "inactive\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-replacement-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}):
                with self.assertRaisesRegex(vm.VmError, "VM_UNIT"):
                    owned.start(int(time.time()) + 60)
                replacement = owned.paths.directory / "unexpected-replacement"
                replacement.write_bytes(b"not recorded as an owned artifact")
                self.assertFalse(owned.stop_owned())
            self.assertTrue(replacement.exists())
            self.assertTrue((owned.paths.directory / "owner.json").exists())

    def test_cleanup_preserves_recorded_name_after_inode_replacement(self):
        vm = vm_module()

        def runner(command, **kwargs):
            output = (
                "inactive\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-inode-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}):
                with self.assertRaisesRegex(vm.VmError, "VM_UNIT"):
                    owned.start(int(time.time()) + 60)
                owned.paths.log.write_bytes(b"original")
                owned._record_files()
                replacement = owned.paths.directory / "new-log"
                replacement.write_bytes(b"replacement")
                replacement.replace(owned.paths.log)
                self.assertFalse(owned.stop_owned())
            self.assertEqual(owned.paths.log.read_bytes(), b"replacement")
            self.assertTrue((owned.paths.directory / "owner.json").exists())

    def test_selected_apps_are_durable_before_unit_invocation(self):
        vm = vm_module()
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            if command[0] == "systemd-run":
                owner = json.loads((owned.paths.directory / "owner.json").read_text())
                self.assertEqual(owner["apps"], ["selected"])
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-apps-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(int(time.time()) + 60, apps=["selected"])
        self.assertTrue(any(command[0] == "systemd-run" for command in commands))

    def test_host_up_passes_selected_closure_into_vm_unit_intent(self):
        vm = vm_module()

        class Cluster:
            @staticmethod
            def catalog(_root):
                return {"selected": {"path": "gitops/apps/selected"}}

            @staticmethod
            def plan(_catalog, selection):
                return list(selection)

            @staticmethod
            def _write_state(_root, _run_id, record):
                states.append(dict(record))
                importlib.import_module("test_cluster")._write_state(
                    _root, _run_id, record
                )

            @staticmethod
            def _run(*_args, **_kwargs):
                raise AssertionError("synthetic test must not invoke a host command")

        states, starts = [], []

        def start(_owned, _deadline, **kwargs):
            starts.append(kwargs.get("apps"))

        with tempfile.TemporaryDirectory(prefix="p07-vm-route-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = importlib.import_module("environment_admission").Admission(
                root, state_dir=root / "ledger"
            )
            with (
                mock.patch.object(vm.VmRun, "start", start),
                mock.patch.object(
                    vm.VmRun, "wait_ready", return_value={"proof": {}, "result": {}}
                ),
                mock.patch.object(vm.CLUSTER_ENV, "arm_expiry_timer") as arm,
            ):
                host_module().up_host(
                    Cluster(),
                    root,
                    ["selected"],
                    "synthetic test authority",
                    run_id="p07vm001",
                    admission=admission,
                )
            self.assertEqual(arm.call_count, 1)
        self.assertEqual(starts, [["selected"]])
        self.assertEqual(states[-1]["apps"], ["selected"])

    def test_failed_vm_step_preserves_stage_and_rc_without_secret_stderr(self):
        vm = vm_module()
        fake_secret = "sk-" + "A" * 32  # pragma: allowlist secret
        fake_github = "ghp_" + "B" * 36
        assignment = "token" + "=" + "synthetic-private"  # pragma: allowlist secret
        password = "password" + "=" + "hunter2"  # pragma: allowlist secret
        pem_marker = "-----" + "BEGIN PRIVATE KEY" + "-----"  # pragma: allowlist secret
        stderr = (
            f"prior line\nssh failed {assignment} {password} "
            f"{fake_secret} {fake_github} {pem_marker} \x1b[31m"
        )

        def failed(_command, **_kwargs):
            raise subprocess.CalledProcessError(42, ["ssh"], stderr=stderr)

        with self.assertRaisesRegex(vm.VmError, "VM_STEP: ssh exit 42") as raised:
            vm._invoke(failed, ["ssh", "example.invalid"])
        diagnostic = str(raised.exception)
        for sensitive in (
            "synthetic-private",
            "hunter2",
            fake_secret,
            fake_github,
            "BEGIN PRIVATE KEY",  # pragma: allowlist secret
            "\x1b",
        ):
            self.assertNotIn(sensitive, diagnostic)
        self.assertIn("ssh failed", diagnostic)
        self.assertLessEqual(len(diagnostic), 200)

    def test_guest_enospc_request_exceeds_entire_filesystem_under_root(self):
        vm = vm_module()
        total = 120 * 4 * 1024 * 1024
        requests = []

        class Vfs:
            f_bavail = 100
            f_blocks = 120
            f_frsize = 4 * 1024 * 1024

        def allocate(_fd, _offset, length):
            requests.append(length)
            if length > total:
                raise OSError(errno.ENOSPC, "synthetic full filesystem")

        with tempfile.TemporaryDirectory(prefix="p07-vm-enospc-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32)
            actual_mkstemp = tempfile.mkstemp

            def temp_file(*, dir):
                self.assertEqual(dir, "/home/hyk8s")
                return actual_mkstemp(dir=temporary)

            def guest(_port, argv, _deadline):
                self.assertIn("python3", argv)
                printed = io.StringIO()
                with contextlib.redirect_stdout(printed):
                    exec(argv[-1], {})
                return printed.getvalue()

            with (
                mock.patch.object(owned, "_ssh", side_effect=guest),
                mock.patch.object(os, "statvfs", return_value=Vfs()),
                mock.patch.object(os, "posix_fallocate", side_effect=allocate),
                mock.patch.object(tempfile, "mkstemp", side_effect=temp_file),
            ):
                free_mib = owned._guest_enospc(40222, int(time.time()) + 60)
        self.assertEqual(free_mib, 400)
        self.assertTrue(requests)
        self.assertGreater(requests[0], total)

    def test_guest_public_tree_and_binaries_become_root_owned_before_execution(self):
        vm = vm_module()
        transport = importlib.import_module("test_cluster_vm_transport")
        cluster = importlib.import_module("test_cluster")
        remote, streams = [], []
        real_popen = subprocess.Popen

        def subprocess_stub(_command, **_kwargs):
            if Path(_command[0]).name == "git":
                return real_popen(_command, **_kwargs)
            process = mock.Mock()
            process.stdin = io.BytesIO()
            process.wait.return_value = 0
            streams.append(process.stdin)
            return process

        def ssh_stub(_vm, _port, argv, _deadline):
            remote.append(argv)
            return ""

        with tempfile.TemporaryDirectory(prefix="p07-vm-public-") as temporary:
            root = Path(temporary)
            for relative in (
                "gitops/apps/root/kustomization.yaml",
                "gitops/apps/selected/kustomization.yaml",
                "scripts/test_cluster.py",
                "scripts/test_cluster_environment.py",
                "scripts/test_cluster_vm.py",
                "scripts/test_cluster_vm_transport.py",
                "scripts/environment_admission.py",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"public test input")
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            subprocess.run(
                ["/usr/bin/git", "-C", str(root), "add", "gitops", "scripts"],
                check=True,
                capture_output=True,
                timeout=10,
            )
            owned = vm.VmRun(root, "p07vm001", "a" * 32)
            deadline = int(time.time()) + 60
            binary = root / "k3d"
            binary.write_bytes(b"synthetic binary")
            with (
                mock.patch.object(owned, "_owner", return_value={"apps": ["selected"]}),
                mock.patch.object(
                    cluster,
                    "catalog",
                    return_value={"selected": {"path": "gitops/apps/selected"}},
                ),
                mock.patch.object(
                    transport.subprocess, "Popen", side_effect=subprocess_stub
                ),
                mock.patch.object(transport, "ssh", side_effect=ssh_stub),
                mock.patch.object(transport.shutil, "which", return_value=str(binary)),
            ):
                transport.copy_public_tree(owned, 40222, deadline)
                transport.copy_binary(owned, 40222, "k3d", deadline)
        chown = next(
            index
            for index, argv in enumerate(remote)
            if argv[:2] == ["sudo", "-n"] and "chown" in argv
        )
        git_init = next(
            index
            for index, argv in enumerate(remote)
            if argv[:2] == ["sudo", "-n"] and "git" in argv and "init" in argv
        )
        install = next(
            index
            for index, argv in enumerate(remote)
            if argv[:2] == ["sudo", "-n"] and "install" in argv
        )
        self.assertLess(chown, git_init)
        self.assertIn("/home/hyk8s/work", " ".join(remote[chown]))
        self.assertIn("/usr/local/bin/k3d", " ".join(remote[install]))
        self.assertEqual(len(streams), 2)

    def test_capsule_transfer_installs_private_root_copy_and_removes_staging(self):
        vm = vm_module()
        transfer, guest = [], []

        def runner(command, **kwargs):
            transfer.append((command, kwargs))
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-capsule-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            owned.paths.directory.mkdir(parents=True)
            owned.paths.capsule.write_bytes(b'{"synthetic":"proof"}')
            owned.paths.capsule.chmod(0o600)
            with mock.patch.object(
                owned,
                "_ssh",
                side_effect=lambda _port, argv, _deadline: guest.append(argv),
            ):
                owned._send_capsule(40222, int(time.time()) + 60)
        self.assertEqual(len(transfer), 1)
        install = next(argv for argv in guest if argv[:3] == ["sudo", "-n", "install"])
        self.assertIn("600", install)
        self.assertIn("/root/hyk8s-vm-capsule.json", install)
        self.assertTrue(
            any(
                argv[:2] == ["rm", "-f"] and "/home/hyk8s/vm-capsule.json" in argv
                for argv in guest
            )
        )

    def test_controller_refuses_missing_outer_lease_before_dummy_or_image(self):
        vm = vm_module()

        class EmptyAdmission:
            def __init__(self, _root):
                pass

            @staticmethod
            def active_for_run(_run_id):
                return []

            @staticmethod
            def reserve(*_args):
                raise AssertionError(
                    "controller reached prep lease without an outer lease"
                )

        def runner(command, **kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        with tempfile.TemporaryDirectory(prefix="p07-vm-parent-") as temporary:
            owned = vm.VmRun(Path(temporary), "p07vm001", "a" * 32, runner=runner)
            deadline = int(time.time()) + 60
            with mock.patch.object(vm, "_user_bus", return_value={}):
                owned.start(deadline, apps=["selected"])
            with (
                mock.patch.object(vm, "Admission", EmptyAdmission),
                mock.patch.object(owned, "_start_dummy") as dummy,
                mock.patch.object(owned, "_download_source") as download,
                mock.patch.object(owned, "_boot_qemu") as boot,
            ):
                with self.assertRaisesRegex(vm.VmError, "VM_OWNERSHIP"):
                    owned.controller(deadline)
            dummy.assert_not_called()
            download.assert_not_called()
            boot.assert_not_called()

    def test_controller_parent_guard_rejects_stale_or_underbudgeted_lease(self):
        vm = vm_module()
        admission_type = importlib.import_module("environment_admission").Admission

        def runner(command, **_kwargs):
            output = (
                "active\n"
                if command[:3] == ["systemctl", "--user", "is-active"]
                else ""
            )
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        for case in ("valid", "stale", "underbudget"):
            with (
                self.subTest(case=case),
                tempfile.TemporaryDirectory(prefix="p07-vm-parent-bind-") as temporary,
            ):
                root = Path(temporary)
                subprocess.run(
                    ["/usr/bin/git", "init", "--quiet", str(root)],
                    check=True,
                    capture_output=True,
                    timeout=10,
                )
                admission = admission_type(root, state_dir=root / "ledger")
                run_id = "p07vm001"
                deadline = int(time.time()) + 60
                budget = {
                    "cpu": 3 if case != "underbudget" else 1,
                    "memory_mib": 4096,
                    "disk_mib": 4096,
                    "seconds": vm_module().VM_SECONDS,
                    "instances": 1,
                }
                token = admission.reserve(
                    run_id,
                    "cluster",
                    ["selected"],
                    budget,
                    {
                        "unit": vm.unit_name(run_id),
                        "vm_dir": str(vm.paths_for(root, run_id).directory),
                        "deadline": deadline,
                        "pid": os.getpid(),
                        "start_ticks": vm._process_start(os.getpid()),
                    },
                )
                owned = vm.VmRun(root, run_id, token, runner=runner)
                with mock.patch.object(vm, "_user_bus", return_value={}):
                    owned.start(deadline, apps=["selected"])
                owned._save_owner(
                    owned._owner()
                    | {
                        "workspace_id": admission.workspace_id,
                        "binding_id": admission.binding_id,
                    }
                )
                if case == "stale":
                    admission.release(token, lambda _: True)
                with mock.patch.object(vm, "Admission", return_value=admission):
                    if case == "valid":
                        owned._require_parent_lease()
                    else:
                        with self.assertRaisesRegex(vm.VmError, "VM_OWNERSHIP"):
                            owned._require_parent_lease()

    def test_environment_flag_cannot_replace_guest_disk_proof(self):
        vm = vm_module()
        environment = importlib.import_module("test_cluster_environment")
        with tempfile.TemporaryDirectory(prefix="p07-vm-proof-") as temporary:
            capsule = Path(temporary) / "missing-capsule.json"
            with mock.patch.dict(
                os.environ, {"HYK8S_VM_VERIFIED": "1", "HYK8S_VM_CAPSULE": str(capsule)}
            ):
                with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                    vm.guest_disk_proof(capsule, sysroot=Path(temporary))
                with self.assertRaisesRegex(ValueError, "CLUSTER_DISK_LIMIT"):
                    environment.require_product_disk_cap()
                with self.assertRaisesRegex(vm.VmError, "VM_PROOF"):
                    environment.verified_guest_profile(capsule)

    def test_restricted_boundary_rejects_guest_reaching_host_dummy(self):
        environment = importlib.import_module("test_cluster_environment")
        nonce = "nonce-for-one-synthetic-run"
        self.assertEqual(
            environment.probe_boundary(
                lambda: nonce, lambda: nonce, nonce, restricted=False
            )["guest_restricted"],
            False,
        )
        self.assertEqual(
            environment.probe_boundary(
                lambda: nonce, lambda: "blocked", nonce, restricted=True
            )["guest_restricted"],
            True,
        )
        with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
            environment.probe_boundary(
                lambda: nonce, lambda: nonce, nonce, restricted=True
            )

        def transport_error():
            raise OSError("synthetic SSH transport failure")

        with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
            environment.probe_boundary(
                lambda: nonce, transport_error, nonce, restricted=True
            )
        observed = iter((nonce, "unreachable"))
        with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
            environment.probe_boundary(
                lambda: next(observed), lambda: "blocked", nonce, restricted=True
            )

    def test_selected_negative_uses_the_proven_http_protocol(self):
        environment = importlib.import_module("test_cluster_environment")
        calls = []

        def run(command, **_kwargs):
            calls.append(command)
            if command[:3] == ["kubectl", "get", "pod"]:
                return "10.42.0.5"
            if command[:2] == ["kubectl", "exec"]:
                return "rc=1" if "10.0.2.2" in " ".join(command) else "synthetic-nonce"
            return ""

        environment.selected_namespace_probe(
            run, "selected", 49152, "synthetic-nonce", "p07vm001"
        )
        external = next(
            command
            for command in calls
            if command[:2] == ["kubectl", "exec"] and "10.0.2.2" in " ".join(command)
        )
        self.assertIn("wget", " ".join(external))
        self.assertIn("http://10.0.2.2:49152", " ".join(external))
        self.assertNotIn("nc -z", " ".join(external))

    def test_selected_namespace_probe_refuses_host_dummy_reachability(self):
        environment = importlib.import_module("test_cluster_environment")
        nonce = "nonce-for-one-synthetic-run"
        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs))
            if command[:3] == ["kubectl", "get", "pod"]:
                return "10.42.0.5"
            if "exec" in command:
                return "rc=0" if "10.0.2.2" in " ".join(command) else nonce
            return ""

        with self.assertRaisesRegex(
            ValueError, r"CLUSTER_NETWORK.*internal=True.*external='rc=0'"
        ):
            environment.selected_namespace_probe(
                run, "selected", 49152, nonce, "p07vm001"
            )
        applied = next(
            json.loads(options["input_text"])
            for command, options in calls
            if command[:3] == ["kubectl", "apply", "-f"]
        )
        self.assertEqual(
            {item["metadata"]["namespace"] for item in applied["items"]}, {"selected"}
        )
        self.assertEqual(
            {
                item["metadata"]["labels"]["hy-home.k8s/run"]
                for item in applied["items"]
            },
            {"p07vm001"},
        )
        for pod in (item for item in applied["items"] if item["kind"] == "Pod"):
            self.assertFalse(pod["spec"]["automountServiceAccountToken"])
            self.assertTrue(
                pod["spec"]["containers"][0]["securityContext"][
                    "readOnlyRootFilesystem"
                ]
            )
            self.assertTrue(
                pod["spec"]["containers"][0]["securityContext"]["runAsNonRoot"]
            )
        self.assertTrue(
            any(
                command[:2] == ["kubectl", "delete"] and "selected" in command
                for command, _ in calls
            )
        )

    def test_selected_namespace_probe_accepts_only_internal_nonce_and_denied_host(self):
        environment = importlib.import_module("test_cluster_environment")
        nonce = "nonce-for-one-synthetic-run"
        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs))
            if command[:3] == ["kubectl", "get", "pod"]:
                return "10.42.0.5"
            if "exec" in command:
                return "rc=1" if "10.0.2.2" in " ".join(command) else nonce
            return ""

        result = environment.selected_namespace_probe(
            run, "selected", 49152, nonce, "p07vm001"
        )
        self.assertEqual(
            result,
            {
                "namespace": "selected",
                "internal_allowed": True,
                "owned_host_denied": True,
            },
        )
        internal = next(
            command
            for command, _ in calls
            if command[:2] == ["kubectl", "exec"]
            and "10.0.2.2" not in " ".join(command)
        )
        self.assertIn("wget", internal)
        applied = next(
            json.loads(options["input_text"])
            for command, options in calls
            if command[:3] == ["kubectl", "apply", "-f"]
        )
        server = next(
            item
            for item in applied["items"]
            if item["kind"] == "Pod"
            and item["metadata"]["labels"]["hyk8s-probe-role"] == "server"
        )
        server_command = " ".join(server["spec"]["containers"][0]["command"])
        self.assertIn("HTTP/1.1 200", server_command)
        self.assertIn("Content-Length", server_command)
        self.assertTrue(
            any(
                command[:2] == ["kubectl", "delete"] and "selected" in command
                for command, _ in calls
            )
        )

    def test_selected_probe_refuses_success_when_owned_policy_cleanup_fails(self):
        environment = importlib.import_module("test_cluster_environment")
        calls = []

        def run(command, **_kwargs):
            calls.append(command)
            if command[:3] == ["kubectl", "get", "pod"]:
                return "10.42.0.5"
            if "exec" in command:
                return "rc=1" if "10.0.2.2" in " ".join(command) else "synthetic-nonce"
            if command[:3] == ["kubectl", "delete", "networkpolicy"]:
                raise OSError("synthetic cleanup failure")
            return ""

        with self.assertRaisesRegex(ValueError, "CLUSTER_NETWORK"):
            environment.selected_namespace_probe(
                run, "selected", 49152, "synthetic-nonce", "p07vm001"
            )
        self.assertTrue(
            any(command[:3] == ["kubectl", "delete", "pod"] for command in calls)
        )
        self.assertTrue(
            any(
                command[:3] == ["kubectl", "delete", "networkpolicy"]
                for command in calls
            )
        )

    def test_failed_create_keeps_state_timer_and_lease_while_child_is_inflight(self):
        cluster = importlib.import_module("test_cluster")
        admission_type = importlib.import_module("environment_admission").Admission
        with tempfile.TemporaryDirectory(prefix="p07-inflight-failure-") as temporary:
            root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            admission = admission_type(root, state_dir=root / "ledger")
            run_id = "fail0001"

            def run(command, **_kwargs):
                if command[:3] == ["k3d", "cluster", "create"]:
                    raise cluster.ClusterError(
                        "CLUSTER_STEP_FAILED: synthetic create failure"
                    )
                return ""

            with (
                mock.patch.object(
                    cluster, "catalog", return_value={"selected": {"path": "selected"}}
                ),
                mock.patch.object(cluster, "plan", return_value=["selected"]),
                mock.patch.object(
                    cluster, "render", return_value=[{"kind": "Namespace"}]
                ),
                mock.patch.object(cluster.CLUSTER_ENV, "require_product_disk_cap"),
                mock.patch.object(cluster.CLUSTER_ENV, "arm_expiry_timer"),
                mock.patch.object(cluster.CLUSTER_ENV, "verify_network"),
                mock.patch.object(
                    cluster.CLUSTER_ENV, "create_inflight", return_value=True
                ),
                mock.patch.object(cluster.CLUSTER_ENV, "disarm_expiry_timer") as disarm,
                mock.patch.object(cluster, "list_clusters", return_value=[]),
                mock.patch.object(cluster, "_cleanup_owned", return_value=True),
                mock.patch.object(cluster, "free_port", return_value=40123),
                mock.patch.object(cluster, "_run", side_effect=run),
            ):
                with self.assertRaisesRegex(
                    cluster.ClusterError, "CLUSTER_STEP_FAILED"
                ):
                    cluster.up(
                        root,
                        ["selected"],
                        authority="synthetic",
                        run_id=run_id,
                        admission=admission,
                    )
            record = cluster._read_state(root, run_id)
            self.assertEqual(record["status"], "failed")
            self.assertEqual(
                [row["token"] for row in admission.active_for_run(run_id)],
                [record["admission_token"]],
            )
            disarm.assert_not_called()


if __name__ == "__main__":
    unittest.main()
