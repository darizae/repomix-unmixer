# Product identity and positioning

## Product

**RepoUnfold** is the public-facing working identity for **Repomix Static Reconstructor**.

**Tagline:** *From a packed export to an inspectable file tree.*

**One sentence:** RepoUnfold reconstructs supported Repomix exports into static directories for offline source review without executing recovered code.

**Audience:** developers, maintainers, documentation authors, and coding-agent operators who need to inspect a packed code snapshot as individual files.

## What makes it useful

- Restore individual text files and directory structure from supported Repomix Markdown, XML, or JSON exports.
- Inspect without executing recovered code: no build, install, shell, containers, hooks, or network access by the extractor.
- Validate output paths before writing: reject traversal, ambiguous paths, cross-platform collisions and file/directory conflicts.
- Write to a fresh output directory through staging, with file and total-size limits and explicit reporting of excluded high-risk paths.
- Run one-off reconstructions or batch exports; use the portable Agent Skill for guided static inspection.

This is **not** a Git history restoration tool, security sandbox, malware or credential scanner, or automatic way to make source safe to share. See [Security](../SECURITY.md), [Compatibility](PARSER_COMPATIBILITY.md) and [Exclusions](EXCLUSIONS.md).

## Where it sits among other tools

| Tool | Primary purpose | Notes |
|---|---|---|
| [Repomix](https://repomix.com/) | Pack a codebase into one export | Upstream project; RepoUnfold is independently maintained, not affiliated. |
| [repomix-unmixer](https://github.com/daymade/claude-code-skills/tree/main/repomix-unmixer) | Unpack Repomix exports as an agent skill | Also supports XML, Markdown and JSON; generally serves reconstruction workflows. |
| [repomix-unpack](https://github.com/jurijat/repomix-unpack) | Extract packed text exports through a CLI | A different format emphasis; check live capabilities before publishing comparisons. |
| **RepoUnfold** | Offline, static-only reconstruction with defensive output constraints | Optimized for inspecting recovered text without running it; not a confidentiality guarantee. |

Do not advertise superior security, complete fidelity, universal agent compatibility, or competitor limitations without a maintained test matrix.

## Naming and distribution continuity

- Public-facing identity: **RepoUnfold** (working identity; final rights/trademark review pending).
- GitHub repository: `darizae/repomix-static-reconstructor` (unchanged).
- Python distribution: `repomix-static-reconstructor` (unchanged).
- Python package: `repomix_static_reconstructor` (unchanged).
- CLI commands: `unmix-repomix` and `reconstruct-all` (unchanged).
- Portable skill: `skills/repomix-static-reconstructor/` (unchanged).
- Version: existing `0.1.0` package metadata; **no public release implied**.

This separates a recognizable visual brand from installed interfaces. Any future rename of the distribution, CLI or repository is a versioned, separately approved compatibility change. Do not claim PyPI or website availability.

## Name and trademark checks

A GitHub repository-name spot check found no exact `RepoUnfold` match among returned results, but a similarly named `RepoUnfolder` repository exists. General web searches found no obvious exact branded tool. **These are not legal clearance or a guarantee of name availability.** Before a public launch: review live GitHub/PyPI collisions, relevant trademarks, and confusion risk; obtain maintainer sign-off. Avoid Repomix's logomark or suggesting endorsement.

## Tone

Short, precise, developer-focused. Lead with the use case and three-step workflow: **inspect the export → validate → reconstruct into a new directory**. Keep security limitations in a concise section with links to detailed policies. Show verified examples, not synthetic success claims or arbitrary badges.
