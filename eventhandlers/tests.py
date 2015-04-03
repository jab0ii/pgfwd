# Author: Jay Kong

from django.test import TestCase
from models import (EventHandlerData, HierarchyLevelDoesNotExist,
                    HierarchyExhausted)
from users.models import UserData, ContactMethodData
from orgs.models import OrgData


class EventHandlerData_test(TestCase):
    def setUp(self):
        pass

    def teardown(self):
        pass

    def generateTestData(self):
        testOrg = OrgData(orgName='Test org',
                          status=1)
        testOrg.save()
        testUser = UserData.createUser('Test', 'Tester', 'test@test.com', 'pw')
        testUser.org = testOrg
        testUser.apiKey = 'TESTAPIKEY'
        testUser.save()
        testContactMethod = ContactMethodData(user=testUser,
                                              contactType='email',
                                              contactData='test@test.com',
                                              priority=0)
        testContactMethod.save()
        hierarchy = '{"numLevels":1,"levels":{"0":{"timeout":30,\
                     "users":[' + str(testUser.pk) + ']}}}'
        newHandler = EventHandlerData(title='TestHandler',
                                      hierarchy=hierarchy,
                                      org=testOrg)
        newHandler.save()
        return newHandler, testUser

    def testGetUserPCMOfLevel(self):
        newHandler, testUser = self.generateTestData()
        testUserPCM = newHandler.getUserPCMOfLevel(0)[0]
        self.assertDictEqual(testUserPCM.toDict(), 
                             testUser.toUserPCM().toDict())

    def testGetUserPCMOfLevelError(self):
        newHandler, testUser = self.generateTestData()
        self.assertRaises(HierarchyExhausted,
                          newHandler.getUserPCMOfLevel, 1)

    def testGetEscalateTimeOfLevel(self):
        newHandler, testUser = self.generateTestData()
        time = newHandler.getEscalateTimeOfLevel(0)
        self.assertEqual(time, 30)

    def testGetEscalateTimeOfLevelError(self):
        newHandler, testUser = self.generateTestData()
        self.assertRaises(HierarchyLevelDoesNotExist,
                          newHandler.getEscalateTimeOfLevel, 1)
