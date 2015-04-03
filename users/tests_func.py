#author Eric Jan

from django.test import TestCase, LiveServerTestCase
import os
import json
import requests
from django.contrib.auth.decorators import login_required
import json
from pageitforward.utils import createErrorDict
from models import UserData, ContactMethodData
from pageitforward.utils import createErrorDict, StatusCode, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.test.client import Client
from django.contrib.auth.models import User
from orgs.models import OrgData


APP_URL = os.environ['APP_URL']

class UserAPI_Test(LiveServerTestCase):
    
    def setUp(self):
        testOrg = OrgData(orgName='Test org',
                          status=1)
        testOrg.pk = 9
        testOrg.save()
      
        self.testUser = UserData.createUser('Test', 'Tester', 
                                       'testu@gi.com', 'pw')
        self.testUser.org = testOrg
        self.testUser.apiKey = 'TESTAPIKEY8'
        self.testUser.save()

        self.hierarchy = '{"numLevels":1,"levels":{"0":{"timeout":30,\
                    "users":[' + str(self.testUser.pk) + ']}}}'
        
        testContactMethod = ContactMethodData(user=self.testUser,
                                              contactType='email',
                                              contactData='testu@gi.com',
                                              priority=0)
        testContactMethod.pk = 7
        testContactMethod.save()
       

        self.client = Client()

        log = self.client.login(username='testu@gi.com',
                          password='pw')
        s = self.client.session
        s['swag'] = 41
        s.save()

        
    def tearDowm(self):
        pass
    
    def test_APILoginStatus(self):
        userPCM = self.testUser.toUserPCM().toDict()

        responses = {'loggedIn': True, 'userPCM': userPCM}
        
        response = self.client.get(APP_URL + '/API/loginStatus',
                                   content_type = "application/json")
        
        self.assertEqual(responses, json.loads(response.content))
    
    
    def test_APIContactMethodUpdateDelete_POST(self):
        
        postData = json.dumps({ 'contactType':'email',
                               'contactData':'cccc@gi.com',
                               'priority':0,
                               'title':'swagger'})
        response = self.client.post(APP_URL + '/API/contactmethods/7',
                                    postData,
                                    content_type = "application/json")

        responses = {'success': True, 'error': None}
        
        self.assertEqual(responses, json.loads(response.content))
        
        
    def test_APIContactMethodUpdateDelete_DEL(self):
        response = self.client.delete(APP_URL + '/API/contactmethods/7',
                                      content_type = "application/json")
        responses = {'success': True, 'error': None}
        self.assertEqual(responses, json.loads(response.content))

    def test_APIContactMethods_GET(self):
        response = self.client.get(APP_URL + '/API/contactmethods',
                                   content_type = "application/json")
        
        userPCM = self.testUser.toUserPCM()
        
        contactMethods = [method.toDict() for method in userPCM.contactMethods]
        responses = {'contactMethods': contactMethods,
                     'error': None}
        
        self.assertEqual(responses,
                         json.loads(response.content))
        
    def test_APIContactMethods_POST(self):
        responses = {'success': True, 'error': None}
        
        postData = json.dumps({'contactType':'email',
                               'contactData':'ccc@gi.com',
                               'title':'prez', 'priority': 4})
        
        response = self.client.post(APP_URL + '/API/contactmethods',
                                    postData, content_type = "application/json")

        self.assertEqual(responses, json.loads(response.content))
        
    def test_APILogin(self):
        self.testUserL = UserData.createUser('Test', 'Tester', 
                                       'testul@gi.com', 'pw')
        self.testUserL.apiKey = 'TESTAPIKEY9'
        self.testUserL.save()
        
        testContactMethod = ContactMethodData(user=self.testUserL,
                                              contactType='email',
                                              contactData='testul@gi.com',
                                              priority=0)
        testContactMethod.pk = 11
        testContactMethod.save()
        
        userPCMDict = self.testUserL.toUserPCM().toDict()

        postData = json.dumps({'username':'testul@gi.com',
                               'password':'pw'})
        
        response = self.client.post(APP_URL + '/API/login',
                                    postData, content_type = "application/json")
    
        responses = {'userPCM': userPCMDict,
                     'error': None}

        self.assertEqual(responses, json.loads(response.content))
        
    def test_APILogout(self):
        responses = {'success': True, 'error': None}
        
        response = self.client.post(APP_URL + '/API/logout',
                                    content_type = "application/json")
        
        self.assertEqual(responses, json.loads(response.content))
        
    def test_APIUsers(self):
        postData = json.dumps({'firstName': 'w',
                               'lastName':'ww',
                               'email': 'ff@gg.com',
                               'password':'pw'})
        
        response = self.client.post(APP_URL + '/API/users',
                                    postData,
                                    content_type = "application/json")
        
        self.assertEqual(json.loads(response.content)['error'], None)

