# gradus-analysis-setup — skill do Claude Code

Provisiona o **andaime de um projeto de análise complexa** da Gradus: uma frota de subagents
especializados + os arquivos-base canônicos que são a fonte da verdade deles, gerados por entrevista
guiada. Replica o padrão validado no MAG001 (Magalu / PLA) sem reescrever do zero, com **anti-drift por
design**.

> ⚠️ **É uma skill do Claude Code, NÃO do Claude Desktop/web.** Ela *age* no projeto (gera arquivos de
> agente, escreve docs, sugere scripts de verificação). No Desktop/mobile ela seria inerte — só funciona
> no Claude Code (CLI ou extensão de IDE), rodando na máquina do consultor, sobre uma pasta de projeto.

## Instalação

1. Descompacte a pasta `gradus-analysis-setup/` dentro do diretório de skills do seu usuário:
   - **Windows:** `C:\Users\<seu-usuário>\.claude\skills\`
   - (resultado esperado: `...\.claude\skills\gradus-analysis-setup\SKILL.md`)
2. Abra o Claude Code (ou, se já estava aberto, abra o menu `/skills` uma vez para reindexar; se não
   aparecer, reinicie a sessão).
3. Confirme: digite `/gradus` e veja `gradus-analysis-setup` no autocomplete.

## Uso

Invoque **explicitamente** com `/gradus-analysis-setup` (ela não dispara por contexto). A skill então:

- **Modo A — setup novo:** faz uma entrevista (projeto, número-chave/headline, universo canônico,
  scripts-chave, se há deck) e gera, na pasta do projeto:
  - `.claude/agents/` → `auditora`, `executora`, `organizadora` (+ `frontend-designer` se houver deck)
  - `docs/` → `FONTE_DA_VERDADE.md`, `PLANO_AUDITORIA.md`, `INVENTARIO_OUTPUTS.md`, `CAMINHO_CRITICO.md`
  - `CLAUDE.md` na raiz (propõe merge se já existir)
- **Modo B — sincronizar:** num projeto que já tem frota, detecta *drift de constantes* (o headline
  copiado em vários lugares e divergente) e propõe converter os agentes ao padrão "apontar-para-fonte".

**Regra de ouro:** a skill **não inventa número** — campo não informado fica como `<a preencher>`.

## A frota gerada (papéis fixos)

| Agente | Ferramentas | Faz | Não faz |
|---|---|---|---|
| **auditora** | Read/Grep/Glob/Write/Web | desenha specs de teste PASS/FAIL | rodar, editar produção |
| **executora** | +Bash, −Edit | roda os testes, reporta nº observado vs alvo | editar produção |
| **frontend-designer** | +Edit/Bash | constrói + valida o deck/dashboard em headless | tocar pipeline/dados |
| **organizadora** | Read/Grep/Glob/Write, −Edit | cataloga outputs + caminho crítico, propõe limpeza | mover/renomear/apagar; rodar scripts |

O **dono** = a sessão principal do Claude Code (não é um arquivo de agente). Só o dono invoca os workers;
subagents não chamam subagents. As restrições de ferramentas são **Poka-yoke** — o erro fica impossível,
não só desencorajado. O "porquê" do desenho está em `references/padrao-agentes.md` (destilado de
"Building Effective Agents", Anthropic).

## Anti-drift (o diferencial)

O número-chave (headline) e o universo canônico moram em **um só lugar** — `CLAUDE.md` +
`docs/FONTE_DA_VERDADE.md`. Os agentes **apontam** para a fonte; nunca repetem a constante. A skill ainda
oferece gerar dois verificadores (manuais, read-only):
- `docs/_check_fonte_verdade.py` — recalcula o headline do output do motor e dá PASS/FAIL contra o doc;
- `docs/_check_organizacao.py` — conta outputs sem catálogo + pendências de proveniência (gatilho da organizadora).

## Conteúdo do pacote

```
gradus-analysis-setup/
  SKILL.md                     # orquestra a entrevista + geração (Modo A/B)
  README.md                    # este arquivo
  references/padrao-agentes.md # princípios do artigo + decisões de design
  templates/                   # 9 templates com {{PLACEHOLDERS}}
    agente-{auditora,executora,frontend,organizadora}.md
    CLAUDE.md · FONTE_DA_VERDADE.md · PLANO_AUDITORIA.md
    INVENTARIO_OUTPUTS.md · CAMINHO_CRITICO.md
```

## Para a área de governança de skills

- **Dependências externas:** nenhuma. São arquivos Markdown + templates de texto.
- **Os scripts que ela *sugere gerar*** (`_check_*.py`) usam Python/DuckDB — presentes no projeto-alvo,
  não na skill.
- **Escopo seguro:** a skill só escreve dentro da pasta do projeto onde é invocada; os agentes que ela
  gera têm ferramentas restritas por papel (read-only onde deve ser).
