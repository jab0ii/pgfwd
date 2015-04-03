# Authors: Eric Jan

from django.test import TestCase

# Create your tests here.
from pageitforward.utils import createErrorDict, StatusCode
from django.utils import timezone
import pytz
from models import LogEvent
import time
import datetime
from django.utils.timezone import utc

class LogEvent_test(TestCase):

    def setUp(self):        
        
        #event1 created
        currTime = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)
        dateSent = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)
        dateAck = datetime.datetime.utcnow().replace(tzinfo=utc)
        LogEvent.objects.create(uuid = 'event1',
                                orgID = 4,
                                date_created = currTime,
                                log_type = StatusCode.EVENTCREATED)
        LogEvent.objects.create(uuid = 'event1',
                                user = 1,
                                orgID = 4,
                                date_created = currTime,
                                date_sent = dateSent,
                                log_type = StatusCode.PAGESENT)
        LogEvent.objects.create(uuid = 'event1',
                                user = 1,
                                orgID = 4,
                                date_created = currTime,
                                date_sent = dateSent,
                                date_ack = dateAck,
                                log_type = StatusCode.ACKED)
        
        #event2
        time.sleep(0.1)
        currTime = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)
        dateSent = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.2)
        dateAck = datetime.datetime.utcnow().replace(tzinfo=utc)
        LogEvent.objects.create(uuid = 'event2',
                                orgID = 4,
                                date_created = currTime,
                                log_type = StatusCode.EVENTCREATED)
        
        LogEvent.objects.create(uuid = 'event2',
                                user = 1,
                                orgID = 4,
                                date_created = currTime,
                                date_sent = dateSent,
                                log_type = StatusCode.PAGESENT)
        LogEvent.objects.create(uuid = 'event2',
                                user = 1,
                                orgID = 4,
                                date_created = currTime,
                                date_sent = dateSent,
                                date_ack = dateAck,
                                log_type = StatusCode.ACKED)
        
        LogEvent.setTimeDiff('event1')
        LogEvent.setTimeDiff('event2')



    def teardown(self):
        pass
    
    
    def testCreateLog(self):
        dateCreated= datetime.datetime.utcnow().replace(tzinfo=utc)
        newLog = LogEvent.createLog('test', dateCreated, StatusCode.EVENTCREATED, 4)
        obj = LogEvent.objects.filter(uuid = 'test')
        testObj = obj[0]
        self.assertTrue(obj.count() > 0)
        self.assertEqual(testObj.date_created, dateCreated)
        self.assertEqual(testObj.log_type, StatusCode.EVENTCREATED)
        self.assertEqual(testObj.uuid, 'test')
        self.assertEqual(testObj.orgID, 4)

        
    def testSetTimeDiff(self):
        currTime = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)
        dateSent = datetime.datetime.utcnow().replace(tzinfo=utc)
        time.sleep(0.1)
        dateAck = datetime.datetime.utcnow().replace(tzinfo=utc)
        LogEvent.objects.create(uuid = 'eventTest',
                                user = 2,
                                orgID = 4,
                                date_created = currTime,
                                date_sent = dateSent,
                                date_ack = dateAck,
                                log_type = StatusCode.ACKED)
        LogEvent.setTimeDiff('eventTest')
        obj = LogEvent.objects.get(uuid = 'eventTest')
        self.assertTrue(obj.time_diff > 0)
        
    def testGetAvgTimeDiff(self):
        avgTime = LogEvent.getAvgTimeDiff(1)
        self.assertTrue(avgTime > 0.0001)
    
    def testTimeDiff(self):
        timeDiff = LogEvent.getTimeDiff('event1')
        self.assertTrue(timeDiff > 0.0001)
        
    #Same event different log_type
    def testMultiLog(self):
        userObj = LogEvent.objects.filter(user = 1)
        eventObj = LogEvent.objects.filter(uuid = 'event1')
        self.assertEqual(userObj.count(), 4)
        self.assertEqual(eventObj.count(), 3)

        
        
        