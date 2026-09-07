# Contrats non implémentés

## Chemin et propriétaires

```text
Fenêtre/CLI -- requêtes + état --> service Kuro [choix durables]
                                     |
NAS monté, lecture seule -> origine HTTP Kuro -> TCP/SSH -> MPD au salon
                             octets originaux             |
                                   agent -> socket MPD    décodeur
                                   contrôle seulement     tampon PCM
                                                          ALSA hw
                                                          tampon pilote
                                                          USB -> DDC
                                                          I2S -> Terminator
```

| Composant propriétaire | État durable | État temporaire et cadence |
| --- | --- | --- |
| Service Kuro | sources, références, métadonnées, playlists, occurrences de file, position enregistrée, préférences, pochettes détenues | sessions, autorisations de fichiers, erreurs ; aucun timer audio |
| Origine dans Kuro | aucun second état de bibliothèque | descripteurs de fichiers, lectures bornées ; cadence HTTP selon demandes et contre-pression TCP |
| Agent salon | identité d'installation et configuration du périphérique, secrets hors sauvegarde | session, échéance de bail, correspondance occurrence/ID MPD ; timer monotone de surveillance |
| MPD privé | aucune file ni lecture restaurée par MPD | entrées originales, décodeur, tampon PCM, file projetée ; alimentation selon consommation ALSA |
| ALSA et pilote USB | configuration de machine hors bibliothèque | ring buffer, format matériel, XRUN ; cadence dépendant du mode USB réel |
| DDC puis DAC | réglages matériels à relever | tampons, FIFO, reclocking et horloge de conversion inconnus pour les exemplaires exacts |

La cadence réseau et le timer du modèle synthétique ne sont pas l'horloge physique de conversion. Un endpoint USB asynchrone suit une horloge indépendante du start-of-frame USB, mais ce mode doit être lu sur le DDC. I2S transporte données et horloges ; contrôleur, pinout et reclocking exacts restent à relever. [USB Audio 2.0](https://www.usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf), [I2S NXP](https://www.nxp.com/docs/en/user-manual/UM11732.pdf).

## Types et signatures métier

```python
# Pseudocode, aucun corps implémenté. Les unions sont des états exclusifs.
SourceId = OpaqueId                 # Indépendant de la racine montée.
CatalogRef = Record(id=RefId, source=SourceId, relative=SafeRelativePath)
Source = Active(SourceId, RootPath) | Removed(SourceId)
Availability = Present | Missing(Reason) | ChangedUnresolved
Occurrence = Record(id=OccurrenceId, media=RefId)  # Doublons permis.
Queue = Record(revision=Revision, ordered=List[Occurrence], current=OccurrenceId | None)
Cursor = Record(occurrence=OccurrenceId, best_position=Duration)
BootState = Record(queue=Queue, cursor=Cursor | None, transport=Stopped)
Evidence[T] = Documented(T, SourceURL) | Observed(T, ArtifactId) | Unknown(Reason)
SignalPath = Record(source=Evidence[Format], decoded=Evidence[Format],
                    delivered=Evidence[Format], transforms=Evidence[List[Transform]],
                    usb_mode=Evidence[ClockMode], downstream=Evidence[Description])
Prepared = Record(id=PlanId, renderer=RendererId, queue_revision=Revision)
Playback = Stopped(Cursor | None) | PreparedState(Prepared) | Priming(SessionId) \
         | Playing(SessionId, Cursor, SignalPath) | Failed(Error, Cursor | None)

class Session:
    def select_device(self, renderer: RendererId) -> DeviceReport: raise NotImplementedError
    def prepare(self, selection: Selection, renderer: RendererId) -> Prepared | Rejected: raise NotImplementedError
    def start(self, plan: PlanId) -> Playback: raise NotImplementedError
    def status(self) -> SessionSnapshot: raise NotImplementedError
    def control(self, action: Stop | Seek | Next | Previous | Quit) -> Playback: raise NotImplementedError
    def edit_queue(self, edit: Append | InsertNext | Reorder | Remove) -> Queue: raise NotImplementedError
    def scan(self, source: SourceId) -> ScanAccepted | Coalesced: raise NotImplementedError

# Frontière privée serveur/agent. Les messages SSH/MPD/HTTP sont parsés ici.
class Renderer:
    def prepare(self, plan: PlaybackPlan) -> Prepared | Rejected: raise NotImplementedError
    def start(self, session: SessionId, plan: PlanId) -> Playback: raise NotImplementedError
    def observe(self) -> RendererReport: raise NotImplementedError
    def stop(self, session: SessionId, reason: StopReason) -> None: raise NotImplementedError
```

