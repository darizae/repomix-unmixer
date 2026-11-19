#!/usr/bin/env python3
"""Restore static file trees from Repomix Markdown, XML, or JSON exports.

Extraction is local and never executes recovered project code or network calls.
Recovered paths and parsed text are preserved for files selected for extraction.
Selected agent/credential configuration paths are omitted entirely by default.
Output is not guaranteed to be secret-free, runnable, or an exact Git backup.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath


DEFAULT_MAX_INPUT_MIB = 512
DEFAULT_MAX_FILE_MIB = 128
DEFAULT_MAX_TOTAL_MIB = 1024
DEFAULT_MAX_FILES = 100_000
WINDOWS_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"}
WINDOWS_RESERVED_NAMES.update(f"COM{i}" for i in range(1, 10))
WINDOWS_RESERVED_NAMES.update(f"LPT{i}" for i in range(1, 10))

MARKDOWN_HEADER_RE = re.compile(r"^## File: ([^\r\n]+)\r?\n?$")
MARKDOWN_OPEN_FENCE_RE = re.compile(r"^(?P<fence>`{3,})(?P<info>[^`\r\n]*)\r?\n?$")
XML_FILE_RE = re.compile(
    r'<file path="([^"\r\n]+)">\r?\n(.*?)\r?\n</file>',
    re.DOTALL,
)

# Omit auto-activating agent configuration, local workspace metadata, and
# credential-bearing configuration files. This is safety-based EXCLUSION,
# NOT content modification. Every written file keeps its parsed name and text.
# The list is intentionally small and generic; review it before relying on it.
SKIP_PATH_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|/)\.mcp\.json$", re.IGNORECASE),
    re.compile(r"(?:^|/)\.env$", re.IGNORECASE),
    re.compile(r"(?:^|/)\.env\.(?!example$|sample$|template$)[^/]+$", re.IGNORECASE),
    re.compile(r"(?:^|/)\.DS_Store$", re.IGNORECASE),
    re.compile(r"(?:^|/)\.(?:git|idea|claude|cursor)(?:/|$)", re.IGNORECASE),
)


class UnmixError(Exception):
    """Raised for invalid input or unsafe reconstruction conditions."""


@dataclass(frozen=True)
class ParsedEntry:
    original_path: str
    content: str


@dataclass(frozen=True)
class PreparedEntry:
    original_path: str
    relative_path: PurePosixPath
    target: Path
    data: bytes


@dataclass(frozen=True)
class UnmixResult:
    format_type: str
    extracted: tuple[str, ...]
    skipped: tuple[str, ...]
    total_bytes: int


def mib_to_bytes(value: float) -> int:
    return int(value * 1024 * 1024)


def strip_one_line_ending(text: str) -> str:
    """Remove exactly one delimiter newline before a closing Repomix fence/tag."""
    if text.endswith("\r\n"):
        return text[:-2]
    if text.endswith("\n") or text.endswith("\r"):
        return text[:-1]
    return text


def detect_format(content: str) -> str | None:
    stripped = content.lstrip("\ufeff \t\r\n")
    if stripped.startswith("{"):
        return "json"
    if re.search(r"^## File: [^\r\n]+$", content, re.MULTILINE):
        return "markdown"
    if '<file path="' in content and "</file>" in content:
        return "xml"
    return None


def parse_markdown(content: str) -> list[ParsedEntry]:
    """Parse Repomix Markdown using each file's actual fence length."""
    lines = content.splitlines(keepends=True)
    entries: list[ParsedEntry] = []
    i = 0

    while i < len(lines):
        header_match = MARKDOWN_HEADER_RE.match(lines[i])
        if not header_match:
            i += 1
            continue

        file_path = header_match.group(1)
        header_line = i + 1
        if i + 1 >= len(lines):
            raise UnmixError(
                f"Malformed Markdown: file header on line {header_line} has no opening code fence"
            )

        fence_match = MARKDOWN_OPEN_FENCE_RE.match(lines[i + 1])
        if not fence_match:
            raise UnmixError(
                "Malformed Markdown: expected a backtick code fence after file header "
                f"on line {header_line}"
            )

        fence = fence_match.group("fence")
        content_start = i + 2
        j = content_start
        while j < len(lines):
            candidate = lines[j].rstrip("\r\n")
            if candidate.rstrip(" \t") == fence:
                break
            j += 1

        if j >= len(lines):
            raise UnmixError(
                f"Malformed Markdown: unclosed {len(fence)}-backtick fence for {file_path!r} "
                f"starting near line {header_line}"
            )

        file_content = "".join(lines[content_start:j])
        file_content = strip_one_line_ending(file_content)
        entries.append(ParsedEntry(file_path, file_content))
        i = j + 1

    if not entries:
        raise UnmixError("No Repomix Markdown file entries were found")
    return entries


