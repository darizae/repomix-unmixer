# Agent handoff — initialize the maintainer's private GitHub repository

**Target account confirmed using the connected GitHub account:** `darizae`.

**Exact repository to create:** `https://github.com/darizae/repomix-static-reconstructor`.

**Visibility:** PRIVATE. This repository was not created by the bundle preparer; the local agent should create it using the maintainer's own authenticated GitHub CLI credentials.

## Do this once from the extracted project root

1. Read root `AGENTS.md`, `README.md`, `SECURITY.md`, `docs/BACKLOG.md`, `docs/RELEASE_CHECKLIST.md` and `.gitignore`.
2. Audit the project files for secrets and personal/private project material. Confirm `repomix-files/` contains only `.gitkeep` and no generated output tree exists. Do not include Repomix exports or reconstructed files in Git history.
3. Ensure `git`, `gh` (GitHub CLI) and `python3` are available; Git has your real author identity configured. If `gh` needs authentication, use its interactive browser login for the `darizae` account. The script checks the authenticated username.
4. Run the single no-placeholder setup command:

```bash
bash scripts/bootstrap_private_github.sh
```

The script runs the local extractor tests; stages **only** an explicit list of approved files; initializes `main`; creates **`darizae/repomix-static-reconstructor`** with `gh repo create --private --source=. --remote=origin --push`; and verifies the remote, `main` SHA and private visibility. It refuses an existing remote, existing Git history, a different GitHub account, an already-existing repository name, or generated input/output material. It will not use `--public` or force-push.

If script validation fails, **stop** and report the specific reason. Do not improvise a new owner or repository slug. If GitHub CLI browser authorization is required, ask the maintainer to complete that interactive authorization. A local Git author identity must be configured through normal Git settings; do not invent it.

## Then prepare for backlog work

`docs/BACKLOG.md` is authoritative. `docs/RELEASE_CHECKLIST.md` lists the release gates. Read `AGENTS.md` at the start of each future task. Do not automatically implement the entire backlog in the setup step.

For a later instruction such as **“Tackle P0-09”**, locate that ID in `docs/BACKLOG.md`, satisfy its definition of done, add or run tests, update the task's status and notes in the backlog, commit code and docs, and report evidence and blockers. Push a feature branch and open a private PR where authorized; otherwise explain why.

Start with P0 security, parser correctness and packaging work before public branding or distribution. Branding/logo/README/website tasks are already tracked under P1. Preserve parsed names and file contents; follow the documented exclusion policy in `docs/EXCLUSIONS.md`. No public release, license selection on behalf of the maintainer, or visibility change without explicit approval.

## Final setup verification

The agent should report these commands' actual results (not presumed success):

```bash
gh repo view darizae/repomix-static-reconstructor --json nameWithOwner,isPrivate,url
git remote -v
git status -sb
git log -1 --oneline
git ls-remote origin refs/heads/main
```

Expected: the account and repository above; `isPrivate: true`; `origin` pointing to `darizae/repomix-static-reconstructor`; committed `main` synchronized with remote and a clean working tree. If any check fails, stop and report instead of claiming setup succeeded.
