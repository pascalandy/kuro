# C. Préparer les fichiers au salon, y posséder la session

## Usage écrit avant les types

L'utilisateur choisit le salon et appuie sur Lecture dans un album. Kuro affiche la préparation et sa progression. Le renderer vérifie les fichiers complets de la première piste et de la suivante avant de commencer. Le même geste autorise le démarrage après préparation; aucune confirmation supplémentaire. Fermer la fenêtre laisse les services actifs. Une coupure du contrôle arrête la session après son délai de détection; le retour du réseau laisse la file arrêtée.

```rust
// Lecture d'un album, depuis la session desktop autorisée.
let salon = playback.select(configured_salon).await?;
let ready = salon.prepare(Selection::Replace(album.ordered_refs()), prepare_op).await?;
salon.start(ready, start_op).await?;

// Jouer ensuite garde la lecture actuelle et les occurrences distinctes.
let state = salon.state().await?;
salon.change(state.revision, QueueChange::InsertNext(vec![track, track]), edit_op).await?;

// Après redémarrage, affichage arrêté; seul Lecture autorise la reprise.
let state = salon.state().await?;
let ready = salon.prepare(Selection::Resume(state.revision), resume_op).await?;
salon.start(ready, restart_op).await?;
```

## Problème et décision

Je choisis un agent renderer qui possède la file durable, la position et la session, avec MPD comme moteur local remplaçable. Le serveur possède bibliothèque et playlists. Il livre les fichiers originaux depuis le montage NAS existant. Cette séparation rapproche l'ordinateur du salon du rôle de stockage local de l'Aurender, sans prétendre reproduire son son. Aurender et Conductor 5 restent la référence d'écoute. L'accès à leur protocole est inutile à cette architecture.

Le cadrage courant a déjà intégré KD-041 à KD-043 lors de cette exploration. La sortie locale partagée et l'absence d'écoute LAN sont l'ancien périmètre. Un renderer distinct est désormais requis; multiroom, mobile, accès distant et gestion des montages NAS restent exclus. Les références stables, sources intactes, doublons de file, reprise arrêtée et snapshot complet restent des contraintes. [Cadrage courant](../../../cadrage-courant.md).

## Forme

Trois propriétaires suffisent. `media` sur le serveur connaît les références et les versions de fichiers. `session` sur le renderer connaît les occurrences, les commandes, les fichiers réservés et la reprise. `engine` sur le renderer connaît MPD, ses identifiants éphémères et la sortie. Le client ne connaît ni URL, ni chemin de cache, ni identifiant MPD. Les méthodes publiques cachent téléchargement, validation, réservation et rapprochement avec le moteur, suivant boundary-discipline et minimize-reader-load.

`CatalogRef` suit la source configurée et le chemin relatif. `ObjectId` identifie des octets par longueur et SHA-256. `OccurrenceId` distingue deux présences de la même référence dans la file. Une modification de tags peut conserver `CatalogRef` tout en produisant un autre `ObjectId`. Un fichier identique peut partager un stockage physique sans fusionner deux références de bibliothèque. Le serveur copie une version dans un spool borné avant d'en publier le manifeste, afin qu'une reprise HTTP ne mélange pas deux versions du NAS.

