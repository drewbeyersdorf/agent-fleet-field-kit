#!/bin/sh
set -e; cd "$(dirname "$0")/.."; T=$(mktemp -d)
printf 'a\nb\n' > $T/i; CKPT_HOME=$T/ck bin/ckpt init j $T/i; CKPT_HOME=$T/ck bin/ckpt done j a; [ "$(CKPT_HOME=$T/ck bin/ckpt next j)" = b ]
touch $T/f; [ "$(bin/lock_truth.py flock $T/f)" = free ]
mkdir $T/l; echo "999999 x" > $T/l/owner; bin/lock_truth.py lease $T/l || [ $? = 2 ]
python3 - "$T" <<'PY'
import os,sys,subprocess,time,signal
T=sys.argv[1]; code=f"import sys;sys.path.insert(0,'bin');from signal_safe_lock import SignalSafeLock as L\nwith L('{T}/locks/s'):\n  import time;time.sleep(30)"
p=subprocess.Popen([sys.executable,"-c",code]); time.sleep(1.5); p.send_signal(signal.SIGTERM); p.wait()
assert not os.path.isdir(f"{T}/locks/s"), "lock left behind"
PY
echo ALL_TESTS_PASS
