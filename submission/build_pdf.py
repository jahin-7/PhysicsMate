"""Convert REPORT.md -> a print-styled HTML, for Chrome headless -> PDF.
Handles the Markdown subset the report uses: #/##/### headings, GFM pipe
tables, - and 1. lists, ``` code fences, > blockquotes, --- rules,
**bold**, `code`, and *italics*."""
import html
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "REPORT.md"
OUT = HERE / "report_print.html"


def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.strip().startswith("```"):                       # code fence
            i += 1; buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            i += 1
            out.append("<pre>" + "\n".join(buf) + "</pre>"); continue

        if re.match(r"^\s*\|.*\|\s*$", ln) and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i+1]):
            header = cells(ln); i += 2; rows = []
            while i < len(lines) and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                rows.append(cells(lines[i])); i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in header] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t)); continue

        if ln.startswith("### "): out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        if ln.startswith("## "):  out.append(f"<h2>{inline(ln[3:])}</h2>"); i += 1; continue
        if ln.startswith("# "):   out.append(f"<h1>{inline(ln[2:])}</h1>"); i += 1; continue
        if ln.strip() == "---":   out.append("<hr>"); i += 1; continue

        if ln.startswith(">"):                                  # blockquote
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(inline(lines[i].lstrip(">").strip())); i += 1
            out.append("<blockquote>" + "<br>".join(buf) + "</blockquote>"); continue

        if re.match(r"^\s*[-*] ", ln):                          # ul
            buf = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                item = re.sub(r"^\s*[-*] ", "", lines[i]); buf.append(f"<li>{inline(item)}</li>"); i += 1
            out.append("<ul>" + "".join(buf) + "</ul>"); continue

        if re.match(r"^\s*\d+\. ", ln):                         # ol
            buf = []
            while i < len(lines) and re.match(r"^\s*\d+\. ", lines[i]):
                item = re.sub(r"^\s*\d+\. ", "", lines[i]); buf.append(f"<li>{inline(item)}</li>"); i += 1
            out.append("<ol>" + "".join(buf) + "</ol>"); continue

        if ln.strip() == "": i += 1; continue
        para = [ln]; i += 1                                     # paragraph
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||```|\s*[-*] |\s*\d+\. |---)", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1a1a1f;
  font-size: 10.5pt; line-height: 1.5; max-width: 100%; }
h1 { font-size: 20pt; color: #0d857f; margin: 0 0 4pt; line-height: 1.2; }
h1 + h3 { color: #555; font-weight: 500; margin-top: 0; }
h2 { font-size: 14pt; color: #0d857f; border-bottom: 1.5pt solid #14a8a0; padding-bottom: 3pt; margin: 20pt 0 8pt; }
h3 { font-size: 11.5pt; color: #14a8a0; margin: 12pt 0 4pt; }
p { margin: 5pt 0; }
ul, ol { margin: 5pt 0; padding-left: 18pt; }
li { margin: 2pt 0; }
strong { color: #0d3d3a; }
code { font-family: "SF Mono", Menlo, monospace; font-size: 9pt; background: #eef6f5; padding: 1pt 3pt; border-radius: 3px; }
pre { font-family: "SF Mono", Menlo, monospace; font-size: 8pt; line-height: 1.35; background: #f4f9f8;
  border: 0.5pt solid #cfe6e3; border-radius: 5px; padding: 8pt; overflow-x: auto; white-space: pre; }
blockquote { margin: 6pt 0; padding: 6pt 10pt; background: #fff7e6; border-left: 3pt solid #e0a52b; font-size: 9.5pt; color: #5a4a20; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9pt; }
th, td { border: 0.5pt solid #bcd; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #14a8a0; color: #fff; font-weight: 600; }
tr:nth-child(even) td { background: #f4f9f8; }
h2, h3 { break-after: avoid; }
table, pre, blockquote { break-inside: avoid; }
"""


def for_version(md, v):
    """v1: drop the whole §10 failures block. v2: keep §10 but drop the v3-only
    evidence-trail paragraph. v3: keep everything. Marker comments are stripped
    either way."""
    if v == 1:
        md = re.sub(r"<!--V2START-->.*?<!--V2END-->", "", md, flags=re.DOTALL)
    elif v == 2:
        md = re.sub(r"<!--V3START-->.*?<!--V3END-->", "", md, flags=re.DOTALL)
    md = re.sub(r"<!--/?V[23](START|END)?-->", "", md)
    return md.rstrip() + "\n"


def main():
    src = SRC.read_text(encoding="utf-8")
    for v in (1, 2, 3):
        body = convert(for_version(src, v))
        doc = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
        out = HERE / f"report_v{v}.html"
        out.write_text(doc, encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
