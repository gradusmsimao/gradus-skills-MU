# Modo Headless / Ralph loop — {{PROJETO}}

> Execução **autônoma** (sem humano no loop) de uma tarefa fechada e verificável. Padrão "Ralph": a sessão
> repete iterações até **sinalizar conclusão** (`docs/.ralph_done`) ou bater o **teto** de iterações.
> Para trabalho exploratório/ambíguo → use o modo interativo normal. Headless é p/ tarefa **determinística**.

## Os dois modos

| | Interativo (default) | Headless / Ralph |
|---|---|---|
| Quem decide o próximo passo | o dono (você) | a própria sessão, em loop |
| `CLAUDE_HEADLESS` | `0`/ausente | `1` |
| Perfil de permissão | `.claude/settings.json` | `.claude/settings.headless.json` (mais apertado) |
| Exec inline (`python -c`) | liberada (inspeção com humano) | **negada** (destructive_guard + deny) |
| `git push` / install | gated (pede OK) | **negado** |
| Parada | quando o dono encerra | hook `stop_gate` (ver abaixo) |

## Como rodar

Da **raiz do projeto** (nunca prefixe `cd`):

```bash
python -X utf8 scripts/_ralph.py "tarefa fechada em uma linha"
python -X utf8 scripts/_ralph.py --file docs/tarefa_ralph.md      # tarefa longa em arquivo
CLAUDE_RALPH_MAX=10 python -X utf8 scripts/_ralph.py "tarefa"      # teto menor (default 30)
python -X utf8 scripts/_ralph.py --dry-run "tarefa"               # só mostra o comando
```

O launcher (`scripts/_ralph.py`): seta `CLAUDE_HEADLESS=1`, **reseta** `docs/.ralph_done` e
`docs/.ralph_count`, e chama `claude -p "<tarefa>" --settings .claude/settings.headless.json`.

## O contrato de parada (hook `stop_gate.py`, Stop/SubagentStop)

Só atua quando `CLAUDE_HEADLESS=1`. A cada tentativa de parar:
1. Se `docs/.ralph_done` existe → **deixa parar** (tarefa concluída).
2. Senão, incrementa `docs/.ralph_count`. Se `count >= CLAUDE_RALPH_MAX` → **deixa parar** (anti-loop-infinito).
3. Senão → **bloqueia** a parada e devolve a instrução de executar o próximo passo pendente.

**A sessão autônoma DEVE criar `docs/.ralph_done`** (arquivo vazio) quando: o verificador
(`docs/_check_fonte_verdade.py` / `tests/`) passar **e** o TODO estiver vazio. Esse é o sinal de "acabei".

No **interativo** o `stop_gate` fica silencioso (um lembrete a cada turno viraria ruído — lição "hook vira ruído").

## Tarefa boa para headless (checklist)

- [ ] **Fechada e verificável**: existe um teste/verificador que dá PASS/FAIL inequívoco.
- [ ] **Determinística**: o caminho é execução/port, não decisão de modelagem (essas o dono trava antes).
- [ ] **Dentro da pasta**: não precisa de push/install/rede nem de tocar dados imutáveis (ex.: `raw inputs/`).
- [ ] **Critério de done explícito** no prompt: "termine criando `docs/.ralph_done` quando `tests/...` passar".

Exemplo de prompt (adapte ao seu pipeline): *"Rode `{{SCRIPT_RUNNER}}` para o cenário X; concilie as âncoras
com `docs/FONTE_DA_VERDADE.md` via `docs/_check_fonte_verdade.py`; se PASS e sem pendência, crie `docs/.ralph_done`.
Se algum passo falhar, corrija e tente de novo até o teto."*

## Depois de uma rodada autônoma (sempre)

- `git diff` — revise toda alteração de código antes de aceitar.
- `docs/_audit.log` — o que foi escrito/rodado (PostToolUse registra tudo).
- `docs/_cost.log` — tokens/modelo da sessão (SessionEnd).
- Mantenha as travas pesadas do projeto (ex.: "1 job pesado por vez") válidas **também** em headless.

## Travas que continuam ativas em headless (defesa em profundidade)

`path_guard` (não escreve fora da pasta; não sobrescreve dados imutáveis) · `path_length_guard` (≤255, sem
temp no OneDrive) · `destructive_guard` (rm -rf/reset --hard/push --force/clean… + **veta exec inline**) ·
`audit` · `session_start` · `cost_log`. O perfil headless ainda **nega** explicitamente `python -c`,
`git push`, `pip/npm install`.
