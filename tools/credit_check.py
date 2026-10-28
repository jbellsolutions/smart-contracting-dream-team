#!/usr/bin/env python3
"""Print the Revenue Partner's remaining OpenRouter credit, and nothing else. The key never leaves this process.

  credit_check.py                   -> "remaining_usd=4.12"
  credit_check.py --warn-under 3    -> adds " WARN" (once per NZ day) or " OK"; the warn date is kept in
                                       ~/.hermes/scdt/state/credit-warned-on so Jesse is told once a day at most

Hermes keeps the key out of tool subprocesses, so this reads it from ~/.hermes/.env itself.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

STATE = Path.home() / ".hermes" / "scdt" / "state"


def load_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    env = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def get(path: str, key: str) -> dict:
    req = urllib.request.Request(f"https://openrouter.ai/api/v1/{path}", headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8")).get("data", {})


def nz_today() -> str:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Pacific/Auckland")).date().isoformat()
    except Exception:
        return dt.date.today().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warn-under", type=float)
    args = parser.parse_args()
    key = load_key()
    if not key:
        print("FAILED: no OpenRouter key found in the environment or ~/.hermes/.env")
        return 1
    remaining = []
    try:
        credits = get("credits", key)
        if "total_credits" in credits:
            remaining.append(float(credits["total_credits"]) - float(credits.get("total_usage", 0)))
    except Exception as exc:  # report the kind of failure, never the key
        print(f"FAILED: couldn't read /credits ({type(exc).__name__})")
        return 1
    try:
        limit_left = get("key", key).get("limit_remaining")
        if limit_left is not None:
            remaining.append(float(limit_left))
    except Exception:
        pass  # older accounts: /credits alone is enough
    if not remaining:
        print("FAILED: OpenRouter returned no balance")
        return 1
    left = min(remaining)
    line = f"remaining_usd={left:.2f}"
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "credit-last.txt").write_text(f"{line} at {dt.datetime.now().isoformat(timespec='minutes')}\n")
    if args.warn_under is not None:
        warned = STATE / "credit-warned-on"
        if left < args.warn_under and (not warned.exists() or warned.read_text().strip() != nz_today()):
            warned.write_text(nz_today())
            line += " WARN"
        else:
            line += " OK"
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
