# Candidat B : décoder au serveur, consommer au salon

## Problem

Kuro remplace l'Aurender par deux ordinateurs distincts. Je retiens le décodage au serveur et une livraison PCM bornée vers le salon. Cela centralise les décodeurs et rend comparable le signal avant et après réseau. Ce choix expose davantage la lecture aux interruptions réseau que la préparation de fichiers complets. Il doit gagner cette comparaison par ses preuves, sans déduire une qualité sonore du langage ou de l'expérience Roon rapportée.

## Usage (caller's view)

L'utilisateur choisit « Salon », ouvre un album puis prépare sa lecture. Kuro affiche « Prêt : PCM stéréo 48 kHz, 16 bits ; gain logiciel absent ; sortie physique non vérifiée ». Lecture démarre explicitement. Une perte de connexion affiche Arrêté et impose une nouvelle Lecture. Fermer la fenêtre laisse le serveur actif. La future fenêtre conserve les commandes et retrouve sa position en revenant de l'album à la liste.

```rust
let device = kuro.select_device(salon)?; // appareil configuré, capacités et erreurs
let ready = kuro.prepare(album.selection(), device)?; // prépare sans son
let playing = kuro.start(ready.ticket)?; // geste Lecture explicite

kuro.edit_queue(InsertNext(selection.with_duplicates()))?; // ne démarre rien
let state = kuro.status()?; // occurrence, position observée, format et inconnues

kuro.seek(playing.session, TrackPosition::seconds(93))?; // invalide l'ancien flux
```

Ces appels sont la spécification métier. Le bouton « Lire cet album » peut masquer la préparation, mais son geste autorise alors explicitement le démarrage. La commande cliente ne construit ni transactions ni paquets PCM.

## Shape

Le serveur possède catalogue, file durable, état de session et décodeurs. Le renderer possède uniquement sa configuration locale, une session temporaire, ses tampons et GStreamer. Une machine d'états de lecture autorise les effets audio. Catalogue et scans ont leurs propres opérations, hors de cette machine. Voir [les contrats](contracts.md).

La livraison proposée est un protocole de laboratoire versionné sur TCP, avec crédits de tampon et commandes indépendantes des gros blocs. Ce n'est pas un nouveau standard adopté. [TCP livre des octets ordonnés](https://www.rfc-editor.org/rfc/rfc9293.html), sans garantie d'arrivée avant consommation. Les numéros de trame et empreintes applicatives servent la preuve et les limites mémoire.

Le moteur du salon est GStreamer existant, `appsrc -> alsasink`, avec format exact et sans convertisseur ajouté. `appsrc` expose tampon borné, blocage et niveaux ; ces fonctions sont [documentées](https://gstreamer.freedesktop.org/documentation/app/appsrc.html) et présentes dans le plugin local 1.28.6. L'application contrôle la livraison, le moteur possède la boucle audio. L'horloge choisie doit être celle du puits, conformément au [modèle GStreamer](https://gstreamer.freedesktop.org/documentation/application-development/advanced/clocks.html), puis être vérifiée à l'exécution. Aucune horloge serveur n'est distribuée.

Je choisis Rust pour le prototype : sockets et files bornées, types distincts pour occurrences et générations, tests de panne déterministes ; puis [bindings GStreamer maintenus par le projet](https://github.com/GStreamer/gstreamer-rs) pour le même contrat de réception sur matériel. Rust 1.98.0, FFmpeg n9.0.1 et GStreamer 1.28.6 sont observés ici. Le premier exécutable utilise seulement un consommateur simulé ; FFmpeg reste un sous-processus de décodage séparé. Les workers de lecture NAS et décodage ne bloquent jamais le propriétaire de session.

La profondeur des interfaces vient de `prepare/start/seek/edit_queue`, qui cachent validation, persistance, annulation et reconnexion. Le renderer ne connaît ni SQL ni chemin NAS. Les types opaques protègent les identités ; les formats externes sont validés à la frontière, conformément à boundary-discipline. Aucun journal universel d'événements ni couche par étape de traitement.

## Synthesis decision

À remplir par le parent après comparaison.

## Tradeoffs accepted

- Nous acceptons un flux réseau continu et davantage de bande passante en échange d'un renderer sans décodeurs de fichiers. Le profil 192 kHz, stéréo, mots 32 bits représente 12,288 Mbit/s de PCM, hors protocole.
- Nous acceptons deux décodeurs serveur au maximum, courant et suivant, pour préparer une transition homogène sans changer le moteur de sortie.
- Nous acceptons le coût d'un adaptateur PCM spécifique pour mesurer directement livraison et échantillons. Il faut encore établir que ce coût vaut mieux que MPD avec fichiers locaux.
- Nous acceptons un arrêt explicite aux erreurs et formats refusés. Une conversion cachée ou une autre sortie ne sauve pas la lecture.

## Alternatives considered

- Fichiers complets préparés au salon puis MPD : meilleure résistance aux coupures et suppression du réseau média pendant la lecture. Cette organisation déplace décodeurs, cache durable et politique de préparation au renderer. Elle gagne si son délai de préparation et son stockage conviennent, ou si la charge réseau affecte les mesures/écoutes à chaîne constante. B peut gagner avec faible stockage salon, démarrage rapide et décodeurs centralisés, pas avec une promesse de meilleur son.
- HTTP progressif vers MPD : masque transport et décodeurs derrière une interface mûre, mais donne moins de contrôle au serveur sur le PCM envoyé et sur les tampons. C'est moins de code et un concurrent sérieux si les captures rendent ses transformations suffisamment observables.
- LMS + Squeezelite : système ouvert crédible pour référence. Le renderer ouvre lui-même la connexion média, selon le [code SlimProto](https://github.com/ralph-irving/squeezelite/blob/c7c4248ddd70e47dbfeba0bf4a8a7ec08d8a995c/slimproto.c). Ce n'est pas une primitive générique de PCM poussé. Réimplémenter SlimProto ou maintenir une seconde autorité de file n'est pas justifié par ce prototype.
- Snapcast/Sendspin ajoutent une synchronisation entre horloges et des corrections de flux inutiles à cette sortie unique ; [Snapcast décrit ces corrections](https://github.com/badaix/snapcast#how-does-it-work). [RAAT propose un SDK fabricant](https://help.roonlabs.com/portal/en/kb/articles/roon-ready), pas une dépendance publique acquise pour Kuro.

## Open questions and risks

- Quel format USB réel, quel modèle « Dynafripp », quelle révision Terminator et quel mode I2S seront observés ? Le modèle Denafrips du DDC reste une hypothèse.
- Les transitions et interruptions acceptées permettent-elles un tampon raisonnable sans altérer les échantillons ? Si non, privilégier la préparation locale.
- Le coût de compilation, de paquet et d'intégration GStreamer Rust dépasse-t-il l'intérêt du langage ? Un probe Go standard-library serait moins coûteux, mais l'étape GStreamer ajoute alors une frontière de binding distincte. Aucun runtime ne promet un son supérieur.
- Le même renderer présente-t-il une différence analogique ou d'écoute reproductible entre PCM réseau et PCM préparé localement ? Le hash seul ne tranche pas.

## Next implementation step

Construire le probe Rust local décrit dans [le plan de preuve](proof-plan.md), avec PCM déterministe, crédits, capture des arrivées et injections d'échecs, avant tout accès au DDC.
