---
name: tcc-safe-tmux
description: Stop repeated macOS "tmux would like to access data from other apps" prompts for agent fleets that run inside tmux. Use when App Data prompts keep returning.
---
# TCC-safe tmux on macOS
## How to
1. Confirm one tmux binary on PATH and one server (`tmux ls`, `pgrep -x tmux`). Record the binary path and its code signature hash.
2. Pin the binary (e.g. `brew pin tmux`) so upgrades do not swap it silently.
3. Run the server from one launchd agent with a fixed socket, so every job has the same responsible process.
4. A human grants Full Disk Access to that pinned binary once (System Settings). Agents never edit TCC.
5. Health check: binary path + signature match baseline, one server, FDA state, prompt count per hour.
## Blockers and fixes log
- 2026-10-15: 26 prompts in 2 hours; Allow is stored per process and short-lived jobs are new processes. Fix: pinned binary + one host + one FDA grant.
