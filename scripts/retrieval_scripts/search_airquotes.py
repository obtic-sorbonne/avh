import os
import sys
import re
import xml.etree.ElementTree as ET

# Liste des guillemets possibles
QUOTES = [
    '"', "`",
    "«", "»",
]

# Classe regex contenant tous les guillemets
QUOTE_CLASS = "[" + re.escape("".join(QUOTES)) + "]"

# Regex : guillemet entouré par des caractères alphanumériques
EMBEDDED_QUOTE_PATTERN = re.compile(rf"[A-Za-z0-9]{QUOTE_CLASS}[A-Za-z0-9]")


def get_namespace(root):
    """Détecte automatiquement le namespace TEI."""
    if root.tag.startswith("{"):
        return root.tag.split("}")[0] + "}"
    return ""


def extract_p_elements(root, ns):
    """Retourne toutes les balises <p> du document."""
    return root.findall(f".//{ns}p")


def contains_embedded_quote(text):
    """Retourne True si un guillemet est entouré de caractères alphanum."""
    return bool(EMBEDDED_QUOTE_PATTERN.search(text))


def process_file(file_path):
    """Analyse un fichier XML et retourne les <p> contenant un guillemet collé."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Erreur de lecture XML dans {file_path}: {e}")
        return []

    ns = get_namespace(root)
    p_elements = extract_p_elements(root, ns)

    results = []

    for p in p_elements:
        # Récupère TOUT le texte du paragraphe, y compris les balises internes
        text = "".join(p.itertext()).strip()

        if not text:
            continue

        if contains_embedded_quote(text):
            results.append(text)

    return results


def write_output(output_file, data):
    """Écrit les résultats dans un fichier texte."""
    with open(output_file, "w", encoding="utf-8") as f:
        for filename, extracts in data.items():
            f.write("=====================================\n")
            f.write(f"Fichier : {filename}\n")
            f.write(f"Nombre d'extraits : {len(extracts)}\n")
            f.write("=====================================\n\n")

            for ex in extracts:
                f.write(ex + "\n\n")

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
        extracts = process_file(file_path)

        if extracts:
            results[filename] = extracts

    write_output(output_file, results)
    print(f"Analyse terminée. Résultats écrits dans : {output_file}")


if __name__ == "__main__":
    main()
