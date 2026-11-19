#!/usr/bin/env bash
# Bootstrap exactly one new private repository for the authenticated GitHub owner.
# This script deliberately refuses to reuse, overwrite, or make public any remote.
set -euo pipefail

OWNER='darizae'
NAME='repomix-static-reconstructor'
FULL_NAME="${OWNER}/${NAME}"
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$ROOT"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

for cmd in git gh python3; do
  command -v "$cmd" >/dev/null 2>&1 || fail "Missing required command: $cmd"
done

[[ -f docs/BACKLOG.md && -f docs/AGENT_HANDOFF.md && -f src/repomix_static_reconstructor/extractor.py ]] || fail 'Run from the repository root.'
[[ -f repomix-files/.gitkeep ]] || fail 'Missing empty input directory marker.'
for directory in repomix-files scripts tests docs src/repomix_static_reconstructor; do
  [[ -d "$directory" && ! -L "$directory" ]] || fail "Missing or symlinked project directory: $directory"
done

# Never commit user inputs or reconstructed output: even in an otherwise clean checkout.
for path in reconstructed extracted; do
  [[ ! -e "$path" ]] || fail "Remove or move generated '$path/' outside this project before setup."
done
if find repomix-files -type f ! -name .gitkeep -print -quit | grep -q .; then
  fail 'repomix-files/ contains input material. Move it out before setup.'
fi

info 'Running local extractor tests (never executing reconstructed repository code)...'
python3 -m unittest discover -s tests -v

if ! gh auth status >/dev/null 2>&1; then
  info 'GitHub CLI authorization is required; opening interactive GitHub login.'
  gh auth login --hostname github.com --git-protocol https --web
fi
LOGIN="$(gh api user --jq .login)" || fail 'Cannot determine GitHub CLI identity.'
[[ "$LOGIN" == "$OWNER" ]] || fail "GitHub CLI is authenticated as '$LOGIN', not '$OWNER'. Switch accounts; do not create under a different owner."

# A name collision or any API connectivity failure is not permission to push to an existing repo.
if gh repo view "$FULL_NAME" --json nameWithOwner >/dev/null 2>&1; then
  fail "GitHub repository $FULL_NAME already exists. Do not modify or replace it automatically."
fi
info "Remote creation will target a NEW PRIVATE repository: $FULL_NAME"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
  TOP="$(git rev-parse --show-toplevel)"
  [[ "$(cd "$TOP" && pwd -P)" == "$ROOT" ]] || fail 'Project is nested in another Git repository; move it to its own folder.'
  # Start from a fresh repository so the initial push has reviewed provenance.
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    fail 'Existing Git history detected. This bootstrap only supports a fresh repository.'
  fi
  [[ -z "$(git remote)" ]] || fail 'A Git remote already exists. Refusing to relink it.'
else
  git init -b main
fi

[[ "$(git branch --show-current)" == main ]] || fail 'Expected main as initial local branch.'
[[ -z "$(git diff --cached --name-only)" ]] || fail 'Already-staged files exist; review and unstage them before setup.'

# Explicit allowlist. Never use `git add .` or `git add -A` during initial setup.
allowed=(
  .gitignore README.md AGENTS.md SKILL.md SECURITY.md pyproject.toml
  docs/AGENT_HANDOFF.md docs/BACKLOG.md docs/RELEASE_CHECKLIST.md
  scripts/bootstrap_private_github.sh
  src/repomix_static_reconstructor/__init__.py
  src/repomix_static_reconstructor/__main__.py
  src/repomix_static_reconstructor/batch.py
  src/repomix_static_reconstructor/cli.py
  src/repomix_static_reconstructor/extractor.py
  src/repomix_static_reconstructor/py.typed
  tests/test_extractor.py repomix-files/.gitkeep
)
for f in "${allowed[@]}"; do
  [[ -f "$f" && ! -L "$f" ]] || fail "Missing or symlinked expected file: $f"
done

git add -- "${allowed[@]}"
mapfile -t staged < <(git diff --cached --name-only)
mapfile -t expected < <(printf '%s\n' "${allowed[@]}" | LC_ALL=C sort)
[[ ${#staged[@]} -eq ${#expected[@]} ]] || fail 'Staged file list differs from allowlist. Stop and inspect.'
for i in "${!expected[@]}"; do
  [[ "${staged[$i]}" == "${expected[$i]}" ]] || fail "Unexpected staged file: ${staged[$i]}"
done

# Refuse unexpected untracked files; do not silently leave undisclosed additions in the workspace.
mapfile -t extra < <(git ls-files --others --exclude-standard)
[[ ${#extra[@]} -eq 0 ]] || fail "Unexpected untracked files found. Review and remove them before setup."

git diff --cached --check
info 'Approved staged files:'
git diff --cached --stat
info 'Review the contents as directed by docs/AGENT_HANDOFF.md before running this script.'

# Require Git to have a legitimate local author identity. Do not fabricate one.
git var GIT_AUTHOR_IDENT >/dev/null || fail 'Configure your local Git author identity and rerun.'
git commit -m 'chore: initialize static Repomix reconstructor'

# Use GitHub CLI's current session to authenticate HTTPS pushes.
gh auth setup-git
# --private is mandatory; no push to an existing remote. No --public, ever.
gh repo create "$FULL_NAME" --private --source=. --remote=origin --push \
  --description 'Reconstruct Repomix exports as static file trees without executing recovered code'

# Post-create checks: error if anything differs, without changing visibility.
PRIVATE="$(gh repo view "$FULL_NAME" --json isPrivate --jq .isPrivate)" || fail 'Unable to verify repository visibility.'
[[ "$PRIVATE" == true ]] || fail 'Repository is NOT private. Stop and investigate immediately.'
[[ "$(git remote get-url origin)" == *"${FULL_NAME}.git" || "$(git remote get-url origin)" == *"${FULL_NAME}" ]] || fail 'Origin remote does not match the expected owner/repo.'
LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_SHA="$(git ls-remote origin refs/heads/main | cut -f1)"
[[ -n "$REMOTE_SHA" && "$REMOTE_SHA" == "$LOCAL_SHA" ]] || fail 'Remote main SHA does not match local HEAD.'
[[ -z "$(git status --porcelain)" ]] || fail 'Working tree is not clean; review local changes.'
info "Verified: https://github.com/$FULL_NAME (PRIVATE, main pushed, remote synchronized)."
info 'Next: work one backlog ID at a time from docs/BACKLOG.md. Do not publish or change visibility without explicit approval.'
