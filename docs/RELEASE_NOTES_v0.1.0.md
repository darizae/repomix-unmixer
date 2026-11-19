# repomix-unmixer v0.1.0 — release notes

**Status: published 2026-11-19.** PyPI `repomix-unmixer 0.1.0` is live, the
repository is public, and tag `v0.1.0` plus this release exist. This is the
release notes and checksum record attached to the GitHub release.

## What it is

A local Python CLI that reconstructs static file trees from Repomix Markdown,
XML and JSON exports **for offline inspection only** — it never runs recovered
code. See [`README.md`](../README.md), [`SECURITY.md`](../SECURITY.md), and
[`STATIC_INSPECTION.md`](STATIC_INSPECTION.md).

## Highlights

- `unmix-repomix`, `reconstruct-all`, and `python -m repomix_unmixer`
  entry points; `--version`, `--help`, `--dry-run`.
- Defensive writing: path validation, duplicate/case-collision detection,
  fresh-only staged output, resource limits, and a documented exclusion policy
  for auto-activating agent/IDE and credential-bearing files.
- Portable Agent Skill (`skills/repomix-unmixer/SKILL.md`) validated against
  the official Agent Skills specification.
- No third-party runtime dependencies; Python ≥ 3.10; MIT license.

## Known limitations (accepted for v0.1.0)

- Parser fidelity verified for Repomix 1.17.0–1.19.0; plain-text and
  line-numbered exports are rejected as lossy; default Repomix XML is ambiguous
  for some content (`--parsable-style` recommended).
- Exclusions are not secret scanning; neither input nor output is automatically
  safe to publish.
- Windows/Linux runtime validation and interactive agent-host smoke tests are
  deferred (GitHub Actions quota exhausted); see [`AGENT_INSTALL.md`](AGENT_INSTALL.md).
- No formal security certification or independent external audit; see
  [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md) for the threat model and residual risks.

## Install

```bash
python3 -m venv .venv
.venv/bin/python -m pip install repomix-unmixer==0.1.0
.venv/bin/unmix-repomix --version
```

## Verification summary (local, macOS arm64, Python 3.12/3.13, 2026-11-19)

- 81 unit tests pass (1 skipped: `/dev/null` device-symlink case).
- `ruff check` / `ruff format --check` / `mypy` all PASS.
- `python -m build` produced wheel + sdist; `twine check` PASSED
  (requires `packaging>=24.2` for PEP 639 metadata).
- Clean-venv install from both wheel and sdist on Python 3.13 verified:
  `--version`, `--help`, `python -m repomix_unmixer`, dry-run (writes nothing),
  real reconstruction of synthetic fixtures with byte-identical content,
  refusal to overwrite existing output, uninstall.
- `agentskills validate skills/repomix-unmixer` → "Valid skill".

## Artifact checksums (sha256, local build 2026-11-19)

Re-hash the exact artifacts you publish; these record the local candidate build.

```
e698a628139dac750dbb3c7b8ba99857778543f5e6ab0dab3586152d0589fb47  repomix_unmixer-0.1.0-py3-none-any.whl
044081d14db574f837d1c6f2ec05e84a894895ede24f0616689bb77f60c75ba8  repomix_unmixer-0.1.0.tar.gz
```

## Status

Published 2026-11-19: PyPI `repomix-unmixer 0.1.0` uploaded via Trusted
Publishing; repository made public; tag `v0.1.0` pushed; Agent Skill indexed in
the Agent Skills marketplace (`status: approved`).

Deferred / non-blocking: Windows/Linux CI validation once Actions quota is
restored, website deployment, social-card upload, demo GIF, host-specific
agent wrappers, and third-party marketplace review.