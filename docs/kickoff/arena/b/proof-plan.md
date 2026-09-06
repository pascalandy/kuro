# Plan de preuve borné

Statut : commandes envisagées pour le parent, pas résultats du candidat. Lire aussi les études partagées verification-research, engine-language-research et transport-research du 2026-09-06. Le prototype ne touche ni musique utilisateur ni sortie audio et n'adopte pas une stack produit.

## Premier exécutable

Un petit crate Rust `pcm-probe` lance producteur et receiver sur deux sockets loopback. Le receiver capture les blocs et calcule la consommation par un modèle explicite. Pas de GStreamer, NAS ou horloge matérielle dans ce premier résultat. PCM généré par index de trame entier, seed fixe, deux canaux différents, 48 kHz/16 bits little-endian. Deux pistes forment exactement un signal continu.

```text
cargo run --locked --bin pcm-probe -- fixture --out /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- run --case clean --dir /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- run --case corrupt --dir /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- run --case truncate --dir /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- run --case stall --dir /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- run --case drift --dir /tmp/kuro-b-proof
cargo run --locked --bin pcm-probe -- verify --dir /tmp/kuro-b-proof
```

Le modèle consomme 480 trames par période de 10 ms, démarre après 4 800 trames et borne la réserve applicative à 9 600 trames. Le cas stall suspend le producteur après consommation confirmée de 24 000 trames pendant 500 ms. À stock mesuré inférieur à 200 ms, le consommateur manque nécessairement des trames. Les timestamps monotoniques de réception reconstruisent la trace ; un mode de rejeu à temps virtuel fournit des attentes exactes et reproductibles. Aucun timestamp n'est une mesure de jitter du DAC.

| Cas | Résultat attendu et limite |
| --- | --- |
| Clean | Ordre et octets reçus identiques ; concaténation PCM égale à la fixture continue ; zéro manque dans le modèle nominal accepté |
| Corrupt | Un bit changé après calcul du digest ; receiver refuse ce bloc et arrête ; code d'échec contrôlé, aucune fausse réussite |
| Truncate | EOF au milieu du bloc ; erreur de longueur visible ; aucun bloc partiel consommé |
| Stall | Livraison totale éventuellement identique en mode capture ; événement de retard/manque avant deadline ; mode session s'arrête et reste arrêté |
| Drift | Rejeu ±200 ppm sur dix minutes virtuelles ; crédits s'adaptent sans croissance non bornée ni modification de trames si capacité réseau suffisante |
| Queue/seek/restart | Occurrences doublées distinctes ; reorder garde le courant ; ancien bloc rejeté après seek ; crash/bail et relance restent silencieux |

Conserver `manifest.json`, version Rust et Cargo.lock, fixture PCM, empreintes source/envoyé/reçu, `arrivals.ndjson`, crédits, niveaux de chaque tampon, paramètres du modèle, sorties attendues et réelles, statuts et stderr. `verify` recalcule depuis les traces brutes. Un profil nominal réel qui manque sa deadline constitue un résultat d'environnement à rapporter, jamais une raison de supprimer le contrôle.

## Décodeur séparé

Encoder la fixture avec `flac`, décoder avec le FFmpeg installé vers `pcm_s16le` sans changement de fréquence ni canaux, puis comparer trames et octets à la fixture. Conserver commandes complètes, version, sortie verbose et propriétés. Cela prouve ce fichier/ce décodeur seulement. Les codecs avec perte, padding et profondeur plus grande ont leur propre corpus ; ne pas extrapoler FLAC à MP3/Opus.

## Prochain essai matériel discriminant

Sur l'ordinateur du salon, ajouter l'adaptateur GStreamer au même receiver et un mode PCM local utilisant exactement le même pipeline. Identifier USB/DDC et Terminator, lire descripteurs, capacités ALSA et modes I2S avant lecture. L'essai propose `hw:` exact et sans conversion, choix expérimental à consigner qui ne rétablit pas l'ancien contrat de volume partagé. Ne jamais augmenter automatiquement un niveau. Rejeter le format si le périphérique le refuse.
Comparer d'abord PCM local versus PCM reçu du serveur avec même fichier, même moteur, même format, même gain et mêmes connexions. Capturer le PCM juste avant appsrc et à l'entrée du puits, caps, clock choisi, propriétés d'asservissement, `hw_params`, compteurs XRUN et niveaux. Cette capture ne prouve pas les données électriques USB ni les clocks de conversion.
Enchaîner les deux pistes homogènes, puis une paire de fréquences différentes. Mesurer les ruptures numériques accessibles ; mesurer le relock et la sortie analogique si un ADC/analyseur adéquat est disponible. Le seuil gapless doit être convenu pour le corpus garanti. Arrêt et retour du pair et du DDC doivent laisser le système silencieux.
Puis comparer la référence Aurender, avec le même DDC/DAC, niveaux analogiques vérifiés, fichiers et réglages consignés. Si la liaison vers DDC diffère, l'attribution au seul streamer est impossible. Une écoute randomisée masquée et les réponses brutes peuvent avancer sans laboratoire complet. Une revendication analogique ou de jitter exige ensuite mesure calibrée, observation pointée et incertitude ; l'absence de mesure n'invalide pas l'expérience rapportée.

## Adoption et contrats encore ouverts

Le probe ne clôt aucun KV produit. Catalogue/scan/recherche : KV-002 à KV-005, fichiers intacts, corpus à échelle KV-013. File/playlists : KV-006 à KV-008. Reprise/restore : KV-010/011 avec interruption réelle. Audio : KV-009 doit être amendé pour ce trajet et volume ; matrix formats, délais/padding, transitions, chaînes réelles. Paquet : KV-001, build propre, versions et plugins exacts, installation offline ; accès pair et absence d'API LAN générale dans KV-012 amendé.
La licence de Kuro, les crates, les bindings, GStreamer et les plugins FFmpeg distribués exigent l'inventaire du paquet réellement livré. Le FFmpeg local déclare `--enable-gpl --enable-version3` ; cela ne décide pas de la licence du produit. Critères de rejet de B : incohérences d'état entre serveur/receiver, transformations non expliquées, mémoire non bornée, marge réseau insuffisante, intégration GStreamer trop coûteuse, ou avantage reproductible de la préparation locale sur la même chaîne. Aucun résultat synthétique ne ferme KB-010 à KB-015 ni KB-022.
