---
name: gradus-explore
description: >-
  Perfil / EDA inicial de uma base em projeto de análise Gradus (parquet/CSV via DuckDB, out-of-core — NÃO
  carregar tudo no pandas). Use ao receber uma base nova e precisar entender forma/grão/qualidade antes da
  análise, ou quando um número surpreende e quer checar o dado por baixo. Roda scripts/explore.py (schema,
  linhas, stats por coluna via SUMMARIZE, head+tail — sem inundar o contexto) e encerra registrando a ficha
  da base no catálogo do projeto. NÃO use para reconciliar fontes que divergem (gradus-metric-reconciliation),
  auditoria metodológica (auditora), nem para montar deck (storyline).
---

# Exploração / perfil de base (Gradus · DuckDB)

Entende a **forma, o grão e a qualidade** de uma base antes da análise — em DuckDB, sem puxar 10⁷–10⁸ linhas pro
pandas. Sai com uma ficha registrável no catálogo de bases do projeto.

> **Genérica** (qualquer projeto). O `scripts/explore.py` viaja com a skill (só `duckdb` + stdlib, sem `_lib`).
> Nomes de base/coluna nos exemplos são ilustrativos *(ex.: …)*; o específico do projeto vem das `references`.

## Quando usar · quando NÃO usar
- **Usar:** base nova a perfilar; "esse dado é confiável?"; um número saiu estranho e quero ver o dado cru; antes de rodar um motor/modelo.
- **NÃO usar:** dois números que deveriam bater não batem → `gradus-metric-reconciliation`; crítica metodológica → **auditora**; virar slide → **gradus-analysis-storyline**.

## Processo
1. **Perfil:** `python -X utf8 <skill>/scripts/explore.py <arquivo.parquet>` → schema, nº de linhas, tamanho, **stats por coluna** (null %, distinct aprox, min/max/avg via `SUMMARIZE`) e **head**.
2. **Confirmar o GRÃO** — o que **uma linha** representa (a pergunta que blinda toda análise micro depois). Se não for óbvio, checar com `--sql "SELECT chave, COUNT(*) FROM \$T GROUP BY 1 ORDER BY 2 DESC"`.
3. **Qualidade:** colunas com null alto, distinct suspeito (1 valor / cardinalidade = nº de linhas), datas fora de janela. *(N1: flagar, não assumir; "parece um ID" ≠ "é um ID".)*
4. **Sanidade dos totais/âncoras** com `--sql` (ex.: `SELECT SUM(valor) FROM \$T WHERE ...`) — confronto com a âncora esperada do projeto.
5. **Registrar a ficha** no catálogo de bases do projeto (ver `references`): grão · nº de linhas · colunas-chave · âncoras · chave de join · gotchas.

## Disciplina (N1)
- **Nunca carregar a base inteira no pandas** para perfilar — o `explore.py` usa DuckDB (`SUMMARIZE`/`COUNT`); resultado sempre **head+tail**, nunca dump.
- **1 job pesado por vez**; em base muito grande o `SUMMARIZE` escaneia (pode levar dezenas de s) — aceitável, mas não rode dois em paralelo.
- **Não inferir** semântica de coluna pelo nome; confirmar com os dados ou com o dono.

## Inputs
- Caminho do arquivo (parquet/CSV; Excel só se a extensão do DuckDB estiver disponível, senão converter p/ parquet antes).
- Contexto de negócio: o que **uma linha** deveria representar.

## Output
- Perfil no stdout (schema + stats + head).
- **Ficha da base** adicionada ao catálogo do projeto.

## Catálogo (registrar a ficha)
- **Tabela-resumo de várias bases de uma vez:** `python -X utf8 <skill>/scripts/catalog.py <dir1> <dir2>` *(ex.: `"raw inputs" "bases tratadas"`)* → markdown com linhas/#col/tamanho via metadados (instantâneo). Cole no catálogo do projeto.
- **Ficha por base** (template — preencher com o perfil do `explore.py`):
```markdown
### <base>.parquet
- **Grão:** <o que é 1 linha> · **Linhas:** <n> · **Tamanho:** <MB>
- **Produzida por:** <script> · **Consumida por:** <scripts/deck>
- **Chave de join:** <coluna(s)> (lembrar `UPPER(TRIM(...))` se for SKU/ID textual)
- **Âncoras:** <ex.: SUM(col)=X — conferir vs o ledger do projeto>
- **Gotchas:** <ex.: coluna aditiva; valor zerado; cash é taxa>
```

## references
Catálogo de bases **do projeto ativo** (nome varia; padrão Gradus *(ex.: `docs/CATALOGO_BASES.md`)*) — onde a ficha é
registrada. Se o projeto tiver um helper de conexão DuckDB *(ex.: `scripts/_lib.py` com `conn()`)*, pode usá-lo no lugar
de `duckdb.connect()` para herdar tuning de memória/threads/spill; o `explore.py` funciona sem ele.
