# Réconcilier le cadrage de kuro par usages

Label: wayfinder:map

## Destination

Produire un cadrage courant de kuro organisé par usages, réconcilié après deux entretiens indépendants puis amendé par la priorité sonore et les rôles donnés directement par l'utilisateur. Le résultat distingue les engagements de U-M1, l'étude préalable du transport, les étapes admises plus tard et le backlog.

## Notes

- Utiliser `grilling-v2`, autorisé en remplacement de `grilling`, avec `domain-modeling`. Depuis la racine de kuro, ses instructions vivent dans `../dotfiles/dot_config/archived_ai_templates/archived_skills/_ARCHIVES/grilling-og/SKILL.md`.
- L'orchestrateur répond au nom de l'utilisateur pendant les entretiens délégués.
- La destination est documentaire. Elle exclut la réalisation du produit et l'exécution des études techniques.
- Le détail d'une décision vit dans la réponse du ticket qui l'a résolue. La carte et les documents courants utilisent son identifiant et un résumé.
- Les réponses des entretiens sont des arbitrages délégués par l'utilisateur. Elles ne sont ni des citations de l'utilisateur, ni des résultats techniques.
- Le corpus P1 à P5 reste historique. Le cadrage courant utilise des identifiants distincts et cite les décisions qui l'autorisent.

## Decisions so far

- [Définir les usages et les limites avec le premier entretien](issues/01-definir-usages-et-limites.md) : 25 décisions déléguées fixent le contrat provisoire de M1, les priorités suivantes et les limites du projet.
- [Projeter le premier entretien dans les documents courants](issues/02-projeter-premier-entretien.md) : le glossaire, le cadrage courant et le backlog donnent au second entretien une base lisible sans modifier le corpus P1 à P5.
- [Réviser le cadrage avec un second entretien indépendant](issues/03-reviser-cadrage-second-entretien.md) : 15 décisions supplémentaires bornent U-M1, sa validation, les étapes suivantes et la disposition du corpus fonctionnel.
- [Réconcilier le dossier et archiver le corpus initial](issues/04-reconcilier-et-archiver.md) : le cadrage courant cite les 40 décisions, dispose les 195 fonctions et conserve les 36 fichiers historiques dans une archive vérifiable.
- [Donner la priorité à la qualité sonore](issues/05-priorite-qualite-sonore.md) : trois décisions directes placent l'étude du chemin `NAS -> serveur kuro -> renderer du salon -> USB -> DDC -> I2S sur HDMI -> DAC Terminator` avant le choix de la stack et les résultats produit.
- [Clarifier les rôles Kuro et les scénarios de déploiement](issues/06-clarifier-les-roles.md) : deux décisions directes ont séparé KuroKor, les Kuro Clients et le NAS de leur hébergement. Leur portée audio générale est remplacée par KD-046.
- [Préciser les destinations de lecture](issues/07-preciser-les-destinations-de-lecture.md) : KD-046 admet la sortie locale de KuroKor, la lecture sur l'hôte d'un Kuro Client et un futur point réseau distinct sans fixer le protocole, le format transporté ou les limites de processus.

## Not yet specified

Le transport, le moteur de production, la répartition du décodage, les transformations, le point de volume et les capacités exactes du DDC restent à étudier. UPnP est un candidat. La compatibilité des streamers et la capacité d'un ordinateur peu puissant ne sont pas établies. Linux sur l'ordinateur du salon est une hypothèse initiale. Les questions techniques nécessaires à l'adoption vivent dans le backlog courant.

## Out of scope

- Déclarer un prototype ou un comportement produit à partir du seul changement de portée.
- Lire ou modifier les médias de l'utilisateur.
- Choisir une stack, un transport, une licence ou un protocole NAS sans les études prévues.
- Fusionner la PR existante.
- Fusionner deux bibliothèques pendant une restauration.
- Promettre une parité avec Roon ou un accès à ses mécanismes privés.
