# Author: Noah Gold Jonathan Ma Feiyang Xue

from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from django.test import TestCase, LiveServerTestCase
from pageitforward.utils import StatusCode
from models import UserData
from orgs.models import OrgData
from eventhandlers.models import EventHandlerData


class AppFuncs:
    """
    Abstracts app functionality into functions which assert that
    the functions called succeeded.

    All functions take a fake self, which is a LiveServerTestCase
    object.
    """

    @staticmethod
    def doLogin(self, email, pw):
        self.sel.get(self.live_server_url)
        self.sel.execute_script('window.sessionStorage.clear();')
        self.sel.execute_script('window.localStorage.clear();')


        # try:
        #     # self.sel.save_screenshot("log0.png")
        #     logout = WebDriverWait(self.sel, 2).until(
        #         EC.element_to_be_clickable((By.ID, 'navLogout')))
        #     logout = self.sel.find_element_by_id('navLogout')
        #     logout.click()
        #     logout.click()
        #     logout.click()
        #     self.sel.save_screenshot("log0.png")
        # except:
        #     self.assertTrue(
        #         False,
        #         'Login failed. Unable to find logout element.')
        #
        # self.sel.save_screenshot("log0.png")

        login = WebDriverWait(self.sel, 2).until(
                    EC.element_to_be_clickable((By.ID, 'navLoginEmail')))


        emailBox = self.sel.find_element_by_id('navLoginEmail')
        pwBox = self.sel.find_element_by_id('navLoginPassword')
        submitBtn = self.sel.find_element_by_id('navLoginSubmit')

        emailBox.send_keys(email)
        pwBox.send_keys(pw)

        submitBtn.click()
        self.sel.save_screenshot("Login01.png")
        dropDowns = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'mainDrop')))

        dropData = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'dropData')))
        dropData.click()
        self.sel.save_screenshot("login02.png")

        try:
            logout = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, 'navLogout')))
            # self.sel.save_screenshot("log1.png")
        except:
            self.assertTrue(
                False,
                'Login failed. Unable to find logout element.')

    @staticmethod
    def doLogout(self):
        try:
            self.sel.save_screenshot("logout01.png")
            logout = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, 'navLogout')))
            self.sel.execute_script('window.sessionStorage.clear();')
            self.sel.execute_script('window.localStorage.clear();')
            logout.click()

            try:
                login = WebDriverWait(self.sel, 2).until(
                    EC.element_to_be_clickable((By.ID, 'navLoginEmail')))
                self.sel.save_screenshot("logout02.png")
            except:
                self.assertTrue(
                    False,
                    'Logout failed. Unable to find login email element.')
        except:
            self.assertTrue(False, 'Unable to find logout element.')


class LoginLogout_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user
        self.user = UserData.createUser('firstName', 'lastName',
                                        'user1@example.com', 'pw')

    def tearDown(self):
        self.sel.quit()

    def testLogin(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')

    def testLogout(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        AppFuncs.doLogout(self)


class RegisterUser_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

    def tearDown(self):
        self.sel.quit()

    def testRegister(self):
        self.doReg(self)

    @staticmethod
    def doReg(self):
        self.sel.get(self.live_server_url)
        signUp = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "signUp")))
        # signUp = self.sel.find_element_by_id('signUp')
        signUp.click()

        self.sel.save_screenshot("register01.png")

        emailBox = self.sel.find_element_by_id('email')
        firstNameBox = self.sel.find_element_by_id('name')
        lastNameBox = self.sel.find_element_by_id('username')
        passwordBox = self.sel.find_element_by_id('password')
        passwordConfirmBox = self.sel.find_element_by_id('password_c')
        submitBtn = self.sel.find_element_by_id('regUserSubmit')

        emailBox.send_keys('user@example.com')
        firstNameBox.send_keys('John')
        lastNameBox.send_keys('Doe')
        passwordBox.send_keys('pw')
        passwordConfirmBox.send_keys('pw')
        self.sel.save_screenshot("register02.png")
        submitBtn.click()

        #self.sel.save_screenshot("IHaveTo.png")
        try:

            dropData = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'dropData')))
            self.sel.save_screenshot("register03.png")
            dropData.click()
            logout = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, 'navLogout')))
            AppFuncs.doLogout(self)
        except:
            AppFuncs.doLogout(self)
            self.assertTrue(
                False,
                'Reg failed. Unable to find logout element.')


