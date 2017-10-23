#!/usr/bin/env python2

import unittest
from cyclon.helpers import format_address, get_ip_from_address_string


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_format_address(self):
        self.assertEqual(format_address("172.0.1.2", 5000), "http://172.0.1.2:5000")

    def test_get_ip_from_address_string(self):
        address = format_address("172.0.1.2", 5000)
        self.assertEqual(get_ip_from_address_string(address), "172.0.1.2")
