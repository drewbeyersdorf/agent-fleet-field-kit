---
name: gpu-coexistence
description: Keep vLLM and Ollama from fighting over one GPU. Use before loading any Ollama model on a GPU that also runs vLLM, or when local inference is suddenly slow.
---
# GPU coexistence (vLLM + Ollama)
## How to
1. Measure free VRAM after vLLM: `nvidia-smi --query-gpu=memory.used,memory.total --format=csv`.
2. `ollama ps` shows PROCESSOR (e.g. "18%/82% CPU/GPU"). Anything not 100% GPU is spilling.
3. Rule: never load an Ollama model larger than the free VRAM. Route heavy prompts to the vLLM OpenAI-compatible endpoint instead.
4. Alert when a model has less than half its weights on GPU, and measure tokens per second, not just "it answered".
5. If you need both, cap vLLM with `--gpu-memory-utilization` and size Ollama models to the remainder.
## Blockers and fixes log
- 2026-10-15: a 54 GB Ollama model got 9.8 GB of GPU next to vLLM and ran around 7 tok/s with 90-120 s timeouts. Fix: route to vLLM; spill check in health.
