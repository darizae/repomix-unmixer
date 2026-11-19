# Release backlog — Repomix Static Reconstructor

Updated 2026-11-19. Implemented items still require independent release verification. This is the source of truth for repository setup and future work. Read root `AGENTS.md` for agent execution rules. All release planning documents live under `docs/` in this single bundle.

## Product contract

Reconstruct files for **static, offline inspection only**. Preserve supported parsed file paths and contents; exclude predefined configuration files entirely rather than changing their contents. Protect the local filesystem with path validation, resource limits, isolated output, and fresh-only writes. Never execute recovered code. Inputs and outputs can contain confidential data and require separate review before distribution.

### P0 — Before considering a public release

| ID | Status | Task | Definition of done |
|---|---|---|---|
| P0-01 | **Implemented; verify** | Enforce repository/input/output separation | Initial commit contains only product source, synthetic tests, docs and empty ignored input directory; input archives and generated outputs remain untracked |
| P0-02 | **Implemented; verify** | Preserve recovered file contents and paths | Test known fixture contents, case-sensitive names, and parser-defined delimiters; no automatic alteration of retained paths or contents |
| P0-03 | **Implemented; verify** | Validate duplicate paths and file-vs-parent-directory conflicts | `p` and `p/x` rejected in either order before writes; case-insensitive collisions rejected on all platforms |
| P0-04 | **Implemented; verify** | Refuse existing extraction destinations | No `--overwrite` or recursive delete of existing output trees; existing final target rejected |
| P0-05 | **Implemented; audit needed** | Stage writes and clean up failures | Failed writes clean up new staging directory; complete outputs moved into new destinations only; audit atomic commit and races |
| P0-06 | **Done** | Create maintainer-owned GitHub repository **`darizae/repomix-static-reconstructor`** as private and synchronize initial `main` | Run `bash scripts/bootstrap_private_github.sh` after reviewing `docs/AGENT_HANDOFF.md`; verify `isPrivate: true`, correct owner/remote and matching local/remote SHA. Stop if the repo already exists or authentication differs; never create public. **Evidence (2026-11-19):** created private repo, 13 approved files, commit `a03b7e8`, local and remote `main` match, 16 unit tests pass |
| P0-07 | **Blocked** | Confirm rights, provenance and license selection | Confirm ownership and no employer/confidential code retained, choose explicit OSS license, add LICENSE before public release |
| P0-08 | **To do** | Independent privacy/history/secret audit before any public switch | Inspect every tracked file and entire history, use local secret scanners, review names/emails/assets/URLs; document approvals; avoid accidental tracked inputs |
| P0-09 | **To do** | Filesystem threat model and independent review | Audit symlink and hardlink races, TOCTOU, temporary directory permissions, ancestor symlinks, Windows path rules and rename semantics; adversarial tests pass |
| P0-10 | **To do** | Repomix parser fidelity using actual generated fixtures | Test Markdown/XML/JSON from supported Repomix versions; XML entity escapes, line endings, BOM, malformed data, inline fences, ambiguous entries; document lossy cases |
| P0-11 | **To do** | Strengthen adversarial and cross-platform tests | Run on Linux/macOS/Windows; property/fuzz tests, permission failures, partial-write injection, limits, symlink trees, huge inputs and invalid UTF-8 |
| P0-12 | **To do** | Decide exclusion policy and publish clear semantics | Safety-based skipped `.mcp.json`, `.env*`, agent/IDE folders defined and tested; scope justified; optional `--strict` policy ONLY if preserves safety invariants |
| P0-13 | **To do** | Packaging plan and distributable CLI | `pyproject.toml`, `src/` package, stable import APIs/entrypoint, `--version`, wheel/sdist, clean install/uninstall, tested command across platforms |
| P0-14 | **To do** | CI and automated release checks | Unit/test matrix Python and OS; lint/format/type checks; build + wheel smoke test; least-privilege workflows and artifact inspection |
| P0-15 | **To do** | Portable Agent Skill validation | Validate frontmatter/body using official Agent Skills validator; installed-context commands and no-execute contract verified |
| P0-16 | **To do** | Docs, security and reporting ready for outsiders | Installation, FAQ, accurate threat model, reporting channel, support policy, no misleading guarantee, contribution instructions |
| P0-17 | **To do** | Complete `v0.1.0` public-release gates | Every required `docs/RELEASE_CHECKLIST.md` item reviewed, branch protection and license added, versioned release and maintainer approval before changing visibility |
| P0-18 | **Implemented; verify** | Self-contained agent handoff and release planning | `docs/BACKLOG.md`, `docs/AGENT_HANDOFF.md`, `docs/RELEASE_CHECKLIST.md`, root `AGENTS.md` and private bootstrap script included in the same ZIP; no separate downloaded document needed |

### P1 — Quality and product differentiation

