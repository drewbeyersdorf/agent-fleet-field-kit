# agent-fleet-field-kit

Built for small businesses and independents.

Small, dependency-free tools and skills from running a multi-model AI agent fleet on a few local machines. Each one came from a real learning moment, written up problem/solution.

```json
{
  "for_agents": true,
  "tools": {
    "bin/ckpt": "resumable chunked jobs: init JOB ITEMS | next JOB | done JOB ITEM | status JOB (CKPT_HOME, default ./.ckpt)",
    "bin/lock_truth.py": "flock PATH | lease DIR -> free(0) | held(1) | dead(2); a lock file existing is not a lock held",
    "bin/signal_safe_lock.py": "mkdir lock that releases on SIGTERM/SIGHUP (Python skips finally on default SIGTERM)",
    "bin/ollama_ctx_check.py": "URL FILE... -> exit 1 if any caller's num_ctx differs from the resident model (causes reloads)",
    "bin/gpu_spill_check.sh": "[OLLAMA_URL] -> exit 1 if any loaded model is not 100% on GPU"
  },
  "skills": ["skills/lock-truth", "skills/checkpointed-orders", "skills/gpu-coexistence", "skills/ollama-ctx-consistency", "skills/tcc-safe-tmux"],
  "requires": ["python3", "sh", "curl (for the Ollama checks)"],
  "license": "AGPL-3.0-only"
}
```

## In plain English

- **ckpt**: break long agent jobs into small pieces and save progress after each one. If the job is killed or hits a rate limit, it picks up where it stopped instead of starting over.
- **lock_truth**: tells you if a lock is really held. A lock file sitting on disk is not proof that anyone holds it.
- **signal_safe_lock**: a lock that cleans up after itself even when the process is asked to stop.
- **ollama_ctx_check**: Ollama reloads a model whenever a caller asks for a different context size. This finds callers that disagree.
- **gpu_spill_check**: warns when a local model does not fit on the GPU and quietly runs on the CPU instead (much slower).
- **skills/**: short how-to guides (SKILL.md format) that agents and people can follow, each with a log of blockers and fixes.

## Try it

```sh
sh tests/test_tools.sh        # prints ALL_TESTS_PASS
printf 'step1\nstep2\n' > items.txt
bin/ckpt init demo items.txt
while i=$(bin/ckpt next demo); do echo "working on $i"; bin/ckpt done demo "$i"; done
```

## License

AGPL-3.0-only (see LICENSE). If you run a modified version as a network service, you share your changes. Built for small businesses and independents.
