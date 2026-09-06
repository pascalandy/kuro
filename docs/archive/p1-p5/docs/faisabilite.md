# Faisabilité et choix encore ouverts

La forme recommandée est un service local kuro avec bibliothèque et file propres, moteur réutilisé et desktop de contrôle. SQLite avec FTS5, libmpv et Tauri sont les premiers candidats à évaluer. Cette priorité donne un point de départ à P4. Elle ne sélectionne aucune licence ni stack définitive.

La documentation établit l'existence des composants et certaines limites. Elle ne prouve ni le gapless du corpus utilisateur, ni la réactivité à 20 000 albums, ni la restauration de kuro. Aucun média utilisateur, montage, DAC ou configuration locale n'a été inspecté. Les [sources techniques](sources-techniques.md) sont séparées du corpus Roon P2.

## Construire le domaine, réutiliser les mécanismes

kuro doit posséder les identités musicales, les règles de disponibilité, la file canonique et l'expérience de navigation. Construire aussi les décodeurs, une base transactionnelle ou les pilotes audio multiplierait les risques sans répondre à un usage distinct. La réutilisation se fait derrière les [contrats C-01 à C-09](architecture.md), avec versions et dépendances à figer après essais.

| Élément | Priorité proposée et justification | Alternative et critère de rejet | Preuve restante |
| --- | --- | --- | --- |
| Catalogue et recherche | SQLite avec FTS5 sur disque local. Catalogue relationnel, transactions et recherche dans le même service. | Index spécialisé si les requêtes et tris restent hors budget après mesure et correction des accès. Une base réseau n'est pas justifiée par le seul nombre d'albums. | Import cible, pagination, accents, concurrence avec lecture, migration et restauration. TECH-001 à TECH-004 |
| Moteur local | libmpv évalué en premier. Décodage, sorties et contrôle existants, sans déléguer le modèle musical. | MPD si sa file peut devenir une projection contrôlée ou une autorité explicitement acceptée. GStreamer si la maîtrise de la chaîne et des transitions justifie davantage de code. | Corpus gapless, préparation NAS, états observables, arrêt/reprise et licence du binaire exact. TECH-101 à TECH-104 |
| Décodage et tags | Réutiliser les capacités du moteur et un extracteur de tags existant à comparer. FFmpeg est un candidat d'analyse et de décodage, pas un service complet de bibliothèque. | Extracteur spécialisé si tags multivalués ou formats du corpus ne sont pas conservés. Éviter plusieurs interprétations contradictoires des tags. | Inventaire codecs réellement compilés, tags bruts, fichiers invalides, coût de scan. TECH-107 |
| Sortie Linux | Sortie partagée via moteur et environnement audio disponible, PipeWire à évaluer en priorité sur Omarchy. | Backend ALSA selon matériel et besoin futur. Aucune exclusivité imposée à M1. | Périphérique réel, volume, format effectif, coexistence avec autres applications. TECH-106 |
| Desktop | Tauri évalué en premier comme contrôle web avec service indépendant. Les interfaces audio ne passent pas par le lecteur du navigateur. | Qt si WebKitGTK, listes, clavier ou intégration Linux ne satisfont pas les essais. Electron si la cohérence du moteur web devient décisive et son coût mesuré acceptable. | Accessibilité proposée, navigation cible, mémoire, démarrage, Wayland et reconnexion. TECH-108 à TECH-110 |
| Serveur existant | MPD et Navidrome comparés comme forme C complète, pas comme bibliothèques interchangeables. | Conserver la forme B si identités et évolutions M2 exigent de maintenir deux catalogues concurrents. | Rapprochement de copies, éditions, file, sauvegarde et sorties. TECH-101, TECH-105 |
| Accès NAS | Consommer un montage existant fourni par le système. SMB monté est la première hypothèse documentaire. | Client SMB natif si le montage ne satisfait pas l'usage. Cela ajoute authentification, reconnexion et lectures aléatoires à kuro. | Protocole réel, droits, débit, disparition du montage et retour. TECH-006, TECH-207 |
| Packaging | Première étude d'un paquet Linux incluant cycle de vie du service utilisateur et desktop. | Flatpak à comparer avec accès fichiers, audio, IPC et service indépendant. Ne pas accorder tout le disque pour contourner un problème de permission. | Environnement propre, lancement, fermeture fenêtre, arrêt service et désinstallation des seuls fichiers kuro. TECH-007 |

