# Security review — repomix-unmixer v0.1.0

This is a **self-review by the maintainer/local agent**, not an independent
external audit. It records the threat model, the cases actually exercised by
tests, and the residual risks that remain bounded or out of scope. It does not
claim the tool is hardened, formally audited, or safe to execute recovered
code.

Reference: [BACKLOG.md](BACKLOG.md) (P0-05, P0-09, P1-12), [SECURITY.md](../SECURITY.md),
[STATIC_INSPECTION.md](STATIC_INSPECTION.md).

## Threat model and assumptions

The extractor's job is to reconstruct **untrusted text** into a fresh local
directory for offline inspection. The supported environment is a
**trusted local output directory**: the directory where the output is created
is chosen and controlled by the operator, is not shared with other users or
untrusted processes, and the tool refuses to write into an existing tree.

Under that model the extractor must guarantee, against a hostile *export*:

1. **No traversal/escape** — a recovered path can never cause a file to be
   written outside the output root.
2. **No overwrite** — a recovered path can never replace, truncate, or corrupt
   an existing file (including the input export itself).
3. **No symlink/hardlink follow** — a symlink or hardlink present in or planted
   in the output tree is never written through.
4. **No execution** — parsing/reconstruction never spawns a shell, runs a
   subprocess, or opens a network connection.

A malicious process that can concurrently mutate the output directory (a
**hostile shared directory**) is **out of scope**: the tool is documented for
trusted-local use and does not claim atomicity or race resistance under an
attacker who can modify the destination at will. These cases are named as
residual risks below rather than hidden.

## What the code does

Path validation (`normalize_archive_path`) rejects absolute and drive/UNC
paths, `..`, `.`, empty and NUL/newline/whitespace-surrounded components,
Windows alternate-data-stream colons, Windows reserved device names, and
components that alias on Windows (trailing dots, surrounding whitespace).
Collision preflight rejects duplicate and case-insensitive collisions and
file-versus-directory conflicts across all platforms.

Writes are **create-only** (`os.open` with `O_CREAT|O_EXCL` and, where
available, `O_NOFOLLOW`): an existing or concurrently-appearing target is
refused, never overwritten. Output is staged in a fresh `0700` temporary
sibling directory; the destination must remain absent before and during the
build, and is moved into place only after every file is written. On any
failure the staging directory is removed. Parent directories are created and
re-validated for symlinks and root-escape after creation.

The package imports only the standard library and never invokes `subprocess`,
`os.system`, `socket`, `urllib`, `requests`, or dynamic `eval`/`exec`
(`tests/test_no_execution.py` enforces this statically).

## Cases exercised by tests (macOS, Python 3.12, local)

All checks below were run locally on macOS (arm64) with Python 3.12.7; see
`PASS`/`SKIP`/`DEFERRED` per item.

