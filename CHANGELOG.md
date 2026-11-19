# Changelog

All notable changes to repomix-unmixer are documented here, following
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The v0.1.0 release candidate. **Not published yet**: no PyPI release or public
GitHub release exists. Publication is gated on the mandatory checks in
[`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).

### Added

- Local Python CLI (`unmix-repomix`, `reconstruct-all`, `python -m repomix_unmixer`)
  that reconstructs static file trees from Repomix Markdown, XML and JSON
  exports without running or rewriting recovered content.
- `--dry-run`, traversal/path rejection, duplicate and case-collision
  detection, file/directory-conflict checks, and configurable file/count/size
  limits (`--max-input-mib`, `--max-file-mib`, `--max-total-mib`, `--max-files`).
- Fresh-only, staged writes: the destination must be absent, output is staged
  in a private temporary directory and moved into place only when complete;
  failures clean up and leave no partial tree.
- Documented safety-based exclusion policy (`docs/EXCLUSIONS.md`) that omits
  auto-activating agent/IDE configuration and credential-bearing environment
  files from reconstructed output.
- Portable [Agent Skill](skills/repomix-unmixer/SKILL.md) validated against the
  official Agent Skills specification.
- Distribution metadata (`pyproject.toml`, `src/` layout, `py.typed`, MIT
  license, console entry points, `--version`).
- Community files: `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`,
  issue forms, PR template, `SECURITY.md` reporting channel.
- Documentation: `README.md`, `docs/FAQ.md`, `docs/STATIC_INSPECTION.md`,
  `docs/PARSER_COMPATIBILITY.md`, `docs/EXCLUSIONS.md`,
  `docs/SECURITY_REVIEW.md`.

### Fixed

- Windows reserved device-name and trailing-dot/whitespace aliasing path
  components are now rejected on every platform so the case-collision preflight
  cannot be bypassed on Windows.
- Permission, `mkdir`, staging-creation and final-`rename` failures now surface
  as clean errors with staging cleanup instead of bare tracebacks.

### Known limitations

- Parser fidelity is verified for Repomix 1.17.0–1.19.0; plain-text and
  line-numbered exports are rejected as lossy, and default Repomix XML is
  ambiguous for some content (regenerate with `--parsable-style`).
- Exclusions are not secret scanning; neither input nor output is automatically
  safe to publish.
- Windows/Linux runtime validation and agent-host integration smoke tests are
  deferred (GitHub Actions quota exhausted); see `docs/AGENT_INSTALL.md`.
- No formal security certification or independent external audit.