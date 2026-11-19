"""Regressions for the parallel work dispatcher (W10-PARALLEL, D10 and D11)."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="work-parallel-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "repo"
        self.root.mkdir()
        self.runtime = self.root.parent / "runtime"
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


class DispatchTest(Fixture):
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
        plan_file = self.root.parent / "plan.json"
        pidfile = self.root.parent / "orphan.pid"
        brief, current = self.brief_files(["docs/a.md"])
        plan_file.write_text(
            json.dumps(
                self.plan(
                    self.unit(
                        "a",
                        ["sh", "-c", f"sleep 60 & echo $! > '{pidfile}'; sleep 1"],
                        ["docs/a.md"],
                    )
                )
            )
        )
        dispatcher = subprocess.Popen(
            [
                PY,
                str(ROOT / "scripts" / "work_parallel.py"),
                "run",
                "--root",
                str(self.root),
                "--runtime",
                str(self.runtime),
                "--plan",
                str(plan_file),
                "--brief",
                str(brief),
                "--current-request",
                str(current),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
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
        dispatcher.send_signal(signal.SIGKILL)
        dispatcher.wait(timeout=5)
        # The group leader exits after 1 s; its child keeps running as the orphan.
        self.assertTrue(wait_dead(state["workers"][0]["pid"]))
        orphan = int(pidfile.read_text())
        self.assertFalse(wait_dead(orphan, 0.3))
        cleaned = PARALLEL.sweep(self.runtime)
        self.assertEqual(cleaned, [state["run"]])
        self.assertTrue(wait_dead(orphan))
        self.assertFalse((self.runtime / state["run"]).exists())
        self.assertEqual(PARALLEL.sweep(self.runtime), [])


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

        with (live / "dispatcher.lock").open("w") as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            bad = self.runtime / "badbad00"
            bad.mkdir()
            (bad / "state.json").write_text("{not json")
            self.assertEqual(PARALLEL.sweep(self.runtime), [])
            self.assertTrue(live.exists())
        self.assertEqual(PARALLEL.sweep(self.runtime), ["0123abcd"])
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


if __name__ == "__main__":
    unittest.main()
