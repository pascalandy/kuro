# Validation du cadrage courant

Ces scénarios définissent les preuves attendues pour U-M1. Aucun scénario n'a été exécuté, car le produit n'existe pas encore. Une future preuve consigne la version, l'environnement, le corpus, les étapes, le résultat brut et l'écart au résultat attendu. L'utilisateur accepte U-M1 seulement lorsque les dix critères MVP et tous les contrats applicables passent ensemble. KD-001, KD-026, KD-038.

## KV-001. Installer et arrêter le service de session

Sur un environnement Linux Omarchy propre, installer des versions figées, démarrer kuro, fermer la fenêtre puis la rouvrir. Le service reste actif après la fermeture de la fenêtre et **Quitter** l'arrête. La désinstallation normale conserve les données. Réinstaller puis relire les données conservées. Limite : ce scénario ne prouve ni la mise à jour automatique, ni un autre système d'exploitation. KD-003, KD-023.

## KV-002. Importer un corpus sans bloquer la lecture

Importer un dossier local qui contient des fichiers valides, un fichier invalide et des tags modifiés pendant un second scan. Annuler, reprendre et demander un autre scan pendant le premier. Les éléments déjà catalogués restent consultables et jouables, le fichier invalide produit une erreur bornée et la demande concurrente est regroupée ou différée. La modification de tags au même chemin conserve la référence. Limite : les délais et le mécanisme de détection dépendent des études KB-011 à KB-013 et KB-022. KD-016, KD-036.

## KV-003. Gérer un NAS absent, retiré et relocalisé

Cataloguer un montage NAS fourni, le rendre indisponible puis le reconnecter. L'absence ne supprime rien et le retour ne relance pas la lecture.

Dans un deuxième cas, retirer explicitement une source puis ajouter le même chemin. Le retrait masque les médias dans les vues, garde les références des playlists et de la file, et l'ajout ne réactive pas la source retirée.

Dans un troisième cas, garder une source configurée et relocaliser sa racine avec les mêmes chemins relatifs. La relocalisation explicite conserve les références non ambiguës. Limite : kuro ne gère ni le protocole, ni les identifiants, ni le montage. KD-005, KD-010, KD-013, KD-028, KD-029.

## KV-004. Afficher un catalogue aux métadonnées imparfaites

Utiliser des albums homonymes, plusieurs sources, un album multidisque, des titres absents et des artistes incomplets. Les vues albums, artistes et pistes montrent les replis déclarés, les ambiguïtés et le contexte de source. L'ordre reste stable et les pistes suivent disque puis piste avec un repli déterministe. Aucune copie ou édition ne fusionne sur son nom ou ses tags seuls. KD-017, KD-027, KD-033.

## KV-005. Rechercher et revenir au même contexte

Rechercher un titre d'album, un titre de piste, un artiste d'album et un artiste de piste avec des variations de casse et d'accents. Ouvrir un album puis revenir. Les mêmes résultats apparaissent avec leur contexte album et source, et la liste retrouve sa position. La piste courante et ses commandes restent visibles. Limite : recherche floue, opérateurs, filtres combinables, historique général et plein écran ne sont pas requis. KD-027, KD-040.

## KV-006. Modifier une playlist durable

Créer deux playlists. Dans la première, ajouter deux fois une piste, renommer la playlist, réordonner et retirer d'autres pistes. Supprimer la deuxième playlist, puis redémarrer kuro. La première conserve son nom, son ordre, ses doublons et ses références, y compris lorsqu'une source devient indisponible. La deuxième reste supprimée. Limite : import, export, playlists intelligentes et conversion de la file restent au backlog. KD-018, KD-029, KD-034.

## KV-007. Appliquer les commandes de file

Lancer un album, utiliser **Jouer ensuite** et **Ajouter**, réordonner, retirer la piste courante et vider la file. Refaire **Jouer ensuite** sans piste courante. Chaque commande suit KD-034, sans démarrage implicite pour **Jouer ensuite** ou **Ajouter**. **Précédent** depuis la première piste revient au début. La fin et le vidage arrêtent la lecture. KD-018, KD-034.

## KV-008. Borner les erreurs de lecture et de sortie

Placer plusieurs références indisponibles dans la file, traverser la file, puis perdre le périphérique audio. Chaque référence indisponible est passée au plus une fois avec une erreur visible. La fin arrête la lecture. La perte de sortie arrête le son sans bascule et son retour ne relance rien. KD-010, KD-011, KD-039.

## KV-009. Mesurer le gapless et respecter le volume système

Sur la sortie partagée identifiée, lire les enchaînements homogènes du corpus PCM stéréo retenu et mesurer la rupture selon le seuil décidé par KB-012. Redémarrer kuro après avoir changé le volume système. kuro utilise le volume système courant, ne restaure aucun ancien niveau et ne l'augmente pas. Limite : DSD, multicanal, mode exclusif, volume matériel et traitement du signal sont hors U-M1. KD-014, KD-020, KD-039.

## KV-010. Restaurer la file sans reprendre le son

Arrêter kuro pendant une piste après avoir préparé une file, puis redémarrer. La file et le meilleur point enregistré reviennent, mais le son reste arrêté. **Lecture** reprend la piste restaurée. Choisir une autre piste démarre celle-ci. Limite : aucune exactitude à l'échantillon n'est promise. KD-004, KD-012.

## KV-011. Sauvegarder et restaurer sans perdre l'état précédent

Créer un snapshot avec des sources absentes, des références, des métadonnées connues, des playlists, une file, des préférences et une pochette détenue par l'application. Restaurer après aperçu et confirmation. Comparer chaque donnée durable au snapshot, vérifier les références indisponibles, puis lancer explicitement un média disponible. kuro repart initialement sans son. Les médias, les images de source, les caches et les secrets sont absents du snapshot.

Tester ensuite un snapshot invalide, un snapshot incompatible et une interruption de restauration. Dans les trois cas, l'état précédent reste récupérable. Limite : la restauration remplace une bibliothèque et garantit seulement le format U-M1 livré. KD-006, KD-030, KD-035.

## KV-012. Fonctionner hors Internet et protéger la session

Après installation, couper Internet, démarrer à froid, relancer et parcourir toutes les fonctions de U-M1. Le produit n'exige aucun compte ou contrôle cloud. Vérifier qu'il n'écoute pas sur le réseau local et que le contrôle local appartient à l'utilisateur de la session. Produire un diagnostic avec données sensibles et contrôler l'aperçu expurgé avant export. Limite : un NAS exige seulement sa joignabilité sur le réseau local. KD-009, KD-022, KD-024.

## KV-013. Accepter la cible complète

Sur le matériel et le corpus cibles, importer environ 20 000 albums et 3 To, mesurer la mémoire, la durée d'import, la première page et le 95e percentile de recherche. Vérifier aussi le clavier, le focus visible, les libellés accessibles, le zoom et le déplacement dans la piste. Les sources restent octet pour octet inchangées après tous les scénarios. Comparer les mesures aux budgets acceptés après KB-013. Limite : 300 ms pour la recherche visible et une seconde pour la première page sont des objectifs tant que les mesures ne sont pas acceptées. KD-015, KD-019, KD-021.
