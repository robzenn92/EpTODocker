#!/usr/bin/env python3

import json


class Ball(set):

    def __init__(self):
        super(Ball, self).__init__()

    def increase_events_ttl(self):
        for event in self:
            event.increase_ttl()

    def is_empty(self):
        return len(self) == 0

    def __str__(self):
        return str(list(self))

    def to_json(self):
        return json.loads(json.dumps(list(self), default=lambda o: o.to_json(), sort_keys=True))

    __repr__ = __str__
