"""Regressions for the parallel work dispatcher (W10-PARALLEL, D10 and D11)."""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import multiprocessing
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
PY = sys.executable


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PARALLEL = _load("work_parallel", "scripts/work_parallel.py")
GIT_ENV = {
    "PATH": "/usr/bin:/bin",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
}


def write(path: str, text: str, sleep: float = 0.0) -> list[str]:
    """A shell worker that waits, then writes one file in its clone."""
    code = (
        "import pathlib,time;"
        f"time.sleep({sleep});"
        f"p=pathlib.Path({path!r});p.parent.mkdir(parents=True,exist_ok=True);"
        f"p.write_text({text!r})"
    )
    return [PY, "-c", code]


def allow(unit) -> None:
    return None


def orphan_dispatcher(root, plan, runtime, admission_state):
    admission = importlib.import_module("environment_admission").Admission(
        root, state_dir=admission_state
    )
    PARALLEL.run(root, plan, runtime=runtime, preflight=allow, admission=admission)


def competing_reservation(root, state, run_id, closure, barrier, results):
    module = importlib.import_module("environment_admission")
    admission = module.Admission(root, state_dir=state)
    barrier.wait(timeout=10)
    budget = {
        "cpu": 1,
        "memory_mib": 512,
        "disk_mib": 512,
        "seconds": 60,
        "instances": 0,
    }
    try:
        token = admission.reserve(run_id, "worker", closure, budget, {"owner": run_id})
    except module.AdmissionError as exc:
        results.put(("denied", str(exc)))
    else:
        results.put(("admitted", token))


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="work-parallel-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo"
        self.root.mkdir()
        self.runtime = self.root.parent / "runtime"
        self.admission_state = self.root.parent / "admission-state"
        self.git("init", "--quiet", "--initial-branch=main")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "a.md").write_text("a\n")
        (self.root / "docs" / "b.md").write_text("b\n")
        (self.root / "src.txt").write_text("source\n")
        (self.root / ".gitignore").write_text("*.out\n")
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "fixture")

    def git(self, *args: str) -> str:
        return subprocess.run(
            [
                "/usr/bin/git",
                "-c",
                "user.name=F",
                "-c",
                "user.email=f@x.invalid",
                *args,
            ],
            cwd=self.root,
            env=GIT_ENV,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()

    def brief_files(self, paths):
        baseline = self.git("rev-parse", "HEAD")
        current = {
            "request_ref": "fixture:user:1",
            "request_digest": hashlib.sha256(b"r").hexdigest(),
            "request_revision": "r1",
            "workspace_id": str(self.root),
            "baseline_id": baseline,
            "brief_id": "fixture-brief",
            "revision": 1,
            "goal": "Edit a.md.",
            "in_scope": ["a.md"],
            "out_of_scope": [],
            "constraints": [],
            "acceptance_criteria": ["a.md edited"],
            "allowed_mutations": paths,
            "expected_checks": [],
            "risk": "low",
            "authority_ref": "fixture:approval",
            "material_inputs": {
                path: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
                for path in paths
            },
            "allowed_actions": {
                "write-worker": {"operation": "dispatch", "paths": paths}
            },
            "unresolved_questions": [],
            "state": "current",
        }
        brief = {
            **{k: v for k, v in current.items() if k != "allowed_actions"},
            "contract_version": "3.0.0",
            "known_facts": [],
            "assumptions": [],
            "state": "ready",
        }
        brief_file = self.root.parent / "brief.json"
        current_file = self.root.parent / "current.json"
        brief_file.write_text(json.dumps(brief))
        current_file.write_text(json.dumps(current))
        return brief_file, current_file

    def unit(self, uid: str, command, owned, **extra):
        return {
            "id": uid,
            "action": "write-worker",
            "depends_on": [],
            "owned_paths": owned,
            "resources": [],
            "services": [],
            "command": command,
            "timeout": 30,
            **extra,
        }

    def plan(self, *units, check=None, workers=4):
        return {
            "task_ref": "SPEC-0161 W10-PARALLEL fixture",
            "base": "HEAD",
            "max_workers": workers,
            "integration_check": check or [PY, "-c", "pass"],
            "units": list(units),
        }

    def run_plan(self, plan, **kwargs):
        kwargs.setdefault("preflight", allow)
        kwargs.setdefault(
            "admission",
            importlib.import_module("environment_admission").Admission(
                self.root, state_dir=self.admission_state
            ),
        )
        return PARALLEL.run(self.root, plan, runtime=self.runtime, **kwargs)

    def assertRefused(self, code: str, call, *args, **kwargs) -> None:
        with self.assertRaises(PARALLEL.ParallelError) as caught:
            call(*args, **kwargs)
        self.assertTrue(str(caught.exception).startswith(code), str(caught.exception))

    def assertNoResidue(self, report) -> None:
        run_dir = self.runtime / report["run"]
        self.assertEqual(sorted(p.name for p in run_dir.glob("clone-*")), [])
        for pid in report["pids"]:
            with self.subTest(pid=pid):
                self.assertFalse(Path(f"/proc/{pid}").exists())

    def overlap(self, first, second) -> bool:
        return (
            first["started"] < second["finished"]
            and second["started"] < first["finished"]
        )


class PlanTest(Fixture):
    def test_bad_plans_are_refused_before_any_worker(self):
        ok = self.unit("a", write("docs/a.md", "x"), ["docs/a.md"])
        cases = {
            "PARALLEL_PLAN": [
                self.plan(ok, dict(ok)),
                self.plan(dict(ok, owned_paths=["/etc/passwd"])),
                self.plan(dict(ok, owned_paths=["../x"])),
                self.plan(dict(ok, owned_paths=[])),
                self.plan(dict(ok, command=[])),
                self.plan(ok, workers=0),
                self.plan(ok, workers=(os.cpu_count() or 1) + 1),
            ],
            "PARALLEL_DEPENDENCY": [
                self.plan(dict(ok, depends_on=["missing"])),
                self.plan(
                    dict(ok, depends_on=["b"]),
                    self.unit("b", ["true"], ["docs/b.md"], depends_on=["a"]),
                ),
            ],
            "PARALLEL_SERVICES": [
                self.plan(dict(ok, services=["all"])),
                self.plan(dict(ok, services=["*"])),
                self.plan(dict(ok, services=["platform-*"])),
            ],
        }
        for code, plans in cases.items():
            for plan in plans:
                with self.subTest(code=code, plan=plan):
                    self.assertRefused(
                        code, PARALLEL.load_plan, plan, closure=lambda s: list(s)
                    )

    def test_a_unit_whose_closure_exceeds_the_limit_is_refused(self):
        plan = self.plan(
            self.unit("a", ["true"], ["docs/a.md"], services=["x"]),
        )
        self.assertRefused(
            "PARALLEL_SERVICES",
            PARALLEL.load_plan,
            plan,
            closure=lambda s: ["x", "y", "z", "w", "v"],
        )


class AdmissionCapacityTest(Fixture):
    def test_cluster_receipt_retains_live_or_ambiguous_child_and_cancels_gate_on_release(
        self,
    ):
        module = importlib.import_module("environment_admission")
        environment = importlib.import_module("test_cluster_environment")
        admission = module.Admission(self.root, state_dir=self.admission_state)
        token = admission.reserve(
            "cluster1",
            "cluster",
            ["selected"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 1,
            },
            {"cluster": "hyk8s-test-cluster1"},
        )
        gate, receipt = admission._gate(token), admission.child_receipt_path(token)
        self.assertEqual(gate.read_bytes(), b"active\n")
        self.assertFalse(environment.create_inflight(admission, token))
        receipt.write_text("malformed")
        receipt.chmod(0o600)
        self.assertTrue(environment.create_inflight(admission, token))
        receipt.write_text(f"12345 77 12345 {os.geteuid()}\n")
        with mock.patch.object(environment, "_process_start", return_value=77):
            self.assertTrue(environment.create_inflight(admission, token))
        with (
            mock.patch.object(environment, "_process_start", return_value=None),
            mock.patch.object(environment.os, "killpg", side_effect=PermissionError),
        ):
            self.assertTrue(environment.create_inflight(admission, token))
        with (
            mock.patch.object(environment, "_process_start", return_value=None),
            mock.patch.object(environment.os, "killpg", side_effect=ProcessLookupError),
        ):
            self.assertFalse(environment.create_inflight(admission, token))
            admission.release(
                token,
                lambda row: not environment.create_inflight(admission, row["token"]),
            )
        self.assertFalse(gate.exists())
        self.assertFalse(receipt.exists())

    def test_private_ledger_rejects_symlink_and_public_database(self):
        module = importlib.import_module("environment_admission")
        state = self.root.parent / "private-ledger"
        state.mkdir(mode=0o700)
        alias = self.root.parent / "ledger-alias"
        alias.symlink_to(state, target_is_directory=True)
        with self.assertRaisesRegex(module.AdmissionError, "ENV_STATE"):
            module.Admission(self.root, state_dir=alias)
        admission = module.Admission(self.root, state_dir=state)
        admission.db.chmod(0o644)
        with self.assertRaisesRegex(module.AdmissionError, "ENV_STATE"):
            module.Admission(self.root, state_dir=state)

    def test_invalid_request_is_refused_without_creating_a_lease(self):
        module = importlib.import_module("environment_admission")
        admission = module.Admission(self.root, state_dir=self.admission_state)
        budget = {
            "cpu": 1,
            "memory_mib": 512,
            "disk_mib": 512,
            "seconds": 60,
            "instances": 0,
        }
        cases = (
            ("../escape", ["safe"], budget, "ENV_BINDING"),
            ("safe0001", ["all*"], budget, "ENV_BINDING"),
            ("safe0001", ["safe"], budget | {"cpu": True}, "ENV_LIMIT"),
            ("safe0001", ["safe"], budget | {"seconds": 0}, "ENV_LIMIT"),
        )
        for run_id, closure, requested, code in cases:
            with self.subTest(run_id=run_id, closure=closure, requested=requested):
                with self.assertRaisesRegex(module.AdmissionError, code):
                    admission.reserve(run_id, "worker", closure, requested, {})
        self.assertEqual(admission.active_for_run("safe0001"), [])

    def test_missing_process_gate_keeps_the_reservation(self):
        module = importlib.import_module("environment_admission")
        admission = module.Admission(self.root, state_dir=self.admission_state)
        token = admission.reserve(
            "gate0001",
            "worker",
            ["safe"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 0,
            },
            {"owner": "fixture"},
        )
        (self.admission_state / f"{token}.gate").unlink()
        with self.assertRaisesRegex(module.AdmissionError, "ENV_STATE"):
            admission.release(token, lambda _: True)
        self.assertEqual(admission.active_for_run("gate0001")[0]["token"], token)

    def test_cluster_run_id_cannot_be_reused_while_another_binding_is_active(self):
        other = self.root.parent / "other-cluster-repo"
        subprocess.run(
            ["/usr/bin/git", "init", "--quiet", str(other)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        module = importlib.import_module("environment_admission")
        state = self.root.parent / "cluster-id-ledger"
        first = module.Admission(self.root, state_dir=state)
        second = module.Admission(other, state_dir=state)
        budget = {
            "cpu": 1,
            "memory_mib": 512,
            "disk_mib": 512,
            "seconds": 60,
            "instances": 1,
        }
        token = first.reserve("same0001", "cluster", ["a"], budget, {"owner": "first"})
        with self.assertRaisesRegex(module.AdmissionError, "ENV_BINDING"):
            second.reserve("same0001", "cluster", ["a"], budget, {"owner": "second"})
        self.assertEqual(first.active_for_run("same0001")[0]["token"], token)

    def test_two_processes_in_distinct_repositories_compete_atomically(self):
        other = self.root.parent / "other-repo"
        subprocess.run(
            ["/usr/bin/git", "init", "--quiet", str(other)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        context = multiprocessing.get_context("fork")
        barrier, results = context.Barrier(3), context.Queue()
        state = self.root.parent / "atomic-ledger"
        competitors = [
            context.Process(
                target=competing_reservation,
                args=(root, state, run_id, closure, barrier, results),
            )
            for root, run_id, closure in (
                (self.root, "first001", ["a", "b", "c"]),
                (other, "second01", ["d", "e"]),
            )
        ]
        try:
            for process in competitors:
                process.start()
            barrier.wait(timeout=10)
            outcomes = [results.get(timeout=10) for _ in competitors]
            for process in competitors:
                process.join(timeout=10)
            self.assertTrue(all(process.exitcode == 0 for process in competitors))
            self.assertEqual(
                sorted(status for status, _ in outcomes), ["admitted", "denied"]
            )
            self.assertIn(
                "ENV_LIMIT",
                next(detail for status, detail in outcomes if status == "denied"),
            )
        finally:
            for process in competitors:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=5)

    def test_account_headroom_counts_existing_reservations(self):
        module = importlib.import_module("environment_admission")
        available_disk = mock.Mock(f_bavail=7 * 1024 * 1024, f_frsize=1024)
        for dimension in ("memory_mib", "disk_mib"):
            with self.subTest(dimension=dimension):
                state = self.root.parent / f"ledger-{dimension}"
                first = module.Admission(self.root, state_dir=state)
                second = module.Admission(self.root, state_dir=state)
                budget = {
                    "cpu": 1,
                    "memory_mib": 512,
                    "disk_mib": 512,
                    "seconds": 60,
                    "instances": 0,
                }
                budget[dimension] = 4096
                with (
                    mock.patch.object(
                        module, "_available_memory_mib", return_value=7168
                    ),
                    mock.patch.object(
                        module.os, "statvfs", return_value=available_disk
                    ),
                ):
                    first.reserve(
                        "first001", "worker", ["same"], budget, {"owner": "first"}
                    )
                    with self.assertRaisesRegex(module.AdmissionError, "ENV_LIMIT"):
                        second.reserve(
                            "second01", "worker", ["same"], budget, {"owner": "second"}
                        )


class DispatchTest(Fixture):
    def test_integration_refusal_does_not_execute_the_check(self):
        module = importlib.import_module("environment_admission")
        admission = module.Admission(self.root, state_dir=self.admission_state)
        original = admission.reserve
        marker = self.root.parent / "integration-should-not-run"

        def reserve(run_id, kind, closure, budget, intent):
            if kind == "integration":
                raise module.AdmissionError("ENV_LIMIT: fixture headroom")
            return original(run_id, kind, closure, budget, intent)

        with mock.patch.object(admission, "reserve", side_effect=reserve):
            report = self.run_plan(
                self.plan(
                    self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                    check=[
                        PY,
                        "-c",
                        f"from pathlib import Path;Path({str(marker)!r}).touch()",
                    ],
                ),
                admission=admission,
            )
        self.assertEqual(report["units"]["a"]["state"], "promoted")
        self.assertEqual(report["integration"]["state"], "ERROR")
        self.assertIn("ENV_LIMIT", report["integration"]["reason"])
        self.assertFalse(marker.exists())

    def test_separate_dispatchers_cannot_exceed_the_shared_service_union(self):
        admission_type = importlib.import_module("environment_admission").Admission
        ledger = self.root.parent / "shared-admission"
        closures = {"x": ["x", "n1", "n2"], "y": ["y", "n3"]}

        def closure(selected):
            return sorted({name for app in selected for name in closures[app]})

        first = self.plan(
            self.unit(
                "first", write("docs/a.md", "A\n", 3.0), ["docs/a.md"], services=["x"]
            )
        )
        second = self.plan(
            self.unit(
                "second", write("docs/b.md", "B\n"), ["docs/b.md"], services=["y"]
            )
        )
        outcome = {}

        def first_dispatcher():
            try:
                outcome["first"] = self.run_plan(
                    first, closure=closure, admission=admission_type(self.root, ledger)
                )
            except Exception as exc:
                outcome["first_error"] = exc

        worker = threading.Thread(target=first_dispatcher)
        worker.start()
        deadline = time.monotonic() + 10
        active = False
        while time.monotonic() < deadline:
            for state_file in self.runtime.glob("*/state.json"):
                state = json.loads(state_file.read_text())
                if state.get("workers"):
                    active = True
                    break
            if active or not worker.is_alive():
                break
            time.sleep(0.02)
        self.assertTrue(active, outcome)
        try:
            outcome["second"] = self.run_plan(
                second, closure=closure, admission=admission_type(self.root, ledger)
            )
        except Exception as exc:
            outcome["second_error"] = exc
        worker.join(timeout=10)
        self.assertFalse(worker.is_alive(), outcome)
        self.assertNotIn("first_error", outcome)
        if "second_error" in outcome:
            self.assertRegex(
                str(outcome["second_error"]), "ENV_LIMIT|PARALLEL_ADMISSION"
            )
        else:
            second_unit = outcome["second"]["units"]["second"]
            if second_unit["state"] == "promoted":
                first_unit = outcome["first"]["units"]["first"]
                self.assertFalse(self.overlap(first_unit, second_unit))
            else:
                self.assertEqual(second_unit["state"], "refused")
                self.assertRegex(second_unit["reason"], "ENV_LIMIT|PARALLEL_ADMISSION")

    def test_independent_units_run_together_and_integrate(self):
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n", 0.8), ["docs/a.md"]),
                self.unit("b", write("docs/b.md", "B\n", 0.8), ["docs/b.md"]),
            )
        )
        units = report["units"]
        self.assertEqual(report["state"], "completed")
        self.assertEqual({u["state"] for u in units.values()}, {"promoted"})
        self.assertTrue(self.overlap(units["a"], units["b"]))
        self.assertEqual(report["integration"]["state"], "PASS")
        candidate = Path(report["candidate"]).read_text()
        self.assertIn("+A", candidate)
        self.assertIn("+B", candidate)
        # The source checkout is never written; the candidate is a patch.
        self.assertEqual((self.root / "docs" / "a.md").read_text(), "a\n")
        for key in ("elapsed", "setup", "workers", "integration_seconds"):
            self.assertIn(key, report["timing"])
        self.assertNoResidue(report)

    def test_shared_resources_and_overlapping_paths_serialize(self):
        report = self.run_plan(
            self.plan(
                self.unit(
                    "a",
                    write("docs/a.md", "A\n", 0.5),
                    ["docs/a.md"],
                    resources=["compose:demo"],
                ),
                self.unit(
                    "b",
                    write("src.txt", "S\n", 0.5),
                    ["src.txt"],
                    resources=["compose:demo"],
                ),
                self.unit("c", write("docs/b.md", "C\n", 0.5), ["docs/"]),
            )
        )
        units = report["units"]
        self.assertEqual({u["state"] for u in units.values()}, {"promoted"})
        self.assertFalse(self.overlap(units["a"], units["b"]))
        self.assertFalse(self.overlap(units["a"], units["c"]))
        self.assertEqual(report["integration"]["state"], "PASS")

    def test_a_dependent_starts_from_its_upstream_result(self):
        read_then_write = [
            PY,
            "-c",
            "import pathlib;t=pathlib.Path('docs/a.md').read_text();"
            "pathlib.Path('docs/b.md').write_text('saw '+t)",
        ]
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                self.unit("b", read_then_write, ["docs/b.md"], depends_on=["a"]),
            )
        )
        self.assertEqual(report["units"]["b"]["state"], "promoted")
        candidate = Path(report["candidate"]).read_text()
        self.assertIn("+saw A", candidate)
        self.assertEqual(candidate.count("+A"), 1)

    def test_a_failure_blocks_only_its_downstream(self):
        report = self.run_plan(
            self.plan(
                self.unit("a", [PY, "-c", "raise SystemExit(3)"], ["docs/a.md"]),
                self.unit(
                    "b", write("docs/b.md", "B\n"), ["docs/b.md"], depends_on=["a"]
                ),
                self.unit("c", write("src.txt", "S\n"), ["src.txt"]),
            )
        )
        units = report["units"]
        self.assertEqual(units["a"]["state"], "failed")
        self.assertEqual(units["b"]["state"], "blocked")
        self.assertEqual(units["c"]["state"], "promoted")
        self.assertEqual(report["state"], "failed")
        # The independent result still reaches the candidate.
        self.assertIn("+S", Path(report["candidate"]).read_text())

    def test_a_change_outside_the_owned_paths_is_refused(self):
        report = self.run_plan(
            self.plan(self.unit("a", write("src.txt", "stolen\n"), ["docs/a.md"]))
        )
        self.assertEqual(report["units"]["a"]["state"], "refused")
        self.assertIn("PARALLEL_OWNERSHIP", report["units"]["a"]["reason"])
        self.assertIsNone(report["candidate"])

    def test_preflight_refusal_stops_only_that_unit(self):
        def preflight(unit):
            if unit["id"] == "a":
                raise PARALLEL.ParallelError("PARALLEL_BRIEF: outside scope")

        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                self.unit("b", write("docs/b.md", "B\n"), ["docs/b.md"]),
            ),
            preflight=preflight,
        )
        self.assertEqual(report["units"]["a"]["state"], "refused")
        self.assertEqual(report["units"]["a"]["attempts"], 0)
        self.assertEqual(report["units"]["b"]["state"], "promoted")

    def test_worker_receives_its_envelope(self):
        dump = [
            PY,
            "-c",
            "import os,json,pathlib;pathlib.Path('docs/a.md').write_text(json.dumps("
            "{k:v for k,v in os.environ.items() if k.startswith('HYK8S_PARALLEL_')}))",
        ]
        report = self.run_plan(
            self.plan(self.unit("a", dump, ["docs/a.md"])), brief_revision="7"
        )
        patch = Path(report["candidate"]).read_text()
        line = next(x for x in patch.splitlines() if x.startswith("+{"))
        env = json.loads(line[1:])
        self.assertEqual(env["HYK8S_PARALLEL_RUN"], report["run"])
        self.assertEqual(env["HYK8S_PARALLEL_UNIT"], "a")
        self.assertEqual(env["HYK8S_PARALLEL_ATTEMPT"], "1")
        self.assertEqual(env["HYK8S_PARALLEL_BRIEF_REVISION"], "7")
        self.assertEqual(
            env["HYK8S_PARALLEL_TASK_REF"], "SPEC-0161 W10-PARALLEL fixture"
        )
        self.assertEqual(env["HYK8S_PARALLEL_BASE"], self.git("rev-parse", "HEAD"))
        self.assertIn("path:docs/a.md", json.loads(env["HYK8S_PARALLEL_TOKENS"]))

    def test_worker_pass_does_not_replace_the_integration_check(self):
        check = [
            PY,
            "-c",
            "import pathlib,sys;"
            "sys.exit(0 if pathlib.Path('docs/a.md').read_text()=="
            "pathlib.Path('docs/b.md').read_text() else 1)",
        ]
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                self.unit("b", write("docs/b.md", "B\n"), ["docs/b.md"]),
                check=check,
            )
        )
        self.assertEqual({u["state"] for u in report["units"].values()}, {"promoted"})
        self.assertEqual(report["integration"]["state"], "FAIL")
        self.assertEqual(report["state"], "failed")

    def test_concurrent_service_union_stays_within_the_limit(self):
        closures = {"x": ["x", "n1", "n2"], "y": ["y", "n1", "n3"]}

        def closure(selection):
            return sorted({a for s in selection for a in closures[s]})

        report = self.run_plan(
            self.plan(
                self.unit(
                    "a", write("docs/a.md", "A\n", 0.5), ["docs/a.md"], services=["x"]
                ),
                self.unit(
                    "b", write("docs/b.md", "B\n", 0.5), ["docs/b.md"], services=["y"]
                ),
            ),
            closure=closure,
        )
        units = report["units"]
        # Union {x,y,n1,n2,n3} exceeds 4, so the two never run together.
        self.assertFalse(self.overlap(units["a"], units["b"]))
        self.assertEqual({u["state"] for u in units.values()}, {"promoted"})


