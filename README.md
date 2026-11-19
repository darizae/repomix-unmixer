<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/wordmark-dark.svg">
    <img src="assets/brand/wordmark-light.svg" alt="repomix-unmixer logo" width="530">
  </picture>
</div>

# repomix-unmixer

**Turn a [Repomix](https://repomix.com/) export into a browsable file tree—without running the recovered code.**

A local Python CLI for unpacking supported Markdown, XML and JSON exports into fresh directories. Designed for **static, offline source inspection**, not for executing a reconstructed application.

## Core features

- **Unpack exports:** restore individual text files and folder structure from Repomix Markdown, XML and JSON.
- **Validate first:** `--dry-run`, traversal/path rejection, duplicate and case-collision detection, and file/directory conflict checks.
- **Write defensively:** new destinations only, staged output, and configurable file/count/size limits.
- **Reduce auto-activation:** exclude a documented, limited set of agent/IDE configuration and environment files; retained text is not changed.
- **Work solo or in batches:** `unmix-repomix`, `reconstruct-all`, or the portable Agent Skill.

## Quick start

Requires **Python 3.10+**. From a trusted checkout (not from a recovered repository):

```bash
python3 -m pip install .
```

**One export**

```bash
unmix-repomix ./repomix-output.md ./restored-tree --dry-run
unmix-repomix ./repomix-output.md ./restored-tree
```

**Multiple exports**

Place your own `.md` exports inside `repomix-files/` (ignored by Git), then:

```bash
reconstruct-all --dry-run
reconstruct-all
```

Batch output appears in `reconstructed/`. The original export and any reconstructed files remain your responsibility; never commit or publish them without review.

## Use it with an AI coding agent

This repository includes a [portable Agent Skill](skills/repomix-static-reconstructor/SKILL.md). Agent-host integration is not yet verified on every platform (tracked as P1-08).

**Agent setup prompt — copy and paste:**

```text
Work in this trusted repomix-unmixer repository.
Read AGENTS.md, SECURITY.md, and
skills/repomix-static-reconstructor/SKILL.md.

Set up the Python CLI in an isolated environment from this trusted
checkout, check --version and --help, and run only the included
synthetic extractor tests. If this agent host supports Agent Skills,
register the existing skill using its documented mechanism; otherwise
use the CLI directly. Do not invent host-specific installation steps.

Never execute, import, build, install, test, or run tools from files
reconstructed from a Repomix export. Keep the repository private,
never commit input/output snapshots, and report what you verified
and which host checks remain deferred.
```

For development tasks, tell the agent to read [AGENTS.md](AGENTS.md) and tackle one ID from [the backlog](docs/BACKLOG.md), using a branch, tests, commit, push and PR.

## How it fits

| | Repomix | repomix-unmixer |
|---|---|---|
| Direction | Repository → packed export | Packed export → file tree |
| Main job | Prepare an aggregated code snapshot | Recreate individual files for inspection |
| Execution | Separate tool | Never runs recovered code |

repomix-unmixer is **independent of the Repomix project**, not an official Repomix component.

## Safety and limitations

Reconstructed content is **untrusted** and may include secrets. Exclusions are not secret scanning; neither input nor output is automatically safe to share. Avoid opening output in tools that run workspace tasks or auto-load plugins. Use a fresh directory that other users cannot modify.

Parser fixtures were checked against Repomix **1.17.0–1.19.0**. Plain-text and line-numbered exports are unsupported; original Git history, omitted binaries and information removed by Repomix cannot be recovered.

Read [Security](SECURITY.md), [static inspection](docs/STATIC_INSPECTION.md), [parser compatibility](docs/PARSER_COMPATIBILITY.md), and [exclusion rules](docs/EXCLUSIONS.md) before handling untrusted inputs.

## Documentation

[Docs preview](docs/site/README.md) · [FAQ](docs/FAQ.md) · [Agent Skill](skills/repomix-static-reconstructor/SKILL.md) · [Contributing](CONTRIBUTING.md) · [Backlog](docs/BACKLOG.md) · [Release checklist](docs/RELEASE_CHECKLIST.md)

**Status:** private pre-release. No public license has been selected and no PyPI release is claimed.
