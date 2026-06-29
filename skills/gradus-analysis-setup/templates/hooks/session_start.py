# -*- coding: utf-8 -*-
"""H5 session_start (SessionStart) — injeta o que NAO esta no CLAUDE.md auto-carregado: as DECISOES recentes
(mudam toda hora) + o nudge de disciplina (consultar FONTE_DA_VERDADE antes de dar numero; catalogar base nova;
checar invariante ao augmentar). Travas do projeto -> CLAUDE.md; universais -> ~/.claude/CLAUDE.md.
Ataca a dor 'aba nova nasce cega' (PCS #4) sem duplicar o que o CLAUDE.md ja carrega."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]

def tail(rel, n):
    f = ROOT / rel
    if not f.exists():
        return f"(sem {rel})"
    return "\n".join(f.read_text(encoding="utf-8", errors="ignore").splitlines()[-n:])

ctx = (
    "HARNESS — disciplina do projeto: consulte docs/FONTE_DA_VERDADE.md ANTES de dar qualquer numero e registre "
    "numero novo la depois; caracterize base nova em docs/CATALOGO_BASES.md na 1a vez; ao augmentar uma base, rode "
    "scripts/_check_invariants.py (rowcount/totais nao podem mudar). "
    "(Travas do projeto: CLAUDE.md. Travas universais: ~/.claude/CLAUDE.md.)\n\n"
    f"DECISOES travadas recentes (docs/DECISOES.md — nao re-litigar):\n{tail('docs/DECISOES.md', 14)}"
)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}}))
