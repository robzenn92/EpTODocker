#!/usr/bin/env python3


class Message(object):

    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.data = data

    def to_json(self):
        return {
            "source": self.source,
            "destination": self.destination,
            "data": self.data.to_json()
        }
