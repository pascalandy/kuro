# Contrats dérivés des appels

## Types et signatures de conception

Esquisse Rust, pas un fichier compilable. Tous les identifiants ont des champs privés; seuls leurs propriétaires construisent une valeur validée. Les données reçues du réseau sont analysées à la frontière. Les durées et formats ci-dessous sont des types métier, jamais des objets HTTP ou MPD.

```rust
struct CatalogRef { source: SourceId, relative: RelativeMediaPath }
struct ObjectId { sha256: [u8; 32], bytes: u64 } // Aucun rôle d'identité catalogue.
struct Occurrence { id: OccurrenceId, media: CatalogRef }
struct Revision { library: LibraryEpoch, session: SessionId, sequence: u64 }
struct Prepared { ticket: TicketId, revision: Revision } // Opaque, révocable, expire.
struct ResumePoint { occurrence: OccurrenceId, offset: MediaTime }
enum Selection { Replace(Vec<CatalogRef>), Resume(Revision) }
enum QueueChange { InsertNext(Vec<CatalogRef>), Append(Vec<CatalogRef>),
    Remove(OccurrenceId), Reorder(Vec<OccurrenceId>), Clear }
enum Control { Stop, Pause, Seek(MediaTime), Previous, Next }
enum Readiness { Missing, Fetching { received: u64, total: u64 }, Verified(ObjectId) }
enum Phase { Stopped, Playing, Paused, Fault(PlaybackError) }
struct PreparationView { requested: Selection, readiness: Vec<Readiness> }
enum Evidence<T> { Observed(T), Configured(T), Unknown }
struct SignalPath { source: Evidence<AudioFormat>, decoded: Evidence<AudioFormat>,
    output: Evidence<AudioFormat>, transforms: Evidence<Vec<Transform>>,
    usb_clock_mode: Evidence<UsbClockMode> }
struct SessionView { revision: Revision, queue: Vec<Occurrence>,
    resume_point: Option<ResumePoint>, phase: Phase, readiness: Vec<Readiness>,
    preparing: Option<PreparationView>,
    path: SignalPath, errors: Vec<PlaybackError> }
enum PlaybackError { StaleRevision, ExpiredPreparation, SourceUnavailable,
    ObjectChanged, IntegrityFailure, CapacityExceeded, ControlLost,
    OutputLost, UnsupportedFormat, EngineFailure, SnapshotUnavailable }
impl Playback {
    async fn select(&self, renderer: ConfiguredRenderer) -> Result<Salon> { unimplemented!() }
}
impl Salon {
    async fn prepare(&self, selection: Selection, op: OperationId) -> Result<Prepared> { unimplemented!() }
    async fn start(&self, ready: Prepared, op: OperationId) -> Result<SessionView> { unimplemented!() }
    async fn state(&self) -> Result<SessionView> { unimplemented!() }
    async fn change(&self, at: Revision, change: QueueChange, op: OperationId) -> Result<SessionView> { unimplemented!() }
    async fn control(&self, at: Revision, command: Control, op: OperationId) -> Result<SessionView> { unimplemented!() }
}
// Privé au serveur: sources en lecture seule, objets immuables et accès limité.
impl MediaStore {
    async fn materialize(&self, media: CatalogRef) -> Result<ImmutableObject> { unimplemented!() }
}
// Privé au renderer: vérification et réservation ne peuvent être séparées par le client.
impl LocalMedia {
    async fn reserve(&self, window: StagingWindow) -> Result<PinnedFiles> { unimplemented!() }
}
impl Engine {
    async fn reconcile(&mut self, desired: ExecutionWindow) -> Result<EngineObservation> { unimplemented!() }
}
```

`prepare` garde la file jouée intacte pendant la préparation d'une sélection de remplacement. `start` valide le ticket et commet la nouvelle file avant de demander son démarrage. L'interface montre la sélection en préparation séparément de la file jouée. Pour Resume, la révision demandée doit être courante; le ticket fixe ensuite l'occurrence et son point enregistré. Une file vide n'a aucun `ResumePoint` et ne produit pas de ticket Resume.

## Propriété et stockage

