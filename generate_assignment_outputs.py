import re
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


INPUT_MD = Path("/workspace/7007SCN_Assignment_Submission_StrictOrdered.md")
OUT_DOCX = Path("/workspace/Final_Assignment_Harsh_Kaushik_17279659.docx")
OUT_PDF = Path("/workspace/Final_Assignment_Harsh_Kaushik_17279659.pdf")


def normalize_text(text: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a3": "GBP ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def set_docx_margins(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)


def add_page_number(run_container):
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run = run_container.add_run()
    run._r.append(fld_char_begin)
    run._r.append(instr_text)
    run._r.append(fld_char_end)


def style_docx_header_footer(doc):
    section = doc.sections[0]
    header = section.header
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.text = "7007SCN Coursework - Harsh Kaushik (17279659)"
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if hp.runs:
        hp.runs[0].font.name = "Calibri"
        hp.runs[0].font.size = Pt(9)
        hp.runs[0].font.color.rgb = RGBColor(68, 68, 68)

    footer = section.footer
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run("Page ")
    fr.font.name = "Calibri"
    fr.font.size = Pt(9)
    fr.font.color.rgb = RGBColor(68, 68, 68)
    add_page_number(fp)


def shade_docx_cell(cell, fill="F5F5F5"):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def parse_blocks(md_text: str):
    blocks = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if stripped == r"\newpage":
            blocks.append(("pagebreak", ""))
            i += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(("code", (lang, "\n".join(code_lines))))
            continue

        img_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if img_match:
            blocks.append(("image", img_match.group(2)))
            i += 1
            continue

        h_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if h_match:
            blocks.append(("heading", (len(h_match.group(1)), h_match.group(2).strip())))
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        para_lines = [raw]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt == r"\newpage" or nxt.startswith("```") or re.match(r"!\[.*\]\(.*\)", nxt) or re.match(r"^#{1,6}\s+", nxt):
                break
            para_lines.append(lines[i])
            i += 1

        text_parts = []
        for idx, ln in enumerate(para_lines):
            text_parts.append(ln.rstrip())
            if idx < len(para_lines) - 1:
                if ln.endswith("  "):
                    text_parts.append("\n")
                else:
                    text_parts.append(" ")
        blocks.append(("paragraph", "".join(text_parts).strip()))
    return blocks


def add_markdown_runs(paragraph, text):
    text = normalize_text(text)
    segments = re.split(r"(\*\*.*?\*\*)", text)
    for seg in segments:
        if not seg:
            continue
        if seg.startswith("**") and seg.endswith("**"):
            run = paragraph.add_run(seg[2:-2])
            run.bold = True
        else:
            paragraph.add_run(seg)


def build_docx(blocks):
    doc = Document()
    set_docx_margins(doc)
    style_docx_header_footer(doc)

    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)

    for block_type, value in blocks:
        if block_type == "pagebreak":
            doc.add_page_break()
        elif block_type == "heading":
            level, text = value
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8 if level <= 2 else 5)
            p.paragraph_format.space_after = Pt(4)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(normalize_text(text))
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.color.rgb = RGBColor(25, 25, 25)
            run.font.size = Pt({1: 16, 2: 13.5, 3: 12, 4: 11}.get(level, 11))
        elif block_type == "paragraph":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.15
            if "\n" in value:
                for idx, line in enumerate(value.split("\n")):
                    add_markdown_runs(p, line)
                    if idx < len(value.split("\n")) - 1:
                        p.add_run().add_break()
            else:
                add_markdown_runs(p, value)
        elif block_type == "code":
            _, code_text = value
            table = doc.add_table(rows=1, cols=1)
            table.autofit = True
            cell = table.cell(0, 0)
            shade_docx_cell(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for idx, line in enumerate(normalize_text(code_text).splitlines() or [""]):
                run = p.add_run(line)
                run.font.name = "Courier New"
                run.font.size = Pt(9.2)
                if idx < len(code_text.splitlines()) - 1:
                    p.add_run().add_break()
            doc.add_paragraph("")
        elif block_type == "image":
            img_path = (INPUT_MD.parent / value).resolve()
            if img_path.exists():
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(str(img_path), width=Inches(6.0))

    doc.save(OUT_DOCX)


def inline_markdown_to_html(text: str) -> str:
    escaped = escape(normalize_text(text))
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    return escaped.replace("\n", "<br/>")


def register_fonts_if_available():
    # Keep robust defaults but use Times if available on machine.
    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    bold_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
    if font_path.exists() and bold_path.exists():
        pdfmetrics.registerFont(TTFont("BodySerif", str(font_path)))
        pdfmetrics.registerFont(TTFont("BodySerif-Bold", str(bold_path)))
        return "BodySerif", "BodySerif-Bold"
    return "Helvetica", "Helvetica-Bold"


def draw_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawCentredString(A4[0] / 2, A4[1] - 1.0 * cm, "7007SCN Coursework - Harsh Kaushik (17279659)")
    canvas.drawCentredString(A4[0] / 2, 0.7 * cm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build_pdf(blocks):
    body_font, bold_font = register_fonts_if_available()
    pdf = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.6 * cm,
    )
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName=body_font,
        fontSize=10.7,
        leading=14,
        spaceAfter=6,
    )
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=bold_font, fontSize=15, leading=18, spaceBefore=8, spaceAfter=6, textColor=colors.HexColor("#111111"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=bold_font, fontSize=13, leading=16, spaceBefore=6, spaceAfter=5, textColor=colors.HexColor("#111111"))
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName=bold_font, fontSize=11.5, leading=14, spaceBefore=5, spaceAfter=4, textColor=colors.HexColor("#111111"))
    code_style = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=8.8,
        leading=11.2,
        leftIndent=8,
        rightIndent=8,
        backColor="#F5F5F5",
        borderColor="#D9D9D9",
        borderWidth=0.5,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=3,
        spaceAfter=5,
    )

    story = []
    for block_type, value in blocks:
        if block_type == "pagebreak":
            story.append(PageBreak())
        elif block_type == "heading":
            level, text = value
            style = h1 if level == 1 else h2 if level == 2 else h3 if level == 3 else normal
            story.append(Paragraph(inline_markdown_to_html(text), style))
        elif block_type == "paragraph":
            story.append(Paragraph(inline_markdown_to_html(value), normal))
        elif block_type == "code":
            _, code_text = value
            story.append(Preformatted(normalize_text(code_text), code_style, dedent=0))
        elif block_type == "image":
            img_path = (INPUT_MD.parent / value).resolve()
            if img_path.exists():
                img = RLImage(str(img_path))
                orig_w, orig_h = img.imageWidth, img.imageHeight
                target_w = 16.0 * cm
                img.drawWidth = target_w
                img.drawHeight = orig_h * (target_w / orig_w)
                story.append(img)
                story.append(Spacer(1, 5))

    pdf.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)


def main():
    md_text = INPUT_MD.read_text(encoding="utf-8")
    blocks = parse_blocks(md_text)
    build_docx(blocks)
    build_pdf(blocks)
    print(f"Created: {OUT_DOCX}")
    print(f"Created: {OUT_PDF}")


if __name__ == "__main__":
    main()
