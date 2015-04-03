# Author: Noah Gold, Jaspreet Singh

from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pageitforward.utils import createErrorDict, StatusCode, ObjectDoesNotExist
import json
from eventhandlers.models import EventHandlerData


@login_required
def APIEventHandlerUpdateDelete(request, handlerID):
    try:
        if request.method == 'POST':
            jsonData = json.loads(request.body)
            EventHandlerData.updateHandler(handlerID, jsonData['title'],
                                           jsonData['hierarchy'])
            return JsonResponse({'success': True, 'error': None})

        elif request.method == 'DELETE':
            EventHandlerData.deleteHandler(handlerID)
            return JsonResponse({'success': True, 'error': None})

        else:
            return JsonResponse({'error':
                                 createErrorDict(title='Invalid verb.')})

    except ObjectDoesNotExist:
        return JsonResponse({'error':
                            createErrorDict(title='Invalid handler.')})


@login_required
def APIEventHandlers(request):
    if request.method == 'GET':
        return APIGetEventHandlers(request)
    elif request.method == 'POST':
        return APICreateEventHandler(request)
    else:
        return JsonResponse({'error': createErrorDict(title='Invalid verb.')})


def APICreateEventHandler(request):
    jsonData = json.loads(request.body)
    handler = EventHandlerData.createHandler(jsonData['title'],
                                             jsonData['hierarchy'],
                                             request.user.org)
    return JsonResponse({'handlerID': handler.pk})


def APIGetEventHandlers(request):
    handlers = EventHandlerData.objects.filter(org=request.user.org,
                                               status=StatusCode.ACTIVE)

    handlerDicts = []
    for handler in handlers:
        handlerDicts.append(handler.toDict())

    return JsonResponse({'eventHandlers': handlerDicts, 'error': None})
