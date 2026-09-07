# Arena de démarrage kuro centrée sur la qualité sonore

## Livrables de cette exécution

Le chemin retenu est NAS → serveur kuro → ordinateur dédié au salon servant de streamer réseau → USB → DDC → HDMI/I2S → DAC Terminator. Le serveur kuro et l’ordinateur du salon sont distincts. Linux sur le renderer est une hypothèse initiale à vérifier. Lire `scope-addendum.md` avant le reste de ce dossier. Les modèles exacts et les capacités USB restent inconnus, sans bloquer la recherche ni le prototype.

L'exécution livre une comparaison de trois architectures, une synthèse argumentée, un choix technique provisoire et un prototype synthétique relançable. Le prototype doit produire des preuves sur l'intégrité des données audio et les effets observables du transport. Il ne mesure pas, à lui seul, l'horloge du DAC ni une qualité sonore.

Le paquet retenu doit rester assez petit pour être lu intégralement. Une page de justification, un schéma de responsabilités et de domaines d'horloge, des contrats essentiels et un plan de preuve suffisent par candidat.

Après synthèse, le parent est autorisé à implémenter et committer le prototype dans le dépôt. Il utilise des médias synthétiques générés et des ressources temporaires. Un protocole de laboratoire doit être nommé comme tel. Il ne constitue pas un faux pilote du streamer utilisateur. Les fichiers musicaux, les réglages audio et le matériel utilisateur restent hors des mutations du prototype.

Le prototype attendu comprend :

- Une source synthétique PCM déterministe avec paramètres explicites, une identité de contenu et des limites de piste identifiables. Un corpus encodé peut s'ajouter si un décodeur réel est disponible et son rôle décrit.
- Un chemin de transport local reproductible qui permet de comparer les données émises et reçues. Le rapport distingue octets du fichier, échantillons décodés et données réellement observées à chaque frontière.
- Des perturbations contrôlées de livraison, par exemple attente ou fragmentation, et l'observation de leurs conséquences sur un récepteur de laboratoire. Le modèle de consommation précise son horloge et ses hypothèses. Ses niveaux de tampon, retards ou sous-alimentations éventuelles ne deviennent jamais une mesure de jitter DAC.
- Au moins un contrôle positif et un contrôle négatif. Le chemin transparent restitue les échantillons attendus, tandis qu'une modification volontaire d'échantillon est détectée. Une coupure ou un délai dépassant le modèle de tampon produit un résultat explicite au lieu d'un succès trompeur.
- Un rapport structuré relançable avec versions, paramètres, commandes, résultats bruts et limites. Les sources synthétiques restent identiques avant et après. Le test échoue lorsque l'intégrité attendue est violée.

Si le transport choisi fonctionne sans décodage côté serveur, sa preuve ne doit pas prétendre caractériser le décodage réel du streamer. Si le serveur décode, la comparaison doit couvrir séparément ce décodage et la livraison. Le prototype peut être plus concentré, mais le journal doit alors nommer la preuve manquante.

## Prompt commun remis aux candidats

Conçois une architecture de démarrage pour kuro centrée sur le transport audio NAS → serveur kuro → ordinateur dédié au salon, distinct du serveur, servant de streamer réseau → USB → DDC → HDMI/I2S → DAC Terminator. La qualité sonore prime. L'utilisateur rapporte entendre des différences entre streamers et avoir peu apprécié le son de Roon il y a environ deux ans. Roon inspire les fonctions, sans imposer son architecture. N'attribue aucune cause technique à cette expérience sans preuve.

Lis `scope-addendum.md`, le grounding partagé, les études primaires fournies par le parent et les documents actifs du dépôt. Lis aussi `architect/SKILL.md`, `architect/references/runner-prompt.md`, `architect/references/rationale-template.md` et `architect/references/design-red-flags.md`. Le dernier message utilisateur reconfigure le travail. Le périmètre local de l'ancien U-M1 est une contradiction à expliciter, pas une interdiction d'étudier le streamer. Les besoins de multiroom, mobile et accès distant ne sont pas réadmis.

La référence d'écoute actuelle est un Aurender avec musique stockée localement, piloté par Conductor 5, relié à un DDC puis à un DAC Terminator via HDMI/I2S. L'utilisateur appelle le fabricant du DDC "Dynafripp". Denafrips est une hypothèse, pas un fait confirmé; les modèles exacts ne sont pas connus. L'objectif est de remplacer l'Aurender par un ordinateur de salon qui reçoit la musique par réseau et sort en USB vers le DDC existant. Cet ordinateur est distinct du serveur kuro. Linux sur cet ordinateur est une hypothèse de travail initiale. Installer un renderer ouvert sur cet ordinateur est une voie pratique à étudier; il n'est pas nécessaire de contrôler l'Aurender ou d'obtenir son protocole propriétaire. N'invente pas les capacités USB, modes d'horloge ou fréquences supportées du DDC. Aucune autre réponse matériel n'est requise avant la recherche ou le prototype. Distingue ce qui se décide maintenant, ce qui dépend de ces capacités et ce qui doit se mesurer sur la chaîne.

