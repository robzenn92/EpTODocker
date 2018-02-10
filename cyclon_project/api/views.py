import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kubernetes.client import ApiClient
from .helpers import format_address, my_ip, who_am_i
from .models import cyclon
from .configuration import logger
from message.message import Message
from partialView.partialView import PartialView

# HTTP Status
# 403 : Forbidden
# 500 : Internal Server Error

# ---------------------
# Debug routes
# The below routes are for debug use only.

@csrf_exempt
def get_hello(request):
    if request.method == 'GET':
        if not request.GET:
            logger.info("Hello")
            return JsonResponse({"success": {"message": "Hello, world! This is a Cyclon peer running on " + my_ip() + "."}})
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


@csrf_exempt
def get_who_am_i(request):
    if request.method == 'GET':
        if not request.GET:
            logger.info("WhoAmI")
            return JsonResponse(ApiClient().sanitize_for_serialization(who_am_i()), safe=False)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


@csrf_exempt
def get_env(request):
    if request.method == 'GET':
        if not request.GET:
            logger.info("Env")
            response = {}
            for k in os.environ:
                response[k] = os.environ[k]
            return JsonResponse(response)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


@csrf_exempt
def get_view(request):
    if request.method == 'GET':
        if not request.GET:
            logger.info("View")
            return JsonResponse(cyclon.partialView.to_json(), safe=False)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


# ---------------------
# Production routes
# The below routes are for production use.


@csrf_exempt
def get_k_view(request):
    if request.method == 'GET':
        logger.info("kView")
        k = int(request.GET.get('k'))
        if k:
            logger.debug("GetKView", request=request, partialView=cyclon.partialView)
            list_ips = cyclon.partialView.sample_ips(k)
            logger.debug("GetKView", list_ips=list_ips)
            return JsonResponse(list_ips, safe=False)
        else:
            return JsonResponse({"error": {"message": "You must specify the parameter k."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


@csrf_exempt
def exchange_view(request):
    if request.method == 'POST':

        logger.info("ExchangeView")
        logger.debug("ExchangeView", request=request, partialView=cyclon.partialView)

        # 1) I cast the received json into a PartialView
        logger.debug("ExchangeView: I cast the received json into a PartialView.")
        message = json.loads(request.body)
        received_partial_view = PartialView.from_dict(message.get('data'))

        # 2) I send a subset of my partial view no matter if the source ip is contained in it
        logger.debug("ExchangeView: I send a subset of my partial view no matter if the source ip is contained in it.")
        to_send = cyclon.partialView.select_neighbors_for_reply()

        # 3) I merge current partial view with the one just received
        logger.debug("ExchangeView: I merge current partial view with the one just received.")
        cyclon.partialView.merge(to_send, received_partial_view)
        logger.debug("ExchangeView", partialView=cyclon.partialView)

        m = Message(format_address(my_ip(), 5000), message.get('source'), to_send)
        logger.debug("ExchangeView", response=m.to_json(), to=message.get('source'))
        return JsonResponse(m.to_json())

    else:
        return JsonResponse({"error": {"message": "Only the POST method is allowed."}}, status=403)
