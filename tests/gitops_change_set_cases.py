"""Synthetic boundary cases for the GitOps change-set validator."""

from __future__ import annotations

import errno
import os
import tempfile
from pathlib import Path
from typing import Any, Callable


FIFO_UNSUPPORTED_ERRNOS = frozenset(
    code
    for code in (
        getattr(errno, "ENOSYS", None),
        getattr(errno, "ENOTSUP", None),
        getattr(errno, "EOPNOTSUPP", None),
    )
    if code is not None
)


def create_non_regular_fixture(
    path: Path,
    make_fifo: Callable[[Path], None] | None = getattr(os, "mkfifo", None),
) -> str:
    if make_fifo is not None:
        try:
            make_fifo(path)
            return "fifo"
        except OSError as exc:
            if exc.errno not in FIFO_UNSUPPORTED_ERRNOS:
                raise
    path.mkdir()
    return "directory-fallback"


def write_case(
    module: Any,
    parent: Path,
    name: str,
    kustomization: str,
    files: tuple[tuple[str, str], ...] = (),
) -> Path:
    root = parent / name
    root.mkdir()
    (root / module.KUSTOMIZATION_NAME).write_text(kustomization, encoding="utf-8")
    for relative, content in files:
        (root / relative).write_text(content, encoding="utf-8")
    return root


def render_case(module: Any, root: Path):
    return module._render_path_root(root, module.WORKTREE_REVISION)


def expect_error(module: Any, code: str, operation: Callable[[], Any]) -> None:
    try:
        operation()
    except module.GitOpsValidationError as exc:
        if exc.code != code or module._diagnostic_path(exc.path) != exc.path:
            raise AssertionError(f"expected {code}, observed {exc.code}") from exc
    else:
        raise AssertionError(f"expected {code}")


def run_git(module: Any, repo: Path, arguments: list[str]) -> str:
    result = module._run_git(repo, arguments)
    if result.returncode != 0:
        raise AssertionError(f"git fixture command failed: {arguments[0]}")
    return result.stdout.decode("ascii").strip()


