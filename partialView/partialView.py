#!/usr/bin/env python2

import os
import json
import random


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

    def __init__(self, ip, size=0, limit=int(os.environ['VIEW_LIMIT']), shuffle_length=int(os.environ['SHUFFLE_LENGTH']), peer_list=None):

        self.ip = ip
        self.size = size
        self.limit = limit
        self.shuffle_length = shuffle_length
        if peer_list is None:
            self.peer_list = []
        else:
            self.peer_list = peer_list

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add_peer(self, peer):
        if isinstance(peer, PodDescriptor):
            if peer.ip != self.ip:
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
        try:
            if isinstance(peer, PodDescriptor):
                self.peer_list.remove(peer)
                self.size -= 1
                return True
        except ValueError:
            pass  # do nothing!
        return False

    def remove_peer_ip(self, ip):
        self.peer_list = [peer for peer in self.peer_list if not peer.ip == ip]
        self.size -= 1

    def contains(self, peer):
        return any(p == peer for p in self.peer_list)

    def contains_ip(self, ip):
        return any(peer.ip == ip for peer in self.peer_list)

    def increment(self):
        for peer in self.peer_list:
            peer.age += 1

    def sort(self):
        self.peer_list.sort()

    # TODO: consider that the other partial view may contain self.ip
    def merge(self, partial_view):

        # For each peer in the view I received
        for peer in partial_view.get_peer_list():
            # Self ip is not allowed
            if not peer.ip == self.ip:
                # If peer is not contained in my partialView
                if not self.contains(peer):
                    # I add peer to the list (I cannot use self.add_peer because of the limit check)
                    self.peer_list.append(peer)
                    self.size += 1
                else:
                    # I need to check which of them is older
                    duplicated = self.get_peer_by_ip(peer.ip)
                    if peer < duplicated:
                        duplicated.age = peer.age

        self.sort()
        self.size = min(self.limit, self.size)
        del self.peer_list[self.size:]

    # TODO: Do I need to check if size > self.size?
    def select_neighbors(self, avoid_peer=None, size=None):
        p = PartialView(self.ip)
        peer_list = [peer for peer in self.peer_list if peer != avoid_peer]
        if size is None:
            size = self.shuffle_length - 1
        while p.size < size:
            random_peer = random.choice(list(peer_list))
            if not p.contains(random_peer):
                p.add_peer(random_peer)
            else:
                peer_list.remove(random_peer)
        return p

    @classmethod
    def from_dict(cls, a_dict):
        ip = a_dict['ip']
        size = int(a_dict['size'])
        limit = int(a_dict['limit'])
        shuffle_length = int(a_dict['shuffle_length'])
        peer_list = []
        for peer in a_dict['peer_list']:
            peer_list.append(PodDescriptor.from_dict(peer))
        return cls(ip, size, limit, shuffle_length, peer_list)

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
        from operator import attrgetter
        return max(self.peer_list, key=attrgetter("age"))

    __repr__ = __str__
