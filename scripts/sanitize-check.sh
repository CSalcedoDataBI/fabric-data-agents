#!/usr/bin/env bash
# Public sanitization guard for the fabric-data-agents repository.
#
# Fails if the tree contains anything that should never be public:
#   1. a GUID          -> real Fabric IDs are GUIDs; the repo uses named placeholders
#   2. a deployed-app  -> real *.fabricapps.net hostnames (a live endpoint)
#   3. TODO-SANITIZE   -> a leftover "clean me before publishing" marker
#
# This is the public backstop. The front line is a PRIVATE denylist of actual client
# tokens, run in the source repository before anything is copied here (see SANITIZATION.md).
#
# Usage: scripts/sanitize-check.sh        (run from the repo root)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Files/dirs the guard must not scan: the guard script and the sanitization policy
# both NAME these patterns to document them, so scanning them is a false positive.
EXCLUDES=(--exclude-dir=.git --exclude="sanitize-check.sh" --exclude="SANITIZATION.md")

fail=0
report() { # <label> <pattern>
  local label="$1" pattern="$2" hits
  # -I skip binary, -r recurse, -n line numbers, -E extended regex
  if hits="$(grep -rInE "${EXCLUDES[@]}" -- "$pattern" . 2>/dev/null)"; then
    echo "FAIL: $label"
    echo "$hits"
    echo
    fail=1
  fi
}

# 1) GUID (hex 8-4-4-4-12). Placeholders like <workspace-id> or xxxxxxxx-... do not match.
report "GUID found (use a <...-id> placeholder instead)" \
  '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

# 2) Deployed-app hostname. A real subdomain label before .fabricapps.net; "*.fabricapps.net"
#    (a wildcard mention in docs) does not match because "*" is not a label character.
report "Live app hostname found (use https://<your-validator-app>.example)" \
  '[a-z0-9][a-z0-9-]*\.fabricapps\.net'

# 3) Leftover sanitize marker.
report "TODO-SANITIZE marker left in the tree" 'TODO-SANITIZE'

if [ "$fail" -ne 0 ]; then
  echo "Sanitization guard FAILED. See matches above."
  exit 1
fi
echo "Sanitization guard passed: no GUIDs, live hostnames, or TODO-SANITIZE markers."
