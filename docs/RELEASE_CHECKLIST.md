# Release readiness checklist (not yet satisfied)

**Execution spec:** [`RELEASE_EXECUTION_PLAN.md`](RELEASE_EXECUTION_PLAN.md). **Blocking:** filesystem/race and dry-run/resource review; rights/provenance; reproducible local build and install; truthful community security/conduct contacts; final approval. **Deferred:** GitHub Actions while quota exhausted, website/social/GIF, unused host integrations, and already accepted name/logo. Keep a deferred check unchecked, never claim it passed.

See `docs/BACKLOG.md` for task IDs. GitHub remote: `darizae/repomix-unmixer` (**private**). Public visibility requires explicit maintainer approval.

## Repository hygiene
- [x] Select and include an MIT license — maintainer authorized MIT on 2026-11-19; root `LICENSE` and package metadata added.
- [ ] Complete independent rights/provenance review (including third-party contributions/assets) before publication; license selection alone does not establish ownership.
- [x] Complete approved Git author/committer metadata history cleanup, re-audit all resulting refs, and assess GitHub-hosted cached/PR objects before public release — P0-19 (2026-11-19): `git-filter-repo` rewrite replaced the maintainer's personal email with the GitHub noreply address across all reachable refs (`main` and the stale `release/` branch); `main` rewritten to `789d766`. Contents, messages and dates preserved; no personal email remains in reachable commit metadata; backup kept outside the repo. Limit: all 16 merged PR head refs (`refs/pull/*/head`) still point at pre-rewrite SHAs and require GitHub Support sensitive-data removal for full purge (account-level, not git-rewriteable).
- [x] Audit code, documentation and assets for credentials, personal information, and unintended files — P0-08 (2026-11-19): all 64 commits (reachable + dangling) and 141 blobs scanned for keys, tokens, emails, URLs, private IPs, hostnames and high-entropy strings; none found. External URLs are intentional comparisons in `docs/BRAND.md`; binary assets carry no embedded metadata
- [x] Run local secret scanning and independently inspect Git's full staged diff and history — P0-08 (2026-11-19): regex/entropy scan across full history, reachable and dangling; removed bootstrap/handoff files carry no secrets. No local secret-scanner CLI installed (gitleaks/trufflehog/detect-secrets deferred); GitHub secret scanning limited by account plan
- [x] Confirm input and output snapshots are untracked; run `git ls-files` and `git status` — P0-08 (2026-11-19): `repomix-files/` holds only `.gitkeep`; no input/output snapshots tracked; working tree clean; `origin/main` in sync
- [x] Protect `main` after the approved history rewrite; verify actual GitHub ruleset/branch-protection settings — 2026-11-19: configured and verified classic `main` branch protection via the GitHub API (`gh`): PR required before merging (no reviewer approval needed), strict required status checks (`Lint (ruff)`, `Types (mypy)`, `Agent Skills validation`, `Build, inspect, wheel smoke test`), `enforce_admins: true`, force-pushes blocked, deletions blocked, linear history required. Repository rulesets were rejected on this plan as paid-only. Private-vulnerability-reporting toggle and secret scanning availability remain account/plan-level review.

## Parser and security
- [x] Repomix-generated fixtures for Markdown/XML/JSON across versions, CRLF/BOM, escapes, malformed content — P0-10: Repomix 1.19.0 fixtures, byte-identical with 1.17.0/1.18.1; see `docs/PARSER_COMPATIBILITY.md`
- [x] Define exactly what is preserved and what is intentionally excluded — P0-12: `docs/EXCLUSIONS.md` defines component-exact rules, matching semantics, rationale, non-exclusions, and the no-`--strict` decision; `tests/test_exclusions.py` verifies them
- [x] Concurrent-filesystem threat model and symlink/race/hardlink audit — P0-09/P0-05 (2026-11-19): threat model and tested cases in `docs/SECURITY_REVIEW.md`; regression tests for O_EXCL create-only writes, staging cleanup, nested symlink chains, write-through-symlink, hardlinks, and permission failures. Windows/Linux runtime (reparse points) and hostile shared-directory races remain documented as bounded/deferred; independent external audit pending.
- [x] Linux/macOS/Windows integration tests and failure-injection tests — P0-11: Added comprehensive adversarial tests covering permission failures, partial-write injection, resource limits, symlinks, invalid UTF-8, and cross-platform validation including macOS Bash 3.2 compatibility simulation
- [x] Check filesystem resource limits; test dry run's lack of writes — P0-05 (2026-11-19): `max_files`/`max_file_bytes`/`max_total_bytes`/`max_input_bytes` enforced at boundaries (`test_limits_preflight`, `test_file_count_boundary`, `test_huge_input_file_rejection`); dry run creates neither the output tree nor any staging directory (`test_dry_run_does_not_write`).

