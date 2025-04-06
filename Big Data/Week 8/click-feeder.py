#!/usr/bin/env python3

import random
import sys
import time

# Configuration: High number of users, low delay
NUM_USERS = 10000               # Total users to simulate
NUM_QUERIES = 100              # Unique queries each user might send
TOTAL_EVENTS = 10000000         # Total events to emit (set high for "infinite" effect)
MEAN_DELAY = 0.01              # Mean delay between events (seconds)
STD_DEV_DELAY = 0.003          # Standard deviation of delay

# Create list of user names and queries
user_ids = [f"user{str(i).zfill(5)}" for i in range(NUM_USERS)]
query_templates = [f"query_{i}" for i in range(NUM_QUERIES)]

# Emit events
for _ in range(TOTAL_EVENTS):
    user = random.choice(user_ids)
    query = random.choice(query_templates)
    timestamp = int(time.time())

    # Output format: <user>\t<query>\t<timestamp>
    print(f"{user}\t{query}\t{timestamp}", flush=True)

    # Control the delay between events
    delay = max(0, random.gauss(MEAN_DELAY, STD_DEV_DELAY))
    time.sleep(delay)
