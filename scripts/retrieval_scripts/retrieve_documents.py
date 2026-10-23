"""
Récupération dans un dossier de fichiers
depuis un dossier de dossiers selon les
spécificités de son extension et/ou fin
de nom de fichier
"""

import os
import sys
import shutil


def collect_html_files(source_dir, dest_dir):
    # Crée le dossier de destination s'il n'existe pas
    os.makedirs(dest_dir, exist_ok=True)
    
    # Parcours récursif des sous-dossiers
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(sys.argv[3]):
                source_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)

                # Gérer les doublons de noms
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dest_dir, f"{base}_{i}{ext}")
                        i += 1

                shutil.copy2(source_path, dest_path)
                print(f"✅ : {source_path} → {dest_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Utilisation : python collect_html.py <dossier_source> <dossier_destination> <file_ending>")
        sys.exit(1)

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    collect_html_files(source_dir, dest_dir)
print("✔  Documents récupérés")
