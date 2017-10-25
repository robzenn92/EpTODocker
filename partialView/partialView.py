#!/usr/bin/env python2

import os
import json
import random
from operator import attrgetter


class PodDescriptor:

    def __init__(self, ip, age=0):
        self.ip = ip
        self.age = age

    def __str__(self):
        return str(self.ip)

    def __eq__(self, other):
        return self.ip == other.ip

    def __lt__(self, other):
        return self.age < other.age

    def __gt__(self, other):
        return self.age > other.age

    @classmethod
    def from_dict(cls, a_dict):
        ip = str(a_dict['ip'])
        age = int(a_dict['age'])
        return cls(ip, age)

    __repr__ = __str__


class PartialView:

    def __init__(self, ip, limit=int(os.environ['VIEW_LIMIT']), shuffle_length=int(os.environ['SHUFFLE_LENGTH']), peer_list=None):

        self.ip = ip
        self.limit = limit
        self.shuffle_length = shuffle_length

        # shuffle_length must be less than limit
        assert self.shuffle_length <= self.limit

        if peer_list is None:
            self.peer_list = []
            self.size = 0
        else:
            self.peer_list = peer_list
            self.size = len(self.peer_list)

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add_peer(self, peer, allow_self=False):
        if isinstance(peer, PodDescriptor):
            if peer.ip != self.ip or allow_self:
                if not self.is_full() and not self.contains(peer):
                    self.peer_list.append(peer)
                    self.size += 1
                    return True
        return False

    def add_peer_ip(self, ip, allow_self_ip=False):
        if ip != self.ip or allow_self_ip:
            if not self.is_full() and not self.contains_ip(ip):
                peer = PodDescriptor(ip)
                self.peer_list.append(peer)
                self.size += 1
                return True
        return False

    def remove_peer(self, peer):
        if isinstance(peer, PodDescriptor):
            if self.contains(peer):
                self.peer_list.remove(peer)
                self.size -= 1
                return True
        return False

    def remove_peer_ip(self, ip):
        if self.contains_ip(ip):
            self.peer_list = [peer for peer in self.peer_list if not peer.ip == ip]
            self.size = len(self.peer_list)
            return True
        return False

    def contains(self, peer):
        return any(p == peer for p in self.peer_list)

    def contains_ip(self, ip):
        return any(peer.ip == ip for peer in self.peer_list)

    def increment(self):
        for peer in self.peer_list:
            peer.age += 1

    def sort(self):
        self.peer_list.sort()

    # Discards entries pointing at P and entries already contained in P's cache.
    # Update P's cache to include all remaining entries, by firstly using empty cache slots (if any),
    # and secondly replacing entries among the ones sent to Q.
    def merge(self, partial_view_sent, partial_view_received):

        # I remove myself from the received partial view
        partial_view_received.remove_peer_ip(self.ip)
        partial_view_sent.remove_peer_ip(self.ip)

        # I get the list of peers that are not already contained in my view
        unknown = [peer for peer in partial_view_received.get_peer_list() if not self.contains(peer)]
        known = [peer for peer in partial_view_received.get_peer_list() if peer not in unknown]
        can_be_replaced = [peer for peer in partial_view_sent.peer_list if peer not in known]

        if unknown:

            i = 0
            while not self.is_full():
                i += 1 if self.add_peer(unknown[i]) else 0

            how_many = i
            while i < len(unknown):
                self.remove_peer(can_be_replaced[i - how_many])
                self.add_peer(unknown[i])
                i += 1

        # # For each peer in the view I received
        # for peer in partial_view.get_peer_list():
        #     # Self ip is not allowed
        #     if not peer.ip == self.ip:
        #         # If peer is not contained in my partialView
        #         if not self.contains(peer):
        #             # I add peer to the list (I cannot use self.add_peer because of the limit check)
        #             self.peer_list.append(peer)
        #             self.size += 1
        #         else:
        #             # I need to check which of them is older
        #             duplicated = self.get_peer_by_ip(peer.ip)
        #             duplicated.age = min(peer.age, duplicated.age)


        # 9) If there is still space in my view I add the peers I removed before
        # for peer in neighbors.get_peer_list():
        #     # If peer is not contained in my view it is going to be added
        #     # Otherwise its age is updated with the minimum value between the two descriptors
        #     if not self.partialView.contains(peer):
        #         self.partialView.add_peer(peer)
        #     else:
        #         p = self.partialView.get_peer_by_ip(peer.ip)
        #         p.age = min(p.age, peer.age)

        self.sort()
        # self.size = min(self.limit, self.size)
        # del self.peer_list[self.size:]

    # Returns a PartialView with one free slot for myself. It will be used as request
    def select_neighbors_for_request(self, avoid_peer=None):

        # I want a sample of at max (self.shuffle_length - 1) peers without avoid_peer
        sample = self.sample(self.shuffle_length - 1, avoid_peer)

        # Note that the PartialView's limit is not self.shuffle_length because size might be less than that
        return PartialView(self.ip, len(sample) + 1, len(sample) + 1, sample)

    # Returns a full PartialView will be used as reply
    def select_neighbors_for_reply(self, avoid_peer=None):

        # I want a sample of at max self.shuffle_length peers without avoid_peer
        sample = self.sample(self.shuffle_length, avoid_peer)

        # Note that the PartialView's limit is not self.shuffle_length because size might be less than that
        return PartialView(self.ip, len(sample), len(sample), sample)

    # Returns a random sample of peers of size less than or equal to limit
    def sample(self, limit, avoid_peer=None):

        sample = []
        peer_list = [peer for peer in self.peer_list if peer != avoid_peer]
        size = min(limit, len(peer_list))

        while len(sample) < size:
            random_peer = random.choice(list(peer_list))
            if random_peer not in sample:
                sample.append(random_peer)
            peer_list.remove(random_peer)
        return sample

    @classmethod
    def from_dict(cls, a_dict):
        ip = a_dict['ip']
        limit = int(a_dict['limit'])
        shuffle_length = int(a_dict['shuffle_length'])
        peer_list = []
        for peer in a_dict['peer_list']:
            peer_list.append(PodDescriptor.from_dict(peer))
        return cls(ip, limit, shuffle_length, peer_list)

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size >= self.limit

    def get_peer_by_ip(self, ip):
        if self.contains_ip(ip):
            for peer in self.peer_list:
                if peer.ip == ip:
                    return peer
        return None

    def get_peer_list(self):
        return self.peer_list[:]

    def get_peer_ip_list(self):
        return [peer.ip for peer in self.peer_list]

    def get_oldest_peer(self):
        return max(self.peer_list, key=attrgetter("age")) if not self.is_empty() else None

    __repr__ = __str__
