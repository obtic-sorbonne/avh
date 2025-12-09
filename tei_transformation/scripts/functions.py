import markdown # Conversion Markdown → HTML
import unicodedata # Informations sur les caractères Unicode
import re  # Expressions régulières
from lxml import etree # Pour créer et écrire le XML TEI


from variables import BLOC_PB1

NS_TEI = "http://www.tei-c.org/ns/1.0"
NSMAP = {"tei": NS_TEI}

ALLOWED_TAGS = ("p", "list", "table", "quote", "figure", "pb", "note", "metamark")


# ======================================================
# =======  TABLE DES MATIERES ========
# ======================================================

TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NSMAP = {"tei": TEI_NS}

def get_full_text(elem):
    """Retourne tout le texte d’un élément (y compris contenu des enfants)."""
    return (elem.xpath("string()") or "").strip()

def ensure_head_id(head, idx_counter):
    """Assure qu'un head a un xml:id, retourne l'id."""
    head_id = head.get(f"{{{XML_NS}}}id")
    if not head_id:
        head_id = f"h{idx_counter[0]}"
        head.set(f"{{{XML_NS}}}id", head_id)
        idx_counter[0] += 1
    return head_id

def build_toc_from_node(node, idx_counter, debug=False):
    """
    Parcourt `node` en profondeur et construit une liste TOC (list of item elements).
    Chaque fois qu'une <div> avec <head> est rencontrée, on crée un <item>.
    """
    toc_list = etree.Element(f"{{{TEI_NS}}}list")

    # Nous parcourons uniquement les éléments enfants (itération profonde via recursion)
    for child in node:
        # on n'agit que sur les éléments TEI (ignore texte / comments)
        if not isinstance(child.tag, str):
            continue

        # Si c'est un <div>, vérifier s'il a un head (même si head est enfoui)
        if child.tag == f"{{{TEI_NS}}}div":
            head = child.find("tei:head", namespaces=NSMAP)
            if head is not None:
                title = get_full_text(head) or "[Sans titre]"
                head_id = ensure_head_id(head, idx_counter)

                if debug:
                    print(f"[TOC] trouvée head id={head_id} titre='{title}'")

                item = etree.Element(f"{{{TEI_NS}}}item")
                ref = etree.Element(f"{{{TEI_NS}}}ref", target=f"#{head_id}")
                # on met le texte du titre dans ref (si tu préfères un element <label> on peut)
                ref.text = title
                item.append(ref)

                # Construire la liste pour les enfants de ce div (récursion)
                sublist = build_toc_from_node(child, idx_counter, debug=debug)
                if len(sublist):
                    item.append(sublist)

                toc_list.append(item)
            else:
                # Même si pas de head ici, il peut y en avoir dans les sous-divs :
                sublist = build_toc_from_node(child, idx_counter, debug=debug)
                # si la sous-liste contient des items, on l'annexe directement (évite listes vides)
                if len(sublist):
                    # Si le parent div n'a pas de head, on veut promouvoir ses items au niveau courant
                    # pour ne pas perdre la hiérarchie.
                    for it in sublist:
                        toc_list.append(it)

        else:
            # Si l'enfant n'est pas un div, continuer à descendre (ex: <p><div> ...)
            sublist = build_toc_from_node(child, idx_counter, debug=debug)
            if len(sublist):
                for it in sublist:
                    toc_list.append(it)

    return toc_list


def build_hierarchical_toc(root, insert_into_body=True, debug=False):
    """
    Construit la div type='toc' complète et renvoie l'élément.
    insert_into_body: si True, la fonction n'insère pas la div dans l'arbre;
                      c'est laissé au caller (tu peux désactiver si tu veux insertion automatique).
    debug: affiche les heads trouvés.
    """
    toc_div = etree.Element(f"{{{TEI_NS}}}div", type="toc")
    toc_head = etree.Element(f"{{{TEI_NS}}}head")
    toc_head.text = "TABLE DES MATIÈRES"
    toc_div.append(toc_head)

    idx_counter = [1]

    # On cherche une racine pratique pour parcourir le contenu : prefer body, sinon text, sinon root
    body = root.find(".//tei:body", namespaces=NSMAP)
    if body is not None:
        scan_root = body
    else:
        text = root.find(".//tei:text", namespaces=NSMAP)
        scan_root = text if text is not None else root

    if debug:
        print("[TOC] point de départ:", scan_root.tag)

    toc_list = build_toc_from_node(scan_root, idx_counter, debug=debug)
    if len(toc_list):
        toc_div.append(toc_list)

    return toc_div



