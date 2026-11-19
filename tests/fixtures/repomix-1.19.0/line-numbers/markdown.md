This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where line numbers have been added.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Line numbers have been added to the beginning of each line

# Directory Structure
`````
docs/
  ambiguous.md
src/
  deep/
    nested/
      file.txt
  app.py
  bom.txt
  crlf.txt
  empty.txt
  fences.md
  no-newline.txt
  special.txt
  unicode.txt
  with space.txt
README.md
`````

# Files

## File: docs/ambiguous.md
`````markdown
1: ## File: not-a-real-entry.txt
2: ```text
3: This line mimics a Repomix header and must stay inside the file.
4: ```
`````

## File: src/deep/nested/file.txt
`````
1: deep content
`````

## File: src/app.py
`````python
1: def add(a, b):
2:     return a + b
`````

## File: src/bom.txt
`````
1: BOM-prefixed line
`````

## File: src/crlf.txt
`````
1: line one
2: line two
`````

## File: src/empty.txt
`````
1: 
`````

## File: src/fences.md
`````markdown
 1: Before fence.
 2: 
 3: ```python
 4: print("inner fence")
 5: ```
 6: 
 7: ````
 8: nested four-backtick example
 9: ````
10: 
11: After fence.
`````

## File: src/no-newline.txt
`````
1: no trailing newline
`````

## File: src/special.txt
`````
1: ampersand & less < greater > quote " apostrophe '
`````

## File: src/unicode.txt
`````
1: unicode: café ☕ 日本語
`````

## File: src/with space.txt
`````
1: space in path
`````

## File: README.md
`````markdown
1: # Fixture README
2: 
3: Synthetic repository used to validate Repomix reconstruction.
`````