class findEventViews_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user and an org
        self.user = UserData.createUser('firstName', 'lastName','user1@example.com', 'pw')

        self.user.org = OrgData.createOrg("theOrg")
        self.user.save()

    def tearDown(self):
        self.sel.quit()

    def testEventView(self):
        self.doFindEvent(self)


    @staticmethod
    def doFindEvent(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        # toEvent = WebDriverWait(self.sel, 20).until(
        #         EC.element_to_be_clickable((By.ID, "gotoEvent")))
        # toEvent.click()
        dropData = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'eventDrop')))
        dropData.click()
        toEvent = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "gotoEvent")))
        self.sel.save_screenshot("findEvent01.png")
        toEvent.click()
        try:
            self.sel.save_screenshot("findEvent02.png")
            createNewEventBtn = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, 'CreateNewEvent')))
        except:
            dropData = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'dropData')))
            dropData.click()
            AppFuncs.doLogout(self)
            self.assertTrue(
                False,
                'Switch view failed.')

        dropData = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'eventDrop')))
        self.sel.save_screenshot("findEvent03.png")
        dropData.click()
        toHandler = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "CreateEventHandler")))
        self.sel.save_screenshot("findEvent04.png")
        toHandler.click()
        try:
            createNewHandlerBtn = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, 'createNewHandler')))
        except:
            dropData = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'dropData')))
            dropData.click()
            AppFuncs.doLogout(self)
            self.assertTrue(
                False,
                'Switch view failed.')
        self.sel.save_screenshot("findEvent05.png")
        dropData = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'dropData')))
        self.sel.save_screenshot("findEvent06.png")
        dropData.click()
        AppFuncs.doLogout(self)


class RealAssociate_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user and an org
        self.user = UserData.createUser('firstName', 'lastName','user1@example.com', 'pw')
        OrgData.createOrg("theOrg")

    def tearDown(self):
        self.sel.quit()

    def testAssociateOrg(self):
        self.doRealAssociate(self)

    @staticmethod
    def doRealAssociate(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        #self.sel.save_screenshot("log5.png")

        associateOrgBtn = self.sel.find_element_by_id('associateBu')
        self.sel.save_screenshot("associate01.png")
        associateOrgBtn.click()
        try:
            # self.sel.save_screenshot("log5.png")
            orgBox = WebDriverWait(self.sel, 20).until(
                EC.visibility_of_element_located((By.ID, 'inputOrgName')))
            submitOrgBtn = self.sel.find_element_by_id('submitAssociate')

            orgBox.send_keys('theOrg')
            self.sel.save_screenshot("associate02.png")
            submitOrgBtn.click()
            try:
                org = WebDriverWait(self.sel, 20).until(
                    EC.text_to_be_present_in_element((By.ID, 'userOrgName'), 'theOrg'))

                try:
                    self.sel.save_screenshot("associate03.png")
                    dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
                    dropData.click()
                    logout = WebDriverWait(self.sel, 20).until(
                                EC.element_to_be_clickable((By.ID, 'navLogout')))
                    self.sel.save_screenshot("associate04.png")
                    AppFuncs.doLogout(self)
                    # self.sel.save_screenshot("log7.png")
                except:
                    self.assertTrue(
                        False,
                        'Login failed. Unable to find logout element.')
            except:
                dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
                dropData.click()
                AppFuncs.doLogout(self)
                self.assertTrue(
                    False,
                    'Unable to associate org.')
        except:
            dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
            dropData.click()
            AppFuncs.doLogout(self)
            self.assertTrue(
                False,
                'Cannnot find orgName Button.')


class CreateOrg_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user
        self.user = UserData.createUser('firstName', 'lastName',
                                        'user1@example.com', 'pw')

    def tearDown(self):
        self.sel.quit()

    def testCreateOrg(self):
        self.doCreateOrg(self)

    @staticmethod
    def doCreateOrg(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        # print 'logged in'
        settingBtn = self.sel.find_element_by_id('settings')
        self.sel.save_screenshot("createOrg01.png")
        settingBtn.click()
        #self.sel.save_screenshot("log7.png")
        createNewOrgBtn = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'createNewOrg')))
        self.sel.save_screenshot("createOrg02.png")
        createNewOrgBtn.click()
        try:
            # print 'waiting for org box'
            orgBox = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'inputOrgName')))
            # print 'got org box'
            
            submitOrgBtn = self.sel.find_element_by_id('submitAssociate')

            # print 'enter keys'
            orgBox.send_keys('org1')
            self.sel.save_screenshot("createOrg03.png")
            submitOrgBtn.click()
            try:
                org = WebDriverWait(self.sel, 2).until(
                    EC.text_to_be_present_in_element((By.ID, 'userOrgName'), 'org1'))
                self.sel.save_screenshot("createOrg04.png")
                dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
                dropData.click()
                AppFuncs.doLogout(self)
                # print 'logout done'
            except:
                # problem can arise here
                AppFuncs.doLogout(self)
                self.assertTrue(
                    False,
                    'Unable to associate org.')
        except:
            dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
            dropData.click()
            AppFuncs.doLogout(self)
            self.assertTrue(
                False,
                'Cannnot find orgName Button.')

