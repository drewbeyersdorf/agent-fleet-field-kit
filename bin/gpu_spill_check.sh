#!/bin/sh
# gpu_spill_check.sh [OLLAMA_URL]: warn when any loaded Ollama model is not fully on GPU (spilling to CPU).
U=${1:-http://127.0.0.1:11434}
curl -s -m 8 "$U/api/ps" | python3 -c '
import json,sys
bad=0
for m in json.load(sys.stdin).get("models",[]):
    size, vram = m.get("size",0), m.get("size_vram",0)
    pct = 100*vram/size if size else 0
    print(f"{m[\"name\"]}: {pct:.0f}% on GPU"); bad |= pct < 100
sys.exit(1 if bad else 0)'
