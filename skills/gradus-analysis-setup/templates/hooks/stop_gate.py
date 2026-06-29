# -*- coding: utf-8 -*-
"""H7 stop_gate (Stop/SubagentStop) — condicao de parada do loop autonomo (Ralph). SO atua em headless
(env CLAUDE_HEADLESS=1): se a tarefa nao sinalizou conclusao (docs/.ralph_done ausente), forca continuar.
No INTERATIVO fica SILENCIOSO de proposito (um lembrete a cada turno viraria ruido — licao 'hook vira ruido')."""
import json, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
if os.environ.get("CLAUDE_HEADLESS") == "1" and not (ROOT / "docs" / ".ralph_done").exists():
    print(json.dumps({"decision": "block",
        "reason": "Tarefa nao concluida (docs/.ralph_done ausente). Execute o proximo passo pendente do TODO; "
                  "crie docs/.ralph_done quando o verificador passar e o TODO estiver vazio."}))
sys.exit(0)
