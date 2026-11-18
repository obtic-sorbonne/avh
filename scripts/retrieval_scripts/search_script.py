import os
import re
import sys
import xml.etree.ElementTree as ET

# ---------------------------------------------------------
# Liste des regex à rechercher
# ---------------------------------------------------------
REGEX_GROUPS = {
    "regex" : [
    r"\\times",
    ],

    "REGEX_PATTERNS_TYPOLOGIE" : [
        r"\b[Éé]nucléés?\b",
        r"\b[Éé]nucléation\b",
        r"\b[Pp]rothèse\s+oculaire\b",
        r"\b[Cc]écité\s+pratique\b",
        r"\b(?:[Œœ]il|Oe?il|yeux(?:\s+à)?)\s+(?:de\s+verre\s+)?(?:artificiels?\s+)?(?:à\s+)?(?:simple|double)\s+coque\b",
        r"\b[Gg]az\s+lacrymogènes?\b",
        r"\b([Bb]i-)?[Mm]anchots?\b",
        r"\b[Tt]répanés\b",
        r"\b[Aa]liénés\b",
        r"\b[Rr]éformé\s+n°\s*(?:1|2)\b",
        r"\b[Aa]lsaciens-Lorrains\b",
        r"\b[Aa]veugles?\s+résistants?\b",
        r"\b[Aa]veugles?\s+chargés?\s+de\s+famille\b",
        r"\b[Aa]veugles?\s+mariés?\b",
        r"\b[Aa]veugles?\s+célibataires?\b",
    ],

    "REGEX_PATTERNS_METIERS" : [
        # Artisanat
        r"\b[Bb]rossier\b",
        r"\b[Bb]rosserie\b",
        r"\b[Cc]haisier\b",
        r"\b[Cc]anneur\b",
        r"\b[Cc]annage\b",
        r"\b[Rr]empailleur\b",
        r"\b[Rr]empaillage\b",
        r"\b[Rr]otinage\b",
        r"\b[Vv]annier\b",
        r"\b[Vv]annerie\b",
        r"\b[Oo]siériculture\b",
        r"\b[Cc]ordonnier\b",
        r"\b[Tt]onnelier\b",
        r"\b[Mm]enuisier\b",
        r"\b[Rr]elieur\b",
        r"\b[Tt]ricoteur\b",
        r"\b[Mm]atelassier\b",
        r"\b[Ss]parterie\b",
        r"\b[Ll]uthier\b",

        # Agriculture
        r"\b[Cc]ultivateur\b",
        r"\b[Jj]ardinier\b",
        r"\b[Aa]piculteur\b",
        r"\b[Aa]viculteur\b",
        r"\b[Vv]igneron\b",

        # Métiers techniques / administratifs
        r"\b[Tt]éléphoniste\b",
        r"\b[Dd]actylographe\b",
        r"\b[Mm]asseur\b",
        r"\b[Aa]justeur-mécanicien\b",
        r"\b[Aa]ccordeur\s+de\s+pianos\b",
        r"\b[Rr]eprésentant\s+de\s+commerce\b",

        # Métiers intellectuels / religieux
        r"\b[Ii]nstituteur\b",
        r"\b[Aa]vocat\b",
        r"\b[Mm]agistrat\b",
        r"\b[Mm]édecin\b",
        r"\b[Oo]rganiste\b",
        r"\b[Éé]crivain\b",
    ],

    "REGEX_PATTERNS_GLOSSAIRE" : [
        r"\b[Cc]agna\b",
        r"\b[Gg]ourbi\b",
        r"\b[Rr]adouille\b",
        r"\b[Aa]batis\b",
        r"\b[Pp]apelard\b",
        r"\b[Ll]oquet\b",
        r"\b[Pp]lacage\b",
        r"\b[Pp]laqueur(\s+de\s+brosses)?\b",
        r"\b(?:[Cc]hiendent|[Tt]ampico|[Pp]iassava|[Bb]assine|[Kk]itool)\b",
        r"\b(?:[Éé]crevisse|[Mm]orue|[Vv]ergette|[Pp]alot|[Ll]angue\s+de\s+chat|[Bb]rasseur|[Ll]ave-pont)\b",
        r"\b(?:[Gg]recquage|[Ee]ndossure|[Jj]aspure)\b",
        r"\b(?:Optophone|Cubarite|Photoélectrographe|Visagraphe|Sténomasque)\b",
        r"\b[Rr]appel\s+d'arrérages\b"
    ],

    "REGEX_PATTERNS_FEMMES" : [
        r"\b[Ii]nfirmières?\b",
        r"\b[Mm]arraines?\b",
        r"\b[Pp]atronesses?\b",
        r"\bAntigone\b",
        r"\b[Ff]emmes\s+d'aliénés\b",
        r"\b[Vv]euves?\b",
    ],

    "REGEX_PATTERNS_LOISIRS" : [
        r"\bMaison\s+de\s+Convalescence\s+de\s+Reuilly\b",
        r"\bÉcoles?\s+de\s+(?:Neuilly|Rochecorbon)\b",
        r"\bInternat\s+départemental\s+des\s+Aveugles\s+de\s+la\s+guerre\b",
        r"\b(?:Internat\s+du\s+)?château\s+de\s+Mazargues\b",
        r"\bVilla\s+des\s+Rosiers(?:\s+à\s+Menton-Garavan)?\b",
        r"\bFoyer\s+de\s+Boulleville\b",
        r"\bMaison\s+de\s+l'Aveugle\s+de\s+Guerre\b",
        r"\b[Ll]ivre\s+[Pp]arlé\b",
    ],

    "REGEX_PATTERNS_ASSOCIATIONS" : [
        r"\b(?:U\.?\s*A\.?\s*G\.?|(?:Union|(?:Groupement|Union)\s+Nationale?)\s+des\s+Aveugles\s+de\s+Guerre)\b",
        r"\b(?:(?:Association\s+dite\s+[\"«]?)?Pour\s+le\s+Foyer\s+du\s+Soldat\s+Aveugle[\"»]?|(?:[Ll]e\s+)?Foyer\s+du\s+Soldat\s+Aveugle|Œuvre\s+Pour\s+le\s+Foyer\s+du\s+Soldat\s+Aveugle|F\.?\s*S\.?\s*A\.?)\b",
        r"\b(?:A\.?\s*V\.?\s*H\.?|Association\s+Valentin\s+Haü?y(?:\s+pour\s+le\s+bien\s+des\s+aveugles)?)\b",
        r"\b(?:SIRLA|(?:Association\s+dite\s+[\"«]?)?Le\s+Livre\s+de\s+l['’]Aveugle[\"»]?|Société\s+d['’]Impression\s+et\s+de\s+Reliure\s+du\s+Livre\s+pour\s+les\s+Aveugles|Bibliothèque\s+du\s+Livre\s+de\s+l['’]Aveugle)\b",
        r"\b(?:A\.?\s*S\.?\s*A\.?|(?:Société\s+[\"«]?)?Les\s+Amis\s+des\s+Soldats\s+Aveugles[\"»]?)\b",
        r"\b(?:L['’])?Abri\s+du\s+Soldat\s+Aveugle\b",
        r"\b(?:Société\s+des\s+)?Ateliers\s+d['’]Aveugles\b",
        r"\b(?:(?:É|E)cole\s+de\s+massage\s+des\s+soldats\s+aveugles|(?:Œ|Oe)uvre\s+des\s+Masseurs)\b",
        r"\b(?:A\.?\s*A\.?\s*F\.?|Amitié\s+des\s+Aveugles\s+de\s+France)\b",
        r"\b(?:O\.?\s*L\.?\s*S\.?\s*A\.?|(?:Comité\s+Central\s+de\s+l['’]|Imprimerie\s+Beaunoise\s+du\s+|(?:Œ|Oe)uvre\s+(?:Nationale\s+du\s+)?)[Ll]ivre\s+des\s+[Aa]veugles\s+de\s+[Gg]uerre)\b",
        r"\b(?:(?:Société|Fédération|Association)\s+des\s+Mutilés\s+des\s+Yeux|Fédération\s+des\s+Aveugles\s+de\s+guerre,\s+des\s+blessés\s+et\s+malades\s+des\s+yeux)\b",
        r"\b(?:U\.?\s*N\.?\s*A\.?\s*C\.?|Union\s+Nationale\s+des\s+Aveugles\s+Civils)\b",
        r"\b(?:U\.?\s*F\.?\s*A\.?\s*C\.?|Union\s+Française\s+des\s+Associations\s+de\s+Combattants(?:\s*,\s*Prisonniers,\s*Combattants\s+de\s+la\s+Libération\s+et\s+Victimes\s+des\s+deux\s+guerres)?)\b",
        r"\b(?:U\.?\s*F\.?|Union\s+Fédérale(?:\s+des\s+Associations\s+(?:Françaises\s+de\s+)?Mutilés(?:\s+et\s+Réformés)?)?)\b",
        r"\b(?:U\.?\s*N\.?\s*C\.?|Union\s+Nationale\s+des\s+Combattants)\b",
        r"\b(?:U\.?\s*N\.?\s*M\.?\s*R\.?|Union\s+Nationale\s+des\s+Mutilés\s+et\s+Réformés)\b",
        r"\b(?:A\.?\s*G\.?\s*M\.?\s*G\.?|Association\s+Générale\s+des\s+Mutilés\s+de\s+la\s+Guerre)\b",
        r"\b(?:Confédération\s+Nationale(?:\s+des\s+Anciens\s+Combattants\s+et\s+Victimes\s+de\s+la\s+Guerre|\s+de\s+la\s+France\s+Meurtrie)?)\b",
        r"\b(?:Comité\s+d['’]Entente(?:\s+des\s+Grandes\s+Associations\s+Nationales\s+de\s+Combattants\s+et\s+de\s+Victimes\s+de\s+la\s+guerre|\s+des\s+Grands\s+Invalides\s+de\s+Guerre)?)\b",
        r"\b(?:P\.?\s*B\.?\s*R\.?\s*W\.?\s*F\.?|P\.?\s*B\.?\s*F\.?|Permanent\s+Blind\s+Relief\s+War\s+Fund(?:\s+(?:for\s+Soldiers\s+and\s+Sailors|incorporated|to\s+the\s+Alliés))?)\b",
        r"\bAmerican\s+Red\s+Cross\b",
        r"\bCroix[- ]rouge\s+am(é|e)ricaine\b",
        r"\b(?:A\.?\s*B\.?\s*P\.?|American\s+Braille\s+Press(?:\s+for\s+War\s+Disabled)?|A\.?\s*F\.?\s*O\.?\s*B\.?|American\s+Foundation\s+for\s+Overseas\s+Blind(?:,\s*Inc\.)?)\b",
        r"\bPhare\s+de\s+France\b",
        r"\bSt\s+Dunstan's\b",
        r"\bNational\s+Institute\s+for\s+the\s+Blind\b",
        r"\bCanadian\s+Institute\b",
        r"\bConseil\s+Mondial\b",
        r"\bFIDAC\b",
        r"\bCIAMAC\b",
        r"\bAmerican\s+Legion\b",
        r"\bBritish\s+Legion\b"
    ],

    "REGEX_PATTERNS_TEXTES_JURIDIQUES" : [
        #Lois et articles
        r"Loi\s+des\s+11\s+et\s+18\s+avril\s+1831",
        r"Loi\s+de\s+1831",
        r"Loi\s+du\s+9\s+avril\s+1898",
        r"Loi\s+du\s+13\s+juillet\s+1917",
        r"Loi\s+du\s+27\s+juillet\s+1917",
        r"Loi\s+des\s+pensions\s+(?:militaires\s+)?de\s+1919",
        r"\b(termes|texte|promulgation|conformité|application|dispositions)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919\b",
        r"\b(?:(rapport|loi)\s+)?Lugol\b",
        r"Article\s+10\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+12\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Articles?\s+(?:13|71)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Articles?\s+(?:14|19)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+55\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Articles?\s+(?:59|60)\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+64\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+67\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+69\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Article\s+76\s+de\s+la\s+loi\s+du\s+31\s+mars\s+1919",
        r"Loi\s+du\s+14\s+f[ée]vrier\s+1920",
        r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+juillet\s+1920",
        r"Loi\s+du\s+29\s+octobre\s+1921",
        r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+d[ée]cembre\s+1921",
        r"Loi\s+du\s+23\s+mars\s+1928",
        r"Loi\s+du\s+13\s+juillet\s+1928",
        r"Loi\s+Loucheur",
        r"Loi\s+(?:de\s+finances\s+)?du\s+30\s+d[ée]cembre\s+1928",
        r"Loi\s+(?:de\s+finances\s+)?du\s+31\s+mars\s+1932",
        r"Loi\s+du\s+22\s+mars\s+1935",
        r"Loi\s+du\s+22\s+ao[ûu]t\s+1946",
        r"Loi\s+du\s+27\s+f[ée]vrier\s+1948",
        r"Loi\s+du\s+29\s+juillet\s+1950",
        r"Loi\s+du\s+31\s+d[ée]cembre\s+1953",

        #Décrets et décisions
        r"D[ée]cision\s+(?:minist[ée]rielle\s+)?du\s+23\s+juillet\s+1887",
        r"(D[ée]cret[-–]loi\s+)?du\s+17\s+juin\s+1938",
        r"(Ordonnance\s+)?du\s+25\s+octobre\s+1945",
        r"(D[ée]cret\s+)?du\s+20\s+juillet\s+1954",

        #Allocations
        r"Allocation\s+(?:N[°o]?\s*)?5\s*bis",
        r"Allocation\s+(?:N[°o]?\s*)?6\b",
        r"Allocation\s+(?:N[°o]?\s*)?7\b",
        r"Allocation\s+(?:N[°o]?\s*)?8\b",

        #Autres
        r"Quart\s+de\s+place",
        r"Carte\s+à\s+double\s+barre\s+bleue",
        r"Statut\s+des\s+Grands\s+Mutil[ée]s(?:\s+de\s+Guerre)?",
        r"Dotation\s+Nationale\s+des\s+Grands\s+Mutil[ée]s",
        r"Code\s+de\s+la\s+Famille",
        r"Plan\s+[Qq]uadriennal",
        r"[Cc]revaison\s+du\s+plafond"
    ],

    "REGEX_PATTERNS_PERSONNES" : [
        r"\b(?:(M\.|Monsieur)\s+)?(?:(E\.|Eugène)\s+)?Brieux\b",
        r"\b(?:(Me|bâtonnier)\s+)?Henri[- ]Robert\b",
        r"\b(?:Dr|Docteur|Professeur)\s*(?:V\.\s*)?Morax\b",
        r"\b(?:M\.\s+)?Maurice\s+Donnay\b",
        r"\b(?:Capitaine\s+)?(?:Henri\s+)?Izaac\b",
        r"\b(?:M\.\s+)?Pierre\s+Villey\b",
        r"\b(?:Édouard\s+)?Herriot\b",
        r"\b(?:Maurice\s+de\s+)?Coppet\b",
        r"\b(?:Général|Maréchal)\s+Lyautey\b",
        r"\b(?:Justin\s+)?Godart\b",
        r"\b(?:Miss\s+)?(?:Alice\s+)?Getty\b",
        r"\b(?:Miss\s+)?(?:Winifred\s+)?Holt\b",
        r"\b(?:Mme\s+)(?:L[eé]opold\s+)?Kahn\b",
        r"\b(?:M\.\s+)?(René\s+)?Favret(\s+\(?René\)?)?\b",
        r"\b(?:Georges\s+)?Scapini\b",
        r"\b(?:Jules\s+)?Siegfried\s[Ff]ils\b",
        r"\b(?:(Mme|Madame)\s+)Brisson\b",
        r"\b(?:(Mme|Madame)\s+)Lévy-Dhurmer\b",
        r"\b(?:Mme\s+)Loiseau\b",
        r"\b(?:M\.\s+)?Alfred\s+Loiseau\b",
        r"\b(?:M\.\s+)?Loiseau\s+\(?Alfred\)?\b",
        r"\b(?:(Mme|Madame)\s+)Contamin\b",
        r"\b(?:(Mme|Madame)\s+)Chevalier\b",
        r"\b(?:le\s+Maréchal\s+et\s+)?Mme\s+la\s+Maréchale\s+Juin\b",
        r"\b(?:(Mme|Madame)\s+)?(?:Marthe\s+)?Brandès\b",
        r"\b(?:M\.\s+)?[Mm]agasinier\b",
        r"\b(?:M\.\s+)?(Népomucène\s+)?Citrouillard(\s+\(?Népomucène\)?)?\b",
        r"\b(?:M\.\s+)?(Albert\s+)?Masselier(\s+\(?Albert\)?)?\b",
        r"\b(?:M\.\s+)?(Albert\s+)?Grattepain(\s+\(?Albert\)?)?\b",
        r"\b(?:Miss\s+)?(?:Grace\s+)?(?:Grass\s+)?Harper\b",
        r"\b(?:M\.\s+)?Hourcade\b",
        r"\b(?:M\.\s+)?René\s+Roy\b",
        r"\b(?:M\.\s+)?Roy\s+\(?René\)?\b",
        r"\b(?:M\.\s+)?Joseph\s+Dupuis\b",
        r"\b(?:M\.\s+)?Dupuis\s+\(?Joseph\)?\b",
        r"\b(?:M\.\s+)?Dupuis\s+\(?René\)?\b",
        r"\b(?:M\.\s+)?Georges\s+Roy\b",
        r"\b(?:M\.\s+)?Roy\s+\(?Georges\)?\b",
        r"\b(?:M\.\s+)?Paul\s+Toutain\b",
        r"\b(?:M\.\s+)?Toutain\s+\(?Paul\)?\b",
        r"\b(?:M\.\s+)?Toutain\s+\(?Lucien\)?\b",
        r"\b(?:M\.\s+)?(Léon\s+)?Faille(\s+\(?Léon\)?)?\b", #Vérifier les cas de faille en minuscules
        r"\b(?:M\.\s+)?Emile\s+Devarrieux\b",
        r"\b(?:M\.\s+)?Devarrieux\s+\(?Emile\)?\b",
        r"\b(?:M\.\s+)?Antoine\s+Perrin\b",
        r"\b(?:M\.\s+)?Perrin\s+\(?Antoine\)?\b",
        r"\b(?:M\.\s+)?(Léon\s+)?Lapôtre(\s+\(?Léon\)?)?\b",
        r"\b(?:M\.\s+)?Louis\s+Roche\b",
        r"\b(?:M\.\s+)?Roche\s+\(?Louis\)?\b",
        r"\b(?:M\.\s+)?Abel\s+Roche\b",
        r"\b(?:M\.\s+)?Roche\s+\(?Abel\)?\b",
        r"\b(?:M\.\s+)?Jean\s+Roche\b",
        r"\b(?:M\.\s+)?Roche\s+\(?Jean\)?\b",
        r"\b(?:M\.\s+)?Louis\s+Philippe\b",
        r"\b(?:M\.\s+)?Philippe\s+\(?Louis\)?\b",
        r"\b(?:M\.\s+)?Guilhemjouan,?\s+\(?Jean\)?\b",
        r"\b(?:M\.\s+)?Roger\s+Lardière\b",
        r"\b(?:M\.\s+)?Lardière\s+\(?Roger\)?\b",
        r"\b(?:M\.\s+)?Lardière\s+\(?Nestor\)?\b",
        r"\b(?:M\.\s+)?Jean[- ]Marie\s+Fourcade\b",
        r"\b(?:M\.\s+)?Fourcade\s+\(?Jean[- ]Marie\)?\b",
        r"\b(?:M\.\s+)?Marcel\s+Bardonnet\b",
        r"\b(?:M\.\s+)?Bardonnet\s+\(?Marcel\)?\b",
        r"\b(?:M\.\s+)?Bardonnet\s+\(?Claude\)?\b",
        r"\b(?:M\.\s+)?Julien\s+Alix\b",
        r"\b(?:M\.\s+)?Alix\s+\(?Julien\)?\b",
        r"\b(?:M\.\s+)?Hippolyte\s+Malingre\b",
        r"\b(?:M\.\s+)?Malingre\s+\(?Hippolyte\)?\b",
        r"\bV(?:eu)?ve\s+Malingre\b",
        r"\b(?:(Mme|Madame)\s+)?(?:(Géo|Georges?)\s+)?Kessler\b",
        r"\b(?:(Mme|Madame)\s+)?Marguerite\s+Noirot\b",
        r"\b(?:M\.\s+)?Maurice\s+Noirot\b",
        r"\b(?:M\.\s+)?Noirot\s+\(?Maurice\)?\b",
        r"\b(?:M\.\s+)?(François\s+)?Dallet(\s+\(?François\)?)?\b",
        r"\b(?:M\.\s+)?(Henri\s+)?Pannetrat(\s+\(?Henri\)?)?\b",
        r"\b(?:M\.\s+)?(Augustin\s+)?Millepied(\s+\(?Augustin\)?)?\b",
        r"\b(?:M\.\s+)?(David\s+)?Citerne(\s+\(?David\)?)?\b", #Vérifier les cas de citerne en minuscules
        r"\b(?:M\.\s+)?(Maurice\s+)?Bocquet(\s+\(?Maurice\)?)?\b",
        r"\b(?:M\.\s+)?(Gustave\s+)?Truy(\s+\(?Gustave\)?)?\b",
        r"\b(?:Commandant\s+)Sallerin\b",
        r"\b(?:M\.\s+)?(Eugène\s+)?Goubin(\s+\(?Eugène\)?)?\b",
        r"\b(?:Capitaine\s+)?Boetzel\b",
        r"\b(?:M\.\s+)?(Ambroise\s+)?Roubaud(\s+\(?Ambroise\)?)?\b",
        r"\b(?:M\.\s+)?René\s+Durand\b",
        r"\b(?:M\.\s+)?Durand\s+\(?René\)?\b",
        r"\b(?:M\.\s+)?(?:(Antonin|Antony)\s+)Léger\b",
        r"\b(?:M\.\s+)?Joseph\s+Brusson\b",
        r"\b(?:M\.\s+)?Brusson\s+\(?Joseph\)?\b",
        r"\b(?:M\.\s+)?((Alfred|Pierre)\s+)?Lacotas(\s+\(?(Alfred|Pierre)\)?)?\b",
        r"\b(?:M\.\s+)?(Alexandre\s+)?Rapilly(\s+\(?Alexandre\)?)?\b",
        r"\b(?:M\.\s+)?Eugène([- ]Lucien)?\s+Capitaine\b",
        r"\b(?:M\.\s+)?Capitaine\s+\(?Eugène([- ]Lucien)?\)?\b",
        r"\b(?:M\.\s+)?(Yves\s+)?Jézéquel(\s+\(?Yves\)?)?\b",
        r"\b(?:M\.\s+)?(Léon\s+)?Thébault(\s+\(?Léon\)?)?\b",
        r"\b(?:M\.\s+)?(Bernard\s+)?Faudot(\s+\(?Bernard\)?)?\b",
        r"\b(?:M\.\s+)?Leveau\s+\(?Désiré\)?\b",
        r"\b(?:M\.\s+)?Désiré\s+Leveau\b",
        r"\b(?:M\.\s+)?Dewitte\b",
        r"\b(?:M\.\s+)?(Léon\s+)?Crozon(\s+\(?Léon\)?)?\b",
        r"\b(?:M\.\s+)?(Antonin\s+)?Escullié(\s+\(?Antonin\)?)?\b",
        r"\b(?:M\.\s+)?Georges\s+Dubois\b",
        r"\b(?:M\.\s+)?(Roger\s+)?Dubrac(\s+\(?Roger\)?)?\b",
        r"\b(?:M\.\s+)?(Paul\s+)?Veyrier(\s+\(?Paul\)?)?\b",
        r"\b(?:Dr|Docteur)\s+Bonnefon\b",
        r"\b(?:M\.\s+)?Léon\s+Fontaine\b",
        r"\b(?:M\.\s+)?Fontaine\s+\(?Léon\)?\b",
        r"\bLouis\s+Antoine\b",
        r"\bAntoine\s+\(?Louis\)?\b",
        r"\b(?:(Maréchal|Général)\s+)Maunoury\b",
        r"\b(?:(camarade|capitaine)\s+)Serre\b",
        r"\b(?:M\.\s+)?Serre\s+\(?Léon\)?\b",
        r"\b(?:M\.\s+)?Serre\s+\(?Pierre\)?\b",
        r"\b(?:M\.\s+)?((É|E)lie([- ]Clainville)?\s+)?(Clainville-Bloncourt|Bloncourt)(\s+\(?(É|E)lie([- ]Clainville)?\)?)?\b",
        r"\b(?:(Docteur|Dr)\s+)?Cantonnet\b",
        r"\b(?:(Docteur|Dr)\s+)?Sexe\b",
        r"\b(?:(Docteur|Dr)\s+)?Bigo\b",
        r"\b(?:M\.\s+)?Ferrier\b",
        r"\b(?:Professeur\s+)?Lagrange\b",
        r"\b(?:M\.\s+)?(Roland\s+)?Dorgelès(\s+\(?Roland\)?)?\b",
        r"\b(?:(Jérôme(\s+et\s+Jean)?|Jean)\s+)?Tharaud\b",
        r"\b(?:M\.\s+)?Barbier\s+de\s+La\s+Serre\b",
        r"\b(?:(Mme|Madame)\s+)(Jeanne\s+)?(Polliot-)?Bouchart\b",
        r"\bRené\s+Bastian\b",
        r"\b(?:William\s+)?(Nelson\s+)?Cromwell\b",
        r"\bDoktor\s+Plein\b",
        r"\b(?:(M\.|Colonel)\s+)?Baker\b",
        r"\b(?:M\.\s+)?Brisac\b",
        r"\b(?:M\.\s+)?Jean\s+Casenave\b",
        r"\b(?:Mme\s+)(Veuve\s+)?Barbier\b",
        r"\b(?:M\.\s+)?(Ren(é|e)\s+)?Vallery-Radot(\s+\(?Ren(é|e)\)?)?\b",
        r"\b(?:M\.\s+)?(Gaston\s+)?L'Evesque(\s+\(?Gaston\)?)?\b",
        r"\b(?:M\.\s+)?(Henri\s+)?Amblard(\s+\(?Henri\)?)?\b",
        r"\b(?:M\.\s+)?(Albert\s+)?Conan(\s+\(?Albert\)?)?\b",
        r"\b(?:Mlle\s+)(Marguerite\s+)?Arbel\b",
        r"\b(?:(Mme|Madame|Mlle)\s+)(Louise\s+)?Pouiles\b",
        r"\b(?:(Mme|Madame|Mlle)\s+)(Marie\s+)?Granger\b",
        r"\b(?:(Mme|Madame|Mlle)\s+)(V(eu)?ve\s+)?Limousin\b",
        r"\b(?:M\.\s+)?(Georges\s+)?Lugol\b",
    ], 

    "REGEX_PATTERNS_LIEUX" : [
        #France
        r"\b[Pp]aris\b",
        r"\b[Nn]euilly(?:-sur-Seine)?\b",
        r"\b[Ll]yon\b",
        r"\b[Mm]arseille\b",
        r"\b[Bb]ordeaux\b",
        r"\b[Tt]oulouse\b",
        r"\b[Nn]antes\b",
        r"\b[Nn]ice\b",
        r"\b[Cc]hartres\b",
        r"\b[Rr]ennes\b",
        r"\b[Ll]ille\b",
        r"\b[Tt]ours\b",
        r"\b[Mm]ontpellier\b",
        r"\b[Aa]miens\b",
        r"\b[Cc]lermont-Ferrand\b",
        r"\b[Dd]ijon\b",
        r"\b[Rr]ouen\b",
        r"\b[Rr]eims\b",
        r"\b[Ll]e\s+Havre\b",
        r"\b[Gg]renoble\b",
        r"\b[Tt]oulon\b",
        r"\b[Ss]trasbourg\b",
        r"\b[Ff]ranceville-Plage\b",
        r"\b[Rr]euilly\b",
        r"\b[Vv]als-les-Bains\b",

        #International
        r"\b[Nn]ew\s+[Yy]ork\b",
        r"\b[Gg]enève\b",
        r"\b[Ll]ausanne\b",
        r"\b[Bb]ruxelles\b",
        r"\b[Mm]adrid\b",
        r"\b[Rr]ome\b",
        r"\b[Ww]ashington\b",
        r"\b[Mm]ontréal\b",
        r"\b[Bb]uenos\s+[Aa]ires\b",
        r"\b[Ss]antiago\b",
        r"\b[Ll]e\s+[Cc]aire\b",
        r"\b[Ll]ondres\b",
        r"\b[Aa]lger\b",
    ]

}

