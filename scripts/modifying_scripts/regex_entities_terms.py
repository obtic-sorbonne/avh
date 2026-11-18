import re

legislation = {
    r"Loi\s+des\s+11\s+et\s+18\s+avril\s+1831" : {
        "loi_1831": "Texte historique régissant les pensions militaires d'infirmité. La cécité y était classée dans la 1ère classe de gravité avec un taux fixe de 975 francs par an. Devenue notoirement insuffisante face à l'inflation de la Première Guerre mondiale, elle a servi de point de départ aux revendications du monde combattant."
        },
    r"Loi\s+de\s+1831" : {
        "loi_1831": "Texte historique régissant les pensions militaires d'infirmité. La cécité y était classée dans la 1ère classe de gravité avec un taux fixe de 975 francs par an. Devenue notoirement insuffisante face à l'inflation de la Première Guerre mondiale, elle a servi de point de départ aux revendications du monde combattant."
        },
    r"Loi\s+du\s+9\s+avril\s+1898" : {
        "loi_1898_04_09": "Loi sur la responsabilité des accidents du travail créant le principe du risque professionnel et de l'indemnisation forfaitaire. Utilisée comme point de comparaison juridique pour l'évaluation de l'incapacité professionnelle et le calcul des indemnités."
        },
    r"Loi\s+du\s+13\s+juillet\s+1917" : {
        "loi_1917_07_13": "Loi rehaussant le tarif de pension des simples soldats aveugles absolus ou amputés de deux membres de 975 fr. à 1 200 fr. par an, avec révision d'office et versement de rappels d'arrérages."
        },
    r"Loi\s+du\s+27\s+juillet\s+1917" : {
        "loi_1917_07_27": "Loi instituant le statut de Pupille de la Nation, organisant l'adoption morale et le soutien financier de l'État pour les enfants de tués, disparus ou invalides de guerre."
        },
    r"Loi\s+des\s+pensions\s+(?:militaires\s+)?de\s+1919" : {
        "loi_1919_03_31": "Texte fondateur du droit à la réparation des victimes de la Première Guerre mondiale, porté par le député Jules Auguste Georges Lugol. Elle établit le droit à pension, fixe la pension de base du soldat aveugle à 2 400 fr. et introduit les articles clés régissant les surpensions, soins gratuits et la rééducation."
        },
    r"\b(termes|texte|promulgation|conformité|application|dispositions)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919\b" : {
        "loi_1919_03_31": "Texte fondateur du droit à la réparation des victimes de la Première Guerre mondiale, porté par le député Jules Auguste Georges Lugol. Elle établit le droit à pension, fixe la pension de base du soldat aveugle à 2 400 fr. et introduit les articles clés régissant les surpensions, soins gratuits et la rééducation."
        },
    r"\b(?:(rapport|loi)\s+)Lugol\b" : {
        "loi_1919_03_31": "Texte fondateur du droit à la réparation des victimes de la Première Guerre mondiale, porté par le député Jules Auguste Georges Lugol. Elle établit le droit à pension, fixe la pension de base du soldat aveugle à 2 400 fr. et introduit les articles clés régissant les surpensions, soins gratuits et la rééducation."
        },
    r"Loi\s+du\s+14\s+f[ée]vrier\s+1920" : {
        "loi_1920_02_14": "Loi accordant le bénéfice du « quart de place » (réduction de 75 % du tarif) sur les grands réseaux de chemin de fer aux invalides de guerre pensionnés à 80 % et plus, ainsi qu'à leur guide accompagnateur."
        },
    r"Quart\s+de\s+place" : {
        "loi_1920_02_14": "Loi accordant le bénéfice du « quart de place » (réduction de 75 % du tarif) sur les grands réseaux de chemin de fer aux invalides de guerre pensionnés à 80 % et plus, ainsi qu'à leur guide accompagnateur."
        },
    r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+juillet\s+1920" : {
        "loi_1920_07_31": "Loi de finances portant fixation du budget général de l'exercice 1920, comporte un article réprimant la propagande anticonceptionnelle et l'avortement dans un contexte de forte politique nataliste après la Première Guerre mondiale, ainsi que des dispositions financières et réglementaires concernant les conséquences de la guerre."
        },
    r"Loi\s+du\s+29\s+octobre\s+1921" : {
        "loi_1921_10_29": "Loi instituant la création et la délivrance de la Carte officielle d'invalidité réservée aux grands invalides et aveugles pensionnés à 100 %, leur garantissant la gratuité, pour eux et leurs guides, ainsi que leur réservant la priorité d'accès aux guichets publics, transports et places assises."
        },
    r"Carte\s+à\s+double\s+barre\s+bleue" : {
        "loi_1921_10_29": "Loi instituant la création et la délivrance de la Carte officielle d'invalidité réservée aux grands invalides et aveugles pensionnés à 100 %, leur garantissant la gratuité, pour eux et leurs guides, ainsi que leur réservant la priorité d'accès aux guichets publics, transports et places assises."
        },
    r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+d[ée]cembre\s+1921" : {
        "loi_1921_12_31": "Loi allouant aux grands invalides titulaires d’une pension d’infirmité égale ou supérieure à 85%, ou régulièrement proposés pour une pension de cette nature, des allocations spéciales temporaires. Les titulaires de l’allocation spéciale temporaire reçoivent, en outre, pour chacun des enfants ouvrant droit à majoration de pension, une majoration supplémentaire temporaire"
        },
    r"Loi\s+du\s+23\s+mars\s+1928" : {
        "loi_1928_03_23": "Loi assouplissant les conditions d'attribution des pensions de réversion aux veuves de grands invalides et aveugles, en prenant maintenant en compte toutes les veuves, tant qu'elles sont pensionnés au titre de la loi du 31 mars 1919."
        },
    r"Loi\s+du\s+13\s+juillet\s+1928" : {
        "loi_1928_07_13": "Loi favorisant la construction de logements populaires et d'Habitations à Bon Marché (HBM), prévoyant des facilités d'accès à la propriété, des prêts bonifiés et des réservations de logements pour certaines catégories de personnes, dont notamment les grands invalides et aveugles de guerre."
        },
    r"Loi\s+Loucheur" : {
        "loi_1928_07_13": "Loi favorisant la construction de logements populaires et d'Habitations à Bon Marché (HBM), prévoyant des facilités d'accès à la propriété, des prêts bonifiés et des réservations de logements pour certaines catégories de personnes, dont notamment les grands invalides et aveugles de guerre."
        },
    r"Loi\s+(?:de\s+finances\s+)?du\s+30\s+d[ée]cembre\s+1928" : {
        "loi_1928_12_30": "Loi mettant en place des dispositions notables concernant les pensions militaires d'invalidité et les grands mutilés, dont certains articles (comme l'article 81) ont instauré des allocations et majorations spécifiques pour les aveugles de guerre et les grands invalides, avec également des réévaluations pour les droits des veuves de guerre, orphelins et ascendants."
        },
    r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+mars\s+1932" : {
        "loi_1932_03_31": "Loi de finances permettant d'ajuster ou de majorer les pensions et allocations accordées aux grands invalides, catégorie à laquelle appartenaient de fait les aveugles de guerre"
        },
    r"Loi\s+du\s+22\s+mars\s+1935" : {
        "loi_1935_03_22": "Texte fondateur créant officiellement le Statut Nationale des Grands Mutilés de Guerre, attribuant aux aveugles une allocation annuelle spéciale de 9 800 francs."
        },
    r"Loi\s+du\s+22\s+ao[ûu]t\s+1946" : {
        "loi_1946_08_22": "Texte fondateur de la protection sociale en France, qui fixe et généralise le régime des prestations familiales au sein de la Sécurité sociale, avec l'intégration notamment du régime des majorations pour enfants des invalides de guerre."
        },
    r"Loi\s+du\s+27\s+f[ée]vrier\s+1948" : {
        "loi_1948_02_27": "Loi instituant le principe du rapport constant, liant automatiquement l'évolution de la valeur du point de pension militaire d'invalidité aux variations des traitements bruts des fonctionnaires de l'État."
        },
    r"Loi\s+du\s+29\s+juillet\s+1950" : {
        "loi_1950_07_29": "Loi affiliant obligatoirement au régime général de la Sécurité sociale les grands invalides pensionnés à au moins 85 %, les veuves de guerre non remariées, et les orphelins non salariés."
        },
    r"Loi\s+du\s+31\s+d[ée]cembre\s+1953" : {
        "loi_1953_12_31": "Loi fixant le plan quadriennal de revalorisation des pensions, supprimant la limite des 10 degrés d'invalidité supplémentaire et doublant l'Allocation N° 8 pour les aveugles et grands invalides."
        },
    r"Plan\s+[Qq]uadriennal" : {
        "loi_1953_12_31": "Loi fixant le plan quadriennal de revalorisation des pensions, supprimant la limite des 10 degrés d'invalidité supplémentaire et doublant l'Allocation N° 8 pour les aveugles et grands invalides."
        },
    r"Article\s+10\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_10_1919": "Dispositif accordant au grand invalide incapable de se conduire ou d'accomplir seul les actes de la vie soit l'hospitalisation, soit une surpension spéciale de 25 % pour rétribuer l'assistance constante d'un guide ou d'une tierce personne."
        },
    r"Article\s+12\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_12_1919": "Dispositif attribuant des surpensions échelonnées par dixièmes pour les blessures, mutilations ou affections associées s'ajoutant à la cécité."
        },
    r"Articles?\s+(?:13|71)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_13_71_1919": "Dispositions accordant une majoration annuelle de pension pour chaque enfant à charge jusqu'à l'âge de 18 ans, déclarée incessible et insaisissable."
        },
    r"Articles?\s+(?:14|19)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_14_19_1919": "Dispositions réglementant le droit à la pension de réversion des veuves d'invalides de guerre et fixant les taux de liquidation selon la cause du décès et la durée du mariage."
        },
    r"Article\s+55\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_55_1919": "Disposition réglant la gestion des pensions et ordonnant le versement direct d'une part de la pension à l'épouse, aux enfants ou aux ascendants lorsque le grand invalide est interné en établissement psychiatrique."
        },
    r"Articles?\s+(?:59|60)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_59_60_1919": "Dispositions définissant les règles de cumul et de choix entre la pension d'ancienneté ou de service et la pension militaire d'invalidité pour les militaires de carrière."
        },
    r"Article\s+64\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_64_1919": "Disposition garantissant la gratuité intégrale des soins médicaux, chirurgicaux, pharmaceutiques, des appareillages et des cures thermales nécessaires pour les affections ayant motivé la pension."
        },
    r"Article\s+67\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_67_1919": "Disposition autorisant la révision des dossiers de pension en cas d'erreur matérielle de liquidation, d'omission ou d'énonciations inexactes."
        },
    r"Article\s+69\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_69_1919": "Disposition majeure assimilant à un fait de guerre la perte du second œil survenue hors service chez un mutilé ayant déjà perdu le premier œil à la guerre, lui ouvrant le droit au tarif d'aveugle de guerre à 100 %."
        },
    r"Article\s+76\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919" : {
        "art_76_1919": "Disposition consacrant le droit à la prise en charge par l'État de la rééducation professionnelle et de l'apprentissage d'un nouveau métier pour tous les mutilés et aveugles de guerre."
        },
    r"D[ée]cision\s+(?:minist[ée]rielle\s+)?du\s+23\s+juillet\s+1887" : {
        "decision_1887_07_23": "Acte historique ayant mis en place le premier classement et le premier barème d'invalidité en droit français, servant à évaluer les infirmités des militaires et des victimes de guerre. Cette décision restreint la définition médicale de la cécité à la « perte totale et irrémédiable de la vue », excluant les militaires conservant une acuité visuelle résiduelle partielle jusqu'à la circulaire de 1916."
        },
    r"(D[ée]cret[-–]loi\s+)?du\s+17\s+juin\s+1938" : {
        "decret_loi_1938_06_17": "Texte étendant le bénéfice du Statut des Grands Mutilés de Guerre et de la Dotation Nationale aux militaires blessés en service commandé, aux victimes civiles de guerre et aux bénéficiaires de l'article 69."
        },
    r"(Ordonnance\s+)?du\s+25\s+octobre\s+1945" : {
        "ordonnance_1945_10_25": "Texte d'après-guerre réorganisant le régime des pensions militaires d'invalidité et préparant la refonte des prestations familiales et de la Sécurité sociale pour les victimes de guerre."
        },
    r"(D[ée]cret\s+)?du\s+20\s+juillet\s+1954" : {
        "decret_1954_07_20": "Décret portant modification du guide-barème des invalidités pour l’attribution des pensions du code des pensions militaires d’invalidité et des victimes de la guerre."
        },
    r"Allocation\s+(?:N[°o]?\s*)?5\s*bis" : {
        "alloc_5bis": "Allocation d'État créée en 1921 garantissant aux aveugles de guerre et grands invalides un plafond minimum de ressources annuelles."
        },
    r"Allocation\s+(?:N[°o]?\s*)?6\b" : {
        "alloc_6": "Allocation complémentaire créée en 1928 accordant un supplément financier par tranche de 10 % d'invalidité supplémentaire au-delà de 100 % pour certains invalides."
        },
    r"Allocation\s+(?:N[°o]?\s*)?7\b" : {
        "alloc_7": "Allocation spécifique créée en 1932 attribuée aux grands invalides cumulant une amputation d'un membre en plus de la cécité complète."
        },
    r"Allocation\s+(?:N[°o]?\s*)?8\b" : {
        "alloc_8": "Majoration d'allocation attribuée aux plus grands invalides et aveugles de guerre, dont le montant annuel a été revalorisé et doublé sous le plan quadriennal de 1953-1954."
        },
    r"Statut\s+des\s+Grands\s+Mutil[ée]s(?:\s+de\s+Guerre)?" : {
        "statut_grands_mutiles": "Ensemble des dispositions législatives et réglementaires (1935, 1938) accordant un statut d'honneur, des priorités sociales et des allocations complémentaires aux invalides les plus gravement atteints."
        },
    r"Dotation\s+Nationale\s+des\s+Grands\s+Mutil[ée]s" : {
        "dotation_nationale": "Fonds d'État et allocation annuelle attribuée aux aveugles de guerre et grands invalides en vertu du Statut de 1935 pour garantir leur autonomie matérielle et morale."
        },
    r"Code\s+de\s+la\s+Famille" : {
        "code_famille": "Recueil législatif régissant les allocations familiales, primes à la naissance et avantages familiaux, auquel ont été rattachés les enfants des invalides de guerre par la loi du 22 août 1946."
        },
    r"[Cc]revaison\s+du\s+plafond" : {
        "crevaison_plafond": "Expression désignant la suppression légale du plafond maximum d'indemnisation de 200 % d'invalidité (loi du 31 décembre 1953), permettant d'évaluer et de rémunérer l'intégralité des blessures supplémentaires des grands invalides à mutilations multiples."
        },
}

