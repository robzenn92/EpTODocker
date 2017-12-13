#!/usr/bin/env python3

import uuid
import random
import unittest
from ball.ball import Ball
from event.event import Event


class Helpers(object):

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


class TestBall(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.ball = Ball()

    def test_empty_ball_should_be_empty(self):
        self.assertTrue(self.ball.is_empty())

    def test_non_empty_ball_should_not_be_empty(self):
        self.ball = Helpers.generate_non_empty_ball(3)
        self.assertFalse(self.ball.is_empty())

    def test_empty_ball_to_string(self):
        self.assertEqual(str(self.ball), "[]")

    def test_non_empty_ball_to_string(self):
        pass

    def test_ball_increase_events_ttl(self):
        self.ball = Helpers.generate_non_empty_ball(3)
        events = list(self.ball)
        ttl = [event.ttl for event in events]
        for i in range(len(events)):
            self.assertEqual(events[i].ttl, ttl[i])
        self.ball.increase_events_ttl()
        for i in range(len(events)):
            self.assertEqual(events[i].ttl, ttl[i] + 1)

    def test_add_different_events_to_ball(self):
        e1 = Event("source")
        self.ball.add(e1)
        e2 = Event("source")
        self.ball.add(e2)
        self.assertEqual(len(self.ball), 2)

    # def test_to_json(self):
    #     self.ball = Helpers.generate_non_empty_ball(3)
    #     print(self.ball.to_json())

if __name__ == '__main__':
    unittest.main()
