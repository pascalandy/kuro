# Plan : client ordinateur

Trouver un album et agir sur l’écoute avec une interface réactive et compréhensible sur Linux Omarchy.

Ce plan organise un domaine du produit futur. Il n’autorise ni ne constate une implémentation. [Roadmap](../roadmap.md) · [Architecture proposée](../architecture.md) · [Faisabilité](../faisabilite.md).

## Responsabilités et périmètre

Le desktop possède navigation, sélection, préférences d’affichage et cache temporaire. Il consomme les contrats de requêtes et commandes du service. Le plan couvre D04, les interactions desktop et l’horizon client D15. Ce rattachement de D15 n’impose pas un framework mobile.

La bibliothèque calcule les résultats et persiste les collections. L’audio rapporte la lecture effective. Le réseau gère autorisation et reconnexion. L’exploitation gère versions, paquet et journaux. Le desktop n’écrit pas directement la base et ne commande pas directement le moteur.

## Exigences et exclusions

C-02, C-03, C-05, C-06, C-07 et C-09; E-06 et E-07; MVP-01, MVP-04 et MVP-05.

Pas de framework adopté aujourd’hui. Tauri, Qt et Electron se comparent sur les mêmes preuves. La recherche ne dépend pas du navigateur audio. Les vues avancées M2 et les contenus externes M5 ne deviennent pas M1.

La [couverture canonique](../couverture.tsv) contient la liste exhaustive des fonctions dont la colonne `plan` désigne ce fichier. Elle conserve la milestone et la disposition du registre P2. Les regroupements ci-dessous nomment les contributions et leurs collaborateurs, sans changer le responsable canonique d’une fonction.

## Phases du domaine

Les dépendances locales et interdomaines exactes figurent dans chaque phase liée. Elles sont aussi représentées par le graphe documentaire de la roadmap. Les résultats et preuves restent futurs.

### 1. Contrôler un album local

Phase produit : [M1-P01](../milestones/m01-mvp-local.md#m1-p01). Dépendances : critères d’entrée de M1.

Ouvrir un service local identifié, lire et reconnecter après fermeture. Afficher l’état observé distinct de la commande acceptée.

Critère observable et preuve : Démarrer, choisir une piste, écouter puis reconnecter après fermeture de fenêtre. [V-001](../validation.md#v-001), [V-007](../validation.md#v-007), [V-009](../validation.md#v-009), [V-019](../validation.md#v-019) précise étapes, résultat, mesure, artefact et cas d’échec.

### 2. Naviguer et manipuler au clavier

Phase produit : [M1-P03](../milestones/m01-mvp-local.md#m1-p03). Dépendances : [M1-P02](../milestones/m01-mvp-local.md#m1-p02).

Albums, artistes, pistes, recherche, playlists et file. Prévoir erreurs, état vide et propositions d’accessibilité.

Critère observable et preuve : Trouver un album, sélectionner, écouter, réordonner et sauvegarder au clavier. [V-005](../validation.md#v-005), [V-006](../validation.md#v-006), [V-008](../validation.md#v-008), [V-015](../validation.md#v-015) précise étapes, résultat, mesure, artefact et cas d’échec.

### 3. Rester utilisable à la taille cible

Phase produit : [M1-P06](../milestones/m01-mvp-local.md#m1-p06). Dépendances : [M1-P05](../milestones/m01-mvp-local.md#m1-p05).

Virtualiser listes et charger les seules pochettes utiles. Mesurer première page visible et RSS sur cache froid et chaud.

Critère observable et preuve : Importer, naviguer, rechercher, écouter, redémarrer et restaurer sur matériel fixé. [V-016](../validation.md#v-016), [V-017](../validation.md#v-017), [V-020](../validation.md#v-020) précise étapes, résultat, mesure, artefact et cas d’échec.

### 4. Explorer les données enrichies locales

Phase produit : [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03). Dépendances : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02).

Focus, versions, classique, profils, dossiers, livrets et collections restent navigables au clavier.

Critère observable et preuve : Parcourir une œuvre, filtrer les versions, enregistrer une sélection puis changer de profil. [V-025](../validation.md#v-025), [V-026](../validation.md#v-026), [V-027](../validation.md#v-027) précise étapes, résultat, mesure, artefact et cas d’échec.

### 5. Reprendre le contrôle sur le LAN

Phase produit : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01). Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06).

Version et permissions sont explicites. Après événement perdu, relire un instantané au lieu d’inventer l’état.

Critère observable et preuve : Modifier une file depuis deux contrôles puis révoquer l’un. [V-036](../validation.md#v-036) précise étapes, résultat, mesure, artefact et cas d’échec.

### 6. Porter les parcours retenus

Phase produit : [M6-P01](../milestones/m06-desktop-et-distribution.md#m6-p01). Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06).

Refaire les usages sur chaque OS, avec permissions et backend réel. Les capacités avancées portées ajoutent leurs propres dépendances.

Critère observable et preuve : Rejouer les usages M1 sur chaque plateforme annoncée. [V-046](../validation.md#v-046) précise étapes, résultat, mesure, artefact et cas d’échec.

### 7. Réutiliser les contrats à distance

Phase produit : [M7-P01](../milestones/m07-mobile.md#m7-p01). Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02), [M1-P05](../milestones/m01-mvp-local.md#m1-p05).

Horizon uniquement. Valider identités, accès sécurisé et reprise avant de détailler l’interface mobile.

Critère observable et preuve : Consulter une édition puis écouter à distance. [V-048](../validation.md#v-048) précise étapes, résultat, mesure, artefact et cas d’échec.

### 8. Lire une copie autorisée sans réseau

Phase produit : [M7-P02](../milestones/m07-mobile.md#m7-p02). Dépendances : [M7-P01](../milestones/m07-mobile.md#m7-p01).

L’état de téléchargement distingue partiel, complet et invalide. La copie locale reste liée à son origine.

Critère observable et preuve : Télécharger un fichier local puis le lire sans aucun réseau. [V-049](../validation.md#v-049) précise étapes, résultat, mesure, artefact et cas d’échec.

### 9. Respecter quota et conservation

Phase produit : [M7-P03](../milestones/m07-mobile.md#m7-p03). Dépendances : [M7-P02](../milestones/m07-mobile.md#m7-p02).

La rotation et les interruptions ne suppriment pas les fichiers protégés. La qualité se vérifie sur les parcours observés.

Critère observable et preuve : Conserver un album, remplir le quota puis vérifier la rotation. [V-050](../validation.md#v-050) précise étapes, résultat, mesure, artefact et cas d’échec.

## Risques et acceptation

Risque majeur : interface fluide sur dix albums mais bloquée sur 20 000. V-005 est repris par V-016 sur corpus cible. Le cache graphique ne doit pas absorber toutes les images. Accessibilité et touches média conservent leurs dispositions proposées F12-010 et F12-012.

Une revue de domaine vérifie les fonctions dont ce plan est responsable dans la couverture et les preuves des phases collaboratrices. L’absence de mesure interdit de déclarer la capacité démontrée. Les décisions de stack, de formats, de droits ou de budgets restent ouvertes jusqu’à leur adoption explicite.