# ======================================================
# =======  ENCODAGE DE TEXTE ========
# ======================================================

def text_enrichment(elem):
    contenu = []

    # --- petite fonction interne locale, PAS séparée ---
    def convert_supers(texte):
        # Exposant brut ou avec \text / \mathrm, avec ou sans $
        texte = re.sub(r"\$?(\w+)\^\{\\(?:mathrm|text)?\s*\{\s*([\wÀ-ÿ]+)\s*\}\}\$?", r'\1<hi rend="superscript">\2</hi>', texte)
        # Forme isolée \text{X} ou \mathrm{X}, avec ou sans $
        texte = re.sub(r"\$?\\(?:mathrm|text)\s*\{\s*([\wÀ-ÿ]+)\s*\}\$?", r'<hi rend="superscript">\1</hi>', texte)
        # Exposant prime, avec ou sans $
        texte = re.sub(r"\$?(\w+)\^\{\\prime\}\$?", r'\1<hi rend="superscript">′</hi>', texte)
        # Exposant degré, avec ou sans $
        texte = re.sub(r"\$?(\w+)\^\{\\circ\}\$?", r'\1<hi rend="superscript">°</hi>', texte)
        # Cas particulier : { }^{\circ} ou ${}^{\circ}12$
        texte = re.sub(r"\$?\{\s*\}\^\{\\circ\}\s*([\d.,]*)\$?", r'<hi rend="superscript">°</hi> \1', texte)
        # Pourcentage : $12\%$ → 12%
        texte = re.sub(r"\$(\d+)\s*\\%\$", r'\1%', texte)
        texte = re.sub(r"\\cdot|\\quad", r'', texte)
        texte = re.sub(r"\$", r'', texte)
        return texte.strip()

    for child in elem.children:

        # --- texte brut ---
        if isinstance(child, str):
            txt = convert_supers(child)
            if txt:
                contenu.append(txt)
            continue

        # --- balises HTML ---
        name = child.name

        if name in ("strong", "b"):
            contenu.append(f'<hi rend="bold">{text_enrichment(child)}</hi>')
        elif name in ("em", "i"):
            contenu.append(f'<hi rend="italic">{text_enrichment(child)}</hi>')
        elif name == "sup":
            contenu.append(f'<hi rend="superscript">{text_enrichment(child)}</hi>')
        elif name == "sub":
            contenu.append(f'<hi rend="subscript">{text_enrichment(child)}</hi>')
        elif name == "code":
            contenu.append(f'<hi rend="monospace">{text_enrichment(child)}</hi>')
        elif name == "a" and child.get("href"):
            contenu.append(f'<ref target="{child["href"]}">{text_enrichment(child)}</ref>')

        else:
            contenu.append(text_enrichment(child))

    return " ".join(c for c in contenu if c).strip()


def list_encoding(elem, parent_el):
    list_type = "ordered" if elem.name == "ol" else None
    list_el = etree.SubElement(parent_el, "list", type=list_type) if list_type else etree.SubElement(parent_el, "list")

    if elem.get("aria-label"):
        label = elem.get("aria-label").strip()
        list_el.append(etree.Comment(f"{elem.name} (aria-label='{label}')"))

    for li in elem.find_all("li", recursive=False):
        item_el = etree.SubElement(list_el, "item")
        for child in li.contents:
            if isinstance(child, str):
                item_el.text = (item_el.text or "") + clean_text(child)
            elif child.name in ["ul", "ol"]:
                list_encoding(child, item_el)
            else:
                item_el.text = (item_el.text or "") + clean_text(child.get_text())


