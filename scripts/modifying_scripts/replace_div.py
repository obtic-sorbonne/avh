import os
import sys
from lxml import etree

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def has_head(div):
    """Retourne True si la div contient un head"""
    return bool(div.xpath("tei:head", namespaces=TEI_NS))

def clean_nested_sections(tree, log_file, file_path):
    root = tree.getroot()
    nested_sections = root.xpath(
        "//tei:div[@type='section']/tei:div[@type='section']",
        namespaces=TEI_NS
    )
    modifications = 0

    for inner_div in nested_sections:
        parent = inner_div.getparent()

        # On supprime seulement si le parent n'a pas de head
        if has_head(parent):
            continue

        line = inner_div.sourceline

        # Extraits pour log
        parent_snippet = etree.tostring(parent, encoding="unicode")[:300].replace("\n", " ")
        inner_snippet = etree.tostring(inner_div, encoding="unicode")[:300].replace("\n", " ")

        log_file.write("\n")
        log_file.write("--------------------------------------------------\n")
        log_file.write(f"Fichier : {file_path}\n")
        log_file.write(f"Ligne   : {line}\n")
        log_file.write("Div parent (extrait) :\n")
        log_file.write(parent_snippet + "\n\n")
        log_file.write("Div supprimée (extrait) :\n")
        log_file.write(inner_snippet + "\n")
        log_file.write("--------------------------------------------------\n")

        # Déplier le contenu
        for child in list(inner_div):
            parent.insert(parent.index(inner_div), child)
        parent.remove(inner_div)

        modifications += 1

    return modifications

def process_file(input_path, output_path, log_file):
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(input_path, parser)

    modifications = clean_nested_sections(tree, log_file, input_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(
        output_path,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )

    return modifications

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py dossier_xml")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = "output"
    total_modifications = 0

    with open("log_nested_sections.txt", "w", encoding="utf-8") as log_file:
        for root_dir, dirs, files in os.walk(input_folder):
            for filename in files:
                if filename.endswith(".xml"):
                    input_path = os.path.join(root_dir, filename)
                    relative_path = os.path.relpath(input_path, input_folder)
                    output_path = os.path.join(output_folder, relative_path)

                    print(f"Traitement : {relative_path}")
                    mods = process_file(input_path, output_path, log_file)
                    total_modifications += mods

        log_file.write("\n==============================\n")
        log_file.write(f"TOTAL MODIFICATIONS : {total_modifications}\n")
        log_file.write("==============================\n")

    print("\nTerminé.")
    print(f"Total des sections imbriquées supprimées : {total_modifications}")
    print("Les fichiers modifiés sont dans le dossier 'output/'")
    print("Voir log_nested_sections.txt pour le détail des modifications.")

if __name__ == "__main__":
    main()