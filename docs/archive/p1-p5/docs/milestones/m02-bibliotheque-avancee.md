# M2. Organiser éditions, classique et sélections

Plan produit futur, non exécuté. [M2 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne corrige un coffret, distingue deux interprétations, retrouve une œuvre avec Focus, sauvegarde une sélection dynamique et exporte une copie vérifiée.

## Critères d’entrée

M1 livré avec C-01, C-02, C-03 et C-06 stabilisés. Préparer un corpus de copies, homonymes, mouvements et crédits. Fixer les champs d’édition après examen des contradictions P2.

## Critères de sortie

Les fonctions M2 retenues ont des preuves d’identité, de corrections préservées, de recherche et d’export. Les sauvegardes restaurent les nouvelles structures. Les invariants de sources intactes et de performance M1 restent vérifiés.

## Périmètre et conditions

M2 ne dépend pas du DSP M3 ni d’un catalogue externe M5. Les correspondances locales et corrections doivent fonctionner sans fournisseur. Le nettoyage reste une proposition, avec prévisualisation et décision explicite.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M2. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M2-P01

### Importer les éditions et structures avancées

Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06)

Étendre les observations d’import et identités pour éditions, copies, playlists de fichiers et structures multidisques. Préserver les données M1 lors de migration.

Responsabilités : domaine musical et bibliothèque, avec desktop et exploitation. Zones futures : metadata, importers et migrations. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Tags multivalués, chemins relatifs et groupements réversibles. |
| Intégration | Migration d’une base M1 et réimport sans perte de références. |
| Parcours réel | Importer un coffret et choisir son édition principale. |
| Performance pertinente | Mesurer coût du réimport et requêtes d’éditions sur volume cible. |

Scénarios : [V-021](../validation.md#v-021), [V-022](../validation.md#v-022). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M2-P02

### Corriger et relier les œuvres

Dépendances : [M2-P01](../milestones/m02-bibliotheque-avancee.md#m2-p01)

Conserver observations et corrections séparées. Ajouter crédits, œuvres, interprétations et mouvements, avec provenance et homonymes explicites.

Responsabilités : domaine musical avec catalogue et desktop. Zones futures : metadata, works et credits. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Priorité des valeurs, relations multiples et regroupements de genres. |
| Intégration | Actualisation qui conserve les corrections et migrations restaurables. |
| Parcours réel | Corriger un album puis trouver deux interprétations depuis le compositeur. |
| Performance pertinente | Mesurer requêtes relationnelles et invalidation d’index, sans suspendre la lecture. |

Scénarios : [V-023](../validation.md#v-023), [V-024](../validation.md#v-024). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M2-P03

### Retrouver et organiser des sélections avancées

Dépendances : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02)

Livrer Focus, profils musicaux, tags, bookmarks, Smart Playlists et vues associées. Conserver le clavier et les états vides utiles.

Responsabilités : desktop et bibliothèque avec coordinateur pour historique d’écoute. Zones futures : desktop, query, collections et profiles. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Tables de vérité conjointes, alternatives et négatives, portée des profils. |
| Intégration | Recalcul après nouvel import, ban et réouverture d’un bookmark. |
| Parcours réel | Parcourir une œuvre, filtrer les versions, enregistrer une sélection puis changer de profil. |
| Performance pertinente | Comparer p95 des filtres composés et délai de recalcul à des budgets approuvés. |

Scénarios : [V-025](../validation.md#v-025), [V-026](../validation.md#v-026), [V-027](../validation.md#v-027). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M2-P04

### Exporter et protéger le travail enrichi

Dépendances : [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03)

Exporter sélection, catalogue et copies vers une destination distincte. Planifier des sauvegardes et restaurer deux points contenant les nouvelles structures.

Responsabilités : bibliothèque avec exploitation et desktop. Zones futures : exports, backup et migrations. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Mapping des champs, sélection exacte et dépendances de sauvegardes. |
| Intégration | M3U relue ailleurs, empreintes originales intactes et restauration de chaque point. |
| Parcours réel | Exporter la sélection courante et retrouver ses corrections dans une restauration. |
| Performance pertinente | Mesurer volumes exportés et temps de sauvegarde pendant lecture. |

Scénarios : [V-028](../validation.md#v-028), [V-029](../validation.md#v-029). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Les plans concernés sont :

- [Bibliothèque et métadonnées](../plans/bibliotheque-et-metadonnees.md)
- [Client ordinateur](../plans/client-ordinateur.md)
- [Installation et exploitation](../plans/installation-et-exploitation.md)
- [Moteur audio](../plans/moteur-audio.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
