# Guia — compartilhar e manter skills do Claude Code na Gradus

> Como cada consultor versiona suas skills num repo GitHub e como o time se conecta aos repos uns dos
> outros mantendo tudo atualizado. Validado contra as docs oficiais (https://code.claude.com/docs —
> `skills`, `plugins`, `plugin-marketplaces`, `settings`). **Confirme a sintaxe na sua versão** do Claude Code
> (`claude --version`); alguns campos são recentes (marcados como *v2.1.x+*).

## O modelo em 3 níveis (e o caminho de promoção)

| Nível | Para quê | Mecanismo | Auto-update |
|---|---|---|---|
| **0. Local (dev)** | skill SUA, em construção; editar e ver ao vivo | *junction/symlink* `~/.claude/skills/x` → seu clone git | — (é o seu working copy) |
| **1. Grassroots** | compartilhar ad-hoc com colegas | **seu repo vira um marketplace leve**; colega faz `/plugin marketplace add você/repo` | opcional (`autoUpdate`) |
| **2. Curado** | skills validadas pelo time de analytics | **marketplace central do time** referenciando os repos via `source: github` | recomendado (`autoUpdate:true`) |

Promoção natural: você prototipa no **nível 0** (junction) → publica no **nível 1** (seu marketplace) → quando
o analytics valida, ela é **promovida para o nível 2** (entra no marketplace central, sem você mover arquivo —
o central só passa a referenciar seu repo / uma versão pinada dele).

## Por que NÃO usar git-pull como mecanismo de compartilhamento

`git pull` + junction é manual, por-pessoa-por-repo e **sem** auto-update. Ele é ótimo como ferramenta de
**dev local da sua própria skill** (nível 0), mas ruim para *distribuir*. Para compartilhar, use marketplace
(níveis 1/2): o colega adiciona uma vez e recebe atualização nativa.

---

## Pré-requisitos (1x por máquina)

```bash
git --version            # git instalado
gh --version             # GitHub CLI (no Windows: winget install --id GitHub.cli)
gh auth login            # autentica no GitHub (browser) — habilita push e repos privados
claude --version         # Claude Code; veja se suporta /plugin (v2.1+)
```

---

## Parte 1 — Criar o SEU repo de skills

### 1.1 Estrutura de uma skill
Cada skill é uma **pasta** com um `SKILL.md` (obrigatório). Frontmatter mínimo:

```markdown
---
name: minha-skill
description: Uma linha clara do QUANDO usar — o Claude usa isto para auto-invocar.
---

# Minha skill
Instruções da skill...
```

Campos úteis (opcionais): `allowed-tools` (pré-aprova ferramentas), `disallowed-tools`,
`disable-model-invocation: true` (só você invoca, via `/minha-skill`), `argument-hint`, `model`.

### 1.2 Inicializar e subir
```bash
mkdir gradus-skills && cd gradus-skills
mkdir -p skills/minha-skill
# ... crie skills/minha-skill/SKILL.md ...
git init
printf '__pycache__/\n*.pyc\n.DS_Store\n' > .gitignore
git add . && git commit -m "skills iniciais"
gh repo create gradus-skills --private --source=. --remote=origin --push
```
Pronto: repo privado versionado. Daqui pra frente, **gerir = commitar**.

---

## Parte 2 — Nível 0: editar ao vivo (junction/symlink)

Para desenvolver a skill e vê-la valer **na hora** no Claude Code, aponte a pasta de skills do usuário
para o seu clone. O Claude Code descobre skills em `~/.claude/skills/<nome>/SKILL.md` automaticamente.

**Windows (junction de diretório não exige admin):**
```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\minha-skill" -Target "C:\caminho\gradus-skills\skills\minha-skill"
```
**macOS/Linux:**
```bash
ln -s /caminho/gradus-skills/skills/minha-skill ~/.claude/skills/minha-skill
```
Editar o `SKILL.md` no repo passa a valer na sessão atual (live change detection). Use isto só para as
**suas** skills em desenvolvimento — não como forma de receber as dos outros.

---

## Parte 3 — Nível 1: transformar o repo num marketplace (grassroots)

Para um colega consumir suas skills, seu repo precisa de **dois** arquivos JSON. As skills ficam dentro de
um "plugin"; o "marketplace" lista os plugins.

### 3.1 Layout
```
gradus-skills/
├── .claude-plugin/
│   └── marketplace.json          # lista os plugins do repo
└── plugins/
    └── minhas-skills/
        ├── .claude-plugin/
        │   └── plugin.json        # manifest do plugin
        └── skills/
            └── minha-skill/SKILL.md
```

