#!/usr/bin/env python3
"""Install the smart-contracting-dream-team overlay into an existing Hermes home without overwriting local edits.

For one role, it copies:
  skills/shared/* and skills/<role>/*      ->  $HERMES_HOME/skills/scdt/<skill>/
  routines/*.prompt whose ROLE matches     ->  $HERMES_HOME/scdt/routines/
  policies/*                               ->  $HERMES_HOME/scdt/policies/

It never touches SOUL.md, AGENTS.md, config.yaml, .env or anything outside those targets.
It replaces a file only if the file still matches what this installer wrote last time,
so edits made on the computer (by Jesse, the team or the agent) survive updates.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

TEAM = "scdt"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(source: Path, target: Path, prior: dict, current: dict, report: dict) -> None:
    key = target.as_posix()
    if target.exists() and digest(target) == digest(source):
        current[key] = digest(source)
        return
    replace = not target.exists()
    if target.exists() and prior.get(key):
        replace = digest(target) == prior[key]
    if replace:
        target.parent.mkdir(parents=True, exist_ok=True)
        existed = target.exists()
        shutil.copy2(source, target)
        current[key] = digest(source)
        report["updated" if existed else "added"].append(key)
    else:
        # A file this installer never wrote is marked "local:" so no later run mistakes it for its own and overwrites it.
        current[key] = prior.get(key) or "local:" + digest(target)
        if digest(target) != digest(source):
            report["kept-local-edit"].append(key)


def routine_role(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ROLE:"):
            return line.split(":", 1)[1].strip()
        if line.strip() == "---":
            break
    return ""


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit("usage: sync_overlay.py REPO_ROOT HERMES_HOME ROLE VAULT_DIR")
    root = Path(sys.argv[1]).resolve()
    hermes_home = Path(sys.argv[2]).expanduser().resolve()
    role = sys.argv[3]
    vault = Path(sys.argv[4]).expanduser().resolve()

    state_dir = hermes_home / TEAM
    manifest_path = state_dir / ".overlay-manifest.json"
    try:
        prior = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    except (OSError, ValueError):
        prior = {}
    current: dict = {}
    report: dict = {"added": [], "updated": [], "kept-local-edit": []}

    for group in ("shared", role):
        for skill_md in sorted((root / "skills" / group).glob("*/SKILL.md")):
            for source in sorted(p for p in skill_md.parent.rglob("*") if p.is_file()):
                rel = source.relative_to(skill_md.parent)
                copy_file(source, hermes_home / "skills" / TEAM / skill_md.parent.name / rel, prior, current, report)

    for source in sorted((root / "routines").glob("*.prompt")):
        if routine_role(source) in (role, "all"):
            copy_file(source, state_dir / "routines" / source.name, prior, current, report)

    for source in sorted((root / "policies").glob("*.md")):
        copy_file(source, state_dir / "policies" / source.name, prior, current, report)

    for sub in ("context", "log", "state"):
        (state_dir / sub).mkdir(parents=True, exist_ok=True)
    vault.mkdir(parents=True, exist_ok=True)
    (state_dir / "role").write_text(role + "\n", encoding="utf-8")
    (state_dir / "repo").write_text(str(root) + "\n", encoding="utf-8")
    (state_dir / "vault").write_text(str(vault) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(current, indent=2, sort_keys=True), encoding="utf-8")

    for kind, paths in report.items():
        print(f"{kind}: {len(paths)}")
        if kind == "kept-local-edit":
            for p in paths:
                print(f"  kept your edit: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
