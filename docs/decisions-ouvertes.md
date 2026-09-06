# Décisions ouvertes après la revue P5

Les neuf questions de [P3](faisabilite.md#décisions-ouvertes-et-effet-sur-la-suite) restent ouvertes. P5 rassemble leur responsable, l'information manquante et leur effet. Aucune option ci-dessous n'est adoptée. Les responsables techniques sont des rôles futurs, sans personne désignée ni travail applicatif autorisé.

Les arbitrages M1 précèdent l'adoption concernée. Leurs preuves demandent une autorisation de développement distincte. Ils ne bloquent pas la remise documentaire. Les questions M4, M5 et M7 ne deviennent pas des préalables à l'écoute locale.

## Arbitrages nécessaires à M1

| ID | État et responsable de décision | Information manquante et options déjà proposées | Effet et preuve future |
| --- | --- | --- | --- |
| O-01 | Ouverte. Utilisateur pour la licence, futur responsable technique pour l'inventaire distribué | Intention de réutilisation et de contribution, versions, liaisons, options de compilation et contenus embarqués. Options MIT, Apache-2.0, GPLv3 et AGPLv3 examinées en P3. | Adoption et distribution M1. E-07 et [V-019](validation.md#v-019). Aucun fichier LICENSE créé. |
| O-02 | Ouverte. Utilisateur avec preuves du futur responsable audio | Formats, conteneurs, fréquences, canaux, DAC, backend et moyen de capture inconnus. Corpus candidat P3 à accepter explicitement. Volume matériel, système, logiciel ou sortie fixe selon capacités. | MVP-05 et MVP-06. E-01 et E-03, [V-004](validation.md#v-004), [V-009](validation.md#v-009), [V-010](validation.md#v-010), [V-011](validation.md#v-011). Définir tolérance et portée de capture avant conclusion. |
| O-03 | Ouverte. Utilisateur pour l'acceptation, futurs responsables exploitation et client pour les mesures | Nombre réel de pistes, matériel, réseau, distribution des fichiers et budgets inconnus. Recherche visible p95 < 300 ms et première page < 1 s sont des propositions. Aucun seuil RAM confirmé. | Acceptation de MVP-03 à 20 000 albums et environ 3 To dès M1. E-01, E-02 et E-06, [V-016](validation.md#v-016). Aucune baseline actuelle. |
| O-04 | Ouverte. Utilisateur pour l'environnement, futur responsable technique pour l'adaptateur | Protocole, montage, permissions et débit NAS inconnus. Montage existant préféré, SMB comme hypothèse documentaire. Client natif seulement comme alternative à comparer. | MVP-02. E-01 et E-02, [V-002](validation.md#v-002), [V-003](validation.md#v-003). L'absence du NAS conserve identités et playlists. Aucune configuration de la machine actuelle. |
| O-05 | Ouverte. Futur responsable technique, revue utilisateur si périmètre affecté | Service local, desktop embarqué ou serveur existant adapté. SQLite avec FTS5, libmpv et Tauri en tête des études. MPD, GStreamer, Navidrome, Qt et Electron restent comparés. Langage et versions non fixés. | Adoption technique M1 après E-02, E-03, E-06 et E-07. [V-001](validation.md#v-001), [V-011](validation.md#v-011), [V-016](validation.md#v-016), [V-020](validation.md#v-020). Réutiliser un moteur, sans décodeur maison. |
| O-06 | Ouverte. Utilisateur pour les comportements, futur responsable technique pour les mécanismes | État durable, point de position, rétention de commandes et contenu de sauvegarde. C-06 propose un retour à l'arrêt après redémarrage du service. C-04 laisse le passage après erreur à arbitrer. Politiques de vidage et de reprise restent explicites avant code. | MVP-07 et MVP-08. E-04 et E-05, [V-008](validation.md#v-008), [V-012](validation.md#v-012), [V-013](validation.md#v-013), [V-014](validation.md#v-014). Restauration isolée avec lecture réelle, sources intactes, sans copie des 3 To dans la sauvegarde applicative proposée. |
| O-09 | Ouverte. Futur responsable technique, utilisateur pour l'environnement | Versions Linux et Omarchy, artefacts et dépendances exacts, paquet et cycle de vie du service. Paquet Linux et Flatpak à comparer selon permissions et service autonome. | Distribution reproductible M1. E-07, [V-001](validation.md#v-001), [V-020](validation.md#v-020). Niveau de reproductibilité à qualifier. Aucun paquet présent aujourd'hui. |

Les corpus, options et études détaillés restent dans la [faisabilité](faisabilite.md). La priorité ci-dessus désigne le moment de décision, sans calendrier ni nouvel engagement.

## Arbitrages des étapes ultérieures

| ID | État et responsable de décision | Information manquante et options déjà proposées | Effet et preuve future |
| --- | --- | --- | --- |
| O-07 | Ouverte et conditionnelle. Utilisateur pour le besoin, fournisseur pour l'accès, futur responsable intégrations pour la preuve | Comptes, territoires, catalogue, lecture, téléchargement, cache, export, attribution, quota, révocation et budget. Fiches par fournisseur de P3, capacités admises séparément. | M5, avec E-08 et [V-040](validation.md#v-040) à [V-045](validation.md#v-045). Aucun fournisseur obligatoire en M1. Un accès catalogue ne prouve aucun accès au PCM ni droit de traitement audio. Les profils audio M3 gardent aussi leurs droits propres dans V-034. |
| O-08 | Ouverte. Futur responsable réseau, utilisateur pour les appareils | Endpoints, capacités, topologie, horloges et budgets de dérive. Endpoint propre ou transport libre, Snapcast candidat, protocoles tiers sous conditions. Accès distant et politiques mobiles à définir à leur étape. | C-09 en M4 puis M7. [V-036](validation.md#v-036) à [V-039](validation.md#v-039), puis [V-048](validation.md#v-048) à [V-050](validation.md#v-050). Zones indépendantes avant synchronisation. RAAT non requis. Aucun effet sur l'accès NAS M1. |

## Options de licence conservées sans sélection

P3 distingue options permissives MIT et Apache-2.0, puis copyleft GPLv3 et AGPLv3. Cette liste est une question de choix du projet. Elle ne conclut pas à la compatibilité d'une combinaison de dépendances.

L'[examen des licences P3](faisabilite.md#licences-des-logiciels-dès-m1) et [TECH-208](sources-techniques.md#tech-208) restent les points de départ. La décision O-01 attend les textes et l'artefact exact. Une frontière de processus ne remplace pas cet examen. Les conditions fournisseurs restent distinctes de la licence du code.

## Réserves de référence et décisions de comportement

Les cinq contradictions, le partage historique et les trois comportements à observer sont attribués dans la [revue finale](revue-finale.md#constats-et-dispositions). Aucun statut de preuve Roon n'est devenu une preuve kuro.

Les illustrations locales, l'accessibilité, les touches média, le positionnement précis, la reprise après incident et les détails de protection ou de construction conservent leurs dispositions P2. Leur présence dans une phase ne les adopte pas. L'utilisateur arbitre les propositions produit. Les futurs responsables de domaine apportent leurs preuves. Les dix critères MVP restent obligatoires.
