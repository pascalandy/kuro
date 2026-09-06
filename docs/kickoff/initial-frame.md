> Historical kickoff attempt, superseded by the sound-quality transport requirement before arena selection. See [scope change](scope-addendum.md).

# Cadrage de l'arena de démarrage kuro

## Livrable borné de cette exécution

Le résultat attendu est une architecture de démarrage argumentée, puis un petit prototype exécutable qui met à l'épreuve ses décisions les plus coûteuses. Le dépôt décrit aujourd'hui un produit à construire. Les documents courants font autorité, en particulier leurs contrats KD et les études KB-010 à KB-015 et KB-022.

Cette exécution peut livrer les éléments suivants sans inventer de besoin produit.

1. Un paquet de conception synthétisé avec parcours d'appel, types, signatures, carte des modules et raisons des choix. Il distingue les choix du prototype des décisions de stack ou de licence qui exigent encore une étude.
2. Un prototype local isolé, lançable par une commande documentée, utilisant un corpus jetable généré par le dépôt. Il exerce au moins un parcours concret d'import ou d'enregistrement de médias, de consultation ou recherche, de préparation de file et de réouverture sans reprise automatique. Un adaptateur audio simulé ne constitue pas une preuve audio. Tout faux catalogue ou média simulé doit être identifié.
3. Un outil de vérification relançable qui observe l'état réel du prototype, produit les résultats bruts et vérifie les invariants retenus. Il couvre au minimum les références conservées après un changement de tags ou une absence de source, les doublons de file et la réouverture arrêtée. La vérification de sources intactes compare les octets avant et après les opérations du prototype.
4. Une étude de faisabilité audio et de dépendances proportionnée aux outils réellement disponibles. Une expérience avec décodage réel, si disponible, précise la sortie utilisée. Elle ne prétend pas garantir le gapless, tous les formats candidats ou le matériel final. L'absence de corpus accepté ou de sortie vérifiable reste une question ouverte documentée.
5. Un journal de décisions et un compte rendu de vérification qui rattachent chaque résultat aux contrats concernés. Les documents courants sont mis à jour seulement pour refléter l'existence et les limites du prototype. Des commits locaux séparent la conception stabilisée et le prototype vérifié si cette séparation aide la revue.

La fin de cette exécution signifie que ces artefacts existent, se relancent et ont des résultats consignés. Elle ne signifie ni U-M1.A accepté ni U-M1 complet, ni KB-011 clôturé. Les mesures sur 20 000 albums, 3 To, le NAS réel, le paquet en environnement propre et les captures gapless attendent leur corpus et leur environnement. L'utilisateur a autorisé une mise en oeuvre après synthèse et des commits autonomes. Cette autorisation ne vaut pas acceptation du produit.

Si le prototype minimum dépasse un choix technique raisonnablement vérifiable, conserver un parcours plus petit et expliquer exactement quelle partie de cette preuve reste absente. Ne pas remplacer les preuves par des mocks non déclarés.

## Prompt commun remis aux candidats

Produis une proposition d'architecture pour démarrer kuro et choisir le premier prototype que le parent implémentera après synthèse. Lis intégralement `architect/SKILL.md`, `architect/references/runner-prompt.md`, `architect/references/rationale-template.md` et `architect/references/design-red-flags.md`. Respecte le cadrage courant du dépôt et le dossier de grounding partagé fourni par le parent. Les archives constituent un historique, pas une autorisation de restaurer d'anciens choix.

Le périmètre produit comprend uniquement les usages existants de U-M1. L'exécution actuelle doit produire une architecture concrète et un prototype local relançable qui fournit des preuves limitées sur import ou enregistrement de médias, consultation ou recherche, préparation de file et réouverture arrêtée. Les fichiers réels du corpus utilisateur restent intacts. Un corpus jetable généré dans un répertoire de test permet les manipulations destructrices nécessaires à la vérification. Choisis un périmètre réalisable et indique ses limites au lieu de promettre un lecteur complet.

Écris d'abord l'expérience visible et deux ou trois vrais exemples d'appel. Déduis ensuite les types, signatures et modules. Le paquet comporte `rationale.md` selon le modèle fourni, un `sketch` lisible avec les corps non implémentés, et un plan de preuve avec commandes envisagées et résultat observable attendu. Ne produis pas l'implémentation complète. La section de synthèse reste à remplir par le parent.

Trace au moins ces questions dans les structures et leurs accès dominants : identité de source indépendante du chemin, référence durable liée à la source et au chemin relatif, absence distincte du retrait, occurrences distinctes d'une même piste dans la file, piste courante conservée lors d'un réordre, reprise arrêtée après redémarrage. Les fichiers remplacés au même chemin relèvent encore de KB-022. Ne résous pas silencieusement cette question en assimilant tags, chemin ou empreinte à une identité de contenu.

Montre qui écrit l'état durable et comment une requête reçue pendant un scan est regroupée ou différée. Concentre les politiques derrière peu d'opérations. La vue ou la commande cliente ne doit pas connaître les étapes d'une transaction, le format de stockage ou les règles internes du moteur audio. Compare explicitement au moins une autre organisation des responsabilités.

