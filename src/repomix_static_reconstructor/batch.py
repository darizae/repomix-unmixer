#!/usr/bin/env python3
"""Reconstruct Repomix Markdown exports from ../repomix-files/.

This driver ONLY calls the local static Repomix extractor. It does not execute,
build, install, test, lint, containerize, or otherwise run reconstructed projects.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from repomix_static_reconstructor.extractor import (
    UnmixError,
    UnmixResult,
    unmix_repomix,
)


BUNDLE_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT_DIR = BUNDLE_ROOT / "repomix-files"
DEFAULT_OUTPUT_DIR = BUNDLE_ROOT / "reconstructed"


def output_name(stem: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-")
    return name or "repository"


def safe_output_name(path: Path) -> str:
    # Derive a filesystem-safe folder label from the input export's filename.
    # This is NOT a transformation of recovered repository names/content.
    return output_name(path.stem)


def discover_markdown_files(input_dir: Path) -> list[Path]:
    return sorted(
        p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".md"
    )


def write_report(
    output_root: Path, rows: list[tuple[Path, Path, UnmixResult]], dry_run: bool
) -> None:
    if dry_run:
        return
    report = output_root / "RECONSTRUCTION_REPORT.md"
    lines = [
        "# Static Repomix Reconstruction Report",
        "",
        "No reconstructed repository code was executed by this workflow.",
        "",
        "| Repomix input | Output | Files | Skipped |",
        "|---|---|---:|---:|",
    ]
    for index, (_, target, result) in enumerate(rows, start=1):
        lines.append(
            f"| `input-{index}.md` | `{target.name}/` | {len(result.extracted)} | "
            f"{len(result.skipped)} |"
        )
    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- These outputs are static example code only.",
            "- Do not run package managers, scripts, builds, tests, containers, CI, MCP, or applications inside them.",
            "- Paths and text are not rewritten; original sensitive content can remain.",
            "- Safety exclusions omitted agent/IDE configuration, credential-bearing environment files, .git/, and OS metadata. They affect only this output, not the original export.",
            "",
        ]
    )
    with report.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Statically reconstruct all Repomix .md files in repomix-files/."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_dir = args.input_dir.resolve()
    raw_output_root = args.output_dir.expanduser()
    if raw_output_root.is_symlink():
        print(
            f"Error: output root must not be a symlink: {raw_output_root}",
            file=sys.stderr,
        )
        return 1
    output_root = raw_output_root.resolve(strict=False)

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: input directory does not exist: {input_dir}", file=sys.stderr)
        return 1

    files = discover_markdown_files(input_dir)
    if not files:
        print(f"No .md files found in {input_dir}")
        return 0

    # No deletion or replacement of existing output trees.
    if output_root.is_symlink() or (output_root.exists() and not output_root.is_dir()):
        print(
            f"Error: output root is not a regular directory: {output_root}",
            file=sys.stderr,
        )
        return 1
    report = output_root / "RECONSTRUCTION_REPORT.md"
    if report.exists() or report.is_symlink():
        print(
            f"Error: reconstruction report already exists (will not replace): {report}",
            file=sys.stderr,
        )
        return 1
    if not args.dry_run:
        output_root.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[Path, Path, UnmixResult]] = []
    used_names: set[str] = set()

    for source in files:
        base_name = safe_output_name(source)
        name = base_name
        suffix = 2
        while name.casefold() in used_names:
            name = f"{base_name}-{suffix}"
            suffix += 1
        used_names.add(name.casefold())

        target = output_root / name
        print(f"\n=== {source.name} -> {target.name}/ ===")
        try:
            result = unmix_repomix(source, target, dry_run=args.dry_run)
        except UnmixError as exc:
            print(f"Error reconstructing {source.name}: {exc}", file=sys.stderr)
            return 1

        print(f"Files: {len(result.extracted)} | skipped: {len(result.skipped)}")
        rows.append((source, target, result))

    write_report(output_root, rows, args.dry_run)
    print(
        "\nDone. Reconstructed repositories are STATIC EXAMPLES ONLY; do not execute them."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
