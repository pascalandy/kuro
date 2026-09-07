# Backlog courant de kuro

Ce registre contient les usages différés et les études requises avant une adoption. Une entrée ne constitue ni un engagement, ni un résultat. Le futur agent ou développeur du lot produit la preuve technique. L'utilisateur accepte le résultat produit et tout changement de portée. KD-025, KD-038.

## Usages différés

| ID | Question de réadmission | Rôle futur chargé de la preuve | Preuve requise |
| --- | --- | --- | --- |
| KB-001 | Le classique avancé répond-il à un besoin prioritaire après U-M3 ? | Bibliothèque | Parcours précis avec œuvres, mouvements et corpus représentatif |
| KB-002 | Une surveillance automatique apporte-t-elle plus que le scan manuel pilotable ? | Bibliothèque et exploitation | Délais, interruptions, débordements et NAS absent sans suppression |
| KB-003 | Quels modes de sortie, contrôles de volume ou traitements répondent au chemin sonore retenu ? | Audio | Format livré, transformations connues, captures et critères d'écoute acceptés |
| KB-004 | Plusieurs sorties, pièces ou contrôleurs doivent-ils suivre le renderer unique ? | Réseau | Appareils, parcours indépendants et mesures de synchronisation |
| KB-005 | Une intégration externe apporte-t-elle un contenu autorisé et durable ? | Intégrations | Accès, droits, quotas, révocation, cache, export et attribution par fournisseur |
| KB-006 | Un autre système d'exploitation a-t-il un utilisateur et un parcours prioritaire ? | Client | Environnement cible et parcours d'acceptation |
| KB-007 | Une mise à jour automatique est-elle préférable à une procédure explicite ? | Exploitation | Distribution, reprise, retour arrière et conservation des données |
| KB-008 | MPRIS améliore-t-il U-M2 sans bloquer les favoris et les filtres ? | Client | Commandes desktop testées séparément du parcours de redécouverte |
| KB-009 | Un usage mobile mérite-t-il une étape après les conditions de U-M4 ? | Produit mobile | Portée distincte pour télécommande, lecture, accès distant et téléchargement |
| KB-016 | Quels imports, exclusions et opérations de source dépassent le scan pilotable de U-M1 ? | Bibliothèque | Parcours de copie, import de playlists, analyse, exclusion ou purge avec règles de données |
| KB-017 | Quelles corrections et métadonnées enrichies dépassent l'organisation limitée de U-M3 ? | Bibliothèque | Cas utilisateur, champs modifiables, provenance, réversibilité et conservation des références |
| KB-018 | Quelles opérations avancées de playlist, de file et d'export répondent à un usage observé ? | Lecture et bibliothèque | Parcours pour mélange, répétition, historique, conversion, import ou export |
| KB-019 | Quelle redécouverte dépasse les favoris et filtres locaux de U-M2 ? | Produit | Besoin observé, corpus et résultat mesurable pour recommandation ou contenu éditorial |
| KB-020 | Quel historique de sauvegardes ou quelle migration devient nécessaire après le format U-M1 ? | Exploitation | Versions concernées, compatibilité, interruption et récupération de l'état précédent |
| KB-021 | Quelle navigation ou présentation avancée améliore un parcours desktop prouvé ? | Client | Parcours pour multisélection, plein écran, historique général ou personnalisation de vues |

## Études avant adoption

| ID | Question | Rôle futur chargé de la preuve | Preuve requise |
| --- | --- | --- | --- |
| KB-010 | Quelle licence convient au code et aux dépendances distribuées ? | Exploitation | Artefact exact, dépendances et comparaison des obligations |
| KB-011 | Quelle stack convient aux parties audio possédées par Kuro ? | Architecture | Rust évalué en priorité pour ces parties, laboratoire Go conservé comme référence, mêmes responsabilités, budgets mémoire et réseau, import, recherche, paquet et reprise comparés avant adoption |
| KB-012 | Quels formats, transformations et enchaînements gapless peuvent être garantis sur chaque chemin retenu ? | Audio | Corpus accepté, représentation transportée, point de lecture et sortie identifiés, captures et mesures reproductibles |
| KB-013 | Quels budgets mémoire et import permettent d'accepter 20 000 albums et environ 3 To ? | Exploitation et bibliothèque | Matériel, corpus cible et mesures reproductibles |
| KB-014 | Le montage NAS fourni satisfait-il les contrats de U-M1 ? | Bibliothèque et exploitation | Montage déclaré, interruption, retour, relocalisation et mesures sur la cible |
| KB-015 | L'installation Linux reste-t-elle reproductible hors de la machine de développement ? | Exploitation | Installation, démarrage, désinstallation et restauration dans un environnement propre |
| KB-022 | Comment détecter un contenu audio remplacé au même chemin sans rapprochement silencieux ? | Bibliothèque | Corpus avec tags modifiés, fichier remplacé et renommage, puis règles de référence observables |
| KB-023 | Quels champs locaux et quels critères détaillés bornent les favoris et filtres de U-M2 ? | Produit et bibliothèque | Usage observé après U-M1, champs retenus et parcours d'acceptation |
| KB-024 | Quels critères détaillés bornent l'organisation des éditions, coffrets et corrections internes de U-M3 ? | Produit et bibliothèque | Cas observés après U-M1, opérations retenues et conservation prouvée des références |
| KB-025 | Quel transport convient aux trois destinations sans masquer les transformations ni les erreurs ? | Architecture et audio | Matrice des fichiers, flux encodés et PCM par destination; frontières du décodage, des tampons et de la sortie; essais adaptés à l'hôte du Kuro Client, à USB, au DDC, au DAC et aux appareils réseau; UPnP reste un candidat sans adoption implicite du DSP ou du multiroom |

Une étude négative demande un nouvel arbitrage. Elle ne réduit pas seule le volume cible, la garantie gapless retenue ou la restauration. Une entrée quitte ce fichier seulement lorsque sa décision de réadmission est enregistrée et que la roadmap est mise à jour.
