# Détail des résultats

## Par Type

### Tous

La répartition se fait ainsi :
* Noms valides (valid_names) : 2070
* Commence/Finit par un tiret (start_or_end_with_dash) : 105
* Contient des tirets (contains_dash) : 774
* Contient des chiffres (contains_digits) : 94
* Mots de plus de 10 caractères (stuck_words) : 212
* Autres (others) : 1418

Il y a une majorité dans les noms valides (prénoms ou nom), avec environ 50%. Ensuite, on trouve 25% du tout dans autres.  
Beaucoup de mots, environ 7%, contient des tirets, et il n'y a que peu de longs mots, nombres ou tirets (environ 2%).

Le total de "Coupures de presse" et de "Reviews" atteint un chiffre plus important que le total que l'on a ici.  
Cela signifie donc qu'il y a un certain nombre de doublons entre les deux


### Coupures de presse

#### Total
La répartition se fait ainsi :
* Noms valides (valid_names) : 579
* Commence/Finit par un tiret (start_or_end_with_dash) : 41
* Contient des tirets (contains_dash) : 205
* Contient des chiffres (contains_digits) : 29
* Mots de plus de 10 caractères (stuck_words) : 125
* Autres (others) : 591

La division ici est d'environ 40 (noms valides)/40 (autres)/20 (le reste)

#### Noms valides (valid_names)
Il y a quelques lettres seules et on trouve quelques mots courts ('ka', 're', 'in', 'dir', 'at')


#### Commence/Finit par un tiret (start_or_end_with_dash)
Il y a beaucoup de mots de fin de lignes dont le tiret a été conservé


#### Contient des tirets (contains_dash)
* On retrouve beaucoup de noms de communes, de mots composés ou de lien verbe-sujet.  
* Il y a quelques cas de mots coupés qui ont été laissés avec leur tiret.  
* On retrouve aussi quelques fautes présentes dans le texte : 'p-o', 'està-dire', 'aveuale-né', 'valentin-hany', 'sourds-maets'


#### Contient des chiffres (contains_digits)
On retrouve plusieurs cas de dates, d'heures, de numéros de pages et de numéros d'éléments


#### Mots de plus de 10 caractères (stuck_words)
* Il y a beaucoup de longs mots qui sont considérés comme erronnées alors qu'ils exustent  
* Beaucoup de mots ont été considérés comme longs alors qu'ils sont séparés par un '/'  
* On retrouve plusieurs cas où les mots sont longs et erronés car ils devraient avoir un tiret (qui a été supprimé) ou un espace (qui a été oublié)  
* Plusieurs cas où l'accent a été oublié ou non reconnu dans le mot


#### Autres (others)
* Il y a la présence de caractères étrangers, tels que du grec
* On retrouve des caractères latins seuls, mais aussi des chiffres romains
* Plusieurs cas sont des noms dans une autre langue ('kipling', 'kopenhague', 'wien')
* Il y a des cas de fins de mots coupés non rattachés
* Plusieurs cas semblent être un problème dans la reconnaissance ('présidalt', 'parisieme', 'inprimerie', 'intitut', 'présemter')
* Quelques cas où un espace/tiret a été oublié/retiré ('estce', 'parisnice', 'dironsnous', 'gratteciel', 'vivanten')
* Il y a plusieurs cas de mots existants mais qui ne sont pas reconnus par la librairie Python utilisée


Séparation proposée par ChatGPT :
* Troncation
* Fautes d'orthographe
* Noms propres/géographiques
* Mots étrangers
* Termes médicaux/scientifiques
* Mots rares anciens ou littéraires
* Expressions altérées
* Bruit OCR


### Reviews

#### Total
La répartition se fait ainsi :
* Noms valides (valid_names) : 1648
* Commence/Finit par un tiret (start_or_end_with_dash) : 70
* Contient des tirets (contains_dash) : 596
* Contient des chiffres (contains_digits) : 65
* Mots de plus de 10 caractères (stuck_words) : 89
* Autres (others) : 897

La division ici est de 50 (noms valides)/25 (autres)/15 (tirets)/10 (le reste)

#### Noms valides (valid_names)
Quelques mots de deux ou trois lettres ne semblent pas être à leur place


#### Commence/Finit par un tiret (start_or_end_with_dash)
* Beaucoup de débuts de mot qui sont tronqués
* Quelques cas de mots où les tirets à l'intérieur ont été conservés en plus des tirets de fin/début


#### Contient des tirets (contains_dash)
* Il y a une très grande quantité de noms de communes
* Il y a plusieurs cas de mix verbe-sujet et de mots composés naturellement
* On retrouve également plusieurs instances de mots tronqués où le tiret a été conservé ('asso-ciations', 'rési-dence', 'ad-versaire', 'ren-forçant')


#### Contient des chiffres (contains_digits)
Il y a beaucoup de numéros de page, quelques numéros de liste avec un °, et plusieurs cas de dates


#### Mots de plus de 10 caractères (stuck_words)
* Beaucoup de cas de noms de communes et de longs mots qui ont été reconnus comme erronés
* Plusieurs cas de longs mots qui ont perdu un accent
* On retrouve quelques cas de fins de mots tronqués
* Quelques cas où des mots sont collés et un espace manque


#### Autres (others)
* Il y a quelques cas de caractères solo ou deux côte-à-côte
* On retrouve un certain nombre d'anglophones ou autres types de mots étrangers, ainsi que de chiffres romains
* Beaucoup de noms semblent désigner des communes
* Plusieurs cas semblent être du bruit d'OCR
* Une grande quantité semblent être des mots totalement inconnus


Séparation proposée par ChatGPT :
* Lieux (corrects ou mal orthographiés)
* Noms propres (réelles ou fictives)
* Mots partiels ou incomplets
* Mots français normaux
* Mots aberrants ou bruit
* Termes administratifs
* Termes techniques ou professionels
* Symboles ou caractères spéciaux


----

## Par Fichier

### Coupures de presse
* La majorité des fichiers ne contiennent pas de mots qui "commence/finit par un tiret" ou de "contient des chiffres"
* La majorité des fichiers ne possèdent qu'un nombre assez faible de mots erronés
* Les fichiers qui contiennent une quantité pouvant être considéré comme conséquente sont : P1000706-043_D-1 (132), P1000706-055_B (68), P1000706-062_A (94), P1000706-064_B (98), P1000706-066_A (71), P1000706-067_A (95), P1000706-075_C (66), P1000706-111_B (64), P1000706-161_B (67)
* Peu de fichiers qui ont des "mots de plus de 10 caractères" ou avec plus de cinq dans cette catégorie. La majorité de ces mots existent dans la langue française et il y a également beaucoup d'entre eux que l'on retrouve d'une coupure à l'autre ("marseillaise", "malvoyantes")


### Reviews
* La liste 'noms valides' reste toujours la plus conséquente : la plus courte a 191 entrées et la plus longue 396.
* A part dans deux cas (30 et 12), la liste 'commence/finit par un tiret' n'a que très peu d'entrées
* La liste 'contient un tiret' a généralement une cinquantaine d'entrées, sauf pour R1000022_1925_10 (175), R1000022_1925_07 (131) et R1000022_1925_05 (123) 
* Les listes de "contient des chiffres" et "mots de plus de 10 caractères" ne monte pas à plus d'une vingtaine d'entrées
* La liste "Autres" varie entre 100 et 173 entrées
* En termes de totaux, le plus bas est 356 (R1000022_1925_09) et le plus haut est de plus de 700 (R1000022_1925_07, 713 ; R1000022_1925_10, 717 ; R1000022_1925_12, 702)
