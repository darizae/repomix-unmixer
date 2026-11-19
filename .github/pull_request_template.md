## Summary

<!-- What does this change do, and why? Keep it scoped to one backlog task. -->

- Backlog ID: <!-- e.g. P0-09, P1-10 -->
- Branch: <!-- feature/<ID>-short-name -->

## Changes

<!-- Bullet list of concrete changes (files, behavior, docs). -->

## Tests actually run

<!--
List the exact local commands you ran and their results (PASS/SKIP/DEFERRED).
GitHub Actions quota is exhausted, so CI checks may remain pending; do not
claim a check passed that you did not run. Include at least:
  python -m unittest discover -s tests -v
  ruff check src tests && ruff format --check src tests
  mypy src/repomix_unmixer
-->

- [ ] `python -m unittest discover -s tests -v`
- [ ] `ruff check src tests && ruff format --check src tests`
- [ ] `mypy src/repomix_unmixer`
- [ ] Packaging / install check (if distribution-affecting): `python -m build && python -m twine check dist/*`
- Result / skips / deferred:

## Security & no-recovered-execution

- [ ] No reconstructed code was executed, imported, built, installed, or run.
- [ ] No input/output snapshots, credentials, or confidential data are tracked or referenced.
- [ ] This change does not weaken the static-only, no-execution, or fresh-output safeguards (see `docs/SECURITY_REVIEW.md`).

## Deferred / limitations

<!-- Anything not verified, deferred to CI, or out of scope for this PR. -->

## Verification notes

<!-- Any evidence that helps reviewers: fixture outputs, error paths, platform caveats. -->