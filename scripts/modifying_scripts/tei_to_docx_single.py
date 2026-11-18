import os
import sys
import re
import xml.etree.ElementTree as ET
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_TAB_ALIGNMENT

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}

# -------------------------
# Nettoyage texte
# -------------------------
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------
# Ajouter texte avec hi rend
# -------------------------
def add_text_with_format(paragraph, node):
    if node.text:
        paragraph.add_run(clean_text(node.text))
    for child in node:
        if child.tag.endswith("hi"):
            run = paragraph.add_run(clean_text(child.text))
            if "italic" in child.attrib.get("rend", ""):
                run.italic = True
        elif child.tag.endswith("note") and child.attrib.get("type") == "foliation":
            insert_foliation(paragraph._parent, child)
        elif child.tag.endswith("fw"):
            insert_fw(paragraph._parent, child)
        else:
            add_text_with_format(paragraph, child)
        if child.tail:
            paragraph.add_run(clean_text(child.tail))

# -------------------------
# Paragraphe avec alinéa et folios internes
# -------------------------
def process_paragraph(node, doc):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)

    if node.text:
        p.add_run(clean_text(node.text))

    for child in node:
        if child.tag.endswith("note") and child.attrib.get("type") == "foliation":
            insert_foliation(doc, child)
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Cm(1.25)
        elif child.tag.endswith("hi"):
            run = p.add_run(clean_text(child.text))
            if "italic" in child.attrib.get("rend",""):
                run.italic = True
        else:
            add_text_with_format(p, child)
        if child.tail:
            p.add_run(clean_text(child.tail))

# -------------------------
# Folio dans la marge
# -------------------------
def insert_foliation(doc, node):
    text = clean_text("".join(node.itertext()))
    if not text:
        return
    p = doc.add_paragraph()
    tabs = p.paragraph_format.tab_stops
    tabs.add_tab_stop(Cm(-1.5), WD_TAB_ALIGNMENT.LEFT)
    run = p.add_run("\t" + text)
    run.italic = True
    run.font.size = Pt(9)

# -------------------------
# Heading niveau
# -------------------------
def heading_level(div_type):
    mapping = {"section":1, "subsection":2, "subsubsection":3}
    return mapping.get(div_type, 2)

# -------------------------
# Listes imbriquées corrigées (max 3 niveaux)
# -------------------------
def process_list(node, doc, level=0):
    max_level = 3  # Limite Word pour List Bullet
    for item in node.findall("tei:item", NS):
        effective_level = min(level, max_level - 1)
        style = f"List Bullet {effective_level+1}" if effective_level > 0 else "List Bullet"
        
        p = doc.add_paragraph(style=style)
        p.paragraph_format.first_line_indent = Cm(1.25)

        # texte direct de l'item (avant enfants)
        if item.text and item.text.strip():
            p.add_run(clean_text(item.text))

        # ajouter les enfants non-list
        for child in item:
            if child.tag.endswith("list"):
                continue
            elif child.tag.endswith("note") and child.attrib.get("type") == "foliation":
                insert_foliation(doc, child)
            elif child.tag.endswith("hi"):
                run = p.add_run(clean_text(child.text))
                if "italic" in child.attrib.get("rend",""):
                    run.italic = True
            else:
                add_text_with_format(p, child)

        # traiter uniquement les sous-listes
        for child in item:
            if child.tag.endswith("list"):
                process_list(child, doc, level=level+1)

# -------------------------
# Tables TEI → DOCX
# -------------------------
def process_table(node, doc):
    """
    Convertit un élément <table> TEI en tableau DOCX.
    """
    # Créer un tableau Word avec autant de lignes que <row>
    rows = node.findall("tei:row", NS)
    if not rows:
        return

    # Déterminer le nombre maximal de cellules
    max_cols = 0
    for r in rows:
        cells = r.findall("tei:cell", NS)
        max_cols = max(max_cols, len(cells))

    table = doc.add_table(rows=len(rows), cols=max_cols)
    table.style = "Table Grid"

    # Remplir le tableau
    for i, r in enumerate(rows):
        cells = r.findall("tei:cell", NS)
        for j, c in enumerate(cells):
            cell = table.cell(i, j)
            process_cell(c, cell)


