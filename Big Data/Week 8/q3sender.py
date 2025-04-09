#!/usr/bin/env python3

"""Quiz6Q3Sender.py"""

import importlib
import os
import sys

from click_gen import *
max_evs = 6000         # Total number of events that will be generated.
                       # If you want to make it run forever, set this number to like a million

n_senders = 3000          # Number of senders
n_queries = 60         # How many different queries (or messages) a sender can send

dispatcher = Dispatcher()
sender_names = shuffle(['sndr%04d' % i for i in range(n_senders)])

class Sender:
   senders = [dispatcher.add_sender(Sender(sender_name, n_queries, 2, 2)) for sender_name in sender_names]


for ev in dispatcher.launch():
    print(ev, flush=True)
    max_evs -= 1
    if max_evs == 0:
        break