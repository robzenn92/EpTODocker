#!/usr/bin/env python2

import uuid


class Event(object):

    def __init__(self, source_id, event_id=None, ttl=0, ts=0):
        self.event_id = uuid.uuid4().int if event_id is None else event_id
        self.source_id = source_id
        self.ttl = ttl
        self.ts = ts #LogicalCLock(source_id)

    def increase_ttl(self):
        self.ttl += 1

    # # todo: has to be atomic!
    # def increase_ts(self):
    #     self.ts += 1

    def __hash__(self):
        return hash(self.event_id)

    def __eq__(self, other):
        return self.event_id == other.event_id

    def __cmp__(self, other):
        if self.event_id < other.event_id:
            return -1
        elif self.event_id == other.event_id:
            return 0
        else:
            return 1

    @classmethod
    def from_dict(cls, a_dict):
        event_id = long(a_dict['event_id'])
        source_id = str(a_dict['source_id'])
        ttl = int(a_dict['ttl'])
        ts = int(a_dict['ts'])
        return cls(source_id, event_id, ttl, ts)

    def __str__(self):
        return '(' + str(self.event_id) + ',' + str(self.source_id) + ',' + str(self.ttl) + ',' + str(self.ts) + ')'

    __repr__ = __str__
