"""Quiz6Q3Listener.py"""


import sys
import time
import math
import struct
from hashlib import sha1

# Predetermined threshold values for different precision values (p)
tresholdData = [ 10, 20, 40, 80, 220, 400, 900, 1800, 3100, 6500, 11500, 20000, 50000, 120000, 350000 ]

def bit_length(w):
    return w.bit_length()

def get_threshold(p):
    return tresholdData[p - 4]

def get_alpha(p):
    """Calculates the alpha parameter in the HyperLogLog algorithm. Alpha is a
    parameter for bias correction.
    https://medium.com/@meeusdylan/implementing-hyperloglog-in-go-ec88a3703a33
    """
    if not (4 <= p <= 16):
        raise ValueError("p=%d should be in range [4 : 16]" % p)

    if p == 4:
        return 0.673

    if p == 5:
        return 0.697

    if p == 6:
        return 0.709

    return 0.7213 / (1.0 + 1.079 / (1 << p))


def get_rho(w, max_width):
    rho = max_width - bit_length(w) + 1

    if rho <= 0:
        raise ValueError('w overflow')

    return rho


class HyperLogLog:
    """
    HyperLogLog is an algorithm for the count-distinct problem, approximating
    the number of distinct elements in a multiset. Uses significantly less
    memory, but can only approximate the cardinality.

    https://en.wikipedia.org/wiki/HyperLogLog
    """

    __slots__ = ('alpha', 'p', 'm', 'M')

    def __init__(self, error_rate):
        """
        Initialize HyperLogLog with the given error rate

            error_rate: float
                Desired error rate (between 0 and 1)
        """

        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate must be between 0 and 1.")

        # Calculate precision (p) based on desired error rate
        # error_rate = 1.04 / sqrt(m) where m = 2^p
        p = int(math.ceil(math.log((1.04 / error_rate) ** 2, 2)))

        self.alpha = get_alpha(p) # param for bias correction
        self.p = p # precision
        self.m = 1 << p
        self.M = [ 0 for i in range(self.m) ]

    def add(self, value):
        """ Add an item to the HyperLogLog

        Process:
        1. Hash the input value
        2. Use first p bits to determine register index (j)
        3. Use remaining bits to update the register value
        """

        # Convert input to bytes for hashing
        if isinstance(value, str):
            value = value.encode('utf-8')  # Encode strings (Unicode) to bytes
        elif not isinstance(value, bytes):
            value = bytes(value)

        x = struct.unpack('!Q', sha1(value).digest()[:8])[0]

        # Use first p bits for register index
        j = x & (self.m - 1)

        # Use remaining bits for the value
        w = x >> self.p

        # Update register with max value of current or new rho
        self.M[j] = max(self.M[j], get_rho(w, 64 - self.p))

    def update(self, *others):
        """ Merge multiple HyperLogLog counters. Takes maximum value for each
        register position.
        """

        for item in others:
            if self.m != item.m:
                raise ValueError('Counters precisions should be equal')

        self.M = [max(*items) for items in zip(*([ item.M for item in others ] + [ self.M ]))]

    def card(self):
        """Estimate cardinality using HyperLogLog algorithm
        """

        # count number of registers equal to 0
        V = self.M.count(0)

        H = self.m * math.log(self.m / float(V))
        return H


def process_stream():
    """Process input stream and estimate unique senders"""
    hll = HyperLogLog(0.01) # Initialize with 1% error rate
    count = 0
    start_time = time.time()
    last_print_time = start_time

    print("Starting HyperLogLog stream processing for unique senders...")
    print("Estimates will be printed every 50 events")

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break

            sender_and_query = line.split('sender ')[1:]
            sender_and_query = sender_and_query[0].split('said:')
            sender = sender_and_query[0].strip()

            # Only add sender to HLL
            hll.add(sender)

            count += 1
            current_time = time.time()

            if count % 50 == 0:
                elapsed_time = current_time - start_time
                rate = count / elapsed_time
                unique_senders = hll.card()

                print("\n=== HyperLogLog Statistics ===")
                print(f"Events processed: {count:,}")
                print(f"Estimated unique senders: {unique_senders:,}")
                print(f"Processing rate: {rate} events/second")
                print(f"Elapsed time: {elapsed_time} seconds")
                print("============================\n")

    except KeyboardInterrupt:
        final_time = time.time()
        elapsed_time = final_time - start_time
        rate = count / elapsed_time

        print("\n=== Final Statistics ===")
        print(f"Total events processed: {count:,}")
        print(f"Final estimate of unique senders: {hll.card():,}")
        print(f"Average processing rate: {rate:.2f} events/second")
        print(f"Total runtime: {elapsed_time:.2f} seconds")
        print("=====================")

if __name__ == "__main__":
    process_stream()