glossary = {
    r"\b[Cc]agna\b" : {
        "term_cagna": "Abri rudimentaire aménagé dans les tranchées, sous terre ou en ciment sur le front de la Grande Guerre. Par extension, désigne une habitation ou un local provisoire et de fortune."
        },
    r"\b[Gg]ourbi\b" : {
        "term_gourbi": "Abri de tranchée, logement sommaire ou baraquement précaire occupé par les soldats sur le front ou dans les dépôts."
        },
    r"\b[Rr]adouille\b" : {
        "term_radouille": "Camionnette de charroi, automobile ou véhicule de transport de marchandises souvent sujet aux pannes ou peu fiable."
        },
    r"\b[Aa]batis\b" : {
        "term_abatis": "Membres ou corps humain. L'expression « prendre pour ses abatis » signifie subir des dégâts corporels, des blessures ou des contrecoups physiques graves."
        },
    r"\b[Pp]apelard\b" : {
        "term_papelard": "Document administratif, papier officiel, lettre de correspondance ou imprimé réglementaire."
        },
    r"\b[Ll]oquet\b" : {
        "term_loquet": "Petite touffe de soies animales ou de fibres végétales (chiendent, tampico, etc.) insérée et fixée dans chaque trou du bois de brosse au moyen d'un fil de laiton ou de ficelle."
        },
    r"\b[Pp]lacage\b" : {
        "term_placage": "Opération de finition consistant à coller ou clouer une mince planche de bois fin (la plaque) sur le dos perforé de la brosse pour masquer et protéger les fils de montage."
        },
    r"\b[Pp]laqueur(\s+de\s+brosses)?\b" : {
        "term_plaqueur": "Ouvrier ou artisan spécialisé effectuant la pose, le collage, le clouage et le polissage du placage sur le dos des brosses."
        },
    r"\b[Cc]hiendent\b" : {
        "term_chiendent": "Fibre végétale rigide d'origine naturelle couramment employée pour garnir les brosses à laver, balais et brosses de ménage."
        },
    r"\b[Tt]ampico\b" : {
        "term_tampico": "Fibre végétale mexicaine extraite de l'agave utilisée pour les brosses moyennes, polissoirs et décrottoirs."
        },
    r"\bPp]iassava\b" : {
        "term_piassava" : "Fibre végétale très solide et grossière tirée de palmiers sud-américains ou africains, spécialement employée pour fabriquer les balais d'extérieur robustes."
        },
    r"\b[Bb]assine\b" : {
        "term_bassine": "Fibre végétale rigide tirée du palmier Palmyra, servant au garnissage des lave-ponts, balais et brosses à récurer."
        },
    r"\b[Kk]itool\b" : {
        "term_kitool": "Fibre végétale fine et élastique d'origine asiatique tirée du palmier Caryota urens, résistant bien à l'eau, utilisée pure ou mélangée pour la brosserie usuelle."
        },
    r"\b[Éé]crevisse\b" : {
        "term_ecrevisse": "Modèle de brosse cintrée à bords arrondis, très populaire pour le lavage et le nettoyage ménager."
        },
    r"\b[Mm]orue\b" : {
        "term_morue": "Brosse plate et allongée, spécialement conçue pour le lavage intérieur des fûts, tonneaux et récipients industriels."
        },
    r"\b[Vv]ergette\b" : {
        "term_vergette": "Petite brosse fine destinée à l'entretien, au dépoussiérage et au brossage des habits et vêtements."
        },
    r"\b(?:[Pp]alot|[Ll]angue\s+de\s+chat)\b" : {
        "term_palot" : "Brosse garnie de soie ou crin (petits, moyens et grands), spécifique pour le pansement et le nettoyage des sabots des chevaux."
        },
    r"\b[Bb]rasseur\b" : {
        "term_brasseur": "Brosse faite en chiendent ou en bassine, utilisée par les brasseurs, limonadiers et vignerons pour nettoyer l'intérieur des fûts."
        },
    r"\b[Ll]ave-pont\b" : {
        "term_lave_pont": "Grande brosse rectangulaire robuste garnie de chiendent ou bassine, munie d'une douille pour fixer un manche, utilisée pour laver les sols, ponts de navires et grands espaces."
        },
    r"\b[Gg]recquage\b" : {
        "term_grecquage": "Entaille ou encoche ménagée à la scie dans le dos du livre débroché pour encastrer et loger les ficelles de couture."
        },
    r"\b[Ee]ndossure\b" : {
        "term_endossure": "Opération façonnant le dos du volume en forme arrondie au moyen d'un marteau et d'une presse pour créer les mors qui recevront les cartons de couverture."
        },
    r"\b[Jj]aspure\b" : {
        "term_jaspure": "Technique de décoration consistant à moucheter ou ombrer les tranches du livre au moyen d'une grille et d'une brosse projetant de petites gouttes de couleur."
        },
    r"\b[Oo]ptophone\b" : {
        "term_optophone": "Appareil d'exploration optico-sonore utilisant des cellules au sélénium et un disque perforé tournant pour traduire la forme des caractères imprimés ordinaires en motifs musicaux audibles au casque."
        },
    r"\b[Cc]ubarite\b" : {
        "term_cubarite": "Plus communément appelé cubarithme. Boîte accueillant de petits cubes amovibles en relief portant les caractères Braille ou chiffres pour poser mécaniquement les opérations arithmétiques ou créer des formes géométriques simples."
        },
    r"\b[Pp]hotoélectrographe\b" : {
        "term_photoelectrographe": "Dispositif expérimental de lecture tactile projetant un faisceau lumineux sur l'écriture et commandant un réseau de tiges mobiles reproduisant en relief la forme des lettres sous le doigt."
        },
    r"\b[Vv]isagraphe\b" : {
        "term_visagraphe": "Appareil photo-électrique de conversion de l'écriture noire ordinaire en relief tactile sur papier ou bande souple."
        },
    r"\b[Ss]ténomasque\b" : {
        "term_stenomasque" : "Masque insonorisé muni d'un microphone permettant au secrétaire ou reporter aveugle de répéter à voix basse les propos d'une assemblée pour les enregistrer sur dictaphone sans déranger l'auditoire."
        },
    r"\b[Rr]appel\s+d'arrérages\b" : {
        "term_rappel_arrerages": "Versement rétroactif des sommes ou arrérages de pension dus à un invalide depuis la date d'ouverture initiale de son droit jusqu'au jour de la liquidation effective."
        },
    r"\b[Ii]nfirmières?\b" : {
        "term_infirmiere": "Personnel soignant féminin assurant les soins oculaires, l'application des pansements, l'accompagnement quotidien et la rééducation initiale des blessés aux yeux dans les hôpitaux et centres de convalescence."
        },
    r"\b[Mm]arraines?\b" : {
        "term_marraine": "Femmes ou jeunes filles bénévoles correspondant avec les soldats, leur envoyant des colis, du linge, du tabac et des secours financiers, ou leur rendant visite dans les hôpitaux et écoles de rééducation pour rompre leur isolement moral et leur apporter une affection fraternelle."
        },
    r"\b[Pp]atronesses?\b" : {
        "term_patronesse": "Dames bienfaitrices de la bourgeoisie ou de l'aristocratie, membres des comités de patronage, des conseils d'administration ou des comités d'honneur des œuvres d'assistance, qui organisent des ventes de charité, des galas, des concerts et des souscriptions publiques pour financer les secours et logements."
        },
    r"\bAntigone\b" : {
        "term_antigone": "Figure mythologique grecque évoquant la fille d'Œdipe, utilisée dans la littérature et la presse des aveugles de guerre comme métaphore poétique pour désigner la femme dévouée qui sert de guide permanent, de secrétaire et de « yeux » à l'invalide visuel."
        },
    r"\b[Ff]emmes\s+d'aliénés\b" : {
        "term_femmes_dalienes": "Épouses de soldats aveugles ou grands invalides internés en établissement psychiatrique pour troubles mentaux ou neurologiques graves consécutifs aux traumatismes de guerre. En vertu de l'article 55 de la loi du 31 mars 1919, une part de la pension du pensionné leur est versée directement pour subvenir aux besoins de la famille."
        },
    r"\b[Vv]euves?\s+(d'aveugles?\s+)?de\s+guerre\b" : {
        "term_veuve": "Épouses survivantes des aveugles de guerre décédés. La législation (loi du 31 mars 1919, lois du 23 mars et 30 décembre 1928) a progressivement aligné le taux de leur pension de réversion sur celui des veuves de guerre (taux d'invalide à 50 %), en supprimant l'exigence d'antériorité du mariage au traumatisme dès lors que l'union a duré au moins deux ans."
        },
    r"\b[Bb]rossier\b" : {
        "trade_brossier": "Ouvrier ou artisan fabriquant des brosses et balais de manière manuelle. Métier emblématique de rééducation pour les aveugles de guerre."
        },
    r"\b[Bb]rosserie\b" : {
        "trade_brosserie": "Branche artisanale et industrielle de fabrication des brosses et balais. Constitue l'activité manuelle la plus pratiquée et organisée au sein des ateliers de l'UAG et de l'Entrepôt de Neuilly."
        },
    r"\b[Cc]haisier\b" : {
        "trade_chaisier": "Artisan spécialisé dans la confection, le garnissage, le rempaillage ou le cannage des assises et dossiers de sièges et chaises."
        },
    r"\b[Cc]anneur\b" : {
        "trade_canneur": "Artisan effectuant le cannage, c'est-à-dire le tissage manuel de cannes de rotin ou de bambou à travers les trous perforés dans le châssis des sièges."
        },
    r"\b[Cc]annage\b" : {
        "trade_cannage": "Technique de tissage de cannes de rotin (motifs en carré ou alsacien) sur les garnitures de chaises, fauteuils et canapés. Métier d'atelier très enseigné dans les écoles de rééducation."
        },
    r"\b[Rr]empailleur\b" : {
        "trade_rempailleur": "Artisan remplaçant ou tressant la paille de chaises rustiques ou de style."
        },
    r"\b[Rr]empaillage\b" : {
        "trade_rempaillage": "Action et technique de garnissage des sièges par tressage de paille ou jonc directement autour des barreaux du châssis. Métier d'appoint rural ou urbain accessible aux aveugles."
        },
    r"\b[Rr]otinage\b" : {
        "trade_rotinage": "Travail et tissage des écorces et fibres de rotin pour le garnissage de sièges ou l'habillement d'objets de vannerie et le cannage de sièges."
        },
    r"\b[Vv]annier\b" : {
        "trade_vannier": "Artisan fabriquant des objets tressés en brins d'osier ou en rotin, tels que des malles, des paniers ou des corbeilles."
        },
    r"\b[Vv]annerie\b" : {
        "trade_vannerie": "Art et industrie du tressage de l'osier, du rotin et des fibres souples pour créer des objets divers."
        },
    r"\b[Oo]siériculture\b" : {
        "trade_osiericulture": "Culture, plantation, taille et récolte des saules osiers destinés aux ateliers de vannerie. Enseignée notamment dans des centres spécialisés comme Fayl-Billot."
        },
    r"\b[Cc]ordonnier\b" : {
        "trade_cordonnier": "Artisan réparant ou fabriquant des chaussures et souliers (ressemelage cloué ou cousu, pose de talons, gravure). Métier enseigné aux aveugles exigeant un apprentissage approfondi."
        },
    r"\b[Tt]onnelier\b" : {
        "trade_tonnelier": "Artisan façonnant et assemblant des fûts, barriques, pièces de vin, bacs et baquets en bois. Métier manuel rémunérateur pratiqué en région viticole par des aveugles ayant l'usage de leurs deux mains."
        },
    r"\b[Mm]enuisier\b" : {
        "trade_menuisier": "Artisan travaillant le bois pour la confection de meubles, bâtis, rayonnages et ouvrages de bâtiment à l'aide de scies, rabots et gabarits adaptés."
        },
    r"\b[Rr]elieur\b" : {
        "trade_relieur": "Artisan effectuant le brochage, le grecquage, l'endossure, la jaspure des tranches et le cartonnage de reliure des livres imprimés en noir ou en Braille."
        },
    r"\b[Tt]ricoteur\b" : {
        "trade_tricoteur": "Ouvrier opérant sur métier à tricoter mécanique ou manuel pour fabriquer des tricots, gilets, chandails et vêtements de maille. Métier adapté au travail à domicile, particulièrement pour les mutilés des mains ou bi-manchots."
        },
    r"\b[Mm]atelassier\b" : {
        "trade_matelassier": "Artisan confectionnant, garnissant et réfectionnant des matelas en laine, crin ou fibre."
        },
    r"\b[Ss]parterie\b" : {
        "trade_sparterie": "Industrie et tressage du sparte et de fibres végétales rigides, destinée à la confection de couffins, grands cabas industriels et paniers de manutention pour les huileries, savonneries et voiries."
        },
    r"\b[Ll]uthier\b" : {
        "trade_luthier": "Artisan fabriquant, réparant et réglant les instruments de musique à cordes (violons, altos, violoncelles)."
        },
    r"\b[Cc]ultivateur\b" : {
        "trade_cultivateur": "Exploitant ou travailleur agricole assurant les travaux de la ferme (soins au bétail, moisson, labours guidés, etc.)."
        },
    r"\b[Jj]ardinier\b" : {
        "trade_jardinier": "Personne entretenant les jardins potagers ou d'agrément, effectuant le bêchage en cordeau, le désherbage et la culture des légumes et fleurs."
        },
    r"\b[Aa]piculteur\b" : {
        "trade_apiculteur": "Éleveur d'abeilles gérant les ruches, la récolte du miel et l'entretien du matériel apicole."
        },
    r"\b[Aa]viculteur\b" : {
        "trade_aviculteur": "Éleveur spécialisé de volailles assurant la conduite des couveuses artificielles, le mirage des œufs, le gavage, le plumage et la vente de la volaille."
        },
    r"\b[Vv]igneron\b" : {
        "trade_vigneron": "Cultivateur de la vigne assurant la taille des ceps, le liage des sarments, la vendange et les travaux de la cave vinicole."
        },
    r"\b[Tt]éléphoniste\b" : {
        "trade_telephoniste": "Opérateur ou opératrice assurant la gestion des standards et tableaux centraux téléphoniques dans les administrations et entreprises à l'aide de repères tactiles Braille et de cadrans adaptés."
        },
    r"\b[Dd]actylographe\b" : {
        "trade_dactylographe": "Personne effectuant la saisie de textes et courriers sur machine à écrire ordinaire ou Braille, très souvent couplée à l'écoute de dictaphones enregistreurs."
        },
    r"\b[Mm]asseur\b" : {
        "trade_masseur": "Praticien diplômé d'État effectuant des massages médicaux, thérapeutiques et rééducatifs dans les établissements thermaux, hôpitaux ou cabinets privés."
        },
    r"\b[Aa]justeur-mécanicien\b" : {
        "trade_ajusteur_mecanicien": "Ouvrier qualifié ajustant, limant, et polissant manuellement des pièces mécaniques de haute précision issues de machines-outils (automobile, aviation, outillage)."
        },
    r"\b[Aa]ccordeur\s+de\s+pianos\b" : {
        "trade_accordeur_pianos": "Spécialiste de l'accordage, du réglage de la mécanique et de l'entretien des pianos, titulaire de la carte syndicale et exerçant en manufacture ou à domicile."
        },
    r"\b[Rr]eprésentant\s+de\s+commerce\b" : {
        "trade_representant_commerce": "Placier ou commis-voyageur assurant la prospection, la présentation de catalogues et la prise de commandes de marchandises (vins, épicerie, bonneterie, brosserie) auprès des clients."
        },
    r"\b[Ii]nstituteur\b" : {
        "trade_instituteur": "Enseignant du premier degré assurant l'instruction des enfants dans les écoles primaires publiques ou privées, ou dans les instituts spécialisés pour aveugles."
        },
    r"\b[Aa]vocat\b" : {
        "trade_avocat": "Auxiliaire de justice inscrit au barreau, plaidant et conseillant les usagers. Plusieurs aveugles de guerre ont poursuivi une brillante carrière d'avocat ou de député (ex. Léon Thébault)."
        },
    r"\b[Mm]agistrat\b" : {
        "trade_magistrat": "Membre du corps judiciaire exerçant des fonctions de juge ou du ministère public dans les tribunaux."
        },
    r"\b[Mm]édecin\b" : {
        "trade_medecin": "Praticien diplômé en médecine générale ou spécialisée (ophtalmologie, chirurgie, physiothérapie)."
        },
    r"\b[Oo]rganiste\b" : {
        "trade_organiste": "Musicien ou musicienne exécutant les pièces musicales et accompagnements sur les grandes orgues ou harmoniums d'églises."
        },
    r"\b[Éé]crivain\b" : {
        "trade_ecrivain": "Auteur d'ouvrages littéraires, poésies, romans, récits de guerre ou articles de presse et revues spécialisées."
        },
    r"\b[Éé]nucléés?\b" : {
        "typ_enucleation": "Ablation chirurgicale complète du globe oculaire consécutive à des traumatismes ou éclats de projectiles subis au combat. L'énucléation nécessite la préparation de la cavité orbitaire pour le port ultérieur d'une prothèse oculaire en émail."
        },
    r"\b[Éé]nucléation\b" : {
        "typ_enucleation": "Ablation chirurgicale complète du globe oculaire consécutive à des traumatismes ou éclats de projectiles subis au combat. L'énucléation nécessite la préparation de la cavité orbitaire pour le port ultérieur d'une prothèse oculaire en émail."
        },
    r"\b[Pp]rothèse\s+oculaire\b" : {
        "typ_prothese_oculaire": "Pièce d'émail ou de matière synthétique peinte reproduisant la forme, la couleur de l'iris et le blanc de l'œil, insérée dans la cavité orbitaire après énucléation pour des raisons d'hygiène, de protection de la cavité et de restauration esthétique."
        },
    r"\b(?:[Œœ]il|Oe?il|yeux(?:\s+à)?)\s+(?:de\s+verre\s+)?(?:artificiels?\s+)?(?:à\s+)?(?:simple|double)\s+coque\b" : {
        "typ_oeil_coque" : "Modèles de prothèses oculaires en émail attribués aux militaires énucléés : 1. L'œil (de verre ou artificiel) à simple coque est une mince pièce d'émail allouée en première mise pour les cavités orbitaires récentes ou modifiées par rétraction cicatricielle. 2. L'œil à double coque présente des bords mousses dessinant une larme sur une coupe perpendiculaire ; offrant un meilleur volume et une tolérance supérieure, il est réservé aux cavités énucléées stabilisées, soit au moins un an après la blessure)."
        },
    r"\b[Gg]az\s+lacrymogènes?\b" : {
        "typ_gaz_lacrymogene": "Substances chimiques toxiques utilisées durant la Grande Guerre, provoquant de sévères brûlures de la cornée, des inflammations chroniques, des opacités et la perte progressive de la vision chez les combattants."
        },
    r"\b([Bb]i-)?[Mm]anchots?\b" : {
        "typ_manchot": "Mutilé de guerre ayant subi l'amputation d'un bras (manchot) ou des deux bras (bi-manchot) en plus de la cécité. Ces cas, appelés 'cumulards', faisaient l'objet d'aménagements prothétiques spécifiques et de taux d'allocations majorés."
        },
    r"\b[Tt]répanés\b" : {
        "typ_trepane": "Blessé de guerre ayant subi une trépanation ou présentant une perte de substance osseuse crânienne consécutive à un traumatisme par éclat d'obus ou balle, souvent associé chez l'aveugle à des migraines sévères, des vertiges ou des crises d'épilepsie."
        },
    r"\b[Aa]liénés\b" : {
        "typ_aliene": "Invalide de guerre atteint de troubles mentaux, neurologiques ou de chocs psycho-traumatiques graves, généralement l'obusite ou choc de l'obus, entraînant l'internement en établissement spécialisé."
        },
    r"\b[Cc]écité\s+pratique\b" : {
        "typ_cecite_pratique": "Elle assimile à la cécité complète tout militaire conservant une acuité visuelle résiduelle égale ou inférieure à 1/20e (ou 1/20e d'un côté avec l'autre œil perdu), lui garantissant le bénéfice de la pension intégrale de 1ère classe."
        },
    r"\b[Rr]éformé\s+n°\s*(?:1|2)\b" : {
        "typ_reformes": "Catégories de démobilisation sanitaire : le Réformé n° 1 bénéficie d'une pension d'État pour infirmité ou maladie directement imputable au service militaire ; le Réformé n° 2 était renvoyé chez lui sans droit à pension en raison d'une cécité ou maladie jugée non imputable au service."
        },
    r"\b[Aa]lsaciens-Lorrains\b" : {
        "typ_alsaciens_lorrains": "Invalides visuels originaires d'Alsace-Lorraine incorporés dans l'armée allemande pendant la guerre de 1914-1918, puis réintégrés dans la nationalité française et dans le droit commun des pensions et au sein de l'UAG après le traité de Versailles."
        },
    r"\b[Aa]veugles?\s+résistants?\b" : {
        "typ_aveugle_resistant": "Combattant des Forces Françaises de l'Intérieur (F.F.I.), de la Résistance ou déporté devenu aveugle au cours des combats, tortures ou sabotages de la Seconde Guerre mondiale, admis au statut et aux avantages des aveugles de guerre au sein de l'Union."
        },
    r"\b[Aa]veugles?\s+chargés?\s+de\s+famille\b" : {
        "typ_charge_famille": "Aveugle de guerre ayant des enfants mineurs ou des ascendants à sa charge. Cette catégorie bénéficiait d'une priorité pour les secours d'urgence, les prêt-mobiliers, l'accès aux logements familiaux de Franceville et les majorations d'allocations de la loi de 1919 et du Code de la Famille."
        },
    r"\b[Aa]veugles?\s+mariés?\b" : {
        "typ_marie": "Aveugle uni par le mariage. La situation de l'épouse ouvrait des droits spécifiques, notamment la réversion de pension de veuve de guerre et l'accès aux séjours de vacances et maisons de repos."
        },
    r"\b[Aa]veugles?\s+célibataires?\b" : {
        "typ_celibataire": "Aveugle de guerre non marié (avec ou sans ascendants à charge). Pour cette catégorie, l'UAG et les œuvres associées proposaient l'accueil en foyers communautaires et l'attribution de gardes/guides ou tierces personnes rémunérées."
        },
}

