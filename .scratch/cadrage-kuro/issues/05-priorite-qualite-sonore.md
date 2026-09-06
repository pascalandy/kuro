# Donner la priorité à la qualité sonore

Type: task
Status: resolved
Assignee: scope_docs
Blocked by: 04

## Question

Comment intégrer la priorité sonore et le chemin réseau demandé sans choisir l'architecture avant l'étude ?

## Comments

### 2026-09-06. Ticket réclamé

Le worker `scope_docs` réclame ce ticket avant de modifier les documents courants. Le changement vient directement de l'utilisateur. Il ne s'agit pas d'une réponse déléguée pendant les anciens entretiens.

## Answer

Les décisions suivantes viennent de trois messages directs de l'utilisateur du 6 septembre 2026. Elles ont plus d'autorité que les arbitrages délégués des entretiens sur les points qu'elles modifient. Elles ne constituent aucun résultat technique ou sonore.

### KD-041. Faire de la qualité sonore le premier critère technique

La qualité sonore prime dans l'étude d'architecture et de transport. La référence d'écoute actuelle est un Aurender avec musique locale, commandé par Conductor 5, puis relié au DDC existant et au DAC Terminator par I2S sur HDMI. Cette référence exprime l'expérience à remplacer. Elle ne prouve aucune cause liée au logiciel, au transport, au jitter ou au matériel. L'étude précède le choix de la stack et le premier résultat produit.

### KD-042. Cibler un renderer distinct dans le salon

Le chemin cible relie le NAS au serveur kuro, puis à un ordinateur distinct dans le salon. Cet ordinateur reçoit les données par le réseau et sort en USB vers le DDC existant. Le DDC rejoint le DAC Terminator par I2S sur HDMI. Linux est une hypothèse initiale pour l'ordinateur du salon. Le fabricant du DDC a été nommé "Dynafripp" par l'utilisateur. Le fabricant exact, le modèle, la révision et ses capacités restent inconnus. Une connexion directe du serveur au DDC peut fournir un diagnostic comparatif. Elle ne remplace pas le renderer distinct demandé.

### KD-043. Réviser seulement les anciennes limites qui bloquent ce chemin

La sortie locale partagée de KD-020 et KD-039, ainsi que l'interdiction générale d'écoute sur le LAN de KD-022, décrivent le cadrage antérieur. Elles restent des décisions historiques en cours de réexamen pour le chemin vers un seul renderer. La disposition des 195 fonctions conserve sa classification antérieure pendant cette revue. Aucune reclassification en bloc n'est déduite du nouveau besoin.

Les sources restent en lecture seule. Les références, la file, les playlists, la sauvegarde et la reprise arrêtée restent durables. Le retour du NAS, du réseau ou de la sortie ne reprend pas le son automatiquement. Le produit continue de fonctionner sans Internet, à l'échelle d'environ 20 000 albums et 3 To. Le multiroom, le mobile, l'accès distant, le DSP et les endpoints génériques restent différés.

## Evidence

Un premier message fixe la priorité sonore. Un deuxième précise la référence Aurender avec musique locale et Conductor 5, ainsi que le nom "Dynafripp" sans modèle vérifiable. Un troisième précise que le remplacement est un ordinateur distinct dans le salon, alimenté par le réseau et relié en USB au DDC. Aucun matériel, protocole, prototype ou résultat d'écoute n'a été testé dans ce ticket.
