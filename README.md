# AVH

## L'évaluation de l'OCR

Les scripts ont pour objectif d’identifier et de catégoriser les mots considérés comme erronés dans des documents textuels. *spellcheck.py* et *spellcheck_by_file.py* lisent des fichiers DOCX, suppriment une liste définie de signes de ponctuation, découpent le texte en tokens, puis comparent chaque mot à un dictionnaire de français pour générer des listes d’erreurs, soit globalement, soit séparées par fichier. *correction.py* reprend ensuite tous les mots détectés comme erronés et les classe selon différents critères (présence de chiffres, tirets, longueur excessive, etc.). Une liste exhaustive de noms et prénoms (*valid_names.py*) permet d’exclure les faux positifs liés aux anthroponymes. 

Les résultats sont organisés dans différents fichiers distinguant erreurs globales, erreurs propres à la presse ou aux reviews, ainsi que des erreurs regroupées par fichier. Plusieurs listes thématiques sont créées pour analyser précisément la nature des anomalies (noms valides, mots tronqués, composés mal reconnus, mots collés, etc.). 

Enfin, un dispositif d’évaluation repose sur un ensemble de PDF et d’images provenant de coupures de presse et de reviews, accompagnés de fichiers texte listant le matériel sélectionné pour l’analyse.


## La transformation XML-TEI

Le processus transforme chaque fichier Markdown en TEI structuré : le Markdown est converti en HTML puis en un squelette TEI, auquel sont ajoutées les métadonnées provenant d’un JSON. Le document est ensuite post-traité pour réorganiser les titres, normaliser les dates, restructurer les notes de bas de page et générer une table des matières hiérarchique. Le résultat est exporté en TEI final, et l’ensemble peut être appliqué automatiquement à un dossier complet.

