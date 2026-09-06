# Réviser le cadrage avec un second entretien indépendant

Type: grilling
Status: resolved
Assignee: orchestrateur avec interviewer_independent
Blocked by: 02

## Question

À partir de la projection courante, quelles contradictions, limites ou décisions manquantes un second entretien indépendant révèle-t-il avant la réconciliation finale ?

## Comments

### 2026-09-06. Reprise de l'entretien indépendant

Un nouvel agent `interviewer_independent` a démarré avec le profil GPT-6 Astra high demandé. Le ticket est réclamé avant le premier échange de questions et réponses. L'orchestrateur répond par délégation explicite de l'utilisateur. Les décisions issues de cet échange restent des arbitrages délégués, pas des citations de l'utilisateur.

### 2026-09-06. Lancement bloqué avant l'entretien

Ce commentaire conserve l'état historique avant la reprise décrite plus haut. La résolution présente de ce ticket remplace cet état.

L'orchestrateur a tenté de lancer un nouvel agent GPT-6 Astra avec effort medium. Le worker documentaire a refait une tentative avec `fork_turns: none`. Les deux appels ont échoué avec `agent thread limit reached`. Aucun agent de remplacement n'a été utilisé, aucune question du second entretien n'a été posée et aucune réponse n'a été simulée.

Le ticket reste `open` avec `Assignee: none`. Une nouvelle session doit tenter de lancer un intervieweur indépendant, puis réclamer ce ticket avant l'entretien. Le refus observé ne prouve pas que la limite sera levée dans cette session future.

L'intervieweur doit lire les instructions et skills suivants avant de travailler :

- `../AGENTS.md` et `../johnny/INDEX.md`, depuis la racine de kuro
- `../dotfiles/dot_config/ai_templates/skills/mattpocock/wayfinder/SKILL.md`
- `../dotfiles/dot_config/archived_ai_templates/archived_skills/_ARCHIVES/grilling-og/SKILL.md`, autorisé comme `grilling-v2`
- `../dotfiles/dot_config/ai_templates/skills/mattpocock/domain-modeling/SKILL.md`, `CONTEXT-FORMAT.md` et `ADR-FORMAT.md`
- `../dotfiles/dot_config/ai_templates/skills/mattpocock/setup-matt-pocock-skills/issue-tracker-local.md`
- `../../.codex/skills/technical-writing/SKILL.md`
- `../../.codex/skills/unslop/SKILL.md`

Pour préserver l'indépendance, l'intervieweur lit le cadrage courant et le backlog, mais pas la réponse détaillée du ticket 01 avant d'avoir terminé ses propres questions. L'orchestrateur peut répondre au nom de l'utilisateur, conformément à l'autorisation existante.

## Answer

L'entretien indépendant est terminé le 6 septembre 2026. L'agent `interviewer_independent`, GPT-6 Astra high, a utilisé Wayfinder, Domain Modeling et la variante `grilling-v2` déjà retenue dans cette carte. L'orchestrateur a répondu à quinze questions en trois rounds au nom de l'utilisateur, conformément à sa délégation explicite. L'intervieweur a confirmé qu'aucune question de cadrage ne reste ouverte.

Les questions ont été élaborées sans lire la réponse du premier entretien. L'intervieweur l'a consultée seulement après le dernier round pour vérifier les amendements. Il n'a modifié aucun fichier. Les réponses ci-dessous sont des arbitrages délégués, pas des citations de l'utilisateur ni des résultats techniques. Les études futures restent au backlog et conditionnent l'adoption concernée.

### KD-026. Démontrer U-M1 progressivement sans réduire son acceptation

Trois passages internes donnent des résultats utilisables : U-M1.A importe un dossier et joue un album; U-M1.B permet de retrouver la musique et de préparer playlists et file; U-M1.C couvre reprise, NAS et sauvegarde, puis vérifie l'échelle, l'usage sans Internet et le paquet. Ces passages ne constituent aucune acceptation partielle des dix critères MVP. Complète KD-001.

### KD-027. Borner la recherche et les tris initiaux

