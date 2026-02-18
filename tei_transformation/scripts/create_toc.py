import os # Interaction avec le système d’exploitation
import re # Expressions régulières
import sys # Accès aux variables et fonctions du système
from lxml import etree # Pour créer et écrire le XML TEI
from datetime import date # Gestion des dates et heures

#Appel des fonctions utiles pour les modifications supplémentaires
from parameters.functions import (build_toc_from_node, 
    build_hierarchical_toc, normalize_dates, 
    group_all_heads, transform_footer_info)


def process_tei(xml_path, output_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    # ======================================================
    # - Fonctions de groupement, normalisation et encodage -
    # ======================================================
    group_all_heads(root)
    normalize_dates(root)
    transform_footer_info(root)

    # ======================================================
    # -- Génération TOC --
    # ======================================================

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}  # ← important

    toc_div = build_hierarchical_toc(root)

    body = root.find(".//tei:body", namespaces=ns)
    if body is not None:
        body.insert(0, toc_div)
    else:
        root.insert(0, toc_div)

    # ======================================================
    # -- Ajout d'une entrée de révision unique --
    # ======================================================
    revision_desc_list = root.xpath("//tei:revisionDesc", namespaces=ns)
    if revision_desc_list:
        revision_desc = revision_desc_list[0]
        change_el = etree.Element("{http://www.tei-c.org/ns/1.0}change",
                                  when=date.today().isoformat(),
                                  who="#fchiffol")
        change_el.text = "Corrections structurelles et génération de la table des matières"
        revision_desc.insert(0, change_el)

    # ======================================================
    # Sauvegarde
    # ======================================================
    tree.write(output_path, pretty_print=True, encoding="utf-8", xml_declaration=True)
    print(f"✅ {output_path}")


# ======================================================
# == Traitement d'un dossier complet de fichiers XML ==
# ======================================================
def batch_process_tei(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.endswith(".xml"):
            input_path = os.path.join(input_dir, fname)
            output_path = os.path.join(output_dir, fname)
            process_tei(input_path, output_path)
    print("✔  PROCESS DONE")

# ======================================================
# ============ Entrée en ligne de commande =============
# ======================================================
if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    batch_process_tei(input_dir, output_dir)

