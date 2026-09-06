# M5. Enrichir et découvrir selon les accès obtenus

Plan produit futur, non exécuté. [M5 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne consulte un enrichissement attribué, reçoit une sélection puis lit un contenu autorisé. Elle peut désactiver le fournisseur et poursuivre sa bibliothèque locale.

## Critères d’entrée

M2 fournit les identités, éditions et provenance nécessaires. Chaque fournisseur passe sa propre admission E-08. Les besoins utilisateur, droits, comptes et limites doivent être établis avant engagement.

## Critères de sortie

Chaque capacité admise dispose d’une preuve et chaque capacité inaccessible d’un statut motivé. Catalogue, lecture, téléchargement et export ont des droits distincts. Les parcours locaux passent fournisseur absent, quota dépassé et accès révoqué.

## Périmètre et conditions

Les 26 entrées M5 sont conditionnelles dans P2. Une milestone de découverte peut livrer seulement les adaptateurs admis sans promettre les autres. Aucune source Roon n’autorise sa réutilisation. M5 ne dépend pas de toute M4.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M5. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M5-P01

### Établir les droits et les limites d’accès

Dépendances : [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02)

Établir une fiche d’admission par fournisseur et chaque capacité. Conserver licences, territoires, quotas, cache, attribution et révocation.

Responsabilités : intégrations avec exploitation pour secrets et domaine pour provenance. Zones futures : providers, access et attribution. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Capacités admises distinctes du catalogue et de la lecture. |
| Intégration | Quota, révocation et adaptateur désactivé. |
| Parcours réel | Désactiver le fournisseur puis écouter un album local. |
| Performance pertinente | Mesurer délais maximums et file de travaux externes pour éviter de bloquer le local. |

Scénarios : [V-040](../validation.md#v-040). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M5-P02

### Afficher un enrichissement attribué

Dépendances : [M5-P01](../milestones/m05-decouverte-et-integrations.md#m5-p01), [M2-P02](../milestones/m02-bibliotheque-avancee.md#m2-p02)

Associer identités externes, textes et relations sans écraser tags ni corrections. Montrer absence, provenance et droits.

Responsabilités : intégrations avec domaine musical et desktop. Zones futures : providers, enrichment et desktop. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Matching et priorité des valeurs. |
| Intégration | Réponse expirée, quota, mauvaise édition et cache vidé. |
| Parcours réel | Lire la provenance d’une biographie et suivre une relation de crédit. |
| Performance pertinente | Mesurer cache et appels réseau hors chemin critique local. Aligner les paroles avec tolérance définie. |

Scénarios : [V-041](../validation.md#v-041). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M5-P03

### Ajouter des sélections et suites explicables

Dépendances : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02), [M2-P03](../milestones/m02-bibliotheque-avancee.md#m2-p03)

Proposer découverte, renouvellement quotidien, Listen Later et suite de file selon accès. Respecter profils, exclusions et choix locaux.

Responsabilités : intégrations avec profils, bibliothèque et coordinateur. Zones futures : discovery et recommendations. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Critères d’éligibilité, états écoutés et règles de vote. |
| Intégration | Fournisseur indisponible et aucune piste candidate. |
| Parcours réel | Choisir une découverte puis poursuivre une écoute depuis une amorce connue. |
| Performance pertinente | Mesurer actualisation et résultat vide. Ne pas inventer une qualité de recommandation non évaluée. |

Scénarios : [V-042](../validation.md#v-042). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M5-P04

### Lire et échanger avec les services admis

Dépendances : [M5-P02](../milestones/m05-decouverte-et-integrations.md#m5-p02), [M2-P04](../milestones/m02-bibliotheque-avancee.md#m2-p04), [M1-P04](../milestones/m01-mvp-local.md#m1-p04)

Ajouter uniquement capacités admises de streaming, playlists, radios, écoutes, extensions et passerelles. Garder conflits, restrictions et provenance visibles.

Responsabilités : intégrations avec audio, bibliothèque et exploitation. Zones futures : providers, sync et extensions. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Matching, déduplication et permissions des extensions. |
| Intégration | Synchronisation aller-retour, jeton expiré et droits de flux. |
| Parcours réel | Lire un contenu autorisé, synchroniser une sélection puis revenir au local. |
| Performance pertinente | Mesurer délais, quotas et interruption des flux. Les interdictions DSP ou téléchargement doivent être respectées selon chaque contrat. |

Scénarios : [V-043](../validation.md#v-043), [V-044](../validation.md#v-044), [V-045](../validation.md#v-045). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Ces plans participent aussi aux contrats, à l’interface, à l’audio et aux preuves décrits dans les phases :

- [Intégrations et découverte](../plans/integrations-et-decouverte.md)

- [Bibliothèque et métadonnées](../plans/bibliotheque-et-metadonnees.md)
- [Moteur audio](../plans/moteur-audio.md)
- [Client ordinateur](../plans/client-ordinateur.md)
- [Installation et exploitation](../plans/installation-et-exploitation.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
