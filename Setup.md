# Setup

*Part of the [Data Analysis Workspace](README.md) — the analysis code this environment runs is described in [Appendix.md](Appendix.md#code-summary).*

Everything needed to get the workspace running. Do this once per machine.

## 1. Obsidian

Choose *Open folder as vault* and select this folder. The vault's settings — attachment folder, file visibility, link format — come with the repository, so there is nothing to configure.

Install the [Claudian](https://github.com/YishenTu/claudian) community plugin (Settings → Community plugins → Browse → "Claudian"). It embeds Claude Code in the vault and is what makes the workspace agentic. Desktop only, and it needs Obsidian 1.13 or later. The vault is already configured to enable it once installed.

Claudian does not include the agent itself: it drives an agent CLI that has to be installed and signed in separately. This workspace is written for Claude Code. Install it following <https://code.claude.com/docs/en/setup>, then run `claude` once in a terminal and sign in with a Claude subscription or an Anthropic API key. Check that Claude Code is the provider selected in Claudian's settings before starting a conversation.

## 2. uv

[uv](https://docs.astral.sh/uv/) manages the Python version and every analysis package.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS / Linux
```

Other platforms and installation methods: <https://docs.astral.sh/uv/getting-started/installation/>

## 3. The Python environment

One command, from the repository root:

```bash
cd Code && ./setup_env.sh
```

This reads `Code/uv.lock`, creates `Code/.venv`, and finishes by printing the exact versions it installed. Everyone who clones the repository gets the same environment, so results reproduce.

Re-run the same command any time `uv.lock` changes — for instance after pulling someone else's work.

## Everyday commands

All Python runs inside the workspace environment, never the system Python:

```bash
cd Code
uv run python my_analysis.py     # run a script
uv run jupyter lab               # notebooks
uv run python check_env.py       # print interpreter and package versions
uv add <package>                 # add a dependency, updating uv.lock
```

`uv run` syncs the environment against `uv.lock` before executing, so a stale `.venv` cannot silently change a result.

**If you add a dependency**, commit the updated `uv.lock` so collaborators pick it up on their next `./setup_env.sh`, and note the addition in [Appendix — Code Summary](Appendix.md#code-summary).

## What the environment contains

| Component | Version |
| --- | --- |
| Python | 3.12.13 |
| pandas | 3.0.5 |
| numpy | 2.5.2 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.1 |
| seaborn | 0.13.2 |
| pyarrow | 25.0.1 |
| openpyxl | 3.1.5 |

Plus `xlrd` for legacy `.xls`, `tabulate` for Markdown tables, and JupyterLab with `ipykernel`. Verified by `uv run python check_env.py` on 2026-09-01.

Record this output in [Appendix.md](Appendix.md) whenever package versions could affect a result.

## Files that define the environment

| Path | Role |
| --- | --- |
| `Code/pyproject.toml` | Declares the Python version and the analysis packages. |
| `Code/uv.lock` | Exact resolved version of every package. **Committed**, so environments match across machines. Do not edit by hand. |
| `Code/.python-version` | Pins the interpreter to Python 3.12 for `uv`. |
| `Code/setup_env.sh` | Creates or updates `Code/.venv` from the lockfile, then verifies it. |
| `Code/check_env.py` | Prints the interpreter path and installed versions; exits non-zero if anything is missing. |
| `Code/.venv/` | The environment itself. Git-ignored and excluded from the Obsidian index — rebuild it, never commit it. |

## Exporting the report (step 8 only)

Nothing before step 8 needs these, so they are not installed as part of the setup above. Install them when you actually want a file to send someone, and only for the format you want.

**Word (`.docx`)** needs a converter. [Pandoc](https://pandoc.org/installing.html) is the usual one:

```bash
brew install pandoc            # macOS
sudo apt install pandoc        # Debian / Ubuntu
```

Then, from the vault root, so the figure paths in the document resolve:

```bash
pandoc Report.md --from markdown -o Code/outputs/report.docx
```

**PDF** needs a LaTeX engine as well as the converter, which is a considerably larger install. [Tectonic](https://tectonic-typesetting.github.io/) is a single self-contained binary and downloads only the packages a document actually uses:

```bash
brew install tectonic
pandoc Report.md --from markdown --pdf-engine=tectonic -o Code/outputs/report.pdf
```

A full TeX distribution (MacTeX, TeX Live) works too and is several gigabytes.

Two things to check in the output rather than trust:

- **Captions.** They are wrapped in `<small>` and `<b>` so Obsidian renders them correctly. Converting keeps the words and drops the tags, so the caption arrives at body size and stops reading as a legend.
- **Unusual characters.** A default LaTeX font has no Greek letters or superscript signs. They are dropped silently, the exit code is zero, and a p-value written `1 × 10⁻¹³` can come out as `1 × 1013` — a different number rather than a visible gap. Search the PDF for every non-ASCII character the source contains.

Record whatever you install in the version table above, so the export can be reproduced.

## Troubleshooting

**`uv: command not found`** — uv is not on your `PATH`. Restart the shell after installing, or see the installation link in step 2.

**`check_env.py` reports a missing package** — run `cd Code && ./setup_env.sh` again. If it still fails, delete `Code/.venv` and re-run; the environment rebuilds from the lockfile in seconds.

**A result changed and you don't know why** — run `cd Code && uv run python check_env.py` and compare against the table above. If versions differ, someone changed `uv.lock`; `git log -- Code/uv.lock` will show when.

**Obsidian is slow or the file explorer is cluttered** — confirm `Code/.venv` is listed under Settings → Files and links → Excluded files. It ships excluded, but a fresh vault-settings file would drop that.
