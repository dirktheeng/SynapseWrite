#!/bin/bash
# Alternates two engine builds on the current network and prints the minimum times of each.
A=$1;B=$2;N=${3:-6}
for i in $(seq $N); do ENGINE=$A node test/bench.js 2>/dev/null|tail -1 >> /tmp/claude-0/cmp_a.$$; ENGINE=$B node test/bench.js 2>/dev/null|tail -1 >> /tmp/claude-0/cmp_b.$$; done
python3 - <<P
import json
for f in ('/tmp/claude-0/cmp_a.$$','/tmp/claude-0/cmp_b.$$'):
    r=[json.loads(l) for l in open(f)];print({k:round(min(x[k] for x in r),2) for k in r[0]})
P
rm -f /tmp/claude-0/cmp_a.$$ /tmp/claude-0/cmp_b.$$
