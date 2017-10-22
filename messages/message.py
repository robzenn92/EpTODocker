#!/usr/bin/env python2

import json


class Message:
    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