# Dictionnaire des motifs : chaque clé = identifiant TEI, chaque valeur = liste de regex
ORG_PATTERNS = {
    "org_uag": [
     #r"\b(?:U\.?\s*A\.?\s*G\.?|(?:Union|(?:Groupement|Union)\s+Nationale?)\s+des\s+Aveugles\s+de\s+Guerre)\b",
     r"\b(?:Union|(?:Groupement|Union)\s+Nationale?)\s+des\s+Aveugles\s+de\s+Guerre\b",
    ],

    "org_fsa": [
     r"\b(?:(?:Association\s+dite\s+[\"«]?)?Pour\s+le\s+Foyer\s+du\s+Soldat\s+Aveugle[\"»]?|(?:[Ll]e\s+)?Foyer\s+du\s+Soldat\s+Aveugle|Œuvre\s+Pour\s+le\s+Foyer\s+du\s+Soldat\s+Aveugle|F\.?\s*S\.?\s*A\.?)\b",
    ],

    "org_avh": [
     r"\b(?:A\.?\s*V\.?\s*H\.?|Association\s+Valentin\s+Haü?y(?:\s+pour\s+le\s+bien\s+des\s+aveugles)?)\b",
    ],

    "org_sirla": [
     r"\b(?:SIRLA|(?:Association\s+dite\s+[\"«]?)?Le\s+Livre\s+de\s+l['’]Aveugle[\"»]?|Société\s+d['’]Impression\s+et\s+de\s+Reliure\s+du\s+Livre\s+pour\s+les\s+Aveugles|Bibliothèque\s+du\s+Livre\s+de\s+l['’]Aveugle)\b",
    ],

    "org_asa": [
     r"\b(?:A\.?\s*S\.?\s*A\.?|(?:Société\s+[\"«]?)?Les\s+Amis\s+des\s+Soldats\s+Aveugles[\"»]?)\b",
    ],

    "org_abri": [
     r"\b(?:L['’])?Abri\s+du\s+Soldat\s+Aveugle\b",
    ],

    "org_ateliers_aveugles": [
     r"\b(?:Société\s+des\s+)?Ateliers\s+d['’]Aveugles\b",
    ],

    "org_ecole_massage": [
     r"\b(?:(?:É|E)cole\s+de\s+massage\s+des\s+soldats\s+aveugles|(?:Œ|Oe)uvre\s+des\s+Masseurs)\b",
    ],

    "org_aaf": [
     r"\b(?:A\.?\s*A\.?\s*F\.?|Amitié\s+des\s+Aveugles\s+de\s+France)\b",
    ],

    "org_olsa": [
     r"\b(?:O\.?\s*L\.?\s*S\.?\s*A\.?|(?:Comité\s+Central\s+de\s+l['’]|Imprimerie\s+Beaunoise\s+du\s+|(?:Œ|Oe)uvre\s+(?:Nationale\s+du\s+)?)[Ll]ivre\s+des\s+[Aa]veugles\s+de\s+[Gg]uerre)\b",
    ],

    "org_fede_mutiles_yeux": [
     r"\b(?:(?:Société|Fédération|Association)\s+des\s+Mutilés\s+des\s+Yeux|Fédération\s+des\s+Aveugles\s+de\s+guerre,\s+des\s+blessés\s+et\s+malades\s+des\s+yeux)\b",
    ],

    "org_unac": [
     r"\b(?:U\.?\s*N\.?\s*A\.?\s*C\.?|Union\s+Nationale\s+des\s+Aveugles\s+Civils)\b",
    ],

    "org_ufac": [
     r"\b(?:U\.?\s*F\.?\s*A\.?\s*C\.?|Union\s+Française\s+des\s+Associations\s+de\s+Combattants(?:\s*,\s*Prisonniers,\s*Combattants\s+de\s+la\s+Libération\s+et\s+Victimes\s+des\s+deux\s+guerres)?)\b",
    ],

    "org_uf": [
     r"\b(?:U\.?\s*F\.?|Union\s+Fédérale(?:\s+des\s+Associations\s+(?:Françaises\s+de\s+)?Mutilés(?:\s+et\s+Réformés)?)?)\b",
    ],

    "org_unc": [
     r"\b(?:U\.?\s*N\.?\s*C\.?|Union\s+Nationale\s+des\s+Combattants)\b",
    ],

    "org_unmr": [
     r"\b(?:U\.?\s*N\.?\s*M\.?\s*R\.?|Union\s+Nationale\s+des\s+Mutilés\s+et\s+Réformés)\b",
    ],

    "org_agmg": [
     r"\b(?:A\.?\s*G\.?\s*M\.?\s*G\.?|Association\s+Générale\s+des\s+Mutilés\s+de\s+la\s+Guerre)\b",
    ],

    "org_confederation_nationale": [
     r"\b(?:Confédération\s+Nationale(?:\s+des\s+Anciens\s+Combattants\s+et\s+Victimes\s+de\s+la\s+Guerre|\s+de\s+la\s+France\s+Meurtrie)?)\b",
    ],

    "org_comite_entente": [
     r"\b(?:Comité\s+d['’]Entente(?:\s+des\s+Grandes\s+Associations\s+Nationales\s+de\s+Combattants\s+et\s+de\s+Victimes\s+de\s+la\s+guerre|\s+des\s+Grands\s+Invalides\s+de\s+Guerre)?)\b",
    ],

    "org_pbrwf": [
     r"\b(?:P\.?\s*B\.?\s*R\.?\s*W\.?\s*F\.?|P\.?\s*B\.?\s*F\.?|Permanent\s+Blind\s+Relief\s+War\s+Fund(?:\s+(?:for\s+Soldiers\s+and\s+Sailors|incorporated|to\s+the\s+Alliés))?)\b",
    ],

    "org_red_cross": [
     r"\bAmerican\s+Red\s+Cross\b",
     r"\bCroix[- ]rouge\s+am(é|e)ricaine\b",
    ],

    "org_abp_afob": [
     r"\b(?:A\.?\s*B\.?\s*P\.?|American\s+Braille\s+Press(?:\s+for\s+War\s+Disabled)?|A\.?\s*F\.?\s*O\.?\s*B\.?|American\s+Foundation\s+for\s+Overseas\s+Blind(?:,\s*Inc\.)?)\b",
    ],

    "org_phare_france": [
     r"\bPhare\s+de\s+France\b",
    ],

    "org_st_dunstans": [
     r"\bSt\s+Dunstan's\b",
    ],

    "org_nib": [
     r"\bNational\s+Institute\s+for\s+the\s+Blind\b",
    ],

    "org_cib": [
     r"\bCanadian\s+Institute\b",
    ],

    "org_conseil_mondial": [
     r"\bConseil\s+Mondial\b",
    ],

    "org_fidac": [
     r"\bFIDAC\b",
    ],

    "org_ciamac": [
     r"\bCIAMAC\b",
    ],

    "org_american_legion": [
     r"\bAmerican\s+Legion\b",
    ],

    "org_british_legion": [
     r"\bBritish\s+Legion\b",
    ],

    "struct_maison_convalescence": [
     r"\bMaison\s+de\s+Convalescence\s+de\s+Reuilly\b",
    ],

    "struct_ecoles_neuilly_rochecorbon": [
     r"\bÉcoles?\s+de\s+(?:Neuilly|Rochecorbon)\b",
    ],

    "struct_chateau_mazargues": [
     r"\bInternat\s+départemental\s+des\s+Aveugles\s+de\s+la\s+guerre\b",
     r"\b(?:Internat\s+du\s+)?château\s+de\s+Mazargues\b",
    ],

    "struct_villa_rosiers": [
     r"\bVilla\s+des\s+Rosiers(?:\s+à\s+Menton-Garavan)?\b",
    ],

    "struct_foyer_boulleville": [
     r"\bFoyer\s+de\s+Boulleville\b",
    ],

    "struct_maison_aveugle_guerre": [
     r"\bMaison\s+de\s+l'Aveugle\s+de\s+Guerre\b",
    ],

    "struct_livre_parle": [
     r"\b[Ll]ivre\s+[Pp]arlé\b",
    ],
}