def encode_elements(elem, parent_el):
    """Transforme un élément HTML (p, div...) en structure TEI dans parent_el"""

    if elem.name in ["h1", "h2", "h3", "h4"]:
        type_map = {
            "h1": "section",
            "h2": "section",
            "h3": "subsection",
            "h4": "subsubsection"
        }
        head_el = etree.SubElement(parent_el, "head", type=type_map[elem.name], rend="align(center)")

        texte_html = text_enrichment(elem)
        fragment = etree.fromstring(f"<wrapper>{texte_html}</wrapper>", parser=etree.XMLParser(recover=True))

        if fragment.text:
            head_el.text = fragment.text

        for child in fragment:
            head_el.append(child)

        if fragment.tail:
            head_el.tail = fragment.tail

    elif elem.name == "p":
        texte = clean_text(elem.get_text())

        if re.match(r"^\s*(-|—){1,3}\s*\d+\s*(-|—){1,3}\s*$", texte):
            etree.SubElement(parent_el, "note", type="foliation").text = texte
        else:
            p_el = etree.SubElement(parent_el, "p")

            texte_html = text_enrichment(elem)
            fragment = etree.fromstring(f"<wrapper>{texte_html}</wrapper>", parser=etree.XMLParser(recover=True))

            if fragment.text:
                p_el.text = fragment.text

            for child in fragment:
                p_el.append(child)

            if fragment.tail:
                p_el.tail = fragment.tail

    elif elem.name == "blockquote":
        quote_el = etree.SubElement(parent_el, "quote")
        for p in elem.find_all("p"):
            etree.SubElement(quote_el, "p").text = clean_text(p.get_text())

    elif elem.name == "dl":
        list_el = etree.SubElement(parent_el, "list")
        children = [c for c in elem.children if getattr(c, "name", None) in ("dt", "dd")]
        i = 0

        while i < len(children):
            current = children[i]
            if current.name == "dt":
                item_el = etree.SubElement(list_el, "item")
                etree.SubElement(item_el, "label").text = clean_text(current.get_text())
                if i + 1 < len(children) and children[i + 1].name == "dd":
                    etree.SubElement(item_el, "desc").text = clean_text(children[i + 1].get_text())
                    i += 1
            elif current.name == "dd":
                etree.SubElement(list_el, "item").text = clean_text(current.get_text())
            i += 1

    elif elem.name == "table":
        table_el = etree.SubElement(parent_el, "table")
        for row in elem.find_all("tr"):
            row_el = etree.SubElement(table_el, "row")
            for cell in row.find_all(["td", "th"]):
                raw_text = clean_text(cell.get_text())
                enriched_text = text_enrichment(cell)

                # Détection : y a-t-il un enrichissement ?
                if enriched_text and enriched_text != raw_text:
                    # On parse comme tu le fais pour <p>
                    wrapper = f"<wrapper>{enriched_text}</wrapper>"
                    fragment = etree.fromstring(wrapper, parser=etree.XMLParser(recover=True))

                    cell_el = etree.SubElement(row_el, "cell")

                    # Si du texte se trouve dans wrapper.text
                    if fragment.text:
                        cell_el.text = fragment.text

                    # Enfants enrichis (balises)
                    for child in fragment:
                        cell_el.append(child)

                    # Tails éventuels
                    if fragment.tail:
                        cell_el.tail = fragment.tail

                else:
                    # Pas d’enrichissement → on met du texte simple
                    etree.SubElement(row_el, "cell").text = raw_text


    elif elem.name == "figure":
        img = elem.find("img")
        if img:
            fig_el = etree.SubElement(parent_el, "figure")
            etree.SubElement(fig_el, "graphic", url=img.get("src"))
            caption = elem.find("figcaption")
            if caption:
                etree.SubElement(fig_el, "figDesc").text = clean_text(caption.get_text())
        else:
            metamark_el = etree.SubElement(parent_el, "metamark")
            caption = elem.find("figcaption")
            metamark_el.text = clean_text(caption.get_text() if caption else elem.get_text())

    elif elem.name in ["ul", "ol"]:
        list_encoding(elem, parent_el)

    elif elem.name == "article":
        article_div = etree.SubElement(parent_el, "div", type="article")
        for child in elem.children:
            if child.name in ["h1", "h2", "h3", "h4"]:
                etree.SubElement(article_div, "head").text = clean_text(child.get_text())
            elif child.name == "p":
                etree.SubElement(article_div, "p").text = clean_text(child.get_text())
            elif child.name == "blockquote":
                quote_el = etree.SubElement(article_div, "quote")
                for p in child.find_all("p"):
                    etree.SubElement(quote_el, "p").text = clean_text(p.get_text())

    elif elem.name == "img":
        fig = etree.SubElement(parent_el, "figure")
        etree.SubElement(fig, "graphic", url=elem.get("src"))


# ======================================================
# =======  PAGINATION ========
# ======================================================
def replace_first_pb(xml: str) -> str:
    """
    Remplacer <pb n="1"/> par le bloc long
    """

    return xml.replace('<pb n="1"/>', BLOC_PB1, 1)


def add_breakno_pb(pb_tag: str) -> str:
    """
    Ajouter break="no" si tiret
    """

    if re.search(r'\bbreak\s*=', pb_tag, flags=re.IGNORECASE):
        return pb_tag
    return re.sub(r'(<pb\b[^>]*?)(\s*/?>)', r'\1 break="no"\2', pb_tag, count=1, flags=re.IGNORECASE)


