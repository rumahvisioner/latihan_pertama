from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUTPUT = Path("PRD Landing Page Jasa - Mohamad Arif Pramarta - Integrasi Superprof v1.2.docx")
SUPERPROF_URL = "https://www.superprof.co.id/lulusan-statistika-ipb-konsultan-staf-ahli-menteri-bappenas-400-sesi-sejak-2022-smpcpnsprofesional-internasional.html"

# standard_business_brief preset + named title/callout overrides.
COLORS = {
    "navy": "0B2545",
    "blue": "2E74B5",
    "dark_blue": "1F4D78",
    "ink": "1F2937",
    "muted": "5B6573",
    "light_gray": "F2F4F7",
    "blue_gray": "E8EEF5",
    "callout": "F4F6F9",
    "white": "FFFFFF",
    "border": "C9D2DC",
    "amber": "7A5A00",
    "red": "9B1C1C",
    "green": "1F5D42",
}


def rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color)


def set_cell_shading(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_row_cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def set_table_geometry(table, widths_dxa, indent_dxa=120):
    table.autofit = False
    tbl_pr = table._tbl.tblPr

    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(sum(widths_dxa)))
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent_dxa))
    tbl_ind.set(qn("w:type"), "dxa")

    layout = tbl_pr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            width = widths_dxa[idx]
            cell.width = Inches(width / 1440)
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(width))
            tc_w.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_table_borders(table, color="C9D2DC", size="4"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), size)
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), color)


def style_table(table, widths_dxa, header=True, font_size=9.2):
    set_table_geometry(table, widths_dxa)
    set_table_borders(table)
    for r_idx, row in enumerate(table.rows):
        set_row_cant_split(row)
        if r_idx == 0 and header:
            set_repeat_table_header(row)
        for cell in row.cells:
            if r_idx == 0 and header:
                set_cell_shading(cell, COLORS["light_gray"])
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.05
                for run in p.runs:
                    set_run_font(run, size=font_size, color=COLORS["ink"], bold=(r_idx == 0 and header))


def set_run_font(run, name="Calibri", size=None, color=None, bold=None, italic=None):
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    r_fonts.set(qn("w:ascii"), name)
    r_fonts.set(qn("w:hAnsi"), name)
    r_fonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = rgb(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    lang = r_pr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        r_pr.append(lang)
    lang.set(qn("w:val"), "id-ID")


def set_paragraph_border(paragraph, edge="bottom", color="2E74B5", size="8", space="4"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    border = p_bdr.find(qn(f"w:{edge}"))
    if border is None:
        border = OxmlElement(f"w:{edge}")
        p_bdr.append(border)
    border.set(qn("w:val"), "single")
    border.set(qn("w:sz"), size)
    border.set(qn("w:space"), space)
    border.set(qn("w:color"), color)


def shade_paragraph(paragraph, fill="F4F6F9"):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = p_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        p_pr.append(shd)
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")


def add_hyperlink(paragraph, text, url, color="2E74B5", underline=True):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), "Calibri")
    r_fonts.set(qn("w:hAnsi"), "Calibri")
    r_pr.append(r_fonts)
    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    r_pr.append(c)
    if underline:
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        r_pr.append(u)
    new_run.append(r_pr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_field(paragraph, instruction, fallback="1"):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = fallback
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instr, separate, text, end):
        run = OxmlElement("w:r")
        run.append(element)
        paragraph._p.append(run)


def add_custom_numbering(doc):
    numbering = doc.part.numbering_part.element
    existing_abs = [int(x.get(qn("w:abstractNumId"))) for x in numbering.findall(qn("w:abstractNum"))]
    existing_nums = [int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))]
    next_abs = max(existing_abs, default=0) + 1
    next_num = max(existing_nums, default=0) + 1

    def insert_abstract(abstract):
        # OOXML requires every abstractNum before the first concrete num.
        insert_at = next(
            (idx for idx, child in enumerate(numbering) if child.tag == qn("w:num")),
            len(numbering),
        )
        numbering.insert(insert_at, abstract)

    def insert_num(num):
        cleanup = numbering.find(qn("w:numIdMacAtCleanup"))
        if cleanup is None:
            numbering.append(num)
        else:
            numbering.insert(list(numbering).index(cleanup), num)

    def build_abstract(abs_id, fmt, lvl_text, font=None):
        abstract = OxmlElement("w:abstractNum")
        abstract.set(qn("w:abstractNumId"), str(abs_id))
        multi = OxmlElement("w:multiLevelType")
        multi.set(qn("w:val"), "singleLevel")
        abstract.append(multi)
        lvl = OxmlElement("w:lvl")
        lvl.set(qn("w:ilvl"), "0")
        start = OxmlElement("w:start")
        start.set(qn("w:val"), "1")
        lvl.append(start)
        num_fmt = OxmlElement("w:numFmt")
        num_fmt.set(qn("w:val"), fmt)
        lvl.append(num_fmt)
        text_el = OxmlElement("w:lvlText")
        text_el.set(qn("w:val"), lvl_text)
        lvl.append(text_el)
        jc = OxmlElement("w:lvlJc")
        jc.set(qn("w:val"), "left")
        lvl.append(jc)
        p_pr = OxmlElement("w:pPr")
        tabs = OxmlElement("w:tabs")
        tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "num")
        tab.set(qn("w:pos"), "720")
        tabs.append(tab)
        p_pr.append(tabs)
        ind = OxmlElement("w:ind")
        ind.set(qn("w:left"), "720")
        ind.set(qn("w:hanging"), "360")
        p_pr.append(ind)
        lvl.append(p_pr)
        if font:
            r_pr = OxmlElement("w:rPr")
            r_fonts = OxmlElement("w:rFonts")
            r_fonts.set(qn("w:ascii"), font)
            r_fonts.set(qn("w:hAnsi"), font)
            r_pr.append(r_fonts)
            lvl.append(r_pr)
        abstract.append(lvl)
        insert_abstract(abstract)

    def build_num(num_id, abs_id):
        num = OxmlElement("w:num")
        num.set(qn("w:numId"), str(num_id))
        abs_el = OxmlElement("w:abstractNumId")
        abs_el.set(qn("w:val"), str(abs_id))
        num.append(abs_el)
        insert_num(num)

    build_abstract(next_abs, "bullet", "\u2022")
    bullet_num = next_num
    build_num(bullet_num, next_abs)
    build_abstract(next_abs + 1, "decimal", "%1.")
    decimal_num = next_num + 1
    build_num(decimal_num, next_abs + 1)
    return bullet_num, decimal_num


def apply_num(paragraph, num_id):
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = p_pr.find(qn("w:numPr"))
    if num_pr is None:
        num_pr = OxmlElement("w:numPr")
        p_pr.append(num_pr)
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num = OxmlElement("w:numId")
    num.set(qn("w:val"), str(num_id))
    num_pr.append(ilvl)
    num_pr.append(num)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.167


def add_bullet(doc, text, bold_prefix=None, color=None):
    p = doc.add_paragraph()
    apply_num(p, BULLET_NUM)
    if bold_prefix and text.startswith(bold_prefix):
        r1 = p.add_run(bold_prefix)
        set_run_font(r1, bold=True, color=color or COLORS["ink"])
        r2 = p.add_run(text[len(bold_prefix):])
        set_run_font(r2, color=color or COLORS["ink"])
    else:
        r = p.add_run(text)
        set_run_font(r, color=color or COLORS["ink"])
    return p


