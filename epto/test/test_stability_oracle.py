#!/usr/bin/env python2

import os
import unittest

from epto.event import Event
from epto.stabilityOracle import StabilityOracle


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.ip = "172.0.0.1"
        self.ttl = int(os.environ['TTL'])
        self.oracle = StabilityOracle(self.ttl)

    # A new oracle should have ttl equal to the given parameter and logical clock set to zero
    def test_new_oracle(self):
        self.assertEqual(self.oracle.ttl, self.ttl)
        self.assertEqual(self.oracle.logical_clock, 0)

    # Should increment logical_clock and return one
    def test_new_oracle_get_clock(self):
        self.assertEqual(self.oracle.logical_clock, 0)
        logical_clock = self.oracle.get_clock()
        self.assertEqual(logical_clock, 1)
        self.assertEqual(self.oracle.logical_clock, 1)

    def test_new_event_should_have_ts_equal_to_one(self):
        e = Event(self.ip, ts=self.oracle.get_clock())
        self.assertEqual(e.ts, 1)

    def test_new_event_should_not_be_deliverable(self):
        e = Event(self.ip, ts=self.oracle.get_clock())
        self.assertFalse(self.oracle.is_deliverable(e))

    def test_event_should_be_deliverable_if_its_ttl_greater_then_TTL(self):
        e = Event(self.ip, ts=self.oracle.get_clock(), ttl=self.ttl+1)
        self.assertTrue(self.oracle.is_deliverable(e))


if __name__ == '__main__':
    unittest.main()
