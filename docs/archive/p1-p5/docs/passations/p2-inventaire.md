# Passation P2 au coordinateur

P2 est validée par le coordinateur. Il a autorisé le commit documentaire local après ses contrôles. La publication reste confiée au coordinateur. L’auteur cède les écritures après cette finalisation.

## Travail terminé

Le registre contient 195 entrées, 84 sources externes et une référence interne. Les quinze familles demandées sont couvertes, y compris autonomie, sécurité, open source et frontière mobile. Le décompte initial de quatorze familles était une erreur du coordinateur, corrigée sans modifier le périmètre.

Les sources ont été ouvertes le 2026-09-06. L’auteur a intégré les recherches serveur et audio, puis client et contenus, produites par deux agents indépendants en lecture seule. La comparaison couvre les générations documentaires, les omissions des listes anciennes et cinq contradictions conservées au niveau des fonctions. Roon n’a pas été exécuté. Sa version et son build restent inconnus.

Technical writing et Unslop ont guidé la rédaction et la revue directe de prose. Deslop reste absent selon la recherche du coordinateur. Aucun skill ni outil n’a été installé ou modifié. Le workflow utilisateur a prévalu sur les prescriptions incompatibles avec le périmètre documentaire.

## Fichiers remis

| Fichier | Résultat |
| --- | --- |
| [Inventaire](../inventaire-roon.md) | Méthode, dictionnaire, quinze familles, réserves et exclusions |
| [Registre fonctionnel](../inventaire-fonctions.tsv) | Douze colonnes, identifiants stables et scénarios futurs |
| [Sources](../sources.md) | Sources primaires datées, liens exacts, ancienneté et accessibilité |
| [README](../../README.md) | Accès aux documents P2 et état de revue |
| [Checklist](../checklist.md) | Rédaction et contrôles P2 séparés du passage manager |
| [Journal](../decisions.tsv) | Lignes P2 ajoutées sans réécriture de P1 |
| [Cette passation](p2-inventaire.md) | Vérification reproductible et limites de remise |

## Vérification documentaire reproductible

Depuis la racine du dépôt, cette commande vérifie les fichiers réels sans installer d’outil ni lire de média. Elle contrôle la forme des TSV, les valeurs normalisées, les références de sources, leurs domaines primaires, les liens locaux avec ancres et les preuves du journal. Elle ne teste pas la disponibilité réseau des pages, dont l’ouverture relève de la recherche datée.

```bash
python - <<'PY'
import csv
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote

root = Path.cwd()
errors = []
p = root / 'docs/inventaire-fonctions.tsv'
with p.open() as f:
    table = list(csv.reader(f, delimiter='\t'))
columns = ['id', 'domaine', 'fonction', 'comportement_reference',
           'statut_preuve', 'date_preuve', 'sources', 'portee_reference',
           'responsable_kuro', 'disposition', 'milestone', 'validation_future']
assert table[0] == columns
rows = [dict(zip(columns, row)) for row in table[1:]]
for path, width in [(p, 12), (root / 'docs/decisions.tsv', 6)]:
    with path.open() as f:
        for number, row in enumerate(csv.reader(f, delimiter='\t'), 1):
            if len(row) != width or any(not v for v in row):
                errors.append(f'{path.name}:{number}: largeur ou champ vide')
            if any(v.lstrip().startswith(('=', '+', '-', '@')) for v in row):
                errors.append(f'{path.name}:{number}: préfixe formule')
            if any('\n' in v or '\r' in v or '\t' in v for v in row):
                errors.append(f'{path.name}:{number}: séparateur interne')
source_text = (root / 'docs/sources.md').read_text()
source_ids = re.findall(r'^## (SRC-\d{3}|INT-P1)$', source_text, re.M)
assert len(source_ids) == len(set(source_ids))
source_blocks = re.split(r'^## ', source_text, flags=re.M)[1:]
allowed_hosts = {'help.roonlabs.com', 'roon.app', 'blog.roonlabs.com', 'github.com'}
external_urls = []
for block in source_blocks:
    assert '2026-09-06' in block
    if block.startswith('SRC-'):
        urls = re.findall(r'\]\((https://[^)]+)\)', block)
        assert len(urls) == 1
        url = urls[0]
        assert urlsplit(url).hostname in allowed_hosts
        if urlsplit(url).hostname == 'github.com':
            assert urlsplit(url).path.startswith('/RoonLabs/')
        external_urls.append(url)
assert len(external_urls) == len(set(external_urls))
allowed = {
    'statut_preuve': {'documente', 'historique', 'contradictoire',
                     'a_observer', 'exigence_kuro', 'proposition_kuro'},
    'portee_reference': {'serveur_desktop', 'serveur_sortie',
                        'serveur_controle_sortie', 'kuro', 'mobile_futur'},
    'responsable_kuro': {'serveur_bibliotheque', 'serveur_lecture', 'sortie_audio',
                        'desktop', 'coordination_reseau', 'integrations',
                        'exploitation', 'projet', 'mobile'},
    'disposition': {'socle', 'retenu_provisoire', 'conditionnel', 'proposition', 'reporte'},
    'milestone': {f'M{i}' for i in range(1, 8)},
    'domaine': {f'D{i:02}' for i in range(1, 16)},
}
assert len(rows) == len({r['id'] for r in rows})
assert {r['domaine'] for r in rows} == allowed['domaine']
for row in rows:
    assert re.fullmatch(r'F\d{2}-\d{3}', row['id'])
    assert row['id'][1:3] == row['domaine'][1:]
    assert row['date_preuve'] == '2026-09-06'
    for column, values in allowed.items():
        assert row[column] in values, (row['id'], column)
    refs = row['sources'].split(';')
    assert set(refs) <= set(source_ids), row['id']
    if row['statut_preuve'] in {'documente', 'historique', 'contradictoire'}:
        assert all(ref.startswith('SRC-') for ref in refs)
    else:
        assert refs == ['INT-P1']
markdown = list(root.rglob('*.md'))
links = 0
for path in markdown:
    for raw in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', path.read_text()):
        if raw.startswith(('http:', 'https:', 'mailto:')):
            continue
        target, _, anchor = unquote(raw).partition('#')
        resolved = (path.parent / target).resolve() if target else path
        links += 1
        if not resolved.is_file():
            errors.append(f'{path.name}: lien absent {raw}')
        elif anchor:
            headings = re.findall(r'^#+ (.+)$', resolved.read_text(), re.M)
            slugs = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings]
            if anchor not in slugs:
                errors.append(f'{path.name}: ancre absente {raw}')
with (root / 'docs/decisions.tsv').open() as f:
    decisions = list(csv.DictReader(f, delimiter='\t'))
for row in decisions:
    assert (root / row['evidence']).is_file()
print(f'{len(rows)} fonctions; {len(external_urls)} sources externes; '
      f'{len(allowed["domaine"])} familles; {len(markdown)} Markdown; '
      f'{links} liens locaux; {len(decisions)} décisions; {len(errors)} erreurs')
print('Statuts:', dict(Counter(r['statut_preuve'] for r in rows)))
print('Milestones:', dict(Counter(r['milestone'] for r in rows)))
assert not errors, errors
PY
```