class AddContactMethod_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user
        self.user = UserData.createUser('firstName', 'lastName',
                                        'user1@example.com', 'pw')

    def tearDown(self):
        self.sel.quit()

    def testCreateContactMethod(self):
        self.doCreateContactMethod(self)

    @staticmethod
    def doCreateContactMethod(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        settingsBtn = self.sel.find_element_by_id('settings')
        settingsBtn.click()
        self.sel.save_screenshot("createContact01.png")
        try:
            #self.sel.save_screenshot("createContact02.png")
            createBox = WebDriverWait(self.sel, 2).until(
                EC.visibility_of_element_located((By.ID, 'createNewBtn')))
            createNew = self.sel.find_element_by_id('createNewBtn')
            createNew.click()
            try:
                self.sel.save_screenshot("createContact02.png")
                createBox = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'contactType')))
                dropdown = Select(self.sel.find_element_by_id("contactType"))
                dropdown.select_by_value("sms")

                contactData = self.sel.find_element_by_id('contactData')
                contactTitle = self.sel.find_element_by_id('title')
                contactPriority = self.sel.find_element_by_id('priority')
                submitBtn = self.sel.find_element_by_id('submitBtnCreate')

                contactData.send_keys('6262516801')
                contactTitle.send_keys('cell')
                contactPriority.send_keys('1')
                self.sel.save_screenshot("createContact03.png")
                submitBtn.click()
                self.sel.save_screenshot("logS.png")
                dropData = WebDriverWait(self.sel, 2).until(
                                    EC.visibility_of_element_located((By.ID, 'dropData')))
                dropData.click()
                self.sel.save_screenshot("createContact04.png")

                settingsBtn = self.sel.find_element_by_id('settings')
                settingsBtn.click()

                try:
                    contactConfirm = WebDriverWait(self.sel, 2).until(
                                        EC.visibility_of_element_located((By.ID, 'contact1')))
                    self.sel.save_screenshot("createContact05.png")
                    dropData = WebDriverWait(self.sel, 2).until(
                                    EC.visibility_of_element_located((By.ID, 'dropData')))
                    dropData.click()
                    AppFuncs.doLogout(self)
                except:
                    dropData = WebDriverWait(self.sel, 2).until(
                                    EC.visibility_of_element_located((By.ID, 'dropData')))
                    dropData.click()
                    AppFuncs.doLogout(self)
                    self.assertTrue(False, 'Could not find created contact method.')

            except:
                dropData = WebDriverWait(self.sel, 2).until(
                                    EC.visibility_of_element_located((By.ID, 'dropData')))
                dropData.click()
                AppFuncs.doLogout(self)
                self.assertTrue(False, 'Could not get into create new contact page')
        except:
            dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
            dropData.click()
            AppFuncs.doLogout(self)
            self.assertTrue(False, 'Could not get into settings page')




class CreateEventHandler_test(LiveServerTestCase):

    def setUp(self):
        self.sel = WebDriver()

        # Create a user and an org
        self.user = UserData.createUser('a', 'b','c@1', 'pw')
        theOrg = OrgData.createOrg("theOrg")
        self.user.org = theOrg
        self.user.save()
        self.user = UserData.createUser('d', 'e','f@1', 'pw')
        self.user.org = theOrg
        self.user.save()


    def tearDown(self):
        self.sel.quit()

    def testCreateEventHandler(self):
        self.doCreateEventHandler(self)

    @staticmethod
    def doCreateEventHandler(self):
        AppFuncs.doLogin(self, self.user.email, 'pw')
        self.sel.save_screenshot("log6.png")


        dropData = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'eventDrop')))
        self.sel.save_screenshot("createHandler01.png")
        dropData.click()
        toHandler = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "CreateEventHandler")))
        self.sel.save_screenshot("createHandler02.png")
        toHandler.click()
        createHandler = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "createNewHandler")))
        self.sel.save_screenshot("createHandler03.png")
        createHandler.click()
        # try:
        userSelect = Select(WebDriverWait(self.sel, 2).until(
                                    EC.visibility_of_element_located((By.ID, 'userSelector'))))
        # userSelect.select_by_value("a b")
        # this should be "a b", I am not sure my the method above does not work.
        userSelect.select_by_index(1)

        handlerTitle = self.sel.find_element_by_id('titleIn')
        timeAck = self.sel.find_element_by_id('timeForAck')
        handlerTitle.send_keys('testHandler')
        timeAck.send_keys('256')

        addNew = self.sel.find_element_by_id('addUser')
        self.sel.save_screenshot("createHandler04.png")
        addNew.click()


        handlerCreateBtn = WebDriverWait(self.sel, 2).until(
                EC.element_to_be_clickable((By.ID, "createHierarchy")))
        self.sel.save_screenshot("createHandler05.png")
        handlerCreateBtn.click()

        successful = WebDriverWait(self.sel, 2).until(
                    EC.visibility_of_element_located((By.ID, 'eventHandlerCreateSuccess')))
        self.sel.save_screenshot("createHandler06.png")
        # except:
        #     dropData = WebDriverWait(self.sel, 2).until(
        #                         EC.visibility_of_element_located((By.ID, 'dropData')))
        #     dropData.click()
        #     AppFuncs.doLogout(self)
        #     self.assertTrue(False, "Cannot find another user or cannot create handler.")

        dropData = WebDriverWait(self.sel, 2).until(
                                EC.visibility_of_element_located((By.ID, 'dropData')))
        dropData.click()
        self.sel.save_screenshot("log5.png")
        AppFuncs.doLogout(self)























