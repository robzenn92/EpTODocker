#!/usr/bin/env python3

import os


def my_ip():
    return os.environ['MY_POD_IP'] if 'MY_POD_IP' in os.environ else '0.0.0.0'


def my_pod_uid():
    return os.environ['MY_POD_UID']


def format_address(ip, port):
    return 'http://' + ip + ':' + str(port)