Les méthodes restantes couvrent les contrats conservés, sans les inclure dans le premier programme de preuve. `prepare` crée un plan arrêté ; une préparation pendant lecture demande d'abord un arrêt explicite. Les modifications de file pendant lecture passent par `edit_queue`, préservent l'occurrence courante et projettent seulement les changements futurs. Lecture d'un nouvel album sera une action métier unique qui compose préparation et départ à l'intérieur de Session.

## Écriture, identités et reprise

Un seul écrivain dans Session valide les requêtes et écrit SQLite en transactions courtes. Scan utilise un worker avec messages bornés ; aucune transaction ne reste ouverte pendant une lecture NAS. Chaque source possède un scan actif et un bit `rescan_requested` : toutes les demandes concurrentes deviennent un seul passage supplémentaire. Les résultats portent la révision de source et ne survivent pas à son retrait/relocalisation sans nouvelle résolution.

Index durable unique sur `(SourceId, relative)` pour résoudre une référence ; ID opaque pour les liens de file. Absence et retrait diffèrent. Relocaliser modifie la racine, pas SourceId. Réajouter un chemin retiré crée une nouvelle source. Un digest de transfert ne définit jamais l'identité du catalogue ; KB-022 reste ouvert pour contenu remplacé. L'origine sert un handle borné sous la racine autorisée, refuse sortie par symlink et mutation détectée ; un stat stable n'est pas une preuve universelle d'immutabilité pendant lecture.

La file est ordonnée par occurrences, avec `current` par ID. Réordonner ne déplace pas l'identité courante ; la supprimer arrête. La traversée porte un ensemble temporaire d'occurrences déjà tentées et visite chaque indisponible au plus une fois. L'agent projette courante et suivante dans MPD et mappe `(session, revision, occurrence)` vers ID MPD ; les observations périmées ne changent pas la session actuelle. La prochaine occurrence doit être installée avant la frontière de piste ; la preuve de transition mesure cette contrainte.

Le client reçoit une réponse à chaque requête. L'agent remonte des snapshots d'état et erreurs ; pas de bus métier générique ni journal d'événements durable. Les notifications UI peuvent simplement invalider son snapshot. Les identifiants de plan/session rendent `start` rejoué idempotent ; après crash, aucune intention de départ persistée n'est rejouée.

Le service survit à la fenêtre ; Quitter attend l'arrêt rapporté puis se termine. En perte de connexion ou expiration d'un bail monotone renouvelé par le serveur, l'agent stoppe MPD et exige une nouvelle action Lecture. Valeur expérimentale du bail : 2 secondes, à mesurer ; ce n'est pas un arrêt physique instantané. Si l'agent meurt, son superviseur arrête aussi MPD. Au démarrage agent/service, MPD est arrêté avant acceptation d'un nouveau plan. Ne jamais restaurer son propre fichier de lecture.

Sauvegarde future : snapshot cohérent des données durables et pochettes détenues, sans médias, secrets, index ni caches. Restauration validée dans un état distinct, remplacement atomique, ancienne génération récupérable et démarrage arrêté. Pas de restauration complète dans la preuve transport.

## Capacité du renderer initial

| Capacité | Fait documentaire | Observé sur cible |
| --- | --- | --- |
| Lecture à la demande | MPD accepte des URL ; Kuro doit encore fournir l'origine | Inconnu |
| Appareil/découverte | Configuration explicite de l'agent et de la sortie ; pas de multicast requis | Inconnu |
| Formats/fréquences | `decoders` décrit le build MPD ; formats ALSA dépendent du DDC | Inconnu |
| Commandes/seek | MPD expose lecture, stop, position et seek ; seek HTTP dépend aussi des plages et du décodeur | Inconnu |
| Volume | MPD offre des contrôles de mixeur ; profil sans mixeur logiciel, volume aval à identifier | Inconnu ; jamais restaurer/augmenter un volume |
| Transition | File MPD et prélecture documentées ; aucune durée garantie pour cette chaîne | Gapless à mesurer |
| État/erreurs | `status`, notifications `idle` et réponses d'erreur du protocole | Projection Kuro non implémentée |

Sources de cette matrice : [protocole MPD](https://mpd.readthedocs.io/en/stable/protocol.html), [manuel MPD](https://mpd.readthedocs.io/en/stable/user.html). Aucun protocole Aurender ou RAAT n'est présumé disponible.

Modules proposés : `session` possède les politiques et SQLite ; `origin` possède lecture sûre et HTTP ; `renderer` possède agent, adaptation MPD et bail ; `desktop` possède navigation et présentation. Une requête traverse au plus Session puis l'adaptateur concerné. Le prototype ne construit que `probe`, séparé du produit.