class LeaseTest(Fixture):
    def test_dispatcher_cannot_release_another_runs_pre_spawn_lease(self):
        admission_type = importlib.import_module("environment_admission").Admission
        admission = admission_type(self.root, state_dir=self.admission_state)
        other = "bbbbbbbb"
        token = admission.reserve(
            other,
            "worker",
            ["selected"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 0,
            },
            {"worker": "synthetic"},
        )
        owner = mock.Mock(
            id="aaaaaaaa", admission=admission, unreleased=False, release_error=None
        )
        with self.assertRaisesRegex(Exception, "ENV_STATE"):
            PARALLEL._Run.release(owner, token)
        self.assertEqual(
            [row["token"] for row in admission.active_for_run(other)], [token]
        )

    def test_sweep_rechecks_actual_lease_after_stale_token_prefetch(self):
        admission_type = importlib.import_module("environment_admission").Admission
        admission = admission_type(self.root, state_dir=self.admission_state)
        other, stale = "bbbbbbbb", "aaaaaaaa"
        token = admission.reserve(
            other,
            "worker",
            ["selected"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 0,
            },
            {"worker": "synthetic"},
        )
        directory = self.runtime / stale
        directory.mkdir(parents=True)
        (directory / "dispatcher.lock").touch()
        (directory / "state.json").write_text(json.dumps({"run": stale, "workers": []}))
        prefetched = admission.active_for_run(other)[0] | {"run_id": stale}
        with mock.patch.object(admission, "active_for_run", return_value=[prefetched]):
            self.assertEqual(PARALLEL.sweep(self.runtime, admission=admission), [])
        self.assertTrue(directory.exists())
        self.assertEqual(
            [row["token"] for row in admission.active_for_run(other)], [token]
        )

    def test_fencing_rejects_a_stale_holder(self):
        locks = self.runtime / "locks"
        first = PARALLEL.Leases(locks)
        second = PARALLEL.Leases(locks)  # another run in another process
        old = first.acquire(["compose:demo"])
        self.assertIsNotNone(old)
        self.assertIsNone(second.acquire(["compose:demo"]))
        first.check(old)
        first.release(old)
        new = second.acquire(["compose:demo"])
        self.assertGreater(new["compose:demo"], old["compose:demo"])
        self.assertRefused("PARALLEL_FENCED", first.check, old)
        second.check(new)
        second.release(new)

    def test_an_expired_attempt_is_retried_with_a_new_token(self):
        slow_first = [
            PY,
            "-c",
            "import os,time,pathlib\n"
            "if os.environ['HYK8S_PARALLEL_ATTEMPT']=='1': time.sleep(30)\n"
            "pathlib.Path('docs/a.md').write_text('second\\n')",
        ]
        report = self.run_plan(
            self.plan(self.unit("a", slow_first, ["docs/a.md"], timeout=1, retries=1))
        )
        unit = report["units"]["a"]
        self.assertEqual(unit["state"], "promoted")
        self.assertEqual(unit["attempts"], 2)
        self.assertEqual(unit["expired"][0]["reason"], "PARALLEL_TIMEOUT")
        self.assertGreater(
            unit["tokens"]["path:docs/a.md"],
            unit["expired"][0]["tokens"]["path:docs/a.md"],
        )
        self.assertIn("+second", Path(report["candidate"]).read_text())
        self.assertNoResidue(report)


