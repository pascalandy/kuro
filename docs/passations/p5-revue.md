# Passation P5 au coordinateur

P5 est validée par le coordinateur. Il a autorisé sa finalisation et son commit local, sans push. La revue indépendante conclut à une couverture documentaire complète des obligations P1. Les décisions produit restent ouvertes. Aucun développement n'est autorisé par cette passation.

## Travail remis

| Fichier | Résultat |
| --- | --- |
| [Revue finale](../revue-finale.md) | Verdict, 20 chaînes usages et MVP, cohérence des étapes, constats et responsables |
| [Décisions ouvertes](../decisions-ouvertes.md) | O-01 à O-09, informations manquantes, options P3, preuves et effets |
| [README](../../README.md) | Accès direct aux conclusions et décisions avant le détail du dossier |
| [Checklist](../checklist.md) | Contrôles P5 réalisés, validation manager et publication séparées |
| [Journal](../decisions.tsv) | Décisions P5 ajoutées sans réécrire les 25 lignes antérieures |
| [Cette passation](p5-revue.md) | Contrôle rejouable et limites du transfert |

P5 a lu le contexte, le programme, les usages, les dix critères, les passations P1 à P4, l'inventaire, les contrats et la faisabilité. La revue couvre les six plans, les sept milestones et les 50 scénarios. Les registres ont été parcourus pour leur couverture et leurs statuts. Deux sondages primaires techniques sont décrits dans la revue finale. P5 n'a pas refait la recherche des 84 sources Roon ni des 30 références TECH.

Le coordinateur a accepté la clarification du dictionnaire `retenu_provisoire`. F12-013 conserve M1, son cas exact et son admission provisoire. Aucun fichier de référence P1 à P4 n'a été corrigé. Aucun autre changement de fond n'a été proposé ou effectué.

## Rejouer les vérifications documentaires

Lire la commande, puis l'exécuter depuis la racine du dépôt. Elle lance le contrôle P4 complet, donc P3 et P2, avec leurs diff de préservation. Elle vérifie ensuite les 20 chaînes, les neuf décisions ouvertes, le préfixe du journal et les fichiers publiables. Python et Git existants suffisent. Les motifs de recherche ciblent des secrets usuels et détails privés, sans lire de fichier extérieur au dépôt.

```bash
python - <<'PY'
import csv
import re
import subprocess
from pathlib import Path

root = Path.cwd()
base = '00bd920a90b04b760c76b92b9f08fc4617dc5f62'
p4 = (root / 'docs/passations/p4-multiplan.md').read_text()
command = re.search(r'```bash\n(.*?)\n```', p4, re.S).group(1)
subprocess.run(['bash', '-e', '-c', command], check=True)
coverage = {r['id_fonction']: r for r in csv.DictReader(
    (root / 'docs/couverture.tsv').open(), delimiter='\t')}
review = (root / 'docs/revue-finale.md').read_text()
chains = [line for line in review.splitlines()
          if re.match(r'^\| (?:MVP|U)-\d{2} ', line)]
expected = {f'{prefix}-{i:02}' for prefix in ['MVP', 'U'] for i in range(1, 11)}
seen = []
for line in chains:
    cells = [v.strip() for v in line.strip('|').split('|')]
    assert len(cells) == 7
    id = cells[0].split()[0]
    seen.append(id)
    ids = re.findall(r'F\d{2}-\d{3}', cells[1])
    assert ids and len(ids) == len(set(ids))
    selected = [coverage[id] for id in ids]
    assert all(r['milestone'] == 'M1' for r in selected)
    contracts = re.findall(r'C-\d{2}', cells[2])
    assert contracts and set(contracts) <= {f'C-{i:02}' for i in range(1, 10)}
    for column, field in [(3, 'plan'), (4, 'phase'), (5, 'scenario')]:
        links = re.findall(r'\]\(([^)]+)\)', cells[column])
        assert set(links) == {r[field] for r in selected}, (id, field)
assert len(seen) == 20 and set(seen) == expected
opened = (root / 'docs/decisions-ouvertes.md').read_text()
questions = re.findall(r'^\| (O-\d{2}) \|', opened, re.M)
assert len(questions) == 9 and set(questions) == {f'O-{i:02}' for i in range(1, 10)}
for p in root.rglob('*.md'):
    for id in re.findall(r'\bC-\d{2}\b', p.read_text()):
        assert id in {f'C-{i:02}' for i in range(1, 10)}, (p, id)
    for id in re.findall(r'\bE-\d{2}\b', p.read_text()):
        assert id in {f'E-{i:02}' for i in range(1, 9)}, (p, id)
    for id in re.findall(r'\bO-\d{2}\b', p.read_text()):
        assert id in set(questions), (p, id)
tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', base], text=True).splitlines()
mutable = {'README.md', 'docs/checklist.md', 'docs/decisions.tsv'}
for name in tracked:
    old = subprocess.check_output(['git', 'show', f'{base}:{name}'])
    current = (root / name).read_bytes()
    if name == 'docs/decisions.tsv':
        assert current.startswith(old), 'journal antérieur modifié'
    elif name not in mutable:
        assert current == old, ('référence P1-P4 modifiée', name)
files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
assert all(p.suffix in {'.md', '.tsv'} and not p.is_symlink() for p in files)
assert not any(p.name.lower().startswith('license') for p in files)
patterns = [r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
            r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{20,}',
            r'(?:/home/|/Users/)[A-Za-z0-9._-]+/',
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}']
findings = []
for p in files:
    content = p.read_text()
    for number, line in enumerate(content.splitlines(), 1):
        if any(re.search(pattern, line) for pattern in patterns):
            findings.append((str(p.relative_to(root)), number))
assert not findings, ('marqueurs à examiner sans exposer leur valeur', findings)
subprocess.run(['git', 'diff', '--check'], check=True)
print('20 chaînes U/MVP valides; 9 décisions ouvertes; références P1-P4 et journal antérieur préservés')
print(f'{len(files)} fichiers documentaires UTF-8; aucun marqueur ciblé détecté; aucun code applicatif ou média')
PY
```

