#!/usr/bin/env python2

import os
import json
from flask import Flask, request
from cyclon import Cyclon
from message.message import Message
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
    list_ips = cyclon.partialView.sample_ips(k)
    logger.info('I am returning a k-view:\n' + str(list_ips))
    return json.dumps(list_ips)


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
    logger.info('I got (from ' + message.get('source') + ') the following:\n' + str(received_partial_view))

    # 2) I send a subset of my partial view no matter if the source ip is contained in it
    to_send = cyclon.partialView.select_neighbors_for_reply()
    logger.info('I will send (to ' + message.get('source') + ') the following:\n' + str(to_send) + ".")

    # 3) I merge current partial view with the one just received
    cyclon.partialView.merge(to_send, received_partial_view)
    logger.info('After merged:\n' + str(cyclon.partialView))

    m = Message(format_address(my_ip(), 5000), message.get('source'), to_send)
    logger.info('Returning this:\n' + str(m.to_json()))
    return str(m.to_json())


if __name__ == '__main__':
    cyclon.bootstrap()
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)
