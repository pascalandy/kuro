# Stratégie de validation

Ce document définit des preuves produit futures et un contrôle documentaire exécutable aujourd’hui. Aucun scénario V-001 à V-050 n’a été exécuté sur kuro. Les choix P3 restent proposés, dont C-06 et les budgets de temps. Une autorisation de développement distincte reste nécessaire.

La [couverture canonique](couverture.tsv) rattache chaque fonction du [registre P2](inventaire-fonctions.tsv) à un plan responsable, sa milestone inchangée, une phase et un scénario. Les cas spécifiques ci-dessous reprennent `validation_future` sans en faire de nouveaux engagements. `socle` conserve le cadrage, `retenu_provisoire` attend confirmation, `proposition` attend adoption, `conditionnel` dépend d’un accès ou de droits et `reporte` reste futur. Une preuve peut être bloquée ou non applicable avec motif, jamais marquée réussie faute d’accès.

## Préparer les corpus et mesures

Définir les corpus avec l’utilisateur dans un environnement de test autorisé. Ne pas examiner maintenant sa bibliothèque, ses montages ou son DAC.

| Corpus proposé | Contenu et usage | Limite |
| --- | --- | --- |
| Petite fixture musicale | Quelques albums réellement écoutables, local et NAS, compilation, multidisque, copies distinctes, homonymes, accents, tags absents, artwork absent et fichier invalide. Manifeste des identités et résultats attendus. | Première tranche M1-P01 et cas déterministes. Ne prouve pas le volume cible. |
| Paires audio de référence | Signal continu connu coupé en deux pistes, puis encodé avec versions documentées. Paires de même format aux limites retenues et paire avec silence naturel connu. MP3 et AAC incluent délai d’encodage et padding connus. | FLAC, WAV, AIFF, ALAC, MP3, AAC, Vorbis et Opus sont les candidats P3, à accepter ou exclure explicitement avec l’utilisateur. Aucun format n’est garanti aujourd’hui. |
| Transitions de formats | Paires à fréquence, profondeur ou canaux différents, sur les sorties retenues. Séparer maintien du format, conversion et réouverture du périphérique. | Une preuve à format identique ne couvre pas ces transitions. DSD attend M3 et le matériel compatible. |
| Corpus cible | 20 000 albums, environ 3 To réels et autorisés, avec répartition locale et NAS décrite. Compter réellement pistes, fichiers, doublons, formats, images et anomalies. | Nombre de pistes inconnu. D’éventuelles variantes de charge, par exemple plusieurs distributions de pistes par album, sont des propositions de test, jamais une description de la collection. Un index synthétique seul ne remplace pas ce corpus. |
| Corpus M2 à M7 | Copies et éditions, œuvres dont les mouvements ne suivent pas les pistes, crédits homonymes, deux profils, filtres aux résultats connus, captures DSP et fixtures fournisseurs autorisées. Endpoints et client mobile seulement à leur milestone. | Établir les droits de chaque donnée de test. Aucune copie de catalogue ou média privé dans Git. |

Pour chaque campagne, relever OS et versions Omarchy, CPU, RAM, stockage et espace libre, versions exactes des composants, backend audio et DAC. Décrire protocole et montage NAS, débit, latence et topologie. Capturer taille DB, index et WAL, état du cache d’images, cache système froid ou chaud et méthode employée pour obtenir cet état. Publier seulement un relevé anonymisé. Sans ces paramètres, ne pas comparer deux mesures comme équivalentes.

Les captures audio distinguent le point logiciel mesuré, la sortie numérique physique et la sortie analogique du DAC. Un sink virtuel démontre la chaîne jusqu’à ce sink. Il ne prouve ni le signal physique ni le bit-perfect du DAC. Une capture matérielle exige un dispositif et une calibration décrits. Pour l’analogique, définir alignement et tolérance tenant compte du bruit et de l’horloge avant l’essai.

Comparer nombre, ordre et valeur des échantillons à la référence, après alignement déclaré. Ne pas assimiler les échantillons nuls à un défaut, puisque le signal peut contenir un silence naturel. Pour une compression avec perte, établir la référence décodée attendue et les délais exacts du codec. Mesurer séparément silence ajouté, données perdues, données dupliquées et transformations. Compléter par une écoute des jonctions. Si le matériel n’est pas capturable, documenter la portée plus étroite de la preuve.

## Mesurer les performances sans inventer de baseline

La campagne M1-P06 comprend import complet à froid, nouvel import sans changement, ajout incrémental défini, retrait et retour NAS, recherche et navigation pendant lecture et scan. Refaire avec caches chauds. Conserver jeu de requêtes, résultats attendus, nombre d’itérations, durée de lecture et quantité de modifications. Proposer ces tailles de campagne après connaissance du matériel, avant de regarder les résultats.

| Mesure | Définition proposée | Acceptation |
| --- | --- | --- |
| Requête p50 et p95 | Latence du service entre demande reçue et résultat prêt, plus mesure utilisateur séparée entre action et résultat visible | Recherche visible p95 < 300 ms est le budget proposé E-02, à approuver sur matériel fixé. Ce n’est ni mesure actuelle ni gate adopté. |
| Première page visible | Action utilisateur jusqu’à page exploitable avec sa sélection, distinguer données et images tardives | < 1 s est le budget proposé E-02, à approuver. Relever cold et warm séparément. |
| Mémoire et CPU | RSS par service, moteur et desktop, pic, état stable, charge et concurrence décrite | Aucun seuil RAM confirmé. Proposer après E-01. Contrôler croissance sur plusieurs cycles. |
| Import | Durée totale, débit fichiers et octets, erreurs, temps de reprise, complet et incrémental distincts | Aucun temps garanti. L’incrémental ne doit pas être présenté comme un scan complet plus rapide sans compter son travail. |
| Stockage et réseau | DB, index, WAL, cache et quota, octets NAS lus et débit pendant lecture | Fixer budgets après description du corpus. Éviter recalcul intégral de hashes à chaque scan. |
| Audio sous charge | Interruptions, sous-alimentations de tampon, jonctions et délai d’erreur sur durée fixée | Zéro silence ajouté pour corpus gapless accepté, avec tolérance instrumentale définie. Aucun résultat ne peut être déduit du seul CPU faible. |
| Synchronisation M4 | Décalage initial et dérive de deux captures physiques simultanées, perturbations réseau décrites | Budget à proposer et approuver selon appareils. Aucune valeur de marketing RAAT n’est reprise comme garantie kuro. |

La baseline n’existe pas. Conserver les données brutes de la première campagne acceptée afin de comparer les évolutions. M6 étend cette campagne aux autres plateformes et charges. M6 ne reporte pas MVP-03.

## Organiser les preuves futures

Chaque phase produit un dossier de preuve privé, dont l’emplacement sera choisi au développement. Il contient manifeste du corpus, versions, commande réelle alors disponible, résultat attendu, résultat observé et statut par fonction. Les noms de modules dans les plans sont des zones futures indicatives, pas des fichiers existants.

Les règles pures se vérifient par unité, les frontières par intégration et le résultat par parcours réel. La CI future exécutera les commandes du dépôt après leur création, avec fixtures autorisées. Les captures DAC, tests NAS et fournisseurs utilisent des environnements déclarés. Ne pas inventer une API `kuro test` aujourd’hui. Les tableaux de phase précisent ces niveaux et les performances utiles.

À chaque milestone, rejouer les preuves M1 affectées par la modification, avec les versions et formats retenus. Une migration appelle restauration réelle. Une nouvelle chaîne appelle capture audio et gapless. Un fournisseur appelle local désactivé et droits. La qualité d’usage ne se reporte pas en M7.

Les manifestes de sources comparent contenu, taille, permissions et date de modification avant et après. L’accès en lecture peut changer atime selon le système, à enregistrer séparément. Utiliser copies autorisées pour les essais qui modifient volontairement la fixture. Les originaux utilisateur restent intacts. Les preuves publiques contiennent comptes et résultats agrégés, sans médias, textes protégés, chemins privés, jetons ou clés. Les secrets sentinelles de test ne sont jamais des secrets réels.

## Scénarios futurs

## V-001

### Une machine et trois rôles

