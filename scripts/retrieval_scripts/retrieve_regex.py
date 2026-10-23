"""
Récupération des noms de fichiers et 
du contexte de présence dans le texte,
selon les expressions régulières fournis
"""

import os
import re
import json
import sys

# ---------- CONFIG ----------
INPUT_FOLDER = sys.argv[1]   # dossier contenant les fichiers TEI
OUTPUT_FILE = "results_list.py"
WINDOW_BEFORE = 2  # tokens avant
WINDOW_AFTER = 2   # tokens après

# ---------- REGEX SIMPLIFIÉES ----------
REGEXES = [
    r''
]

# ---------- FONCTION DE LECTURE DU FICHIER TEI BRUT ----------
def read_tei_file(file_path):
    """
    Lit le fichier TEI comme texte brut en utf-8 pour ne pas perdre les balises.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # normaliser les retours à la ligne pour la regex
    return text.replace("\n", " ").replace("\r", " ")

# ---------- FONCTION DE RECHERCHE DES FORMULES AVEC CONTEXTE ----------
def find_contexts(text):
    """
    Pour chaque regex, cherche toutes les occurrences et retourne le contexte
    de 2 tokens avant et 2 tokens après.
    """
    tokens = re.findall(r'\S+', text)
    results = []

    # reconstruire les positions des tokens pour retrouver le contexte exact
    positions = []
    index = 0
    for t in tokens:
        start = text.find(t, index)
        positions.append((start, start + len(t)))
        index = start + len(t)

    for regex in REGEXES:
        for match in re.finditer(regex, text, flags=re.DOTALL):
            start_idx, end_idx = match.start(), match.end()
            token_indices = [i for i, (s, e) in enumerate(positions) if not (e <= start_idx or s >= end_idx)]
            if not token_indices:
                continue
            first_token = max(0, token_indices[0] - WINDOW_BEFORE)
            last_token = min(len(tokens), token_indices[-1] + WINDOW_AFTER + 1)
            context = tokens[first_token:last_token]
            results.append(" ".join(context))

    return results

# ---------- PARCOURS DU DOSSIER ----------
all_results = []

for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".xml"):
        filepath = os.path.join(INPUT_FOLDER, filename)
        try:
            text = read_tei_file(filepath)
        except UnicodeDecodeError:
            print(f"Erreur d'encodage sur {filename}, fichier ignoré")
            continue

        contexts = find_contexts(text)
        for ctx in contexts:
            all_results.append({
                "file": filename,
                "context": ctx
            })

# ---------- ÉCRITURE DANS UN FICHIER PYTHON ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("results = ")
    f.write(json.dumps(all_results, ensure_ascii=False, indent=4))

print(f"✔  {len(all_results)} contextes trouvés. Résultats dans '{OUTPUT_FILE}'")
