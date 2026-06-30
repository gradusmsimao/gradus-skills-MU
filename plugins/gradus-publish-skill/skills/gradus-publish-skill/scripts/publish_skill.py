# -*- coding: utf-8 -*-
"""publish_skill.py — publica/atualiza UMA skill no repo de marketplace (à la carte: 1 plugin por skill).
Embrulha a skill como plugin, registra no `.claude-plugin/marketplace.json`, valida com `claude plugin validate`,
commita, (push), e re-aponta o junction `~/.claude/skills/<nome>` para o repo (dev local segue valendo).

Uso (da raiz do repo de skills OU de qualquer lugar):
  python publish_skill.py <nome-skill> [--source DIR] [--repo DIR] [--no-push] [--dry-run]
Defaults: source = ~/.claude/skills/<nome> · repo = ~/gradus-skills · marketplace = o name já gravado no repo.

Casos:
  - NOVA skill (source é dir real fora do repo): copia p/ plugins/<nome>/skills/<nome>, cria plugin.json,
    registra no marketplace, valida, commit+push, re-aponta o junction p/ o repo.
  - ATUALIZAR (source já é o junction p/ o repo): pula a cópia (a edição já está no repo), re-valida, commit+push.
"""
import argparse, json, os, shutil, subprocess, sys, pathlib

HOME = pathlib.Path.home()
IS_WIN = os.name == "nt"


def parse_frontmatter(skill_md: pathlib.Path):
    """name + description do frontmatter YAML (description pode ser folded `>-`)."""
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"SKILL.md sem frontmatter YAML: {skill_md}")
    fm = []
    for l in lines[1:]:
        if l.strip() == "---":
            break
        fm.append(l)
    out = {}
    i = 0
    while i < len(fm):
        l = fm[i]
        if l.startswith("name:"):
            out["name"] = l.split(":", 1)[1].strip()
        elif l.startswith("description:"):
            rest = l.split(":", 1)[1].strip()
            if rest in (">", ">-", "|", "|-", ""):       # bloco: junta linhas indentadas seguintes
                buf = []
                j = i + 1
                while j < len(fm) and (fm[j].startswith((" ", "\t")) or not fm[j].strip()):
                    buf.append(fm[j].strip())
                    j += 1
                out["description"] = " ".join(x for x in buf if x)
                i = j - 1
            else:
                out["description"] = rest
        i += 1
    return out


def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")  # cmd usa cp850
    if check and r.returncode != 0:
        print(f"  ! falhou: {' '.join(cmd)}\n  stdout: {r.stdout}\n  stderr: {r.stderr}")
        raise SystemExit(r.returncode)
    return r


def repoint_junction(link: pathlib.Path, target: pathlib.Path):
    """re-aponta ~/.claude/skills/<nome> -> target (a pasta da skill no repo). Junction no Windows; symlink no resto."""
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        if IS_WIN:
            subprocess.run(["cmd", "/c", "rmdir", str(link)], capture_output=True, text=True, errors="replace")
        else:
            link.unlink() if link.is_symlink() else shutil.rmtree(link)
    if IS_WIN:
        run(["cmd", "/c", "mklink", "/J", str(link), str(target)])
    else:
        link.symlink_to(target, target_is_directory=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--source", default=None)
    ap.add_argument("--repo", default=str(HOME / "gradus-skills"))
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    name = a.name
    repo = pathlib.Path(a.repo).resolve()
    source = pathlib.Path(a.source).resolve() if a.source else (HOME / ".claude" / "skills" / name)
    plugin_dir = repo / "plugins" / name
    skills_dst = plugin_dir / "skills" / name
    junction = HOME / ".claude" / "skills" / name
    mkt = repo / ".claude-plugin" / "marketplace.json"

    if not (repo / ".claude-plugin").exists():
        raise SystemExit(f"repo de marketplace não encontrado em {repo} (falta .claude-plugin/)")
    # resolve a origem real (pode ser junction p/ o próprio repo = caso ATUALIZAR)
    src_real = source.resolve()
    skill_md = src_real / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md não encontrado em {src_real}")
    fm = parse_frontmatter(skill_md)
    desc = fm.get("description", "")
    is_update = (src_real == skills_dst.resolve()) or (repo in src_real.parents)

    print(f">> publish '{name}'  | repo={repo}")
    print(f"   source={src_real}  ({'ATUALIZAR (já no repo)' if is_update else 'NOVA (copiar)'})")
    print(f"   plugin -> {plugin_dir.relative_to(repo)}  | desc={desc[:70]}...")

    if a.dry_run:
        print("   [dry-run] não escrevi nada.")
        return 0

    # 1) copia os arquivos da skill p/ plugins/<nome>/skills/<nome> (só se for NOVA)
    if not is_update:
        skills_dst.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_real, skills_dst, dirs_exist_ok=True)
    # 2) plugin.json
    pj = plugin_dir / ".claude-plugin" / "plugin.json"
    pj.parent.mkdir(parents=True, exist_ok=True)
    pj.write_text(json.dumps({
        "name": name, "description": desc, "version": "1.0.0",
        "author": {"name": "Gradus", "email": "analytics@gradusconsultoria.com.br"},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 3) registra no marketplace.json (add/replace por name)
    m = json.loads(mkt.read_text(encoding="utf-8"))
    plugins = [p for p in m.get("plugins", []) if p.get("name") != name]
    plugins.append({"name": name, "source": f"./plugins/{name}", "description": desc, "version": "1.0.0"})
    m["plugins"] = sorted(plugins, key=lambda p: p["name"])
    mkt.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   marketplace: {len(plugins)} plugins")

    # 4) valida (claude é claude.CMD no Windows -> precisa de cmd /c p/ o subprocess achar)
    claude_cmd = (["cmd", "/c", "claude"] if IS_WIN else ["claude"]) + ["plugin", "validate", "."]
    v = run(claude_cmd, cwd=str(repo), check=False)
    if "passed" not in (v.stdout + v.stderr).lower():
        print(f"   ! validate NÃO passou:\n{v.stdout}\n{v.stderr}")
        raise SystemExit(1)
    print("   validate: passed ✓")

    # 5) git add + commit + push
    run(["git", "-C", str(repo), "add", "-A"])
    msg = f"publica/atualiza skill {name} no marketplace (a la carte)\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
    c = run(["git", "-C", str(repo), "-c", "core.autocrlf=true", "commit", "-q", "-m", msg], check=False)
    if c.returncode == 0:
        print("   commit ✓")
    else:
        print("   (nada a commitar / já commitado)")
    if not a.no_push:
        run(["git", "-C", str(repo), "push", "origin", "HEAD"])
        print("   push ✓")

    # 6) re-aponta o junction p/ o repo (dev local usa a cópia do repo)
    repoint_junction(junction, skills_dst)
    ok = (junction / "SKILL.md").exists()
    print(f"   junction {junction} -> repo  | SKILL.md visível: {ok}")
    print(f">> OK: '{name}' publicada." + ("" if a.no_push else " (pushed)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
