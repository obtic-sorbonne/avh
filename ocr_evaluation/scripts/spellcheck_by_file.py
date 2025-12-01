import os
import sys
from spellchecker import SpellChecker  # Utilise pyspellchecker
import docx
from PyPDF2 import PdfReader
from valid_names import valid_names  # Liste des noms valides à importer

# Initialisation de SpellChecker
spell = SpellChecker(language="fr", case_sensitive=True)

def suppress_punctuation(text):
    """ Suppress punctuation in a text """
    punctuation = "!:;\",?'’.()»•«"
    for sign in punctuation:
        text = text.replace(sign, " ")
    return text

def read_docx(file_path):
    """ Read content from a DOCX file """
    doc = docx.Document(file_path)
    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return content

def read_pdf(file_path):
    """ Read content from a PDF file """
    reader = PdfReader(file_path)
    content = "\n".join([page.extract_text() for page in reader.pages])
    return content

def categorize_words(word_list, valid_names):
    """ Categorize words into specific groups based on criteria and count elements in each category. """
    categorized = {
        "valid_names": {"words": set(), "count": 0},
        "start_or_end_with_dash": {"words": set(), "count": 0},
        "contains_dash": {"words": set(), "count": 0},
        "contains_digits": {"words": set(), "count": 0},
        "stuck_words": {"words": set(), "count": 0},
        "others": {"words": set(), "count": 0}
    }

    for word in word_list:
        word = word.strip()  # Nettoyage des espaces inutiles

        if word in valid_names:
            categorized["valid_names"]["words"].add(word)
        elif any(char.isdigit() for char in word):
            categorized["contains_digits"]["words"].add(word)
        elif word.startswith('-') or word.endswith('-'):
            categorized["start_or_end_with_dash"]["words"].add(word)
        elif '-' in word:  # Vérifie les tirets ailleurs
            if word not in categorized["start_or_end_with_dash"]["words"]:
                categorized["contains_dash"]["words"].add(word)
        elif len(word) > 10:  # Mots de plus de 10 caractères
            categorized["stuck_words"]["words"].add(word)
        else:
            categorized["others"]["words"].add(word)

    # Calcul des comptes par catégorie
    for category in categorized:
        categorized[category]["count"] = len(categorized[category]["words"])
    
    return categorized

def write_results_to_file(errors_by_file, output_file):
    """ Write the categorized results into a new file """
    try:
        with open(output_file, "w", encoding="utf-8") as file_out:
            for filename, result in errors_by_file.items():
                file_out.write(f"Fichier : {filename}\n")
                for category, details in result.items():
                    # Convertir le set en liste pour une écriture lisible
                    file_out.write(f"{category}: {details['count']} mots\n")
                    file_out.write("[" + '", "'.join(sorted(details['words'])) + "]\n\n")
                file_out.write("\n")
        print(f"Les résultats ont été écrits avec succès dans {output_file}.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'écriture dans le fichier : {e}")

# Dictionnaire pour stocker les erreurs catégorisées par fichier
errors_by_file = {}

# Parcours des fichiers dans le dossier spécifié
for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        file_path = os.path.join(root, filename)
        content = ""

        # Lecture des fichiers DOCX et PDF
        if filename.endswith('.docx'):
            content = read_docx(file_path)
        elif filename.endswith('.pdf'):
            content = read_pdf(file_path)
        else:
            print(f"Unsupported file format: {filename}")
            continue

        print(f"Processing file: {filename}")

        # Diviser le contenu en lignes, puis en mots, et récupérer les mots non reconnus
        words_in_file = []
        for line in content.split('\n'):
            line = suppress_punctuation(line).lower()  # Normaliser en minuscules
            words = line.split()
            misspelled = spell.unknown(words)  # Récupérer les mots mal orthographiés
            words_in_file.extend(misspelled)

        # Catégoriser les mots pour chaque fichier
        errors_by_file[filename] = categorize_words(words_in_file, valid_names)

# Spécifier le fichier de sortie
output_file = sys.argv[2]
write_results_to_file(errors_by_file, output_file)
