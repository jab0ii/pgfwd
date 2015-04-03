#Author: Eric Jan
from django.test import TestCase, LiveServerTestCase
import os
import json
import requests
from models import (EventHandlerData, HierarchyLevelDoesNotExist,
                    HierarchyExhausted)
from users.models import UserData, ContactMethodData
from orgs.models import OrgData
from pageitforward.utils import createErrorDict, StatusCode, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.test.client import Client
from django.contrib.auth.models import User

    
APP_URL = os.environ['APP_URL']

class evenhandlersApi_Test(LiveServerTestCase):

    def setUp(self):
        testOrg = OrgData(orgName='Test org',
                          status=1)
        testOrg.pk = 3
        testOrg.save()
      
        self.testUser = UserData.createUser('Test', 'Tester', 
                                       'testEvenH@gg.com', 'pw')
        self.testUser.org = testOrg
        self.testUser.apiKey = 'TESTAPIKEY2'
        self.testUser.save()

        self.hierarchy = '{"numLevels":1,"levels":{"0":{"timeout":30,\
                    "users":[' + str(self.testUser.pk) + ']}}}'
        
        testContactMethod = ContactMethodData(user=self.testUser,
                                              contactType='email',
                                              contactData='testEvenH@gg.com',
                                              priority=0)
        testContactMethod.save()
       
        newHandler = EventHandlerData(title='TestHandler',
                                      hierarchy=self.hierarchy,
                                      org=testOrg)
        newHandler.pk = 5
        newHandler.save()

        self.client = Client()

        log = self.client.login(username='testEvenH@gg.com',
                          password='pw')
        
        s = self.client.session
        s['swag'] = 69
        s.save()
        
    def tearDown(self):
        pass
    
    def test_APIEventHandlers_POST(self):
        eventData = json.dumps({'title': 'TestHandler2',
                                'hierarchy': self.hierarchy})
        
        response = self.client.post(APP_URL +'/API/eventhandlers',
                                    eventData,
                                    content_type = "application/json")

        self.assertTrue(json.loads(response.content)['handlerID'] > 0)

    
    def test_APIEventHandlerUpdate(self):
        updateData = json.dumps({'title': 'TestHandlerUpdate',
                                 'hierarchy':self.hierarchy})
        
        response = self.client.post(APP_URL + '/API/eventhandlers/5',
                                 updateData,
                                 content_type = "application/json")
        responses = {'success': True, 'error': None}
        
        self.assertEqual(responses, json.loads(response.content))
        
    def test_APIEventHandlerUpdate_Error(self):

            updateData = json.dumps({'title': 'TestHandlerUpdate',
                                     'hierarchy':self.hierarchy})
            
            response = self.client.post(APP_URL + '/API/eventhandlers/2',
                                 updateData,
                                 content_type = "application/json")

            responses= {'error':
                            createErrorDict(title='Invalid handler.')}
            
            self.assertEqual(responses, json.loads(response.content))
            
    def test_APIEventHandlers_GET(self):
        handlerDicts = [{'eventHandlerID': 5,
                         'title': 'TestHandler',
                'hierarchy': json.loads(self.hierarchy),
                'orgID': 3}]
        
        responses = {'eventHandlers': handlerDicts,
                     'error': None}
        
        response = self.client.get(APP_URL + '/API/eventhandlers',
                                   content_type = "application/json")
        
        self.assertEqual(responses, json.loads(response.content))
    


