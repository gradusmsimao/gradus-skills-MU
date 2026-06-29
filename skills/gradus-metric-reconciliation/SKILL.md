---
name: gradus-metric-reconciliation
description: >-
  Reconcilia uma métrica que diverge entre fontes e investiga a CAUSA da diferença, em projetos de análise
  Gradus (dados em parquet/CSV/Excel via DuckDB, não warehouse SQL). Use quando dois números que DEVERIAM bater
  não batem — duas agregações/escadas, total de uma base antes×depois de re-rodar, número de deck antigo×novo,
  gabarito×base, uma fonte×outra — ou para validar uma base reconstruída. Encerra SEMPRE registrando o número
  reconciliado no ledger de números do projeto (com proveniência). NÃO use para explorar base nova (use
  gradus-explore / programmatic-eda), auditoria metodológica ampla (auditora), nem para montar deck (storyline).
---

# Reconciliação de métrica (Gradus · DuckDB)

Compara uma métrica entre 2+ fontes, localiza a divergência, **investiga a causa** e produz um veredito **com
proveniência** — encerrando com o registro no ledger de números do projeto, para a pergunta não voltar.

> **Esta skill é genérica** (qualquer projeto Gradus). Os nomes de base/coluna/filtro são **placeholders**; os
> exemplos marcados *(ex.: …)* são ilustrativos de um projeto específico e **não** devem ser assumidos. O que é
> específico do projeto vem das `references` (os docs canônicos daquele projeto), nunca hardcoded aqui.

## Quando usar · quando NÃO usar
- **Usar:** "esses dois números deveriam bater e não batem" (escada A × escada B; total de uma base antes × depois de re-rodar; headline antigo × novo; gabarito × base).
- **NÃO usar:** base nova a explorar → `gradus-explore`/`programmatic-eda`; crítica metodológica/fragilidades → **auditora**; transformar achado em slide → **gradus-analysis-storyline**.

## Contexto mínimo (pergunte só o que faltar)
1. **As 2+ fontes** (caminho do arquivo / nome da agregação).
2. **Definição da métrica em cada fonte** — coluna + filtro + grão. *(N1: nunca chutar; se não souber como a fonte calcula, abrir o script/coluna e ler. "Não consta" é resposta válida.)*
3. **Variância aceitável** (financeiro <0,1%; volume <2%) — e o que deveria ser exato.
4. **Janela temporal** a reconciliar.
5. **Chave de join** (se for além de comparar totais).

## Processo (DuckDB — não pandas; bases de análise costumam ter 10⁷–10⁸ linhas)
1. **Totais por fonte** (1 query cada). Use o helper de conexão do projeto se houver (`_lib.conn`), senão `duckdb.connect()`:
```python
import duckdb; con = duckdb.connect(); con.execute("SET enable_progress_bar=false")
def total(parquet, col, filtro=""):  # placeholders — substitua pela métrica real de cada fonte
    w = f"WHERE {filtro}" if filtro else ""
    return con.execute(f"SELECT SUM({col}) FROM read_parquet('{parquet}') {w}").fetchone()[0]
a = total("FONTE_A.parquet", "VALOR_A", "FILTRO_A")
b = total("FONTE_B.parquet", "VALOR_B", "FILTRO_B")
print(f"A={a:,.1f} | B={b:,.1f} | dif={a-b:,.1f} ({100*(a-b)/a:.2f}%)")
```
2. **Decompor a diferença por degrau** ("escada"): aplicar **um filtro de cada vez** e medir o quanto cada um tira. Um `CREATE TEMP TABLE` por degrau — **`ILIKE` encadeado vaza no DuckDB** (gotcha conhecido).
3. **Drill nos maiores gaps** (por categoria/dia/chave): `GROUP BY … ORDER BY abs(dif) DESC LIMIT 10`. Resumo head+tail, nunca dump.
4. **Classificar a causa** (checklist abaixo). 5. **Veredito** (qual número é o certo e por quê, ou "diferença esperada = X, causa Y"). 6. **Fechar** (registrar no ledger).

## Causas comuns (genéricas — confirme com dados, não assuma)
- **Fonte stale / não re-rodada** — conferir a data do arquivo vs o doc; re-rodar o produtor e re-medir. **Suspeite disto primeiro.** *(ex. real: um número de atribuição que ficou de uma versão anterior da base.)*
- **Filtro / escopo diferente** (um lado aplica um recorte que o outro não). *(ex.: filtro de canal numa escada GMV.)*
- **Janela temporal** (D+0 vs D+1; same-day vs ±N dias; períodos diferentes entre as fontes).
- **Metodologia dependente de parâmetro** (o número muda conforme o modelo/premissa escolhido). *(ex.: GMV por modelo de atribuição last/first/u.)*
- **Grão errado** — agregado vs linha; filtro `>0` no `WHERE` em vez de `HAVING` infla/deflaciona.
- **Normalização de chave** faltando num lado (`UPPER(TRIM(...))`) → universo infla.
- **Órfão de timing / definição de "sem-X"** (duas definições próximas que diferem por uma fatia pequena).
- **Splits não casados** (categorias/segmentos dobrados ou omitidos num dos lados).

## Saída + fechamento (obrigatório)
1. **Veredito curto:** "A=X, B=Y; a diferença Z é [causa]; o certo é W porque […]" — com a **fonte (arquivo/coluna/filtro/script)** de cada lado.
2. **Registrar no ledger de números do projeto** (ver `references`): linha com `métrica · resposta · escopo · fonte · data · proveniência`. Se o número entra em deck, anotar também no log de decisões.
3. Se uma fonte estava errada/stale: dizer **o que re-rodar** para corrigi-la.

> O fechamento (passo 2) é o que diferencia esta skill da genérica de mercado: **número reconciliado sem registro volta como pergunta repetida.**

## references
Carregar os docs canônicos **do projeto ativo** (nomes variam por projeto; padrão Gradus):
- **Ledger de números** — onde mora cada número + de que arquivo/coluna/script sai *(ex.: `docs/FONTE_DA_VERDADE.md`)*.
- **Catálogo de bases** — grão/colunas/âncoras/chave/gotchas de cada base *(ex.: `docs/CATALOGO_BASES.md`)*.
- **Log de decisões** — decisões travadas pelo dono *(ex.: `docs/DECISOES.md`)*.
Se o projeto não tiver esses docs, propor criá-los (é o que torna a reconciliação registrável).
