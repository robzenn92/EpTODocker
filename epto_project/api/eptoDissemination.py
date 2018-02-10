#!/usr/bin/env python3

import os
import json
import time
import requests
from ball.ball import Ball
from event.event import Event
from message.message import Message
from apscheduler.schedulers.background import BackgroundScheduler
from .configuration import logger
from .helpers import my_ip, format_address
from .eptoOrdering import EpTOOrdering
from .stabilityOracle import StabilityOracle


class EpTODissemination(object):

    def __init__(self, initial_delay, interval):
        self.ip = my_ip()
        self.api_version = 'v1'
        self.next_ball = Ball()
        self.view = []
        self.fanout = int(os.environ['FANOUT'])
        self.ttl = int(os.environ['TTL'])
        self.stability_oracle = StabilityOracle(self.ttl)
        self.ordering = EpTOOrdering(self.stability_oracle)
        self.schedule_repeated_task(initial_delay, interval)

    def schedule_repeated_task(self, initial_delay, interval):
        logger.debug('This is a repeated task but I am waiting a delay to start.',  delay=initial_delay)
        time.sleep(initial_delay)
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.repeated_task, 'interval', seconds=interval, max_instances=1)
        scheduler.start()

    def broadcast(self):
        event = Event(self.ip, ts=self.stability_oracle.get_clock())
        logger.debug('I am adding an event to next_ball.', added_event=event)
        self.next_ball.add(event)

    def receive_ball(self, received_ball):
        logger.debug('I received a ball.', received_ball=received_ball)
        ball = []
        for event in received_ball:
            logger.debug('Looping events.', current_event=event)
            ball.append(Event.from_dict(event))

        for event in ball:
            if event.ttl < self.ttl:
                if event in self.next_ball:
                    for e in self.next_ball:
                        if e.event_id == event.event_id and e.ttl < event.ttl:
                            e.ttl = event.ttl
                else:
                    self.next_ball.add(event)
            self.stability_oracle.update_clock(event.ts)

    def get_k_view(self, k):
        logger.debug('Getting PartialView of size k from Cyclon', k=k)
        ret = requests.get('http://localhost:5000/' + self.api_version + '/k-view', params={'k': k}, timeout=5)
        logger.debug('I got the a response:',  response=ret.content)
        return json.loads(ret.content)
        # return [ip.encode('ascii', 'ignore') for ip in json.loads(ret.content)]

    def send_next_ball(self, destination_ip):
        destination = os.getenv('TEST_IP', format_address(destination_ip, 5001))
        m = Message(format_address(self.ip, 5001), destination, self.next_ball)
        logger.debug('I am sending next ball message.', message=m.to_json(), destination=destination)
        ret = requests.post(m.destination + '/' + self.api_version + '/receive-ball', json=m.to_json(), timeout=5)
        return ret.content

    # Task executed every delta time units
    def repeated_task(self):

        logger.debug('This repeated_task is started.', next_ball=self.next_ball)

        if not self.next_ball.is_empty():

            self.next_ball.increase_events_ttl()
            logger.debug('I increased the ttl of events in self.next_ball.')
            self.view = self.get_k_view(self.fanout)
            logger.info('I got a k-view from cyclon: ' + str(self.view))
            for destination in self.view:
                response = self.send_next_ball(destination)
                logger.info('I sent next ball to ' + destination + ' and I got ' + str(response))

            self.ordering.order(self.next_ball.copy())
            self.next_ball = Ball()
            logger.debug("I reset next_ball.", next_ball=self.next_ball)

        else:

            logger.debug('My next_ball is still empty! Need to wait', next_ball=self.next_ball)
