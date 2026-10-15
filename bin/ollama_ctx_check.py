#!/usr/bin/env python3
"""ollama_ctx_check.py URL FILE... : compare resident context_length (URL/api/ps) with every "num_ctx": N found in FILEs.
A mismatch means Ollama will reload the model whenever that caller runs. Exit 1 on mismatch."""
import json, re, sys, urllib.request
if len(sys.argv) < 3: print(__doc__); sys.exit(64)
ps = json.load(urllib.request.urlopen(sys.argv[1].rstrip("/") + "/api/ps", timeout=8))
res = {m["name"]: m.get("context_length") for m in ps.get("models", [])}
sent = {f: sorted({int(n) for n in re.findall(r'"num_ctx"\s*:\s*(\d+)', open(f).read())}) for f in sys.argv[2:]}
bad = {f: [n for n in v if n not in res.values()] for f, v in sent.items() if any(n not in res.values() for n in v)}
print(json.dumps({"resident": res, "senders": sent, "mismatch": bad}, indent=1)); sys.exit(1 if bad else 0)
