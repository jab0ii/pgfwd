#author: Eric Jan
from django.test import TestCase, LiveServerTestCase
from models import LogEvent
from pageitforward.utils import createErrorDict, StatusCode
from django.utils import timezone
import pytz
import time
import datetime
from django.utils.timezone import utc
import os
import json
import requests

from django.contrib.auth.decorators import login_required
from pageitforward.utils import createErrorDict
from users.models import UserData, ContactMethodData
from pageitforward.utils import createErrorDict, StatusCode, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.test.client import Client
from django.contrib.auth.models import User
from orgs.models import OrgData
from eventhandlers.models import EventHandlerData
from events.models import EventData

APP_URL = os.environ['APP_URL']
creationTime = datetime.datetime.utcnow().replace(tzinfo=utc)
time.sleep(0.1)
class LogEventApi_Test(LiveServerTestCase):

    def setUp(self):      
        LogEvent.objects.create(uuid = 'event1',
                                date_created = creationTime,
                                log_type = StatusCode.EVENTCREATED,
                                orgID = 3)

        
        self.testOrg = OrgData(orgName='Test org',
                          status=1)
        self.testOrg.save()
      
        self.testUser = UserData.createUser('Test', 'Tester', 
                                       'testlog@gi.com', 'pw')
        self.testUser.org = self.testOrg
        self.testUser.apiKey = 'TESTAPIKEY4'
        self.testUser.save()

        self.hierarchy = '{"numLevels":1,"levels":{"0":{"timeout":30,\
                    "users":[' + str(self.testUser.pk) + ']}}}'
        
        testContactMethod = ContactMethodData(user=self.testUser,
                                              contactType='email',
                                              contactData='testlog@gi.com',
                                              priority=0)
        testContactMethod.pk = 7
        testContactMethod.save()
       
        self.newHandler = EventHandlerData(title='TestHandler',
                                      hierarchy=self.hierarchy,
                                      org=self.testOrg)
        self.newHandler.pk = 5
        self.newHandler.save()
        
        self.client = Client()

        log = self.client.login(username='testlog@gi.com',
                          password='pw')
        s = self.client.session
        s['abc'] = 31
        s.save()
        
   
        
    def tearDown(self):
        pass
    
    
    def test_CreateLogEvent_API_PAGESENT(self):

        logData = json.dumps({'uuid': 'event1', 'acked': False, 'userID': 1, 'orgID': 2})
        
        response = requests.post(APP_URL + '/API/createLogEvent',
                                 logData).json()
        
        responses = {'log_type': StatusCode.PAGESENT, 'success': True, 'error': None}

        self.assertEqual(responses, response)
        

    
    def test_CreateLogEvent_API_ACK(self):
        currTime = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)

        LogEvent.objects.create(uuid = 'event1',
                                date_sent = currTime,
                                date_created = creationTime,
                                log_type = StatusCode.PAGESENT,
                                orgID = 3)
        
        logData = json.dumps({'uuid': 'event1', 'acked': True, 'userID': 1, 'orgID': 2})
        
        response = requests.post(APP_URL + '/API/createLogEvent',
                                 logData).json()

        responses = {'log_type': StatusCode.ACKED, 'success': True, 'error': None}
        
        obj = LogEvent.objects.filter(uuid = 'event1', log_type = StatusCode.ACKED)
        
        self.assertTrue(obj.count() > 0)
        self.assertEqual(responses, response)

    def test_CreateLogEvent_API_CREATE(self):
        
        logData = json.dumps({'uuid': 'event2', 'acked': False, 'userID': 1, 'orgID': 2})
        
        response = requests.post(APP_URL + '/API/createLogEvent',
                                 logData).json()
        
        responses = {'log_type': StatusCode.EVENTCREATED, 'success': True, 'error': None}

        
        self.assertEqual(responses, response)

        
    def test_APIGetLogEvent(self):
        EventData.objects.create(uuid = 'event7',
                                 title = 'event1',
                                 message = 'test1',
                                 handler = self.newHandler,
                                 currentPos = 1,
                                 status = 1)
        
        EventData.objects.create(uuid = 'event8',
                                 title = 'event2',
                                 message = 'test1',
                                 handler = self.newHandler,
                                 currentPos = 1,
                                 status = 1)
        EventData.objects.create(uuid = 'event9',
                                 title = 'event3',
                                 message = 'test1',
                                 handler = self.newHandler,
                                 currentPos = 1,
                                 status = 1)
        
        LogEvent.objects.create(uuid = 'event7',
                                date_created = creationTime,
                                log_type = StatusCode.EVENTCREATED,
                                orgID =  self.testOrg.pk)
        LogEvent.objects.create(uuid = 'event8',
                                date_created = creationTime,
                                log_type = StatusCode.EVENTCREATED,
                                orgID =  self.testOrg.pk)
        LogEvent.objects.create(uuid = 'event9',
                                date_created = creationTime,
                                log_type = StatusCode.EVENTCREATED,
                                orgID =  self.testOrg.pk)
        
        response = self.client.get(APP_URL + '/API/getLogEvent',
                                   content_type = "application/json")
        
        self.assertEqual(json.loads(response.content)['error'], None)