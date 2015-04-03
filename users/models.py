# Author: Jay Kong, Noah Gold, Jaspreet Singh

from django.db import models
from orgs.models import OrgData
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from users.data_ex import ContactMethod, UserPCM
from uuid import uuid4
from pageitforward.utils import StatusCode
import json


class CustomUserManager(BaseUserManager):

    def create_user(self, firstName, lastName, email, password=None):
        user = self.model(firstName=firstName, lastName=lastName, email=email)
        user.set_password(password)
        user.apiKey = str(uuid4())
        user.save(using=self.db)
        return user

    def create_superuser(self, firstName, lastName, email, password=None):
        user = self.create_user(firstName, lastName, email, password)
        user.is_superuser = True
        user.save(using=self.db)
        return user


class UserData(AbstractBaseUser, PermissionsMixin):

    email = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = CustomUserManager()
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    status = models.IntegerField(default=StatusCode.ACTIVE)
    org = models.ForeignKey(OrgData, null=True, blank=True)
    apiKey = models.CharField(max_length=255, unique=True)

    def get_full_name(self):
        """
        Returns the person's full name.
        """
        return '%s %s' % (self.firstName, self.lastName)

    def get_short_name(self):
        """
        Returns person's first name
        """
        return self.firstName

    @property
    def is_staff(self):
        return self.is_superuser

    def __unicode__(self):
        return str(self.id)

    def toUserPCM(self):
        """
        Converts UserData object to a UserPCM object
        """
        methodObjects = self.contactmethoddata_set.all()
        methods = []
        for method in methodObjects:
            methods.append(method.toContactMethod())

        orgID = self.org.pk if self.org is not None else -1
        return UserPCM(self.firstName, self.lastName, self.status, methods,
                       orgID, self.apiKey, self.pk)

    @staticmethod
    def createUser(firstName, lastName, email, password):
        """
        Creates a new user and returns it.

        Args:
            firstName (str): first name
            lastName (str): last name
            email (str): email
            password (str): password
        """
        newUser = UserData.objects.create_user(firstName, lastName,
                                               email, password)
        return newUser


class ContactMethodData(models.Model):
    user = models.ForeignKey(UserData)
    contactType = models.CharField(max_length=50)
    contactData = models.CharField(max_length=255)
    priority = models.IntegerField()
    title = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (('user', 'priority'),)

    def __unicode__(self):
        return str(self.id)

    def toContactMethod(self):
        """
        Converts ContactMethodData object to a ContactMethod object
        """
        return ContactMethod(self.user.pk, self.contactType,
                             self.contactData, self.priority,
                             self.pk, self.title)
