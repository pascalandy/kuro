# Priorité sonore et chemin d'écoute cible

Ce document consigne les changements de portée donnés directement par l'utilisateur les 6 et 7 septembre 2026. Ils placent la qualité sonore au premier rang, précisent la référence Aurender, puis séparent les rôles logiques de leur déploiement. Ce document complète le cadrage issu des deux entretiens. Il ne choisit ni architecture, ni protocole, ni stack.

## Besoin confirmé

La qualité sonore prime dans les choix à venir. La référence d'écoute actuelle utilise un Aurender avec musique locale et Conductor 5, suivi du DDC existant et du DAC Terminator en I2S sur HDMI. Cette référence décrit l'expérience à remplacer. Elle n'impose ni le matériel Aurender, ni son logiciel, ni son protocole.

La première cible est le chemin local suivant :

`NAS -> KuroKor dans le salon -> USB -> DDC -> I2S sur HDMI -> DAC Terminator`

Un Kuro Client peut partager l'ordinateur de KuroKor ou fonctionner à distance. Son rôle de contrôle transmet les intentions et affiche l'état. L'ordinateur qui l'héberge peut aussi produire le son envoyé par KuroKor. Cette capacité n'impose pas une application ou un processus séparé. Linux est l'hypothèse initiale pour l'ordinateur du salon. Le fabricant du DDC a été nommé "Dynafripp" par l'utilisateur. Le fabricant exact, le modèle, la révision et les capacités USB ou d'horloge restent inconnus. KD-041, KD-042, KD-046.

Un autre scénario place KuroKor et le Kuro Client sur deux ordinateurs distincts, avec le NAS comme équipement de stockage. L'ordinateur du Kuro Client est alors le point de lecture. Une troisième destination peut utiliser un appareil supplémentaire, tel qu'un streamer commercial ou un ordinateur peu puissant. Les [scénarios de déploiement](../scenarios-deploiement.md) distinguent ces destinations. KD-046.

## Effet sur l'ancien cadrage

La sortie locale partagée et l'interdiction générale d'écoute sur le LAN ne sont plus des contraintes fermées pour tous les déploiements. L'ancienne lecture obligatoire en deux machines venait d'une interprétation désormais remplacée. KuroKor et Kuro Client désignent des rôles logiciels distincts qui peuvent partager un ordinateur. Leur séparation logique n'impose pas des applications ou des processus séparés. Le NAS est l'appareil qui conserve les médias maîtres.

Le NAS reste la source maîtresse des fichiers musicaux. Kuro lit ces fichiers et ne les modifie pas. KuroKor reste l'autorité distincte pour le catalogue, les playlists, la file et les autres données durables de Kuro. Cette fonction ne détermine pas l'emplacement physique de l'état de Kuro. Un emplacement NAS distinct pourrait accueillir des données applicatives ou des sauvegardes après étude, sans autoriser la modification des fichiers musicaux maîtres. La cible reste d'environ 20 000 albums et 3 To. Le multiroom, le mobile, l'accès distant et le DSP restent différés. UPnP reste un candidat pour un point réseau distinct et ne rend pas le multiroom automatique dans U-M1. KD-043, KD-046.

La disposition des 195 fonctions conserve sa classification antérieure pendant la revue de ce chemin réseau. Les lignes sur la sortie locale, le contrôle réseau et les endpoints sont des décisions historiques en cours de réexamen. Elles ne constituent ni une nouvelle classification, ni une preuve technique.

## Preuves requises avant un choix technique

L'étude doit comparer les transports licites et réalisables pour les scénarios retenus. Pour chaque candidat, elle décrit qui lit, décode, tamponne, transforme et cadence les données. Le chemin peut transporter un fichier, un flux encodé ou du PCM. Kuro possède les parties qu'il implémente, sans revendiquer les tampons internes d'un appareil tiers. L'étude distingue le rythme des paquets réseau, la consommation logicielle du point de lecture et l'horloge physique de conversion.

Un essai synthétique peut prouver l'intégrité des données reçues, une corruption volontaire, une coupure ou une livraison tardive selon un modèle déclaré. Il ne mesure pas le jitter du DAC. Toute affirmation sur la qualité sonore, le jitter physique, la compatibilité du DDC ou la transparence du chemin demande une observation adaptée sur le matériel connu.

L'étude d'architecture et de transport précède le choix de la stack et le premier résultat produit. Elle évalue Rust en priorité pour les parties audio possédées par Kuro, sans appliquer cette exigence au matériel ou au logiciel interne d'un appareil tiers. Elle ne choisit pas encore Rust comme langage de production et ne demande pas de porter le laboratoire Go. MPD reste une référence testée pour comparer les moteurs, sans choix exclusif. Sa fin ne vaut ni acceptation de U-M1, ni preuve de supériorité sonore. Aucun produit ou prototype n'est déclaré livré par le présent addendum. KD-046.
