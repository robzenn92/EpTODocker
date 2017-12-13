#!/usr/bin/env python2

import os
import json
import unittest
from partialView.partialView import PartialView, PodDescriptor


class TestPartialView(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.partialView = PartialView("172.0.1.0")
        self.descriptors = []
        self.ips = ["172.0.1.1", "172.0.1.2", "172.0.1.3", "172.0.1.4", "172.0.1.5"]
        for ip in self.ips:
            self.descriptors.append(PodDescriptor(ip))

    # Limit should be equal to VIEW_LIMIT and shuffle_length should be equal to SHUFFLE_LENGTH
    def test_set_up_ok(self):
        self.assertEqual(self.partialView.limit, int(os.environ['VIEW_LIMIT']))
        self.assertEqual(self.partialView.shuffle_length, int(os.environ['SHUFFLE_LENGTH']))

    # Initial partialView should be empty
    def test_initial_partial_view_empty(self):
        self.assertEqual(self.partialView.size, 0)
        self.assertTrue(self.partialView.is_empty())

    # Method is_full should return false if partial view is not full
    def test_initial_partial_view_should_not_be_full(self):
        self.assertFalse(self.partialView.is_full())

    # Method is_full should return true if partial view is full
    def test_is_full_should_return_true_if_full(self):
        for i in range(self.partialView.limit):
            self.partialView.add_peer(self.descriptors[i])
        self.assertTrue(self.partialView.is_full())
        self.assertEqual(self.partialView.size, self.partialView.limit)

    # Method add_peer should return false if peer already contained
    def test_add_peer_should_return_false_if_peer_already_contained(self):
        peer = PodDescriptor("A new IP")
        self.partialView.add_peer(peer)
        size = self.partialView.size
        duplicated = PodDescriptor("A new IP")
        success = self.partialView.add_peer(duplicated)
        self.assertFalse(success)
        self.assertEqual(self.partialView.size, size)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

    # Method add_peer should not allow to insert a self entry
    def test_add_peer_should_not_allow_self_entry(self):
        ip = "my ip"
        p1 = PartialView(ip)
        peer = PodDescriptor(ip)
        size = self.partialView.size
        success = p1.add_peer(peer)
        self.assertFalse(success)
        self.assertFalse(p1.contains_ip(ip))
        self.assertEqual(p1.size, size)

    # Method add_peer should allow to insert a self entry if forced
    def test_add_peer_with_allow_self_should_allow_self_entry(self):
        ip = "my ip"
        p1 = PartialView(ip)
        peer = PodDescriptor(ip)
        size = self.partialView.size
        success = p1.add_peer(peer, True)
        self.assertTrue(success)
        self.assertTrue(p1.contains_ip(ip))
        self.assertEqual(p1.size, size + 1)

    # Method add_peer should increment size if view is not full
    def test_add_peer_should_increment_size_if_not_full(self):
        size = self.partialView.size
        peer = PodDescriptor("A new IP")
        self.partialView.add_peer(peer)
        self.assertTrue(self.partialView.contains(peer))
        self.assertEqual(self.partialView.size, size + 1)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

    # Method add_peer should not increment size if view is full
    def test_add_peer_should_not_increment_size_if_full(self):
        peer = PodDescriptor("A new IP")
        for i in range(self.partialView.limit):
            self.partialView.add_peer(self.descriptors[i])
        size = self.partialView.size
        success = self.partialView.add_peer(peer)
        self.assertFalse(success)
        self.assertFalse(self.partialView.contains(peer))
        self.assertEqual(self.partialView.size, size)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

    # Method add_peer_ip should return false if peer already contained
    def test_add_peer_ip_should_return_false_if_peer_already_contained(self):
        peer = "A new IP"
        self.partialView.add_peer_ip(peer)
        size = self.partialView.size
        duplicated = "A new IP"
        success = self.partialView.add_peer_ip(duplicated)
        self.assertFalse(success)
        self.assertEqual(self.partialView.size, size)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

    # Method add_peer_ip should not allow to insert a self entry
    def test_add_peer_ip_should_not_allow_self_entry(self):
        ip = "my ip"
        p1 = PartialView(ip)
        size = self.partialView.size
        success = p1.add_peer_ip(ip)
        self.assertFalse(success)
        self.assertFalse(p1.contains_ip(ip))
        self.assertEqual(p1.size, size)

    # Method add_peer_ip should allow to insert a self entry if forced
    def test_add_peer_ip_with_allow_self_should_allow_self_entry(self):
        ip = "my ip"
        p1 = PartialView(ip)
        size = self.partialView.size
        success = p1.add_peer_ip(ip, True)
        self.assertTrue(success)
        self.assertTrue(p1.contains_ip(ip))
        self.assertEqual(p1.size, size + 1)

    # Method add_peer_ip should increment size if view is not full
    def test_add_peer_ip_should_increment_size_if_not_full(self):
        size = self.partialView.size
        peer = "A new IP"
        self.partialView.add_peer_ip(peer)
        self.assertTrue(self.partialView.contains_ip(peer))
        self.assertEqual(self.partialView.size, size + 1)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

    # Method add_peer_ip should not increment size if view is full
    def test_add_peer_ip_should_not_increment_size_if_full(self):
        peer = "A new IP"
        for i in range(self.partialView.limit):
            self.partialView.add_peer(self.descriptors[i])
        size = self.partialView.size
        success = self.partialView.add_peer_ip(peer)
        self.assertFalse(success)
        self.assertFalse(self.partialView.contains_ip(peer))
        self.assertEqual(self.partialView.size, size)
        self.assertEqual(self.partialView.size, len(self.partialView.peer_list))

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

    # Method sample_descriptors should return an empty list if view is empty
    def test_sample_descriptors_should_return_empty_list_if_empty_view(self):
        sample = self.partialView.sample_descriptors(3)
        self.assertEqual(len(sample), 0)
        self.assertEqual(sample, [])
        self.assertTrue(isinstance(sample, list))

    # Method sample_descriptors should return a list of size element if the view's size is less than the limit given as parameter
    def test_sample_descriptors_should_return_less_than_limit_peers_if_size_less_than_limit(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        size = self.partialView.size
        sample = self.partialView.sample_descriptors(3)
        self.assertEqual(len(sample), size)

    # Method sample_descriptors should return a list of limit peers despite the size of the the view is greater then limit
    def test_sample_descriptors_should_return_no_more_than_limit_peers(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(PodDescriptor("172.0.1.9", 4))
        limit = 2
        size = self.partialView.size
        sample = self.partialView.sample_descriptors(limit)
        self.assertNotEqual(limit, size)
        self.assertEqual(len(sample), limit)

    # Method sample_descriptors should return a list of 1 peer and avoid the peer given as parameter
    def test_sample_descriptors_with_avoid_peer_more_than_limit(self):
        to_avoid = PodDescriptor("172.0.1.9", 4)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(to_avoid)
        limit = 1
        sample = self.partialView.sample_descriptors(limit, to_avoid)
        self.assertEqual(len(sample), limit)
        self.assertFalse(to_avoid in sample)

    # Method sample_descriptors should return a list of 2 peers and avoid the peer given as parameter
    def test_sample_descriptors_with_avoid_peer_less_than_limit(self):
        to_avoid = PodDescriptor("172.0.1.9", 4)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(to_avoid)
        limit = 3
        sample = self.partialView.sample_descriptors(limit, to_avoid)
        self.assertEqual(len(sample), 2)
        self.assertFalse(to_avoid in sample)

    # Method sample_descriptors should return a list of 3 peers if the peer to avoid is not contained in the view
    def test_sample_descriptors_with_avoid_peer_not_in_view(self):
        to_avoid = PodDescriptor("172.0.1.9", 4)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(PodDescriptor("172.0.1.10", 8))
        limit = 3
        sample = self.partialView.sample_descriptors(limit, to_avoid)
        self.assertEqual(len(sample), limit)
        self.assertFalse(to_avoid in sample)

    # Method sample_ips should return a list of 3 ips
    def test_sample_ips_should_return_a_list_of_ips(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
        self.partialView.add_peer(PodDescriptor("172.0.1.10", 8))
        limit = 3
        sample = self.partialView.sample_ips(limit)
        self.assertIn("172.0.1.5", sample)
        self.assertIn("172.0.1.4", sample)
        self.assertIn("172.0.1.10", sample)

    # Method sample_ips should return a list of 3 ips loadable by epto
    # def test_sample_ips_should_return_a_list_of_ips_loadable_by_epto(self):
    #     self.partialView.add_peer(PodDescriptor("172.0.1.5", 2))
    #     self.partialView.add_peer(PodDescriptor("172.0.1.4", 3))
    #     self.partialView.add_peer(PodDescriptor("172.0.1.10", 8))
    #     sample = json.dumps(self.partialView.sample_ips(2))
    #     # EpTO's code when EpTO invokes get_k_view()
    #     view = [ip.encode('ascii', 'ignore') for ip in json.loads(sample)]
    #     for destination in view:
    #         self.assertIsInstance(destination, str)
    #         self.assertIn(destination, self.partialView.get_peer_ip_list())

    # Test the exchange of views.
    # P1 plays the role of P while P2 plays the role of Q described in comments
    def test_exchange_views(self):

        p1 = PartialView("First IP", 4, 3)
        p1.add_peer(PodDescriptor("172.0.1.6", 0))
        p1.add_peer(PodDescriptor("172.0.1.3", 2))
        p1.add_peer(PodDescriptor("172.0.1.5", 3))
        p1.add_peer(PodDescriptor("Second IP", 5))

        p2 = PartialView("Second IP", 4, 3)
        p2.add_peer(PodDescriptor("172.0.1.3", 0))
        p2.add_peer(PodDescriptor("172.0.1.5", 1))
        p2.add_peer(PodDescriptor("172.0.1.2", 2))
        p2.add_peer(PodDescriptor("172.0.1.1", 4))

        ########################
        # P1 starts the exchange
        ########################

        # 1) Increase by one the age of all neighbors
        p1.increment()
        # 2) Select neighbor Q with the highest age among all neighbors.
        oldest = p1.get_oldest_peer()
        # 3) Select l - 1 other random neighbors (meaning avoid oldest).
        request = p1.select_neighbors_for_request(oldest)
        # 4) Replace Q's entry with a new entry of age 0 and with P's address.
        request.add_peer_ip(p1.ip, allow_self_ip=True)

        self.assertTrue(request.is_full())
        self.assertEqual(request.size, p1.shuffle_length)

        ################################################
        # P2 receives neighbors and prepares a reply
        ################################################

        reply = p2.select_neighbors_for_reply()

        self.assertTrue(request.is_full())
        self.assertEqual(request.size, p1.shuffle_length)

        # Note that in p1 the oldest is p2
        # p1 and p2 know two peers in common
        # p2 does not have an entry with p1's ip
        # p1.merge should:
        # - Discard 172.0.1.3 and 172.0.1.5
        # - Put in unknown list 172.0.1.2, 172.0.1.1

        # 6) I remove the oldest peer from my view
        p1.remove_peer(oldest)
        p1.merge(request, reply)

        self.assertTrue(p1.is_full())
        for peer in reply.get_peer_list():
            self.assertTrue(p1.contains(peer))

        self.assertLessEqual(self.partialView.size, self.partialView.limit)

    # Test the exchange of views.
    # P1 plays the role of P while P2 plays the role of Q described in comments
    # def test_exchange_views_2(self):
    #
    #     p1 = PartialView("First IP", 4, 3)
    #     p1.add_peer(PodDescriptor("172.0.1.6", 0))
    #     p1.add_peer(PodDescriptor("172.0.1.3", 2))
    #     p1.add_peer(PodDescriptor("172.0.1.5", 3))
    #     p1.add_peer(PodDescriptor("Second IP", 5))
    #
    #     p2 = PartialView("Second IP", 4, 3)
    #     p2.add_peer(PodDescriptor("172.0.1.3", 0))
    #     p2.add_peer(PodDescriptor("172.0.1.5", 1))
    #     p2.add_peer(PodDescriptor("172.0.1.2", 2))
    #     p2.add_peer(PodDescriptor("First IP", 4))
    #
    #     ########################
    #     # P1 starts the exchange
    #     ########################
    #
    #     # 1) Increase by one the age of all neighbors
    #     p1.increment()
    #     # 2) Select neighbor Q with the highest age among all neighbors.
    #     oldest = p1.get_oldest_peer()
    #     # 3) Select l - 1 other random neighbors (meaning avoid oldest).
    #     request = p1.select_neighbors_for_request(oldest)
    #     # 4) Replace Q's entry with a new entry of age 0 and with P's address.
    #     request.add_peer_ip(p1.ip, allow_self_ip=True)
    #
    #     self.assertTrue(request.is_full())
    #     self.assertEqual(request.size, p1.shuffle_length)
    #
    #     ################################################
    #     # P2 receives neighbors and prepares a reply
    #     ################################################
    #
    #     reply = p2.select_neighbors_for_reply()
    #
    #     self.assertTrue(request.is_full())
    #     self.assertEqual(request.size, p1.shuffle_length)
    #
    #     # Note that in p1 the oldest is p2
    #     # p1 and p2 know two peers in common
    #     # p2 does have an entry with p1's ip
    #     # p1.merge should:
    #     # - Discard 172.0.1.3 and 172.0.1.5 because are well known
    #     # - Discard First IP because self ip is not allowed
    #
    #     # 6) I remove the oldest peer from my view
    #     p1.remove_peer(oldest)
    #     p1.merge(request, reply)
    #
    #     for peer in reply.get_peer_list():
    #         if peer != p1.ip:
    #             self.assertTrue(p1.contains(peer))
    #
    #     self.assertLessEqual(self.partialView.size, self.partialView.limit)

    # Method get_oldest_peer should return a PodDescriptor
    def test_get_oldest_peer_should_return_none_if_empty_view(self):
        oldest = self.partialView.get_oldest_peer()
        self.assertEqual(oldest, None)

    # Method get_oldest_peer should return a PodDescriptor
    def test_get_oldest_peer_should_return_a_pod_descriptor(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 1))
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        oldest = self.partialView.get_oldest_peer()
        self.assertTrue(isinstance(oldest, PodDescriptor))

    # Method get_oldest_peer should return the peer with the highest age
    def test_get_oldest_peer(self):
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(PodDescriptor("172.0.1.4", 1))
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        oldest = self.partialView.get_oldest_peer()
        self.assertEqual(oldest.ip, "172.0.1.5")
        self.assertEqual(oldest.age, 4)

    def test_select_neighbors_for_request_should_return_a_non_full_view(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors_for_request(oldest)
        self.assertFalse(neighbors.is_full())
        self.assertEqual(neighbors.size, neighbors.shuffle_length - 1)

    def test_select_neighbors_for_request_should_not_contain_oldest_peer(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors_for_request(oldest)
        self.assertFalse(neighbors.contains(oldest))

    def test_select_neighbors_for_request_and_add_peer_should_return_full_view(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors_for_request(oldest)
        neighbors.add_peer_ip(self.partialView.ip, allow_self_ip=True)
        self.assertEqual(neighbors.size, self.partialView.shuffle_length)
        self.assertTrue(neighbors.is_full())

    def test_select_neighbors_for_reply_should_return_a_full_view(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors_for_reply(oldest)
        self.assertTrue(neighbors.is_full())
        self.assertEqual(neighbors.size, neighbors.shuffle_length)

    def test_select_neighbors_for_reply_should_contain_avoid_peer_if_size_eq_shuffle_length(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        neighbors = self.partialView.select_neighbors_for_reply(oldest)
        self.assertTrue(neighbors.is_full())
        self.assertEqual(neighbors.size, neighbors.shuffle_length)

    def test_select_neighbors_for_reply_should_not_contain_oldest_peer(self):
        oldest = PodDescriptor("172.0.1.4", 1)
        self.partialView.add_peer(PodDescriptor("172.0.1.6", 2))
        self.partialView.add_peer(oldest)
        self.partialView.add_peer(PodDescriptor("172.0.1.5", 4))
        neighbors = self.partialView.select_neighbors_for_reply(oldest)
        self.assertFalse(neighbors.contains(oldest))

    def test_empty_partial_view_to_json(self):
        jsonized = self.partialView.to_json()
        self.assertEqual(jsonized, json.dumps({"ip": "172.0.1.0", "limit": 3, "shuffle_length": 2, "peer_list": [], "size": 0}, sort_keys=True, indent=4))

    def test_unmarshal_partial_view(self):
        for ip in self.ips:
            self.partialView.add_peer_ip(ip)
        jsonized = json.loads(self.partialView.to_json())
        partial_view = PartialView.from_dict(jsonized)
        self.assertIsInstance(partial_view,PartialView)
        for peer in partial_view.peer_list:
            self.assertIsInstance(peer, PodDescriptor)
        self.assertEqual(partial_view.ip, self.partialView.ip)
        self.assertEqual(partial_view.size, 3)
        self.assertEqual(partial_view.limit, 3)

        for i in range(self.partialView.limit):
            self.assertEqual(partial_view.peer_list[i].ip, self.descriptors[i].ip)
            self.assertEqual(partial_view.peer_list[i].age, self.descriptors[i].age)

    # Every time the view size is checked if it is equal to the actual size
    def tearDown(self):
        self.assertEqual(len(self.partialView.peer_list), self.partialView.size)


if __name__ == '__main__':
    unittest.main()
