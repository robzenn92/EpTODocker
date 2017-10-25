#!/usr/bin/env python2

import os
import json
from flask import Flask, request
from cyclon import Cyclon
from messages.message import Message
from partialView.partialView import PartialView
from configuration import logger
from helpers import my_ip, format_address, who_am_i

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
    # logger.info('/k-view: I am returning this:\n' + str(cyclon.partialView))
    return str(view)


# Given a message containing a PartialView withing the data field
# Like in basic shuffling, the receiving peer replies by sending back a random subset of at most l neighbors.
# It then updates its own cache to accommodate all received entries.
# It does not increase, though, any entry's age until its own turn comes to initiate a shuffle.
@app.route('/exchange-view', methods=['POST'])
def exchange_view():

    global cyclon
    logger.info("My view before the exchange is:\n" + str(cyclon.partialView))

    # 1) I cast the received json into a PartialView
    message = json.loads(request.get_json())
    received_partial_view = PartialView.from_dict(message.get('data'))
    logger.info('I got (from ' + message.get('source') + ') the following:\n' + str(received_partial_view) + ".")

    try:
        assert received_partial_view.size == received_partial_view.shuffle_length
    except AssertionError:
        logger.critical('AssertionError (received_partial_view.size == received_partial_view.shuffle_length)')
        logger.critical('AssertionError (received_partial_view.size) was:\n' + str(received_partial_view.size))
        logger.critical('AssertionError (received_partial_view.shuffle_length) was:\n' + str(received_partial_view.shuffle_length))
        raise

    # 2) I check whether there is the source ip within my partialView. If so, I need to avoid it.
    # if cyclon.partialView.contains_ip(received_partial_view.ip):
    #     to_send = cyclon.partialView.select_neighbors_for_reply(
    #       cyclon.partialView.get_peer_by_ip(received_partial_view.ip)
    #     )
    # else:
    #     to_send = cyclon.partialView.select_neighbors_for_reply()

    # 2) I send a subset of my partial view no matter if the source ip is contained in it
    to_send = cyclon.partialView.select_neighbors_for_reply()
    logger.info('I will send (to ' + message.get('source') + ') the following:\n' + str(to_send) + ".")

    try:
        assert to_send.size == received_partial_view.size
    except AssertionError:
        logger.critical('AssertionError (to_send.size == received_partial_view.size)')
        logger.critical('AssertionError (to_send.size) was:\n' + str(to_send.size))
        logger.critical('AssertionError (received_partial_view.size) was:\n' + str(received_partial_view.size))
        raise

    # 3) I remove from my view the peers I want to send
    for peer in to_send.get_peer_list():
        cyclon.partialView.remove_peer(peer)
    logger.info('After having removed:\n' + str(cyclon.partialView))

    # 4) I merge current partial view with the one just received
    cyclon.partialView.merge(to_send, received_partial_view)
    logger.info('After merged:\n' + str(cyclon.partialView))

    # # 5) If there is still space in my view I add the peers I removed before
    # for peer in to_send.get_peer_list():
    #     # If peer is not contained in my view it is going to be added
    #     # Otherwise its age is updated with the minimum value between the two descriptors
    #     if not cyclon.partialView.contains(peer):
    #         cyclon.partialView.add_peer(peer)
    #     else:
    #         p = cyclon.partialView.get_peer_by_ip(peer.ip)
    #         p.age = min(p.age, peer.age)
    # logger.info('I merged my view with the one received. The result is:\n' + str(cyclon.partialView) + ".")

    m = Message(format_address(my_ip(), 5000), message.get('source'), to_send)
    logger.info('Returning this:\n' + str(m.to_json()))
    return str(m.to_json())


if __name__ == '__main__':
    cyclon.bootstrap()
    app.run(debug=False, use_reloader=False, host='0.0.0.0')
