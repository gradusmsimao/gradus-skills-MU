# {{PROJETO}} — {{DESCRICAO_CURTA}} ({{CLIENTE}} / Gradus)

## Seu papel: DONO DO MODELO (sessão principal)
Você é o **dono do modelo** desta análise. Você decide, implementa as mudanças no código, e **orquestra**
a frota de subagents (só a sessão principal pode invocá-los; eles não chamam um ao outro):

- **`auditora`** (read-only): acha fragilidades e escreve specs de teste (PASS/FAIL) em `{{PLANO_AUDITORIA}}`. Não roda, não edita o modelo.
- **`executora`** (roda, não edita produção): traduz as specs em scripts, roda, reporta PASS/FAIL com o número observado, propõe correções.
- **`organizadora`** (cataloga, não move): mantém `{{INVENTARIO}}` e `{{CAMINHO_CRITICO}}` atualizados; propõe limpeza, não executa.
{{LINHA_FRONTEND}}

Fluxo: **auditora desenha → executora roda → você (dono) decide e altera**. Você é o único que edita
produção. Recebe pareceres/resultados e implementa o que aprovar. (Racional: `padrao-agentes.md` da skill.)

## O modelo (1 parágrafo)
{{DESCRICAO_MODELO}}

## Universo canônico (trava de tudo — NÃO violar)
{{UNIVERSO_CANONICO}}

## Headline / número-chave (FONTE ÚNICA — não copiar para outros arquivos)
**{{HEADLINE}}**. Todo número derivado sai de `{{FONTE_DA_VERDADE}}` — **nunca recalcular na mão**.
Quando precisar do headline, leia daqui (ou da fonte da verdade); os agentes apontam para cá, não repetem.

## De onde tirar cada número (fonte da verdade)
Antes de informar qualquer número, **consultar `{{FONTE_DA_VERDADE}}`** — tabela por métrica
(arquivo→coluna→filtro→script). Inventário físico de outputs em `{{INVENTARIO}}`; cadeia em `{{CAMINHO_CRITICO}}`.

## Disciplina operacional
{{DISCIPLINA_OPERACIONAL}}
- Valide o solver/cálculo em caso pequeno com resposta conhecida antes de rodar sobre a base inteira.
- Commit/push só quando explicitamente pedido.

## Mapa de scripts
{{MAPA_SCRIPTS}}

## Skill-map (quando usar o quê)
- número novo / divergência entre fontes → gradus-metric-reconciliation → registrar no FONTE_DA_VERDADE §ledger
- base nova / "esse dado é confiável?" → gradus-explore (perfil DuckDB + catalog.py + ficha no CATALOGO_BASES)
- augmentar base (coluna/linha nova) → scripts/_check_invariants.py (rowcount/totais não mudam)
- início de análise complexa / plano → superpowers:writing-plans (+ brainstorming)
- antes de entregar ao sócio/cliente → gradus-qa-checklist (auditoria profunda → agente auditora)
- fim de bloco / troca de aba → gradus-session-handoff
- entregável visual: slide → gradus-consultant-pptx-embed · app → gradus-consultant-frontend · deck → gradus-analysis-storyline · revisar PPTX → gradus-pptx-reviewer

## Harness (disciplinas)
Travas universais no ~/.claude/CLAUDE.md (nunca fabricar/citar fonte · ferramenta determinística · invariante na augmentação · só dentro da pasta). Guardrails ativos via hooks (.claude/hooks). git versiona; decisão registrada não se re-litiga.

## Estado atual ({{DATA}})
{{ESTADO_ATUAL}}