| Module et machine | État durable | État temporaire et règle |
| --- | --- | --- |
| `media`, serveur Kuro | Références, source configurée, playlists, bibliothèque et epoch | Spool immuable borné par octets; liens catalogue/version; lecteurs NAS bornés. Aucune écriture source. |
| `session`, agent du salon | Journal local file/position/révision; résultats des opérations acquittées; renderer sélectionné | Préparations expirables, téléchargements `.part`, index d'éviction et fichiers vérifiés reconstruisibles; un acteur écrit la session. |
| `engine`, salon | Configuration de sortie identifiée, jamais restauration de volume | MPD, projection courte des occurrences, identifiants MPD, décodeur et tampons PCM; un seul client de commande, socket Unix privée. |
| Desktop, serveur | Préférences de vue | Vue de la révision renderer; fermer la fenêtre ne touche pas au service. |
| USB/DDC/DAC | Réglages physiques externes | FIFOs, réhorlogage et horloge de conversion exacts inconnus avant identification. |

À chaque démarrage d'agent, arrêter et vider MPD avant de reconstruire une projection arrêtée. Un superviseur arrête MPD si l'agent meurt; MPD ne doit pas survivre en continuant sa file. Un état moteur absent ou ambigu devient un arrêt visible. Les commandes MPD partiellement appliquées ne sont jamais supposées annulées. Le renderer garde l'opération durable et sa phase, puis reconstruit arrêté après panne. Rejouer le même `OperationId` renvoie le résultat enregistré sans deuxième lancement. Une nouvelle session ou un redémarrage invalide tous les tickets de démarrage antérieurs.

## Préparation, mutations et pannes

Chaque fichier doit être complet avant d'entrer dans MPD. Une fenêtre réserve la piste courante et la suivante; la dernière piste exige seulement elle-même. Le renderer vérifie longueur et SHA-256, synchronise le fichier, puis publie par renommage atomique sur le même filesystem. Un fichier partiel n'a jamais un nom jouable. Le serveur publie ses propres objets seulement après copie complète et vérification de stabilité de la source; si cette stabilité ne peut être établie, il refuse la préparation. Une empreinte porte sur les octets capturés, pas une garantie de snapshot du NAS sans support de celui-ci.

Le budget compte fichiers réservés, fichiers prêts et partiels. Éviction des objets non réservés seulement. Un couple de pistes trop grand produit `CapacityExceeded`; aucun passage silencieux à un flux progressif. Les pistes suivantes sont préparées en ordre avec une concurrence bornée. Un album entièrement en cache ne génère aucun nouveau transfert audio. Les grandes playlists restent des références, sans réserver leur totalité.

Une insertion ou un déplacement change la révision et recalcule la fenêtre suivante. Retirer l'occurrence courante ou vider arrête le moteur. Réordonner conserve cette occurrence. La transition ne peut viser qu'un fichier vérifié. Si le nouveau suivant manque à l'échéance, arrêt avec piste en attente; fin de téléchargement ou retour du NAS ne relance rien. Une référence indisponible est sautée au plus une fois par traversée avec erreur. Previous/Next prépare sa nouvelle cible si nécessaire; Seek reste local au fichier et n'est pas promis à l'échantillon près.

La session reste sous contrôle du service autorisé. Le renderer ouvre vers le serveur configuré un canal TLS à identités épinglées, distinct des capacités de lecture média. Seul le serveur relaie les commandes reçues sur son IPC local autorisé; le serveur ne publie aucune commande utilisateur au LAN. Un heartbeat maintient cette autorisation. Prototype: chaque seconde, arrêt après trois secondes sans message valide; ce délai est un budget d'essai à mesurer. Perte du contrôle ou de l'USB arrête, sans sortie de secours ni reprise au retour. Une panne du seul service média peut laisser jouer les fichiers préparés tant que le contrôle demeure vivant. Cette règle n'autorise pas une écoute autonome après déconnexion réseau complète. Quitter demande Stop puis termine le serveur; si le contrôle échoue, le watchdog renderer borne l'arrêt.