# ======================================================
# =======  FOLIATION ========
# ======================================================
def insert_foliation(tree):
    """
    Insère des notes de foliation après les balises <pb> et normalise
    les tirets en tirets cadratin dans les <note type='foliation'>.
    """
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    # ================================
    # 1) Insérer les notes de foliation
    # ================================
    pb_tags = tree.xpath("//tei:pb", namespaces=ns)

    for pb in pb_tags:
        n_val = pb.get("n")

        # n doit être un nombre >= 4 sinon on ignore
        try:
            n_int = int(n_val)
            if n_int < 4:
                continue
        except (TypeError, ValueError):
            continue

        parent = pb.getparent()
        index = parent.index(pb)

        # Élément suivant
        next_elem = parent[index + 1] if index + 1 < len(parent) else None
        next_tag = getattr(next_elem, "tag", None)

        # Vérifier si une note de foliation est déjà présente
        if (
            next_tag
            and isinstance(next_tag, str)
            and next_tag.endswith("note")
            and next_elem.get("type") == "foliation"
        ):
            continue

        # Calcul du numéro de folio (page n → folio n-2)
        folio_number = n_int - 2
        note_text = f"\u2014 {folio_number} \u2014"

        note = etree.Element("{http://www.tei-c.org/ns/1.0}note", type="foliation")
        note.text = note_text
        parent.insert(index + 1, note)

    # ================================
    # 2) Remplacer les tirets dans toutes les notes
    # ================================
    notes = tree.xpath("//tei:note[@type='foliation']", namespaces=ns)
    for note in notes:
        if note.text:
            # remplacer simple tiret "-" par tiret cadratin "—"
            note.text = note.text.replace("-", "\u2014")


# ======================================================
# =======  GROUPING ========
# ======================================================
def group_head_with_content(root):
    """
    Regroupe <head> + contenu structuré autorisé dans un nouveau <div>.
    """
    for div in root.xpath("//tei:div", namespaces=NSMAP):
        i = 0
        while i < len(div):
            child = div[i]

            if isinstance(child.tag, str) and child.tag.endswith("head"):
                start = i
                end = i

                # Étendre la zone tant que les tags suivants sont autorisés
                while end + 1 < len(div):
                    next_elem = div[end + 1]
                    if isinstance(next_elem.tag, str) and next_elem.tag.split("}")[-1] in ALLOWED_TAGS:
                        end += 1
                    else:
                        break

                if end > start:
                    to_group = list(div[start:end + 1])
                    new_div = etree.Element(f"{{{NS_TEI}}}div")

                    head_type = child.get("type")
                    new_div.set("type", head_type if head_type in ("section", "subsection", "subsubsection") else "section")

                    # Ajouter les éléments dans le nouveau div
                    for elem in to_group:
                        new_div.append(elem)

                    # Supprimer les anciens éléments du parent
                    for elem in to_group:
                        if elem.getparent() is div:
                            div.remove(elem)

                    # Réinsérer
                    div.insert(start, new_div)
                    i = start  # repositionner

            i += 1


def group_head_with_subdivs(root):
    """
    Regroupe <head> + <div> suivants en un <div> englobant.
    """
    for container in root.xpath("//tei:div", namespaces=NSMAP):
        i = 0
        while i < len(container):
            child = container[i]

            if isinstance(child.tag, str) and child.tag.endswith("head"):
                start = i
                end = i

                # Étendre la zone pour inclure les <div> suivants
                while end + 1 < len(container):
                    next_elem = container[end + 1]

                    if not (isinstance(next_elem.tag, str) and next_elem.tag.endswith("head")):
                        next_tag = next_elem.tag.split("}")[-1] if isinstance(next_elem.tag, str) else None
                        if next_tag == "div":
                            end += 1
                        else:
                            break
                    else:
                        break

                if end > start:
                    to_group = list(container[start:end + 1])
                    new_div = etree.Element(f"{{{NS_TEI}}}div")

                    head_type = child.get("type")
                    new_div.set("type", head_type if head_type in ("section", "subsection", "subsubsection") else "section")

                    # Transférer les éléments
                    for elem in to_group:
                        new_div.append(elem)

                    # Supprimer du parent
                    for elem in to_group:
                        if elem.getparent() is container:
                            container.remove(elem)

                    # Réinsérer le nouveau bloc
                    container.insert(start, new_div)
                    i = start

            i += 1

