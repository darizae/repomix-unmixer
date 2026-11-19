"""Synthetic regression tests for the TRUSTED extractor, never recovered projects."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from unmix_repomix import (  # noqa: E402
    UnmixError,
    normalize_archive_path,
    parse_json,
    parse_markdown,
    parse_xml,
    unmix_repomix,
)


def markdown(files):
    return ''.join(f'## File: {path}\n```\n{content}\n```\n' for path, content in files)


class ExtractorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.input = self.root / 'in.md'
        self.output = self.root / 'out'

    def tearDown(self):
        self.tmp.cleanup()

    def run_files(self, files, **kwargs):
        self.input.write_text(markdown(files), encoding='utf-8')
        return unmix_repomix(self.input, self.output, **kwargs)

    def test_content_and_path_fidelity(self):
        literal = 'package sample-name\nfunction ExampleFunction() {}'
        res = self.run_files([('OrgName/CaseSensitive.js', literal)])
        self.assertEqual(res.extracted, ('OrgName/CaseSensitive.js',))
        self.assertEqual((self.output / 'OrgName/CaseSensitive.js').read_text(), literal)

    def test_variable_fences(self):
        raw = '## File: a.md\n````\n```js\nconst x = 1\n```\n````\n'
        self.input.write_text(raw)
        unmix_repomix(self.input, self.output)
        self.assertEqual((self.output / 'a.md').read_text(), '```js\nconst x = 1\n```')

    def test_dry_run_does_not_write(self):
        result = self.run_files([('src/a.txt', 'hi')], dry_run=True)
        self.assertEqual(result.extracted, ('src/a.txt',))
        self.assertFalse(self.output.exists())

    def test_skips_unsafe_agent_metadata_without_rewriting(self):
        res = self.run_files([('.mcp.json', '{}'), ('.claude/settings.json', '{}'),
                              ('.env', 'secret=foo'), ('.env.example', 'KEY='),
                              ('code.js', 'keep me')])
        self.assertEqual(len(res.skipped), 3)
        self.assertTrue((self.output / '.env.example').exists())
        self.assertEqual((self.output / 'code.js').read_text(), 'keep me')
        self.assertFalse((self.output / '.mcp.json').exists())

    def test_conflicting_paths_both_orders(self):
        for paths in [[('p', 'foo'), ('p/x', 'bar')],
                      [('p/x', 'foo'), ('p', 'bar')]]:
            with self.subTest(paths=paths):
                with self.assertRaises(UnmixError):
                    self.run_files(paths, dry_run=True)
                self.assertFalse(self.output.exists())

    def test_case_collisions_cross_platform(self):
        with self.assertRaises(UnmixError):
            self.run_files([('Src/A.TXT', 'a'), ('src/a.txt', 'b')], dry_run=True)

    def test_unsafe_paths_even_when_excluded(self):
        with self.assertRaises(UnmixError):
            self.run_files([('../.mcp.json', '{}')], dry_run=True)

    def test_windows_and_absolute_paths(self):
        for path in ['../escape', '/absolute', 'C:\\unsafe.txt', '//server/share',
                     'a//b', 'a/./b', 'AUX.log', 'a:evil', 'a/b.']:
            with self.subTest(path=path), self.assertRaises(UnmixError):
                normalize_archive_path(path)

    def test_existing_target_refused_untouched(self):
        self.output.mkdir()
        (self.output / 'sensitive.txt').write_text('do not delete')
        with self.assertRaises(UnmixError):
            self.run_files([('a.txt', 'x')])
        self.assertEqual((self.output / 'sensitive.txt').read_text(), 'do not delete')

    def test_limits_preflight(self):
        for kwargs in [{'max_files': 1}, {'max_file_bytes': 2}, {'max_total_bytes': 2}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(UnmixError):
                self.run_files([('a.txt', 'hello'), ('b.txt', 'world')], dry_run=True, **kwargs)

    def test_xml_and_json_parser(self):
        self.assertEqual(parse_xml('<root><file path="a.txt">\nhello\n</file></root>')[0].content, 'hello')
        self.assertEqual(parse_json(json.dumps({'files': {'x.txt': 'abc'}}))[0].content, 'abc')
        self.assertEqual(parse_json(json.dumps({'files': [{'path': 'x.txt', 'content': 'abc'}]}))[0].content, 'abc')

    def test_xml_full_reconstruct(self):
        xml = self.root / 'repo.xml'
        xml.write_text('<files>\n<file path="src/main.py">\nprint(1)\n</file>\n</files>')
        unmix_repomix(xml, self.output)
        self.assertEqual((self.output / 'src/main.py').read_text(), 'print(1)')

    def test_json_full_reconstruct(self):
        data = self.root / 'repo.json'
        data.write_text(json.dumps({'files': {'a.txt': 'x', 'b.txt': 'y'}}))
        unmix_repomix(data, self.output)
        self.assertEqual((self.output / 'a.txt').read_text(), 'x')

    def test_symlinked_target_rejected(self):
        outside = self.root / 'outside'; outside.mkdir()
        try:
            self.output.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('symlinks unavailable')
        with self.assertRaises(UnmixError):
            self.run_files([('x.txt', 'bad')])
        self.assertEqual(list(outside.iterdir()), [])

    def test_no_partially_committed_output_on_failure(self):
        # Two file paths colliding in preflight must not create a directory.
        with self.assertRaises(UnmixError):
            self.run_files([('good.txt', 'x'), ('bad/../evil.txt', 'y')])
        self.assertFalse(self.output.exists())

    def test_batch_workflow_and_report(self):
        inp = self.root / 'inputs'; inp.mkdir()
        output = self.root / 'outputs'
        (inp / 'demo.md').write_text(markdown([('src/file.txt', 'content')]))
        script = Path(__file__).resolve().parents[1] / 'scripts/reconstruct_all.py'
        first = subprocess.run([sys.executable, str(script), '--input-dir', str(inp),
                                '--output-dir', str(output), '--dry-run'],
                               capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertFalse(output.exists())
        second = subprocess.run([sys.executable, str(script), '--input-dir', str(inp),
                                 '--output-dir', str(output)], capture_output=True, text=True)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((output / 'demo/src/file.txt').read_text(), 'content')
        self.assertTrue((output / 'RECONSTRUCTION_REPORT.md').exists())
        third = subprocess.run([sys.executable, str(script), '--input-dir', str(inp),
                                '--output-dir', str(output)], capture_output=True, text=True)
        self.assertNotEqual(third.returncode, 0)
        self.assertEqual((output / 'demo/src/file.txt').read_text(), 'content')


if __name__ == '__main__':
    unittest.main()
