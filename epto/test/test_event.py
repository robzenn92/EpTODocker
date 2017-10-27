#!/usr/bin/env python2

import random
import unittest
import uuid
from epto.event import Event
from epto.test.helpers import Helpers


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.event = Helpers.generate_empty_event()

    def test_new_event(self):
        self.assertTrue(isinstance(self.event.event_id, long))
        self.assertIsNotNone(self.event.event_id)
        self.assertIsNotNone(self.event.source_id)
        self.assertEqual(self.event.ttl, 0)
        self.assertEqual(self.event.ts, 0)

    def test_different_events_should_not_be_equal(self):
        e1 = Event("source")
        e2 = Event("source")
        self.assertNotEqual(e1, e2)

    def test_different_events_should_not_have_the_same_id(self):
        e1 = Event("source")
        e2 = Event("source")
        self.assertNotEqual(e1.event_id, e2.event_id)

    def test_different_events_should_have_different_hash(self):
        e1 = Event("source")
        e2 = Event("source")
        self.assertNotEqual(e1.__hash__(), e2.__hash__())

    def test_new_event_given_attributes_values(self):
        initial_uuid = uuid.uuid4().int
        initial_source_id = "my new ip"
        initial_ts = random.randint(1, 10)
        initial_ttl = random.randint(1, 10)
        self.event = Event(initial_source_id, initial_uuid, initial_ttl, initial_ts)
        self.assertEqual(self.event.event_id, initial_uuid)
        self.assertEqual(self.event.source_id, initial_source_id)
        self.assertEqual(self.event.ttl, initial_ttl)
        self.assertEqual(self.event.ts, initial_ts)

    def test_new_event_to_string(self):
        self.assertEqual(str(self.event), "(" + str(self.event.event_id) + "," + self.event.source_id + ",0,0)")

    def test_new_event_increment_ttl(self):
        initial_ttl = random.randint(0, 10)
        self.event.ttl = initial_ttl
        self.assertEqual(self.event.ttl, initial_ttl)
        self.event.increase_ttl()
        self.assertEqual(self.event.ttl, initial_ttl + 1)

    def test_event_increment_should_not_affect_other_attributes(self):
        initial_uuid = uuid.uuid4().int
        initial_source_id = "my new ip"
        initial_ts = random.randint(1, 10)
        initial_ttl = random.randint(1, 10)
        self.event = Event(initial_source_id, initial_uuid, initial_ttl, initial_ts)
        self.event.increase_ttl()
        self.assertEqual(self.event.source_id, initial_source_id)
        self.assertEqual(self.event.event_id, initial_uuid)
        self.assertEqual(self.event.ts, initial_ts)
        self.assertEqual(self.event.ttl, initial_ttl + 1)


if __name__ == '__main__':
    unittest.main()
