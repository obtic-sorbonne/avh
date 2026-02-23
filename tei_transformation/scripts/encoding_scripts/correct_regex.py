"""
Correction du bruit et autres qui restent de l'OCR
"""

import os
import re
import sys
from parameters.regex import REPLACEMENTS

INPUT_FOLDER = sys.argv[1]    # dossier contenant les fichiers TEI
OUTPUT_FOLDER = sys.argv[2]   # dossier où sauvegarder les fichiers corrigés
LOG_FILE = "replacements.log"

# encodage : UTF-8 requis (TEI + caractères spéciaux)
ENCODING = "utf-8"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(LOG_FILE, "w", encoding=ENCODING) as log:

    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(".xml"):
            continue

        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(input_path, "r", encoding=ENCODING) as f:
            text = f.read()

        original_text = text
        file_changes = []

        for regex, replacement in REPLACEMENTS:
            matches = list(re.finditer(regex, text, flags=re.DOTALL))
            if not matches:
                continue

            for m in matches[:5]:  # limiter les exemples
                before = m.group(0)
                after = re.sub(regex, replacement, before, flags=re.DOTALL)
                file_changes.append((regex, before, after))

            text = re.sub(regex, replacement, text, flags=re.DOTALL)

        if file_changes:
            log.write(f"\n=== {filename} ===\n")
            for regex, before, after in file_changes:
                log.write(f"REGEX: {regex}\n")
                log.write(f"- AVANT: {before}\n")
                log.write(f"+ APRES: {after}\n\n")

        with open(output_path, "w", encoding=ENCODING) as f:
            f.write(text)

        print(f"✅ {filename} ({len(file_changes)} remplacements loggés).")

print(f"✔  DONE. Log écrit dans '{LOG_FILE}'.")