## Résultats et limites

Le contrôle P4 indépendant initial a confirmé 29 Markdown, 628 liens locaux, 25 décisions et aucune erreur. Les 195 fonctions gardent leurs cas spécifiques et dispositions, avec six plans, sept milestones, 28 phases sans cycle et 50 scénarios. Les 30 références TECH, neuf contrats et huit études sont valides.

Le contrôle P5 exécuté a produit 32 Markdown, 755 liens locaux, 25 décisions avant ajout des quatre lignes P5 et aucune erreur. Il confirme 20 chaînes valides, neuf décisions ouvertes, 35 fichiers documentaires UTF-8 et aucun marqueur ciblé. Les références P1 à P4 et le journal antérieur sont préservés. Après ajout du journal P5, le contrôle a confirmé 32 Markdown, 755 liens locaux, 29 décisions et aucune erreur, avec les mêmes invariants. Les comptes de liens et de journal évoluent avec les nouvelles références et décisions. La commande régénère l'état réel.

Aucun test runtime, import, scan NAS, mesure DAC, restauration, installation ou inspection de média utilisateur n'a eu lieu. La recherche ciblée des secrets complète la lecture de contenu, sans garantie universelle. Aucun compte fournisseur ni droit commercial n'est acquis.

## Suite et transfert d'écriture

Le coordinateur a lu les nouveaux documents, rejoué le contrôle et validé P5. Il a autorisé le commit local `docs(kuro): review coverage and consolidate open decisions`. La publication autorisée sera vérifiée séparément avec SHA distant et URL de PR. La licence reste ouverte, sans fichier LICENSE. La fin documentaire n'autorise pas le développement.

Après finalisation et vérification du commit local, l'auteur cesse les écritures. Les adaptations de skills et le modèle imposé figurent dans la checklist.

## Attention

Revue indépendante par GPT-6 Astra, effort medium. Aucune revue multimodèle n'a été réalisée.

Les décisions O-01 à O-09 et les observations de référence restent ouvertes. Le journal décrit la rédaction et les contrôles réellement exécutés. Il ne présente aucune milestone produit comme réalisée. La validation du coordinateur est consignée après son contrôle indépendant. Aucun transcript local propre à cette phase n'a été fourni comme fichier. La vérification du journal repose sur les opérations de cette session et les preuves locales citées.

## Validation du coordinateur

Le coordinateur a lu intégralement les trois nouveaux documents et le diff du README, de la checklist et du journal. Il a exécuté la première commande de cette passation avec arrêt sur erreur. Son contrôle a confirmé 32 Markdown, 755 liens, 29 décisions, 195 fonctions, 20 chaînes et neuf décisions ouvertes, sans erreur. Les références P1 à P4 et le préfixe du journal sont préservés.

Il a accepté P5 et autorisé le commit local, sans push. La ligne de validation ajoutée au journal porte le total à 30 décisions. Le contrôle final de l'auteur confirme 32 Markdown, 755 liens, 30 décisions et aucune erreur, avec les mêmes invariants. La publication reste une opération distincte confiée au coordinateur.
