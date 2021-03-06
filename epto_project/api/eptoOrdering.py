#!/usr/bin/env python3

from .configuration import logger


class EpTOOrdering(object):

    def __init__(self, stability_oracle, application):
        self.received = set()   # received map of (id, event) pairs with all known but not yet delivered events
        self.delivered = []     # list of all the events already delivered to the application
        self.stability_oracle = stability_oracle
        self.last_delivered_ts = 0
        self.application = application  # reference to the application layer

    # Procedure order is called every round and its goal is to deliver events to the application.
    # The main task of this procedure is to move events from the received set to the delivered set,
    # preserving the total order of the events.
    def order(self, ball):

        logger.debug('This Ordering component has been invoked.', ball=ball, received=self.received)

        # We start by incrementing the ttl of all events previously received to indicate the start of a new round.
        for event in self.received:
            event.increase_ttl()

        # Then, all the events received in ball are processed.
        # An event delivered or whose timestamp is smaller than the timestamp of the last event delivered is discarded.
        # Delivering such an event in the former case would violate integrity due to the delivery of a duplicate,
        # and in the latter case would violate total order. Otherwise, the event is added to received or,
        # if already there, its ttl value is set to the largest of both occurrences.
        for event in ball:
            if event not in self.delivered and event.ts >= self.last_delivered_ts:
                if event in self.received:
                    for e in self.received:
                        if e == event:
                            e.ttl = max(e.ttl, event.ttl)
                else:
                    self.received.add(event)

        # The next step is to build the set of events to be delivered in the current round (deliverable_events).
        # An event e becomes deliverable if it is deemed so by the isDeliverable oracle and if its timestamp is
        # smaller than any non deliverable event in the received set.
        # Deliverable events are collected in the deliverable_events set and the minimum timestamp of all the events
        # that cannot yet be delivered is calculated.
        min_queued_ts = float('inf')
        deliverable_events = set()
        for event in self.received:
            if self.stability_oracle.is_deliverable(event):
                deliverable_events.add(event)
            elif min_queued_ts > event.ts:
                min_queued_ts = event.ts

        # All the events whose timestamp is greater than min_queued_ts are removed from the deliverable_events set,
        # as they cannot yet be delivered without violating total order.
        # The remaining events are ready to be delivered and thus are removed from the received set.
        events_to_remove = set()
        for event in deliverable_events:
            if event.ts >= min_queued_ts:
                events_to_remove.add(event)
            else:
                self.received.remove(event)
        for event in events_to_remove:
            deliverable_events.remove(event)

        # Finally, the events in deliverableEvents are delivered to the application in timestamp order.
        sorted_deliverable_events = sorted(deliverable_events)
        for event in sorted_deliverable_events:
            self.deliver(event)

    def deliver(self, event):
        self.delivered.append(event)
        self.last_delivered_ts = event.ts
        self.application.deliver_event(event)
