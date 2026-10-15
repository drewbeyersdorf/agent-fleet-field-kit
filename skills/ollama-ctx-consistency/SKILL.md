---
name: ollama-ctx-consistency
description: Stop Ollama model reload churn caused by callers sending different num_ctx values. Use when a local model keeps reloading or first-token latency jumps.
---
# Ollama context consistency
## How to
1. Read the resident context: `curl -s HOST:11434/api/ps` -> `context_length` per model.
2. Find every caller that sets `num_ctx` (grep your dispatchers).
3. Send exactly the resident value, or create one alias per needed size with `PARAMETER num_ctx N` in a Modelfile, so each alias stays warm.
4. Add a health check that compares resident context with every hardcoded sender.
## Blockers and fixes log
- 2026-10-15: one dispatcher sent 16384 and another 32768 to the same model; each switch reloaded it. Fix: ctx-consistency check; balancer owner aligning values.
