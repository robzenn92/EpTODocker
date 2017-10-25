#!/usr/bin/env python2

import logging
import random
import time
import json
import requests
from os import environ
from requests import Timeout
from helpers import format_address
from kubernetesClient import KubernetesClient
from messages.message import Message
from partialView.partialView import PartialView, PodDescriptor
from apscheduler.schedulers.background import BackgroundScheduler


class Cyclon:

    def __init__(self):
        self.ip = environ['MY_POD_IP']
        self.logger = logging.getLogger()
        self.k8s = KubernetesClient()
        self.partialView = PartialView(self.ip)

    def bootstrap(self):
        self.bootstrap_exponential_backoff(0, 1)
        self.schedule_change(15, 15)

    def bootstrap_exponential_backoff(self, initial_delay, delay):

        self.logger.info("Bootstrapping cyclon's view: " + str(self.partialView))
        time.sleep(initial_delay)

        ips = self.k8s.list_pods_ips_by_field_selector(label_selector="app=epto", field_selector="status.phase=Running")
        self.logger.info('There are ' + str(len(ips)) + " Pods running")

        # Exponential backoff starts in case the number of running pods is lower than the partialView's limit.
        # TODO: Did I consider also that some pods might not be ready yet?
        # TODO: Consider that there is no need to have at least self.partialView.limit peers ready to start!
        # TODO: There can be peers running with an initial partial view of size < self.partialView.limit
        while len(ips) <= self.partialView.limit:
            delay *= 2
            time.sleep(delay)
            ips = self.k8s.list_pods_ips_by_field_selector(label_selector="app=epto", field_selector="status.phase=Running")
            self.logger.info('There are ' + str(len(ips)) + " Pods running")

        # I populate the PartialView and I avoid to consider myself
        ips.remove(self.ip)
        while not self.partialView.is_full():
            random_ip = random.choice(ips)
            # TODO: REPLACE WITH self.partialView.add_peer_ip(random_ip)
            self.partialView.add_peer(PodDescriptor(random_ip, random.randint(0, 9)))

        self.logger.info('My view after bootstrap is:\n' + str(self.partialView))

    def schedule_change(self, initial_delay, interval):

        initial_delay = random.randint(0, initial_delay)
        time.sleep(initial_delay)

        scheduler = BackgroundScheduler(logger=self.logger)
        scheduler.add_job(self.shuffle_partial_view, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    def shuffle_partial_view(self):

        # PartialView's size should always be greater than shuffle_length
        # try:
        #     assert self.partialView.size >= self.partialView.shuffle_length
        # except AssertionError:
        #     self.logger.critical('AssertionError (self.partialView.size >= self.partialView.shuffle_length)' + str(self.partialView))
        #     self.logger.critical('AssertionError (self.partialView) was:\n' + str(self.partialView))
        #     raise

        # 1) Increase by one the age of all neighbors
        self.partialView.increment()
        self.logger.info('My partialView:\n' + str(self.partialView))
        # 2) Select neighbor Q with the highest age among all neighbors.
        oldest = self.partialView.get_oldest_peer()
        self.logger.info('Selected oldest: ' + str(oldest))
        # 3) Select l - 1 other random neighbors (meaning avoid oldest).
        neighbors = self.partialView.select_neighbors_for_request(oldest)
        self.logger.info('Selected neighbors:\n' + str(neighbors))
        # 4) Replace Q's entry with a new entry of age 0 and with P's address.
        neighbors.add_peer_ip(self.ip, allow_self_ip=True)
        self.logger.info('Selected neighbors + myself (will be sent to ' + oldest.ip + '):\n' + str(neighbors))

        # I should always send shuffle_length neighbors
        # try:
        #     assert neighbors.size == self.partialView.shuffle_length
        # except AssertionError:
        #     self.logger.critical('AssertionError (neighbors.size == self.partialView.shuffle_length)')
        #     self.logger.critical('AssertionError (self.neighbors) was:\n' + str(self.neighbors))
        #     self.logger.critical('AssertionError (self.partialView.shuffle_length) was:\n' + str(self.partialView.shuffle_length))
        #     raise

        try:

            # 5) Send the updated subset to peer Q.
            response = json.loads(self.send_message(oldest.ip, 'exchange-view', neighbors))
            received_partial_view = PartialView.from_dict(response.get('data'))
            self.logger.info('I received (from ' + oldest.ip + '):\n' + str(received_partial_view))

            # 6) I remove the oldest peer from my view
            self.partialView.remove_peer(oldest)
            self.logger.info('My partialView after removing oldest:\n' + str(self.partialView))

            # 7) I remove neighbors from my view
            # for peer in neighbors.get_peer_list():
            #     self.partialView.remove_peer(peer)
            # self.logger.info('My partialView after removing neighbors:\n' + str(self.partialView))

            # 8) I merge my view with the one just received
            self.partialView.merge(neighbors, received_partial_view)
            self.logger.info('My partialView after merging:\n' + str(self.partialView))

            # 9) If there is still space in my view I add the peers I removed before
            # for peer in neighbors.get_peer_list():
            #     # If peer is not contained in my view it is going to be added
            #     # Otherwise its age is updated with the minimum value between the two descriptors
            #     if not self.partialView.contains(peer):
            #         self.partialView.add_peer(peer)
            #     else:
            #         p = self.partialView.get_peer_by_ip(peer.ip)
            #         p.age = min(p.age, peer.age)

            self.logger.info('My partialView after adding neighbors:\n' + str(self.partialView))

        except Timeout:
            self.logger.info('TimeoutException: Request to ' + str(oldest.ip) + 'timed out.')

        # PartialView's size should always be greater than shuffle_length
        try:
            assert self.partialView.size >= self.partialView.shuffle_length
        except AssertionError:
            self.logger.critical('AssertionError (self.partialView.size >= self.partialView.shuffle_length)')
            self.logger.critical('AssertionError (self.partialView) was:\n' + str(self.partialView))
            raise

    def send_message(self, destination_ip, path, data):
        m = Message(format_address(self.ip, 5000), format_address(destination_ip, 5000), data)
        ret = requests.post(m.destination + '/' + path, json=m.to_json(), timeout=5)
        return ret.content
