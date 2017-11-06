#!/usr/bin/env python2

import os
import json
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from configuration import logger, format_address
from ball import Ball
from event import Event
# from eptoOrdering import EpTOOrdering
from logicalClock import LogicalCLock
from messages.message import Message


class EpTODissemination(object):

    def __init__(self, ip, initial_delay, interval):
        self.ip = ip
        self.next_ball = Ball()
        self.view = []
        self.fanout = int(os.environ['FANOUT'])
        self.ttl = int(os.environ['TTL'])
        # self.ordering = EpTOOrdering()
        self.logicalClock = LogicalCLock(self.ip)
        self.schedule_repeated_task(initial_delay, interval)

    def schedule_repeated_task(self, initial_delay, interval):

        logger.info('This is schedule_repeated_task but I am waiting ' + str(initial_delay) + 's to start.')
        time.sleep(initial_delay)
        scheduler = BackgroundScheduler(logger=logger)
        scheduler.add_job(self.repeated_task, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    def broadcast(self):
        event = Event(self.ip)
        logger.info('I am adding ' + str(event) + ' to next_ball')
        self.next_ball.add(event)

    def receive_ball(self, received_ball):

        ball = []
        logger.info('I received =  ' + str(type(received_ball)) + " and ball is =\n" + str(received_ball))

        for event in received_ball:
            ball.append(Event.from_dict(event))

        for event in ball:
            if event.ttl < self.ttl:
                if event in self.next_ball:
                    for e in self.next_ball:
                        if e.event_id == event.event_id and e.ttl < event.ttl:
                            e.ttl = event.ttl
                else:
                    self.next_ball.add(event)

    @staticmethod
    def get_k_view(k):
        ret = requests.get('http://localhost:5000/k-view', params={'k': k}, timeout=5)
        return [ip.encode('ascii', 'ignore') for ip in json.loads(ret.content)]

    def send_next_ball(self, destination):
        m = Message(format_address(self.ip, 5001), format_address(destination, 5001), list(self.next_ball))
        logger.info('I am sending next ball to: ' + str(destination))
        ret = requests.post(m.destination + '/receive-ball', json=m.to_json(), timeout=5)
        return ret.content

    # Task executed every delta time units
    def repeated_task(self):

        logger.critical('This repeated_task is started. NextBall is ' + str(self.next_ball))

        if not self.next_ball.is_empty():

            self.next_ball.increase_events_ttl()
            logger.info('I increased the ttl of events in self.next_ball.')
            self.view = self.get_k_view(self.fanout)
            logger.info('I got a k-view from cyclon: ' + str(self.view))
            for destination in self.view:
                logger.info('I send next ball to ' + destination + ' and I got ' + str(self.send_next_ball(destination)))

            # self.ordering.order(self.next_ball.copy())
            self.next_ball = Ball()
            logger.critical("Next ball is empty: " + str(self.next_ball))

        else:

            logger.info('My next_ball is still empty! Need to wait')
