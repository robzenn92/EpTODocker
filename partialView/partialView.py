#!/usr/bin/env python3

import os
import json
import random
from operator import attrgetter
from typing import List


class PodDescriptor(object):

    def __init__(self, ip: str, age: int = 0) -> None:
        self.ip = ip
        self.age = age

    def __str__(self) -> str:
        return str(self.ip)

    def __eq__(self, other: object) -> bool:

        if other is None:
            return False

        if isinstance(other, PodDescriptor):
            return self.ip == other.ip
        else:
            raise TypeError

    def __lt__(self, other: object) -> bool:
        if isinstance(other, PodDescriptor):
            return self.age < other.age
        else:
            raise TypeError

    def __gt__(self, other: object) -> bool:
        if isinstance(other, PodDescriptor):
            return self.age > other.age
        raise TypeError

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @classmethod
    def from_dict(cls, pod_descriptor: dict):
        ip = str(pod_descriptor['ip'])
        age = int(pod_descriptor['age'])
        return cls(ip, age)

    __repr__ = __str__


class PartialView(object):

    def __init__(self,
                 ip: str,
                 limit: int = int(os.environ['VIEW_LIMIT']),
                 shuffle_length: int = int(os.environ['SHUFFLE_LENGTH']),
                 peer_list: list = None) -> None:

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

    def __str__(self) -> str:
        return str(self.to_json())

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True))

    def add_peer(self, peer: PodDescriptor, allow_self: bool = False) -> bool:
        if isinstance(peer, PodDescriptor):
            if peer.ip != self.ip or allow_self:
                if not self.is_full() and not self.contains(peer):
                    self.peer_list.append(peer)
                    self.size += 1
                    return True
        return False

    def add_peer_ip(self, ip: str, allow_self_ip: bool = False) -> bool:
        if ip != self.ip or allow_self_ip:
            if not self.is_full() and not self.contains_ip(ip):
                peer = PodDescriptor(ip)
                self.peer_list.append(peer)
                self.size += 1
                return True
        return False

    def remove_peer(self, peer: PodDescriptor) -> bool:
        if isinstance(peer, PodDescriptor):
            if self.contains(peer):
                self.peer_list.remove(peer)
                self.size -= 1
                return True
        return False

    def remove_peer_ip(self, ip: str) -> bool:
        if self.contains_ip(ip):
            self.peer_list = [peer for peer in self.peer_list if not peer.ip == ip]
            self.size = len(self.peer_list)
            return True
        return False

    def contains(self, peer: PodDescriptor) -> bool:
        if isinstance(peer, PodDescriptor):
            return any(p == peer for p in self.peer_list)
        else:
            raise TypeError

    def contains_ip(self, ip: str) -> bool:
        return any(peer.ip == ip for peer in self.peer_list)

    def increment(self) -> None:
        for peer in self.peer_list:
            peer.age += 1

    def sort(self) -> None:
        self.peer_list.sort()

    # Discards entries pointing at P and entries already contained in P's cache.
    # Update P's cache to include all remaining entries, by firstly using empty cache slots (if any),
    # and secondly replacing entries among the ones sent to Q.
    def merge(self, partial_view_sent, partial_view_received) -> None:

        if isinstance(partial_view_sent, PartialView) and isinstance(partial_view_received, PartialView):

            # Discards entries pointing at P and entries already contained in P's cache.
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

            self.sort()
            # self.size = min(self.limit, self.size)
            # del self.peer_list[self.size:]

        else:
            raise TypeError

    # Returns a PartialView with one free slot for myself. It will be used as request
    def select_neighbors_for_request(self, avoid_peer: PodDescriptor = None):

        # I want a sample of at max (self.shuffle_length - 1) peers without avoid_peer
        sample = self.sample_descriptors(self.shuffle_length - 1, avoid_peer)

        # Note that the PartialView's limit is not self.shuffle_length because size might be less than that
        return PartialView(self.ip, len(sample) + 1, len(sample) + 1, sample)

    # Returns a full PartialView will be used as reply
    def select_neighbors_for_reply(self, avoid_peer: PodDescriptor = None):

        # I want a sample of at max self.shuffle_length peers without avoid_peer
        sample = self.sample_descriptors(self.shuffle_length, avoid_peer)

        # Note that the PartialView's limit is not self.shuffle_length because size might be less than that
        return PartialView(self.ip, len(sample), len(sample), sample)

    # Returns a random sample of peers of size less than or equal to limit
    def sample_descriptors(self, limit: int, avoid_peer: PodDescriptor = None) -> List[PodDescriptor]:

        sample = []
        peer_list = [peer for peer in self.peer_list if peer != avoid_peer]
        size = min(limit, len(peer_list))

        while len(sample) < size:
            random_peer = random.choice(list(peer_list))
            if random_peer not in sample:
                sample.append(random_peer)
            peer_list.remove(random_peer)
        return sample

    def sample_ips(self, limit: int) -> List[str]:
        return [peer.ip for peer in self.sample_descriptors(limit)]

    @classmethod
    def from_dict(cls, partial_view: dict):
        ip = partial_view['ip']
        limit = int(partial_view['limit'])
        shuffle_length = int(partial_view['shuffle_length'])
        peer_list = []
        for peer in partial_view['peer_list']:
            peer_list.append(PodDescriptor.from_dict(peer))
        return cls(ip, limit, shuffle_length, peer_list)

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size >= self.limit

    def get_peer_by_ip(self, ip: str) -> PodDescriptor:
        if self.contains_ip(ip):
            for peer in self.peer_list:
                if peer.ip == ip:
                    return peer
        return None

    def get_peer_list(self) -> List[PodDescriptor]:
        return self.peer_list[:]

    def get_peer_ip_list(self) -> List[str]:
        return [peer.ip for peer in self.peer_list]

    def get_oldest_peer(self) -> PodDescriptor:
        return max(self.peer_list, key=attrgetter("age")) if not self.is_empty() else None

    __repr__ = __str__
