#!/usr/bin/env python2

import uuid
import random
from epto.event import Event
from epto.ball import Ball


class Helpers(object):

    def __init__(self):
        pass

    @classmethod
    def get_random_ip(cls):
        ips = ["172.0.1." + str(i) for i in range(40)]
        return random.choice(ips)

    @classmethod
    def generate_empty_event(cls):
        return Event(Helpers.get_random_ip())

    @classmethod
    def generate_non_empty_event(cls):
        event = cls.generate_empty_event()
        event.event_id = uuid.uuid4().int
        event.ts = random.randint(1, 10)
        event.ttl = random.randint(1, 10)
        return event

    @classmethod
    def generate_empty_ball(cls):
        return Ball()

    @classmethod
    def generate_non_empty_ball(cls, event_count):
        ball = cls.generate_empty_ball()
        # In order to generate a valid Ball..
        # I should avoid e.g. e1 = (172.0.1.36, ts=4, ttl=6), e2 = (172.0.1.36, ts=4, ttl=4)
        # This can't happen in real life due to lock however it can happen with random events.
        # Although events are different cause e1 != e2 due to different ids, they have the same ip and ts.
        while len(ball) < event_count:
            e = cls.generate_non_empty_event()
            contained = False
            for event in ball:
                if e.source_id == event.source_id and e.ts == event.ts:
                    contained = True
            if not contained:
                ball.add(e)

        assert len(ball) == event_count
        return ball
