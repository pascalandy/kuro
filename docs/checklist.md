# Vérifier et suivre le programme

Cochez un résultat seulement lorsque sa preuve existe. Lisez le [programme](programme.md) pour les critères de chaque phase. Consignez les décisions dans le [journal](decisions.tsv).

## Préparer le travail

- [x] Lire la section Principles de Poteto Mode en entier. Lecture effectuée par le coordinateur, puis par l'agent P1.
- [x] Lire les instructions du répertoire parent et l'index du wiki voisin. Limiter les écritures à kuro.
- [x] Lire Poteto Mode, Technical writing, Unslop et Show me your work.
- [x] Conserver l'autorisation documentaire et les limites dans le contexte utilisateur.
- [x] Définir les critères P1 à P5 avant la rédaction des phases dépendantes.
- [x] Initialiser le dépôt local avec la branche main. Ne pas commiter avant revue.

## Appliquer les playbooks au périmètre documentaire

Les étapes numérotées ci-dessous reprennent les intitulés ou extraits des étapes des playbooks lus. Les lignes d'état précisent leur application. Les instructions utilisateur priment sur les étapes qui exigent du développement, un autre modèle ou une modification hors du projet.

### Multi-phase or multi-PR plan

1. When the change is one or two files with an obvious approach, skip the plan. Say so and stop.

   Sans objet. Le programme approuvé comprend cinq phases et exige un dossier complet.

2. Settle open questions by prototype before you write.

   Skip. L'utilisateur interdit les prototypes applicatifs. Consigner les inconnues et les preuves futures. Ne pas prétendre les avoir résolues par exécution.

3. Explore in subagents with `subagent_type: "poteto-agent"` and an explicit model per the Subagents section.

   Adapté. Le coordinateur affecte un agent par phase et peut ajouter des chercheurs en lecture seule. Le modèle imposé est GPT-6 Astra medium. Aucune délégation en cascade.

4. Copy the skeleton below into the plan file and fill every placeholder.

   Adapté. Le programme utilise les phases P1 à P5 approuvées. Le squelette applicatif avec boot, captures, dix lanes et merge par fonctionnalité ne correspond pas aux livrables autorisés. Les critères documentaires remplacent ces preuves applicatives.

5. Write under `/technical-writing` in full, then `/unslop`.

   Appliqué à la rédaction et à la revue de prose. Les fichiers de référence séparent les paramètres confirmés, propositions et inconnues.

6. Run `node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan.md>` and fix every line it prints.

   Skip. Ce vérificateur impose le squelette applicatif écarté. Vérifier les vrais liens, les identifiants, le TSV et les critères documentaires. N'installer aucun outil pour reproduire le squelette.

7. Hand back. Post the plan path and the script's output, then stop.

   Adapté. Remettre chaque phase au coordinateur pour revue. L'autorisation de poursuivre P1 à P5 existe déjà. La fin de P5 ne déclenche pas de développement.

### Autonomous run

1. State the exit condition as a checkable predicate before the first iteration.

   Appliqué dans le programme. P1 à P5 doivent être révisées et cohérentes. La publication exige des références distantes vérifiées.

2. Pick the wake mechanism using Cursor's `/loop` command.

   Adapté. Le coordinateur reste actif dans la session et attend les passations via les outils d'agents disponibles. Aucun service ou mécanisme local supplémentaire n'est installé.

3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help.

   Adapté. Une phase constitue une unité vérifiable. Le coordinateur révise avant la phase suivante et avant tout commit.

4. Mid-run discoveries are yours.

   Adapté. Corriger les documents dans le périmètre. Les réparations de skills, de machine et de logiciels voisins restent exclues par l'utilisateur.

5. Checkpoint every iteration via the **show-me-your-work** skill, a row for what changed and whether the predicate moved.

   Appliqué. Le journal est append-only et sera inclus dans le dossier publié.

6. Stop when the predicate is met.

   Appliqué. Terminer le dossier et la publication autorisée. Ne jamais réduire les critères pour annoncer la fin.

### Conserver le checkpoint de débit

