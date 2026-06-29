# -*- coding: utf-8 -*-
"""H7 stop_gate (Stop/SubagentStop) — condicao de parada do loop autonomo (Ralph). SO atua em headless
(env CLAUDE_HEADLESS=1): se a tarefa nao sinalizou conclusao (docs/.ralph_done ausente), forca continuar.
No INTERATIVO fica SILENCIOSO de proposito (um lembrete a cada turno viraria ruido — licao 'hook vira ruido')."""
import json, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
DONE = ROOT / "docs" / ".ralph_done"
COUNT = ROOT / "docs" / ".ralph_count"
MAX = int(os.environ.get("CLAUDE_RALPH_MAX", "30"))

# interativo: silencioso (um lembrete a cada turno viraria ruido)
if os.environ.get("CLAUDE_HEADLESS") != "1":
    sys.exit(0)
# tarefa sinalizou conclusao: deixa parar
if DONE.exists():
    sys.exit(0)
# conta iteracoes; ao atingir o teto, PARA de bloquear (anti-loop-infinito)
try:
    n = int(COUNT.read_text(encoding="utf-8").strip()) if COUNT.exists() else 0
except Exception:
    n = 0
n += 1
try:
    COUNT.write_text(str(n), encoding="utf-8")
except Exception:
    pass
if n >= MAX:
    sys.exit(0)   # teto atingido: deixa a sessao parar (sem loop infinito)
print(json.dumps({"decision": "block",
    "reason": f"Tarefa nao concluida (docs/.ralph_done ausente; iteracao {n}/{MAX}). Execute o proximo passo "
              "pendente do TODO; crie docs/.ralph_done quando o verificador passar e o TODO estiver vazio."}))
sys.exit(0)
