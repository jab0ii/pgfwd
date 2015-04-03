# Author: Jay Kong, Noah Gold

from django.db import models
from pageitforward.utils import StatusCode


class OrgAlreadyExistsException:
    pass


class InvalidOrgNameException:
    pass


class OrgData(models.Model):
    orgName = models.CharField(max_length=255)
    status = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    def toDict(self):
        """
        Converts OrgData to a dict.
        """
        return {'orgID': self.pk, 'orgName': self.orgName,
                'status': self.status}


    @staticmethod
    def createOrg(orgName):
        """
        Given an org name, create this org in database and returns it.
        Raises OrgAlreadyExistsException if it already exists.

        Args:
            orgName (str): the name of new org

        Returns:
            {'orgName': str,
             'uuid': str,
             'status': int,
             'error': Error object}
        """
        if len(orgName) <= 0:
            raise InvalidOrgNameException()

        existingOrgs = OrgData.objects.filter(orgName=orgName)
        if existingOrgs.count() > 0:
            raise OrgAlreadyExistsException()

        org = OrgData()
        org.orgName = orgName
        org.status = StatusCode.ACTIVE
        org.save()
        return org
