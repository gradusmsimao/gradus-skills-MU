# Padrão de agentes para análise complexa (o "porquê")

> Destilado de "Building Effective Agents" (Anthropic, engineering) + a experiência do MAG001.
> Lido pelo SKILL.md e citado nos templates. É o racional que justifica cada decisão de design da frota.

## 1. A topologia: orchestrator-workers em estrela

A frota implementa o padrão **orchestrator-workers**:

- **Dono (sessão principal)** = o orquestrador. **Não é um arquivo de agente.** Decide, implementa as
  mudanças no código/modelo, e despacha os workers na ordem certa. É o único que edita produção.
- **Workers** (auditora, executora, frontend, organizadora) = especialistas com escopo MECE e prompt
  otimizado por papel (padrão *routing*).

**Regra de ouro da topologia:** subagents NÃO chamam subagents. Só o dono invoca workers. Isso mantém
a estrela (evita ciclos, recursão e custo descontrolado) e garante o human-in-the-loop no centro.

## 2. Poka-yoke: a permissão É a salvaguarda

Não basta escrever "por favor não edite produção". O artigo recomenda tornar o erro **impossível**, não
só desencorajado. Por isso cada papel restringe `tools`/`disallowedTools` no frontmatter:

| Papel | tools | disallowedTools | Por quê |
|---|---|---|---|
| auditora | Read, Grep, Glob, Write, WebSearch, WebFetch | (sem Bash, sem Edit) | desenha testes, não roda nem altera; Write só p/ o plano de auditoria |
| executora | Read, Grep, Glob, Bash, Write | Edit | roda testes e cria scripts de teste novos; **não reescreve produção** |
| frontend | Read, Grep, Glob, Edit, Write, Bash | — | constrói e valida o deck; precisa de Edit no HTML e Bash p/ headless |
| organizadora | Read, Grep, Glob, Write | Edit | **cataloga e propõe**; sem Edit e sem mover/apagar — "catalogar, não limpar" |

## 3. Blackboard: o estado vive em disco, não no contexto

Os workers compartilham estado por **arquivos versionados em `docs/`**, não passando contexto entre si:

- `PLANO_AUDITORIA.md` — blackboard da auditora→executora (specs PASS/FAIL).
- `FONTE_DA_VERDADE.md` — onde cada número mora (anti-drift).
- `INVENTARIO_OUTPUTS.md` / `CAMINHO_CRITICO.md` — domínio da organizadora.

Isso dá **transparência** (os planning steps ficam auditáveis) e permite retomar entre sessões.

## 4. Anti-drift: fonte da verdade ÚNICA

A falha clássica é copiar a constante de comunicação (o "headline") em vários lugares; quando o número
muda, os agentes ficam dessincronizados e contaminam uma auditoria.

**Regra:** o headline/universo/mapa de scripts moram em UM lugar (`CLAUDE.md §Universo canônico` +
`docs/FONTE_DA_VERDADE.md`). Os agentes **apontam** para a fonte, não repetem a constante. Divergência
entre doc e código É um achado, não algo a "consertar silenciosamente".

## 5. Human-in-the-loop nos checkpoints

O humano (dono) fica no ponto de maior alavancagem: a decisão de **mudar o modelo de produção**. Os
workers recomendam; o dono decide e aplica. Nenhum worker altera o que comunica o número sozinho.

## 6. Simplicidade: só a complexidade que se paga

- O agente **frontend só existe se o projeto tiver deck/dashboard.** Sem isso, não gere o arquivo.
- Nem todo pedido precisa de worker: tarefa simples e isolada o dono faz direto. Workers são para
  trabalho que se beneficia de especialização (ceticismo dedicado, QA reprodutível, organização contínua).
- Sandbox antes de escalar: validar em caso pequeno com resposta conhecida antes de rodar sobre a base
  inteira; nunca dois processos pesados de dados ao mesmo tempo numa máquina de analista.
