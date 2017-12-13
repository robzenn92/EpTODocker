#!/usr/bin/env python3

import json
import unittest

import os

from messages.message import Message
from partialView.partialView import PartialView


class TestMessage(unittest.TestCase):

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

        partial_view = PartialView("172.0.1.0")
        partial_view.add_peer_ip("172.0.1.1")
        partial_view.add_peer_ip("172.0.1.2")
        m = Message("source_ip", "destination_ip", partial_view)

        # Transform it into json
        json_path = os.path.join(os.path.dirname(__file__), "message.json")
        with open(json_path) as json_file:
            d = json.load(json_file)
            self.assertEqual(m.to_json(), d)
            json_file.close()


if __name__ == '__main__':
    unittest.main()
