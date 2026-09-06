# Sources techniques P3

Ce registre documente les composants candidats, leurs limites et les fournisseurs. Il ne modifie pas les identifiants SRC de [P2](sources.md). Les liens TECH servent à [l'architecture](architecture.md) et à la [faisabilité](faisabilite.md).

Consultation du corpus : 2026-09-06. Les sources sont primaires. Les pages `stable`, `latest`, `master`, `main` et les dépôts sans révision figée sont mobiles. Aucune version installée ni compilation n'a été examinée. Les résumés décrivent des faits documentaires, sans garantie d'adéquation à kuro. Les recommandations de P3 sont des inférences de conception distinctes.

L'auteur a ouvert les sources de stockage, de packaging et les principaux composants. Les deux chercheurs indépendants en lecture seule ont consulté les sources audio et fournisseurs. Les limites d'accès de la seconde consultation sont indiquées. Aucun compte ni accès commercial n'a été obtenu.

## TECH-001

[SQLite WAL](https://www.sqlite.org/wal.html)

Auteur, accessible. WAL ne fonctionne pas sur système de fichiers réseau. Un seul écrivain à la fois. Checkpoints et niveau de synchronisation influencent durabilité et coût. La page ne prouve pas une politique de sauvegarde kuro.

## TECH-002

[SQLite FTS5](https://www.sqlite.org/fts5.html)

Auteur, accessible. Recherche plein texte, tokenisation et options de traitement des diacritiques. La pertinence, les tris et les temps sur le corpus kuro restent à tester.

## TECH-003

[SQLite Backup API](https://www.sqlite.org/backup.html)

Auteur, accessible. Copie d'une base active via l'API de sauvegarde. Cette capacité ne remplace pas la vérification du manifeste, des versions et de la restauration applicative.

## TECH-004

[SQLite Copyright](https://www.sqlite.org/copyright.html) et [Transactions](https://www.sqlite.org/lang_transaction.html).

Auteur, accessibles. Code placé dans le domaine public et transactions de lecture ou écriture. Les connecteurs et outils distribués doivent être examinés séparément.

## TECH-005

[inotify, manuel Linux](https://man7.org/linux/man-pages/man7/inotify.7.html)

Auteur, accessible. Débordement de file, courses et limites des événements sur fichiers réseau. Source du besoin de réconciliation proposé, sans inspection du NAS utilisateur.

## TECH-006

[CIFS usage, documentation du noyau Linux](https://docs.kernel.org/admin-guide/cifs/usage.html)

Auteur et chercheur données, accessible. Montage SMB et options d'accès. Aucun protocole, montage ou paramètre de la machine utilisateur n'est confirmé par cette page.

## TECH-007

[Flatpak sandbox permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html)

Auteur, accessible. Permissions fichiers, réseau et IPC, avec recours aux portails. Compatibilité avec un service audio autonome à tester, aucune permission appliquée.

## TECH-101

[MPD user manual](https://mpd.readthedocs.io/en/stable/user.html) et [MPD COPYING](https://github.com/MusicPlayerDaemon/MPD/blob/master/COPYING).

Auteur et chercheur audio, accessible. Base de fichiers et tags, file, partitions, sorties et plugins. Texte GPLv2 dans le dépôt. Le relevé du chercheur indique GPLv2 ou ultérieure; vérifier les en-têtes de la version distribuée. L'index MPD n'établit pas un modèle équivalent aux éditions, œuvres et crédits proposés pour kuro.

## TECH-102

[mpv manual](https://mpv.io/manual/stable/)

Auteur et chercheur audio, accessible. Commandes, propriétés, libmpv et politiques `gapless-audio`. Maintenir le format de sortie peut entraîner une conversion. Rouvrir la sortie peut interrompre le flux. Aucune transition sur le matériel utilisateur n'a été mesurée.

## TECH-103

[GStreamer playbin](https://gstreamer.freedesktop.org/documentation/playback/playbin.html) et [Licensing advisory](https://gstreamer.freedesktop.org/documentation/application-development/appendix/licensing.html).

Auteur et chercheur audio, accessibles. Préparation de la prochaine URI via `about-to-finish`. Bibliothèques LGPL, plugins et dépendances à examiner. Une fonction de préparation n'est pas une garantie gapless universelle.

## TECH-104

[mpv Copyright](https://github.com/mpv-player/mpv/blob/master/Copyright)

Auteur et chercheur audio, accessible. GPLv2 ou ultérieure par défaut. Mode sans fichiers GPL exclusifs visant LGPLv2.1 ou ultérieure, avec réserves sur les fichiers et la construction. Le seul paramètre de compilation ne constitue pas une concession automatique de licence.

## TECH-105

[Navidrome jukebox](https://www.navidrome.org/docs/usage/features/jukebox/) et [dépôt Navidrome](https://github.com/navidrome/navidrome).

Auteur et chercheur audio, accessibles. Bibliothèque musicale, clients et playlists. Jukebox serveur utilisant mpv IPC, commande par clients compatibles distincte de la Web UI native. Licence GPLv3 du dépôt consulté. Compatibilité future avec les contrats kuro non démontrée.

## TECH-106

[PipeWire audio](https://docs.pipewire.org/page_audio.html)

Auteur et chercheur audio, accessible. Graphe audio, formats, conversion et gestion du volume. La documentation décrit les mécanismes, pas le DAC ni les paramètres de la machine utilisateur.

## TECH-107

[FFmpeg legal](https://ffmpeg.org/legal.html)

Auteur et chercheur audio, accessible. LGPLv2.1 ou ultérieure pour la base, composants GPL et dépendances pouvant affecter la redistribution. Les codecs et licences du binaire effectif dépendent de la construction.

## TECH-108

[Tauri](https://v2.tauri.app/) et [dépôt Tauri](https://github.com/tauri-apps/tauri).

Auteur, accessibles. Interface web dans une application, WebView système, projet MIT ou Apache-2.0. Aucun avantage chiffré de mémoire n'est repris comme benchmark kuro.

## TECH-109

[Qt licensing](https://doc.qt.io/qt-6/licensing.html)

Auteur et chercheur audio, accessible. Licences commerciales et open source selon les modules. Les obligations du paquet et de la liaison restent à examiner avant adoption.

## TECH-110

[Electron security](https://www.electronjs.org/docs/latest/tutorial/security) et [dépôt Electron](https://github.com/electron/electron).

Auteur, accessibles. Isolation, sandbox et précautions de contenu web. Licence MIT du projet, composants tiers séparés. La consommation du futur desktop reste à mesurer.

## TECH-111

[Snapcast](https://github.com/snapcast/snapcast)

Auteur, accessible après redirection de l'ancien dépôt `badaix/snapcast`. Transport audio multiroom serveur et clients, sources PCM, horodatage et correction de dérive. Dépôt sous GPLv3. Les chiffres de synchronisation annoncés ne sont pas des mesures kuro. La correction temporelle interdit de déduire une transmission bit-perfect universelle.

## TECH-201

[MusicBrainz data license](https://musicbrainz.org/doc/About/Data_License) et [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API).

Chercheur données, accessibles. Seconde ouverture auteur de la licence refusée par HTTP 429. API accessible à l'auteur. Données centrales CC0, données supplémentaires CC BY-NC-SA 3.0 selon le relevé du chercheur. L'API impose une requête par seconde et un User-Agent. Usage commercial soumis à des conditions distinctes. Relire les licences par catégorie avant adoption.

## TECH-202

[Cover Art Archive](https://coverartarchive.org/)

Chercheur données, accessible. Images associées aux éditions musicales. Copyrights tiers conservés. L'accès à l'API ne fournit pas une licence générale de redistribution des pochettes.

## TECH-203

[Discogs API Terms of Use](https://support.discogs.com/hc/en-us/articles/360009334593-API-Terms-of-Use)

Auteur et chercheur données, accessible. Distinction données CC0 et données restreintes, notamment images, utilisateurs et marketplace. Restrictions de transfert, d'usage commercial des données restreintes, d'attribution et de fraîcheur. Quota numérique officiel non confirmé dans cette recherche.

## TECH-204

[ListenBrainz API](https://listenbrainz.readthedocs.io/en/latest/users/api/index.html) et [Core API](https://listenbrainz.readthedocs.io/en/latest/users/api/core.html).

Chercheur données, accessibles. Dépôt et récupération d'écoutes, recommandations. Consentement et correspondance avec les identités locales restent des responsabilités kuro proposées.

## TECH-205

[OPRA](https://github.com/opra-project/OPRA) et [OPRA license](https://github.com/opra-project/OPRA/blob/main/LICENSE.md).

Chercheur données, accessibles. Code MIT et données CC BY-SA 4.0. Attribution au créateur et au projet à conserver. Les données provenant d'autres projets gardent leur provenance.

## TECH-206

[TIDAL developer terms](https://developer.tidal.com/documentation/guidelines/guidelines-developer-terms), [developer guidelines](https://developer.tidal.com/documentation/guidelines/guidelines-developer-guidelines) et [design guidelines](https://developer.tidal.com/documentation/guidelines/guidelines-design-guidelines).

Chercheur données, texte consulté. Seconde ouverture auteur des terms accessible sans texte exploitable. Le relevé signale lecture intégrale via Embed pour abonnés, module officiel et restrictions de traitement ou fusion entre services. Accès et droits d'une architecture kuro non établis. Conditions à relire avec le fournisseur avant engagement.

## TECH-207

[libsmb2](https://github.com/sahlberg/libsmb2)

Chercheur données, accessible. Bibliothèque SMB avec API asynchrone, licence LGPLv2.1. Candidat si un accès SMB natif est retenu. Aucune preuve sur les interruptions, seeks et identifiants du NAS utilisateur.

## TECH-208

[MIT](https://opensource.org/license/mit), [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0), [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) et [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html).

Chercheur données, textes de référence pour la comparaison des licences. Auteur : MIT et Apache accessibles, ouvertures GNU en erreur interne. MIT et Apache sont permissives. Apache précise notamment brevets et notices. GPL et AGPL proposent un copyleft, avec clause réseau propre à l'AGPL. Aucun texte choisi pour kuro.

## TECH-209

[Qobuz API Terms of Use](https://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf)

Auteur et chercheur données, PDF accessible. Clés fournies par Qobuz et secret non partageable. Ce document ne prouve pas l'admission actuelle de kuro ni une permission de distribution du secret dans un client open source.

## TECH-210

[KKBOX OpenAPI Python SDK](https://kkbox.github.io/OpenAPI-Python/kkbox_developer_sdk.html)

Chercheur données, accessible. API de catalogue avec credentials. Onboarding actuel, droits de lecture native et intégration kuro non démontrés.

## TECH-211

[nugs, utilisation dans Roon](https://help.nugs.net/support/solutions/articles/6000281896-how-do-i-use-nugs-on-roon-)

Chercheur données, accessible. Partenariat Roon documenté. Aucune API publique réutilisable par kuro n'est établie.

## TECH-212

[LyricFind lyric display](https://www.lyricfind.com/products/lyric-display) et [TiVo music metadata](https://business.tivo.com/products-solutions/metadata/music-metadata).

Chercheur données, accessibles. Offres commerciales de contenus. Conditions, budget et accès kuro à obtenir. L'offre produit ne fournit pas de licence de réutilisation.
