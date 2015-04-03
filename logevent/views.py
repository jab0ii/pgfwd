# Authors: Eric Jan
from pageitforward.utils import createErrorDict, StatusCode
from django.core.exceptions import ObjectDoesNotExist
from users.data_ex import UserPCM
from django.shortcuts import render
from django.utils.timezone import utc
from models import LogEvent
from users.models import UserData
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
import datetime
import json



# Create your views here.
@csrf_exempt
@require_POST
def APICreateLogEvent(request):
    
    """
    Creates the given Logevent in Celery.
    See Celery's createEvent for details on the required arguments.

    Arguments:
    "event uuid": uuid,
    "paged user": user,

    Returns
    "log_type":log type for this event
    "success": boolean
    "error" : Error object | null
    """
    
    returnInfo = {'log_type': StatusCode.NOEVENT, 'success': False, 'error': None}
    currTime = datetime.datetime.utcnow().replace(tzinfo=utc)
    #Load json object
    try:
        eventInfo = json.loads(request.body)
        uuid = eventInfo['uuid']
        acked = eventInfo['acked']
        user = eventInfo['userID']
        org = eventInfo['orgID']
    except (ValueError, KeyError) as e:
        returnInfo['error'] = createErrorDict(title='Bad parameters')
        return JsonResponse(returnInfo)
    
    #uuid lookup
    try:
        events = LogEvent.objects.filter(uuid = uuid)
        pagedEvents = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.PAGESENT)
    except ObjectDoesNotExist as e:
        returnInfo['error'] = createErrorDict(title='Bad parameters (uuid)')
        return JsonResponse(returnInfo)
    
    #create PAGESENT LOGEVENT
    if not acked and events.count() > 0:
        status = StatusCode.PAGESENT
        date_created = events[0].date_created
        newLog = LogEvent.createLog(uuid, date_created, status, org)
        newLog.date_sent = currTime
        newLog.user = user
        newLog.save()
        returnInfo['log_type'] = StatusCode.PAGESENT
        returnInfo['success'] = True
        return JsonResponse(returnInfo)
    
    #create ACK LOGEVENT
    elif acked and pagedEvents.count() > 0:
        ackedEvent = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.ACKED)
        if ackedEvent.count() > 0:
            returnInfo['error'] = createErrorDict(title='Event Already Acked')
            return JsonResponse(returnInfo)  
        else:
            log = LogEvent.createLog(uuid, currTime, StatusCode.ACKED, org)
            returnInfo['log_type'] = StatusCode.ACKED
            returnInfo['success'] = True
            return JsonResponse(returnInfo)

    #create NEW LOGEVENT
    else:
        log = LogEvent.createLog(uuid, currTime, StatusCode.EVENTCREATED, org)
        returnInfo['log_type'] = StatusCode.EVENTCREATED
        returnInfo['success'] = True
        return JsonResponse(returnInfo)

    

@login_required
@require_GET
def APIGetLogEvent(request):
    """
    Returns latest 100 events from descending order.
    
    Arg: User's OrgID
    
    Returns:
    *refer to model toDict params
    
    *time will return in %Y-%m-%d %H:%M:%S string format. 
    ex. '2014-11-22 00:11:22'
    
    TODO: Create Another API that returns user's associated events
    """
    
    returnInfo = {'success': False, 'error': None}

    try:
        orgid = request.user.org.pk
        logEvents = LogEvent.objects.filter(orgID = orgid).order_by('-id')[:100]
        
        logEventDicts = []
        for log in logEvents:            
            logEventDicts.append(log.toDict())
        return JsonResponse({'logEvents': logEventDicts, 'error': None})
             
    except (ValueError, KeyError) as e:
        returnInfo['error'] = createErrorDict(title='org DNE')
        return JsonResponse(returnInfo)
