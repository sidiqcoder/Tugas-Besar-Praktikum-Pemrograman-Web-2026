#!/usr/bin/env python3
"""Continuous delivery: kemas folder kelompok setelah MERGE ke main.

Tidak menjalankan aplikasi kiriman, tidak melakukan deploy ke server.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_pr import scan_files, ValidationError


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    before = os.environ.get("BEFORE_SHA", "")
    after = os.environ.get("AFTER_SHA", "HEAD")
    if not re.fullmatch(r"[a-fA-F0-9]{40,64}", after):
        # Allows HEAD for local testing, but real workflow passes a hash.
        if after != "HEAD":
            print("Invalid AFTER_SHA")
            return 1
    if re.fullmatch(r"0{40,64}", before):
        command = ["git", "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", after]
    elif re.fullmatch(r"[a-fA-F0-9]{40,64}", before):
        command = ["git", "diff", "--name-only", before, after, "--"]
    else:
        print("Invalid BEFORE_SHA")
        return 1
    result = subprocess.run(command, cwd=repo, capture_output=True, text=True)
    if result.returncode:
        print(result.stderr)
        return 1
    groups = sorted({m.group(1) for filename in result.stdout.splitlines()
                     if (m := re.fullmatch(r"kelompok/kelompok_(\d{2})/.+", filename))})
    out = repo / "dist"
    out.mkdir(exist_ok=True)
    packaged = 0
    for group in groups:
        project = repo / "kelompok" / f"kelompok_{group}"
        if not (project / "project.json").exists():
            continue
        try:
            files = scan_files(project)
        except ValidationError as exc:
            print(f"Cannot package {group}: {exc}")
            return 1
        archive = out / f"kelompok_{group}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for file in files:
                z.write(file, file.relative_to(repo))
        print(f"Packaged {archive.name} ({len(files)} files)")
        packaged += 1
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"has_artifacts={'true' if packaged else 'false'}\n")
    print(f"OK: {packaged} package(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
