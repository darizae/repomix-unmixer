# Static inspection guide

How to inspect a reconstructed tree without triggering execution, network
access, or configuration side effects. Read this before opening the output in
an editor, IDE, agent session, or anything that indexes directories.

## The core rule

A reconstructed tree is **untrusted data**. Reading files with a text viewer
(`cat`, `less`, `grep`, `rg`, a plain text editor) is safe. Everything else —
building, testing, installing, opening in an IDE, pointing an AI coding agent
at the folder — has side effects you cannot see from the file contents.

## What auto-activates and why it was excluded

The extractor omits the highest-risk paths entirely; the rationale and exact
matching rules are in [`EXCLUSIONS.md`](EXCLUSIONS.md):

- MCP clients launch servers declared in `.mcp.json` or agent settings.
- Claude Code, Cursor, Codex, Gemini CLI, and OpenCode load hooks, plugins,
  and MCP definitions from their configuration directories.
- `direnv` executes `.envrc` on directory entry.
- IDE metadata (`.vscode/`, `.idea/`) can define tasks, launchers, and
  interpreter paths.
- `.git/hooks/` run on ordinary Git commands.
- `.env`/`.env.*` conventionally hold credentials.

The exclusion list is deliberately small. It does **not** make the tree safe
to execute, and retained files can still contain whatever an attacker wanted
you to read or run.

## Commands with hidden side effects on recovered code

Treat all of the following as **execution of recovered code**, even when they
look read-only:

| Category | Examples | Hidden effect |
|---|---|---|
| Installers | `pip install -e .`, `npm install`, `uv sync` | Runs `setup.py`, `postinstall` scripts, lifecycle hooks; fetches packages over the network |
| Build/test tools | `make`, `cmake`, `pytest`, `npm test`, `cargo test` | Compiles and executes recovered source, build scripts, `conftest.py`, `tox.ini` |
| Git operations | `git log`, `git status`, `git checkout` | Runs `.git/hooks/*` if a `.git` directory survived (it is excluded by default, but check) |
| Containers | `docker build`, `docker compose up` | Executes Dockerfiles, compose commands, image build steps |
| Agent integrations | Claude Code, Codex CLI, Cursor, Gemini CLI, OpenCode pointed at the folder | May load MCP configs and hooks, index files, run project commands, or send code to remote services |
| Editors/IDEs | VS Code, JetBrains with the folder as workspace | Workspace trust prompts, task/launch configs, extensions |
| Language servers | Pylance, gopls, rust-analyzer | Execute build scripts to resolve imports |

## Recommended environment

1. **Fresh output directory, written by the extractor only.** The tool refuses
   existing destinations; do not merge trees from different exports.
2. **Outbound-network isolation when available.** Inspect from an offline
   machine, container, or VM, or block egress with your firewall/proxy. The
   extractor makes no network calls, but *your tooling* will if you let it.
3. **No administrator/root.** Run under an unprivileged account, in a working
   directory not shared with other users or processes.
4. **Read-only tools only:** `rg`, `cat`, `less`, `diff`. Open files
   individually rather than letting a tool walk and index the tree.
5. **Never run a recovered project's commands**, its package managers, its
   hooks, its containers, or its CI configuration — including "just to see if
   it builds".

## What "static" guarantees — and what it does not

| Guaranteed | Not guaranteed |
|---|---|
| The extractor itself never executes recovered content, spawns shells, or contacts the network | Anything *you* run afterwards (editors, agents, builds) is outside that boundary |
| Retained paths/contents are preserved exactly (within parser limits) | The export may be lossy — see `PARSER_COMPATIBILITY.md` |
| High-risk auto-activation paths are omitted from output | Output contains no secrets — it may, and you must review before sharing |
| Fresh-only writes; existing trees are never replaced | Filesystem-level attacks under concurrent manipulation (independent audit pending) |

## Reporting

Found a safety issue in the extractor itself? See
[`SECURITY.md`](SECURITY.md) for the reporting channel. Do not open a public
issue with proof-of-concept details for anything that could help attackers.
