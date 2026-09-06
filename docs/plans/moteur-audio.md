# Plan : moteur audio

Entendre la piste réellement choisie et connaître les transformations qui atteignent la sortie.

Ce plan organise un domaine du produit futur. Il n’autorise ni ne constate une implémentation. [Roadmap](../roadmap.md) · [Architecture proposée](../architecture.md) · [Faisabilité](../faisabilite.md).

## Responsabilités et périmètre

Le coordinateur possède une file canonique et ses transitions. L’adaptateur traduit cette intention vers un moteur réutilisé et remonte son état observé. Décodage, tampons et périphérique appartiennent au moteur. Le plan couvre D06 à D08, hors intégrations conditionnelles confiées au plan fournisseurs.

Le client envoie des commandes avec révision. La bibliothèque fournit les références de médias et leur disponibilité. L’exploitation conserve l’état C-06 et borne les tâches. Le réseau ajoute sessions et horloges en M4, sans créer une seconde file moteur.

## Exigences et exclusions

C-03 à C-06, C-08 et C-09; E-03 et E-04; MVP-05, MVP-06 et MVP-07.

Aucun décodeur maison ni moteur choisi par la rédaction. libmpv, MPD et GStreamer restent à éprouver. M1 ne requiert ni exclusif, ni DSD, ni DSP complet. MQA et HQPlayer restent des admissions M5.

La [couverture canonique](../couverture.tsv) contient la liste exhaustive des fonctions dont la colonne `plan` désigne ce fichier. Elle conserve la milestone et la disposition du registre P2. Les regroupements ci-dessous nomment les contributions et leurs collaborateurs, sans changer le responsable canonique d’une fonction.

## Phases du domaine

Les dépendances locales et interdomaines exactes figurent dans chaque phase liée. Elles sont aussi représentées par le graphe documentaire de la roadmap. Les résultats et preuves restent futurs.

### 1. Entendre la première tranche

Phase produit : [M1-P01](../milestones/m01-mvp-local.md#m1-p01). Dépendances : critères d’entrée de M1.

Comparer commande acceptée et son réel sur une sortie identifiée. La petite fixture départage les moteurs, sans valider le volume cible.

Critère observable et preuve : Démarrer, choisir une piste, écouter puis reconnecter après fermeture de fenêtre. [V-001](../validation.md#v-001), [V-007](../validation.md#v-007), [V-009](../validation.md#v-009), [V-019](../validation.md#v-019) précise étapes, résultat, mesure, artefact et cas d’échec.

### 2. Modifier la file sans double autorité

Phase produit : [M1-P03](../milestones/m01-mvp-local.md#m1-p03). Dépendances : [M1-P02](../milestones/m01-mvp-local.md#m1-p02).

Invalider la préparation suivante après réordre. Les événements d’une ancienne session n’avancent jamais la nouvelle file.

Critère observable et preuve : Trouver un album, sélectionner, écouter, réordonner et sauvegarder au clavier. [V-005](../validation.md#v-005), [V-006](../validation.md#v-006), [V-008](../validation.md#v-008), [V-015](../validation.md#v-015) précise étapes, résultat, mesure, artefact et cas d’échec.

### 3. Prouver jonctions et erreurs

Phase produit : [M1-P04](../milestones/m01-mvp-local.md#m1-p04). Dépendances : [M1-P03](../milestones/m01-mvp-local.md#m1-p03).

Mesurer le corpus gapless, padding MP3 et AAC, changements de fréquence, perte du DAC et NAS lent. Tester crash entre mutation et accusé.

Critère observable et preuve : Écouter les paires, modifier la file et retrouver un état explicite après incident. [V-010](../validation.md#v-010), [V-011](../validation.md#v-011), [V-012](../validation.md#v-012), [V-013](../validation.md#v-013) précise étapes, résultat, mesure, artefact et cas d’échec.

### 4. Lire pendant le travail de fond

Phase produit : [M1-P06](../milestones/m01-mvp-local.md#m1-p06). Dépendances : [M1-P05](../milestones/m01-mvp-local.md#m1-p05).

Priorité à la préparation audio pendant scan, recherche et sauvegarde à l’échelle cible.

Critère observable et preuve : Importer, naviguer, rechercher, écouter, redémarrer et restaurer sur matériel fixé. [V-016](../validation.md#v-016), [V-017](../validation.md#v-017), [V-020](../validation.md#v-020) précise étapes, résultat, mesure, artefact et cas d’échec.

### 5. Rapporter la vérité de la sortie

Phase produit : [M3-P01](../milestones/m03-audio-audiophile.md#m3-p01). Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06).

Afficher source, décodage, transformations et format effectif. Inconnu reste inconnu.

Critère observable et preuve : Choisir une sortie et lire en vérifiant chaque étape affichée. [V-030](../validation.md#v-030) précise étapes, résultat, mesure, artefact et cas d’échec.

### 6. Analyser avec marge de calcul

Phase produit : [M3-P02](../milestones/m03-audio-audiophile.md#m3-p02). Dépendances : [M3-P01](../milestones/m03-audio-audiophile.md#m3-p01).

Loudness et ReplayGain suivent une priorité testée. Les créneaux d’analyse ne privent pas l’audio de ressources.

Critère observable et preuve : Analyser une sélection puis comparer normalisation piste et album. [V-031](../validation.md#v-031) précise étapes, résultat, mesure, artefact et cas d’échec.

### 7. Mesurer chaque traitement

Phase produit : [M3-P03](../milestones/m03-audio-audiophile.md#m3-p03). Dépendances : [M3-P02](../milestones/m03-audio-audiophile.md#m3-p02).

Comparer réponse, impulsion, gain et délais. Fondu et gapless gardent des preuves distinctes.

Critère observable et preuve : Choisir un preset, comparer le bypass puis réécouter l’album gapless. [V-032](../validation.md#v-032), [V-035](../validation.md#v-035) précise étapes, résultat, mesure, artefact et cas d’échec.

### 8. Qualifier les capacités spécialisées

Phase produit : [M3-P04](../milestones/m03-audio-audiophile.md#m3-p04). Dépendances : [M3-P03](../milestones/m03-audio-audiophile.md#m3-p03).

DSD, multicanal et profils requièrent matériel, données et licences disponibles.

Critère observable et preuve : Sélectionner un profil puis lire un signal DSD ou multicanal admis. [V-033](../validation.md#v-033), [V-034](../validation.md#v-034) précise étapes, résultat, mesure, artefact et cas d’échec.

### 9. Fournir une session par endpoint

Phase produit : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02). Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M1-P04](../milestones/m01-mvp-local.md#m1-p04).

Réutiliser les preuves audio nécessaires au format réseau retenu. Tout M3 n’est pas préalable.

Critère observable et preuve : Écouter deux albums différents puis transférer une file. [V-037](../validation.md#v-037) précise étapes, résultat, mesure, artefact et cas d’échec.

## Risques et acceptation

Risque majeur : prendre un accusé pour du son, ou masquer une coupure par un fondu. V-008 et V-011 observent les transitions et captures. Un moteur qui échoue aux formats indispensables est à remplacer avant adoption. Une capture virtuelle ne prouve pas le signal physique du DAC.

Une revue de domaine vérifie les fonctions dont ce plan est responsable dans la couverture et les preuves des phases collaboratrices. L’absence de mesure interdit de déclarer la capacité démontrée. Les décisions de stack, de formats, de droits ou de budgets restent ouvertes jusqu’à leur adoption explicite.
