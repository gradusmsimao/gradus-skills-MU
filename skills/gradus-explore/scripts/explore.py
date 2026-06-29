# -*- coding: utf-8 -*-
r"""explore.py — perfil rapido de uma base via DuckDB. PORTATIL (qualquer projeto; so duckdb + stdlib, sem _lib).
Nao carrega a base no pandas (out-of-core): SUMMARIZE da stats por coluna em 1 passada; head+tail nunca dump.

Uso:
  python -X utf8 explore.py <arquivo.parquet|.csv>            # perfil (schema, linhas, stats por coluna, head)
  python -X utf8 explore.py <arquivo> --sql "SELECT ... FROM \$T ..."   # query custom (\$T = a fonte), head+tail
  python -X utf8 explore.py <arquivo> --rows 8                # tamanho da amostra head/tail
"""
import sys, argparse, pathlib, duckdb

def fonte(path):
    p = pathlib.Path(path).as_posix(); ext = pathlib.Path(path).suffix.lower()
    if ext == ".csv":
        return f"read_csv_auto('{p}', sample_size=-1)"
    if ext in (".xlsx", ".xls"):
        return f"read_xlsx('{p}')"   # requer extensao excel do DuckDB; senao converter p/ parquet antes
    return f"read_parquet('{p}')"     # default: parquet

def head_tail(df, k):
    h = df.head(k).to_string(index=False)
    if len(df) <= 2 * k:
        return f"({len(df)} linhas)\n{h}"
    return f"({len(df)} linhas; head+tail {k})\n{h}\n  ...\n{df.tail(k).to_string(index=False)}"

def main():
    ap = argparse.ArgumentParser(description="Perfil DuckDB de uma base (head+tail; nao inunda o contexto).")
    ap.add_argument("path")
    ap.add_argument("--sql", default=None, help="SQL custom; use $T no lugar da fonte")
    ap.add_argument("--rows", type=int, default=5)
    a = ap.parse_args()
    con = duckdb.connect(); con.execute("SET enable_progress_bar=false")
    T = fonte(a.path)
    if a.sql:
        df = con.execute(a.sql.replace("$T", T)).df()
        print(head_tail(df, a.rows)); return
    n = con.execute(f"SELECT COUNT(*) FROM {T}").fetchone()[0]
    try:
        mb = pathlib.Path(a.path).stat().st_size / 1e6
        tam = f"{mb/1000:.1f} GB" if mb >= 1000 else f"{mb:.0f} MB"
    except Exception:
        tam = "?"
    print(f"== {pathlib.Path(a.path).name} | {n:,} linhas | {tam} ==")
    summ = con.execute(f"SUMMARIZE SELECT * FROM {T}").df()
    cols = [c for c in ["column_name", "column_type", "null_percentage", "approx_unique", "min", "max", "avg"]
            if c in summ.columns]
    print(summ[cols].to_string(index=False))
    print("\n-- head --")
    print(con.execute(f"SELECT * FROM {T} LIMIT {a.rows}").df().to_string(index=False))
    print("\n>> confirme o GRAO (o que 1 linha representa) e registre a ficha no catalogo de bases do projeto.")

if __name__ == "__main__":
    main()
