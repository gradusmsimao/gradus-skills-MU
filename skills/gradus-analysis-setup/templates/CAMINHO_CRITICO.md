# Caminho crítico — inputs → {{ALVO_CADEIA}} — {{PROJETO}} ({{CLIENTE}})

> Mantido pela **organizadora**. Cadeia de arquivos que sai dos inputs crus e chega ao
> {{ALVO_CADEIA}}, com o grão e o filtro de universo de cada etapa. **Atualizar quando alterar qualquer
> elo da cadeia.** Divergência entre este doc e o código É um achado — reportar, não corrigir em silêncio.

## 1. Cadeia (quem alimenta quem)

```
INPUTS (crus)
  <a preencher> ─► <script> ─► <output>            (grão)
  ...
  ── ramo PRINCIPAL ────────────────────────────────────────
  <fonte da verdade do modelo> ─► <motor> ─► <output do headline>   ★ FONTE DO MODELO

  ── ramos LATERAIS (não realimentam o modelo) ─────────────
  <a preencher>
```

## 2. Tabela input → output (caminho crítico até o modelo)

| # | script | lê | gera | grão saída | filtro de universo |
|---|---|---|---|---|---|
| 01 | `<a preencher>` | `<a preencher>` | `<a preencher>` | `<a preencher>` | `<a preencher>` |

## 3. Regras de integridade da cadeia
{{REGRAS_CADEIA}}
<!-- Ex.: "nunca substituir a base do motor por um derivado de ramo lateral"; "o filtro gmv>0 vai no
     HAVING, nunca no WHERE". Travas que protegem a cadeia de regressões conhecidas. -->
