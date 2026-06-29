---
name: gradus-qa-checklist
description: >-
  Gate LEVE de qualidade ANTES de entregar um número/análise/slide ao sócio ou cliente, em projetos Gradus.
  Use logo antes de mandar um entregável (número, tabela, deck, dashboard) para conferir o essencial:
  número bate com o ledger? proveniência citada? premissas explícitas? grão/janela corretos? sem dado
  fabricado? É uma verificação rápida pré-entrega — NÃO é auditoria metodológica profunda (use a auditora),
  nem revisão visual de PPTX (use gradus-pptx-reviewer), nem o gate de render de deck/HTML (frontend).
---

# QA pré-entrega (Gradus · leve)

Última conferência antes de algo chegar ao sócio/cliente. **Rápido e de superfície** — pega o erro bobo que
queima credibilidade. Auditoria pesada (fragilidades estatísticas/econômicas) é da **auditora**, não aqui.

> **Genérica** (qualquer projeto). Confere contra os docs canônicos do projeto ativo (ver `references`).

## Quando usar · quando NÃO usar
- **Usar:** "vou mandar isso pro sócio/cliente"; fechar um número/tabela/slide/dashboard.
- **NÃO usar:** crítica metodológica/teste de robustez → **auditora**; padrão visual de PPTX → **gradus-pptx-reviewer**; render/overflow de HTML → **frontend**.

## Checklist (rodar todos; reportar PASS/FAIL com evidência)
1. **Número bate com o ledger?** Cada número do entregável existe em `FONTE_DA_VERDADE` (ou foi registrado lá agora) com o mesmo valor. Divergência → parar e usar `gradus-metric-reconciliation`.
2. **Proveniência citada?** Todo número tem fonte rastreável (arquivo/coluna/filtro/script). Nada "de cabeça".
3. **Sem fabricação.** Nenhum dado/categoria inventado; o que não se sabe está marcado como "não consta", não preenchido por chute.
4. **Grão e janela corretos** (SKU vs SKU×dia; `>0` no HAVING não no WHERE; janela do projeto; `UPPER(TRIM)` nos joins).
5. **Premissas explícitas** e decisões coerentes com o `DECISOES` (não contradiz nada travado pelo dono).
6. **Dado parcial sinalizado.** Se a conclusão se apoia em recorte/amostra, o limite está dito.
7. **Consistência interna do entregável** — totais batem com a soma das partes; rótulos/unidades certos (R$ MM, %); 1P+3P = total; sinais (custo negativo) corretos.
8. **Mensagem ↔ dado.** O título/leitura corresponde ao que o número mostra (não exagera nem suaviza).

## Output
- Lista PASS/FAIL item a item, com a evidência (o valor/fonte conferido). Qualquer FAIL → **não entregar**; apontar o que corrigir e a skill/ação para corrigir.

## references
Docs canônicos do projeto ativo (padrão Gradus): ledger *(ex.: `docs/FONTE_DA_VERDADE.md`)* · decisões
*(ex.: `docs/DECISOES.md`)*. Para auditoria profunda, acionar a **auditora** (não esta skill).
