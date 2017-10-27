#!/usr/bin/env python2


import simplejson as json
from configuration import logger
from flask import Flask, request
from configuration import my_ip
from eptoApplication import EpTOApplication

# -----
# Global vars
# -----
app = Flask(__name__)
epto = EpTOApplication(my_ip())


@app.route('/receive-ball', methods=['POST'])
def receive_ball():
    global epto
    logger.info("I received this:\n" + str(request.get_json()))
    message_data = json.loads(request.get_json()).get('data')
    epto.dissemination.receive_ball(message_data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':

    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5001)
