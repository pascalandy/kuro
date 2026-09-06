# Proposition A : récupération progressive, décodage au salon

## Usage (caller's view)

L'utilisateur choisit l'ordinateur du salon, prépare un album, puis presse Lecture. Il voit « préparation », « lecture » ou une erreur située : source, réseau, renderer ou sortie. Les commandes restent visibles pendant la navigation album/liste ; Retour restitue recherche et position. Fermer la fenêtre conserve la session. Quitter arrête le renderer et le service. Après redémarrage, la file et la position reviennent sans son.

```python
device = session.select_device(RendererId("salon"))
prepared = session.prepare(AlbumSelection(album_id), device.id)
# Un clic Lecture, distinct de la préparation :
session.start(prepared.id)
# Une reconnexion de fenêtre obtient aussi les erreurs et les preuves de format :
state = session.status()
```

Ces appels sont métier. Aucun client ne fabrique d'URL, ne manipule les identifiants MPD ou ne coordonne une transaction. « Préparé » signifie plan accepté et file projetée arrêtée, pas audio préchargé : MPD peut attendre Lecture avant de lire l'URL.

## Problem

La nouvelle priorité remplace la sortie exclusivement locale par NAS → serveur Kuro → ordinateur de salon → USB → DDC → I2S/HDMI → Terminator. Linux au salon reste une hypothèse initiale. Les documents actifs n'apportent encore aucune preuve audio. L'expérience Aurender constitue la référence d'écoute ; son contrôle propriétaire n'est aucune dépendance. Le fabricant « Dynafripp », le modèle du DDC et les révisions matérielles restent inconnus. Les protections des sources, identités, file et reprise arrêtée continuent de s'appliquer.

## Shape

Je retiens un serveur de session propriétaire du catalogue et des choix durables, avec une origine HTTP de fichiers originaux. Un agent sur l'ordinateur du salon projette le plan dans un MPD privé, puis MPD récupère progressivement les fichiers et possède le décodage et les tampons audio. Kuro n'envoie aucun PCM cadencé et ne crée aucun moteur audio. MPD documente les URL distantes, ALSA et les réglages de traitement dans son [manuel](https://mpd.readthedocs.io/en/stable/user.html) et son [protocole](https://mpd.readthedocs.io/en/stable/protocol.html).

Le serveur ne décode, ne rééchantillonne et n'applique aucun gain. Au renderer, premier profil expérimental : sortie ALSA exacte, sans mixeur logiciel, ReplayGain, normalisation ou crossfade. MPD peut toutefois convertir quand le matériel refuse un format : les paramètres demandés ne prouvent pas les paramètres livrés. Consigner les logs de conversion et `hw_params`, arrêter et signaler toute conversion non acceptée. Ce contrôle détecte un écart ; il ne garantit pas son absence avant le premier échantillon. [Checklist MPD](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback).

Les quatre opérations publiques cachent résolution de source, validation, transaction, projection MPD et erreurs, per boundary-discipline. L'agent cache MPD et la surveillance de session ; il ne possède aucun second catalogue. Le petit ensemble de modules évite une chaîne contrôleur/service/repository par entité, per minimize-reader-load. Les types distinguent références, occurrences et sessions, per model-the-domain.

Pour le premier prototype, choisir Go avec bibliothèque standard : HTTP avec plages d'octets, fixtures WAV, SHA-256, erreurs, tests et traces monotones sans FFI. [`http.ServeContent`](https://pkg.go.dev/net/http#ServeContent) fournit les requêtes partielles. Le serveur effectue stockage et contrôle ; il ne tient pas une échéance de DAC. Go 1.27.0 est indiqué comme installé dans l'étude commune. Le GC doit être mesuré sous charge concurrente ; aucune propriété de Go, Rust ou C++ ne démontre une supériorité sonore. Rust reste une autre adoption crédible si typage et comptabilité mémoire justifient son coût ; C++ n'apporte ici aucun accès moteur nécessaire.

Le premier essai reste sur loopback, sans MPD ni matériel. L'étape sur deux machines utilise SSH à hôte épinglé et un compte renderer restreint : contrôle par flux de l'agent, HTTP de Kuro accessible au renderer par transfert de port vers loopback. MPD reste sur son socket Unix. Cela évite une API générale sur le LAN ; le déploiement et les restrictions exactes de clé sont encore à éprouver. HTTP et commandes restent deux canaux distincts, même s'ils partagent SSH.

## Synthesis decision

À remplir par le parent après comparaison.

## Tradeoffs accepted

- Nous acceptons une dépendance continue au réseau en échange d'un démarrage sans téléchargement complet et d'un cache disque facultatif.
- Nous acceptons un agent local pour imposer le cycle de vie et masquer MPD ; une connexion distante directe à MPD ne couvre pas la perte de session.
- Nous acceptons une observation partielle de MPD avant instrumentation ; aucune case inconnue du chemin audio ne devient « transparent ».
- Nous acceptons qu'un manque prolongé de données arrête la lecture ; aucun retour réseau ne la reprend seul.

## Alternatives considered

- Préparation locale vérifiée avant lecture : retire les lectures réseau du morceau actif et vérifie tout le fichier avant ouverture. Elle gagne si les pannes NAS/LAN ou une différence analogique/écoutée reproductible l'exigent. Elle ajoute attente initiale, stockage, éviction et invalidation que le progressive pull n'impose pas. Le comparer avec le même MPD et la même sortie isole ce choix.
- PCM poussé par Kuro : centralise décodeurs et continuité, mais impose protocole de frames, préchargement, débit adapté au récepteur et reprises. Le serveur et le renderer doivent alors partager davantage de règles audio. Sans synchronisation multiroom ni DSP demandé, cette complication n'est pas justifiée par une preuve.
- OpenHome sur Linux : file résidente, identifiants et actions de transport sont documentés, mais un adaptateur ajoute découverte et reconciliation d'une seconde file. Direct MPD donne un environnement contrôlable sur le PC choisi. [Playlist1](https://github.com/openhome/ohPipeline/blob/942497b74f9c30d6288a56ac73fb18c738a14c3c/OpenHome/Av/ServiceXml/OpenHome/Playlist1.xml).

## Open questions and risks

- Le MPD exact peut-il respecter les formats et transitions retenus sans conversion inexpliquée, et permettre de prouver la frontière PCM réelle ?
- Le préchargement progressif tolère-t-il le réseau réel avec une latence de départ acceptable ? Sinon, passer à la préparation locale.
- La surcharge HTTP/SSH et le GC Go respectent-ils cette marge sous import et recherche ? Sinon, comparer Go et Rust avec les mêmes traces et budgets.
- Quels descripteurs USB, modes I2S, formats, point de volume et réglages du Terminator sont réellement présents ?
- Quels résultats analogiques et d'écoute distinguent ce renderer de l'Aurender, toutes les variables accessibles étant contrôlées ?

## Next implementation step

Écrire le programme Go de preuve HTTP et son consommateur WAV de laboratoire, puis exécuter transfert normal, corruption, troncature et arrêt temporaire avec traces recalculables.
