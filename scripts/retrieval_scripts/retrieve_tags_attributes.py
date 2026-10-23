"""
Récupération des balises (et leurs attributs) contenus 
dans un dossier de fichiers XML-TEI selon le <teiHeader>
ou le <text>
"""

import os
import sys
import glob
import xml.etree.ElementTree as ET
from collections import defaultdict


XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"


def extract_structure(folder_path, section):
    structure = defaultdict(lambda: {
        "count": 0,
        "attributes": defaultdict(lambda: {
            "count": 0,
            "values": defaultdict(int)
        })
    })

    xml_files = glob.glob(os.path.join(folder_path, "*.xml"))

    for file in xml_files:
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            target = root.find(f".//{{{TEI_NAMESPACE}}}{section}")
            if target is None:
                continue

            for elem in target.iter():
                tag = elem.tag
                if "}" in tag:
                    tag = tag.split("}", 1)[1]

                structure[tag]["count"] += 1

                for attr, value in elem.attrib.items():
                    if attr.startswith("{"):
                        ns, attr_name = attr[1:].split("}")
                        if ns == XML_NAMESPACE:
                            continue
                    else:
                        attr_name = attr

                    structure[tag]["attributes"][attr_name]["count"] += 1
                    structure[tag]["attributes"][attr_name]["values"][value] += 1

        except ET.ParseError:
            print(f"Erreur de parsing dans : {file}")

    return structure


def write_structure_to_file(structure, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for tag in sorted(structure.keys()):
            tag_count = structure[tag]["count"]
            f.write(f"{tag} ({tag_count})\n")

            attributes = structure[tag]["attributes"]

            if attributes:
                for attr in sorted(attributes.keys()):
                    attr_count = attributes[attr]["count"]
                    f.write(f" ├─ @{attr} ({attr_count})\n")

                    for val, val_count in sorted(attributes[attr]["values"].items()):
                        f.write(f" │    ├─ \"{val}\" ({val_count})\n")
            else:
                f.write(" ├─ (aucun attribut)\n")

            f.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python script.py chemin_du_dossier teiHeader|text")
        sys.exit(1)

    dossier = sys.argv[1]
    section = sys.argv[2]

    if section not in ["teiHeader", "text"]:
        print("Section doit être 'teiHeader' ou 'text'")
        sys.exit(1)

    if not os.path.isdir(dossier):
        print("Le chemin fourni n'est pas un dossier valide.")
        sys.exit(1)

    structure = extract_structure(dossier, section)

    output_file = f"resultat_{section}.txt"
    write_structure_to_file(structure, output_file)

    print(f"✔  Résultats écrits dans : {output_file}")