### 3.2 `.claude-plugin/marketplace.json`
```json
{
  "name": "gradus-murilo",
  "description": "Skills do Murilo (analytics Gradus)",
  "owner": { "name": "Murilo Simão" },
  "plugins": [
    { "name": "minhas-skills", "source": "./plugins/minhas-skills",
      "description": "Pacote de skills de análise" }
  ]
}
```

### 3.3 `plugins/minhas-skills/.claude-plugin/plugin.json`
```json
{ "name": "minhas-skills", "description": "Skills de análise da Gradus", "version": "1.0.0" }
```

### 3.4 Validar e publicar
```bash
claude plugin validate .            # valida o marketplace.json / a estrutura
git add . && git commit -m "publica como marketplace" && git push
```

### 3.5 Um colega passa a usar (1x)
```bash
/plugin marketplace add gradusmsimao/gradus-skills      # owner/repo do GitHub
/plugin install minhas-skills@gradus-murilo             # instala o plugin
```
Atualizar quando você commitar algo novo:
```bash
/plugin marketplace update gradus-murilo
```

---

## Parte 4 — Nível 2: marketplace central do time (curado)

O time de analytics mantém **um** repo (ex.: `gradus/gradus-skills-marketplace`) cujo `marketplace.json`
**referencia o repo de cada consultor** via `source: github` — não copia arquivo. Skills validadas entram aqui.

### 4.1 `.claude-plugin/marketplace.json` do repo central
```json
{
  "name": "gradus",
  "description": "Skills validadas — analytics Gradus",
  "owner": { "name": "Analytics Gradus" },
  "plugins": [
    { "name": "murilo", "source": { "source": "github", "repo": "gradusmsimao/gradus-skills", "ref": "v1.0.0" } },
    { "name": "fulano", "source": { "source": "github", "repo": "fulano/skills" } }
  ]
}
```
`ref`/`sha` **pinam** uma versão (curadoria = versão estável, não o último commit de cada um).

### 4.2 Cada consultor adiciona só ESTE marketplace (1x)
```bash
/plugin marketplace add gradus/gradus-skills-marketplace
/plugin install murilo@gradus
```

### 4.3 Distribuição + auto-update via `settings.json`
Em `~/.claude/settings.json` (pessoal) ou no `.claude/settings.json` do projeto, o time pode pré-cadastrar o
marketplace e habilitar auto-update — aí ele é adicionado/atualizado sozinho:
```json
{
  "extraKnownMarketplaces": {
    "gradus": {
      "source": { "source": "github", "repo": "gradus/gradus-skills-marketplace" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "murilo@gradus": true }
}
```
> `autoUpdate` e o auto-install via `enabledPlugins` são recentes (*v2.1.150+*); confirme na sua versão.

### 4.4 Repos privados + auto-update no background
Interativo usa o seu `gh auth`. Para o **auto-update em background** de repo **privado**, exporte um token:
```bash
export GITHUB_TOKEN=ghp_xxx        # ou GH_TOKEN  (Windows: setx GITHUB_TOKEN ghp_xxx)
```

---

## Atualização — colinha de comandos

```bash
/plugin                              # UI: Discover | Installed | Marketplaces | Errors
/plugin marketplace list             # marketplaces conhecidos
/plugin marketplace update [nome]    # puxa as últimas versões (ou todos se omitir)
/plugin marketplace remove <nome>
/plugin install  <plugin>@<mktplace> [--scope user|project|local]
/plugin uninstall <plugin>@<mktplace>
/plugin enable | disable <plugin>@<mktplace>
/plugin list [--enabled|--disabled]
/plugin reload-plugins               # aplica mudanças sem reiniciar
```
Tudo também existe como CLI não-interativa: `claude plugin marketplace add ...`, `claude plugin install ...`.

## Precedência de descoberta (se houver nome repetido)
`enterprise (managed)` > `pessoal (~/.claude/skills)` > `projeto (.claude/skills)` > `plugin`.
Skills de plugin ficam com namespace (`<plugin>:<skill>`), então não colidem.

## Fluxo recomendado para a Gradus
1. **Prototipe** sua skill no nível 0 (junction) no seu `gradus-skills`.
2. **Publique** como marketplace (nível 1); colegas que quiserem fazem `/plugin marketplace add você/repo`.
3. Quando o analytics **validar**, a skill é **promovida** ao marketplace central (nível 2) com `ref` pinado +
   `autoUpdate` — e cai automaticamente para todo o time.

## Notas de integridade
- Os mecanismos acima são das docs oficiais; campos marcados *v2.1.x+* podem não existir em versões antigas.
- Não há auto-pull nativo para o caminho junction (nível 0) — é git manual, de propósito.
- A sintaxe de permissão granular por skill de marketplace (`Skill(<mktplace>:*)`) não está claramente
  documentada — valide antes de depender dela.