def process_cell(node, cell):
    """
    Remplit une cellule DOCX à partir d'un <cell> TEI.
    """
    # Nettoyage du contenu direct
    if node.text and node.text.strip():
        p = cell.paragraphs[0]
        p.add_run(clean_text(node.text))

    # Gestion des enfants (hi, note, etc.)
    for child in node:
        if child.tag.endswith("hi"):
            run = cell.paragraphs[0].add_run(clean_text(child.text))
            if "italic" in child.attrib.get("rend", ""):
                run.italic = True

        elif child.tag.endswith("note") and child.attrib.get("type") == "foliation":
            # foliation dans la marge → on l’ajoute dans le doc, pas dans la cellule
            insert_foliation(cell._tc.getparent().getparent(), child)

        elif child.tag.endswith("fw"):
            insert_fw(cell._tc.getparent().getparent(), child)

        else:
            # texte récursif
            add_text_with_format(cell.paragraphs[0], child)

        if child.tail:
            cell.paragraphs[0].add_run(clean_text(child.tail))

# -------------------------
# Forme de mot (<fw>) dans la marge
# -------------------------
def insert_fw(doc, node):
    text = clean_text("".join(node.itertext()))
    if not text:
        return
    p = doc.add_paragraph()
    tabs = p.paragraph_format.tab_stops
    tabs.add_tab_stop(Cm(-1.5), WD_TAB_ALIGNMENT.LEFT)
    run = p.add_run("\t" + text)
    run.font.size = Pt(9)
    run.italic = False  # ou True si tu préfères


# -------------------------
# Traitement noeuds
# -------------------------
def process_node(node, doc):
    tag = node.tag

    if tag.endswith("pb"):
        return

    if tag.endswith("note") and node.attrib.get("type") == "foliation":
        insert_foliation(doc,node)
        return

    if tag.endswith("div"):
        div_type = node.attrib.get("type")
        head = node.find("tei:head", NS)
        if head is not None:
            text = clean_text("".join(head.itertext()))
            level = heading_level(div_type)
            doc.add_heading(text, level=level)
        for child in node:
            process_node(child, doc)
        return

    if tag.endswith("p"):
        process_paragraph(node, doc)
        return

    if tag.endswith("list"):
        process_list(node, doc)
        return

    if tag.endswith("table"):
        process_table(node, doc)
        return

    if tag.endswith("fw"):
        insert_fw(doc, node)
        return

    for child in node:
        process_node(child, doc)


# -----------------------------------------------------
# Conversion d’un fichier TEI → ajout dans un DOCX existant
# -----------------------------------------------------
def append_tei_into_docx(input_file, doc):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Titre du fichier (optionnel mais utile)
    doc.add_heading(f"Fichier : {os.path.basename(input_file)}", level=1)

    title = root.find(".//tei:titleStmt/tei:title", NS)
    if title is not None and title.text:
        doc.add_heading(clean_text(title.text), level=2)

    author = root.find(".//tei:titleStmt/tei:author", NS)
    if author is not None and author.text:
        p = doc.add_paragraph(f"Auteur : {clean_text(author.text)}")
        p.paragraph_format.first_line_indent = Cm(1.25)

    body = root.find(".//tei:text/tei:body", NS)
    if body is not None:
        for child in body:
            process_node(child, doc)

    # Séparateur visuel entre fichiers
    doc.add_page_break()


# -----------------------------------------------------
# Fusion de tous les TEI dans un seul DOCX
# -----------------------------------------------------
def merge_all_into_one_docx(input_folder, output_file, template=None):
    doc = Document(template) if template else Document()

    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".xml")])

    if not files:
        print("Aucun fichier XML trouvé.")
        return

    for f in files:
        in_path = os.path.join(input_folder, f)
        try:
            append_tei_into_docx(in_path, doc)
            print("✓ ajouté :", f)
        except Exception as e:
            print("Erreur avec", f, ":", e)

    doc.save(output_file)
    print("\n✓ Fusion terminée →", output_file)


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\npython tei_to_docx.py dossier_TEI sortie.docx [template.docx]")
        sys.exit()

    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    template = sys.argv[3] if len(sys.argv) == 4 else None

    merge_all_into_one_docx(input_folder, output_file, template)
