"""Synthetic ownership and recovery regressions for the P07 cluster lifecycle."""

from __future__ import annotations

import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class ClusterLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="p07-cluster-lifecycle-")
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

    def reserve_cluster(self, run_id: str) -> str:
        return self.admission.reserve(
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
                "pid": os.getpid(),
                "start_ticks": self.cluster._process_start(os.getpid()),
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

    def test_sweep_keeps_a_creating_vm_with_live_creator_or_controller(self):
        run_id = "active01"
        token = self.reserve_vm(run_id)
        unit = self.vm.unit_name(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "creating",
                "unit": unit,
                "admission_token": token,
                "pid": os.getpid(),
                "pid_start_ticks": self.cluster._process_start(os.getpid()),
                "expires_at": time.time() + 60,
            },
        )
        with (
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "labelled_runs", return_value={}),
            mock.patch.object(self.vm_lifecycle, "down_host") as stop,
        ):
            result = self.cluster.sweep(self.root, admission=self.admission)
            with (
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
                ),
                mock.patch.object(
                    self.cluster.CLUSTER_ENV,
                    "vm_start_inflight",
                    return_value=True,
                    create=True,
                ),
            ):
                controller_result = self.cluster.sweep(
                    self.root, admission=self.admission
                )
            with (
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
                ),
                mock.patch.object(
                    self.cluster.CLUSTER_ENV,
                    "vm_start_inflight",
                    return_value=None,
                    create=True,
                ),
            ):
                unknown_result = self.cluster.sweep(self.root, admission=self.admission)
            failed_record = json.loads(state.read_text()) | {
                "status": "failed",
                "expires_at": 0,
            }
            state.write_text(json.dumps(failed_record))
            with (
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
                ),
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "vm_start_inflight", return_value=True
                ),
            ):
                failed_result = self.cluster.sweep(self.root, admission=self.admission)
            with (
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
                ),
                mock.patch.object(
                    self.cluster.CLUSTER_ENV, "vm_start_inflight", return_value=None
                ),
            ):
                failed_unknown_result = self.cluster.sweep(
                    self.root, admission=self.admission
                )
        stop.assert_not_called()
        self.assertIn(unit, result["kept"])
        self.assertIn(unit, controller_result["kept"])
        self.assertIn(unit, unknown_result["kept"])
        self.assertIn(unit, failed_result["kept"])
        self.assertIn(unit, failed_unknown_result["kept"])
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_direct_down_keeps_inflight_create_then_cancels_exact_finished_owner(self):
        run_id = "direct01"
        token = self.reserve_cluster(run_id)
        state = self.state(
            run_id,
            {
                "cluster": f"hyk8s-test-{run_id}",
                "admission_token": token,
                "status": "creating",
            },
        )
        with (
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "_cleanup_owned", return_value=True),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "create_inflight", return_value=True
            ),
        ):
            with self.assertRaisesRegex(
                self.cluster.ClusterError, "CLUSTER_CLEANUP|ENV_STATE"
            ):
                self.cluster.down(self.root, run_id, admission=self.admission)
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )
        with (
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "_cleanup_owned", return_value=True),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            self.assertEqual(
                self.cluster.down(self.root, run_id, admission=self.admission),
                {"deleted": f"hyk8s-test-{run_id}"},
            )
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_vm_down_refuses_changed_workspace_before_stopping_exact_unit(self):
        run_id = "foreign1"
        token = self.reserve_vm(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        record = self.cluster._read_state(self.root, run_id)
        with (
            mock.patch.object(self.admission, "workspace_id", "different-common-dir"),
            mock.patch.object(self.vm.VmRun, "stop_owned", return_value=True) as stop,
        ):
            with self.assertRaisesRegex(self.vm.VmError, "VM_OWNERSHIP"):
                self.vm_lifecycle.down_host(
                    None, self.root, record, admission=self.admission
                )
        stop.assert_not_called()
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_vm_release_rechecks_workspace_if_binding_changes_after_preflight(self):
        run_id = "foreign2"
        token = self.reserve_vm(run_id)
        self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
            },
        )
        record = self.cluster._read_state(self.root, run_id)

        def stop_and_change_workspace(_vm):
            self.admission.workspace_id = "different-common-dir"
            return True

        with mock.patch.object(
            self.vm.VmRun, "stop_owned", new=stop_and_change_workspace
        ):
            with self.assertRaisesRegex(ValueError, "VM_OWNERSHIP|ENV_STATE"):
                self.vm_lifecycle.down_host(
                    None, self.root, record, admission=self.admission
                )
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_expire_refuses_foreign_workspace_before_any_cleanup(self):
        run_id = "expire02"
        token = self.reserve_cluster(run_id)
        state = self.state(
            run_id,
            {
                "cluster": f"hyk8s-test-{run_id}",
                "admission_token": token,
                "status": "up",
                "expires_at": 0,
            },
        )
        with (
            mock.patch.object(self.admission, "workspace_id", "different-common-dir"),
            mock.patch.object(
                self.cluster, "_cleanup_owned", return_value=True
            ) as cleanup,
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
        ):
            self.assertEqual(
                self.cluster.expire(self.root, run_id, token, admission=self.admission),
                {"kept": run_id},
            )
        self.assertEqual(cleanup.call_count, 0)
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_completed_cluster_expires_even_when_original_caller_is_alive(self):
        run_id = "finish01"
        token = self.reserve_cluster(run_id)
        self.state(
            run_id,
            {
                "cluster": f"hyk8s-test-{run_id}",
                "admission_token": token,
                "status": "up",
                "expires_at": 0,
            },
        )
        with (
            mock.patch.object(self.cluster, "_cleanup_owned", return_value=True),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
        ):
            self.assertEqual(
                self.cluster.expire(self.root, run_id, token, admission=self.admission),
                {"deleted": f"hyk8s-test-{run_id}"},
            )
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_sweep_refuses_foreign_workspace_or_wrong_cluster_intent_before_cleanup(
        self,
    ):
        admission_type = importlib.import_module("environment_admission").Admission
        for case, run_id in (("workspace", "sweep001"), ("cluster", "sweep002")):
            with self.subTest(case=case):
                admission = admission_type(
                    self.root, state_dir=self.root / f"ledger-{case}"
                )
                name = (
                    f"hyk8s-test-{run_id}"
                    if case == "workspace"
                    else "hyk8s-test-other001"
                )
                token = admission.reserve(
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
                    {"cluster": name, "pid": 99999999, "start_ticks": 1},
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
                if case == "workspace":
                    admission.workspace_id = "different-common-dir"
                with (
                    mock.patch.object(self.cluster, "list_clusters", return_value=[]),
                    mock.patch.object(self.cluster, "labelled_runs", return_value={}),
                    mock.patch.object(
                        self.cluster, "_cleanup_owned", return_value=True
                    ) as cleanup,
                    mock.patch.object(
                        self.cluster, "_resources_absent", return_value=True
                    ),
                ):
                    self.cluster.sweep(self.root, admission=admission)
                self.assertEqual(cleanup.call_count, 0)
                self.assertTrue(state.exists())
                self.assertEqual(
                    [row["token"] for row in admission.active_for_run(run_id)], [token]
                )

    def test_vm_intent_recovery_releases_only_exact_bound_preparation_child(self):
        run_id = "orphan01"
        outer = self.reserve_vm(run_id, creator=99999999)
        source = str(self.vm.paths_for(self.root, run_id).source)
        budget = {
            "cpu": 1,
            "memory_mib": 256,
            "disk_mib": 512,
            "seconds": 60,
            "instances": 0,
        }
        bound = self.admission.reserve(
            run_id, "worker", [], budget, {"parent_token": outer, "vm_source": source}
        )
        unrelated = self.admission.reserve(
            run_id,
            "worker",
            [],
            budget,
            {"parent_token": "0" * 32, "vm_source": source},
        )
        timer_stops = []

        def runner(command, **_kwargs):
            if command[:3] == ["systemctl", "--user", "stop"]:
                timer_stops.append(command[-1])
                self.assertEqual(
                    {row["token"] for row in self.admission.active_for_run(run_id)},
                    {unrelated},
                )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
            self.assertEqual(command[-1], f"{self.vm.unit_name(run_id)}.service")
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        with mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}):
            self.vm_lifecycle.recover_vm_intents(
                self.root, self.admission, self.cluster._read_state, runner=runner
            )
        active = {row["token"] for row in self.admission.active_for_run(run_id)}
        self.assertEqual(active, {unrelated})
        self.assertNotIn(bound, active)
        self.assertEqual(
            timer_stops,
            [f"{self.cluster.CLUSTER_ENV.expiry_unit(run_id, outer)}.timer"],
        )
        unknown_run = "orphan02"
        unknown_outer = self.reserve_vm(unknown_run, creator=99999999)
        unknown_child = self.admission.reserve(
            unknown_run,
            "worker",
            [],
            budget,
            {
                "parent_token": unknown_outer,
                "vm_source": str(self.vm.paths_for(self.root, unknown_run).source),
            },
        )

        unknown_stops = []

        def unknown_unit(command, **_kwargs):
            if command[:3] == ["systemctl", "--user", "stop"]:
                unknown_stops.append(command[-1])
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=loaded\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        with mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}):
            self.vm_lifecycle.recover_vm_intents(
                self.root, self.admission, self.cluster._read_state, runner=unknown_unit
            )
        self.assertEqual(
            {row["token"] for row in self.admission.active_for_run(unknown_run)},
            {unknown_outer, unknown_child},
        )
        self.assertEqual(unknown_stops, [])

    def test_docker_network_creation_has_the_same_child_receipt_as_k3d_create(self):
        captured = {}

        def run(command, **kwargs):
            if command[:3] == ["docker", "network", "create"]:
                captured.update(kwargs)
                raise self.cluster.ClusterError(
                    "CLUSTER_STEP_FAILED: synthetic network create"
                )
            return ""

        with (
            mock.patch.object(
                self.cluster, "catalog", return_value={"selected": {"path": "selected"}}
            ),
            mock.patch.object(self.cluster, "plan", return_value=["selected"]),
            mock.patch.object(
                self.cluster, "render", return_value=[{"kind": "Namespace"}]
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "arm_expiry_timer"),
            mock.patch.object(
                self.cluster.CLUSTER_ENV,
                "host_pause_tar",
                return_value="/r/.workspace-test/network1/pause.tar",
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "_cleanup_owned", return_value=True),
            mock.patch.object(self.cluster, "_resources_absent", return_value=True),
            mock.patch.object(self.cluster, "_run", side_effect=run),
        ):
            with self.assertRaisesRegex(
                self.cluster.ClusterError, "synthetic network create"
            ):
                self.cluster.up(
                    self.root,
                    ["selected"],
                    authority="synthetic",
                    run_id="network1",
                    admission=self.admission,
                )
        self.assertTrue(callable(captured.get("preexec_fn")))

    def test_successful_vm_arms_exact_expiry_before_unit_and_disarms_after_verified_down(
        self,
    ):
        run_id = "vmtime01"
        steps = []
        selected = mock.Mock()
        selected.catalog.return_value = {}
        selected.plan.return_value = ["selected"]
        selected._write_state = self.cluster._write_state
        with (
            mock.patch.object(
                self.cluster.CLUSTER_ENV,
                "arm_expiry_timer",
                side_effect=lambda *_args: steps.append("arm"),
            ) as arm,
            mock.patch.object(
                self.cluster.CLUSTER_ENV,
                "disarm_expiry_timer",
                side_effect=lambda *_args: steps.append("disarm"),
            ) as disarm,
            mock.patch.object(
                self.vm.VmRun,
                "start",
                side_effect=lambda *_args, **_kwargs: steps.append("start"),
            ),
            mock.patch.object(
                self.vm.VmRun, "wait_ready", return_value={"status": "up"}
            ),
            mock.patch.object(self.vm.VmRun, "stop_owned", return_value=True),
            mock.patch.object(self.vm.VmRun, "payload_absent", return_value=True),
        ):
            record = self.vm_lifecycle.up_host(
                selected,
                self.root,
                ["selected"],
                "synthetic",
                run_id=run_id,
                admission=self.admission,
            )
            token = record["admission_token"]
            self.assertEqual(steps[:2], ["arm", "start"])
            self.assertEqual(arm.call_args.args[3], token)
            self.vm_lifecycle.down_host(
                selected, self.root, record, admission=self.admission
            )
            self.assertEqual(steps[-1], "disarm")
            self.assertEqual(disarm.call_args.args[1:3], (run_id, token))
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_vm_expiry_routes_only_the_exact_current_workspace_token(self):
        run_id = "vmexp001"
        token = self.reserve_vm(run_id)
        unit = self.vm.unit_name(run_id)
        self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "up",
                "unit": unit,
                "admission_token": token,
                "expires_at": 0,
            },
        )
        with mock.patch.object(
            self.vm_lifecycle, "down_host", return_value={"deleted": unit}
        ) as stop:
            self.assertEqual(
                self.cluster.expire(self.root, run_id, token, admission=self.admission),
                {"deleted": unit},
            )
            self.assertEqual(
                self.cluster.expire(
                    self.root, run_id, "0" * 32, admission=self.admission
                ),
                {"kept": run_id},
            )
            with mock.patch.object(
                self.admission, "workspace_id", "different-common-dir"
            ):
                self.assertEqual(
                    self.cluster.expire(
                        self.root, run_id, token, admission=self.admission
                    ),
                    {"kept": run_id},
                )
        self.assertEqual(stop.call_count, 1)
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_expired_pre_owner_vm_uses_verified_intent_recovery(self):
        run_id = "vmpre001"
        token = self.reserve_vm(run_id, creator=99999999)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "failed",
                "unit": self.vm.unit_name(run_id),
                "admission_token": token,
                "pid": 99999999,
                "pid_start_ticks": 1,
                "expires_at": 0,
            },
        )
        recover = self.vm_lifecycle.recover_vm_intents

        def runner(command, **_kwargs):
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        def verified_recover(root, admission, read_state, *, only_token):
            return recover(
                root, admission, read_state, runner=runner, only_token=only_token
            )

        with (
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "vm_start_inflight", return_value=False
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "_user_bus", return_value={}),
            mock.patch.object(self.vm_lifecycle, "disarm_expiry_timer") as disarm,
            mock.patch.object(
                self.vm_lifecycle, "recover_vm_intents", side_effect=verified_recover
            ) as recovery,
        ):
            self.cluster.expire(self.root, run_id, token, admission=self.admission)
        self.assertEqual(recovery.call_count, 1)
        self.assertEqual(disarm.call_count, 1)
        self.assertEqual(disarm.call_args.args[1:3], (run_id, token))
        self.assertFalse(state.exists())
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_failed_vm_state_keeps_a_live_controller_during_automatic_sweep(self):
        run_id = "failed01"
        token = self.reserve_vm(run_id, creator=99999999)
        unit = self.vm.unit_name(run_id)
        state = self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "failed",
                "unit": unit,
                "admission_token": token,
                "pid": 99999999,
                "pid_start_ticks": 1,
                "expires_at": 0,
            },
        )
        with (
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
            ),
            mock.patch.object(
                self.cluster.CLUSTER_ENV,
                "vm_unit_state",
                return_value={
                    "LoadState": "loaded",
                    "ActiveState": "active",
                    "MainPID": "99999999",
                },
            ),
            mock.patch.object(self.vm, "VmRun") as owned_type,
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "labelled_runs", return_value={}),
            mock.patch.object(self.vm_lifecycle, "down_host") as stop,
        ):
            owned_type.return_value.absent_owned.return_value = False
            result = self.cluster.sweep(self.root, admission=self.admission)
        self.assertIn(unit, result["kept"])
        self.assertEqual(stop.call_count, 0)
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_direct_vm_down_cannot_cancel_live_creator_before_owner_exists(self):
        run_id = "early001"
        token = self.reserve_vm(run_id)
        record = {
            "run_id": run_id,
            "environment_kind": "vm",
            "status": "creating",
            "admission_token": token,
            "unit": self.vm.unit_name(run_id),
        }
        with mock.patch.object(self.vm.VmRun, "stop_owned", return_value=True) as stop:
            with self.assertRaisesRegex(self.vm.VmError, "VM_OWNERSHIP|VM_CLEANUP"):
                self.vm_lifecycle.down_host(
                    self.cluster, self.root, record, admission=self.admission
                )
        self.assertEqual(stop.call_count, 0)
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_native_sweep_preserves_state_until_cleanup_and_lease_release_succeed(self):
        for case, run_id in (("network", "retain01"), ("release", "retain02")):
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

                def refused_release(absent):
                    lease = self.admission.active_for_run(run_id)[0]
                    decision = absent(lease)
                    if decision is None:
                        return []
                    self.assertTrue(decision)
                    raise ValueError("ENV_STATE: synthetic lease release failed")

                cleanup_result = case != "network"
                with (
                    mock.patch.object(self.cluster, "list_clusters", return_value=[]),
                    mock.patch.object(self.cluster, "labelled_runs", return_value={}),
                    mock.patch.object(
                        self.cluster.CLUSTER_ENV, "create_inflight", return_value=False
                    ),
                    mock.patch.object(
                        self.cluster, "_cleanup_owned", return_value=cleanup_result
                    ),
                    mock.patch.object(
                        self.cluster, "_resources_absent", return_value=True
                    ),
                ):
                    if case == "release":
                        with mock.patch.object(
                            self.admission, "recover", side_effect=refused_release
                        ):
                            with self.assertRaisesRegex(ValueError, "ENV_STATE"):
                                self.cluster.sweep(self.root, admission=self.admission)
                    else:
                        self.cluster.sweep(self.root, admission=self.admission)
                self.assertTrue(state.exists())
                self.assertEqual(
                    [row["token"] for row in self.admission.active_for_run(run_id)],
                    [token],
                )

    def test_admission_inventory_includes_only_current_workspace_binding(self):
        admission_type = importlib.import_module("environment_admission").Admission
        budget = {
            "cpu": 1,
            "memory_mib": 512,
            "disk_mib": 512,
            "seconds": 60,
            "instances": 0,
        }
        own_token = self.admission.reserve(
            "invent01", "worker", [], budget, {"purpose": "owned"}
        )
        with tempfile.TemporaryDirectory(prefix="p07-foreign-binding-") as temporary:
            foreign_root = Path(temporary)
            subprocess.run(
                ["/usr/bin/git", "init", "--quiet", str(foreign_root)],
                check=True,
                capture_output=True,
                timeout=10,
            )
            foreign = admission_type(foreign_root, state_dir=self.root / "ledger")
            foreign_token = foreign.reserve(
                "invent02", "worker", [], budget, {"purpose": "foreign"}
            )
            self.assertEqual(
                {row["token"] for row in self.admission.active_for_binding()},
                {own_token},
            )
            self.assertEqual(
                {row["token"] for row in foreign.active_for_binding()}, {foreign_token}
            )

    def test_dead_vm_with_collected_unit_reaps_exact_owned_nonempty_directory(self):
        run_id = "collect1"
        token = self.reserve_vm(run_id, creator=99999999)
        unit = self.vm.unit_name(run_id)
        self.state(
            run_id,
            {
                "environment_kind": "vm",
                "status": "failed",
                "unit": unit,
                "admission_token": token,
                "pid": 99999999,
                "pid_start_ticks": 1,
                "expires_at": 0,
            },
        )
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.mkdir(mode=0o700)
        paths.raw.write_bytes(b"synthetic owned disk")
        show_allowed = {"value": False}

        def runner(command, **_kwargs):
            if command[:3] == ["systemctl", "--user", "is-active"]:
                output = "unknown\n"
                return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")
            elif command[:3] == ["systemctl", "--user", "show"]:
                return subprocess.CompletedProcess(
                    command,
                    0 if show_allowed["value"] else 1,
                    stdout="LoadState=not-found\nActiveState=inactive\nMainPID=0\n",
                    stderr="permission denied",
                )
            else:
                raise AssertionError("unexpected synthetic systemd operation")

        vm_type = self.vm.VmRun
        owned = vm_type(self.root, run_id, token, runner=runner)
        owned._save_owner(
            {
                "run_id": run_id,
                "token": token,
                "unit": unit,
                "workspace_id": self.admission.workspace_id,
                "binding_id": self.admission.binding_id,
                "main_pid": 99999998,
                "main_start": 1,
                "qemu_pid": 99999997,
                "qemu_start": 1,
            }
        )
        owned._record_files()
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
            mock.patch.object(
                self.cluster.CLUSTER_ENV, "creator_gone", return_value=True
            ),
            mock.patch.object(self.cluster.CLUSTER_ENV, "disarm_expiry_timer"),
            mock.patch.object(self.cluster, "list_clusters", return_value=[]),
            mock.patch.object(self.cluster, "labelled_runs", return_value={}),
        ):
            unknown_result = self.cluster.sweep(self.root, admission=self.admission)
            self.assertIn(unit, unknown_result["kept"])
            self.assertTrue(paths.directory.exists())
            self.assertEqual(
                [row["token"] for row in self.admission.active_for_run(run_id)], [token]
            )
            show_allowed["value"] = True
            result = self.cluster.sweep(self.root, admission=self.admission)
        self.assertIn(unit, result["deleted"], result)
        self.assertFalse(paths.directory.exists())
        self.assertEqual(self.admission.active_for_run(run_id), [])

    def test_interrupted_vm_file_cleanup_keeps_owner_and_retries_exact_files(self):
        run_id, token = "partial1", "a" * 32
        paths = self.vm.paths_for(self.root, run_id)
        paths.directory.parent.mkdir(parents=True, mode=0o700)
        paths.directory.mkdir(mode=0o700)
        paths.raw.write_bytes(b"synthetic raw")
        paths.vars.write_bytes(b"synthetic vars")

        def runner(command, **_kwargs):
            self.assertEqual(command[:3], ["systemctl", "--user", "show"])
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="LoadState=loaded\nActiveState=inactive\nMainPID=0\n",
                stderr="",
            )

        owned = self.vm.VmRun(self.root, run_id, token, runner=runner)
        owned._save_owner(
            {"run_id": run_id, "token": token, "unit": self.vm.unit_name(run_id)}
        )
        owned._record_files()
        original_unlink = os.unlink
        removed = []

        def interrupted_unlink(path, *args, **kwargs):
            name = Path(path).name
            if name != "owner.json" and (
                kwargs.get("dir_fd") is not None or Path(path).parent == paths.directory
            ):
                if removed:
                    raise OSError("synthetic interruption after one VM artifact")
                removed.append(name)
            return original_unlink(path, *args, **kwargs)

        def interrupted_rmtree(_directory):
            original_unlink(paths.directory / "owner.json")
            original_unlink(paths.raw)
            raise OSError("synthetic interruption after owner loss")

        with (
            mock.patch.object(self.vm, "_user_bus", return_value={}),
            mock.patch.object(self.vm.shutil, "rmtree", side_effect=interrupted_rmtree),
            mock.patch("os.unlink", side_effect=interrupted_unlink),
        ):
            try:
                first = owned.stop_owned()
            except (OSError, self.vm.VmError):
                first = False
        self.assertFalse(first)
        self.assertTrue((paths.directory / "owner.json").exists())
        with mock.patch.object(self.vm, "_user_bus", return_value={}):
            self.assertTrue(owned.stop_owned())
        self.assertTrue((paths.directory / "owner.json").exists())
        self.assertFalse(paths.raw.exists())
        self.assertFalse(paths.vars.exists())

    def test_vm_down_keeps_private_state_when_lease_release_fails(self):
        run_id = "vmrel001"
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
        record = self.cluster._read_state(self.root, run_id)
        with (
            mock.patch.object(self.vm.VmRun, "stop_owned", return_value=True),
            mock.patch.object(
                self.admission,
                "release",
                side_effect=ValueError("ENV_STATE: synthetic release"),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "ENV_STATE"):
                self.vm_lifecycle.down_host(
                    self.cluster, self.root, record, admission=self.admission
                )
        self.assertTrue(state.exists())
        self.assertEqual(
            [row["token"] for row in self.admission.active_for_run(run_id)], [token]
        )

    def test_guest_cli_imports_with_only_the_five_copied_scripts(self):
        public_scripts = (
            "test_cluster.py",
            "test_cluster_vm.py",
            "test_cluster_environment.py",
            "test_cluster_vm_transport.py",
            "environment_admission.py",
        )
        with tempfile.TemporaryDirectory(prefix="p07-guest-import-") as temporary:
            directory = Path(temporary)
            for name in public_scripts:
                shutil.copyfile(ROOT / "scripts" / name, directory / name)
            command = [
                sys.executable,
                "-I",
                "-c",
                f"import sys; sys.path.insert(0, {str(directory)!r}); import test_cluster",
            ]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_controller_checks_own_unit_caps_before_dummy_or_work(self):
        run_id, token = "owncap01", "a" * 32
        deadline = int(time.time()) + 300
        owned = self.vm.VmRun(self.root, run_id, token)
        with (
            mock.patch.object(owned, "_owner", return_value={"deadline": deadline}),
            mock.patch.object(owned, "_require_parent_lease"),
            mock.patch.object(owned, "_save_owner"),
            mock.patch.object(
                owned,
                "_own_cgroup_caps",
                side_effect=self.vm.VmError("VM_LIMIT: unbounded unit"),
                create=True,
            ),
            mock.patch.object(owned, "_start_dummy") as dummy,
            mock.patch.object(owned, "_controller_body") as work,
            mock.patch.object(owned, "_stop_dummy"),
        ):
            with self.assertRaisesRegex(self.vm.VmError, "VM_LIMIT"):
                owned.controller(deadline)
        dummy.assert_not_called()
        work.assert_not_called()


if __name__ == "__main__":
    unittest.main()
