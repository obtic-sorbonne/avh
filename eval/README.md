# Evaluation des fichiers choisis aléatoirement

## Métriques

### Press

|  | 45C | 46B | 49A7 | 55A | 55C | 64B | 68A4 | 71A | 77D | 78A1 |
|--|--|--|--|--|--|--|--|--|--|--|
| Word Error Rate (WER in %) |   |   |   |   |   |   |   |   |   |   |
| Char. Error Rate (CER in %) |   |   |   |   |   |   |   |   |   |   |
| Word Accuracy (Wacc in %) |   |   |   |   |   |   |   |   |   |   |
| Substitutions |   |   |   |   |   |   |   |   |   |   |
| Deletions |   |   |   |   |   |   |   |   |   |   |
| Insertions |   |   |   |   |   |   |   |   |   |   |


### Reviews

|  | 01-12 | 01-29 | 01-36 | 04-08 | 04-20 | 04-23 | 07-09 | 07-24 | 07-29 | 10-09 | 10-13 | 10-26 | 12-04 | 12-20 | 12-35 |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| Word Error Rate (WER in %) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Char. Error Rate (CER in %) |    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Word Accuracy (Wacc in %) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Substitutions |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Deletions |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Insertions |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |

----

## Observations

### Press

55A ; 77D ; 49A7 --> Aucune observation particulière à faire
45C ; 46B --> Ajout d'une mise à la ligne non existente
55C --> Quelques différences sur la structure
64B --> Quelques caractères manquants, changement dans la structure
68A4 --> Manque d'un caractère (-)
71A --> Ajout de caractères non présents dans l'image (alors que ce ne fut pas le cas auparavant), le journal a écrit certains mots de manière erronée et le modèle l'a corrigé
78A1 --> Sélection d'élements non voulus, les (°) ont été remplacés par des points (.).

### Reviews

* Les tableaux ont été mis en forme, avec des noms de colonnes, même si cela change la manière dont le tableau apparait et ajout d'une légende aussi
* Changement des (°) par des (.)
* Mise en ligne quand ce n'est pas le cas parfois
* Un tiret de mot mis en fin de ligne a été supprimé
* Malgré la disparition habituelle du tiret, il est gardé à plusieurs reprises : "rembourse-ment", "établis-sement", "Direc-tion", "con-former"

