# Clarifier les rôles Kuro et les scénarios de déploiement

Type: task
Status: resolved
Assignee: align_role_docs
Blocked by: 05

## Question

Comment séparer les rôles logiques KuroKor, Kuro Client et NAS des machines qui les hébergent, puis corriger le cadrage audio sans transformer une première cible en contrainte générale ?

## Comments

### 2026-09-06. Ticket réclamé

Le worker `align_role_docs` réclame ce ticket avant de modifier les documents courants. Les précisions viennent directement de l'utilisateur et remplacent l'interprétation selon laquelle le besoin imposait toujours deux machines.

## Answer

Les décisions suivantes viennent des précisions directes de l'utilisateur du 6 septembre 2026. Elles remplacent l'interprétation selon laquelle le chemin audio imposait toujours un serveur et un renderer sur deux machines distinctes. Elles ne constituent aucun résultat technique ou sonore.

### KD-044. Séparer les rôles logiques de leur hébergement

KuroKor est le rôle central. Il possède l'état durable de Kuro et coordonne la lecture. Un Kuro Client transmet les intentions de l'utilisateur et affiche l'état. Il ne décode pas, ne produit pas le son et ne transporte pas de PCM. Le NAS conserve les fichiers musicaux maîtres, que Kuro consulte en lecture seule. Cette fonction ne détermine pas l'emplacement physique de l'état de Kuro ou de ses sauvegardes.

Ces rôles ne fixent pas le nombre de machines. Dans le premier scénario, KuroKor et le Kuro Client occupent deux ordinateurs distincts, en plus du NAS. L'emplacement du point de lecture reste ouvert. Dans la première cible matérielle, KuroKor fonctionne dans le salon et pilote une chaîne locale `USB -> DDC -> I2S sur HDMI -> DAC Terminator`. Le Kuro Client peut partager cette machine ou fonctionner à distance. Un futur point de lecture UPnP resterait distinct du Kuro Client et ne rendrait pas le multiroom automatique dans U-M1.

### KD-045. Évaluer Rust en priorité sans choisir le langage de production

Kuro doit posséder ses tampons PCM et sa sortie audio. L'étude du futur cœur évalue donc Rust en priorité, avec les mêmes responsabilités, budgets mémoire, coûts réseau et contraintes de maintenance pour chaque candidat. Cette priorité ne vaut pas adoption de Rust et ne demande pas de portage immédiat.

Le laboratoire Go reste une preuve valide du transport et de ses erreurs. MPD reste un moteur testé pour comparaison, sans choix exclusif pour la production. L'analogie avec Roon n'admet pas automatiquement le DSP dans le produit.

## Evidence

L'utilisateur a nommé KuroKor, Kuro Client et NAS, puis a précisé leur responsabilité et deux scénarios d'hébergement. Il a confirmé que Kuro possède les tampons PCM et la sortie audio, et que ce choix rend Rust prioritaire à évaluer. Aucun moteur, langage de production, protocole réseau ou emplacement du point de lecture distant n'a été choisi dans ce ticket.
