# Plan : intégrations et découverte

Ajouter des données et écoutes externes quand leur accès est établi, avec retour permanent à la bibliothèque locale.

Ce plan organise un domaine du produit futur. Il n’autorise ni ne constate une implémentation. [Roadmap](../roadmap.md) · [Architecture proposée](../architecture.md) · [Faisabilité](../faisabilite.md).

## Responsabilités et périmètre

Chaque adaptateur possède normalisation des réponses, provenance, quotas et capacités admises. Le domaine conserve ses identités et corrections. Le plan couvre D10, D11, l’identification enrichie, MQA, HQPlayer et les droits fournisseurs.

La bibliothèque gère éditions et profils, le coordinateur reçoit les pistes autorisées, le client montre origine et indisponibilité. L’exploitation stocke les secrets et examine les droits. Aucun jeton ne traverse le modèle musical ou les exports.

## Exigences et exclusions

C-02, C-04, C-07 et C-08; E-08; O-07. Les données d’admission réutilisent la faisabilité P3 sans supposer les conditions encore valides au futur développement.

Pas de fournisseur obligatoire, de clé fournie, de réutilisation d’algorithme Roon ni de catalogue donnant implicitement droit de lecture. Cache, export et téléchargement sont des capacités distinctes. Toutes les entrées M5 restent conditionnelles.

La [couverture canonique](../couverture.tsv) contient la liste exhaustive des fonctions dont la colonne `plan` désigne ce fichier. Elle conserve la milestone et la disposition du registre P2. Les regroupements ci-dessous nomment les contributions et leurs collaborateurs, sans changer le responsable canonique d’une fonction.

## Phases du domaine

Les dépendances locales et interdomaines exactes figurent dans chaque phase liée. Elles sont aussi représentées par le graphe documentaire de la roadmap. Les résultats et preuves restent futurs.

### 1. Admettre séparément chaque capacité

Phase produit : [M5-P01](../milestones/m05-decouverte-et-integrations.md#m5-p01). Dépendances : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02).

Documenter compte, territoire, droits, cache, attribution et révocation. Une interdiction bloque son adaptateur, pas le local.

Critère observable et preuve : Désactiver le fournisseur puis écouter un album local. [V-040](../validation.md#v-040) précise étapes, résultat, mesure, artefact et cas d’échec.

### 2. Enrichir sans écraser

Phase produit : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02). Dépendances : [M5-P01](../milestones/m05-decouverte-et-integrations.md#m5-p01), [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02).

Provenance, correspondance et textes absents sont visibles. Les tags et corrections M2 gardent leur priorité.

Critère observable et preuve : Lire la provenance d’une biographie et suivre une relation de crédit. [V-041](../validation.md#v-041) précise étapes, résultat, mesure, artefact et cas d’échec.

### 3. Tester découverte et suite de file

Phase produit : [M5-P03](../milestones/m05-decouverte-et-integrations.md#m5-p03). Dépendances : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02), [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03).

Comparer profils et renouvellement, Listen Later, amorce et exclusions. Ne pas promettre l’algorithme de référence.

Critère observable et preuve : Choisir une découverte puis poursuivre une écoute depuis une amorce connue. [V-042](../validation.md#v-042) précise étapes, résultat, mesure, artefact et cas d’échec.

### 4. Lire et synchroniser selon droits

Phase produit : [M5-P04](../milestones/m05-decouverte-et-integrations.md#m5-p04). Dépendances : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02), [M2-P04](../milestones/m02-bibliotheque-avancee.md#m2-p04), [M1-P04](../milestones/m01-mvp-local.md#m1-p04).

Tester chaque fournisseur, les conflits aller-retour, matching et refus. Radio, écoutes, extensions, partage, HQPlayer et MQA gardent leur admission propre.

Critère observable et preuve : Lire un contenu autorisé, synchroniser une sélection puis revenir au local. [V-043](../validation.md#v-043), [V-044](../validation.md#v-044), [V-045](../validation.md#v-045) précise étapes, résultat, mesure, artefact et cas d’échec.

## Risques et acceptation

Risque majeur : confondre API de catalogue et droit au flux, ou effacer une playlist locale après retrait distant. V-040 et V-043 isolent ces preuves. Les contradictions P2 de playlists, éditions streaming et MQA restent visibles jusqu’à observation ou exclusion motivée.

Une revue de domaine vérifie les fonctions dont ce plan est responsable dans la couverture et les preuves des phases collaboratrices. L’absence de mesure interdit de déclarer la capacité démontrée. Les décisions de stack, de formats, de droits ou de budgets restent ouvertes jusqu’à leur adoption explicite.
