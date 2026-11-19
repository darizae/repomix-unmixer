# repomix-unmixer — product identity

**Name:** repomix-unmixer  
**Tagline:** Unpack Repomix exports for static, offline inspection.

## Positioning

An independent, local Python tool that reconstructs supported Repomix Markdown, XML, and JSON exports into an inspectable file tree. It does not execute recovered code and refuses unsafe output paths or existing destinations.

For developers, maintainers, and coding-agent workflows that need individual text files instead of a packed export.

**Core user journey:** export with Repomix → preview with `--dry-run` → reconstruct into a new folder → inspect the files as untrusted text.

**Differentiators:** fresh-output-only staged extraction, portable path validation, collision and resource limits, documented file exclusions, batch conversion, and a portable Agent Skill. These are preventive measures, **not** a sandbox, vulnerability audit, or secrecy guarantee.

## Naming and compatibility

- Product/display name: **repomix-unmixer**.
- GitHub repository: `darizae/repomix-unmixer`.
- Python distribution and import path: `repomix_unmixer`.
- CLI commands: `unmix-repomix` and `reconstruct-all`.
- The project is independent of [Repomix](https://repomix.com/); it is not an official Repomix component.

## Landscape

The name `repomix-unmixer` is also used by an existing [agent skill](https://github.com/daymade/claude-code-skills/tree/main/repomix-unmixer); [repomix-unpack](https://github.com/jurijat/repomix-unpack) is another extraction CLI. We should **not** imply exclusivity or claim to be the only reverse-Repomix tool. Our documented focus is local, static-only inspection with conservative filesystem controls.

**Before publication:** review naming confusion, the Repomix trademark, GitHub/PyPI naming availability, and any rights/licensing questions. No trademark clearance or exclusivity is claimed.

## Visual direction

- Independent geometric mark: a packed document expanding into a three-file tree.
- Palette: midnight `#0B1220`, soft white `#F8FAFC`, iris `#8EA6FF`, mint `#65E5C8`.
- Readable system-font typography; accessible contrast; equivalent light and dark layouts.
- Product language: clear, restrained, concrete. Never call extracted code "safe to run" or "safe to publish".

See [README](../README.md), [Security](../SECURITY.md), and [Release checklist](RELEASE_CHECKLIST.md).
