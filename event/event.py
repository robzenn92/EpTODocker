#!/usr/bin/env python3
import json
import uuid
import ipaddress


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
    # However, it is used to check lt (e.g. e1 < e2).
    def __lt__(self, other):
        if self.ts < other.ts:
            return True
        elif self.ts == other.ts:
            ip_source = ipaddress.ip_address(self.source_id)
            ip_other = ipaddress.ip_address(other.source_id)
            return ip_source < ip_other
        else:
            return False

    # Allows to sort events by (ts, srcId)
    # This is used only for sorting purposes, is not used to check equality (or inequality) e.g. e1 == e2 (or e1 != e2)
    # However, it is used to check gt (e.g. e1 > e2).
    def __gt__(self, other):
        if self.ts > other.ts:
            return True
        elif self.ts == other.ts:
            ip_source = ipaddress.ip_address(self.source_id)
            ip_other = ipaddress.ip_address(other.source_id)
            return ip_source > ip_other
        else:
            return False

    @classmethod
    def from_dict(cls, a_dict):
        event_id = int(a_dict['event_id'])
        source_id = str(a_dict['source_id'])
        ttl = int(a_dict['ttl'])
        ts = int(a_dict['ts'])
        return cls(source_id, event_id, ttl, ts)

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True))

    def __str__(self):
        letters = [chr(letter).upper() for letter in range(ord('a'), ord('z')+1)]
        ip = str(ipaddress.ip_address(self.source_id))
        return str(letters[list(map(int, ip.split('.')))[-1] % len(letters)]) + str(self.ts) + ' (' + ip + ', ts=' + str(self.ts) + ', ttl=' + str(self.ttl) + ')'

    __repr__ = __str__
