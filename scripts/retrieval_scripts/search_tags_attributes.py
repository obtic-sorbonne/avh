import os
import sys
import xml.etree.ElementTree as ET

# ---------------------------------------------------------
# CONFIGURATION : balises et attributs obligatoires
# ---------------------------------------------------------
# Exemple :
#   "persName": ["type", "xml:id"]
#   "hi": ["rend"]
#   "note": ["type"]

TARGETS = {
    "table": ["cols"],
}
# ---------------------------------------------------------


def get_namespace(root):
    """Détecte automatiquement le namespace TEI."""
    if root.tag.startswith("{"):
        return root.tag.split("}")[0] + "}"
    return ""


def find_targets(root, ns):
    """Trouve uniquement les balises qui possèdent l'attribut demandé."""
    results = []

    for tag, attrs in TARGETS.items():
        full_tag = f".//{ns}{tag}"

        for elem in root.findall(full_tag):

            # Vérifier si l'élément possède AU MOINS un des attributs demandés
            matched_attrs = {attr: elem.attrib[attr] for attr in attrs if attr in elem.attrib}

            if not matched_attrs:
                continue  # ignorer si aucun attribut demandé n'est présent

            info = {
                "tag": tag,
                "attributes": matched_attrs,
                "text": "".join(elem.itertext()).strip()
            }

            results.append(info)

    return results


def process_file(file_path):
    """Analyse un fichier XML et retourne les infos trouvées."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Erreur dans {file_path}: {e}")
        return []

    ns = get_namespace(root)
    return find_targets(root, ns)


def write_output(output_file, data):
    """Écrit les résultats dans un fichier texte."""
    with open(output_file, "w", encoding="utf-8") as f:

        for filename, items in data.items():
            f.write("=====================================\n")
            f.write(f"Fichier : {filename}\n")
            f.write(f"Nombre d'occurrences : {len(items)}\n")
            f.write("=====================================\n\n")

            for item in items:
                f.write(f"Balise : <{item['tag']}>\n")

                f.write("Attributs présents :\n")
                for k, v in item["attributes"].items():
                    f.write(f"  - {k} = {v}\n")

            f.write("\n\n")


def main():
    if len(sys.argv) < 3:
        print("Usage : python script.py <dossier_xml> <fichier_sortie>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_file = sys.argv[2]

    results = {}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".xml"):
            continue

        file_path = os.path.join(folder_path, filename)
        items = process_file(file_path)

        if items:
            results[filename] = items

    write_output(output_file, results)
    print(f"Analyse terminée. Résultats écrits dans : {output_file}")


if __name__ == "__main__":
    main()
