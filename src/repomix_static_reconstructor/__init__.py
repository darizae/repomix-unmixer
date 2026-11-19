"""Static reconstruction of files from Repomix exports.

Reconstruct repository-shaped, static files from Repomix Markdown, XML, or
JSON exports for offline inspection only. This package never executes
recovered code, never contacts the network, and never rewrites retained
paths or contents.
"""

from __future__ import annotations

from repomix_static_reconstructor.extractor import (
    DEFAULT_MAX_FILE_MIB,
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_INPUT_MIB,
    DEFAULT_MAX_TOTAL_MIB,
    PreparedEntry,
    ParsedEntry,
    UnmixError,
    UnmixResult,
    detect_format,
    exclusion_category,
    mib_to_bytes,
    normalize_archive_path,
    parse_json,
    parse_markdown,
    parse_repomix,
    parse_xml,
    preflight_entries,
    unmix_repomix,
)

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_MAX_FILE_MIB",
    "DEFAULT_MAX_FILES",
    "DEFAULT_MAX_INPUT_MIB",
    "DEFAULT_MAX_TOTAL_MIB",
    "ParsedEntry",
    "PreparedEntry",
    "UnmixError",
    "UnmixResult",
    "__version__",
    "detect_format",
    "exclusion_category",
    "mib_to_bytes",
    "normalize_archive_path",
    "parse_json",
    "parse_markdown",
    "parse_repomix",
    "parse_xml",
    "preflight_entries",
    "unmix_repomix",
]
