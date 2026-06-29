# -*- coding: utf-8 -*-
"""PCS #3 — invariante na AUGMENTACAO: ao agregar coluna/linha a uma base, o que ja existia NAO pode mudar.
assert_invariants(antes, depois, chaves_totais) compara nrows + somas de colunas-ancora (tol. relativa 1e-6);
levanta AssertionError se mudou. Uso: chamar APOS gravar a base enriquecida (vide regra N1 do ~/.claude/CLAUDE.md)."""
import duckdb, pathlib

def assert_invariants(antes, depois, chaves_totais):
    """antes/depois = caminhos de parquet; chaves_totais = {nome: expr_sql_agregada} (ex.: {'gmv':'SUM(VENDA)'})."""
    con = duckdb.connect(); con.execute("SET enable_progress_bar=false")
    def q(p, expr):
        pq = pathlib.Path(p).as_posix()
        return con.execute(f"SELECT {expr} FROM read_parquet('{pq}')").fetchone()[0]
    na, nd = q(antes, "COUNT(*)"), q(depois, "COUNT(*)")
    msgs = []
    if na != nd:
        msgs.append(f"rowcount mudou: {na:,} -> {nd:,}")
    for nome, expr in chaves_totais.items():
        va, vd = q(antes, expr), q(depois, expr)
        if va in (None, 0):
            continue
        if abs((vd - va) / va) > 1e-6:
            msgs.append(f"{nome} mudou: {va:.6g} -> {vd:.6g}")
    con.close()
    if msgs:
        raise AssertionError("INVARIANTE QUEBRADA na augmentacao: " + " | ".join(msgs))
    return f"OK invariantes preservados ({na:,} linhas; {len(chaves_totais)} ancoras conferidas)"

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        # uso CLI: _check_invariants.py antes.parquet depois.parquet "col=SUM(col)" ...
        chaves = dict(kv.split("=", 1) for kv in sys.argv[3:])
        print(assert_invariants(sys.argv[1], sys.argv[2], chaves))
