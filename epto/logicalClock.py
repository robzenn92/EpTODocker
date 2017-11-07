#!/usr/bin/env python2


class LogicalClock(object):

    def __init__(self, ip, ttl, event_id=0):
        self.ip = ip
        self.ttl = ttl
        self.event_id = event_id

    def __gt__(self, other):
        return self.event_id > other.event_id
