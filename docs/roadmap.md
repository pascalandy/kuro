# Roadmap courante de kuro

Cette roadmap ordonne les usages retenus après les deux entretiens. Elle ne reprend pas les milestones M1 à M7 du [corpus P1 à P5](archive/p1-p5/README.md). Les passages internes de U-M1 rendent le travail démontrable, mais seul U-M1 entier peut être accepté. KD-026, KD-032.

## U-M1. Écoute locale fiable

| Passage | Résultat observable | Passage suivant |
| --- | --- | --- |
| U-M1.A | Importer un dossier local et jouer un album sur la sortie partagée | Import, lecture de base et erreurs visibles fonctionnent sur un petit corpus |
| U-M1.B | Retrouver la musique et préparer des playlists et une file | Recherche, vues, tri, navigation, playlists et file respectent le [cadrage](cadrage-courant.md) |
| U-M1.C | Reprendre après redémarrage, utiliser le NAS et restaurer un snapshot | Persistance, NAS, sauvegarde et échec de restauration sont prouvés avant les mesures finales |

L'acceptation finale vérifie les dix critères MVP ensemble, dont le corpus cible, le gapless retenu, l'usage sans Internet, les sources intactes et le paquet reproductible. Les scénarios [KV-001 à KV-013](validation.md) donnent les preuves attendues. KD-001, KD-026.

## U-M2. Redécouverte locale

U-M2 permet de marquer des albums ou des pistes comme favoris, de les retrouver et de filtrer sur des champs locaux retenus après usage. Mélange, répétition et MPRIS peuvent être admis séparément. U-M2 n'impose aucun moteur de recommandation. Ses critères seront précisés après l'acceptation de U-M1. KD-007, KD-019, KD-034, KD-037.

La priorité de U-M2 est présumée. L'utilisateur la revalide à partir de l'usage réel avant son démarrage. KD-032, KD-038.

## U-M3. Éditions et coffrets

U-M3 permet d'organiser volontairement des éditions et des coffrets en conservant les références existantes. Des corrections internes de métadonnées peuvent y être admises. Œuvres, mouvements, crédits détaillés et enrichissement externe ne sont pas requis. Ses critères seront précisés après U-M1. KD-033, KD-037.

L'utilisateur revalide l'ordre entre U-M2 et U-M3 à partir de l'usage réel. KD-032, KD-038.

## U-M4. Étude mobile conditionnelle

U-M4 autorise une étude. Il n'engage aucune fonction mobile. Avant de l'ouvrir, les conditions suivantes sont toutes remplies :

- U-M1 est accepté.
- Les parcours desktop retenus et la restauration sont prouvés.
- U-M2 et U-M3 sont achevés ou reportés explicitement avec une raison.
- Au moins quatorze jours d'usage représentatif journalisé se sont écoulés depuis la dernière correction bloquante, sans blocage ni perte de données pendant cette période.
- Aucun incident critique non résolu ne subsiste.

L'étude distingue télécommande, lecture sur téléphone, accès distant et téléchargement. La durée de stabilité ne suffit pas seule à engager l'une de ces fonctions. KD-031.

## Réviser la roadmap

L'utilisateur accepte les résultats produit et les changements de portée. Le futur agent ou développeur du lot apporte les preuves techniques. Les éléments sans engagement courant restent dans le [backlog](backlog.md). Une réadmission exige un besoin, la preuve demandée et un arbitrage explicite. KD-038.
