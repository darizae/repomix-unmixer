# Contributing

Thanks for your interest. This is currently a **private, pre-release**
project, so contributing works a little differently.

## Ground rules

- **Never execute reconstructed output.** Tests and tooling run against the
  trusted extractor in `src/repomix_unmixer/`, never against
  recovered code. See [`docs/STATIC_INSPECTION.md`](docs/STATIC_INSPECTION.md).
- **Never commit Repomix inputs or reconstructed trees.** `repomix-files/`
  and `reconstructed/` are git-ignored for a reason. Use synthetic fixtures
  (see `tests/fixtures/` and its `generate.sh`) for tests.
- **Offline only.** The extractor must stay standard-library-only, with no
  network calls and no subprocess execution of recovered content.
- `docs/BACKLOG.md` is the source of truth for what is worth building. Claim a
  task by ID (e.g. P1-05) before starting.

## Development setup

```bash
git clone git@github.com:darizae/repomix-unmixer.git
cd repomix-unmixer
pip install -e .            # or: pip install -e ".[dev]"
```

## Running the checks

Run every applicable check **locally** — the project currently operates with
GitHub Actions quota exhausted, so CI is not relied on for validation. Put
`[skip ci]` in commit messages so existing push/PR workflows are skipped, and
never claim a check passed that you did not actually run. A skipped required
CI check stays **Pending**; report it as such, not as a pass.

```bash
python -m unittest discover -s tests -v        # tests
ruff check src tests && ruff format --check src tests   # lint + format
mypy src/repomix_unmixer          # types
python -m build && python -m twine check dist/*         # packaging (when distribution-affecting)
```

Pinned tool versions used in CI: ruff 0.17.5, mypy 1.19.1, build 1.6.1,
twine 6.2.0. If a tool is not installed locally, record the check as
**deferred** rather than passing.

## Pull requests

1. Branch from `main` with a descriptive name, ideally referencing the
   backlog ID: `feature/P1-05-cli-ergonomics`.
2. Keep the change scoped to the claimed task; do not silently broaden scope.
3. Add or update tests for behavior changes. Bug fixes need a regression test.
4. Update `docs/BACKLOG.md` (status/evidence) and, when a release gate is
   genuinely satisfied, `docs/RELEASE_CHECKLIST.md`.
5. PR descriptions state what changed, how it was verified, and any
   limitations. Never mark a task done based only on a proposed plan.
6. Do not force-push. Because `main` requires strict CI checks that remain
   Pending while Actions quota is exhausted, a maintainer may need to merge
   locally-reviewed work after temporarily adjusting branch protection; the
   settings are always restored immediately afterward.

## Security issues

Do not open public issues for security problems. Follow
[`SECURITY.md`](SECURITY.md).

## Licensing

This project is licensed under the [MIT License](LICENSE). By contributing,
you agree your contribution may be distributed under MIT. Contribute only
material you have the rights to submit. Public release still depends on
completing the checks in `docs/RELEASE_CHECKLIST.md`.
