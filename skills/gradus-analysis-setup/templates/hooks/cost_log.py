# -*- coding: utf-8 -*-
"""H8 cost_log (SessionEnd) — observabilidade de consumo: le o transcript da sessao e loga TOKENS (in/out/cache)
+ modelos usados em docs/_cost.log. NAO crava R$ (nao inventar preco; multiplique pela tabela vigente).
Defensivo: qualquer erro -> loga linha minima, nunca quebra a sessao."""
import json, sys, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
LOG = ROOT / "docs" / "_cost.log"

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tp = data.get("transcript_path")
    sid = str(data.get("session_id") or "")[:8]
    inp = out = cr = cw = msgs = 0
    models = set()
    if tp and pathlib.Path(tp).exists():
        try:
            for line in pathlib.Path(tp).read_text(encoding="utf-8", errors="ignore").splitlines():
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                m = rec.get("message") or {}
                u = m.get("usage") or {}
                if u:
                    inp += u.get("input_tokens", 0) or 0
                    out += u.get("output_tokens", 0) or 0
                    cr += u.get("cache_read_input_tokens", 0) or 0
                    cw += u.get("cache_creation_input_tokens", 0) or 0
                    if m.get("model"):
                        models.add(m["model"])
                    msgs += 1
        except Exception:
            pass
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    line = (f"{ts} | sess {sid} | msgs {msgs} | in {inp:,} | out {out:,} | "
            f"cache_r {cr:,} | cache_w {cw:,} | modelos: {','.join(sorted(models)) or '?'}\n")
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    sys.exit(0)

if __name__ == "__main__":
    main()
