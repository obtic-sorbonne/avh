# 📂 TEI Utilities Toolkit

Collection de scripts Python pour l’exploration, l’extraction et la manipulation de corpus **XML-TEI**.

## 📦 Contenu

* `retrieve_tags_attributes.py`
* `retrieve_documents.py`
* `retrieve_metadata.py`
* `retrieve_regex.py`

Chaque script est indépendant et s’exécute en ligne de commande.

---

# 1️⃣ `retrieve_tags_attributes.py`

## 🎯 Objectif

Extraire la **structure des balises TEI**, leurs **attributs** et les **valeurs associées**, à partir :

* du `<teiHeader>`
* ou du `<text>`

Le script produit un fichier texte hiérarchisé avec :

* le nombre d’occurrences des balises
* le nombre d’occurrences des attributs
* la fréquence des valeurs d’attributs

---

## ⚙️ Fonctionnement

### 1. Parcours du dossier

* Recherche tous les fichiers `.xml`
* Ignore les fichiers non valides XML

### 2. Ciblage d’une section

Recherche soit :

* `teiHeader`
* `text`

Namespace TEI utilisé :

```python
http://www.tei-c.org/ns/1.0
```

### 3. Comptage structuré

Structure interne :

```python
{
  "tag": {
      "count": int,
      "attributes": {
          "attr": {
              "count": int,
              "values": {
                  "val": int
              }
          }
      }
  }
}
```

Les attributs du namespace XML (`xml:`) sont ignorés.

---

## 📤 Sortie

Un fichier :

```
resultat_teiHeader.txt
ou
resultat_text.txt
```

Exemple :

```
div (42)
 ├─ @type (42)
 │    ├─ "chapter" (30)
 │    ├─ "section" (12)
```

---

## ▶️ Utilisation

```bash
python retrieve_tags_attributes.py <dossier> teiHeader
python retrieve_tags_attributes.py <dossier> text
```

---

## 💡 Cas d’usage

* Analyse structurelle d’un corpus
* Normalisation TEI
* Audit de balisage
* Préparation à un schéma ODD

---

# 2️⃣ `retrieve_documents.py`

## 🎯 Objectif

Collecter des fichiers spécifiques depuis un **dossier de dossiers** selon :

* leur extension
* ou leur suffixe de nom

Et les copier dans un dossier unique.

---

## ⚙️ Fonctionnement

### 1. Parcours récursif

Utilise `os.walk()` pour explorer tous les sous-dossiers.

### 2. Filtrage

Filtre selon :

```python
file.lower().endswith(sys.argv[3])
```

Exemples :

* `.html`
* `_clean.xml`
* `_v2.txt`

### 3. Gestion des doublons

Si un nom existe déjà :

```
file.html
file_1.html
file_2.html
```

Aucune collision. Pas de drame.

---

## 📤 Sortie

Tous les fichiers correspondants sont copiés dans :

```
<dossier_destination>
```

---

## ▶️ Utilisation

```bash
python retrieve_documents.py <dossier_source> <dossier_destination> <file_ending>
```

Exemple :

```bash
python retrieve_documents.py corpus/ html_files/ .html
```

---

## 💡 Cas d’usage

* Centralisation de versions finales
* Récupération de fichiers OCR
* Extraction d’un sous-corpus
* Nettoyage de projets dispersés

---

# 3️⃣ `retrieve_metadata.py`

## 🎯 Objectif

Extraire des métadonnées spécifiques d’un corpus TEI et générer un CSV.

Métadonnées extraites :

* `title`
* `creation/date`

---

## ⚙️ Fonctionnement

### 1. Parcours des `.xml`

Ignore les autres fichiers.

### 2. Extraction XPath

Avec namespace TEI :

```python
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
```

Requêtes :

```python
.//tei:titleStmt/tei:title
.//tei:creation/tei:date
```

Si absent → chaîne vide.

---

## 📤 Sortie

Fichier :

```
tei_metadata.csv
```

Structure :

| filename | title | date |
| -------- | ----- | ---- |

---

## ▶️ Utilisation

```bash
python retrieve_metadata.py <dossier_xml>
```

---

## 💡 Cas d’usage

* Construction d’un catalogue
* Vérification des métadonnées
* Création d’index
* Alimentation d’une base de données

---

# 4️⃣ `retrieve_regex.py`

## 🎯 Objectif

Identifier des occurrences d’expressions régulières dans des fichiers TEI **et récupérer leur contexte**.

Produit une liste Python contenant :

* nom du fichier
* extrait contextuel

---

## ⚙️ Fonctionnement

### 1. Lecture brute du TEI

Le fichier est lu comme texte brut.

Les balises sont conservées.
Aucun parsing XML ici. On joue côté regex.

---

### 2. Tokenisation simple

```python
tokens = re.findall(r'\S+', text)
```

Contexte configurable :

```python
WINDOW_BEFORE = 2
WINDOW_AFTER = 2
```

---

### 3. Recherche regex

Expressions à définir dans :

```python
REGEXES = [
    r''
]
```

Chaque occurrence récupère :

* 2 tokens avant
* 2 tokens après

---

### 4. Structure des résultats

```python
[
    {
        "file": "document.xml",
        "context": "mot mot CIBLE mot mot"
    }
]
```

---

## 📤 Sortie

Fichier :

```
results_list.py
```

Contient :

```python
results = [...]
```

---

## ▶️ Utilisation

```bash
python retrieve_regex.py <dossier_xml>
```

---

# 🧠 Architecture générale

Ces scripts couvrent quatre niveaux d’analyse :

| Niveau            | Script                        |
| ----------------- | ----------------------------- |
| Structure XML     | `retrieve_tags_attributes.py` |
| Gestion de corpus | `retrieve_documents.py`       |
| Métadonnées       | `retrieve_metadata.py`        |
| Analyse textuelle | `retrieve_regex.py`           |

Ils peuvent être combinés dans une pipeline de traitement TEI.

---

# 🔧 Dépendances

Standard library uniquement :

* `os`
* `sys`
* `glob`
* `shutil`
* `csv`
* `json`
* `re`
* `xml.etree.ElementTree`
* `collections`

---