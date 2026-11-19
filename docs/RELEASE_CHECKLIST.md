# Release readiness checklist (not yet satisfied)

See `docs/BACKLOG.md` for task IDs. GitHub remote: `darizae/repomix-static-reconstructor` (**private**). Public visibility requires explicit maintainer approval.

## Repository hygiene
- [ ] Rights and ownership approval; choose and include a LICENSE
- [x] Audit code, documentation and assets for credentials, personal information, and unintended files — P0-08 (2026-11-19): all 64 commits (reachable + dangling) and 141 blobs scanned for keys, tokens, emails, URLs, private IPs, hostnames and high-entropy strings; none found. External URLs are intentional comparisons in `docs/BRAND.md`; binary assets carry no embedded metadata
- [x] Run local secret scanning and independently inspect Git's full staged diff and history — P0-08 (2026-11-19): regex/entropy scan across full history, reachable and dangling; removed bootstrap/handoff files carry no secrets. No local secret-scanner CLI installed (gitleaks/trufflehog/detect-secrets deferred); GitHub secret scanning limited by account plan
- [x] Confirm input and output snapshots are untracked; run `git ls-files` and `git status` — P0-08 (2026-11-19): `repomix-files/` holds only `.gitkeep`; no input/output snapshots tracked; working tree clean; `origin/main` in sync
- [ ] Protect default branch and verify GitHub security settings — `SECURITY.md` and `CONTRIBUTING.md` exist. Branch protection and the private-vulnerability-reporting toggle remain deferred; secret scanning is limited by the account plan.

## Parser and security
- [x] Repomix-generated fixtures for Markdown/XML/JSON across versions, CRLF/BOM, escapes, malformed content — P0-10: Repomix 1.19.0 fixtures, byte-identical with 1.17.0/1.18.1; see `docs/PARSER_COMPATIBILITY.md`
- [x] Define exactly what is preserved and what is intentionally excluded — P0-12: `docs/EXCLUSIONS.md` defines component-exact rules, matching semantics, rationale, non-exclusions, and the no-`--strict` decision; `tests/test_exclusions.py` verifies them
- [ ] Concurrent-filesystem threat model and symlink/race/hardlink audit
- [x] Linux/macOS/Windows integration tests and failure-injection tests — P0-11: Added comprehensive adversarial tests covering permission failures, partial-write injection, resource limits, symlinks, invalid UTF-8, and cross-platform validation including macOS Bash 3.2 compatibility simulation
- [ ] Check filesystem resource limits; test dry run's lack of writes

## Packaging and agent integrations
- [ ] Define stable product name, CLI name, package name and repository slug; verify availability
- [x] Create `pyproject.toml`, `src/` layout, console entrypoint, version command, wheel/sdist — P0-13: setuptools src/ layout, `unmix-repomix`/`reconstruct-all` entry points, `--version`, wheel+sdist build with `twine check` PASSED
- [x] Clean environment installation, uninstall, and pinned supported Python-version tests — P0-13/P0-14: clean-venv install (wheel and sdist), single-export + batch smoke, uninstall verified locally; CI matrix runs Python 3.10–3.13 on ubuntu/macos/windows with the full test suite
- [x] Portable Agent Skill validates against the official specification (P0-15), including CI structure tests.
- [ ] Execute host-specific installation smoke tests for Claude Code, Codex, Cursor, Gemini CLI and OpenCode (P1-08; deferred).
- [ ] Only after validation, add targeted wrappers for Claude Code, Codex, Cursor, Gemini CLI, OpenCode
- [x] Document installation, offline operation, safety limits, parser coverage and FAQ; add agent setup prompt (P0-16/P1-03).
- [ ] Record authentic terminal walkthrough GIF/capture and test README rendering (deferred).

## Brand / open-source polish
- [x] Choose visual identity: name, tagline, color/type palette, icon/logo in SVG and PNG — P1-01/P1-02: initial repomix-unmixer identity, vector and raster assets; final clearance deferred
- [ ] Verify logo/name aren't confusingly similar to Repomix or other brands; indicate independent project
- [x] README wordmark, concise feature set, CLI commands and safety links (P1-03).
- [ ] Authentic demo GIF/capture and independent README visual review (deferred).
- [x] Branded local documentation landing page, original social-card SVG and extraction diagram (P1-04).
- [ ] Export hosted social-card PNG, upload GitHub preview and approve deployment (deferred).
- [ ] Independent visual/accessibility check (responsive layout, dark/light wordmarks, alt text, contrast) on actual browser/device; source assets and semantic HTML are present (deferred).

## Quality and publication
- [x] CI quality gates: lint, types, tests across supported OS/Python versions, build/install checks — PR #8 completed successfully with all 14 jobs including Python 3.10 on Windows.
- [ ] Dependabot or equivalent maintenance, dependabot alerts, optional release provenance
- [ ] CONTRIBUTING, CODE_OF_CONDUCT decision, issue templates, PR template, CHANGELOG
- [ ] Versioning strategy, release notes, checksums, tags and release artifacts
- [ ] Test install instructions with a new contributor; obtain maintainer approval to make public
- [ ] Optional distribution: PyPI, skills directory/marketplaces, docs/website after approval
