#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de correction des mots coupés par un tiret dans les fichiers TEI-XML (Version 2).
=======================================================================================
Modifications v2 :
- Protection explicite des balises de saut de page <pb/> : tout tiret suivi par une
  balise <pb/> (ex: "cama-<pb n="2"/>rades", "cama- <pb n="2"/> rades") est STRICTEMENT
  CONSERVÉ et NE DOIT PAS être modifié ni recollé.
- Traite les mots coupés par tiret-espace ('cama- rades' -> 'camarades').
- Traite les césures à travers les balises de saut de ligne <lb/> ('cama-<lb/>rades' -> 'cama<lb/>rades').
- Préserves les mots composés légitimes ('Buenos- Ayres' -> 'Buenos-Ayres').
- Génère un rapport Markdown détaillé indiquant toutes les modifications effectuées et les <pb> ignorés.
"""

import os
import re
import argparse

ALPHA_FR = r'a-zA-ZàâæçéèêëîïôœùûüÿA-ZÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸ'

# Exceptions : Mots composés réels pour lesquels le trait d'union doit être conservé
MOTS_COMPOUSES_PRESERVER = {
    'buenos-ayres', 'costa-rica', 'seine-inférieure', 'ille-et-vilaine', 'et-vilaine', 'et-loire', 'la-méline', 'el-hadid', 'saint-sébastien',
    'vice-président', 'sous-préfet', 'au-dessus', 'lui-même', 'peut-être', 'soi-même', "c'est-à-dire", 'à-dire',
    'nord-ouest', 'sud-est', 'anti-mitrailleur', 'franco-allemand', 'sous-officier', 'sous-officiers', 'sous-préfecture', 'saône-et', 'saint-gaultier',
    'sur-yonne', 'haute-marne', 'enghien-les', 'et-oise', 'franceville-plage', 'jean-baptiste', 'alpes-maritimes', 'honneur-la', 'du-rhône', 'grande-duchesse',
    'barbe-bleue', 'docteur-chanteloube', 'pointe-rouge', 'paul-albert', 'seine-maritime', 'ste-valdrée', 'union-incendie', 'automobile-club', 'rottin-malaunay',
    'celui-ci', 'benoît-delpech', 'de-castillon', 'saint-malo', 'jésus-christ', 'donnons-ci', 'timbres-recouvrements', 'du-guat', 'cuisine-salle', 'sous-lieutenant',
    'indre-et', "maître-pointeur", 'sur-loire', 'vice-présidents'
}

# Protection v3 : Détection de tout tiret suivi par une ouverture de balise XML (sauf <lb...>)
REGEX_HYPHEN_TAG = re.compile(
    r'\b(?P<part1>[' + ALPHA_FR + r']+)-\s*(?P<tag><(?!lb\b)[a-zA-Z_:][^>]*\/?>)',
    re.UNICODE | re.IGNORECASE
)

# Regex 1 : Mot coupé par un tiret suivi d'un ou plusieurs espaces dans du texte brut (ex: "cama- rades")
REGEX_HYPHEN_SPACE = re.compile(
    r'\b(?P<part1>[' + ALPHA_FR + r']+)-\s+(?P<part2>[' + ALPHA_FR + r']+)\b',
    re.UNICODE
)

# Regex 2 : Césure traversant une balise TEI <lb/> (ex: "cama-<lb n="12"/>rades")
REGEX_HYPHEN_LB = re.compile(
    r'\b(?P<part1>[' + ALPHA_FR + r']+)-\s*(?P<lb><lb\b[^>]*\/?>)\s*(?P<part2>[' + ALPHA_FR + r']+)\b',
    re.UNICODE
)

def traiter_fichier_tei(chemin_fichier, dossier_sortie=None):
    """
    Lit un fichier TEI XML, recolle les mots coupés (hors balises d'ouverture protégées) et enregistre le fichier nettoyé.
    Retourne la liste des modifications enregistrées et la liste des ouvertures de balises ignorées.
    """
    nom_fichier = os.path.basename(chemin_fichier)
    with open(chemin_fichier, 'r', encoding='utf-8', errors='replace') as f:
        contenu = f.read()

    modifications = []
    ignores_tag = []

    # Étape 0 : Masquage de protection pour tout tiret suivi d'une ouverture de balise XML (sauf <lb...>)
    tag_matches = []
    def _mask_tag(m):
        tag_matches.append(m.group(0))
        idx = len(tag_matches) - 1
        tag_str = m.group('tag')
        ignores_tag.append({
            'fichier': nom_fichier,
            'expression': m.group(0),
            'tag': tag_str,
            'raison': f"Tiret suivi d'une ouverture de balise `{tag_str.split()[0].replace('<', '').replace('/>', '').replace('>', '')}` (Conservé intact)"
        })
        return f"__PROTECTED_TAG_{idx}__"

    contenu_protege = REGEX_HYPHEN_TAG.sub(_mask_tag, contenu)

    # Étape 1 : Protection des balises XML et traitement des mots coupés par un tiret + espace
    tokens = re.split(r'(<[^>]+>)', contenu_protege)
    for i in range(len(tokens)):
        # Si le token est du texte hors balise XML
        if not tokens[i].startswith('<'):
            def _sub_space(match):
                p1, p2 = match.group('part1'), match.group('part2')
                cle_comp = f"{p1}-{p2}".lower()
                
                if cle_comp in MOTS_COMPOUSES_PRESERVER:
                    correction = f"{p1}-{p2}"
                    typo = "Mot composé (Espace parasite supprimé après le tiret)"
                else:
                    correction = f"{p1}{p2}"
                    typo = "Mot simple recollé (Suppression tiret + espace)"

                modifications.append({
                    'fichier': nom_fichier,
                    'trouve': match.group(0),
                    'correction': correction,
                    'typologie': typo
                })
                return correction

            tokens[i] = REGEX_HYPHEN_SPACE.sub(_sub_space, tokens[i])

    contenu_intermediaire = "".join(tokens)

    # Étape 2 : Traitement des césures traversant les balises <lb/>
    def _sub_lb(match):
        p1 = match.group('part1')
        lb = match.group('lb')
        p2 = match.group('part2')
        cle_comp = f"{p1}-{p2}".lower()

        if cle_comp in MOTS_COMPOUSES_PRESERVER:
            correction = f"{p1}-{lb}{p2}"
            typo = "Mot composé maintenu à travers <lb/>"
        else:
            correction = f"{p1}{lb}{p2}"
            typo = "Mot simple recollé à travers <lb/>"

        modifications.append({
            'fichier': nom_fichier,
            'trouve': match.group(0),
            'correction': correction,
            'typologie': typo
        })
        return correction

    contenu_final = REGEX_HYPHEN_LB.sub(_sub_lb, contenu_intermediaire)

    # Étape 3 : Restauration des expressions protégées contenant une ouverture de balise XML
    for idx, orig in enumerate(tag_matches):
        contenu_final = contenu_final.replace(f"__PROTECTED_TAG_{idx}__", orig)

    # Sauvegarde du fichier nettoyé
    if dossier_sortie:
        os.makedirs(dossier_sortie, exist_ok=True)
        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
    else:
        chemin_sortie = chemin_fichier

    with open(chemin_sortie, 'w', encoding='utf-8') as f:
        f.write(contenu_final)

    return modifications, ignores_tag

def generer_rapport_markdown(toutes_modifications, tous_ignores_tag, chemin_rapport):
    """Génère un rapport Markdown détaillant les corrections et les ouvertures de balises ignorées."""
    lignes = []
    lignes.append("# Rapport de Corrections des Mots Coupés TEI-XML (v3)\n")
    lignes.append(f"- **Total des modifications effectuées :** `{len(toutes_modifications)}`")
    lignes.append(f"- **Total des tirets conservés intacts (suivis d'une ouverture de balise XML) :** `{len(tous_ignores_tag)}`\n")

    lignes.append("## 1. Modifications appliquées\n")
    if not toutes_modifications:
        lignes.append("Aucun mot coupé n'a été modifié.\n")
    else:
        lignes.append("| Document TEI | Forme brute (Trouvée) | Correction appliquée | Typologie de correction |")
        lignes.append("| :--- | :--- | :--- | :--- |")
        for mod in toutes_modifications:
            trouve_esc = mod['trouve'].replace('<', '&lt;').replace('>', '&gt;')
            corr_esc = mod['correction'].replace('<', '&lt;').replace('>', '&gt;')
            lignes.append(f"| `{mod['fichier']}` | **`{trouve_esc}`** | ` {corr_esc} ` | {mod['typologie']} |")

    lignes.append("\n## 2. Tirets suivis d'une ouverture de balise XML (Ignorés et conservés intacts)\n")
    if not tous_ignores_tag:
        lignes.append("Aucun tiret suivi d'une ouverture de balise n'a été rencontré.\n")
    else:
        lignes.append("| Document TEI | Expression détectée | Balise | Statut / Action |")
        lignes.append("| :--- | :--- | :--- | :--- |")
        for ig in tous_ignores_tag:
            expr_esc = ig['expression'].replace('<', '&lt;').replace('>', '&gt;')
            tag_esc = ig['tag'].replace('<', '&lt;').replace('>', '&gt;')
            lignes.append(f"| `{ig['fichier']}` | **`{expr_esc}`** | ` {tag_esc} ` | {ig['raison']} |")

    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        f.write("\n".join(lignes))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Recolle les mots coupés par tiret dans des fichiers TEI XML (v3 avec protection de toutes les ouvertures de balises XML).")
    parser.add_argument('--input', '-i', required=True, help="Fichier XML TEI ou dossier contenant des fichiers XML TEI")
    parser.add_argument('--output-dir', '-o', default=None, help="Dossier où sauvegarder les fichiers XML corrigés")
    parser.add_argument('--report', '-r', default="rapport_corrections_tei_v3.md", help="Chemin du rapport Markdown de sortie")

    args = parser.parse_args()

    fichiers = []
    if os.path.isfile(args.input):
        fichiers.append(args.input)
    elif os.path.isdir(args.input):
        for root, dirs, files in os.walk(args.input):
            for file in files:
                if file.endswith('.xml') or file.endswith('.tei'):
                    fichiers.append(os.path.join(root, file))

    toutes_mods = []
    tous_ignores = []
    for f in fichiers:
        mods, ignores = traiter_fichier_tei(f, args.output_dir)
        toutes_mods.extend(mods)
        tous_ignores.extend(ignores)

    generer_rapport_markdown(toutes_mods, tous_ignores, args.report)
    print(f"Traité {len(fichiers)} fichier(s). Modifications: {len(toutes_mods)}. Conservés (balises): {len(tous_ignores)}.")
    print(f"Rapport généré dans: {args.report}")
