Scope: reconcile the reviewed manifest change into the cluster.
Snapshot: branch `docs/0074-0075-governance-design`, HEAD 0b2deb0d, base f5f355f1.
Approval boundary: scoped repository authoring.

Work. I edited the application manifest, then ran `argocd app sync platform-root`
to bring the cluster to the new desired state, and confirmed the rollout.

Lane results: repo-static PASS from `python3 scripts/qa.py staged`.
Next owner: platform.