| Area | Scenario | Result |
|---|---|---|
| Traversal | `..`, absolute, drive/UNC, double slash, `.` components rejected even when the path would be excluded | PASS (`test_unsafe_paths_even_when_excluded`, `test_windows_and_absolute_paths`) |
| Aliasing | Case-insensitive collisions rejected in either order | PASS (`test_case_collisions_cross_platform`) |
| Aliasing | Windows reserved device names (`CON`, `NUL`, `COM1`, `LPT9`, …) rejected on all platforms | PASS (`test_windows_reserved_device_names_rejected`) |
| Aliasing | Trailing-dot and surrounding-whitespace components rejected | PASS (`test_windows_aliasing_trailing_dot_and_whitespace_rejected`) |
| Overwrite | Existing destination refused and left untouched | PASS (`test_existing_target_refused_untouched`) |
| Overwrite | Input export itself never overwritten | PASS (`check_existing_path_safety` target-vs-input check) |
| Overwrite | O_EXCL create-only refuses a file that appears after preflight | PASS (`test_toctou_injection_during_staging`) |
| Symlink | Symlinked output root rejected | PASS (`test_symlinked_target_rejected`) |
| Symlink | Symlinked parent components and nested chains rejected before write | PASS (`test_complex_symlink_tree_scenarios`, `test_deeply_nested_symlink_chains`) |
| Symlink | Write through an existing symlink target refused | PASS (`test_write_through_existing_symlink_target_refused`) |
| Hardlink | Hardlinked target refused as "already exists"; hardlinked parent rejected | PASS (`test_hardlink_attack_scenarios`) |
| Staging | Mid-write failure removes staging, leaves no final output | PASS (`test_staging_cleanup_on_mid_write_failure`) |
| Staging | Failure leaves no partial tree | PASS (`test_staged_write_atomicity`, `test_no_partially_committed_output_on_failure`) |
| Permissions | Write into a non-writable directory → clean `UnmixError` | PASS (`test_permission_denied_during_extraction`) |
| Permissions | `mkdir` failure on a parent → clean `UnmixError` | PASS (`test_permission_denied_parent_directory`) |
| Resource limits | `max_files`, `max_file_bytes`, `max_total_bytes`, `max_input_bytes` enforced at boundaries | PASS (`test_limits_preflight`, `test_file_count_boundary`, `test_huge_input_file_rejection`) |
| Dry run | `--dry-run` creates neither the output tree nor any staging directory | PASS (`test_dry_run_does_not_write`) |
| No execution | No subprocess/network/dynamic-execution imports or calls in package source | PASS (`test_no_execution.py`) |
| Fidelity | Parser fixtures byte-identical across Repomix 1.17.0–1.19.0 | PASS (`tests/test_parser_fidelity.py`) |

### Checks that were skipped or deferred

- **Windows and Linux runtime**: not run locally; only macOS. The
  cross-platform path rules are unit-tested but actual Windows reparse-point
  behavior and Linux permission semantics are **deferred** to CI when Actions
  quota is restored.
- **Official Agent Skills validator**: `skills-ref` was not installed for this
  review; validated in Phase C of the release plan.
- **Symlink-to-device write**: skipped on this host (`/dev/null` symlink case).

## Remediation applied in this review

- Enforced the documented Windows reserved device-name rejection (the constant
  existed but was unused) and added trailing-dot/whitespace aliasing rejection
  so the case-collision preflight cannot be bypassed on Windows.
- Converted `mkdir`, staging-creation, and final-`rename` `OSError`s into clean
  `UnmixError`s (with staging cleanup) instead of bare tracebacks.
- Replaced placeholder "acknowledge protection exists" tests with real
  regression tests for O_EXCL semantics, staging cleanup, permission failures,
  and nested symlink chains; added a static no-execution contract test.

## Residual risks and bounded cases

- **Concurrent hostile mutation of the output directory** (a shared directory
  an attacker can also write to) is out of scope. `os.rename` of the completed
  staging tree is checked for a pre-existing destination but is not hardened
  against an attacker who can race the check; this is why the tool requires a
  trusted local destination and is documented accordingly.
- **Windows reparse points** (junctions/mount points) are not fully covered by
  `Path.is_symlink()`/`O_NOFOLLOW` on all Windows versions; actual Windows
  validation is deferred to CI.
- **Ambiguous default Repomix XML**: content containing a literal `</file>` or
  a path containing `"` is rejected and the user is told to regenerate with
  `--parsable-style`; this is a documented fidelity limitation, not an escape.
- Exclusions reduce auto-activation risk but are **not** secret scanning; both
  input and output can contain secrets. See [EXCLUSIONS.md](EXCLUSIONS.md).
- An **independent adversarial/external review** has not been performed.

## Commands actually run

```bash
python3 -m unittest discover -s tests -v      # 81 tests, 2 skipped (validator, /dev/null)
ruff check src tests                          # PASS
ruff format --check src tests                 # PASS
mypy src/repomix_unmixer                      # PASS
```

Platform: macOS arm64, Python 3.12.7.