#!/bin/bash
# Runs the headless benchmark N times (default 4) and prints the minimum per event, since other work shares the machine.
N=${1:-4}; for i in $(seq $N); do node test/bench.js 2>/dev/null | tail -1; done | python3 -c "
import sys,json
r=[json.loads(l) for l in sys.stdin]
print({k:round(min(x[k] for x in r),2) for k in r[0]})"
