import os
import json
from .models import epto
from .configuration import logger
from .helpers import my_ip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
            return JsonResponse({"success": {"message": "Hello, world! This is an EpTO peer running on " + my_ip() + "."}})
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


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
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


@csrf_exempt
def get_ball(request):
    if request.method == 'GET':
        if not request.GET:
            return JsonResponse(epto.dissemination.next_ball.to_json(), safe=False)
        else:
            return JsonResponse({"error": {"message": "The list of parameters has to be empty."}}, status=500)
    else:
        return JsonResponse({"error": {"message": "Only the GET method is allowed."}}, status=403)


# ---------------------
# Production routes
# The below routes are for production use.

@csrf_exempt
def receive_ball(request):
    if request.method == 'POST':
        logger.info("I received this:\n" + str(request.body))
        message = json.loads(request.body)
        epto.dissemination.receive_ball(message.get('data'))
        return JsonResponse({'success': True})
    else:
        return JsonResponse({"error": {"message": "Only the POST method is allowed."}}, status=403)


@csrf_exempt
def broadcast_event(request):
    if request.method == 'POST':
        logger.info("I received this:\n" + str(request.body))
        message = json.loads(request.body)
        epto.dissemination.broadcast(message.get('event'))
        return JsonResponse({'success': True})
    else:
        return JsonResponse({"error": {"message": "Only the POST method is allowed."}}, status=403)
