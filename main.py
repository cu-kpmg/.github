from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

CSS_STYLE = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #334155; /* Slate 700 */
    line-height: 1.625;
    font-size: 10.5pt;
}

h1, h2, h3, h4, h5, h6 {
    color: #0f172a; /* Slate 900 */
    font-weight: 700;
    margin-top: 1.75em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h1 {
    font-size: 26pt;
    border-bottom: 3px solid #6366f1; /* Indigo accent border */
    padding-bottom: 0.3em;
    margin-top: 0;
    color: #4338ca; /* Indigo-700 */
}

h2 {
    font-size: 17pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.25em;
    color: #1e3a8a; /* Deep blue */
}

h3 {
    font-size: 13pt;
    color: #2563eb; /* Blue-600 */
}

h4 {
    font-size: 11pt;
    color: #475569; /* Slate-600 */
}

p {
    margin-top: 0;
    margin-bottom: 1em;
}

a {
    color: #4f46e5;
    text-decoration: none;
    font-weight: 500;
}

ul, ol {
    margin-top: 0;
    margin-bottom: 1.2em;
    padding-left: 1.5em;
}

li {
    margin-bottom: 0.4em;
}

code {
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, Courier, monospace;
    background-color: #f1f5f9; /* Slate-100 */
    color: #0f172a;
    padding: 0.15em 0.3em;
    border-radius: 4px;
    font-size: 9pt;
}

pre {
    background-color: #0f172a; /* Slate-900 */
    border-left: 4px solid #6366f1; /* Left indigo accent strip */
    color: #f8fafc;
    padding: 1.25em;
    border-radius: 6px;
    overflow-x: auto;
    margin-top: 0;
    margin-bottom: 1.5em;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
    font-size: 8.5pt;
}

blockquote {
    border-left: 4px solid #3b82f6; /* Blue-500 */
    background-color: #f8fafc; /* Slate-50 */
    padding: 1em 1.25em;
    margin-left: 0;
    margin-right: 0;
    margin-top: 0;
    margin-bottom: 1.5em;
    border-radius: 0 6px 6px 0;
}

blockquote p {
    margin: 0;
    color: #334155;
    font-style: italic;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.25em;
    margin-bottom: 1.5em;
    font-size: 9.5pt;
}

th, td {
    padding: 0.75em 1em;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

th {
    background-color: #f8fafc;
    color: #0f172a;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.05em;
    border-bottom: 2px solid #cbd5e1;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

hr {
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 2.25em 0;
}
"""


def convert_md_to_pdf(md_path: Path) -> None:
    pdf_path = md_path.with_suffix(".pdf")
    content = md_path.read_text(encoding="utf-8")

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(content, root=str(md_path.parent)), user_css=CSS_STYLE)
    pdf.meta["title"] = md_path.stem
    pdf.save(str(pdf_path))

    print(f"  Created: {pdf_path.relative_to(Path.cwd())}")


def sort_key(p: Path) -> tuple:
    result = []
    for part in p.parts:
        stem = part
        if part.endswith(".md"):
            stem = part[:-3]
        if stem.isdigit():
            result.append((0, int(stem)))
        else:
            result.append((1, stem.lower()))
    return tuple(result)


def main():
    root = Path(__file__).parent
    lectures_dir = root / "lectures"
    md_files = [
        p
        for p in lectures_dir.rglob("*.md")
        if p.stat().st_size > 0
    ]

    if not md_files:
        print("No .md files found.")
        return

    print(f"Found {len(md_files)} markdown file(s). Converting...\n")
    errors = []

    for md_file in sorted(md_files, key=sort_key):
        try:
            convert_md_to_pdf(md_file)
        except Exception as exc:
            errors.append((md_file, exc))
            print(f"  ERROR: {md_file.relative_to(root)} — {exc}")

    print(f"\nDone. {len(md_files) - len(errors)} converted, {len(errors)} failed.")


if __name__ == "__main__":
    main()