## Packaging and agent integrations
- [x] **repomix-unmixer** naming and repo/package/CLI identifiers accepted by maintainer (2026-11-19). No further naming review.
- [x] Create `pyproject.toml`, `src/` layout, console entrypoint, version command, wheel/sdist — P0-13: setuptools src/ layout, `unmix-repomix`/`reconstruct-all` entry points, `--version`, wheel+sdist build with `twine check` PASSED
- [x] Clean environment installation, uninstall, and pinned supported Python-version tests — P0-13/P0-14: clean-venv install (wheel and sdist), single-export + batch smoke, uninstall verified locally; CI matrix runs Python 3.10–3.13 on ubuntu/macos/windows with the full test suite
- [x] Portable Agent Skill validates against the official specification (P0-15) — 2026-11-19 Phase C: `agentskills validate` → "Valid skill" (skills-ref 0.1.1); installed CLI commands asserted against the built wheel/sdist; no-execute contract enforced (`tests/test_no_execution.py`).
- [ ] Execute host-specific installation smoke tests for Claude Code, Codex, Cursor, Gemini CLI and OpenCode (P1-08; **deferred** — interactive in-host discovery would invoke model APIs and modify personal agent config; installed versions and per-host install paths recorded in `docs/AGENT_INSTALL.md`).
- [ ] **Conditional, not mandatory:** add host wrappers only where real host testing proves portability insufficient.
- [x] Document installation, offline operation, safety limits, parser coverage and FAQ; add agent setup prompt (P0-16/P1-03); agent validation + per-host install notes in `docs/AGENT_INSTALL.md` (Phase C).
- [ ] **Deferred / non-blocking:** optional authentic demo capture and independent README rendering review; current README accepted.

## Brand / open-source polish
- [x] Choose visual identity: name, tagline, color/type palette, icon/logo in SVG and PNG — P1-01/P1-02: initial repomix-unmixer identity, vector and raster assets; final clearance deferred
- [x] Maintainer accepted current name/logo; existing docs state independence from Repomix. This is product acceptance, **not a claim of trademark clearance**.
- [x] README wordmark, concise feature set, CLI commands and safety links (P1-03).
- [ ] **Deferred / non-blocking:** optional demo GIF and visual README review; no duplicated release gate.
- [x] Branded local documentation landing page, original social-card SVG and extraction diagram (P1-04).
- [ ] **Deferred / non-blocking:** social-card PNG, GitHub preview upload and website deployment.
- [ ] **Deferred / non-blocking:** independent device/browser accessibility check; existing responsive assets retained.

## Quality and publication
- [x] CI quality gates: lint, types, tests across supported OS/Python versions, build/install checks — PR #8 completed successfully with all 14 jobs including Python 3.10 on Windows.
- [ ] **Best-effort release prep:** lightweight dependency maintenance and supply-chain documentation; no GitHub Actions runs. Provenance automation optional.
- [x] **P1-10** (2026-11-19): `CHANGELOG.md` (Keep a Changelog, v0.1.0 candidate); `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, enforcement contact = maintainer GitHub `darizae`/SECURITY channel, no invented email); bug/feature issue forms + `config.yml` (parse OK, blank issues disabled, security routed to SECURITY.md); `pull_request_template.md`; `CONTRIBUTING.md` revised for local-validation/`[skip ci]`. All links exist.
- [ ] **P0-17:** local artifacts, v0.1.0 notes, checksums; release/tag only when blocking gates pass (release plan Phase E).
- [ ] Test install instructions with a new contributor; obtain maintainer approval to make public
- [ ] **Prepare now:** verified PyPI metadata, Trusted Publisher configuration and Agent Skills distribution guide; **actual upload/listing gated**. Website remains deferred.
