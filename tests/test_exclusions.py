"""Tests for the documented exclusion policy (P0-12).

The policy is safety-based exclusion, not content rewriting: retained files
must be byte-identical to the parsed export content. See docs/EXCLUSIONS.md.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from repomix_static_reconstructor.extractor import (
    UnmixError,
    exclusion_category,
    unmix_repomix,
)


def markdown(files):
    return "".join(f"## File: {path}\n```\n{content}\n```\n" for path, content in files)


def xml(files):
    entries = "".join(f'<file path="{path}">\n{content}\n</file>\n' for path, content in files)
    return f"<files>\n{entries}</files>"


def json_export(files):
    return json.dumps({"files": {path: content for path, content in files}})


class ExclusionRuleTests(unittest.TestCase):
    def test_excluded_paths_and_categories(self):
        cases = {
            ".mcp.json": "agent-config",
            "nested/.mcp.json": "agent-config",
            ".MCP.JSON": "agent-config",
            ".claude/settings.json": "agent-config",
            ".CLAUDE/settings.json": "agent-config",
            ".codex/config.toml": "agent-config",
            ".cursor/mcp.json": "agent-config",
            ".gemini/settings.json": "agent-config",
            ".opencode/config.json": "agent-config",
            ".vscode/settings.json": "ide-metadata",
            ".idea/workspace.xml": "ide-metadata",
            ".git/config": "vcs-metadata",
            ".env": "credential-config",
            ".ENV": "credential-config",
            ".env.local": "credential-config",
            "app/.env.production": "credential-config",
            ".env.example.local": "credential-config",
            ".env.sample.local": "credential-config",
            ".envrc": "credential-config",
            ".DS_Store": "os-metadata",
            "nested/.ds_store": "os-metadata",
            ".claude/.env.example": "agent-config",
            ".claude": "agent-config",
            ".vscode": "ide-metadata",
            ".git": "vcs-metadata",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(exclusion_category(path), expected)

    def test_retained_paths(self):
        cases = [
            ".env.example",
            ".env.sample",
            ".env.template",
            ".ENV.EXAMPLE",
            "docs/.env.template",
            "mcp.json",
            ".mcp.json.bak",
            ".claude-backup/settings.json",
            "foo.claude/x",
            ".github/workflows/ci.yml",
            ".gitignore",
            "my.env",
            "environment.md",
            "git/config",
            ".vscodefile",
            "src/app.py",
            "README.md",
        ]
        for path in cases:
            with self.subTest(path=path):
                self.assertIsNone(exclusion_category(path))

    def test_windows_separators_are_normalized_before_matching(self):
        self.assertEqual(exclusion_category(r".claude\settings.json"), "agent-config")
        self.assertEqual(exclusion_category(r"nested\.mcp.json"), "agent-config")
        self.assertIsNone(exclusion_category(r"docs\.env.example"))

    def test_directory_rules_use_complete_components(self):
        self.assertEqual(exclusion_category(".claude/nested/deep/file"), "agent-config")
        self.assertIsNone(exclusion_category(".claude-not-config/file"))
        self.assertIsNone(exclusion_category("x/.claude-backup/file"))
        self.assertIsNone(exclusion_category("x/git/config"))


class ExclusionExtractionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.input = self.root / "in.md"
        self.output = self.root / "out"

    def tearDown(self):
        self.tmp.cleanup()

    def run_files(self, files, input_file=None, output_dir=None, **kwargs):
        input_path = Path(input_file) if input_file else self.input
        output_path = Path(output_dir) if output_dir else self.output
        input_path.write_text(markdown(files), encoding="utf-8")
        return unmix_repomix(input_path, output_path, **kwargs)

    def test_retained_content_is_unchanged_and_excluded_paths_are_absent(self):
        files = [
            ("src/app.py", "print('keep')\n\n  indented"),
            ("README.md", "# Keep\n\nNo rewriting."),
            (".env.example", "SECRET=\nOTHER="),
            ("nested/.env.template", "TOKEN="),
            (".env", "SECRET=real"),
            (".env.local", "SECRET=local"),
            ("nested/.env.production", "SECRET=prod"),
            (".env.example.local", "SECRET=derived"),
            (".envrc", "export SECRET=1"),
            (".mcp.json", '{"mcpServers": {"x": {"command": "run"}}}'),
            (".claude/settings.json", '{"hooks": {}}'),
            (".claude/.env.example", "SECRET="),
            (".cursor/mcp.json", "{}"),
            (".codex/config.toml", 'model = "x"'),
            (".gemini/settings.json", "{}"),
            (".opencode/config.json", "{}"),
            (".vscode/tasks.json", "{}"),
            (".idea/workspace.xml", "<project/>"),
            (".git/config", "[core]"),
            (".DS_Store", "metadata"),
            ("nested/.DS_Store", "metadata"),
        ]
        excluded = {
            ".env",
            ".env.local",
            "nested/.env.production",
            ".env.example.local",
            ".envrc",
            ".mcp.json",
            ".claude/settings.json",
            ".claude/.env.example",
            ".cursor/mcp.json",
            ".codex/config.toml",
            ".gemini/settings.json",
            ".opencode/config.json",
            ".vscode/tasks.json",
            ".idea/workspace.xml",
            ".git/config",
            ".DS_Store",
            "nested/.DS_Store",
        }
        retained = {path: content for path, content in files if path not in excluded}

        result = self.run_files(files)

        self.assertEqual(set(result.skipped), excluded)
        self.assertEqual(set(result.extracted), set(retained))
        self.assertEqual(result.total_bytes, sum(len(text.encode()) for text in retained.values()))
        for path, content in retained.items():
            self.assertEqual((self.output / path).read_bytes(), content.encode("utf-8"), path)
        for path in excluded:
            self.assertFalse((self.output / path).exists(), path)
        self.assertFalse((self.output / ".claude").exists())
        self.assertFalse((self.output / ".git").exists())

    def test_policy_applies_identically_to_xml_and_json(self):
        files = [
            ("keep.txt", "keep"),
            (".mcp.json", "{}"),
            (".env", "SECRET=1"),
            (".env.example", "SECRET="),
            (".vscode/settings.json", "{}"),
        ]
        for name, serializer in (("export.xml", xml), ("export.json", json_export)):
            with self.subTest(format=name):
                source = self.root / name
                source.write_text(serializer(files), encoding="utf-8")
                target = self.root / f"out-{name}"
                result = unmix_repomix(source, target)
                self.assertEqual(result.extracted, ("keep.txt", ".env.example"))
                self.assertEqual(
                    set(result.skipped), {".mcp.json", ".env", ".vscode/settings.json"}
                )
                self.assertEqual((target / "keep.txt").read_text(), "keep")
                self.assertEqual((target / ".env.example").read_text(), "SECRET=")
                self.assertFalse((target / ".mcp.json").exists())

    def test_excluded_paths_are_still_path_validated(self):
        for path in ["../.env", "/.mcp.json", r"C:\.env", ".claude/../../escape"]:
            with self.subTest(path=path):
                with self.assertRaises(UnmixError):
                    self.run_files([(path, "x")], dry_run=True)
                self.assertFalse(self.output.exists())

    def test_excluded_entries_still_count_against_file_limit(self):
        with self.assertRaises(UnmixError):
            self.run_files([(".env", "x"), ("keep.txt", "y")], dry_run=True, max_files=1)
        self.assertFalse(self.output.exists())

    def test_dry_run_reports_exclusions_without_writing(self):
        result = self.run_files([(".mcp.json", "{}"), ("keep.txt", "y")], dry_run=True)
        self.assertEqual(result.skipped, (".mcp.json",))
        self.assertFalse(self.output.exists())

    def test_cli_reports_exclusion_category(self):
        self.input.write_text(markdown([(".mcp.json", "{}"), ("keep.txt", "y")]), encoding="utf-8")
        src = Path(__file__).resolve().parents[1] / "src"
        env = dict(os.environ)
        env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "repomix_static_reconstructor.cli",
                str(self.input),
                str(self.output),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(".mcp.json [agent-config]", completed.stdout)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
