# 📚 AVH TEI Documentation

Bienvenue dans la **documentation AVH TEI**, un repository Python pour la gestion, l’analyse et la conversion de fichiers **XML-TEI** de la collection de la bibliothèque patrimoniale de l'AVH.

Ce repo permet de :

* Analyser la **structure des fichiers TEI**
* Extraire des **métadonnées** et des **contextes regex**
* Collecter et centraliser des documents
* Convertir du **Markdown en TEI**
* Travailler avec un **ODD TEI personnalisé**

---

## 🗂 Structure du repo
```text
.
├── odd/
│   └── tei_avh.xml                # ODD TEI personnalisé pour validation et encodage
│
├── scripts/
│   ├── retrieve_tags_attributes.py       # Analyse structure des balises et attributs TEI
│   ├── retrieve_documents.py             # Collecte de fichiers depuis des sous-dossiers
│   ├── retrieve_metadata.py              # Extraction de métadonnées TEI vers CSV
│   ├── retrieve_regex.py                 # Extraction de contextes regex depuis TEI
│   ├── md_to_tei_converter.py            # Conversion Markdown → XML-TEI
│   └── ... autres scripts utilitaires
│
├── tei_documents/
│   ├── old_names/                   # TEI générés avec les noms de fichiers d'origine
│   └── new_name/                    # TEI avec noms explicites et normalisés
│
└── README.md                      # Cette documentation
```


---

### 📁 `odd/`

Contient l’**ODD TEI personnalisé**.

* Fichier `tei_avh.xml` : définit les balises, attributs et structures autorisées pour le corpus.
* Sert à **valider les fichiers TEI**, assurer la cohérence du balisage et guider la conversion Markdown → TEI.

C’est le **référentiel de règles TEI** pour le projet.

---

### 📁 `scripts/`

Contient tous les scripts Python pour manipuler et analyser le corpus TEI.

* Scripts d’analyse de **structure** (`retrieve_tags_attributes.py`)
* Scripts de **collecte de fichiers** (`retrieve_documents.py`)
* Scripts d’**extraction de métadonnées** (`retrieve_metadata.py`)
* Scripts d’**analyse textuelle par regex** (`retrieve_regex.py`)
* Scripts de **conversion Markdown → TEI** (`md_to_tei_converter.py`)

Chaque script est autonome et exécutable en ligne de commande pour des tâches spécifiques sur le corpus TEI.

---

### 📁 `tei_files/`

Contient tous les fichiers TEI générés ou collectés pour le corpus.

* `old_name/` : TEI avec les noms de fichiers d’origine, tels qu’ils ont été produits ou récupérés depuis les sources.
* `new_name/` : TEI renommés avec des noms explicites et normalisés, plus faciles à exploiter dans les pipelines et analyses.

Ce dossier est la **source principale pour tous les traitements ultérieurs**, analyses, ou conversions.

---
