# Glossaire de kuro

Ce glossaire fixe les termes propres au cadrage de la bibliothèque musicale kuro.

## Language

**KuroKor**:
Le rôle logique central de kuro qui détient l'état de Kuro et coordonne la lecture.
_Avoid_: Kuro Core, serveur audio

**Kuro Client**:
Le rôle logique de contrôle qui transmet les intentions de l'utilisateur à KuroKor et présente l'état reçu. Son hôte peut aussi fournir la lecture locale, sans imposer une application ou un processus distinct.
_Avoid_: KuroClient, renderer, point de lecture

**Rôle logique**:
Une responsabilité de kuro qui peut partager un hôte physique avec d'autres rôles ou vivre sur un hôte distinct.
_Avoid_: Machine, processus

**Hôte physique**:
Un ordinateur qui exécute un ou plusieurs rôles logiques de kuro. Le nombre d'hôtes ne détermine pas à lui seul l'emplacement de la sortie audio.
_Avoid_: Rôle, composant

**Déploiement**:
L'affectation des rôles logiques de kuro à des hôtes physiques et à leurs connexions de contrôle et de média.
_Avoid_: Architecture produit

**État de Kuro**:
L'ensemble sur lequel kuro fait autorité, dont le catalogue, les playlists, la file et les données durables. Son emplacement physique reste indéterminé.
_Avoid_: Contenu du NAS, médias

**Catalogue**:
L'ensemble durable des références de catalogue et des métadonnées connues de kuro. Certaines données du catalogue sont reconstructibles, mais le catalogue ne se réduit pas à un scan des sources musicales.
_Avoid_: Source musicale, dossier du NAS

**Source musicale**:
Un emplacement configuré dont kuro consulte les médias.
_Avoid_: Bibliothèque, stockage

**NAS**:
L'appareil qui conserve, en lecture seule pour kuro, les fichiers médias maîtres de la source musicale. Cette fonction ne détermine pas l'emplacement physique de l'état de Kuro.
_Avoid_: KuroKor, stockage de l'état de Kuro

**Média**:
Un fichier audio de l'utilisateur que kuro consulte depuis une source musicale.
_Avoid_: Donnée d'application

**Référence de catalogue**:
Un lien durable entre le catalogue et un média, conservé lorsque la racine change mais que le chemin relatif reste identique.
_Avoid_: Identité musicale, empreinte universelle

**Donnée durable**:
Une donnée créée ou choisie dans kuro qui doit pouvoir être restaurée.
_Avoid_: Cache, index

**Donnée reconstructible**:
Une donnée que kuro peut recréer à partir des sources musicales et des données durables.
_Avoid_: Donnée durable

**Cache audio**:
Une copie reconstructible d'un média du NAS, conservée par kuro pour préparer ou maintenir la lecture. Le cache audio n'est ni la source musicale maîtresse ni une donnée durable.
_Avoid_: Média maître, sauvegarde

**Moteur audio**:
La responsabilité logique qui transforme une représentation du média en son au point de lecture. Sa répartition dépend de la destination et ne désigne ni un produit séparé ni un hôte physique imposé.
_Avoid_: Kuro Client, lecteur externe

**Tampon PCM de lecture**:
Les échantillons décodés qu'une partie du chemin média tient prêts pour la sortie. Un tampon PCM est transitoire et ne remplace ni le média du NAS ni le cache audio.
_Avoid_: Cache audio, fichier maître

**Point de lecture**:
L'hôte ou l'appareil qui remet l'audio à la chaîne de sortie. Il peut s'agir de l'hôte de KuroKor, de l'hôte d'un Kuro Client ou d'un appareil réseau distinct.
_Avoid_: Contrôleur, Kuro Client

**Point de lecture réseau**:
Un point de lecture qui reçoit par le réseau une représentation du média adaptée au protocole, puis alimente sa sortie locale.
_Avoid_: Kuro Client, multiroom

**Chemin de contrôle**:
Le trajet logique des intentions de l'utilisateur et de l'état entre un Kuro Client et KuroKor. Il reste distinct du chemin média même lorsque les deux partagent un hôte, une application ou un processus.
_Avoid_: Chemin média

**Chemin média**:
Le trajet logique du média depuis le NAS jusqu'au point de lecture et à la chaîne de sortie. Selon la destination et le protocole, il transporte un fichier, un flux encodé ou du PCM, et répartit autrement le décodage, les tampons et la sortie.
_Avoid_: Chemin de contrôle

**Bit-perfect**:
L'égalité des échantillons audio observés entre deux points de contrôle nommés du chemin du signal. Cette égalité ne prouve ni la qualité sonore ni le comportement des horloges après le second point.
_Avoid_: Qualité sonore, absence de jitter

**Pochette détenue par l'application**:
Une image durable ajoutée ou conservée dans les données de kuro.
_Avoid_: Image de source

**Image de source**:
Une image externe présente dans une source musicale et consultée en lecture seule.
_Avoid_: Pochette détenue par l'application

**Snapshot de sauvegarde**:
Une copie cohérente des données durables et des métadonnées connues à un instant donné.
_Avoid_: Copie des médias, historique de sauvegardes

**Restauration**:
Le remplacement confirmé de l'état de Kuro par un snapshot de sauvegarde compatible.
_Avoid_: Fusion de bibliothèques

**File**:
La suite de pistes destinée à la session d'écoute courante.
_Avoid_: Playlist

**Playlist**:
Une sélection durable de références de catalogue, indépendante de la file.
_Avoid_: File

**Cadrage courant**:
L'ensemble des usages et des limites retenus après les deux entretiens de cadrage.
_Avoid_: Corpus P1 à P5

**Corpus P1 à P5**:
Le dossier préparatoire initial qui conserve l'inventaire, les hypothèses, les plans et leurs preuves documentaires.
_Avoid_: Cadrage courant

**Backlog**:
Le registre des usages différés et des études requises avant une décision d'adoption.
_Avoid_: Roadmap

**Réadmission**:
La décision explicite qui replace un élément du backlog dans la roadmap après l'apparition d'un besoin et des preuves requises.
_Avoid_: Priorité implicite
