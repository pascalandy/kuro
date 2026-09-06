# Suivi local des décisions

Les cartes Wayfinder de kuro utilisent des fichiers Markdown suivis par Git sous `.scratch/`. Elles ne créent pas d'issues GitHub.

## Organisation

- Une carte vit dans `.scratch/<effort>/map.md`.
- Une carte porte `Label: wayfinder:map`.
- Chaque ticket vit dans `.scratch/<effort>/issues/NN-<nom>.md`.
- `Type:` vaut `research`, `prototype`, `grilling` ou `task`.
- `Status:` vaut `open`, `claimed` ou `resolved`.
- `Assignee:` nomme la personne ou l'agent qui a réclamé le ticket. Une valeur `none` signifie que le ticket reste disponible.
- `Blocked by:` contient les numéros des tickets préalables ou `none`.

Le premier ticket `open`, non assigné, dont tous les préalables sont `resolved` constitue le prochain ticket disponible. Pour réclamer un ticket, passez son statut à `claimed` et renseignez `Assignee:` avant le travail. Pour le résoudre, ajoutez `## Answer`, passez son statut à `resolved`, puis ajoutez son titre lié et un résumé d'une ligne dans `Decisions so far` de la carte.

Les numéros de ticket sont propres à une carte. Ils ne remplacent pas les identifiants produit, fonctionnels ou de décision.
