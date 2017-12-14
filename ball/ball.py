#!/usr/bin/env python3

import json
from event.event import Event


class Ball(set):

    def __init__(self):
        super(Ball, self).__init__()

    def increase_events_ttl(self) -> None:
        for event in self:
            event.increase_ttl()

    def is_empty(self) -> bool:
        return len(self) == 0

    def to_json(self):
        return json.loads(json.dumps(list(self), default=lambda o: o.to_json(), sort_keys=True))

    def add(self, event: Event) -> None:
        if isinstance(event, Event):
            super().add(event)
        else:
            raise TypeError

    def __str__(self) -> str:
        return str(list(self))

    __repr__ = __str__
