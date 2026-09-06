# Architecture proposée pour kuro

P3 recommande un service local autonome, un desktop de contrôle et un moteur audio réutilisé. Les trois rôles cohabitent sur la machine Linux en M1. Un seul dépôt contient leurs modules. Cette forme conserve la lecture lorsque la fenêtre se ferme et prépare des contrôleurs futurs sans distribuer la bibliothèque dès le MVP.

Il s'agit d'une recommandation de conception, pas d'un choix approuvé ni d'une faisabilité démontrée. Les contrats ci-dessous sont adoptables comme base documentaire après revue. Les moteurs, langages et outils restent conditionnés aux études de [faisabilité](faisabilite.md). Aucun code, signature implémentée ou prototype n'accompagne ce document.

Les [critères MVP-01 à MVP-10](produit-et-mvp.md) restent inchangés. La cible est de 20 000 albums et environ 3 To, avec médias locaux et NAS dès M1. Le nombre de pistes reste inconnu. Les 195 entrées de [P2](inventaire-fonctions.tsv) ne sont pas 195 engagements M1. Les flux décrivent kuro proposé, sans prétendre révéler les mécanismes internes de Roon.

## Trois formes complètes comparées

| Forme | Bibliothèque, contrôle et lecture | Apport pour M1 | Coût et condition de choix |
| --- | --- | --- | --- |
| A. Desktop avec moteur embarqué | Un processus possède base, file et moteur. La fenêtre appelle les modules en mémoire. | Installation et débogage initiaux concentrés. Aucun transport de contrôle nécessaire. | Fermer ou crasher le desktop affecte la lecture. Extraire ensuite un service impose de revoir le cycle de vie. Alternative si la continuité hors fenêtre n'est pas retenue et si le service compromet le packaging. |
| B. Service local autonome, recommandée | Le service possède bibliothèque et file. Le desktop demande des opérations. Un adaptateur délègue le décodage et la sortie à un moteur, embarqué dans le service ou enfant supervisé. | Fenêtre remplaçable, reprise du contrôle et état persistant commun. Médias NAS lus par le service local. | Gestion du démarrage, reconnexion et compatibilité de versions nécessaire dès M1. À tester avant adoption de la stack. |
| C. Serveur existant adapté | MPD peut posséder index de fichiers, file et sorties. Navidrome peut posséder bibliothèque, playlists et accès clients, avec lecture serveur via son jukebox mpv. Le desktop kuro devient client ou adaptation de ce serveur. | Réutilise une chaîne fonctionnelle plus large et réduit le travail initial. | Accepter le modèle amont ou maintenir une adaptation. Ajouter une seconde bibliothèque et une seconde file créerait des conflits. Comparer les identités, éditions et sauvegardes avant de choisir cette forme. |

Les capacités MPD et Navidrome sont documentées, mais leur adéquation au modèle kuro et au corpus utilisateur n'est pas mesurée. Navidrome n'est pas écarté sous prétexte d'absence de sortie serveur. Son jukebox existe, avec une interface de commande distincte de sa Web UI. [TECH-101](sources-techniques.md#tech-101), [TECH-105](sources-techniques.md#tech-105)

B est proposée parce que l'état appartient à un service et que les évolutions M2 et M4 concernent cet état. A reste un repli si l'exploitation de B coûte trop pour M1, après examen du comportement hors fenêtre proposé par F01-002. C devient préférable si les essais montrent que son modèle satisfait les contrats sans double autorité ni adaptation profonde. Un échec de gapless de libmpv conduit d'abord à comparer MPD ou GStreamer, pas à réécrire tout le produit.

Une forme distribuée, avec serveur sur une autre machine et endpoints audio, appartient à M4. Elle ajoute transport audio, horloges, pertes réseau et appairage. Elle n'est pas nécessaire pour lire un montage NAS en M1. Aucun microservice de recherche, de pochette ou de métadonnées n'est proposé.

## Un monorepo modulaire avant plusieurs dépôts

Le monorepo proposé regroupe documentation, domaine musical, service, adaptateurs et desktop. Les frontières sont des responsabilités, pas des répertoires créés aujourd'hui. Une évolution du contrat et ses consommateurs peuvent être revus ensemble. Une seule politique de version accompagne le premier produit.

Le multirepo sépare publications, permissions et calendriers. Il demande aussi des versions de contrats, des tests de compatibilité et des mises à jour coordonnées. Il devient pertinent lorsqu'un endpoint ou client possède réellement un cycle de livraison indépendant. Aucun besoin confirmé M1 ne justifie ce coût. La distribution en processus et la répartition des dépôts restent deux décisions distinctes.

## Composants et autorité

