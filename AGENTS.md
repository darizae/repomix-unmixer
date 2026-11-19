# Agent operating instructions — Repomix Static Reconstructor

## First: understand the repository

Read `README.md`, `SECURITY.md`, `docs/BACKLOG.md` and `docs/RELEASE_CHECKLIST.md` before working. `docs/BACKLOG.md` is the **single source of truth** for product decisions, task IDs, statuses and acceptance criteria. The repository belongs to the GitHub account **`darizae`** and its intended private remote is **`darizae/repomix-static-reconstructor`**.

### If GitHub has not yet been initialized

1. Read `docs/AGENT_HANDOFF.md` and review the files you intend to commit. Ensure no Repomix exports, reconstructed output trees, credentials, or unintended files are included in the first commit.
2. Check that GitHub CLI is authenticated to `darizae` (the setup script verifies this and can launch interactive authentication).
3. Run **`bash scripts/bootstrap_private_github.sh`** from the project root. It tests, creates a new **private** remote, initializes Git, pushes `main` and verifies the remote and visibility. It refuses existing Git history, unexpected GitHub owners and an already-existing repository. Never manually work around those guardrails or create a public repository.
4. If setup fails, report the exact blocker; do not guess another owner/name, force-push, alter visibility or upload input archives.

### When instructed to tackle a backlog task

1. Identify the requested task by its exact ID in `docs/BACKLOG.md` (or select the next highest-priority unblocked task only if given general permission to proceed). Read the definition of done and any linked release checklist items.
2. Confirm scope and inspect current implementation before changing code. Preserve supported parsed paths and contents without automatic rewriting. Add tests with bug fixes. Do not silently broaden scope to unrelated tasks.
3. Work on an appropriately named feature branch when a private GitHub remote exists; otherwise work locally and report that synchronization is unavailable. Never force-push or change repository visibility.
4. Run `python3 -m unittest discover -s tests -v` and other task-specific checks; verify no generated exports or source snapshots are tracked.
5. Update task status, notes and evidence in `docs/BACKLOG.md`; update `docs/RELEASE_CHECKLIST.md` if a release gate is actually satisfied. Commit the code and docs together, push the branch if authenticated and authorized, and open a PR if the environment permits. Otherwise provide the exact commit/branch and commands to continue.
6. In the handoff, give the task ID, what changed, what was tested, current status, blockers and follow-up. Never mark a task done based only on a proposed plan.

## Execution and privacy boundaries

This repository contains a trusted **extractor** and may handle untrusted **Repomix inputs/outputs**. You may run its tests and the scripts in `scripts/`. Do **not** run, import, build, test, install, lint or otherwise execute any files produced from Repomix exports. Do not contact endpoints referenced in extracted code or run its Git hooks, containers, package managers, MCP configurations or scripts.

Preserve recovered filenames and parsed text. The tool uses deliberate high-risk file exclusions, path/resource constraints, offline operation and static-only handling. Output can still contain secrets. Do not publicly upload recovered inputs or outputs. Never recursively delete arbitrary user paths or overwrite existing output folders.

Only make the repository public after explicit maintainer approval **and** all applicable items in `docs/RELEASE_CHECKLIST.md` are satisfied. The project is private-first and does not yet have licensing/publication approval.