def add_numbered(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    apply_num(p, DECIMAL_NUM)
    if bold_prefix and text.startswith(bold_prefix):
        r1 = p.add_run(bold_prefix)
        set_run_font(r1, bold=True, color=COLORS["ink"])
        r2 = p.add_run(text[len(bold_prefix):])
        set_run_font(r2, color=COLORS["ink"])
    else:
        r = p.add_run(text)
        set_run_font(r, color=COLORS["ink"])
    return p


def add_body(doc, text, bold_prefix=None, italic=False, after=None):
    p = doc.add_paragraph()
    if bold_prefix and text.startswith(bold_prefix):
        r1 = p.add_run(bold_prefix)
        set_run_font(r1, bold=True, color=COLORS["ink"])
        r2 = p.add_run(text[len(bold_prefix):])
        set_run_font(r2, color=COLORS["ink"], italic=italic)
    else:
        r = p.add_run(text)
        set_run_font(r, color=COLORS["ink"], italic=italic)
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def add_small_note(doc, text, label="Catatan"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Inches(0.12)
    shade_paragraph(p, COLORS["callout"])
    set_paragraph_border(p, edge="left", color=COLORS["blue"], size="14", space="7")
    r1 = p.add_run(f"{label}: ")
    set_run_font(r1, size=10, bold=True, color=COLORS["dark_blue"])
    r2 = p.add_run(text)
    set_run_font(r2, size=10, color=COLORS["ink"])
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(text, style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    return p


def add_kv(doc, label, value):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    r1 = p.add_run(f"{label}: ")
    set_run_font(r1, size=10.5, bold=True, color=COLORS["navy"])
    r2 = p.add_run(value)
    set_run_font(r2, size=10.5, color=COLORS["ink"])
    return p


def add_table(doc, headers, rows, widths, font_size=9.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for idx, header in enumerate(headers):
        table.rows[0].cells[idx].text = header
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            cells[idx].text = str(value)
    style_table(table, widths, header=True, font_size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def set_document_styles(doc):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = rgb(COLORS["ink"])
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10
    normal.paragraph_format.widow_control = True

    title = styles["Title"]
    title.font.name = "Calibri"
    title.font.size = Pt(25)
    title.font.bold = True
    title.font.color.rgb = rgb(COLORS["navy"])
    title._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    title._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(6)
    title.paragraph_format.keep_with_next = True
    title_p_pr = title._element.get_or_add_pPr()
    title_border = title_p_pr.find(qn("w:pBdr"))
    if title_border is not None:
        title_p_pr.remove(title_border)

    subtitle = styles["Subtitle"]
    subtitle.font.name = "Calibri"
    subtitle.font.size = Pt(13)
    subtitle.font.italic = False
    subtitle.font.color.rgb = rgb(COLORS["muted"])
    subtitle._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    subtitle._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    subtitle.paragraph_format.space_before = Pt(0)
    subtitle.paragraph_format.space_after = Pt(14)
    subtitle.paragraph_format.keep_with_next = True

    heading_tokens = {
        "Heading 1": (16, COLORS["blue"], 16, 8),
        "Heading 2": (13, COLORS["blue"], 12, 6),
        "Heading 3": (12, COLORS["dark_blue"], 8, 4),
    }
    for style_name, (size, color, before, after) in heading_tokens.items():
        style = styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = rgb(color)
        style._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.keep_together = True


def set_section_layout(section):
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)


def set_header_footer(section):
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r1 = p.add_run("PRODUCT REQUIREMENTS DOCUMENT")
    set_run_font(r1, size=8.5, bold=True, color=COLORS["muted"])
    r2 = p.add_run("  |  LANDING PAGE PERSONAL BRAND")
    set_run_font(r2, size=8.5, color=COLORS["muted"])

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    r = fp.add_run("Mohamad Arif Pramarta  |  Halaman ")
    set_run_font(r, size=8.5, color=COLORS["muted"])
    add_field(fp, "PAGE", "1")
    r2 = fp.add_run(" dari ")
    set_run_font(r2, size=8.5, color=COLORS["muted"])
    add_field(fp, "NUMPAGES", "1")


doc = Document()
doc.core_properties.title = "PRD Landing Page Jasa - Mohamad Arif Pramarta - Integrasi Superprof v1.2"
doc.core_properties.subject = "Landing page personal brand untuk konsultasi, pengajaran, dan workshop"
doc.core_properties.author = "Mohamad Arif Pramarta"
doc.core_properties.keywords = "PRD, landing page, konsultasi, pengajaran, workshop, data, AI"
doc.core_properties.comments = "Draft implementasi v1.0 - 26 Agustus 2026"

set_document_styles(doc)
for section in doc.sections:
    set_section_layout(section)
    set_header_footer(section)

BULLET_NUM, DECIMAL_NUM = add_custom_numbering(doc)

# First-page memo masthead.
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(18)
p.paragraph_format.space_after = Pt(5)
r = p.add_run("PRD / PERSONAL BRAND")
set_run_font(r, size=9.5, bold=True, color=COLORS["blue"])

title = doc.add_paragraph("PRODUCT REQUIREMENTS DOCUMENT", style="Title")
subtitle = doc.add_paragraph("Landing Page Jasa Konsultasi, Pengajaran, dan Workshop", style="Subtitle")
name_line = doc.add_paragraph()
name_line.paragraph_format.space_after = Pt(14)
r1 = name_line.add_run("Mohamad Arif Pramarta, S.Stat.")
set_run_font(r1, size=15, bold=True, color=COLORS["navy"])
r2 = name_line.add_run("  |  Data, Kebijakan, dan Pembelajaran")
set_run_font(r2, size=11, color=COLORS["muted"])

add_kv(doc, "Status", "Draft siap implementasi - menunggu persetujuan aset dan beberapa keputusan P0")
add_kv(doc, "Versi", "1.2 - pemodelan kebijakan & harga per jam Superprof")
add_kv(doc, "Tanggal", "26 Agustus 2026")
add_kv(doc, "Pemilik produk", "Mohamad Arif Pramarta")
add_kv(doc, "Target", "Landing page berbahasa Indonesia; mobile-first; fokus lead berkualitas")
rule = doc.add_paragraph()
rule.paragraph_format.space_before = Pt(4)
rule.paragraph_format.space_after = Pt(12)
set_paragraph_border(rule, edge="bottom", color=COLORS["blue"], size="10", space="5")

decision = doc.add_paragraph()
decision.paragraph_format.space_before = Pt(0)
decision.paragraph_format.space_after = Pt(12)
decision.paragraph_format.left_indent = Inches(0.12)
decision.paragraph_format.right_indent = Inches(0.05)
shade_paragraph(decision, COLORS["blue_gray"])
set_paragraph_border(decision, edge="left", color=COLORS["blue"], size="18", space="8")
dr1 = decision.add_run("KEPUTUSAN PRODUK UTAMA  ")
set_run_font(dr1, size=10.5, bold=True, color=COLORS["navy"])
dr2 = decision.add_run("Gunakan satu personal brand dengan tiga jalur layanan, satu CTA utama: Diskusikan Kebutuhan, serta jalur trust opsional melalui Superprof.")
set_run_font(dr2, size=10.5, bold=True, color=COLORS["ink"])

add_heading(doc, "Ringkasan eksekutif", 1)
add_body(doc, "Landing page ini berfungsi sebagai satu tautan utama yang menjelaskan bagaimana Mohamad Arif Pramarta membantu instansi, organisasi, profesional, dan pelajar melalui konsultasi statistika dan analisis kebijakan, pengajaran yang personal, serta workshop Excel, AI, dan analisis data. Produk tidak diposisikan sebagai tiga identitas terpisah; ketiganya adalah tiga format untuk menghasilkan keputusan yang lebih jelas dan keterampilan yang dapat langsung dipakai.")
add_body(doc, "Hasil bisnis utama adalah inquiry yang relevan dan dapat ditindaklanjuti. Halaman harus membuat calon klien memahami kecocokan layanan dalam kurang dari 10 detik, menemukan bukti kredibilitas, lalu menghubungi melalui formulir atau kanal langsung tanpa kebingungan. Bagi pengguna yang masih membutuhkan validasi pihak ketiga, halaman menyediakan jalur opsional menuju profil Superprof untuk melihat bukti sosial dan melakukan reservasi sesuai cakupan layanan di platform.")

add_heading(doc, "Keputusan yang sudah direkomendasikan", 2)
for item in [
    "Bahasa utama: Bahasa Indonesia. Versi Inggris masuk fase lanjutan.",
    "Format MVP: satu landing page, notice privasi, dan state konfirmasi.",
    "CTA: \"Diskusikan Kebutuhan\"; CTA layanan mengisi pilihan form secara otomatis.",
    "Superprof: CTA trust/booking sekunder untuk pengajaran atau mentoring; konsultasi organisasi dan workshop tetap memakai jalur diskusi langsung.",
    "Harga: tarif per jam mengikuti tarif aktif di Superprof; konsultasi proyek dan workshop tetap berbasis ruang lingkup.",
    "Bukti: hanya klaim terverifikasi; testimoni, logo, kontak, dan artefak perlu izin.",
    "Nada: profesional, hangat, konkret, dan berorientasi pada hasil pengguna.",
]:
    add_bullet(doc, item)

add_heading(doc, "Cakupan dokumen", 2)
add_body(doc, "PRD mencakup tujuan, audiens, positioning, arsitektur informasi, spesifikasi konten, requirement fungsional dan nonfungsional, SEO, pengukuran, acceptance criteria, roadmap, risiko, serta daftar keputusan yang harus ditutup sebelum rilis.")


add_heading(doc, "1. Latar belakang dan peluang", 1)
add_body(doc, "Saat ini materi profesional tersedia dalam beberapa versi CV yang menonjolkan sisi berbeda: statistik dan kebijakan, AI dan analisis data, pengajaran, serta workshop. Bagi calon klien, format CV belum menjawab tiga pertanyaan komersial dengan cepat: apakah kompetensinya relevan, apa bentuk hasil yang diterima, dan bagaimana memulai kerja sama.")
add_body(doc, "Peluang produk adalah membuat satu halaman yang mudah dibagikan melalui LinkedIn, referral, QR pada materi presentasi, email, dan pencarian organik. Halaman harus mengubah pengalaman yang luas menjadi pilihan layanan yang sederhana tanpa menghilangkan kedalaman bukti.")

add_heading(doc, "Asumsi kerja", 2)
for item in [
    "Layanan ditawarkan dalam kapasitas profesional pribadi; tidak mewakili atau menjadi endorsement institusi tempat bekerja.",
    "Pasar awal adalah Indonesia, dengan layanan daring secara nasional dan luring sesuai kesepakatan.",
    "Email publik adalah arifpramarta@gmail.com; nomor WhatsApp publik masih memerlukan persetujuan eksplisit.",
    "Landing page tidak memuat data pribadi sensitif, bahan kerja rahasia, atau hasil internal yang belum mendapat izin.",
    "Pengelolaan inquiry pada MVP dapat memakai email atau penyimpanan ringan; CRM penuh belum diperlukan.",
    "Profil Superprof merupakan kanal pihak ketiga sekaligus sumber acuan tarif per jam; tarif, rating, jumlah ulasan, jumlah murid, dan waktu respons di sana bersifat dinamis.",
]:
    add_bullet(doc, item)


add_heading(doc, "2. Tujuan, non-goals, dan metrik", 1)
add_heading(doc, "Tujuan bisnis", 2)
add_table(
    doc,
    ["Tujuan", "Indikator utama", "Makna berhasil"],
    [
        ("Menghasilkan inquiry relevan", "Qualified leads per bulan", "Prospek memiliki kebutuhan nyata, konteks, jadwal, dan kontak valid."),
        ("Menjelaskan kecocokan", "Pemahaman hero dan service selection", "Pengguna dapat menyebutkan bidang, sasaran, dan tiga jalur layanan dalam <=10 detik."),
        ("Membangun kepercayaan", "Interaksi dengan bukti dan studi kasus", "Pengguna menemukan kontribusi, pendekatan, dan bukti - bukan sekadar logo."),
        ("Mempercepat follow-up", "Kelengkapan inquiry dan SLA respons", "Kebutuhan awal cukup jelas untuk diskusi atau proposal berikutnya."),
        ("Mendukung referral", "Share/referral traffic dan social preview", "Satu URL mudah diteruskan dan tampil profesional saat dibagikan."),
    ],
    [2500, 2700, 4160],
)

add_small_note(doc, "North-star metric adalah jumlah inquiry berkualitas per bulan. Page view dan jumlah klik hanya metrik pendukung.", "North star")

add_heading(doc, "Definisi qualified lead", 2)
for item in [
    "Dapat dihubungi melalui kanal yang valid.",
    "Memiliki kebutuhan profesional atau pembelajaran yang spesifik.",
    "Menyebutkan sasaran, audiens, atau output yang diharapkan.",
    "Memiliki perkiraan waktu pelaksanaan; anggaran dapat dikualifikasi saat follow-up.",
]:
    add_bullet(doc, item)

add_heading(doc, "KPI awal", 2)
add_body(doc, "Angka konversi berikut adalah hipotesis produk, bukan benchmark. Gunakan 2-4 minggu pertama untuk membangun baseline, lalu tetapkan target 90 hari berdasarkan sumber traffic dan jenis layanan.")
add_table(
    doc,
    ["Metrik", "Definisi", "Hipotesis/guardrail awal"],
    [
        ("Primary CTA click rate", "Klik CTA utama / sesi landing page", ">=5% setelah optimasi awal"),
        ("Inquiry conversion", "Submit sukses / sesi landing page", "2-4%; disesuaikan setelah baseline"),
        ("Form completion", "Submit sukses / form_start", ">=45% dengan maksimal 5 field wajib"),
        ("Qualified lead rate", "Qualified leads / submit sukses", "Dipantau per layanan; target ditetapkan setelah baseline"),
        ("Lead-to-meeting", "Pertemuan terjadwal / qualified leads", "Target setelah proses follow-up stabil"),
        ("Respons", "Waktu dari submit ke respons manusia", "Rekomendasi <=1 hari kerja - perlu konfirmasi"),
        ("Tracking integrity", "Transaksi uji dengan event lengkap", ">=95%; duplikasi submit 0"),
    ],
    [2300, 3800, 3260],
)

add_heading(doc, "Non-goals MVP", 2)
for item in [
    "Pembayaran langsung, checkout, atau paket berlangganan.",
    "Learning management system, area anggota, atau login.",
    "Blog besar, resource hub, newsletter, dan lead magnet.",
    "Penjadwalan otomatis sebelum proses dan ketersediaan benar-benar siap.",
    "Proposal otomatis yang kompleks atau kalkulator harga.",
    "Versi multibahasa dan halaman detail untuk setiap layanan.",
]:
    add_bullet(doc, item)


add_heading(doc, "3. Audiens dan Jobs to Be Done", 1)
add_table(
    doc,
    ["Segmen", "Kebutuhan utama", "Keraguan yang harus dijawab"],
    [
        ("Pengambil keputusan konsultasi", "Analisis, metodologi, validasi, dashboard, rekomendasi, atau dukungan keputusan.", "Apakah memahami konteks, menjaga kualitas data, dan menghasilkan output yang dapat dipakai?"),
        ("HR/L&D dan penyelenggara", "Trainer atau narasumber yang relevan, praktis, dan dapat menyesuaikan materi.", "Apakah sesi interaktif, sesuai level peserta, dan jelas hasil belajarnya?"),
        ("Mahasiswa dan profesional", "Pendampingan personal pada statistik, riset, Excel, dan analisis data.", "Apakah penjelasan mudah dipahami, etis, dan sesuai kebutuhan nyata?"),
        ("Referral/pengadaan", "Profil ringkas yang mudah dibagikan dan diverifikasi.", "Apakah kompetensi, pengalaman, kontak, dan kapasitas layanan cukup jelas?"),
    ],
    [2200, 3600, 3560],
)

add_heading(doc, "Jobs to Be Done", 2)
for job in [
    "Ketika saya memerlukan dukungan analisis atau metodologi, saya ingin cepat memahami pengalaman dan bentuk output Mohamad Arif agar dapat memutuskan apakah perlu berdiskusi.",
    "Ketika saya menyiapkan pelatihan atau workshop, saya ingin melihat topik, format, pendekatan, dan bukti fasilitasi agar yakin sesi dapat disesuaikan dengan peserta.",
    "Ketika saya memerlukan pendampingan belajar, saya ingin mengetahui cakupan materi dan cara mengajar agar dapat memilih sesi yang sesuai level dan target saya.",
    "Ketika saya belum cukup yakin memesan langsung, saya ingin melihat rekam jejak dan mekanisme reservasi di platform pihak ketiga agar dapat mengambil keputusan dengan lebih percaya diri.",
]:
    add_numbered(doc, job)


add_heading(doc, "4. Positioning dan strategi pesan", 1)
add_heading(doc, "Positioning utama", 2)
positioning = doc.add_paragraph()
positioning.paragraph_format.space_before = Pt(2)
positioning.paragraph_format.space_after = Pt(12)
positioning.paragraph_format.left_indent = Inches(0.18)
positioning.paragraph_format.right_indent = Inches(0.18)
shade_paragraph(positioning, COLORS["callout"])
set_paragraph_border(positioning, edge="left", color=COLORS["navy"], size="16", space="8")
pr = positioning.add_run("Mohamad Arif Pramarta membantu instansi, organisasi, profesional, dan pelajar mengubah data yang kompleks menjadi keputusan yang lebih jelas dan keterampilan yang dapat langsung dipakai - melalui konsultasi, pengajaran, dan workshop yang kontekstual.")
set_run_font(pr, size=11, bold=True, color=COLORS["navy"])

add_heading(doc, "Pilar pesan", 2)
for item in [
    "Ketajaman analitis: statistika, metodologi, survei, policy analytics, visualisasi, dan quality assurance.",
    "Pembelajaran aplikatif: materi menyesuaikan tujuan, level peserta, dan kasus kerja nyata.",
    "Komunikasi yang dapat dipakai: insight diterjemahkan menjadi rekomendasi, materi, dashboard, atau langkah aksi.",
    "Praktik AI yang bertanggung jawab: AI membantu workflow, tetapi tetap memerlukan pemeriksaan logika, sumber, dan perlindungan data.",
]:
    add_bullet(doc, item)

add_heading(doc, "Draft hero copy", 2)
add_kv(doc, "Eyebrow", "Konsultasi Data | Pengajaran | Workshop AI & Data")
add_kv(doc, "H1", "Data yang rumit menjadi keputusan dan keterampilan yang bisa dipakai.")
add_kv(doc, "Subheadline", "Saya membantu instansi, organisasi, profesional, dan mahasiswa melalui konsultasi statistika dan analisis kebijakan, pengajaran yang personal, serta workshop Excel, AI, dan analisis data yang aplikatif.")
add_kv(doc, "CTA utama", "Diskusikan Kebutuhan")
add_kv(doc, "CTA sekunder", "Lihat Layanan dan Pengalaman")
add_kv(doc, "CTA trust", "Lihat Ulasan & Pesan via Superprof")
add_small_note(doc, "Jangan memakai headline generik seperti \"membantu Anda bertumbuh\". Hero wajib menyebut bidang, target pengguna, dan hasil yang konkret.", "Copy guardrail")

add_heading(doc, "Bukti ringkas yang dapat dipertimbangkan", 2)
for item in [
    "400+ sesi pengajaran sejak 2022 (wajib ditulis sebagai estimasi).",
    "Pengolahan dan analisis data 75.000+ desa.",
    "Pemodelan 260+ paket kebijakan di 34 provinsi; publikasinya didiseminasikan kepada 34 provinsi, Kementerian Keuangan, dan Kementerian Dalam Negeri.",
    "Survei hingga 1.322 responden serta portofolio dashboard publik.",
    "Publikasi jurnal statistika dan pengalaman workshop AI/Data.",
    "Profil Superprof publik sebagai jalur ulasan dan reservasi pihak ketiga; metrik dinamis tidak disalin sebagai klaim tetap.",
]:
    add_bullet(doc, item)
add_small_note(doc, "Nama institusi menjelaskan konteks pengalaman, bukan endorsement. Setiap angka harus memiliki sumber dan clearance publik sebelum tampil.", "Keamanan klaim")

add_heading(doc, "Nada dan gaya bahasa", 2)
add_body(doc, "Profesional, hangat, jernih, dan tidak menggurui. Gunakan \"saya\" untuk kedekatan dan \"Anda/tim Anda\" untuk orientasi pengguna. Utamakan masalah, output, dan hasil; batasi jargon teknis; hindari klaim superlatif seperti \"terbaik\" atau \"pakar terkemuka\" tanpa bukti independen.")


add_heading(doc, "5. Arsitektur layanan", 1)
add_heading(doc, "5.1 Konsultasi statistika dan analisis kebijakan", 2)
add_body(doc, "Untuk instansi, perusahaan konsultan, organisasi, atau tim program yang membutuhkan pendekatan analitis yang dapat dipertanggungjawabkan.")
for item in [
    "Masalah: data tidak rapi, metodologi belum kuat, hasil survei belum bermakna, dashboard belum mendukung keputusan, atau analisis kebijakan memerlukan sintesis kuantitatif.",
    "Output: kerangka analisis, data bersih/tervalidasi, model atau indikator, dashboard/visualisasi, laporan insight, rekomendasi, dan sesi pembahasan.",
    "Topik prioritas: statistika terapan, desain dan analisis survei, data quality, policy analytics, forecasting, analisis regional, serta visualisasi dan komunikasi insight.",
    "Format: project-based, advisory session, review metodologi, atau pendampingan berkala sesuai ruang lingkup.",
]:
    add_bullet(doc, item)
add_kv(doc, "CTA kontekstual", "Diskusikan Konsultasi")

add_heading(doc, "5.2 Pengajaran dan mentoring", 2)
add_body(doc, "Untuk mahasiswa, profesional, atau institusi yang membutuhkan pemahaman bertahap, pendampingan personal, dan latihan berbasis tujuan nyata.")
for item in [
    "Topik: statistika, metode penelitian, analisis data, Excel, matematika, visualisasi, dan pendampingan riset S1/S2.",
    "Hasil belajar: memahami konsep, mampu menerapkan langkah analisis, membaca output, menjelaskan temuan, dan bekerja lebih mandiri.",
    "Format: 1-on-1 atau kelompok kecil, daring/luring, sesi tunggal atau paket pembelajaran.",
    "Batas etika: pendampingan tidak menggantikan pekerjaan akademik peserta dan tidak menawarkan pembuatan skripsi/tesis.",
]:
    add_bullet(doc, item)
add_kv(doc, "CTA kontekstual", "Tanyakan Kelas atau Mentoring")
superprof_cta = doc.add_paragraph()
superprof_cta.paragraph_format.space_after = Pt(8)
sr1 = superprof_cta.add_run("CTA trust: ")
set_run_font(sr1, bold=True, color=COLORS["navy"])
add_hyperlink(superprof_cta, "Lihat Ulasan & Pesan via Superprof", SUPERPROF_URL)

add_heading(doc, "5.3 Workshop dan training", 2)
add_body(doc, "Untuk HR/L&D, institusi pendidikan, komunitas, penyelenggara acara, dan tim kerja yang membutuhkan sesi interaktif serta materi yang dapat langsung dicoba.")
for item in [
    "Topik prioritas: Excel untuk kebutuhan kerja, AI-assisted Excel, AI untuk produktivitas/karier, responsible AI, data literacy, analisis data, dan data storytelling.",
    "Output: materi, worksheet atau latihan, demo, praktik terpandu, rangkuman, dan rekomendasi tindak lanjut sesuai paket.",
    "Format: talk, mini class, webinar, workshop hands-on, atau training intensif.",
    "Kustomisasi: tujuan, durasi, tingkat peserta, contoh data, mode daring/luring, dan kebutuhan evaluasi ditentukan saat discovery.",
]:
    add_bullet(doc, item)
add_kv(doc, "CTA kontekstual", "Diskusikan Workshop")

add_heading(doc, "Keputusan harga MVP", 2)
add_body(doc, "Tarif per jam untuk pengajaran atau mentoring mengikuti tarif aktif pada profil Superprof sebagai sumber acuan. Landing page menggunakan copy \"Tarif per jam mengikuti Superprof\" dan menautkan profil, sehingga tidak perlu menyimpan angka yang cepat usang. Konsultasi berbasis proyek dan workshop tidak memakai tarif per jam yang sama; biayanya tetap ditentukan berdasarkan ruang lingkup, durasi, jumlah peserta, tingkat kustomisasi, lokasi, dan output.")


add_heading(doc, "6. Arsitektur informasi dan blueprint halaman", 1)
add_body(doc, "Urutan konten mengikuti alur keputusan pengguna: memahami nilai -> memilih layanan -> menilai bukti -> memahami proses -> mengatasi keberatan -> menghubungi.")
add_table(
    doc,
    ["#", "Section", "Tujuan", "Requirement inti"],
    [
        ("1", "Header", "Orientasi dan akses CTA", "Nama/wordmark, anchor Layanan-Pengalaman-Tentang-FAQ, CTA tetap."),
        ("2", "Hero", "Jelaskan fit <=10 detik", "Foto autentik, H1 hasil, target pengguna, tiga jalur layanan, dua CTA."),
        ("3", "Proof strip", "Bangun kredibilitas cepat", "Maksimal 3-4 bukti terverifikasi; sertakan trust link Superprof tanpa menyalin metrik dinamis."),
        ("4", "Cocok untuk Anda jika...", "Mencocokkan masalah", "3-5 situasi nyata menurut target pengguna."),
        ("5", "Tiga layanan", "Membantu memilih jalur", "Audiens, masalah, output, format, CTA per layanan."),
        ("6", "Pilihan topik", "Perjelas cakupan", "4-8 topik prioritas; bukan semua hal dalam CV."),
        ("7", "Pengalaman terpilih", "Buktikan pendekatan", "2-3 studi kasus: konteks-peran-pendekatan-output."),
        ("8", "Cara bekerja", "Kurangi ketidakpastian", "Discovery -> desain -> pelaksanaan -> tindak lanjut."),
        ("9", "Tentang", "Humanisasi dan verifikasi", "Bio 120-180 kata, foto, kredensial, tautan publik."),
        ("10", "Testimoni/trust", "Social proof", "Testimoni berizin; sediakan tautan ke ulasan dan reservasi di Superprof."),
        ("11", "FAQ", "Jawab keberatan", "Biaya, format, durasi, lokasi, kustomisasi, output, persiapan."),
        ("12", "CTA + form", "Konversi dan kualifikasi", "Form sebagai jalur utama; Superprof sebagai jalur trust eksternal yang jelas."),
        ("13", "Footer", "Kontak dan legal", "Email, LinkedIn, Superprof, lokasi/cakupan, privasi, disclaimer kapasitas pribadi."),
    ],
    [480, 1900, 2300, 4680],
    font_size=8.8,
)

add_heading(doc, "Perilaku mobile", 2)
for item in [
    "Konten terbaca pada lebar 320 px tanpa scroll horizontal.",
    "Hero menampilkan pesan utama dan CTA tanpa bergantung pada video atau animasi.",
    "Service card menjadi satu kolom; CTA tetap berjarak dan mudah disentuh.",
    "Navigasi dapat diringkas, tetapi CTA utama tetap jelas.",
    "WhatsApp tidak menjadi satu-satunya jalur; email/form tetap tersedia sebagai fallback.",
]:
    add_bullet(doc, item)


add_heading(doc, "7. Requirement konten dan bukti", 1)
add_heading(doc, "Format studi kasus", 2)
add_body(doc, "Setiap studi kasus memuat lima unsur: konteks, tantangan, peran pribadi, pendekatan, dan output/hasil. Jika nama klien atau data bersifat terbatas, gunakan deskripsi anonim yang tetap spesifik dan tidak menyesatkan.")

add_heading(doc, "Calon studi kasus MVP", 2)
case_rows = [
    ("Policy analytics", "Pemodelan 260+ paket kebijakan di 34 provinsi; diseminasi publikasi ke 34 provinsi, Kementerian Keuangan, dan Kementerian Dalam Negeri", "Pencarian, cleaning, pemodelan/sintesis, interpretasi, visualisasi", "Bukti metode, skala, dan jangkauan diseminasi; artefak publik/ter-redaksi setelah clearance"),
    ("Data skala besar", "Pengolahan data 75.000+ desa dan dashboard indikator", "Validasi, reduksi/struktur data, clustering/visualisasi", "Tunjukkan proses dari data kompleks ke insight; tanpa data sensitif"),
    ("Pengajaran & workshop", "Estimasi 400+ sesi sejak 2022 dan workshop AI 2026", "Penyesuaian level, demo, latihan, komunikasi konsep", "Bukti konsistensi mengajar dan fasilitasi; testimoni perlu izin"),
]
add_table(doc, ["Tema", "Konteks", "Peran/pendekatan", "Bukti yang boleh tampil"], case_rows, [1500, 3300, 2300, 2260], font_size=8.5)

add_heading(doc, "Draft bio singkat", 2)
bio = (
    "Mohamad Arif Pramarta, S.Stat. adalah konsultan statistika dan analisis kebijakan, pengajar, serta fasilitator workshop AI/Data. Lulusan Statistika dan Sains Data IPB University ini mendukung analisis pembangunan wilayah, survei, kualitas data, visualisasi, dan pemodelan untuk kebutuhan pemerintah maupun proyek konsultansi. Sejak 2022, ia telah menjalankan estimasi lebih dari 400 sesi pengajaran pada statistika, metode penelitian, analisis data, Excel, dan matematika. Pendekatannya menggabungkan ketelitian metodologis, komunikasi yang mudah dipahami, serta penggunaan AI secara bertanggung jawab agar hasil analisis dan pembelajaran dapat benar-benar dipakai."
)
add_body(doc, bio, italic=True)
add_small_note(doc, "Bio publik perlu direview untuk memastikan judul peran terbaru dan penggunaan nama institusi telah disetujui.", "Approval")

add_heading(doc, "Aset yang dibutuhkan", 2)
for item in [
    "Foto profesional autentik: rasio 4:5 untuk hero, 1:1 untuk social/structured data, dan versi WebP/AVIF.",
    "2-3 screenshot portofolio yang sudah direduksi, diberi konteks, dan aman dari data sensitif.",
    "Testimoni spesifik untuk tiap jalur layanan; nama, jabatan, organisasi, dan izin publikasi tercatat.",
    "Logo hanya jika ada izin; lebih baik tampilkan studi kasus naratif daripada deretan logo.",
    "Social preview 1200x630, favicon, dan wordmark sederhana.",
    "Capability statement/CV satu halaman sebagai aset P1, bukan blocker MVP.",
]:
    add_bullet(doc, item)

add_heading(doc, "FAQ minimum", 2)
for item in [
    "Layanan apa yang paling sesuai untuk kebutuhan saya?",
    "Topik apa saja yang dapat dibawakan atau diajarkan?",
    "Apakah materi dapat disesuaikan dengan kasus dan level peserta?",
    "Apakah tersedia daring dan luring, serta wilayah mana yang dilayani?",
    "Berapa durasi konsultasi, kelas, atau workshop?",
    "Bagaimana biaya ditentukan dan apa yang termasuk?",
    "Berapa waktu persiapan yang dibutuhkan?",
    "Apakah peserta/klien menerima materi, file kerja, atau rangkuman?",
    "Bagaimana cara meminta proposal dan kapan akan mendapat respons?",
    "Apakah saya dapat melihat ulasan dan memesan sesi melalui Superprof?",
]:
    add_bullet(doc, item)


add_heading(doc, "8. Functional requirements", 1)
fr_rows = [
    ("FR-01", "P0", "Navigasi anchor", "Header mengarah ke section yang benar; fokus keyboard berpindah secara logis."),
    ("FR-02", "P0", "CTA utama konsisten", "Semua CTA utama membuka/alihkan ke alur inquiry yang sama dan terukur."),
    ("FR-03", "P0", "CTA kontekstual", "CTA layanan otomatis mengisi service_type: consultation, teaching, atau workshop."),
    ("FR-04", "P0", "Form inquiry", "Wajib: nama, satu kontak, jenis layanan, ringkasan kebutuhan, persetujuan privasi; maksimal 5 wajib."),
    ("FR-05", "P0", "Validasi dan state", "Inline error, loading, sukses, gagal, retry; data tidak hilang saat error diperbaiki."),
    ("FR-06", "P0", "Pencegahan duplikat", "Submit dikunci saat proses dan idempotency mencegah lead ganda."),
    ("FR-07", "P0", "Penerimaan lead", "Lead tersimpan/terkirim ke tujuan yang disepakati dan memicu notifikasi yang dapat diuji."),
    ("FR-08", "P0", "Fallback contact", "Email selalu tersedia; WhatsApp memakai pesan awal dan nomor yang telah disetujui."),
    ("FR-09", "P0", "Konfirmasi", "Pengguna melihat keberhasilan dan ekspektasi waktu respons; tidak mengklaim sukses sebelum backend mengonfirmasi."),
    ("FR-10", "P0", "Attribution", "UTM dan referral disimpan hingga pencatatan lead tanpa memasukkan PII ke analytics."),
    ("FR-11", "P0", "Analytics funnel", "Event CTA, form, submit, qualified lead, dan meeting dapat dilacak per jenis layanan."),
    ("FR-12", "P0", "SEO/social metadata", "Title, description, canonical, OG, sitemap, robots, dan structured data tersedia."),
    ("FR-13", "P0", "Privacy", "Purpose notice dan kebijakan privasi tersedia sebelum submit; marketing consent terpisah jika ada."),
    ("FR-14", "P0", "Spam protection", "Honeypot/rate limiting atau setara; tidak mengandalkan challenge yang menghambat aksesibilitas."),
    ("FR-15", "P0", "Superprof trust & pricing path", "CTA membuka profil Superprof yang benar; tersedia pada area trust dan pengajaran/mentoring; tarif per jam merujuk ke tarif aktif di platform."),
    ("FR-16", "P1", "Capability statement", "Profil satu halaman dapat diunduh dan event download tercatat."),
    ("FR-17", "P1", "CMS ringan", "Layanan, studi kasus, FAQ, dan testimoni dapat diperbarui tanpa deploy penuh."),
    ("FR-18", "P1", "Calendar", "Integrasi hanya jika kalender selalu akurat dan tidak menambah hambatan konversi."),
]
add_table(doc, ["ID", "Prioritas", "Requirement", "Acceptance ringkas"], fr_rows, [900, 1000, 2500, 4960], font_size=8.6)

add_heading(doc, "Spesifikasi form", 2)
add_table(
    doc,
    ["Field", "Status", "Aturan"],
    [
        ("Nama", "Wajib", "Nama panggilan/nama lengkap; label programatik."),
        ("Email atau WhatsApp", "Wajib", "Minimal satu kontak valid; jangan kirim nilainya ke analytics/URL."),
        ("Jenis layanan", "Wajib", "Konsultasi, Pengajaran/Mentoring, Workshop/Training, Belum yakin."),
        ("Ringkasan kebutuhan", "Wajib", "Tujuan, audiens, masalah, atau output; batas karakter dan helper text."),
        ("Organisasi/jabatan", "Opsional", "Membantu kualifikasi tanpa menghambat individu."),
        ("Perkiraan waktu", "Opsional", "Bulan/tanggal perkiraan, bukan kalender kompleks."),
        ("Persetujuan privasi", "Wajib", "Persetujuan pemrosesan inquiry; tidak dicentang otomatis."),
    ],
    [2800, 1300, 5260],
)


add_heading(doc, "9. Non-functional requirements", 1)
add_heading(doc, "Aksesibilitas", 2)
for item in [
    "Target WCAG 2.2 Level AA; validasi otomatis dilengkapi audit manual.",
    "Navigasi, CTA, form, dan dialog dapat digunakan dengan keyboard; fokus terlihat dan tidak tertutup.",
    "Satu H1; hierarki heading berurutan; bahasa dokumen ditetapkan ke id-ID.",
    "Semua input memiliki label; error tidak hanya mengandalkan warna; status sukses/gagal diumumkan ke assistive technology.",
    "Alt text mendeskripsikan fungsi gambar; elemen dekoratif diabaikan screen reader.",
    "Konten dan fungsi tetap tersedia pada zoom 200%; animasi menghormati reduced motion.",
]:
    add_bullet(doc, item)

add_heading(doc, "Performance dan reliability", 2)
add_table(
    doc,
    ["Area", "Target/guardrail"],
    [
        ("Core Web Vitals", "Pada p75 pengguna mobile: LCP <=2,5 detik; INP <=200 ms; CLS <=0,1."),
        ("Hero", "Tidak bergantung pada video/autoplay; gambar responsif dan terkompresi."),
        ("Asset", "Lazy load di bawah fold; batasi font weight, script, widget, dan tracker pihak ketiga."),
        ("Progressive enhancement", "Konten utama tetap terbaca jika JavaScript gagal; kanal kontak fallback tersedia."),
        ("Form", "Menangani timeout, retry, duplicate submit, dan failure; monitoring mendeteksi error."),
        ("Compatibility", "Uji pada dua versi terbaru browser utama serta Safari iOS dan Chrome Android."),
    ],
    [3000, 6360],
)

add_heading(doc, "Privacy dan keamanan", 2)
for item in [
    "HTTPS; validasi server-side; rate limiting; secret tidak berada di front-end.",
    "Kumpulkan data minimum untuk menindaklanjuti inquiry; tujuan pengumpulan dijelaskan dekat form.",
    "PII tidak boleh berada pada URL, parameter kampanye, log event, atau payload analytics.",
    "Marketing consent terpisah dan opsional; pengguna tetap dapat mengirim inquiry tanpa menyetujui pemasaran.",
    "Masa simpan, vendor pemroses, akses internal, dan prosedur akses/koreksi/penghapusan ditetapkan sebelum rilis.",
    "Tautan Superprof diberi penanda tujuan eksternal; tidak ada data form atau PII yang diteruskan otomatis sebelum pengguna memilih membuka platform tersebut.",
    "Tinjauan hukum final dilakukan oleh pihak yang memahami regulasi yang berlaku; PRD ini bukan opini hukum.",
]:
    add_bullet(doc, item)

add_heading(doc, "Arah visual", 2)
add_body(doc, "Tampilan harus terasa kredibel, manusiawi, dan modern: tipografi sans-serif yang jelas, palet biru tua/putih dengan aksen terbatas, foto autentik, ruang putih cukup, serta elemen data yang ringan. Hindari estetika korporat yang kaku, terlalu banyak kartu, gradient berlebihan, foto stok generik, dan animasi yang tidak membantu keputusan.")


add_heading(doc, "10. SEO dan social sharing", 1)
add_heading(doc, "Search intent MVP", 2)
add_body(doc, "Halaman utama menargetkan intent personal-professional: mencari Mohamad Arif atau tenaga profesional untuk konsultasi data, pengajaran statistik, dan workshop AI/Data. Karena tiga intent dapat berkembang berbeda, fase P1 sebaiknya membuat halaman detail per layanan setelah data pencarian dan inquiry tersedia.")
add_kv(doc, "URL rekomendasi", "https://[domain]/")
add_kv(doc, "Title draft", "Mohamad Arif - Konsultan Data, Pengajar Statistik & Trainer AI")
add_kv(doc, "Meta description draft", "Konsultasi statistika dan kebijakan, pengajaran statistik/analisis data, serta workshop Excel dan AI yang praktis. Diskusikan kebutuhan Anda.")
add_kv(doc, "H1", "Data yang rumit menjadi keputusan dan keterampilan yang bisa dipakai.")

add_heading(doc, "Requirement SEO", 2)
for item in [
    "Satu H1, H2/H3 logis, copy manusiawi, dan tanpa keyword stuffing.",
    "Canonical menuju URL final; sitemap dan robots terkonfigurasi; status 200 dan dapat dirayapi.",
    "Open Graph dan social image mencerminkan nama, positioning, dan CTA.",
    "Structured data JSON-LD menggunakan Person sebagai entitas utama; Service/WebSite hanya memuat fakta yang terlihat di halaman.",
    "Profil Superprof dapat dicantumkan pada sameAs untuk entitas Person; jangan menyalin aggregateRating atau review markup Superprof ke landing page.",
    "ProfilePage dipakai hanya bila fokus halaman benar-benar profil personal dan implementasi lolos validasi dokumentasi Google.",
    "Jangan menambahkan rating, review markup, atau afiliasi yang tidak memenuhi syarat.",
    "Validasi melalui Rich Results Test dan URL Inspection setelah deploy.",
]:
    add_bullet(doc, item)

add_small_note(doc, "Google merekomendasikan JSON-LD untuk structured data dan menekankan bahwa properti harus lengkap serta akurat. Implementasi akhir wajib divalidasi setelah domain tersedia.", "Referensi teknis")


add_heading(doc, "11. Analytics dan operasional lead", 1)
add_body(doc, "Funnel harus terhubung sampai hasil bisnis, bukan berhenti pada klik. Submit sukses hanya dicatat setelah backend mengonfirmasi penyimpanan/pengiriman, bukan ketika pengguna menekan tombol.")
add_table(
    doc,
    ["Event", "Trigger", "Parameter non-PII"],
    [
        ("service_view", "Section layanan terlihat bermakna", "service_type"),
        ("primary_cta_click", "CTA utama diklik", "cta_location, service_type"),
        ("service_cta_click", "CTA pada layanan diklik", "service_type, cta_location"),
        ("superprof_click", "CTA trust Superprof diklik", "cta_location, service_type"),
        ("form_start", "Interaksi pertama dengan form", "service_type, traffic_source"),
        ("form_submit_success", "Backend mengonfirmasi lead tersimpan", "service_type, form_outcome"),
        ("form_submit_error", "Submit gagal", "error_category, service_type"),
        ("whatsapp_click", "Deep link WhatsApp diklik", "cta_location, service_type"),
        ("email_click", "Email diklik", "cta_location"),
        ("portfolio_click", "Bukti/portofolio dibuka", "asset_id, service_type"),
        ("profile_download", "Capability statement diunduh (P1)", "asset_version"),
        ("qualified_lead", "Lead ditandai qualified di pencatatan", "service_type, lead_source"),
        ("meeting_booked", "Pertemuan terkonfirmasi", "service_type, lead_source"),
    ],
    [2500, 3500, 3360],
    font_size=8.7,
)
add_small_note(doc, "Jangan mengirim nama, email, nomor telepon, organisasi, atau isi pesan ke analytics. Pertahankan UTM hanya sebagai data atribusi.", "Data guardrail")

add_heading(doc, "Dashboard minimum", 2)
for item in [
    "Traffic menurut sumber, kampanye, perangkat, dan landing section.",
    "CTA click rate, form start, form completion, dan error rate.",
    "Inquiry, qualified lead, meeting, dan klien menurut jenis layanan.",
    "Waktu respons serta drop-off di setiap tahap funnel.",
    "Rekonsiliasi backend/lead log vs analytics; selisih submit sukses <=5%.",
]:
    add_bullet(doc, item)


add_heading(doc, "12. Acceptance criteria dan release gates", 1)
add_table(
    doc,
    ["Area", "Acceptance criteria P0"],
    [
        ("Kejelasan", "Minimal 5 dari 6 pengguna uji dapat menjelaskan siapa, bidang, target pengguna, dan menemukan CTA dalam <=10 detik."),
        ("Service selection", "Pengguna membedakan tiga jalur layanan; CTA mengisi service_type yang benar."),
        ("Form", "Submit valid diterima tepat satu kali; invalid state spesifik, dapat diakses, dan tidak menghapus input."),
        ("Kontak", "Email berfungsi; WhatsApp hanya dirilis setelah nomor dan pesan awal disetujui; fallback diuji."),
        ("Trust", "Setiap kategori layanan memiliki minimal satu bukti; semua angka, logo, artefak, dan testimoni terlacak ke sumber/izin."),
        ("Superprof", "CTA membuka profil yang benar, berlabel sebagai platform eksternal, dapat digunakan dengan keyboard, tarif per jam merujuk ke harga aktif di platform, dan event superprof_click tercatat tanpa PII."),
        ("Responsive", "Lulus uji pada 320, 375, 768, 1024, dan 1440 px tanpa hilang fungsi atau horizontal scroll."),
        ("Accessibility", "Keyboard-only dan zoom 200% berhasil; tidak ada temuan kritis otomatis; audit fokus, form, kontras, dan alt text lulus."),
        ("Performance", "LCP/INP/CLS memenuhi target p75 setelah traffic memadai; lab test menunjukkan tidak ada blocker berat sebelum launch."),
        ("SEO", "Title, meta, canonical, OG, sitemap, robots, indexability, dan structured data tervalidasi."),
        ("Analytics", ">=95% transaksi uji menghasilkan event benar tanpa duplikasi; PII tidak muncul di event/URL."),
        ("Privacy", "Notice dan kebijakan dapat diakses sebelum submit; owner proses data dan retensi terdokumentasi."),
        ("Operasional", "Pemilik inbox/lead log, SLA respons, fallback, dan monitoring error telah ditetapkan."),
    ],
    [2200, 7160],
    font_size=8.8,
)

add_heading(doc, "Release blockers", 2)
for item in [
    "Positioning atau perbedaan tiga layanan belum jelas.",
    "CTA/form tidak dapat diselesaikan pada mobile atau hanya dengan keyboard.",
    "Submit tidak sampai ke tujuan, menampilkan sukses palsu, atau menghasilkan duplikasi.",
    "Klaim, testimoni, logo, atau artefak belum memiliki bukti/izin.",
    "Tidak ada notice privasi; PII masuk ke analytics/URL; owner data belum ditentukan.",
    "Broken link, error kritis aksesibilitas, social preview salah, atau halaman tidak dapat diindeks.",
    "Tautan Superprof rusak, salah profil, tarif per jam tidak mengikuti harga aktif Superprof, atau copy menyajikan metrik platform yang sudah tidak aktual.",
    "Funnel CTA -> lead -> qualified lead belum dapat diukur.",
]:
    add_bullet(doc, item, color=COLORS["red"])


add_heading(doc, "13. Roadmap dan tanggung jawab", 1)
add_table(
    doc,
    ["Fase", "Output", "Exit criteria"],
    [
        ("0. Discovery & approval", "Positioning, target prioritas, klaim, aset, kontak, privacy owner", "Semua keputusan P0 dan clearance konten selesai."),
        ("1. Content & wireframe", "Copy final, studi kasus, FAQ, responsive wireframe", "Uji 5-second/10-second dan review konten lulus."),
        ("2. Build MVP", "Landing page, form, email/lead log, CTA Superprof, analytics, SEO", "Functional test, tracking, privacy, dan device test lulus."),
        ("3. QA & launch", "Accessibility, performance, link, form, social/SEO validation", "Semua release gate P0 hijau."),
        ("4. Optimasi 30-90 hari", "Dashboard, insight funnel, perbaikan hero/CTA, service pages P1", "Keputusan berdasarkan baseline dan kualitas lead."),
    ],
    [2200, 4000, 3160],
)

add_heading(doc, "Owner yang diperlukan", 2)
for item in [
    "Product/content owner - Mohamad Arif: positioning, fakta, aset, layanan, harga, dan SLA.",
    "Design/development: wireframe, visual system, responsive build, integrasi, dan QA.",
    "Lead operations: inbox/lead log, kualifikasi, respons, meeting, dan outcome.",
    "Review/clearance: aset institusi, privasi, dan copy sensitif.",
]:
    add_bullet(doc, item)


add_heading(doc, "14. Risiko dan mitigasi", 1)
add_table(
    doc,
    ["Risiko", "Dampak", "Mitigasi"],
    [
        ("Positioning terlalu luas", "Pengguna bingung memilih", "Satu hasil payung; tiga jalur berdasarkan kebutuhan dan output."),
        ("Halaman menjadi CV panjang", "Manfaat klien tenggelam", "Urutkan masalah-output-bukti; bio dibatasi; detail pindah ke P1."),
        ("Klaim institusi disalahartikan", "Risiko reputasi", "Jelaskan peran personal; disclaimer; clearance artefak/logo."),
        ("Bukti pengajaran/workshop belum seimbang", "Trust antar layanan tidak merata", "Kumpulkan testimoni dan dokumentasi berizin per jalur."),
        ("Form terlalu panjang", "Drop-off tinggi", "Maksimal 5 field wajib; kualifikasi lanjutan saat follow-up."),
        ("Lead hilang atau ganda", "Peluang bisnis hilang", "Backend confirmation, idempotency, monitoring, dan fallback contact."),
        ("Aturan harga membingungkan", "Prospek ragu atau melihat harga berbeda", "Tarif per jam mengikuti Superprof; konsultasi proyek/workshop menjelaskan faktor pembentuk biaya."),
        ("Widget pihak ketiga berat", "Lambat dan tidak aksesibel", "MVP ringan; muat integrasi hanya setelah interaksi atau fase P1."),
        ("Data Superprof cepat usang", "Trust menurun atau copy menyesatkan", "Jadikan profil sumber acuan tarif per jam; gunakan tautan, bukan embed; verifikasi profil berkala."),
    ],
    [2600, 2600, 4160],
    font_size=8.8,
)


add_heading(doc, "15. Keputusan yang harus ditutup sebelum build", 1)
add_body(doc, "Butir bertanda P0 adalah launch blocker. Rekomendasi sudah diberikan agar keputusan dapat diambil cepat.")
decisions = [
    ("P0", "Domain final", "Pilih domain personal yang singkat; tetapkan canonical URL."),
    ("P0", "Audiens prioritas pertama", "Rekomendasi: organisasi/instansi untuk konsultasi dan workshop; pengajaran tetap jalur ketiga."),
    ("P0", "Nomor WhatsApp publik", "Publikasikan hanya setelah persetujuan eksplisit; email tetap fallback."),
    ("P0", "SLA respons", "Rekomendasi: maksimal 1 hari kerja bila operasional memungkinkan."),
    ("P0", "Klaim dan studi kasus", "Pilih 3 bukti; lakukan clearance angka, nama, gambar, dan artefak."),
    ("P0", "Testimoni dan logo", "Gunakan hanya dengan izin; section boleh disembunyikan sampai siap."),
    ("P0", "Tujuan form dan owner lead", "Tentukan inbox/lead log, notifikasi, dan siapa yang merespons."),
    ("P0", "Foto dan social preview", "Sediakan aset autentik, crop, alt text, dan versi ringan."),
    ("P0", "Privacy owner/retensi", "Tetapkan notice, vendor, akses, retensi, dan kanal hak data."),
    ("P0", "Aturan tarif per jam", "Tarif per jam mengikuti tarif aktif Superprof; harga konsultasi proyek/workshop tetap berbasis ruang lingkup."),
    ("P1", "Calendar dan CRM", "Tambahkan hanya jika proses dan pemeliharaan siap."),
    ("P1", "Versi Inggris/service pages", "Prioritaskan berdasarkan sumber traffic dan permintaan nyata."),
]
add_table(doc, ["Prioritas", "Keputusan", "Rekomendasi"], decisions, [1200, 3000, 5160], font_size=8.9)


add_heading(doc, "16. Content governance", 1)
add_heading(doc, "Boleh dipakai setelah fact-check", 2)
for item in [
    "Nama dan gelar: Mohamad Arif Pramarta, S.Stat.",
    "Positioning: konsultan statistika dan analisis kebijakan, pengajar, serta fasilitator workshop AI/Data.",
    "S1 Statistika dan Sains Data, IPB University.",
    "Pengalaman mendukung analisis pembangunan wilayah sejak 2024; detail jabatan memakai versi terbaru dan tidak menyiratkan pegawai tetap/endorsement.",
    "Pemodelan 260+ paket kebijakan di 34 provinsi; publikasinya didiseminasikan kepada 34 provinsi, Kementerian Keuangan, dan Kementerian Dalam Negeri.",
    "Data 75.000+ desa; survei hingga 1.322 responden; dashboard dan portofolio publik.",
    "Estimasi 400+ sesi pengajaran sejak April 2022; workshop AI/Data pada 2026.",
    "Topik Excel, AI-assisted analysis, responsible AI, statistika, metode riset, policy analytics, visualisasi, dan data storytelling.",
    "Tautan profil Superprof publik sebagai kanal ulasan dan reservasi pihak ketiga.",
]:
    add_bullet(doc, item)

add_heading(doc, "Jangan dipublikasikan atau perlu persetujuan khusus", 2)
for item in [
    "NIM, riwayat kesehatan/medical leave, alamat rinci, dan informasi pribadi sensitif.",
    "Nomor telepon/WhatsApp sebelum persetujuan eksplisit.",
    "Data internal, file kerja, informasi responden, atau screenshot yang belum direduksi.",
    "Logo institusi, testimoni, foto peserta, dan materi event tanpa izin.",
    "Klaim sertifikasi Microsoft/BNSP, Microsoft Certified Trainer, Power Query/VBA/macro, atau kompetensi lain yang belum terbukti.",
    "Bahasa yang menyiratkan endorsement resmi dari Bappenas, Microsoft, BNSP, atau institusi lain.",
    "Rating, jumlah ulasan/murid, waktu respons, atau kutipan ulasan Superprof tanpa pemeriksaan terkini dan izin/ketentuan penggunaan yang sesuai.",
    "Tarif per jam yang dicantumkan sebagai angka statis atau berbeda dari tarif aktif pada profil Superprof.",
]:
    add_bullet(doc, item, color=COLORS["red"])


add_heading(doc, "17. Referensi dan evidence registry", 1)
add_heading(doc, "Sumber profil internal yang diprioritaskan", 2)
for item in [
    "CV Policy Analytics, Responsible AI & Media - Mohamad Arif Pramarta - 13 August 2026.",
    "CV Trainer Excel & AI untuk Analisis Data - Mohamad Arif Pramarta - 3 August 2026.",
    "CV Master - Mohamad Arif Pramarta - Update 1 August 2026.",
    "AI & Statistical Analyst CV - Mohamad Arif Pramarta - Update 1 August 2026.",
]:
    add_bullet(doc, item)
add_small_note(doc, "Jika angka atau jabatan berbeda antarversi, gunakan sumber paling baru dan minta konfirmasi pemilik sebelum publikasi.", "Version control")

add_heading(doc, "Tautan publik terverifikasi", 2)
links = [
    ("LinkedIn", "https://id.linkedin.com/in/mohamad-arif-pramarta"),
    ("Tableau Public", "https://public.tableau.com/app/profile/mohamad.arif.pramarta"),
    ("Publikasi/DOI", "https://doi.org/10.26740/jram.v6n1.p80-92"),
    ("Artikel DQLab", "https://dqlab.id/indeks-pembangunan-manusia-ipm-dan-penetrasi-internet-tren-wawasan-dan-korelasi-di-indonesia-2015-2022"),
    ("Rumah Visioner", "https://rumahvisioner.org/"),
    ("Film sosial", "https://www.youtube.com/watch?v=GcEhh9KAqOA"),
    ("Superprof (ulasan & reservasi)", SUPERPROF_URL),
]
public_links = doc.add_paragraph()
public_links.paragraph_format.space_after = Pt(8)
for index, (label, url) in enumerate(links):
    add_hyperlink(public_links, label, url)
    if index < len(links) - 1:
        separator = public_links.add_run("  |  ")
        set_run_font(separator, color=COLORS["muted"])

add_heading(doc, "Referensi teknis", 2)
tech_links = [
    ("W3C - WCAG 2.2", "https://www.w3.org/WAI/standards-guidelines/wcag/"),
    ("web.dev - Core Web Vitals", "https://web.dev/articles/vitals"),
    ("Google - Structured Data", "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data"),
    ("Google - ProfilePage", "https://developers.google.com/search/docs/appearance/structured-data/profile-page"),
]
technical_links = doc.add_paragraph()
technical_links.paragraph_format.space_after = Pt(8)
for index, (label, url) in enumerate(tech_links):
    add_hyperlink(technical_links, label, url)
    if index < len(tech_links) - 1:
        separator = technical_links.add_run("  |  ")
        set_run_font(separator, color=COLORS["muted"])

add_heading(doc, "Definition of Done", 2)
add_body(doc, "Produk dianggap selesai ketika seluruh keputusan P0 tertutup, copy dan bukti telah disetujui, landing page lulus acceptance criteria, alur lead bekerja end-to-end, tautan serta event Superprof telah diuji, tidak ada PII di analytics/URL, dan semua release gate kritis berstatus hijau. Setelah rilis, baseline 2-4 minggu menjadi dasar optimasi berikutnya.")


# Final structural cleanup.
for paragraph in doc.paragraphs:
    paragraph.paragraph_format.widow_control = True
    if paragraph.style.name.startswith("Heading"):
        paragraph.paragraph_format.keep_with_next = True

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.widow_control = True

# Update fields on open/render.
settings = doc.settings._element
update_fields = settings.find(qn("w:updateFields"))
if update_fields is None:
    update_fields = OxmlElement("w:updateFields")
    settings.append(update_fields)
update_fields.set(qn("w:val"), "true")

doc.save(OUTPUT)
print(str(OUTPUT.resolve()))
