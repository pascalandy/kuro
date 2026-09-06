# Inventaire fonctionnel Roon et dispositions pour kuro

Le [registre canonique](inventaire-fonctions.tsv) contient 195 entrées dans les quinze familles demandées. Il s’appuie sur [84 sources primaires externes](sources.md) et une référence interne au cadrage. Ce nombre comprend des capacités Roon, des exigences propres à kuro et des questions non résolues. Il ne mesure ni la parité, ni l’avancement d’un logiciel.

Roon n’a pas été exécuté. La version et le build de référence sont inconnus. Les sources ont été ouvertes le 2026-09-06 par l’auteur P2 et deux chercheurs indépendants en lecture seule. Aucun comportement applicatif n’a été testé.

## Méthode et frontière de preuve

Une entrée distingue une action ou un résultat que l’on peut vérifier séparément. Les variantes proches restent regroupées lorsque le même parcours les couvre. Les commandes de transport forment ainsi une entrée, tandis qu’une sauvegarde et une restauration en forment deux. Les identifiants `F01-001` à `F15-003` sont stables. Les suffixes ne doivent pas être réattribués lorsqu’une entrée est retirée.

La couverture est bornée au corpus répertorié. Les listes anciennes de navigateurs et traitements ont été complétées par les pages Smart Playlists, Listen Later, Daily Picks, OPRA, nugs et Folder Browser. Les contradictions restent visibles. Le relevé ne prouve pas que toutes les fonctions de toutes les versions ont été découvertes.

Le champ `comportement_reference` décrit seulement le fait documentaire ou le manque indiqué par `statut_preuve`. Les champs `responsable_kuro`, `disposition`, `milestone` et `validation_future` sont des propositions de traduction pour kuro. Une source Roon ne prouve jamais ces propositions. La validation future décrit un résultat à observer, sans annoncer que ce test existe ou réussit.

Les textes de sources sont paraphrasés. Les dates de consultation ne remplacent pas les dates de publication manquantes. Un build cité dans un article, notamment le build 1625 pour l’analyse programmée, n’est pas un build observé.

## Lire le TSV

Le fichier est UTF-8, avec une ligne par entrée et douze colonnes. Les listes de sources utilisent le point-virgule. Aucun champ ne contient de tabulation ou saut de ligne interne.

| Colonne | Sens |
| --- | --- |
| `id` | Identifiant stable de fonction ou exigence |
| `domaine` | Famille D01 à D15, définie ci-dessous |
| `fonction` | Action ou résultat inventorié |
| `comportement_reference` | Résumé court, à lire avec son statut |
| `statut_preuve` | Nature de la preuve, jamais résultat d’un test |
| `date_preuve` | Date de consultation documentaire |
| `sources` | Identifiants SRC du registre ou INT-P1 pour le cadrage |
| `portee_reference` | Composants de référence concernés ou portée propre à kuro |
| `responsable_kuro` | Propriétaire fonctionnel proposé, sans choix de module technique |
| `disposition` | Traitement provisoire pour kuro |
| `milestone` | Premier examen ou livraison envisagé, selon la disposition |
| `validation_future` | Scénario observable à préciser avant exécution |

Les statuts de preuve sont les suivants.

| Valeur | Interprétation |
| --- | --- |
| `documente` | Une source primaire décrit le comportement. Application non observée. |
| `historique` | Le texte décrit une fonction, mais ses services ou générations sont anciens. |
| `contradictoire` | Des affirmations du corpus divergent. Aucune résolution produit n’est inventée. |
| `a_observer` | Le corpus ne suffit pas à établir le comportement ou son contrat. |
| `exigence_kuro` | Contrainte confirmée dans le cadrage, sans attribution à Roon. |
| `proposition_kuro` | Précision proposée, à examiner avant engagement. |

Les dispositions séparent l’inventaire de la décision produit.

| Valeur | Interprétation |
| --- | --- |
| `socle` | Contribution proposée à un critère M1 déjà approuvé. Les détails restent à arbitrer. |
| `retenu_provisoire` | Capacité à instruire dans une milestone ultérieure, sans parité promise. |
| `conditionnel` | Accès, droits, matériel ou faisabilité à établir avant engagement. |
| `proposition` | Examen proposé. Le numéro M ne transforme pas cette entrée en exigence obligatoire. |
| `reporte` | Frontière future M7, sans conception mobile détaillée en P2. |

