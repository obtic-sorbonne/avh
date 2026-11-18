import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

NS = "{http://www.tei-c.org/ns/1.0}"
ET.register_namespace("", "http://www.tei-c.org/ns/1.0")

def ajouter_change(root, message, who):
    """Ajoute un <change> en premier dans <revisionDesc>."""
    # Trouver teiHeader
    teiHeader = root.find(f".//{NS}teiHeader")
    if teiHeader is None:
        return False

    # Trouver ou créer revisionDesc
    revisionDesc = teiHeader.find(f".//{NS}revisionDesc")
    if revisionDesc is None:
        revisionDesc = ET.SubElement(teiHeader, f"{NS}revisionDesc")

    # Créer la balise <change>
    change = ET.Element(f"{NS}change")
    change.set("when", datetime.now().strftime("%Y-%m-%d"))
    change.set("who", who)
    change.text = message

    # Insérer en premier
    revisionDesc.insert(0, change)

    return True


def traiter_dossier(dossier_entree):
    # Création du dossier de sortie avec sys
    dossier_sortie = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(dossier_sortie, exist_ok=True)

    print(f"Dossier de sortie créé : {dossier_sortie}")

    for fichier in os.listdir(dossier_entree):
        if not fichier.lower().endswith(".xml"):
            continue

        chemin_in = os.path.join(dossier_entree, fichier)
        chemin_out = os.path.join(dossier_sortie, fichier)

        try:
            tree = ET.parse(chemin_in)
            root = tree.getroot()

            # Ajout du <change>
            ok = ajouter_change(
                root,
                message="Corrections de divers éléments (balises, erreurs ORC, coupures de mots, etc.)",
                who="#fchiffol"
            )

            if not ok:
                print(f"⚠ Aucun <teiHeader> trouvé dans {fichier}, fichier ignoré.")
                continue

            # Écriture du fichier modifié
            tree.write(chemin_out, encoding="utf-8", xml_declaration=True)
            print(f"✔ Fichier traité : {fichier}")

        except ET.ParseError:
            print(f"❌ Erreur de parsing dans {fichier}, fichier ignoré.")

    print("Traitement terminé.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python script.py <dossier_xml>")
        sys.exit(1)

    dossier_entree = sys.argv[1]
    traiter_dossier(dossier_entree)