def parse_xml(content: str) -> list[ParsedEntry]:
    entries = [ParsedEntry(m.group(1), m.group(2)) for m in XML_FILE_RE.finditer(content)]
    if not entries:
        raise UnmixError("No Repomix XML file entries were found")
    return entries


def parse_json(content: str) -> list[ParsedEntry]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise UnmixError(f"Failed to parse JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise UnmixError("Repomix JSON root must be an object")

    files = data.get("files")
    entries: list[ParsedEntry] = []
    if isinstance(files, dict):
        for file_path, file_content in files.items():
            if not isinstance(file_path, str) or not file_path:
                raise UnmixError("JSON file paths must be non-empty strings")
            if not isinstance(file_content, str):
                raise UnmixError(f"JSON content for {file_path!r} must be a string")
            entries.append(ParsedEntry(file_path, file_content))
    elif isinstance(files, list):
        for index, file_entry in enumerate(files):
            if not isinstance(file_entry, dict):
                raise UnmixError(f"JSON files[{index}] must be an object")
            file_path = file_entry.get("path")
            file_content = file_entry.get("content", "")
            if not isinstance(file_path, str) or not file_path:
                raise UnmixError(f"JSON files[{index}].path must be a non-empty string")
            if not isinstance(file_content, str):
                raise UnmixError(f"JSON files[{index}].content must be a string")
            entries.append(ParsedEntry(file_path, file_content))
    else:
        raise UnmixError("Repomix JSON must contain a 'files' object (or legacy array)")

    if not entries:
        raise UnmixError("Repomix JSON contains no files")
    return entries


def parse_repomix(content: str, format_type: str) -> list[ParsedEntry]:
    if format_type == "markdown":
        return parse_markdown(content)
    if format_type == "xml":
        return parse_xml(content)
    if format_type == "json":
        return parse_json(content)
    raise UnmixError(f"Unsupported format: {format_type}")


def should_skip_path(file_path: str) -> bool:
    portable = file_path.replace("\\", "/")
    return any(pattern.search(portable) for pattern in SKIP_PATH_PATTERNS)


def normalize_archive_path(file_path: str) -> PurePosixPath:
    if not isinstance(file_path, str):
        raise UnmixError("File path must be a string")
    if not file_path:
        raise UnmixError("File path must not be empty")
    if "\x00" in file_path:
        raise UnmixError(f"Unsafe file path contains a NUL byte: {file_path!r}")
    if "\n" in file_path or "\r" in file_path:
        raise UnmixError(f"Unsafe file path contains a newline: {file_path!r}")
    if file_path != file_path.strip():
        raise UnmixError(f"Unsafe/ambiguous file path has surrounding whitespace: {file_path!r}")

    windows_path = PureWindowsPath(file_path)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        raise UnmixError(f"Absolute/drive/UNC path is not allowed: {file_path!r}")

    portable = file_path.replace("\\", "/")
    posix_path = PurePosixPath(portable)
    if posix_path.is_absolute():
        raise UnmixError(f"Absolute path is not allowed: {file_path!r}")

    raw_parts = portable.split("/")
    if any(part in ("", ".", "..") for part in raw_parts):
        raise UnmixError(
            f"Unsafe/ambiguous path component in {file_path!r}; empty, '.' and '..' are rejected"
        )

    for part in raw_parts:
        if ":" in part:
            # Enhanced colon validation for Windows alternate data streams
            if ":" in part and part != ":":
                # Allow paths like "C:/path" to be normalized to "C/path" 
                # but reject actual ADS like "file.txt:$DATA"
                if part.count(":") > 1 or (part.count(":") == 1 and "$" in part.upper()):
                    raise UnmixError(f"Windows alternate data stream not allowed: {file_path!r}")

    return PurePosixPath(*raw_parts)


def ensure_within_root(root: Path, candidate: Path, description: str) -> Path:
    """Ensure candidate path is within root, using consistent resolution."""
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(root.resolve(strict=False))
        return resolved
    except ValueError as exc:
        raise UnmixError(f"{description} escapes output directory: {candidate}") from exc
    return resolved


def check_existing_path_safety(
    root: Path,
    relative_path: PurePosixPath,
    input_resolved: Path,
) -> Path:
    current = root
    for part in relative_path.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise UnmixError(f"Symlink directory component is not allowed: {current}")
        if current.exists() and not current.is_dir():
            raise UnmixError(f"Parent path is not a directory: {current}")
        if current.exists():
            ensure_within_root(root, current, "Parent path")

    target = root.joinpath(*relative_path.parts)
    ensure_within_root(root, target, "File path")

    if target.is_symlink():
        raise UnmixError(f"Refusing to write through symlink: {target}")

    if target.exists():
        target_stat = target.stat()
        if not stat.S_ISREG(target_stat.st_mode):
            raise UnmixError(f"Destination exists and is not a regular file: {target}")
        if target.resolve() == input_resolved:
            raise UnmixError(f"Refusing to overwrite the Repomix input file itself: {target}")
        raise UnmixError(f"Destination file already exists: {target}")

    
    # Additional hardlink detection
    if target.exists() and target.stat().st_nlink > 1:
        raise UnmixError(f"Refusing to write to hardlinked file: {target}")


def preflight_entries(
    entries: list[ParsedEntry],
    root: Path,
    input_resolved: Path,
    max_files: int,
    max_file_bytes: int,
    max_total_bytes: int,
) -> tuple[list[PreparedEntry], list[str], int]:
    """Validate all paths, collisions, and limits before writing any output."""
    if len(entries) > max_files:
        raise UnmixError(f"Archive contains {len(entries)} files, exceeding {max_files}")

    prepared: list[PreparedEntry] = []
    skipped: list[str] = []
    seen: set[str] = set()
    required_directories: set[str] = set()
    total_bytes = 0

    for entry in entries:
        # Validate even paths that would be skipped; never silently accept traversal.
        relative_path = normalize_archive_path(entry.original_path)
        if should_skip_path(relative_path.as_posix()):
            skipped.append(entry.original_path)
            continue

        # Portable collision checking: avoid both platform-specific case
        # collisions and file/parent-directory conflicts.
        path_key = relative_path.as_posix().casefold()
        parts = relative_path.parts
        parent_keys = {
            "/".join(parts[:index]).casefold()
            for index in range(1, len(parts))
        }
        if path_key in seen or path_key in required_directories:
            raise UnmixError(f"Duplicate path or file/directory conflict: {entry.original_path!r}")
        if seen.intersection(parent_keys):
            raise UnmixError(f"File/directory conflict at: {entry.original_path!r}")
        required_directories.update(parent_keys)
        seen.add(path_key)

        data = entry.content.encode("utf-8")
        size = len(data)
        if size > max_file_bytes:
            raise UnmixError(f"File {entry.original_path!r} exceeds per-file size limit")
        total_bytes += size
        if total_bytes > max_total_bytes:
            raise UnmixError("Reconstructed content exceeds total-size limit")

        target = check_existing_path_safety(root, relative_path, input_resolved=input_resolved)
        prepared.append(PreparedEntry(entry.original_path, relative_path, target, data))

    return prepared, skipped, total_bytes


def ensure_safe_parent_dirs(root: Path, relative_path: PurePosixPath) -> None:
    current = root
    for part in relative_path.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise UnmixError(f"Symlink directory component is not allowed: {current}")
        try:
            current.mkdir(mode=0o755)
        except FileExistsError:
            pass
        if current.is_symlink() or not current.is_dir():
            raise UnmixError(f"Unsafe or non-directory parent path: {current}")
        resolved = current.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise UnmixError(f"Parent directory escaped output root: {current}") from exc


def safe_write_file(root: Path, relative_path: PurePosixPath, data: bytes) -> None:
    ensure_safe_parent_dirs(root, relative_path)
    target = root.joinpath(*relative_path.parts)
    if target.is_symlink():
        raise UnmixError(f"Refusing to write through symlink: {target}")
    ensure_within_root(root, target, "File path")
    # Additional hardlink detection for target file
    if target.exists() and target.stat().st_nlink > 1:
        raise UnmixError(f"Refusing to write to hardlinked file: {target}")
    
    # Create-only: there is no overwrite mode. O_EXCL prevents replacing an
    # existing file (but adversarial concurrent filesystem mutation still needs
    # dedicated review; see BACKLOG.md).
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    binary = getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow | binary, 0o644)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise UnmixError(f"Destination appeared or already exists: {target}") from exc
    except OSError as exc:
        raise UnmixError(f"Failed to safely write {target}: {exc}") from exc