Les responsables normalisés sont `serveur_bibliotheque`, `serveur_lecture`, `sortie_audio`, `desktop`, `coordination_reseau`, `integrations`, `exploitation`, `projet` et `mobile`. Ils indiquent qui doit porter le résultat dans la conception future. Ils n’imposent ni processus séparés, ni langage, ni bibliothèque logicielle.

Les portées normalisées sont `serveur_desktop`, `serveur_sortie`, `serveur_controle_sortie`, `kuro` et `mobile_futur`. Un serveur de bibliothèque peut posséder l’état affiché par le desktop. Cette affectation n’exclut pas leur collaboration.

## Couverture des familles demandées

Le coordinateur a corrigé son décompte initial de quatorze familles. La liste transmise en comprend quinze avec le mobile futur. Cette correction de comptage ne modifie pas le périmètre.

| Famille | Code | Entrées | Couverture et limite principale |
| --- | --- | --- | --- |
| Installation et démarrage | D01 | 8 | Rôles, service, connexion, versions, mise à jour et migration. Le desktop Linux est la cible kuro. |
| Import et stockage | D02 | 18 | Local, NAS, surveillance, exclusions, tags, formats, playlists importées et analyse. Protocole NAS utilisateur inconnu. |
| Identité musicale | D03 | 24 | Copies, éditions, corrections, crédits, classique, genres, illustrations et livrets. Fournisseurs non réutilisables par défaut. |
| Consultation et recherche | D04 | 15 | Albums, artistes, pistes, recherche, tri, Focus, sélection, dossiers et pochettes. Aucune latence mesurée. |
| Organisation personnelle | D05 | 23 | Playlists, profils, historique, tags, bookmarks, Smart Playlists, bans et exports. Profils distincts d’une isolation de sécurité. |
| Lecture | D06 | 14 | Transport, file, shuffle, répétition, réutilisation et crossfade. Gapless local à prouver sur formats retenus. |
| Audio | D07 | 13 | Sorties, volume, exclusif, DSD, multicanal, adaptation, signal path et MQA historique. Capacités matérielles inconnues. |
| Traitements audio | D08 | 18 | Analyse, normalisation, ReplayGain, chaîne DSP, égalisation, convolution, casque et enceintes. Aucune mesure audio. |
| Réseau et appareils | D09 | 15 | Contrôles, zones, transfert, synchronisation, Bridge, protocoles, commandes et displays. Compatibilité conditionnelle par technologie. |
| Découverte et contenus | D10 | 10 | Biographies, relations, paroles, Discover, Daily Picks, Listen Later et Radio. Accès aux données conditionnel. |
| Intégrations | D11 | 12 | TIDAL, Qobuz, KKBOX, nugs, playlists, radio, scrobbling, extensions et partage. Plusieurs textes divergent. |
| Fiabilité et expérience desktop | D12 | 13 | Sauvegarde, restauration, logs, clavier, lecture courante, persistance, volume cible et incidents. Accessibilité à examiner. |
| Autonomie et sécurité | D13 | 5 | Exigences kuro hors Internet, sources intactes, NAS absent; propositions sur secrets et accès réseau. |
| Open source | D14 | 4 | Licence ouverte, construction, droits des fournisseurs et licences des dépendances. Aucune licence choisie. |
| Mobile futur | D15 | 3 | ARC distant, téléchargements locaux et Smart Downloads. Frontière M7 uniquement. |

La précision supplémentaire sur les licences distingue les dépendances nécessaires dès M1 des fournisseurs de données envisagés en M5. Les pochettes locales sont une proposition de présentation M1. Leur édition avancée relève de M2 et l’enrichissement externe de M5.

## Points de référence qui changent la lecture de l’inventaire