class CancelTest(Fixture):
    def test_cancel_stops_workers_and_leaves_nothing_running(self):
        marker = self.root.parent / "late-marker"
        late = [
            PY,
            "-c",
            f"import time,pathlib;time.sleep(1.5);pathlib.Path({str(marker)!r}).write_text('x')",
        ]
        cancel = threading.Event()
        threading.Timer(0.5, cancel.set).start()
        report = self.run_plan(
            self.plan(
                self.unit("a", late, ["docs/a.md"]),
                self.unit(
                    "b", write("docs/b.md", "B\n"), ["docs/b.md"], depends_on=["a"]
                ),
            ),
            cancel=cancel,
        )
        self.assertEqual(report["state"], "cancelled")
        self.assertEqual(report["units"]["a"]["state"], "cancelled")
        self.assertEqual(report["units"]["b"]["state"], "cancelled")
        self.assertEqual(report["integration"]["state"], "SKIPPED")
        time.sleep(1.5)
        self.assertFalse(marker.exists())
        self.assertNoResidue(report)

    def test_sweep_cleans_up_after_a_killed_dispatcher(self):
        pidfile = self.root.parent / "orphan.pid"
        admission_state = self.root.parent / "admission-state"
        plan = self.plan(
            self.unit(
                "a",
                ["sh", "-c", f"sleep 60 & echo $! > '{pidfile}'; sleep 1"],
                ["docs/a.md"],
            )
        )
        dispatcher = multiprocessing.get_context("fork").Process(
            target=orphan_dispatcher,
            args=(self.root, plan, self.runtime, admission_state),
        )
        dispatcher.start()
        deadline = time.monotonic() + 15
        state = None
        while time.monotonic() < deadline:
            found = list(self.runtime.glob("*/state.json"))
            if found:
                state = json.loads(found[0].read_text())
                if state["workers"]:
                    break
            time.sleep(0.05)
        self.assertTrue(state and state["workers"], state)
        dispatcher.kill()
        dispatcher.join(timeout=5)
        # The group leader exits after 1 s; its child keeps running as the orphan.
        self.assertTrue(wait_dead(state["workers"][0]["pid"]))
        orphan = int(pidfile.read_text())
        self.assertFalse(wait_dead(orphan, 0.3))
        admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=admission_state
        )
        cleaned = PARALLEL.sweep(self.runtime, admission=admission)
        self.assertEqual(cleaned, [state["run"]])
        self.assertTrue(wait_dead(orphan))
        self.assertFalse((self.runtime / state["run"]).exists())
        self.assertEqual(PARALLEL.sweep(self.runtime, admission=admission), [])

    def test_sweep_recovers_a_child_started_before_dispatcher_state_was_saved(self):
        run_id = "0123abcd"
        run_dir = self.runtime / run_id
        run_dir.mkdir(parents=True)
        (run_dir / "state.json").write_text(
            json.dumps({"run": run_id, "dispatcher": 999999999, "workers": []})
        )
        admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=self.admission_state
        )
        token = admission.reserve(
            run_id,
            "worker",
            ["fixture-service"],
            {
                "cpu": 1,
                "memory_mib": 512,
                "disk_mib": 512,
                "seconds": 60,
                "instances": 0,
            },
            {"unit": "fixture"},
        )
        child = subprocess.Popen(
            [PY, "-c", "import time; time.sleep(60)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            preexec_fn=lambda: admission.write_child_receipt(token),
        )
        try:
            self.assertEqual(admission.active_for_run(run_id)[0]["pid"], None)
            self.assertTrue(admission.child_receipt_path(token).exists())
            self.assertEqual(
                PARALLEL.sweep(self.runtime, admission=admission), [run_id]
            )
            self.assertTrue(wait_dead(child.pid))
            self.assertEqual(admission.active_for_run(run_id), [])
            self.assertFalse(run_dir.exists())
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
            child.wait(timeout=5)


class BriefTest(Fixture):
    def test_the_real_brief_preflight_refuses_a_widened_worker(self):
        brief_file, current_file = self.brief_files(["docs/a.md"])
        preflight = PARALLEL.brief_preflight(self.root, brief_file, current_file)
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                self.unit("b", write("docs/b.md", "B\n"), ["docs/b.md"]),
            ),
            preflight=preflight,
        )
        self.assertEqual(report["units"]["a"]["state"], "promoted")
        self.assertEqual(report["units"]["b"]["state"], "refused")
        self.assertIn("PARALLEL_BRIEF", report["units"]["b"]["reason"])