U-M1 recherche les titres d'album, les titres de piste et les artistes, sans distinction de casse ou d'accents. Les listes utilisent un ordre alphabétique stable. Les pistes d'un album suivent les numéros de disque et de piste, avec un repli déterministe explicite quand ils manquent. Les résultats donnent le contexte album et source nécessaire aux homonymes. Recherche floue, opérateurs et filtres combinables ne conditionnent pas U-M1. Les budgets de KD-015 restent des objectifs à mesurer.

### KD-028. Remplacer la promesse d'identité universelle par une référence de catalogue

U-M1 conserve une référence lors d'une relocalisation explicite de racine dont les chemins relatifs restent identiques. Un renommage interne peut produire une ancienne référence indisponible et un nouveau fichier distinct. Aucun rapprochement silencieux par nom, tags ou empreinte n'est promis. La détection d'un contenu remplacé au même chemin reste une question précise de l'étude d'import et d'identité. Précise KD-013 et corrige le glossaire courant.

### KD-029. Distinguer source retirée et source indisponible

Un retrait explicite masque les médias de cette source dans les vues courantes, mais conserve les références indisponibles des playlists et de la file. Un scan, même réussi, ne purge jamais automatiquement les références durables. Ajouter de nouveau le même chemin ne réactive pas silencieusement une source retirée. Une purge éventuelle constitue une opération distincte au backlog. Complète KD-016 et KD-021.

### KD-030. Définir le contenu utile d'une sauvegarde

Une sauvegarde manuelle cohérente conserve les choix, les relations durables et les métadonnées déjà connues, afin de parcourir aussi les médias temporairement absents. Elle inclut les pochettes durables détenues par l'application. Les images présentes dans les sources restent des fichiers externes consultés en lecture seule, comme les médias audio. La restauration remplace une bibliothèque après aperçu et confirmation; elle ne fusionne pas deux bibliothèques. Les médias absents restent indisponibles. Historique automatique et migration depuis un autre lecteur ne sont pas requis. Précise KD-002 et KD-006.

### KD-031. Faire du mobile une étude conditionnelle après le desktop

U-M4 autorise seulement l'ouverture d'une étude mobile. U-M1 doit être accepté, les parcours desktop retenus et la restauration prouvés, et U-M2/U-M3 achevés ou explicitement reportés avec une raison. Il faut ensuite au moins quatorze jours d'usage représentatif depuis la dernière correction bloquante, sans blocage, perte de données ou incident critique non résolu. Cette durée ne suffit pas seule à autoriser le passage. Télécommande, lecture sur téléphone, accès distant et téléchargement ne sont pas engagés. Remplace la portée encore indéterminée de KD-008.

### KD-032. Maintenir une roadmap ordonnée et révisable par les usages

La destination reste écouter et retrouver sa propre musique. U-M2 puis U-M3 forment des priorités présumées, à revalider à partir de l'usage réel. Roon fournit des usages de référence sans créer un objectif de parité. Les 195 fonctions doivent recevoir une disposition courante, mais leur présence dans l'inventaire ne constitue aucun engagement de réalisation. Précise KD-007.

### KD-033. Rendre les métadonnées imparfaites utilisables

La vue artistes présente les artistes d'album selon `albumartist`, puis `artist`, puis une valeur inconnue explicite. La recherche couvre aussi l'artiste de piste. Sans titre, la piste utilise son nom de fichier et l'album son dossier, avec un repli identifiable. Les disques ne sont regroupés que lorsque les informations et le contexte d'une même source concordent; copies et éditions ne fusionnent pas automatiquement. U-M1 permet de voir et lire les cas ambigus. Leur correction manuelle dans les données applicatives reste candidate pour U-M3. Complète KD-017 sans autoriser l'écriture dans les sources.

### KD-034. Fixer les opérations de playlist et de file

U-M1 permet de créer, nommer, renommer et supprimer une playlist, puis d'ajouter, retirer et réordonner ses pistes. Les doublons sont conservés. La lecture d'une sélection remplace la file et démarre sa première piste. **Jouer ensuite** insère après la piste courante, ou en tête en l'absence de piste courante sans démarrer. **Ajouter** insère en fin sans démarrer. La sélection initiale peut être un album ou une piste.

