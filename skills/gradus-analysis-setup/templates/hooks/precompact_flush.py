# -*- coding: utf-8 -*-
"""H6 precompact_flush (PreCompact) — antes de o contexto ser resumido (~85%), lembra de persistir o que se perde:
big numbers no FONTE_DA_VERDADE e decisoes no DECISOES. Nao bloqueia. (PCS #5: 'se perde nos big numbers'.)"""
import json
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreCompact",
    "additionalContext": ("ANTES de compactar: garanta que todo big number novo esta em docs/FONTE_DA_VERDADE.md "
                          "(secao de numeros entregues) e toda decisao do dono em docs/DECISOES.md. "
                          "O que nao foi registrado se perde no resumo do contexto.")}}))
