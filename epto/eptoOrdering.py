#!/usr/bin/env python2


# from numpy import inf
from configuration import logger


class EpTOOrdering(object):

    def __init__(self):
        # todo: remember set() is wrong
        self.received = set()
        self.delivered = set()
        self.last_delivered_ts = 0

    def order(self, ball):
        logger.info("I am ordering ball : " + str(type(ball)) +  " - "+ str(ball))
        for event in self.received:
            event.increase_ttl()

        for event in ball:
            if event not in self.delivered and event.ts >= self.last_delivered_ts:
                if event in self.received:
                    for e in self.received:
                        if e.event_id == event.event_id and e.ttl < event.ttl:
                            e.ttl = event.ttl
                else:
                    self.received.add(event)

        # minQueuedTs = -inf
        deliverableEvents = set()

        for event in self.received:
            if True: # isDeliverable
                deliverableEvents.add(event)
            elif minQueuedTs > event.ts:
                minQueuedTs = event.ts

        for event in deliverableEvents:
            if event.ts > minQueuedTs:
                deliverableEvents.remove(event)
            else:
                self.received.remove(event)

        sortedDeliverableEvents = deliverableEvents.copy()
        for event in sortedDeliverableEvents:
            self.delivered.add(event)
            self.last_delivered_ts = event.ts
            logger.critical("I Delivered " + str(event))