def wait_dead(pid: int, seconds: float = 5.0) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not Path(f"/proc/{pid}").exists():
            return True
        try:
            if Path(f"/proc/{pid}/stat").read_text().split(") ")[1][0] == "Z":
                return True
        except (OSError, IndexError):
            return True
        time.sleep(0.05)
    return False


class ReviewTest(Fixture):
    def sh(self, script: str) -> list[str]:
        return ["sh", "-c", script]

    def test_ownership_sees_renames_deletions_and_odd_names(self):
        cases = {
            "rename": (self.sh("mv src.txt docs/moved.md"), ["docs/"], "src.txt"),
            "delete": (self.sh("rm src.txt"), ["docs/a.md"], "src.txt"),
            "space": (
                self.sh("mkdir ' docs' && echo hi > ' docs/a.md'"),
                ["docs/a.md"],
                " docs/a.md",
            ),
            "sibling": (self.sh("echo x > docs2.md"), ["docs/"], "docs2.md"),
        }
        for name, (command, owned, path) in cases.items():
            with self.subTest(name):
                report = self.run_plan(self.plan(self.unit("a", command, owned)))
                unit = report["units"]["a"]
                self.assertEqual(unit["state"], "refused", unit)
                self.assertIn(path, unit["changed"])
                self.assertIn("PARALLEL_OWNERSHIP", unit["reason"])

    def test_ignored_output_is_reported_not_silently_dropped(self):
        report = self.run_plan(
            self.plan(
                self.unit(
                    "a", self.sh("echo A > docs/a.md; echo x > x.out"), ["docs/a.md"]
                )
            )
        )
        unit = report["units"]["a"]
        self.assertEqual(unit["state"], "promoted")
        self.assertEqual(unit["ignored"], ["x.out"])

    def test_a_token_changed_during_the_attempt_is_refused_at_promotion(self):
        lock = PARALLEL.Leases(self.runtime / "locks")._file("path:docs/a.md")
        command = self.sh(f"echo A > docs/a.md; echo 99 > '{lock}'")
        report = self.run_plan(self.plan(self.unit("a", command, ["docs/a.md"])))
        unit = report["units"]["a"]
        self.assertEqual(unit["state"], "refused")
        self.assertIn("PARALLEL_FENCED", unit["reason"])
        self.assertIsNone(report["candidate"])

    def test_cross_run_locks_cover_directory_prefixes(self):
        locks = self.runtime / "locks"
        first, second = PARALLEL.Leases(locks), PARALLEL.Leases(locks)
        held = first.acquire(*PARALLEL.lock_keys(["docs/"], []))
        self.assertIsNotNone(held)
        self.assertIsNone(second.acquire(*PARALLEL.lock_keys(["docs/a.md"], [])))
        first.release(held)
        a = first.acquire(*PARALLEL.lock_keys(["docs/a.md"], []))
        b = second.acquire(*PARALLEL.lock_keys(["docs/b.md"], []))
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNone(
            PARALLEL.Leases(locks).acquire(*PARALLEL.lock_keys(["docs/"], []))
        )
        first.release(a)
        second.release(b)

    def test_unsafe_plan_strings_are_refused(self):
        ok = self.unit("a", ["true"], ["docs/a.md"])
        for plan in (
            self.plan(dict(ok, command=["tr\0ue"])),
            dict(self.plan(ok), base="--output=/tmp/x"),
        ):
            with self.subTest(plan=plan):
                self.assertRefused("PARALLEL_PLAN", PARALLEL.load_plan, plan)

    def test_a_git_failure_fails_only_that_unit(self):
        report = self.run_plan(
            self.plan(
                self.unit("a", self.sh("echo junk > .git/index"), ["docs/a.md"]),
                self.unit("b", write("docs/b.md", "B\n"), ["docs/b.md"]),
            )
        )
        self.assertEqual(report["units"]["a"]["state"], "failed")
        self.assertIn("PARALLEL_GIT", report["units"]["a"]["reason"])
        self.assertEqual(report["units"]["b"]["state"], "promoted")
        self.assertNoResidue(report)

    def test_cancel_kills_a_grandchild_promptly(self):
        pidfile = self.root.parent / "grandchild.pid"
        cancel = threading.Event()
        threading.Timer(0.5, cancel.set).start()
        begin = time.monotonic()
        report = self.run_plan(
            self.plan(
                self.unit(
                    "a",
                    self.sh(f"sleep 30 & echo $! > '{pidfile}'; wait"),
                    ["docs/a.md"],
                )
            ),
            cancel=cancel,
        )
        self.assertLess(time.monotonic() - begin, 1.5)
        self.assertEqual(report["state"], "cancelled")
        self.assertTrue(wait_dead(int(pidfile.read_text())))

    def test_cancel_works_when_the_caller_blocks_interrupt_signals(self):
        # qa.py starts each gate with SIGINT and SIGTERM blocked; children
        # inherit the mask, so a worker must not keep it.
        marker = self.root.parent / "masked-marker"
        # A Python worker keeps the mask it inherits (dash would clear it).
        late = [
            PY,
            "-c",
            f"import time,pathlib;time.sleep(1);pathlib.Path({str(marker)!r}).touch()",
        ]
        blocked = {signal.SIGINT, signal.SIGTERM}
        previous = signal.pthread_sigmask(signal.SIG_BLOCK, blocked)
        try:
            cancel = threading.Event()
            threading.Timer(0.5, cancel.set).start()
            begin = time.monotonic()
            report = self.run_plan(
                self.plan(self.unit("a", late, ["docs/a.md"])), cancel=cancel
            )
            took = time.monotonic() - begin
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous)
        self.assertEqual(report["state"], "cancelled")
        self.assertLess(took, 1.0)
        time.sleep(1.0)
        self.assertFalse(marker.exists())

    def test_cancel_under_a_subreaper_does_not_wait_for_zombies(self):
        # qa.py's runner is a child subreaper: an orphaned grandchild becomes its
        # unreaped zombie, which still answers killpg(pgid, 0).
        import ctypes

        prctl = ctypes.CDLL(None, use_errno=True).prctl
        self.assertEqual(prctl(36, 1, 0, 0, 0), 0)  # PR_SET_CHILD_SUBREAPER
        try:
            cancel = threading.Event()
            threading.Timer(0.5, cancel.set).start()
            begin = time.monotonic()
            report = self.run_plan(
                self.plan(self.unit("a", self.sh("sleep 30 & wait"), ["docs/a.md"])),
                cancel=cancel,
            )
            took = time.monotonic() - begin
        finally:
            prctl(36, 0, 0, 0, 0)
            while True:  # reap what we adopted
                try:
                    if os.waitpid(-1, os.WNOHANG) == (0, 0):
                        break
                except ChildProcessError:
                    break
        self.assertEqual(report["state"], "cancelled")
        self.assertLess(took, 1.5)

    def test_cancel_during_integration_stops_the_check(self):
        marker = self.root.parent / "integration-marker"
        cancel = threading.Event()
        threading.Timer(0.8, cancel.set).start()
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                check=self.sh(f"sleep 3; touch '{marker}'"),
            ),
            cancel=cancel,
        )
        self.assertEqual(report["state"], "cancelled")
        self.assertEqual(report["integration"]["state"], "CANCELLED")
        time.sleep(3)
        self.assertFalse(marker.exists())
        self.assertNoResidue(report)

    def test_sweep_spares_a_live_dispatcher_and_survives_bad_state(self):
        live = self.runtime / "0123abcd"
        live.mkdir(parents=True)
        (live / "state.json").write_text(
            json.dumps({"run": "0123abcd", "dispatcher": 1, "workers": []})
        )
        import fcntl

        admission = importlib.import_module("environment_admission").Admission(
            self.root, state_dir=self.admission_state
        )
        with (live / "dispatcher.lock").open("w") as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            bad = self.runtime / "badbad00"
            bad.mkdir()
            (bad / "state.json").write_text("{not json")
            self.assertEqual(PARALLEL.sweep(self.runtime, admission=admission), [])
            self.assertTrue(live.exists())
        self.assertEqual(
            PARALLEL.sweep(self.runtime, admission=admission), ["0123abcd"]
        )
        self.assertTrue(bad.exists())


