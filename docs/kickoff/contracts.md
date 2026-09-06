# Contrats de conception et limite du laboratoire

Ce document sépare l'esquisse du produit et l'outil construit pendant le démarrage. Les signatures produit sont du pseudocode non implémenté. Elles conservent le candidat MPD du kickoff afin de rendre ses limites examinables. L'étude de KuroKor doit réévaluer la propriété du moteur et la limite locale ou distante avant toute implémentation produit. Le contrat Go exact du laboratoire vit dans [le plan d'implémentation](implementation-plan.md). KD-044, KD-045.

## Esquisse produit et rôles logiques

| Élément | État durable | État temporaire ou responsabilité |
| --- | --- | --- |
| KuroKor | Sources, références, métadonnées, playlists, occurrences de file, meilleur point enregistré, préférences et pochettes détenues | Préparations, sessions, erreurs, autorisations média et coordination de lecture |
| NAS | Fichiers musicaux maîtres | Accès aux médias en lecture seule; aucun second catalogue faisant autorité |
| Kuro Client | Préférences locales de présentation, si elles existent | Intentions de l'utilisateur, contexte de navigation et état reçu de KuroKor |
| Moteur audio à étudier | Aucune autorité durable distincte | Décodage, tampons PCM et sortie audio possédés par Kuro; hébergement local ou distant à fixer |
| MPD de référence | Aucune reprise de file faisant autorité | File courte, décodeur et tampons observés seulement dans le candidat du kickoff |

Le tableau attribue l'autorité logique. Il ne fixe pas le support physique des données applicatives ou des sauvegardes. KuroKor ne modifie pas les fichiers musicaux maîtres. Un stockage NAS distinct pourrait être étudié pour les données applicatives ou les sauvegardes sans déplacer l'autorité logique.

L'état matériel du DDC et du DAC reste externe. Le rôle réel de leurs horloges est inconnu avant inventaire. Les réglages logiciels, les données observées et les inconnues ont des statuts distincts.

## Types et opérations produit

```text
SourceId, ReferenceId, OccurrenceId, SessionId, Generation, OperationId = identifiants distincts
CatalogReference = {id: ReferenceId, source: SourceId, relative: SafeRelativePath}
Source = Active(root) | Removed
Availability = Present | Missing(reason) | ChangedUnresolved
TransferObject = {sha256, bytes}          # Version des octets, jamais identité catalogue.
Occurrence = {id: OccurrenceId, media: ReferenceId}
Queue = {revision, ordered_occurrences, current: OccurrenceId?}
Position = {occurrence, best_reported_time, observed_at, uncertainty}
Playback = Stopped | Preparing | Playing | Paused | Failed
Evidence<T> = Configured(T) | Observed(T, artifact) | Unknown(reason)
SignalPath = {source_format, decoded_format, delivered_format, transforms, downstream}
Preparation = {id, requested_selection, base_revision, readiness}
SessionView = {queue, position?, playback, pending_preparation?, signal_path, errors}

Session.play_album(album, output, operation) -> accepted | error
Session.edit_queue(edit, revision, operation) -> SessionView | error
Session.control(play | pause | stop | seek | previous | next | quit,
                revision, operation) -> SessionView | error
Session.snapshot() -> SessionView

# Frontière privée, aucun Kuro Client n'appelle ces étapes.
PlaybackPoint.prepare(plan, generation) -> preparation | error
PlaybackPoint.activate(preparation, generation) -> observation | error
PlaybackPoint.observe() -> observation
PlaybackPoint.stop(generation, reason) -> observation
```

`play_album` compose préparation et activation sous le geste Lecture initial. La préparation d'un remplacement garde la file active jusqu'à ce que le nouveau plan soit prêt et encore valide. Une modification concurrente invalide un ticket devenu périmé. L'activation n'est pas un simple acquittement réseau; l'interface montre la phase réelle et les erreurs. Le Kuro Client ne coordonne pas ces étapes.

KuroKor est la seule autorité logique qui écrit les données durables de Kuro par transactions courtes. Un worker de scan retourne des lots. Une demande supplémentaire pendant scan devient au plus un passage différé. Aucun accès aux fichiers musicaux du NAS ne conserve une transaction ouverte.

`SourceId` ne dépend pas du montage. Tags modifiés et relocalisation explicite conservent les références selon les contrats courants. Retrait et absence diffèrent. Réajouter un chemin retiré ne réactive pas l'ancienne source. L'identité de contenu remplacé au même chemin reste KB-022. Un SHA-256 de transfert ne tranche pas cette question.

