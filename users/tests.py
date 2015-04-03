# Authors: Jay Kong, Noah Gold

from django.test import TestCase
from models import UserData, ContactMethodData
from orgs.models import OrgData
from data_ex import ContactMethod, UserPCM


class UserPCM_test(TestCase):

    def setUp(self):
        pass

    def teardown(self):
        pass

    def testToDict(self):
        method = ContactMethod(0, 'type', 'data', 0, 0, 'title')
        user = UserPCM('test', 'user', 1, [method], 1, 'TESTAPIKEY', 0)
        userDict = {'firstName': 'test', 'lastName': 'user',
                    'status': 1, 'orgID': 1, 'contactMethods': [
                        {'user': 0, 'contactType': 'type',
                         'contactData': 'data', 'priority': 0,
                         'contactMethodID': 0, 'title': 'title'}],
                         'apiKey': 'TESTAPIKEY', 'user': 0}
        self.assertDictEqual(userDict, user.toDict())

    def testToDictNoContactMethod(self):
        user = UserPCM('test', 'user', 1, [], 1, 'TESTAPIKEY', 0)
        userDict = {'firstName': 'test', 'lastName': 'user',
                    'status': 1, 'orgID': 1, 'contactMethods': [],
                    'apiKey': 'TESTAPIKEY', 'user': 0}
        self.assertDictEqual(userDict, user.toDict())

    def testFromDict(self):
        method = ContactMethod(0, 'type', 'data', 0, 0, 'title')
        user = UserPCM('test', 'user', 1, [method], 1, 'TESTAPIKEY', 0)
        userDict = {'firstName': 'test', 'lastName': 'user',
                    'status': 1, 'orgID': 1, 'contactMethods': [
                        {'user': 0, 'contactType': 'type',
                         'contactData': 'data', 'priority': 0,
                         'contactMethodID': 0, 'title': 'title'}],
                         'apiKey': 'TESTAPIKEY', 'user': 0}
        otherUser = UserPCM.fromDict(userDict)
        self.assertDictEqual(user.toDict(), otherUser.toDict())

    def testPriority(self):
        method0 = ContactMethod(0, 'type', 'data', 0, 0, None)
        method1 = ContactMethod(0, 'type1', 'data1', 1, 0, None)
        method2 = ContactMethod(0, 'type2', 'data2', 2, 0, None)
        user = UserPCM('test', 'user', 1, 
                       [method1, method2, method0], 1,'TESTAPIKEY', 0)
        userDict = {'firstName': 'test', 'lastName': 'user',
                    'status': 1, 'orgID': 1, 'contactMethods': [
                        {'user': 0, 'contactType': 'type',
                         'contactData': 'data', 'priority': 0,
                         'contactMethodID': 0, 'title': None}, 
                        {'user': 0, 'contactType': 'type1',
                         'contactData': 'data1', 'priority': 1,
                         'contactMethodID': 0, 'title': None}, 
                        {'user': 0, 'contactType': 'type2',
                         'contactData': 'data2', 'priority': 2,
                         'contactMethodID': 0, 'title': None}], 
                         'apiKey': 'TESTAPIKEY', 'user': 0}
        self.assertDictEqual(userDict, user.toDict())

    def testPriority2(self):
        method0 = ContactMethod(0, 'type', 'data', 0, 0, None)
        method1 = ContactMethod(0, 'type1', 'data1', 1, 0, None)
        user = UserPCM('test', 'user', 1, [method1, method0], 1,'TESTAPIKEY', 0)
        userDict = {'firstName': 'test', 'lastName': 'user',
                    'status': 1, 'orgID': 1, 'contactMethods': [
                        {'user': 0, 'contactType': 'type',
                         'contactData': 'data', 'priority': 0,
                         'contactMethodID': 0, 'title': None}, 
                        {'user': 0, 'contactType': 'type1',
                         'contactData': 'data1', 'priority': 1,
                         'contactMethodID': 0, 'title': None}], 
                         'apiKey': 'TESTAPIKEY', 'user': 0}
        otherUser = UserPCM.fromDict(userDict)
        self.assertDictEqual(user.toDict(), otherUser.toDict())

class ContactMethod_test(TestCase):

    def setUp(self):
        pass

    def teardown(self):
        pass

    def testToDict(self):
        method = ContactMethod(0, 'type', 'data', 0, 0, None)
        methodDict = {'user': 0,
                      'contactType': 'type',
                      'contactData': 'data',
                      'priority': 0,
                      'title': None,
                      'contactMethodID': 0}
        self.assertDictEqual(methodDict, method.toDict())

    def testFromDict(self):
        method = ContactMethod(0, 'type', 'data', 0, 0, None)
        methodDict = {'user': 0,
                      'contactType': 'type',
                      'contactData': 'data',
                      'priority': 0,
                      'title': None,
                      'contactMethodID': 0}
        otherMethod = ContactMethod.fromDict(methodDict)
        self.assertDictEqual(method.toDict(), otherMethod.toDict())


class UserData_test(TestCase):

    def setUp(self):
        pass

    def teardown(self):
        pass

    def testToUserPCM(self):
        testOrg = OrgData(orgName='Test org',
                          status=1)
        testOrg.save()
        testUser = UserData.createUser('Test', 'Tester', 
                                       'test@test.com', 'pw')
        testUser.org = testOrg
        testUser.apiKey = 'TESTAPIKEY'
        testUser.save()
        testContactMethod = ContactMethodData(user=testUser,
                                              contactType='email',
                                              contactData='test@test.com',
                                              priority=0)
        testContactMethod.save()
        userDict = {'firstName': 'Test', 'lastName': 'Tester',
                    'status': 1, 'orgID': testOrg.pk, 'contactMethods': [
                        {'user': testUser.pk, 'contactType': 'email',
                         'contactData': 'test@test.com', 'priority': 0,
                         'title': None, 'contactMethodID': testContactMethod.pk
                         }], 'apiKey': 'TESTAPIKEY', 'user': testUser.pk}
        self.assertDictEqual(testUser.toUserPCM().toDict(), userDict)
