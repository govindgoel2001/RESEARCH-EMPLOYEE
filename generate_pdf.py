#!/usr/bin/env python3
"""Convert Bilasgarh research dossier markdown to PDF with embedded SVG figures."""

import markdown
import os
from weasyprint import HTML, CSS

base_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(base_dir, "bilasgarh_research_dossier.md")
pdf_path = os.path.join(base_dir, "Bilasgarh_Research_Dossier.pdf")

with open(md_path, "r", encoding="utf-8") as f:
    md_text = f.read()

body_html = markdown.markdown(
    md_text,
    extensions=["tables", "toc", "fenced_code", "nl2br"]
)

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Bilasgarh Research Dossier</title>
</head>
<body>
{body_html}
</body>
</html>"""

css = CSS(string="""
@page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @top-center {
        content: "BILASGARH RESEARCH DOSSIER — CONFIDENTIAL AUTHOR BRIEF";
        font-size: 7pt;
        color: #888;
        font-family: 'Georgia', serif;
        letter-spacing: 0.5px;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 7pt;
        color: #888;
        font-family: 'Georgia', serif;
    }
}

@page :first {
    @top-center { content: ""; }
    @bottom-center { content: ""; }
}

/* ── Base Typography ── */
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.65;
    color: #1a1a1a;
}

/* ── Headings ── */
h1 {
    font-family: 'Georgia', serif;
    font-size: 20pt;
    font-weight: bold;
    color: #1a1a1a;
    margin-top: 0;
    margin-bottom: 4pt;
    padding-bottom: 6pt;
    border-bottom: 3px solid #8B0000;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    page-break-after: avoid;
}

h2 {
    font-family: 'Georgia', serif;
    font-size: 14pt;
    font-weight: bold;
    color: #8B0000;
    margin-top: 22pt;
    margin-bottom: 6pt;
    padding-bottom: 3pt;
    border-bottom: 1.5px solid #8B0000;
    text-transform: uppercase;
    letter-spacing: 1px;
    page-break-after: avoid;
}

h3 {
    font-family: 'Georgia', serif;
    font-size: 11.5pt;
    font-weight: bold;
    color: #2c2c2c;
    margin-top: 16pt;
    margin-bottom: 4pt;
    padding-left: 8pt;
    border-left: 3px solid #8B0000;
    page-break-after: avoid;
}

h4 {
    font-family: 'Georgia', serif;
    font-size: 10.5pt;
    font-weight: bold;
    font-style: italic;
    color: #444;
    margin-top: 12pt;
    margin-bottom: 2pt;
    page-break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 7pt;
    orphans: 3;
    widows: 3;
}

h1 + p {
    font-size: 9pt;
    color: #555;
    line-height: 1.9;
    border: 1px solid #ccc;
    background: #f9f9f9;
    padding: 8pt 10pt;
    margin-bottom: 14pt;
}

/* ── Blockquote ── */
blockquote {
    background: #fff3cd;
    border-left: 5px solid #e6ac00;
    margin: 10pt 0 14pt 0;
    padding: 8pt 12pt;
    font-size: 9.5pt;
    color: #5a4000;
    font-style: italic;
}
blockquote p {
    margin: 0;
}

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0 14pt 0;
    font-size: 8.5pt;
    page-break-inside: auto;
}
thead {
    background-color: #8B0000;
    color: #fff;
}
thead th {
    padding: 5pt 7pt;
    text-align: left;
    font-weight: bold;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    font-size: 7.5pt;
}
tbody tr:nth-child(even) {
    background-color: #f5f0ee;
}
tbody tr:nth-child(odd) {
    background-color: #ffffff;
}
tbody td {
    padding: 4.5pt 7pt;
    vertical-align: top;
    border-bottom: 0.5pt solid #ddd;
}
tr { page-break-inside: avoid; }

/* ── Lists ── */
ul, ol {
    margin: 4pt 0 8pt 0;
    padding-left: 18pt;
}
li {
    margin-bottom: 3pt;
    line-height: 1.55;
}
li > ul, li > ol {
    margin-top: 2pt;
    margin-bottom: 2pt;
}

/* ── Code ── */
code {
    font-family: 'Courier New', monospace;
    font-size: 8pt;
    background: #f4f4f4;
    padding: 1pt 3pt;
    border-radius: 2pt;
}

/* ── HR ── */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 14pt 0;
}

/* ── Links ── */
a {
    color: #8B0000;
    text-decoration: none;
}

strong { font-weight: bold; color: #1a1a1a; }
em { font-style: italic; color: #333; }

a[name] { display: block; padding-top: 4pt; }

/* ── IMAGES (SVG figures) ── */
img {
    display: block;
    max-width: 100%;
    width: 100%;
    height: auto;
    margin: 10pt auto;
    page-break-inside: avoid;
    page-break-before: auto;
    page-break-after: auto;
}

/* Cover image — full page feel */
h1 + img {
    margin-top: 2pt;
    margin-bottom: 10pt;
    border: 1px solid #3a2a20;
}

/* Figure caption (the alt text becomes the title attribute) */
""")

print("Generating PDF with embedded figures...")
HTML(string=html_doc, base_url=base_dir).write_pdf(pdf_path, stylesheets=[css])

size_kb = os.path.getsize(pdf_path) // 1024
print(f"PDF saved: {pdf_path}")
print(f"Size: {size_kb} KB")
