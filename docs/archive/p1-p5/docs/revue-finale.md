# Revue finale de couverture P5

La revue indépendante ne relève aucun critère obligatoire perdu entre P1, le registre P2, les contrats P3 et les plans P4. Le coordinateur a validé P5 après lecture des livrables et exécution indépendante du contrôle complet. Cette conclusion porte sur la documentation. Elle ne prouve aucune capacité du futur logiciel.

La base examinée est le commit P4 `00bd920a90b04b760c76b92b9f08fc4617dc5f62`. Les critères, registres, contrats, plans et scénarios P1 à P4 restent inchangés. P5 ajoute les correspondances ci-dessous et consolide les [neuf décisions ouvertes](decisions-ouvertes.md).

## Méthode et portée

Un nouvel agent GPT-6 Astra avec effort medium a lu le cadrage, les passations, l'inventaire, l'architecture, la faisabilité, les six plans, les sept milestones et les 50 scénarios. Le contrôle intégral P4 a été relu puis rejoué. Il vérifie 195 correspondances uniques, cas spécifiques exacts, dispositions et milestones inchangées, neuf contrats, huit études et 28 phases sans cycle.

La lecture sémantique a suivi les dix usages et les dix critères ci-dessous. Elle a distingué résultat sonore et commande acceptée, NAS absent et suppression, sauvegarde lisible et données restaurées utilisables. Elle a aussi vérifié la séparation entre cible obligatoire, comportement proposé et preuve encore absente.

Deux sources techniques primaires ont été rouvertes le 2026-09-06. La contrainte WAL sur un même hôte conforte la base locale proposée en P3. Le manuel mpv confirme les compromis de maintien du format, réouverture et sous-alimentation lors d'un démarrage réseau lent. Ces sondages ne valident ni moteur ni benchmark kuro. [SQLite WAL](https://sqlite.org/wal.html), [mpv gapless](https://mpv.io/manual/stable/#options-gapless-audio).

Cette revue utilise le même modèle imposé que les auteurs précédents. Elle est indépendante par l'agent, sans diversité de modèles. Les sources Roon n'ont pas toutes été reconsultées en P5. Roon n'a pas été exécuté, sa version et son build restent inconnus.

## Traçabilité des critères obligatoires

Chaque ligne donne des fonctions témoins du critère, leurs contrats proposés et leurs destinations canoniques P4. La liste exhaustive des fonctions reste dans la [couverture](couverture.tsv). Les noms des plans sont liés dans la colonne responsable. Toutes les preuves produit restent non exécutées.

