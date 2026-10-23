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
│   └── tei_avh.xml                  # ODD TEI personnalisé pour validation et encodage
│
├── scripts/
│   ├── schema_conversion_avh.png    # Schématise les étapes de création des fichiers XML-TEI
│   ├── encoding_scripts/            # Scripts pour la transformation de MD à XML-TEI complets
│   └── retrieval_scripts/           # Scripts pour récupérer divers éléments
│
├── tei_documents/
│   ├── old_names/                   # TEI générés avec les noms de fichiers d'origine
│   └── new_name/                    # TEI avec noms explicites et normalisés
│
└── README.md                        # Cette documentation
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

* Schéma de **création** des fichiers XML-TEI (`schema_conversion_avh.png`)
* Scripts de **transformation de MD à XML-TEI complets** (`encoding_scripts/`)
* Scripts de **récupération** de divers éléments (`retrieval_scripts/`)

Chaque script est autonome et exécutable en ligne de commande pour des tâches spécifiques sur le corpus TEI.

---

### 📁 `tei_files/`

Contient tous les fichiers TEI générés ou collectés pour le corpus.

* `old_name/` : TEI avec les noms de fichiers d’origine, tels qu’ils ont été produits ou récupérés depuis les sources.
* `new_name/` : TEI renommés avec des noms explicites et normalisés, plus faciles à exploiter dans les pipelines et analyses.

Ce dossier est la **source principale pour tous les traitements ultérieurs**, analyses, ou conversions.

---
