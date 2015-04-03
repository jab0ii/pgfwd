# Authors: Jay Kong, Noah Gold

from django.test import TestCase
from orgs.models import (OrgData, OrgAlreadyExistsException,
                         InvalidOrgNameException)


class OrgData_test(TestCase):

    def setUp(self):
        pass

    def teardown(self):
        pass

    def testDuplicateOrgName(self):
        OrgData.createOrg("Same")
        self.assertRaises(OrgAlreadyExistsException, OrgData.createOrg, "Same")

    def testEmptyOrgName(self):
        self.assertRaises(InvalidOrgNameException, OrgData.createOrg, "")
