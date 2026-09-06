# Plan : bibliothèque et métadonnées

Retrouver la même musique malgré réimport, copies, corrections ou changement d’emplacement.

Ce plan organise un domaine du produit futur. Il n’autorise ni ne constate une implémentation. [Roadmap](../roadmap.md) · [Architecture proposée](../architecture.md) · [Faisabilité](../faisabilite.md).

## Responsabilités et périmètre

Le service de bibliothèque possède catalogue, identités, index et collections durables. Le domaine musical définit album, édition, piste, œuvre et crédit selon le modèle proposé P3. Le plan couvre D02, D03 et les collections de D05 selon le TSV.

Le desktop possède la navigation, pas une seconde base. Le coordinateur possède la file courante. Les fournisseurs proposent des données avec provenance. L’exploitation possède sauvegarde et migrations. Bibliothèque et index restent locaux même si les médias sont sur NAS.

## Exigences et exclusions

C-01, C-02, C-06 et C-08; E-01, E-02 et E-05; MVP-02, MVP-03, MVP-04, MVP-07 et MVP-09.

Ni décodeur audio, ni écriture dans les tags sources, ni catalogue fournisseur obligatoire. Le schéma P3 reste conceptuel. SQLite et FTS5 sont candidats, sans migration SQL inventée.

La [couverture canonique](../couverture.tsv) contient la liste exhaustive des fonctions dont la colonne `plan` désigne ce fichier. Elle conserve la milestone et la disposition du registre P2. Les regroupements ci-dessous nomment les contributions et leurs collaborateurs, sans changer le responsable canonique d’une fonction.

## Phases du domaine

Les dépendances locales et interdomaines exactes figurent dans chaque phase liée. Elles sont aussi représentées par le graphe documentaire de la roadmap. Les résultats et preuves restent futurs.

### 1. Distinguer disponibilité et suppression

Phase produit : [M1-P02](../milestones/m01-mvp-local.md#m1-p02). Dépendances : [M1-P01](../milestones/m01-mvp-local.md#m1-p01).

Le scan par génération peut être repris. Copies et source relocalisée conservent leurs références. Une interruption NAS ne retire rien des playlists.

Critère observable et preuve : Importer les deux origines puis lire leurs albums. [V-002](../validation.md#v-002), [V-003](../validation.md#v-003), [V-004](../validation.md#v-004) précise étapes, résultat, mesure, artefact et cas d’échec.

### 2. Publier des requêtes et collections cohérentes

Phase produit : [M1-P03](../milestones/m01-mvp-local.md#m1-p03). Dépendances : [M1-P02](../milestones/m01-mvp-local.md#m1-p02).

Catalogue et index portent une révision. La pagination conserve un ordre stable. Playlist et occurrences ont leurs identités propres.

Critère observable et preuve : Trouver un album, sélectionner, écouter, réordonner et sauvegarder au clavier. [V-005](../validation.md#v-005), [V-006](../validation.md#v-006), [V-008](../validation.md#v-008), [V-015](../validation.md#v-015) précise étapes, résultat, mesure, artefact et cas d’échec.

### 3. Prouver la taille cible

Phase produit : [M1-P06](../milestones/m01-mvp-local.md#m1-p06). Dépendances : [M1-P05](../milestones/m01-mvp-local.md#m1-p05).

Coopérer avec le client et l’exploitation sur 20 000 albums et environ 3 To. Publier nombre réel de pistes, DB, cache et débit NAS.

Critère observable et preuve : Importer, naviguer, rechercher, écouter, redémarrer et restaurer sur matériel fixé. [V-016](../validation.md#v-016), [V-017](../validation.md#v-017), [V-020](../validation.md#v-020) précise étapes, résultat, mesure, artefact et cas d’échec.

### 4. Étendre import et éditions

Phase produit : [M2-P01](../milestones/m02-bibliotheque-avancee.md#m2-p01). Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06).

Importer dates, tags multivalués et playlists externes. Groupements, scissions et édition principale restent réversibles.

Critère observable et preuve : Importer un coffret et choisir son édition principale. [V-021](../validation.md#v-021), [V-022](../validation.md#v-022) précise étapes, résultat, mesure, artefact et cas d’échec.

### 5. Séparer corrections et observations

Phase produit : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02). Dépendances : [M2-P01](../milestones/m02-bibliotheque-avancee.md#m2-p01).

Une actualisation ne remplace pas une correction. Œuvres, interprétations, mouvements et crédits restent distincts.

Critère observable et preuve : Corriger un album puis trouver deux interprétations depuis le compositeur. [V-023](../validation.md#v-023), [V-024](../validation.md#v-024) précise étapes, résultat, mesure, artefact et cas d’échec.

### 6. Évaluer les collections avancées

Phase produit : [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03). Dépendances : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02).

Focus et Smart Playlists partagent les mêmes critères. Profils musicaux et tags ont une portée explicite.

Critère observable et preuve : Parcourir une œuvre, filtrer les versions, enregistrer une sélection puis changer de profil. [V-025](../validation.md#v-025), [V-026](../validation.md#v-026), [V-027](../validation.md#v-027) précise étapes, résultat, mesure, artefact et cas d’échec.

### 7. Exporter les sélections exactes

Phase produit : [M2-P04](../milestones/m02-bibliotheque-avancee.md#m2-p04). Dépendances : [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03).

Écrire dans une destination distincte, vérifier les copies et conserver les originaux. Restaurer aussi le modèle enrichi.

Critère observable et preuve : Exporter la sélection courante et retrouver ses corrections dans une restauration. [V-028](../validation.md#v-028), [V-029](../validation.md#v-029) précise étapes, résultat, mesure, artefact et cas d’échec.

### 8. Recevoir des enrichissements facultatifs

Phase produit : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02). Dépendances : [M5-P01](../milestones/m05-decouverte-et-integrations.md#m5-p01), [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02).

Les intégrations possèdent l’accès. La bibliothèque refuse qu’un identifiant fournisseur remplace les identités locales.

Critère observable et preuve : Lire la provenance d’une biographie et suivre une relation de crédit. [V-041](../validation.md#v-041) précise étapes, résultat, mesure, artefact et cas d’échec.

## Risques et acceptation

Risque majeur : confondre chemin et identité ou NAS absent et catalogue vide. V-003 impose retour de source et scan interrompu. Une base reconstruite mais playlists cassées échoue. Les requêtes relationnelles M2 devront conserver les budgets approuvés M1.

Une revue de domaine vérifie les fonctions dont ce plan est responsable dans la couverture et les preuves des phases collaboratrices. L’absence de mesure interdit de déclarer la capacité démontrée. Les décisions de stack, de formats, de droits ou de budgets restent ouvertes jusqu’à leur adoption explicite.
