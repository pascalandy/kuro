# kuro

kuro est un projet de bibliothèque musicale et de lecture audio destiné d'abord à Linux sur Omarchy. La cible initiale comprend des fichiers locaux et un dossier NAS, pour environ 20 000 albums et 3 To.

Ce dépôt contient le cadrage du produit. Aucun logiciel kuro n'existe encore. Le cadrage fixe les usages et les preuves attendues avant le développement, sans choisir une stack ni attribuer une licence.

La qualité sonore est désormais la priorité du projet. Le chemin cible part du NAS, passe par le serveur kuro et un ordinateur distinct dans le salon, puis rejoint le DDC existant en USB et le DAC Terminator en I2S sur HDMI. Linux sur l'ordinateur du salon reste une hypothèse de travail. Le [changement de portée demandé par l'utilisateur](docs/kickoff/scope-addendum.md) précède le choix du transport et de l'architecture. KD-041, KD-042.

La sortie locale partagée et l'absence d'écoute réseau décrivent le cadrage antérieur. Elles ne bloquent plus l'étude du chemin cible. Les 195 dispositions conservent leur classification antérieure pendant cette revue limitée. Elles ne prouvent pas que le nouveau chemin est réalisable ou accepté. KD-043.

## Lire le cadrage courant

| Document | Contenu |
| --- | --- |
| [Glossaire](CONTEXT.md) | Termes propres au cadrage |
| [Cadrage courant](docs/cadrage-courant.md) | Usages et contrats retenus après deux entretiens |
| [Roadmap](docs/roadmap.md) | Ordre des étapes et conditions de passage |
| [Backlog](docs/backlog.md) | Usages différés et études avant adoption |
| [Disposition des fonctions](docs/disposition-fonctions.tsv) | Disposition courante des 195 fonctions historiques |
| [Validation](docs/validation.md) | Scénarios futurs et preuves attendues |
| [Sources du cadrage](docs/sources-cadrage.md) | Sources externes consultées et limites de preuve |
| [Priorité sonore](docs/kickoff/scope-addendum.md) | Changement demandé par l'utilisateur et limites de l'étude |
| [Carte Wayfinder](.scratch/cadrage-kuro/map.md) | Index des décisions prises pendant les entretiens |

Les décisions détaillées vivent dans les tickets liés depuis la carte Wayfinder. Les identifiants `KD-*` relient les documents courants à ces décisions. Les identifiants `KB-*` désignent les questions du backlog. Les identifiants `KV-*` désignent les scénarios de validation.

## Consulter le corpus initial

Le [corpus P1 à P5 archivé](docs/archive/p1-p5/README.md) conserve le dossier préparatoire initial, ses hypothèses et ses preuves. Son [reçu de provenance](docs/archive/p1-p5-source.md) donne le commit source et la commande de contrôle.

Ce corpus historique n'est plus le cadrage courant. Ses milestones M1 à M7, ses dispositions et ses scénarios restent inchangés dans l'archive. La roadmap courante utilise les identifiants U-M1 à U-M4.

## Statut du projet

Le produit reste à développer. Aucun prototype n'est encore déclaré dans ce cadrage. L'étude de transport et de la chaîne audio précède le choix de la stack et le premier résultat produit. Les études de licence, de formats, de matériel et de NAS restent nécessaires. Roon fournit un corpus de comparaison documentaire, sans objectif de parité et sans preuve du comportement futur de kuro.
