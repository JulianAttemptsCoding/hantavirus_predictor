"""Convert manuscript_eid.md to EID-formatted manuscript_eid.docx.

EID format: 12-pt Times New Roman, double-spaced, left-justified.
Tables are built as Word tables. Line numbering must be enabled manually in Word.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches
ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "submission_eid" / "manuscript_eid.md"
DOCX_PATH = ROOT / "docs" / "submission_eid" / "manuscript_eid.docx"
COVER_MD_PATH = ROOT / "docs" / "submission_eid" / "cover_letter_eid.md"
COVER_DOCX_PATH = ROOT / "docs" / "submission_eid" / "cover_letter_eid.docx"
STATEMENTS_MD_PATH = ROOT / "docs" / "submission_eid" / "author_statements.md"
STATEMENTS_DOCX_PATH = ROOT / "docs" / "submission_eid" / "author_statements.docx"
APPENDIX_MD_PATH = ROOT / "docs" / "submission_eid" / "supplements" / "Appendix_methods_eid.md"
APPENDIX_DOCX_PATH = ROOT / "docs" / "submission_eid" / "supplements" / "Appendix_methods_eid.docx"


def _set_font(
    run,
    bold: bool = False,
    italic: bool = False,
    size: int = 12,
    font_name: str = "Times New Roman",
) -> None:
    run.font.name = font_name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def _para_format(para, space_before: int = 0, space_after: int = 0) -> None:
    para.paragraph_format.space_before = Pt(space_before)
    para.paragraph_format.space_after = Pt(space_after)
    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE


def _enable_line_numbering(doc: Document) -> None:
    for section in doc.sections:
        sect_pr = section._sectPr
        existing = sect_pr.find(qn("w:lnNumType"))
        if existing is not None:
            sect_pr.remove(existing)
        ln_num = OxmlElement("w:lnNumType")
        ln_num.set(qn("w:start"), "1")
        ln_num.set(qn("w:countBy"), "1")
        ln_num.set(qn("w:restart"), "continuous")
        sect_pr.append(ln_num)


def _add_marked_runs(para, text: str, size: int = 12, font_name: str = "Times New Roman") -> None:
    text = text.replace("`", "")
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = para.add_run(part[2:-2])
            _set_font(run, bold=True, size=size, font_name=font_name)
        elif part.startswith("*") and part.endswith("*"):
            run = para.add_run(part[1:-1])
            _set_font(run, italic=True, size=size, font_name=font_name)
        else:
            run = para.add_run(part)
            _set_font(run, size=size, font_name=font_name)


def _add_heading(doc: Document, text: str, level: int) -> None:
    para = doc.add_paragraph()
    _para_format(para, space_before=6, space_after=0)
    run = para.add_run(text)
    _set_font(run, bold=True, size=12)


def _add_body(doc: Document, text: str, italic: bool = False) -> None:
    if not text.strip():
        return
    para = doc.add_paragraph()
    _para_format(para)
    if italic:
        run = para.add_run(text)
        _set_font(run, italic=True)
    else:
        _add_marked_runs(para, text)


def _add_table(doc: Document, header: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(header))
    # Header row
    for i, cell_text in enumerate(header):
        cell = table.rows[0].cells[i]
        _add_marked_runs(cell.paragraphs[0], cell_text, size=8, font_name="Arial")
        for run in cell.paragraphs[0].runs:
            run.bold = True
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, cell_text in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            _add_marked_runs(cell.paragraphs[0], cell_text, size=8, font_name="Arial")
    doc.add_paragraph()  # spacer after table


def _parse_md_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    header: list[str] = []
    rows: list[list[str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.match(r"^[-: ]+$", c) for c in cells):
            continue  # separator row
        if not header:
            header = cells
        else:
            rows.append(cells)
    return header, rows


def build_docx(md_path: Path, docx_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    doc = Document()

    # Set default style
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)

    # Set margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    lines = text.split("\n")
    i = 0
    in_table = False
    table_lines: list[str] = []
    skip_note = False

    while i < len(lines):
        line = lines[i]

        # Skip NOTE TO AUTHOR lines
        if line.startswith("**NOTE TO AUTHOR"):
            skip_note = True
        if skip_note:
            if line.strip() == "" and i > 0:
                skip_note = False
            i += 1
            continue

        # Skip markdown front matter / horizontal rules
        if line.startswith("---") and len(line.strip()) == 3:
            i += 1
            continue

        # Table handling
        if line.startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            in_table = False
            header, rows = _parse_md_table(table_lines)
            if header:
                _add_table(doc, header, rows)
            table_lines = []

        # Skip [NOTE TO AUTHOR...] inline notes
        if line.startswith("[NOTE TO AUTHOR"):
            i += 1
            continue

        # H1 title (# heading)
        if line.startswith("# ") and not line.startswith("## "):
            run_text = line[2:].strip()
            para = doc.add_paragraph()
            _para_format(para, space_before=0, space_after=6)
            run = para.add_run(run_text)
            _set_font(run, bold=True, size=14)
            i += 1
            continue

        # H2 heading
        if line.startswith("## "):
            _add_heading(doc, line[3:].strip(), 2)
            i += 1
            continue

        # H3 heading
        if line.startswith("### "):
            _add_heading(doc, line[4:].strip(), 3)
            i += 1
            continue

        # H4 heading
        if line.startswith("#### "):
            para = doc.add_paragraph()
            _para_format(para, space_before=6)
            run = para.add_run(line[5:].strip())
            _set_font(run, bold=True, italic=True, size=12)
            i += 1
            continue

        # Bold **text** lines (like field labels in title page)
        if line.startswith("**") and line.count("**") >= 2:
            # Check if it's a label: value line
            clean = line.replace("**", "")
            para = doc.add_paragraph()
            _para_format(para)
            run = para.add_run(clean)
            _set_font(run)
            i += 1
            continue

        # Empty line → paragraph break
        if line.strip() == "":
            i += 1
            continue

        # Regular paragraph
        _add_body(doc, line)
        i += 1

    # Handle any remaining table
    if in_table and table_lines:
        header, rows = _parse_md_table(table_lines)
        if header:
            _add_table(doc, header, rows)

    _enable_line_numbering(doc)
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(docx_path)
    print(f"Saved: {docx_path}")


if __name__ == "__main__":
    build_docx(MD_PATH, DOCX_PATH)
    build_docx(COVER_MD_PATH, COVER_DOCX_PATH)
    build_docx(STATEMENTS_MD_PATH, STATEMENTS_DOCX_PATH)
    build_docx(APPENDIX_MD_PATH, APPENDIX_DOCX_PATH)