def get_namespace(root):
    """Détecte automatiquement le namespace TEI."""
    m = re.match(r"\{.*\}", root.tag)
    return m.group(0) if m else ""


def extract_body_elements(root, ns):
    """
    Retourne les éléments du <body> en excluant <list> et <table>.
    Chaque élément est conservé avec son texte propre.
    """
    body = root.find(f".//{ns}body")
    if body is None:
        return []

    forbidden = {f"{ns}list", f"{ns}table", f"{ns}item", f"{ns}cell", f"{ns}ref"}

    elements = []
    for elem in body.iter():
        if elem.tag in forbidden:
            continue
        text = (elem.text or "").strip()
        if text:
            elements.append(elem)
    return elements


def split_into_sentences(text):
    """Découpe un texte en phrases en conservant la ponctuation."""
    return re.split(r'(?<=[\.\?\!])\s+', text)


def search_in_element(elem, regex):
    """
    Cherche une regex dans un élément TEI.
    Retourne : (forme trouvée, phrase complète, balise)
    """
    text = elem.text or ""
    sentences = split_into_sentences(text)
    pattern = re.compile(regex, re.IGNORECASE)

    results = []
    tag = re.sub(r"\{.*\}", "", elem.tag)  # enlever namespace

    for sentence in sentences:
        for m in pattern.finditer(sentence):
            form = m.group()
            results.append((form, sentence.strip(), tag))

    return results