Explique la relation entre le prototype et le futur service de session qui survit à la fermeture de fenêtre. Une interface terminal peut servir la preuve initiale, mais elle n'est pas la livraison de l'expérience desktop. Une interface graphique proposée décrit au moins la navigation album/liste avec retour au contexte et la présence continue des commandes de lecture. N'introduis ni favoris, recommandations, MPRIS, mobile ni gestion du montage NAS dans le démarrage.

Propose une technique de prototype à partir des faits disponibles. Sépare ce choix réversible d'une adoption de stack, d'une licence ou d'une garantie audio. Énumère les preuves encore nécessaires pour import, recherche, audio, paquet, reprise et restauration. Si le prototype utilise un moteur audio, indique comment distinguer décodage, routage de sortie partagé et gapless mesuré. Aucun silence sur ces distinctions ne peut servir de preuve.

Écris exclusivement dans ton répertoire candidat. Le dépôt de travail et les fichiers des autres candidats restent en lecture seule. Livre une proposition ferme et concentrée, avec alternatives rejetées, risques et première étape immédiatement implémentable.

## Points de vue remis séparément

Chaque candidat reçoit le même prompt ci-dessus et un seul angle ci-dessous. L'angle force une autre organisation des responsabilités sans changer les exigences.

### A. Bibliothèque transactionnelle et service propriétaire

Pars d'un service de session qui possède le catalogue, la file et les transactions, avec une vue desktop cliente. Cherche des opérations métier qui cachent la coordination de stockage, scan et lecture. Évalue un prototype piloté par commande, la séparation requête/événement et le contrat de fermeture de fenêtre. Résiste à la multiplication de couches et de bus génériques.

### B. Session de lecture gouvernée par une machine à états

Pars des gestes de l'utilisateur et des transitions de file/lecture. Une machine à états définit les effets autorisés, avec catalogue et persistance derrière ses accès. Évalue ce que ce centre de gravité simplifie pour les occurrences en doublon, la perte de sortie, le redémarrage et les erreurs bornées. N'en fais pas un journal d'événements universel par défaut. Justifie comment l'import continue sans que le modèle de lecture possède tout le catalogue.

### C. Application native concentrée autour d'un document de bibliothèque

Pars d'une application desktop dont la durée de vie appartient à la session et dont la fenêtre est une projection du document durable. Regroupe le catalogue, les opérations de bibliothèque et la navigation derrière une API locale sans transport initial. Évalue un processus unique, une fenêtre fermable et un moteur audio intégré ou adapté. Le prototype peut isoler le coeur exécutable. Précise la frontière qui permettra de respecter le service de session sans imposer dès maintenant un daemon RPC. Compare la simplicité de ce modèle à la robustesse des deux autres formes possibles.

## Rubrique réservée au parent et au juge

Ne pas transmettre cette section aux candidats. Chaque critère se note de 0 à 2 : 0 absent ou contradictoire, 1 partiel, 2 démontré par un parcours, une signature ou une preuve envisagée vérifiable. Total sur 12. Une contradiction non corrigée avec le cadrage élimine la proposition, quel que soit son score.

| Critère | Condition pour 2 points |
| --- | --- |
| Contrats d'identité et de file | Les types distinguent source, référence de piste et occurrence de file. Les chemins de tags modifiés, absence/retrait, doublon/réordre et reprise arrêtée se tracent sans convention cachée chez l'appelant. |
| Responsabilités concentrées | Deux ou trois appels couvrent les parcours montrés sans exposition de transaction ou de pipeline. Un propriétaire de chaque invariant durable est nommé et les requêtes de scan concurrentes ont une règle explicite. |
| Prototype réalisable | Le paquet désigne les fichiers et commandes du premier parcours exécutable, avec dépendances connues ou à vérifier, corpus généré et différence nette entre ce qui sera réel et simulé. |
| Preuves falsifiables | Le plan observe l'état durable réel après réouverture, les doublons et l'absence de source, et compare les sources avant/après. Il indique résultats attendus, limites et lien aux KD/KV sans transformer un test partiel en acceptation. |
| Expérience et cycle de vie | Un parcours utilisateur montre catalogue, album et commandes de lecture, conserve le contexte de navigation, et explique précisément comment le processus survit à la fermeture de fenêtre puis s'arrête à Quitter. Les limites du prototype sont distinguées. |
| Discipline d'adoption | La proposition garde ouverts stack final, licence, corpus/mesure gapless, NAS et paquet tant que leurs preuves manquent. Elle propose un prochain test décisif pour les risques majeurs au lieu de les déclarer résolus par la conception. |

À égalité, préférer la proposition qui expose le moins de règles internes aux appelants et permet de supprimer le plus de code de coordination. Le parent lit chaque candidat intégralement, confronte son classement à celui du juge puis consigne base, greffes et rejets. Tous les candidats et le juge utilisent GPT-6 Astra, raisonnement high, conformément à l'instruction utilisateur.
