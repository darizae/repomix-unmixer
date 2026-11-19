# Security policy (pre-release)

This software reconstructs **untrusted text**. **It is not a sandbox**, a malware scanner, a secret detector, or a release-ready tool for safely publishing proprietary code. Use only local output directories not writable by other users/processes; run under an unprivileged account.

## Current safeguards

- Offline and extraction-only: no network calls, shell, recovered-code execution, dependency resolution or container startup.
- Path validation rejects absolute, `..`, empty, Windows drive/UNC/ADS and Windows reserved device-name components.
- Preflight rejects duplicates, case-insensitive output collisions and file-versus-directory conflicts; applies file count and byte limits.
- A small, documented file *exclusion* policy omits auto-activating agent/IDE configuration (`.mcp.json`, `.claude/`, `.codex/`, `.cursor/`, `.gemini/`, `.opencode/`, `.idea/`, `.vscode/`), credential-bearing environment files (`.env` and `.env.*` except plain templates, `.envrc`), `.git/`, and `.DS_Store` from reconstructed output. Exact rules, matching semantics, and explicit non-exclusions are in [`docs/EXCLUSIONS.md`](docs/EXCLUSIONS.md). This list is not comprehensive; never rely on it to remove secrets.
- Fresh-output-only workflow, exclusive file creation, no recursive replacement of existing target trees. Staged writes reduce partial outputs when extraction fails.

## Important unfinished security work

No completed independent adversarial security review. Directory traversal through concurrent filesystem mutation, symlink races, `rename` behavior on different platforms, hardlinks, permission inheritance, and file types need comprehensive testing. Parser fidelity is verified for Repomix 1.17.0–1.19.0 in [`docs/PARSER_COMPATIBILITY.md`](docs/PARSER_COMPATIBILITY.md), but default Repomix XML is not well-formed and remains ambiguous for some content; use `--parsable-style` for untrusted or special-character-heavy exports. Do not describe this project as hardened, formally audited, confidential, or safe to execute.

## Output and privacy

File contents and paths are intentionally unchanged except for handling Repomix encoding, delimiters and skipped files. They may contain credentials or private IPs. File exclusions affect only reconstructed output and do not establish whether retained files are confidential; the original export still contains excluded paths. See [`docs/EXCLUSIONS.md`](docs/EXCLUSIONS.md) for the exact policy and explicit non-exclusions. `repomix-files/` and `reconstructed/` are ignored by Git, but `.gitignore` does not remove already-tracked files. Before any private push, stage only expected files and inspect the staged diff; before a public release, perform a full history, secrets, and ownership review.

Please use the eventual repository's private security-reporting mechanism when configured; until then report findings privately to the maintainer. The public contact address is not yet selected.