| Critère ou usage | Fonctions témoins | Contrats proposés | Plans responsables | Phases canoniques | Scénarios canoniques | Point vérifié et réserve |
| --- | --- | --- | --- | --- | --- | --- |
| MVP-01 Linux sur Omarchy | F01-001, F12-005 | C-03, C-07 | [Client](plans/client-ordinateur.md), [Exploitation](plans/installation-et-exploitation.md) | [M1-P01](milestones/m01-mvp-local.md#m1-p01), [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-001](validation.md#v-001), [V-015](validation.md#v-015) | O-05 et O-09. V-020 complète le paquet futur. |
| MVP-02 Import local et NAS | F02-001, F02-002, F13-003 | C-01, C-08 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md) | [M1-P02](milestones/m01-mvp-local.md#m1-p02) | [V-002](validation.md#v-002), [V-003](validation.md#v-003) | O-02 et O-04. Reprise sans perte de références. |
| MVP-03 20 000 albums et environ 3 To dès M1 | F12-009 | C-02, C-08 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P06](milestones/m01-mvp-local.md#m1-p06) | [V-016](validation.md#v-016) | O-03. Petit corpus et index synthétique seuls insuffisants. |
| MVP-04 Albums, artistes et recherche | F04-001, F04-002, F04-004 | C-02, C-08 | [Client](plans/client-ordinateur.md) | [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-005](validation.md#v-005) | O-03. Reprise sur corpus cible en V-016. |
| MVP-05 Playlists, file et sortie locale | F05-001, F06-003, F07-001 | C-03, C-04, C-05, C-06 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md), [Audio](plans/moteur-audio.md) | [M1-P01](milestones/m01-mvp-local.md#m1-p01), [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-006](validation.md#v-006), [V-008](validation.md#v-008), [V-009](validation.md#v-009) | O-02 et O-06. Commande et son observé distincts. |
| MVP-06 Gapless sur formats retenus | F06-013 | C-04, C-05, C-08 | [Audio](plans/moteur-audio.md) | [M1-P04](milestones/m01-mvp-local.md#m1-p04) | [V-011](validation.md#v-011) | O-02. Échantillons, padding et transitions mesurés. |
| MVP-07 Données conservées après redémarrage | F12-008 | C-03, C-06 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P04](milestones/m01-mvp-local.md#m1-p04) | [V-012](validation.md#v-012) | O-06. Arrêt sonore après redémarrage proposé. |
| MVP-08 Sauvegarde restaurable | F12-001, F12-003 | C-06 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P05](milestones/m01-mvp-local.md#m1-p05) | [V-014](validation.md#v-014) | O-06. Lecture après restauration et réassociation. |
| MVP-09 Sources intactes | F13-002 | C-01, C-06, C-07 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P05](milestones/m01-mvp-local.md#m1-p05) | [V-018](validation.md#v-018) | Manifestes avant et après. atime relevé séparément. |
| MVP-10 Usage local sans Internet | F13-001 | C-01, C-02, C-08 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P06](milestones/m01-mvp-local.md#m1-p06) | [V-017](validation.md#v-017) | LAN et NAS disponibles. Fournisseurs désactivés. |
| U-01 Ajouter local et NAS | F02-001, F02-002, F02-010, F13-003 | C-01, C-07, C-08 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md) | [M1-P02](milestones/m01-mvp-local.md#m1-p02) | [V-002](validation.md#v-002), [V-003](validation.md#v-003), [V-004](validation.md#v-004) | Permissions, fichier invalide, scan interrompu et retour NAS. |
| U-02 Parcourir albums et artiste | F04-001, F04-002, F02-011, F03-001 | C-01, C-02 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md), [Client](plans/client-ordinateur.md) | [M1-P02](milestones/m01-mvp-local.md#m1-p02), [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-004](validation.md#v-004), [V-005](validation.md#v-005) | Compilation, multidisque, tags absents et homonymes en V-004. |
| U-03 Chercher album, artiste ou piste | F04-004 | C-02, C-08 | [Client](plans/client-ordinateur.md) | [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-005](validation.md#v-005) | Accents, absence et résultats nombreux. V-016 reprend la cible. |
| U-04 Lancer un album et modifier la file | F06-001, F06-003, F06-004, F12-013 | C-03, C-04, C-05 | [Audio](plans/moteur-audio.md) | [M1-P01](milestones/m01-mvp-local.md#m1-p01), [M1-P03](milestones/m01-mvp-local.md#m1-p03), [M1-P04](milestones/m01-mvp-local.md#m1-p04) | [V-007](validation.md#v-007), [V-008](validation.md#v-008), [V-013](validation.md#v-013) | Fin de file et erreurs explicites. O-06 arbitre la suite après erreur. |
| U-05 Conserver une playlist | F05-001, F05-002 | C-01, C-03, C-06 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md) | [M1-P03](milestones/m01-mvp-local.md#m1-p03) | [V-006](validation.md#v-006) | Réordre, redémarrage et piste indisponible gardant sa référence. |
| U-06 Enchaîner deux pistes | F06-013 | C-04, C-05, C-08 | [Audio](plans/moteur-audio.md) | [M1-P04](milestones/m01-mvp-local.md#m1-p04) | [V-011](validation.md#v-011) | O-02. Pas de silence ajouté. Portée de capture déclarée. |
| U-07 Fermer et rouvrir | F01-002, F12-008 | C-03, C-06 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P01](milestones/m01-mvp-local.md#m1-p01), [M1-P04](milestones/m01-mvp-local.md#m1-p04) | [V-001](validation.md#v-001), [V-012](validation.md#v-012) | O-06 distingue fenêtre fermée et redémarrage du service. |
| U-08 Restaurer une sauvegarde | F12-003 | C-01, C-06, C-07 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P05](milestones/m01-mvp-local.md#m1-p05) | [V-014](validation.md#v-014) | Schéma, archive corrompue, chemins déplacés et sources absentes. |
| U-09 Couper Internet, conserver le LAN | F13-001, F13-003 | C-01, C-02, C-08 | [Bibliothèque](plans/bibliotheque-et-metadonnees.md), [Exploitation](plans/installation-et-exploitation.md) | [M1-P02](milestones/m01-mvp-local.md#m1-p02), [M1-P06](milestones/m01-mvp-local.md#m1-p06) | [V-003](validation.md#v-003), [V-017](validation.md#v-017) | V-017 sépare Internet et NAS. V-003 traite le NAS absent. |
| U-10 Ouvrir la bibliothèque cible | F12-009 | C-02, C-08 | [Exploitation](plans/installation-et-exploitation.md) | [M1-P06](milestones/m01-mvp-local.md#m1-p06) | [V-016](validation.md#v-016) | O-03. Pistes, matériel, mémoire et réseau à mesurer. |

M1-P06 rejoue U-01 à U-10 sur le corpus cible. Le rattachement canonique d'une fonction à une phase antérieure ne dispense pas de cette acceptation finale. Les budgets p95 < 300 ms et première page < 1 s restent proposés. Aucun nombre de pistes, matériel, format, DAC ou protocole NAS n'a été déduit du wiki machine.

## Cohérence des étapes ultérieures

| Étape | Lecture croisée et résultat documentaire | Décision encore nécessaire |
| --- | --- | --- |
| M2 | Identités minimales M1 prolongées par éditions, crédits, œuvres, Focus, tags et exports. V-022 à V-029 conservent corrections et originaux. M2 n'attend pas de fournisseur. | Champs de crédits après résolution de F03-017. Responsable bibliothèque et utilisateur. |
| M3 | Exclusif, signal path, DSP et formats spécialisés suivent le gapless M1. V-032 teste deux configurations successivement, sans supposer des zones réseau déjà réalisées. | O-02, O-05 et droits des profils V-034. Responsables audio et utilisateur. |
| M4 | M4-P02 réalise les zones indépendantes avant M4-P03 et V-038 pour la synchronisation. Protocoles tiers dans M4-P04, sans RAAT requis. | O-08. Responsable réseau et utilisateur pour appareils et budgets. |
| M5 | Les 26 entrées restent conditionnelles. V-040 admet chaque capacité avant enrichissement, streaming ou échange. Un catalogue ne donne pas implicitement accès au flux ou au PCM. | O-07. Fournisseur pour accès, utilisateur pour besoin et futur responsable intégrations pour preuves. |
| M6 | Portage et exploitation prolongent les mesures M1. M6-P03 reprend V-016 et V-020, sans reporter la cible de bibliothèque. | O-09 et plateformes à choisir. Futurs responsables client et exploitation. |
| M7 | Trois fonctions F15-001, F15-002 et F15-003 restent reportées. V-048 à V-050 distinguent distant, copie autorisée hors réseau et quota. Aucun design mobile détaillé n'est ajouté. | O-08 et décision utilisateur à cette étape. Futurs responsables mobile et réseau. |

## Constats et dispositions

| Constat | Preuve et effet | Statut après P5 | Responsable et sortie attendue |
| --- | --- | --- | --- |
| Libellé `retenu_provisoire` trop étroit dans le dictionnaire P2 | Le dictionnaire parle de milestone ultérieure, mais F12-013 est M1 dans les deux TSV et V-013. | Clarification documentaire traitée avec accord du coordinateur. Ce statut indique une admission provisoire, sans imposer intrinsèquement une milestone ultérieure. F12-013 et son cas restent inchangés. | Coordinateur. L'éventuelle harmonisation future du glossaire ne conditionne pas la remise. |
| Cinq contradictions Roon | F03-017, F07-013, F11-005, F11-006 et F11-007 sont conservées. V-024, V-043 et V-045 portent leurs observations futures. | Ouvertes, non bloquantes pour le dossier. Aucune parité déclarée sur ces points. | Bibliothèque pour les crédits, intégrations avec audio pour MQA, intégrations pour versions et playlists. Version de référence à identifier avant observation. |
| Un élément historique | F11-012 et V-044 concernent des destinations de partage anciennes. | Historique conservé, capacité M5 conditionnelle. | Intégrations. Vérifier chaque destination actuelle et son accès avant engagement. |
| Trois comportements à observer | F06-014 dans V-008, F12-010 dans V-015 et F12-011 dans V-012. | `a_observer` conservé. Les propositions de position, accessibilité et reprise restent proposées. | Audio, client et exploitation, avec décision utilisateur sur les comportements. |
| Inconnues qui empêchent une acceptation produit | Formats, DAC, nombre de pistes, matériel, NAS, budgets, état durable, stack, licence et versions restent inconnus ou proposés. | Ouvertes dans O-01 à O-09. Aucun blocage documentaire masqué. | Responsables et preuves dans les décisions ouvertes. Aucune réduction du MVP pour les contourner. |
| Faisabilité et performance non démontrées | Neuf contrats, huit études et 50 scénarios sont des documents. Aucun exécutable ni corpus réel kuro. | Preuves produit non exécutées. | Futurs responsables techniques après autorisation distincte. Aucun succès déduit de la revue. |
| Étendue du corpus Roon | 173 entrées documentées, cinq contradictoires, une historique et trois à observer. Sept exigences et six propositions kuro complètent les 195 entrées. | Inventaire borné au corpus, sans parité exhaustive démontrée. | Futur responsable produit pour toute revendication de parité, avec version et observations identifiées. |
| Validation manager et publication | P5 remet un dossier local. Les commits, références distantes et PR sont des opérations séparées. | Revue du coordinateur validée. Commit local autorisé, publication séparée. | Coordinateur. Vérifier les références réelles avant d'annoncer publication. |

## Preuves documentaires et limites

La [passation P5](passations/p5-revue.md) contient le contrôle rejouable, ses résultats et le périmètre des fichiers relus. Les TSV gardent largeur, valeurs, références, casse des cas et chemins de preuve valides. Le journal antérieur reste un préfixe intact.

Les fichiers publiables ont été inspectés comme textes du dépôt. La liste des fichiers et une recherche ciblée complètent la revue de contenu pour les médias, secrets, chemins privés et adresses personnelles. Cette recherche ne constitue pas une preuve universelle d'absence de secret. Les métadonnées locales Git ne sont pas des fichiers produit.

Le principe Prove it works a conduit à rejouer les contrôles sur les fichiers remis et à lire les chaînes métier. Build the lever a conduit à conserver le contrôle P5 dans la passation, avec validation de chaque chaîne de la matrice. Technical writing et Unslop ont guidé les nouveaux textes. Le journal conserve les décisions vérifiées, avec la validation du coordinateur consignée après son contrôle indépendant.
