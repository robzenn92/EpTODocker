#!/usr/bin/env python2

import os
import time
import random
from configuration import logger
from apscheduler.schedulers.background import BackgroundScheduler
from eptoDissemination import EpTODissemination


class EpTOApplication(object):

    def __init__(self, ip):
        self.ip = ip
        self.dissemination = EpTODissemination(self.ip, 15, 15)
        self.schedule_probabilistic_broadcast(15, 3)

    def schedule_probabilistic_broadcast(self, initial_delay, interval):
        logger.info('This is schedule_probabilistic_broadcast but I am waiting ' + str(initial_delay) + 's to start.')
        time.sleep(initial_delay)
        scheduler = BackgroundScheduler(logger=logger)
        scheduler.add_job(self.probabilistic_broadcast, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    # EpTO-broadcast(event)
    # Based on a given probability decides whether to broadcast an event or not.
    # It will invoke EpTODissemination.broadcast()
    def probabilistic_broadcast(self):
        prob = random.uniform(0, 1)
        logger.info('This is probabilistic_broadcast and prob = ' + str(prob))
        if prob <= os.environ['BROADCAST_PROB']:
            self.dissemination.broadcast()
