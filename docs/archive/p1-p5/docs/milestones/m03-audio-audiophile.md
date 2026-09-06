# M3. Mesurer et régler la chaîne audio

Plan produit futur, non exécuté. [M3 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne identifie sa sortie, examine les transformations réelles, choisit une chaîne DSP et compare le son produit aux signaux de référence.

## Critères d’entrée

M1 livré et C-04, C-05, C-08 stabilisés. Identifier le DAC, les formats et les moyens de capture. Approuver les tolérances et vérifier les licences des traitements et profils avant adoption.

## Critères de sortie

Les capacités audio retenues sont mesurées sur matériel identifié. Le signal path correspond aux transformations et limites réelles. Le gapless M1 reste vérifié avec DSP désactivé, puis avec les traitements compatibles retenus.

## Périmètre et conditions

M2 peut avancer en parallèle. DSD et profils spécifiques dépendent des capacités et droits établis. Le bit-perfect ne peut pas être revendiqué avec DSP, gain numérique ou conversion active. Deux configurations de zone peuvent être testées successivement ici. Le réseau simultané appartient à M4.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M3. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M3-P01

### Observer la sortie et son exclusivité

Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06)

Adopter les backends compatibles retenus et afficher le signal path réel. Traiter formats limites, volumes et resynchronisation.

Responsabilités : adaptateur audio et desktop avec coordinateur. Zones futures : audio, capabilities et signal-path. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Capacités annoncées et distinction format demandé ou observé. |
| Intégration | Accès concurrent au DAC, niveau fixe, conversion et fréquence changée. |
| Parcours réel | Choisir une sortie et lire en vérifiant chaque étape affichée. |
| Performance pertinente | Mesurer délai audible et conversions. Aucun format matériel inconnu ne devient une valeur devinée. |

Scénarios : [V-030](../validation.md#v-030). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M3-P02

### Analyser en préservant l’écoute

Dépendances : [M3-P01](../milestones/m03-audio-audiophile.md#m3-p01)

Planifier ou déclencher l’analyse audio, publier ses résultats et appliquer les priorités de normalisation retenues.

Responsabilités : analyse audio avec bibliothèque et ordonnanceur. Zones futures : analysis, jobs et loudness. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Valeurs loudness, priorité ReplayGain et plages horaires. |
| Intégration | Analyse corrompue, mise en pause des travaux et lecture concurrente. |
| Parcours réel | Analyser une sélection puis comparer normalisation piste et album. |
| Performance pertinente | Mesurer marge de calcul, CPU et interruptions sous charge. |

Scénarios : [V-031](../validation.md#v-031). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M3-P03

### Composer et mesurer les traitements

Dépendances : [M3-P02](../milestones/m03-audio-audiophile.md#m3-p02)

Ajouter chaînes DSP ordonnées, filtres, bypass et fondu séparé du gapless. Préserver des réglages distincts de configurations de zone.

Responsabilités : chaîne audio avec stockage de presets et contrôle. Zones futures : dsp, presets et audio. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Coefficients, ordre, headroom et calculs par canal. |
| Intégration | Captures de référence pour PEQ, convolution, crossfeed et conversions. |
| Parcours réel | Choisir un preset, comparer le bypass puis réécouter l’album gapless. |
| Performance pertinente | Mesurer réponse, retard, écrêtage et marge CPU par chaîne. Cible de qualité à fixer avant adoption. |

Scénarios : [V-032](../validation.md#v-032), [V-035](../validation.md#v-035). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M3-P04

### Étendre selon matériel et profils accessibles

Dépendances : [M3-P03](../milestones/m03-audio-audiophile.md#m3-p03)

Évaluer DSD, multicanal et profils Audeze ou OPRA sur matériel et données autorisés. Produire la matrice des limites.

Responsabilités : audio avec catalogue de profils et exploitation pour licences. Zones futures : audio, profiles et notices. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Mapping de canaux et format de profil. |
| Intégration | DAC compatible, codecs exacts et coefficients issus des bonnes versions. |
| Parcours réel | Sélectionner un profil puis lire un signal DSD ou multicanal admis. |
| Performance pertinente | Mesurer latences, formats et marge. Les fonctions non accessibles gardent une décision explicite, sans fausse preuve. |

Scénarios : [V-033](../validation.md#v-033), [V-034](../validation.md#v-034). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Ces plans participent aussi aux contrats, à l’interface, à l’audio et aux preuves décrits dans les phases :

- [Bibliothèque et métadonnées](../plans/bibliotheque-et-metadonnees.md)
- [Moteur audio](../plans/moteur-audio.md)

- [Client ordinateur](../plans/client-ordinateur.md)
- [Installation et exploitation](../plans/installation-et-exploitation.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
