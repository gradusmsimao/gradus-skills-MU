# Plano de auditoria e testes — {{PROJETO}} ({{CLIENTE}})

**Papel deste documento.** Especificação de testes desenhada pela *auditora*. Quem executa é a
*executora*; quem altera o modelo é o *dono*. Este doc define **o que testar, com que entrada, qual o
número-alvo e o critério de PASS/FAIL** — não contém o código de execução (a executora traduz cada spec
em script, em `{{DIR_TESTES}}`).

**Fonte da verdade.** Os outputs em `{{OUTPUTS}}` e os scripts `{{SCRIPTS_CHAVE}}`. O headline e o
universo canônico moram em `CLAUDE.md`/`{{FONTE_DA_VERDADE}}` — **não os copie aqui**. Quando narrativa
e código divergirem, **o teste reporta a divergência** (não assume que um dos dois está certo).

**Universo canônico** (trava de todos os testes): ver `CLAUDE.md §Universo canônico`. Qualquer teste
cujo universo não bata com aquilo é inválido antes de avaliar o resultado.

**Convenções.**
- **Severidade**: 🔴 bloqueante (invalida o número de comunicação) · 🟡 relevante (afeta robustez/defesa) · 🟢 documental.
- **PASS/FAIL** sempre com tolerância explícita. "≈" sem tolerância é proibido num teste.
- Cada teste declara se é **determinístico** (vira regressão) ou **exploratório** (alvo = faixa + decisão a tomar).

---

## Famílias (ajuste à natureza do modelo deste projeto)

| Família | O que cobre | Por quê |
|---|---|---|
| A — Invariantes & regressão | trava o que já está certo contra reincidência | — |
| B — Conciliação numérica do report | os números do report batem com os dados | — |
| C — {{FAMILIA_C}} | `<a preencher>` | — |
| D — Motor (otimalidade & factibilidade) | o solver acha o ótimo e respeita restrições | — |
| E — {{FAMILIA_E}} | `<a preencher>` | — |
| F — Robustez / sensibilidade | quanto o número move com premissas | separa número robusto de frágil |
| G — Fragilidades estruturais | causalidade, viés, temporalidade | objeções sem fix no código |

---

## A — Invariantes e regressão (🔴 em bloco)

> Determinísticos. Devem virar suíte que roda a cada mudança do modelo. Se algum falhar, **pare**.

### A1 — Conciliação de universo
- **Objetivo.** Garantir que o universo do modelo é o agregado correto (não o grão fino filtrado).
- **Entrada.** `<a preencher: arquivo>`.
- **Procedimento.** `<a preencher>`.
- **Alvo / PASS-FAIL.** `<a preencher: número-alvo ± tolerância>`.

<!-- Replicar o esqueleto de teste (ID · objetivo · entrada · procedimento · alvo/PASS-FAIL · severidade)
     para cada fragilidade que a auditora identificar. Este arquivo é o blackboard auditora→executora. -->
