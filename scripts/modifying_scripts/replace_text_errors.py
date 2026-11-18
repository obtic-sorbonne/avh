import os
import re
import sys
import xml.etree.ElementTree as ET

# Ton dictionnaire de corrections OCR
CORRECTIONS_OCR_first_version = {
    # Erreurs d'OCR courantes et substitutions de lettres
    "commecent": "commencent",
    "claissement": "classement",
    "intégrai": "intégral",
    "aiministration": "administration",
    "Aiministration": "Administration",
    "Aministration": "Administration",
    "Idminisiration": "Administration",
    "idminisiration": "administration",
    "procts-verbal": "procès-verbal",
    "Proces-verbal": "Procès-verbal",
    "constilulive": "constitutive",
    "protographiée": "photographiée",
    "iele": "elle",
    "IEle": "Elle",
    "buccursale": "succursale",
    "BUCCURSALE": "SUCCURSALE",
    "chaiz": "chaix",
    "chaik": "chaix",
    "CHAIZ": "CHAIX",
    "CHAIK": "CHAIX",
    "dubcisabauer": "dubois & bauer",
    "Aueugles": "Aveugles",
    "Averugies": "Aveugles",
    "Aueugies": "Aveugles",
    "Aveugels": "Aveugles",
    "honorair": "honoraire",
    "cputé": "député",
    "Consail": "Conseil",
    "orulaire": "oculaire",
    "Sénce": "Séance",
    "Sdance": "Séance",
    "Pévrier": "Février",
    "Médreine": "Médecine",
    "3o mai": "30 mai",
    "Francaise": "Française",
    "Veeux": "Vœux",
    "asscmblée": "assemblée",
    "cucillir": "cueillir",
    "renoulevable": "renouvelable",
    "crire": "écrire",
    "Blesses": "Blessées",
    "rgle": "règle",
    "biblioteque": "bibliothèque",
    "ues Avocats": "des Avocats",
    "Loterie de la Delle": "Loterie de la Dette",
    "TABLE DES MATIRES": "TABLE DES MATIÈRES",
    "Dépariemenlale": "Départementale",
    "clans": "dans", 
    "cst": "est", 
    "reclasscment": "reclassement", 
    "modeme": "moderne", 
    "s-mililaires": "s-militaires", 
    "mililaires": "militaires", 
    "Comil": "Comité", 
    "Modificalions": "Modifications",
    "Administralion": "Administration", 
    "applicalion": "application",
    "confesseur": "professeur",
    
    # Erreurs de segmentation (mots collés)
    "monjournal": "mon Journal",
    "lemanuel": "le Manuel",
    "généralet": "Général et",
    "larevue": "la Revue",
    "petitesvilles": "petites villes",
    "toujourssignifie": "toujours signifie",
    
    # Déformations de patronymes et noms propres
    "Bricux": "Brieux",
    "BrieUx": "Brieux",
    "Brikla": "Brieux",
    "Brikux": "Brieux",
    "BORBEL": "BORREL",
    "BRANDAS": "BRANDÈS",
    "Balfourif": "Balfourier",
    "Balpourier": "Balfourier",
    "Bartrou": "Barthou",
    "Valzert-Radot": "Vallery-Radot",
    "Valdery-Radoy": "Vallery-Radot",
    "GettY": "Getty",
    "Gritty": "Getty",
    "Mobra": "Morax",
    "Cabsagnac": "Cassagnac",
    "Gopart": "Godart",
    "Walrher": "Walther",
    "MALVV": "MALVY",
    "Pats": "Paté",
    "Dieqo": "Diego",
    "Krung": "Krug",
    "Quenille": "Queuille",
    "Toudsuri": "Toudouri",
    "E. I. D. A. C.": "F. I. D. A. C."
}

