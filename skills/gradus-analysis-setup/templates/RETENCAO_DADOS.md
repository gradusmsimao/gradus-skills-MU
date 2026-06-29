# Política de retenção de dados — {{PROJETO}}

> Evitar que versões "+1 coluna" de arquivos enormes compitam por espaço. Princípio geral (padrão Gradus).

## Regras
1. **Preservar o original do cliente** (imutável, em `raw inputs/`). Nunca sobrescrever (hook `path_guard` bloqueia).
2. **1 versão canônica por base.** Checkpoints intermediários **regeneráveis** NÃO se guardam como cópia full.
   - *(ex.: ao enriquecer uma base grande, apagar os checkpoints `_ORIGINAL` / `_PRE_xxx` regeneráveis depois de validar
     que o canônico está intacto — pode liberar muitos GB; sempre com OK do dono e registro no `DECISOES.md`.)*
3. **Coluna aditiva = sidecar, não nova cópia full.** Em vez de reescrever um parquet enorme para somar colunas,
   gravar um **sidecar** (chave + colunas novas) e juntar no read:
```python
# canônica + sidecar de enriquecimento (junta no read; não reescreve o arquivo enorme)
con.execute("""SELECT b.*, e.col_nova_1, e.col_nova_2
  FROM read_parquet('raw inputs/base_canonica.parquet') b
  LEFT JOIN read_parquet('raw inputs/base__enrich_<tema>.parquet') e USING (CHAVE)""")
```
   Nome do sidecar: `<base>__enrich_<tema>.parquet`.
4. **Outputs do pipeline são regeneráveis** → não versionar (gitignore dos dados pesados); a "memória" deles é a
   **ficha no `CATALOGO_BASES.md`** (grão/âncoras) + o script que os produz.
5. **Temporários** → disco local (`AppData/Local/Temp`), nunca no OneDrive (hook `path_length_guard` + N1).

## Antes de apagar/arquivar (checklist)
- [ ] É **regenerável**? (existe o script + input que o reconstrói — registrar o comando aqui)
- [ ] O **canônico** está intacto? (conferir rowcount/âncora vs `CATALOGO_BASES`)
- [ ] É **delete** → exige **OK explícito do dono** + registro no `DECISOES.md`.
- [ ] Preferir **arquivar** (mover p/ fora do OneDrive) a apagar, se o histórico tiver valor.

## Regeneração registrada
<!-- ex.: <base_canonica> <- upstream <fonte> via scripts/<gera>.py (+ scripts/enriquece_<tema>.py) -->
