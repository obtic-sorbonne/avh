import sys
from pathlib import Path
from lxml import etree

# --------------------------------------------------
# Vérification des arguments
# --------------------------------------------------

if len(sys.argv) != 3:
    print("Usage : python add_interpretation.py <input_dir> <output_dir>")
    sys.exit(1)

INPUT_DIR = Path(sys.argv[1])
OUTPUT_DIR = Path(sys.argv[2])

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
TEI = "{http://www.tei-c.org/ns/1.0}"

# Texte à insérer
INTERPRETATION_TEXT = "Pour aider à la compréhension et à l'accessibilité du texte, des en-têtes ont été rajoutés à certains tableaux, et les tirets représentant des répétitions ont été remplacés par l'information même qu'ils désignaient."

parser = etree.XMLParser(remove_blank_text=False)

for xml_file in sorted(INPUT_DIR.glob("*.xml")):

    print(f"Traitement : {xml_file.name}")

    tree = etree.parse(str(xml_file), parser)
    root = tree.getroot()

    # ---------------------------------------
    # teiHeader
    # ---------------------------------------
    teiHeader = root.find(f"{TEI}teiHeader")
    if teiHeader is None:
        print("Pas de teiHeader.")
        continue

    # ---------------------------------------
    # encodingDesc
    # ---------------------------------------
    encodingDesc = teiHeader.find(f"{TEI}encodingDesc")
    if encodingDesc is None:
        encodingDesc = etree.SubElement(teiHeader, TEI + "encodingDesc")

    # ---------------------------------------
    # editorialDecl
    # ---------------------------------------
    editorialDecl = encodingDesc.find(f"{TEI}editorialDecl")
    if editorialDecl is None:
        editorialDecl = etree.SubElement(encodingDesc, TEI + "editorialDecl")

    # ---------------------------------------
    # interpretation
    # ---------------------------------------
    interpretation = editorialDecl.find(f"{TEI}interpretation")
    if interpretation is None:
        interpretation = etree.SubElement(editorialDecl, TEI + "interpretation")

    # ---------------------------------------
    # p
    # ---------------------------------------
    p = etree.SubElement(interpretation, TEI + "p")
    p.text = INTERPRETATION_TEXT

    # Sauvegarde
    tree.write(
        str(OUTPUT_DIR / xml_file.name),
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True,
    )

print("Terminé.")