Produis un paquet compact dans ton répertoire candidat, avec `rationale.md`, `contracts.md` et `proof-plan.md`. Écris d'abord le parcours utilisateur et deux ou trois vrais appels métier. Déduis ensuite les types et signatures, avec corps non implémentés et une carte de modules. Le schéma doit montrer les données audio, les commandes, les tampons, les conversions et les domaines d'horloge. Pour chaque composant, nomme son propriétaire et son état durable ou temporaire. Les types de transport restent derrière une frontière métier.

Ton point de vue dédié impose une organisation initiale des responsabilités. Défends-la fermement, puis indique les faits qui la feraient perdre. Compare au moins une autre forme structurelle, pas seulement une autre bibliothèque dans la même architecture.

Trace le parcours de Lecture jusqu’à la sortie USB de l’ordinateur du salon, puis les frontières DDC et DAC connues ou inconnues. Indique qui lit les fichiers du NAS, décode, choisit le format transmis, applique éventuellement un gain ou un autre traitement, cadence la livraison, tamponne, consomme les échantillons et pilote la sortie. Lorsque le matériel ou la documentation ne permet pas de connaître une étape, écris inconnu. Sépare une cadence de livraison réseau, une horloge logicielle de simulation et l'horloge physique de conversion. Ne transforme pas l'équivalence d'échantillons en conclusion de qualité sonore.

Analyse les capacités réellement nécessaires du protocole : lecture à la demande, découverte ou configuration de l'appareil, formats et fréquences acceptés, commandes, volume, navigation dans la piste, transition entre pistes, état et erreurs. Classe chaque capacité comme documentée, observée ou inconnue. Un protocole propriétaire sans accès démontré ne peut pas devenir une dépendance acquise. Les pages officielles fournies par les chercheurs font autorité pour leurs faits précis. Cite les affirmations techniques qui orientent la décision, et distingue une inférence d'un fait documenté.

Le serveur doit pouvoir rester actif lorsque la fenêtre ferme. Les contrats existants qui protègent les sources, les références de bibliothèque, la file et la reprise arrêtée restent utiles. Propose seulement le minimum d'API pour sélectionner un appareil compatible, préparer une lecture, la démarrer explicitement et obtenir un état ou une erreur. N'invente pas une interface complète, des réglages audiophiles ou des traitements du signal sans besoin établi. Décris comment rendre visibles le format livré et les traitements connus sans affirmer que des étapes inconnues sont transparentes.

Choisis un langage de prototype et justifie-le par le travail réel du serveur, les composants audio et protocolaires accessibles, la testabilité et le coût opérationnel. Présente l'adoption finale comme réversible tant que les essais manquent. Une propriété générale du langage n'est pas une preuve de son supérieur. Explique quel essai pourrait rendre ce choix inadapté.

Propose un petit prototype qui génère un PCM déterministe, le transporte vers un récepteur de laboratoire et compare le contenu reçu. Il doit détecter une corruption volontaire et rendre visibles une coupure ou une livraison trop tardive selon un modèle de consommation explicite. Ce modèle peut produire une mesure de comportement du transport, jamais une mesure de l'horloge du DAC. Identifie les frontières où l'on compare octets et échantillons, et toute simulation. Un décodeur réel, s'il est disponible, peut être éprouvé séparément. Donne les commandes envisagées, les résultats attendus et les artefacts bruts conservés.

Complète par le prochain essai sur matériel qui départagerait les principales hypothèses. Distingue contrôle de format et de traitements, comparaison d'écoute avec variables contrôlées, mesure analogique ou d'horloge et compatibilité du protocole. N'exige pas un laboratoire complet pour rendre un progrès utile, mais n'invente pas de preuve physique en son absence.

Ne code pas le produit complet et ne modifie pas le dépôt. Écris uniquement dans ton répertoire candidat. Le parent implémentera après synthèse. Livre une proposition concentrée avec alternatives rejetées, risques et première étape immédiatement exécutable.

Une connexion directe du serveur kuro au DDC peut servir de comparaison diagnostique ultérieure. Elle ne remplace pas l'architecture demandée avec un ordinateur de salon distinct et ne constitue pas un quatrième candidat recommandé.

## Points de vue attribués séparément