Une playlist éditée au serveur ne réécrit pas la file issue d'un instantané précédent. Chaque nouveau Play résout une version source actuelle. Une source explicitement retirée invalide ses autorisations de lecture et ses préparations, sans effacer les références; le cache ne la réactive pas. Les occurrences déjà jouées gardent leur version jusqu'à arrêt, sauf retrait explicite qui arrête aussi l'occurrence courante.

Le snapshot complet requiert un export cohérent du renderer sous une barrière de mutations bibliothèque/file. Il contient sa file et sa position, jamais les fichiers cache. Renderer inaccessible signifie `SnapshotUnavailable`, pas sauvegarde complète annoncée depuis une vue périmée. Restaurer prépare une génération bibliothèque et une session arrêtée avant activation; un journal d'activation permet de revenir à l'ancienne génération en cas d'interruption. Les deux copies restent récupérables jusqu'à l'acquittement. Un epoch distinct empêche l'ancienne session d'émettre du son avec la bibliothèque restaurée. Ce protocole distribué doit passer KV-011 avant adoption, et reste un coût majeur de C.

## Frontières audio et commande

```text
NAS --lecture fichiers--> media Kuro [spool fichier immuable]
  --HTTP octets originaux, débit libre et reprise--> salon [cache .part -> vérifié]
  --lecture locale--> MPD [décodage local -> tampon PCM]
  --ALSA périphérique identifié [tampon noyau]--> hôte USB -> DDC [FIFO/mode inconnus]
  --I2S sur câble HDMI [données/BCLK/LRCLK, rôle réel à confirmer]--> Terminator
  --[FIFO/réhorlogage/horloge conversion inconnus]--> analogique
Desktop --IPC session locale--> service Kuro --canal autorisé--> agent salon
  --socket Unix privée, commandes/état--> MPD
```

Le serveur choisit la représentation fichier originale et ne décode ni n'applique de gain. MPD choisit le PCM décodé et négocie la sortie; le pilote et le périphérique règlent sa consommation. Débit réseau et temps monotone du simulateur ne sont pas l'horloge de conversion. Un USB asynchrone suit une horloge libre ou externe, mais le mode du DDC reste inconnu. I2S transporte ses horloges avec les données; son connecteur HDMI ne détermine ni pinout ni reclocking. [USB Audio 2.0](https://usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf), [NXP I2S](https://www.nxp.com/docs/en/user-manual/UM11732.pdf).

| Capacité | Statut et décision minimale |
| --- | --- |
| Sélection et accès | Conception Kuro non observée. Un renderer configuré, identité épinglée, contrôle local relayé par canal autorisé; aucun moteur MPD exposé au LAN. |
| Lecture à la demande, reprise HTTP | HTTP documenté; implémentation Kuro à prouver. Identifiants objets autorisés, jamais chemins fournis par le client; une capacité média ne confère aucun droit de commande. |
| Play/Stop/Pause/Seek, file, état/erreur | Protocole MPD documenté, adaptation Kuro non observée. Les délais et Seek dépendent aussi du codec. |
| Formats, fréquences, transitions | MPD documente décodeurs et réglages; build réel, DDC et gapless inconnu. Prober un corpus homogène avant garantie. |
| Gain et traitements | Configurer sans ReplayGain, normalisation, crossfade ou mixer logiciel; ne jamais restaurer/augmenter le volume. Gain aval inconnu et aucun contrôle volume Kuro au premier essai. |
| Sortie réelle | ALSA `hw` envisagé après inventaire; MPD peut convertir quand un format natif échoue. Consigner logs et `hw_params`; conversion imprévue échoue au test, sans prétendre qu'un observateur peut l'empêcher avant le premier échantillon. |

La configuration et les observations ont des statuts différents dans `SignalPath`. L'interface montre « inconnu » après une frontière non instrumentée. Le [manuel MPD](https://mpd.readthedocs.io/en/stable/user.html#bit-perfect-playback) documente ses conversions possibles; il ne mesure pas le DAC. La release 0.24.15 est confirmée dans les [téléchargements officiels](https://www.musicpd.org/download/mpd/0.24/); figer l'archive, sa signature et le build réellement essayé.
