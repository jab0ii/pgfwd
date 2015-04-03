# Authors: Jay Kong, Noah Gold, Eric Jan

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import EventData
from users.models import UserData
from users.data_ex import ContactMethod, UserPCM
from logevent.models import LogEvent
from eventhandlers.models import EventHandlerData, HierarchyLevelDoesNotExist
from events.models import EventData
from pageitforward.utils import createErrorDict, StatusCode
from django.core.exceptions import ObjectDoesNotExist
import json
import uuid
import eventProcessor
from data_ex import EventDetails
from django.utils import timezone
import datetime
from django.utils.timezone import utc
from forms import AckForm


@csrf_exempt
@require_POST
def APIGetEventStatus(request):
    uuid = json.loads(request.body)['uuid']
    statusInfo = EventData.getEventStatus(uuid)
    return JsonResponse(statusInfo)


@csrf_exempt
@require_POST
def APIGetEscalationData(request):
    uuid = json.loads(request.body)['uuid']
    escalationData = EventData.getEscalationData(uuid)
    return JsonResponse(escalationData)


@csrf_exempt
def APIAckEvent(request):
    """
    Acks the current event to stop further escalations. Following this,
    all paged users are then notified of the acknowledgement.

    Arguments:
    "uuid" : string,
    "apiKey" : string,
    "message": string

    Returns
    "success": boolean
    "error": Error object | null
    """
    returnInfo = {'success': False, 'error': None}
    event_uuid = request.GET.get('uuid', None)
    apiKey = request.GET.get('apiKey', None)
    currtime = datetime.datetime.utcnow().replace(tzinfo=utc)

    def _ackAuthenticateAndGetEvent():
        """
        Helper method to authenticate against event_uuid and apiKey
        """
        if (event_uuid is None) or (apiKey is None):
            returnInfo['error'] = createErrorDict(title='Bad PARAM')
            return JsonResponse(returnInfo)
        #ApiKey lookup
        try:
            user = UserData.objects.get(apiKey=apiKey)
        except ObjectDoesNotExist as e:
            returnInfo['error'] = createErrorDict(title='Bad PARAM (APIK)')
            return False
        #Event lookup
        try:
            event = EventData.objects.get(uuid=event_uuid)
        except ObjectDoesNotExist as e:
            returnInfo['error'] = createErrorDict(title='Bad PARAM (uuid)')
            return False
        #Check if user has access to this event, TODO: any user in org can ack event
        try:
            handler = EventHandlerData.objects.get(pk=event.handler.pk, 
                                                   org=user.org)
        except ObjectDoesNotExist as e:            
            returnInfo['error'] = createErrorDict(title='Bad PARAM (access)')
            return False

        if event.status == StatusCode.ACKED:
            returnInfo['error'] = createErrorDict(title='Already Acked')
            return False

        return event

    def _notifyAck(handler, currentPos, message):
        """
        Helper method to notify all those who have been paged.
        """
        wrappedMessage = EventDetails('Page has been acked!',
                                      message)

        for level in xrange(currentPos+1):
            users = handler.getUserPCMOfLevel(level)
            for user in users:
                eventProcessor.pageUserCM(user, 0, wrappedMessage)

    if request.method == 'GET': #Generate form view
        event = _ackAuthenticateAndGetEvent()
        if not event:
            return JsonResponse(returnInfo)

        form = AckForm(label_suffix='')
        return render(request, 
                      'pageitforward/ack_template.html', 
                      {'form': form})

    elif request.method == 'POST': #Form post
        event = _ackAuthenticateAndGetEvent()
        if not event:
            return JsonResponse(returnInfo)

        form = AckForm(request.POST)        
        if form.is_valid():
            #Ack event
            event.status = StatusCode.ACKED
            event.save()
            
            user = UserData.objects.get(apiKey=apiKey)

            log = LogEvent.createLog(event_uuid, currtime, StatusCode.ACKED, user.org.pk)

            _notifyAck(event.handler, event.currentPos, 
                       form.cleaned_data['message'])
            returnInfo['success'] = True
            return JsonResponse(returnInfo)


@csrf_exempt
@require_POST
def APICreateEvent(request):
    """
    Creates the given event in Celery (calls Celery's createEvent).
    See Celery's createEvent for details on the required arguments.

    Arguments:
    "handler": integer,
    "eventDetails": EventDetailJSON,
    "apikey": string

    Returns
    "success": boolean
    "error" : Error object | null
    """
    returnInfo = {'success': False, 'error': None}

    # Load data
    try:
        createEventArgs = json.loads(request.body)
        handler_id = createEventArgs['handler']
        eventDetails = EventDetails(createEventArgs['eventDetails']['title'],
                                    createEventArgs['eventDetails']['message'])
        title = eventDetails.title
        message = eventDetails.message
        apiKey = createEventArgs['apiKey']
    except (ValueError, KeyError) as e:
        returnInfo['error'] = createErrorDict(title='Bad parameters')
        return JsonResponse(returnInfo)

    # ApiKey lookup
    try:
        user = UserData.objects.get(apiKey=apiKey)
    except ObjectDoesNotExist as e:
        returnInfo['error'] = createErrorDict(title='Bad parameters (APIKey)')
        return JsonResponse(returnInfo)

    # Handler lookup
    try:
        handler = EventHandlerData.objects.get(pk=handler_id, org=user.org,
                                               status=StatusCode.ACTIVE)
    except ObjectDoesNotExist as e:
        returnInfo['error'] = createErrorDict(title='Bad parameters (Handler)')
        return JsonResponse(returnInfo)

    # Get UserPCM objects
    initialLevel = 0
    try:
        users = handler.getUserPCMOfLevel(initialLevel)
        escalateTime = handler.getEscalateTimeOfLevel(initialLevel)
    except HierarchyLevelDoesNotExist as e:
        returnInfo['error'] = createErrorDict(title='No hierarchy defined')
        return JsonResponse(returnInfo)

    # Create Django event; TODO: perhaps abstract this some more
    eventUUID = str(uuid.uuid4())
    
    newEvent = EventData.objects.create(uuid=eventUUID, 
                                        title=title, 
                                        message=message, 
                                        handler_id=handler_id, 
                                        currentPos=initialLevel, 
                                        status=StatusCode.ACTIVE)

    # Create Celery event
    eventProcessor.createEvent(eventUUID, users, eventDetails, escalateTime)
    
    # Create a new log with current time
    currtime = datetime.datetime.utcnow().replace(tzinfo=utc)
    orgID = user.org.pk
    log = LogEvent.createLog(eventUUID, currtime, StatusCode.EVENTCREATED, orgID)
    
    returnInfo['success'] = True
    returnInfo['uuid'] = eventUUID
    return JsonResponse(returnInfo)
    #TODO: update docs with error codes
