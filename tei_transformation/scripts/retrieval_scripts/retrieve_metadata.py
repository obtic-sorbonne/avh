"""
Récupération de métadonnées spécifiques dans
un dossier de fichiers XML-TEI
"""

import os
import csv
import sys
import xml.etree.ElementTree as ET

# Dossier contenant les fichiers XML-TEI
INPUT_DIR = sys.argv[1]
OUTPUT_CSV = "tei_metadata.csv"

# Namespace TEI (à adapter si besoin)
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

rows = []

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(".xml"):
        continue

    filepath = os.path.join(INPUT_DIR, filename)

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Extraction du title
        title_el = root.find(".//tei:titleStmt/tei:title", NS)
        title = title_el.text.strip() if title_el is not None and title_el.text else ""

        # Extraction de la date de création
        date_el = root.find(".//tei:creation/tei:date", NS)
        date = date_el.text.strip() if date_el is not None and date_el.text else ""

        rows.append([filename, title, date])

    except ET.ParseError as e:
        print(f"Erreur XML dans {filename} : {e}")

# Écriture du CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "title", "date"])
    writer.writerows(rows)

print(f"✔  CSV généré : {OUTPUT_CSV}")
