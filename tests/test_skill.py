"""Tests for the portable Agent Skill (P0-15).

The skill must stay valid against the Agent Skills specification
(agentskills.io): YAML frontmatter with name/description, directory name
matching, and a no-execute safety contract. The official `skills-ref`
validator is invoked when it is importable so regressions are caught locally
and in CI; the structural checks below always run.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

SKILL_DIR = Path(__file__).resolve().parents[1] / "skills" / "repomix-static-reconstructor"
SKILL_MD = SKILL_DIR / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)


def _frontmatter() -> dict[str, str]:
    text = SKILL_MD.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    assert match, "SKILL.md is missing YAML frontmatter delimiters"
    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


class SkillStructureTests(unittest.TestCase):
    def test_skill_md_exists_in_named_directory(self):
        self.assertTrue(SKILL_MD.is_file())
        self.assertEqual(SKILL_DIR.name, "repomix-static-reconstructor")

    def test_frontmatter_fields(self):
        fields = _frontmatter()
        self.assertEqual(fields.get("name"), "repomix-static-reconstructor")
        # Spec: name is lowercase letters, numbers, and hyphens (<= 64 chars).
        self.assertLessEqual(len(fields["name"]), 64)
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertTrue(fields.get("description"))

    def test_no_execute_contract_stated(self):
        body = SKILL_MD.read_text(encoding="utf-8")
        for phrase in ("never execute", "not overwritten", "untrusted"):
            self.assertIn(phrase, body)

    def test_documented_commands_match_installed_cli(self):
        body = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("unmix-repomix", body)
        self.assertIn("reconstruct-all", body)
        self.assertNotIn("scripts/unmix_repomix.py", body)
        self.assertNotIn("scripts/reconstruct_all.py", body)

    def test_official_validator_passes_when_available(self):
        try:
            from skills_ref import validate  # type: ignore[import-not-found]
        except ImportError:
            self.skipTest("skills-ref not installed")
        problems = validate(SKILL_DIR)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
