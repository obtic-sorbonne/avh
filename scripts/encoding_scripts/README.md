# 📘 Documentation technique complète

## Pipeline d’édition numérique Markdown → XML-TEI

**Projet d’édition numérique, inclusive et critique – Bibliothèque patrimoniale Valentin Haüy**

---

# 1. Vue d’ensemble du système

Ce projet met en œuvre un **pipeline automatisé de transformation éditoriale** permettant de produire des fichiers **XML-TEI structurés, normalisés et enrichis** à partir de sources Markdown.

Le système comprend :

1. Conversion Markdown → HTML
2. Encodage HTML → TEI
3. Normalisation typographique et structurelle
4. Injection de métadonnées JSON
5. Génération automatique d’une table des matières
6. Ajout de mécanismes de traçabilité éditoriale
7. Traitement batch industrialisé

L’ensemble forme une **chaîne cohérente et modulaire**, adaptée à l’édition critique de périodiques historiques.

---

# 2. Configuration générale

## 2.1 Namespaces TEI

```python
NS_TEI = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NSMAP = {"tei": NS_TEI}
```

Ces constantes assurent :

* compatibilité XPath
* création correcte des éléments TEI via `lxml.etree`
* cohérence dans tout le pipeline

---

## 2.2 Balises autorisées pour regroupement

```python
ALLOWED_TAGS = ("p", "list", "table", "quote", "figure", "pb", "note", "metamark")
```

Utilisées lors du regroupement hiérarchique pour encapsuler automatiquement :

```xml
<head>
<p>
<table>
...
```

dans un `<div>` cohérent.

---

# 3. Conversion Markdown → HTML

## Fonction : `markdown_to_html(markdown_path)`

* Lecture du fichier Markdown
* Conversion via `markdown.markdown()`
* Extensions activées : `extra`, `tables`, `toc`

Cette étape prépare un HTML intermédiaire destiné à être encodé en TEI.

---

# 4. Encodage HTML → TEI

## 4.1 Enrichissement typographique

### Fonction : `text_enrichment(elem)`

Transforme les balises HTML en TEI :

| HTML       | TEI                       |
| ---------- | ------------------------- |
| `<strong>` | `<hi rend="bold">`        |
| `<em>`     | `<hi rend="italic">`      |
| `<sup>`    | `<hi rend="superscript">` |
| `<sub>`    | `<hi rend="subscript">`   |
| `<code>`   | `<hi rend="monospace">`   |
| `<a>`      | `<ref target="">`         |

Gestion avancée des exposants LaTeX :

* `^{\circ}` → `°`
* `^{\prime}` → `e`
* `\%`
* suppression `\cdot`, `\quad`, `$`

---

## 4.2 Encodage structurel

### Fonction : `encode_elements(elem, parent_el)`

Correspondances principales :

| HTML         | TEI                                |
| ------------ | ---------------------------------- |
| `h1-h4`      | `<head type="section|subsection|subsubsection">`|
| `p`          | `<p>` ou `<note type="foliation">` |
| `blockquote` | `<quote>`                          |
| `ul/ol`      | `<list>`                           |
| `dl`         | `<list><label><desc>`              |
| `table`      | `<table><row><cell>`               |
| `figure`     | `<figure><graphic/><figDesc>`      |
| `article`    | `<div type="article">`             |

---

# 5. Pagination

## 5.1 Remplacement du premier `<pb>`

### `replace_first_pb(xml)`

Remplace :

```xml
<pb n="1"/>
```

par le bloc complexe `BLOC_PB1`.

---

## 5.2 Bloc `BLOC_PB1`

Structure éditoriale de première page :

* en-têtes (`<fw type="header">`)
* sections principales
* sommaire
* mentions administratives
* pied de page

Il reconstitue la mise en page historique du périodique.

---

## 5.3 Ajout automatique de `break="no"`

### `add_breakno_pb(pb_tag)`

Garantit la cohérence des sauts de page en cas de coupure de mot.

---

# 6. Foliation

### Fonction : `insert_foliation(tree)`

Insère automatiquement :

```xml
<note type="foliation">— X —</note>
```

après `<pb n="X">` pour X ≥ 4 et normalise les tirets en cadratin.

---

# 7. Regroupement hiérarchique

## 7.1 `group_head_with_content(root)`

Regroupe :

```xml
<head/>
<p/>
<table/>
```

en :

```xml
<div type="section">
   <head/>
   ...
</div>
```

---

## 7.2 `group_head_with_subdivs(root)`

Regroupe un `<head>` avec les `<div>` suivants.

---

## 7.3 `group_all_heads(root)`

Appelle les deux fonctions précédentes.

Objectif : produire une hiérarchie stable exploitable par la TOC.

---

# 8. Normalisation des dates

### `normalize_dates(root)`

Reconnaît :

* `1921`
* `Mars 1921`
* `12 Mars 1921`
* `01/03/1921`

Ajoute automatiquement :

```xml
<date when="1921-03-12">
```

---

# 9. Transformation des mentions d’imprimeur

### `transform_footer_info(root)`

Détecte par regex :

* Imp. Dubois
* Imprimerie Dubois
* Le Gérant
* variantes ORNE

Transforme en :

```xml
<fw type="footer">
```

---

# 10. Dictionnaire de normalisation (`REPLACEMENTS`)

Ce dictionnaire applique une **normalisation terminale par expressions régulières**.

## 10.1 Normalisation des exposants

Uniformisation :

