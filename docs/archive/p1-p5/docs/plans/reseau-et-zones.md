# Plan : réseau et zones

Piloter plusieurs sorties sans mélanger leurs files, puis synchroniser seulement les groupes compatibles.

Ce plan organise un domaine du produit futur. Il n’autorise ni ne constate une implémentation. [Roadmap](../roadmap.md) · [Architecture proposée](../architecture.md) · [Faisabilité](../faisabilite.md).

## Responsabilités et périmètre

La coordination réseau possède appairage, capacités, sessions de zone, transfert et groupement. Le transport audio traite format, tampon, horloge et dérive. Le plan couvre D09 réseau et l’accès des contrôleurs F13-005.

Le service reste l’autorité des commandes et identités. L’audio définit les capacités de sortie. Le client affiche zones et droits. L’exploitation protège les secrets et déploiements. L’accès à un montage NAS reste le travail bibliothèque M1.

## Exigences et exclusions

C-03, C-07 et C-09; E-04 et E-07 comme preuves réutilisées; F09-001 à F09-013, F09-015 et F13-005 selon couverture.

Ni ouverture LAN obligatoire en M1, ni RAAT requis, ni synchronisation déduite des commandes. Snapcast est candidat libre à comparer avant choix. Les protocoles tiers exigent leurs propres accès et matériels.

La [couverture canonique](../couverture.tsv) contient la liste exhaustive des fonctions dont la colonne `plan` désigne ce fichier. Elle conserve la milestone et la disposition du registre P2. Les regroupements ci-dessous nomment les contributions et leurs collaborateurs, sans changer le responsable canonique d’une fonction.

## Phases du domaine

Les dépendances locales et interdomaines exactes figurent dans chaque phase liée. Elles sont aussi représentées par le graphe documentaire de la roadmap. Les résultats et preuves restent futurs.

### 1. Appairer et autoriser

Phase produit : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01). Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06).

Refuser un tiers, révoquer un contrôleur puis tester deux auteurs concurrents. Dépend des identités et commandes M1, pas du DSP complet.

Critère observable et preuve : Modifier une file depuis deux contrôles puis révoquer l’un. [V-036](../validation.md#v-036) précise étapes, résultat, mesure, artefact et cas d’échec.

### 2. Livrer des zones indépendantes

Phase produit : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02). Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M1-P04](../milestones/m01-mvp-local.md#m1-p04).

Deux programmes simultanés, transfert de file, commandes matérielles et display. Une panne d’endpoint reste locale à sa session.

Critère observable et preuve : Écouter deux albums différents puis transférer une file. [V-037](../validation.md#v-037) précise étapes, résultat, mesure, artefact et cas d’échec.

### 3. Mesurer un groupe synchronisé

Phase produit : [M4-P03](../milestones/m04-reseau-domestique.md#m4-p03). Dépendances : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02).

Ajouter une horloge et correction de dérive après les zones indépendantes. Capturer plusieurs sorties à la fois sur une durée fixée.

Critère observable et preuve : Grouper deux zones, écouter puis retirer une sortie. [V-038](../validation.md#v-038) précise étapes, résultat, mesure, artefact et cas d’échec.

### 4. Qualifier les tiers sous conditions

Phase produit : [M4-P04](../milestones/m04-reseau-domestique.md#m4-p04). Dépendances : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02).

RAAT et chaque protocole ont une fiche d’accès et une matrice de modèles. Leur refus ne retarde pas le socle propre.

Critère observable et preuve : Découvrir puis lire sur l’appareil admis avec contrôle explicite. [V-039](../validation.md#v-039) précise étapes, résultat, mesure, artefact et cas d’échec.

### 5. Préparer l’accès distant mobile

Phase produit : [M7-P01](../milestones/m07-mobile.md#m7-p01). Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02), [M1-P05](../milestones/m01-mvp-local.md#m1-p05).

Collaborer sur identité, transport protégé, révocation et reprise. Le mobile ne devient pas autorité du catalogue.

Critère observable et preuve : Consulter une édition puis écouter à distance. [V-048](../validation.md#v-048) précise étapes, résultat, mesure, artefact et cas d’échec.

## Risques et acceptation

Risque majeur : état convergent mais sorties désynchronisées. V-038 mesure décalage et dérive, sans reprendre une garantie RAAT. Le budget dépend des appareils et doit être approuvé. Une topologie réseau non décrite ne produit pas de preuve reproductible.

Une revue de domaine vérifie les fonctions dont ce plan est responsable dans la couverture et les preuves des phases collaboratrices. L’absence de mesure interdit de déclarer la capacité démontrée. Les décisions de stack, de formats, de droits ou de budgets restent ouvertes jusqu’à leur adoption explicite.
