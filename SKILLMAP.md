# SKILLMAP — quando usar o quê

Mapa rápido de decisão entre as 5 skills da biblioteca. Cada uma resolve um momento
diferente do ciclo de análise; não se sobrepõem.

| Situação | Skill | Gatilho |
|---|---|---|
| Chegou uma **base nova** (parquet/CSV) e você precisa entender forma/grão/qualidade antes de analisar | **gradus-explore** | "o que tem nessa base?", "perfila isso", número surpreende e quer checar o dado por baixo |
| Dois números que **DEVERIAM bater não batem** (escada×escada, base antes×depois, deck antigo×novo, gabarito×base) | **gradus-metric-reconciliation** | "por que esses dois totais divergem?", "valida essa base reconstruída" |
| **Fim de bloco/sessão** — destilar a conversa em fatos pra próxima sessão não nascer cega | **gradus-session-handoff** | encerrando o trabalho, trocando de tema, contexto ficando longo (pré-compactação) |
| **Antes de entregar** um número/tabela/slide ao sócio ou cliente | **gradus-qa-checklist** | "pronto pra mandar?", gate leve pré-entrega |
| **Começar um projeto de análise complexo** — montar a frota de subagents + docs canônicos + harness (hooks/git/verificadores) | **gradus-analysis-setup** | comando explícito `/gradus-analysis-setup` (não dispara por contexto) |

## Fluxo típico

1. **Base nova** → `gradus-explore` (entende o dado).
2. Durante a análise, **número diverge** → `gradus-metric-reconciliation` (acha a causa, registra no ledger).
3. **Vai entregar** → `gradus-qa-checklist` (gate leve).
4. **Fecha a sessão** → `gradus-session-handoff` (distila fatos e aprendizados).

## O que NÃO é cada uma

- `gradus-explore` ≠ reconciliar fontes que divergem (isso é `gradus-metric-reconciliation`).
- `gradus-metric-reconciliation` ≠ explorar base nova, ≠ auditoria metodológica ampla, ≠ montar deck.
- `gradus-qa-checklist` ≠ auditoria metodológica profunda, ≠ revisão visual de PPTX, ≠ gate de render de deck/HTML.
- `gradus-session-handoff` ≠ injetar contexto no INÍCIO da sessão, ≠ escrever deck.
- `gradus-analysis-setup` ≠ rodar uma análise pontual (o dono faz direto), ≠ montar deck, ≠ dashboard; só provisiona o andaime/frota/harness, sob comando explícito.
