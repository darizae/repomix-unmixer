# Agent instructions — repomix-unmixer

Read `README.md`, `SECURITY.md`, `docs/BACKLOG.md`, `docs/RELEASE_CHECKLIST.md`, and `docs/STATIC_INSPECTION.md` before modifying this repository. The backlog is the source of truth for task IDs and acceptance criteria.

## Working on a task

1. Work in the trusted clone of `darizae/repomix-unmixer`. Verify `origin`, check `main` is current, and read the requested backlog task. Do not reinitialize GitHub or create a new remote.
2. Create a scope-specific branch. Update code/docs and add regression tests for behavioral changes; do not implement unrelated tasks.
3. Run the trusted extractor tests (`python3 -m unittest discover -s tests -v`) and applicable lint, type, build, docs and CI checks. Run only what is available; describe unavailable checks as **deferred**, not passed.
4. Inspect `git status` and staged changes for unexpected files. Update `docs/BACKLOG.md` with evidence and `docs/RELEASE_CHECKLIST.md` only for satisfied gates.
5. Commit, push the task branch, and open a PR to `main` when authorized. Report the PR link, checks run, remaining risk and any deferred check. Never force-push or change repository visibility without explicit instruction.

## Static-only boundary

**Never execute or install code from reconstructed repositories.** Do not run recovered application entry points, package managers, test/build tools, Git hooks, containers, MCP servers or editor tasks. Do not contact endpoints in recovered files. Treat both inputs and outputs as potentially confidential and untrusted.

The extractor itself is a trusted, stdlib-only local tool. Only retained files are reconstructed; documented exclusions are not a secrecy guarantee. Use output locations not writable by untrusted users and never overwrite an existing target.

Keep `repomix-files/`, `reconstructed/`, `extracted/`, credentials and unrelated data out of Git. Preserve the private remote until the maintainer approves a public release after all applicable gates, including rights/licensing and privacy review.