Tauri, Qt et Electron n'imposent pas le langage du service. Le choix de Rust, C++ ou d'un autre langage dépendra notamment de l'intégration du moteur, de la maintenance et des compétences retenues. Aucun fichier applicatif ou manifeste n'est créé pour matérialiser cette préférence documentaire.

## Compromis audio à vérifier avant adoption

mpv propose plusieurs politiques gapless. Le mode qui conserve le format initial peut convertir les pistes suivantes. Celui qui conserve la sortie seulement pour des formats compatibles peut la rouvrir au changement. Une lecture NAS lente peut épuiser les tampons. GStreamer fournit une préparation de l'URI suivante via `about-to-finish`, mais cette fonction ne prouve pas une transition sans rupture pour chaque DAC. [TECH-102](sources-techniques.md#tech-102), [TECH-103](sources-techniques.md#tech-103)

MPD réutilise davantage de fonctions, dont index, file, partitions et sorties. Cette couverture devient un coût si kuro maintient les mêmes décisions ailleurs. Navidrome offre bibliothèque et accès clients, ainsi qu'un jukebox par mpv IPC. Son adoption exige un examen du modèle et du contrôle serveur, pas seulement une comparaison des lecteurs web. [TECH-101](sources-techniques.md#tech-101), [TECH-105](sources-techniques.md#tech-105)

