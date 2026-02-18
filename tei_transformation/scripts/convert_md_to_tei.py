import json # Sérialisation et désérialisation de données en JSON
import os # Interaction avec le système d’exploitation
import re # Expressions régulières
import sys # Accès aux variables et fonctions du système
from bs4 import BeautifulSoup  # Pour parser le HTML
from lxml import etree        # Pour créer et écrire le XML TEI
from datetime import date # Gestion des dates et heures

#Appel de variables pour remplir les métadonnées
from parameters.variables import (projectDesctext, seriesStmttext, countrytext, 
    settlementtext, institutiontext, repositorytext, digitizationtext, 
    digitizationresp, transcriptiontext, transcriptionresp, encodingtext, 
    encodingresp, hyphenationtext, quotationtext, authoritytext, 
    collectiontext)

#Appel des fonctions utiles pour l'encodage
from parameters.functions import (markdown_to_html, clean_text, slugify, 
    text_enrichment, list_encoding, encode_elements,
    insert_foliation, normalize_dates)

#Appel du contenu des métadonnées JSON
from parameters.metadata_json import inject_metadata


def md_to_tei(md_path, tei_path, metadata):
    html = markdown_to_html(md_path)
    soup = BeautifulSoup(html, "html.parser")

    # Création de l'élément racine TEI avec namespace
    NS = "http://www.tei-c.org/ns/1.0"
    tei = etree.Element("{%s}TEI" % NS, nsmap={None: NS})

    # --- Création du teiHeader et des métadonnées de base ---
    teiHeader = etree.SubElement(tei, "teiHeader")
    fileDesc = etree.SubElement(teiHeader, "fileDesc")
    encodingDesc = etree.SubElement(teiHeader, "encodingDesc")
    profileDesc = etree.SubElement(teiHeader, "profileDesc")
    revisionDesc = etree.SubElement(teiHeader, "revisionDesc")
    
    titleStmt = etree.SubElement(fileDesc, "titleStmt")
    publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
    seriesStmt = etree.SubElement(fileDesc, "seriesStmt")
    sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
    textClass = etree.SubElement(profileDesc, "textClass")
    langUsage = etree.SubElement(profileDesc, "langUsage")
    etree.SubElement(langUsage, "language", ident="fr")

    # ======================================================
    # --- Ajout des éléments de <respStmt> ---
    # ======================================================
    digitization = etree.SubElement(titleStmt, "respStmt")
    etree.SubElement(digitization, "resp").text = digitizationtext
    etree.SubElement(digitization, "name").text = digitizationresp

    transcription = etree.SubElement(titleStmt, "respStmt")
    etree.SubElement(transcription, "resp").text = transcriptiontext
    etree.SubElement(transcription, "name").text = transcriptionresp

    encoding = etree.SubElement(titleStmt, "respStmt")
    etree.SubElement(encoding, "resp").text = encodingtext
    etree.SubElement(encoding, "name").text = encodingresp

    # ======================================================
    # --- Ajout d'une entrée de révision automatique ---
    # ======================================================
    etree.SubElement(
        revisionDesc,
        "change",
        when=date.today().isoformat(),
        who="#fchiffol"
    ).text = "Conversion du texte en XML-TEI"

    # ======================================================
    # --- Informations sur le projet ---
    # ======================================================
    projectDesc = etree.SubElement(encodingDesc, "projectDesc")
    etree.SubElement(projectDesc, "p").text = projectDesctext
    etree.SubElement(projectDesc, "p").text = "Métadonnées combinées: IA (Gemini) + SharePoint (Catalogue)"
    etree.SubElement(publicationStmt, "authority").text = authoritytext

    # ======================================================
    # --- Ajout du sourceDesc avec msDesc ---
    # ======================================================
    msDesc = etree.SubElement(sourceDesc, "msDesc")
    msIdentifier = etree.SubElement(msDesc, "msIdentifier")
    etree.SubElement(msIdentifier, "country").text = countrytext
    etree.SubElement(msIdentifier, "settlement").text = settlementtext
    etree.SubElement(msIdentifier, "institution").text = institutiontext
    etree.SubElement(msIdentifier, "repository").text = repositorytext
    etree.SubElement(msIdentifier, "collection").text = collectiontext

    # ======================================================
    # --- Ajout d'informations d'édition ---
    # ======================================================
    editorialDecl = etree.SubElement(encodingDesc, "editorialDecl")
    hyphenation = etree.SubElement(editorialDecl, 'hyphenation', eol="none")
    etree.SubElement(hyphenation, "p").text = hyphenationtext
    quotation = etree.SubElement(editorialDecl, "quotation")
    etree.SubElement(quotation, "p").text = quotationtext

    # ======================================================
    # --- Ajout d'un seriesStmt ---
    # ======================================================
    etree.SubElement(seriesStmt, "title", type="main").text = seriesStmttext


    inject_metadata(metadata, titleStmt, publicationStmt, profileDesc, seriesStmt, textClass, msDesc, slugify)

    # ======================================================
    # --- Corps du texte ---
    # ======================================================
    text = etree.SubElement(tei, "text")
    body = etree.SubElement(text, "body")
    div = etree.SubElement(body, "div", type="text")

    # Crée une seule div TEI englobante
    main_div = etree.SubElement(div, "{%s}div" % NS, type="main")

    # Parcours des paragraphes HTML
    for elem in soup.find_all(["p", "h1", "h2", "h3", "h4", "blockquote", "dl", "table", "figure", "ul", "ol", "article", "img"]):
        text = elem.get_text(strip=True)

        # Détection des marqueurs de page
        match = re.match(r"\[Page (\d+)\]", text)
        if match:
            pb = etree.SubElement(main_div, "{%s}pb" % NS)
            pb.set("n", match.group(1))
        else:
            encode_elements(elem, main_div)

    insert_foliation(tei)

    # ======================================================
    # --- Écriture du fichier TEI final ---
    # ======================================================
    os.makedirs(os.path.dirname(tei_path), exist_ok=True)
    etree.ElementTree(tei).write(tei_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
    print(f'✅ {tei_path}')


# ======================================================
# == Traitement d'un dossier complet de fichiers MD ==
# ======================================================
def batch_process_md(dossier_md, dossier_tei):
    for fichier in os.listdir(dossier_md):
        if fichier.endswith(".md"):
            chemin_md = os.path.join(dossier_md, fichier)
            nom_sans_ext = os.path.splitext(fichier)[0]
            chemin_tei = os.path.join(dossier_tei, nom_sans_ext + ".xml")

            # Lecture du JSON correspondant
            chemin_json = os.path.join(dossier_md, nom_sans_ext + ".json")
            if os.path.exists(chemin_json):
                with open(chemin_json, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            else:
                metadata = {}

            md_to_tei(chemin_md, chemin_tei, metadata)
    print("✔  TRANSFORMATION DONE")

# ======================================================
# ============ Entrée en ligne de commande =============
# ======================================================
if __name__ == "__main__":
    dossier_source = sys.argv[1]  # premier argument : dossier HTML source
    dossier_sortie = sys.argv[2]  # deuxième argument : dossier de sortie TEI
    batch_process_md(dossier_source, dossier_sortie)
