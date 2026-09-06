# Réconcilier le dossier et archiver le corpus initial

Type: task
Status: resolved
Assignee: docs_reconcile
Blocked by: 03

## Question

Après les deux entretiens, rendre le cadrage, la roadmap, le backlog et la traçabilité des 195 fonctions canoniques, puis archiver P1 à P5 sans perdre leurs preuves historiques.

## Answer

Le corpus P1 à P5 est archivé sous [`docs/archive/p1-p5/`](../../../docs/archive/p1-p5/README.md). Ses 36 fichiers reproduisent `README.md` et `docs/**` du commit `c478909` sans modifier leur contenu ni leur arborescence interne. Le [reçu de provenance](../../../docs/archive/p1-p5-source.md) et le manifeste SHA-256 permettent de comparer l'archive au commit source.

Le cadrage courant tient dans le glossaire, le cadrage, la roadmap, le backlog, les sources, la validation et la disposition fonctionnelle liés depuis le [`README.md`](../../../README.md). Les anciennes pages actives P1 à P5 n'occupent plus la racine de `docs/`.

[`docs/disposition-fonctions.tsv`](../../../docs/disposition-fonctions.tsv) attribue une disposition courante à chacun des 195 identifiants historiques. Chaque ligne cite sa décision `KD-*`, sa question `KB-*` lorsque le travail est différé ou étudié, sa portée exacte et un scénario `KV-*` lorsqu'elle participe à U-M1. Le générateur [`scripts/build_disposition.py`](../../../scripts/build_disposition.py) refuse les identifiants manquants ou ajoutés.

[`docs/validation.md`](../../../docs/validation.md) décrit treize scénarios futurs. Aucun n'est déclaré réussi, car kuro n'existe pas encore. La revue indépendante et le contrôle documentaire reproductible précèdent toute publication du nouvel état.

## Contrôle documentaire

La commande `python3 scripts/verify_docs.py` passe le 6 septembre 2026 avec 36 fichiers d'archive identiques au commit source, 195 dispositions uniques, 24 références de backlog utilisées et 53 fonctions rattachées à U-M1 avec une validation future. `git diff --check` passe aussi. Ces contrôles portent sur les documents. Ils ne testent aucun comportement du futur produit.