| Composant proposé | État possédé et responsabilité | Frontière |
| --- | --- | --- |
| Domaine musical | Identités, relations, règles de priorité des métadonnées et références des playlists | Indépendant de l'interface, du moteur et des fournisseurs |
| Service de bibliothèque | Sources, catalogue, recherche, corrections et travaux d'import | Seul écrivain logique des données persistantes |
| Coordinateur de lecture | File canonique, ordre des commandes, session et intention de lecture | Seul décideur des transitions de file |
| Adaptateur audio | Traduction des commandes et observation du moteur | Rapporte l'état réel. Il ne décide pas d'une autre file métier |
| Moteur et sortie locale | Décodage, tampons, ouverture du périphérique et émission audio | État matériel observé, distinct de l'intention du coordinateur |
| Desktop | Navigation, sélection et cache d'affichage | Aucune écriture directe dans la base ou commande directe au moteur |
| Adaptateurs de sources et fournisseurs | Lecture des fichiers ou réponses externes, normalisation et provenance | Aucun fournisseur obligatoire en M1. Aucun secret dans le domaine musical |
| Exploitation du service | Démarrage, arrêt, migrations, sauvegardes et journaux | Un seul service actif par bibliothèque |

Le service de bibliothèque et le coordinateur peuvent être des modules d'un même processus. Leur séparation logique évite de faire dépendre une transition audio d'une transaction d'import longue. La base, l'index et le cache résident sur stockage local. SQLite avec FTS5 est le premier candidat, pas une promesse de performance. WAL requiert des accès sur le même hôte et ne fonctionne pas sur un système de fichiers réseau. [TECH-001](sources-techniques.md#tech-001), [TECH-002](sources-techniques.md#tech-002)

## Identités musicales et fichiers

Ces structures décrivent les concepts utiles, sans imposer de schéma SQL ou de types de langage.

| Concept | Identité et relations proposées | Portée |
| --- | --- | --- |
| Source | Identifiant durable, type local ou montage, emplacement courant, état d'accès, génération de scan | M1 |
| Fichier média | Identifiant interne durable, source, chemin relatif, observations de taille et date, signature de contenu facultative | M1. L'identité ne se réduit ni au chemin ni au titre |
| Piste de bibliothèque | Référence musicale jouable liée à un fichier. Durée, ordre de disque et de piste, tags bruts conservés | M1 |
| Album et artiste | Identifiants locaux, noms affichés, relations ordonnées aux pistes et artistes | M1. Aucun rapprochement irréversible par nom seul |
| Édition | Publication précise d'un album, avec copies et versions distinctes | Référence minimale compatible en M1, regroupement et édition avancés en M2 |
| Œuvre et interprétation | Œuvre abstraite, interprétation enregistrée, liens vers une ou plusieurs pistes et mouvements | M2. Une piste n'est pas automatiquement une œuvre |
| Crédit | Entité créditée, rôle, cible et provenance | M2. Homonymes et rôles multiples conservés |
| Valeur de métadonnée | Champ, valeur brute et normalisée, origine, date de collecte, identifiant externe éventuel | Tags locaux en M1. Fournisseurs facultatifs ultérieurs |
| Correction utilisateur | Valeur choisie et portée, distinctes des observations de scan ou fournisseur | Contrat préparé, édition avancée M2 |
| Playlist et entrée de file | Identifiant de liste et identifiant de chaque occurrence, référence à une piste | M1. Deux occurrences d'une même piste restent distinctes |

Un déplacement confirmé modifie l'emplacement du fichier sans remplacer son identifiant. Un chemin réutilisé pour un autre contenu ne suffit pas à prouver cette continuité. Les informations de système de fichiers et signatures aident au rapprochement, mais les collisions ou copies ambiguës restent explicites. Un calcul intégral de signatures sur 3 To n'est pas imposé à chaque scan.

La relocalisation d'une source NAS conserve son identifiant après association explicite au nouvel emplacement. Un répertoire local vide sous un montage absent n'est pas une nouvelle bibliothèque vide. Les playlists gardent leurs références quand un fichier devient indisponible.

Le service conserve les observations brutes et une valeur effective calculée. Proposition de priorité pour les champs éditables futurs : correction utilisateur, préférence explicite de source, puis valeur importée. Un nouvel import ne détruit pas une correction. L'identification externe reste un lien avec provenance, jamais un remplacement de tous les identifiants locaux. Cette séparation prépare M2 sans rendre l'enrichissement Internet nécessaire à M1.

## Contrats documentaires

Les identifiants C-01 à C-09 servent aux plans P4. Tous sont des propositions à éprouver avant développement autorisé.

### C-01. Import et disponibilité des sources

Une demande de scan identifie la source et une génération de travail. Les observations se valident par lots courts et reprenables. Rejouer le même lot ne crée pas de doublons. Un scan incomplet ne conclut pas qu'un fichier a été supprimé.

L'état distingue source inaccessible, accès refusé, fichier absent sur source vérifiée, fichier invalide et fichier disponible. Le nettoyage de références reste explicite. Les notifications accélèrent le scan, sans en constituer la preuve complète. Un débordement, une interruption ou un retour du NAS déclenche une réconciliation. inotify peut perdre des événements et ne couvre pas les changements distants d'un système de fichiers réseau. [TECH-005](sources-techniques.md#tech-005)

### C-02. Catalogue et recherche

Les écritures métier et la révision du catalogue partagent une transaction. L'index de recherche est soit mis à jour dans cette transaction, soit associé à une révision publiée avec son retard visible. Un index endommagé se reconstruit depuis le catalogue.

Une requête indique filtres, tri et curseur. La réponse contient des identifiants et une page bornée, avec ordre stable et identifiant comme départage. Une révision évite de mélanger silencieusement plusieurs états entre pages. L'interface virtualise les listes et ne charge pas les 20 000 pochettes en mémoire. La recherche sans accents est un comportement à tester, pas une propriété supposée de toutes les collations. [TECH-002](sources-techniques.md#tech-002)

### C-03. Commandes, événements et reconnexion

L'API conceptuelle distingue requêtes de lecture, commandes de mutation et événements. Chaque connexion annonce version de contrat et capacités. Une incompatibilité empêche les mutations avec un diagnostic exploitable. Aucun choix de HTTP, WebSocket, RPC ou format de sérialisation n'est figé.

M1 peut réaliser ce contrat avec un canal local, des révisions et un instantané à la reconnexion. Aucun broker, journal complet d’événements métier ou consensus distribué n’est requis. Les identités de contrôleurs et capacités préparent M4 sans ouvrir le LAN en M1.

Une mutation porte identifiant de commande, identité du contrôleur et révision attendue de l'objet. Le service accepte une fois la mutation et conserve son résultat avec une durée de rétention à définir. Une répétition identique renvoie ce résultat. Le même identifiant avec un autre contenu est refusé. Après expiration, le client relit l'état avant de réessayer. Une révision périmée produit un conflit explicite, sans écrasement silencieux d'une playlist.

Les événements comportent session serveur et séquence. Après perte d'événements ou reconnexion trop ancienne, le desktop relit un instantané et reprend depuis sa séquence. Les événements ne remplacent pas l'état canonique. L'accusé de réception d'une commande de lecture signifie acceptation, pas émission effective de son.

### C-04. File et moteur audio

Le coordinateur conserve une seule file avec identifiants d'occurrences et révision. Le moteur reçoit une projection de la piste courante et de la préparation suivante. Un adaptateur utilisant la playlist du moteur doit en interdire la modification par un second contrôleur, puis vérifier sa concordance.

Une transition porte un identifiant de session et de piste. Un événement tardif de l'ancienne piste ne peut pas avancer la nouvelle file. Le coordinateur distingue intention, chargement, lecture observée, pause, fin et erreur. Une source perdue produit une erreur visible. La politique proposée arrête cette tentative sans boucle de relance infinie. Le passage automatique à la suivante reste à arbitrer dans les validations P4.

### C-05. Format, gapless et vérité de la sortie

L'adaptateur distingue format du fichier, format décodé, transformations, format demandé à la sortie et format effectivement rapporté. Une information inconnue reste inconnue. Une sortie partagée ne permet pas d'affirmer une transmission bit-perfect au DAC sans preuve.

Le moteur prépare la piste suivante avant la fin courante. Le test de gapless examine les frontières du corpus retenu, les délais du NAS et les changements de paramètres. Conserver un flux à format fixe peut impliquer un rééchantillonnage. Rouvrir une sortie à chaque changement peut créer une interruption. mpv documente ce compromis. [TECH-102](sources-techniques.md#tech-102)

Le gapless M1 n'implique ni fondu enchaîné ni DSP. Le contrat recueille les transformations utiles au futur signal path, dont l'affichage détaillé appartient à M3. Exclusif, DSD, convolution et synchronisation de DAC restent hors promesse M1.

### C-06. Persistance, sauvegarde et restauration

Proposition d'état M1 durable : sources et leurs identifiants, catalogue, playlists et ordre, file et ordre, préférences de sortie et réglages utilisateur. La position de lecture est un point de reprise périodique proposé. Après redémarrage du service, la file revient à l'arrêt sans reprise sonore automatique. Une fenêtre fermée ne commande pas à elle seule l'arrêt du service. Ces précisions doivent être examinées avec U-07.

Une sauvegarde contient un instantané cohérent de la base, version du schéma, version du format de sauvegarde, identité de bibliothèque et manifeste d'intégrité. Les illustrations non reconstructibles, si cette proposition est retenue, sont incluses avec leurs droits. Index et caches reconstructibles sont exclus. Les médias, donc les 3 To, ne sont pas copiés par cette sauvegarde. Les secrets ne sont pas exportés en clair.

L'API de sauvegarde SQLite est un candidat pour copier une base active. Copier seulement son fichier principal pendant une activité WAL n'est pas le contrat. Durabilité, checkpoints et panne d'alimentation exigent une politique explicite et des essais. [TECH-001](sources-techniques.md#tech-001), [TECH-003](sources-techniques.md#tech-003)

La restauration se prépare dans un emplacement isolé, vérifie intégrité et compatibilité, puis migre vers un schéma supporté. Une version trop récente est refusée. L'ancienne base reste récupérable jusqu'à validation. Identifiants et références sont comparés après restauration. Les sources déplacées sont réassociées avant lecture. La preuve inclut une piste lue sur une source disponible, pas seulement une archive ouvrable.

### C-07. Sécurité et accès

M1 propose un accès local uniquement, sans port exposé au LAN par défaut. Un canal local restreint au compte utilisateur est préféré. Si le desktop utilise un service HTTP local, une page web étrangère peut tenter de l'appeler. Il faut alors authentification, vérification d'origine et protection CSRF pour les mutations, selon le transport retenu. localhost seul ne constitue pas une autorisation.

Le service limite les lectures aux sources autorisées, contrôle liens symboliques et sorties de racine, et traite tags et illustrations comme données non fiables. Aucun import ou enrichissement n'écrit dans les médias. Les journaux évitent secrets, jetons et chemins privés complets par défaut.

L'ouverture LAN future exige appairage explicite, permissions par contrôleur, révocation et transport protégé. Un profil musical n'est pas une permission d'accès. Les secrets fournisseurs passent par le coffre système quand celui-ci est disponible, sinon le fournisseur reste désactivé jusqu'au choix d'un stockage sûr. Le desktop n'accède pas directement aux jetons.

### C-08. Travail de fond et budget de ressources

Le service borne les travaux concurrents, leur file d'attente et leurs tampons. La lecture et sa préparation ont priorité sur les scans, l'analyse audio et les pochettes. Les accès NAS ont délai, annulation et reprise. Une tâche bloquée ne bloque pas le coordinateur audio.

Les illustrations ont tailles dérivées, quota et éviction. Les pages visibles déclenchent les chargements utiles. L'enrichissement externe accepte quotas et indisponibilité sans retarder recherche ou lecture locale. Les valeurs de budgets restent à proposer et mesurer sur matériel identifié.

### C-09. Contrôle et transport audio futurs

L'API de contrôle transporte des identités, commandes et états. Le transport audio transporte des octets ou échantillons avec format et temps. Un événement de contrôle ne fournit pas une horloge audio synchronisée.

M4 pourra attribuer une session à chaque zone, négocier les capacités d'endpoint et ajouter tampon, horloge et correction de dérive. Les zones indépendantes précèdent leur synchronisation. Le mobile M7 pourra utiliser les mêmes identités et versions de contrat. Téléchargement, quotas et écoute mobile hors ligne exigent un contrat supplémentaire, non implémenté ni détaillé ici.

## Flux proposés et liens vers P2

| Parcours | Flux et résultat à vérifier | Références |
| --- | --- | --- |
| Ajouter une source puis la perdre | Desktop → commande → service → scan par lots → catalogue → page. Une coupure NAS change la disponibilité, conserve les références, puis un retour déclenche réconciliation. | U-01, U-09; F02-001, F02-002, F02-004, F13-003; C-01 |
| Rechercher dans la bibliothèque cible | Desktop → requête paginée → index local → identifiants du catalogue → page. Aucune requête fournisseur nécessaire. | U-02, U-03, U-10; F04-001, F04-002, F04-004, F12-009; C-02, C-08 |
| Lire et réordonner | Commande avec révision → coordinateur → file canonique → moteur → sortie. Un changement utilisateur invalide une préparation suivante devenue périmée. | U-04, U-06; F06-003, F06-004, F06-013, F07-001; C-03 à C-05 |
| Sauver une playlist et reconnecter | Mutation transactionnelle → accusé durable → événement. Au retour du desktop, lecture de l'instantané et vérification de la révision. | U-05, U-07; F05-001, F05-002, F12-008; C-03, C-06 |
| Restaurer puis retrouver une piste | Instantané vérifié → schéma compatible → identités conservées → réassociation des sources → lecture. Les médias restent intacts. | U-08; F12-001, F12-003, F13-002; C-06, C-07 |

Le domaine musical absorbe D02 et D03. Le service et le desktop se partagent D04 et D05. Lecture et sortie couvrent D06 à D08. C-09 prépare D09 et D15. Les adaptateurs facultatifs portent D10 et D11. L'exploitation couvre D01 et D12 à D14. Cette correspondance donne un propriétaire conceptuel aux quinze familles. La couverture de chaque fonction, les six plans et leurs validations relèvent de P4 puis P5.
