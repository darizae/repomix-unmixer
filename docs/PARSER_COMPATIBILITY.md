# Repomix parser compatibility and fidelity

This document defines what the reconstructor accepts, what it rejects, and which information
cannot be recovered. It complements the security model in [`../SECURITY.md`](../SECURITY.md) and
the task tracking in [`BACKLOG.md`](BACKLOG.md) (P0-10).

## Verified Repomix versions

- Fixtures were generated with **Repomix 1.19.0**.
- The same synthetic sample produced **byte-identical** Markdown, XML, and JSON output with
  **1.17.0** and **1.18.1**. The fixture set in
  [`tests/fixtures/repomix-1.19.0/`](../tests/fixtures/repomix-1.19.0/) therefore covers the
  verified range **1.17.0 through 1.19.0**.
- Earlier versions and future versions are untested. Re-run
  [`tests/fixtures/generate.sh`](../tests/fixtures/generate.sh) and the test suite before
  claiming support for another version.

## Fidelity contract

For every entry Repomix emits, the reconstructor writes the **exact parsed path and text**,
subject only to the safety path checks and the exclusion list described in `README.md` and
`SECURITY.md`. It does not reformat, re-indent, normalize line endings, or decode content that
Repomix left encoded.

This contract cannot restore information that Repomix itself removes:

- Repomix trims leading and trailing whitespace from each file's content. A file's final
  newline, leading blank lines, and first-line indentation are typically absent from the export.
- Repomix strips a UTF-8 BOM at the start of a packed file.
- Binary files, ignored files, `.gitignore` matches, and files excluded by Repomix configuration
  are not present.
- Git history, commits, diffs, and logs are not reconstructed.
- Repomix options that transform content (`--compress`, `--remove-comments`,
  `--remove-empty-lines`, `--truncate-base64`) produce transformed text. The reconstructor
  writes that text as-is and cannot recover the original.

## Supported formats

### Markdown

- Default and `--parsable-style` Markdown.
- File entries are recognized by a line-start `## File: <path>` header followed by a backtick
  fence. The opening fence may carry a language tag; the closing fence must use the same
  backtick run.
- Repomix chooses a fence longer than any backtick run in the file content. Fixtures cover
  content with 3, 4, 5, 6, and 10 backticks.
- A `## File:` line inside file content is preserved because content is consumed until its
  closing fence.

### XML

- Default XML and `--parsable-style` XML.
- Default XML is **not well-formed XML**. Repomix delimits entries with
  `<file path="...">\ncontent\n</file>` and does not escape `&`, `<`, `>`, or `"`.
- `--parsable-style` wraps the document in `<repomix>`, puts content directly between tags, and
  escapes `&`, `<`, `>`, `"`, and `'`. The reconstructor decodes exactly those five entities
  once, so literal text such as `&lt;` round-trips as `&lt;`, not `<`.
- Default XML cannot represent a path containing a double quote or file content containing a
  literal `</file>`. Detectable cases are rejected with a message recommending
  `--parsable-style`; a complete fake `<file path="...">...</file>` block inside default-style
  content remains inherently ambiguous, so use `--parsable-style` for untrusted or
  special-character-heavy inputs.

### JSON

- Current Repomix JSON with a `files` object mapping path to content.
- Legacy `files` arrays of `{"path": ..., "content": ...}` objects.
- Duplicate JSON keys are rejected rather than silently collapsed.

### Format detection

The first structural marker wins:

- a leading `{` selects JSON;
- the earliest of a line-start `## File:` header, `<repomix>`, `<file_summary>`,
  `<directory_structure>`, or `<files>` selects Markdown or XML.

This prevents XML file content containing `## File:` from being mistaken for Markdown, and
Markdown file content containing `<repomix>` from being mistaken for XML.

## Encoding and line endings

- Input must be valid UTF-8. A UTF-8 BOM at the start of the export is accepted and ignored.
- Content line endings are preserved exactly as Repomix emitted them. CRLF inside file content
  survives all three formats; CRLF structural line endings in the export are also accepted.
- A file whose content ends in a bare CR is ambiguous in Markdown and default XML because the
  structural newline before the closing delimiter is removed as a unit with it. Prefer JSON or
  `--parsable-style` XML for such content.

## Rejected and unsupported inputs

| Input | Behavior |
|---|---|
| `--output-show-line-numbers` | **Rejected.** Line-number prefixes are annotations, not file content. Detected from the export preamble and from per-file prefix patterns, including when `--no-file-summary` removes the preamble marker. |
| Plain-text style (`--style plain`) | **Unsupported.** Format detection fails with an error. |
| `--no-files` / no file entries | **Rejected** with "no file entries" rather than producing an empty tree. |
| `--split-output` | Each numbered part is a partial export. Parsing one part reconstructs only the files in that part; combine parts only after verifying completeness. |
| `--output-file-path-style cwd-relative` | Paths containing `..` or escaping the output root are rejected by path validation. |
| Malformed Markdown/XML/JSON | **Rejected** with a format-specific error; no output is written. |
| Default XML with unrepresentable path/content | **Rejected** when detectable; see the XML section. |
| Markdown header-like line in the generated preamble | Repomix's preamble does not produce a line-start `## File:` header, but a hand-edited export could. Such a line is interpreted as an entry. |
| Compressed / comment-stripped / truncated exports | Accepted as emitted; original content is unrecoverable. |

## Exclusions are not a confidentiality guarantee

The parser preserves what Repomix emits, but the writer then omits a small safety-based set of
agent, IDE, and credential configuration paths. Those paths are listed in `README.md`,
`SECURITY.md`, and `scripts/unmix_repomix.py`. Exclusions affect only reconstructed output; the
original export still contains the excluded data and neither artifact is automatically safe to
publish.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

The fixture tests assert that Markdown, parsable Markdown, default XML, parsable XML, and JSON
reconstruct the same 12-file tree byte-for-byte, and cover BOM input, CRLF content, empty files,
missing final newlines, inline fences, XML entities, special-character paths, malformed input,
and line-numbered rejection.
