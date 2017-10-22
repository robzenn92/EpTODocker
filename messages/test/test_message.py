#!/usr/bin/env python2

import json
import unittest
from messages.message import Message
from partialView.partialView import PartialView


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_new_message(self):

        list_of_something = ["this", "is", "something"]
        m = Message("source_ip", "destination_ip", list_of_something)

        self.assertEqual(m.source, "source_ip")
        self.assertEqual(m.destination, "destination_ip")
        self.assertEqual(m.data, list_of_something)

    def test_message_can_carry_partial_view(self):

        partial_view = PartialView("172.0.1.0")
        partial_view.add_peer_ip("172.0.1.1")
        partial_view.add_peer_ip("172.0.1.2")
        m = Message("source_ip", "destination_ip", partial_view)

        self.assertEqual(m.source, "source_ip")
        self.assertEqual(m.destination, "destination_ip")
        self.assertEqual(m.data, partial_view)

    def test_new_message_to_json(self):

        list_of_something = ["this", "is", "something"]
        m = Message("source_ip", "destination_ip", list_of_something)
        m_json = m.to_json()

        self.assertEqual(type(m_json), str)
        self.assertEqual(type(json.loads(m_json)), dict)


if __name__ == '__main__':
    unittest.main()
