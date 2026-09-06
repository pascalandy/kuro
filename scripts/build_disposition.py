#!/usr/bin/env python3
"""Build the current disposition of the 195 archived functions."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/archive/p1-p5/docs/inventaire-fonctions.tsv"
TARGET = ROOT / "docs/disposition-fonctions.tsv"
FIELDS = [
    "id_fonction",
    "disposition_courante",
    "etape",
    "source_decision",
    "reference_backlog",
    "portee_courante",
    "validation_courante",
]


def ids(domain: int, *numbers: int) -> list[str]:
    return [f"F{domain:02d}-{number:03d}" for number in numbers]


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        archived = list(csv.DictReader(stream, delimiter="\t"))
    names = {row["id"]: row["fonction"] for row in archived}
    dispositions: dict[str, tuple[str, str, str, str, str, str]] = {}

    def assign(function_ids: list[str], disposition: str, step: str, decisions: str,
               backlog: str, scope: str, validation: str = "") -> None:
        for function_id in function_ids:
            if function_id in dispositions:
                raise ValueError(f"Disposition dupliquée: {function_id}")
            dispositions[function_id] = (disposition, step, decisions, backlog, scope, validation)

    # D01. Installation et rôles
    assign(ids(1, 1), "partiel", "U-M1", "KD-003;KD-023", "KB-011", "Service et desktop sur la même machine; découpage interne à étudier", "KV-001")
    assign(ids(1, 2), "engage", "U-M1", "KD-003", "", "Service actif après fermeture de la fenêtre et arrêté par Quitter", "KV-001")
    assign(ids(1, 3), "partiel", "U-M1", "KD-022", "KB-004", "Contrôle local limité à l'utilisateur de la session; contrôle réseau différé", "KV-012")
    assign(ids(1, 4), "differe", "backlog", "KD-007", "KB-006", "Clients autres que Linux Omarchy sans engagement")
    assign(ids(1, 5), "hors_portee", "backlog", "KD-005", "KB-014", "Le NAS fournit une source montée; kuro n'y déploie pas son service")
    assign(ids(1, 6), "engage", "U-M1", "KD-023", "", "Versions installées figées et identifiables", "KV-001")
    assign(ids(1, 7), "differe", "backlog", "KD-023", "KB-007", "Mise à jour automatique sans engagement")
    assign(ids(1, 8), "partiel", "U-M1", "KD-030;KD-035", "KB-020", "Restauration du format U-M1; migration ou relocalisation entre versions différée", "KV-011")

    # D02. Sources et import
    assign(ids(2, 1), "engage", "U-M1", "KD-001;KD-036", "", "Dossier local lu sans modifier ses fichiers", "KV-002;KV-013")
    assign(ids(2, 2), "partiel", "U-M1", "KD-005", "KB-014", "Montage NAS déjà disponible; protocole et identifiants hors de kuro", "KV-003")
    assign(ids(2, 3), "differe", "backlog", "KD-021", "KB-016", "Aucune copie de média par kuro")
    assign(ids(2, 4), "partiel", "U-M1", "KD-016;KD-036", "KB-002", "Changements trouvés par un scan pilotable; surveillance automatique différée", "KV-002")
    assign(ids(2, 5), "engage", "U-M1", "KD-016;KD-036", "", "Nouveau scan manuel, annulable et reprenable", "KV-002")
    assign(ids(2, 6), "partiel", "U-M1", "KD-029", "KB-016", "Retrait explicite qui masque la source; réactivation automatique interdite", "KV-003")
    assign(ids(2, 7), "partiel", "U-M1", "KD-028", "KB-022", "Relocalisation de racine avec chemins relatifs identiques seulement", "KV-003")
    assign(ids(2, 8), "differe", "backlog", "KD-036", "KB-016", "Règles d'exclusion configurables sans engagement")
    assign(ids(2, 9), "partiel", "U-M1", "KD-014;KD-039", "KB-012", "Sous-ensemble garanti des formats PCM stéréo candidats; DSD exclu", "KV-009")
    assign(ids(2, 10), "engage", "U-M1", "KD-036", "", "Fichier invalide signalé sans bloquer le reste du scan", "KV-002")
    assign(ids(2, 11), "engage", "U-M1", "KD-017;KD-033", "", "Tags locaux lus avec replis explicites", "KV-004")
    assign(ids(2, 12, 13, 14, 15), "differe", "backlog", "KD-033", "KB-016", "Import spécialisé non requis par U-M1")
    assign(ids(2, 16), "differe", "backlog", "KD-029", "KB-016", "Purge des références comme opération séparée à décider")
    assign(ids(2, 17), "differe", "backlog", "KD-016;KD-036", "KB-002", "Analyse ou scan programmé sans engagement")
    assign(ids(2, 18), "differe", "backlog", "KD-036", "KB-016", "Analyse spécialisée à la demande sans engagement")

    # D03. Identité, éditions et métadonnées
    assign(ids(3, 1), "partiel", "U-M1", "KD-028;KD-033", "KB-017", "Références et copies distinctes; organisation avancée différée", "KV-004")
    assign(ids(3, 2, 3), "differe", "backlog", "KD-028", "KB-017", "Identification enrichie ou manuelle sans engagement")
    assign(ids(3, 4, 5, 7, 9, 10, 11), "differe", "U-M3", "KD-037", "KB-024", "Organisation volontaire des éditions et corrections internes à préciser après U-M1")
    assign(ids(3, 6, 8, 12, 13, 14, 15, 16, 17, 21, 22, 24), "differe", "backlog", "KD-037", "KB-017", "Métadonnée ou édition avancée au-delà de U-M3 limité")
    assign(ids(3, 18, 19, 20, 23), "differe", "backlog", "KD-037", "KB-001", "Modèle classique avancé non requis")

    # D04. Vues, recherche et navigation
    assign(ids(4, 1, 2, 3), "engage", "U-M1", "KD-001;KD-033", "", "Vue locale avec replis et ambiguïtés visibles", "KV-004")
    assign(ids(4, 4), "engage", "U-M1", "KD-027", "", "Recherche album, piste et artiste sans casse ni accents", "KV-005")
    assign(ids(4, 5, 8, 9), "differe", "U-M2", "KD-037", "KB-023", "Filtres locaux à préciser après l'usage de U-M1")
    assign(ids(4, 6), "engage", "U-M1", "KD-027", "", "Ordre alphabétique stable et ordre disque-piste déterministe", "KV-004")
    assign(ids(4, 7, 13, 14), "differe", "backlog", "KD-040", "KB-021", "Navigation ou personnalisation avancée sans engagement")
    assign(ids(4, 10), "partiel", "U-M1", "KD-040", "KB-021", "Retour à la liste ou recherche avec place conservée; historique général différé", "KV-005")
    assign(ids(4, 11), "differe", "backlog", "KD-037", "KB-001", "Vues classiques avancées non requises")
    assign(ids(4, 12), "partiel", "U-M1", "KD-028;KD-033", "KB-017", "Source, copie et ambiguïté visibles; gestion avancée des versions différée", "KV-004")
    assign(ids(4, 15), "partiel", "U-M1", "KD-002;KD-030", "KB-017", "Images de source en lecture seule et pochettes détenues restaurables; édition différée", "KV-004;KV-011")

    # D05. Playlists, favoris et organisation personnelle
    assign(ids(5, 1, 2, 3, 4), "engage", "U-M1", "KD-034", "", "Création, nom, renommage, suppression, ordre et doublons d'une playlist", "KV-006")
    assign(ids(5, 7), "differe", "U-M2", "KD-037", "KB-023", "Favoris d'albums et de pistes après U-M1")
    assign(ids(5, 5, 6, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23), "differe", "backlog", "KD-034;KD-037", "KB-018", "Organisation, historique, automatisation ou export au-delà des playlists U-M1")
    assign(ids(5, 8), "hors_portee", "backlog", "KD-024", "KB-018", "U-M1 sert une personne sur son compte local")
    assign(ids(5, 10, 11, 12, 13), "differe", "backlog", "KD-037", "KB-017", "Tags d'objets et import de tags sans engagement")

    # D06. Transport et file
    assign(ids(6, 1, 2, 3, 4, 5, 6), "engage", "U-M1", "KD-018;KD-034", "", "Transport et file selon les effets précis de Lecture, Jouer ensuite et Ajouter", "KV-007")
    assign(ids(6, 7, 8), "differe", "U-M2", "KD-034", "KB-018", "Mélange et répétition candidats après U-M1")
    assign(ids(6, 9, 10, 11), "differe", "backlog", "KD-034", "KB-018", "Historique et conversion de file sans engagement")
    assign(ids(6, 12), "differe", "backlog", "KD-039", "KB-003", "Fondu enchaîné hors audio U-M1")
    assign(ids(6, 13), "engage", "U-M1", "KD-014;KD-039", "KB-012", "Gapless exigé; corpus PCM homogène et seuil exacts fixés par l'étude", "KV-009")
    assign(ids(6, 14), "engage", "U-M1", "KD-004;KD-012;KD-019", "", "Déplacement temporel accessible et meilleur point restauré à l'arrêt", "KV-010;KV-013")

    # D07. Sortie audio
    assign(ids(7, 1), "engage", "U-M1", "KD-039", "", "Sortie locale partagée avec le système", "KV-008;KV-009")
    assign(ids(7, 2), "partiel", "U-M1", "KD-011;KD-039", "KB-003", "Sortie partagée active; perte arrêtée sans bascule", "KV-008")
    assign(ids(7, 3, 9), "etude", "étude", "KD-014;KD-039", "KB-012", "Capacités de la sortie à établir pour le corpus PCM stéréo")
    assign(ids(7, 4, 5, 6, 7, 11, 12), "differe", "backlog", "KD-039", "KB-003", "Contrôle ou diagnostic audio avancé hors U-M1")
    assign(ids(7, 8, 10, 13), "hors_portee", "backlog", "KD-039", "KB-003", "DSD, multicanal ou MQA hors du corpus U-M1")

    # D08. Traitement du signal
    assign(ids(8, *range(1, 19)), "differe", "backlog", "KD-039", "KB-003", "Traitement ou analyse audio hors U-M1")

    # D09. Réseau et zones
    assign(ids(9, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15), "differe", "backlog", "KD-007;KD-031", "KB-004", "Contrôle réseau, endpoint ou multiroom sans engagement")
    assign(ids(9, 8), "hors_portee", "backlog", "KD-032", "KB-004", "Aucun accès RAAT supposé et aucune parité Roon")

    # D10. Découverte et contenus éditoriaux
    assign(ids(10, *range(1, 11)), "differe", "backlog", "KD-037", "KB-019", "Contenu éditorial ou recommandation au-delà des favoris et filtres U-M2")

    # D11. Services externes
    assign(ids(11, *range(1, 13)), "differe", "backlog", "KD-007;KD-025", "KB-005", "Service, synchronisation ou API externe sans engagement")

    # D12. Sauvegarde, desktop et résilience
    assign(ids(12, 1), "engage", "U-M1", "KD-006;KD-030", "", "Snapshot manuel cohérent des données durables et métadonnées connues", "KV-011")
    assign(ids(12, 2), "differe", "backlog", "KD-030", "KB-020", "Planification et historique de sauvegardes non requis")
    assign(ids(12, 3), "engage", "U-M1", "KD-030;KD-035", "", "Remplacement confirmé, compatible et récupérable en cas d'échec", "KV-011")
    assign(ids(12, 4), "engage", "U-M1", "KD-022", "", "Journaux expurgés avec aperçu avant export", "KV-012")
    assign(ids(12, 5), "partiel", "U-M1", "KD-019;KD-040", "KB-008", "Commandes clavier accessibles; intégration MPRIS différée", "KV-013")
    assign(ids(12, 6), "differe", "backlog", "KD-019", "KB-021", "Infobulles non imposées par le socle d'accessibilité")
    assign(ids(12, 7), "partiel", "U-M1", "KD-040", "KB-021", "Piste courante et commandes visibles; plein écran différé", "KV-005")
    assign(ids(12, 8), "engage", "U-M1", "KD-004;KD-012", "", "File, position, playlists et préférences durables", "KV-006;KV-010;KV-011")
    assign(ids(12, 9), "engage", "U-M1", "KD-001;KD-015", "KB-013", "Environ 20 000 albums et 3 To; mesures requises sur la cible connue", "KV-013")
    assign(ids(12, 10), "engage", "U-M1", "KD-019", "", "Clavier, focus, libellés, zoom et déplacement dans la piste", "KV-013")
    assign(ids(12, 11), "partiel", "U-M1", "KD-004;KD-035", "KB-020", "Reprise U-M1 et restauration échouée récupérable; migrations futures différées", "KV-010;KV-011")
    assign(ids(12, 12), "differe", "U-M2", "KD-019", "KB-008", "Touches média et MPRIS comme confort indépendant")
    assign(ids(12, 13), "engage", "U-M1", "KD-010;KD-011;KD-039", "", "Erreur de média ou perte de sortie bornée sans reprise automatique", "KV-008")

    # D13. Hors connexion et protection des données
    assign(ids(13, 1), "engage", "U-M1", "KD-009;KD-024", "", "Toutes les fonctions U-M1 sans Internet après installation", "KV-012")
    assign(ids(13, 2), "engage", "U-M1", "KD-021", "", "Médias et images de source jamais modifiés ou supprimés", "KV-013")
    assign(ids(13, 3), "engage", "U-M1", "KD-010;KD-029", "", "Références conservées et aucune reprise lors du retour du NAS", "KV-003;KV-008")
    assign(ids(13, 4), "engage", "U-M1", "KD-006;KD-022", "", "Secrets exclus des sauvegardes et des diagnostics exportés", "KV-011;KV-012")
    assign(ids(13, 5), "engage", "U-M1", "KD-022", "", "Contrôle limité à l'utilisateur local de la session", "KV-012")

    # D14. Adoption et licences
    assign(ids(14, 1, 4), "etude", "étude", "KD-025;KD-038", "KB-010", "Licence du code et des dépendances à décider sur l'artefact exact")
    assign(ids(14, 2), "engage", "U-M1", "KD-023", "KB-015", "Construction reproductible exigée; environnement exact fixé par l'étude", "KV-001")
    assign(ids(14, 3), "differe", "backlog", "KD-025", "KB-005", "Droits examinés seulement pour chaque fournisseur candidat")

    # D15. Mobile
    assign(ids(15, 1, 2, 3), "differe", "U-M4", "KD-031", "KB-009", "Question séparée de l'étude mobile; aucune fonction engagée")

    missing = sorted(set(names) - set(dispositions))
    extra = sorted(set(dispositions) - set(names))
    if missing or extra:
        raise ValueError(f"IDs manquants={missing}, inattendus={extra}")

    with TARGET.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in archived:
            function_id = row["id"]
            disposition, step, decisions, backlog, scope, validation = dispositions[function_id]
            writer.writerow({
                "id_fonction": function_id,
                "disposition_courante": disposition,
                "etape": step,
                "source_decision": decisions,
                "reference_backlog": backlog,
                "portee_courante": f"{names[function_id]} : {scope}",
                "validation_courante": validation,
            })


if __name__ == "__main__":
    main()
