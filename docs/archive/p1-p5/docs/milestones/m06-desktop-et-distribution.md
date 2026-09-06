# M6. Porter, mettre à jour et exploiter

Plan produit futur, non exécuté. [M6 dans la roadmap](../roadmap.md) · [Validation](../validation.md) · [Couverture](../couverture.tsv). Les phases documentaires P1 à P5 sont un autre programme.

## Parcours livré

Une personne installe sur un autre desktop retenu, retrouve les mêmes données et usages, met à jour puis déplace le serveur vers un hôte compatible.

## Critères d’entrée

M1 est déjà accepté à son volume cible. Sélectionner OS, architectures et capacités à porter. Avant de porter une fonction M2 à M5, ajouter sa phase validée aux dépendances de la phase concernée.

## Critères de sortie

Les plateformes annoncées ont une matrice de capacités testée et une procédure de mise à jour et restauration. Les limites d’hébergement NAS sont documentées. Les optimisations supplémentaires ont une comparaison mesurée avec les preuves M1.

## Périmètre et conditions

Cette milestone n’accueille pas les performances indispensables du MVP. Une source NAS en M1 n’implique pas un serveur kuro installable sur un NAS. Aucune plateforme n’est déclarée supportée à partir de son seul lancement.

Les fonctions exhaustives et leurs dispositions sont les lignes de `couverture.tsv` dont `milestone` vaut M6. Une attribution de phase ne transforme aucune proposition, fonction conditionnelle ou report en engagement obligatoire. Tous les résultats ci-dessous restent à vérifier. Les choix de fichiers et données P3 restent proposés.

## Phases et dépendances

L’ordre de lecture est topologique. Chaque phase dépend seulement des prédécesseurs indiqués, des critères d’entrée et des conditions de ses fonctions. Une branche conditionnelle peut rester bloquée avec motif sans bloquer le socle indépendant.

## M6-P01

### Porter les capacités choisies sur chaque desktop

Dépendances : [M1-P06](../milestones/m01-mvp-local.md#m1-p06)

Porter le service et le contrôle vers les OS retenus, avec matrice explicite des fonctions. Pour toute capacité avancée portée, ajouter sa phase M2 à M5 validée comme dépendance avant exécution.

Responsabilités : client ordinateur avec audio, stockage et exploitation. Zones futures : platform, desktop et packaging. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Adaptateurs OS et chemins. |
| Intégration | Permissions, cycle de vie et backend audio réel sur chaque OS. |
| Parcours réel | Rejouer les usages M1 sur chaque plateforme annoncée. |
| Performance pertinente | Mesurer des budgets propres au matériel en gardant le même volume cible de comparaison. |

Scénarios : [V-046](../validation.md#v-046). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M6-P02

### Mettre à jour et relocaliser le service

Dépendances : [M6-P01](../milestones/m06-desktop-et-distribution.md#m6-p01), [M1-P05](../milestones/m01-mvp-local.md#m1-p05)

Qualifier hôtes et éventuel serveur NAS. Ajouter migration de version, reprise et retour documenté. Restaurer sur une autre machine avec sources réassociées.

Responsabilités : exploitation avec stockage et service. Zones futures : updater, migrations et packaging. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Compatibilité des schémas et des artefacts. |
| Intégration | Ancienne version supportée, échec de migration et restauration ailleurs. |
| Parcours réel | Mettre à jour puis retrouver sa playlist sur le nouvel hôte. |
| Performance pertinente | Mesurer indisponibilité, durée de migration et ressources. Un serveur NAS reste soumis à compatibilité réelle. |

Scénarios : [V-047](../validation.md#v-047). Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## M6-P03

### Approfondir distribution et performances

Dépendances : [M6-P02](../milestones/m06-desktop-et-distribution.md#m6-p02), [M1-P06](../milestones/m01-mvp-local.md#m1-p06)

Étendre les campagnes à plus de charge, plateformes et capacités validées. Publier les limites et recettes de reproduction propres à chaque paquet.

Responsabilités : exploitation avec les responsables de chaque capacité portée. Zones futures : benchmarks, packaging et release. Ces zones ne désignent aucun fichier créé aujourd’hui.

| Niveau de preuve future | Vérification attendue |
| --- | --- |
| Unité | Non-régression des règles critiques. |
| Intégration | Rejouer V-016, V-020, V-046 et V-047 sur artefacts portés selon leurs préconditions. |
| Parcours réel | Installer, importer, écouter, mettre à jour et restaurer sur chaque cible. |
| Performance pertinente | Comparer à la baseline M1 qui existera alors. Aucune correction nécessaire aux 20 000 albums M1 ne peut être différée ici. |

Scénarios : [V-016](../validation.md#v-016), [V-020](../validation.md#v-020), [V-046](../validation.md#v-046), [V-047](../validation.md#v-047) à rejouer sur les capacités portées. Leurs artefacts et cas d’échec définissent la preuve attendue.

- [ ] Réaliser et vérifier le résultat de cette phase après autorisation de développement.
- [ ] Consigner les preuves et statuts des fonctions concernées, puis faire examiner la sortie.

## Plans collaborateurs

Les propriétaires exacts sont dans la couverture. Ces plans participent aussi aux contrats, à l’interface, à l’audio et aux preuves décrits dans les phases :

- [Installation et exploitation](../plans/installation-et-exploitation.md)

- [Bibliothèque et métadonnées](../plans/bibliotheque-et-metadonnees.md)
- [Moteur audio](../plans/moteur-audio.md)
- [Client ordinateur](../plans/client-ordinateur.md)

## Risques et décision de passage

Un scénario non exécuté ou privé d’accès ne vaut pas succès. Le responsable produit examine les dispositions et les critères approuvés, avec le responsable technique pour les mesures. Conserver toute décision de retrait, report ou changement de seuil dans le futur journal de développement avant de modifier la couverture. Les limites de cette milestone sont indiquées plus haut et les échecs précis figurent dans chaque scénario.