class GitTrustTest(Fixture):
    def sh(self, script: str) -> list[str]:
        return ["sh", "-c", script]

    def test_a_worker_that_changes_its_git_config_is_refused(self):
        for script in (
            "echo A > docs/a.md; git config diff.noprefix true",
            "echo A > docs/a.md; mkdir -p .git/info; echo '* -diff' > .git/info/attributes",
        ):
            with self.subTest(script=script):
                report = self.run_plan(
                    self.plan(self.unit("a", self.sh(script), ["docs/a.md"]))
                )
                unit = report["units"]["a"]
                self.assertEqual(unit["state"], "refused", unit)
                self.assertIn("PARALLEL_GITCONFIG", unit["reason"])

    def test_a_swapped_rename_patch_is_refused_by_its_applied_paths(self):
        # The forged rename moves an unowned file onto unit a's new file.
        forged = (
            "diff --git a/src.txt b/docs/new.md\n"
            "similarity index 100%%\nrename from src.txt\nrename to docs/new.md\n"
        )
        swap = self.sh(f"printf '{forged}' > ../a.patch; echo B > docs/b.md")
        report = self.run_plan(
            self.plan(
                self.unit("a", self.sh("echo n > docs/new.md"), ["docs/new.md"]),
                self.unit("b", swap, ["docs/b.md"], depends_on=["a"]),
            )
        )
        integration = report["integration"]
        self.assertEqual(integration["state"], "REFUSED", integration)
        self.assertIn("src.txt", integration["reason"])
        self.assertIsNone(report["candidate"])

    def test_a_patch_swapped_after_promotion_is_rechecked_at_integration(self):
        # Unit b runs after a is promoted and rewrites a's patch to touch src.txt.
        forged = (
            "diff --git a/src.txt b/src.txt\n"
            "--- a/src.txt\n+++ b/src.txt\n@@ -1 +1 @@\n-source\n+stolen\n"
        )
        swap = self.sh(f"printf '{forged}' > ../a.patch; echo B > docs/b.md")
        report = self.run_plan(
            self.plan(
                self.unit("a", write("docs/a.md", "A\n"), ["docs/a.md"]),
                self.unit("b", swap, ["docs/b.md"], depends_on=["a"]),
            )
        )
        self.assertEqual(report["integration"]["state"], "REFUSED")
        self.assertIn("PARALLEL_OWNERSHIP", report["integration"]["reason"])
        self.assertIsNone(report["candidate"])
        self.assertEqual(report["state"], "failed")


