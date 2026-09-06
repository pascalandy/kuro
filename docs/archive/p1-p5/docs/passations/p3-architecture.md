# Passation P3 au coordinateur

P3 est validée par le coordinateur, qui a autorisé le commit documentaire local. Aucun push ou développement n'a été effectué par l'auteur P3. Après finalisation, les écritures reviennent au coordinateur. P4 peut commencer.

## Travail terminé

Trois formes complètes sont comparées : desktop avec moteur embarqué, service local autonome et serveur existant adapté. Le service local en monorepo est recommandé, avec SQLite, libmpv et Tauri comme premiers candidats d'étude. Les alternatives comprennent MPD, GStreamer, Navidrome, Qt et Electron. Aucune recommandation ne vaut choix utilisateur ou test réussi.

Neuf contrats documentaires précisent les identités, scans, commandes, file, format audio, sauvegarde, sécurité, ressources et distribution future. Huit études futures donnent les preuves nécessaires. Les décisions ouvertes identifient leurs responsables et l'effet sur M1 ou une étape ultérieure.

Les sources techniques sont distinctes du corpus Roon. Les deux chercheurs indépendants ont fourni leurs recherches audio et données en lecture seule. L'auteur a vérifié les principales sources et enregistré les limites d'accès. La recherche n'a consulté ni médias privés ni configuration NAS ou audio.

Technical writing et Unslop ont guidé la rédaction. How s'applique à l'explication de l'architecture proposée : aucun code kuro existant ne permet une trace runtime. Les exigences de prototypes, signatures implémentées et délégation depuis l'auteur restent exclues par le programme utilisateur. Les critères P1 et le registre P2 n'ont pas changé.

## Fichiers remis

| Fichier | Résultat |
| --- | --- |
| [Architecture](../architecture.md) | Recommandation, alternatives, composants, modèle et C-01 à C-09 |
| [Faisabilité](../faisabilite.md) | Build ou reuse, licences, fournisseurs, E-01 à E-08 et décisions ouvertes |
| [Sources techniques](../sources-techniques.md) | Sources primaires TECH, dates et limites |
| [README](../../README.md) | Accès P3 et état de revue |
| [Checklist](../checklist.md) | Rédaction et contrôle distincts de la validation manager |
| [Journal](../decisions.tsv) | Entrées ajoutées sans réécrire l'historique |
| [Cette passation](p3-architecture.md) | Contrôles et limites de remise |

## Vérification reproductible

La commande suivante, depuis la racine du dépôt, reprend le contrôle P2 et vérifie les nouveaux identifiants et liens. Elle ne requiert ni installation ni code applicatif. La vérification réseau des sources reste une recherche datée distincte.

```bash
python - <<'PY'
import csv
import re
from pathlib import Path

root = Path.cwd()
p2 = (root / 'docs/passations/p2-inventaire.md').read_text()
command = re.search(r"```bash\npython - <<'PY'\n(.*?)\nPY\n```", p2, re.S).group(1)
exec(compile(command, 'verification-p2', 'exec'))
tech = (root / 'docs/sources-techniques.md').read_text()
ids = re.findall(r'^## (TECH-\d{3})$', tech, re.M)
assert len(ids) == len(set(ids))
for block in re.split(r'^## TECH-', tech, flags=re.M)[1:]:
    assert re.search(r'\]\(https://[^)]+\)', block)
functions = {r['id'] for r in csv.DictReader(
    (root / 'docs/inventaire-fonctions.tsv').open(), delimiter='\t')}
for path in root.rglob('*.md'):
    if path.name == 'p3-architecture.md':
        continue
    content = path.read_text()
    for ref in re.findall(r'\bTECH-\d{3}\b', content):
        assert ref in ids, (path, ref)
    for ref in re.findall(r'\bF\d{2}-\d{3}\b', content):
        assert ref in functions, (path, ref)
architecture = (root / 'docs/architecture.md').read_text()
contracts = re.findall(r'^### (C-\d{2})\.', architecture, re.M)
assert contracts == [f'C-{i:02}' for i in range(1, 10)]
feasibility = (root / 'docs/faisabilite.md').read_text()
studies = re.findall(r'^\| (E-\d{2}) \|', feasibility, re.M)
assert studies == [f'E-{i:02}' for i in range(1, 9)]
print(f'{len(ids)} sources TECH; {len(contracts)} contrats; '
      f'{len(studies)} études futures; références valides')
PY
git diff --check
git diff --exit-code 734ed69 -- docs/produit-et-mvp.md docs/programme.md docs/inventaire-fonctions.tsv docs/inventaire-roon.md docs/sources.md
```

Résultat exécuté avant remise :

```text
195 fonctions; 84 sources externes Roon; 15 familles; 13 Markdown;
112 liens locaux; 19 décisions; 0 erreur
30 sources TECH; 9 contrats; 8 études futures; références valides
```

`git diff --check` est propre. `git status --short` montre trois fichiers suivis modifiés et quatre nouveaux Markdown P3. Les comptes de liens et références se régénèrent avec la commande ci-dessus.

Le contrôle sur les fichiers réels a vérifié les identifiants, les sources, les liens locaux et ancres, les colonnes TSV, les préfixes de formule et les preuves du journal. Le diff des critères et du corpus P2 contre 734ed69 est vide. La revue de prose a maintenu les statuts proposés et les limites de preuve.

## Limites et suite

Aucun résultat audio, benchmark, import, restauration, installation ou essai UI n'existe. Les 20 000 albums et 3 To restent une cible confirmée, pas un corpus examiné. Les formats, le DAC, le matériel, les budgets, la licence et les versions exactes restent ouverts. Les textes fournisseurs ne constituent pas une autorisation d'intégration.

Le coordinateur a validé les contrats, les sources et leur cohérence avec P1-P2. P4 peut créer exactement six plans de domaine et affiner les sept milestones, avec liens vers les fonctions, contrats et études. Les études restent futures. Aucun développement ne découle de cette passation.

## Revue manager et finalisation locale

Le coordinateur a lu l'architecture, la faisabilité, le registre TECH et cette passation. Il a exécuté indépendamment la commande P3 intégrale. Son contrôle a confirmé 13 Markdown, 112 liens locaux, 19 décisions et aucune erreur, avec 30 références TECH, neuf contrats et huit études futures. Les critères P1 et le corpus P2 sont inchangés contre 734ed69.

Le passage P3 vers P4 est validé. Le coordinateur a autorisé le commit local intitulé `docs(kuro): compare architectures and integration feasibility`, sans push. La ligne de validation ajoutée au journal porte le total à 20 décisions. Les choix de licence, les seuils proposés et les composants restent ouverts, conformément aux documents validés.