- [x] Blocking first steps. Gates run before fan-out. Valider chaque phase avant ses dépendants.
- [x] Independent workstreams. Disjoint files, services, or layers parallelize. Shared writes serialize. Seules les recherches indépendantes peuvent avancer en parallèle de l'auteur.
- [x] Shared mutable state. Default to splitting the target. Serialize only for real invariants. Le dossier et le journal ont un seul écrivain.
- [x] Smallest safe decomposition. If one worker is best, name why. Un auteur par phase maintient les mêmes critères et identifiants entre documents.

### Garder les exceptions visibles

- [x] `architect skipped`. P1 cadre les usages. Les options documentaires relèvent de P3. Les prototypes et signatures de code n'appartiennent pas au travail autorisé.
- [x] Vérification runtime, UI et benchmarks applicatifs différée. Aucun produit n'existe. Leur résultat reste non démontré.
- [x] Revue multimodèle non exécutée. L'utilisateur impose un seul modèle et effort. La revue finale sera confiée à un nouvel agent GPT-6 Astra medium, puis examinée par le coordinateur.
- [x] `deslop` indisponible selon la recherche locale du coordinateur. Appliquer Unslop et une revue directe de prose. Ne pas réparer les skills hors périmètre.
- [x] `no-comments` adapté à la revue documentaire. Ne pas lancer un agent supplémentaire depuis une phase. Le coordinateur examine répétitions, prescriptions non prouvées et texte inutile.

## Passer les phases

- [x] Rédiger P1 avec usages, critères M1, corpus, inconnues, programme et journal.
- [x] Faire valider P1 par le coordinateur et consigner le passage. Voir la passation P1 et le journal.
- [x] Rédiger P2 avec registre canonique, sources, quinze familles et limites explicites. Voir [inventaire](inventaire-roon.md).
- [x] Vérifier les colonnes, identifiants, sources, dates, milestones et liens P2. Commande dans la [passation P2](passations/p2-inventaire.md).
- [x] Faire valider P2 par le coordinateur avant P3. Revue consignée dans la passation P2 et le journal.
- [x] Rédiger P3 avec trois formes, contrats, composants, fournisseurs, licences et études futures.
- [x] Vérifier les références P3 et préserver les critères et le registre P1-P2. Voir la [passation P3](passations/p3-architecture.md).
- [x] Faire valider P3 par le coordinateur avant P4. Revue consignée dans la passation P3 et le journal.
- [x] Rédiger P4 avec six plans, sept milestones, 28 phases et 50 scénarios futurs. Voir la [roadmap](roadmap.md).
- [x] Vérifier les 195 correspondances uniques, cas spécifiques conservés, liens et dépendances sans cycle. Commande dans la [passation P4](passations/p4-multiplan.md).
- [x] Faire valider P4 par le coordinateur avant P5 ou commit. Revue intégrale et autorisation de commit local consignées dans la passation P4 et le journal.
- [x] Rédiger et vérifier P5 avec couverture et cohérence. Voir la [revue finale](revue-finale.md) et la [passation P5](passations/p5-revue.md).
- [x] Faire valider P5 par le coordinateur avant commit. Lecture intégrale des nouveaux livrables et contrôle indépendant consignés dans la passation P5.

## Vérifier les fichiers et publier

- [x] Vérifier les liens locaux et les chemins de preuve du journal au dernier état du dossier.
- [x] Vérifier l'unicité et les références des identifiants ajoutés en P2 à P5.
- [x] Vérifier la largeur du TSV et l'absence de cellules interprétables comme formules.
- [x] Relire les critères M1 dans tous les plans. Vérifier le NAS, le volume cible, les sources intactes et l'usage sans Internet.
- [x] Vérifier les fichiers publiables. Exclure secrets, détails privés et médias réels.
- [x] Relire la prose et le journal avant commit. Ne pas présenter une revue indépendante comme déjà effectuée.
- [x] Après revue, créer les commits documentaires selon la stratégie du coordinateur. Les phases validées sont publiées. Voir le [reçu](publication.md).
- [x] Publier la branche et créer la PR autorisées. PR #1 ouverte et non draft, sans fusion. Voir le [reçu](publication.md).
- [x] Vérifier le SHA distant, le contenu de la PR et les liens de publication. Références initiales concordantes et commande de contrôle du HEAD final dans le [reçu](publication.md).
- [x] Préparer la remise publiée au coordinateur avec dossier, décisions ouvertes et limites de preuve. Le [reçu](publication.md) permet son contrôle avant le retour final au demandeur. Arrêt avant tout développement.
