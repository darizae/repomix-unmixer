<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/wordmark-dark.svg">
    <img src="assets/brand/wordmark-light.svg" alt="repomix-unmixer logo" width="530">
  </picture>
  <p>
    <a href="https://pypi.org/project/repomix-unmixer/"><img src="https://img.shields.io/pypi/v/repomix-unmixer.svg?color=blue" alt="PyPI version"></a>
    <a href="https://pypi.org/project/repomix-unmixer/"><img src="https://img.shields.io/pypi/pyversions/repomix-unmixer.svg?color=blue" alt="Python versions"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://www.agentskills.in/marketplace?author=darizae"><img src="https://img.shields.io/badge/Agent%20Skill-indexed-brightgreen.svg" alt="Agent Skill indexed in the Agent Skills marketplace"></a>
  </p>
</div>

# repomix-unmixer

**Unmix Repomix. Inspect the code, not its side effects.**

**Security-first, offline unpacking:** reconstruct [Repomix](https://repomix.com/) Markdown, XML and JSON exports into readable file trees—**without ever executing recovered code**. The extractor rejects unsafe paths, refuses overwrites, enforces resource limits and omits common auto-activating configurations.

Built for **safer static inspection** of untrusted exports in a trusted local output directory; not a sandbox, malware scanner or guarantee that recovered files are confidential.

## Core features

- **Three export formats:** reconstruct text files and directories from Repomix **Markdown, XML and JSON**.
- **Block unsafe paths:** reject traversal, Windows-special names, duplicate/case-colliding paths and file/directory conflicts before writing.
- **Protect existing files:** dry-run first; fresh-output-only staged writes refuse existing destinations, with file-count and byte limits.
- **Reduce accidental auto-execution:** exclude common agent/IDE auto-start configuration and environment files; never run recovered code or make network requests.
- **CLI, batches and agents:** `unmix-repomix` for individual exports, `reconstruct-all` for Markdown batches, plus the portable Agent Skill.

## Quick start

Requires **Python 3.10+**. From a trusted checkout (not from a recovered repository):

```bash
python3 -m pip install .
```

**One export (Markdown, XML or JSON)**

```bash
unmix-repomix ./repomix-output.md ./restored-tree --dry-run
unmix-repomix ./repomix-output.md ./restored-tree
# Other supported formats:
unmix-repomix ./repomix-output.xml ./restored-xml
unmix-repomix ./repomix-output.json ./restored-json
```

The CLI detects the input format automatically. For XML, Repomix `--parsable-style` is recommended when content is ambiguous. Plain-text and line-numbered exports are unsupported.

**Batch Markdown exports**

Place your own `.md` exports inside `repomix-files/` (ignored by Git), then:

```bash
reconstruct-all --dry-run
reconstruct-all
```

Batch output appears in `reconstructed/`. The original export and any reconstructed files remain your responsibility; never commit or publish them without review.

## Use it with an AI coding agent

This repository includes a [portable Agent Skill](skills/repomix-unmixer/SKILL.md). Agent-host integration is not yet verified on every platform (tracked as P1-08).

**Agent setup prompt — copy and paste:**

```text
Work in this trusted repomix-unmixer repository.
Read AGENTS.md, SECURITY.md, and
skills/repomix-unmixer/SKILL.md.

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

[Docs preview](docs/site/README.md) · [FAQ](docs/FAQ.md) · [Agent Skill](skills/repomix-unmixer/SKILL.md) · [Contributing](CONTRIBUTING.md) · [Backlog](docs/BACKLOG.md) · [Release checklist](docs/RELEASE_CHECKLIST.md)

**Status:** v0.1.0 published — available on [PyPI](https://pypi.org/project/repomix-unmixer/), [MIT-licensed](LICENSE), with an [Agent Skill](https://www.agentskills.in/marketplace?author=darizae) indexed in the Agent Skills marketplace.

## Agent-assisted setup

[Open the agent setup page](https://darizae.github.io/repomix-unmixer/) or [copy the plain-text prompt](docs/agent-setup.txt) into your coding agent. Review its proposed changes and verification results.
