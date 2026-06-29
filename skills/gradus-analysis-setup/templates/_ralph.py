# -*- coding: utf-8 -*-
"""Launcher do MODO HEADLESS / Ralph loop (execucao autonoma, sem humano no loop).

O que faz, em ordem:
  1. Seta CLAUDE_HEADLESS=1  -> destructive_guard veta exec inline (python -c) e o stop_gate passa a atuar.
  2. Reseta o estado do loop -> apaga docs/.ralph_done e docs/.ralph_count (comeca limpo).
  3. Roda `claude -p "<tarefa>" --settings .claude/settings.headless.json` (perfil minimo/deterministico).

O loop em si e do harness: o hook Stop (stop_gate.py) BLOQUEIA a parada enquanto a tarefa nao sinalizou
conclusao (docs/.ralph_done ausente), ate o TETO de iteracoes (CLAUDE_RALPH_MAX, default 30) -> anti-loop-infinito.
A sessao autonoma DEVE criar docs/.ralph_done quando o verificador passar e o TODO estiver vazio.

Uso (da raiz do projeto):
    python -X utf8 scripts/_ralph.py "tarefa em uma linha"
    python -X utf8 scripts/_ralph.py --file caminho/da/tarefa.md
    CLAUDE_RALPH_MAX=10 python -X utf8 scripts/_ralph.py "tarefa"   # teto menor
    python -X utf8 scripts/_ralph.py --dry-run "tarefa"            # so mostra o comando, nao executa

Seguranca: NAO commita/empurra sozinho a menos que a tarefa peca; o perfil headless nega push/install/exec-inline.
Sempre revise o docs/_audit.log e `git diff` ao terminar uma rodada autonoma.
"""
import os, sys, subprocess, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
DONE = ROOT / "docs" / ".ralph_done"
COUNT = ROOT / "docs" / ".ralph_count"
SETTINGS = ROOT / ".claude" / "settings.headless.json"


def parse_args(argv):
    dry = False
    task = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--dry-run":
            dry = True
        elif a == "--file":
            i += 1
            task = pathlib.Path(argv[i]).read_text(encoding="utf-8")
        else:
            task = a
        i += 1
    return task, dry


def main():
    task, dry = parse_args(sys.argv[1:])
    if not task or not task.strip():
        print("uso: python -X utf8 scripts/_ralph.py \"tarefa\"  (ou --file tarefa.md)")
        return 2
    if not SETTINGS.exists():
        print(f"ERRO: nao achei o perfil headless em {SETTINGS}")
        return 2

    # 1) reseta o estado do loop (comeca limpo)
    for p in (DONE, COUNT):
        try:
            if p.exists():
                p.unlink()
        except Exception as e:
            print(f"aviso: nao consegui apagar {p.name}: {e}")

    # 2) ambiente headless
    env = dict(os.environ)
    env["CLAUDE_HEADLESS"] = "1"
    env.setdefault("CLAUDE_RALPH_MAX", "30")

    claude = shutil.which("claude") or "claude"
    cmd = [claude, "-p", task, "--settings", str(SETTINGS)]
    print(f"[ralph] CLAUDE_HEADLESS=1  CLAUDE_RALPH_MAX={env['CLAUDE_RALPH_MAX']}")
    print(f"[ralph] teto de iteracoes via stop_gate; conclusao via docs/.ralph_done")
    print(f"[ralph] cmd: {claude} -p \"{task[:80]}{'...' if len(task) > 80 else ''}\" --settings .claude/settings.headless.json")
    if dry:
        print("[ralph] --dry-run: nao executei.")
        return 0

    proc = subprocess.run(cmd, cwd=str(ROOT), env=env)
    print(f"\n[ralph] claude saiu com codigo {proc.returncode}.")
    print(f"[ralph] .ralph_done {'PRESENTE (tarefa sinalizou conclusao)' if DONE.exists() else 'AUSENTE (parou por teto ou erro)'}"
          f"  | iteracoes={COUNT.read_text(encoding='utf-8').strip() if COUNT.exists() else '0'}")
    print("[ralph] revise: git diff  +  docs/_audit.log  antes de aceitar a rodada.")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
