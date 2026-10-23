from lxml import etree # Pour créer et écrire le XML TEI

def inject_metadata(metadata, titleStmt, publicationStmt, profileDesc, seriesStmt, textClass, msDesc, slugify):
    # ================================
    # --- Métadonnées du JSON ---
    # ================================
    bloc_ia = metadata.get("metadata_ia", {})
    bloc_sp = metadata.get("metadata_sharepoint", {})
    all_fields = bloc_sp.get("all_fields", {})

    resume = bloc_ia.get("resume")
    resume_detaille = bloc_ia.get("resume_detaille")
    editeur = bloc_ia.get("editeur")
    type_document = bloc_ia.get("type_document")
    classification_dewey = bloc_ia.get("classification_dewey")
    sujets = bloc_ia.get("sujets")
    mots_cles = bloc_ia.get("mots_cles")

    title = bloc_sp.get("title")

    Format = all_fields.get("Format")
    TypeDroit = all_fields.get("TypeDroit")
    RevueIdentNum = all_fields.get("Revue_x002d_Ident_x002d_Num")
    AVHDate = all_fields.get("AVH_x002d_Date")

    
    # ================================
    # --- Type du document ---
    # ================================
    if type_document:
        etree.SubElement(seriesStmt, "title", type="genre").text = type_document

    # ================================
    # --- Mots clés (multiples) ---
    # ================================
    if mots_cles:
        keywords_el = etree.SubElement(textClass, "keywords")
        if isinstance(mots_cles, list):
            for mc in mots_cles:
                etree.SubElement(keywords_el, "term", ref=slugify(mc)).text = mc
        else:
            etree.SubElement(keywords_el, "term", ref=slugify(mots_cles)).text = mots_cles

    # ================================
    # --- Sujets (multiples) ---
    # ================================
    if sujets:
        if isinstance(sujets, list):
            for s in sujets:
                etree.SubElement(seriesStmt, "title", type="topic").text = s
        else:
            etree.SubElement(seriesStmt, "title", type="topic").text = sujets

    # ================================
    # --- Titre principal ---
    # ================================
    if title and RevueIdentNum:
        title_el = etree.Element("title")
        title_el.text = title + " - " + RevueIdentNum
        titleStmt.insert(0, title_el)
    else:
        title_el = etree.Element("title")
        title_el.text = "TBD"
        titleStmt.insert(0, title_el)

    if editeur:
        author_el = etree.Element("author")
        author_el.text = editeur
        titleStmt.insert(1, author_el)


    # ================================
    # --- Résumés ---
    # ================================
    if resume_detaille:
        abstract_el = etree.SubElement(profileDesc, "abstract")
        etree.SubElement(abstract_el, "p").text = resume_detaille
    elif resume:
        abstract_el = etree.SubElement(profileDesc, "abstract")
        etree.SubElement(abstract_el, "p").text = resume

    # ================================
    # --- Classification Dewey ---
    # ================================
    if classification_dewey:
        etree.SubElement(textClass, "classCode", scheme="DDC").text = classification_dewey

    # ================================
    # --- Date du document ---
    # ================================
    if AVHDate:
        creation = etree.SubElement(profileDesc, "creation")
        etree.SubElement(creation, "date").text = AVHDate

    # ================================
    # --- Format du document ---
    # ================================
    if Format:
        physDesc = etree.SubElement(msDesc, "physDesc")
        etree.SubElement(physDesc, "p").text = Format

    # ================================
    # --- Droit(s) du document ---
    # ================================
    if TypeDroit:
        availability = etree.SubElement(publicationStmt, "availability")
        etree.SubElement(availability, "p").text = TypeDroit
