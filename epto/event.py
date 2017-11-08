#!/usr/bin/env python2

import uuid


class Event(object):

    def __init__(self, source_id, event_id=None, ttl=0, ts=0):
        self.event_id = uuid.uuid4().int if event_id is None else event_id
        self.source_id = source_id
        self.ttl = ttl
        self.ts = ts

    # Increases the event's ttl by one
    def increase_ttl(self):
        self.ttl += 1

    # Allows to check if an event is already included in a set
    def __hash__(self):
        return hash(self.event_id)

    # Events are equal if they have the same event_id, does not matter other attributes
    # This is used e.g. (e1 == e2)
    def __eq__(self, other):
        return self.event_id == other.event_id

    # Events are not equal if they do not have the same event_id, does not matter other attributes
    # This is used e.g. (e1 != e2)
    def __ne__(self, other):
        return self.event_id != other.event_id

    # Allows to sort events by (ts, srcId)
    # This is used only for sorting purposes, is not used to check equality (or inequality) e.g. e1 == e2 (or e1 != e2)
    # However, it is used to check: lt, lte, gt, gte (e.g. e1 < e2 or e1 > e2) cause those methods are not defined.
    def __cmp__(self, other):
        cmp_ts = cmp(self.ts, other.ts)
        return cmp_ts if cmp_ts != 0 else cmp(map(int, self.source_id.split('.')), map(int, other.source_id.split('.')))

    @classmethod
    def from_dict(cls, a_dict):
        event_id = long(a_dict['event_id'])
        source_id = str(a_dict['source_id'])
        ttl = int(a_dict['ttl'])
        ts = int(a_dict['ts'])
        return cls(source_id, event_id, ttl, ts)

    def __str__(self):
        letters = [chr(letter).upper() for letter in range(ord('a'), ord('z')+1)]
        return str(letters[map(int, self.source_id.split('.'))[-1] % len(letters)]) + str(self.ts) + ' (' + str(self.source_id) + ', ts=' + str(self.ts) + ', ttl=' + str(self.ttl) + ')'

    __repr__ = __str__
