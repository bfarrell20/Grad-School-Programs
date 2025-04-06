#!/usr/bin/env python3

import sys
import time
import hyperloglog

# Initialize HyperLogLog with error rate ~1% (~1KB memory usage)
hll = hyperloglog.HyperLogLog(0.01)

# Track time
start_time = time.time()
interval = 1  # seconds between measurements
next_tick = start_time + interval

# Optional: for logging (to create a graph later if desired)
log = []

print("Elapsed(s)\tEstimated Unique Users", flush=True)

try:
    for line in sys.stdin:
        try:
            user, query, timestamp = line.strip().split('\t')
        except ValueError:
            continue  # skip malformed lines

        hll.add(user)

        now = time.time()
        if now >= next_tick:
            elapsed = int(now - start_time)
            est_count = len(hll)
            print(f"{elapsed}\t{est_count}", flush=True)
            log.append((elapsed, est_count))
            next_tick += interval

except KeyboardInterrupt:
    print("Streaming stopped by user.")
    sys.exit(0)