| ID | Status | Task | Definition of done |
|---|---|---|---|
| P1-01 | To do | Product naming and positioning | Choose memorable name/repo slug/PyPI name and tagline; compare reverse-Repomix projects and clearly explain static-only/no-execution benefits |
| P1-02 | To do | Brand identity | Professional original logo/icon, SVG master, PNG export, favicon, light/dark assets, accessible palette, typography and usage guidelines; respect Repomix trademark |
| P1-03 | To do | Modern README presentation | Hero/logo/banner, feature highlights, quick install, CLI demo/GIF, security/limitations section, comparison table, badges once CI is real |
| P1-04 | To do | Documentation site and social cards | Polished responsive landing page/docs, copy-paste examples, architecture and safety diagram, Open Graph preview image, mobile accessibility checks |
| P1-05 | To do | CLI ergonomics and JSON manifest | Stable exit codes, `--help`, `--version`, progress summary, path/size diagnostics, machine-readable report with hashes and excluded counts |
| P1-06 | To do | More formats | Repomix plain-text export and line-numbered Markdown as explicit documented options with test fixtures; do not silently corrupt content |
| P1-07 | To do | Robust batch workflow | Dry-run entire batch before writing any outputs, collision-resistant folder names, safe report output/rollback behavior, tests for failures midway |
| P1-08 | To do | Agent host smoke tests | Test Claude Code, OpenAI Codex, Cursor, Gemini CLI, and OpenCode; document exact setup/versions and incompatibilities |
| P1-09 | To do | Build/release supply-chain hygiene | Automated dependency updates, secret scanning, artifact checksums, trusted publisher/PyPI identity, provenance and signatures where practical |
| P1-10 | To do | Contributor experience | CONTRIBUTING, CHANGELOG, issue/PR templates, coding standards, maintainers/ownership, good-first-issues, optional CODE_OF_CONDUCT |
| P1-11 | To do | Performance and memory budget | Memory/time benchmarks for large exports, streaming possibilities, no catastrophic regex, explicit limits |
| P1-12 | To do | No-execution verification | Document threat boundary and add static checks verifying no subprocess/network imports or recovered-code execution in core paths |

### P2 — After a stable release

| ID | Status | Task | Definition of done |
|---|---|---|---|
| P2-01 | To do | Agent-specific adapters and marketplace packaging | Claude plugin/Codex/Cursor/Gemini wrapper *only* where portable skill can't cover it; one canonical source of instructions |
| P2-02 | To do | Optional local pre-publication scanner integration | Separate optional secret scan command/guide that reports risks but **never edits** recovered files or makes a secrecy guarantee |
| P2-03 | To do | Benchmarks and compatibility matrix | Compare correctness, performance, exclusion semantics, handling of malicious paths vs existing open-source unpackers |
| P2-04 | To do | Release channels | Publish PyPI and Agent Skills directories/registries after review; version links and checksums |
| P2-05 | To do | Community polish | Demo recordings, roadmap, discussions, changelog automation and contribution triage |

## Execution sequence

1. **Private repository only:** follow `docs/AGENT_HANDOFF.md` and run `scripts/bootstrap_private_github.sh` against the verified GitHub owner `darizae`. Verify visibility, remote and tracked contents; never commit input exports or generated output trees.
2. **Safety and fidelity:** resolve P0-09 through P0-12; tests first, then revise claims and documentation.
3. **Packaging and validation:** P0-13 through P0-16, install in clean venv and run supported-host smoke tests.
4. **Modern identity:** P1-01 through P1-04; choose brand before producing icons, assets, and distribution names.
5. **Release decision:** after ownership/legal and checklist are complete, explicitly approve publication and tag a version. Keep private until then.

## Agent task protocol (for future “tackle this task” prompts)

- Always read root `AGENTS.md` and this backlog, then work on the specified task ID; otherwise choose the next highest-priority unblocked P0 only if the maintainer authorizes autonomous selection.
- Use a scoped branch/PR after remote setup. Link changes to the backlog ID in commit/PR descriptions. Avoid attempting unrelated tasks implicitly.
- Update this file's status and evidence and `docs/RELEASE_CHECKLIST.md` when gates are truly satisfied. Include tests run, limitations, and remaining blockers.
- If a task requires external permissions, interactive authentication, licensing/ownership judgment, publication, purchasing, or visibility changes, stop at the boundary and report the blocker rather than improvising.
- Use statuses `To do`, `In progress`, `Blocked`, and `Done` with evidence; “Implemented; verify” means functionality exists but independent release verification remains outstanding.

Suggested issue labels: `priority:P0`, `priority:P1`, `priority:P2`, `area:security`, `area:parser`, `area:cli`, `area:agent-skill`, `area:branding`, `area:docs`, `area:release`, `blocked`, `good-first-issue`.