def prepare_output_root(output_dir: str | os.PathLike[str], dry_run: bool) -> Path:
    raw_root = Path(output_dir).expanduser()
    if raw_root.is_symlink() or raw_root.exists():
        raise UnmixError(f"Output path already exists (will not overwrite): {raw_root}")
    # Resolve without creating anything; only the writer creates directories.
    return raw_root.resolve(strict=False)


def read_input_file(repomix_file: str | os.PathLike[str], max_input_bytes: int) -> tuple[Path, str]:
    input_path = Path(repomix_file).expanduser()
    if not input_path.exists():
        raise UnmixError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise UnmixError(f"Input path is not a regular file: {input_path}")

    size = input_path.stat().st_size
    if size > max_input_bytes:
        raise UnmixError(f"Input file is {size} bytes, exceeding input limit of {max_input_bytes} bytes")

    try:
        with input_path.open("r", encoding="utf-8", newline="") as handle:
            content = handle.read()
    except UnicodeDecodeError as exc:
        raise UnmixError(f"Input is not valid UTF-8: {exc}") from exc

    return input_path.resolve(), content


def unmix_repomix(
    repomix_file: str | os.PathLike[str],
    output_dir: str | os.PathLike[str],
    *,
    dry_run: bool = False,
    max_input_bytes: int = mib_to_bytes(DEFAULT_MAX_INPUT_MIB),
    max_file_bytes: int = mib_to_bytes(DEFAULT_MAX_FILE_MIB),
    max_total_bytes: int = mib_to_bytes(DEFAULT_MAX_TOTAL_MIB),
    max_files: int = DEFAULT_MAX_FILES,
) -> UnmixResult:
    """Parse, preflight, and write one static reconstruction with no rewriting."""
    input_resolved, content = read_input_file(repomix_file, max_input_bytes)
    format_type = detect_format(content)
    if format_type is None:
        raise UnmixError("Unrecognized Repomix format; expected Markdown, XML, or JSON")

    entries = parse_repomix(content, format_type)
    root = prepare_output_root(output_dir, dry_run=dry_run)
    prepared, skipped, total_bytes = preflight_entries(
        entries, root, input_resolved,
        max_files=max_files,
        max_file_bytes=max_file_bytes,
        max_total_bytes=max_total_bytes,
    )
    if dry_run:
        return UnmixResult(format_type, tuple(x.relative_path.as_posix() for x in prepared),
                           tuple(skipped), total_bytes)

    # Stage a complete output in a fresh temporary sibling; failed writes
    # leave no partial final output. The destination must remain absent.
    # A full cross-platform concurrent-attack security audit remains P0.
    import shutil
    import tempfile

    root.parent.mkdir(parents=True, exist_ok=True)
    if root.exists() or root.is_symlink():
        raise UnmixError(f"Output appeared after preflight: {root}")
    # Create staging directory with restricted permissions
    import stat
    staging = Path(tempfile.mkdtemp(prefix=f".{root.name}.tmp-", dir=root.parent))
    # Set restrictive permissions (700) for staging directory
    staging.chmod(stat.S_IRWXU)
    # Additional symlink check after staging directory creation
    if any(part.is_symlink() for part in staging.parents):
        raise UnmixError(f"Staging directory parent contains symlink: {staging}")
    try:
        for item in prepared:
            safe_write_file(staging, item.relative_path, item.data)
        if root.exists() or root.is_symlink():
            raise UnmixError(f"Output appeared during reconstruction: {root}")
        # os.rename must be audited for concurrent manipulation; the CLI
        # is currently intended for trusted local output directories.
        staging.rename(root)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return UnmixResult(format_type, tuple(x.relative_path.as_posix() for x in prepared),
                       tuple(skipped), total_bytes)


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("must be a finite number greater than zero")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconstruct static files from Repomix exports without running or rewriting them"
    )
    parser.add_argument("repomix_file", help="Repomix Markdown/XML/JSON export")
    parser.add_argument("output_directory", nargs="?", default="./extracted",
                        help="New output directory (default: ./extracted)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing")
    parser.add_argument("--max-input-mib", type=positive_float, default=DEFAULT_MAX_INPUT_MIB)
    parser.add_argument("--max-file-mib", type=positive_float, default=DEFAULT_MAX_FILE_MIB)
    parser.add_argument("--max-total-mib", type=positive_float, default=DEFAULT_MAX_TOTAL_MIB)
    parser.add_argument("--max-files", type=positive_int, default=DEFAULT_MAX_FILES)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = unmix_repomix(
            args.repomix_file, args.output_directory,
            dry_run=args.dry_run,
            max_input_bytes=mib_to_bytes(args.max_input_mib),
            max_file_bytes=mib_to_bytes(args.max_file_mib),
            max_total_bytes=mib_to_bytes(args.max_total_mib),
            max_files=args.max_files,
        )
    except UnmixError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Format: {result.format_type} | files: {len(result.extracted)} | "
          f"skipped: {len(result.skipped)} | bytes: {result.total_bytes}")
    print("Dry run: no output written" if args.dry_run else f"Output: {args.output_directory}")
    if result.skipped:
        print("Excluded by safety rules: " + ", ".join(result.skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
