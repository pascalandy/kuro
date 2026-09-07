# Contrats et frontières

## Chemin et propriétaires

```text
Fenêtre -- gestes locaux --> serveur Kuro, unique auteur durable SQLite
NAS monté -- fichiers RO --> catalogue/résolution --> FFmpeg serveur
                                             décode en PCM déclaré, aucun gain
                                         [tampon producteur borné]
                                      -- blocs TCP --> renderer salon
                                      <-- crédits -- [tampon PCM vérifié]
serveur -- prepare/start/stop/seek --> agent renderer -- appsrc --> alsasink
serveur <-- état / erreur / position --                  [tampon ALSA/USB]
                                                        USB --> DDC --> I2S --> DAC
```

Serveur : stockage durable des sources, références, métadonnées connues, playlists, occurrences de file, sélection et meilleure position rapportée. Index de recherche reconstructible. Processus de session indépendant de la fenêtre, arrêté par Quitter.
Renderer : configuration et identité de pair durables hors snapshot de bibliothèque ; pipeline, crédits, génération et PCM temporaires. Aucun NAS ni catalogue local. Boot et nouvelle connexion restent silencieux.
FFmpeg : worker serveur isolé, fichier ouvert en lecture seule, sortie PCM temporaire. Le profil initial WAV/FLAC entier stéréo 48 kHz/16 bits ne force ni `-ar` ni gain. Élargir les codecs exige une preuve de délai/padding et format de décodage.
GStreamer : propriétaire des files internes, de la consommation et du périphérique exact. `appsrc` reçoit PTS calculés à partir du compte d'échantillons, jamais des arrivées réseau. Bornes de chaque tampon et crédits comptabilisent séparément mémoire agent, appsrc et ALSA.
Horloges : NAS/réseau règlent disponibilité ; le puits règle la cadence logicielle de lecture. Le rôle exact USB/DDC puis les clocks I2S et conversion DAC restent inconnus. [USB Audio définit plusieurs modes](https://usb.org/sites/default/files/Audio2_with_Errata_and_ECN_through_Apr_2_2025.pdf) ; aucun mode de l'appareil n'est déduit de sa marque. Le câble HDMI transporte ici I2S, pas HDMI audio vidéo.

## Esquisse métier, corps non implémentés

```rust
// Pseudocode Rust. Identifiants opaques, constructeurs privés ; aucun type réseau public.
struct SourceId(Uuid); struct CatalogRef(Uuid); struct OccurrenceId(Uuid);
struct DeviceId(Uuid); struct SessionId(Uuid); struct Generation(u64);
struct Source { id: SourceId, root: AbsolutePath, state: SourceState }
enum SourceState { Active, Missing, Removed }
struct Reference { id: CatalogRef, source: SourceId, relative: RelativePath }
struct Entry { id: OccurrenceId, media: CatalogRef }
struct Queue { order: Vec<OccurrenceId>, entries: Map<OccurrenceId, Entry> }
struct Cursor { occurrence: OccurrenceId, position: TrackPosition }
struct Resume { queue: Queue, cursor: Option<Cursor> }
enum Phase { Stopped(Resume), Preparing(Preparation), Ready(Prepared),
             Playing(Active), Paused(Active), Failed(Resume, PlaybackError) }
struct Active { session: SessionId, generation: Generation, cursor: Cursor }
struct Prepared { ticket: PreparationTicket, path: SignalPath }
enum Knowledge<T> { Reported(T), Observed(T), Unknown }
struct PcmFormat { rate: Hertz, encoding: SignedLittleEndian, valid_bits: BitDepth,
                   storage_bits: BitDepth, layout: InterleavedStereoLeftRight }
struct SignalPath { decoded: Knowledge<PcmFormat>, delivered: Knowledge<PcmFormat>,
                    device: Knowledge<PcmFormat>, treatments: Vec<TreatmentEvidence> }
enum PlaybackError { SourceMissing, DeviceLost, PeerLost, UnsupportedFormat,
                     Underrun, CorruptBlock, DecodeFailed, StalePreparation }
enum QueueEdit { InsertNext(Selection), Append(Selection), Remove(OccurrenceId),
                 Reorder(Vec<OccurrenceId>), Clear }
impl Kuro {
 fn select_device(&mut self, id: DeviceId) -> Result<Device> { unimplemented!() }
 fn prepare(&mut self, selection: Selection, device: Device) -> Result<Prepared> { unimplemented!() }
 fn start(&mut self, ticket: PreparationTicket) -> Result<Active> { unimplemented!() }
 fn edit_queue(&mut self, edit: QueueEdit) -> Result<QueueView> { unimplemented!() }
 fn seek(&mut self, session: SessionId, at: TrackPosition) -> Result<PlaybackView> { unimplemented!() }
 fn status(&self) -> Result<PlaybackView> { unimplemented!() }
 fn stop(&mut self) -> Result<PlaybackView> { unimplemented!() }
}
impl Catalog {
 fn configure(&mut self, change: SourceChange) -> Result<Source> { unimplemented!() }
 fn request_scan(&mut self, source: SourceId) -> ScanStatus { unimplemented!() }
 fn search(&self, query: SearchQuery) -> Page<AlbumOrTrack> { unimplemented!() }
}
```

Modules : `session` possède transitions et écritures durables ; `catalog` possède identité, sources, scan et recherche ; `pcm` possède décodage et formats ; `renderer` possède framing privé, réseau, crédits et pipeline. SQLite reste privé au serveur ; workers ne l'écrivent jamais. Le client voit les opérations métier, pas un repository ni les étapes d'une transaction.

## Identité et concurrence

Index unique `(source_id, relative_path)` pour retrouver les références ; racine relocalisable sans changement d'identité. Retrait conserve les références indisponibles ; ajouter le même chemin crée une autre SourceId. Absence ne vaut pas retrait. Tags et empreintes ne deviennent jamais des identités de contenu ; remplacement au même chemin reste KB-022. Le token taille/date détecte seulement une mutation possible pendant lecture.
Ordre de file et occurrences sont distincts : doublons valides, recherche de l'occurrence courante par identifiant. Reorder doit contenir exactement les identifiants présents ; courant inchangé. Retrait du courant et Clear arrêtent. Append/InsertNext n'autorisent aucun démarrage. Une traversée garde l'ensemble des occurrences déjà essayées et un horizon initial fini ; les ajouts pendant traversée ne créent pas une boucle infinie.
Un worker scan par source retourne des lots identifiés par génération ; un second request_scan active au plus un nouveau passage. Annulation conserve les lots déjà validés et un checkpoint ; fin interrompue ou source absente ne déclare pas les fichiers supprimés. Le propriétaire durable applique de petits commits, en donnant priorité aux commandes de session.
Sauvegarde cohérente des données durables et métadonnées connues ; caches, médias et secrets exclus. Restore valide dans une génération de stockage candidate, puis échange le pointeur actif atomiquement après confirmation ; l'ancienne génération reste récupérable. Cette opération invalide les sessions renderer et repart arrêtée.

## États et effets audio

Prepare vérifie capacités, ouvre la source, crée une génération et précharge sans son ; Ready porte un ticket lié à cette préparation. Start consomme ce ticket après commit du nouvel état durable. Réessayer la même requête ne crée pas deux lectures ; un identifiant de commande fournit la déduplication de session. Une préparation invalidée par modification de sélection refuse le démarrage.
Le serveur garde la file autoritaire. Le renderer ne reçoit que la fenêtre courant/suivant et ne persiste aucune queue. Chaque bloc, transition et rapport porte SessionId + Generation + OccurrenceId. Seek et changement du prochain titre invalident les blocs futurs, puis attendent l'accusé de purge avant la nouvelle génération. Aucun prochain titre ne devient courant sur un simple ACK de réception ; il faut le rapport de position de sortie, avec son incertitude.
Stop, perte USB, corruption et Underrun purgent le pipeline et rendent la session inexécutable. Perte du pair détectée par EOF ou délai de contrôle borné : même effet. Retour réseau/device ne démarre rien. Après crash serveur, le renderer cesse à expiration de bail ; après redémarrage serveur, la meilleure position rapportée revient dans Stopped. Le délai de détection est visible, pas présenté comme un arrêt instantané d'un réseau partitionné.

## Transport borné et rythme

Laboratoire seulement : contrôle TCP séparé de PCM TCP pour qu'un tampon média plein ne bloque pas Stop. Listener limité à loopback ; aucun port LAN pendant cette preuve. Étape deux machines : pair explicitement configuré, authentification mutuelle et accès limité au renderer ; contrôle utilisateur uniquement par socket local protégé. Ni découverte générale ni API LAN utilisateur.
Framing privé version 1 : génération, occurrence, offset de trame, nombre de trames, longueur bornée et SHA-256 du bloc. L'en-tête de segment fixe fréquence, signedness, ordre L/R, interleaving, profondeur valide et conteneur. Un bloc est accepté seulement s'il respecte format, crédits, hash et offset attendu. Une empreinte vérifie l'intégrité, pas l'autorisation du pair.
Le receiver annonce une fenêtre absolue de trames autorisées. Le serveur pousse dès qu'il a des crédits ; les crédits répétés n'augmentent pas la fenêtre. Le producteur s'arrête en amont lorsque les tampons bornés se remplissent. Les socket buffers sont mesurés séparément. Aucun `sleep(1/rate)` serveur ne cadence le son.
La dérive entre ordinateurs modifie le débit de crédits ; le serveur décode plus vite que le temps réel puis attend. Le renderer ne supprime, répète ni rééchantillonne pour suivre le serveur. Le pipeline doit utiliser le clock du puits et désactiver son asservissement à une autre horloge ; GStreamer expose cette [politique d'asservissement](https://gstreamer.freedesktop.org/documentation/audio/gstaudiobasesink.html). Absence de traitement reste à capturer, pas seulement à configurer.
Gapless homogène : deux fichiers décodés avant la frontière, un format, PTS contigus et marqueur d'occurrence dans un flux continu, sans EOS ni réouverture ALSA entre pistes. Si format/fréquence change : drain de l'ancien segment, renégociation explicite, précharge puis continuation seulement si la session reste autorisée. La durée de transition et le relock matériel sont mesurés séparément ; aucune garantie gapless inter-fréquences.

## Capacités et limites du statut

| Capacité nécessaire | État de preuve | Décision |
| --- | --- | --- |
| Lecture à la demande, prepare/start/stop/seek | Proposée, non observée | Contrat v1 et tests de génération ; seek redécode puis purge |
| Configuration appareil | Proposée | Un pair configuré ; découverte non nécessaire |
| PCM/rates acceptés | Plugin GStreamer observé, DDC inconnu | 48/16 stéréo au labo ; négocier puis tester la sortie exacte |
| Tampon et backpressure moteur | API documentée, plugin installé | Crédits bornés en amont ; consommation matérielle à instrumenter |
| Gain/volume | Politique proposée ; contrôle aval inconnu | Aucun gain ajouté, aucune hausse/restauration de volume ; ne pas exposer un curseur sans contrôle validé |
| Gapless | Mécanisme proposé, aucun résultat matériel | Tester concaténation puis frontière ALSA et analogique |
| État et erreurs | Proposés, non observés | Rapport format livré, traitements connus, buffer, perte et position avec incertitude |
| USB/DDC/I2S/DAC | Inconnus pour ces appareils | Afficher inconnu au-delà des observations ; jamais un badge « transparent » global |