MPD lit uniquement les chemins locaux vérifiés. Son protocole documente l'ajout local via socket Unix, les identifiants de piste, la navigation, les événements et les erreurs. Ses commandes groupées ne sont pas une transaction avec retour arrière. L'agent reste le seul client autorisé et reconstruit cette projection après incident. [Protocole MPD](https://mpd.readthedocs.io/en/stable/protocol.html).

Cette ownership diffère volontairement de la recherche partagée qui préfère une file serveur. Le renderer peut décider la transition, la réservation et l'arrêt dans une seule transaction locale. En échange, serveur et sauvegarde ne peuvent modifier la file pendant son indisponibilité. Le serveur ne tient qu'une vue marquée de sa révision, jamais une deuxième file modifiable.

## Coûts acceptés

- J'accepte une attente initiale et deux caches bornés, serveur et renderer, pour retirer les lectures NAS et HTTP du chemin de la piste en cours. Estimation affichée depuis les octets restants et le débit observé; aucune promesse de latence avant mesure. Pour 200 Mo manquants à 25 Mo/s, huit secondes de transfert restent nécessaires, hors copie NAS et vérification.
- J'accepte une file temporairement non modifiable quand le renderer manque, pour garder une seule autorité. La bibliothèque et les playlists serveur restent accessibles.
- J'accepte des lectures disque et du hachage au salon. Le staging peut réduire l'activité réseau, mais augmenter d'autres activités. Leur effet électrique ou sonore doit être testé.
- J'accepte MPD séparé et son packaging, plutôt qu'un nouveau décodeur, ordonnanceur ou pilote audio. Les diagnostics ne garantissent pas l'interdiction préalable de toutes ses conversions.

## Alternatives structurelles

| Forme | Complexité cachée ou exposée | Pourquoi elle perd ici; fait qui inverserait le choix |
| --- | --- | --- |
| Lecture progressive tirée, file serveur | Cache plus petit, départ plus rapide; l'adaptateur doit rapprocher la file serveur et la lecture qui avance à distance, et gérer un réseau actif jusqu'à la fin du fichier. | C isole plus nettement la piste déjà prête. La lecture progressive gagne si les gros fichiers rendent l'attente ou le stockage inacceptables et passent les mêmes essais de format, transitions et chaîne analogique. |
| PCM décodé au serveur et poussé | Centralise décodeur et traitements; transporte débit PCM, discontinuités et régulation du tampon. Un serveur ne doit pas imposer son horloge logicielle au DAC. | Travail supplémentaire sans traitement demandé. Cette forme gagne si les ressources du salon ne permettent pas le décodage local, ou si un moteur existant offre une intégration et des résultats matériel meilleurs. |
| Fichiers préparés, file serveur | Même isolation des médias; sauvegarde centrale plus simple, mais rapprochement session/file entre deux machines. | Perte d'autorité locale inutile dans C. Elle gagne si sauvegarde complète et édition de file avec renderer éteint deviennent des priorités confirmées. |

LMS/Squeezelite reste une référence ouverte de comparaison; une réimplémentation de SlimProto ajouterait une obligation protocolaire. RAAT n'est pas une base acquise, car les pages officielles présentent un SDK destiné aux fabricants, pas un protocole audio public réutilisable. [Roon Ready](https://help.roonlabs.com/portal/en/kb/articles/roon-ready).

## Langage et risques ouverts

Je retiens Rust pour le prototype de service et d'agent. Les types opaques séparent références, occurrences et tickets; HTTP et socket MPD restent hors moteur. Axum fournit un [exemple de service de fichiers](https://github.com/tokio-rs/axum/blob/main/examples/static-file-server/src/main.rs); les tâches NAS et hash passent dans un pool borné, car [Tokio coopère entre tâches](https://docs.rs/tokio/latest/tokio/task/). Aucun avantage sonore ne découle de Rust. Le coût de compilation, le graphe des dépendances et les erreurs opérationnelles feront partie du résultat. Go reste un remplacement crédible si son [ServeContent standard](https://pkg.go.dev/net/http#ServeContent) permet un outil plus simple à maintenir; C++ n'apporte ici aucun accès moteur indispensable. Pas de FFI dans ce premier outil.

Quelle attente et quel budget de stockage sont acceptables pour le plus gros couple de pistes? Le renderer réel expose-t-il les formats natifs requis sans conversion? Le besoin de sauvegarder quand le salon est éteint justifie-t-il une file serveur? Ces questions deviennent des conditions de révision, sans bloquer le prototype synthétique.

## Décision de synthèse

À remplir par l'orchestrateur après comparaison. Ce candidat recommande C pour la maîtrise des responsabilités et l'expérience mesurable avec fichiers locaux; il ne revendique aucune supériorité sonore.

## Première étape

Construire le test Rust décrit dans `proof-plan.md`, avec récepteur disque, manifeste immuable, corruption et modèle de consommation, avant toute installation audio.
