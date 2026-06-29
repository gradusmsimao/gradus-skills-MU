# -*- coding: utf-8 -*-
"""H3 destructive_guard (PreToolUse: Bash) — duas travas:
  (1) SEMPRE: veta comandos destrutivos (rm -rf, reset --hard, push --force, clean -f, del /s, Remove-Item -Recurse).
  (2) SO EM HEADLESS (env CLAUDE_HEADLESS=1): veta execucao INLINE arbitraria (python -c, node -e, bash -c ...) —
      no autonomo nao ha humano p/ revisar codigo solto; use script versionado. No INTERATIVO a inline e liberada
      (e o idioma de inspecao do dia a dia; convenience que vale a pena com humano presente).
Casa o verbo SO em POSICAO DE COMANDO (inicio / apos ; & | newline) p/ nao disparar com o termo entre aspas."""
import json, sys, re, os
BOUND = r"(?:^|[\n;&|])\s*"   # inicio ou apos separador; NAO inclui '(' p/ nao casar dentro de heredoc/subshell
DESTRUTIVO = [
    BOUND + r"rm\s+-[a-z]*r[a-z]*f",          # rm -rf / -rfv ...
    BOUND + r"rm\s+-[a-z]*f[a-z]*r",          # rm -fr ...
    BOUND + r"rm\s+-r(?:\s|$)",               # rm -r
    BOUND + r"git\s+reset\s+--hard",
    BOUND + r"git\s+push\s+[^\n;&|]*--force",
    BOUND + r"git\s+clean\s+-[a-z]*f",
    BOUND + r"del\s+/[sq]",
    BOUND + r"Remove-Item\b[^\n;&|]*-Recurse",
]
INLINE_EXEC = [   # exec inline arbitraria (negada SO em headless)
    r"\bpython[0-9.]*\b[^\n;&|]*\s-c\b",
    r"\bnode\b[^\n;&|]*\s-e\b",
    r"\b(perl|ruby)\b[^\n;&|]*\s-e\b",
    r"\b(bash|sh|zsh)\s+-c\b",
]

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)

def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if d.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (d.get("tool_input") or {}).get("command", "") or ""
    if any(re.search(p, cmd, re.I) for p in DESTRUTIVO):
        deny("Comando destrutivo em posicao de comando. Em modo autonomo e bloqueado; no interativo, reescreva se for intencional.")
    if os.environ.get("CLAUDE_HEADLESS") == "1" and any(re.search(p, cmd, re.I) for p in INLINE_EXEC):
        deny("Execucao inline arbitraria (-c/-e) bloqueada em modo autonomo (headless). Use um script versionado em scripts/ ou exploracoes/.")
    sys.exit(0)

if __name__ == "__main__":
    main()
