#!/usr/bin/env bash
# Create or update the reproducible Python environment for this workspace.
#
# Usage:  cd Code && ./setup_env.sh
#
# Reads:    pyproject.toml, uv.lock, .python-version
# Produces: Code/.venv/  (git-ignored)
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
    cat >&2 <<'MSG'
Error: uv is not installed.

uv manages the Python version and all packages for this workspace. Install it with:

    curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS / Linux

then re-run this script. See https://docs.astral.sh/uv/getting-started/installation/
MSG
    exit 1
fi

echo "Syncing environment from uv.lock ..."
uv sync --frozen 2>/dev/null || {
    echo "No usable lockfile found; resolving from pyproject.toml instead."
    uv sync
}

echo
uv run python check_env.py

cat <<'MSG'

Environment ready at Code/.venv

Run analysis code with:      cd Code && uv run python your_script.py
Start a notebook with:       cd Code && uv run jupyter lab
Add a package with:          cd Code && uv add <package>   (updates uv.lock)
MSG
