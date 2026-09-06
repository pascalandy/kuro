# Cadrage courant de kuro

Ce document fixe le cadrage retenu après deux entretiens indépendants, puis amendé par la [priorité sonore demandée directement par l'utilisateur](kickoff/scope-addendum.md). Les tickets [Définir les usages et les limites avec le premier entretien](../.scratch/cadrage-kuro/issues/01-definir-usages-et-limites.md), [Réviser le cadrage avec un second entretien indépendant](../.scratch/cadrage-kuro/issues/03-reviser-cadrage-second-entretien.md), [Donner la priorité à la qualité sonore](../.scratch/cadrage-kuro/issues/05-priorite-qualite-sonore.md) et [Clarifier les rôles Kuro](../.scratch/cadrage-kuro/issues/06-clarifier-les-roles.md) contiennent les décisions détaillées. Les identifiants `KD-*` ci-dessous en indiquent la source.

Le cadrage décrit un produit à construire. Il ne prouve aucun comportement, ne choisit aucune technique et ne crée aucun objectif de parité avec Roon. KD-025, KD-032, KD-038.

## Destination et acceptation de U-M1

kuro permet à une personne d'écouter et de retrouver sa propre musique depuis un desktop Linux Omarchy. KuroKor possède l'état durable de Kuro et coordonne la lecture. Les Kuro Clients servent seulement au contrôle et à l'affichage. Le NAS conserve les fichiers musicaux maîtres. L'état durable du catalogue, des playlists et de la file appartient à KuroKor. Cette fonction ne détermine pas l'emplacement physique de l'état de Kuro. KD-041, KD-044.

Les rôles logiques ne fixent pas le nombre de machines. La première cible place KuroKor dans le salon avec la chaîne audio locale `KuroKor -> USB -> DDC -> I2S sur HDMI -> DAC Terminator`. Un Kuro Client peut fonctionner sur cette machine ou à distance. Le [scénario séparé](scenarios-deploiement.md#scénario-1-kurokor-et-kuro-client-sur-deux-ordinateurs) place KuroKor et le Kuro Client sur deux ordinateurs, mais ne fixe pas encore le point de lecture. Linux reste l'hypothèse initiale pour la machine du salon. KD-044.

U-M1 conserve environ 20 000 albums et 3 To, les vues et la recherche, les playlists et la file, le gapless retenu, la persistance, une sauvegarde restaurable, les sources intactes et l'usage sans Internet. Les pochettes détenues par l'application font partie des données durables. KD-001, KD-002, KD-005, KD-009, KD-024, KD-043.

U-M1.A, U-M1.B et U-M1.C produisent des résultats utilisables dans cet ordre. Ces passages ne valent pas acceptation partielle. L'utilisateur accepte U-M1 lorsque les dix critères historiques MVP-01 à MVP-10 et les contrats courants sont prouvés ensemble sur la cible connue. KD-026, KD-038.

## Import et catalogue

Le scan peut être annulé et repris. Les éléments déjà catalogués restent consultables et jouables. Un fichier invalide ne bloque pas les autres. Une demande reçue pendant un scan est regroupée ou différée. Une source NAS absente et un scan réussi ne suppriment aucune référence durable. KD-010, KD-016, KD-036.

Une référence de catalogue survit à une relocalisation explicite de racine lorsque le chemin relatif reste identique. Elle survit aussi à une modification de tags au même chemin. Un renommage interne peut produire une ancienne référence indisponible et un nouveau fichier. kuro ne rapproche jamais silencieusement des fichiers selon leur nom, leurs tags ou une empreinte supposée. KD-013, KD-028, KD-036.

Le retrait explicite d'une source masque ses médias dans les vues courantes. Les playlists et la file conservent leurs références, désormais indisponibles. Ajouter le même chemin ne réactive pas silencieusement la source retirée. Une purge demande une décision distincte. KD-021, KD-029.

## Métadonnées, vues et recherche

L'artiste d'album vient de `albumartist`, puis de `artist`, puis d'une valeur inconnue explicite. La recherche couvre les titres d'album, les titres de piste, l'artiste d'album et l'artiste de piste, sans distinction de casse ou d'accents. Sans titre, la piste utilise son nom de fichier et l'album son dossier avec un repli identifiable. KD-017, KD-027, KD-033.

Les listes suivent un ordre alphabétique stable. Les pistes d'un album suivent les numéros de disque et de piste, avec un repli déterministe déclaré. Le résultat de recherche montre l'album et la source nécessaires pour distinguer les homonymes. Les disques d'un album se regroupent seulement lorsque les informations et le contexte d'une même source concordent. Les copies et les éditions restent distinctes. Les ambiguïtés restent visibles et lisibles. KD-027, KD-033.

Le retour depuis un album conserve la place dans la liste ou la recherche précédente. La piste courante et ses commandes restent visibles sans imposer une vue plein écran. KD-040.

## Playlists, file et lecture

U-M1 permet de créer, nommer, renommer et supprimer une playlist, puis d'ajouter, retirer et réordonner ses pistes. Une playlist et la file acceptent les doublons. La lecture d'un album ou d'une piste remplace la file et démarre sa première piste. **Jouer ensuite** insère après la piste courante, ou en tête s'il n'y en a pas, sans démarrer. **Ajouter** place la sélection en fin sans démarrer. KD-018, KD-034.

Retirer la piste courante arrête la lecture et garde le reste de la file. Vider la file arrête aussi la lecture. Réordonner la file conserve la piste en cours. **Précédent** et **Suivant** parcourent la file. Depuis la première piste, **Précédent** revient au début de celle-ci. KD-034.

Une traversée passe une piste indisponible au plus une fois et affiche l'erreur. La fin de la file arrête la lecture. Le retour du NAS ne relance rien. La perte de la coordination de lecture ou de la sortie audio arrête la lecture sans choisir une autre sortie. Leur retour ne relance rien. KD-010, KD-011, KD-018, KD-039, KD-043.

## Audio et transport à étudier

Le corpus candidat comprend FLAC, MP3, AAC, ALAC, WAV, AIFF, Vorbis et Opus en PCM stéréo. Une étude fixe le sous-ensemble garanti et mesure le gapless sur ses enchaînements homogènes. Elle doit aussi rendre visibles les conversions, le rééchantillonnage, le gain et les limites de format connus. DSD, DSF, DFF, multicanal et traitement du signal restent hors U-M1 tant qu'une décision explicite ne les réadmet pas. KD-014, KD-039, KD-041, KD-043.

L'étude compare les transports licites et réalisables selon chaque [scénario de déploiement](scenarios-deploiement.md). Elle distingue le transport réseau, les tampons possédés par Kuro, la sortie USB, le DDC et le DAC. Elle doit fixer la limite entre le moteur audio et KuroKor lorsque le point de lecture est distant. L'équivalence des octets ou des échantillons ne prouve ni le jitter physique au DAC, ni une supériorité sonore. Le volume et les éventuels modes exclusifs dépendent de cette étude. kuro ne réimpose aucun ancien volume au démarrage et ne l'augmente jamais automatiquement. KD-020, KD-039, KD-041, KD-044.

## Persistance, sauvegarde et cycle de vie

Fermer la fenêtre laisse le service de la session actif. **Quitter** arrête kuro. Après un redémarrage, kuro restaure la file et le meilleur point enregistré de la piste, puis reste arrêté. **Lecture** reprend cette piste. Le choix d'une autre piste commence la nouvelle piste. KD-003, KD-004, KD-012.

Le snapshot de sauvegarde contient les sources configurées, les références de catalogue, les métadonnées connues, les playlists, la file, la position, les préférences et les pochettes détenues par l'application. Il exclut les médias, les images de source, les index, les caches reconstructibles et les secrets. KD-006, KD-030.

La restauration vérifie la compatibilité, montre les sources manquantes et demande confirmation avant de remplacer la bibliothèque. Elle ne fusionne pas deux bibliothèques et repart sans son. Une sauvegarde invalide ou une interruption laisse l'état précédent récupérable. U-M1 garantit son propre format livré. KD-030, KD-035.

L'installation et la désinstallation utilisent des versions figées et sont reproductibles dans un environnement propre. Une désinstallation normale conserve les données. Le service appartient à la session utilisateur. KD-023.

## Accès, diagnostic et fonctionnement hors Internet

Après l'installation, toutes les fonctions de U-M1 démarrent et fonctionnent sans Internet pendant une durée indéfinie. Aucun compte ou contrôle cloud n'est requis. L'accès au NAS dépend seulement du réseau local. KD-009, KD-024.

Le chemin cible autorise seulement les échanges réseau nécessaires entre KuroKor, les Kuro Clients autorisés et un éventuel point de lecture distinct. L'étude doit séparer l'accès aux médias, le contrôle de la session, la découverte et l'état du point de lecture. Cette ouverture limitée n'autorise ni plusieurs zones, ni un accès distant. Un futur point de lecture UPnP reste distinct du Kuro Client et ne crée pas automatiquement un produit multiroom en U-M1. Les journaux retirent les données sensibles et présentent un aperçu avant export. Le clavier, un focus visible, les libellés accessibles, le zoom et le déplacement dans la piste font partie de U-M1. KD-019, KD-022, KD-043, KD-044.

## Mesures et décisions techniques

La recherche visible sous 300 ms au 95e percentile et la première page sous une seconde restent des objectifs de conception. La mémoire et la durée d'import doivent être mesurées sur le matériel et le corpus cibles. Ces nombres ne sont pas des résultats actuels. KD-015, KD-027.

Le transport et la chaîne audio doivent être étudiés avant la stack. Puisque Kuro doit posséder ses tampons PCM et sa sortie audio, l'étude du futur cœur évalue Rust en priorité. Le laboratoire Go reste une preuve valide. Cette priorité ne choisit pas encore le langage de production et ne demande aucun portage immédiat. La licence, le corpus de formats garanti, le matériel, l'accès NAS et le paquet demandent aussi les études du [backlog](backlog.md). Une étude négative entraîne un arbitrage explicite. Elle ne réduit pas seule le volume cible, le gapless retenu ou la restauration. KD-025, KD-038, KD-041, KD-045.
