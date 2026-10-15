---
name: lock-truth
description: Decide whether a file or directory lock is really held, and make lock holders release on the way out. Use when a lock "looks stale" or lock folders pile up as .stale.
---
# Lock truth
## How to
1. Never judge a lock by a file's presence. Identify the lock type: flock sentinel (a file you open and flock), mkdir lease (a directory with an owner file), or pidfile.
2. flock: try a non-blocking exclusive flock (`python3 -c "import fcntl;f=open(P,'a');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)"`). Success = free. Release immediately.
3. mkdir lease: read the owner pid and expiry. Held only if the pid is alive AND the lease is not expired.
4. If dead: archive (rename to .stale.<epoch>), never delete.
5. In every lock holder: convert SIGTERM and SIGHUP to SystemExit so `finally: release()` runs. SIGKILL can never be caught; keep a TTL for that case.
6. Count archived stale locks per day; a rising count means holders are dying.
## Blockers and fixes log
- 2026-10-15: a flock sentinel file reported as a stale lock. It is a flock sentinel and is meant to exist. Fix: test the flock, not the file.
- 2026-10-15: seat locks left behind after SIGTERM. Fix: signal handlers raising SystemExit; verified with a temp lock dir.
