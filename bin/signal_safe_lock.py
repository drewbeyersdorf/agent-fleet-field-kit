#!/usr/bin/env python3
"""Pattern: an mkdir lock that is released even on SIGTERM/SIGHUP (Python skips finally on default SIGTERM).
Import and use:  with SignalSafeLock("/tmp/locks/seat-a"): do_work()"""
import os, signal, sys, time
def install_exit_on_signals():
    for s in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(s, lambda n, f: sys.exit(128 + n))
class SignalSafeLock:
    def __init__(self, path, wait=60): self.path, self.wait, self.owned = path, wait, False
    def __enter__(self):
        install_exit_on_signals(); os.makedirs(os.path.dirname(self.path), exist_ok=True); t0 = time.time()
        while True:
            try:
                os.mkdir(self.path); open(os.path.join(self.path, "owner"), "w").write(f"{os.getpid()} {time.time()}\n")
                self.owned = True; return self
            except FileExistsError:
                try: pid = int(open(os.path.join(self.path, "owner")).read().split()[0]); os.kill(pid, 0)
                except (ProcessLookupError, ValueError, FileNotFoundError, IndexError):
                    os.rename(self.path, f"{self.path}.stale.{int(time.time())}"); continue  # archive, never delete
                except PermissionError: pass
                if time.time() - t0 > self.wait: raise TimeoutError(self.path)
                time.sleep(1)
    def __exit__(self, *a):
        if self.owned: os.rename(self.path, f"{self.path}.released.{os.getpid()}.{int(time.time())}"); self.owned = False
