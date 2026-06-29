# -*- coding: utf-8 -*-
"""H4 audit_log (PostToolUse: Write/Edit/Bash) — registra toda escrita/comando em docs/_audit.log (ts | tool | alvo).
'Trust traces, not scores': o traco auditavel do que o agente fez. Nunca bloqueia."""
import json, sys, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
LOG = ROOT / "docs" / "_audit.log"

def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = d.get("tool_name", "")
    if tool not in ("Write", "Edit", "NotebookEdit", "Bash"):
        sys.exit(0)
    ti = d.get("tool_input") or {}
    alvo = ti.get("file_path") or ti.get("notebook_path") or ti.get("command") or ""
    alvo = str(alvo).replace("\n", " ")[:200]
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')} | {tool} | {alvo}\n"
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    sys.exit(0)

if __name__ == "__main__":
    main()
