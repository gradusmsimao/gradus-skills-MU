# Convenção de pastas & nomenclatura — {{PROJETO}}

> Contrato de **onde mora o quê** e **como nomear**, para a pasta se manter navegável. O princípio é geral
> (padrão Gradus); ajuste os nomes de diretório ao seu projeto.

## Contrato de diretórios (papel + regra)
| Diretório | Papel | Regra |
|---|---|---|
| `raw inputs/` | **Imutável** — original do cliente + fontes | **Só leitura.** Nada gerado vai pra cá. Escrita bloqueada por hook (`path_guard`). |
| `scripts/` | Pipeline + libs + utilitários (`_check_*`, `_catalogo_*`) | Código de produção. Versionado. |
| `bases tratadas/` | **Outputs canônicos do pipeline** (regeneráveis) | Carimbar por cenário/variante quando houver. Não versionar os dados pesados (gitignore). |
| `excel-outputs/` · `dashboards/` | **Entregáveis** (Excel, decks, embeds) | Decks `*.html` versionados; xlsx/pdf/embeds regeneráveis (gitignore). |
| `exploracoes/` | **Ad-hoc, com prazo** (script + saída efêmera de uma investigação) | Ciclo de vida (ver abaixo). Não é depósito permanente. |
| `docs/` | **Canônico** (FONTE_DA_VERDADE, CATALOGO_BASES, DECISOES, planos, metodologia) | Fonte da verdade. Versionado. |
| `tests/` | Regressão + testes de hooks/ferramentas | Versionado. |
| `.claude/` | Config do harness (settings, agents, hooks, skills) | Versionado (exceto `settings.local.json`). |

## Convenção de nomes
| Tipo | Padrão | Exemplo |
|---|---|---|
| Script de pipeline | `NN_descricao.py` (ordem) | (ex.: `06_motor.py`) |
| Script de exploração | `expl_<tema>.py` (tema claro) | (ex.: `expl_distribuicao_<tema>.py`) |
| Base/output | `<base>_<grão>[_<variante>].parquet` | (ex.: `motor_resultado.parquet`) |
| Embed p/ slide | `embed_<assunto>.html` | (ex.: `embed_<assunto>.html`) |
| Excel de slide | `slideNN_<assunto>.xlsx` ou `<assunto>.xlsx` | (ex.: `slide18_<assunto>.xlsx`) |
| Lib/utilitário interno | `_nome.py` (prefixo `_`) | `_lib.py`, `_check_invariants.py` |
| **Variante/cenário** | **sempre sufixo consistente** | (ex.: `_cenarioA` / `_cenarioB`) |

## Ciclo de vida de `exploracoes/`
A **organizadora** classifica cada item e **propõe** (nunca executa) ação; o dono decide:
- 🟢 **alimenta deck/docs** → manter; idealmente referenciado no `INVENTARIO_OUTPUTS`.
- 🟡 **reusável** (script genérico de inspeção) → manter; considerar promover a `scripts/`.
- ⚪ **órfão** (sem menção em docs/inventário, > 14 dias) → propor **arquivar/remover** (decisão do dono).

Detector read-only: `python -X utf8 docs/_check_organizacao.py` (lista órfãos + dados pesados duplicados).
