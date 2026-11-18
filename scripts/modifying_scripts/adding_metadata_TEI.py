import json
import os
import sys
import xml.etree.ElementTree as ET
import re
import unicodedata
import datetime

# --- Normalisation des mots-clés pour l'attribut @ref ---
def normalize_term(term):
    term = term.lower()
    # Décomposition Unicode et suppression des accents
    term = ''.join(c for c in unicodedata.normalize('NFD', term) if unicodedata.category(c) != 'Mn')
    term = term.replace(" ", "-")
    # Suppression des caractères non alphanumériques sauf "-"
    term = ''.join(c for c in term if c.isalnum() or c == "-")
    return term.strip("-")

# --- Fonction principale ---
def process_json_to_tei(json_path, dossier_xml_entree, dossier_xml_sortie):
    # Charger le JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Parcourir les collections
    for collection_name, items in data["collections"].items():
        for item in items:
            fichier = item["fichier"]
            resume = item["resume"]
            sujets = item["sujets"]
            mots_cles = item["mots_cles"]

            # Chemin du fichier XML source
            xml_in = os.path.join(dossier_xml_entree, fichier.replace(".docx", ".xml"))
            xml_out = os.path.join(dossier_xml_sortie, fichier.replace(".docx", ".xml"))

            if not os.path.exists(xml_in):
                print(f"⚠️ Fichier XML introuvable : {xml_in}")
                continue

            # Charger le TEI existant
            tree = ET.parse(xml_in)
            root = tree.getroot()

            # Trouver <teiHeader>
            header = root.find(".//{http://www.tei-c.org/ns/1.0}teiHeader")
            if header is None:
                print(f"⚠️ Pas de teiHeader dans {xml_in}")
                continue

            # --- 1. Ajouter / remplacer <abstract> ---
            profile_desc = header.find(".//{http://www.tei-c.org/ns/1.0}profileDesc")
            if profile_desc is None:
                profile_desc = ET.SubElement(header, "profileDesc")

            abstract = profile_desc.find("{http://www.tei-c.org/ns/1.0}abstract")
            if abstract is None:
                abstract = ET.SubElement(profile_desc, "abstract")
                p = ET.SubElement(abstract, "p")

            p.text = resume

            # --- 2. Ajouter <seriesStmt> avec les sujets ---
            file_desc = header.find(".//{http://www.tei-c.org/ns/1.0}fileDesc")
            if file_desc is None:
                file_desc = ET.SubElement(header, "fileDesc")

            series_stmt = file_desc.find("{http://www.tei-c.org/ns/1.0}seriesStmt")
            if series_stmt is None:
                series_stmt = ET.SubElement(file_desc, "seriesStmt")

            t = ET.SubElement(series_stmt, "title")
            t.set("type", "genre")
            t.text = "Journal"

            for sujet in sujets:
                t = ET.SubElement(series_stmt, "title")
                t.set("type", "topic")
                t.text = sujet

            # --- 3. Ajouter les mots-clés dans <textClass> ---
            text_class = profile_desc.find("{http://www.tei-c.org/ns/1.0}textClass")
            if text_class is None:
                text_class = ET.SubElement(profile_desc, "textClass")

            # Ajouter keywords
            keywords = text_class.find("{http://www.tei-c.org/ns/1.0}keywords")
            if keywords is None:
                keywords = ET.SubElement(text_class, "keywords")

            for mot in mots_cles:
                term = ET.SubElement(keywords, "term")
                term.set("ref", f"#{normalize_term(mot)}")
                term.text = mot

            # Ajouter classCode DDC
            class_code = ET.SubElement(text_class, "classCode")
            class_code.set("scheme", "DDC")
            class_code.text = "362.41"

            # --- Ajouter une entrée <change> dans <revisionDesc> ---
            revision_desc = header.find(".//{http://www.tei-c.org/ns/1.0}revisionDesc")
            if revision_desc is None:
                revision_desc = ET.SubElement(header, "{http://www.tei-c.org/ns/1.0}revisionDesc")

            # Créer l'élément sans l'ajouter
            change = ET.Element("{http://www.tei-c.org/ns/1.0}change")
            change.set("when", sys.argv[4])
            change.set("who", "#fchiffol")
            change.text = "Ajout de nouvelles métadonnées (abstract, topic, keywords)"

            # L'insérer en première position
            revision_desc.insert(0, change)


            ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

            # --- 4. Sauvegarde ---
            tree.write(xml_out, encoding="utf-8", xml_declaration=True)
            print(f"✔️ Fichier écrit : {xml_out}")


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    process_json_to_tei(
        json_path=sys.argv[1],
        dossier_xml_entree=sys.argv[2],
        dossier_xml_sortie=sys.argv[3]
    )