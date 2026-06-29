# -*- coding: utf-8 -*-
"""H1 path_guard (PreToolUse: Write/Edit) — só escrever DENTRO da pasta do projeto; raw inputs/ é imutável.
Lê o JSON do PreToolUse no stdin; emite permissionDecision=deny quando o alvo é proibido; senão sai 0 sem output."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]   # .claude/hooks/x.py -> raiz do projeto
RAW = (ROOT / "raw inputs").resolve()

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if data.get("tool_name") not in ("Write", "Edit", "NotebookEdit"):
        sys.exit(0)
    ti = data.get("tool_input") or {}
    fp = ti.get("file_path") or ti.get("notebook_path")
    if not fp:
        sys.exit(0)
    try:
        target = pathlib.Path(fp).resolve()
    except Exception:
        sys.exit(0)
    if ROOT != target and ROOT not in target.parents:
        deny(f"Fora da raiz do projeto ({ROOT.name}). O agente só escreve dentro da pasta.")
    if RAW == target or RAW in target.parents:
        deny("`raw inputs/` e imutavel (original do cliente / fonte). Nao sobrescrever.")
    sys.exit(0)

if __name__ == "__main__":
    main()
