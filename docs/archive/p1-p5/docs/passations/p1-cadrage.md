# Passation P1 au coordinateur

P1 est validée. Le coordinateur a lu les six fichiers Markdown et le journal. Son contrôle indépendant a produit 6 Markdown, 13 liens locaux, 6 décisions et 0 erreur. Il a autorisé la finalisation Git locale de P1. Aucun push ou PR ne fait partie de cette finalisation.

## Travail terminé

Le dossier décrit les usages M1, dix critères MVP, sept décisions ouvertes et les paramètres inconnus. Il conserve la cible de 20 000 albums et environ 3 To dès M1, avec sources locales et NAS.

Le programme définit P1 à P5, les six domaines proposés pour les plans P4, les sept milestones, le checkpoint de débit et la fin vérifiable. Le corpus P1 garde les quatre adresses fournies par les chercheurs préparatoires. Aucun fait technique Roon n'est repris comme vérifié par P1.

Les principes Sequence work into verifiable units et Prove it works ont guidé deux choix concrets. P2 attend la revue P1. Les liens et le journal sont contrôlés sur les fichiers produits, sans confondre cette vérification documentaire avec un test du futur logiciel.

## Fichiers remis

| Fichier | Rôle |
| --- | --- |
| `README.md` | Sommaire des documents existants et statut |
| `docs/contexte-utilisateur.md` | Faits et autorisations transmis à P1 |
| `docs/programme.md` | Programme et critères de passage |
| `docs/produit-et-mvp.md` | Parcours, MVP et décisions ouvertes |
| `docs/checklist.md` | Suivi et exceptions aux playbooks |
| `docs/decisions.tsv` | Journal append-only |
| `docs/passations/p1-cadrage.md` | Cette passation |

## Vérifications P1

Depuis la racine du dépôt, `git symbolic-ref --short HEAD` a affiché `main`. `git status --short` a montré `?? README.md` et `?? docs/`. `git rev-parse --verify HEAD` a échoué avec `fatal: Needed a single revision`, puisqu'aucun commit n'existe encore.

Un contrôle Python ponctuel a parcouru les fichiers Markdown, résolu les liens locaux et les chemins de preuve du TSV. Il a contrôlé six colonnes par ligne et l'absence de cellules commençant par un préfixe de formule. Le résultat était `6 Markdown files, 13 local links, 5 decision rows, 0 errors`. Une sixième ligne de journal enregistre ce contrôle.

La liste `rg --files -g '!.git'` contient sept documents. Une recherche de marqueurs usuels de secrets et chemins personnels n'a trouvé aucun résultat. Cette recherche ne remplace pas la revue humaine du contenu avant publication.

## Limites et suite

Aucun produit kuro, logiciel Roon, média réel ou configuration audio n'a été exécuté ou inspecté. Aucun benchmark n'a été réalisé. Les formats, le nombre de pistes, le matériel serveur, le NAS et le DAC restent inconnus.

La revue indépendante du coordinateur a validé P1. La revue multimodèle prescrite par certains skills est écartée selon l'instruction utilisateur. Le skill deslop manque selon la recherche du coordinateur. La revue de prose directe et Unslop constituent le remplacement documentaire, sans réparation de skills.

P2 établit un inventaire serveur et desktop avec identifiants stables et statut de preuve par affirmation. P2 reconsulte les sources préparatoires, relève leurs dates et leurs limites, puis relie l'inventaire aux critères MVP. La checklist et le journal consignent le passage validé par le coordinateur.

Le coordinateur a autorisé un commit initial vide sur main, puis un commit documentaire P1 sur docs/plan-kuro. Après ces commits locaux, l'agent P1 cède les écritures au coordinateur. La publication reste confiée au coordinateur.
