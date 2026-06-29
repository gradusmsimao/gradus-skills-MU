# -*- coding: utf-8 -*-
"""catalog.py — tabela-resumo (markdown) das bases de 1+ diretorios, via metadados DuckDB (instantaneo).
PORTATIL (so duckdb + stdlib). Cola a tabela no catalogo de bases do projeto; complete com a ficha por base.

Uso: python -X utf8 catalog.py <dir1> [<dir2> ...]   (ex.: "raw inputs" "bases tratadas")"""
import sys, argparse, pathlib, duckdb

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+")
    a = ap.parse_args()
    con = duckdb.connect(); con.execute("SET enable_progress_bar=false")
    print("| base | dir | linhas | #col | tamanho |")
    print("|---|---|---:|---:|---:|")
    for d in a.dirs:
        for p in sorted(pathlib.Path(d).glob("*.parquet")):
            pq = p.as_posix()
            try:
                n = con.execute(f"SELECT COUNT(*) FROM read_parquet('{pq}')").fetchone()[0]
                c = len(con.execute(f"DESCRIBE SELECT * FROM read_parquet('{pq}')").fetchall())
                mb = p.stat().st_size / 1e6
                tam = f"{mb/1000:.1f} GB" if mb >= 1000 else f"{mb:.0f} MB"
                print(f"| {p.name} | {pathlib.Path(d).name} | {n:,} | {c} | {tam} |")
            except Exception as e:
                print(f"| {p.name} | {pathlib.Path(d).name} | ERRO | {str(e)[:30]} | |")

if __name__ == "__main__":
    main()
