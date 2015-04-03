# Authors: Jay Kong, Noah Gold

from django.test import TestCase, LiveServerTestCase
from models import EventData
from eventhandlers.models import EventHandlerData
from orgs.models import OrgData
from pageitforward.utils import createErrorDict, StatusCode
from eventProcessor import EventProcessor, PageSender, PageScheduler
import testData
import uuid
import json
import mox


class EventData_test(TestCase):

    def setUp(self):
        org = OrgData.objects.create(status=0)

        handler = EventHandlerData.objects.create(org=org)

        EventData.objects.create(uuid='uuid_active', title='active title',
                                 message='active message', currentPos=0,
                                 status=StatusCode.ACTIVE, handler=handler)

        EventData.objects.create(uuid='uuid_acked', title='acked title',
                                 message='acked message', currentPos=0,
                                 status=StatusCode.ACKED, handler=handler)

        EventData.objects.create(uuid='uuid_invalidstatus', title='title',
                                 message='message', currentPos=0,
                                 status=-1, handler=handler)

    def tearDown(self):
        pass

    def testGetEventStatusAcked(self):
        statusInfo = EventData.getEventStatus('uuid_acked')
        expected = {'acked': True, 'error': None}
        self.assertDictEqual(expected, statusInfo)

    def testGetEventStatusInvalidEvent(self):
        statusInfo = EventData.getEventStatus('uuid_invalid')
        expected = {'acked': None, 'error':
                    createErrorDict(title='Event does not exist.')}
        self.assertDictEqual(expected, statusInfo)

    def testGetEscalationDataAcked(self):
        escalationInfo = EventData.getEscalationData('uuid_acked')
        expected = {'acked': True, 'error': None, 'users': None}
        self.assertDictEqual(expected, escalationInfo)

    def testGetEscalationDataInvalidEvent(self):
        escalationInfo = EventData.getEscalationData('uuid_invalid')
        expected = {'acked': None, 'error':
                    createErrorDict(title='Event does not exist.'),
                    'users': None}
        self.assertDictEqual(expected, escalationInfo)

    def testGetEscalationDataInvalidStatus(self):
        escalationInfo = EventData.getEscalationData('uuid_invalidstatus')
        expected = {'acked': None, 'error':
                    createErrorDict(title='Invalid event status.',
                                    errorCode=-1),
                    'users': None}
        self.assertDictEqual(expected, escalationInfo)


class EventProcessor_test(LiveServerTestCase):

    def setUp(self):
        # Create the mocks
        self.senderMox = mox.Mox()
        self.pageSender = self.senderMox.CreateMock(PageSender)
        self.scheduler = PageScheduler()
        self.schedulerMox = mox.Mox()
        self.scheduler.pageUser = self.schedulerMox.CreateMockAnything()
        self.scheduler.createEvent = self.schedulerMox.CreateMockAnything()
        self.scheduler.escalateEvent = self.schedulerMox.CreateMockAnything()
        self.eventProc = EventProcessor(self.pageSender, self.scheduler)

        # Create data
        testData.createTestData(self)

    def tearDown(self):
        pass

    def testPageUser(self):
        self.pageSender.dispatch(self.userPCM, 0,
                                 self.details, uuid='uuid_active')
        self.scheduler.pageUser.apply_async(args=['uuid_active',
                                                  self.details,
                                                  self.userPCM, 1, 0],
                                            countdown=0)
        self.senderMox.ReplayAll()
        self.schedulerMox.ReplayAll()
        self.eventProc.pageUser('uuid_active', self.details,
                                self.userPCM, 0, 0)
        self.senderMox.VerifyAll()
        self.schedulerMox.VerifyAll()

    def testEscalateEvent(self):
        self.scheduler.pageUser.delay('uuid_active', self.details,
                                      self.secondUserPCM, 0, 0)
        self.scheduler.escalateEvent.apply_async(
            args=['uuid_active', self.details], countdown=0)
        self.schedulerMox.ReplayAll()
        self.eventProc.escalateEvent('uuid_active', self.details)
