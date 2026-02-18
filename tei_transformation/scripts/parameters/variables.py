# ======================================================
# --- Informations sur le projet ---
# ======================================================
projectDesctext = """Cet encodage est réalisé dans le cadre du Projet d'édition numérique, inclusive et critique des collections 
de la Bibliothèque patrimoniale Valentin Haüy (Association Valentin Haüy, Sorbonne Université, CNRS)."""
authoritytext = "Association Valentin Haüy, Sorbonne Université et CNRS"

# ======================================================
# --- Ajout des éléments de <respStmt> ---
# ======================================================
digitizationtext = "Numérisation par"
digitizationresp = "L'Atelier de la Villette"
transcriptiontext = "Transcription par"
transcriptionresp = "AVH"
encodingtext = "Encodage par"
encodingresp = "ObTIC"

# ======================================================
# --- Ajout d'un seriesStmt ---
# ======================================================
seriesStmttext = "Bulletin de l'Union des aveugles de guerre et Journal des soldats blessés aux yeux (1919-1957)"
#seriesStmttext = "Le Journal des soldats blessés aux yeux (1916-1919)"
#seriesStmttext = "Pour le foyer du soldat aveugle (1916-1934)"
#seriesStmttext = "Le Mutilé des yeux (1928-1957)"
#seriesStmttext = "Le Trait d'union (1921-1925)"

# ======================================================
# --- Ajout du sourceDesc avec msDesc ---
# ======================================================
countrytext = "France"
settlementtext = "Paris"
institutiontext = "Association Valentin Haüy"
repositorytext = "Bibliothèque patrimoniale"
collectiontext = 'Fonds "Aveugles de guerre"'

# ======================================================
# --- Ajout d'informations d'édition ---
# ======================================================
hyphenationtext = "Les tirets de fin de ligne n'ont pas été conservés et les mots ont été remis dans une version de lecture"
quotationtext = "Tous les guillemets du texte ont été transformés en guillemets anglais"

# -------------------------------------------------------------------------
# Bloc XML à insérer à la place de <pb n="1"/>
# -------------------------------------------------------------------------
BLOC_PB1 = """<pb n="1"/>
<fw type="header">e Année. — N° </fw>
<fw type="header">
  <hi rend="underline">19</hi>
  <lb/>
  <hi rend="underline">POUR LES AVEUGLES PAR LES AVEUGLES</hi>
</fw>
<div type="section">
  <head type="main" rend="align(center)">BULLETIN MENSUEL <lb/>de <lb/>L'UNION DES
    AVEUGLES DE GUERRE <lb/>Reconnue d'utilité publique par décret du 9 avril 1921<lb/> et
    <lb/>Journal des Soldats Blessés aux Yeux</head>
  <div type="section">
    <head type="section" rend="align(center)">SOMMAIRE</head>
    <list>
      <item>...</item>
    </list>
  </div>
  <div type="section">
    <head type="section" rend="align(center)">Informations</head>
    <list>
      <item>...</item>
    </list>
  </div>
  <div type="section">
    <head type="section" rend="align(center)">Chronique de l'U. A. G.</head>
    <list>
      <item>...</item>
    </list>
  </div>
</div>
<fw type="footer" rend="align(center)">Administration :<lb/> Siège de l'U. A. G., 25, rue
  Ballu, PARIS (9<hi rend="superscript">e</hi>) <lb/> TÉLÉPH. : Central 44-88 —
  Chèque postal 160-31</fw>
<fw type="footer" rend="align(center)">Administration :<lb/> SIEGE DE l'U. A. G., 49, RUE
  BLANCHE, PARIS (9<hi rend="superscript">e</hi>) <lb/> TÉLÉPH. : TRINITE 85-83 — Chèque postal
  160-31</fw>

""".strip()
