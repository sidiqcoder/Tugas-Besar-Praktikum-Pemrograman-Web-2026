#!/usr/bin/env python3
"""Pemeriksa PR mahasiswa. Jalankan dari CHECKOUT MAIN yang tepercaya.

PENTING: Jangan jalankan file Python validator dari checkout PR; PR adalah kode tak tepercaya.
Tidak mengeksekusi kode aplikasi (hanya php -l untuk syntax check).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from validate_manifest import load_and_validate, ManifestError

GROUP_RE = re.compile(r"^kelompok/kelompok_(\d{2})/(.+)$", re.ASCII)
GITHUB_USER = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$", re.ASCII)
REQUIRED_FILES = ("README.md", "CONTRIBUTIONS.md", "project.json", "public/index.php", "database/schema.sql")
FORBIDDEN_DIRS = {".git", ".github", "node_modules", "vendor", ".idea", ".vscode", "__pycache__"}
FORBIDDEN_FILES = {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json", ".htpasswd"}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3", ".db", ".zip", ".rar", ".7z", ".tar", ".exe"}
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_TOTAL_SIZE = 80 * 1024 * 1024
MAX_FILES = 1000


class ValidationError(ValueError):
    pass


def changed_paths(repo: Path, base: str) -> list[str]:
    if not re.fullmatch(r"[a-fA-F0-9]{40,64}", base):
        raise ValidationError("Git base SHA tidak valid")
    proc = subprocess.run(["git", "-C", str(repo), "diff", "--name-status", "-z", "--no-renames",
                           "--no-ext-diff", base, "HEAD", "--"], capture_output=True)
    if proc.returncode:
        raise ValidationError(f"git diff gagal: {proc.stderr.decode(errors='replace').strip()}")
    records = proc.stdout.split(b"\0")
    if records and records[-1] == b"":
        records.pop()
    if len(records) % 2:
        raise ValidationError("Format git diff tidak dikenali")
    result = []
    for offset in range(0, len(records), 2):
        status = records[offset].decode("ascii", errors="replace")
        path = records[offset + 1].decode("utf-8", errors="strict")
        if status[0] not in "ACDMRTUXB":
            raise ValidationError(f"Status git tidak dikenal: {status}")
        result.append(path)
    return result


def validate_changed_scope(paths: list[str]) -> str:
    if not paths:
        raise ValidationError("PR tidak memiliki perubahan file")
    groups = set()
    for filename in paths:
        matched = GROUP_RE.fullmatch(filename)
        if not matched:
            raise ValidationError(f"Perubahan di luar folder kelompok dilarang: {filename}")
        group, relative = matched.groups()
        if not 1 <= int(group) <= 27 or not relative:
            raise ValidationError(f"Nama/nomor folder kelompok tidak valid: {filename}")
        if any(part in {".", ".."} for part in PurePosixPath(relative).parts):
            raise ValidationError(f"Path tidak aman: {filename}")
        groups.add(group)
    if len(groups) != 1:
        raise ValidationError(f"Satu PR hanya boleh menyentuh satu folder kelompok; ditemukan {sorted(groups)}")
    return groups.pop()


def is_forbidden(relative: Path) -> bool:
    parts = relative.parts
    if any(p in FORBIDDEN_DIRS for p in parts):
        return True
    basename = relative.name.lower()
    if basename in FORBIDDEN_FILES:
        return True
    if basename.startswith(".env") and basename != ".env.example":
        return True
    if basename.endswith(".tar.gz") or relative.suffix.lower() in FORBIDDEN_SUFFIXES:
        return True
    return False


def check_gitlinks(repo: Path, group: str) -> None:
    """Menolak submodule/gitlink (mode 160000) pada perubahan mahasiswa."""
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--stage", "-z", "--", f"kelompok/kelompok_{group}"],
        capture_output=True,
    )
    if proc.returncode:
        raise ValidationError("Gagal memeriksa mode Git")
    for item in proc.stdout.split(b"\0"):
        if item.startswith(b"160000 "):
            raise ValidationError("Git submodule/gitlink tidak diperbolehkan dalam proyek kelompok")


def scan_files(root: Path) -> list[Path]:
    files: list[Path] = []
    total = 0
    if root.is_symlink() or not root.is_dir():
        raise ValidationError(f"Folder proyek tidak ditemukan atau symlink: {root}")
    for directory, subdirs, filenames in os.walk(root, topdown=True, followlinks=False):
        for name in subdirs + filenames:
            path = Path(directory) / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ValidationError(f"Symlink dilarang: {path.relative_to(root)}")
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise ValidationError(f"Tipe berkas tidak didukung: {path.relative_to(root)}")
            rel = path.relative_to(root)
            if is_forbidden(rel):
                raise ValidationError(f"Berkas/folder terlarang: {rel}")
        for file in filenames:
            path = Path(directory) / file
            size = path.stat().st_size
            total += size
            if size > MAX_FILE_SIZE:
                raise ValidationError(f"Berkas melebihi batas 10 MiB: {path.relative_to(root)}")
            files.append(path)
            if len(files) > MAX_FILES or total > MAX_TOTAL_SIZE:
                raise ValidationError("Proyek melewati batas 1000 file atau 80 MiB")
    return files


def validate_project_metadata(root: Path, group: str, faculty: str, members_per_group: int) -> None:
    for required in REQUIRED_FILES:
        target = root / required
        if not target.is_file() or target.stat().st_size == 0:
            raise ValidationError(f"File wajib tidak ada/kosong: {required}")
    try:
        obj = json.loads((root / "project.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"project.json rusak: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValidationError("project.json harus berisi object JSON")
    if type(obj.get("group")) is not int or obj["group"] != int(group):
        raise ValidationError(f"project.json: group harus {int(group)}")
    if obj.get("faculty") != faculty:
        raise ValidationError(f"project.json: faculty harus {faculty} sesuai penetapan admin")
    title = obj.get("title")
    if not isinstance(title, str) or len(title.strip()) < 5 or "GANTI" in title.upper():
        raise ValidationError("project.json: title wajib berisi judul asli (minimal 5 karakter)")
    members = obj.get("members")
    if not isinstance(members, list) or len(members) != members_per_group:
        raise ValidationError(f"project.json: members harus berisi {members_per_group} anggota")
    handles = []
    for idx, member in enumerate(members, 1):
        if not isinstance(member, dict):
            raise ValidationError(f"project.json: anggota #{idx} bukan object")
        name, handle = member.get("name"), member.get("github")
        if not isinstance(name, str) or len(name.strip()) < 3 or re.fullmatch(r"(?i)anggota\s*\d+", name.strip()):
            raise ValidationError(f"project.json: nama anggota #{idx} belum valid")
        if not isinstance(handle, str) or not GITHUB_USER.fullmatch(handle) or handle.lower().startswith("username"):
            raise ValidationError(f"project.json: username GitHub anggota #{idx} belum valid")
        handles.append(handle.lower())
    if len(set(handles)) != len(handles):
        raise ValidationError("project.json: username GitHub anggota harus unik")


def lint_php(files: list[Path]) -> int:
    count = 0
    for file in files:
        if file.suffix.lower() != ".php":
            continue
        result = subprocess.run(["php", "-l", str(file)], capture_output=True, text=True)
        if result.returncode:
            message = (result.stdout + "\n" + result.stderr).strip()
            raise ValidationError(f"Syntax PHP tidak valid di {file.name}: {message}")
        count += 1
    if not count:
        raise ValidationError("Minimal harus ada file PHP")
    return count


def check(repo: Path, base: str, manifest_path: Path, themes_path: Path, php: bool = True) -> str:
    assignments, _ = load_and_validate(manifest_path, themes_path)
    group = validate_changed_scope(changed_paths(repo, base))
    faculty = assignments["groups"][group]["faculty"]
    if faculty is None:
        raise ValidationError(f"kelompok_{group} belum diberi tema di manifest oleh admin. Hubungi asisten.")
    root = repo / "kelompok" / f"kelompok_{group}"
    check_gitlinks(repo, group)
    files = scan_files(root)
    validate_project_metadata(root, group, faculty, assignments["members_per_group"])
    php_count = lint_php(files) if php else len([x for x in files if x.suffix.lower() == ".php"])
    print(f"OK: kelompok_{group} | {faculty} | {len(files)} file | {php_count} PHP")
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as handle:
            handle.write(f"group={group}\nfaculty={faculty}\n")
    return group


def main() -> int:
    p = argparse.ArgumentParser(description="Validasi PR dari fork")
    p.add_argument("--repo", type=Path, required=True, help="Path checkout PR (tidak tepercaya)")
    p.add_argument("--base-sha", required=True, help="SHA branch main sebelum PR")
    p.add_argument("--manifest", type=Path, required=True, help="Path trusted manifest di checkout main")
    p.add_argument("--themes", type=Path, required=True, help="Path trusted daftar tema di checkout main")
    args = p.parse_args()
    try:
        check(args.repo.resolve(), args.base_sha, args.manifest, args.themes)
    except (ValidationError, ManifestError, OSError, UnicodeError) as exc:
        print(f"::error::{exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
