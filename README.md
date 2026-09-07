# kuro

kuro est un projet de bibliothèque musicale et de lecture audio destiné d'abord à Linux sur Omarchy. La cible initiale comprend des fichiers locaux et un dossier NAS, pour environ 20 000 albums et 3 To.

Ce dépôt contient le cadrage du produit et un prototype technique relançable. Le [laboratoire Go](experiments/transport/go.mod) éprouve le transfert HTTP sur loopback, l'admission atomique et un modèle de lecture progressive face à la préparation complète. Un second laboratoire vérifie le trajet FLAC et le décodage silencieux par MPD. [Relancer les preuves](docs/kickoff/verification.md).

La qualité sonore est désormais la priorité du projet. `KuroKor` désigne le rôle central qui possède l'état durable de Kuro et coordonne la lecture. Un `Kuro Client` envoie les intentions de l'utilisateur et affiche l'état. L'ordinateur qui l'héberge peut aussi fournir la lecture locale. Le NAS reste la source maîtresse des fichiers musicaux, distincte de l'état durable de Kuro. Ces rôles logiques ne fixent ni le nombre de machines, ni les limites d'une application ou d'un processus. Le [changement de portée demandé par l'utilisateur](docs/kickoff/scope-addendum.md) précède le choix du transport et de l'architecture. KD-041, KD-046.

Les [scénarios de déploiement](docs/scenarios-deploiement.md) retiennent trois destinations possibles. KuroKor peut lire sur sa sortie locale existante. Il peut aussi envoyer le média à l'ordinateur qui héberge un Kuro Client, où l'utilisateur écoute. Une option ultérieure peut viser un streamer commercial ou un ordinateur peu puissant, par exemple de la famille Raspberry Pi. Aucun protocole, modèle ou niveau de capacité n'est encore adopté pour cette troisième destination. KD-046.

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
| [Scénarios de déploiement](docs/scenarios-deploiement.md) | Rôles logiques et hébergements envisagés |
| [Architecture de démarrage](docs/kickoff/architecture.md) | Rôles courants et candidats techniques déjà éprouvés |
| [Synthèse de l'arena](docs/kickoff/synthesis.md) | Choix, rejets et résultats des laboratoires |
| [Vérification du prototype](docs/kickoff/verification.md) | Commandes relançables, résultats et limites de preuve |
| [Journal de décisions](docs/kickoff/decisions.tsv) | Décisions et preuves du kickoff |
| [Carte Wayfinder](.scratch/cadrage-kuro/map.md) | Index des décisions prises pendant les entretiens |

Les décisions détaillées vivent dans les tickets liés depuis la carte Wayfinder. Les identifiants `KD-*` relient les documents courants à ces décisions. Les identifiants `KB-*` désignent les questions du backlog. Les identifiants `KV-*` désignent les scénarios de validation.

## Consulter le corpus initial

Le [corpus P1 à P5 archivé](docs/archive/p1-p5/README.md) conserve le dossier préparatoire initial, ses hypothèses et ses preuves. Son [reçu de provenance](docs/archive/p1-p5-source.md) donne le commit source et la commande de contrôle.

Ce corpus historique n'est plus le cadrage courant. Ses milestones M1 à M7, ses dispositions et ses scénarios restent inchangés dans l'archive. La roadmap courante utilise les identifiants U-M1 à U-M4.

## Statut du projet

Le produit reste à développer. Le laboratoire Go et les essais MPD restent des preuves techniques utiles, pas des choix exclusifs pour le produit. L'étude évalue Rust en priorité pour les parties audio que Kuro possède. Cette priorité ne s'étend pas au matériel ou au logiciel interne d'un streamer tiers. Elle ne vaut ni adoption de Rust, ni portage du laboratoire. Le dépôt ne contient encore ni bibliothèque utilisable, ni interface, ni installation produit, ni agent de session. Les essais silencieux ne garantissent pas la qualité sonore sur USB, le DDC, I2S, le DAC ou la chaîne analogique. Les études de licence, de formats, de matériel et de NAS restent nécessaires. Roon fournit un corpus de comparaison documentaire, sans objectif de parité, sans adoption implicite du DSP et sans preuve du comportement futur de kuro. KD-046.