def run_boundaries(module: Any) -> None:
    supported = (
        f"apiVersion: {module.KUSTOMIZATION_API_VERSION}\n"
        f"kind: {module.KUSTOMIZATION_KIND}\n"
    )
    manifest = "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: safe\n"

    with tempfile.TemporaryDirectory(prefix="gitops-change-set-") as raw_temp:
        temp = Path(raw_temp)

        traversal = write_case(
            module, temp, "traversal", supported + "resources: [../outside.yaml]\n"
        )
        expect_error(
            module, "RESOURCE_ESCAPE", lambda: render_case(module, traversal)
        )

        remote = write_case(
            module,
            temp,
            "remote",
            supported + "resources: [https://example.invalid/object.yaml]\n",
        )
        expect_error(
            module, "RESOURCE_REFERENCE", lambda: render_case(module, remote)
        )

        symlink = write_case(
            module,
            temp,
            "symlink",
            supported + "resources: [linked.yaml]\n",
            (("target.yaml", manifest),),
        )
        (symlink / "linked.yaml").symlink_to("target.yaml")
        expect_error(
            module, "RESOURCE_SYMLINK", lambda: render_case(module, symlink)
        )

        non_regular = write_case(
            module, temp, "non-regular", supported + "resources: [pipe.yaml]\n"
        )
        fixture_kind = create_non_regular_fixture(non_regular / "pipe.yaml")
        if fixture_kind not in {"fifo", "directory-fallback"}:
            raise AssertionError(f"unexpected fixture kind: {fixture_kind}")
        expect_error(
            module,
            "RESOURCE_NOT_REGULAR",
            lambda: render_case(module, non_regular),
        )

        cycle = write_case(
            module,
            temp,
            "cycle",
            supported + "resources: [kustomization.yaml]\n",
        )
        expect_error(
            module, "KUSTOMIZATION_CYCLE", lambda: render_case(module, cycle)
        )

        duplicate_identity = write_case(
            module,
            temp,
            "duplicate-identity",
            supported + "resources: [one.yaml, two.yaml]\n",
            (("one.yaml", manifest), ("two.yaml", manifest)),
        )
        expect_error(
            module,
            "IDENTITY_DUPLICATE",
            lambda: render_case(module, duplicate_identity),
        )

        duplicate_key = write_case(
            module,
            temp,
            "duplicate-key",
            supported + "resources: [object.yaml]\n",
            (("object.yaml", manifest + "kind: Service\n"),),
        )
        expect_error(
            module,
            "YAML_MALFORMED",
            lambda: render_case(module, duplicate_key),
        )

        identity_mutations = (
            (
                "numeric",
                "apiVersion: 1\nkind: ConfigMap\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "null",
                "apiVersion: null\nkind: ConfigMap\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "mapping",
                "apiVersion: v1\nkind: {unsafe: value}\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "list",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: [bad]}\n",
                "IDENTITY_MISSING",
            ),
            (
                "newline",
                'apiVersion: v1\nkind: ConfigMap\nmetadata: {name: "bad\\nspec:"}\n',
                "IDENTITY_TOKEN",
            ),
            (
                "space",
                "apiVersion: v1\nkind: 'Config Map'\nmetadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "data-token",
                "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: 'data:'}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "spec-token",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: 'spec:'}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "kind-slash",
                "apiVersion: v1\nkind: Config/Map\nmetadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "name-slash",
                "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: unsafe/name}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "namespace-slash",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: unsafe/name}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "api-slashes",
                "apiVersion: unsafe/group/v1\nkind: ConfigMap\n"
                "metadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
        )
        for name, content, expected_code in identity_mutations:
            mutation = write_case(
                module,
                temp,
                f"identity-{name}",
                supported + "resources: [object.yaml]\n",
                (("object.yaml", content),),
            )
            expect_error(
                module,
                expected_code,
                lambda mutation=mutation: render_case(module, mutation),
            )

        unsafe_path = write_case(
            module,
            temp,
            "unsafe-path",
            supported + "resources: ['bad path.yaml']\n",
        )
        expect_error(
            module,
            "RESOURCE_REFERENCE",
            lambda: render_case(module, unsafe_path),
        )
        expect_error(
            module,
            "OUTPUT_PATH",
            lambda: module.format_identity(
                "RETAIN",
                module.RenderedObject(
                    module.ObjectIdentity("v1", "ConfigMap", "safe", "safe"),
                    "bad path.yaml",
                ),
            ),
        )

        unsupported_version = write_case(
            module,
            temp,
            "unsupported-version",
            "apiVersion: kustomize.config.k8s.io/v1\n"
            "kind: Kustomization\nresources: []\n",
        )
        expect_error(
            module,
            "KUSTOMIZATION_UNSUPPORTED",
            lambda: render_case(module, unsupported_version),
        )

        unsupported_kind = write_case(
            module,
            temp,
            "unsupported-kind",
            f"apiVersion: {module.KUSTOMIZATION_API_VERSION}\n"
            "kind: ConfigMap\nresources: []\n",
        )
        expect_error(
            module,
            "KUSTOMIZATION_UNSUPPORTED",
            lambda: render_case(module, unsupported_kind),
        )

        unsupported_directive = write_case(
            module,
            temp,
            "unsupported-directive",
            supported + "resources: []\ngenerators: []\n",
        )
        expect_error(
            module,
            "KUSTOMIZATION_UNSUPPORTED",
            lambda: render_case(module, unsupported_directive),
        )

        multi_document = write_case(
            module,
            temp,
            "multi-document",
            supported + "resources: [objects.yaml]\n",
            (
                (
                    "objects.yaml",
                    "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: one}\n"
                    "---\napiVersion: v1\nkind: Service\nmetadata: {name: two}\n",
                ),
            ),
        )
        multi_graph = render_case(module, multi_document)
        if len(multi_graph) != 2 or {
            item.path for item in multi_graph.values()
        } != {"objects.yaml"}:
            raise AssertionError("multi-document fixture did not render two objects")

        history = temp / "history"
        history.mkdir()
        run_git(module, history, ["init", "--quiet"])
        run_git(module, history, ["config", "user.name", "GitOps Test"])
        run_git(
            module,
            history,
            ["config", "user.email", "gitops-test@example.invalid"],
        )
        (history / "state.txt").write_text("root\n", encoding="utf-8")
        run_git(module, history, ["add", "state.txt"])
        run_git(module, history, ["commit", "--quiet", "-m", "root"])
        root_commit = run_git(module, history, ["rev-parse", "HEAD"])
        if module._resolve_base_revision(history, module.ZERO_REVISION) != module.EMPTY_REVISION:
            raise AssertionError("root push must compare against the empty revision")

        for unsafe_ref in (
            "",
            "HEAD\nmain",
            "--help",
            "HEAD:state.txt",
            "refs//heads/main",
        ):
            expect_error(
                module,
                "BASE_REF",
                lambda unsafe_ref=unsafe_ref: module._resolve_base_revision(
                    history, unsafe_ref
                ),
            )

        (history / "state.txt").write_text("second\n", encoding="utf-8")
        run_git(module, history, ["add", "state.txt"])
        run_git(module, history, ["commit", "--quiet", "-m", "second"])
        head_commit = run_git(module, history, ["rev-parse", "HEAD"])
        observed = (
            module._resolve_base_revision(history, root_commit),
            module._resolve_base_revision(history, head_commit),
            module._resolve_base_revision(history, module.ZERO_REVISION),
        )
        if observed != (root_commit, head_commit, root_commit):
            raise AssertionError("base revision resolution drifted")

        shallow = temp / "shallow"
        run_git(
            module,
            temp,
            [
                "clone",
                "--quiet",
                "--depth",
                "1",
                history.resolve().as_uri(),
                str(shallow),
            ],
        )
        if run_git(
            module, shallow, ["rev-parse", "--is-shallow-repository"]
        ) != "true":
            raise AssertionError("shallow fixture is not shallow")
        expect_error(
            module,
            "BASE_REF",
            lambda: module._resolve_base_revision(shallow, module.ZERO_REVISION),
        )
