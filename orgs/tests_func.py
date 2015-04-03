#Author: Eric Jan
from django.test import TestCase, LiveServerTestCase
import os
import json
import requests

from users.models import UserData, ContactMethodData
from models import OrgData
from pageitforward.utils import createErrorDict, StatusCode, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.test.client import Client
from django.contrib.auth.models import User

APP_URL = os.environ['APP_URL']
class OrgApi_Test(LiveServerTestCase):
    
    def setUp(self):
        testOrg = OrgData(orgName='Test org',
                          status=1)
        testOrg.pk = 2
        testOrg.save()
      
        self.testUser = UserData.createUser('Test',
                                            'Tester', 
                                       'testEvenH@gi.com',
                                       'pw')
        self.testUser.org = testOrg
        self.testUser.apiKey = 'TESTAPIKEY3'
        self.testUser.save()

        self.hierarchy = '{"numLevels":1,"levels":{"0":{"timeout":30,\
                    "users":[' + str(self.testUser.pk) + ']}}}'
        
        testContactMethod = ContactMethodData(user=self.testUser,
                                              contactType='email',
                                              contactData='testEvenH@gg.com',
                                              priority=0)
        testContactMethod.save()
       

        self.client = Client()

        log = self.client.login(username='testEvenH@gi.com',
                          password='pw')
        s = self.client.session
        s['swag'] = 55
        s.save()

    def tearDown(self):
        pass
    
    def test_APIOrgsGet(self):
        
        responses = {'org': {'orgID': 2,
                             'orgName': 'Test org',
                'status': 1},
                             'error': None}
        
        response = self.client.get(APP_URL + '/API/orgs/2',
                                   content_type = "application/json")
        self.assertEqual(responses, json.loads(response.content))

    def test_APIOrgMembers(self):
        
        retUsers = []
        retUsers.append({'id': self.testUser.pk,
                             'firstName': self.testUser.firstName,
                             'lastName': self.testUser.lastName})
        
        responses = {'users': retUsers, 'error': None}
        response = self.client.get(APP_URL + '/API/orgUsers/2',
                                   content_type = "application/json")
        self.assertEqual(responses, json.loads(response.content))
    
    def test_APIOrgsPost(self):
        self.testUser2 = UserData.createUser('Test',
                                             'Tester', 
                                       'testUSER2@gi.com', 'pw')
        self.testUser2.apiKey = 'TESTAPIKEY4'
        self.testUser2.save()
        self.client2 = Client()
        log = self.client2.login(username='testUSER2@gi.com',
                          password='pw')
        s = self.client2.session
        s['swag2'] = 59
        s.save()
        
        postData = json.dumps({'orgName': 'Swag org'})
        """responses = {'org': {'orgID': 18, 'orgName': 'Swag org',
                'status': 1},
                             'error': None}"""
        
        
        response = self.client2.post(APP_URL + '/API/orgs',
                                     postData, 
                                   content_type = "application/json")
        
        self.assertEqual(json.loads(response.content)['error'], None)

    
    def test_APIJoinOrg(self):
        self.testUser3 = UserData.createUser('Test',
                                             'Tester', 
                                       'testUSER3@gi.com', 'pw')
        self.testUser3.apiKey = 'TESTAPIKEY5'
        self.testUser3.save()
        self.client3 = Client()
        log = self.client3.login(username='testUSER3@gi.com',
                          password='pw')
        s = self.client3.session
        s['swag3'] = 60
        s.save()
        
        postData = json.dumps({'orgName': 'Test org'})
        
        response = self.client3.post(APP_URL + '/API/associateUser',
                                     postData, 
                                   content_type = "application/json")
        
        responses = {'org': {'orgID': 2, 'orgName': 'Test org',
                'status': 1}, 'error': None}
        
        self.assertEqual(responses, json.loads(response.content))

        

        