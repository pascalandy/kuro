# kuro

kuro est un projet de bibliothèque musicale et de lecture audio, destiné d'abord à Linux sur Omarchy. La cible initiale comprend des fichiers locaux et un dossier NAS, pour environ 20 000 albums et 3 To.

Ce dépôt contient le dossier préparatoire. Aucun logiciel kuro n'existe dans ce dépôt. Le programme autorisé couvre les phases documentaires P1 à P5. Il s'arrête avant tout développement.

Pour commencer, lire la [revue finale](docs/revue-finale.md) et les [décisions ouvertes](docs/decisions-ouvertes.md). La roadmap donne ensuite les six plans et les sept milestones futures.

## Lire le dossier

| Document | Contenu |
| --- | --- |
| [Revue finale P5](docs/revue-finale.md) | Couverture des dix usages et dix critères MVP, constats et limites |
| [Décisions ouvertes](docs/decisions-ouvertes.md) | Neuf arbitrages, responsables, informations manquantes et effet sur la suite |
| [Passation P5](docs/passations/p5-revue.md) | Revue indépendante validée et contrôle complet rejouable |
| [Contexte utilisateur](docs/contexte-utilisateur.md) | Demande confirmée, autorisations et informations manquantes |
| [Programme](docs/programme.md) | Phases, critères de passage et définition de fin |
| [Produit et MVP](docs/produit-et-mvp.md) | Usages, frontière du MVP et décisions ouvertes |
| [Inventaire Roon](docs/inventaire-roon.md) | Couverture, méthode, contradictions et limites de preuve |
| [Registre fonctionnel](docs/inventaire-fonctions.tsv) | Fonctions identifiées, sources et dispositions provisoires |
| [Sources](docs/sources.md) | Corpus primaire daté et référence interne |
| [Architecture proposée](docs/architecture.md) | Trois formes comparées, recommandation et contrats documentaires |
| [Faisabilité](docs/faisabilite.md) | Composants, licences, fournisseurs, études futures et décisions ouvertes |
| [Sources techniques](docs/sources-techniques.md) | Registre primaire TECH de P3, distinct des sources Roon |
| [Roadmap](docs/roadmap.md) | Six plans, sept milestones et dépendances des 28 phases futures |
| [Validation](docs/validation.md) | Corpus, mesures et 50 scénarios futurs avec cas fonctionnels conservés |
| [Couverture](docs/couverture.tsv) | Traçabilité des 195 fonctions vers responsable, phase et scénario |
| [Passation P4](docs/passations/p4-multiplan.md) | Plans validés et contrôle documentaire reproductible |
| [Passation P3](docs/passations/p3-architecture.md) | Architecture validée et contrôles documentaires |
| [Passation P2](docs/passations/p2-inventaire.md) | Inventaire validé et vérifications |
| [Checklist](docs/checklist.md) | Progression et adaptation des playbooks au travail documentaire |
| [Journal des décisions](docs/decisions.tsv) | Décisions datées et preuves locales |
| [Passation P1](docs/passations/p1-cadrage.md) | Résultat remis au coordinateur avant P2 |

P1 à P5 sont validées par le coordinateur. P5 a été relue par un nouvel agent GPT-6 Astra medium, puis contrôlée indépendamment par le coordinateur. La publication est une opération séparée. Les livrables documentaires ne sont pas des fonctionnalités disponibles.

## Statut du projet

Le projet est destiné à devenir open source. Le choix de licence reste ouvert et aucune licence n'est attribuée par défaut.

Roon fournit un corpus de comparaison documentaire. Aucune parité exhaustive n'est démontrée et Roon n'a pas été exécuté pendant ce cadrage. kuro ne suppose aucun accès à RAAT pour son MVP.
