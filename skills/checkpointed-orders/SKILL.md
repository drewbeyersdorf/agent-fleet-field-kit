---
name: checkpointed-orders
description: Split any long agent job into resumable chunks with a durable checkpoint, so a kill or rate limit costs one chunk. Use for any job longer than one tool call.
---
# Checkpointed orders
## How to
1. Write the chunk list first (one line per chunk, each 15 minutes or less).
2. `ckpt init JOB items.txt` once; it is a no-op if the job already exists (resume).
3. Loop: `item=$(ckpt next JOB) || break`; do the work; write output to a file; `ckpt done JOB "$item"`.
4. Run the loop in tmux (`tmux new-session -d -s JOB "loop > log 2>&1"`), never with a bare `&` from an agent shell.
5. On restart, run the same command; it continues at the first undone chunk.
## Blockers and fixes log
- 2026-10-15: monolithic executor runs lost all progress on rate limits. Fix: ckpt + rule in the worker standing order.
- 2026-10-15: background jobs started with `&` died with the agent's shell call. Fix: tmux.
