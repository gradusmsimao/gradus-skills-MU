# gradus-skills

Biblioteca de **skills de análise de dados da Gradus** — habilidades genéricas e portáveis
(não atadas a nenhum projeto específico) para serem usadas pelo Claude Code em qualquer
projeto de análise da Gradus. As skills cobrem o ciclo de trabalho com dados: explorar uma
base nova, reconciliar números que divergem, fechar uma sessão sem perder contexto, e checar
um entregável antes de mandar pro sócio/cliente.

Cada skill é uma pasta em `skills/` com um `SKILL.md` (frontmatter `name` + `description` que
o Claude Code lê para decidir quando acioná-la) e, quando precisa, uma subpasta `scripts/`.

## Skills

- **gradus-explore** — perfil/EDA inicial de uma base (parquet/CSV via DuckDB, out-of-core): schema, grão, qualidade, sem inundar o contexto. Inclui `scripts/explore.py` e `scripts/catalog.py`.
- **gradus-metric-reconciliation** — reconcilia uma métrica que diverge entre fontes e investiga a CAUSA, registrando o número reconciliado no ledger do projeto.
- **gradus-session-handoff** — ritual de fim de sessão: distila a conversa em FATOS, atualiza estado e captura aprendizados pra próxima sessão não nascer cega.
- **gradus-qa-checklist** — gate leve de qualidade antes de entregar um número/análise/slide (bate com o ledger? proveniência? premissas? grão/janela? sem dado fabricado?).

Para "quando usar o quê", ver [SKILLMAP.md](SKILLMAP.md).

## Instalação

Skills do Claude Code são descobertas em `~/.claude/skills/`. Para ativar estas skills
**globalmente** (em todos os projetos), basta copiar — ou linkar — as pastas de `skills/`
para lá.

Copiar:

```bash
cp -r skills/* ~/.claude/skills/
```

Ou linkar (symlink — mantém atualizado com o repo via `git pull`):

```bash
for d in skills/*/; do
  ln -s "$(pwd)/$d" "$HOME/.claude/skills/$(basename "$d")"
done
```

Depois é só reabrir o Claude Code; as skills aparecem na lista de skills disponíveis.

> Atenção a conflito de nome: se a mesma skill já existir num projeto (`<projeto>/.claude/skills/`),
> a versão do projeto tem precedência. Para usar a versão global, remova a cópia local do projeto.
