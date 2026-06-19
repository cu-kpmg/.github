from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

CSS_STYLE = """
@page {
    size: A4;
    margin: 2.5cm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 11pt;
}

h1, h2, h3, h4, h5, h6 {
    color: #0f172a;
    font-weight: 700;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    font-size: 24pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.3em;
    margin-top: 0;
    color: #1e3a8a;
}

h2 {
    font-size: 16pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.2em;
    color: #2563eb;
}

h3 {
    font-size: 13pt;
    color: #1e40af;
}

h4 {
    font-size: 11pt;
    color: #334155;
}

p {
    margin-top: 0;
    margin-bottom: 1em;
}

a {
    color: #2563eb;
    text-decoration: none;
}

code {
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, Courier, monospace;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 0.15em 0.3em;
    border-radius: 4px;
    font-size: 9pt;
}

pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 1em;
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
    border-left: 4px solid #3b82f6;
    background-color: #eff6ff;
    padding: 0.75em 1em;
    margin-left: 0;
    margin-right: 0;
    margin-top: 0;
    margin-bottom: 1.5em;
    border-radius: 0 6px 6px 0;
}

blockquote p {
    margin: 0;
    color: #1e40af;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1em;
    margin-bottom: 1.5em;
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
}

tr:nth-child(even) {
    background-color: #f8fafc;
}

hr {
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 2em 0;
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
    excluded_parts = {"profile", ".venv"}
    md_files = [
        p
        for p in root.rglob("*.md")
        if p.stat().st_size > 0 and not any(part in excluded_parts for part in p.parts)
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
