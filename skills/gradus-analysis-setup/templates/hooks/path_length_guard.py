# -*- coding: utf-8 -*-
"""H2 path_length_guard (PreToolUse: Write/Edit) — PCS #6: nao explodir OneDrive / estourar MAX_PATH do Windows.
Veta caminho longo (> LIMIT) ou temporario/intermediario gravado dentro do OneDrive (deve ir p/ disco local)."""
import json, sys
LIMIT = 255  # margem sob o MAX_PATH 260; base OneDrive ja ~190, entao 200 travava tudo

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)

def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if d.get("tool_name") not in ("Write", "Edit", "NotebookEdit"):
        sys.exit(0)
    fp = (d.get("tool_input") or {}).get("file_path") or ""
    if not fp:
        sys.exit(0)
    if len(str(fp)) > LIMIT:
        deny(f"Caminho longo ({len(fp)}>{LIMIT}). Encurte nome/pasta (risco de MAX_PATH no Windows).")
    low = str(fp).lower()
    if "onedrive" in low and any(t in low for t in ("_tmp", "_scratch", "_temp", "intermediate", "intermediario")):
        deny("Temporario/intermediario no OneDrive — grave em disco LOCAL (AppData/Local/Temp), nao no OneDrive.")
    sys.exit(0)

if __name__ == "__main__":
    main()
