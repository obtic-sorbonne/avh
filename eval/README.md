# Evaluation des fichiers choisis aléatoirement

## Métriques

### Press

|  | 45C | 46B | 49A7 | 55A | 55C | 64B | 68A4 | 71A | 77D | 78A1 |
|--|--|--|--|--|--|--|--|--|--|--|
| Word Error Rate | 0.49 | 2.04 | 1.62 | 0 | 0.217 | 2.875 | 3.614 | 1.457 | 0 | 2.889 |
| Char. Error Rate | 0.244 | 1.034 | 1.88 | 0.066 | 0.065 | 1.946 | 0.702 | 0.225 | 0 | 0.415 |
| Word Accuracy | 99.509 | 97.959 | 98.379 | 100 | 99.782 | 97.124 | 96.385 | 98.542 | 100 | 97.11 |
| Substitutions | 1 | 3 | 0 | 0 | 0 | 14 | 0 | 5 | 0 | 7 |
| Deletions | 2 | 0 | 47 | 0 | 1 | 8 | 3 | 0 | 0 | 5 |
| Insertions | 0 | 0 | 0 | 1 | 1 | 55 | 0 | 0 | 0 | 4 |


### Reviews

|  | 01-12 | 01-29 | 01-36 | 04-08 | 04-20 | 04-23 | 07-09 | 07-24 |
|--|--|--|--|--|--|--|--|--|
| Word Error Rate | 0.769 | 7.749 | 2.702 | 2.121 | 6.343 | 17.543 | 4.487 | 0.45 |
| Char. Error Rate | 0.28  | 6.032 | 0.882 | 1.818 | 0.843 | 3.284 | 4.584 | 0.097 |
| Word Accuracy | 99.23 | 92.25 | 97.297 | 97.878 | 93.656 | 82.456 | 95.512 | 99.549 |
| Substitutions | 0 | 3 | 12 | 0 | 0 | 2 | 1 | 0 |
| Deletions | 7 | 21 | 0 | 1 | 7 | 35 | 6 | 2 |
| Insertions | 0 | 73 | 2 | 34 | 7 | 1 | 78 | 0 |


|  | 07-29 | 10-09 | 10-13 | 10-26 | 12-04 | 12-20 | 12-35 |
|--|--|--|--|--|--|--|--|
| Word Error Rate | 0 | 9.693 | 0.7 | 10 | 0.845 | 1.687 | 0 |
| Char. Error Rate | 0  | 9.696 | 0.272 | 10.658 | 0.256 | 0.527 | 0 |
| Word Accuracy | 100 | 90.306 | 99.299 | 90 | 99.154 | 98.312 | 100 |
| Substitutions | 0 | 26 | 0 | 39 | 0 | 1 | 0 |
| Deletions | 0 | 24 | 7 | 30 | 6 | 7 | 0 |
| Insertions | 0 | 65 | 0 | 67 | 0 | 0 | 0 |


----

## Observations superficielles

### Press

* 55A ; 77D ; 49A7 --> Aucune observation particulière à faire  
* 45C ; 46B --> Ajout d'une mise à la ligne non existente  
* 55C --> Quelques différences sur la structure  
* 64B --> Quelques caractères manquants, changement dans la structure  
* 68A4 --> Manque d'un caractère (-)
* 71A --> Ajout de caractères non présents dans l'image (alors que ce ne fut pas le cas auparavant), le journal a écrit certains mots de manière erronée et le modèle l'a corrigé
* 78A1 --> Sélection d'élements non voulus, les (°) ont été remplacés par des points (.).

### Reviews

* Les tableaux ont été mis en forme, avec des noms de colonnes, même si cela change la manière dont le tableau apparait et ajout d'une légende aussi
* Changement des (°) par des (.)
* Mise en ligne quand ce n'est pas le cas parfois
* Un tiret de mot mis en fin de ligne a été supprimé
* Malgré la disparition habituelle du tiret, il est gardé à plusieurs reprises : "rembourse-ment", "établis-sement", "Direc-tion", "con-former"

----

## Observations détaillées

### Press

* 45C --> Un signe de ponctuation a été oublié
* 46B --> Un mot a été mal reconnu
* 49A7 --> L'en-tête de la page a été oublié
* 55A --> Aucune différence
* 55C --> Une parenthèse a été oublié
* 64B --> Des caractères ont été mal reconnus, certains mots oubliés et la structure de liste a été changée
* 68A4 --> Des espaces ont été oubliés
* 71A --> Des caractères mal imprimés ont été corrigés à la reconnaissance
* 77D --> Aucune différence
* 78A1 --> Des signes de ponctuation ont été remplacés, certains oubliés, et un chiffre a été mal reconnu

### Reviews

* 01-12 --> La foliation a été oublié
* 01-29 --> La foliation a été oublié, des éléments de tableaux ont été rajoutés (catégories) ou enlevés (guillemets)
* 01-36 --> Un tiret qui n'apparait pas sur l'image a été rajouté, des sauts à la ligne ont été rajoutés
* 04-08 --> Des éléments de tableaux ont été rajoutés (catégories), un tiret dans un mot a été oublié
* 04-20 --> La foliation a été oublié, quelques espaces entre un chiffre et le 'e' ou 'er' ont été rajoutés
* 04-23 --> La ponctuation de fin de chaque élément de liste a été oublié, un des noms de famille a été mis en minuscule
* 07-09 --> La foliation a été oublié, des éléments de tableaux ont été rajoutés (catégories)
* 07-24 --> 
* 07-29 --> 
* 10-09 --> 
* 10-13 --> 
* 10-26 --> 
* 12-04 --> 
* 12-20 --> 
* 12-35 --> 