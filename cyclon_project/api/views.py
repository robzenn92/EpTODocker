import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kubernetes.client import ApiClient
from .helpers import format_address, my_ip, who_am_i
from .models import cyclon
from .configuration import logger
from messages.message import Message
from partialView.partialView import PartialView


# ---------------------
# Debug routes
# The below routes are for debug use only.


@csrf_exempt
def get_hello(request):
    if request.method == 'GET':
        if not request.GET:
            return JsonResponse({"success": {"message": "Hello, world! This is a peer."}})
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=500)


@csrf_exempt
def get_who_am_i(request):
    if request.method == 'GET':
        if not request.GET:
            return JsonResponse(ApiClient().sanitize_for_serialization(who_am_i()), safe=False)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=500)


@csrf_exempt
def get_env(request):
    if request.method == 'GET':
        if not request.GET:
            response = {}
            for k in os.environ:
                response[k] = os.environ[k]
            return JsonResponse(response)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=500)


@csrf_exempt
def get_view(request):
    if request.method == 'GET':
        if not request.GET:
            return JsonResponse(cyclon.partialView.to_json(), safe=False)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=500)


# ---------------------
# Production routes
# The below routes are for production use.


@csrf_exempt
def get_k_view(request):
    if request.method == 'GET':
        k = int(request.GET.get('k'))
        if k:
            logger.info(str(cyclon.partialView))
            cyclon.partialView = cyclon.partialView.select_neighbors_for_request()
            list_ips = cyclon.partialView.sample_ips(k)
            logger.debug('I am returning a k-view:\n' + str(list_ips))
            return JsonResponse(list_ips, safe=False)
        else:
            return JsonResponse({"error": {"message": "You must specify the parameter k."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=500)


@csrf_exempt
def exchange_view(request):
    if request.method == 'POST':

        logger.info("My view before the exchange is:\n" + str(cyclon.partialView))

        # 1) I cast the received json into a PartialView
        message = json.loads(request.body)
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
        return JsonResponse(m.to_json())

    else:
        return JsonResponse({"error": {"message": "Only the POST method is allowed."}}, status=500)
