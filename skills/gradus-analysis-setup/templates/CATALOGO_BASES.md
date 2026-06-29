# CATÁLOGO DE BASES — {{PROJETO}}

> **Macro→micro:** caracterize a base na 1ª vez que tocá-la (grão · âncoras · chave · gotchas). Evita re-explorar
> e blinda as análises micro. A tabela-resumo é **auto-gerada por `scripts/_catalogo_bases.py`** (lê metadados dos
> parquet; instantâneo) — re-rode ao criar uma base nova. Âncoras numéricas detalhadas: ver `docs/FONTE_DA_VERDADE.md`.

## Tabela-resumo (auto-gerada — re-rodar `_catalogo_bases.py` ao criar base)

| base | dir | linhas | #col | tamanho |
|---|---|---:|---:|---:|
| <a preencher pelo _catalogo_bases.py> | | | | |

---

## Fichas das bases-chave

> Uma ficha por base relevante. Template (copiar e preencher):

### <nome_da_base>.parquet  *(<papel: ex. spine / fonte da atribuição / base do motor>)*
- **Grão:** <uma linha = ?> (ex.: linha de pedido `CHAVE × SKU × …`). <N linhas, M col>.
- **Campos-chave:** <colunas que importam> (ex.: `CHAVE`, `VALOR`, `categoria`, …).
- **Âncora:** <agregação verificável> (ex.: `SUM(VALOR) WHERE filtro` = R$ <a preencher> MM).
- **Chave de join:** <coluna(s)> = <coluna na outra base>.
- **Gotchas:** <pegadinhas> (ex.: colunas aditivas → cuidado com `SELECT *`; `UPPER(TRIM(...))` no join; código vs nome).
