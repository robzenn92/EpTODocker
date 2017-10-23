#!/usr/bin/env python2

import os
import re
from kubernetesClient import KubernetesClient


def who_am_i():
    k8s = KubernetesClient()
    return k8s.list_pods_by_field_selector("metadata.name=" + os.environ['MY_POD_NAME'])[0]


def my_ip():
    return os.environ['MY_POD_IP']


def my_pod_uid():
    return os.environ['MY_POD_UID']


def format_address(ip, port):
    return 'http://' + ip + ':' + str(port)


def get_ip_from_address_string(address):
    return re.search(r'[0-9]+(?:\.[0-9]+){3}', address).group(0)
