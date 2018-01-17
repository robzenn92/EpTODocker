#!/usr/bin/env python3
# coding: utf-8

import yaml


class DockerRegistry(object):
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.load(f)
            self.host = config['registry']['host']
            self.port = config['registry']['port']
            self.address = self.host + ":" + str(self.port) + "/"
