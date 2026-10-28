#!/usr/bin/env bash
# Add the smart-contracting-dream-team overlay to a Hermes agent that is already running on this computer.
# Usage: install/install.sh <role>     roles: revenue-partner
set -euo pipefail

ROLE="${1:-}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
VAULT_DIR="${VAULT_DIR:-$HOME/PartnerDesk}"   # the partner ledger lives here
ROLES="revenue-partner"

fail() { printf '\nInstall stopped: %s\n' "$*" >&2; exit 1; }

case " $ROLES " in
  *" $ROLE "*) [ -n "$ROLE" ] || fail "say which computer this is: install/install.sh <one of: $ROLES>" ;;
  *) fail "say which computer this is: install/install.sh <one of: $ROLES>" ;;
esac

command -v python3 >/dev/null 2>&1 || fail "python3 is missing"
[ -d "$HERMES_HOME" ] || fail "no Hermes home at $HERMES_HOME. This overlay goes on a computer that already runs Hermes"
# The skills and routines read ~/.hermes/scdt, so a Hermes home anywhere else would install where nothing looks.
[ "$HERMES_HOME" = "$HOME/.hermes" ] || [ -n "${SCDT_ALLOW_OTHER_HOME:-}" ] || \
  fail "HERMES_HOME is $HERMES_HOME, but the scdt- skills read $HOME/.hermes. Ask Justin's team"

echo "smart-contracting-dream-team overlay: $ROLE"
echo "Adds skills, routines and policies. Leaves SOUL.md, config, .env, memory, the existing outreach skills and crons alone."

# The skills point at ~/smart-contracting-dream-team, so the repo must live there.
if [ "$REPO_DIR" != "$HOME/smart-contracting-dream-team" ]; then
  echo "Note: this copy is at $REPO_DIR, but the skills expect $HOME/smart-contracting-dream-team."
  echo "      Move it there (or symlink it) before using the scdt- skills."
fi

python3 "$REPO_DIR/install/sync_overlay.py" "$REPO_DIR" "$HERMES_HOME" "$ROLE" "$VAULT_DIR"

# The partner ledger: creates empty CSVs and terms.json the first time; never overwrites records.
python3 "$REPO_DIR/tools/partner_ledger.py" --dir "$VAULT_DIR" init
python3 "$REPO_DIR/tools/partner_ledger.py" --dir "$VAULT_DIR" check || true

SOURCES="$HERMES_HOME/scdt/context/sources.md"
if [ ! -f "$SOURCES" ]; then
  cp "$REPO_DIR/client-context/sources.template.md" "$SOURCES"
  echo "Wrote $SOURCES from the template. START-HERE Step 1 fills in the real paths."
fi

# Each routine has a UTC schedule (CRON:) and an NZ one (CRON_NZ:). START-HERE Step 4 picks one; nothing here changes the clock.
echo "Hermes time zone: ${HERMES_TIMEZONE:-not set} (START-HERE Step 4 picks CRON or CRON_NZ from this)."

# SKIP_HERMES_CLI=1 for dry runs against a throwaway HERMES_HOME: the hermes CLI bootstraps a full install there.
if [ -z "${SKIP_HERMES_CLI:-}" ] && command -v hermes >/dev/null 2>&1; then
  n="$(hermes skills list 2>/dev/null | grep -c "scdt-" || true)"
  echo "Hermes sees ${n:-0} scdt skills."
fi

# Step 1 (the inventory) fills sources.md. If it still says UNKNOWN for the key paths, it hasn't run yet.
STEPS="Steps 3 to 6"
if grep -Eq '^(tracker|replies|send_with):[[:space:]]+UNKNOWN' "$SOURCES"; then
  STEPS="Step 1, then Steps 3 to 6"
  echo "sources.md still has UNKNOWN paths, so the inventory (Step 1) comes first."
fi

cat <<TEXT

Done. Next, send this agent:

  Read ~/smart-contracting-dream-team/START-HERE.md and do $STEPS for the $ROLE role.
  Create every routine paused. Ask me in plain English before anything goes live.

TEXT
