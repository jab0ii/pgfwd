# Author: Noah Gold

from django.test import TestCase, LiveServerTestCase
import os
import zmq
import json
import requests
import mox
import time
# Needed to build our test data
import eventProcessor
from page_sender import PageSender
import testData

APP_URL = os.environ['APP_URL']
FUNC_TEST_ENDPOINT = os.environ['FUNC_TEST_ENDPOINT']


class EventProcessorLive_test(LiveServerTestCase):

    def setUp(self):
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.PAIR)
        self.sock.bind(FUNC_TEST_ENDPOINT)
        self.poller = zmq.Poller()
        self.poller.register(self.sock, zmq.POLLIN)

        # Create test data
        testData.createTestData(self)

        # Set up mocks
        self.senderMox = mox.Mox()
        self.pageSender = self.senderMox.CreateMock(PageSender)
        self.eventProc = eventProcessor.EventProcessor(
            self.pageSender,
            eventProcessor.PageScheduler())

    def tearDown(self):
        self.poller.unregister(self.sock)
        self.sock.close()

    def testCreateEventEscalation(self):
        """
        Tests the createEvent Celery endpoint.
        Celery tasks run in the current process as blocking function calls.
        Desired behavior is asserted with the PageSender mock.
        """

        # setUp
        eventProcessor.app.conf.update(CELERY_ALWAYS_EAGER=True)
        liveEventProc = eventProcessor.liveEventProcessor
        eventProcessor.liveEventProcessor = self.eventProc

        # Prepare the mock
        self.pageSender.dispatch('uuid_active', self.userPCM, 0, self.details)
        self.pageSender.dispatch('uuid_active', self.secondUserPCM, 0,
                                 self.details)
        self.senderMox.ReplayAll()
        self.eventProc.createEvent('uuid_active', [self.userPCM], self.details,
                                   0)
        self.senderMox.VerifyAll()

        # tearDown
        eventProcessor.liveEventProcessor = liveEventProc
        eventProcessor.app.conf.update(CELERY_ALWAYS_EAGER=False)

    def testAPICreateEvent(self):
        """
        Tests to see if a simple ping is made successfully.
        """
        reqData = json.dumps({'handler': self.handlerID, 'apiKey': self.apiKey,
                              'eventDetails':
                              {'title': 'test event', 'message': 'test msg'}})

        response = requests.post(APP_URL + '/API/createEvent',
                                 reqData).json()

        expectedMessage = PageSender.appendAckInfo(response['uuid'],
                                                   self.userPCM,
                                                   'test msg')

        responses = [{'contactData': 'contact data',
                      'title': 'test event', 'message': expectedMessage}]

        self.assertResponses(responses)

    def testBasicEventEscalation(self):
        """
        Tests to see if a basic event escalation is handled properly.
        """
        reqData = json.dumps({'handler': self.escalationHandlerID,
                              'apiKey': self.apiKey,
                              'eventDetails':
                              {'title': 'test event', 'message': 'test msg'}})

        response = requests.post(APP_URL + '/API/createEvent',
                                 reqData).json()

        expectedMessage = PageSender.appendAckInfo(response['uuid'],
                                                   self.userPCM,
                                                   'test msg')
        expectedMessage2 = PageSender.appendAckInfo(response['uuid'],
                                                   self.secondUserPCM,
                                                   'test msg')
        responses = [{'contactData': 'contact data',
                      'title': 'test event', 'message': expectedMessage},
                     {'contactData': 'contact data escalation',
                      'title': 'test event', 'message': expectedMessage2}]

        self.assertResponses(responses)

    def testBasicAck(self):
        """
        Tests to see if a basic ack works by aligning timeouts.

        Only one response shoudl be received.
        """
        eventMessage = 'This is an event msg.'
        eventTitle = 'Test Ack.'
        reqData = json.dumps({'handler': self.ackHandlerID,
                              'apiKey': self.apiKey,
                              'eventDetails':
                              {'title': eventTitle, 'message': eventMessage}})

        eventResponse = requests.post(APP_URL + '/API/createEvent',
                                      reqData).json()

        time.sleep(3)

        #Send the ACK
        uuid = eventResponse['uuid']
        ackData = {'message': 'OK'}
        ackAppend = '/API/ackEvent/?uuid={uuid}&apiKey={apiKey}'
        ackURL = APP_URL + ackAppend.format(uuid=uuid, apiKey=self.apiKey)
        ackResponse = requests.post(ackURL, data=ackData)

        expectedMessage = PageSender.appendAckInfo(eventResponse['uuid'],
                                                   self.userPCM,
                                                   eventMessage)

        responses = [{'contactData': 'contact data',
                      'title': eventTitle, 'message': expectedMessage}]

        #BUG: if you don't ack, we should expect 2 message, but asserting
        #     only one response allows the test to pass
        #TODO: should I include the "Page has been acked!" in responses?

        self.assertResponses(responses)

    def assertResponses(self, responses):
        """
        Helper to assert that a given sequence of responses occur.

        Args:
            responses (list): list of responses to expect.
        """
        # Try to receive each response
        for i in range(len(responses)):
            response = responses[i]
            sockets = dict(self.poller.poll(1000))
            if self.sock in sockets:
                actualResp = json.loads(self.sock.recv())
                self.assertDictEqual(response, actualResp,
                                     "Response not expected.\n" +
                                     "Expected: " + str(response) + "\n" +
                                     "Got: " + str(actualResp))
            else:
                self.assertTrue(False, "No response available." + "\n" +
                                "Still expecting: " + str(responses[i:]))

        # Make sure that we don't have any extra messages
        sockets = self.poller.poll(1000)
        if self.sock in sockets:
            self.assertTrue(False, "Too many JSON responses.")
