# Projet AVH

### Scripts

- **spellcheck.py** : lecture de documents DOCX, suppression de tout ce qui est de la ponctuation selon une liste donnée de symboles, séparation par token, comparaison de chaque mot à un dictionnaire de mots français et production d'une liste de mots considérés erronés
- **spellcheck_by_file.py** : lecture de documents DOCX, suppression de tout ce qui est de la ponctuation selon une liste donnée de symboles, séparation par token, comparaison de chaque mot à un dictionnaire de mots français et production d'une liste de mots considérés erronés, séparés par fichier et divisé par catégories
- **correction.py** : placement de tous les mots considérés comme erronés dans des listes selon certains critères spécifiques
- **valid_names.py** : longue liste contenant des noms et/ou prénoms en minuscules (environ 230 000 noms)

----

### Résultats

#### Fichiers

- **Error by type** : Division des erreurs selon six types de listes
  - _ALL_ : Coupures de presse + Reviews
  - _PRESS_ : Coupures de presse
  - _REVIEWS_ : Reviews
- **Errors by file** : Division des erreurs par fichier et selon six types de listes
  - _errors_press_by_file.py_ : Coupures de presse
  - _errors_reviews_by_file.py_ : Reviews

#### Listes créées

- *valid_names* : tous les mots considérés erronés qui étaient en fait des noms et/ou prénoms, présents dans la liste **[valid_names](https://github.com/FloChiff/avh/blob/main/scripts/valid_names.py)**
- *start_or_end_with_dash* : tous les mots considérés erronés qui contiennent un tiret comme premier ou dernier caractère (cela est généralement dû à la structure de la page)
- *contains_dash* : tous les mots considérés erronés contenant un tiret dans son corps (mots composés mal reconnues, noms de communes, ou autres)
- *contains_digits* : tous les mots considérés erronés contenant un ou plusieurs chiffre.s
- *stuck_words* : tous les mots considérés erronés qui contiennent plus de 10 caractères (cela peut révéler des erreurs dans l'espacement pendant la reconnaissance)
- *others* : tous les mots considérés erronés restants

----

### Evaluation

- **press** : Dossier de PDF des coupures de presse sélectionnées pour l'évaluation
- **reviews** : Dossier d'images PNG des pages de reviews sélectionnées pour l'évaluation
- **eval_press.txt** : Fichier texte des coupures de presse sélectionnées pour l'évaluation
- **eval_review.txt** : Fichier texte des pages de reviews sélectionnées pour l'évaluation