Retirer la piste courante arrête la lecture et conserve le reste de la file; vider la file arrête; réordonner conserve la piste en cours. Précédent et suivant parcourent la file; précédent depuis sa première piste revient au début de celle-ci. La reprise de la piste restaurée prévue par KD-004 et KD-012 reste distincte de la lecture d'une nouvelle sélection. Mélange et répétition sont candidats U-M2. Multisélection avancée, historique d'écoute, conversion file vers playlist, import-export et playlists intelligentes restent au backlog. Complète KD-018.

### KD-035. Préserver la bibliothèque existante lors d'une restauration échouée

Une sauvegarde invalide ou incompatible, ainsi qu'une restauration interrompue, laissent l'état précédent récupérable. La compatibilité est vérifiée avant remplacement, l'aperçu montre les sources manquantes et la restauration réussie repart sans son. U-M1 garantit la restauration de son propre format livré. Les migrations entre versions seront définies lorsqu'une nouvelle version existe. Complète KD-006 sans imposer maintenant une infrastructure universelle de migration.

### KD-036. Conserver les progrès utiles pendant l'import

Les éléments déjà catalogués restent consultables et jouables pendant le scan. Une nouvelle demande de scan est regroupée ou différée lorsqu'un scan tourne. Un fichier invalide ne bloque pas les autres. L'annulation conserve les éléments déjà catalogués et permet une reprise ultérieure. Une modification de tags au même chemin conserve la référence, sans étendre cette garantie aux renommages ou au remplacement du contenu audio. Les mécanismes de détection, les délais et la concurrence restent à étudier. Complète KD-016.

### KD-037. Donner aux étapes suivantes un résultat observable limité

U-M2 permet de marquer albums ou pistes comme favoris, de les retrouver et de filtrer selon des champs locaux retenus après usage. U-M3 permet de distinguer et d'organiser volontairement éditions et coffrets tout en conservant les références existantes. Des corrections internes de métadonnées peuvent y être admises. Ces étapes n'imposent ni moteur de recommandation, ni œuvres et mouvements, ni crédits détaillés, ni enrichissement externe. Leurs critères détaillés seront précisés après U-M1. Complète KD-007 et KD-032.

### KD-038. Attribuer explicitement les arbitrages futurs

L'utilisateur accepte les résultats produit et les changements de portée. Le futur agent ou développeur du lot apporte les preuves techniques. Les responsables du backlog désignent des rôles, sans supposer une équipe constituée. Une étude négative impose un nouvel arbitrage explicite; elle ne permet pas de diminuer silencieusement le volume cible, le gapless retenu ou la restauration. Les réponses des entretiens sont des décisions déléguées, distinctes des faits utilisateur et des résultats mesurés. Complète KD-025.

### KD-039. Limiter l'audio initial à la sortie partagée

Le corpus candidat reste PCM stéréo. DSD, DSF, DFF, multicanal, volume matériel et traitement du signal sont hors U-M1. Le contrôle système de la sortie partagée suffit initialement pour le volume. Une commande dans kuro peut être adoptée après étude audio, sans devenir un critère caché du MVP. kuro n'augmente jamais automatiquement le volume et ne réimpose pas au système un ancien volume au démarrage. Le volume système courant fait autorité. La perte de périphérique arrête la lecture sans repli automatique. Complète KD-014 et KD-011; amende KD-020, dont la mémorisation ne doit pas être comprise comme une obligation de restaurer le volume système.

### KD-040. Préserver le contexte de navigation et montrer l'écoute courante

U-M1 permet de revenir d'un album à la liste ou à la recherche précédente en conservant sa place. La piste en cours et ses commandes sont visibles sans exiger une vue plein écran. Historique général de navigation, plein écran et multisélection avancée restent au backlog. Les commandes précédent/suivant audio et la file persistante restent dans U-M1. Complète KD-019 sans prescrire une interface particulière.

## Evidence

L'intervieweur a consulté le cadrage courant, le backlog, le glossaire, les critères MVP, le contexte utilisateur et l'inventaire fonctionnel initial. La réponse du premier entretien a été lue après clôture des questions. Aucune source externe n'a été consultée directement par cet intervieweur et aucun comportement de kuro n'a été testé. La recherche documentaire parallèle sur Roon est distincte de cet entretien et sera référencée dans la réconciliation.
