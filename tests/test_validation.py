"""Automated tests for trusted validators; no network dependencies."""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from validate_manifest import load_and_validate, ManifestError
from validate_pr import (validate_changed_scope, validate_project_metadata, scan_files,
                         lint_php, ValidationError, check)
from assign_group import assign

ROOT = SCRIPT_DIR.parent


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.p = Path(self.temp.name) / "assignments.json"
        self.themes = ROOT / "config/themes.json"
        self.p.write_text((ROOT / "config/assignments.json").read_text(encoding="utf-8"), encoding="utf-8")

    def test_empty_registry_valid(self):
        data, _ = load_and_validate(self.p, self.themes)
        self.assertEqual(len(data["groups"]), 27)

    def test_four_slots_then_reject_fifth(self):
        for i in range(1, 5):
            assign(self.p, self.themes, i, "FK")
        with self.assertRaises(ManifestError):
            assign(self.p, self.themes, 5, "FK")
        self.assertIsNone(load_and_validate(self.p, self.themes)[0]["groups"]["05"]["faculty"])

    def test_requires_force_for_reassignment(self):
        assign(self.p, self.themes, 1, "FEB")
        with self.assertRaises(ManifestError):
            assign(self.p, self.themes, 1, "FH")
        assign(self.p, self.themes, 1, "FH", force=True)
        self.assertEqual(load_and_validate(self.p, self.themes)[0]["groups"]["01"]["faculty"], "FH")


class ScopeTests(unittest.TestCase):
    def test_single_group_only(self):
        self.assertEqual(validate_changed_scope(["kelompok/kelompok_12/public/index.php"]), "12")
        with self.assertRaises(ValidationError):
            validate_changed_scope(["kelompok/kelompok_02/a.php", "kelompok/kelompok_03/b.php"])
        with self.assertRaises(ValidationError):
            validate_changed_scope([".github/workflows/validate-pr.yml"])
        with self.assertRaises(ValidationError):
            validate_changed_scope(["kelompok/kelompok_99/index.php"])


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "kelompok_12"
        shutil.copytree(ROOT / "templates/project-starter", self.root)
        doc = json.loads((self.root / "project.json").read_text(encoding="utf-8"))
        doc.update({"group":12,"faculty":"FKIP","title":"Sistem Bank Soal Pendidikan"})
        doc["members"] = [{"name":f"Nama Peserta {n}","github":f"peserta{n}"} for n in range(1,6)]
        (self.root / "project.json").write_text(json.dumps(doc), encoding="utf-8")

    def test_valid_starter_after_metadata_is_filled(self):
        validate_project_metadata(self.root, "12", "FKIP", 5)
        self.assertGreater(lint_php(scan_files(self.root)), 0)

    def test_reject_uncommitted_secret(self):
        (self.root / ".env").write_text("DB_PASSWORD=secret")
        with self.assertRaises(ValidationError):
            scan_files(self.root)

    def test_reject_wrong_faculty(self):
        with self.assertRaises(ValidationError):
            validate_project_metadata(self.root, "12", "FH", 5)

    def test_reject_symlink(self):
        (self.root / "outside").symlink_to("/etc/passwd")
        with self.assertRaises(ValidationError):
            scan_files(self.root)

    def test_reject_php_parse_error(self):
        if not shutil.which("php"):
            self.skipTest("PHP unavailable")
        (self.root / "public/bad.php").write_text("<?php echo ( ;")
        with self.assertRaises(ValidationError):
            lint_php(scan_files(self.root))


class FullPullRequestTests(unittest.TestCase):
    def test_end_to_end_valid_pull_request(self):
        if not shutil.which("git") or not shutil.which("php"):
            self.skipTest("git/php unavailable")
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            repo = tmp / "repo"
            repo.mkdir()
            def git(*args):
                return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()
            git("init", "-q")
            git("config", "user.email", "testing@example.org")
            git("config", "user.name", "Testing")
            (repo / "README.md").write_text("Base")
            git("add", ".")
            git("commit", "-qm", "base")
            base = git("rev-parse", "HEAD")
            project = repo / "kelompok/kelompok_12"
            shutil.copytree(ROOT / "templates/project-starter", project)
            metadata = json.loads((project / "project.json").read_text())
            metadata.update({"group": 12, "faculty": "FKIP", "title": "Portal Belajar Tematik"})
            metadata["members"] = [{"name": f"Mahasiswa {i}", "github": f"mahasiswa{i}"} for i in range(1, 6)]
            (project / "project.json").write_text(json.dumps(metadata))
            git("add", ".")
            git("commit", "-qm", "submit")
            m = tmp / "registry.json"
            a = json.loads((ROOT / "config/assignments.json").read_text())
            a["groups"]["12"]["faculty"] = "FKIP"
            m.write_text(json.dumps(a))
            self.assertEqual(check(repo, base, m, ROOT / "config/themes.json"), "12")
            (repo / "hijack.txt").write_text("bad")
            git("add", ".")
            git("commit", "-qm", "scope breach")
            with self.assertRaises(ValidationError):
                check(repo, base, m, ROOT / "config/themes.json")


if __name__ == "__main__":
    unittest.main()