PERS_PATTERNS = {
    "pers_alix_julien": [
     r"\b(?:M\.\s+)?Julien\s+Alix\b",
     r"\b(?:M\.\s+)?Alix\s+\(?Julien\)?\b",
    ],

    "pers_amblard_henri": [
     r"\b(?:(M\.|monsieur)\s+)Amblard\b",
     r"\b(?:M\.\s+)?Henri\s+Amblard\b",
     r"\b(?:M\.\s+)?Amblard\s+\(?Henri\)?\b",
    ],

    "pers_antoine_louis": [
     r"\bLouis\s+Antoine\b",
     r"\bAntoine\s+\(?Louis\)?\b",
    ],

    "pers_arbel_marguerite": [
     r"\b(?:Mlle\s+)(Marguerite\s+)?Arbel\b",
    ],

    "pers_bastian_rene": [
     r"\bRené\s+Bastian\b",
    ],

    "pers_baker_colonel": [
     r"\b(?:M\.\s+)?Baker\b",
    ],

    "pers_barbier_veuve": [
     r"\b(?:Mme\s+)(Veuve\s+)?Barbier\b",
    ],

    "pers_barbier_de_la_serre": [
     r"\b(?:M\.\s+)?Barbier\s+de\s+La\s+Serre\b",
    ],

    "pers_bardonnet": [
     r"\b(?:M\.\s+)?Marcel\s+Bardonnet\b",
     r"\b(?:M\.\s+)?Bardonnet\s+\(?Marcel\)?\b",
     r"\b(?:M\.\s+)?Bardonnet\s+\(?Claude\)?\b",
    ],

    "pers_bigo_dr": [
     r"\b(?:(Docteur|Dr)\s+)?Bigo\b",
    ],

    "pers_bloncourt_elie": [
     r"\b(?:M\.\s+)?((É|E)lie([- ]Clainville)?\s+)?(Clainville-Bloncourt|Bloncourt)(\s+\(?(É|E)lie([- ]Clainville)?\)?)?\b",
    ],

    "pers_bocquet_maurice": [
     r"\b(?:M\.\s+)?(Maurice\s+)?Bocquet(\s+\(?Maurice\)?)?\b",
    ],

    "pers_boetzel_capitaine": [
     r"\b(?:Capitaine\s+)?Boetzel\b",
    ],

    "pers_bonnefon_dr": [
     r"\b(?:Dr|Docteur)\s+Bonnefon\b",
    ],

    "pers_brandes_marthe": [
     r"\b(?:(Mme|Madame)\s+)?(?:Marthe\s+)?Brandès\b",
    ],

    "pers_brieux_eugene": [
     r"\b(?:(M\.|monsieur)\s+)Brieux\b",
     r"\b(?:M\.\s+)?(E\.|Eugène)\s+Brieux\b",
     r"\b(?:M\.\s+)?Brieux\s+\(?(E\.|Eugène)\)?\b",
    ],

    "pers_brisac": [
     r"\b(?:M\.\s+)?Brisac\b",
    ],

    "pers_brisson_yvonne": [
     r"\b(?:(Mme|Madame)\s+)Brisson\b",
    ],

    "pers_brusson_joseph": [
     r"\b(?:M\.\s+)?Joseph\s+Brusson\b",
     r"\b(?:M\.\s+)?Brusson\s+\(?Joseph\)?\b",
    ],

    "pers_cantonnet_dr": [
     r"\b(?:(Docteur|Dr)\s+)?Cantonnet\b",
    ],

    "pers_casenave_jean": [
     r"\b(?:M\.\s+)?Jean\s+Casenave\b",
    ],

    "pers_chevalier_mme": [
     r"\b(?:(Mme|Madame)\s+)Chevalier\b",
    ],

    "pers_citerne_david": [
     r"\b(?:M\.\s+)?(David\s+)?Citerne(\s+\(?David\)?)?\b",
    ],

    "pers_magasinier": [
     r"\b(?:M\.\s+)?(Népomucène\s+)?Citrouillard(\s+\(?Népomucène\)?)?\b",
     r"\b(?:M\.\s+)?[Mm]agasinier\b",
    ],

    "pers_conan_albert": [
     r"\b(?:(M\.|monsieur)\s+)\s+Conan\b",
     r"\b(?:M\.\s+)?Albert\s+Conan\b",
     r"\b(?:M\.\s+)?Conan\s+\(?Albert\)?\b",
    ],

    "pers_contamin_henriette": [
     r"\b(?:(Mme|Madame)\s+)Contamin\b",
    ],

    "pers_coppet_maurice_de": [
     r"\b(?:Maurice\s+de\s+)?Coppet\b",
    ],

    "pers_cromwell_william_nelson": [
     r"\b(?:William\s+)?(Nelson\s+)?Cromwell\b",
    ],

    "pers_crozon_leon": [
     r"\b(?:M\.\s+)?(Léon\s+)?Crozon(\s+\(?Léon\)?)?\b",
    ],

    "pers_dallet_francois": [
     r"\b(?:M\.\s+)?(François\s+)?Dallet(\s+\(?François\)?)?\b",
    ],

    "pers_devarrieux_emile": [
     r"\b(?:M\.\s+)?Emile\s+Devarrieux\b",
     r"\b(?:M\.\s+)?Devarrieux\s+\(?Emile\)?\b",
    ],

    "pers_dewitte": [
     r"\b(?:M\.\s+)?Dewitte\b",
    ],

    "pers_donnay_maurice": [
     r"\b(?:M\.\s+)?Maurice\s+Donnay\b",
    ],

    "pers_dorgeles_roland": [
     r"\b(?:M\.\s+)?(Roland\s+)?Dorgelès(\s+\(?Roland\)?)?\b",
    ],

    "pers_dubois_georges": [
     r"\b(?:M\.\s+)?Georges\s+Dubois\b",
    ],

    "pers_dubrac_roger": [
     r"\b(?:M\.\s+)?(Roger\s+)?Dubrac(\s+\(?Roger\)?)?\b",
    ],

    "pers_dupuis": [
     r"\b(?:M\.\s+)?Joseph\s+Dupuis\b",
     r"\b(?:M\.\s+)?Dupuis\s+\(?Joseph\)?\b",
     r"\b(?:M\.\s+)?Dupuis\s+\(?René\)?\b",
    ],

    "pers_durand_rene": [
     r"\b(?:M\.\s+)?René\s+Durand\b",
     r"\b(?:M\.\s+)?Durand\s+\(?René\)?\b",
    ],

    "pers_escullie_antonin": [
     r"\b(?:M\.\s+)?(Antonin\s+)?Escullié(\s+\(?Antonin\)?)?\b",
    ],

    "pers_capitaine_eugene_lucien": [
     r"\b(?:M\.\s+)?Eugène([- ]Lucien)?\s+Capitaine\b",
     r"\b(?:M\.\s+)?Capitaine\s+\(?Eugène([- ]Lucien)?\)?\b",
    ],

    "pers_faille_leon": [
     r"\b(?:M\.\s+)?(Léon\s+)?Faille(\s+\(?Léon\)?)?\b",
    ],

    "pers_faudot_bernard": [
     r"\b(?:M\.\s+)?(Bernard\s+)?Faudot(\s+\(?Bernard\)?)?\b",
    ],

    "pers_favret_rene": [
     r"\b(?:M\.\s+)?(René\s+)?Favret(\s+\(?René\)?)?\b",
    ],

    "pers_ferrier_dr": [
     r"\b(?:M\.\s+)?Ferrier\b",
    ],

    "pers_fontaine_leon": [
     r"\b(?:M\.\s+)?Léon\s+Fontaine\b",
     r"\b(?:M\.\s+)?Fontaine\s+\(?Léon\)?\b",
    ],

    "pers_fourcade_jean_marie": [
     r"\b(?:M\.\s+)?Jean[- ]Marie\s+Fourcade\b",
     r"\b(?:M\.\s+)?Fourcade\s+\(?Jean[- ]Marie\)?\b",
    ],

    "pers_getty_alice": [
     r"\b(?:Miss\s+)?(?:Alice\s+)?Getty\b",
    ],

    "pers_godart_justin": [
     r"\b(?:Justin\s+)?Godart\b",
    ],

    "pers_goubin_eugene": [
     r"\b(?:M\.\s+)?(Eugène\s+)?Goubin(\s+\(?Eugène\)?)?\b",
    ],

    "pers_granger_marie": [
     r"\b(?:(Mme|Madame|Mlle)\s+)(Marie\s+)?Granger\b",
    ],

    "pers_grattepain_albert": [
     r"\b(?:M\.\s+)?(Albert\s+)?Grattepain(\s+\(?Albert\)?)?\b",
    ],

    "pers_guilhemjouan": [
     r"\b(?:M\.\s+)?Guilhemjouan,?\s+\(?Jean\)?\b",
    ],

    "pers_harper_grace": [
     r"\b(?:Miss\s+)?(?:Grace\s+)?(?:Grass\s+)?Harper\b",
    ],

    "pers_herriot_edouard": [
     r"\b(?:Édouard\s+)?Herriot\b",
    ],

    "pers_holt_winifred": [
     r"\b(?:Miss\s+)?(?:Winifred\s+)?Holt\b",
    ],

    "pers_hourcade": [
     r"\b(?:M\.\s+)?Hourcade\b",
    ],

    "pers_izaac_henri": [
     r"\b(?:Capitaine\s+)?(?:Henri\s+)?Izaac\b",
    ],

    "pers_jezequel_yves": [
     r"\b(?:M\.\s+)?(Yves\s+)?Jézéquel(\s+\(?Yves\)?)?\b",
    ],

    "pers_juin_alphonse_marie_therese": [
     r"\b(?:le\s+Maréchal\s+et\s+)?Mme\s+la\s+Maréchale\s+Juin\b",
    ],

    "pers_kahn_leopold_mme": [
     r"\b(?:(Mme|Madame)\s+)(L[eé]opold\s+)?Kahn\b",
    ],

    "pers_kessler_georges_cora": [
     r"\b(?:(Mme|Madame)\s+)?(?:(Géo|Georges?)\s+)?Kessler\b",
     r"\b(?:(Mme|Madame)\s+)?Cora\s+Parsons\s+Kessler\b",
    ],

    "pers_levesque_gaston": [
     r"\b(?:M\.\s+)?(Gaston\s+)?L'Evesque(\s+\(?Gaston\)?)?\b",
    ],

    "pers_lacotas_alfred": [
     r"\b(?:M\.\s+)?((Alfred|Pierre)\s+)?Lacotas(\s+\(?(Alfred|Pierre)\)?)?\b",
    ],

    "pers_lagrange_prof": [
     r"\b(?:Professeur\s+)?Lagrange\b",
    ],

    "pers_lapotre_leon": [
     r"\b(?:M\.\s+)?(Léon\s+)?Lapôtre(\s+\(?Léon\)?)?\b",
    ],

    "pers_lardiere": [
     r"\b(?:M\.\s+)?Lardière\s+\(?Nestor\)?\b",
     r"\b(?:M\.\s+)?Lardière\s+\(?Roger\)?\b",
     r"\b(?:M\.\s+)?Roger\s+Lardière\b",
    ],

    "pers_leger_antonin": [
     r"\b(?:M\.\s+)?(?:(Antonin|Antony)\s+)Léger\b",
    ],

    "pers_leveau_desire": [
     r"\b(?:M\.\s+)?Leveau\s+\(?Désiré\)?\b",
     r"\b(?:M\.\s+)?Désiré\s+Leveau\b",
    ],

    "pers_levy_dhurmer_emmy": [
     r"\b(?:(Mme|Madame)\s+)Lévy-Dhurmer\b",
    ],

    "pers_limousin_veuve": [
     r"\b(?:(Mme|Madame|Mlle)\s+)(V(eu)?ve\s+)?Limousin\b",
    ],

    "pers_loiseau_alfred": [
     r"\b(?:Mme\s+)Loiseau\b",
     r"\b(?:M\.\s+)?Alfred\s+Loiseau\b",
     r"\b(?:M\.\s+)?Loiseau\s+\(?Alfred\)?\b",
    ],

    "pers_lugol_georges": [
     r"\b(?:M\.\s+)?(Georges\s+)?Lugol\b",
    ],

    "pers_lyautey_hubert": [
     r"\b(?:Général|Maréchal)\s+Lyautey\b",
    ],

    "pers_malingre": [
     r"\bV(?:eu)?ve\s+Malingre\b",
     r"\b(?:M\.\s+)?Hippolyte\s+Malingre\b",
     r"\b(?:M\.\s+)?Malingre\s+\(?Hippolyte\)?\b",
    ],

    "pers_masselier_albert": [
     r"\b(?:M\.\s+)?(Albert\s+)?Masselier(\s+\(?Albert\)?)?\b",
    ],

    "pers_maunoury_marechal": [
     r"\b(?:(Maréchal|Général)\s+)Maunoury\b",
    ],

    "pers_millepied_augustin": [
     r"\b(?:M\.\s+)?(Augustin\s+)?Millepied(\s+\(?Augustin\)?)?\b",
    ],

    "pers_morax_victor": [
     r"\b(?:Dr|Docteur|Professeur)\s*(?:V\.\s*)?Morax\b",
    ],

    "pers_noirot": [
     r"\b(?:(Mme|Madame)\s+)?Marguerite\s+Noirot\b",
     r"\b(?:M\.\s+)?Noirot\s+\(?Maurice\)?\b",
     r"\b(?:M\.\s+)?Maurice\s+Noirot\b",
    ],

    "pers_pannetrat_henri": [
     r"\b(?:M\.\s+)?(Henri\s+)?Pannetrat(\s+\(?Henri\)?)?\b",
    ],

    "pers_perrin_antoine": [
     r"\b(?:M\.\s+)?Antoine\s+Perrin\b",
     r"\b(?:M\.\s+)?Perrin\s+\(?Antoine\)?\b",
    ],

    "pers_philippe_louis": [
     r"\b(?:M\.\s+)?Louis\s+Philippe\b",
     r"\b(?:M\.\s+)?Philippe\s+\(?Louis\)?\b",
    ],

    "pers_plein_doktor": [
     r"\bDoktor\s+Plein\b",
    ],

    "pers_polliot_bouchart_jeanne": [
     r"\b(?:(Mme|Madame)\s+)(Jeanne\s+)?(Polliot-)?Bouchart\b",
    ],

    "pers_pouiles_louise": [
     r"\b(?:(Mme|Madame)\s+)(Louise\s+)?Pouiles\b",
    ],

    "pers_rapilly_alexandre": [
     r"\b(?:M\.\s+)?(Alexandre\s+)?Rapilly(\s+\(?Alexandre\)?)?\b",
    ],

    "pers_henri_robert": [
     r"\b(?:(Me|bâtonnier)\s+)?Henri[- ]Robert\b",
    ],

    "pers_roche": [
     r"\b(?:M\.\s+)?Abel\s+Roche\b",
     r"\b(?:M\.\s+)?Roche\s+\(?Abel\)?\b",
     r"\b(?:M\.\s+)?Jean\s+Roche\b",
     r"\b(?:M\.\s+)?Roche\s+\(?Jean\)?\b",
     r"\b(?:M\.\s+)?Louis\s+Roche\b",
     r"\b(?:M\.\s+)?Roche\s+\(?Louis\)?\b",
    ],

    "pers_roubaud_ambroise": [
     r"\b(?:M\.\s+)?(Ambroise\s+)?Roubaud(\s+\(?Ambroise\)?)?\b",
    ],

    "pers_roy": [
     r"\b(?:M\.\s+)?Georges\s+Roy\b",
     r"\b(?:M\.\s+)?Roy\s+\(?Georges\)?\b",
     r"\b(?:M\.\s+)?René\s+Roy\b",
     r"\b(?:M\.\s+)?Roy\s+\(?René\)?\b",
    ],

    "pers_sallerin_commandant": [
     r"\b(?:Commandant\s+)Sallerin\b",
    ],

    "pers_scapini_georges": [
    r"\b(?:Georges\s+)?Scapini\b",
    ],

    "pers_serre_capitaine": [
     r"\b(?:(camarade|capitaine)\s+)Serre\b",
     r"\b(?:M\.\s+)?Serre\s+\(?Léon\)?\b",
     r"\b(?:M\.\s+)?Serre\s+\(?Pierre\)?\b",
    ],

    "pers_sexe_dr": [
     r"\b(?:(Docteur|Dr)\s+)?Sexe\b",
    ],

    "pers_siegfried_jules_fils": [
     r"\b(?:Jules\s+)?Siegfried\s[Ff]ils\b",
    ],

    "pers_tharaud_jerome_jean": [
     r"\b(?:(Jérôme(\s+et\s+Jean)?|Jean)\s+)?Tharaud\b",
    ],

    "pers_thebault_leon": [
     r"\b(?:M\.\s+)?(Léon\s+)?Thébault(\s+\(?Léon\)?)?\b",
    ],

    "pers_toutain_lucien": [
     r"\b(?:M\.\s+)?Toutain\s+\(?Lucien\)?\b",
    ],

    "pers_toutain_paul": [
     r"\b(?:M\.\s+)?(Paul\s+)?Toutain(\s+\(?Paul\)?)?\b",
    ],

    "pers_truy_gustave": [
     r"\b(?:M\.\s+)?(Gustave\s+)?Truy(\s+\(?Gustave\)?)?\b",
    ],

    "pers_vallery_radot_rene": [
     r"\b(?:M\.\s+)?(Ren(é|e)\s+)?Vallery-Radot(\s+\(?Ren(é|e)\)?)?\b",
    ],

    "pers_veyrier_paul": [
     r"\b(?:M\.\s+)?(Paul\s+)?Veyrier(\s+\(?Paul\)?)?\b",
    ],

    "pers_villey_pierre": [
     r"\b(?:M\.\s+)?Pierre\s+Villey\b",
    ],
}

def persName(text):
    """
    Encode all person names found in the text using TEI <persName> tags.

    :param text: str — input text
    :return: (str, dict) — encoded text + matches found
    """

    matches = {}  # dictionnaire des correspondances trouvées

    for ref, patterns in PERS_PATTERNS.items():
        for pattern in patterns:
            regex = re.compile(pattern, flags=re.IGNORECASE)

            # On récupère les correspondances AVANT substitution
            for match in regex.finditer(text):
                found = match.group(0)   # <-- CORRECTION ICI
                matches.setdefault(ref, []).append(found)

            # On encode dans le texte
            text = regex.sub(fr'<persName ref="#{ref}">\g<0></persName>', text)

    return text, matches

def orgName(text):
    """
    Encode all organization names found in the text using TEI <orgName> tags.
    Returns: encoded text + matches found
    """

    matches = {}

    for ref, patterns in ORG_PATTERNS.items():
        for pattern in patterns:
            regex = re.compile(pattern, flags=re.IGNORECASE)

            found = regex.findall(text)
            if found:
                matches.setdefault(ref, []).extend(found)

            text = regex.sub(fr'<orgName ref="#{ref}">\g<0></orgName>', text)

    return text, matches