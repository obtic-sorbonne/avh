import os
import re
import sys
from lxml import etree

from parameters.functions import (
    replace_first_pb, add_breakno_pb,
    p_to_list_regex)

# -------------------------------------------------------------------------
# Traitement principal XML : transformation des séquences </p> <pb> <note> <p>
# -------------------------------------------------------------------------
def process_xml(chemin_in: str, chemin_out: str):
    with open(chemin_in, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # --- NOUVEAU : remplacer <pb n="1"/> avant tout le reste ---
    xml_content = replace_first_pb(xml_content)

# 2️⃣ Transformer les séquences </p><pb><note><p> correctement
    pattern = re.compile(
        r"""</p>\s*
            (?P<pb><pb\b[^>]*?(?:/?>))\s*
            (?P<note><note\b[^>]*?>.*?</note>)\s*
            <p>
        """,
        re.DOTALL | re.IGNORECASE | re.VERBOSE
    )

    out_parts = []
    last_pos = 0

    for m in pattern.finditer(xml_content):
        start, end = m.start(), m.end()
        pb_tag, note_tag = m.group("pb"), m.group("note")

        # Chercher le caractère juste avant </p>
        i = start - 1
        while i >= 0 and xml_content[i].isspace():
            i -= 1
        prev_char = xml_content[i] if i >= 0 else ""

        # Tout ce qui est avant </p>
        before_p = xml_content[last_pos:start].rstrip('</p>')

        if prev_char in ('.', ';', '"', ")"):
            # On garde le </p> et le <p> comme ils sont
            out_parts.append(xml_content[last_pos:end])
        else:
            is_hyphen = prev_char == '-'
            # Ajouter break="no" si tiret
            if is_hyphen:
                pb_tag = add_breakno_pb(pb_tag)

            # Insérer pb + note en dehors de tout <p>
            replacement = before_p + ' ' + pb_tag + ' ' + note_tag + ' '
            out_parts.append(replacement)

        last_pos = end

    # Ajouter le reste du texte
    out_parts.append(xml_content[last_pos:])
    xml_content = ''.join(out_parts)

    # Nettoyer les espaces multiples
    xml_content = re.sub(r' {2,}', ' ', xml_content)

    # 3️⃣ Transformer <p> avec " - " en <list> via regex
    #xml_content = p_to_list_regex(xml_content)

    # 4️⃣ Sauvegarder
    with open(chemin_out, "w", encoding="utf-8") as f:
        f.write(xml_content)

# -------------------------------------------------------------------------
# Traitement d’un dossier entier
# -------------------------------------------------------------------------
def batch_process(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.lower().endswith(".xml"):
            input_path = os.path.join(input_dir, fname)
            output_path = os.path.join(output_dir, fname)
            print("✅", fname)
            process_xml(input_path, output_path)
    print("✔  MODIFICATION DONE")

# ---------------------------------------------------------------------
# Exemple d'utilisation :
# ---------------------------------------------------------------------
if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    batch_process(input_dir, output_dir)
