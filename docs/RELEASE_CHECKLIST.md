# Release readiness checklist (not yet satisfied)

See `docs/BACKLOG.md` for task IDs. GitHub target: `darizae/repomix-static-reconstructor` (PRIVATE initially). Follow `docs/AGENT_HANDOFF.md` for private setup; public visibility requires explicit approval.

## Repository hygiene
- [ ] Rights and ownership approval; choose and include a LICENSE
- [ ] Audit code, documentation and assets for credentials, personal information, and unintended files
- [ ] Run local secret scanning and independently inspect Git's full staged diff and history
- [ ] Confirm input and output snapshots are untracked; run `git ls-files` and `git status`
- [ ] Protect default branch; set issue/security reporting policy and code owners as appropriate

## Parser and security
- [x] Repomix-generated fixtures for Markdown/XML/JSON across versions, CRLF/BOM, escapes, malformed content — P0-10: Repomix 1.19.0 fixtures, byte-identical with 1.17.0/1.18.1; see `docs/PARSER_COMPATIBILITY.md`
- [x] Define exactly what is preserved and what is intentionally excluded — P0-12: `docs/EXCLUSIONS.md` defines component-exact rules, matching semantics, rationale, non-exclusions, and the no-`--strict` decision; `tests/test_exclusions.py` verifies them
- [ ] Concurrent-filesystem threat model and symlink/race/hardlink audit
- [x] Linux/macOS/Windows integration tests and failure-injection tests — P0-11: Added comprehensive adversarial tests covering permission failures, partial-write injection, resource limits, symlinks, invalid UTF-8, and cross-platform validation including macOS Bash 3.2 compatibility simulation
- [ ] Check filesystem resource limits; test dry run's lack of writes

## Packaging and agent integrations
- [ ] Define stable product name, CLI name, package name and repository slug; verify availability
- [ ] Create `pyproject.toml`, `src/` layout, console entrypoint, version command, wheel/sdist
- [ ] Clean environment installation, uninstall, and pinned supported Python-version tests
- [ ] Portable `SKILL.md` validated against Agent Skills spec; run actual host smoke tests
- [ ] Only after validation, add targeted wrappers for Claude Code, Codex, Cursor, Gemini CLI, OpenCode
- [ ] Document installation, offline operation, limitations, screenshots, comparison, and FAQ

## Brand / open-source polish
- [ ] Choose visual identity: name, tagline, color/type palette, icon/logo in SVG and PNG
- [ ] Verify logo/name aren't confusingly similar to Repomix or other brands; indicate independent project
- [ ] README hero, CLI terminal demo/GIF, concise feature matrix, security model illustration
- [ ] Branded docs website or lightweight landing page and social-preview image
- [ ] Accessible dark/light variants, alt text, responsive layout, consistent iconography

## Quality and publication
- [ ] CI quality gates: unit, formatting, types, tests on all platforms, build/install checks
- [ ] Dependabot or equivalent maintenance, dependabot alerts, optional release provenance
- [ ] CONTRIBUTING, CODE_OF_CONDUCT decision, issue templates, PR template, CHANGELOG
- [ ] Versioning strategy, release notes, checksums, tags and release artifacts
- [ ] Test install instructions with a new contributor; obtain maintainer approval to make public
- [ ] Optional distribution: PyPI, skills directory/marketplaces, docs/website after approval
