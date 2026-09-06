# M4. Contrôler et écouter dans plusieurs pièces

Plan produit futur, non exécuté. [M4 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Deux contrôleurs autorisés pilotent des files indépendantes sur deux endpoints. Une étape suivante permet de grouper des sorties compatibles puis de les dissocier.

## Critères d’entrée

M1 livré avec autorité de bibliothèque, identités et C-03 stabilisés. Choisir appareils et topologie. Adopter les règles d’appairage C-07 et le contrat C-09 avant toute ouverture LAN.

## Critères de sortie

Zones indépendantes et synchronisation ont des preuves distinctes. La perte d’un contrôleur ou endpoint n’altère pas les autres sessions. Les budgets de décalage et de dérive sont approuvés et mesurés pour le groupe supporté.

## Périmètre et conditions

Le socle M4 utilise un endpoint kuro ou un transport libre. Snapcast reste candidat à comparer selon P3. Les fonctions RAAT et protocoles tiers restent conditionnelles et leur blocage ne bloque pas les zones propres. Le DSP complet M3 n’est pas un préalable.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M4. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M4-P01

### Autoriser plusieurs contrôleurs

Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06)

Ouvrir le contrôle LAN seulement après appairage, transport protégé et permissions adoptés. Éprouver concurrence, reconnexion et révocation.

Responsabilités : coordination réseau avec sécurité et desktop. Zones futures : control, pairing et access. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Permissions, révisions et versions de contrat. |
| Intégration | Deux contrôleurs concurrents et tiers non autorisé. |
| Parcours réel | Modifier une file depuis deux contrôles puis révoquer l’un. |
| Performance pertinente | Mesurer convergence et reprise après perte d’événements, sans horloge audio déduite des événements. |

Scénarios : [V-036](../validation.md#v-036). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M4-P02

### Livrer endpoints et zones indépendantes

Dépendances : [M4-P01](../milestones/m04-reseau-domestique.md#m4-p01), [M1-P04](../milestones/m01-mvp-local.md#m1-p04)

Découvrir endpoints propres ou libres et négocier leurs capacités. Donner une file à chaque zone, puis transfert, commandes matérielles et display.

Responsabilités : coordination réseau avec audio et client. Zones futures : endpoints, zones et displays. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Isolation de sessions et négociation de format. |
| Intégration | Deux endpoints, déconnexion d’un seul et transfert de session. |
| Parcours réel | Écouter deux albums différents puis transférer une file. |
| Performance pertinente | Mesurer retard de transfert, interruptions et charge réseau. Exécuter les preuves audio nécessaires au format retenu, sans attendre tout M3. |

Scénarios : [V-037](../validation.md#v-037). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M4-P03

### Synchroniser les sorties compatibles

Dépendances : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02)

Comparer transport libre candidat Snapcast et implémentation propre avant adoption. Négocier horloge, tampon et dérive, puis groupement et dissociation.

Responsabilités : transport audio avec endpoints et coordinateur. Zones futures : transport, clocks et groups. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Calcul de correction et règles d’appartenance. |
| Intégration | Captures simultanées avec jitter, perte et dérive introduits. |
| Parcours réel | Grouper deux zones, écouter puis retirer une sortie. |
| Performance pertinente | Mesurer décalage et dérive sur durée définie. Aucun seuil RAAT n’est une garantie kuro. Budget à approuver. |

Scénarios : [V-038](../validation.md#v-038). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M4-P04

### Qualifier les protocoles tiers admis

Dépendances : [M4-P02](../milestones/m04-reseau-domestique.md#m4-p02)

Pour chaque protocole autorisé, ajouter un adaptateur isolé et sa matrice de modèles. Cette branche conditionnelle peut avancer indépendamment de M4-P03.

Responsabilités : adaptateurs réseau avec exploitation et audio. Zones futures : protocol-adapters et capabilities. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Capacités et erreurs de l’adaptateur. |
| Intégration | Matériel et versions exacts, groupement propre au protocole. |
| Parcours réel | Découvrir puis lire sur l’appareil admis avec contrôle explicite. |
| Performance pertinente | Mesurer latence et limites par protocole. Un refus d’accès ne bloque pas les endpoints propres. |

Scénarios : [V-039](../validation.md#v-039). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Ces plans participent aussi aux contrats, à l’interface, à l’audio et aux preuves décrits dans les phases :

- [Réseau et zones](../plans/reseau-et-zones.md)

- [Moteur audio](../plans/moteur-audio.md)
- [Client ordinateur](../plans/client-ordinateur.md)
- [Installation et exploitation](../plans/installation-et-exploitation.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
