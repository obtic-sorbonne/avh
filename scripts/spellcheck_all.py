# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: March 2025
- description: Recovering orthographic errors in DOCX or PDF files
- input: DOCX or PDF files
- output: A single dictionary containing all errors without duplicates
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3

    arg1: folder of the DOCX or PDF files
    arg2: name of the output Python file

"""

import os
import sys
from spellchecker import SpellChecker
import docx
from PyPDF2 import PdfReader

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

# Initialize the global dictionary to store all errors
all_errors = set()  # Use a set to ensure there are no duplicates

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        file_path = os.path.join(root, filename)
        content = ""

        if filename.endswith('.docx'):
            content = read_docx(file_path)
        elif filename.endswith('.pdf'):
            content = read_pdf(file_path)
        else:
            print(f"Unsupported file format: {filename}")
            continue

        print(f"Reading from {filename}")

        for line in content.split('\n'):
            line = suppress_punctuation(line).lower()  # Normalize to lowercase
            words = line.split()
            misspelled = spell.unknown(words)
            for word in misspelled:
                all_errors.add(word.lower())  # Add only unique words

# Convert the set to a dictionary
errors_dict = {"errors": list(all_errors)}

# Write all errors to a single output file
output_file = sys.argv[2]
with open(output_file, "w") as file_out:
    print(f"Writing all errors to {output_file}")
    file_out.write("errors_dict = ")
    file_out.write(str(errors_dict).replace("',", "',\n"))