CORRECTIONS_OCR = {
    "M'": "Me",
    "M*": "Me",
    "M・": "Me",
    "M-": "Me",
    "Henin-Robert": "Henri-Robert",
    "IzAAc": "Izaac",
    "IzaAc": "Izaac",
    "D' COUTELA" : "Dr COUTELA",
    "D' RICORD" : "Dr RICORD",
    "D' Schneider" : "Dr Schneider",
    "D' Cugnier" : "Dr Cugnier",
    "D' Scineider" : "Dr Schneider",
    "D' RICORD" : "Dr RICORD",
    "D' Scunender" : "Dr Schneider",
    "D' Scunzder" : "Dr Schneider",
    "D' Soumeder" : "Dr Schneider",
    "D' Baudet" : "Dr Baudet",
    "D' Robin" : "Dr Robin",
    "D' Julié" : "Dr Julié",
    "D' Vacher" : "Dr Vacher",
    "D' Monnet" : "Dr Monnet",
    "D' Dufour" : "Dr Dufour",
    "D' Sainte-Rose" : "Dr Sainte-Rose",
    "D' Vinsonneau" : "Dr Vinsonneau",
    "D' Delante" : "Dr Delante",
    "D' Scimeider" : "Dr Schneider",
    "D' René" : "Dr Dufour",
    "D' Scunetder" : "Dr Schneider",
    "D' Dvariansky" : "Dr Dvariansky",
    "Scuneder" : "Schneider",
    "Traversat" : "Traversay",
}

def nettoyer_texte(texte, dictionnaire_corrections):
    """
    Remplace chaque clé du dictionnaire par sa valeur,
    en utilisant une regex avec bordures de mots.
    Retourne le texte corrigé + la liste des corrections effectuées.
    """
    corrections_effectuees = []

    # Tri pour éviter les collisions (mots composés)
    mots_tries = sorted(dictionnaire_corrections.keys(), key=len, reverse=True)

    for erreur in mots_tries:
        correction = dictionnaire_corrections[erreur]

        # Regex avec bordures de mots
        pattern = r'(?<!\w)' + re.escape(erreur) + r'(?!\w)'

        # Recherche des occurrences AVANT remplacement
        for m in re.finditer(pattern, texte):
            start, end = m.start(), m.end()
            avant = texte[max(0, start - 40):start]
            apres = texte[end:end + 40]

            corrections_effectuees.append({
                "erreur": erreur,
                "correction": correction,
                "avant": avant,
                "apres": apres
            })

        # Remplacement
        texte = re.sub(pattern, correction, texte)

    return texte, corrections_effectuees


def traiter_dossier_xml(dossier_entree, dossier_sortie, rapport_path):
    rapport = []

    for fichier in os.listdir(dossier_entree):
        if not fichier.lower().endswith(".xml"):
            continue

        xml_in = os.path.join(dossier_entree, fichier)
        xml_out = os.path.join(dossier_sortie, fichier)

        # Lecture du XML brut
        with open(xml_in, "r", encoding="utf-8") as f:
            contenu = f.read()

        # Nettoyage + corrections
        contenu_corrige, corrections = nettoyer_texte(contenu, CORRECTIONS_OCR)

        # Écriture du XML corrigé
        with open(xml_out, "w", encoding="utf-8") as f:
            f.write(contenu_corrige)

        print(f"✔ Fichier corrigé : {xml_out}")

        # Ajout au rapport
        for c in corrections:
            rapport.append(
                f"=== {fichier} ===\n"
                f"Erreur : {c['erreur']} → {c['correction']}\n"
                f"Contexte avant : {c['avant']}\n"
                f"Contexte après : {c['apres']}\n"
                f"----------------------------------------\n"
            )

    # Écriture du rapport
    with open(rapport_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rapport))

    print(f"📄 Rapport généré : {rapport_path}")


# --- Utilisation ---
if __name__ == "__main__":
    dossier_entree = sys.argv[1]
    dossier_sortie = sys.argv[2]
    rapport_path = sys.argv[3]

    traiter_dossier_xml(dossier_entree, dossier_sortie, rapport_path)