def group_all_heads(root):
    """
    Appelle les deux fonctions de groupement dans le bon ordre.
    """
    group_head_with_content(root)
    group_head_with_subdivs(root)


# ======================================================
# =======  DIVERS ========
# ======================================================
def markdown_to_html(markdown_path):
    """Convertit le contenu écrit en markdown en un balisage HTML"""

    with open(markdown_path, "r", encoding="utf-8") as f:
        texte_md = f.read()
    html = markdown.markdown(texte_md, extensions=["extra", "tables", "toc"])
    return html


def clean_text(t):
    """Supprime les espaces superflus et normalise le texte"""

    return ' '.join(t.strip().split())


def slugify(texte):
    """
    Transforme un texte en identifiant TEI/ref compatible (ex: "#mon-texte")
    - Minuscule
    - Supprime accents
    - Remplace espaces par "-"
    - Ne garde que lettres, chiffres et "-"
    """

    txt = texte.lower()
    # Décomposition Unicode et suppression des accents
    txt = ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
    txt = txt.replace(" ", "-")
    # Suppression des caractères non alphanumériques sauf "-"
    txt = ''.join(c for c in txt if c.isalnum() or c == "-")
    return f"#{txt}"


def normalize_dates(root):
    """Normalise les dates dans les balises <date> et ajoute l'attribut @when."""

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    re_year = re.compile(r"^\d{4}$")

    re_month_year = re.compile(
        r"^(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s+\d{4}$",
        re.IGNORECASE
    )

    re_day_month_year = re.compile(
        r"^\d{1,2}\s+(Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s+\d{4}$",
        re.IGNORECASE
    )

    # Format numérique : 01/03/1921, 1-3-1921, etc.
    re_numeric = re.compile(
        r"^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2}|\d{4})$"
    )

    mois_map = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }

    for date_el in root.xpath("//tei:date", namespaces=ns):
        txt = (date_el.text or "").strip()
        if not txt:
            continue

        when_val = None

        # ---- Année simple : "1921"
        if re_year.match(txt):
            when_val = txt

        # ---- Mois + Année : "Mars 1921"
        elif re_month_year.match(txt):
            mois, annee = txt.split()
            when_val = f"{annee}-{mois_map[mois.lower()]}"

        # ---- Jour + Mois + Année : "12 Mars 1921"
        elif re_day_month_year.match(txt):
            jour, mois, annee = txt.split()
            when_val = f"{annee}-{mois_map[mois.lower()]}-{int(jour):02d}"

        # ---- Formats numériques : "01/03/1921"
        else:
            m = re_numeric.match(txt)
            if m:
                jour, mois, annee = m.groups()

                # Année sur 2 chiffres → 19xx par défaut
                if len(annee) == 2:
                    annee = "19" + annee

                when_val = f"{annee}-{int(mois):02d}-{int(jour):02d}"

        # Appliquer l'attribut @when
        if when_val:
            date_el.set("when", when_val)


def transform_footer_info(root):
    """
    Transforme certains paragraphes (<p>) en <fw type="footer">
    lorsque leur contenu correspond à des mentions d'imprimeur,
    de gérant ou d'indications similaires.
    """

    # Expressions régulières pour détecter les mentions en bas de page
    imprimeur = re.compile(r"Imp\. Dubois.+", re.IGNORECASE)
    imprimeur2 = re.compile(r"Imprimerie Dubois.+", re.IGNORECASE)
    gerant = re.compile(r"Le Gérant.+", re.IGNORECASE)
    impgerant = re.compile(r"Imp.+ORNE\.?", re.IGNORECASE)

    regex_list = (imprimeur, imprimeur2, gerant, impgerant)

    # Parcours des paragraphes
    for p in root.xpath("//tei:p", namespaces=NSMAP):

        text = (p.text or "").strip()
        if not text:
            continue

        # Si le texte correspond à un des motifs recherchés
        if any(regex.match(text) for regex in regex_list):
            new_tag = etree.Element(f"{{{NS_TEI}}}fw", type="footer")
            new_tag.text = text

            parent = p.getparent()
            parent.replace(p, new_tag)


def p_to_list_regex(xml: str) -> str:
    """
    Transformer <p> avec " - " en <list><item> via regex
    """

    pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL | re.IGNORECASE)

    def replace(match):
        content = match.group(1).strip()
        if ' - ' not in content:
            return match.group(0)  # ne rien changer
        items = content.split(' - ')
        items_xml = ''.join(f'<item>{item.strip()}</item>' for item in items)
        return f'<list>{items_xml}</list>'

    return pattern.sub(replace, xml)
