# Release execution plan — repomix-unmixer v0.1.0

**Status:** approved implementation plan; NOT evidence of completed work.  
**Owner:** maintainer / trusted local coding agent.  
**Reference:** [BACKLOG.md](BACKLOG.md), [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md), [SECURITY.md](../SECURITY.md), [CONTRIBUTING.md](../CONTRIBUTING.md).  
**Target:** existing MIT-licensed `darizae/repomix-unmixer` repo; keep it private until the final release gate.

## Fixed scope and decisions

- The maintainer has **accepted the current product name, package/CLI names and logo**. P1-01/P1-02 are complete. Do not repeat branding, availability, or visual/trademark exercises; report any *actual* legal conflict discovered during provenance review rather than claiming legal clearance.
- The historic email-metadata residual exposure is **accepted**; no more history rewriting, support requests, or re-audits solely to remove old PR cache objects. Keep future commits on GitHub noreply.
- GitHub Actions usage is exhausted. **Do not dispatch, rerun, enable or otherwise deliberately trigger any GitHub Actions workflows.** Use local validations; report cloud-only checks as deferred. Commit with `[skip ci]` so existing push/PR workflows are skipped. GitHub required status checks may remain Pending as a consequence: never claim a skipped check passed.
- **Website deployment, social preview upload, demo GIF, extra marketing and live-hosted docs remain deferred.** README and existing branding are accepted. No new feature formats/CLI features just for this release.
- Do not execute, import, build, install, test or run **reconstructed source**; only execute the trusted extractor and its own tests against synthetic, untrusted-as-data fixtures.
- Preserve the existing protected `main`, no force pushes, no public visibility, and no PyPI upload before the final gate. No secrets in GitHub, commits, PR text, logs or output.
- Use the existing task IDs below. This document does **not** authorize inventing accomplishments or declaring tests passed without actually running them.

## Definition of a qualified v0.1.0 release

Qualification means independent evidence that a new user can install the **built distribution**, use both CLI entrypoints on synthetic exports, and receive correctly reconstructed text *without ever running recovered code*, while the extractor respects security boundaries. It also means distributable metadata, a clear MIT/provenance position, supported documentation, release notes and community entry points. It is **not** a claim of formal security certification or fidelity beyond the documented Repomix versions.

A release candidate is ready only if all **blocking** items below are satisfied or explicitly classified as known, accepted limitations in the release notes; unverified high-impact filesystem or ownership issues cannot be waived by hiding them.

## Execution phases — implement in this order

### A. Security and qualification (P0-05, P0-09, P0-17, P1-12)

Review actual current source first; do not trust prior backlog claims as proof. Prefer a compact written threat model and regression tests to a large refactor.

1. Audit temporary staging and final commit: local output directory ownership, ancestor symlinks, race between validation/create/open/rename, hardlinks, symlink swaps, cross-device rename and `os.replace`/rename semantics, temporary cleanup on exceptions, Windows reparse points, path aliasing, case collisions, and unsafe traversal. Test attacks inside temporary test directories only. Preserve fresh-only output and refuse overwrite.
2. Check input/read limits and file-count/per-file/total-byte thresholds on boundary values. Verify no final/staging output, unintended directories, or writes during `--dry-run`; inject permission errors, partial writes and simulated races where feasible. Never claim atomicity or race resistance beyond evidence; document unsupported hostile shared-directory cases plainly.
3. Verify no recovered-code execution: no shell/subprocess invocation, network traffic, package install, import or hooks caused by parsing/reconstruction. Keep reconstructed text untrusted; test only the trusted reconstructor. Add static assertions/regressions where useful.
4. Run the trusted unit suite, `ruff check src tests`, `ruff format --check src tests`, `mypy src/repomix_unmixer`, official Agent Skills validation if available, and packaging checks. Distinguish PASS, FAIL, SKIP and DEFERRED. For platform cases unavailable locally, report deferred rather than claiming Linux/Windows passed now.
5. Document a concise non-sensitive `docs/SECURITY_REVIEW.md`: threat assumptions, tested cases, remediation, residual risks, actual commands, platforms and results. Update `SECURITY.md` only when supported by tests; do not claim independent external audit merely because an agent reviewed it.