Le contrôle exécuté après finalisation du journal a produit :

```text
195 fonctions; 84 sources externes; 15 familles; 9 Markdown; 76 liens locaux; 13 décisions; 0 erreurs
Statuts: documente 173; contradictoire 5; exigence_kuro 7; a_observer 3; historique 1; proposition_kuro 6
Milestones: M1 60; M2 57; M3 30; M4 15; M5 26; M6 4; M7 3
```

`git diff --check` n’a signalé aucune erreur. `git status --short` montre trois fichiers suivis modifiés et quatre nouveaux documents P2. La lecture directe a vérifié les limites M1 et l’absence de choix de stack ou plan P4. Les sources externes sont 84 URL distinctes; leur préfixe officiel et toutes les références locales ont été contrôlés.

Les statistiques par milestone incluent les propositions et capacités conditionnelles. Elles ne comptent pas des engagements approuvés.

## Limites et prochaine étape

Aucune installation, application, capture d’interface, mesure audio, restauration ou lecture de média n’a eu lieu. Les validations du TSV sont futures. Il n’existe ni benchmark de 20 000 albums, ni preuve de gapless, ni garantie de droits fournisseurs.

Les formats M1 forment un sous-ensemble à définir. DSD est envisagé en M3. Les illustrations locales et les précisions d’accessibilité sont des propositions M1; elles ne changent pas les critères P1. Les licences des dépendances sont à examiner dès M1, tandis que les droits des contenus fournisseurs relèvent des intégrations conditionnelles M5.

Les conflits documentaires ne bloquent pas la remise P2. Ils interdisent certaines affirmations de parité. Le coordinateur a relu les sources et les dispositions, puis validé le passage P2. P3 peut examiner options, contrats et faisabilité. Aucun développement ne découle de cette passation.

## Revue manager et finalisation locale

Le coordinateur a lu l’inventaire complet, les 195 intitulés et comportements, puis sondé les sources, dont nugs, Discover et les playlists. Il a exécuté la commande de vérification complète. Son résultat était : 195 fonctions, 84 sources externes, 15 familles, 9 Markdown, 76 liens locaux, 13 décisions et 0 erreur. `git diff --check` était propre.

Le coordinateur a validé P2 et autorisé le commit `docs(kuro): map Roon features and evidence`, sans push. La checklist et le README consignent ce passage. Une quatorzième ligne de journal conserve cette validation; elle explique la différence avec les treize décisions comptées lors de la remise et de la revue.
