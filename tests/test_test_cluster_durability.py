"""Durability regressions for P07 native and VM cleanup."""

from __future__ import annotations

import importlib
import contextlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class ClusterDurabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="p07-cluster-durability-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        subprocess.run(
            ["/usr/bin/git", "init", "--quiet", str(self.root)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        self.cluster = importlib.import_module("test_cluster")
        self.vm = importlib.import_module("test_cluster_vm")
        self.vm_lifecycle = importlib.import_module("test_cluster_vm_lifecycle")
        admission_type = importlib.import_module("environment_admission").Admission
        self.admission = admission_type(self.root, state_dir=self.root / "ledger")

    def reserve_vm(self, run_id: str, *, creator: int | None = None) -> str:
        creator = os.getpid() if creator is None else creator
        return self.admission.reserve(
            run_id,
            "cluster",
            ["selected"],
            {
                "cpu": 2,
                "memory_mib": 4096,
                "disk_mib": 4096,
                "seconds": 600,
                "instances": 1,
            },
            {
                "unit": self.vm.unit_name(run_id),
                "vm_dir": str(self.vm.paths_for(self.root, run_id).directory),
                "deadline": int(time.time()) + 600,
                "pid": creator,
                "start_ticks": self.cluster._process_start(creator) or 1,
            },
        )

    def state(self, run_id: str, record: dict) -> Path:
        directory = self.cluster._state_dir(self.root, run_id)
        directory.mkdir(parents=True, mode=0o700)
        state = directory / "state.json"
        binding = (
            {
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
            }
            if record.get("environment_kind") == "vm"
            else {}
        )
        state.write_text(json.dumps({"run_id": run_id} | binding | record))
        state.chmod(0o600)
        return state

    def recover_vm(self) -> list[str]:
        def runner(command, **_kwargs):
            self.assertEqual(command[:3], ["systemctl", "--user", "show"])
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        with (
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(self.vm_lifecycle, "disarm_expiry_timer"),
        ):
            return self.vm_lifecycle.recover_vm_intents(
                self.root, self.admission, self.cluster._read_state, runner=runner
            )

    def test_vm_intent_recovery_keeps_lease_when_metadata_removal_refuses(self):
        run_id = "n6ref001"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "creating",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        directory = self.vm.paths_for(self.root, run_id).directory
        directory.mkdir(mode=0o700)
        with mock.patch.object(
            self.cluster.CLUSTER_ENV,
            "remove_vm_run_parent_locked",
            side_effect=OSError("synthetic metadata refusal"),
        ):
            try:
                self.recover_vm()
            except (OSError, self.vm.VmError):
                pass
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_vm_intent_recovery_retries_after_state_unlink_interruption(self):
        run_id = "n6unlink"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "creating",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        directory = self.vm.paths_for(self.root, run_id).directory
        directory.mkdir(mode=0o700)

        def unlink_then_interrupt(descriptor, *_args):
            os.unlink("state.json", dir_fd=descriptor)
            raise OSError("synthetic interruption after state unlink")

        with mock.patch.object(
            self.cluster.CLUSTER_ENV,
            "remove_vm_run_parent_locked",
            side_effect=unlink_then_interrupt,
        ):
            try:
                self.recover_vm()
            except (OSError, self.vm.VmError):
                pass
        self.assertFalse(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )
        self.recover_vm()
        self.assertEqual(self.admission.active_for_run(run_id), [])
        self.assertFalse(directory.parent.exists())

    def test_vm_intent_recovery_retries_after_database_release_refuses(self):
        run_id = "n6dbref1"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "creating",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        directory = self.vm.paths_for(self.root, run_id).directory
        directory.mkdir(mode=0o700)
        real_release = self.admission.release

        def refuse_parent(release_token, absent):
            if release_token == token:
                raise ValueError("ENV_STATE: synthetic database refusal")
            return real_release(release_token, absent)

        with mock.patch.object(self.admission, "release", side_effect=refuse_parent):
            try:
                self.recover_vm()
            except (OSError, ValueError, self.vm.VmError):
                pass
        self.assertFalse(state.exists())
        self.assertFalse(directory.parent.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )
        self.recover_vm()
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_failed_unit_status_with_misleading_inactive_output_retains_vm_proof(self):
        run_id, token = "badunit1", "a" * 32
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.parent.mkdir(parents=True, mode=0o700)
        paths.directory.mkdir(mode=0o700)
        paths.raw.write_bytes(b"synthetic owned disk")

        def runner(command, **_kwargs):
            self.assertEqual(command[:2], ["systemctl", "--user"])
            if command[2] == "show":
                output = "LoadState=loaded\nActiveState=inactive\nMainPID=0\n"
            else:
                self.assertEqual(command[2], "is-active")
                output = "inactive\n"
            return subprocess.CompletedProcess(
                command, 1, stdout=output, stderr="permission denied"
            )

        owned = self.vm.VmRun(self.root, run_id, token, runner=runner)
        owned._save_owner(
            {"run_id": run_id, "token": token, "unit": self.vm.unit_name(run_id)}
        )
        owned._record_files()
        with mock.patch.object(self.vm, "_user_bus", return_value={}):
            try:
                stopped = owned.stop_owned()
            except self.vm.VmError:
                stopped = False
        self.assertFalse(stopped)
        self.assertTrue((paths.directory / "owner.json").exists())
        self.assertTrue(paths.raw.exists())

    def test_owner_replacement_syncs_directory_after_atomic_rename(self):
        run_id, token = "owners01", "a" * 32
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.parent.mkdir(parents=True, mode=0o700)
        paths.directory.mkdir(mode=0o700)
        owned = self.vm.VmRun(self.root, run_id, token)
        events = []
        real_fsync, real_replace = os.fsync, os.replace

        def observed_fsync(fd):
            events.append(("fsync", stat.S_ISDIR(os.fstat(fd).st_mode)))
            return real_fsync(fd)

        def observed_replace(source, target, **kwargs):
            events.append(("replace", Path(target).name))
            return real_replace(source, target, **kwargs)

        with (
            mock.patch.object(self.vm.os, "fsync", side_effect=observed_fsync),
            mock.patch.object(self.vm.os, "replace", side_effect=observed_replace),
        ):
            owned._save_owner(
                {"run_id": run_id, "token": token, "unit": self.vm.unit_name(run_id)}
            )
        replace_at = events.index(("replace", "owner.json"))
        self.assertIn(("fsync", True), events[replace_at + 1 :])
        self.assertTrue((paths.directory / "owner.json").exists())

    def test_run_phase_replacement_syncs_state_and_parent_directory(self):
        run_id = "phase001"
        directory = self.cluster._state_dir(self.root, run_id)
        directory.mkdir(parents=True, mode=0o700)
        events = []
        real_fsync, real_replace = os.fsync, os.replace

        def observed_fsync(fd):
            events.append(("fsync", stat.S_ISDIR(os.fstat(fd).st_mode)))
            return real_fsync(fd)

        def observed_replace(source, target, **kwargs):
            events.append(("replace", Path(target).name))
            return real_replace(source, target, **kwargs)

        with (
            mock.patch.object(self.cluster.os, "fsync", side_effect=observed_fsync),
            mock.patch.object(self.cluster.os, "replace", side_effect=observed_replace),
        ):
            self.cluster._write_state(
                self.root, run_id, {"run_id": run_id, "status": "leases-released"}
            )
        replace_at = events.index(("replace", "state.json"))
        self.assertIn(("fsync", False), events[:replace_at])
        self.assertIn(("fsync", True), events[replace_at + 1 :])
        self.assertEqual(
            self.cluster._read_state(self.root, run_id)["status"], "leases-released"
        )

    def test_vm_state_write_rejects_oversize_before_creating_temp_file(self):
        directory = self.cluster._state_dir(self.root, "overs001")
        directory.mkdir(parents=True, mode=0o700)
        with self.cluster.CLUSTER_ENV.locked_run_dir(directory) as descriptor:
            with self.assertRaises(ValueError):
                self.cluster.CLUSTER_ENV.write_state_locked(
                    descriptor, {"padding": "x" * 5000}
                )
        self.assertEqual(list(directory.iterdir()), [])

    def test_vm_authority_limit_refuses_before_lease_or_run_directory(self):
        run_id = "auth0010"
        selected = mock.Mock()
        selected.catalog.return_value = {}
        selected.plan.return_value = ["selected"]
        with mock.patch.object(
            self.cluster.CLUSTER_ENV,
            "arm_expiry_timer",
            side_effect=AssertionError("authority reached timer"),
        ):
            with self.assertRaisesRegex(self.vm.VmError, "VM_AUTHORITY"):
                self.vm_lifecycle.up_host(
                    selected,
                    self.root,
                    ["selected"],
                    "x" * 513,
                    run_id=run_id,
                    admission=self.admission,
                )
        self.assertEqual(self.admission.active_for_run(run_id), [])
        self.assertFalse(self.cluster._state_dir(self.root, run_id).exists())

    def test_native_sweep_refuses_state_cluster_or_run_identity_mismatch(self):
        for case, run_id in (("cluster", "state001"), ("run", "state002")):
            with self.subTest(case=case):
                token = self.admission.reserve(
                    run_id,
                    "cluster",
                    ["selected"],
                    {
                        "cpu": 1,
                        "memory_mib": 512,
                        "disk_mib": 512,
                        "seconds": 60,
                        "instances": 1,
                    },
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "pid": 99999999,
                        "start_ticks": 1,
                    },
                )
                mismatch = (
                    {"cluster": "hyk8s-test-other001"}
                    if case == "cluster"
                    else {"run_id": "other001"}
                )
                state = self.state(
                    run_id,
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "admission_token": token,
                        "status": "failed",
                        "pid": 99999999,
                        "pid_start_ticks": 1,
                    }
                    | mismatch,
                )
                with (
                    mock.patch.object(self.cluster, "list_clusters", return_value=[]),
                    mock.patch.object(self.cluster, "labelled_runs", return_value={}),
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
                    ),
                    mock.patch.object(
                        self.cluster, "_cleanup_owned", return_value=True
                    ) as cleanup,
                    mock.patch.object(
                        self.cluster, "_resources_absent", return_value=True
                    ),
                ):
                    self.cluster.sweep(self.root, admission=self.admission)
                self.assertEqual(cleanup.call_count, 0)
                self.assertTrue(state.exists())
                self.assertEqual(
                    [row["token"] for row in self.admission.active_for_run(run_id)],
                    [token],
                )

    def test_native_sweep_rechecks_state_identity_after_lease_release(self):
        run_id = "state003"
        token = self.admission.reserve(
            run_id,
            "cluster",
            ["selected"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": f"hyk8s-test-{run_id}", "pid": 99999999, "start_ticks": 1},
        )
        state = self.state(
            run_id,
            {
                "cluster": f"hyk8s-test-{run_id}",
                "admission_token": token,
                "status": "failed",
                "pid": 99999999,
                "pid_start_ticks": 1,
            },
        )
        real_recover = self.admission.recover

        def replace_state_after_release(absent):
            released = real_recover(absent)
            if token in released:
                state.write_text(
                    json.dumps(
                        json.loads(state.read_text())
                        | {"cluster": "hyk8s-test-other001"}
                    )
                )
            return released

        with (
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "labelled_runs", return_value={}),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
            ),
            mock.patch.object(self.cluster, "_cleanup_owned", return_value=True),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(
                self.admission, "recover", side_effect=replace_state_after_release
            ),
        ):
            self.cluster.sweep(self.root, admission=self.admission)
        self.assertTrue(state.exists())
        self.assertEqual(
            json.loads(state.read_text())["cluster"], "hyk8s-test-other001"
        )

    def test_vm_release_failure_keeps_owner_for_loaded_inactive_unit_retry(self):
        run_id = "vmretry1"
        token = self.reserve_vm(run_id, creator=99999999)
        unit = self.vm.unit_name(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": unit,
                "admission_token": token,
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
            },
        )
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.mkdir(mode=0o700)
        paths.raw.write_bytes(b"synthetic owned disk")

        def runner(command, **_kwargs):
            if command[:3] == ["systemctl", "--user", "is-active"]:
                output = "inactive\n"
            elif command[:3] == ["systemctl", "--user", "show"]:
                output = "LoadState=loaded\nActiveState=inactive\nMainPID=0\n"
            else:
                raise AssertionError("unexpected synthetic systemd operation")
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        vm_type = self.vm.VmRun
        owned = vm_type(self.root, run_id, token, runner=runner)
        owned._save_owner(
            {
                "run_id": run_id,
                "token": token,
                "unit": unit,
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
            }
        )
        owned._record_files()
        record = self.cluster._read_state(self.root, run_id)
        with (
            mock.patch.object(
                self.vm,
                "VmRun",
                side_effect=lambda root, rid, tok: vm_type(
                    root, rid, tok, runner=runner
                ),
            ),
            mock.patch.object(self.vm, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            with mock.patch.object(
                self.admission,
                "release",
                side_effect=ValueError("ENV_STATE: release refused"),
            ):
                with self.assertRaisesRegex(ValueError, "ENV_STATE"):
                    self.vm_lifecycle.down_host(
                        self.cluster, self.root, record, admission=self.admission
                    )
            self.assertTrue((paths.directory / "owner.json").exists())
            self.assertFalse(paths.raw.exists())
            self.assertTrue(state.exists())
            self.assertEqual(
                [row["token"] for row in self.admission.active_for_run(run_id)], [token]
            )
            self.assertEqual(
                self.vm_lifecycle.down_host(
                    self.cluster, self.root, record, admission=self.admission
                ),
                {"deleted": unit},
            )
        self.assertFalse(state.exists())
        self.assertFalse(paths.directory.exists())
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_vm_finalization_crash_after_lease_release_recovers_owner_metadata(self):
        run_id = "vmfin001"
        token = self.reserve_vm(run_id, creator=99999999)
        unit = self.vm.unit_name(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": unit,
                "admission_token": token,
                "expires_at": 0,
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
            },
        )
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.mkdir(mode=0o700)
        paths.raw.write_bytes(b"synthetic owned disk")

        def runner(command, **_kwargs):
            if command[:3] == ["systemctl", "--user", "is-active"]:
                output = "inactive\n"
            elif command[:3] == ["systemctl", "--user", "show"]:
                output = "LoadState=loaded\nActiveState=inactive\nMainPID=0\n"
            else:
                raise AssertionError("unexpected synthetic systemd operation")
            return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

        vm_type = self.vm.VmRun
        owned = vm_type(self.root, run_id, token, runner=runner)
        owned._save_owner(
            {
                "run_id": run_id,
                "token": token,
                "unit": unit,
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
            }
        )
        owned._record_files()
        record = self.cluster._read_state(self.root, run_id)
        with (
            mock.patch.object(
                self.vm,
                "VmRun",
                side_effect=lambda root, rid, tok: vm_type(
                    root, rid, tok, runner=runner
                ),
            ),
            mock.patch.object(self.vm, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "labelled_runs", return_value={}),
        ):
            with mock.patch.object(
                vm_type,
                "finalize_owned",
                side_effect=OSError("synthetic finalization crash"),
                create=True,
            ):
                with self.assertRaises((OSError, self.vm.VmError)):
                    self.vm_lifecycle.down_host(
                        self.cluster, self.root, record, admission=self.admission
                    )
            self.assertEqual(self.admission.active_for_run(run_id), [])
            self.assertTrue(state.exists())
            self.assertTrue((paths.directory / "owner.json").exists())
            self.cluster.sweep(self.root, admission=self.admission)
        self.assertFalse(state.exists())
        self.assertFalse(paths.directory.exists())

    def test_released_vm_with_owner_gone_and_loaded_inactive_unit_finishes_metadata(
        self,
    ):
        run_id, token = "orphan03", "a" * 32
        unit = self.vm.unit_name(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "cleanup_phase": "leases-released",
                "unit": unit,
                "admission_token": token,
            },
        )
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.mkdir(mode=0o700)

        def runner(command, **_kwargs):
            self.assertEqual(command[:3], ["systemctl", "--user", "show"])
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=loaded\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        vm_type = self.vm.VmRun
        with (
            mock.patch.object(
                self.vm,
                "VmRun",
                side_effect=lambda root, rid, tok: vm_type(
                    root, rid, tok, runner=runner
                ),
            ),
            mock.patch.object(self.vm, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            result = self.vm_lifecycle.down_host(
                self.cluster,
                self.root,
                self.cluster._read_state(self.root, run_id),
                admission=self.admission,
            )
        self.assertEqual(result, {"deleted": unit})
        self.assertFalse(state.exists())
        self.assertFalse(paths.directory.exists())

    def test_native_expire_refuses_foreign_state_identity_before_cleanup(self):
        for case, run_id in (("cluster", "expira01"), ("run", "expira02")):
            with self.subTest(case=case):
                token = self.admission.reserve(
                    run_id,
                    "cluster",
                    ["selected"],
                    {
                        "cpu": 1,
                        "memory_mib": 512,
                        "disk_mib": 512,
                        "seconds": 60,
                        "instances": 1,
                    },
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "pid": 99999999,
                        "start_ticks": 1,
                    },
                )
                mismatch = (
                    {"cluster": "hyk8s-test-other001"}
                    if case == "cluster"
                    else {"run_id": "other001"}
                )
                state = self.state(
                    run_id,
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "admission_token": token,
                        "status": "up",
                        "expires_at": 0,
                    }
                    | mismatch,
                )
                created = self.admission.active_for_run(run_id)[0]["created_at"]
                with (
                    mock.patch.object(
                        self.cluster.time, "time", return_value=created + 120
                    ),
                    mock.patch.object(
                        self.cluster, "_cleanup_owned", return_value=True
                    ) as cleanup,
                    mock.patch.object(
                        self.cluster, "_resources_absent", return_value=True
                    ),
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
                    ),
                ):
                    result = self.cluster.expire(
                        self.root, run_id, token, admission=self.admission
                    )
                self.assertEqual(result, {"kept": run_id})
                self.assertEqual(cleanup.call_count, 0)
                self.assertTrue(state.exists())
                self.assertEqual(
                    [row["token"] for row in self.admission.active_for_run(run_id)],
                    [token],
                )

    def test_native_down_rechecks_state_after_cleanup_before_lease_release(self):
        run_id = "downswap"
        token = self.admission.reserve(
            run_id,
            "cluster",
            ["selected"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": f"hyk8s-test-{run_id}", "pid": 99999999, "start_ticks": 1},
        )
        state = self.state(
            run_id,
            {
                "cluster": f"hyk8s-test-{run_id}",
                "admission_token": token,
                "status": "up",
            },
        )

        def replace_state(_run_id, _env):
            state.write_text(
                json.dumps(
                    json.loads(state.read_text()) | {"cluster": "hyk8s-test-other001"}
                )
            )
            return True

        with (
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(
                self.cluster, "_cleanup_owned", side_effect=replace_state
            ),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "await_create_quiescent", return_value=True
            ),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            with self.assertRaisesRegex(
                self.cluster.ClusterError, "CLUSTER_NOT_OWNED|ENV_STATE"
            ):
                self.cluster.down(self.root, run_id, admission=self.admission)
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_native_direct_cleanup_rechecks_state_after_lease_release(self):
        for operation, run_id in (("expire", "postexp1"), ("down", "postdown")):
            with self.subTest(operation=operation):
                token = self.admission.reserve(
                    run_id,
                    "cluster",
                    ["selected"],
                    {
                        "cpu": 1,
                        "memory_mib": 512,
                        "disk_mib": 512,
                        "seconds": 60,
                        "instances": 1,
                    },
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "pid": 99999999,
                        "start_ticks": 1,
                    },
                )
                state = self.state(
                    run_id,
                    {
                        "cluster": f"hyk8s-test-{run_id}",
                        "admission_token": token,
                        "status": "up",
                        "expires_at": 0,
                    },
                )
                real_release = self.admission.release

                def release_then_replace(release_token, absent):
                    real_release(release_token, absent)
                    state.write_text(
                        json.dumps(
                            json.loads(state.read_text())
                            | {"cluster": "hyk8s-test-other001"}
                        )
                    )

                with (
                    mock.patch.object(self.cluster, "list_clusters", return_value=[]),
                    mock.patch.object(
                        self.cluster, "_cleanup_owned", return_value=True
                    ),
                    mock.patch.object(
                        self.cluster, "_resources_absent", return_value=True
                    ),
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV,
                        "await_create_quiescent",
                        return_value=True,
                    ),
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
                    ),
                    mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
                    mock.patch.object(
                        self.admission, "release", side_effect=release_then_replace
                    ),
                ):
                    if operation == "expire":
                        self.cluster.expire(
                            self.root, run_id, token, admission=self.admission
                        )
                    else:
                        self.cluster.down(self.root, run_id, admission=self.admission)
                self.assertTrue(state.exists())
                self.assertEqual(
                    json.loads(state.read_text())["cluster"], "hyk8s-test-other001"
                )
                self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_vm_down_rejects_state_replacement_after_saved_read(self):
        run_id = "swapvm01"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        saved = self.cluster._read_state(self.root, run_id)

        def replace_during_stop(_owned):
            state.write_text(
                json.dumps(
                    json.loads(state.read_text())
                    | {"workspace_id": "foreign-common-dir"}
                )
            )
            return True

        with (
            mock.patch.object(self.vm.VmRun, "stop_owned", new=replace_during_stop),
            mock.patch.object(self.vm.VmRun, "payload_absent", return_value=True),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            with self.assertRaisesRegex(self.vm.VmError, "VM_OWNERSHIP|VM_CLEANUP"):
                self.vm_lifecycle.down_host(
                    self.cluster, self.root, saved, admission=self.admission
                )
        self.assertTrue(state.exists())
        self.assertEqual(
            json.loads(state.read_text())["workspace_id"], "foreign-common-dir"
        )
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_vm_finalizer_preserves_state_replaced_after_phase_write(self):
        run_id = "swapvm02"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        saved = self.cluster._read_state(self.root, run_id)
        original_write = self.cluster.CLUSTER_ENV.write_state_locked

        def replace_after_phase(descriptor, record):
            original_write(descriptor, record)
            if record.get("cleanup_phase") == "leases-released":
                state.write_text(
                    json.dumps(
                        json.loads(state.read_text())
                        | {"binding_id": "foreign-binding"}
                    )
                )

        with (
            mock.patch.object(self.vm.VmRun, "stop_owned", return_value=True),
            mock.patch.object(self.vm.VmRun, "payload_absent", return_value=True),
            mock.patch.object(
                self.cluster.CLUSTER_ENV,
                "write_state_locked",
                side_effect=replace_after_phase,
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            try:
                self.vm_lifecycle.down_host(
                    self.cluster, self.root, saved, admission=self.admission
                )
            except self.vm.VmError:
                pass
        self.assertTrue(state.exists())
        self.assertEqual(json.loads(state.read_text())["binding_id"], "foreign-binding")
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_vm_intent_recovery_rejects_same_token_foreign_workspace_or_binding(self):
        for field, run_id in (("workspace_id", "recov001"), ("binding_id", "recov002")):
            with self.subTest(field=field):
                token = self.reserve_vm(run_id, creator=99999999)
                state = self.state(
                    run_id,
                    {
                        "environment_kind": "vm",
                        "status": "creating",
                        "unit": self.vm.unit_name(run_id),
                        "admission_token": token,
                        field: "foreign-identity",
                    },
                )

                def runner(command, **_kwargs):
                    self.assertEqual(command[:3], ["systemctl", "--user", "show"])
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                        stderr="",
                    )

                with (
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV, "_user_bus", return_value={}
                    ),
                    mock.patch.object(self.vm_lifecycle, "disarm_expiry_timer"),
                ):
                    self.vm_lifecycle.recover_vm_intents(
                        self.root,
                        self.admission,
                        self.cluster._read_state,
                        runner=runner,
                    )
                self.assertTrue(state.exists())
                self.assertEqual(
                    json.loads(state.read_text())[field], "foreign-identity"
                )
                self.assertEqual(
                    [row["token"] for row in self.admission.active_for_run(run_id)],
                    [token],
                )

    def test_vm_up_preserves_state_replaced_during_readiness(self):
        run_id = "upswap01"
        selected = mock.Mock()
        selected.catalog.return_value = {}
        selected.plan.return_value = ["selected"]
        selected._write_state = self.cluster._write_state
        state = self.cluster._state_dir(self.root, run_id) / "state.json"

        def ready(_owned, _deadline):
            state.write_text(
                json.dumps(
                    json.loads(state.read_text()) | {"binding_id": "foreign-binding"}
                )
            )
            return {"status": "up"}

        with (
            mock.patch.object(self.cluster.CLUSTER_ENV, "arm_expiry_timer"),
            mock.patch.object(self.vm.VmRun, "start"),
            mock.patch.object(self.vm.VmRun, "wait_ready", new=ready),
        ):
            with self.assertRaisesRegex(self.vm.VmError, "VM_OWNERSHIP|VM_CLEANUP"):
                self.vm_lifecycle.up_host(
                    selected,
                    self.root,
                    ["selected"],
                    "synthetic",
                    run_id=run_id,
                    admission=self.admission,
                )
        self.assertTrue(state.exists())
        self.assertEqual(json.loads(state.read_text())["binding_id"], "foreign-binding")
        self.assertEqual(len(self.admission.active_for_run(run_id)), 1)

    def test_vm_intent_recovery_reads_cooperating_replacement_under_lock(self):
        run_id = "recov003"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "creating",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )

        environment = self.cluster.CLUSTER_ENV
        original_lock = environment.locked_run_dir
        replaced = False

        @contextlib.contextmanager
        def replace_before_lock(parent):
            nonlocal replaced
            if not replaced:
                saved = self.cluster._read_state(self.root, run_id)
                with original_lock(parent) as writer:
                    environment.write_state_locked(
                        writer, saved | {"binding_id": "foreign-binding"}
                    )
                replaced = True
            with original_lock(parent) as descriptor:
                yield descriptor

        def runner(command, **_kwargs):
            self.assertEqual(command[:3], ["systemctl", "--user", "show"])
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        with (
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "locked_run_dir", new=replace_before_lock
            ),
            mock.patch.object(self.vm_lifecycle, "disarm_expiry_timer"),
        ):
            self.vm_lifecycle.recover_vm_intents(
                self.root, self.admission, self.cluster._read_state, runner=runner
            )
        self.assertTrue(state.exists())
        self.assertEqual(json.loads(state.read_text())["binding_id"], "foreign-binding")
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )


if __name__ == "__main__":
    unittest.main()
