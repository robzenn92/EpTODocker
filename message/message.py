#!/usr/bin/env python3


class Message(object):

    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.data = data

    def to_json(self):
        try:
            to_json = self.data.to_json()
        except Exception:
            to_json = self.data

        return {
            "source": self.source,
            "destination": self.destination,
            "data": to_json
        }
