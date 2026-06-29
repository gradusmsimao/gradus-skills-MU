---
name: gradus-session-handoff
description: >-
  Ritual de FIM de bloco/sessão num projeto de análise Gradus: distila a conversa em FATOS (não logs),
  atualiza o estado e captura aprendizados — para a próxima sessão (ou outra aba) não nascer cega. Use ao
  encerrar um bloco de trabalho, ao trocar de tema, antes de fechar a sessão, ou quando o contexto está
  ficando longo (pré-compactação). Distila: memória (fatos novos, SUBSTITUINDO os obsoletos), log de decisões,
  foco atual, e uma retrospectiva curta (o que funcionou / o que melhorar). NÃO é para injetar contexto no
  INÍCIO (isso é o hook SessionStart), nem para escrever deck (storyline).
---

# Handoff de sessão (Gradus)

Fecha o ciclo "explorar → registrar" preservando o que importa **como fatos curtos**, não como transcrição.
Princípio (PropMem): *é mais fácil lembrar uma lista curta de fatos do que uma longa de conversas.*

> **Genérica** (qualquer projeto). Os nomes de arquivo são padrão Gradus *(ex.: `docs/DECISOES.md`)*; o destino
> real vem das `references` do projeto ativo.

## Quando usar · quando NÃO usar
- **Usar:** fim de um bloco de trabalho; troca de tema; antes de fechar/compactar; "vou abrir outra aba".
- **NÃO usar:** início de sessão (o hook `SessionStart` já injeta o chão) ; transformar achado em slide → **gradus-analysis-storyline**.

## Processo (distilação)
1. **Big numbers novos →** registrar no **ledger de números** do projeto (métrica · valor · escopo · fonte/script · data · proveniência). *Antes de qualquer coisa* — é o que mais se perde.
2. **Decisões do dono →** anexar ao **log de decisões** (data · decisão · porquê). Não re-litigar depois.
3. **Memória de projeto →** gravar/atualizar **fatos** (1 fato por nota), **substituindo** os que ficaram obsoletos (não empilhar versões). Linkar fatos relacionados.
4. **Foco atual →** atualizar 1–2 linhas de "estado da rodada" (o que está feito, o que falta) no doc de handoff/estado.
5. **Retrospectiva curta →** 2–4 bullets *o que funcionou / o que melhorar* (inclui falsos-positivos, gotchas, retrabalho evitável). Aprendizado vira regra/skill se recorrente.
6. **Sanidade →** se o motor/bases mudaram, rodar o verificador do projeto antes de encerrar.

## Disciplina (N1)
- **Distilar fato, não copiar conversa.** Cada fato é curto, com proveniência, e **substitui** o obsoleto.
- **Não inventar** "progresso": registrar o que está verificado; o que ficou pela metade fica explícito no foco atual.
- Converter datas relativas em absolutas ("hoje" → a data).

## Inputs
- A conversa/bloco a distilar; os docs canônicos do projeto (ledger, decisões, memória, handoff/estado).

## Output
- Ledger, log de decisões, memória e "foco atual" atualizados + retrospectiva curta. Nada de novo arquivo por sessão.

## references
Docs canônicos **do projeto ativo** (padrão Gradus): ledger de números *(ex.: `docs/FONTE_DA_VERDADE.md`)* ·
log de decisões *(ex.: `docs/DECISOES.md`)* · catálogo de bases *(ex.: `docs/CATALOGO_BASES.md`)* · memória de
projeto (`~/.claude/projects/<proj>/memory/` + `MEMORY.md`) · doc de estado/handoff do projeto. O verificador do
projeto *(ex.: `docs/_check_fonte_verdade.py`)* se houver.
