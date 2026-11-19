"""Static no-execution contract tests (P1-12).

The extractor is documented (SECURITY.md, README) to never spawn shells, invoke
subprocesses, or initiate outbound network traffic while parsing or
reconstructing. These tests inspect the trusted package's source with `ast` so
that a regression that adds such a capability is caught in review, without
ever executing reconstructed content.

Only the trusted package in ``src/repomix_unmixer`` is scanned; test modules
may legitimately use subprocess and sockets for their own harness work.
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
PACKAGE_DIR = SRC_ROOT / "repomix_unmixer"

# Top-level module names that would indicate subprocess or network capability.
FORBIDDEN_IMPORTS = (
    "subprocess",
    "socket",
    "urllib",
    "requests",
    "http",
    "ftplib",
    "smtplib",
    "telnetlib",
    "pty",
    "xmlrpc",
    "webbrowser",
)

# Builtin/attribute calls that would indicate dynamic or external execution.
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__", "globals"}
FORBIDDEN_ATTRS = {
    "system",
    "popen",
    "spawn",
    "execl",
    "execv",
    "kill",
    "connect",
    "send",
    "recv",
}


class NoExecutionContractTests(unittest.TestCase):
    def test_package_source_has_no_forbidden_imports(self):
        for source_file in sorted(PACKAGE_DIR.glob("*.py")):
            tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._assert_import_allowed(source_file, alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self._assert_import_allowed(source_file, node.module)

    def test_package_source_has_no_dynamic_or_external_execution(self):
        for source_file in sorted(PACKAGE_DIR.glob("*.py")):
            tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    self._assert_call_allowed(source_file, node)

    def _assert_import_allowed(self, source_file: Path, module_name: str) -> None:
        root = module_name.split(".")[0]
        self.assertNotIn(
            root,
            FORBIDDEN_IMPORTS,
            f"{source_file.name} imports forbidden module {module_name!r} "
            "(subprocess/network capability violates the no-execution contract)",
        )

    def _assert_call_allowed(self, source_file: Path, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.assertNotIn(
                node.func.id,
                FORBIDDEN_CALLS,
                f"{source_file.name} calls {node.func.id!r} (dynamic execution)",
            )
        elif (
            isinstance(node.func, ast.Attribute)
            # Allow importlib.metadata.version used for --version; everything
            # on os/socket/urllib/etc. that could run or connect is rejected.
            and node.func.attr in FORBIDDEN_ATTRS
        ):
            self.fail(
                f"{source_file.name} calls {node.func.attr!r} (subprocess/network capability)"
            )


if __name__ == "__main__":
    sys.exit(unittest.main())
