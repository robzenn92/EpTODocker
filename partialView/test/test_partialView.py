#!/usr/bin/env python2

import json
import os
import unittest
from partialView.partialView import PartialView, PodDescriptor


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.partialView = PartialView("172.0.1.0")
        self.descriptors = []
        self.ips = ["172.0.1.1", "172.0.1.2", "172.0.1.3", "172.0.1.4", "172.0.1.5"]
        for ip in self.ips:
            self.descriptors.append(PodDescriptor(ip))

    # PartialView.limit should be equal to VIEW_LIMIT
    def test_set_up_ok(self):
        self.assertEqual(self.partialView.limit, int(os.environ['VIEW_LIMIT']))

    # Initial partialView should be empty
    def test_initial_partial_view_empty(self):
        self.assertTrue(self.partialView.is_empty())
        self.assertEqual(self.partialView.size, 0)

    # Method add_peer should increment size
    def test_add_peer_increments_size(self):
        size = self.partialView.size
        self.partialView.add_peer(PodDescriptor("172.0.1.5"))
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))
        self.assertEqual(self.partialView.size, size + 1)

    # Method add_peer_ip should increment size
    def test_add_peer_ip_increments_size(self):
        size = self.partialView.size
        self.partialView.add_peer_ip("172.0.1.5")
        self.assertEqual(self.partialView.size, size + 1)

    # Initial age should be zero
    def test_initial_age_peer(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5"))
        self.assertEqual(self.partialView.peer_list[0].age, 0)

    # Initial age should be zero
    def test_initial_age_peer_ip(self):
        self.partialView.add_peer_ip("172.0.1.5")
        self.assertEqual(self.partialView.peer_list[0].age, 0)

    # Method get_peer_ip_list should return a list of ips
    def test_get_peer_ip_list_returns_ips(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        self.assertEqual(self.partialView.get_peer_ip_list(), self.ips[:self.partialView.limit])

    # Initial age should be zero
    def test_partial_view_size_limit(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        self.assertEqual(self.partialView.size, self.partialView.limit)
        self.assertTrue(self.partialView.is_full())

        for i in range(self.partialView.limit):
            self.assertEqual(self.partialView.peer_list[i].ip, self.ips[i])

    def test_contains_return_true_if_contained(self):
        for descr in self.descriptors:
            self.partialView.add_peer(descr)
        for descr in self.descriptors[:self.partialView.size]:
            self.assertTrue(self.partialView.contains(descr))
        for descr in self.descriptors[self.partialView.size:]:
            self.assertFalse(self.partialView.contains(descr))

    def test_contains_ip_return_true_if_contained(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        for ip in self.ips[:self.partialView.size]:
            self.assertTrue(self.partialView.contains_ip(ip))
        for ip in self.ips[self.partialView.size:]:
            self.assertFalse(self.partialView.contains_ip(ip))

    # Age should be incremented by one
    def test_increment(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 1))
        self.partialView.add_peer(PodDescriptor("172.0.1.7", 3))
        self.partialView.increment()
        self.assertEqual(self.partialView.peer_list[0].age, 2)
        self.assertEqual(self.partialView.peer_list[1].age, 4)

    # Sort should sort view by peer's age
    def test_sort(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(PodDescriptor("172.0.1.8", 1))
        self.partialView.sort()
        self.assertEqual(self.partialView.peer_list[0].ip, "172.0.1.8")
        self.assertEqual(self.partialView.peer_list[1].ip, "172.0.1.5")
        self.assertEqual(self.partialView.peer_list[2].ip, "172.0.1.4")

    # Merge views should keep only the younger peers
    def test_merge_views(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 1))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        p = PartialView("172.0.1.9")
        p.add_peer(PodDescriptor("172.0.1.3", 0))
        p.add_peer(PodDescriptor("172.0.1.2", 1))
        p.add_peer(PodDescriptor("172.0.1.1", 4))
        self.partialView.merge(p)
        self.assertEqual(self.partialView.peer_list[0].ip, "172.0.1.3")
        self.assertEqual(self.partialView.peer_list[1].ip, "172.0.1.6")
        self.assertEqual(self.partialView.peer_list[2].ip, "172.0.1.2")
        self.assertTrue((self.partialView.is_full()))
        self.assertEqual(self.partialView.size, self.partialView.limit)

    # Merge views should keep only the younger peers
    def test_merge_views_without_duplicates(self):

        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.assertEqual(self.partialView.size, 1)
        self.assertEqual(len(self.partialView.peer_list), self.partialView.size)

        p = PartialView("172.0.2.0")
        p.add_peer(PodDescriptor("172.0.1.8", 1))
        p.add_peer(PodDescriptor("172.0.1.7", 2))
        p.add_peer(PodDescriptor("172.0.1.6", 3))

        self.partialView.merge(p)
        self.assertTrue(self.partialView.is_full())
        self.assertEqual(self.partialView.size, 3)
        self.assertEqual(self.partialView.size, self.partialView.limit)

        self.assertTrue(self.partialView.contains_ip("172.0.1.8"))
        self.assertTrue(self.partialView.contains_ip("172.0.1.7"))
        self.assertTrue(self.partialView.contains_ip("172.0.1.5"))
        self.assertFalse(self.partialView.contains_ip("172.0.1.6"))

    # Merge views should keep only the younger peers and avoid duplicates
    def test_merge_views_with_duplicates(self):

        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.assertEqual(self.partialView.size, 1)
        self.assertEqual(len(self.partialView.peer_list), self.partialView.size)

        p = PartialView("172.0.2.0")
        p.add_peer(PodDescriptor("172.0.1.5", 1))
        p.add_peer(PodDescriptor("172.0.1.7", 2))
        p.add_peer(PodDescriptor("172.0.1.6", 3))

        self.partialView.merge(p)
        self.assertTrue(self.partialView.is_full())
        self.assertEqual(self.partialView.size, 3)
        self.assertEqual(self.partialView.size, self.partialView.limit)

        self.assertTrue(self.partialView.contains_ip("172.0.1.5"))
        self.assertTrue(self.partialView.contains_ip("172.0.1.7"))
        self.assertTrue(self.partialView.contains_ip("172.0.1.6"))
        self.assertEqual(self.partialView.get_peer_by_ip("172.0.1.5").age, 1)

    # Method get_oldest_peer should return the peer with the highest age
    def test_get_oldest_peer(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 1))
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        oldest = self.partialView.get_oldest_peer()
        self.assertEqual(oldest.ip, "172.0.1.5")

    def test_select_neighbors(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors(oldest)
        self.assertTrue(neighbors.size > 0)
        self.assertFalse(neighbors.contains(oldest))

    def test_select_k_neighbors(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        partialView = self.partialView.select_neighbors(size=2)
        self.assertEqual(partialView.size, 2)

    def test_empty_partial_view_to_json(self):
        jsonized = self.partialView.to_json()
        self.assertEqual(jsonized, json.dumps({"ip": "172.0.1.0", "limit": 3, "shuffle_length": 2, "peer_list": [], "size": 0}, sort_keys=True, indent=4))

    def test_unmarshal_partial_view(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        jsonized = json.loads(self.partialView.to_json())
        partialView = PartialView.from_dict(jsonized)
        self.assertIsInstance(partialView,PartialView)
        for peer in partialView.peer_list:
            self.assertIsInstance(peer, PodDescriptor)
        self.assertEqual(partialView.ip, self.partialView.ip)
        self.assertEqual(partialView.size, 3)
        self.assertEqual(partialView.limit, 3)

        for i in range(self.partialView.limit):
            self.assertEqual(partialView.peer_list[i].ip, self.descriptors[i].ip)
            self.assertEqual(partialView.peer_list[i].age, self.descriptors[i].age)

    # # Exchange views should keep only the younger peers
    # def test_exchange_views(self):
    #
    #     p1_ip = "172.0.1.0"
    #     p2_ip = "172.0.2.0"
    #
    #     p1 = PartialView(p1_ip, limit=4)
    #     p1.add_peer(PodDescriptor("172.0.1.6", 0))
    #     p1.add_peer(PodDescriptor("172.0.1.4", 2))
    #     p1.add_peer(PodDescriptor("172.0.1.14", 4))
    #     p1.add_peer(PodDescriptor(p2_ip, 5))
    #
    #     p2 = PartialView(p2_ip, limit=4)
    #     p2.add_peer(PodDescriptor("172.0.1.3", 1))
    #     p2.add_peer(PodDescriptor("172.0.1.16", 3))
    #     p2.add_peer(PodDescriptor("172.0.1.2", 3))
    #     p2.add_peer(PodDescriptor("172.0.1.1", 4))
    #
    #     oldest = p1.get_oldest_peer()
    #     self.assertEqual(oldest.ip, p2_ip)
    #
    #     to_send_to_p2 = p1.select_neighbors(oldest, 2)
    #     to_send_to_p2.add_peer_ip(p1_ip, allow_self_ip=True)
    #
    #     self.assertEqual(to_send_to_p2.size, 3)
    #     self.assertTrue(to_send_to_p2.contains_ip(p1_ip))
    #     self.assertTrue(to_send_to_p2.get_peer_by_ip(p1_ip).age, 0)
    #     self.assertFalse(to_send_to_p2.contains_ip(p2_ip))
    #
    #     # source = message.get('source')
    #     # size = received_partial_view.size
    #     # to_avoid = None
    #     # if cyclon.partialView.contains_ip(source):
    #     #     to_avoid = cyclon.partialView.get_peer_by_ip(source)
    #     # to_send = cyclon.partialView.select_neighbors(to_avoid, size)
    #     #
    #     # # Merge current partial view with the one just received
    #     # cyclon.partialView.merge(received_partial_view)
    #
    #     size = to_send_to_p2.size
    #
    #     to_send_to_p1 = p2.select_neighbors(size=size)
    #
    #     self.assertEqual(to_send_to_p1.size, size)
    #
    #     p2.merge(to_send_to_p2)
    #     p1.merge(to_send_to_p1)
    #
    #     self.assertTrue(p2.contains_ip(p1_ip))
    #     self.assertFalse(p1)
    #     self.assertTrue((p2.is_full()))

    # Every time the view size is checked if it is equal to the actual size
    def tearDown(self):
        self.assertEqual(len(self.partialView.peer_list), self.partialView.size)


if __name__ == '__main__':
    unittest.main()
