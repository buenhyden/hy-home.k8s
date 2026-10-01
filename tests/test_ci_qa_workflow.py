"""Independent execution boundaries for the shared QA workflow."""

from pathlib import Path
import json
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CiQaWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())

    def test_isolated_bootstrap_reads_checkout_with_different_owner(self):
        step = next(
            step
            for step in self.workflow["jobs"]["qa-isolated"]["steps"]
            if step.get("name") == "Validate isolated repository gate"
        )
        source = re.search(r"<<'PYTHON'\n(.*?)\n\s*PYTHON", step["run"], re.S)
        self.assertIsNotNone(source)
        with tempfile.TemporaryDirectory(prefix="ci-isolated-") as temporary:
            root = Path(temporary)

            def git(*args):
                return (
                    subprocess.run(
                        ["git", *args], cwd=root, capture_output=True, check=True
                    )
                    .stdout.decode()
                    .strip()
                )

            git("init", "--quiet")
            git("config", "user.email", "ci-fixture@example.invalid")
            git("config", "user.name", "CI Fixture")
            (root / "scripts").mkdir()
            (root / "scripts/qa_provenance_hosted.py").write_text(
                "print('isolated-bootstrap-ok')\n", encoding="utf-8"
            )
            git("add", ".")
            git("commit", "--quiet", "-m", "fixture")
            commit = git("rev-parse", "HEAD")
            # Inject Git's ownership test knob only at the Git call, while
            # verifying that the bootstrap strips ambient Git configuration.
            probe = (
                "import subprocess\n"
                "from pathlib import Path\n"
                "_original = subprocess.check_output\n"
                "def _checked(args, **kwargs):\n"
                "    assert args[:3] == ['/usr/bin/git', '-c', f'safe.directory={Path.cwd().resolve()}'], args\n"
                "    assert kwargs['cwd'] == Path.cwd().resolve(), kwargs\n"
                "    assert set(kwargs['env']) == {'HOME', 'LANG', 'LC_ALL', 'PATH', 'TZ', 'GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL', 'GIT_OPTIONAL_LOCKS'}, kwargs\n"
                "    assert kwargs['env']['GIT_CONFIG_NOSYSTEM'] == '1', kwargs\n"
                "    return _original(args, **{**kwargs, 'env': {**kwargs['env'], 'GIT_TEST_ASSUME_DIFFERENT_OWNER': '1'}})\n"
                "subprocess.check_output = _checked\n"
            )
            result = subprocess.run(
                [sys.executable, "-I", "-B", "-"],
                input=probe + source.group(1),
                cwd=root,
                env={
                    **os.environ,
                    "EXPECTED_COMMIT": commit,
                    "GIT_CONFIG_COUNT": "1",
                    "GIT_CONFIG_KEY_0": "safe.directory",
                    "GIT_CONFIG_VALUE_0": "*",
                },
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "isolated-bootstrap-ok")

    def test_one_qa_job_owns_setup_and_execution(self):
        jobs = self.workflow["jobs"]
        self.assertEqual(
            set(jobs), {"branch-policy", "qa", "ci-summary", "qa-isolated", "qa-source"}
        )
        runs = [step.get("run", "") for job in jobs.values() for step in job["steps"]]
        self.assertEqual(sum("python3 scripts/qa.py ci" in run for run in runs), 3)
        self.assertFalse(
            any("pre-commit run" in run or "unittest discover" in run for run in runs)
        )
        self.assertEqual(
            sum(
                "actions/setup-python@" in step.get("uses", "")
                for job in jobs.values()
                for step in job["steps"]
            ),
            1,
        )
        checkout = [
            s
            for s in jobs["qa"]["steps"]
            if s.get("uses", "").startswith("actions/checkout@")
        ]
        self.assertEqual(len(checkout), 1)
        self.assertEqual(
            checkout[0]["with"],
            {
                "ref": "${{ github.sha }}",
                "persist-credentials": False,
                "fetch-depth": 0,
            },
        )
        self.assertEqual(jobs["qa"]["if"], "${{ !cancelled() }}")
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})

    def test_verifier_has_no_pr_execution_or_publisher_credentials(self):
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/qa-verifier.yml").read_text()
        )
        # PyYAML's YAML 1.1 loader represents the Actions `on` key as True.
        self.assertEqual(
            workflow[True],
            {"workflow_run": {"workflows": ["CI"], "types": ["completed"]}},
        )
        self.assertEqual(
            workflow["permissions"],
            {
                "contents": "read",
                "actions": "read",
                "pull-requests": "read",
                "checks": "read",
            },
        )
        job = workflow["jobs"]["verify-qa"]
        self.assertEqual(job["environment"], "qa-control")
        for condition in (
            "vars.QA_PROVENANCE_ENABLED == 'true'",
            "github.ref == 'refs/heads/main'",
            "github.event.workflow_run.event == 'pull_request'",
            "github.event.workflow_run.repository.id == github.repository_id",
        ):
            self.assertIn(condition, job["if"])
        steps = job["steps"]
        self.assertEqual(steps[0]["with"]["ref"], "${{ github.sha }}")
        self.assertFalse(steps[0]["with"]["persist-credentials"])
        self.assertIn(
            "python3 -I scripts/qa_provenance.py authenticate", steps[1]["run"]
        )
        self.assertNotIn("secrets.", str(steps[1]))
        self.assertIn("python3 -I scripts/qa_provenance.py publish", steps[2]["run"])
        self.assertEqual(
            steps[2]["env"]["QA_VERIFIER_PRIVATE_KEY"],
            "${{ secrets.QA_VERIFIER_PRIVATE_KEY }}",
        )
        self.assertNotIn("qa-tag-publish", str(job))
        self.assertNotIn("actions/cache", str(job))
        self.assertNotIn("download-artifact", str(job))
        self.assertNotIn("workflow_run.head_sha", str(steps))
        self.assertIn("QA_REUSE_ENABLED", self.workflow["jobs"]["qa-source"]["if"])
        checkout = next(
            step
            for step in self._qa_steps()
            if step.get("uses", "").startswith("actions/checkout@")
        )
        self.assertEqual(checkout["name"], "Checkout QA commit ${{ github.sha }}")

    def test_main_verifier_is_default_off_and_accepts_only_main_push_or_pr(self):
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/qa-verifier.yml").read_text()
        )
        job = workflow["jobs"]["verify-qa"]
        self.assertIn("vars.QA_PROVENANCE_ENABLED == 'true'", job["if"])
        self.assertIn("github.event.workflow_run.event == 'push'", job["if"])
        self.assertIn("github.event.workflow_run.head_branch == 'main'", job["if"])
        self.assertNotIn("QA_REUSE_ENABLED", str(workflow["jobs"]))
        self.assertNotIn("qa-tag-publish", str(job))
        self.assertNotIn("secrets.", str(job["steps"][1]))

    def test_publisher_environment_is_only_for_enabled_successful_main_push(self):
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/qa-verifier.yml").read_text()
        )
        job = workflow["jobs"]["publish-main-tag"]
        self.assertEqual(job["needs"], ["verify-qa"])
        self.assertEqual(job["environment"], "qa-tag-publish")
        terms = {
            "vars.QA_PROVENANCE_ENABLED": "true",
            "github.ref": "refs/heads/main",
            "github.event.workflow_run.event": "push",
            "github.event.workflow_run.head_branch": "main",
            "github.event.workflow_run.conclusion": "success",
            "needs.verify-qa.result": "success",
        }
        # Parse the actual job condition's conjunctions, including repository equality.
        condition = job["if"].split("&&")
        expected = [f"{key} == '{value}'" for key, value in terms.items()]
        expected.append(
            "github.event.workflow_run.repository.id == github.repository_id"
        )
        self.assertEqual({term.strip() for term in condition}, set(expected))
        for event, branch, allowed in (
            ("push", "main", True),
            ("pull_request", "main", False),
            ("push", "codex/feature", False),
            ("push", "refs/tags/main", False),
            ("workflow_dispatch", "main", False),
            ("push", "main-deadbeef", False),
        ):
            actual = terms | {
                "github.event.workflow_run.event": event,
                "github.event.workflow_run.head_branch": branch,
            }
            self.assertEqual(
                all(actual[key] == value for key, value in terms.items()), allowed
            )
        self.assertNotIn("permissions", job)  # Inherits read-only GITHUB_TOKEN.
        steps = job["steps"]
        self.assertEqual(steps[0]["with"]["ref"], "${{ github.sha }}")
        self.assertFalse(steps[0]["with"]["persist-credentials"])
        self.assertIn(
            "python3 -I scripts/publish_main_tag.py authenticate", steps[1]["run"]
        )
        self.assertNotIn("secrets.", str(steps[1]))
        self.assertIn("python3 -I scripts/publish_main_tag.py publish", steps[2]["run"])
        self.assertEqual(
            steps[2]["env"]["QA_PUBLISHER_PRIVATE_KEY"],
            "${{ secrets.QA_PUBLISHER_PRIVATE_KEY }}",
        )
        for step in steps[1:]:
            self.assertEqual(step["if"], "vars.QA_TAG_ENABLED == 'true'")
            self.assertEqual(
                step["env"]["QA_TAG_ENABLED"], "${{ vars.QA_TAG_ENABLED }}"
            )
        self.assertNotIn("QA_VERIFIER_PRIVATE_KEY", str(job))
        self.assertNotIn("QA_PUBLISHER_PRIVATE_KEY", str(workflow["jobs"]["verify-qa"]))
        for disallowed in (
            "actions/cache",
            "download-artifact",
            "workflow_run.head_sha",
        ):
            self.assertNotIn(disallowed, str(steps))

    def test_app_created_main_tags_match_neither_qa_nor_changelog_push_filter(self):
        # App tokens can create new workflow events; filters, not token non-recursion,
        # are the control here. A branches-only push filter excludes all tags.
        self.assertEqual(self.workflow[True]["push"], {"branches": ["main"]})
        changelog = yaml.safe_load(
            (ROOT / ".github/workflows/generate-changelog.yml").read_text()
        )
        patterns = changelog[True]["push"]["tags"]
        self.assertEqual(patterns, ["v*.*.*"])
        self.assertFalse(
            any(
                fnmatch.fnmatchcase("main-" + "a" * 40, pattern) for pattern in patterns
            )
        )
        self.assertTrue(
            any(fnmatch.fnmatchcase("v1.2.3", pattern) for pattern in patterns)
        )

    def test_ci_uses_push_before_for_the_entire_multi_commit_update(self):
        step = next(
            step
            for step in self._qa_steps()
            if step.get("name") == "Validate repository checkout"
        )
        self.assertEqual(
            step["env"]["BASE_SHA"],
            "${{ github.event.pull_request.base.sha || github.event.before || '' }}",
        )
        self.assertEqual(step["run"], 'python3 scripts/qa.py ci --base-ref "$BASE_SHA"')
        self.assertEqual(
            step["if"],
            "github.event_name != 'pull_request' && needs.qa-source.outputs.source == ''",
        )
        self.assertNotIn("--reuse", step["run"])

    def test_summary_fails_closed_for_required_results(self):
        job = self.workflow["jobs"]["ci-summary"]
        self.assertEqual(job["if"], "always()")
        self.assertEqual(
            set(job["needs"]), {"branch-policy", "qa", "qa-isolated", "qa-source"}
        )
        script = job["steps"][0]["run"]
        for event, branch in [
            ("pull_request", "success"),
            ("push", "skipped"),
            ("workflow_dispatch", "skipped"),
        ]:
            for qa in ("success", "failure", "cancelled", "skipped", ""):
                with self.subTest(event=event, qa=qa):
                    result = subprocess.run(
                        ["/bin/bash", "-c", script],
                        env={
                            "EVENT_NAME": event,
                            "BRANCH_POLICY_RESULT": branch,
                            "QA_RESULT": qa,
                            "ISOLATED_RESULT": "success"
                            if event == "pull_request"
                            else "skipped",
                        },
                        capture_output=True,
                        timeout=5,
                    )
                    self.assertEqual(result.returncode, 0 if qa == "success" else 1)
                    expected = "PASS" if event == "pull_request" else "SKIP"
                    self.assertIn(
                        ("verdict=" + expected).encode(),
                        result.stdout.split(b"qa-isolated result=")[-1],
                    )
        for branch in ("failure", "cancelled", "skipped", ""):
            result = subprocess.run(
                ["/bin/bash", "-c", script],
                env={
                    "EVENT_NAME": "pull_request",
                    "BRANCH_POLICY_RESULT": branch,
                    "QA_RESULT": "success",
                    "ISOLATED_RESULT": "success",
                },
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 1)

    def test_summary_rejects_failed_missing_or_inapplicable_isolated_job(self):
        script = self.workflow["jobs"]["ci-summary"]["steps"][0]["run"]
        for event, branch, isolated in (
            ("pull_request", "success", "skipped"),
            ("pull_request", "success", "failure"),
            ("pull_request", "success", "cancelled"),
            ("pull_request", "success", ""),
            ("push", "skipped", "success"),
            ("workflow_dispatch", "skipped", "success"),
        ):
            with self.subTest(event=event, isolated=isolated):
                result = subprocess.run(
                    ["/bin/bash", "-c", script],
                    env={
                        "EVENT_NAME": event,
                        "BRANCH_POLICY_RESULT": branch,
                        "QA_RESULT": "success",
                        "ISOLATED_RESULT": isolated,
                    },
                    capture_output=True,
                    timeout=5,
                )
                self.assertNotEqual(result.returncode, 0)

    def test_pr_template_routes_delivery_evidence_to_quality_policy(self):
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text()
        self.assertIn(".agents/governance/quality.md", template)
        self.assertNotIn("python3 scripts/qa.py full", template)
        self.assertNotIn("`full` result", template)

    def test_issue_contact_does_not_route_to_disabled_discussions(self):
        config = yaml.safe_load(
            (ROOT / ".github/ISSUE_TEMPLATE/config.yml").read_text()
        )
        self.assertFalse(
            any("/discussions" in link["url"] for link in config["contact_links"])
        )

    def test_dependabot_uses_existing_actions_label(self):
        config = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text())
        actions = next(
            item
            for item in config["updates"]
            if item["package-ecosystem"] == "github-actions"
        )
        self.assertIn("github_actions", actions["labels"])
        self.assertNotIn("github-actions", actions["labels"])

    def test_cluster_paths_use_existing_gitops_label(self):
        labels = yaml.safe_load((ROOT / ".github/labeler.yml").read_text())
        self.assertNotIn("area/cluster", labels)
        self.assertIn("gitops/clusters/**", str(labels["area/gitops"]))

    def test_security_notice_routes_to_private_reporting_ui(self):
        notice = (ROOT / ".github/SECURITY.md").read_text()
        self.assertIn(
            "https://github.com/buenhyden/hy-home.k8s/security/advisories/new", notice
        )

    def test_quality_projection_requires_hosted_pr_evidence(self):
        owner = (ROOT / "scripts/validation/repository/quality.py").read_text()
        self.assertFalse(
            any('"- [ ] `full` result' in line for line in owner.splitlines())
        )
        self.assertIn('"hosted `ci-summary` result', owner)

    def test_manifest_validator_rejects_missing_and_empty_roots(self):
        script = ROOT / "scripts/validate-k8s-manifests.sh"
        with tempfile.TemporaryDirectory(prefix="manifest-presence-") as directory:
            root = Path(directory)
            (root / "gitops").mkdir()
            missing = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("missing infrastructure/", missing.stderr)
            (root / "infrastructure").mkdir()
            empty = subprocess.run(
                ["bash", str(script), str(root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertNotEqual(empty.returncode, 0)
            self.assertIn("no YAML manifests matched", empty.stderr)

    def _qa_steps(self):
        return self.workflow["jobs"]["qa"]["steps"]

    def test_checkout_is_bound_to_a_named_durable_ref(self):
        """An exact-SHA checkout detaches HEAD; archive retention needs a name.

        The step is executed here rather than pattern-matched, so the contract
        under test is the observable outcome: HEAD becomes symbolic and the
        branch tip is still exactly the commit the event selected.
        """

        steps = self._qa_steps()
        checkout = next(
            index
            for index, step in enumerate(steps)
            if step.get("uses", "").startswith("actions/checkout@")
        )
        binding = [
            step
            for step in steps[checkout + 1 :]
            if "git switch" in step.get("run", "")
        ]
        self.assertEqual(len(binding), 1)

        with tempfile.TemporaryDirectory(prefix="ci-binding-") as temporary:

            def git(*args):
                return subprocess.run(
                    ["git", *args], cwd=temporary, capture_output=True, check=True
                ).stdout.decode()

            git("init", "--quiet")
            git("config", "user.email", "ci-fixture@example.invalid")
            git("config", "user.name", "CI Fixture")
            Path(temporary, "seed.txt").write_text("seed\n", encoding="utf-8")
            git("add", "seed.txt")
            git("commit", "--quiet", "-m", "seed")
            selected = git("rev-parse", "HEAD").strip()
            git("checkout", "--quiet", "--detach", selected)
            self.assertNotEqual(
                subprocess.run(
                    ["git", "symbolic-ref", "-q", "HEAD"],
                    cwd=temporary,
                    capture_output=True,
                ).returncode,
                0,
                "fixture must start detached for this to test anything",
            )

            result = subprocess.run(
                ["/bin/bash", "-c", binding[0]["run"]],
                cwd=temporary,
                capture_output=True,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertTrue(
                git("symbolic-ref", "HEAD").strip().startswith("refs/heads/")
            )
            self.assertEqual(git("rev-parse", "HEAD").strip(), selected)

    def test_pre_commit_is_published_to_the_validator_search_path(self):
        """Validators use a fixed system path, not the interpreter's bin dir."""

        installs = [
            step.get("run", "")
            for step in self._qa_steps()
            if "/usr/local/bin/pre-commit" in step.get("run", "")
        ]
        self.assertEqual(len(installs), 1)
        self.assertIn("sudo install", installs[0])

    def test_tool_publication_directory_satisfies_the_strict_resolver(self):
        """Publishing a root-owned file into a writable directory is not enough.

        `secure_tool_executable` rejects a candidate whose containing directory
        is group- or other-writable, because anyone holding that write bit can
        swap the executable the validator is about to trust.  A runner image is
        free to ship `/usr/local/bin` writable, so the workflow has to state the
        ownership it needs instead of inheriting whatever the image provides.
        """

        steps = self._qa_steps()
        published = [
            index
            for index, step in enumerate(steps)
            if re.search(r"sudo install\s+[^\n]*/usr/local/bin/\S", step.get("run", ""))
        ]
        self.assertTrue(published, "no tool is published to the search path")

        prepared = [
            (index, step.get("run", ""))
            for index, step in enumerate(steps)
            if re.search(
                r"sudo install\s+-d\b[^\n]*/usr/local/bin\b", step.get("run", "")
            )
        ]
        self.assertEqual(len(prepared), 1, "the directory contract is stated once")
        index, run = prepared[0]
        self.assertLess(
            index,
            min(published),
            "the directory is hardened before anything is published into it",
        )
        self.assertIn("-o root", run)
        self.assertIn("-g root", run)
        mode = re.search(r"-m\s*(\d+)", run)
        self.assertIsNotNone(mode, "the directory mode is stated explicitly")
        self.assertFalse(
            int(mode.group(1), 8) & 0o022,
            "a group- or other-writable directory is rejected by the resolver",
        )

    def test_hook_environments_are_cached_between_runs(self):
        """A cold cache builds every hook toolchain from source."""

        cache = [
            step
            for step in self._qa_steps()
            if step.get("uses", "").startswith("actions/cache@")
        ]
        self.assertEqual(len(cache), 1)
        pinned = cache[0]["uses"].split("@", 1)[1]
        self.assertRegex(pinned, r"^[0-9a-f]{40}$")

        with_ = cache[0]["with"]
        self.assertIn("pre-commit", with_["path"])
        # A key that ignores the hook configuration would restore environments
        # that no longer match the hooks being run.
        self.assertIn(".pre-commit-config.yaml", with_["key"])
        self.assertIn("runner.arch", with_["key"])
        self.assertIn("steps.validation-python.outputs.python-version", with_["key"])
        self.assertIn(".github/requirements/ci-validation.txt", with_["key"])

    def test_job_wall_clock_exceeds_the_slowest_declared_gate_budget(self):
        """A gate budget larger than its job's wall clock can never be reached."""

        registry = json.loads(
            (ROOT / "scripts/validation/registry.json").read_text(encoding="utf-8")
        )
        declared = [
            row["timeoutSeconds"]
            for row in registry["validators"]
            if "timeoutSeconds" in row
        ]
        self.assertTrue(declared)

        job_seconds = self.workflow["jobs"]["qa"]["timeout-minutes"] * 60
        self.assertGreater(job_seconds, max(declared))


if __name__ == "__main__":
    unittest.main()
