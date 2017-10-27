#!/usr/bin/env python2
import json
import uuid
import random
from epto.event import Event
from epto.ball import Ball


class Helpers(object):

    def __init__(self):
        pass

    @classmethod
    def generate_empty_event(cls):
        return Event("my ip")

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
        for i in range(event_count):
            ball.add(cls.generate_non_empty_event())
        assert len(ball) == event_count
        return ball
