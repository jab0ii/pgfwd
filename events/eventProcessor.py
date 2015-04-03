# Author: Noah Gold, Eric Jan
# Resources used:
#       http://documentation.mailgun.com/quickstart-sending.html#send-via-smtp


import os
import celery
import requests
import json
from pageitforward.utils import ErrorCode
from page_sender import PageSender


# You must import classes that are used as task parameters
# otherwise Celery cannot find them on the path.
# There is probably a way to fix this, so consider this a workaround.
from users.data_ex import ContactMethod, UserPCM
from data_ex import EventDetails
from datetime import datetime



# Create the Celery app
app = celery.Celery('events.eventProcessor')
app.conf.update(BROKER_URL=os.environ['CLOUDAMQP_URL'])
app.conf.update(BROKER_POOL_LIMIT=int(os.environ['CELERY_BROKER_POOL_LIMIT']))

# Fetch the URL of the Django app
APP_URL = os.environ['APP_URL']


# *********************************************
# Celery Tasks
#   All tasks simply call the EventProcessor
#   instance. Look to that class for docs.
# *********************************************
@app.task
def pageUser(uuid, eventDetails, user, contactIndx, escalateTime):
    liveEventProcessor.pageUser(uuid, eventDetails, user,
                                contactIndx, escalateTime)


@app.task
def escalateEvent(uuid, eventDetails):
    liveEventProcessor.escalateEvent(uuid, eventDetails)


@app.task
def createEvent(uuid, users, eventDetails, escalateTime):
    liveEventProcessor.createEvent(uuid, users, eventDetails, escalateTime)


@app.task
def pageUserCM(user, contactIndx, eventDetails):
    liveEventProcessor.pageUserCM(user, contactIndx, eventDetails)


class EventProcessor:
    """
    Encapsulates logic used by the Celery tasks.
    """

    def __init__(self, pageSender, scheduler):
        """
        Args:
            pageSender: instance of the page sender class.
        """
        self.pageSender = pageSender
        self.scheduler = scheduler

    def escalateEvent(self, uuid, eventDetails):
        """
        Escalates the event identified by the given uuid.
        Args:
            uuid (str): identifies the event.
            eventDetails: EventDetails instance for the given event.
        """

        reqData = json.dumps({'uuid': uuid})
        escalationData = requests.post(APP_URL + '/API/getEscalationData',
                                       reqData).json()

        # Did anything go wrong?
        if escalationData['error'] is None:

            # If the event hasn't been acked, page the next level
            if not escalationData['acked']:
                timeout = escalationData['timeout']
                for rawUserPCM in escalationData['users']:
                    user = UserPCM.fromDict(rawUserPCM)
                    self.scheduler.pageUser.delay(uuid, eventDetails,
                                                  user, 0, timeout)

                self.scheduler.escalateEvent.apply_async(
                    args=[uuid, eventDetails],
                    countdown=timeout)
            else:
                # Event acked, nothing for us to do
                pass

        elif escalationData['error']['errorCode'] == ErrorCode.HIER_EXHAUSTED:
            # No more users to page. Nothing for us to do.
            pass
        else:
            # TODO: This should never happen. Log it.
            pass

    def pageUser(self, uuid, eventDetails, user, contactIndx, escalateTime):
        """
        Pages the given user, and escalates through their contact methods.
        Args:
            uuid (str): identifies the event.
            eventDetails: EventDetails instance for the given event.
            user (UserPCM): user to page.
            contactIndx (int): contact index to page.
            escalateTime (int): time to wait, in seconds, before escalating
                                the event.
        """
        # We're done paging this user
        if contactIndx >= len(user.contactMethods):
            return

        reqData = json.dumps({'uuid': uuid})
        eventStatus = requests.post(APP_URL + '/API/getEventStatus',
                                    reqData).json()
        
        #logEvent
        userID = user.toDict()['user']
        orgID = user.toDict()['orgID']
        #userObj = UserData.objects.filter(id = userID)
        #if userObj.count() > 0:
        #theuser = userObj[0]
        status = eventStatus['acked']
        logData = json.dumps({'uuid': uuid, 'acked': status, 'userID': userID, 'orgID' : orgID})
        eventLog = requests.post(APP_URL + '/API/createLogEvent', logData).json()
        
        # Verify that the API request was successful, and page the user
        if eventStatus['error'] is None:
            if not eventStatus['acked']:
                self.pageSender.dispatch(user, 
                                         contactIndx, 
                                         eventDetails,
                                         uuid=uuid)
                self.scheduler.pageUser.apply_async(args=[uuid, eventDetails,
                                                    user, contactIndx + 1,
                                                    escalateTime],
                                                    countdown=escalateTime /
                                                    len(user.contactMethods))
            else:
                # Page acked, nothing for us to do
                pass
        else:
            # TODO: This should never happen. Log it.
            pass

    def createEvent(self, uuid, users, eventDetails, escalateTime):
        """
        Creates an event in the processing queue.
        Args:
            uuid (str): identifies the event.
            users (list): list of UserPCM objects, which are the first users to
                          page.
            eventDetails (EventDetails): Details for the given event.
            escalateTime (int): time to wait, in seconds, before
                                escalating the event.
        """
        for user in users:
            self.scheduler.pageUser.delay(uuid, eventDetails, user, 0,
                                          escalateTime)

        self.scheduler.escalateEvent.apply_async(args=[uuid, eventDetails],
                                                 countdown=escalateTime)

    def pageUserCM(self, user, contactIndx, eventDetails):
        """
        Pages the contact method refered to by contactIndx.

        Args:
            user (UserPCM):    user to page
            contactIndx (int): index of the CM to page
        """
        if contactIndx < len(user.contactMethods):
            self.pageSender.dispatch(user, contactIndx, eventDetails)
        else:
            # TODO: Invalid contact index. Log it.
            pass


class PageScheduler:
    """
    Wrapper around Celery tasks.
    """
    def __init__(self):
        self.pageUser = pageUser
        self.createEvent = createEvent
        self.escalateEvent = escalateEvent
        self.pageUserCM = pageUserCM


# Create the event processor instance used by the Celery tasks
liveEventProcessor = EventProcessor(PageSender(), PageScheduler())
