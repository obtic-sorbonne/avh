import os
import re
import sys
from bs4 import BeautifulSoup

# Fonctions d’annotation existantes
from regex_entities_terms import persName
from regex_entities_terms import orgName
from regex_entities_terms import legislation
from regex_entities_terms import glossary


# ------------------------------
# Fonction d’annotation des termes de léglisation via regex
# ------------------------------
def annotate_terms_legislation(text, legislation, report_lines, filename, laws_counts):
    for pattern, id_def in legislation.items():
        for term_id, definition in id_def.items():

            def replacer(match):
                found = match.group(0)

                # compteur global
                laws_counts[term_id] = laws_counts.get(term_id, 0) + 1

                term_tag = f'<term ref="#{term_id}">{found}</term><note type="legislation">{definition}</note>'

                report_lines.append(f"- {found}' → ref=\"#{term_id}\"")
                return term_tag

            text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)

    return text

# ------------------------------
# Fonction d’annotation des termes de glossaire via regex
# ------------------------------
def annotate_terms_glossary(text, glossary, report_lines, filename, gloss_counts):
    for pattern, id_def in glossary.items():
        for term_id, definition in id_def.items():

            def replacer(match):
                found = match.group(0)

                # compteur global
                gloss_counts[term_id] = gloss_counts.get(term_id, 0) + 1

                term_tag = f'<term ref="#{term_id}">{found}</term><note type="gloss">{definition}</note>'

                report_lines.append(f"- {found}' → ref=\"#{term_id}\"")
                return term_tag

            text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)

    return text


# ------------------------------
# SCRIPT PRINCIPAL
# ------------------------------

report_lines = []
report_lines.append("=== Rapport d’annotation TEI ===\n")

# Compteurs globaux des entités
pers_counts = {}
org_counts = {}
laws_counts = {}
gloss_counts = {}


for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        report_lines.append(f"Fichier : {filename}")
        if not filename.lower().endswith(".xml"):
            continue

        with open(os.path.join(sys.argv[1], filename), "r", encoding="utf-8") as file_in:
            print("reading from " + sys.argv[1] + filename)
            soup = BeautifulSoup(file_in, "xml")

        # Prologue TEI
        declaration = '<?xml version="1.0" encoding="utf-8"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0">'
        end = "</TEI>"

        header = soup.find("teiHeader")
        revision = soup.find("revisionDesc")

        # Ajout du <change>
        new_change = soup.new_tag("change", who="#fchiffol")
        new_change['when'] = sys.argv[4]
        new_change.string = "Annotation des entités nommées et des termes de législation et glossaire via regex"
        revision.insert(0, new_change)

        # ------------------------------
        # ENCODAGE UNIQUEMENT DANS <div type="text">
        # en excluant totalement les balises interdites
        # ------------------------------

        ns = "{" + soup.find().namespace + "}"
        forbidden = {f"{ns}list", f"{ns}table", f"{ns}item", f"{ns}cell", f"{ns}ref", f"{ns}note"}

        body = soup.find("text")

        for div in body.find_all("div"):
            # On encode uniquement les div type="text"
            if div.get("type") != "text":
                continue

            # Si le div contient une balise interdite → on saute complètement
            if div.find(forbidden):
                continue

            # Contenu interne du div
            div_content = div.decode_contents()

            # Parse interne pour protéger les balises interdites
            div_soup = BeautifulSoup(div_content, "xml")

            protected = {}
            for i, bad in enumerate(div_soup.find_all(forbidden)):
                key = f"__PROTECTED_{i}__"
                protected[key] = bad.decode_contents()
                bad.clear()
                bad.append(key)


            # ------------------------------
            # 1) Annotation persName
            # ------------------------------
            report_lines.append("\n-- Termes encodés en persName --")
            encoded, pers_matches = persName(div_soup.decode_contents())
            if pers_matches:
                for ref, found_list in pers_matches.items():
                    for found in found_list:
                        report_lines.append(f"- {found}' → ref=\"#{ref}\"")
                    pers_counts[ref] = pers_counts.get(ref, 0) + len(found_list)

            # ------------------------------
            # 2) Annotation orgName
            # ------------------------------
            report_lines.append("\n-- Termes encodés en orgName --")
            encoded, org_matches = orgName(encoded)
            if org_matches:
                for ref, found_list in org_matches.items():
                    for found in found_list:
                        report_lines.append(f"- {found}' → ref=\"#{ref}\"")
                    org_counts[ref] = org_counts.get(ref, 0) + len(found_list)

            # ------------------------------
            # 3) Annotation des termes
            # ------------------------------
            report_lines.append("\n-- Termes encodés en <note type=\"legislation\"> --")
            encoded = annotate_terms_legislation(encoded, legislation, report_lines, filename, laws_counts)
            
            report_lines.append("\n-- Termes encodés en <note type=\"gloss\"> --")
            encoded = annotate_terms_glossary(encoded, glossary, report_lines, filename, gloss_counts)

            report_lines.append(f"\n")

            # ------------------------------
            # 4) Restauration des balises interdites
            # ------------------------------
            for key, original in protected.items():
                encoded = encoded.replace(key, original)

            # ------------------------------
            # 5) Réinjection dans le <div>
            # ------------------------------
            # Reparse le fragment pour éviter l'échappement des balises
            fragment = BeautifulSoup(encoded, "xml")

            div.clear()
            for child in fragment.contents:
                div.append(child)

            # ------------------------------
            # Écriture du fichier XML modifié
            # ------------------------------
            output_path = os.path.join(sys.argv[2], filename)

            with open(output_path, "w", encoding="utf-8") as file_out:
                print("writing to " + output_path)
                file_out.write(declaration)
                file_out.write(str(header))
                file_out.write(str(body))
                file_out.write(end)

# ------------------------------
# Résumé final des occurrences
# ------------------------------
report_lines.append("\n=== Compteur global des occurrences persName ===")
for ref, count in sorted(pers_counts.items()):
    report_lines.append(f"- {ref} : {count} occurrence(s)")

report_lines.append("\n=== Compteur global des occurrences orgName ===")
for ref, count in sorted(org_counts.items()):
    report_lines.append(f"- {ref} : {count} occurrence(s)")

report_lines.append("\n=== Compteur global des termes législatifs ===")
for term_id, count in sorted(laws_counts.items()):
    report_lines.append(f"- {term_id} : {count} occurrence(s)")

report_lines.append("\n=== Compteur global des termes du glossaire ===")
for term_id, count in sorted(gloss_counts.items()):
    report_lines.append(f"- {term_id} : {count} occurrence(s)")

# ------------------------------
# Écriture du rapport
# ------------------------------
with open(sys.argv[3], "w", encoding="utf-8") as rep:
    rep.write("\n".join(report_lines))

print("Annotation terminée. Rapport généré.")

