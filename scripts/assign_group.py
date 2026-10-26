#!/usr/bin/env python3
"""Khusus admin: tetapkan atau kosongkan tema kelompok (commit ke main)."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from validate_manifest import load_and_validate, ManifestError


def assign(manifest_path: Path, themes_path: Path, group: int, faculty: str | None, force: bool = False) -> None:
    data, themes = load_and_validate(manifest_path, themes_path)
    key = f"{group:02d}"
    if key not in data["groups"]:
        raise ManifestError("Nomor kelompok harus antara 1 dan 27")
    if faculty is not None and faculty not in themes:
        raise ManifestError(f"Tema tidak dikenal: {faculty}")
    current = data["groups"][key]["faculty"]
    if current is not None and current != faculty and not force:
        raise ManifestError(f"Kelompok {key} sudah di {current}. Gunakan --force untuk mengganti")
    data["groups"][key]["faculty"] = faculty
    temp = manifest_path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        load_and_validate(temp, themes_path)
        temp.replace(manifest_path)
    finally:
        temp.unlink(missing_ok=True)
    print(f"OK: kelompok_{key} => {faculty or 'belum ditetapkan'}")


def main() -> int:
    p = argparse.ArgumentParser(description="Tetapkan tema fakultas untuk kelompok")
    p.add_argument("group", type=int, help="Nomor kelompok 1..27")
    p.add_argument("faculty", help="FEB/FH/FP/FKIP/FT/FISIP/FMIPA/FK atau NONE")
    p.add_argument("--force", action="store_true", help="Izin mengganti tema yang sudah ditetapkan")
    p.add_argument("--manifest", type=Path, default=Path("config/assignments.json"))
    p.add_argument("--themes", type=Path, default=Path("config/themes.json"))
    args = p.parse_args()
    try:
        assign(args.manifest, args.themes, args.group,
               None if args.faculty.upper() == "NONE" else args.faculty.upper(), args.force)
    except ManifestError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
