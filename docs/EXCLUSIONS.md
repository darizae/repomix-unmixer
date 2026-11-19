# Exclusion policy

Status: implemented for **P0-12**. This document defines exactly which paths the
reconstructor omits from **reconstructed output**, why, and what the policy does not do.
The rules are implemented in `scripts/unmix_repomix.py` (`EXCLUDED_DIRECTORY_COMPONENTS`,
`EXCLUDED_FILE_NAMES`, `ENV_TEMPLATE_NAMES`, `exclusion_category`) and tested in
`tests/test_exclusions.py`.

## Contract

- **Exclusion only.** A matching path is omitted entirely. No empty placeholder is written and
  no retained file is edited, redacted, re-encoded, or normalized.
- **Retained content is unchanged.** Every written file keeps the exact parsed path and text,
  subject only to the parser fidelity limits in `docs/PARSER_COMPATIBILITY.md`.
- **Output only.** Exclusions affect the reconstructed tree, never the original Repomix export.
  The export still contains the excluded paths and their contents.
- **No confidentiality guarantee.** Neither the export nor the reconstructed tree is
  automatically safe to publish. The policy is not a secret scanner and is not exhaustive.

## Why these paths are excluded

Static inspection can still activate recovered configuration. Common tools load configuration
from a directory as soon as it is opened or entered, and some of that configuration starts
processes:

- MCP clients may launch the servers declared in `.mcp.json` or in agent-specific settings.
- Claude Code, Cursor, Codex, Gemini CLI, and OpenCode load hooks, plugins, or MCP definitions
  from their configuration directories.
- `direnv` executes `.envrc` when entering a directory.
- IDE workspace metadata can define tasks, launch configurations, interpreter paths, and
  machine-local settings.
- Git hooks in `.git/hooks/` run on ordinary Git commands, and `.git/config` can contain
  credentials and remote URLs with embedded tokens.
- `.env` and `.env.*` files conventionally hold credentials.

Omitting these paths reduces accidental auto-activation and credential propagation when the
reconstructed tree is opened. It does not make the tree safe to execute or safe to publish.

## Matching semantics

1. The parsed path is normalized to POSIX separators (`\` becomes `/`) and case-folded.
2. Rules match **complete path components**, not substrings or glob patterns.
3. A **directory rule** excludes the named component and everything beneath it.
   `.claude/settings.json`, `nested/.claude/hooks.json`, and a file named `.claude` all match.
   `.claude-backup/settings.json` and `foo.claude/x` do not.
4. A **file rule** matches only the final component.
5. Directory rules take precedence over file rules and over the environment-template exception.
6. Path validation runs **before** exclusion. `../.env`, `/.mcp.json`, and other unsafe paths are
   rejected rather than silently skipped.
7. Every parsed entry still counts against `--max-files`, so excluded entries cannot bypass the
   file-count limit. Excluded content is not written and does not count toward the total-output
   byte limit.
8. Duplicate and file-versus-directory collision checks apply to retained paths. Excluded paths
   do not collide with each other or with retained output because they are never written.

## Rules

| Category | Rule | Matching paths | Rationale |
|---|---|---|---|
| `agent-config` | File name `.mcp.json` | `.mcp.json`, `sub/.mcp.json` | MCP server definitions can start processes when an agent client opens the tree. |
| `agent-config` | Directory `.claude` | `.claude/`, `x/.claude/settings.json` | Hooks, commands, agents, and MCP settings can execute commands. |
| `agent-config` | Directory `.codex` | `.codex/config.toml` | Codex configuration can define MCP servers and notification commands. |
| `agent-config` | Directory `.cursor` | `.cursor/mcp.json`, `.cursor/rules/` | Cursor loads MCP servers, rules, and hooks from this directory. |
| `agent-config` | Directory `.gemini` | `.gemini/settings.json` | Gemini CLI loads MCP servers and hooks from its settings. |
| `agent-config` | Directory `.opencode` | `.opencode/config.json` | OpenCode loads configuration and plugins from this directory. |
| `ide-metadata` | Directory `.idea` | `.idea/workspace.xml` | IDE run configurations, tasks, and machine-local paths. |
| `ide-metadata` | Directory `.vscode` | `.vscode/settings.json`, `.vscode/tasks.json` | Workspace settings and tasks can define commands and interpreter paths. |
| `credential-config` | File name `.env` | `.env`, `app/.env` | Conventional secret-bearing environment file. |
| `credential-config` | File name `.env.*`, except templates | `.env.local`, `.env.production`, `.env.example.local` | Environment variants and derived files can contain real values. |
| `credential-config` | File name `.envrc` | `.envrc` | `direnv` executes this file on directory entry. |
| `vcs-metadata` | Directory `.git` | `.git/config`, `.git/hooks/pre-commit` | Hooks run on Git commands; config and history can contain credentials. |
| `os-metadata` | File name `.DS_Store` | `.DS_Store`, `sub/.DS_Store` | Finder metadata with no inspection value; can expose local names. |

### Retained environment templates

Exactly these file names are retained at any depth, case-insensitively:

- `.env.example`
- `.env.sample`
- `.env.template`

They are retained because they conventionally document required variables without values. This
is a convention, not a guarantee: review their contents before publishing. Variants such as
`.env.example.local`, `.env.example.bak`, and `.env.sample.txt` are **not** templates under this
policy and are excluded.

## Explicit non-exclusions

The following are **retained** and may contain secrets, machine-local paths, or execution
configuration. They are outside this policy and must be reviewed manually:

- Credential-bearing files such as `.npmrc`, `.pypirc`, `.netrc`, `.git-credentials`,
  `.pgpass`, `.docker/config.json`, `.aws/`, `.ssh/`, `.kube/config`, and private keys
  (`*.pem`, `*.key`, `id_rsa`, and similar).
- Execution configuration such as `.devcontainer/`, `.github/workflows/`,
  `docker-compose.yml`, `Makefile`, and package scripts.
- Agent-adjacent files that are not auto-loaded, such as `.mcp.json.bak`, `.claude-backup/`,
  `mcp.json` (no leading dot), `.cursorrules`, and `.aider.conf.yml`.
- Ordinary source, documentation, and configuration files, including `config.json` and
  `.gitignore`.

## No `--strict` mode

A strict mode is deliberately **not** implemented. The default exclusions cannot be disabled by
a flag, and adding a second opt-in policy would create a less-exercised rule set and a
misleading impression that non-strict output has been reviewed. If a strict mode is added later,
it must only **add** exclusions, never remove or weaken the default rules, and it must ship with
the same category labels, documentation, and tests. Any future flag that disables exclusions is
out of scope and would violate the safety contract.

## Changing the policy

Update the constants in `scripts/unmix_repomix.py`, the table above, and
`tests/test_exclusions.py` together. Keep the list small, component-exact, and justified by
auto-activation or credential risk. Do not turn it into a broad secret scanner or a promise
that retained output is safe.

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_exclusions.py' -v
python3 -m unittest discover -s tests -v
```

The exclusion tests cover the full rule table, case and separator normalization, component
boundaries, identical behavior for Markdown/XML/JSON, byte-for-byte retention of allowed files,
path validation before exclusion, file-count limits, dry-run behavior, and CLI category output.
