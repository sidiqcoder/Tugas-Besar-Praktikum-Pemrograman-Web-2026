#!/usr/bin/env python3
"""Validasi daftar tema dan pengalokasian kelompok resmi (trusted code)."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path


class ManifestError(ValueError):
    pass


def load_and_validate(assignments_path: Path, themes_path: Path) -> tuple[dict, dict]:
    try:
        assignments = json.loads(assignments_path.read_text(encoding="utf-8"))
        themes = json.loads(themes_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"File konfigurasi tidak bisa dibaca: {exc}") from exc

    required = {"FEB", "FH", "FP", "FKIP", "FT", "FISIP", "FMIPA", "FK"}
    if set(themes) != required:
        raise ManifestError("config/themes.json wajib memuat tepat 8 kode fakultas")
    if assignments.get("year") != 2026:
        raise ManifestError("Tahun di manifest harus 2026")
    if assignments.get("max_groups") != 27 or assignments.get("members_per_group") != 5:
        raise ManifestError("Manifest harus memuat 27 kelompok, masing-masing 5 mahasiswa")
    limit = assignments.get("max_groups_per_faculty")
    if type(limit) is not int or limit != 4:
        raise ManifestError("Batas setiap fakultas harus 4 kelompok")
    groups = assignments.get("groups")
    if not isinstance(groups, dict) or set(groups) != {f"{i:02d}" for i in range(1, 28)}:
        raise ManifestError("groups harus memiliki key 01..27 tepat satu kali")
    counts: Counter[str] = Counter()
    for group, entry in groups.items():
        if not isinstance(entry, dict) or set(entry) != {"faculty"}:
            raise ManifestError(f"Kelompok {group}: isi harus {{'faculty': CODE_ATAU_NULL}}")
        faculty = entry["faculty"]
        if faculty is not None:
            if faculty not in required:
                raise ManifestError(f"Kelompok {group}: fakultas tidak dikenal: {faculty}")
            counts[faculty] += 1
    over = [faculty for faculty, count in counts.items() if count > limit]
    if over:
        raise ManifestError(f"Kuota 4 kelompok/fakultas terlampaui: {', '.join(over)}")
    return assignments, themes


def main() -> int:
    parser = argparse.ArgumentParser(description="Validasi manifest resmi")
    parser.add_argument("--manifest", type=Path, default=Path("config/assignments.json"))
    parser.add_argument("--themes", type=Path, default=Path("config/themes.json"))
    args = parser.parse_args()
    try:
        assignments, _ = load_and_validate(args.manifest, args.themes)
    except ManifestError as exc:
        print(f"::error::{exc}")
        return 1
    registered = sum(1 for group in assignments["groups"].values() if group["faculty"])
    print(f"OK: manifest sah; {registered}/27 kelompok telah mendapat tema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
