#!/usr/bin/env python2

import unittest
from epto.ball import Ball
from epto.event import Event
from epto.test.helpers import Helpers


class TestStringMethods(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
