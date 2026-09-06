# M7. Préparer puis valider les usages mobiles

Plan produit futur, non exécuté. [M7 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne accède à sa bibliothèque à distance, télécharge un fichier local autorisé, l’écoute hors réseau puis gère un quota de stockage.

## Critères d’entrée

C-03 et C-09 validés sur M4, permissions et révocation éprouvées, données C-06 restaurables. Définir le mode d’accès distant protégé avant tout déploiement. Choisir OS mobile, politique de téléchargement et droits avant adoption.

## Critères de sortie

Les trois entrées F15-001, F15-002 et F15-003 ont une preuve distante, hors ligne et de rotation. Les identités restent compatibles avec le serveur. Accès sécurisé, intégrité locale et comportement sous interruption sont vérifiés.

## Périmètre et conditions

M7 est un horizon utile, sans design détaillé d’interface mobile. Les téléchargements de médias locaux ne donnent aucun droit de copie de streaming. La qualité d’usage et la protection des données restent présentes à chaque milestone, pas réservées au mobile.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M7. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M7-P01

### Valider le contrat mobile distant

Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02), [M1-P05](../milestones/m01-mvp-local.md#m1-p05)

Définir l’accès distant sécurisé et un client de parcours minimal après choix des plateformes. Réutiliser identités, versions et permissions, sans figer l’interface mobile aujourd’hui.

Responsabilités : client futur avec réseau et exploitation. Zones futures : mobile, remote-access et control. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Compatibilité, expiration et autorisations. |
| Intégration | Changement de réseau, révocation et reprise d’événements. |
| Parcours réel | Consulter une édition puis écouter à distance. |
| Performance pertinente | Mesurer reconnexion, trafic et contraintes batterie à définir. |

Scénarios : [V-048](../validation.md#v-048). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M7-P02

### Télécharger et lire hors réseau

Dépendances : [M7-P01](../milestones/m07-mobile.md#m7-p01)

Définir le manifeste de téléchargement, l’intégrité, les droits et les états partiels. Persister les seules copies admises.

Responsabilités : client futur avec sources et stockage. Zones futures : mobile-downloads et local-cache. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | État incomplet ou complet, checksum et droits. |
| Intégration | Réseau coupé, source modifiée et redémarrage mobile. |
| Parcours réel | Télécharger un fichier local puis le lire sans aucun réseau. |
| Performance pertinente | Mesurer espace, trafic et reprise. Les données streaming interdites restent exclues. |

Scénarios : [V-049](../validation.md#v-049). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M7-P03

### Gérer quota et rotation sous interruption

Dépendances : [M7-P02](../milestones/m07-mobile.md#m7-p02)

Ajouter quota, réservation d’espace, conservation et rotation. Affiner l’usage mobile selon les parcours observés.

Responsabilités : client futur et exploitation. Zones futures : mobile-cache et quota. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Éviction, fichiers protégés et réservation. |
| Intégration | Quota saturé et arrêt pendant remplacement. |
| Parcours réel | Conserver un album, remplir le quota puis vérifier la rotation. |
| Performance pertinente | Mesurer espace réel, batterie et réseau selon budgets futurs. Ne pas réduire la qualité d’usage à une phase finale. |

Scénarios : [V-050](../validation.md#v-050). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Ces plans participent aussi aux contrats, à l’interface, à l’audio et aux preuves décrits dans les phases :

- [Client ordinateur](../plans/client-ordinateur.md)

- [Bibliothèque et métadonnées](../plans/bibliotheque-et-metadonnees.md)
- [Moteur audio](../plans/moteur-audio.md)
- [Réseau et zones](../plans/reseau-et-zones.md)
- [Installation et exploitation](../plans/installation-et-exploitation.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