# A stand-in for the provider CLI: it never reaches a provider. It reads its
# prompt from stdin, writes the cleared environment's names to docs/a.md, tries
# a write outside its clone, can leave a `setsid` child, and prints the result
# shape of the real CLI.
FAKE_PROVIDER = """#!/usr/bin/env python3
import json, os, pathlib, subprocess, sys, time
lines = dict(l.split("=", 1) for l in sys.stdin.read().split() if "=" in l)
pathlib.Path("docs/a.md").write_text("\\n".join(sorted(os.environ)) + "\\n")
try:
    pathlib.Path(lines["escape"]).write_text("escaped")
except OSError:
    pass
if "spawn" in lines:
    subprocess.Popen(
        ["setsid", sys.executable, "-c", "import time; time.sleep(300)", lines["spawn"]],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
time.sleep(float(lines.get("sleep", "0")))
if sys.argv[1] == "exec":
    print(json.dumps({"type": "thread.started", "thread_id": "t-1"}))
    print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 7}}))
else:
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False,
        "result": "done", "session_id": "s-1", "total_cost_usd": 0.01,
        "num_turns": 2, "usage": {"input_tokens": 5}}))
"""


def _alive(marker: str) -> bool:
    for cmdline in Path("/proc").glob("[0-9]*/cmdline"):
        try:
            if marker.encode() in cmdline.read_bytes():
                return True
        except OSError:
            continue
    return False


