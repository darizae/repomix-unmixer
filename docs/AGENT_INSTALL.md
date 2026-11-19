# Agent install and compatibility

This page documents how to install and use the portable
[repomix-unmixer Agent Skill](../skills/repomix-unmixer/SKILL.md) in AI coding
agents. The skill is validated against the official
[Agent Skills specification](https://agentskills.io/specification); see the
"Validation" section for the exact command and result.

**Always read [`SECURITY.md`](../SECURITY.md) and
[`STATIC_INSPECTION.md`](STATIC_INSPECTION.md) first.** The skill's job is to
reconstruct **untrusted text** for static inspection. It never executes
recovered code. Pointing any agent at a reconstructed tree can still trigger
plugins, hooks, MCP servers, indexing, or remote uploads — keep inspection
offline and out of a live agent workspace.

## Validation

The skill directory is `skills/repomix-unmixer/` and its file is `SKILL.md`.

```bash
pip install skills-ref            # provides the `agentskills` command
agentskills validate skills/repomix-unmixer
# -> "Valid skill: skills/repomix-unmixer"
agentskills read-properties skills/repomix-unmixer
agentskills to-prompt skills/repomix-unmixer
```

Verified 2026-11-19 with `skills-ref` 0.1.1 (`agentskills`): `validate` returns
"Valid skill", and `read-properties`/`to-prompt` produce spec-correct output.
The installed CLI commands the skill references (`unmix-repomix`,
`reconstruct-all`, `python -m repomix_unmixer`) are asserted against the built
distribution in `tests/test_skill.py`.

## Installing the CLI

The skill drives the Python CLI. Install it from a **trusted checkout** (never
from a recovered repository) into an isolated environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
# or from a built distribution:
.venv/bin/python -m pip install repomix_unmixer-0.1.0-py3-none-any.whl
```

## Per-host setup

The skill is one portable file; most hosts only need it copied or linked into
their skills directory. The table below records what was verified on this
machine on 2026-11-19 and what remains deferred.

| Host | Version verified | Skills location | Manual install |
|---|---|---|---|
| Codex CLI | `codex-cli 0.170.0` | `~/.codex/skills/` | `mkdir -p ~/.codex/skills && cp -r skills/repomix-unmixer ~/.codex/skills/` |
| Claude Code | `2.1.223` | `~/.claude/skills/` (per-session `--plugin-dir` also works) | `mkdir -p ~/.claude/skills && cp -r skills/repomix-unmixer ~/.claude/skills/` |
| OpenCode | `1.4.6` | `~/.config/opencode/` (agent/instructions) | Link the skill into the host's agent/instructions path |
| Cursor | not installed locally | IDE skill/config path | see Cursor docs; **deferred** |
| Gemini CLI | not installed locally | — | **deferred** |

Notes:

- Copying the skill into `~/.codex/skills/` or `~/.claude/skills/` is how these
  hosts discover a skill by name (Codex: built-in skills live under
  `~/.codex/skills/`; Claude Code: `skills` directory plus `/skill-name`
  resolution, and `--plugin-dir` for session-only loading).
- The skill's example commands use the **installed** entry points
  (`unmix-repomix`, `reconstruct-all`) and `python -m repomix_unmixer`, not
  repository-relative script paths, so it works from a distribution install.
- OpenCode and Cursor vary by version; verify the exact path for your install
  before relying on discovery.

## What was actually tested (2026-11-19)

- **Skill file validation:** PASS — `agentskills validate` returns "Valid
  skill".
- **CLI the skill drives:** PASS on a clean install from both the wheel and
  sdist on Python 3.13 (`--version`, `--help`, dry-run, real reconstruction of
  synthetic fixtures, uninstall); full matrix in the release checklist.
- **Interactive in-host skill discovery:** **DEFERRED.** Confirming a host
  actually resolves and invokes the skill requires running `codex`/`claude`
  against a model (a remote API call using the operator's credentials) and
  modifying personal agent configuration. That was intentionally not done in
  this qualification pass to avoid contacting remote endpoints and touching the
  maintainer's agent config. Cursor and Gemini CLI are not installed locally
  and are deferred for the same reason. Re-run these checks when CI quota and
  explicit host approval are available.

## Known limitations

- One portable skill is the canonical source of instructions. Host-specific
  adapters are added **only** if a particular host demonstrably cannot use the
  portable skill (tracked as P2-01).
- No universal agent-marketplace or skills-directory listing is claimed. The
  skill is distributed from this repository's canonical GitHub path; see
  [`PUBLISHING.md`](PUBLISHING.md) for submission plans.
- Line-numbered and plain-text Repomix exports are rejected as lossy; the skill
  reports unsupported formats rather than guessing.

## No-execution warning

Before opening a reconstructed tree in an agent, an editor, or a build tool,
read [`STATIC_INSPECTION.md`](STATIC_INSPECTION.md). The skill itself performs
no execution of recovered content, but the *host* you point at the output may.