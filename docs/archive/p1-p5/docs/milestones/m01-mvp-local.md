# M1. Écouter sa bibliothèque locale et NAS sur Linux

Plan produit futur, non exécuté. [M1 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne importe ses fichiers locaux et NAS, trouve un album dans 20 000 albums, écoute en gapless, modifie une playlist, redémarre et restaure ses données sans modifier les sources.

## Critères d’entrée

Autorisation de développement distincte obtenue. Définir le matériel Omarchy, le protocole NAS et le corpus avec l’utilisateur. Avant adoption, arbitrer O-01 à O-06 et O-09 avec E-01 à E-07. Les essais futurs départagent les candidats P3. Une licence, un framework ou un moteur n’est pas choisi par ce plan.

## Critères de sortie

Les dix critères MVP-01 à MVP-10 sont prouvés sur Linux Omarchy, service, contrôle et sortie sur le même ordinateur. Les sources locales et NAS sont couvertes à 20 000 albums et environ 3 To. Les formats gapless, le comportement durable et les budgets ont une approbation explicite. Une petite démonstration seule ne permet pas la livraison.

## Périmètre et conditions

La sortie partagée et le contrôle de volume système sont possibles selon le matériel. Le signal path détaillé, l’exclusif et le DSP complet relèvent de M3. L’usage sans Internet conserve un LAN disponible. Les propositions P2 restent proposées même quand leur scénario est planifié.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M1. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M1-P01

### Écouter un album réel de bout en bout

Dépendances : Aucune phase produit antérieure. Appliquer les critères d’entrée.

Après arbitrage des préconditions, réaliser une tranche avec petite fixture autorisée, import minimal, vue album et son réel. Conserver la séparation des rôles proposée par P3. Les essais de moteur servent à choisir avant adoption, pas à annoncer le MVP.

Responsabilités : domaine musical, service local, contrôle minimal et adaptateur audio. Zones futures indicatives : domain, library, playback, audio et desktop. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Identités de piste et transitions de transport. |
| Intégration | Commande locale, moteur observé et versions compatibles. |
| Parcours réel | Démarrer, choisir une piste, écouter puis reconnecter après fermeture de fenêtre. |
| Performance pertinente | Relever démarrage et son observé. Cette fixture ne valide pas 20 000 albums. |

Scénarios : [V-001](../validation.md#v-001), [V-007](../validation.md#v-007), [V-009](../validation.md#v-009), [V-019](../validation.md#v-019). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M1-P02

### Importer et réconcilier local et NAS

Dépendances : [M1-P01](../milestones/m01-mvp-local.md#m1-p01)

Ajouter scans reprenables, exclusions, disponibilité, tags, copies et déplacement explicite des sources. Garder catalogue, index et cache sur disque local.

Responsabilités : service de bibliothèque et adaptateurs fichiers, avec exploitation pour droits et diagnostics. Zones futures : library, sources et persistence. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Réconciliation de générations, priorités de tags et identités distinctes. |
| Intégration | Montage NAS perdu, retour, source déplacée et index réconcilié. |
| Parcours réel | Importer les deux origines puis lire leurs albums. |
| Performance pertinente | Mesurer scan complet et incrémental préliminaires. Ne pas imposer un hash intégral de 3 To à chaque scan. |

Scénarios : [V-002](../validation.md#v-002), [V-003](../validation.md#v-003), [V-004](../validation.md#v-004). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M1-P03

### Choisir et conserver son écoute

Dépendances : [M1-P02](../milestones/m01-mvp-local.md#m1-p02)

Fournir navigation, recherche, playlists et file canonique modifiable. Invalider toute précharge qui ne correspond plus à la prochaine occurrence. Traiter le clavier Omarchy et les propositions d’accessibilité.

Responsabilités : desktop avec catalogue, coordinateur et stockage. Zones futures : desktop, query, playlists et playback. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Tris, filtres, doublons d’occurrences et conflits de révision. |
| Intégration | Pagination avec mutation, commandes de file pendant préparation et playlist durable. |
| Parcours réel | Trouver un album, sélectionner, écouter, réordonner et sauvegarder au clavier. |
| Performance pertinente | Mesurer p50, p95, première page visible et RSS. La validation cible complète arrive en M1-P06. |

Scénarios : [V-005](../validation.md#v-005), [V-006](../validation.md#v-006), [V-008](../validation.md#v-008), [V-015](../validation.md#v-015). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M1-P04

### Prouver jonctions et reprise cohérente

Dépendances : [M1-P03](../milestones/m01-mvp-local.md#m1-p03)

Éprouver gapless sur formats retenus, changement de paramètres, volume et périphérique perdu. Stabiliser C-03 à C-06 face aux crashes et retards NAS.

Responsabilités : coordinateur et adaptateur audio, avec persistance et desktop. Zones futures : playback, audio, persistence et diagnostics. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Événements tardifs, rétention de commandes et ordre d’occurrences. |
| Intégration | Crash entre commande et accusé, flux interrompu, DAC retiré et retour. |
| Parcours réel | Écouter les paires, modifier la file et retrouver un état explicite après incident. |
| Performance pertinente | Capturer les jonctions et interruptions. Fixer tolérances et formats avant conclusion, sans prétendre bit-perfect sur sortie partagée. |

Scénarios : [V-010](../validation.md#v-010), [V-011](../validation.md#v-011), [V-012](../validation.md#v-012), [V-013](../validation.md#v-013). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M1-P05

### Sauvegarder et restaurer sans toucher aux sources

Dépendances : [M1-P04](../milestones/m01-mvp-local.md#m1-p04)

Produire un instantané cohérent C-06, le restaurer isolément et relire après réassociation des sources. Vérifier les sources intactes, les diagnostics et les protections locales proposées C-07.

Responsabilités : exploitation avec stockage, bibliothèque et adaptateurs. Zones futures : backup, migrations, diagnostics et access. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Intégrité, version de manifeste et règles de compatibilité. |
| Intégration | Sauvegarde en activité, archive corrompue, ancien schéma et refus d’une version trop récente. |
| Parcours réel | Restaurer playlists et réglages, réassocier un NAS déplacé puis lire. |
| Performance pertinente | Mesurer taille et durée. Conserver médias hors sauvegarde applicative et protéger les preuves privées. |

Scénarios : [V-014](../validation.md#v-014), [V-018](../validation.md#v-018). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M1-P06

### Accepter le MVP à 20 000 albums

Dépendances : [M1-P05](../milestones/m01-mvp-local.md#m1-p05)

Exécuter U-01 à U-10 sur Linux Omarchy, local et NAS, à 20 000 albums et environ 3 To. Refaire les parcours sans Internet avec LAN disponible. Vérifier un paquet propre selon la proposition retenue.

Responsabilités : exploitation pilote l’acceptation avec tous les domaines M1. Zones futures : packaging, benchmarks et acceptance. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Rejouer les règles métier critiques sur les formats et versions retenus. |
| Intégration | Scan, recherche, audio et sauvegarde simultanés sur le corpus cible. |
| Parcours réel | Importer, naviguer, rechercher, écouter, redémarrer et restaurer sur matériel fixé. |
| Performance pertinente | Campagne complète V-016. Les budgets recherche p95 < 300 ms et première page < 1 s restent proposés à approuver. Aucune baseline n’existe. |

Scénarios : [V-016](../validation.md#v-016), [V-017](../validation.md#v-017), [V-020](../validation.md#v-020). Leurs artefacts et cas d’échec définissent la preuve attendue.

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