class ProviderPlanTest(Fixture):
    def native(self, **extra):
        unit = {
            "id": "a",
            "action": "write-worker",
            "owned_paths": ["docs/a.md"],
            "provider": "claude",
            "model": "haiku",
            "prompt": "Edit docs/a.md.",
            "budget_usd": 0.5,
            "timeout": 30,
        }
        unit.update(extra)
        return {k: v for k, v in unit.items() if v is not None}

    def test_provider_units_are_validated(self):
        bad = [
            self.native(provider="gemini"),
            self.native(prompt=None),
            self.native(prompt=" "),
            self.native(model="Haiku; rm"),
            self.native(budget_usd=0),
            self.native(budget_usd=float("inf")),
            self.native(budget_usd=None),
            self.native(command=["true"]),
            self.native(provider="codex", budget_usd=0.5),
            self.native(provider="command", command=["true"]),
        ]
        for unit in bad:
            with self.subTest(unit=unit):
                self.assertRefused("PARALLEL_PLAN", PARALLEL.load_plan, self.plan(unit))
        checked = PARALLEL.load_plan(
            self.plan(
                self.native(),
                self.native(
                    id="b", owned_paths=["docs/b.md"], provider="codex", budget_usd=None
                ),
            )
        )
        self.assertEqual(
            sorted(u["provider"] for u in checked["units"]), ["claude", "codex"]
        )
        plain = PARALLEL.load_plan(self.plan(self.unit("c", ["true"], ["src.txt"])))
        self.assertEqual(plain["units"][0]["provider"], "command")

    def test_provider_argv_maps_the_installed_cli_options(self):
        clone = Path("/work/clone")
        self.assertEqual(
            PARALLEL.provider_argv(self.native(), clone, "/bin/claude"),
            [
                "/bin/claude",
                "-p",
                "--output-format",
                "json",
                "--model",
                "haiku",
                "--safe-mode",
                "--strict-mcp-config",
                "--tools",
                "Read,Edit,Write",
                "--permission-mode",
                "acceptEdits",
                "--no-session-persistence",
                "--max-budget-usd",
                "0.5",
            ],
        )
        codex = self.native(provider="codex", model="gpt-6.1-sol", budget_usd=None)
        self.assertEqual(
            PARALLEL.provider_argv(codex, clone, "/bin/codex"),
            [
                "/bin/codex",
                "exec",
                "--json",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "workspace-write",
                "--model",
                "gpt-6.1-sol",
                "--cd",
                "/work/clone",
                "-",
            ],
        )

    def test_provider_results_are_parsed(self):
        claude = json.dumps(
            {
                "type": "result",
                "is_error": False,
                "session_id": "s",
                "total_cost_usd": 0.02,
                "num_turns": 3,
                "usage": {"input_tokens": 1},
            }
        )
        self.assertEqual(
            PARALLEL.parse_result("claude", claude.encode()),
            {
                "session": "s",
                "cost_usd": 0.02,
                "turns": 3,
                "usage": {"input_tokens": 1},
                "error": None,
            },
        )
        events = b"\n".join(
            json.dumps(e).encode()
            for e in [
                {"type": "thread.started", "thread_id": "t"},
                {"type": "turn.completed", "usage": {"output_tokens": 4}},
            ]
        )
        self.assertEqual(
            PARALLEL.parse_result("codex", events),
            {
                "session": "t",
                "cost_usd": None,
                "turns": 1,
                "usage": {"output_tokens": 4},
                "error": None,
            },
        )
        self.assertEqual(
            PARALLEL.parse_result("claude", b"not json")["error"],
            "PARALLEL_RESULT: no result object",
        )
        failed = json.dumps(
            {
                "type": "result",
                "is_error": True,
                "session_id": "s",
                "result": "budget exceeded",
            }
        )
        self.assertIn(
            "budget exceeded", PARALLEL.parse_result("claude", failed.encode())["error"]
        )

    def test_a_provider_unit_needs_a_current_request(self):
        unit = self.native()
        report = self.run_plan(self.plan(unit))
        self.assertEqual(report["units"]["a"]["state"], "refused")
        self.assertIn("PARALLEL_BRIEF", report["units"]["a"]["reason"])

        def stale():
            raise PARALLEL.ParallelError("PARALLEL_BRIEF: BRIEF-STALE: superseded")

        report = self.run_plan(self.plan(unit), request_check=stale)
        self.assertEqual(report["units"]["a"]["state"], "refused")
        self.assertIn("BRIEF-STALE", report["units"]["a"]["reason"])


