#!/usr/bin/env python2

import os
import json
from flask import Flask, request
from cyclon import Cyclon
from messages.message import Message
from partialView.partialView import PartialView
from configuration import my_ip, format_address, who_am_i, logger

# -----
# Global vars
# -----
app = Flask(__name__)
cyclon = Cyclon()


# ---------------------
# Debug routes
# The below routes are for debug use only.


@app.route('/hello')
def hello_world():
    return "Hello World. This is a cyclon protocol running on " + my_ip()


@app.route('/who-am-i')
def get_who_am_i():
    return str(who_am_i())


@app.route('/env')
def get_env():
    return str(os.environ)


@app.route('/view', methods=['GET'])
def get_view():
    global cyclon
    return str(cyclon.partialView)


# ---------------------
# Production routes

# Given a parameter k (integer)
# k-view returns a PartialView of size k as a subset of peers belonging to cyclon.partialView
@app.route('/k-view', methods=['GET'])
def get_k_view():
    global cyclon
    k = int(request.args.get('k'))
    view = cyclon.partialView.select_neighbors(size=k)
    logger.info('/k-view: I am returning this:\n' + str(cyclon.partialView))
    return str(view)


# Given a message containing a PartialView withing the data field
# exchange-view allows two peers to exchange each other subset of their partial views.
# Like in basic shuffling, the receiving peer replies by sending back a random subset of at most l neighbors.
# It then updates its own cache to accommodate all received entries.
@app.route('/exchange-view', methods=['POST'])
def exchange_view():
    global cyclon

    logger.info('My view is:\n' + str(cyclon.partialView) + ".")
    message = json.loads(request.get_json())

    received_partial_view = PartialView.from_dict(message.get('data'))
    logger.info('Got this (from ' + message.get('source') + ') as received_partial_view:\n' + str(
        received_partial_view) + ".")

    source = message.get('source')
    size = received_partial_view.size
    to_avoid = None
    if cyclon.partialView.contains_ip(source):
        to_avoid = cyclon.partialView.get_peer_by_ip(source)
    to_send = cyclon.partialView.select_neighbors(to_avoid, size)

    logger.info('I will send (to ' + message.get('source') + ') the following:\n' + str(
        to_send) + ".")

    for peer in to_send.get_peer_list():
        done = cyclon.partialView.remove_peer(peer)
        logger.info('I tried to remove ' + str(peer) + " -> " + str(done))

    logger.info('After having removed:\n' + str(cyclon.partialView))

    # Merge current partial view with the one just received
    cyclon.partialView.merge(received_partial_view)
    logger.info('After merged:\n' + str(cyclon.partialView))

    for peer in to_send.get_peer_list():
        if cyclon.partialView.contains(peer):
            p = cyclon.partialView.get_peer_by_ip(peer.ip)
            p.age = min(p.age, peer.age)
        else:
            cyclon.partialView.add_peer(peer)

    logger.info('I merged my view with the one received obtaining the following:\n' + str(
        cyclon.partialView) + ".")

    m = Message(format_address(my_ip(), 5000), message.get('source'), to_send)
    logger.info('Returning this:\n' + str(m.to_json()) + ".")
    return str(m.to_json())


if __name__ == '__main__':
    cyclon.bootstrap()
    app.run(debug=False, use_reloader=False, host='0.0.0.0')
