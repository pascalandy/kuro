# Priorité sonore et chemin d'écoute cible

Ce document consigne le changement de portée donné directement par l'utilisateur dans trois messages du 6 septembre 2026. Le premier place la qualité sonore au premier rang. Le deuxième précise la référence Aurender. Le troisième précise le remplacement par un ordinateur distinct dans le salon, relié en USB au DDC. Ce document complète le cadrage issu des deux entretiens. Il ne choisit ni architecture, ni protocole, ni stack.

## Besoin confirmé

La qualité sonore prime dans les choix à venir. La référence d'écoute actuelle utilise un Aurender avec musique locale et Conductor 5, suivi du DDC existant et du DAC Terminator en I2S sur HDMI. Cette référence décrit l'expérience à remplacer. Elle n'impose ni le matériel Aurender, ni son logiciel, ni son protocole.

Le chemin cible est le suivant :

`NAS -> serveur kuro -> ordinateur distinct dans le salon -> USB -> DDC -> I2S sur HDMI -> DAC Terminator`

L'ordinateur du salon remplit le rôle de renderer réseau. Linux est l'hypothèse initiale pour cet ordinateur. Le fabricant du DDC a été nommé "Dynafripp" par l'utilisateur. Le fabricant exact, le modèle, la révision et les capacités USB ou d'horloge restent inconnus. KD-041, KD-042.

## Effet sur l'ancien cadrage

La sortie locale partagée et l'interdiction générale d'écoute sur le LAN ne sont plus des contraintes fermées pour ce chemin. Un transport entre le serveur et un seul renderer doit être étudié. Cette ouverture ne donne pas un accès général au contrôle de kuro depuis le LAN.

Les contrats sur les sources en lecture seule, les références durables, le NAS absent, la file, les playlists, la sauvegarde, le fonctionnement sans Internet et l'absence de reprise automatique restent en vigueur. La cible reste d'environ 20 000 albums et 3 To. Le multiroom, le mobile, l'accès distant, le DSP et la prise en charge générique de plusieurs endpoints restent différés. KD-043.

La disposition des 195 fonctions conserve sa classification antérieure pendant la revue de ce chemin réseau. Les lignes sur la sortie locale, le contrôle réseau et les endpoints sont des décisions historiques en cours de réexamen. Elles ne constituent ni une nouvelle classification, ni une preuve technique.

## Preuves requises avant un choix technique

L'étude doit comparer les transports licites et réalisables vers le renderer. Pour chaque candidat, elle décrit qui lit, décode, tamponne, transforme et cadence les données. Elle distingue le rythme des paquets réseau, la consommation logicielle du renderer et l'horloge physique de conversion.

Un essai synthétique peut prouver l'intégrité des données reçues, une corruption volontaire, une coupure ou une livraison tardive selon un modèle déclaré. Il ne mesure pas le jitter du DAC. Toute affirmation sur la qualité sonore, le jitter physique, la compatibilité du DDC ou la transparence du chemin demande une observation adaptée sur le matériel connu.

L'étude d'architecture et de transport précède le choix de la stack et le premier résultat produit. Sa fin ne vaut ni acceptation de U-M1, ni preuve de supériorité sonore. Aucun produit ou prototype n'est déclaré livré par le présent addendum.