def process_folder(folder_path, regex_list):
    """Analyse tous les fichiers XML du dossier."""
    results = {regex: {} for regex in regex_list}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".xml"):
            continue

        file_path = os.path.join(folder_path, filename)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except Exception as e:
            print(f"Erreur de lecture XML dans {filename}: {e}")
            continue

        ns = get_namespace(root)
        elements = extract_body_elements(root, ns)

        for regex in regex_list:
            matches = []
            for elem in elements:
                found = search_in_element(elem, regex)
                if found:
                    matches.extend(found)

            if matches:
                results[regex][filename] = matches

    return results


def write_output(output_file, results):
    """Écrit les résultats dans un fichier texte."""
    with open(output_file, "w", encoding="utf-8") as f:

        for regex, files in results.items():
            total = sum(len(v) for v in files.values())

            f.write(f"=============================\n")
            f.write(f"REGEX : {regex}\n")
            f.write(f"Total occurrences : {total}\n")
            f.write(f"=============================\n\n")

            for filename, matches in files.items():
                f.write(f"--- {filename} ---\n")
                for form, sentence, tag in matches:
                    f.write(f"Mot trouvé : '{form}'\n")
                    f.write(f"Balise     : <{tag}>\n")
                    f.write(f"Phrase     : {sentence}\n")
                    f.write("\n")

            f.write("\n\n")


def main():
    if len(sys.argv) < 4:
        print("Usage : python script.py <dossier_xml> <fichier_sortie> <nom_du_groupe>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_file = sys.argv[2]
    group_name = sys.argv[3]

    if group_name not in REGEX_GROUPS:
        print(f"Groupe '{group_name}' introuvable.")
        print("Groupes disponibles :", ", ".join(REGEX_GROUPS.keys()))
        sys.exit(1)

    regex_list = REGEX_GROUPS[group_name]

    results = process_folder(folder_path, regex_list)
    write_output(output_file, results)

    print(f"Analyse terminée. Groupe utilisé : {group_name}")
    print(f"Résultats écrits dans : {output_file}")


if __name__ == "__main__":
    main()
