---
name: gradus-analysis-setup
description: Provisiona o andaime completo de um projeto de análise complexa da Gradus — a frota de subagents (auditora, executora, frontend, organizadora) MAIS os arquivos-base canônicos (CLAUDE.md estruturado, FONTE_DA_VERDADE, PLANO_AUDITORIA, INVENTÁRIO, CAMINHO_CRÍTICO), parametrizados por entrevista guiada. Também detecta e corrige drift de constantes em projetos já montados. ACIONE ESTA SKILL SOMENTE quando o consultor invocar explicitamente com o comando /gradus-analysis-setup. NÃO acione por inferência de contexto nem por palavras-chave no chat.
---

# Gradus Analysis Setup

Skill para **montar o andaime de uma análise complexa** no padrão que já provou funcionar no MAG001:
uma frota de subagents especializados (*orchestrator-workers*) **mais** os arquivos-base que são a fonte
da verdade que eles consomem. O produto é: `.claude/agents/*.md` (os workers) + `docs/*.md` (os
documentos canônicos) + o `CLAUDE.md` do projeto, todos parametrizados e coerentes entre si.

## Propósito

Replicar, em qualquer projeto de análise complexa, a arquitetura de agentes do MAG001 sem reescrever do
zero e **sem o drift de constantes** que apareceu lá (o headline copiado em 4 lugares, dessincronizado).
A skill resolve isso por design: gera um andaime onde o número-chave mora em **um só lugar**
(`CLAUDE.md` + `docs/FONTE_DA_VERDADE.md`) e os agentes **apontam** para a fonte em vez de repetir a
constante. O racional completo está em `references/padrao-agentes.md` (destilado de "Building Effective
Agents", Anthropic).

**Problema que resolve:** começar um projeto de análise novo com a frota certa e os documentos canônicos
no lugar; ou consertar um projeto existente cujos agentes ficaram desatualizados em relação ao CLAUDE.md.

## Quando usar

Acione **SOMENTE** com o comando explícito `/gradus-analysis-setup`. NÃO acionar por inferência de
contexto nem por palavras-chave ("agente", "auditoria", "organizar"). A invocação deve ser intencional.

## Quando NÃO usar (anti-gatilhos)

- Construir/evoluir um **deck de DO** → `gradus-analysis-storyline`.
- **Dashboard/ferramenta interativa** para o cliente → `gradus-consultant-frontend`.
- **Revisar PPTX** existente → `gradus-pptx-reviewer`.
- Rodar uma análise pontual ou um teste isolado → o dono faz direto, sem montar frota (princípio da
  simplicidade: só adicione agentes quando o trabalho se beneficia de especialização contínua).

## A frota que esta skill gera (papéis fixos)

| Agente | tools / disallowedTools | Faz | Não faz |
|---|---|---|---|
| **auditora** | Read,Grep,Glob,Write,WebSearch,WebFetch | desenha specs PASS/FAIL no PLANO_AUDITORIA | rodar, editar produção |
| **executora** | Read,Grep,Glob,Bash,Write · ~~Edit~~ | roda os testes, reporta nº observado vs alvo | editar produção |
| **frontend** | Read,Grep,Glob,Edit,Write,Bash | constrói + valida o deck/dashboard em headless | tocar pipeline/dados |
| **organizadora** | Read,Grep,Glob,Write · ~~Edit~~ | cataloga outputs + caminho crítico, propõe limpeza | mover/renomear/apagar |

O **dono** = a sessão principal (não é arquivo). Só o dono invoca os workers; subagents não chamam
subagents. As restrições de `tools` são **Poka-yoke**: o erro fica impossível, não só desencorajado.

## Modos de operação

Decida o modo no início. Se já existe `.claude/agents/` no projeto → **Modo B** (sincronizar); senão →
**Modo A** (setup novo).

### Modo A — Setup novo

1. **Confirme o diretório-alvo** (a raiz do projeto de análise; `.claude/agents/` e `docs/` ficam ali).
2. **Entrevista guiada** — colete via AskUserQuestion (uma pergunta por vez quando a resposta destrava a
   próxima). Se já existe um `CLAUDE.md` parcial, **leia-o primeiro** e só pergunte o que faltar:
   - **Projeto / cliente / descrição curta** do modelo.
   - **Número-chave (headline)** + unidade, e **de qual arquivo/coluna/script** ele sai.
   - **Universo canônico** — a "trava de tudo": filtros, grão, GROUP BY/HAVING, totais. (Cuidado com o
     grão fino vs agregado — o bug clássico do MAG001.)
   - **Scripts/etapas-chave** da cadeia (quem produz a fonte da verdade) e **pasta de outputs**.
   - **Stack** de execução (ex.: Python/DuckDB) e **disciplina operacional** crítica da máquina.
   - **Tem frontend/deck?** Se NÃO, **não gere `agente-frontend.md`** (simplicidade). Se sim: arquivo-alvo,
     padrão visual, onde ficam os dados agregados.
3. **Gere os arquivos** preenchendo os `{{PLACEHOLDERS}}` dos templates:
   - Agentes → `<projeto>/.claude/agents/{auditora,executora,organizadora}.md` (+ `frontend-designer.md` se houver deck).
   - Docs → `<projeto>/docs/{FONTE_DA_VERDADE,PLANO_AUDITORIA,INVENTARIO_OUTPUTS,CAMINHO_CRITICO}.md`.
   - `CLAUDE.md` → na raiz (se já existir, **proponha o merge**, não sobrescreva).
   - `references/padrao-agentes.md` → copie para `<projeto>/docs/` como referência do "porquê".
4. **Regra de ouro da geração:** **NÃO invente número.** Campo não informado fica como `<a preencher>`
   explícito. O headline entra SÓ no `CLAUDE.md` e no `FONTE_DA_VERDADE.md`; os agentes apontam para lá.
4b. **Provisiona o harness v2** (além da frota + docs):
   - `git init` + `.gitignore` (ignora dados pesados: raw inputs/, *.parquet, *.xlsx, *.pdf, *.csv, temporários, logs `_audit.log`/`_cost.log`, estado do Ralph `.ralph_done`/`.ralph_count`).
   - Copie `templates/hooks/*.py` → `<projeto>/.claude/hooks/` e registre-os no `<projeto>/.claude/settings.json` (use `templates/settings.json` como base do bloco `hooks`). São 8: path_guard, path_length_guard, destructive_guard (PreToolUse) · audit (PostToolUse) · session_start (SessionStart) · precompact_flush (PreCompact) · stop_gate (Stop) · cost_log (SessionEnd). Calibrados (sem falso-positivo de mensagem de commit; stop_gate silencioso no interativo — supera o caveat antigo do "hook Stop = ruído"; o stop_gate tem **teto** de iterações `CLAUDE_RALPH_MAX` p/ não entrar em loop infinito).
   - Gere os docs canônicos extras a partir dos templates: `docs/{DECISOES,CATALOGO_BASES,CONVENCAO_PASTAS,RETENCAO_DADOS}.md` + copie `_check_invariants.py` (scripts/) e `_check_organizacao.py` (docs/). **Modo headless:** `settings.headless.json` · `_ralph.py` (→ scripts/) · `MODO_HEADLESS.md` (→ docs/).
   - Adicione o **Skill-map** + o bloco **Harness** ao `CLAUDE.md` (já vêm no template de CLAUDE.md).
   - **Modo headless/Ralph** (execução autônoma, sem humano no loop): copie `templates/settings.headless.json` →
     `<projeto>/.claude/` (perfil mínimo: nega exec inline/push/install), `templates/_ralph.py` → `<projeto>/scripts/`
     (launcher: seta `CLAUDE_HEADLESS=1`, reseta o estado, chama `claude -p … --settings .claude/settings.headless.json`)
     e `templates/MODO_HEADLESS.md` → `<projeto>/docs/` (contrato de uso). A **parada do loop** já é o `stop_gate`
     instalado, com teto `CLAUDE_RALPH_MAX` (default 30) e conclusão via `docs/.ralph_done`. **Só ofereça** se o
     projeto tiver tarefas fechadas e verificáveis (port/execução determinística) — não p/ trabalho exploratório.

5. **Manutenção da fonte da verdade (anti-obsolescência).** O `FONTE_DA_VERDADE.md` gerado já traz a coluna
   **`Proven.`** (🟢 derivado do motor/recalculável · 🟡 conciliação manual · 🔵 externo: baseline
   contábil/gerencial em §0 "Perímetro & baselines"). **Ofereça gerar** um verificador
   `docs/_check_fonte_verdade.py` (espelhado do MAG001): recalcula os 🟢 do parquet do motor e dá PASS/FAIL
   contra o que o doc declara, avisando se o parquet ficou mais novo que o doc. Ele entra como teste
   determinístico (família A) da bateria da executora; os 🟡/🔵 a organizadora vigia (lista pendências). A
   regra "ao re-rodar o motor, rode o verificador" entra no `CLAUDE.md`.
   **Gatilho da organizadora (opcional):** ofereça também gerar `docs/_check_organizacao.py` — um detector
   read-only que conta outputs sem catálogo + pendências de proveniência + propaga o PASS/FAIL do verificador.
   **Default: rodar à mão** (`python -X utf8 docs/_check_organizacao.py`) quando o dono quiser um raio-x. Um
   **hook Stop** que dispara isso a cada turno é tecnicamente possível (no Windows, wrapper PowerShell que emite
   `hookSpecificOutput.additionalContext` só quando há drift), mas **vira ruído** se o projeto tiver pendências
   planejadas de longa duração (ex.: baselines `<a preencher>` que só entram depois) — o aviso repete todo turno
   sem ação. Só proponha o hook se o dono pedir explicitamente, e calibre o `--quiet` para não gritar pendências
   não-acionáveis. (Aprendizado MAG001, 10/jun: o hook foi removido por isso.)
6. **Verifique** (ver §Verificação) e **relate** o que foi criado, listando os `<a preencher>` que o dono
   ainda precisa fechar.

### Modo B — Sincronizar / corrigir drift

Para um projeto que já tem a frota (ou parte dela):

1. **Detecte drift:** identifique constantes de comunicação (o headline e os totais do universo) e
   procure-as (Grep) em `.claude/agents/*.md`, `CLAUDE.md`, `docs/*.md`. Reporte cada lugar onde o número
   aparece **literal** e onde diverge da fonte (`CLAUDE.md`/`FONTE_DA_VERDADE.md`).
2. **Proponha a correção** (não aplique sem OK do dono): trocar a constante inline pelo padrão
   *apontar-para-fonte* ("leia `CLAUDE.md §Universo canônico`"). Mostre o diff de cada agente.
3. **Complete a frota:** se faltar a `organizadora` (ou outro papel fixo), gere a partir do template,
   parametrizada pelo que já existe nos docs do projeto.
4. **Registre a frota** na seção de orquestração do `CLAUDE.md` (quem são os workers, o que cada um faz).

## Templates (em `templates/`)

`agente-auditora.md` · `agente-executora.md` · `agente-frontend.md` · `agente-organizadora.md` ·
`CLAUDE.md` · `FONTE_DA_VERDADE.md` · `PLANO_AUDITORIA.md` · `INVENTARIO_OUTPUTS.md` · `CAMINHO_CRITICO.md`.
**Harness v2 (novos):** `hooks/` (8 hooks .py genéricos: path_guard, path_length_guard, destructive_guard, audit,
session_start, precompact_flush, stop_gate, cost_log) · `settings.json` (bloco `hooks` que registra os 8) ·
`DECISOES.md` · `CATALOGO_BASES.md` · `CONVENCAO_PASTAS.md` · `RETENCAO_DADOS.md` · `_check_invariants.py` (scripts/) ·
`_check_organizacao.py` (docs/).

Cada placeholder `{{NOME}}` é substituído pelas respostas da entrevista. Placeholders comuns:
`{{PROJETO}}` `{{CLIENTE}}` `{{HEADLINE}}` `{{UNIVERSO_CANONICO}}` `{{SCRIPTS_CHAVE}}` `{{OUTPUTS}}`
`{{FONTE_DA_VERDADE}}` `{{PLANO_AUDITORIA}}` `{{INVENTARIO}}` `{{CAMINHO_CRITICO}}` `{{DIR_TESTES}}`
`{{STACK}}` `{{DISCIPLINA_OPERACIONAL}}` `{{DATA}}` `{{ESTADO_ATUAL}}` `{{MAPA_SCRIPTS}}`.
Os de frontend (`{{ARQUIVO_FRONTEND}}` `{{PADRAO_VISUAL}}` etc.) só se o projeto tiver deck.
A `{{LINHA_FRONTEND}}` do CLAUDE.md fica vazia se não houver frontend.

## Verificação (rodar antes de relatar "pronto")

1. **Frontmatter válido** em cada agente gerado: `name`, `description`, `tools`, e o `disallowedTools`
   correto (auditora sem Bash; executora e organizadora sem Edit).
2. **Anti-drift:** Grep pelo valor literal do headline nos agentes gerados → deve dar **zero** ocorrências
   (todos apontam para `CLAUDE.md`/`FONTE_DA_VERDADE.md`).
3. **Sem placeholder solto:** Grep por `{{` nos arquivos gerados → zero (todo placeholder foi substituído
   ou virou `<a preencher>` explícito).
4. **Sem número inventado:** todo campo não informado na entrevista está como `<a preencher>`, não como
   um valor chutado.
5. **Coerência da frota:** o `CLAUDE.md` lista exatamente os agentes que foram gerados (frontend só se
   houver deck).
6. **Harness v2 instalado** (Modo A): os 8 hooks estão em `<projeto>/.claude/hooks/`, registrados no
   `settings.json` (bloco `hooks`); os 4 docs extras (`DECISOES`, `CATALOGO_BASES`, `CONVENCAO_PASTAS`,
   `RETENCAO_DADOS`) existem em `docs/`; `_check_invariants.py` em `scripts/`; `_check_organizacao.py` em `docs/`;
   e o `CLAUDE.md` traz o **Skill-map** + o bloco **Harness**.
7. **Modo headless** (Modo A, se ofertado): `.claude/settings.headless.json`, `scripts/_ralph.py` e
   `docs/MODO_HEADLESS.md` existem; o `stop_gate.py` instalado tem o teto `CLAUDE_RALPH_MAX` (grep confirma).
