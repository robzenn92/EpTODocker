#!/usr/bin/env python3

import os
import time
import random
from .configuration import logger
from .eptoDissemination import EpTODissemination
from apscheduler.schedulers.background import BackgroundScheduler


class EpTOApplication(object):

    def __init__(self):
        logger.debug('Epto Dissemination component will broadcast Balls every delta time unit.', delta=10, unit='seconds')
        logger.debug('Epto Ordering component will deliver Balls every delta time unit.', delta=15, unit='seconds')
        self.dissemination = EpTODissemination(10, 15)
        self.schedule_probabilistic_broadcast(10, 10)

    def schedule_probabilistic_broadcast(self, initial_delay, interval):
        logger.debug('This is schedule_probabilistic_broadcast but I am waiting a delay to start.', delay=initial_delay)
        time.sleep(initial_delay)
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.probabilistic_broadcast, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    # EpTO-broadcast(event)
    # Based on a given probability decides whether to broadcast an event or not.
    # It will invoke EpTODissemination.broadcast()
    def probabilistic_broadcast(self):
        prob = random.uniform(0, 1)
        logger.debug('This is probabilistic_broadcast.', prob=prob)
        if prob <= float(os.environ['BROADCAST_PROB']):
            self.dissemination.broadcast()

    def broadcast(self, data: str):
        self.dissemination.broadcast(data)
