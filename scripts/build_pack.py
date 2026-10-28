#!/usr/bin/env python3
"""Build dist/revenue-partner-upgrade.zip: the part of this repo the Revenue Partner's computer needs.

Jesse drags the zip into his Slack DM with the Revenue Partner (START-HERE). It unpacks to
~/smart-contracting-dream-team/ there. The zip is deterministic (fixed timestamps, sorted entries),
so `--check` can tell whether the committed zip matches the repo.

  python3 scripts/build_pack.py           build it
  python3 scripts/build_pack.py --check   exit 1 if dist/ is out of date
"""
from __future__ import annotations

import hashlib
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOP = "smart-contracting-dream-team"
INCLUDE = ["START-HERE.md", "PROJECT_CHARTER.md", "OPEN_QUESTIONS.md", "manifest.json",
           "agents", "skills", "routines", "policies", "program", "tools", "install",
           "client-context", "dashboard", "radar/storm-day.md"]
SKIP_PARTS = {"__pycache__", ".DS_Store"}
OUT = ROOT / "dist" / "revenue-partner-upgrade.zip"


def files() -> list[Path]:
    found = []
    for name in INCLUDE:
        path = ROOT / name
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            found += [p for p in path.rglob("*") if p.is_file() and not SKIP_PARTS & set(p.parts)
                      and not p.name.startswith("test_")]
    return sorted(found)


def build() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files():
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"{TOP}/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
            executable = path.suffix in (".sh", ".py")
            info.external_attr = ((0o755 if executable else 0o644) | 0o100000) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    return buf.getvalue()


def main() -> int:
    data = build()
    if "--check" in sys.argv:
        current = OUT.read_bytes() if OUT.exists() else b""
        if current != data:
            print(f"{OUT.relative_to(ROOT)} is out of date: run python3 scripts/build_pack.py")
            return 1
        print(f"{OUT.relative_to(ROOT)} is current ({len(files())} files)")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_bytes(data)
    print(f"Built {OUT.relative_to(ROOT)}: {len(files())} files, {len(data) // 1024} KB, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
