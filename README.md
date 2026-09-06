# kuro

kuro est un projet de bibliothèque musicale et de lecture audio destiné d'abord à Linux sur Omarchy. La cible initiale comprend des fichiers locaux et un dossier NAS, pour environ 20 000 albums et 3 To.

Ce dépôt contient le cadrage du produit. Aucun logiciel kuro n'existe encore. Le cadrage fixe les usages et les preuves attendues avant le développement, sans choisir une stack ni attribuer une licence.

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
| [Carte Wayfinder](.scratch/cadrage-kuro/map.md) | Index des décisions prises pendant les entretiens |

Les décisions détaillées vivent dans les tickets liés depuis la carte Wayfinder. Les identifiants `KD-*` relient les documents courants à ces décisions. Les identifiants `KB-*` désignent les questions du backlog. Les identifiants `KV-*` désignent les scénarios de validation.

## Consulter le corpus initial

Le [corpus P1 à P5 archivé](docs/archive/p1-p5/README.md) conserve le dossier préparatoire initial, ses hypothèses et ses preuves. Son [reçu de provenance](docs/archive/p1-p5-source.md) donne le commit source et la commande de contrôle.

Ce corpus historique n'est plus le cadrage courant. Ses milestones M1 à M7, ses dispositions et ses scénarios restent inchangés dans l'archive. La roadmap courante utilise les identifiants U-M1 à U-M4.

## Statut du projet

Le produit reste à développer. Les études de licence, de stack, de formats, de matériel et de NAS précèdent les choix techniques concernés. Roon fournit un corpus de comparaison documentaire, sans objectif de parité et sans preuve du comportement futur de kuro.