@unittest.skipUnless(PARALLEL.sandbox_available(), "needs systemd --user and bwrap")
class ContainmentTest(Fixture):
    def setUp(self) -> None:
        super().setUp()
        self.fake = self.root.parent / "bin" / "fake-provider"
        self.fake.parent.mkdir()
        self.fake.write_text(FAKE_PROVIDER)
        self.fake.chmod(0o755)
        self.escape = self.root.parent / "escaped.txt"
        self.marker = f"hyk8s-fake-{os.getpid()}-{time.monotonic_ns()}"
        self.addCleanup(lambda: subprocess.run(["pkill", "-f", self.marker]))

    def native(self, provider="claude", prompt="", timeout=30):
        return {
            "id": "a",
            "action": "write-worker",
            "owned_paths": ["docs/a.md"],
            "provider": provider,
            "model": "haiku",
            "prompt": f"escape={self.escape} spawn={self.marker} {prompt}",
            **({"budget_usd": 0.5} if provider == "claude" else {}),
            "timeout": timeout,
        }

    def run_native(self, unit):
        fixture = {"HYK8S_FAKE_SECRET": "leak"}  # pragma: allowlist secret
        with mock.patch.dict(os.environ, fixture):
            return self.run_plan(
                self.plan(unit),
                request_check=lambda: None,
                binaries={"claude": str(self.fake), "codex": str(self.fake)},
            )

    def test_a_contained_worker_writes_only_its_clone_and_is_reclaimed(self):
        for provider, session in (("claude", "s-1"), ("codex", "t-1")):
            with self.subTest(provider=provider):
                report = self.run_native(self.native(provider))
                record = report["units"]["a"]
                self.assertEqual(report["state"], "completed", report)
                self.assertEqual(record["session"], session)
                self.assertTrue(record["scope"].startswith("hyk8s-par-"))
                self.assertFalse(self.escape.exists(), "a write outside the clone")
                self.assertFalse(_alive(self.marker), "a setsid child outlived it")
                patch = Path(report["candidate"]).read_text()
                self.assertIn("HYK8S_PARALLEL_UNIT", patch)
                self.assertNotIn("HYK8S_FAKE_SECRET", patch)
                self.assertNotIn("DBUS_SESSION_BUS_ADDRESS", patch)
                self.assertNoResidue(report)

    def test_a_timed_out_worker_loses_its_whole_scope(self):
        report = self.run_native(self.native(prompt="sleep=60", timeout=3))
        self.assertEqual(report["units"]["a"]["state"], "expired", report)
        self.assertFalse(_alive(self.marker), "a setsid child outlived the timeout")
        self.assertNoResidue(report)


if __name__ == "__main__":
    unittest.main()