Le volume partagé M1 est distinct du DSP audiophile M3. Proposition : utiliser le contrôle de volume système ou logiciel disponible et rapporter la méthode. Si le DAC n'a pas de mixer matériel, cela ne doit pas supprimer toute commande de volume. À défaut de contrôle disponible, l'interface indique une sortie à niveau fixe et son contrôle externe. Le choix exact et le niveau de reprise attendent le matériel et la revue utilisateur. Une conversion ou un gain logiciel ne sera pas présenté comme bit-perfect. [TECH-106](sources-techniques.md#tech-106)

Les formats candidats à soumettre pour M1 comprennent FLAC, WAV, AIFF, ALAC, MP3, AAC, Vorbis et Opus. Cette liste est une proposition de corpus, pas une liste de compatibilité kuro. Les conteneurs, délais d'encodage, fréquences et canaux doivent être précisés. DSD et MQA ne deviennent pas des conditions M1. Aucun sous-ensemble ne peut être retenu silencieusement s'il exclut les fichiers nécessaires à l'utilisateur.

## Licences des logiciels dès M1

L'examen porte sur les versions, options de compilation, liaisons, plugins et fichiers distribués. Un nom de projet ne suffit pas à déterminer les obligations du paquet final. La séparation en processus ne résout pas automatiquement toutes les questions de licence.

| Dépendance candidate | Fait documentaire | Conséquence proposée |
| --- | --- | --- |
| SQLite | Code dans le domaine public selon le projet. TECH-004 | Candidat favorable, dépendances d'intégration à inventorier séparément |
| mpv et libmpv | GPLv2 ou ultérieure par défaut. Une construction sans fichiers GPL exclusifs vise LGPLv2.1 ou ultérieure, avec réserves explicites du projet. TECH-104 | Examiner la construction réelle et ses dépendances avant adoption |
| MPD | GPLv2 ou ultérieure. TECH-101 | Étudier les obligations de distribution et les éventuelles modifications |
| GStreamer | Bibliothèques sous LGPL, plugins et dépendances à examiner. TECH-103 | Lister précisément les plugins nécessaires aux formats M1 |
| FFmpeg | LGPLv2.1 ou ultérieure par défaut, composants GPL facultatifs et combinaisons non redistribuables possibles. TECH-107 | Conserver une configuration de compilation redistribuable vérifiée |
| Navidrome | GPLv3 dans le dépôt consulté. TECH-105 | Évaluer le coût d'une adaptation et ses obligations de publication |
| Tauri | MIT ou Apache-2.0 pour le projet. TECH-108 | Examiner aussi WebKitGTK, plugins et bibliothèques embarquées |
| Qt | Options commerciales, LGPLv3 et GPL, variables selon les modules. TECH-109 | Vérifier les modules exacts, la distribution et les conditions LGPL |
| Electron | MIT pour le projet, licences tierces pour le paquet. TECH-110 | Inventorier Chromium, Node et autres contenus distribués |

La licence kuro reste O-01. MIT et Apache-2.0 constituent des options permissives à comparer. GPLv3 et AGPLv3 proposent un copyleft avec des portées différentes, notamment pour les interactions réseau. L'utilisateur choisit après examen des textes et des dépendances retenues. Aucun fichier LICENSE n'est créé. Les droits fournisseurs M5 n'exemptent pas d'examiner les logiciels nécessaires dès M1. [TECH-208](sources-techniques.md#tech-208)

## Fournisseurs et protocoles conditionnels

Le contrat proposé de chaque fournisseur comprend identifiant externe, provenance, date, licence ou conditions, attribution, quota, expiration, droit de cache et droit d'export. Une réponse de catalogue ne prouve ni disponibilité de lecture ni droit de télécharger le média. L'adaptateur doit pouvoir être désactivé sans empêcher la bibliothèque locale de fonctionner.

| Fournisseur ou accès | Possibilité documentée et limite | Disposition pour kuro |
| --- | --- | --- |
| Tags et images locaux | Lecture des fichiers fournis. Les droits de redistribution des images ne sont pas déduits de leur présence locale. | Tags nécessaires M1. Pochettes locales restent proposition P2, aucune publication de médias |
| MusicBrainz | API d'identités et relations. Core CC0 et données supplémentaires sous autre licence. API avec quota et conditions commerciales distinctes. TECH-201 | Premier enrichisseur à étudier, facultatif. Respecter licence par catégorie et éviter requête par affichage |
| Cover Art Archive | Accès aux images, copyrights tiers conservés. TECH-202 | Cache, attribution et export à examiner avant ajout |
| Discogs | Catalogue et données restreintes soumis à des règles différentes, dont images, fraîcheur et cache. TECH-203 | Ne pas traiter toute réponse comme CC0. Quota numérique non confirmé dans cette recherche |
| ListenBrainz | Dépôt d'écoutes et recommandations documentés. TECH-204 | Consentement explicite et rapprochement d'identités requis. M5 |
| OPRA | Code MIT, jeu de données CC BY-SA 4.0 selon licence du dépôt. TECH-205 | Profils audio M3 conditionnels à attribution et provenance, distincts d'une intégration streaming |
| TIDAL | Portail développeur et règles d'usage. Lecture intégrale et traitement audio soumis à conditions. TECH-206 | Accès kuro et architecture autorisée non acquis. Ne pas promettre lecture native ni DSP |
| Qobuz | Conditions API avec clés fournies par Qobuz et secret non partageable. TECH-209 | Admission et autorisation d'intégration à obtenir avant engagement |
| KKBOX | Documentation de catalogue avec credentials. TECH-210 | Onboarding courant et lecture native non démontrés |
| nugs | Intégration partenaire Roon documentée. TECH-211 | Aucune API publique réutilisable pour kuro établie |
| LyricFind et TiVo | Offres commerciales de paroles et métadonnées. TECH-212 | Contrat et budget inconnus. Ni biographie ni paroles promises |
| Roon API et RAAT | Extensions de contrôle liées à un serveur Roon. Aucun droit RAAT déduit. SRC-132 et SRC-123 | Pas une base ouverte pour le moteur kuro. Aucun accès requis M1 |
| Snapcast | Transport multiroom libre avec serveur, clients et synchronisation documentés. TECH-111 | Candidat M4 à comparer avant une synchronisation propre. Formats, dérive, sécurité et licence restent à vérifier sur les appareils retenus |
| Autres sorties réseau | Capacités Roon recensées, sans preuve d'API ou de droits kuro. D09 dans P2 | Examiner chaque protocole et appareil en M4. Pas de groupement universel promis |

Les éléments TIDAL proviennent aussi de la recherche en lecture seule, car l'ouverture de l'auteur renvoie une page sans texte exploitable. Les restrictions doivent être relues dans leur version courante avant toute décision. Les documents commerciaux ne valent pas approbation d'une application. [TECH-206](sources-techniques.md#tech-206)

## Études futures qui départagent les options

Ces études attendent une autorisation de développement distincte. P4 les transforme en validations rattachées aux fonctions. Les nombres ci-dessous sont des seuils proposés à discuter, sans modifier MVP-03 ou MVP-06.

| ID | Protocole proposé | Mesures et décision |
| --- | --- | --- |
| E-01 | Décrire OS, stockage local, NAS, réseau, DAC, formats et nombre réel de pistes. Construire ensuite un corpus autorisé de 20 000 albums et environ 3 To. | Matériel et volume vérifiables. Un petit corpus n'est qu'un essai préparatoire |
| E-02 | Comparer SQLite et FTS5 avec scans froids, incrémentaux, coupure et reprise NAS, recherche pendant lecture. | Temps d'import, débit, p50/p95 des requêtes, mémoire maximale, taille DB et WAL, erreurs. Proposition de recherche visible p95 sous 300 ms et première page sous 1 s, à approuver sur matériel fixé |
| E-03 | Lire les mêmes paires connues avec libmpv puis les alternatives nécessaires. Mesurer sortie, silence ajouté, échantillons manquants, doublons et conversions. Refaire avec changement de format et retard NAS. | Zéro silence ajouté sur le corpus gapless accepté. Une tolérance de mesure doit être définie, pas inventée comme résultat. Rejeter le moteur qui échoue aux formats indispensables |
| E-04 | Tuer service ou moteur entre mutation, accusé et événement. Rejouer commande, perdre événements et reconnecter. | Une occurrence de mutation, file cohérente, erreur explicite. Rétention et délais à fixer |
| E-05 | Sauvegarder pendant import et lecture, restaurer isolément, migrer un ancien schéma, déplacer une source et lire une piste. | Identités, références et valeurs comparées. Médias contrôlés avant/après. Échec de restauration bloque MVP-08 |
| E-06 | Comparer Tauri puis Qt ou Electron sur le même parcours avec listes à l'échelle cible. Tester lancement, clavier, focus, zoom, fermeture et reconnexion. | Temps de page, mémoire, CPU, fluidité et parcours. Seuil mémoire à proposer après E-01, aucun chiffre déduit de marketing |
| E-07 | Vérifier le paquet choisi sur environnement propre, accès limités, démarrage service et appels HTTP depuis origine étrangère si ce transport existe. | Permissions minimales utiles, mutations non autorisées refusées, désinstallation maîtrisée. Aucun réglage de la machine actuelle |
| E-08 | Pour chaque fournisseur retenu, examiner conditions actuelles, obtenir accès autorisé, tester quota, révocation, cache et attribution. | Accès et droits démontrés avant engagement fournisseur. M1 reste utilisable fournisseur désactivé |

## Décisions ouvertes et effet sur la suite

| Question | Responsable de décision | Proposition et preuve manquante | Blocage |
| --- | --- | --- | --- |
| O-01 Licence kuro | Utilisateur | Comparer modèles de licence après inventaire des dépendances | Adoption et distribution M1, pas la documentation |
| O-02 Formats et sortie | Utilisateur, avec preuves audio | Corpus E-01 et E-03, DAC et volume inconnus | Validation de MVP-05 et MVP-06 |
| O-03 Budgets de performance | Utilisateur, propositions techniques P4 | E-02 et E-06 sur matériel identifié | Acceptation M1 à 20 000 albums |
| O-04 NAS | Utilisateur pour environnement, futur responsable technique pour adaptateur | Montage existant préféré. E-01 et E-02 | MVP-02, aucune modification système autorisée aujourd'hui |
| O-05 Stack et forme | Futur responsable technique, revue utilisateur si périmètre affecté | Service local, SQLite, libmpv et Tauri en tête. Alternatives selon E-02, E-03, E-06 et E-07 | Adoption technique M1 |
| O-06 État et sauvegarde | Utilisateur sur comportement, futur responsable technique sur mécanisme | C-06, arrêt sonore après redémarrage proposé, E-04 et E-05 | MVP-07 et MVP-08 |
| O-07 Fournisseurs | Utilisateur pour besoin, fournisseur pour accès | E-08 et conditions par adaptateur | M5 conditionnel, pas M1 |
| O-08 Contrats réseau et appareils | Futur responsable technique, utilisateur pour appareils | C-09, capacités et horloges à mesurer | M4 et M7, pas accès NAS M1 |
| O-09 Versions et paquet Linux | Futur responsable technique, utilisateur pour environnement | Versions exactes et empreintes des artefacts après essais, E-07 | Distribution reproductible M1 |

P3 fournit des recommandations assez précises pour planifier les preuves. Elle ne ferme aucune question par une mesure fictive. La prochaine phase produit les six plans de domaine et les sept milestones à partir de ces contrats et études.
