# FAQ

## Is reconstructed output safe to run?

No. The reconstruction is a **static, offline copy** of what Repomix exported.
It is for reading and searching only. Never build, test, install, or run the
recovered project — see [`STATIC_INSPECTION.md`](STATIC_INSPECTION.md) for why
and for the recommended inspection environment.

## Is reconstructed output safe to publish or share?

No, not automatically. Retained file contents are byte-identical to the
parsed export; if the source repo contained credentials, private URLs, or
confidential text, they are still there. The exclusion policy
([`EXCLUSIONS.md`](EXCLUSIONS.md)) omits a small set of high-risk paths from
the *output*, but it is not a secret scanner. Review inputs and outputs
separately before sharing either.

## What formats are supported?

Repomix Markdown, XML (default and `--parsable-style`), and JSON exports,
verified against Repomix 1.17.0–1.19.0 fixtures. Line-numbered exports are
rejected as lossy; plain-text, split, and compressed exports are unsupported.
Details and known fidelity limits: [`PARSER_COMPATIBILITY.md`](PARSER_COMPATIBILITY.md).

## Why are some files missing from the output?

A small, documented set of auto-activating configuration and credential files
is intentionally excluded (`.mcp.json`, `.env`/`.env.*` except plain
templates, `.envrc`, agent/IDE directories, `.git/`, `.DS_Store`). The CLI
reports every skipped path with its category. The original export still
contains them; exclusions affect only the reconstructed tree.

## Why can't I extract into an existing directory?

Safety invariant: the tool never overwrites or merges. Output directories
must be new. To re-extract, pick a new directory; delete an old one only
after verifying its contents.

## Does the tool need network access?

No. The extractor is standard-library-only, makes no network calls, and runs
no external commands. Install it with `pip install .` from a checkout; there
is no runtime dependency on PyPI. (Publishing to PyPI is not yet approved.)

## Does the tool recover Git history, binary files, or deleted files?

No. Repomix exports text snapshots; anything Repomix trimmed, BOM-stripped,
whitespace-trimmed, or omitted (binaries, ignored files, history) is
irrecoverably absent from the input. See
[`PARSER_COMPATIBILITY.md`](PARSER_COMPATIBILITY.md) for documented lossy cases.

## Which Python versions are supported?

Python 3.10+ (tested 3.10–3.13 on Linux, macOS, and Windows in CI).

## How do I report a security problem?

See [`SECURITY.md`](SECURITY.md) for the reporting channel and what to
include. Do not open public issues with exploitable details.

## How is this different from just unzipping or reverse-engineering a repo?

It restores a *tree of files from a Repomix export* with path validation,
resource limits, and no code execution — nothing more. It is not a Git
recovery tool and makes no claim about repository completeness.