**Exit gate:** no known exploitable traversal/overwrite/escape in supported trusted-local-directory use; dry-run truly writes nothing; local regression suite passes; residual concurrency cases are explicitly bounded.

### B. Community and maintainer files (P1-10)

Create/refresh only these useful files, without boilerplate duplication:

- `CHANGELOG.md` with a concise v0.1.0 entry and [Keep a Changelog](https://keepachangelog.com/) structure; include only delivered behavior and meaningful limitations.
- `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, and `config.yml`. Fields: version/platform/Python, reproducible synthetic example, expected/actual behavior, safety and privacy reminder. Disable blank issues only if suitable; link security reports to `SECURITY.md`.
- `.github/pull_request_template.md` with backlog ID, summary, tests actually run, security/no-recovered-execution checkbox, and deferred checks.
- `CODE_OF_CONDUCT.md` using a recognized community policy (prefer Contributor Covenant 2.1, with attribution/license intact) and an **actual** private enforcement contact. Do not invent an email or publish the maintainer's private address. If no private contact is available, keep contact activation as an explicit release blocker; do not fabricate reporting instructions.
- Refine `CONTRIBUTING.md` only to match the current local-validation/no-Actions practice, existing MIT terms, accepted PR workflow and privacy rules. No gratuitous new badges or pages.

**Exit gate:** all links/paths exist, GitHub templates parse, no fake release claims, and no private contact/address is exposed.

### C. Installability and Agent Skills (P0-15, P1-08, P0-17, P2-01)

- From a fresh trusted checkout, build wheel and sdist (`python -m build`); run `python -m twine check dist/*`, inspect wheel/sdist membership and project metadata, and install **both** archives separately into clean virtual environments; verify `unmix-repomix --version`, `unmix-repomix --help`, `reconstruct-all --help`, `python -m repomix_unmixer`, dry-run and real reconstruction of **synthetic** fixtures, content/path assertions, and uninstall.
- Verify Python versions available **locally** and document version gaps. No fabricated CI results and no restored running of GitHub Actions.
- Validate `skills/repomix-unmixer/SKILL.md` with `skills-ref validate` when locally installable. Ensure examples use current names and absolute/portable instructions, safe static-only contract, and do not rely on old repo identifiers.
- Smoke-test actual skill discovery and CLI use in **already-installed** Codex, Claude Code, Cursor, Gemini CLI and OpenCode where available. Record host, version, exact invocation, test result, and missing-host deferrals. Do not install untrusted/reconstructed code, use hidden credentials, or claim any platform integration not tested. Prefer **one portable skill**; add adapter files only if a particular host demonstrably needs one.
- Add `docs/AGENT_INSTALL.md` with verified host setup, manual copy/symlink instructions, known limitations, and a no-execution warning. Do not claim a universal agent marketplace listing.

**Exit gate:** locally reproducible build and smoke tests, validated skill, and honest host compatibility notes. Unavailable host tests may remain deferred.

### D. PyPI + distribution preparation (P1-09, P2-04, P0-17)

**Prepare now; publish only after the final safety/provenance gate and when the publishing method is available.**

1. Check current `repomix-unmixer` project-name availability and repository ownership using the authoritative [PyPI site](https://pypi.org/) (not guessing from a 404). If occupied, stop; do not publish over someone else's package or silently rename the project.
2. Confirm package metadata, README links, Python requirements, entrypoints, MIT `LICENSE`, package data and wheel/sdist contents are correct. Avoid secrets, real archives, and generated source trees.
3. Prefer [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) via GitHub OIDC with a narrowly-scoped `pypi` environment and publish job `id-token: write` only; no stored PyPI API token. Configure a *pending publisher* for a new project if supported, or an existing-project publisher if owned, using the **exact** repository and workflow filename. Any interactive PyPI/GitHub account steps are reported precisely as manual blockers, not invented success.
4. Write a **publication-ready but non-executed** `.github/workflows/publish-pypi.yml`, gated to protected release tags or an explicit approved release workflow. Never trigger it, publish packages, start GitHub Actions, or accidentally give OIDC permissions to PR jobs. Preserve user control over environment approvals and tag creation.
5. Prepare `docs/PUBLISHING.md`: preflight, artifact checksums, PyPI setup, safe release/tag sequence, rollback/yank options, repository visibility, no-token policy, and how to verify the installed PyPI package *after* publication. Do not claim a published artifact or use `pip install repomix-unmixer` as a current instruction until it exists.
6. Prepare distribution notes for the portable Agent Skill (`skills/repomix-unmixer`), including canonical GitHub path, validation proof, optional directory/submission processes, and actual host compatibility. Submit to any directory only after its listing requirements are satisfied and public repo approval is obtained; avoid unsupported marketplace claims.
7. Optionally add narrowly scoped Dependabot or dependency-maintenance configuration only if useful with the existing low-dependency runtime; avoid any new Actions usage and record account-level limitations.

**Exit gate:** validated local distributions and verified publishing configuration; exact pending account tasks recorded. The PyPI upload, directory registration and website deployment remain **deferred**, unless the final release gate is completed and a safe publication route is explicitly available.

### E. Final release gate (P0-07, P0-17)

- Perform a source/asset/license provenance review: identify authorship and outside material, verify permissions for MIT redistribution and original visual assets, and record the evidence in a **non-sensitive** `docs/RELEASE_CHECKLIST.md` entry. Escalate actual rights uncertainty rather than asserting an unverified legal conclusion.
- Confirm no input/output snapshots, credentials, old private codebases, or accidental binary/sample data are tracked. Refresh the *current reachable tree* privacy check without reopening the already-accepted old PR cache/email-metadata issue.
- Confirm local QA gates from A–D, links, version and clean install. Prepare accurate release notes and checksum list; review `SECURITY.md` for statements stronger than tested evidence. Do not promote unverified external-audit claims.
- Keep the remaining *optional* items out of the blocking list: website hosting, social-image upload, GIF, codebase expansion, extra formats and uninstalled host integrations.
- Mark P0-17 **Done only when** mandatory evidence is documented and the maintainer's publication decision is confirmed. Keep all visibility changes, public GitHub release, live PyPI upload and directory submission **on hold** until then.
- If blocked, stop with **one concise completion table**: Done / Deferred / Needs maintainer action. Do not restart a new planning cycle.

## Git/GitHub procedure while Actions quota is exhausted

1. Start from current private `origin/main`, verify branch protection and clean worktree. Use scoped branches/PRs (or one cohesive release-prep branch if merging per task is impractical), and keep per-task evidence in the backlog.
2. Do not dispatch or retry Actions. For commits that would otherwise trigger push/PR workflows, put `[skip ci]` in the commit message; **skipped required checks remain Pending**, not passed. Run and capture the equivalent local checks instead.
3. Existing `main` requires strict GitHub CI checks. A PR may therefore be unmergeable while quota is exhausted. **Do not force-push or bypass branch protection silently**. If a narrowly scoped, reversible rule adjustment is absolutely required to merge locally verified work, record the before/after settings, preserve the PR requirement and force-push/deletion protections, and restore the original check requirements immediately. If that cannot be done safely, leave the PR awaiting quota restoration and report the blocker.
4. Never create a public release or PyPI publication simply because local tests passed. A complete local release candidate can remain private until its administrative gates are resolved.

## Sources of current practice

- [GitHub community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [GitHub issue and PR templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [PyPI pending publishers](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
- [Agent Skills specification](https://agentskills.io/specification)
- [Skipping GitHub Actions runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)
