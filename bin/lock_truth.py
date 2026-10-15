#!/usr/bin/env python3
"""lock_truth.py: is a lock really held? Usage:
  lock_truth.py flock PATH          -> free | held   (non-blocking flock test; the file existing means nothing)
  lock_truth.py lease DIR           -> free | held | dead (DIR/owner first token = pid, optional DIR/expires epoch)
Exit 0 = free, 1 = held, 2 = dead holder (archive it: rename to DIR.stale.<epoch>, never delete)."""
import fcntl, os, sys, time
def alive(pid):
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False
    except PermissionError: return True
def flock(path):
    with open(path, "a") as f:
        try: fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); fcntl.flock(f, fcntl.LOCK_UN); return "free", 0
        except BlockingIOError: return "held", 1
def lease(d):
    if not os.path.isdir(d): return "free", 0
    try: pid = int(open(os.path.join(d, "owner")).read().split()[0])
    except Exception: pid = 0
    exp = None
    try: exp = float(open(os.path.join(d, "expires")).read().strip())
    except Exception: pass
    if pid and alive(pid) and (exp is None or exp > time.time()): return "held", 1
    return "dead", 2
if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("flock", "lease"): print(__doc__); sys.exit(64)
    s, rc = (flock if sys.argv[1] == "flock" else lease)(sys.argv[2]); print(s); sys.exit(rc)
