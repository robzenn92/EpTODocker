#!/usr/bin/env python3

import random
import unittest
import uuid
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


class TestEvent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.event = Helpers.generate_empty_event()

    def test_new_event(self):
        self.assertTrue(isinstance(self.event.event_id, int))
        self.assertIsNotNone(self.event.event_id)
        self.assertIsNotNone(self.event.source_id)
        self.assertEqual(self.event.ttl, 0)
        self.assertEqual(self.event.ts, 0)

    def test_new_event_with_data(self):
        self.assertIsNone(self.event.data)
        self.event.data = 'secret'
        self.assertIsNotNone(self.event.data)

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
        self.event = Event(initial_source_id, initial_uuid, None, initial_ttl, initial_ts)
        self.assertEqual(self.event.event_id, initial_uuid)
        self.assertEqual(self.event.source_id, initial_source_id)
        self.assertEqual(self.event.ttl, initial_ttl)
        self.assertEqual(self.event.ts, initial_ts)

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
        self.event = Event(initial_source_id, initial_uuid, None, initial_ttl, initial_ts)
        self.event.increase_ttl()
        self.assertEqual(self.event.source_id, initial_source_id)
        self.assertEqual(self.event.event_id, initial_uuid)
        self.assertEqual(self.event.ts, initial_ts)
        self.assertEqual(self.event.ttl, initial_ttl + 1)

    def test_events_comparision_with_different_ts(self):
        e1 = Helpers.generate_empty_event()
        e2 = Helpers.generate_empty_event()
        e1.ts = 3
        e2.ts = 4
        self.assertTrue(e1 < e2)
        e1.ts = 5
        e2.ts = 4
        self.assertTrue(e1 > e2)

    def test_events_comparision_with_same_ts_but_different_source_id(self):
        e1 = Event("172.0.0.9")
        e2 = Event("172.0.0.10")
        self.assertTrue(e1 < e2)


if __name__ == '__main__':
    unittest.main()
