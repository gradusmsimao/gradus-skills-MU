# Fonte da verdade por campo/métrica — {{PROJETO}} ({{CLIENTE}})

> **Para quê:** quando alguém pede "me dá o número X", este doc diz **de qual arquivo, qual coluna, com
> qual filtro/agregação, e qual script** o número sai — para não tirar de base errada nem no grão errado.
> **É o único lugar onde o headline/número-chave mora** (junto com `CLAUDE.md`). Os agentes apontam para cá.
> Inventário físico completo: `{{INVENTARIO}}`.

> **Coluna `Proven.` (proveniência) — como cada número se mantém atualizado:** 🟢 `dd/mm` = derivado do
> motor, recalculável do parquet (entra no verificador `_check_fonte_verdade.py`); 🟡 `dd/mm` = conciliação
> manual, revalidar a cada marco; 🔵 `dd/mm` = fonte externa (cliente/contábil/gerencial/decisão de
> enquadramento), revalidar quando a fonte mudar. A **organizadora** lista linhas com data velha/sem
> proveniência como pendência; o dono confirma. **Todo número nasce com uma marca de proveniência.**

## ⚠️ Travas que valem para TODA métrica
{{TRAVAS_GLOBAIS}}
<!-- Ex.: grão = unidade agregada no período (nunca o grão fino); filtro X no HAVING e não no WHERE;
     universo canônico (totais); convenções de unidade (% vs absoluto). A preencher pelo dono/auditora. -->

---

## 1. Headline / número-chave (o número do projeto)

| Métrica | Valor atual | Arquivo | Coluna | Script | Proven. |
|---|---|---|---|---|---|
| **{{HEADLINE_METRICA}}** | **{{HEADLINE_VALOR}}** | `{{HEADLINE_ARQUIVO}}` | `<a preencher>` | `{{HEADLINE_SCRIPT}}` | 🟢 `<a conferir>` |
| <métrica derivada> | `<a preencher>` | `<a preencher>` | `<a preencher>` | `<a preencher>` | 🟢/🟡/🔵 |

> **Regra de ouro:** nunca recalcular o headline na mão — sair sempre de `{{HEADLINE_ARQUIVO}}`.

## 2. Universo / totais

| Métrica | Valor | Arquivo | Como | Script de ref. |
|---|---|---|---|---|
| <total 1> | `<a preencher>` | `<a preencher>` | `<a preencher>` | `<a preencher>` |

## 3. Demais métricas (uma seção por família de número)

<!-- Replicar o padrão da tabela acima para cada grupo de métricas do projeto.
     Preencher conforme as análises forem se consolidando. -->
