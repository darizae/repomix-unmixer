# Publishing guide — repomix-unmixer

This page describes how the **v0.1.0 release** was published to PyPI and how
the portable Agent Skill is distributed. **Published 2026-11-19:** PyPI
`repomix-unmixer 0.1.0` is live (Trusted Publishing), the repository is public,
and the Agent Skill is indexed in the Agent Skills marketplace.

Publication gates were satisfied and the v0.1.0 release was published on
2026-11-19; the repository is public and PyPI `repomix-unmixer 0.1.0` is live.
Website deployment, social-preview upload, demo GIF, and marketing remain
deferred.

## 1. Preflight (run locally, before tagging)

From a clean checkout of the release tag:

```bash
python3 -m venv .preflight-venv
.preflight-venv/bin/python -m pip install --upgrade build twine "packaging>=24.2"
.preflight-venv/bin/python -m unittest discover -s tests -v
ruff check src tests && ruff format --check src tests
mypy src/repomix_unmixer
.preflight-venv/bin/python -m build
.preflight-venv/bin/python -m twine check dist/*
```

`twine check` requires `packaging>=24.2` to accept the PEP 639
`License-Expression: MIT` metadata. Verify the wheel/sdist contents (MIT
`LICENSE`, `py.typed`, both console entry points, README) and install each
archive into a fresh venv as described in [`AGENT_INSTALL.md`](AGENT_INSTALL.md).

## 2. Artifact checksums

Record `sha256` (and optionally `sha512`) for every artifact you ship so
downstream users can verify downloads:

```bash
shasum -a 256 dist/*       # macOS
sha256sum dist/*           # Linux
```

Example (v0.1.0 candidate, built locally 2026-11-19):

```
# NOTE: re-hash the exact artifacts you publish; these were the local build.
```

See the release notes/checksum file attached to the GitHub release for the
authoritative values.

## 3. PyPI setup — Trusted Publishing

Prefer [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
(GitHub OpenID Connect). No PyPI API token is stored anywhere; the publish
workflow mints a short-lived credential per run.

Because `repomix-unmixer` is **not yet registered** on PyPI (verified
2026-11-19 via `https://pypi.org/pypi/repomix-unmixer/json` → 404 and the
simple index), use a
[pending publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/):

- **Project name:** `repomix-unmixer`
- **Owner / repository:** `darizae/repomix-unmixer`
- **Workflow filename:** `.github/workflows/publish-pypi.yml`

If the name were already taken, stop and resolve ownership rather than
silently renaming. The maintainer must complete the PyPI account/owner steps
interactively; record them as manual tasks.

The committed workflow is gated to `v*` tag pushes and explicit
`workflow_dispatch`, uses `permissions: { id-token: write, contents: read }`
on the publish job only, and routes through a `pypi` GitHub environment so
required reviewers must approve before any upload. It is intentionally not run
during release preparation.

## 4. Safe release / tag sequence

1. Merge all approved work to `main`; run the local preflight above.
2. Create and push the signed tag: `git tag -s v0.1.0 && git push origin v0.1.0`.
   Tag creation is a human action, not automated.
3. The `Publish to PyPI` workflow runs on the tag; the `pypi` environment
   approval gates the upload.
4. Create a GitHub release for the tag with the release notes and checksum
   file.
5. After publication, verify the installed package (see §6).

Never force-push tags, never upload over an existing project you do not own,
and keep the repository **private** until the final visibility decision.

## 5. Rollback / yank

- **Yank a broken release:** on PyPI, yank `repomix-unmixer==0.1.0` so new
  installs avoid it while the files remain for those already pinned.
- **Fix-forward:** push the corrected version as `0.1.1` (or `0.1.0.post1`)
  and update the GitHub release.
- **Revert a tag:** only by deleting/rewriting a tag you own, with
  communication, never force-push a shared tag silently.

## 6. Verify after publication

```bash
python3 -m venv /tmp/verify
/tmp/verify/bin/python -m pip install repomix-unmixer==0.1.0
/tmp/verify/bin/unmix-repomix --version
/tmp/verify/bin/reconstruct-all --help
/tmp/verify/bin/python -m repomix_unmixer --version
```

Then reconstruct a **synthetic** fixture and confirm byte-identical content,
and check the checksums from §2 against the installed distribution.

## 7. Agent Skill distribution

The portable skill lives at `skills/repomix-unmixer/SKILL.md` in the canonical
GitHub repository `darizae/repomix-unmixer` (path after a public release:
`https://github.com/darizae/repomix-unmixer/blob/main/skills/repomix-unmixer/SKILL.md`).
Validation proof: `agentskills validate skills/repomix-unmixer` → "Valid
skill".

To submit to a skills directory/registry or agent marketplace, satisfy **that
directory's** listing requirements first (many require a public repo, a
license, and a tested skill), and obtain explicit public-release approval.
Submit **only after** the repo is public; do not claim a marketplace listing
that does not exist. Per-host install steps are in
[`AGENT_INSTALL.md`](AGENT_INSTALL.md).

## 8. Repository visibility

Keep `darizae/repomix-unmixer` **private** until the maintainer approves the
public switch after all gates, including the history-metadata and provenance
review. Making the repository public is a separate, explicit action from
publishing the package.