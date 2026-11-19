# Repomix Static Reconstructor

**Reconstruct repository-shaped, static files from Repomix exports — without running recovered code.**

This is an early-stage, private-first tool. It is **not** a public release, a confidentiality scanner, or a complete Git repository recovery system. Development and release tasks are tracked in [`docs/BACKLOG.md`](docs/BACKLOG.md).

## What makes this useful

- **Inspect, don't execute:** unpack exported source for reading, searching, comparison, and architectural review. Do not build/test/run the *reconstructed* project.
- **Filesystem guardrails:** reject ambiguous, absolute, traversal and Windows-special paths; detect case-insensitive path collisions and file/directory conflicts; reject existing output; enforce limits.
- **Conservative exclusions:** skip a small generic set of auto-activating agent configuration, local IDE metadata, and credential configuration files (`.mcp.json`, `.env`, `.claude/`, etc.). The skip list is not a guarantee that sensitive content is absent.
- **Batch workflow:** unpack multiple `.md` exports to separate folders and produce a report.
- **No network:** the extractor uses Python's standard library and does not fetch dependencies or execute extracted repository commands.

**Crucial:** The extractor preserves the parsed filenames and text provided by Repomix (subject to documented parsing and file exclusions). Outputs may contain confidential data. **Review inputs and reconstructed outputs separately before sharing or publishing.**

## Quick start (Python 3.10+)

Place your own Repomix Markdown files in `repomix-files/`. That folder is empty in the distributed bundle.

```bash
python3 scripts/reconstruct_all.py --dry-run
python3 scripts/reconstruct_all.py
```

The driver creates `reconstructed/<export-stem>/` and a `reconstructed/RECONSTRUCTION_REPORT.md`. Existing per-export output folders are not overwritten. Never run commands from inside a reconstructed folder.

Single input (Markdown, XML, or JSON):

```bash
python3 scripts/unmix_repomix.py ./repo-export.md ./my-static-copy --dry-run
python3 scripts/unmix_repomix.py ./repo-export.md ./my-static-copy
```

The CLI has **no overwrite command**. To reconstruct again, choose a new output directory; manually remove old generated files only after verifying their contents.

Run tests *against the trusted extractor*, not against reconstructed repositories:

```bash
python3 -m unittest discover -s tests -v
```

## Security boundaries and limitations

The extractor never executes packed source; it does not run a shell, imports, package managers, builds, Docker, CI or project-defined scripts. It rejects unsafe path patterns and writes into newly created directories through a temporary staging directory. Some potential symlink race / concurrent filesystem attack scenarios still require an independent audit; **do not run as administrator/root or in a shared adversarial writable directory**. See [`SECURITY.md`](SECURITY.md).

The input format itself may be lossy. Repomix trims leading/trailing file whitespace, strips file BOMs, and omits binary/ignored files; no Git history or information removed by Repomix transformations can be restored. Parser coverage is verified against Repomix 1.17.0–1.19.0 fixtures for Markdown, XML (default and `--parsable-style`), and JSON, including CRLF, export BOMs, empty files, inline fences, XML entities, and special-character paths. Line-numbered exports are rejected; plain-text, split, compressed, and otherwise lossy exports are documented in [`docs/PARSER_COMPATIBILITY.md`](docs/PARSER_COMPATIBILITY.md).

## Repository scope

This repository contains the extractor, synthetic tests, a portable agent skill, and release documentation. No real input archives or reconstructed output trees belong in version control. The project is not yet licensed for public distribution; ownership review and license selection are release prerequisites.

## Private GitHub setup (local agent)

The target owner and repository name are already set. After checking the files and reading `docs/AGENT_HANDOFF.md`, an agent running on your machine can initialize Git and create the **private** repository with:

```bash
bash scripts/bootstrap_private_github.sh
```

The script requires local GitHub CLI authorization to the `darizae` account and checks that the remote is private. Do not make the repository public as part of setup. It has **not** been created or pushed by this ZIP preparation step.

## Repository roadmap

Start with [`docs/AGENT_HANDOFF.md`](docs/AGENT_HANDOFF.md) for no-placeholder setup of the new private **`darizae/repomix-static-reconstructor`** remote, [`docs/BACKLOG.md`](docs/BACKLOG.md) for tasks, and [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md) for the release gates. Agent behavior is defined in [`AGENTS.md`](AGENTS.md). The agent usage guide is in [`SKILL.md`](SKILL.md). Branding, logo assets, packaging into a conventional `pip`-installable CLI, multi-agent skill adapters, and website/docs design are **planned, not implemented**.
