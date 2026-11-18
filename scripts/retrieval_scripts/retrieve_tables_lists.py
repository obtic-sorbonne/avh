import sys
from pathlib import Path
from lxml import etree
from copy import deepcopy

# ----------------------------------------
# Vérification des arguments
# ----------------------------------------

if len(sys.argv) != 2:
    print("Usage : python extract_tables_lists.py <dossier_tei>")
    sys.exit(1)

INPUT_FOLDER = Path(sys.argv[1])

if not INPUT_FOLDER.exists():
    print(f"Le dossier {INPUT_FOLDER} n'existe pas.")
    sys.exit(1)

# Namespace TEI
NS = {
    "tei": "http://www.tei-c.org/ns/1.0"
}

from pathlib import Path

# Fichiers de sortie (dans le répertoire courant)
tables_output = Path("tables_uag.txt")
lists_output = Path("listes_uag.txt")

with open(tables_output, "w", encoding="utf-8") as tables_file, \
     open(lists_output, "w", encoding="utf-8") as lists_file:

    # Parcours des fichiers XML
    for tei_file in sorted(INPUT_FOLDER.glob("*.xml")):

        print(f"Traitement : {tei_file.name}")

        try:
            tree = etree.parse(str(tei_file))
        except Exception as e:
            print(f"Erreur lors de la lecture de {tei_file.name} : {e}")
            continue

        # -----------------------------
        # Tables
        # -----------------------------
        tables = tree.xpath("//tei:table", namespaces=NS)

        for i, table in enumerate(tables, 1):

            tables_file.write("=" * 80 + "\n")
            tables_file.write(f"FICHIER : {tei_file.name}\n")
            tables_file.write(f"TABLE {i}\n")
            tables_file.write("=" * 80 + "\n\n")

            # Copie de la table
            table_copy = deepcopy(table)

            # On ne conserve que le premier row
            rows = table_copy.xpath("./tei:row", namespaces=NS)

            for row in rows[1:]:
                table_copy.remove(row)

            tables_file.write(
                etree.tostring(
                    table_copy,
                    pretty_print=True,
                    encoding="unicode"
                )
            )

            tables_file.write("\n\n")

        # -----------------------------
        # Listes
        # -----------------------------
        lists = tree.xpath("//tei:list", namespaces=NS)

        for i, lst in enumerate(lists, 1):

            lists_file.write("=" * 80 + "\n")
            lists_file.write(f"FICHIER : {tei_file.name}\n")
            lists_file.write(f"LISTE {i}\n")
            lists_file.write("=" * 80 + "\n\n")

            # Copie de la liste
            list_copy = deepcopy(lst)

            # On ne conserve que les trois premiers items
            items = list_copy.xpath("./tei:item", namespaces=NS)

            for item in items[3:]:
                list_copy.remove(item)

            lists_file.write(
                etree.tostring(
                    list_copy,
                    pretty_print=True,
                    encoding="unicode"
                )
            )

            lists_file.write("\n\n")

print("\nExtraction terminée.")
print(f"Tables enregistrées dans : {tables_output}")
print(f"Listes enregistrées dans : {lists_output}")