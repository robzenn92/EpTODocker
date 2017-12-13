#!/usr/bin/env python3

import threading


class StabilityOracle(object):

    def __init__(self, ttl):
        self.lock = threading.Lock()
        self.logical_clock = 0
        self.ttl = ttl

    def is_deliverable(self, event):
        return event.ttl > self.ttl

    def get_clock(self):
        with self.lock:
            self.logical_clock += 1
            return self.logical_clock

    def update_clock(self, ts):
        with self.lock:
            if ts > self.logical_clock:
                self.logical_clock = ts