Phase responsable : [M1-P01](milestones/m01-mvp-local.md#m1-p01). État : non exécuté, produit futur.

1. Démarrer le service, ouvrir le contrôle local et lancer un album. Fermer la fenêtre, vérifier le service, puis reconnecter le contrôle. Relever séparément les versions du service, du client et du moteur.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La session reste attribuée au même service et le contrôle retrouve son état. Le comportement hors fenêtre suit C-06 proposé.

Mesures et artefacts prévus : Temps de reconnexion, identités de session et versions. Prévoir un journal de cycle de vie et une capture du contrôle.

Échecs et limites : Double service, version de contrat incompatible et service absent doivent donner un diagnostic, sans commande envoyée à un autre serveur.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F01-001 | Démarrer bibliothèque, contrôle et sortie sur la même machine | socle |
| F01-002 | Fermer le contrôle puis vérifier que le serveur reste joignable | socle |
| F01-003 | Ouvrir le desktop sur le serveur local sélectionné | socle |
| F01-006 | Identifier séparément les versions installées | socle |

## V-002

### Importer puis écouter local et NAS

Phase responsable : [M1-P02](milestones/m01-mvp-local.md#m1-p02). État : non exécuté, produit futur.

1. Importer une petite collection locale puis son complément sur NAS. Ouvrir un album de chaque origine et lire une piste. Inspecter les chemins utilisés et les octets transférés.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les deux sources restent distinctes et jouables. La base et son index résident sur disque local. Aucun transfert intégral des médias vers le disque local n’est nécessaire.

Mesures et artefacts prévus : Albums, pistes et tailles réellement lus, trafic NAS et emplacement de base. Prévoir manifeste du corpus et trace des lectures.

Échecs et limites : Accès refusé, montage absent et lien sortant de la racine autorisée restent des erreurs distinctes.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F02-001 | Importer un dossier puis retrouver ses albums | socle |
| F02-002 | Lire depuis un NAS joignable sans copier toute la collection | socle |

## V-003

### Réconcilier les sources sans effacer les références

Phase responsable : [M1-P02](milestones/m01-mvp-local.md#m1-p02). État : non exécuté, produit futur.

1. Ajouter un fichier à une fixture, laisser la surveillance agir, puis lancer un rescan manuel. Désactiver la source et la réactiver. Déplacer la source avec association explicite. Couper le NAS pendant un scan, simuler un point de montage vide, puis rétablir le NAS.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les générations de scan ne dupliquent pas les fichiers. Les playlists conservent les identités. Un scan incomplet ne prouve aucune suppression. Les exclusions ciblent seulement le dossier annoncé.

Mesures et artefacts prévus : Comparaison des identifiants avant et après, générations et durée de réconciliation. Prévoir snapshots logiques, événements de scan et liste des exclusions.

Échecs et limites : Chemin réutilisé par un autre contenu, copie ambiguë, événement perdu et arrêt entre deux lots ne doivent pas fusionner ou oublier des fichiers silencieusement.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F02-004 | Modifier un corpus de test puis comparer son index | socle |
| F02-005 | Ajouter un fichier puis le trouver après rescan | socle |
| F02-006 | Désactiver puis réactiver une source sans perdre les playlists | socle |
| F02-007 | Déplacer un corpus de test et vérifier ses références | socle |
| F02-008 | Exclure un dossier et constater son absence de l’index | socle |
| F13-003 | Déconnecter le NAS puis vérifier identités, playlists et retour des fichiers | socle |

## V-004

### Formats, tags et copies

Phase responsable : [M1-P02](milestones/m01-mvp-local.md#m1-p02). État : non exécuté, produit futur.

1. Importer chaque format et conteneur accepté, un format exclu, un fichier tronqué, un album multidisque, une compilation et deux copies distinctes. Comparer tags bruts, valeurs affichées et référence choisie dans une playlist.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le catalogue conserve les copies et les identités. Album, artiste et piste correspondent au manifeste. Chaque rejet explique sa cause. DSD reste un sujet M3.

Mesures et artefacts prévus : Nombre accepté et refusé par format, différences de champs et identités. Prévoir rapport d’import et manifeste des tags.

Échecs et limites : Tags manquants, homonymes et illustration malformée ne doivent ni fusionner les artistes par nom seul ni bloquer tout l’import.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F02-009 | Définir puis tester le sous-ensemble M1; DSD envisagé M3; signaler les formats refusés | socle |
| F02-010 | Importer un fichier invalide et retrouver son motif de rejet | socle |
| F02-011 | Comparer album, artiste et piste aux tags du corpus | socle |
| F03-001 | Conserver deux copies distinctes et une référence précise en playlist | socle |

## V-005

### Naviguer et rechercher dans le catalogue

Phase responsable : [M1-P03](milestones/m01-mvp-local.md#m1-p03). État : non exécuté, produit futur.

1. Parcourir albums, artistes et pistes des deux sources. Rechercher titres accentués, noms et titres absents. Filtrer, trier des nombres et accents, revenir à la recherche, puis avancer. Sélectionner trois pistes. Refaire sans Internet avec images locales et album sans image.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les résultats correspondent au jeu attendu. La sélection ne touche que ses trois pistes. La pagination a un ordre stable et le retour conserve le contexte selon la politique retenue.

Mesures et artefacts prévus : p50 et p95 des requêtes, délai jusqu’à première page visible, doublons ou omissions entre pages. Prévoir captures et résultats ordonnés comparés au manifeste.

Échecs et limites : Révision modifiée entre pages, résultats très nombreux et cache de pochettes vide ne doivent pas charger toute la collection en mémoire. F04-015 reste proposition.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F04-001 | Retrouver les albums locaux et NAS dans une vue | socle |
| F04-002 | Ouvrir un artiste et retrouver ses albums | socle |
| F04-003 | Retrouver une piste et lancer sa lecture | socle |
| F04-004 | Trouver album, artiste et piste par des requêtes connues | socle |
| F04-005 | Filtrer une liste et vérifier les éléments restants | socle |
| F04-006 | Trier titres et vérifier l’ordre sur accents et nombres | socle |
| F04-010 | Revenir à une recherche puis avancer à l’album | socle |
| F04-013 | Sélectionner trois pistes et vérifier les seules pistes ajoutées | socle |
| F04-015 | Afficher les images locales et une absence de pochette sans Internet | proposition |

## V-006

### Conserver une playlist locale

Phase responsable : [M1-P03](milestones/m01-mvp-local.md#m1-p03). État : non exécuté, produit futur.

1. Créer une playlist depuis un album et une sélection. Réordonner, retirer une occurrence, renommer, puis redémarrer. Créer et supprimer une autre playlist.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Identités et ordre persistants correspondent à la sélection. Retirer une entrée ou une liste ne supprime aucun média.

Mesures et artefacts prévus : Comparaison des identités d’occurrences et des empreintes sources. Prévoir états avant et après, avec trace des commandes.

Échecs et limites : Deux occurrences de la même piste restent distinctes. Une piste indisponible garde sa référence. Une commande répétée ne crée pas une seconde playlist.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F05-001 | Créer une playlist et comparer les identités et l’ordre | socle |
| F05-002 | Déplacer puis retirer une piste sans supprimer son fichier | socle |
| F05-003 | Renommer puis supprimer une playlist locale | socle |

## V-007

### Écouter la première tranche complète

Phase responsable : [M1-P01](milestones/m01-mvp-local.md#m1-p01). État : non exécuté, produit futur.

1. Depuis la vue minimale d’un album local, lancer une piste, pause, reprise, arrêt, précédent et suivant. Démarrer aussi au milieu d’une sélection.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La piste réellement entendue et la suite correspondent à l’intention acceptée. Ce petit parcours traverse import minimal, catalogue, contrôle, coordinateur et sortie réelle.

Mesures et artefacts prévus : Position annoncée contre position entendue, séquence des commandes et piste observée. Prévoir journal corrélé et courte capture de référence autorisée.

Échecs et limites : Un accusé de réception sans son effectif ne vaut pas lecture réussie. Le moteur absent doit apparaître comme erreur.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F06-001 | Exécuter chaque commande et comparer piste et position | socle |
| F06-002 | Lancer au milieu d’une playlist et vérifier la suite | socle |

## V-008

### Modifier la file pendant la préparation

Phase responsable : [M1-P03](milestones/m01-mvp-local.md#m1-p03). État : non exécuté, produit futur.

1. Afficher la file, déplacer puis retirer la piste suivante alors qu’elle est préchargée. Vider seulement les prochains, puis toute la file selon la politique choisie. Tester shuffle, répétition, historique de session, sauvegarde de sélection et recherche temporelle proposée.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La séquence entendue suit la révision canonique. Une précharge périmée ne prend pas la main. Shuffle respecte l’appartenance et la fin de cycle. La playlist sauvegardée contient seulement les occurrences retenues.

Mesures et artefacts prévus : Révisions de file, transitions de piste, temps et appartenance des occurrences. Prévoir trace corrélée moteur et coordinateur.

Échecs et limites : Événement tardif d’ancienne piste et double clic ne doivent pas avancer deux fois la file. F06-014 reste proposition, avec tolérance de position à fixer.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F06-003 | Comparer la file affichée à la séquence entendue | socle |
| F06-004 | Déplacer une piste et vérifier le prochain morceau | socle |
| F06-005 | Retirer une piste future sans interrompre la courante | socle |
| F06-006 | Vider les prochains puis vérifier l’état courant | socle |
| F06-007 | Vérifier appartenance des pistes jouées et fin de cycle | socle |
| F06-008 | Atteindre la fin et constater le retour attendu | socle |
| F06-009 | Revenir à une piste déjà jouée pendant la session | socle |
| F06-010 | Sauver les prochains morceaux et comparer la playlist | socle |
| F06-014 | Aller à une position puis comparer horodatage et son | proposition |

## V-009

### Sélectionner la sortie réelle

Phase responsable : [M1-P01](milestones/m01-mvp-local.md#m1-p01). État : non exécuté, produit futur.

1. Activer une sortie Linux identifiée, la sélectionner puis lire la tranche d’album. Comparer nom demandé, périphérique ouvert et son émis.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La sortie disponible devient sélectionnable. Le son sort du périphérique désigné et son état effectif remonte au contrôle.

Mesures et artefacts prévus : Identifiant matériel et format observé. Prévoir trace du backend et relevé de l’environnement audio.

Échecs et limites : Périphérique refusé ou déjà occupé doit rester visible comme échec. M1 peut utiliser une sortie partagée, sans promesse d’exclusivité.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F07-001 | Lire une piste sur la sortie locale désignée | socle |
| F07-002 | Activer une sortie et vérifier qu’elle devient sélectionnable | socle |

## V-010

### Volume partagé et perte de périphérique

Phase responsable : [M1-P04](milestones/m01-mvp-local.md#m1-p04). État : non exécuté, produit futur.

1. Changer le volume sur le matériel qui dispose d’un mixer, puis comparer la commande et l’état réel. Tester aussi la solution système proposée en P3. Débrancher la sortie pendant lecture, puis la reconnecter.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La méthode de volume est annoncée. Sans mixer matériel, appliquer la disposition P3 explicitement retenue, ou afficher contrôle externe à niveau fixe. Le retour du DAC ne provoque pas de reprise sonore surprise selon C-06 proposé.

Mesures et artefacts prévus : Niveau demandé et observé, méthode matérielle ou système, délai et erreur de déconnexion. Prévoir relevé matériel et trace des transitions.

Échecs et limites : Absence de mixer n’autorise pas à prétendre que F07-005 est démontrée sur ce matériel. Le choix du comportement de repli reste ouvert.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F07-005 | Changer le volume et comparer l’état matériel | socle |

## V-011

### Jonctions gapless et changements de format

Phase responsable : [M1-P04](milestones/m01-mvp-local.md#m1-p04). État : non exécuté, produit futur.

1. Lire et capturer chaque paire audio de référence définie dans le corpus, sur disque puis NAS. Comparer les échantillons à la concaténation attendue. Refaire MP3 et AAC avec délai d’encodage et padding connus. Tester séparément chaque changement de fréquence, profondeur et nombre de canaux retenu.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le corpus accepté n’a aucun silence ajouté, échantillon perdu ou dupliqué au-delà de la tolérance de mesure fixée avant essai. Chaque conversion et réouverture de sortie est déclarée. L’écoute complète la capture.

Mesures et artefacts prévus : Écart en échantillons, durée de rupture, format effectif et méthode d’alignement. Prévoir captures autorisées et rapport de comparaison avec tolérance explicite.

Échecs et limites : Une jonction PCM réussie ne valide ni un padding compressé ni un changement de format. Une sortie partagée ne prouve pas le bit-perfect au DAC.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F06-013 | Mesurer et écouter les jonctions sur chaque format retenu | socle |

## V-012

### Commande durable et reprise après crash

Phase responsable : [M1-P04](milestones/m01-mvp-local.md#m1-p04). État : non exécuté, produit futur.

1. Arrêter le service entre mutation et accusé, puis entre accusé et événement. Rejouer le même identifiant, puis le réutiliser avec un autre contenu. Perdre des événements et reconnecter. Interrompre un scan et la lecture. Redémarrer et comparer les données C-06.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Une seule mutation acceptée subsiste. Conflits et identifiants réutilisés sont explicites. Bibliothèque, playlists, file et réglages reviennent. La reprise à l’arrêt et le point de position périodique restent les comportements C-06 proposés à approuver.

Mesures et artefacts prévus : Nombre de mutations, révisions, état durable, perte maximale de position mesurée. Prévoir snapshots logiques et chronologie de crash.

Échecs et limites : Après expiration de rétention, relire l’état avant nouvel essai. Ne pas confondre acceptation durable et son déjà émis. F12-011 reste proposition.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-008 | Redémarrer puis comparer bibliothèque, playlists, file et réglages | socle |
| F12-011 | Interrompre import ou lecture puis comparer état et diagnostics | proposition |

## V-013

### Retards de source pendant lecture

Phase responsable : [M1-P04](milestones/m01-mvp-local.md#m1-p04). État : non exécuté, produit futur.

1. Introduire un retard NAS puis des interruptions répétées pendant lecture. Tester un fichier devenu illisible à la préparation suivante. Réduire puis restaurer la latence.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La lecture observée et l’erreur affichée correspondent. Une tentative échouée s’arrête selon C-04 proposé, sans boucle infinie. Le passage automatique à la suivante reste une décision avant code.

Mesures et artefacts prévus : Tampon restant, interruptions audio, durée de blocage et délai d’erreur. Prévoir chronologie réseau, moteur et interface.

Échecs et limites : Un scan bloqué ne doit pas bloquer le coordinateur. Un écran qui annonce lecture pendant une erreur durable échoue au scénario.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-013 | Retarder la source puis vérifier erreur visible et état de lecture | retenu_provisoire |

## V-014

### Sauvegarder puis restaurer une bibliothèque utilisable

Phase responsable : [M1-P05](milestones/m01-mvp-local.md#m1-p05). État : non exécuté, produit futur.

1. Sauvegarder pendant import et lecture. Restaurer dans un emplacement isolé. Vérifier manifeste, versions et intégrité. Comparer playlists, file et réglages. Réassocier une source déplacée, puis lire une piste locale et une piste NAS disponible.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les identifiants restent cohérents. La sauvegarde ne duplique pas les 3 To de médias et exclut index et caches reconstructibles selon C-06. L’ancienne base reste récupérable jusqu’à validation.

Mesures et artefacts prévus : Durée et taille de sauvegarde, différences logiques, lecture réelle après restauration. Prévoir manifeste, comparaison des identités et compte rendu de lecture.

Échecs et limites : Archive corrompue, version trop récente, espace insuffisant et source absente ne doivent pas remplacer la base valide. Un fichier d’archive ouvrable ne suffit pas.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-001 | Sauvegarder puis vérifier playlists, réglages et absence de médias copiés | socle |
| F12-003 | Restaurer en isolation puis comparer données et lecture | socle |

## V-015

### Utiliser le contrôle au clavier sur Omarchy

Phase responsable : [M1-P03](milestones/m01-mvp-local.md#m1-p03). État : non exécuté, produit futur.

1. Effectuer recherche, sélection, lecture et édition de playlist au clavier. Quitter Now Playing puis revenir à la piste courante. Évaluer focus visible, lisibilité et lecteur d’écran. Essayer touches média, notifications et fermeture de fenêtre.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les raccourcis essentiels et le retour à la piste fonctionnent. Les observations d’accessibilité et d’intégration bureau conservent leur statut de propositions.

Mesures et artefacts prévus : Parcours complétés, éléments sans nom accessible, perte de focus et commandes média reçues. Prévoir capture du parcours et journal d’accessibilité.

Échecs et limites : Fenêtre fermée et service arrêté sont deux actions différentes dans l’option P3. Versions Wayland, Omarchy et outils d’assistance doivent être consignées.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-005 | Exécuter les parcours essentiels au clavier sur Linux | socle |
| F12-007 | Quitter la position courante puis y revenir | socle |
| F12-010 | Évaluer clavier, focus visible, lisibilité et lecteur d’écran | proposition |
| F12-012 | Vérifier les touches média, notifications et fermeture de fenêtre | proposition |

## V-016

### Valider le volume dès M1

Phase responsable : [M1-P06](milestones/m01-mvp-local.md#m1-p06). État : non exécuté, produit futur.

1. Exécuter la [campagne de performance](#mesurer-les-performances-sans-inventer-de-baseline) sur 20 000 albums et environ 3 To autorisés. Mesurer import complet, incrémental, navigation, recherche et lecture simultanée. Refaire cache froid puis chaud.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : MVP-03 est éprouvé à sa taille cible, sans substitution par la petite fixture. Les budgets proposés sont comparés seulement après approbation sur matériel fixé.

Mesures et artefacts prévus : p50 et p95 requêtes, première page visible, RSS par processus, CPU, DB et WAL, cache, débit de scan, octets NAS, interruptions audio. Prévoir données brutes et rapport sans baseline inventée.

Échecs et limites : Une collection synthétique de métadonnées ne prouve pas la lecture et le scan de 3 To. Un nombre de pistes supposé ne doit pas remplacer le nombre mesuré.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-009 | Mesurer import, navigation, recherche et lecture à l’échelle cible | socle |

## V-017

### Continuer sans Internet avec LAN disponible

Phase responsable : [M1-P06](milestones/m01-mvp-local.md#m1-p06). État : non exécuté, produit futur.

1. Bloquer l’accès Internet dans un environnement de test autorisé en gardant le NAS joignable. Ouvrir le contrôle, parcourir, rechercher, créer une playlist et lire local puis NAS. Refaire avec caches externes vides.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les usages M1 des données locales n’attendent aucun fournisseur. L’état du NAS reste distinct de la disponibilité Internet.

Mesures et artefacts prévus : Délais des parcours, tentatives externes et erreurs. Prévoir relevé de topologie anonymisé et chronologie des actions.

Échecs et limites : Couper aussi le LAN ne valide pas ce cas. Les contenus distants facultatifs peuvent être indisponibles, sans bloquer la bibliothèque locale.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F13-001 | Couper Internet et réaliser navigation, recherche et lecture locales | socle |

## V-018

### Prouver sources intactes et diagnostics publiables

Phase responsable : [M1-P05](milestones/m01-mvp-local.md#m1-p05). État : non exécuté, produit futur.

1. Créer un manifeste d’empreintes et permissions de la fixture autorisée. Effectuer import, lecture, correction en base si disponible et restauration. Comparer les médias. Provoquer une erreur datée avec des secrets sentinelles puis inspecter logs et exports.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Aucune modification des médias n’est nécessaire. Le diagnostic situe l’erreur sans jeton ni chemin privé complet. L’exigence sources intactes est distincte de la protection des secrets proposée.

Mesures et artefacts prévus : Différence de contenu, taille, mode et date de modification, avec atime traité séparément. Prévoir manifeste privé, rapport agrégé et recherche des sentinelles.

Échecs et limites : Permissions de lecture seule, lien symbolique hors source et tags malformés font partie du corpus. Aucun média ni secret réel ne rejoint les artefacts publics.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-004 | Reproduire une erreur et retrouver un diagnostic daté sans secret | socle |
| F13-002 | Comparer les empreintes avant import, lecture et restauration | socle |
| F13-004 | Vérifier que diagnostics et exports ne révèlent aucun identifiant secret | proposition |

## V-019

### Choisir la licence avant adoption

Phase responsable : [M1-P01](milestones/m01-mvp-local.md#m1-p01). État : non exécuté, produit futur.

1. Avant adoption de composants, examiner versions, options de compilation, décodeurs, liaison et contenus distribués. Soumettre les options de licence kuro à la décision utilisateur. Vérifier ensuite notices et obligations de l’artefact exact.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La décision de licence est explicite, avec inventaire des dépendances. La production du présent dossier n’attribue aucune licence.

Mesures et artefacts prévus : Correspondance entre inventaire et paquet, obligations satisfaites ou bloquantes. Prévoir relevé de décisions et notices vérifiées.

Échecs et limites : Un nom de projet ou une séparation de processus ne constitue pas à lui seul une conclusion de compatibilité. Une autorisation fournisseur ne couvre pas une licence logicielle.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F14-001 | Consigner la licence approuvée et vérifier les notices de distribution | socle |
| F14-004 | Vérifier licences du moteur, décodeurs et interface retenus | proposition |

## V-020

### Reconstruire le premier paquet Linux

Phase responsable : [M1-P06](milestones/m01-mvp-local.md#m1-p06). État : non exécuté, produit futur.

1. Depuis un environnement propre autorisé, suivre la procédure publique future avec versions figées. Démarrer les trois rôles, effectuer U-01 à U-09 et vérifier désinstallation des seuls fichiers kuro.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La procédure reconstruit un artefact traçable. Les droits fichiers, audio et IPC suffisent aux parcours. Le niveau de reproductibilité, fonctionnel ou bit à bit, doit être choisi avant de le revendiquer.

Mesures et artefacts prévus : Empreintes et versions, différences entre constructions, succès des parcours et permissions. Prévoir recette de build future et manifeste de paquet.

Échecs et limites : Aucune commande kuro de test ou construction n’existe aujourd’hui. F14-002 reste proposition. Un paquet nécessitant un accès intégral au disque demande correction des permissions.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F14-002 | Reconstruire depuis un environnement propre avec versions documentées | proposition |

## V-021

### Importer et nettoyer la bibliothèque avancée

Phase responsable : [M2-P01](milestones/m02-bibliotheque-avancee.md#m2-p01). État : non exécuté, produit futur.

1. Copier par glisser-déposer vers une destination explicite. Importer tags multivalués, dates choisies, playlists relatives et XML iTunes. Prévisualiser un nettoyage sur des références indisponibles avant de le confirmer.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Destination, noms d’artistes, ordre et dates correspondent au manifeste. Les pistes manquantes sont listées. Le nettoyage proposé annonce les références affectées.

Mesures et artefacts prévus : Copies, membres ordonnés, dates et références avant et après. Prévoir manifestes source et destination et rapport d’import.

Échecs et limites : Artiste contenant un séparateur, XML incomplet, playlist pointant hors source et NAS absent ne doivent pas provoquer de suppression globale.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F02-003 | Comparer destination choisie et fichiers copiés | retenu_provisoire |
| F02-012 | Importer artistes multiples sans scinder les noms à tort | retenu_provisoire |
| F02-013 | Comparer date choisie et date affichée après réimport | retenu_provisoire |
| F02-014 | Importer des chemins relatifs et identifier les pistes manquantes | retenu_provisoire |
| F02-015 | Importer un XML de test puis comparer son ordre | retenu_provisoire |
| F02-016 | Afficher les références affectées avant nettoyage | proposition |

## V-022

### Distinguer éditions et structures

Phase responsable : [M2-P01](milestones/m02-bibliotheque-avancee.md#m2-p01). État : non exécuté, produit futur.

1. Choisir une correspondance locale d’édition, grouper puis séparer deux versions, changer la principale. Réunir deux disques, puis scinder un coffret. Redémarrer.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les fichiers et références de piste restent distincts, avec ordre de disque correct. Le choix manuel persiste. Aucun fournisseur n’est nécessaire à ces structures locales.

Mesures et artefacts prévus : Graphe d’identités et ordre avant et après. Prévoir snapshots logiques et captures de versions.

Échecs et limites : Éditions avec même titre ou nombres de pistes différents ne doivent pas fusionner leurs fichiers. Une association ambiguë reste réversible.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F03-003 | Choisir une correspondance et retrouver ce choix après redémarrage | retenu_provisoire |
| F03-004 | Grouper puis séparer deux éditions sans fusionner les fichiers | retenu_provisoire |
| F03-005 | Changer l’édition principale puis vérifier la vue album | retenu_provisoire |
| F03-010 | Réunir deux disques et vérifier l’ordre obtenu | retenu_provisoire |
| F03-011 | Scinder un coffret sans perdre ses références de pistes | retenu_provisoire |

## V-023

### Corriger sans écraser les données originales

Phase responsable : [M2-P02](milestones/m02-bibliotheque-avancee.md#m2-p02). État : non exécuté, produit futur.

1. Opposer titre importé et correction, changer la priorité, éditer une sélection, masquer un album, modifier ses indicateurs et sa pochette. Changer une image externe sur la fixture puis rescanner.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les seuls objets sélectionnés changent. Les corrections persistent après actualisation, avec provenance. Le filtre retrouve le masquage et le rescan retrouve l’image modifiée.

Mesures et artefacts prévus : Différences de valeurs brutes et effectives et empreintes sources. Prévoir comparaison avant et après, origine des champs et des images.

Échecs et limites : Fournisseur indisponible, ancienne correction et cache d’image périmé ne doivent pas détruire les valeurs choisies. Les originaux restent intacts.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F03-006 | Résoudre un conflit de titre selon la priorité choisie | retenu_provisoire |
| F03-007 | Corriger un titre puis comparer les fichiers sources | retenu_provisoire |
| F03-008 | Appliquer un changement aux seuls objets sélectionnés | retenu_provisoire |
| F03-009 | Actualiser les métadonnées et conserver le titre corrigé | retenu_provisoire |
| F03-012 | Masquer puis retrouver un album via filtre explicite | retenu_provisoire |
| F03-013 | Modifier un indicateur et vérifier son affichage | retenu_provisoire |
| F03-014 | Changer une pochette et vérifier sa provenance | retenu_provisoire |
| F03-015 | Changer une image externe puis constater le rescan | retenu_provisoire |

## V-024

### Parcourir crédits, œuvres et mouvements

Phase responsable : [M2-P02](milestones/m02-bibliotheque-avancee.md#m2-p02). État : non exécuté, produit futur.

1. Avant de fixer les champs, observer la surface de crédits actuellement documentée ou consigner son absence. Relier une œuvre à deux interprétations, dont les mouvements ne suivent pas un découpage piste pour piste. Chercher compositeur et chef, parcourir et corriger la hiérarchie de genres.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Personne, rôle, œuvre, mouvement et piste gardent des identités différentes. Les descripteurs filtrent les œuvres attendues. Les contradictions de F03-017 restent explicites.

Mesures et artefacts prévus : Relations attendues et obtenues, filtres et homonymes. Prévoir graphe de référence et captures des parcours.

Échecs et limites : Crédits incomplets et mouvements répartis sur plusieurs pistes ne doivent pas imposer une fausse relation un pour un. Fusion de genres ne modifie pas les tags sources.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F03-016 | Retrouver un musicien depuis le crédit d’une piste | retenu_provisoire |
| F03-017 | Observer l’éditeur actuel avant de fixer les champs | retenu_provisoire |
| F03-018 | Relier une œuvre à deux interprétations distinctes | retenu_provisoire |
| F03-019 | Afficher une œuvre dont les mouvements ne suivent pas un découpage un pour un | retenu_provisoire |
| F03-020 | Chercher une œuvre par compositeur et par chef | retenu_provisoire |
| F03-021 | Parcourir genre puis sous-genre et retrouver les albums attendus | retenu_provisoire |
| F03-022 | Fusionner deux libellés sans modifier les tags sources | retenu_provisoire |
| F03-023 | Filtrer les œuvres selon un descripteur connu | retenu_provisoire |

## V-025

### Focus et navigation avancée

Phase responsable : [M2-P03](milestones/m02-bibliotheque-avancee.md#m2-p03). État : non exécuté, produit futur.

1. Configurer colonnes et infobulles. Combiner genre, format et date, puis exclure un format. Ouvrir les interprétations depuis un compositeur. Comparer versions et emplacements. Lire un sous-dossier récursif, puis ouvrir image et livret de son album.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le résultat correspond à l’ensemble de référence. Réglages persistants, album du livret et périmètre du sous-dossier restent cohérents.

Mesures et artefacts prévus : Ensembles retournés, réglages au redémarrage et p95 des requêtes composées. Prévoir captures et résultats attendus.

Échecs et limites : Focus vide, intersection contradictoire, fichier PDF absent et dossier inaccessible doivent avoir des états lisibles. Aucun rendu de livret ne doit écrire le média.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F03-024 | Ouvrir l’image puis le livret du bon album | retenu_provisoire |
| F04-007 | Masquer une colonne puis conserver le réglage | retenu_provisoire |
| F04-008 | Combiner genre, format et date sur un corpus connu | retenu_provisoire |
| F04-009 | Exclure un format et comparer les résultats | retenu_provisoire |
| F04-011 | Ouvrir les interprétations d’une œuvre depuis son compositeur | retenu_provisoire |
| F04-012 | Identifier format et emplacement de deux versions | retenu_provisoire |
| F04-014 | Lire un sous-dossier et comparer les pistes incluses | retenu_provisoire |
| F12-006 | Activer puis masquer les infobulles | retenu_provisoire |

## V-026

### Organiser playlists et profils

Phase responsable : [M2-P03](milestones/m02-bibliotheque-avancee.md#m2-p03). État : non exécuté, produit futur.

1. Ajouter deux fois une sélection avec choix des nouveaux titres. Déplacer une playlist entre dossiers puis modifier une copie. Créer deux profils, marquer un favori et écouter une piste dans chacun.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La copie n’altère pas sa source. Bibliothèque commune, favoris et historique correspondent à la portée du profil. Les doublons restent un choix explicite.

Mesures et artefacts prévus : Membres des listes et données par profil. Prévoir comparaison des deux sessions.

Échecs et limites : Un profil musical n’est pas une autorisation réseau. Changer de profil ne doit pas dupliquer le catalogue ni attribuer l’écoute au profil précédent.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F05-004 | Ajouter deux fois la même sélection et choisir les nouveaux titres | retenu_provisoire |
| F05-005 | Déplacer une playlist entre deux dossiers | retenu_provisoire |
| F05-006 | Modifier une copie sans changer la source | retenu_provisoire |
| F05-007 | Marquer un album et retrouver le favori du profil | retenu_provisoire |
| F05-008 | Changer de profil et conserver la bibliothèque commune | retenu_provisoire |
| F05-009 | Lire une piste et retrouver son écoute au bon profil | retenu_provisoire |

## V-027

### Tags, bookmarks et automatismes locaux

Phase responsable : [M2-P03](milestones/m02-bibliotheque-avancee.md#m2-p03). État : non exécuté, produit futur.

1. Taguer plusieurs types et une sélection, importer ROONALBUMTAG et ROONTRACKTAG, puis changer de profil. Enregistrer, renommer et réordonner des bookmarks. Tester critères conjoints, alternatifs et exclusions d’une Smart Playlist. Ajouter un album éligible, bannir puis débannir un objet. Marquer un dossier favori.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Portée des tags et critères sauvegardés restent fidèles. La liste dynamique se recalcule. Le ban s’applique aux automatismes retenus sans interdire la lecture directe.

Mesures et artefacts prévus : Ensembles de référence avant et après mutation, retard de recalcul et références sauvegardées. Prévoir tables de vérité Focus et captures.

Échecs et limites : Actualisation concurrente, tag imbriqué et objet disparu ne doivent pas produire de membres fantômes. Radio fournisseur n’est pas requise pour tester les automatismes locaux.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F05-010 | Taguer des objets de types différents et les retrouver | retenu_provisoire |
| F05-011 | Taguer une sélection puis comparer ses membres | retenu_provisoire |
| F05-012 | Changer de profil et constater la visibilité attendue | retenu_provisoire |
| F05-013 | Importer ces champs sans modifier les fichiers | retenu_provisoire |
| F05-014 | Rouvrir un bookmark et vérifier ses critères | retenu_provisoire |
| F05-015 | Réordonner les bookmarks puis rouvrir le bon | retenu_provisoire |
| F05-016 | Ajouter un album éligible et constater l’actualisation | retenu_provisoire |
| F05-017 | Comparer critères conjoints et alternatifs sur un même corpus | retenu_provisoire |
| F05-018 | Bannir puis vérifier les automatismes et la lecture directe séparément | retenu_provisoire |
| F05-019 | Retrouver puis débannir un objet exclu | retenu_provisoire |
| F05-020 | Marquer un dossier et le retrouver en tête | retenu_provisoire |

## V-028

### Exporter sans toucher aux originaux

Phase responsable : [M2-P04](milestones/m02-bibliotheque-avancee.md#m2-p04). État : non exécuté, produit futur.

1. Exporter une portion de file, un catalogue et une playlist M3U. Copier des médias vers un dossier distinct avec métadonnées choisies. Ouvrir la M3U dans un lecteur indépendant.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Identités, ordre et champs correspondent à la sélection. Les tags de copie suivent le choix d’export. Les empreintes des originaux sont inchangées.

Mesures et artefacts prévus : Comparaison lignes, identités, tags copiés et hashes sources. Prévoir rapport d’export et lecture indépendante.

Échecs et limites : Destination égale à la source, permissions refusées et piste distante sans droits doivent être refusées ou signalées. Les cellules exportées ne doivent pas devenir des formules non voulues.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F05-021 | Comparer tags de la copie et empreintes des sources | retenu_provisoire |
| F05-022 | Rouvrir l’export dans un lecteur indépendant | retenu_provisoire |
| F05-023 | Comparer identités, ordre et champs exportés | retenu_provisoire |
| F06-011 | Exporter une portion choisie sans les autres pistes | retenu_provisoire |

## V-029

### Restaurer deux sauvegardes planifiées

Phase responsable : [M2-P04](milestones/m02-bibliotheque-avancee.md#m2-p04). État : non exécuté, produit futur.

1. Planifier deux sauvegardes avec une modification connue entre elles. Attendre les deux échéances puis restaurer chacune dans un espace isolé. Lire une piste dans chaque état.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Chaque point restitue sa propre version des playlists et des corrections. La dépendance aux sauvegardes antérieures, si incrémentales, est vérifiée.

Mesures et artefacts prévus : Échéances, taille, durée et comparaison logique. Prévoir manifestes de chaîne et rapports de restauration.

Échecs et limites : Maillon manquant, disque plein et service arrêté à l’échéance ne doivent pas annoncer une sauvegarde réussie. La politique de rattrapage reste à fixer.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F12-002 | Attendre deux sauvegardes et restaurer chacune | retenu_provisoire |

## V-030

### Exclusivité et vérité de la sortie

Phase responsable : [M3-P01](milestones/m03-audio-audiophile.md#m3-p01). État : non exécuté, produit futur.

1. Identifier le DAC réel et comparer modes partagé et exclusif face à une application concurrente. Tester volume fixe et atténuation logicielle. Demander un format au-dessus de la limite, changer de fréquence et comparer chaque étape du signal path.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le format affiché distingue demandé et observé. Niveau fixe et gain correspondent aux contrôles. Adaptations et délai de resynchronisation sont visibles. DSP actif exclut la revendication bit-perfect.

Mesures et artefacts prévus : Format effectif, niveau, durée de réouverture et chaîne observée. Prévoir capture audio et relevé matériel.

Échecs et limites : Backend qui ne rapporte pas le format laisse cette information inconnue. Refus d’exclusivité ne doit pas se présenter comme succès.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F07-003 | Comparer le modèle reconnu au matériel réel | retenu_provisoire |
| F07-004 | Observer les accès concurrents et le format de sortie | retenu_provisoire |
| F07-006 | Vérifier niveau et absence de réglage dans le contrôle | retenu_provisoire |
| F07-007 | Mesurer l’atténuation demandée sur un signal de test | retenu_provisoire |
| F07-009 | Demander un format supérieur et constater l’adaptation | retenu_provisoire |
| F07-011 | Changer de fréquence et mesurer le début audible | retenu_provisoire |
| F07-012 | Comparer chaque étape affichée aux réglages appliqués | retenu_provisoire |

## V-031

### Analyser sans affamer la lecture

Phase responsable : [M3-P02](milestones/m03-audio-audiophile.md#m3-p02). État : non exécuté, produit futur.

1. Planifier puis relancer une analyse sur sélection. Comparer loudness, dynamique et forme d’onde aux références, avec silences et fichier endommagé. Opposer ReplayGain importé et analyse. Écouter modes piste et album pendant la charge.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Créneau, progression et résultats sont visibles. La priorité du gain suit le réglage. Le niveau reste cohérent dans un album et l’indicateur de marge correspond à la continuité réelle.

Mesures et artefacts prévus : Valeurs de référence, marge calculée, CPU, retard d’analyse et interruptions audio. Prévoir résultats d’analyse et capture comparée.

Échecs et limites : Une tâche d’analyse lente ou corrompue ne bloque pas la lecture. La normalisation ne doit pas être annoncée sans gain effectivement appliqué.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F02-017 | Vérifier créneau d’analyse et progression visible | retenu_provisoire |
| F02-018 | Relancer une analyse et retrouver son résultat | retenu_provisoire |
| F08-001 | Comparer le résultat d’un corpus aux valeurs de référence | retenu_provisoire |
| F08-002 | Comparer affichage et sections silencieuses connues | retenu_provisoire |
| F08-003 | Analyser un fichier volontairement endommagé | retenu_provisoire |
| F08-004 | Comparer continuité intra-album et niveaux entre albums | retenu_provisoire |
| F08-005 | Comparer gain des tags et gain d’analyse selon le réglage | retenu_provisoire |
| F08-018 | Comparer l’indicateur au maintien d’une lecture continue | retenu_provisoire |

## V-032

### Chaînes DSP et conversion PCM

Phase responsable : [M3-P03](milestones/m03-audio-audiophile.md#m3-p03). État : non exécuté, produit futur.

1. Enregistrer deux chaînes pour deux configurations de zone, puis comparer leurs sorties successivement sur la sortie locale. Inverser deux filtres et les bypasser. Tester dépassement puis headroom, conversion, PEQ, mixage, crossfeed, convolution et délais de canaux avec signaux connus.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Ordre, bypass, réponse fréquentielle, impulsion, gains et délais correspondent aux références. Les réglages restent propres à chaque configuration. Deux zones simultanées seront validées en M4.

Mesures et artefacts prévus : Erreur de réponse et impulsion selon tolérance fixée, niveau maximal et retard par canal. Prévoir captures et paramètres des filtres.

Échecs et limites : Filtre incompatible, écrêtage et absence de marge CPU doivent être détectés. Une chaîne transformée n’est pas bit-perfect, même en sortie exclusive.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F08-006 | Comparer deux chaînes enregistrées et leurs sorties | retenu_provisoire |
| F08-007 | Inverser deux filtres puis mesurer l’effet et le bypass | retenu_provisoire |
| F08-008 | Provoquer un dépassement contrôlé puis le corriger | retenu_provisoire |
| F08-009 | Mesurer la fréquence après conversion | retenu_provisoire |
| F08-011 | Comparer la réponse mesurée au filtre choisi | retenu_provisoire |
| F08-012 | Appliquer délai, inversion et mixage à des canaux identifiés | retenu_provisoire |
| F08-013 | Mesurer le signal transféré au canal opposé | retenu_provisoire |
| F08-014 | Comparer l’impulsion produite au filtre chargé | retenu_provisoire |
| F08-017 | Mesurer gain et retard de chaque canal | retenu_provisoire |

## V-033

### DSD et multicanal selon capacités

Phase responsable : [M3-P04](milestones/m03-audio-audiophile.md#m3-p04). État : non exécuté, produit futur.

1. Après choix de matériel compatible, tester DSD natif, DoP ou conversion PCM selon capacités retenues. Identifier les canaux d’un fichier multicanal. Vérifier aussi le flux PCM converti vers DSD si cette fonction est adoptée.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Chaque stratégie admise produit le format et les canaux annoncés. Les stratégies impossibles restent indisponibles et documentées.

Mesures et artefacts prévus : Formats de flux et correspondance de canaux. Prévoir relevé DAC, captures et matrice de compatibilité.

Échecs et limites : Pas de DAC compatible signifie preuve matérielle manquante, sans prétendre réussir par simulation. Les possibilités P3 restent conditionnées au matériel et à la licence.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F07-008 | Tester les stratégies avec un DAC et des fichiers identifiés | retenu_provisoire |
| F07-010 | Identifier chaque canal d’un fichier de test | retenu_provisoire |
| F08-010 | Vérifier le flux obtenu sur une sortie compatible | retenu_provisoire |

## V-034

### Profils de casque et provenance

Phase responsable : [M3-P04](milestones/m03-audio-audiophile.md#m3-p04). État : non exécuté, produit futur.

1. Examiner accès et droits des profils retenus. Choisir le modèle de casque, comparer les deux modes Audeze documentés si accessibles, puis inspecter le PEQ OPRA éditable et son attribution.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le profil appliqué correspond au modèle et à sa version. Les modes et coefficients restent vérifiables. L’absence d’accès ne bloque pas le PEQ manuel.

Mesures et artefacts prévus : Coefficients, latence comparée et attribution. Prévoir provenance, réponse mesurée et référence de licence.

Échecs et limites : Modèle absent ou licence incompatible suspend ce profil. Ne pas copier un jeu de profils propriétaire en supposant son accès libre.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F08-015 | Sélectionner un modèle puis comparer les deux modes | retenu_provisoire |
| F08-016 | Choisir un casque puis inspecter le PEQ éditable | retenu_provisoire |

## V-035

### Fondu enchaîné distinct du gapless

Phase responsable : [M3-P03](milestones/m03-audio-audiophile.md#m3-p03). État : non exécuté, produit futur.

1. Configurer un fondu, lire une paire avec motifs distincts et capturer la sortie. Modifier sa durée puis désactiver le fondu. Rejouer la paire gapless de M1.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le chevauchement suit la durée choisie et disparaît au bypass. Le retour au gapless conserve la jonction de référence.

Mesures et artefacts prévus : Durée de chevauchement, enveloppe de gain et différence avec capture gapless. Prévoir captures alignées.

Échecs et limites : Une jonction sans silence obtenue par chevauchement ne valide pas le gapless. La portée par zone attend la validation de M4.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F06-012 | Mesurer le chevauchement sur un corpus de test | retenu_provisoire |

## V-036

### Appairer et révoquer des contrôleurs

Phase responsable : [M4-P01](milestones/m04-reseau-domestique.md#m4-p01). État : non exécuté, produit futur.

1. Appairer deux contrôleurs, refuser un tiers puis révoquer le second. Envoyer des mutations concurrentes et reconnecter après perte d’événements. Déclarer une zone privée.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les contrôleurs autorisés convergent vers l’état canonique. Le conflit de révision est explicite. L’accès révoqué et la zone privée respectent les permissions proposées C-07.

Mesures et artefacts prévus : Révisions, refus d’accès et temps de convergence. Prévoir traces expurgées des trois contrôleurs.

Échecs et limites : Profil musical et identité autorisée restent distincts. Une reconnexion avec ancien jeton ne doit pas rétablir un accès révoqué.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F09-001 | Modifier la file depuis deux contrôles et comparer leur état | retenu_provisoire |
| F09-006 | Vérifier qu’un autre contrôleur ne voit pas la zone privée | retenu_provisoire |
| F13-005 | Refuser un contrôleur non autorisé puis révoquer un accès | proposition |

## V-037

### Écouter sur des zones indépendantes

Phase responsable : [M4-P02](milestones/m04-reseau-domestique.md#m4-p02). État : non exécuté, produit futur.

1. Découvrir deux endpoints propres ou libres, lire des programmes différents, transférer piste et file, puis commander depuis un appareil. Afficher le titre courant sur un display et changer de piste.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Chaque zone conserve sa file. Le transfert garde la position selon tolérance convenue et le display suit la session réelle. Les commandes matérielles n’introduisent pas une seconde autorité.

Mesures et artefacts prévus : Position de transfert, identités de session, isolation de file et retard du display. Prévoir traces par endpoint et captures.

Échecs et limites : Déconnexion d’un endpoint ne doit pas arrêter les autres zones. Une capacité incompatible refuse le transfert avec motif. Aucune synchronisation n’est encore revendiquée.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F09-002 | Lire deux programmes différents simultanément | retenu_provisoire |
| F09-003 | Transférer une lecture et comparer position et file | retenu_provisoire |
| F09-007 | Découvrir un endpoint puis y lire une piste | retenu_provisoire |
| F09-012 | Commander depuis l’appareil et observer le contrôle | retenu_provisoire |
| F09-013 | Afficher le titre courant et suivre le changement de piste | retenu_provisoire |

## V-038

### Synchroniser puis dissocier un groupe

Phase responsable : [M4-P03](milestones/m04-reseau-domestique.md#m4-p03). État : non exécuté, produit futur.

1. Après zones indépendantes validées, grouper deux sorties compatibles. Capturer simultanément leurs impulsions au départ puis dans la durée. Introduire jitter et perte réseau. Retirer une sortie puis dissoudre le groupe.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le décalage et la dérive respectent le budget approuvé pour le matériel. Les zones restantes poursuivent selon la politique fixée et retrouvent leurs identités après dissociation.

Mesures et artefacts prévus : Décalage initial, dérive par durée, jitter, remplissage tampon et interruptions audio. Prévoir capture multivoie horodatée et relevé réseau.

Échecs et limites : Commandes arrivant ensemble ne prouvent pas la synchronisation audio. Une horloge incompatible doit empêcher le groupement ou produire une limite explicite.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F09-004 | Grouper deux sorties compatibles et mesurer leur décalage | retenu_provisoire |
| F09-005 | Retirer une sortie et vérifier les zones restantes | retenu_provisoire |

## V-039

### Protocoles et appareils tiers conditionnels

Phase responsable : [M4-P04](milestones/m04-reseau-domestique.md#m4-p04). État : non exécuté, produit futur.

1. Pour chaque protocole envisagé, établir droits et accès puis identifier matériel et version. Tester transport individuel et groupement réellement annoncé. Essayer Chromecast sur groupe externe configuré, Sonos et KEF par modèle, et Devialet AIR sur matériel retenu.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La matrice décrit les seuls appareils éprouvés. RAAT nécessite une autorisation propre et ne devient pas une condition de livraison des zones kuro.

Mesures et artefacts prévus : Accès autorisé, capacités et résultat par protocole et modèle. Prévoir matrice et traces expurgées.

Échecs et limites : Sans accès ou droits, marquer le connecteur bloqué et préserver M4 propre ou libre. Aucun groupement universel ne se déduit d’une marque.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F09-008 | Établir accès et droits avant essai sur matériel | conditionnel |
| F09-009 | Tester chaque protocole retenu sur matériel identifié | conditionnel |
| F09-010 | Vérifier support et groupement par modèle | conditionnel |
| F09-011 | Lire sur un groupe configuré par le système externe | conditionnel |
| F09-015 | Tester le modèle retenu et documenter ses limites | conditionnel |

## V-040

### Admettre chaque fournisseur séparément

Phase responsable : [M5-P01](milestones/m05-decouverte-et-integrations.md#m5-p01). État : non exécuté, produit futur.

1. Pour chaque fournisseur demandé, examiner conditions courantes, territoires, comptes, clés, quotas, cache, attribution, export et révocation. Distinguer droits de catalogue, de lecture et de téléchargement. Désactiver l’adaptateur et rejouer le local.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Une fiche d’admission explicite autorise ou bloque chaque capacité. Le catalogue local et sa lecture fonctionnent fournisseur absent.

Mesures et artefacts prévus : Droits établis, erreurs de quota et délai de retrait des accès. Prévoir fiche datée sans secret et tests de désactivation.

Échecs et limites : Une clé de catalogue ne vaut pas droit au flux. Une page commerciale ne vaut pas admission du projet kuro. E-08 reste futur.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F14-003 | Documenter les droits de chaque fournisseur retenu | conditionnel |

## V-041

### Enrichir avec provenance et textes facultatifs

Phase responsable : [M5-P02](milestones/m05-decouverte-et-integrations.md#m5-p02). État : non exécuté, produit futur.

1. Identifier une édition depuis un fournisseur admis. Comparer ses valeurs aux tags et corrections. Afficher biographie, relations, paroles statiques et synchronisées disponibles, puis supprimer temporairement la réponse fournisseur.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La provenance et l’attribution sont visibles. Les données locales restent intactes. Les lignes de paroles suivent la position sonore selon tolérance approuvée. Un texte absent a un état normal.

Mesures et artefacts prévus : Correspondances d’identité, différences de champs et décalage des paroles. Prévoir réponses de fixture autorisées et captures sans contenus protégés publiés.

Échecs et limites : Mauvaise édition, quota, texte retiré ou attribution absente empêchent cette donnée de remplacer la valeur locale. Les crédits utiles proviennent de M2.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F03-002 | Afficher résultat et provenance sans écraser les tags locaux | conditionnel |
| F10-001 | Afficher auteur ou fournisseur et gérer un texte absent | conditionnel |
| F10-002 | Naviguer d’un crédit vers une collaboration identifiée | conditionnel |
| F10-003 | Afficher les paroles disponibles et leur provenance | conditionnel |
| F10-004 | Comparer horodatage des lignes et position sonore | conditionnel |

## V-042

### Découvrir puis poursuivre une écoute

Phase responsable : [M5-P03](milestones/m05-decouverte-et-integrations.md#m5-p03). État : non exécuté, produit futur.

1. Rafraîchir Discover, comparer deux profils éligibles à deux dates, ajouter albums, artistes et pistes à Listen Later puis les écouter. Terminer une file depuis une amorce connue. Changer vote, limite bibliothèque et filtre explicite.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les sélections, renouvellements et états écoutés suivent les règles du fournisseur ou de l’algorithme retenu. Les réglages modifient les propositions sans altérer une file déjà choisie.

Mesures et artefacts prévus : Identités proposées, renouvellement daté, transitions Listen Later et respect des exclusions. Prévoir journal des recommandations et critères configurés.

Échecs et limites : Résultat vide, fournisseur coupé et aucune piste éligible doivent laisser une fin de file compréhensible. Aucun algorithme propriétaire Roon n’est promis.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F10-005 | Rafraîchir et constater la sélection renvoyée | conditionnel |
| F10-006 | Comparer deux profils éligibles puis le renouvellement quotidien | conditionnel |
| F10-007 | Ajouter un objet et le retrouver dans la liste dédiée | conditionnel |
| F10-008 | Lire un objet et vérifier son changement d’état | conditionnel |
| F10-009 | Terminer la file et observer la suite depuis une amorce connue | conditionnel |
| F10-010 | Changer un réglage puis comparer les pistes proposées | conditionnel |

## V-043

### Catalogues streaming et playlists distantes

Phase responsable : [M5-P04](milestones/m05-decouverte-et-integrations.md#m5-p04). État : non exécuté, produit futur.

1. Tester séparément chaque service admis avec compte autorisé. Vérifier territoires, langues et qualités, favoris Qobuz et limites nugs. Choisir une édition hors bibliothèque. Modifier une playlist aller-retour, supprimer une entrée et comparer le matching local et distant.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le contrat du service détermine ce qui est lisible et synchronisable. Les correspondances introuvables apparaissent dans un rapport. Les contradictions P2 restent à observer avant promesse de parité.

Mesures et artefacts prévus : Identités, ordre, conflits de synchronisation, qualité et restrictions par compte. Prévoir matrice de droits, réponses expurgées et rapport de matching.

Échecs et limites : Jeton expiré, région refusée, doublon et suppression concurrente ne doivent pas effacer une playlist locale. Pas de DSP ou téléchargement supposé permis sur un flux tiers.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F11-001 | Vérifier accès territorial et lecture avec un compte autorisé | conditionnel |
| F11-002 | Comparer favoris du service et bibliothèque après synchronisation | conditionnel |
| F11-003 | Vérifier territoire, langue et lecture disponible | conditionnel |
| F11-004 | Vérifier recherche complète et limites bibliothèque, vidéo et Radio | conditionnel |
| F11-005 | Observer le choix de version hors bibliothèque | conditionnel |
| F11-006 | Tester modification aller-retour et effets de suppression | conditionnel |
| F11-007 | Comparer fichiers locaux, références distantes et rapport d’échecs | conditionnel |

## V-044

### Radio, écoutes partagées et extensions

Phase responsable : [M5-P04](milestones/m05-decouverte-et-integrations.md#m5-p04). État : non exécuté, produit futur.

1. Rechercher une station par genre, lieu et langue. Enregistrer une URL de flux de test. Activer l’envoi d’écoutes au compte choisi avec radio désactivée. Autoriser puis révoquer une extension. Vérifier les destinations actuelles du partage avant connexion.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La station choisit le flux attendu. Les écoutes vont seulement au compte et aux catégories autorisés. Révocation retire les commandes de l’extension. Une destination historique non disponible reste exclue.

Mesures et artefacts prévus : Flux sélectionné, envois capturés et autorisations. Prévoir traces expurgées et résultat par destination.

Échecs et limites : URL invalide, répétition d’envoi et extension révoquée ne doivent pas exposer un secret ou répéter une mutation. Le consentement à envoyer reste explicite.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F11-008 | Retrouver une station par genre, lieu et langue | conditionnel |
| F11-009 | Enregistrer une URL de test et vérifier le flux sélectionné | conditionnel |
| F11-010 | Vérifier envoi au compte choisi et option radio désactivée | conditionnel |
| F11-011 | Autoriser puis révoquer une extension de test | conditionnel |
| F11-012 | Vérifier les destinations actuelles avant connexion | conditionnel |

## V-045

### Passerelles audio externes et MQA

Phase responsable : [M5-P04](milestones/m05-decouverte-et-integrations.md#m5-p04). État : non exécuté, produit futur.

1. Vérifier disponibilité et droits actuels MQA avant de définir une cible. Pour HQPlayer, utiliser une instance autorisée et vérifier transport, contrôle et sortie effective.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Chaque fonction reste conditionnelle à un accès démontré. Le format réellement traité et les limites sont déclarés. Aucune contradiction historique MQA n’est tranchée par supposition.

Mesures et artefacts prévus : Accès, versions et chaîne de sortie observée. Prévoir fiche de capacité et trace de transport.

Échecs et limites : Pas d’accès signifie intégration bloquée, sans bloquer le moteur local. Une étape MQA affichée ne prouve pas un décodage autorisé.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F07-013 | Vérifier disponibilité et droits avant toute cible de parité | conditionnel |
| F09-014 | Vérifier transport et sortie avec une instance autorisée | conditionnel |

## V-046

### Porter le parcours sur les desktops retenus

Phase responsable : [M6-P01](milestones/m06-desktop-et-distribution.md#m6-p01). État : non exécuté, produit futur.

1. Pour chaque OS retenu après Linux, installer dans un environnement propre et refaire import, navigation, recherche, playlist, lecture, arrêt puis restauration. Tester backend audio, permissions et clavier propres à cet OS.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les mêmes contrats métier et preuves M1 restent valides. Les fonctions M2 à M5 portées sont listées explicitement, sans supposer leur présence.

Mesures et artefacts prévus : Parcours et matrice de capacités par OS, budgets mesurés sur matériel décrit. Prévoir rapports par plateforme.

Échecs et limites : Un lancement réussi ne valide pas une sortie audio ni les permissions NAS. Une capacité non portée doit être visible, sans état métier différent.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F01-004 | Réaliser le même parcours sur chaque desktop retenu | retenu_provisoire |

## V-047

### Mettre à jour et déplacer le serveur

Phase responsable : [M6-P02](milestones/m06-desktop-et-distribution.md#m6-p02). État : non exécuté, produit futur.

1. Confirmer d’abord la possibilité native ou conteneur du NAS serveur choisi. Mettre à jour depuis une version supportée. Vérifier version et données. Restaurer sur un autre hôte puis retrouver playlists et lecture avec sources réassociées.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Un seul service actif possède chaque bibliothèque. Migration et relocalisation conservent les identités. Le support NAS serveur reste une cible à confirmer, distincte du NAS source M1.

Mesures et artefacts prévus : Versions, durée d’indisponibilité, différences de données et ressources. Prévoir manifestes de paquet, rapport de migration et restauration.

Échecs et limites : Architecture CPU, stockage local de DB absent ou accès audio incompatible peuvent exclure un hôte. Une migration ratée conserve une procédure de retour avec données récupérables.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F01-005 | Confirmer le support natif ou conteneur avant choix | conditionnel |
| F01-007 | Mettre à jour puis lire la version et vérifier les données | retenu_provisoire |
| F01-008 | Restaurer ailleurs puis retrouver les mêmes playlists | retenu_provisoire |

## V-048

### Consulter et écouter depuis le mobile distant

Phase responsable : [M7-P01](milestones/m07-mobile.md#m7-p01). État : non exécuté, produit futur.

1. Après choix du transport distant sécurisé, appairer un client mobile de test. Parcourir bibliothèque et éditions, lancer une piste autorisée puis comparer avec le serveur. Révoquer l’accès et changer de réseau.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Les identités et versions de contrat restent communes. L’état distant converge sans donner au mobile une seconde autorité sur la bibliothèque. Révocation retire l’accès.

Mesures et artefacts prévus : Identités, état de lecture, temps de reconnexion et consommation réseau. Prévoir traces expurgées et parcours mobile.

Échecs et limites : Réseau intermittent et contrat incompatible doivent préserver les commandes déjà acceptées. Le design précis de l’interface mobile attend cette étape.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F15-001 | Comparer données mobile et serveur sur un parcours distant | reporte |

## V-049

### Télécharger les seuls médias autorisés

Phase responsable : [M7-P02](milestones/m07-mobile.md#m7-p02). État : non exécuté, produit futur.

1. Télécharger un fichier local autorisé puis couper tous les réseaux. Lire la copie, redémarrer le client et reprendre la consultation des téléchargements. Demander aussi un contenu streaming non autorisé au téléchargement.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : Le fichier téléchargé est intègre et jouable hors ligne. L’origine et les droits sont conservés. Le contenu streaming exclu n’est pas téléchargé.

Mesures et artefacts prévus : Empreinte, espace local, état persistant et résultat sans réseau. Prévoir manifeste de téléchargement et preuve de lecture.

Échecs et limites : Interruption partielle, fichier modifié à la source et manque de place doivent conserver un état distinct d’un téléchargement complet.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F15-002 | Télécharger puis lire sans réseau et vérifier les exclusions streaming | reporte |

## V-050

### Gérer quota, rotation et conservation mobile

Phase responsable : [M7-P03](milestones/m07-mobile.md#m7-p03). État : non exécuté, produit futur.

1. Fixer un quota de test, remplir le cache, marquer des fichiers à conserver puis dépasser le quota. Observer la rotation, redémarrer et interrompre un remplacement en cours.
2. Comparer le résultat aux cas spécifiques ci-dessous et consigner chaque écart.

Résultat attendu : La rotation respecte le quota et les règles de conservation retenues. Les fichiers conservés ne sont pas supprimés silencieusement. Un remplacement interrompu converge vers un état récupérable.

Mesures et artefacts prévus : Octets utilisés et réservés, ordre d’éviction, intégrité et consommation réseau. Prévoir journal de quota et manifeste avant et après.

Échecs et limites : Si les fichiers protégés occupent tout le quota, annoncer l’impossibilité d’ajouter. Les seuils batterie, réseau et espace restent à définir avant adoption.

| Fonction | Cas spécifique conservé du registre | Disposition inchangée |
| --- | --- | --- |
| F15-003 | Saturer un quota de test et constater la rotation des fichiers | reporte |