Le serveur tient la bibliothèque et les files, tandis que les contrôles affichent et modifient cet état. Les sorties produisent l’audio. Cette séparation fonctionnelle n’oblige pas kuro à répartir ces rôles sur plusieurs machines en M1. [SRC-001](sources.md#src-001)

L’identité musicale ne se réduit pas au titre d’un album. Deux copies locales peuvent garder des identités distinctes, puis appartenir à un ensemble de versions. Une œuvre peut relier plusieurs interprétations, elles-mêmes liées à des pistes. Le socle M1 demande des références stables. Le modèle classique et les regroupements avancés restent en M2. [SRC-002](sources.md#src-002), [SRC-212](sources.md#src-212)

Les playlists manuelles, bookmarks de vues, Smart Playlists et Listen Later sont quatre fonctions distinctes. Les deux dernières ont leurs propres articles récents. Un ancien tutoriel proposant une playlist d’attente ne décrit pas Listen Later. [SRC-204](sources.md#src-204), [SRC-205](sources.md#src-205), [SRC-222](sources.md#src-222), [SRC-235](sources.md#src-235)

Daily Picks renouvelle une sélection quotidienne par profil. Le corpus exige un service de streaming connecté et un historique suffisant. Le rafraîchissement manuel de Discover est une autre action. Aucune recommandation Daily Picks locale seule n’est établie. [SRC-220](sources.md#src-220), [SRC-221](sources.md#src-221)

La sauvegarde Roon porte sur sa base et ses réglages, sans dupliquer les médias. La restauration remplace une base existante. La future preuve kuro doit comparer les données restaurées et une lecture réelle en isolation. Elle ne doit pas annoncer une sauvegarde des 3 To de fichiers. [SRC-013](sources.md#src-013), [SRC-014](sources.md#src-014)

## Contradictions et réserves du corpus

| Sujet | Constat sourcé | Traitement P2 |
| --- | --- | --- |
| Synchronisation des playlists | [SRC-015](sources.md#src-015) interdit le retour vers TIDAL. [SRC-206](sources.md#src-206) décrit 2-Way Playlist Sync tout en conservant un ancien texte non éditable. | F11-006 contradictoire. Tester chaque fournisseur et génération avant engagement M5. |
| Playlists nugs | [SRC-206](sources.md#src-206) cite nugs pour le matching et les transferts. [SRC-136](sources.md#src-136) décrit des restrictions de playlists et conserve aussi une référence My nugs playlists. | F11-007 contradictoire. Ne pas promettre synchronisation ou ajout aux playlists Roon. |
| Recherche et contenus nugs | La recherche instantanée omet les shows, présents dans la recherche complète. Métadonnées non éditables; bibliothèque, Radio, vidéo et live streams limités. [SRC-136](sources.md#src-136) | F11-004 garde les restrictions. Les concerts ne sont pas assimilés aux albums des autres services. |
| Édition des crédits | Le texte Roon 1.1 de [SRC-004](sources.md#src-004) annonce une fonction future; [SRC-002](sources.md#src-002) décrit des données éditées. | F03-017 contradictoire. Observer l’éditeur actuel avant de fixer les champs. |
| MQA | [SRC-114](sources.md#src-114) annonce encore du support futur; [SRC-137](sources.md#src-137) décrit un décodeur et cite TIDAL Masters. | F07-013 contradictoire et conditionnelle. Aucune disponibilité actuelle TIDAL déduite. |
| Versions choisies par Radio | [SRC-223](sources.md#src-223) décrit un choix non configurable; [SRC-233](sources.md#src-233) documente des préférences de contenus. | F11-005 contradictoire. Comparer Radio et choix hors bibliothèque sur une version identifiée. |
| Installation Linux | [SRC-133](sources.md#src-133) et [SRC-135](sources.md#src-135) présentent Docker; [SRC-134](sources.md#src-134) conserve un installateur natif. | Coexistence possible, pas contradiction prouvée. Support actuel à confirmer; aucune installation effectuée. |
| Groupes de zones | [SRC-125](sources.md#src-125) a une liste plus courte que [SRC-124](sources.md#src-124). Chromecast délègue le groupe à Google Home. | Support et groupement sont deux capacités distinctes. Aucun groupe interprotocoles promis. |
| DSP et OPRA | La liste générale MUSE omet OPRA, décrit dans un article de 2025. [SRC-112](sources.md#src-112), [SRC-121](sources.md#src-121) | F08-016 distincte des profils Audeze. Aucun accès à une API AutoEQ déduit. |
| Partage social | [SRC-020](sources.md#src-020) cite Twitter et Imgur. | F11-012 historique. Vérifier les destinations et interfaces réellement disponibles. |

## Lacunes et exclusions explicites

Les cas de panne ne sont pas validés par une description heureuse d’import ou de lecture. Les délais de détection NAS, permissions retirées, fichiers partiellement copiés, chemins modifiés et concurrence de rescans restent à définir. Pour kuro, un NAS absent ne doit jamais être traité comme une demande de suppression. Cette exigence vient du cadrage, pas d’une généralisation de Roon.

Le corpus distingue nettoyage de base et rescan. Il décrit aussi une commande qui supprime physiquement les médias. Cette commande destructive n’est pas retenue pour le socle kuro, dont les sources doivent rester intactes. Une éventuelle proposition future exige une décision de périmètre distincte. [SRC-104](sources.md#src-104), [SRC-004](sources.md#src-004)

Le gapless local reste une preuve à obtenir. La page Chromecast annonce le gapless sur cette technologie, ce qui ne démontre pas chaque format sur un DAC local. Les formats utilisateur, leur résolution, le nombre de pistes et le matériel sont inconnus. Ni le signal path affiché, ni une mention bit-perfect ne remplacent une mesure. Certains traitements matériels échappent à cet affichage. [SRC-126](sources.md#src-126), [SRC-110](sources.md#src-110)

L’objectif de synchronisation RAAT inférieur ou égal à une milliseconde est annoncé par Roon, sans mesure dans ce travail. La documentation publique de l’API d’extensions ne donne pas à kuro un accès RAAT ni un contrat d’import arbitraire. Ces capacités restent conditionnelles. [SRC-123](sources.md#src-123), [SRC-132](sources.md#src-132)

Le clavier Windows et macOS est documenté. Le contrôle natif Linux, les touches média Linux, le lecteur d’écran, le contraste, le zoom et une navigation clavier complète ne sont pas établis pour Roon par ce corpus. Linux sur Omarchy est la cible confirmée de kuro. Les détails d’intégration et d’accessibilité restent des propositions visibles, sans ajout silencieux de critère MVP. [SRC-011](sources.md#src-011), [contexte utilisateur](contexte-utilisateur.md)

L’autonomie hors Internet de kuro ne découle pas d’ARC. ARC télécharge certains médias locaux pour le mobile; il ne prouve pas l’autonomie du serveur et du desktop. La recherche locale M1, l’absence de dépendance obligatoire aux fournisseurs et la conservation des fichiers restent des exigences kuro distinctes. [SRC-231](sources.md#src-231), [produit et MVP](produit-et-mvp.md)

Nucleus, ROCK et l’administration RoonOS donnent un contexte de déploiement. Leurs opérations système, formatage et matériel dédié ne constituent pas un objectif de clone matériel kuro. Le corpus ne détaille pas tous leurs écrans. [SRC-023](sources.md#src-023)

Les fournisseurs de biographies, pochettes, paroles, concerts et streaming ont leurs propres conditions. Une capacité utilisateur Roon n’établit ni une API publique équivalente, ni une licence réutilisable. La licence du projet reste ouverte. L’examen des dépendances M1 doit précéder leur adoption; les droits des contenus externes sont à examiner pour M5.

## Passage vers P3

P3 doit examiner les responsables fonctionnels, préciser les contrats et comparer les options. P2 ne choisit aucune stack et ne crée aucun plan P4. Les affectations conservent M1 local et NAS à 20 000 albums et environ 3 To; M2 bibliothèque avancée; M3 audio; M4 distribution; M5 intégrations conditionnelles; M6 autres desktops et approfondissement; M7 mobile.

La [passation P2](passations/p2-inventaire.md) donne les vérifications et la revue manager. La [checklist](checklist.md) consigne le passage P2 validé.