Les doublons possèdent des `OccurrenceId` différents. Réordonner conserve l'occurrence courante. La retirer ou vider la file arrête. Les rapports du point de lecture portent session, génération et occurrence. Une observation ancienne ne fait pas avancer la nouvelle file. La position durable exprime le meilleur point rapporté et son incertitude, jamais une exactitude implicite à l'échantillon.

## Politiques média du candidat à comparer

Le candidat progressif donne une URL au moteur. Le candidat préparé écrit un temporaire par transfert, vérifie longueur et empreinte puis publie atomiquement un fichier local. Dans l'essai MPD, seuls les fichiers complets entrent dans sa projection locale. Le budget de préparation compte courant, suivant et partiels. Il ne peut pas évincer une réservation active pour dissimuler un manque de capacité.

Une préparation de la piste suivante tardive peut arrêter à la frontière. Sa fin ultérieure ne redémarre rien. L'attente initiale et l'activité disque supplémentaires sont des coûts explicites du mode préparé. Aucun des deux modes n'est déclaré meilleur en qualité sonore.

La production doit garantir une version cohérente pendant une reprise de fichier NAS. Le laboratoire utilise des fixtures immuables. Il ne décide ni d'un spool NAS supplémentaire ni d'une preuve universelle de stabilité fondée sur `stat`.

## Arrêts et récupération proposés

La perte du service média et celle du contrôle sont deux événements. Un fichier complet peut rester lisible si seul le service média tombe. La perte du contrôle arrête après expiration d'un délai mesuré, même avec des fichiers prêts. Retour du réseau, retour du périphérique et redémarrage restent arrêtés. Un essai sans aucun trafic réseau est un mode de laboratoire distinct.

Dans le candidat du kickoff, l'agent est le seul client du MPD privé. Sa supervision doit arrêter MPD si l'agent meurt. Cette règle reste une hypothèse à comparer avec un moteur audio possédé par Kuro. La fermeture de fenêtre laisse KuroKor actif. Quitter attend l'arrêt ou en rapporte l'incertitude. Le mécanisme réseau authentifié et son délai restent à éprouver lorsque le point de lecture est distant. Le Kuro Client n'est jamais ce transport audio.

KuroKor dirige la sauvegarde des données durables et des pochettes détenues sans dépendre d'un snapshot du point de lecture. Le support physique de la sauvegarde reste à choisir. Les caches et secrets restent exclus. La restauration conserve une génération précédente récupérable et invalide toute autorisation de lecture antérieure. La preuve de restauration demeure un lot produit futur.

## Ce que le laboratoire implémente

Le laboratoire est un exécutable Go autonome. Il génère ses deux fixtures, les sert sur loopback et reçoit les données dans des fichiers temporaires isolés. Il vérifie admission atomique, reprise avec validateur, corruption, troncature, budget et retard injecté. Il conserve les traces qui permettent de recalculer un consommateur progressif et un départ après préparation complète.

Le PCM canonique fixe fréquence, signedness, endian, profondeur utile, taille du mot, entrelacement et ordre des canaux. L'empreinte du WAV comprend en-tête et métadonnées; l'empreinte PCM porte sur les mots d'échantillons. Une égalité à l'une de ces frontières ne prouve pas les suivantes.

| Niveau | Observation dans cette exécution | Limite |
| --- | --- | --- |
| HTTP Go | Corps reçus, plages, validateurs, tailles, empreintes et admission | Loopback et fixtures seulement |
| Consommation calculée | Échéances et périodes manquantes recalculées depuis les arrivées | Modèle, aucun MPD ni USB |
| FLAC séparé | Encodage puis décodage vers PCM canonique, si exécutés | Codec et fixtures identifiés |
| MPD FIFO séparé | PCM capturé silencieusement, si exécuté | Build FIFO, aucune sortie ALSA dans le build de test |
| USB, DDC, DAC et analogique | Aucune observation par le laboratoire Go | Inventaire et essai physique encore requis |

Le laboratoire n'implémente ni les types produit ci-dessus, ni SQLite, ni NAS, ni interface, ni agent de session, ni bail réseau. Il ne peut donc valider aucun KV complet. L'état des contrôles effectivement exécutés est consigné dans [la synthèse](synthesis.md).
