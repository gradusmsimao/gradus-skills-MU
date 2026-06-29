# -*- coding: utf-8 -*-
"""Detector READ-ONLY de organização (não move/apaga nada — só reporta). Roda à mão p/ um raio-x da pasta:
  python -X utf8 docs/_check_organizacao.py
Lista: (1) scripts de exploracoes/ sem menção em docs/ ou no inventário (candidatos a órfão);
(2) parquets grandes em raw inputs/ (retenção); (3) versões duplicadas aparentes do mesmo arquivo."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]

docs_txt = ""
for p in (ROOT / "docs").glob("*.md"):
    docs_txt += p.read_text(encoding="utf-8", errors="ignore")

# (1) exploracoes/*.py sem mencao em docs
expl = sorted((ROOT / "exploracoes").glob("*.py"))
orf = [p.name for p in expl if p.stem not in docs_txt]
print(f"== exploracoes/*.py SEM mencao em docs/ ({len(orf)} de {len(expl)}) — candidatos a orfao/cataloga ==")
for x in orf:
    print("   ", x)

# (2) parquets grandes em raw inputs
big = sorted(((p.name, p.stat().st_size / 1e9) for p in (ROOT / "raw inputs").glob("*.parquet")),
             key=lambda t: -t[1])
print(f"\n== parquets em raw inputs/ (retencao) ==")
for n, g in big:
    print(f"   {g:5.1f} GB  {n}")

# (3) versoes duplicadas aparentes (mesmo prefixo + sufixo de versao/backup)
sufx = re.compile(r"(_ORIGINAL|_PRE_|_BKP|_BACKUP|_OLD|_v\d|_sem_)", re.I)
dups = [p.name for p in (ROOT / "raw inputs").glob("*.parquet") if sufx.search(p.name)]
if dups:
    print(f"\n== possiveis backups/versoes em raw inputs/ (rever retencao) ==")
    for d in dups:
        print("   ", d)
else:
    print("\n== sem backups/versoes aparentes em raw inputs/ (ok) ==")
print("\n(read-only: nada foi movido/apagado. A organizadora propoe; o dono decide.)")