### A. Le renderer tire les données à mesure de la lecture

Place le décodage, le tampon de lecture et la consommation côté ordinateur du salon. Le serveur expose les médias du NAS et orchestre la session; le renderer récupère les données à mesure de ses besoins, sans exiger la copie complète du média avant Lecture. Évalue un renderer ouvert et un contrôle distinct du transfert. Montre les limites du flux progressif face aux interruptions, les transitions entre pistes et ce que le logiciel peut observer jusqu'à la sortie USB. Le serveur reste dans le chemin de données demandé.

### B. Le serveur prépare et pousse un flux audio explicite

Place le décodage et la définition du flux PCM côté serveur. Un récepteur ouvert installé sur l'ordinateur du salon tamponne le flux et le livre à sa sortie USB vers le DDC. Explique le contrat de débit, la rétroaction et le comportement face au manque ou à l'excès de données, sans supposer que le serveur commande l'horloge physique du DAC. Évalue le coût du protocole et de son récepteur, les formats et transitions de fréquence, ainsi que les conditions qui invalideraient ce choix.

### C. Le renderer prépare une copie vérifiée et possède la session locale

Place la file d'exécution, la préparation locale des pistes ou albums, la vérification d'intégrité, le décodage et la lecture USB dans l'ordinateur du salon. Le serveur kuro transmet les références et les médias du NAS; le renderer n'admet une piste prête que lorsque sa copie complète est vérifiée. Compare la préparation à la piste et à l'album. Définis l'identité du contenu, les changements de fichier pendant le transfert, l'invalidation et le budget du stockage reconstructible, sans confondre ce cache avec une nouvelle bibliothèque durable. Montre le comportement lors d'un arrêt du réseau et lors d'une commande de file concurrente. Justifie la propriété de la session côté renderer sans dupliquer une seconde vérité de playlist ou déclencher une reprise automatique. Cette forme teste l'intérêt d'une lecture locale préparée sur le renderer; elle ne promet aucun avantage sonore par ce seul mécanisme.

## Rubrique réservée au parent et au juge

Ne pas transmettre cette section aux candidats. Chaque critère reçoit 0, 1 ou 2 points. Zéro signifie absent ou contradictoire, un signifie incomplet, deux signifie traçable dans les contrats et vérifiable par les preuves proposées. Total sur 12.

| Critère | Condition pour 2 points |
| --- | --- |
| Responsabilités audio et horloges | Le trajet nomme lecture NAS, décodage, traitements, transport, tampon et sortie, avec domaines d'horloge et inconnues explicites. Aucune mesure de temporisation réseau n'est appelée jitter DAC. |
| Fidélité au nouveau besoin | La proposition traite NAS → serveur → ordinateur de salon distinct → USB DDC → I2S DAC, vise le remplacement de l’Aurender et explicite la contradiction avec U-M1 local. Elle conserve les protections utiles de bibliothèque sans inventer les modèles exacts. |
| Faisabilité protocolaire et matériel | Les capacités requises et leurs statuts documenté/observé/inconnu apparaissent. Les capacités USB inconnues produisent des essais conditionnels. Un renderer installable sur l’ordinateur du salon évite de dépendre du protocole Aurender. Linux reste une hypothèse initiale explicite. |
| Preuve synthétique falsifiable | Le prototype proposé transporte réellement le contenu dans sa limite déclarée, détecte une corruption injectée et une livraison insuffisante, préserve les sources et produit des résultats bruts relançables. Il sépare octets, échantillons, simulation et sortie physique. |
| Architecture et langage proportionnés | Quelques opérations métier cachent la coordination, les types montrent la session et ses erreurs, et le langage se justifie par des composants et expériences accessibles. Une condition concrète de révision est donnée. |
| Décision SQ honnête et test suivant | Les conclusions reposent sur sources primaires ou résultats identifiés. Elles séparent hypothèse audible, intégrité numérique et mesure physique. Le prochain test sur matériel peut départager au moins deux causes ou architectures. |

Une affirmation non corrigée de supériorité sonore déduite du langage, d'une égalité de fichiers ou d'un modèle réseau élimine le candidat. Un protocole propriétaire présenté comme utilisable sans accès démontré est aussi bloquant. À égalité, choisir la forme qui expose le moins de règles internes aux appelants et qui obtient la prochaine preuve décisive avec le moins de composants.

Le parent lit chaque proposition intégralement, compare son classement au juge puis consigne base, greffes et rejets. Tous les candidats et le juge restent GPT-6 Astra, raisonnement high, conformément à l'instruction utilisateur. Le journal consigne pourquoi la première arena a été suspendue et ce que cette nouvelle étude prouve réellement.
