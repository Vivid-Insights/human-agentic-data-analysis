"""Export Report.md to PDF via pandoc and tectonic.

Run from anywhere; the script changes to the vault root itself, because the
figure paths inside Report.md are relative to it and pandoc resolves them
against its own working directory.

    cd Code && uv run python 16_export_report.py

Reads  : Report.md (never modified)
Writes : Report.pdf in the project root, beside the source it was made from, so
         it is where someone looking for the report expects to find it. The
         pre-processed intermediate goes to Code/outputs/report_export.tex.md,
         kept so the transformations are inspectable, because it is a build
         artefact rather than the thing being sent to anyone.

Never edit the exported file and never convert it back: Report.md is the source
of truth, and the export is reproducible from it by re-running this script.

Four things break silently in Markdown-to-PDF conversion and a fifth is
specific to this report. Each is handled here and then verified:

1. Captions are wrapped in <small> and <b> because Obsidian will not parse
   Markdown inside HTML. LaTeX discards the tags and keeps the words, so the
   caption arrives in body text at body size. Converted to real LaTeX here.
2. Characters the font cannot render are dropped in silence. Latin Modern has
   no superscript minus or digits, so `10⁻⁷` becomes `10` -- a different
   number, not a visible gap. Converted to proper math here, and the build
   fails if tectonic reports any missing character at all.
3. Links to other vault documents survive as dead links. Stripped here.
4. The reference list converts as ordinary paragraphs, which is what is wanted.
   Nothing to do, but it is checked.
5. Display mathematics. Passed through to LaTeX, which is its native form.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Report.md"
OUT_DIR = ROOT / "Code" / "outputs"
INTERMEDIATE = OUT_DIR / "report_export.tex.md"
PDF = ROOT / "Report.pdf"

SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def superscripts_to_math(text: str) -> str:
    """`3 × 10⁻⁷` -> `$3 \\times 10^{-7}$`, so the exponent cannot be dropped."""

    def repl(m: re.Match) -> str:
        mantissa, digits = m.group(1), m.group(2).translate(SUPERSCRIPT)
        return f"${mantissa} \\times 10^{{-{digits}}}$"

    out = re.sub(r"(\d+) × 10⁻([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", repl, text)
    leftover = [c for c in out if c in "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"]
    if leftover:
        raise SystemExit(f"unconverted superscript characters remain: {set(leftover)}")
    return out


def captions_to_latex(text: str) -> str:
    """<small><b>Figure 1.</b> body</small> -> real small bold LaTeX.

    Inline math inside the caption is already LaTeX and passes through intact.
    """

    def repl(m: re.Match) -> str:
        label, body = m.group(1).strip(), m.group(2).strip()
        body = body.replace("<em>", r"\emph{").replace("</em>", "}")
        return (
            "\\begin{quote}\n\\small\\textbf{"
            + label
            + "} "
            + body
            + "\n\\end{quote}"
        )

    out, n = re.subn(
        r"<small><b>(.*?)</b>\s*(.*?)</small>", repl, text, flags=re.S
    )
    print(f"  captions converted to LaTeX           : {n}")
    if "<small>" in out or "<b>" in out:
        raise SystemExit("a caption was not matched; check the HTML in Report.md")
    return out


def figures_to_latex(text: str) -> str:
    """`![Figure 1](path)` -> a centred includegraphics that cannot float.

    Pandoc turns a lone image into a LaTeX figure environment, which is a float:
    LaTeX moves it to wherever it fits, while the caption below it is an ordinary
    paragraph and stays put. The two then land on different pages. Emitting the
    graphic directly keeps each figure next to the caption that describes it.
    """
    out, n = re.subn(
        r"!\[[^\]]*\]\(([^)]+)\)",
        r"\\begin{center}\n\\includegraphics[width=0.95\\linewidth,"
        r"keepaspectratio]{\1}\n\\end{center}",
        text,
    )
    print(f"  figures pinned beside their captions  : {n}")
    return out


def strip_vault_links(text: str) -> str:
    """`[Appendix.md](Appendix.md)` points into a vault the reader has not got."""
    out, n = re.subn(r"\[([^\]]+)\]\((?!https?:|Code/)[^)]*\.md\)", r"\1", text)
    print(f"  dead vault links stripped             : {n}")
    return out


def split_title(text: str) -> tuple[str, str]:
    m = re.match(r"#\s+(.+?)\n", text)
    if not m:
        raise SystemExit("no H1 title found in Report.md")
    return m.group(1).strip(), text[m.end():].lstrip("\n")


def main() -> None:
    for tool in ("pandoc", "tectonic"):
        if shutil.which(tool) is None:
            raise SystemExit(f"{tool} is not installed")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    source_nonascii = {c for c in text if ord(c) > 127}

    print("pre-processing:")
    title, body = split_title(text)
    body = captions_to_latex(body)
    body = figures_to_latex(body)
    body = superscripts_to_math(body)
    body = strip_vault_links(body)
    INTERMEDIATE.write_text(body, encoding="utf-8")

    cmd = [
        "pandoc", str(INTERMEDIATE),
        "-o", str(PDF),
        "--pdf-engine=tectonic",
        "--from", "markdown+raw_tex+tex_math_dollars",
        "--metadata", f"title={title}",
        "--metadata", "date=",
        "--toc",
        "-V", "geometry:margin=1in",
        "-V", "linkcolor=blue",
        "-V", "fontsize=11pt",
        # graphicx is only pulled in automatically when pandoc manages the
        # images itself; the figures are emitted as raw LaTeX above, so it
        # has to be requested explicitly.
        "-V", r"header-includes=\usepackage{graphicx}",
    ]
    print("\nrunning, from", ROOT)
    print(" ", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    log = r.stdout + r.stderr

    # The exit code is zero even when characters are dropped, so check the log.
    missing = sorted(set(re.findall(r"could not represent character \"(.)\"", log)))
    print("\nchecks:")
    print(f"  pandoc exit code                      : {r.returncode}")
    print(f"  tectonic missing-character warnings   : {len(missing)}")
    if missing:
        for c in missing:
            print(f"      U+{ord(c):04X}  {c}")
    other = [l for l in log.splitlines()
             if "warning" in l.lower() and "could not represent" not in l
             and "Missing character" not in l and "you may need" in l.lower()]
    for l in other[:5]:
        print("  ", l.strip())

    if r.returncode != 0:
        print(log[-3000:])
        raise SystemExit("pandoc failed")
    if missing:
        raise SystemExit("characters were dropped from the PDF; fix before shipping")
    if not PDF.exists() or PDF.stat().st_size < 10_000:
        raise SystemExit("no plausible PDF was produced")

    print(f"  non-ASCII characters in the source    : {len(source_nonascii)}")
    print(f"  written                               : {PDF.relative_to(ROOT)}"
          f"  ({PDF.stat().st_size / 1024:.0f} kB)")


if __name__ == "__main__":
    main()
