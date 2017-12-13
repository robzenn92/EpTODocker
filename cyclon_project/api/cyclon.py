#!/usr/bin/env python3

import random
import time
import json
import requests
from os import environ
from requests import Timeout
from .configuration import logger
from .helpers import format_address
from kubernetesClient.kubernetesClient import KubernetesClient
from messages.message import Message
from partialView.partialView import PartialView, PodDescriptor
from apscheduler.schedulers.background import BackgroundScheduler


class Cyclon(object):

    def __init__(self):
        self.ip = environ['MY_POD_IP']
        self.k8s = KubernetesClient()
        self.partialView = PartialView(self.ip)
        self.bootstrap()

    def bootstrap(self):
        self.bootstrap_exponential_backoff(5, 5)
        self.schedule_change(5, 15)
        self.schedule_change(15, 15)

    def bootstrap_exponential_backoff(self, initial_delay, delay):

        logger.info("Bootstrapping cyclon's view: " + str(self.partialView))
        time.sleep(initial_delay)

        attempt = 1
        ips = self.k8s.list_pods_ips_by_field_selector(label_selector="app=epto", field_selector="status.phase=Running")
        logger.info('There are ' + str(len(ips)) + " Pods running. This is attempt #" + str(attempt))

        # Exponential backoff starts in case the number of running pods is lower than the partialView's limit.
        # TODO: Did I consider also that some pods might not be ready yet?
        # TODO: Consider that there is no need to have at least self.partialView.limit peers ready to start!
        # TODO: There can be peers running with an initial partial view of size < self.partialView.limit
        while len(ips) <= self.partialView.limit:
            attempt += 1
            delay *= 2
            time.sleep(delay)
            ips = self.k8s.list_pods_ips_by_field_selector(label_selector="app=epto", field_selector="status.phase=Running")
            logger.info('There are ' + str(len(ips)) + " Pods running. This is attempt #" + str(attempt))

        # I populate the PartialView and I avoid to consider myself
        try:
            ips.remove(self.ip)
        except ValueError:
            print("self.ip was not there")

        while not self.partialView.is_full():
            random_ip = random.choice(ips)
            # TODO: REPLACE WITH self.partialView.add_peer_ip(random_ip)
            self.partialView.add_peer(PodDescriptor(random_ip, random.randint(0, 9)))

        logger.info('My view after bootstrap is:\n' + str(self.partialView))

    def schedule_change(self, initial_delay, interval):

        initial_delay = random.randint(0, initial_delay)
        time.sleep(initial_delay)

        scheduler = BackgroundScheduler(logger=logger)
        scheduler.add_job(self.shuffle_partial_view, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    def shuffle_partial_view(self):

        logger.info("Shuffling")

        # 1) Increase by one the age of all neighbors
        self.partialView.increment()
        logger.info('My partialView:\n' + str(self.partialView))
        # 2) Select neighbor Q with the highest age among all neighbors.
        oldest = self.partialView.get_oldest_peer()
        logger.info('Selected oldest: ' + str(oldest))
        # 3) Select l - 1 other random neighbors (meaning avoid oldest).
        neighbors = self.partialView.select_neighbors_for_request(oldest)
        logger.info('Selected neighbors:\n' + str(neighbors))
        # 4) Replace Q's entry with a new entry of age 0 and with P's address.
        neighbors.add_peer_ip(self.ip, allow_self_ip=True)
        logger.info('Selected neighbors + myself (will be sent to ' + oldest.ip + '):\n' + str(neighbors))

        try:

            # 5) Send the updated subset to peer Q.
            response = json.loads(self.send_message(oldest.ip, 'exchange-view', neighbors))
            received_partial_view = PartialView.from_dict(response.get('data'))
            logger.info('I received (from ' + oldest.ip + '):\n' + str(received_partial_view))

            # 6) I remove the oldest peer from my view
            self.partialView.remove_peer(oldest)
            logger.info('My partialView after removing oldest:\n' + str(self.partialView))

            # 7) I merge my view with the one just received
            self.partialView.merge(neighbors, received_partial_view)
            logger.info('My partialView after merging:\n' + str(self.partialView))

        except Timeout:

            logger.info('TimeoutException: Request to ' + str(oldest.ip) + 'timed out.')

    def send_message(self, destination_ip, path, data):
        m = Message(format_address(self.ip, 5000), format_address(destination_ip, 5000), data)
        logger.info('I am sending Message: \n' + str(m.to_json()))
        ret = requests.post(m.destination + '/' + path, json=m.to_json(), timeout=5)
        logger.info('I got the following response:\n' + str(ret))
        return ret.content