* `n^{\circ}` → `n°`
* `1^{er}` → `1er`
* `M^{me}` → `Mme`
* `D^{r}` → `Dr`
* chiffres romains + `°`

Garantit une cohérence TEI :

```xml
M<hi rend="superscript">me</hi>
```

---

## 10.2 Nettoyage des unités scientifiques

Suppression des traces LaTeX :

* `\mathrm{~h}`
* `\mathrm{~m}`
* `\mathrm{~cm}`
* `m^{2}`

Transformation en TEI conforme :

```xml
m<hi rend="superscript">2</hi>
```

---

## 10.3 Suppression artefacts LaTeX

Élimination :

* `\left`, `\right`
* `\ldots`
* `\begin{aligned}`
* `array`
* structures vides `{ }^{...}`

---

## 10.4 Corrections corpus-spécifiques

* `DUBOIS \ BAUER` → `DUBOIS &amp; BAUER`
* `\dagger` → `<g rend="obele">`
* `V \propto u` → `Voeu`
* suppression de paragraphes parasites

---

# 11. Injection des métadonnées JSON

## 11.1 Fonction : `inject_metadata(...)`

Sources :

### `metadata_ia`

* resume
* resume_detaille
* editeur
* type_document
* classification_dewey
* sujets
* mots_cles

### `metadata_sharepoint`

* title
* Format
* TypeDroit
* RevueIdentNum
* AVHDate

---

## 11.2 Injections réalisées

* `<title>` principal
* `<author>`
* `<abstract>`
* `<keywords>`
* `<classCode scheme="DDC">`
* `<creation><date>`
* `<physDesc>`
* `<availability>`

Utilise `slugify()` pour générer les identifiants :

* minuscule
* suppression accents
* espaces → tirets

---

# 12. Constantes éditoriales du projet

## 12.1 Description du projet

* `projectDesctext`
* `authoritytext`

Destinés à `<encodingDesc>`.

---

## 12.2 Responsabilités

* Numérisation : L’Atelier de la Villette
* Transcription : AVH
* Encodage : ObTIC

Structure :

```xml
<respStmt>
  <resp>Encodage par</resp>
  <name>ObTIC</name>
</respStmt>
```

---

## 12.3 Série éditoriale

```xml
<seriesStmt>
  <title>Bulletin de l'Union des aveugles de guerre...</title>
</seriesStmt>
```

---

## 12.4 Source manuscrite

```xml
<msDesc>
  <msIdentifier>
    <country>France</country>
    <settlement>Paris</settlement>
    <institution>Association Valentin Haüy</institution>
    <repository>Bibliothèque patrimoniale</repository>
    <collection>Fonds "Aveugles de guerre"</collection>
  </msIdentifier>
</msDesc>
```

---

## 12.5 Informations éditoriales

* normalisation des césures
* transformation des guillemets

---

# 13. Génération automatique de la table des matières

## 13.1 `build_toc_from_node(node)`

Parcours récursif des `<div>` contenant `<head>`.

Génère :

```xml
<item>
  <ref target="#h1">Titre</ref>
</item>
```

---

## 13.2 `build_hierarchical_toc(root)`

Produit :

```xml
<div type="toc">
  <head>TABLE DES MATIÈRES</head>
  <list>...</list>
</div>
```

Inséré en tête du `<body>`.

---

# 14. Script d’orchestration final

## 14.1 Fonction : `process_tei(xml_path, output_path)`

Étapes :

1. Parsing XML
2. `group_all_heads`
3. `normalize_dates`
4. `transform_footer_info`
5. Génération TOC
6. Insertion dans `<body>`
7. Ajout d’une entrée `<revisionDesc>`
8. Sauvegarde formatée

---

## 14.2 Ajout automatique dans `<revisionDesc>`

```xml
<change when="YYYY-MM-DD" who="#fchiffol">
  Corrections structurelles et génération de la table des matières
</change>
```

---

## 14.3 Traitement batch

### `batch_process_tei(input_dir, output_dir)`

* Parcourt tous les `.xml`
* Applique `process_tei`
* Industrialisation complète

---

# 15. Ordre logique d’implémentation

Pipeline consolidé :

1. Markdown → HTML
2. Encodage HTML → TEI
3. Injection métadonnées
4. Pagination / BLOC_PB1
5. Foliation
6. Nettoyage regex (`REPLACEMENTS`)
7. Regroupement hiérarchique
8. Normalisation dates
9. Transformation footer
10. Génération TOC
11. Ajout `<revisionDesc>`
12. Export final
13. Traitement batch

---

# 16. Conclusion

Le système constitue :

* ✔️ Un pipeline complet Markdown → TEI
* ✔️ Une structuration hiérarchique automatisée
* ✔️ Une normalisation éditoriale avancée
* ✔️ Une gestion spécifique des périodiques AVH
* ✔️ Une injection contrôlée de métadonnées JSON
* ✔️ Une génération dynamique de table des matières
* ✔️ Une industrialisation batch
* ✔️ Une traçabilité éditoriale intégrée

Il s’agit d’une **architecture modulaire robuste**, adaptée aux exigences d’un projet d’édition numérique critique en humanités numériques.  

Le travail de création des fichiers XML-TEI ne se fait cependant pas entièrement automatiquement. Deux phases de correction manuelle sont introduites : une avant d'exécuter le script de création de table des matières, et une après. Le document après sa conversion MD - TEI nécessite quelques modifications et corrections pour s'assurer que la création des divisions du document et de la table des matières se réalise correctement. Une fois le script exécuté, une dernière vérification est effectué, pour s'assurer que tout a été correctement encodé. 
